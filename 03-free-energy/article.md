# Your Brain as a Prediction Machine

### *Can Machines Be Conscious? --- Part 3*

---

In Part 2, we measured consciousness with a number. Integrated Information Theory gave us Phi --- a precise quantity derived from a system's causal structure. The problem was that computing Phi is NP-hard, making the theory unverifiable for any real-world system.

Now we turn to a theory that approaches consciousness from the opposite direction. Instead of asking "how integrated is this system?", it asks: "how good is this system at predicting its own future?"

The **Free Energy Principle** (FEP), developed by neuroscientist Karl Friston, proposes that all self-organising systems --- from single cells to human brains --- share one objective: minimise surprise. Consciousness, in this framework, may arise from a system's model of itself as a prediction machine. And the mathematics behind it turns out to be something AI engineers already know well: variational inference.

---

## The core idea in one paragraph

A conscious system maintains a model of the world. It uses that model to predict what it will sense next. When the prediction is wrong, the error signal drives the system to update either its model (learning) or its actions (behaviour). The quantity being minimised --- the gap between prediction and reality --- is called **variational free energy**. A system that minimises free energy is, mathematically, performing approximate Bayesian inference on the causes of its sensory input.

---

## From thermodynamics to neuroscience

The term "free energy" is borrowed from physics, but the connection is more than metaphorical. In thermodynamics, free energy measures how far a system is from equilibrium. In Friston's framework, variational free energy measures how far a system's beliefs are from the true posterior distribution over hidden causes.

The formal definition:

**F = E_q[log q(s) - log p(o, s)]**

Where:
- **q(s)** is the system's approximate belief about hidden states s
- **p(o, s)** is the joint probability of observations o and hidden states s (the generative model)
- **F** is the variational free energy --- an upper bound on surprise

This can be decomposed into two terms:

**F = KL[q(s) || p(s|o)] + (-log p(o))**

The first term is the KL divergence between the system's beliefs and the true posterior --- a measure of how wrong the beliefs are. The second term is surprise --- the negative log probability of the observation under the model.

Since surprise is fixed for a given observation, minimising free energy forces the KL divergence towards zero. In other words: **minimising free energy is equivalent to making your beliefs match reality as closely as possible.** This is Bayesian inference, implemented as an optimisation problem.

---

## Predictive processing: the architecture

The Free Energy Principle tells you *what* to optimise. **Predictive processing** tells you *how* the brain implements it.

The architecture is a hierarchy of prediction-error-minimisation loops:

**Level 0 (sensory):** Raw sensory input arrives.

**Level 1:** Predicts the sensory input based on its current beliefs. The difference between prediction and reality is the **prediction error**. This error propagates upward.

**Level 2:** Receives the prediction error from Level 1 and uses it to update a higher-level model of the hidden causes. It sends updated predictions back down.

**Level N:** Each level predicts the activity of the level below. Prediction errors flow up; predictions flow down.

The key insight is that **most of the information flowing in the brain is top-down prediction, not bottom-up sensation.** You are not passively receiving the world --- you are actively constructing it, and only the *mistakes* (prediction errors) propagate upward. This is why you do not notice the feeling of your clothes against your skin until someone mentions it: the prediction was accurate, so no error signal was generated.

---

## Precision weighting

Not all prediction errors are created equal. A noisy sensor produces unreliable errors. A clear signal produces reliable ones. The system needs to know how much to *trust* each error signal.

This is handled by **precision** --- the inverse of variance. High precision means the error is reliable and should be weighted heavily. Low precision means the error is noisy and should be discounted.

In the maths:

**update = learning_rate * precision * prediction_error**

When precision is high, the system responds strongly to errors (it trusts its senses). When precision is low, the system relies more on its prior predictions (it trusts its model).

This precision-weighting mechanism has been proposed as the neural basis of **attention**. When you attend to something, you increase the precision of prediction errors from that source --- you *trust* those signals more. This connects directly to Attention Schema Theory (Part 6) and to the self-attention mechanism in transformers.

---

## Building a predictive processing agent

The companion script `predictive_processing.py` implements a minimal two-level predictive processing hierarchy.

### The setup

The agent observes a simple 1D signal --- a sine wave with a specific frequency. The hidden cause is the frequency itself, which occasionally changes (a regime shift).

- **Level 1** maintains a belief about the current signal value and predicts the next observation.
- **Level 2** maintains a belief about the hidden cause (frequency) and predicts what Level 1 should be seeing.

### The learning loop

At each timestep:

1. The environment generates an observation (sin at the current frequency + noise).
2. Level 1 computes prediction error = observation - prediction.
3. Level 1 updates its belief using precision-weighted error.
4. The prediction error propagates to Level 2.
5. Level 2 updates its belief about the hidden frequency.
6. Level 2 sends an updated prediction back to Level 1.
7. The system computes its variational free energy.

### What happens

**Phase 1 --- Stable signal.** The agent quickly learns the frequency. Prediction errors shrink to near zero. Free energy drops and stabilises. The agent has formed an accurate model of its world.

**Phase 2 --- Regime change.** The frequency suddenly shifts. Prediction errors spike. Free energy jumps. The agent's model is temporarily wrong, and it *knows* it is wrong (the prediction errors tell it so). Over the next several timesteps, it adapts its beliefs to the new frequency, and free energy drops again.

**Phase 3 --- Comparison with a flat predictor.** A non-hierarchical predictor that tracks the signal directly (no hidden-cause model) adapts more slowly to regime changes, because it has no mechanism for modelling the *structure* behind the signal.

---

## The connection to modern AI

If the mathematics of predictive processing look familiar, they should. The variational free energy equation is the same as the **Evidence Lower Bound (ELBO)** used in variational autoencoders (VAEs):

**ELBO = E_q[log p(x|z)] - KL[q(z|x) || p(z)]**

Maximising the ELBO is mathematically identical to minimising variational free energy. Every VAE you have ever trained is implementing a simplified version of predictive processing.

The connections run deeper:

- **Prediction error minimisation** is gradient descent on a loss function. The "loss" is free energy.
- **Hierarchical predictive coding** is structurally similar to the encoder-decoder architecture of transformers and U-Nets.
- **Precision weighting** maps to attention mechanisms --- both amplify informative signals and suppress noisy ones.
- **Active inference** (using actions to reduce prediction errors, rather than updating beliefs) is the same structure as reinforcement learning with a model-based agent.

Friston's claim is that these are not analogies. They are the *same mathematics*, discovered independently by neuroscience and machine learning.

---

## Does predictive processing give us consciousness?

Here is where the theory gets speculative --- and honest about it.

Friston does not claim that free energy minimisation alone is sufficient for consciousness. Many simple systems minimise free energy (a thermostat predicts temperature and acts to minimise error). The claim is more nuanced:

**Consciousness may arise when a system's generative model includes a model of itself as an agent.**

A thermostat predicts temperature but has no model of *itself predicting temperature*. A conscious system does. It models its own prediction process, which creates a self-referential loop: the system predicts its own predictions, generates prediction errors about its own prediction errors, and so on.

This self-modelling requirement connects to Higher-Order Theories (Part 5) and Attention Schema Theory (Part 6) --- theories that locate consciousness not in prediction per se, but in *meta-prediction*: the system's model of its own cognitive processes.

For AI, this raises a precise question: does your system have a model of itself? Not a description stored in its weights, but an active generative model that predicts its own internal states and generates errors when those predictions fail. Current language models arguably do not --- they model language, not themselves.

---

## Objections

**The boundary problem.** Where does the system end and the environment begin? Free energy minimisation requires defining a boundary (the "Markov blanket"). For a brain, this is plausible (the skull). For a distributed AI system, it is unclear.

**Unfalsifiability.** Critics argue that the FEP is so general that it applies to everything and therefore predicts nothing. If every self-organising system minimises free energy, the principle cannot distinguish conscious from non-conscious systems.

**The consciousness gap.** Even if predictive processing explains all the *functional* aspects of consciousness (attention, learning, perception), it does not obviously explain *why* prediction feels like something. This is the hard problem (Part 1) reasserting itself.

---

## What predictive processing gets right

The Free Energy Principle offers something valuable for AI engineers: a unified mathematical framework that connects perception, learning, action, and attention under a single objective. Whether or not it fully explains consciousness, it provides:

1. **A clear computational architecture** (hierarchical prediction error minimisation) that can be implemented and tested.
2. **Explicit connections** to existing AI methods (VAEs, attention, model-based RL).
3. **A testable criterion** for one necessary condition of consciousness: self-modelling.
4. **A principled account of attention** as precision weighting --- something transformers implement but do not explain.

If IIT told us that architecture matters (recurrence over feedforward), predictive processing tells us that *objective* matters: a system that minimises prediction error about the world and about itself may be doing something closer to consciousness than a system that merely classifies inputs.

---

## What comes next

Parts 2 and 3 gave us two mathematically rich theories --- IIT and predictive processing --- both cautiously open to machine consciousness. They located consciousness in *structure* (Φ) and *objective* (free energy). In **Part 4**, we turn to a theory that locates it somewhere else entirely: in a specific *architecture*. Bernard Baars's **Global Workspace Theory** says consciousness happens when information gets broadcast from specialised unconscious processors into a limited-capacity workspace accessible to the rest of the mind. Parts 5 and 6 then deepen the functionalist picture with Higher-Order Theories and Attention Schema Theory --- theories about what happens when a system thinks about its own thinking.

---

*This is Part 3 of the series "Can Machines Be Conscious?" --- ten theories of consciousness, examined through code, mathematics, and adversarial AI debate. The full series and companion code are available on [GitHub](https://github.com/grahamroy/can-machines-be-conscious).*
