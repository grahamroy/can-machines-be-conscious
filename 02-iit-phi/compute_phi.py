#!/usr/bin/env python3
"""
Computing Phi: A Simplified Implementation of Integrated Information Theory (IIT)

Demonstrates the core mathematical ideas behind Tononi's Integrated Information
Theory by computing a simplified version of Phi on small causal networks.

Key insight: Phi measures how much a system is "more than the sum of its parts."
A system with high Phi cannot be reduced to independent components without
losing information about its causal structure.

Usage:
    python compute_phi.py

Requires only numpy. No external IIT libraries needed.
"""

import sys
import numpy as np
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
# TRANSITION PROBABILITY MATRICES (TPMs)
#
# A TPM encodes the causal structure of a network. Entry TPM[i, j] gives the
# probability that node j is ON at t+1, given that state i occurred at time t.
# States are binary vectors encoded as integers: e.g., for 3 nodes,
# state 5 = (1,0,1) means nodes A and C are ON, node B is OFF.
# ─────────────────────────────────────────────────────────────────────────────


def state_to_binary(state, n_nodes):
    """Convert an integer state index to a binary tuple of node activations."""
    return tuple((state >> i) & 1 for i in range(n_nodes))


def binary_to_state(binary):
    """Convert a binary tuple back to an integer state index."""
    return sum(b << i for i, b in enumerate(binary))


def build_tpm_from_weights(weights, threshold=0.5, noise=0.1):
    """
    Build a TPM from a weight matrix using a noisy threshold function.

    Each node j turns ON at t+1 if the weighted sum of inputs exceeds
    a threshold, with some noise (probability of flipping).

    Args:
        weights: n x n matrix where weights[i][j] = connection strength from i to j
        threshold: activation threshold for each node
        noise: probability of a node being in the "wrong" state (adds stochasticity)

    Returns:
        TPM of shape (2^n, n) — state-by-node conditional probability format
    """
    n = len(weights)
    n_states = 2 ** n
    tpm = np.zeros((n_states, n))

    for state_idx in range(n_states):
        current = state_to_binary(state_idx, n)
        for node_j in range(n):
            # Weighted sum of inputs to node j
            input_sum = sum(weights[i][node_j] * current[i] for i in range(n))
            # Deterministic output before noise
            if input_sum >= threshold:
                tpm[state_idx, node_j] = 1.0 - noise
            else:
                tpm[state_idx, node_j] = noise

    return tpm


# ─────────────────────────────────────────────────────────────────────────────
# INFORMATION-THEORETIC MEASURES
# ─────────────────────────────────────────────────────────────────────────────


def entropy(prob_dist):
    """
    Shannon entropy H(X) = -sum(p * log2(p)) for a probability distribution.

    Measures the uncertainty or "information content" of a distribution.
    """
    # Filter out zero probabilities to avoid log(0)
    p = prob_dist[prob_dist > 1e-12]
    return -np.sum(p * np.log2(p))


def mutual_information(joint_prob):
    """
    Mutual information I(X; Y) from a joint probability table.

    MI measures how much knowing X reduces uncertainty about Y (and vice versa).
    I(X; Y) = H(X) + H(Y) - H(X, Y)

    In IIT, this captures how much information the parts share — information
    that would be lost if we severed the connection between them.
    """
    # Marginals
    p_x = joint_prob.sum(axis=1)
    p_y = joint_prob.sum(axis=0)

    h_x = entropy(p_x)
    h_y = entropy(p_y)
    h_xy = entropy(joint_prob.flatten())

    return h_x + h_y - h_xy


def tpm_to_full_distribution(tpm):
    """
    Convert a state-by-node TPM to a full state-by-state transition matrix.

    Each row gives the probability distribution over next states, assuming
    node activations are conditionally independent given the current state.
    """
    n_states, n_nodes = tpm.shape
    full = np.zeros((n_states, n_states))

    for current in range(n_states):
        for next_state in range(n_states):
            next_bits = state_to_binary(next_state, n_nodes)
            # Product of independent node probabilities
            prob = 1.0
            for j in range(n_nodes):
                if next_bits[j] == 1:
                    prob *= tpm[current, j]
                else:
                    prob *= (1.0 - tpm[current, j])
            full[current, next_state] = prob

    return full


# ─────────────────────────────────────────────────────────────────────────────
# COMPUTING PHI (simplified)
#
# The core idea: Phi is the information lost when we partition the system at
# its "weakest link" (the Minimum Information Partition, or MIP).
#
# Full IIT computes Phi using cause-effect repertoires and the Earth Mover's
# Distance (EMD). Here we use a simplified approach based on mutual information
# between subsystems, which captures the essential insight: integrated systems
# lose information when partitioned; modular systems do not.
#
# Why this is NP-hard: for n nodes, we must check all possible bipartitions.
# The number of bipartitions grows as 2^(n-1) - 1, making exact computation
# intractable for large systems. This is a real limitation of IIT.
# ─────────────────────────────────────────────────────────────────────────────


def get_all_bipartitions(n_nodes):
    """
    Enumerate all non-trivial bipartitions of n nodes into two non-empty groups.

    For n=3 nodes {A,B,C}, the bipartitions are:
        {A} | {B,C}
        {B} | {A,C}
        {C} | {A,B}

    For n=4, there are 7 bipartitions. For n=10, there are 511.
    In general: 2^(n-1) - 1 bipartitions. This exponential growth is why
    computing Phi is NP-hard.
    """
    nodes = list(range(n_nodes))
    partitions = []

    # Generate all subsets of size 1 to n//2 for one side of the partition
    for size in range(1, n_nodes):
        for part_a in combinations(nodes, size):
            part_b = tuple(n for n in nodes if n not in part_a)
            # Avoid duplicates: only keep partitions where min(A) < min(B)
            if part_a < part_b:
                partitions.append((list(part_a), list(part_b)))

    return partitions


def compute_partition_information_loss(full_tpm, part_a, part_b, n_nodes):
    """
    Compute the information lost by partitioning the system into part_a | part_b.

    We measure this as the mutual information between the two partitions in the
    system's transition dynamics. If severing the connection between A and B
    loses a lot of mutual information, the system is tightly integrated.

    This is a simplification of IIT's actual measure, which uses cause-effect
    repertoires and EMD. But it captures the core idea.
    """
    n_states = 2 ** n_nodes

    # Build a joint distribution over (part_a states at t+1) x (part_b states at t+1)
    # by marginalizing the full TPM, averaged over a uniform distribution of current states
    n_a = len(part_a)
    n_b = len(part_b)
    joint = np.zeros((2 ** n_a, 2 ** n_b))

    # Average over all current states (uniform prior, as in IIT's unconstrained repertoire)
    for current in range(n_states):
        for next_state in range(n_states):
            prob = full_tpm[current, next_state] / n_states  # uniform prior

            # Extract the sub-states for each partition
            next_bits = state_to_binary(next_state, n_nodes)
            a_bits = tuple(next_bits[i] for i in part_a)
            b_bits = tuple(next_bits[i] for i in part_b)
            a_idx = binary_to_state(a_bits)
            b_idx = binary_to_state(b_bits)

            joint[a_idx, b_idx] += prob

    return mutual_information(joint)


def compute_phi(tpm, network_name="Network"):
    """
    Compute Phi for a network defined by its state-by-node TPM.

    Steps:
        1. Convert to full state-by-state transition matrix
        2. Enumerate all bipartitions
        3. For each bipartition, compute mutual information lost
        4. Phi = minimum information lost across all partitions (the MIP)

    Phi = 0 means the system can be fully decomposed without losing information.
    Phi > 0 means the system is irreducibly integrated.
    """
    n_states, n_nodes = tpm.shape
    full_tpm = tpm_to_full_distribution(tpm)
    bipartitions = get_all_bipartitions(n_nodes)

    print(f"  Transition probability matrix (state-by-node):")
    print(f"  {'State':<8} " + " ".join(f"{'Node '+chr(65+j):>8}" for j in range(n_nodes)))
    for i in range(min(n_states, 8)):  # Print first 8 states max
        bits = state_to_binary(i, n_nodes)
        label = "".join(str(b) for b in bits)
        probs = " ".join(f"{tpm[i,j]:8.3f}" for j in range(n_nodes))
        print(f"  {label:<8} {probs}")
    if n_states > 8:
        print(f"  ... ({n_states - 8} more states)")

    print(f"\n  Number of bipartitions to check: {len(bipartitions)}")
    print(f"  (For n={n_nodes} nodes: 2^(n-1) - 1 = {2**(n_nodes-1) - 1} bipartitions)")

    # Find the Minimum Information Partition (MIP)
    min_info = float("inf")
    mip = None
    partition_results = []

    for part_a, part_b in bipartitions:
        info_loss = compute_partition_information_loss(full_tpm, part_a, part_b, n_nodes)
        partition_results.append((part_a, part_b, info_loss))

        label_a = "{" + ",".join(chr(65 + i) for i in part_a) + "}"
        label_b = "{" + ",".join(chr(65 + i) for i in part_b) + "}"
        print(f"    Partition {label_a} | {label_b}: MI = {info_loss:.6f} bits")

        if info_loss < min_info:
            min_info = info_loss
            mip = (part_a, part_b)

    phi = min_info
    mip_a = "{" + ",".join(chr(65 + i) for i in mip[0]) + "}"
    mip_b = "{" + ",".join(chr(65 + i) for i in mip[1]) + "}"

    print(f"\n  Minimum Information Partition (MIP): {mip_a} | {mip_b}")
    print(f"  Phi = {phi:.6f} bits")

    return phi


# ─────────────────────────────────────────────────────────────────────────────
# EXAMPLE NETWORKS
# ─────────────────────────────────────────────────────────────────────────────


def define_networks():
    """
    Define four example networks that illustrate how topology affects Phi.

    Returns a list of (name, description, weight_matrix) tuples.
    """
    networks = []

    # 1. Chain: A -> B -> C (feedforward — information flows one way)
    #    Expected: Low Phi. The system can be decomposed because information
    #    only propagates forward; cutting at any link preserves local dynamics.
    chain = np.array([
        [0.0, 1.0, 0.0],  # A sends to B
        [0.0, 0.0, 1.0],  # B sends to C
        [0.0, 0.0, 0.0],  # C sends to nobody
    ])
    networks.append((
        "Chain (A -> B -> C)",
        "Feedforward: information flows only forward. Expect LOW Phi.",
        chain,
    ))

    # 2. Cycle: A -> B -> C -> A (recurrent loop with self-connections)
    #    Expected: Higher Phi. Each node influences and is influenced by others
    #    through the loop, creating integrated dynamics.
    #    Self-connections + loop create richer cross-partition dependencies.
    cycle = np.array([
        [0.5, 1.0, 0.0],  # A sends to B (and weak self)
        [0.0, 0.5, 1.0],  # B sends to C (and weak self)
        [1.0, 0.0, 0.5],  # C sends back to A (and weak self)
    ])
    networks.append((
        "Cycle (A -> B -> C -> A)",
        "Recurrent loop: each node affects every other via the cycle. Expect HIGHER Phi.",
        cycle,
    ))

    # 3. Fully connected: every node connects to every other node
    #    Expected: Highest Phi. Maximum causal integration — every node
    #    directly influences every other node.
    fully_connected = np.array([
        [0.5, 1.0, 1.0],  # A sends to B and C (+ self)
        [1.0, 0.5, 1.0],  # B sends to A and C (+ self)
        [1.0, 1.0, 0.5],  # C sends to A and B (+ self)
    ])
    networks.append((
        "Fully Connected (A <-> B <-> C <-> A)",
        "Every node connects to every other. Expect HIGHEST Phi.",
        fully_connected,
    ))

    # 4. Disconnected: three independent nodes (no connections)
    #    Expected: Phi = 0. No integration at all — the system IS the sum
    #    of its parts, because the parts don't interact.
    disconnected = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ])
    networks.append((
        "Disconnected (A  B  C)",
        "No connections. The system IS the sum of its parts. Expect Phi = 0.",
        disconnected,
    ))

    return networks


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  COMPUTING PHI: Integrated Information Theory in Practice")
    print("=" * 70)
    print()
    print("  Phi measures how much a system is 'more than the sum of its parts.'")
    print("  A system with high Phi cannot be decomposed into independent pieces")
    print("  without losing information about its causal dynamics.")
    print()
    print("  This simplified computation uses mutual information between subsystems")
    print("  to approximate the integrated information lost at each partition.")
    print("  Full IIT uses cause-effect repertoires and Earth Mover's Distance.")
    print()
    print("  Computational complexity: checking all bipartitions is O(2^n),")
    print("  making exact Phi computation NP-hard for large systems.")
    print()

    networks = define_networks()
    results = []

    for idx, (name, description, weights) in enumerate(networks):
        print("-" * 70)
        print(f"  Network {idx + 1}: {name}")
        print(f"  {description}")
        print("-" * 70)
        print()

        # Build TPM from weight matrix
        tpm = build_tpm_from_weights(weights, threshold=0.5, noise=0.1)

        # Compute Phi
        phi = compute_phi(tpm, name)
        results.append((name, phi))
        print()

    # ── Summary ──
    print("=" * 70)
    print("  SUMMARY: Phi Values by Network Topology")
    print("=" * 70)
    print()
    print(f"  {'Network':<42} {'Phi (bits)':>10}")
    print(f"  {'-'*42} {'-'*10}")

    for name, phi in results:
        bar = "#" * int(phi * 40)  # Simple visual bar
        print(f"  {name:<42} {phi:>10.6f}  {bar}")

    print()
    print("  Key takeaways:")
    print("  - Feedforward (chain) networks have low Phi: they can be decomposed")
    print("    into stages without losing much information.")
    print("  - Recurrent networks (cycles) have higher Phi: information circulates,")
    print("    creating irreducible causal dependencies.")
    print("  - Fully connected networks have the highest Phi: every node directly")
    print("    constrains every other, maximizing integration.")
    print("  - Disconnected networks have Phi near zero: they ARE the sum of")
    print("    their independent parts.")
    print()
    print("  According to IIT, consciousness is identical to integrated information.")
    print("  A system is conscious to the degree that it has high Phi -- meaning")
    print("  it generates more information as a whole than its parts do separately.")
    print()


if __name__ == "__main__":
    main()
