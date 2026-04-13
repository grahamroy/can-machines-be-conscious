#!/usr/bin/env python3
"""
Predictive Processing: Your Brain as a Prediction Machine

Demonstrates the Free Energy Principle (Karl Friston) by building a minimal
hierarchical predictive processing agent. The agent maintains a two-level
belief hierarchy and minimises variational free energy to track a changing
sensory signal -- illustrating how prediction-error minimisation IS
approximate Bayesian inference.

Key ideas:
    - Conscious systems are hierarchical prediction machines (Friston, Clark, Hohwy)
    - Free energy F = prediction_error^2 / (2 * precision) + log(precision)
    - Minimising F is equivalent to gradient descent on a variational bound
    - Precision-weighting determines what surprises "count" (attention)
    - Hierarchy lets the system learn both fast dynamics AND slow context

Usage:
    python predictive_processing.py

Requires only numpy. No external libraries needed.
"""

import sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# MATHEMATICAL BACKGROUND  (Friston, 2010)
#
#   Variational free energy:  F = E_q[log q(s) - log p(o, s)]
#     q(s)    = approximate posterior (the agent's beliefs)
#     p(o, s) = generative model (joint over observations and hidden states)
#
#   Under Gaussian assumptions (Laplace approximation):
#     F ≈ error^2 / (2 * precision) + 0.5 * log(2*pi / precision)
#         |--- accuracy term ---|     |--- complexity cost ---|
#
#   Minimising F w.r.t. beliefs IS gradient descent on a variational bound,
#   recovering approximate Bayesian inference. The update equations ARE
#   Bayes' rule under Gaussian assumptions -- this is not a metaphor.
#
#   Hohwy (2013) and Clark (2016) argue conscious experience IS the brain's
#   best prediction. Precision-weighting (attention) determines which
#   prediction errors reach awareness.
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# THE GENERATIVE PROCESS (the "world" that produces sensory data)
# ─────────────────────────────────────────────────────────────────────────────

class GenerativeProcess:
    """
    A hidden process that generates sensory observations.

    The process produces a sine wave whose frequency can change abruptly,
    simulating regime changes in the environment (e.g., a predator appearing,
    a new melody starting). The agent does not know the frequency directly --
    it must infer it from raw sensory data.
    """

    def __init__(self, initial_frequency=1.0, amplitude=1.0, noise_std=0.1):
        self.frequency = initial_frequency
        self.amplitude = amplitude
        self.noise_std = noise_std
        self.time = 0.0
        self.dt = 0.05  # Timestep size

    def step(self):
        """Generate one observation from the hidden process."""
        signal = self.amplitude * np.sin(2.0 * np.pi * self.frequency * self.time)
        observation = signal + np.random.randn() * self.noise_std
        self.time += self.dt
        return observation, signal  # noisy observation + clean signal

    def change_frequency(self, new_frequency):
        """Regime change: abruptly switch the hidden cause."""
        self.frequency = new_frequency


# ─────────────────────────────────────────────────────────────────────────────
# PREDICTIVE PROCESSING HIERARCHY  (Rao & Ballard 1999; Friston 2005)
#
#   Level 1 (fast): predicts raw sensory input    | mu_l1, sigma_l1
#   Level 2 (slow): predicts hidden cause (freq)  | mu_l2, sigma_l2
#
#   Bottom-up: prediction errors propagate UPWARD  (surprise ascends)
#   Top-down:  predictions propagate DOWNWARD      (expectations descend)
# ─────────────────────────────────────────────────────────────────────────────

class PredictiveProcessingAgent:
    """
    A two-level hierarchical predictive processing agent.

    Level 1 tracks the instantaneous sensory value via precision-weighted
    prediction errors. Level 2 maintains a probability distribution over
    candidate frequencies (hidden causes) and updates it via Bayesian
    belief updating -- each frequency hypothesis generates a prediction,
    and hypotheses that predict well gain probability mass.

    This is equivalent to minimising variational free energy under a
    discrete mixture model at Level 2, which is how the brain may
    implement hierarchical inference via population coding.
    """

    def __init__(self, learning_rate_l1=0.3, n_hypotheses=100, freq_range=(0.2, 4.0)):
        # Level 1: belief about the current sensory value
        self.mu_l1 = 0.0          # Predicted sensory value
        self.sigma_l1 = 1.0       # Uncertainty (variance) about sensory value
        self.lr_l1 = learning_rate_l1

        # Level 2: distribution over frequency hypotheses (population code)
        # Each hypothesis is a candidate frequency with an associated weight.
        # This is a discrete approximation to the continuous posterior q(freq).
        self.freqs = np.linspace(freq_range[0], freq_range[1], n_hypotheses)
        self.log_weights = np.zeros(n_hypotheses)  # Log-space for numerical stability
        self._normalise_weights()

        # Observation noise model (known -- sets the precision of likelihood)
        self.obs_precision = 20.0  # 1/sigma^2 of sensory noise

        # Internal clock
        self.time = 0.0
        self.dt = 0.05

    def _normalise_weights(self):
        """Normalise log-weights to proper log-probabilities."""
        max_lw = np.max(self.log_weights)
        self.log_weights -= max_lw  # Shift for numerical stability
        log_sum = np.log(np.sum(np.exp(self.log_weights)))
        self.log_weights -= log_sum

    @property
    def mu_l2(self):
        """Expected frequency under the current posterior (belief mean)."""
        weights = np.exp(self.log_weights)
        return np.sum(weights * self.freqs)

    @property
    def sigma_l2(self):
        """Variance of frequency belief (uncertainty about hidden cause)."""
        weights = np.exp(self.log_weights)
        mean = np.sum(weights * self.freqs)
        return np.sum(weights * (self.freqs - mean) ** 2) + 1e-6

    def predict(self):
        """
        Generate a top-down prediction: the expected sensory value under
        the current frequency posterior (weighted average over hypotheses).
        """
        weights = np.exp(self.log_weights)
        predictions = np.sin(2.0 * np.pi * self.freqs * self.time)
        self.mu_l1 = np.sum(weights * predictions)
        return self.mu_l1

    def update(self, observation):
        """
        Minimise free energy given a new observation.

        Level 1: precision-weighted prediction error update (fast).
        Level 2: Bayesian update of frequency hypotheses -- each hypothesis
        is scored by how well it predicted the observation, and weights
        are updated via Bayes' rule (this IS free energy minimisation).

        The update rule for Level 2 in log-space:
          log w_i += -0.5 * precision * (observation - prediction_i)^2
        is exactly variational free energy minimisation under a mixture model.
        """
        # ── Level 1: prediction and error ──
        prediction = self.predict()
        error_l1 = observation - prediction

        # Precision-weighted update at Level 1
        precision_l1 = 1.0 / self.sigma_l1
        self.mu_l1 += self.lr_l1 * precision_l1 * error_l1

        # Adapt Level 1 variance
        self.sigma_l1 += 0.01 * (error_l1 ** 2 - self.sigma_l1)
        self.sigma_l1 = np.clip(self.sigma_l1, 0.01, 10.0)

        # ── Level 2: Bayesian belief update over frequency hypotheses ──
        # Each hypothesis generates its own prediction of the observation.
        # The log-likelihood of each hypothesis is proportional to
        # -precision * (obs - pred_i)^2 / 2  (Gaussian likelihood).
        predictions_i = np.sin(2.0 * np.pi * self.freqs * self.time)
        errors_i = observation - predictions_i
        log_likelihoods = -0.5 * self.obs_precision * errors_i ** 2

        # Bayesian update: posterior ∝ prior × likelihood
        # In log-space: log_posterior = log_prior + log_likelihood
        # We use a forgetting factor (0.995) to allow adaptation to change:
        # this slightly flattens the prior at each step, preventing the
        # posterior from becoming so peaked that it cannot recover from
        # regime changes. This is related to "volatility" in predictive
        # processing (Mathys et al., 2011).
        self.log_weights = 0.96 * self.log_weights + log_likelihoods
        self._normalise_weights()

        # Compute the Level 2 prediction error (surprise about the cause)
        error_l2 = self.sigma_l2  # High variance = high uncertainty = high surprise

        # Advance internal clock
        self.time += self.dt

        # ── Compute variational free energy ──
        # F = prediction_error^2 / (2*variance) + 0.5*log(2*pi*variance)
        free_energy = (
            (error_l1 ** 2) / (2.0 * self.sigma_l1)
            + 0.5 * np.log(2.0 * np.pi * self.sigma_l1)
        )

        return error_l1, error_l2, free_energy


# ─────────────────────────────────────────────────────────────────────────────
# FLAT (NON-HIERARCHICAL) PREDICTOR -- baseline for comparison
# ─────────────────────────────────────────────────────────────────────────────

class FlatPredictor:
    """Non-hierarchical exponential-smoothing predictor. No hidden causes."""

    def __init__(self, alpha=0.2):
        self.prediction = 0.0
        self.alpha = alpha  # Smoothing factor
        self.sigma = 1.0

    def update(self, observation):
        """Update prediction and compute free energy."""
        error = observation - self.prediction
        # Exponential moving average
        self.prediction += self.alpha * error
        # Adapt variance
        self.sigma += 0.01 * (error ** 2 - self.sigma)
        self.sigma = np.clip(self.sigma, 0.01, 10.0)
        # Free energy
        free_energy = (
            (error ** 2) / (2.0 * self.sigma)
            + 0.5 * np.log(2.0 * np.pi * self.sigma)
        )
        return error, free_energy


# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(n_steps=300, regime_change_at=100, new_frequency=2.5):
    """Run hierarchical + flat agents on the same sensory stream."""
    np.random.seed(42)

    world = GenerativeProcess(initial_frequency=1.0, noise_std=0.1)
    agent = PredictiveProcessingAgent()
    baseline = FlatPredictor()

    # Storage for results
    history = {
        "observation": [], "clean_signal": [],
        "prediction_hier": [], "prediction_flat": [],
        "error_l1": [], "error_l2": [],
        "fe_hier": [], "fe_flat": [],
        "freq_belief": [], "true_freq": [],
        "sigma_l1": [], "sigma_l2": [],
    }

    for step in range(n_steps):
        # Regime change
        if step == regime_change_at:
            world.change_frequency(new_frequency)

        # Generate observation
        obs, clean = world.step()

        # Hierarchical agent update
        pred_hier = agent.predict()
        err_l1, err_l2, fe_hier = agent.update(obs)

        # Flat baseline update
        err_flat, fe_flat = baseline.update(obs)

        # Record
        history["observation"].append(obs)
        history["clean_signal"].append(clean)
        history["prediction_hier"].append(pred_hier)
        history["prediction_flat"].append(baseline.prediction)
        history["error_l1"].append(err_l1)
        history["error_l2"].append(err_l2)
        history["fe_hier"].append(fe_hier)
        history["fe_flat"].append(fe_flat)
        history["freq_belief"].append(agent.mu_l2)
        history["true_freq"].append(world.frequency)
        history["sigma_l1"].append(agent.sigma_l1)
        history["sigma_l2"].append(agent.sigma_l2)

    return history, regime_change_at


# ─────────────────────────────────────────────────────────────────────────────
# FORMATTED OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

def print_phase_summary(history, start, end, label):
    """Print aggregate statistics for a phase of the simulation."""
    fe_hier = history["fe_hier"][start:end]
    fe_flat = history["fe_flat"][start:end]
    errors = history["error_l1"][start:end]
    freq_beliefs = history["freq_belief"][start:end]
    true_freqs = history["true_freq"][start:end]

    mean_fe_h = np.mean(fe_hier)
    mean_fe_f = np.mean(fe_flat)
    mean_err = np.mean(np.abs(errors))
    final_freq = freq_beliefs[-1]
    true_freq = true_freqs[-1]
    freq_error = abs(final_freq - true_freq)

    print(f"  {label}")
    print(f"    Mean |prediction error|:        {mean_err:.4f}")
    print(f"    Mean free energy (hierarchical): {mean_fe_h:.4f}")
    print(f"    Mean free energy (flat):         {mean_fe_f:.4f}")
    print(f"    Advantage of hierarchy:          {mean_fe_f - mean_fe_h:+.4f}")
    print(f"    Frequency belief:                {final_freq:.3f}  (true: {true_freq:.3f}, error: {freq_error:.3f})")
    print()


def print_timestep_detail(history, steps):
    """Print a detailed table for selected timesteps."""
    print(f"  {'Step':>5}  {'Observ':>8}  {'Predict':>8}  {'Error':>8}  {'FE(hier)':>9}  {'FE(flat)':>9}  {'Freq':>6}  {'True':>6}")
    print(f"  {'-----':>5}  {'--------':>8}  {'--------':>8}  {'--------':>8}  {'---------':>9}  {'---------':>9}  {'------':>6}  {'------':>6}")

    for t in steps:
        if t >= len(history["observation"]):
            continue
        print(
            f"  {t:>5}  "
            f"{history['observation'][t]:>8.3f}  "
            f"{history['prediction_hier'][t]:>8.3f}  "
            f"{history['error_l1'][t]:>8.3f}  "
            f"{history['fe_hier'][t]:>9.4f}  "
            f"{history['fe_flat'][t]:>9.4f}  "
            f"{history['freq_belief'][t]:>6.3f}  "
            f"{history['true_freq'][t]:>6.3f}"
        )
    print()


def display_results(history, regime_change_at):
    """Display the full simulation results."""
    n_steps = len(history["observation"])

    print()
    print("=" * 70)
    print("  PREDICTIVE PROCESSING: Your Brain as a Prediction Machine")
    print("=" * 70)
    print()
    print("  The Free Energy Principle (Friston, 2010) proposes that all")
    print("  self-organising systems minimise variational free energy -- a")
    print("  tractable upper bound on sensory surprise. Conscious experience")
    print("  may be the brain's best top-down prediction of its sensory input.")
    print()
    print("  This simulation builds a 2-level predictive processing hierarchy:")
    print("    Level 1 (fast): tracks the raw sensory signal")
    print("    Level 2 (slow): infers the hidden cause (signal frequency)")
    print()
    print("  F = error^2 / (2 * variance) + 0.5 * log(2*pi*variance)")
    print("      |--- accuracy term ---|   |--- complexity term ---|")
    print()

    # ── Phase 1: Stable environment ──
    print("-" * 70)
    print("  PHASE 1: Stable Environment (learning)")
    print("-" * 70)
    print()
    print("  The agent encounters a sine wave at frequency 1.0 Hz.")
    print("  Watch free energy decrease as beliefs converge on the true cause.")
    print()

    # Show early, middle, and late timesteps from Phase 1
    phase1_steps = list(range(0, min(regime_change_at, 5))) + \
                   [regime_change_at // 2] + \
                   list(range(regime_change_at - 3, regime_change_at))
    phase1_steps = sorted(set(s for s in phase1_steps if 0 <= s < regime_change_at))
    print_timestep_detail(history, phase1_steps)
    print_phase_summary(history, 0, regime_change_at, "Phase 1 summary (stable signal):")

    # ── Phase 2: Regime change ──
    print("-" * 70)
    print(f"  PHASE 2: Regime Change at step {regime_change_at}")
    print("-" * 70)
    print()
    print(f"  The hidden frequency shifts from 1.0 to {history['true_freq'][regime_change_at]:.1f} Hz.")
    print("  Free energy spikes (the agent is surprised!) then decreases")
    print("  as it updates its beliefs about the new hidden cause.")
    print()

    # Show timesteps around the regime change and late adaptation
    phase2_steps = list(range(regime_change_at, min(regime_change_at + 8, n_steps))) + \
                   list(range(n_steps - 5, n_steps))
    phase2_steps = sorted(set(s for s in phase2_steps if regime_change_at <= s < n_steps))
    print_timestep_detail(history, phase2_steps)
    print_phase_summary(history, regime_change_at, n_steps, "Phase 2 summary (after regime change):")

    # ── Free energy trajectory ──
    print("-" * 70)
    print("  FREE ENERGY TRAJECTORY")
    print("-" * 70)
    print()

    sample_steps = list(range(0, n_steps, 20)) + [n_steps - 1]
    max_fe = max(max(history["fe_hier"]), 0.1)
    bar_width = 35

    for t in sample_steps:
        fe = history["fe_hier"][t]
        bar_len = int(min(fe / max_fe, 1.0) * bar_width)
        bar = "#" * bar_len
        marker = " <<< REGIME CHANGE" if t == regime_change_at else ""
        print(f"  t={t:>3}  FE={fe:>6.3f}  |{bar:<{bar_width}}|{marker}")

    print()

    # ── Frequency belief tracking ──
    print("-" * 70)
    print("  FREQUENCY BELIEF vs TRUE FREQUENCY")
    print("-" * 70)
    print()

    # Show every 20 steps for conciseness
    freq_steps = list(range(0, n_steps, 20)) + [n_steps - 1]
    for t in freq_steps:
        belief = history["freq_belief"][t]
        true = history["true_freq"][t]
        scale = 40
        b_pos = int(np.clip(belief / 5.0, 0, 1) * scale)
        t_pos = int(np.clip(true / 5.0, 0, 1) * scale)
        line = ["."] * (scale + 1)
        line[t_pos] = "T"
        line[b_pos] = "B"
        if b_pos == t_pos:
            line[b_pos] = "*"
        marker = " <<< SHIFT" if t == regime_change_at else ""
        print(f"  t={t:>3}  {''.join(line)}  B={belief:.2f} T={true:.2f}{marker}")

    print()

    # ── Hierarchy vs flat comparison ──
    print("-" * 70)
    print("  HIERARCHY vs FLAT PREDICTOR")
    print("-" * 70)
    print()

    # Compute windowed averages
    window = 20
    for phase_start, phase_end, label in [
        (0, regime_change_at, "Stable phase"),
        (regime_change_at, n_steps, "After regime change"),
    ]:
        # Last window of each phase
        ws = max(phase_start, phase_end - window)
        fe_h = np.mean(history["fe_hier"][ws:phase_end])
        fe_f = np.mean(history["fe_flat"][ws:phase_end])
        winner = "HIERARCHY" if fe_h < fe_f else "FLAT"
        ratio = fe_f / fe_h if fe_h > 0.01 else float("inf")

        print(f"  {label} (last {phase_end - ws} steps):")
        print(f"    Hierarchical free energy: {fe_h:.4f}")
        print(f"    Flat predictor free energy: {fe_f:.4f}")
        print(f"    Winner: {winner} (ratio: {ratio:.2f}x)")
        print()

    # ── Precision dynamics ──
    print("-" * 70)
    print("  PRECISION = ATTENTION (Feldman & Friston, 2010)")
    print("-" * 70)
    print()
    print("  Precision (1/variance) determines how much prediction errors 'count'.")
    print("  High precision = high confidence = errors drive large belief updates.")
    print()

    for t in list(range(0, n_steps, 20)) + [n_steps - 1]:
        prec_l1 = 1.0 / history["sigma_l1"][t]
        # L2 precision: use log scale since discrete posteriors can become very peaked
        sigma_l2 = history["sigma_l2"][t]
        conf_l2 = np.clip(-np.log10(sigma_l2 + 1e-10), 0.0, 6.0)  # Log confidence
        bar_l1 = "#" * int(min(prec_l1 / 5.0, 1.0) * 20)
        bar_l2 = "#" * int(min(conf_l2 / 6.0, 1.0) * 20)
        print(f"  t={t:>3}  L1={prec_l1:>5.2f} |{bar_l1:<20}|  L2 conf={conf_l2:>4.1f} |{bar_l2:<20}|")

    print()

    # ── Final summary ──
    print("=" * 70)
    print("  IMPLICATIONS FOR CONSCIOUSNESS")
    print("=" * 70)
    print()
    print("  This simulation demonstrates the core claims of predictive processing:")
    print()
    print("  1. PREDICTION-ERROR MINIMISATION: the agent learns to predict its")
    print("     sensory input, driving free energy toward zero. Friston argues")
    print("     all adaptive systems must do this to persist.")
    print()
    print("  2. HIERARCHICAL INFERENCE: Level 2 infers the abstract hidden cause")
    print("     (frequency) that explains Level 1 fluctuations. The brain may")
    print("     stack many such levels, from edges to objects to concepts.")
    print()
    print("  3. SURPRISE AND ADAPTATION: regime changes spike free energy.")
    print("     The hierarchy adapts by updating its causal model -- not just")
    print("     memorising new values, but revising its generative model.")
    print()
    print("  4. PRECISION AS ATTENTION: precision-weighting controls which")
    print("     errors drive updates. Feldman & Friston (2010) argue this")
    print("     is the computational mechanism of selective attention.")
    print()
    print("  5. CONSCIOUSNESS AS PREDICTION: Clark (2016) and Hohwy (2013)")
    print("     propose that conscious experience IS the brain's best")
    print("     prediction -- the content of the top-level generative model.")
    print("     On this view, any system that minimises free energy over a")
    print("     sufficiently deep hierarchy might be a candidate for")
    print("     phenomenal experience -- including artificial ones.")
    print()
    print("  The critical open question: does free energy minimisation require")
    print("  only the right computational structure (functionalism), or does it")
    print("  require the right kind of embodied, autopoietic self-organisation")
    print("  (enactivism)? This is the deepest fault line in the debate over")
    print("  machine consciousness.")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    history, regime_change_at = run_simulation(
        n_steps=300,
        regime_change_at=100,
        new_frequency=2.5,
    )
    display_results(history, regime_change_at)


if __name__ == "__main__":
    main()
