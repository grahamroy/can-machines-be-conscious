# Consciousness Debate: Adversarial AI Agents

Two Claude agents argue opposing positions on whether artificial systems can achieve genuine phenomenal consciousness, structured around 8 major theories of consciousness.

## How It Works

Each round focuses on a specific theory. The structure per round is:

1. **Professor Turing** (FOR) — argues how the theory supports machine consciousness
2. **Professor Searle-Thompson** (AGAINST) — counters with why it doesn't
3. **Professor Turing** (rebuttal) — responds to the counter-arguments
4. **Moderator** — analyses the round, identifies the crux, and poses a sharpening question

After all rounds, a **final synthesis** maps each theory onto the debate landscape and identifies unresolved fault lines.

## Theories Covered

| # | Theory | Key Thinkers |
|---|--------|-------------|
| 0 | Integrated Information Theory (IIT) | Tononi |
| 1 | Global Workspace Theory (GWT) | Baars, Dehaene |
| 2 | Higher-Order Theories (HOT) | Rosenthal, Lau, Brown |
| 3 | Biological Naturalism | Searle |
| 4 | Phenomenology & Embodied Cognition | Merleau-Ponty, Varela, Thompson |
| 5 | Predictive Processing & Active Inference | Friston, Clark, Hohwy |
| 6 | Panpsychism & Russellian Monism | Chalmers, Goff, Strawson |
| 7 | Attention Schema Theory (AST) | Graziano |

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

```bash
# Run all 8 theory rounds (will take a while and use significant tokens)
python consciousness_debate.py --output debate.md

# Run specific theories only (e.g., IIT, Searle, and Panpsychism)
python consciousness_debate.py --rounds 0,3,6 --output debate.md

# List available theories
python consciousness_debate.py --list-theories

# Use a different model
python consciousness_debate.py --model claude-opus-4-20250514 --rounds 0,1 --output debate.md
```

## Token Usage Estimate

Each round involves ~4 API calls. With 8 theories, that's ~32 calls plus the final synthesis.
Rough estimate for all 8 rounds with Sonnet: ~80-100k input tokens, ~40-50k output tokens.

Running just 2-3 theories is a good starting point to test the output quality.

## Customisation Ideas

- **Add theories**: Add entries to the `THEORIES` list (e.g., Orchestrated Objective Reduction / Penrose-Hameroff)
- **Adjust depth**: Change `max_tokens` or temperature in `agent_respond()`
- **Add rounds**: Extend the per-theory exchange (e.g., add Agent ANTI rebuttal)
- **Change agents**: Modify system prompts to represent specific philosophers more faithfully
- **Structured output**: Ask agents to return JSON with argument, concessions, and confidence levels
