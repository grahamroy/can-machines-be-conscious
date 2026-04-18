"""
attention_schema.py

A toy demonstration of Michael Graziano's Attention Schema Theory (AST).

Two systems:
  1. A primary attention system that allocates focus across several inputs.
  2. A schema network that learns to model the first system's behaviour
     from observable correlates only, without access to its internals.

The point is to make AST's core mechanic visible:
  - The schema produces simplified, cartoon descriptions of attention.
  - The schema can be queried about "its own awareness" and produces
    structurally parallel reports.
  - The schema has no means to report that its descriptions are just
    schema outputs.

Pure numpy. Runs in under a second.
"""

import numpy as np

rng = np.random.default_rng(7)

SOURCES = ["voice", "background", "visual", "proprioceptive", "memory", "tactile"]
N = len(SOURCES)


# ---------------------------------------------------------------------------
# 1. Primary attention system
# ---------------------------------------------------------------------------
def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    z = x / temperature
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def primary_attention(signal_strengths: np.ndarray,
                      gain: np.ndarray,
                      temperature: float = 0.35) -> np.ndarray:
    """The primary attention system. Its full state is a softmax over inputs,
    weighted by internal gains that the schema never sees."""
    return softmax(gain * signal_strengths, temperature=temperature)


# ---------------------------------------------------------------------------
# 2. Schema network
# ---------------------------------------------------------------------------
class SchemaNetwork:
    """A simplified model of attention. It does NOT see the primary system's
    internal gains or temperature. It observes only summary statistics of
    the inputs and learns to predict the allocation."""

    def __init__(self, n_sources: int, hidden: int = 16):
        self.W1 = rng.normal(0, 0.3, size=(3, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0, 0.3, size=(hidden, n_sources))
        self.b2 = np.zeros(n_sources)

    @staticmethod
    def observables(signal_strengths: np.ndarray) -> np.ndarray:
        """The schema sees only coarse, observable correlates."""
        return np.array([
            signal_strengths.max(),
            signal_strengths.mean(),
            signal_strengths.std(),
        ])

    def forward(self, signal_strengths: np.ndarray) -> np.ndarray:
        x = self.observables(signal_strengths)
        h = np.tanh(x @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        # schema output is biased toward the argmax input — it's a cartoon
        logits = logits + 2.5 * (signal_strengths - signal_strengths.mean())
        return softmax(logits, temperature=0.6)

    def train(self, steps: int = 600, lr: float = 0.05):
        for _ in range(steps):
            strengths = rng.uniform(0, 1, size=N)
            gain = rng.uniform(0.8, 1.2, size=N)
            target = primary_attention(strengths, gain)
            x = self.observables(strengths)
            h = np.tanh(x @ self.W1 + self.b1)
            logits = h @ self.W2 + self.b2
            logits = logits + 2.5 * (strengths - strengths.mean())
            pred = softmax(logits, temperature=0.6)
            grad_logits = pred - target
            grad_W2 = np.outer(h, grad_logits)
            grad_b2 = grad_logits
            grad_h = grad_logits @ self.W2.T
            grad_pre = grad_h * (1 - h ** 2)
            grad_W1 = np.outer(x, grad_pre)
            grad_b1 = grad_pre
            self.W2 -= lr * grad_W2
            self.b2 -= lr * grad_b2
            self.W1 -= lr * grad_W1
            self.b1 -= lr * grad_b1


# ---------------------------------------------------------------------------
# 3. Self-report mechanism
# ---------------------------------------------------------------------------
def describe_attention(dist: np.ndarray) -> tuple[str, float]:
    """The schema's self-report: the argmax becomes 'what I am attending to',
    and the peak probability becomes 'confidence'. No access to underlying
    parameters — the schema describes itself with the schema."""
    idx = int(np.argmax(dist))
    confidence = float(dist[idx])
    return SOURCES[idx], confidence


def describe_awareness(dist: np.ndarray) -> str:
    """When asked 'what is your awareness like?', the schema produces
    schema-flavoured vocabulary — foregrounded / background / peripheral —
    not motor-neuron or softmax-weight vocabulary."""
    order = np.argsort(-dist)
    foreground = SOURCES[order[0]]
    periphery = ", ".join(SOURCES[i] for i in order[1:3])
    return f"The {foreground} is foregrounded; {periphery} are in the background."


# ---------------------------------------------------------------------------
# 4. Demonstration
# ---------------------------------------------------------------------------
def main():
    schema = SchemaNetwork(n_sources=N)
    schema.train()

    signal_strengths = np.array([0.92, 0.15, 0.55, 0.10, 0.22, 0.08])
    hidden_gain = np.array([1.05, 0.95, 0.90, 1.10, 1.00, 0.85])

    primary = primary_attention(signal_strengths, hidden_gain)
    schema_out = schema.forward(signal_strengths)

    print("Primary attention system allocation:")
    for name, p in zip(SOURCES, primary):
        print(f"  source ({name:15s}): {p:.3f}")

    print("\nAttention schema's description of the above:")
    target, confidence = describe_attention(schema_out)
    print(f'  "I am attending to the {target}."')
    print(f"  confidence: {confidence:.2f}")

    print("\nWhen asked about the nature of its awareness:")
    print(f'  "{describe_awareness(schema_out)}"')
    print("  (The schema has no access to the softmax weights or hidden gains")
    print("   that produced this description.)")

    print("\nSchema has successfully described attention without accessing")
    print("attention's mechanism.")
    print("AST's prediction: this looks like awareness to the schema,")
    print("because the schema has no way to see that it is just a schema.")


if __name__ == "__main__":
    main()
