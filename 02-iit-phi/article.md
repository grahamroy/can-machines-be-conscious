# Measuring Consciousness with a Number

### *Can Machines Be Conscious? --- Part 2*

---

You finished [Part 1](https://medium.com/@grahamjroy) knowing that the question "is this machine conscious?" has at least eight competing answers. Now we start working through them --- and we begin with the one that tried hardest to be a science.

Integrated Information Theory (IIT), developed by neuroscientist Giulio Tononi, does something no other consciousness theory attempts: it defines a single number --- Phi, written $\Phi$ --- that is supposed to *measure* how conscious a system is. Not whether it acts conscious. Not whether it reports being conscious. How much consciousness it actually has.

The appeal is obvious. If you could compute $\Phi$ for a neural network, you would have a principled answer to the question that opened this series. The catch --- and it is a serious one --- is that computing $\Phi$ exactly is NP-hard. For anything larger than a handful of nodes, the calculation is intractable.

This article unpacks the theory, derives $\Phi$ step by step, and builds a Python script that computes it for small networks. Along the way, we discover something surprising: the theory predicts that most current AI architectures --- including transformers --- have very low $\Phi$, regardless of how intelligent they appear.

---

## The five axioms

IIT starts not from neuroscience but from phenomenology --- the structure of experience itself. Tononi identifies five properties that every conscious experience has:

**Intrinsic existence.** A conscious experience exists from the system's own perspective, not just as described by an external observer.

**Composition.** Experiences are structured. You do not just see "something" --- you see a red ball on a green table, with specific shapes, colours, and spatial relationships all bound together.

**Information.** Each experience is specific. Seeing a red ball is different from seeing a blue cube. The experience specifies which state you are in out of a vast repertoire of possible states.

**Integration.** Experiences are unified. You cannot decompose seeing a red ball into an experience of "red" and a separate experience of "ball" --- it arrives as one thing. This is the property that gives $\Phi$ its name: *integrated* information.

**Exclusion.** There is a definite "grain" to experience. It is neither more nor less than what it is --- not split into sub-experiences, not merged into a super-experience.

Each axiom maps to a corresponding *postulate* about the physical system that realises the experience. The integration axiom maps to $\Phi$.

---

## From axioms to a number

The intuition behind $\Phi$ is simple: if a system is truly integrated, you cannot split it into independent parts without losing information. The more information you lose at the weakest split, the more integrated the system is.

Formalise this in three steps.

### Step 1: Define the system's causal structure

A system has $n$ elements, each in one of two states (on or off). The system's dynamics are defined by a **Transition Probability Matrix (TPM)**: given a current state, what is the probability of each next state?

For a system of $n$ binary elements, there are $2^n$ possible states. The TPM is a $2^n \times 2^n$ matrix where entry $(i, j)$ gives $P(\text{next state} = j \mid \text{current state} = i)$.

### Step 2: Partition the system

Now try to break the system into two parts, $A$ and $B$. After partitioning, each part evolves independently --- there are no causal connections between $A$ and $B$.

The partitioned system has its own TPM: the product of the individual TPMs of $A$ and $B$. Because the cross-connections are severed, this partitioned TPM is generally different from the whole-system TPM.

### Step 3: Measure the information lost

Compare the whole-system TPM with the partitioned TPM. The difference is the **integrated information for that partition** --- the information that exists only because the parts are connected.

The formal measure uses the **Earth Mover's Distance (EMD)** between probability distributions, though for our implementation we will use **KL divergence** as a tractable approximation.

$\Phi$ is then defined as:

$$\Phi = \min_{\text{partition}} D(TPM_{\text{whole}} \| TPM_{\text{partitioned}})$$

The minimum is taken over all possible bipartitions. The partition that achieves this minimum is the **Minimum Information Partition (MIP)** --- the weakest link in the system's integration.

---

## Why this is NP-hard

For a system of $n$ elements, the number of bipartitions grows as a **Stirling number of the second kind**, approximately $\frac{2^{n-1} - 1}{1}$ for bipartitions. For $n = 10$, that is 511 partitions. For $n = 20$, over half a million. For $n = 100$, more than $10^{29}$.

And that is just the partitions. Each partition requires computing a marginalised TPM and a distance metric, both of which scale exponentially in $n$.

A typical GPT-scale transformer has billions of parameters. Computing $\Phi$ for such a system is not merely expensive --- it is computationally impossible with any foreseeable hardware. This is perhaps the most important practical fact about IIT: the theory makes a precise claim about consciousness, but that claim is unverifiable for any system larger than a few dozen elements.

---

## Computing $\Phi$ in Python

Let us build this from scratch. The companion script `compute_phi.py` defines small networks and computes $\Phi$ step by step.

### Defining networks as TPMs

We represent each network as a transition probability matrix. For three binary nodes, the state space is $2^3 = 8$ states (000, 001, 010, ..., 111). Each row of the TPM gives the probability of transitioning to each of the eight possible next states.

```python
def make_chain_tpm():
    """A -> B -> C  (feedforward chain)"""
    tpm = np.zeros((8, 8))
    for state in range(8):
        a, b, c = (state >> 2) & 1, (state >> 1) & 1, state & 1
        # A stays the same, B copies A, C copies B
        new_a = a
        new_b = a
        new_c = b
        next_state = (new_a << 2) | (new_b << 1) | new_c
        tpm[state, next_state] = 1.0
    return tpm
```

A feedforward chain: A drives B, which drives C, but there is no feedback. Each node simply copies the node upstream.

### Enumerating bipartitions

For $n = 3$ nodes, there are three non-trivial bipartitions:

- $\{A\}$ vs $\{B, C\}$
- $\{B\}$ vs $\{A, C\}$
- $\{C\}$ vs $\{A, B\}$

```python
def enumerate_bipartitions(n):
    """All non-trivial bipartitions of n elements."""
    partitions = []
    for mask in range(1, 2**n - 1):
        complement = (2**n - 1) ^ mask
        if mask < complement:  # avoid duplicates
            part_a = [i for i in range(n) if (mask >> i) & 1]
            part_b = [i for i in range(n) if (complement >> i) & 1]
            partitions.append((part_a, part_b))
    return partitions
```

### Partitioning the TPM

When we partition a system into $A$ and $B$, we marginalise each part independently. The partitioned TPM is the outer product of the two marginal distributions:

```python
def partition_tpm(tpm, part_a, part_b, n):
    """Sever connections between part_a and part_b."""
    n_states = 2**n
    partitioned = np.zeros((n_states, n_states))
    for s in range(n_states):
        # marginalise: P_A(future_A | current) and P_B(future_B | current)
        prob_a = marginalise(tpm[s], part_a, n)
        prob_b = marginalise(tpm[s], part_b, n)
        # recombine as independent product
        for sa in range(2**len(part_a)):
            for sb in range(2**len(part_b)):
                full_state = reconstruct(sa, sb, part_a, part_b, n)
                partitioned[s, full_state] = prob_a[sa] * prob_b[sb]
    return partitioned
```

### Computing Phi

Finally, $\Phi$ is the minimum KL divergence across all bipartitions:

```python
def compute_phi(tpm, n):
    """Compute Phi: integrated information."""
    partitions = enumerate_bipartitions(n)
    min_phi = float('inf')
    mip = None
    for part_a, part_b in partitions:
        part_tpm = partition_tpm(tpm, part_a, part_b, n)
        phi = kl_divergence(tpm, part_tpm)
        if phi < min_phi:
            min_phi = phi
            mip = (part_a, part_b)
    return min_phi, mip
```

---

## What the numbers tell us

Running the script on our four example networks:

### 1. Disconnected nodes --- $\Phi = 0$

Three independent nodes with no connections. The system can be perfectly partitioned with zero information loss. This is the baseline: no integration, no consciousness.

### 2. Feedforward chain --- $\Phi \approx 0$ (very low)

$A \to B \to C$. Information flows in one direction. Although B depends on A and C depends on B, cutting the chain at any point preserves most of the information in each part. The system is barely integrated.

This is the IIT prediction that matters most for AI. A feedforward neural network --- and a transformer is, in its forward pass, feedforward --- has low $\Phi$ regardless of how many layers it has or how intelligent its outputs are.

### 3. Cycle --- $\Phi > 0$ (moderate)

$A \to B \to C \to A$. Now information flows in a loop. Cutting any connection severs a feedback pathway, and information is genuinely lost. The system is integrated.

### 4. Fully connected --- $\Phi$ (highest)

$A \leftrightarrow B \leftrightarrow C \leftrightarrow A$. Every node influences every other node. No partition can avoid severing multiple connections. This topology maximises integrated information.

---

## The IIT verdict on current AI

IIT makes a striking prediction: **most current AI architectures are not conscious**, no matter how intelligent they appear.

The reasoning:

1. Transformers process information in a feedforward sweep during inference. The self-attention mechanism creates rich information flow within a layer, but the forward pass from input to output is directional.

2. Feedforward architectures have low $\Phi$ by definition. Information is not *integrated* across the whole system --- it flows from input to output without the recurrent feedback that IIT requires.

3. Even recurrent neural networks (RNNs, LSTMs) may have low $\Phi$ if their recurrence is shallow or if the feedback connections carry little causal information.

The implication is that consciousness, for IIT, is about *architecture*, not about capability. A system could pass every intelligence benchmark while having $\Phi \approx 0$. Conversely, a simple recurrent circuit with strong feedback could have significant $\Phi$ while being useless at any cognitive task.

This decoupling of intelligence from consciousness is either IIT's deepest insight or its fatal flaw, depending on whom you ask.

---

## Objections

IIT is not without serious critics.

**The complexity objection.** If $\Phi$ is uncomputable for real systems, the theory is unfalsifiable in practice. A theory of consciousness that cannot be applied to the systems we most want to understand --- brains and AIs --- is of limited scientific value.

**The exclusion postulate problem.** IIT says consciousness exists at the spatial and temporal grain that maximises $\Phi$. But this can lead to counterintuitive results: a lookup table implementing any function has $\Phi = 0$ (it is feedforward), even if the function it computes is identical to a conscious system.

**Panpsychist implications.** IIT implies that even simple systems (a thermostat, a logic gate) have some non-zero $\Phi$, and therefore some minimal consciousness. Whether this is a feature or a bug is a matter of philosophical taste --- we will return to this in Part 6 when we discuss panpsychism.

**Scott Aaronson's reductio.** The computer scientist Scott Aaronson constructed a simple system (a grid of XOR gates) that IIT assigns very high $\Phi$, despite having no plausible claim to consciousness. Tononi responded that the theory's postulates prevent this, but the exchange highlighted the difficulty of calibrating $\Phi$ against intuition.

---

## What IIT gets right

Despite these objections, IIT contributes something no other theory does: a precise, mathematical framework for asking about consciousness. Even if $\Phi$ is not the final answer, the approach --- start from phenomenology, derive mathematical postulates, make testable (in principle) predictions --- sets a standard that other theories should aspire to.

For AI engineers, the key takeaway is structural. If IIT is even partially correct, then the architecture of a system matters for consciousness in ways that go beyond its input-output behaviour. Two systems with identical capabilities could differ in consciousness depending on how their internal causal structure is organised.

This is not an idle observation. If we ever need to answer the question "is this system conscious?" with practical confidence, we will need something like $\Phi$ --- a measure derived from the system's internal structure, not just its behaviour.

---

## What comes next

IIT gave us a number. In **Part 3**, we turn to a theory that gives us an *equation*: Karl Friston's Free Energy Principle. Where IIT measures integration, predictive processing proposes that consciousness arises from a system's drive to minimise surprise --- and the maths connects directly to the variational inference that powers modern generative AI.

---

*This is Part 2 of the series "Can Machines Be Conscious?" --- eight theories of consciousness, examined through code, mathematics, and adversarial AI debate. The full series and companion code are available on [GitHub](https://github.com/grahamroy/can-machines-be-conscious).*
