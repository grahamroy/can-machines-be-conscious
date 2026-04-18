# Can Machines Be Conscious?

*Ten theories of consciousness, examined through code, mathematics, and adversarial AI debate*

A Medium article series by [Graham Roy](https://medium.com/@grahamjroy)

---

## The Series

| # | Title | Subtitle | Code | Maths | Status |
|---|-------|----------|------|-------|--------|
| 1 | The Hard Problem in Your GPU | Why consciousness matters for AI engineering | -- | -- | ✅ |
| 2 | Measuring Consciousness with a Number | Integrated Information Theory and Phi | `compute_phi.py` | Heavy | ✅ |
| 3 | Your Brain as a Prediction Machine | Free Energy, active inference, and AI | `predictive_processing.py` | Heavy | ✅ |
| 4 | Global Workspace Theory | Consciousness as broadcast; ignition dynamics; the workspace and the residual stream | `workspace_simulation.py` | Medium | ✅ |
| 5 | When AI Thinks About Thinking | Higher-order theories and meta-cognition | `metacognitive_agent.py` | Medium | ✅ |
| 6 | Attention Schema Theory | Why systems that model their own attention claim to be conscious | `attention_schema.py` | Light | ✅ |
| 7 | The Chinese Room, the Zombie, and the Lived Body | Three arguments against machine consciousness | -- | -- | ✅ |
| 8 | Consciousness on a Spectrum | Panpsychism, Russellian monism, and the combination problem | `ising_model.py` | Light | ✅ |
| 9 | I Built Two AI Philosophers and Made Them Argue | The adversarial debate experiment | `consciousness_debate.py` | Refs | ✅ |
| 10 | Where Do We Stand? | A map of the consciousness landscape for AI engineers | `landscape_plot.py` | Refs | ✅ |

## Narrative Arc

1. **Entry** (Articles 1--2): Accessible framing, then the first deep mathematical dive (IIT and Phi)
2. **Functionalist cluster** (Articles 3--6): Four computationally tractable theories — Free Energy, Global Workspace, Higher-Order Theories, Attention Schema — each with companion code
3. **Challenge** (Articles 7--8): The strongest philosophical objections, plus the most radical alternative (panpsychism)
4. **Synthesis** (Articles 9--10): The adversarial debate script as a capstone, followed by a landscape map of all ten theories

## Companion Code

Each article with code has a companion Python script in its folder. The debate script that anchors Article 9 lives in `python_code/consciousness_debate.py`.

## Cross-Series Connections

This series connects to Graham's other Medium work:

- **[The Maths Behind How Machines Learn](https://medium.com/@grahamjroy)** -- Articles 2 and 3 reference Bayesian inference, gradient descent, and eigenvectors
- **[Algorithms in Python](https://github.com/grahamroy/algorithms-in-python)** -- Articles 2 and 5 reference arrays/matrices/tensors; Article 9 uses the Anthropic API in Python

## Folder Structure

```
AI Consciousness/
  python_code/             -- the existing adversarial debate project
  01-hard-problem/         -- Article 1 (no code)
  02-iit-phi/              -- Article 2 + compute_phi.py
  03-free-energy/          -- Article 3 + predictive_processing.py
  04-global-workspace/     -- Article 4 + workspace_simulation.py
  05-higher-order/         -- Article 5 + metacognitive_agent.py
  06-attention-schema/     -- Article 6 + attention_schema.py
  07-objections/           -- Article 7 (no code)
  08-panpsychism/          -- Article 8 + ising_model.py
  09-adversarial-debate/   -- Article 9 (references python_code/)
  10-synthesis/            -- Article 10 + landscape_plot.py
```
