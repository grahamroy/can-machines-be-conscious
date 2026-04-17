"""
ising_model.py
--------------
Companion script for "Consciousness on a Spectrum" --- Part 6 of the
'Can Machines Be Conscious?' series.

A 2D Ising model Monte Carlo simulation on a 50x50 lattice, run at three
temperatures: below, at, and above the critical point T_c = 2/ln(1+sqrt(2))
approximately 2.269. Onsager's exact result.

The point of the script is illustrative, not probative. It is an analogy
for the combination problem in panpsychism: local interactions among many
micro-components can yield a qualitatively new macroscopic property
(a magnetisation) through a phase transition. It does not follow that
consciousness works the same way. It follows that nature has at least
one mechanism by which macro-properties can emerge from micro-rules.
"""

from __future__ import annotations

import math
import time

import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# Constants and reproducibility
# ------------------------------------------------------------
L = 50                              # lattice side length
N_SITES = L * L
T_C = 2.0 / math.log(1.0 + math.sqrt(2.0))   # Onsager's critical temperature

RNG = np.random.default_rng(20260417)


# ------------------------------------------------------------
# Core Metropolis sweep
# ------------------------------------------------------------
def metropolis_sweep(spins: np.ndarray, beta: float, n_flips: int) -> None:
    """
    Perform n_flips single-spin Metropolis updates on the lattice in place.
    Periodic boundary conditions.
    """
    # Pre-sample all random choices for speed.
    xs = RNG.integers(0, L, size=n_flips)
    ys = RNG.integers(0, L, size=n_flips)
    us = RNG.random(size=n_flips)

    for k in range(n_flips):
        i = xs[k]
        j = ys[k]
        s = spins[i, j]
        nb = (spins[(i + 1) % L, j]
              + spins[(i - 1) % L, j]
              + spins[i, (j + 1) % L]
              + spins[i, (j - 1) % L])
        dE = 2.0 * s * nb
        if dE <= 0.0 or us[k] < math.exp(-beta * dE):
            spins[i, j] = -s


def magnetisation(spins: np.ndarray) -> float:
    return float(np.mean(spins))


# ------------------------------------------------------------
# Run a single temperature and track equilibration
# ------------------------------------------------------------
def run_temperature(T: float,
                    n_equil_sweeps: int = 400,
                    n_measure_sweeps: int = 200,
                    random_start: bool = True) -> dict:
    """
    Run the Ising model at temperature T.  One "sweep" is N_SITES single-spin
    updates.  Returns a dict with the final state, mean |M|, and the step at
    which the rolling magnetisation first stabilised.
    """
    beta = 1.0 / T
    if random_start:
        spins = RNG.choice([-1, 1], size=(L, L)).astype(np.int8)
    else:
        spins = np.ones((L, L), dtype=np.int8)

    mag_history = []

    # Equilibration phase
    equil_step = None
    rolling_window = 20
    tol = 0.02
    for sweep in range(n_equil_sweeps):
        metropolis_sweep(spins, beta, N_SITES)
        mag_history.append(abs(magnetisation(spins)))
        if equil_step is None and len(mag_history) >= 2 * rolling_window:
            recent = np.array(mag_history[-rolling_window:])
            prev = np.array(mag_history[-2 * rolling_window:-rolling_window])
            if abs(recent.mean() - prev.mean()) < tol:
                equil_step = sweep

    # Measurement phase
    measurements = []
    for _ in range(n_measure_sweeps):
        metropolis_sweep(spins, beta, N_SITES)
        measurements.append(abs(magnetisation(spins)))

    if equil_step is None:
        equil_step = n_equil_sweeps  # never equilibrated within budget

    return {
        "T": T,
        "spins": spins.copy(),
        "mean_abs_M": float(np.mean(measurements)),
        "std_abs_M": float(np.std(measurements)),
        "equil_sweep": equil_step,
    }


# ------------------------------------------------------------
# Main experiment: three temperatures + a sweep curve
# ------------------------------------------------------------
def main() -> None:
    start = time.time()

    print(f"2D Ising model, L = {L}, critical T_c = {T_C:.4f}")
    print("-" * 60)

    phase_points = [
        ("ordered",   1.5),
        ("critical",  T_C),
        ("disordered", 3.5),
    ]
    phase_results = []
    for name, T in phase_points:
        res = run_temperature(T, n_equil_sweeps=500, n_measure_sweeps=200)
        res["name"] = name
        phase_results.append(res)
        print(f"  T = {T:5.3f} ({name:10s})  "
              f"<|M|> = {res['mean_abs_M']:.3f} +/- {res['std_abs_M']:.3f}  "
              f"equilibration at sweep ~{res['equil_sweep']}")

    # Magnetisation curve across a range of T.
    # Start from an aligned configuration so that sub-critical runs don't get
    # trapped in domain walls within the finite sweep budget.  Physically this
    # is just choosing which of the two symmetry-broken states the system
    # settles into; it does not bias the measured |M|.
    print("\nSweeping T in [1.5, 3.5] for the |M|(T) curve...")
    Ts = np.linspace(1.5, 3.5, 21)
    curve = []
    for T in Ts:
        res = run_temperature(T,
                              n_equil_sweeps=600,
                              n_measure_sweeps=200,
                              random_start=False)
        curve.append(res["mean_abs_M"])
        print(f"  T = {T:5.3f}   <|M|> = {res['mean_abs_M']:.3f}")

    # --------------------------------------------------------
    # Plot 1: three lattices side by side
    # --------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, res in zip(axes, phase_results):
        ax.imshow(res["spins"], cmap="gray", vmin=-1, vmax=1,
                  interpolation="nearest")
        ax.set_title(f"T = {res['T']:.3f}  ({res['name']})\n"
                     f"<|M|> = {res['mean_abs_M']:.2f}")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("2D Ising model: three regimes of the phase transition",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig("ising_phases.png", dpi=140)
    plt.close(fig)

    # --------------------------------------------------------
    # Plot 2: magnetisation vs temperature
    # --------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(Ts, curve, marker="o", color="black", linewidth=1.2)
    ax.axvline(T_C, color="tab:red", linestyle="--",
               label=f"T_c = {T_C:.3f} (Onsager)")
    ax.set_xlabel("Temperature T")
    ax.set_ylabel("Mean |M|")
    ax.set_title("Order parameter vs temperature (2D Ising)")
    ax.set_ylim(-0.02, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("ising_magnetization.png", dpi=140)
    plt.close(fig)

    elapsed = time.time() - start
    print("-" * 60)
    print(f"Wrote ising_phases.png and ising_magnetization.png")
    print(f"Elapsed: {elapsed:.1f} s")
    print()
    print("Phase transition summary:")
    print(f"  Below T_c (T = 1.5):    high |M| -- macroscopic order")
    print(f"  Near  T_c (T = {T_C:.3f}): critical fluctuations, |M| falling")
    print(f"  Above T_c (T = 3.5):    |M| ~ 0 -- disordered phase")


if __name__ == "__main__":
    main()
