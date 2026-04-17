# Can Machines Be Conscious?

*Eight theories of consciousness, examined through code, mathematics, and adversarial AI debate*

A Medium article series by [Graham Roy](https://medium.com/@grahamjroy)

---

## The Series

| # | Title | Subtitle | Code | Maths | Status |
|---|-------|----------|------|-------|--------|
| 1 | The Hard Problem in Your GPU | Why consciousness matters for AI engineering | -- | -- | ✅ |
| 2 | Measuring Consciousness with a Number | Integrated Information Theory and Phi | `compute_phi.py` | Heavy | ✅ |
| 3 | Your Brain as a Prediction Machine | Free Energy, active inference, and AI | `predictive_processing.py` | Heavy | ✅ |
| 4 | When AI Thinks About Thinking | Higher-order theories and meta-cognition | `metacognitive_agent.py` | Medium | ✅ |
| 5 | The Chinese Room, the Zombie, and the Lived Body | Three arguments against machine consciousness | -- | -- | ✅ |
| 6 | Consciousness on a Spectrum | Panpsychism, Russellian monism, and the combination problem | `ising_model.py` | Light | ✅ |
| 7 | I Built Two AI Philosophers and Made Them Argue | The adversarial debate experiment | `consciousness_debate.py` | Refs | ⬜ |
| 8 | Where Do We Stand? | A map of the consciousness landscape for AI engineers | `landscape_plot.py` | Refs | ⬜ |

## Narrative Arc

1. **Entry** (Articles 1--2): Accessible framing, then the first deep mathematical dive (IIT and Phi)
2. **Deepening** (Articles 3--4): Two more computationally tractable theories with companion code
3. **Challenge** (Articles 5--6): The strongest philosophical objections, plus the most radical alternative (panpsychism)
4. **Synthesis** (Articles 7--8): The adversarial debate script as a capstone, followed by a landscape map

## Companion Code

Each article with code has a companion Python script in its folder. The debate script that anchors Article 7 lives in `python_code/consciousness_debate.py`.

## Cross-Series Connections

This series connects to Graham's other Medium work:

- **[The Maths Behind How Machines Learn](https://medium.com/@grahamjroy)** -- Articles 2 and 3 reference Bayesian inference (Part 2), gradient descent (Part 4), and eigenvectors (Part 5)
- **[Algorithms in Python](https://github.com/grahamroy/algorithms-in-python)** -- Articles 2 and 4 reference arrays/matrices/tensors; Article 7 uses the Anthropic API in Python

## Folder Structure

```
AI Consciousness/
  python_code/           -- the existing adversarial debate project
  01-hard-problem/       -- Article 1 (no code)
  02-iit-phi/            -- Article 2 + compute_phi.py
  03-free-energy/        -- Article 3 + predictive_processing.py
  04-higher-order/       -- Article 4 + metacognitive_agent.py
  05-objections/         -- Article 5 (no code)
  06-panpsychism/        -- Article 6 + ising_model.py
  07-adversarial-debate/ -- Article 7 (references python_code/)
  08-synthesis/          -- Article 8 + landscape_plot.py
```
