"""
workspace_simulation.py

A minimal Global Workspace Theory simulation.

- Specialised modules produce signal strengths for a given stimulus.
- A workspace runs a winner-take-all competition with an ignition threshold.
- Above threshold, the winning module's content is broadcast to downstream
  consumers; below threshold, nothing is broadcast.
- Sweeping input strength from low to high reveals an S-shaped ignition
  curve -- the empirical signature Dehaene's Global Neuronal Workspace
  model predicts.

Run: python workspace_simulation.py
Produces: ignition_curve.png
"""

import numpy as np
import matplotlib.pyplot as plt


# ----- specialised modules -------------------------------------------------

MODULES = [
    "visual_cortex",
    "auditory",
    "semantic",
    "motor_planning",
    "working_memory",
    "verbal_report",
    "episodic_memory",
]

CONSUMERS = [
    "working_memory",
    "verbal_report",
    "motor_planning",
    "episodic_memory",
    "attention_control",
]

# affinity[i, j] = how relevant module i is to stimulus j (0..1)
STIMULI = ["object at 3 deg", "faint tone", "remembered word"]


def make_affinity(rng):
    n_mod = len(MODULES)
    n_stim = len(STIMULI)
    a = rng.uniform(0.0, 0.3, size=(n_mod, n_stim))
    # plant strong specialists
    a[MODULES.index("visual_cortex"), 0] = 0.85
    a[MODULES.index("semantic"), 0] = 0.50
    a[MODULES.index("auditory"), 1] = 0.70
    a[MODULES.index("semantic"), 1] = 0.30
    a[MODULES.index("episodic_memory"), 2] = 0.80
    a[MODULES.index("semantic"), 2] = 0.55
    return a


def module_strengths(affinity, stim_idx, input_gain, rng):
    """Per-module signal strength for a given stimulus at a given gain."""
    base = affinity[:, stim_idx] * input_gain
    noise = rng.normal(0.0, 0.08, size=base.shape)
    return np.clip(base + noise, 0.0, 1.0)


# ----- workspace competition -----------------------------------------------

IGNITION_THRESHOLD = 0.70


def workspace_step(strengths, threshold=IGNITION_THRESHOLD):
    """Winner-take-all with a hard ignition threshold.

    Returns (winner_index, broadcast_strength). If nothing exceeds the
    threshold, returns (-1, 0.0) -- preconscious processing, no ignition.
    """
    winner = int(np.argmax(strengths))
    top = float(strengths[winner])
    if top < threshold:
        return -1, 0.0
    return winner, top


def broadcast(winner, strength):
    if winner < 0:
        return {}
    return {c: (MODULES[winner], strength) for c in CONSUMERS}


# ----- ignition curve ------------------------------------------------------

def ignition_curve(affinity, stim_idx, gains, trials_per_gain, rng):
    """Frequency of ignition as a function of input gain."""
    freqs = []
    for g in gains:
        hits = 0
        for _ in range(trials_per_gain):
            s = module_strengths(affinity, stim_idx, g, rng)
            w, _ = workspace_step(s)
            if w >= 0:
                hits += 1
        freqs.append(hits / trials_per_gain)
    return np.array(freqs)


# ----- main ----------------------------------------------------------------

def main():
    rng = np.random.default_rng(7)
    affinity = make_affinity(rng)

    # 1. single illustrative tick
    stim_idx = 0
    strengths = module_strengths(affinity, stim_idx, input_gain=1.0, rng=rng)
    print(f'Module strengths on stimulus "{STIMULI[stim_idx]}":')
    for name, s in zip(MODULES, strengths):
        print(f"  {name:<16s} {s:.2f}")
    print()
    print(f"Ignition threshold: {IGNITION_THRESHOLD:.2f}")
    winner, top = workspace_step(strengths)
    if winner < 0:
        print("No ignition this tick (preconscious processing only).")
    else:
        print(f"Winner this tick: {MODULES[winner]} ({top:.2f})")
        cast = broadcast(winner, top)
        print("Broadcast to: " + ", ".join(cast.keys()))
    print()

    # 2. ignition curve (averaged across stimuli)
    gains = np.round(np.linspace(0.1, 1.3, 13), 2)
    trials = 400
    freqs = np.zeros_like(gains, dtype=float)
    for s_idx in range(len(STIMULI)):
        freqs += ignition_curve(affinity, s_idx, gains, trials, rng)
    freqs /= len(STIMULI)

    print("Ignition frequency vs input strength:")
    for g, f in zip(gains, freqs):
        print(f"  {g:.2f}: {int(round(100 * f)):3d}%")

    # 3. plot
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(gains, freqs, marker="o", linewidth=2, color="#1f4e79")
    ax.axhline(0.5, color="#bbbbbb", linestyle=":", linewidth=1)
    ax.axvline(IGNITION_THRESHOLD, color="#c44", linestyle="--",
               linewidth=1, label=f"threshold = {IGNITION_THRESHOLD:.2f}")
    ax.set_xlabel("input gain")
    ax.set_ylabel("P(ignition)")
    ax.set_title("Ignition curve: global broadcast vs input strength")
    ax.set_ylim(-0.02, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig("ignition_curve.png", dpi=140)
    print("\nSaved ignition_curve.png")


if __name__ == "__main__":
    main()
