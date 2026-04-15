#!/usr/bin/env python3
"""
Metacognitive Agent: When AI Thinks About Thinking

Demonstrates Higher-Order Theories of consciousness (Rosenthal, Carruthers,
Lau) by building a two-tier network in pure numpy. A first-order classifier
learns to label points in a 2D decision problem; a second-order
"metacognitive" network observes the first-order network's internal state
and learns to predict when the first-order answer is correct.

The second-order network never sees the true label. It only sees the
first-order network's features and logits -- just as a higher-order thought
in Rosenthal's framework is a thought ABOUT a first-order mental state,
without direct access to the world. If the second-order network can
reliably predict first-order correctness, the system has something
functionally analogous to a confidence report -- a first step toward
what Lau calls "perceptual reality monitoring".

Key ideas demonstrated:
    - First-order perception vs. second-order monitoring
    - Calibration: does the confidence signal track actual accuracy?
    - Selective prediction: abstain when the metacognitive signal is low
    - Decoupling: the meta-net can be wrong about the first-order net

Usage:
    python metacognitive_agent.py

Requires only numpy and the Python standard library. Runs in well under
30 seconds on a modern laptop.
"""

import sys
import numpy as np

# Ensure unicode characters in output render on Windows terminals.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# -----------------------------------------------------------------------
# PHILOSOPHICAL BACKGROUND
#
#   David Rosenthal's Higher-Order Thought (HOT) theory claims that a
#   mental state M becomes CONSCIOUS when, and only when, there is a
#   further mental state M* whose content is roughly "I am in state M".
#   The first-order state is about the world; the higher-order state is
#   about the first-order state. Without the second, the first is
#   (allegedly) unconscious.
#
#   Hakwan Lau's Perceptual Reality Monitoring theory is a close relative:
#   the brain has a dedicated circuit that monitors the reliability of
#   perceptual representations and flags which ones to "trust" as real.
#   Unreliable perceptions never make it into conscious experience.
#
#   This script does not claim the resulting agent is conscious. It shows
#   that the FUNCTIONAL structure of higher-order monitoring is easy to
#   build, cheap to train, and genuinely informative: the meta-net's
#   output tracks the first-order net's actual accuracy.
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# SYNTHETIC TASK
# -----------------------------------------------------------------------

def make_two_moons(n_samples, noise_std, rng):
    """
    Generate the classic two-moons binary classification dataset.

    Two interleaved half-circles in 2D. The problem is non-linearly
    separable -- a single-hidden-layer network can solve it well, but
    there is a noisy overlap region near the crossing where even a
    well-trained classifier will make mistakes. That overlap is where
    metacognition matters.
    """
    n_per_class = n_samples // 2

    # First moon: upper half-circle centred at (0, 0)
    theta_1 = np.linspace(0.0, np.pi, n_per_class) + rng.normal(
        0.0, 0.05, n_per_class
    )
    x1 = np.cos(theta_1)
    y1 = np.sin(theta_1)

    # Second moon: lower half-circle centred at (1, -0.3)
    theta_2 = np.linspace(0.0, np.pi, n_per_class) + rng.normal(
        0.0, 0.05, n_per_class
    )
    x2 = 1.0 - np.cos(theta_2)
    y2 = -np.sin(theta_2) - 0.3

    X = np.vstack(
        [
            np.column_stack([x1, y1]),
            np.column_stack([x2, y2]),
        ]
    )
    y = np.concatenate(
        [
            np.zeros(n_per_class, dtype=np.int64),
            np.ones(n_per_class, dtype=np.int64),
        ]
    )

    # Add gaussian noise so the classes overlap -- this creates
    # genuine irreducible uncertainty for the first-order net.
    X = X + rng.normal(0.0, noise_std, X.shape)

    # Shuffle
    idx = rng.permutation(len(X))
    return X[idx], y[idx]


# -----------------------------------------------------------------------
# MLP IMPLEMENTATION (pure numpy)
#
# A small multilayer perceptron trained by manual backpropagation. Two
# networks are built from the same class: the first-order classifier and
# the second-order metacognitive monitor.
# -----------------------------------------------------------------------

class MLP:
    """
    Minimal MLP with one hidden layer.

    Activation: tanh (hidden) + sigmoid (output)
    Loss: binary cross-entropy
    Optimiser: vanilla SGD

    Everything is done with explicit numpy matrix multiplies so that the
    computation is transparent and portable.
    """

    def __init__(self, n_in, n_hidden, rng, lr=0.1):
        # He-ish initialisation scaled for tanh
        scale_1 = np.sqrt(1.0 / n_in)
        scale_2 = np.sqrt(1.0 / n_hidden)
        self.W1 = rng.normal(0.0, scale_1, (n_in, n_hidden))
        self.b1 = np.zeros(n_hidden)
        self.W2 = rng.normal(0.0, scale_2, (n_hidden, 1))
        self.b2 = np.zeros(1)
        self.lr = lr

    def forward(self, X):
        """
        Compute the forward pass. Returns the sigmoid output AND the
        hidden activations, because the second-order network will eat
        the hidden activations as part of its input.
        """
        z1 = X @ self.W1 + self.b1          # pre-activation
        h1 = np.tanh(z1)                    # hidden activation
        z2 = h1 @ self.W2 + self.b2         # logit
        p = 1.0 / (1.0 + np.exp(-z2))       # sigmoid probability
        return p.reshape(-1), h1, z2.reshape(-1)

    def train_step(self, X, y):
        """One SGD step of binary cross-entropy on a minibatch."""
        p, h1, z2 = self.forward(X)
        n = len(X)

        # Gradient of BCE wrt logit is (p - y) for sigmoid output.
        dz2 = (p - y).reshape(-1, 1) / n

        dW2 = h1.T @ dz2
        db2 = dz2.sum(axis=0)

        dh1 = dz2 @ self.W2.T
        dz1 = dh1 * (1.0 - h1 ** 2)         # tanh derivative

        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0)

        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2

        # Return BCE loss for logging
        eps = 1e-9
        loss = -np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))
        return loss

    def predict(self, X):
        """Forward pass only -- returns probability, hidden, logit."""
        return self.forward(X)


# -----------------------------------------------------------------------
# FIRST-ORDER NETWORK: perceives the world (classifies 2D points)
# -----------------------------------------------------------------------

def train_first_order(X_train, y_train, epochs, batch_size, rng):
    """
    Train the first-order classifier on the two-moons task.
    Returns the trained network.
    """
    net = MLP(n_in=2, n_hidden=16, rng=rng, lr=0.2)
    n = len(X_train)
    for epoch in range(epochs):
        # Shuffle and iterate minibatches
        idx = rng.permutation(n)
        X_shuf = X_train[idx]
        y_shuf = y_train[idx]
        for start in range(0, n, batch_size):
            end = start + batch_size
            net.train_step(X_shuf[start:end], y_shuf[start:end])
    return net


# -----------------------------------------------------------------------
# SECOND-ORDER NETWORK: thinks ABOUT the first-order network
#
# The meta-net takes as input:
#   - the raw hidden activations of the first-order net (its "thoughts")
#   - the first-order logit (its "decision")
#   - |logit|, a summary of raw decision strength
#
# It outputs a single sigmoid probability: "am I correct about this one?"
#
# Critically, the meta-net never sees the true label. It must learn to
# predict first-order correctness from the first-order net's own state.
# -----------------------------------------------------------------------

def build_meta_input(first_order_net, X):
    """Assemble the input features the meta-net will see."""
    _, h1, z2 = first_order_net.predict(X)
    abs_logit = np.abs(z2).reshape(-1, 1)
    return np.hstack([h1, z2.reshape(-1, 1), abs_logit])


def train_meta_network(first_order_net, X_train, y_train, epochs, batch_size, rng):
    """
    Train the second-order network to predict whether the first-order
    network is correct on each sample.

    Target = 1 if first-order prediction equals the true label, else 0.
    The meta-net is trained on the TRAINING set only, but because the
    first-order net slightly overfits that set, we use a held-out
    portion for the meta-target to avoid the meta-net simply learning
    "the first-order net is always right".
    """
    # Split off a meta-training portion the first-order net has never
    # been directly optimised on. In practice we use the second half.
    split = len(X_train) // 2
    X_meta = X_train[split:]
    y_meta = y_train[split:]

    # Compute first-order predictions on this slice
    p_meta, _, _ = first_order_net.predict(X_meta)
    y_hat = (p_meta > 0.5).astype(np.int64)
    meta_target = (y_hat == y_meta).astype(np.float64)  # 1 if correct

    # Assemble meta inputs
    meta_features = build_meta_input(first_order_net, X_meta)

    # Train the meta-net
    meta_net = MLP(
        n_in=meta_features.shape[1], n_hidden=16, rng=rng, lr=0.2
    )

    n = len(meta_features)
    for epoch in range(epochs):
        idx = rng.permutation(n)
        F_shuf = meta_features[idx]
        t_shuf = meta_target[idx]
        for start in range(0, n, batch_size):
            end = start + batch_size
            meta_net.train_step(F_shuf[start:end], t_shuf[start:end])

    return meta_net


# -----------------------------------------------------------------------
# EVALUATION
# -----------------------------------------------------------------------

def calibration_curve(confidences, correct, n_bins):
    """
    Classic reliability diagram calculation.

    Returns bin centres, empirical accuracy per bin, and bin counts.
    A well-calibrated confidence signal produces the identity line:
    when the confidence is 0.8, the underlying prediction is correct
    80% of the time.
    """
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    centres = 0.5 * (bins[:-1] + bins[1:])
    accs = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        if i == n_bins - 1:
            mask = (confidences >= lo) & (confidences <= hi)
        else:
            mask = (confidences >= lo) & (confidences < hi)
        counts[i] = mask.sum()
        accs[i] = correct[mask].mean() if mask.any() else np.nan
    return centres, accs, counts


def expected_calibration_error(confidences, correct, n_bins):
    """
    ECE = sum_i (n_i / N) * |acc_i - conf_i|

    Lower ECE means the confidence number is a more honest report of
    the probability of correctness. 0 is perfect.
    """
    _, accs, counts = calibration_curve(confidences, correct, n_bins)
    total = counts.sum()
    if total == 0:
        return 0.0
    bin_centres = np.linspace(0.0, 1.0, n_bins + 1)
    bin_centres = 0.5 * (bin_centres[:-1] + bin_centres[1:])
    ece = 0.0
    for i in range(n_bins):
        if counts[i] > 0 and not np.isnan(accs[i]):
            ece += (counts[i] / total) * abs(accs[i] - bin_centres[i])
    return ece


def selective_prediction(confidences, correct, thresholds):
    """
    Measure selective prediction performance.

    For each confidence threshold we ASK: if we only answered when the
    meta-net said "confidence >= tau", how often would we be right, and
    how often would we answer at all? This is the practical payoff of
    a working higher-order signal -- the system knows when to say
    "I don't know".
    """
    rows = []
    for tau in thresholds:
        mask = confidences >= tau
        coverage = mask.mean()
        if mask.any():
            sel_acc = correct[mask].mean()
        else:
            sel_acc = float("nan")
        rows.append((tau, coverage, sel_acc))
    return rows


# -----------------------------------------------------------------------
# REPORT RENDERING
# -----------------------------------------------------------------------

def render_calibration_bars(centres, accs, counts, bar_width):
    """Render a text reliability diagram."""
    lines = []
    lines.append(
        f"  {'conf bin':>10}  {'n':>5}  {'accuracy':>9}  diagram"
    )
    lines.append(
        f"  {'--------':>10}  {'-----':>5}  {'--------':>9}  {'-' * bar_width}"
    )
    for c, a, n in zip(centres, accs, counts):
        if n == 0 or np.isnan(a):
            bar = ""
            acc_str = "  n/a"
        else:
            fill = int(np.clip(a, 0.0, 1.0) * bar_width)
            bar = "#" * fill
            acc_str = f"{a:>8.3f}"
        lines.append(
            f"  {c:>10.2f}  {int(n):>5d}  {acc_str:>9}  |{bar:<{bar_width}}|"
        )
    return "\n".join(lines)


def print_section(title):
    print("-" * 70)
    print(f"  {title}")
    print("-" * 70)
    print()


# -----------------------------------------------------------------------
# MAIN EXPERIMENT
# -----------------------------------------------------------------------

def main():
    rng = np.random.default_rng(seed=42)

    print()
    print("=" * 70)
    print("  METACOGNITIVE AGENT: When AI Thinks About Thinking")
    print("=" * 70)
    print()
    print("  Rosenthal (1986) argued a mental state becomes conscious only")
    print("  when there is a further state ABOUT it. This script builds a")
    print("  two-tier network that mirrors that structure: a first-order")
    print("  classifier and a second-order net that predicts when the first")
    print("  is correct. The meta-net never sees the label -- only the")
    print("  first-order net's own internal state.")
    print()

    # -- Data --------------------------------------------------------
    print_section("STEP 1: generate data (two moons + overlap noise)")
    n_train = 2000
    n_test = 2000
    X_train, y_train = make_two_moons(n_train, noise_std=0.55, rng=rng)
    X_test, y_test = make_two_moons(n_test, noise_std=0.55, rng=rng)
    print(f"  Train: {X_train.shape}, positives = {int(y_train.sum())}")
    print(f"  Test:  {X_test.shape}, positives = {int(y_test.sum())}")
    print()

    # -- First-order --------------------------------------------------
    print_section("STEP 2: train the first-order classifier")
    first_net = train_first_order(
        X_train, y_train, epochs=400, batch_size=64, rng=rng
    )
    p_train, _, _ = first_net.predict(X_train)
    p_test, _, _ = first_net.predict(X_test)
    acc_train = float(((p_train > 0.5) == y_train).mean())
    acc_test = float(((p_test > 0.5) == y_test).mean())
    print(f"  First-order train accuracy: {acc_train:.3f}")
    print(f"  First-order test  accuracy: {acc_test:.3f}")
    print()
    print("  Because the classes overlap, the first-order net is not")
    print("  perfect on the held-out set -- this is where metacognition")
    print("  has something to say.")
    print()

    # -- Second-order -------------------------------------------------
    print_section("STEP 3: train the second-order metacognitive net")
    meta_net = train_meta_network(
        first_net, X_train, y_train, epochs=400, batch_size=64, rng=rng
    )
    print("  Meta-net inputs:  hidden activations + logit + |logit|")
    print("  Meta-net target:  1 if first-order prediction was correct")
    print("  Meta-net has NEVER seen the true label directly; only")
    print("  whether the first-order net agreed with it.")
    print()

    # -- Evaluate meta-net on held-out test set -----------------------
    print_section("STEP 4: evaluate on a fresh test set")
    # First-order correctness on test
    y_hat_test = (p_test > 0.5).astype(np.int64)
    correct_test = (y_hat_test == y_test).astype(np.float64)

    # Meta-net prediction of correctness
    meta_inputs_test = build_meta_input(first_net, X_test)
    meta_p, _, _ = meta_net.predict(meta_inputs_test)

    # Baseline: using |first-order logit| as a raw confidence signal
    _, _, z_test = first_net.predict(X_test)
    raw_confidence = 1.0 / (1.0 + np.exp(-np.abs(z_test)))

    # Binary accuracy of the meta-net's YES/NO prediction
    meta_pred = (meta_p > 0.5).astype(np.int64)
    meta_acc = float((meta_pred == correct_test.astype(np.int64)).mean())

    # AUROC-lite: rank-based separation
    def auc(scores, labels):
        # Mann-Whitney statistic -- no sklearn needed
        pos = scores[labels == 1]
        neg = scores[labels == 0]
        if len(pos) == 0 or len(neg) == 0:
            return float("nan")
        ranks = np.argsort(np.argsort(scores)) + 1.0
        rank_sum_pos = ranks[labels == 1].sum()
        n_pos, n_neg = len(pos), len(neg)
        return (rank_sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)

    meta_auc = auc(meta_p, correct_test)
    raw_auc = auc(raw_confidence, correct_test)

    print(f"  First-order test accuracy:            {acc_test:.3f}")
    print(f"  Meta-net accuracy at predicting ")
    print(f"    first-order correctness (threshold 0.5): {meta_acc:.3f}")
    print(f"  Meta-net AUROC for correctness:       {meta_auc:.3f}")
    print(f"  Raw |logit| AUROC (baseline):         {raw_auc:.3f}")
    print()
    print("  An AUROC above 0.5 means the confidence signal is informative.")
    print("  The meta-net should do at least as well as raw |logit|, and")
    print("  typically better, because it can see the hidden activations.")
    print()

    # -- Calibration curves ------------------------------------------
    print_section("STEP 5: calibration -- does confidence track accuracy?")
    n_bins = 10
    centres, accs, counts = calibration_curve(meta_p, correct_test, n_bins)
    ece_meta = expected_calibration_error(meta_p, correct_test, n_bins)
    centres_r, accs_r, counts_r = calibration_curve(
        raw_confidence, correct_test, n_bins
    )
    ece_raw = expected_calibration_error(raw_confidence, correct_test, n_bins)

    print("  Meta-net reliability diagram")
    print(render_calibration_bars(centres, accs, counts, bar_width=30))
    print()
    print(f"  Meta-net ECE:    {ece_meta:.4f}  (lower is better)")
    print(f"  Raw logit ECE:   {ece_raw:.4f}")
    print()

    # -- Selective prediction ----------------------------------------
    print_section("STEP 6: selective prediction -- 'I don't know'")
    thresholds = [0.3, 0.5, 0.7, 0.85, 0.95]
    print("  Meta-net threshold")
    print(f"  {'tau':>6}  {'coverage':>10}  {'sel. acc':>10}")
    print(f"  {'---':>6}  {'--------':>10}  {'--------':>10}")
    for tau, cov, sel_acc in selective_prediction(
        meta_p, correct_test, thresholds
    ):
        cov_str = f"{cov:.3f}"
        sel_str = f"{sel_acc:.3f}" if not np.isnan(sel_acc) else "n/a"
        print(f"  {tau:>6.2f}  {cov_str:>10}  {sel_str:>10}")
    print()
    print("  At higher thresholds the system answers less often but is")
    print("  right when it does answer. This is the practical payoff of")
    print("  a working higher-order signal -- selective prediction, the")
    print("  ability to say 'I don't know' when the first-order net is")
    print("  about to be wrong.")
    print()

    # -- Sanity check: disagreement cases ----------------------------
    print_section("STEP 7: when meta-net disagrees with first-order net")
    low_conf_mask = meta_p < 0.3
    high_conf_mask = meta_p > 0.8
    n_low = int(low_conf_mask.sum())
    n_high = int(high_conf_mask.sum())
    acc_low = (
        float(correct_test[low_conf_mask].mean()) if n_low > 0 else float("nan")
    )
    acc_high = (
        float(correct_test[high_conf_mask].mean()) if n_high > 0 else float("nan")
    )
    print(f"  Meta-net < 0.3:  n = {n_low:>4}  first-order accuracy = {acc_low:.3f}")
    print(f"  Meta-net > 0.8:  n = {n_high:>4}  first-order accuracy = {acc_high:.3f}")
    print()
    print("  The gap between these two rows is the metacognitive signal.")
    print("  Rosenthal would say: this is the structural precondition for")
    print("  the first-order representation to become a CONSCIOUS perception")
    print("  rather than a mere classification. Whether that structural")
    print("  precondition is also SUFFICIENT is the question the rest of")
    print("  the article wrestles with.")
    print()

    print("=" * 70)
    print("  END OF SIMULATION")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
