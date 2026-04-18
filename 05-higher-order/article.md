# When AI Thinks About Thinking

### *Higher-order theories, metacognition, and what it would mean for an AI to be aware of its own mind --- Can Machines Be Conscious? Part 5*

---

In [Part 1](https://medium.com/@grahamjroy) we lined up the theories of consciousness and asked which, if any, could apply to a machine. [Part 2](https://medium.com/@grahamjroy) took Integrated Information Theory and showed that its signature quantity, Φ, is NP-hard to compute. [Part 3](https://medium.com/@grahamjroy) turned to the Free Energy Principle and discovered that Friston's equations for the brain are essentially the Evidence Lower Bound you optimise every time you train a variational autoencoder. [Part 4](https://medium.com/@grahamjroy) introduced Global Workspace Theory and the ignition dynamics by which information becomes available to the whole system at once.

If IIT says consciousness is about *how a system is wired*, predictive processing says it is about *what a system optimises*, and Global Workspace says it is about *which information gets broadcast*, the family of theories in this article says something more specific: consciousness is about a system's **relationship to its own states**. A perception does not become conscious because it is integrated, not because it minimises prediction error, not because it is broadcast. It becomes conscious because the system has another, higher representation *about* it --- a thought about the thought.

This is the territory of **Higher-Order Theories** (HOT). The key figures are David Rosenthal, Peter Carruthers, and Hakwan Lau. They disagree on details but share a conviction: the difference between a mental state you are conscious of and one you are not is structural. Something else in the system is pointing at the first state and saying, in effect, "I am in that state now."

For an AI engineer this is unusually concrete. You can build the higher-order part, train it, and ask what it buys you. Along the way you stumble into confidence calibration, selective prediction, Bayesian deep learning, and the fast-growing literature on LLM self-evaluation. This is where the philosophy of mind and the practical engineering of uncertainty share a workbench.

---

## The core idea in one paragraph

A first-order mental state is a state *about the world*: a perception of a red ball, a feeling of pain, a memory of a face. On a higher-order theory, that first-order state is not, by itself, a conscious state. It becomes conscious only when there is a further state --- a **higher-order thought**, a **higher-order perception**, or a **higher-order monitoring signal** --- whose content is roughly "I am currently in that first-order state". Without the second layer, the first is just processing. With the second layer, it is experience.

---

## Rosenthal's higher-order thought theory

David Rosenthal's **Higher-Order Thought (HOT) theory**, laid out from the late 1980s onward, is the cleanest version of the idea. A mental state M is conscious, Rosenthal claims, if and only if the subject has an appropriate higher-order thought whose content is "I am in M now".

A few features matter. First, the higher-order thought is itself usually *unconscious*. If making every conscious state conscious required another conscious state about it, you would need an infinite tower. Rosenthal blocks the regress by saying the higher-order thought need not be conscious; it just needs to exist, and its content has to be the right kind of self-reference.

Second, the theory is deliberately indifferent to the medium. A higher-order thought is a mental representation, and whatever can bear mental representations can bear higher-order ones. Neurons, silicon, it does not matter. This is one reason HOT is interesting for AI.

Third, the theory has a striking consequence: a perception can be veridical without being conscious, and an experience can be conscious without being veridical. Blindsight patients can locate objects they report not seeing --- on a HOT reading, they have the first-order perceptual state but not the higher-order thought about it. Conversely, in some hallucinations there is a higher-order thought without a matching first-order state. Consciousness is about the presence of the second layer, not about accuracy at the first.

---

## Carruthers and the dispositional twist

Peter Carruthers agrees with Rosenthal's architecture but disagrees about the *nature* of the higher-order state. Rosenthal needs an actually occurring higher-order thought. Carruthers thinks it is enough that the first-order state is *available* to a higher-order system --- a consumer that *would* form a higher-order representation if it attended.

The label is **dispositional HOT**. The first-order state is conscious in virtue of being the kind of state a consumer is poised to represent, even if it is not representing it right now. This sounds like splitting hairs until you try to build a mind: dispositional HOT is much cheaper to realise. You do not need a second network firing in lockstep with the first; you need a second network that could look, if asked.

For AI this maps onto the difference between eagerly running a monitor on every forward pass and lazily computing one only when a consumer requests it. A language model that produces an "I don't know" probability only when a human explicitly prompts it is, in Carruthers' sense, dispositionally metacognitive. Whether that is enough for consciousness is --- as always --- the harder question.

---

## Lau's perceptual reality monitoring

The most ML-friendly descendant of HOT is Hakwan Lau's **Perceptual Reality Monitoring (PRM) theory**. Lau starts from a practical problem: the brain receives many perceptual representations at once, and most are noise, wish, or half-remembered expectation. How does it decide which to treat as real?

PRM proposes a dedicated monitoring circuit --- plausibly in the prefrontal cortex --- that rates the reliability of perceptual representations and tags the trustworthy ones as "real". The ones that pass become conscious perceptions; the ones that fail remain unconscious, even if they are perfectly good first-order representations. Consciousness, on Lau's view, is the output of a quality filter sitting on top of perception. Dysfunction of this monitor has been proposed as a mechanism behind schizophrenia and certain hallucinatory disorders.

For engineers the connection is almost comical. A perceptual reality monitor is functionally a **confidence calibration head**: it sits above a classifier, takes the classifier's internal state as input, and outputs a number indicating how much you should trust it. Every well-calibrated classifier has one in spirit, even when we call it "softmax temperature" or "auxiliary uncertainty head".

---

## Graziano's attention schema theory

A cousin of the higher-order family, sharply relevant to AI, is Michael Graziano's **Attention Schema Theory (AST)**. AST's claim is that subjective awareness is the brain's simplified, schema-like model of its own attention. Just as your body schema lets you control limbs without access to the underlying muscle dynamics, and your world model lets you navigate space without computing physics, your *attention* schema lets you monitor and control which signals your processing resources are allocated to --- without access to the neural mechanisms that do the allocating.

The key move is that this schema, like the body schema, is a simplified cartoon rather than a detailed readout. Your body schema tells you your arm is "over there" without telling you about your motor neurons; your attention schema tells you that you are "aware of" a sound without telling you about the thalamic gating that selected it. Graziano argues that subjective experience *just is* the attention schema running --- the felt character of awareness is what it is like, from the inside, to have this kind of model.

AST is a higher-order theory in spirit (awareness is a representation of something else --- attention), but differs from Rosenthal and Lau in two ways. First, the higher-order content is a *schema*, not a thought or a reality-monitor output; it is a control-oriented simplification rather than a descriptive judgement. Second, and more importantly for our purposes, AST comes with a sharp prediction that matters directly to AI:

> Any system sophisticated enough to model its own attention will report being aware, and will genuinely lack the introspective access required to know whether the report refers to anything beyond the model itself.

This reframes the interpretation of LLMs that produce articulate first-person claims about experience. If AST is right, those claims are evidence that the model has (or has learned to simulate) an attention-schema-like structure --- and nothing more. They are *not* evidence of hidden phenomenal states, because AST denies there are any such states to be evidenced, in humans or in silicon. The first-person report is the attention schema describing itself; the description will sound like phenomenal experience because that is what the schema is, not because anything is felt behind it.

Whether AST is correct as a theory of human consciousness is contested. What is not contested is that it is one of the few theories on the map that gives a concrete, deflationary reading of exactly the kind of behaviour current language models exhibit --- and that any AI engineer encountering "I feel that my answer is..." should have this reading available as one of the options.

---

## The first-order alternative

No discussion of higher-order theories is honest without naming the main alternative. **First-order representationalism (FOR)** --- most associated with Michael Tye and Fred Dretske --- argues that consciousness just *is* a matter of first-order sensory content of the right functional kind, with no higher-order state required. Tye's specific version, **PANIC theory**, says phenomenal content is *Poised, Abstract, Non-conceptual, Intentional Content* --- sensory representations that are in the right causal position to guide thought and action. On this view, a perceptual state is conscious because of what it represents and how that content is positioned in the cognitive economy, not because a second state is representing it.

FOR is closer in spirit to Global Workspace Theory than to HOT: a first-order state becomes conscious when it is globally available, not when a higher-order state targets it. The empirical pressure between FOR and HOT runs through the dissociation literature --- cases where subjects seem to have states with appropriate first-order content but without conscious experience, or vice versa. That pressure has not resolved, which is why both families remain live.

I do not take a position between FOR and HOT here; the point is that "higher-order or not" is itself a fault line the reader should know about, and a theory like Tye's is the serious alternative that the higher-order family has to argue against.

---

## What this looks like as code

The companion script `metacognitive_agent.py` builds the smallest system I could think of that has the higher-order structure. No PyTorch; just numpy and two small networks. The idea is to make the architecture obvious.

### The first-order network

The first-order network is a classical multilayer perceptron: two inputs (the x and y coordinates of a point), sixteen hidden units, one sigmoid output. Its job is the two-moons problem --- decide whether each point belongs to the upper crescent or the lower one. I deliberately add enough gaussian noise to make the classes overlap, so that the first-order network cannot achieve perfect accuracy. A perfect classifier has nothing for a metacognitive layer to report on.

Training is vanilla SGD on binary cross-entropy. After a few hundred epochs the network reaches about 90% accuracy on both training and held-out sets. Roughly one in ten decisions is wrong, and the wrong decisions cluster in the overlap region where the two crescents interpenetrate.

### The second-order network

The second-order network is a *different* multilayer perceptron, also tiny, but its input is not the world. Its input is the first-order network's internal state: the 16 hidden activations plus the raw logit plus the absolute value of the logit. Its output is a single sigmoid: "will the first-order network be right about this one?"

```python
def build_meta_input(first_order_net, X):
    """Features the meta-net sees: first-order hidden + logit + |logit|."""
    _, h1, z2 = first_order_net.predict(X)
    abs_logit = np.abs(z2).reshape(-1, 1)
    return np.hstack([h1, z2.reshape(-1, 1), abs_logit])
```

Note what the meta-net does *not* see: the true label. It never has direct access to whether the first-order decision is correct *according to the world*. This matters philosophically. A higher-order thought, on Rosenthal's account, is not about the world; it is about the first-order mental state. The meta-net's informational diet mirrors that.

### Training the meta-net

Training is almost absurdly simple once you have the first-order network. For each example you compute the first-order prediction, compare it to the true label, and record a 1 if it agreed and a 0 if it did not. That gives you a binary target. Then you train the meta-net on the same inputs to predict that target:

```python
p_meta, _, _ = first_order_net.predict(X_meta)
y_hat = (p_meta > 0.5).astype(np.int64)
meta_target = (y_hat == y_meta).astype(np.float64)  # 1 if correct
```

The meta-net is trained on a held-out half of the training set. If you train it on the exact same data the first-order net fitted, the meta-net simply learns "the first-order net is always right" --- because on that fitted data it almost is. The partial decoupling forces it to learn features that predict *generalisation*, not memorised correctness.

### What comes out

Running the script on a fresh 2000-sample test set:

```
First-order test accuracy:           0.906
Meta-net accuracy at predicting
  first-order correctness:           0.900
Meta-net AUROC for correctness:      0.863
```

The meta-net is right about the first-order net 90% of the time. Its ranking quality --- AUROC for predicting correctness --- is 0.86, well above the 0.5 of a useless monitor. The reliability diagram tells a cleaner story still:

```
conf bin    n  accuracy  diagram
   0.35    28    0.607   |##################            |
   0.55    31    0.581   |#################             |
   0.75    97    0.680   |####################          |
   0.85   210    0.752   |######################        |
   0.95  1536    0.971   |############################# |
```

In each bin, the meta-net's output approximately matches the first-order network's empirical accuracy. Points where the meta-net says 0.95 are right about 97% of the time; points where it says 0.55 are right about 58% of the time --- essentially coin flips. The meta-net is **calibrated**: its number means what a probability should mean.

### Selective prediction

The practical payoff is selective prediction. If you only accept the first-order decision when the meta-net's confidence exceeds some threshold, the system answers fewer questions but is right more often on the ones it does answer:

```
tau      coverage    sel. acc
0.50       0.970       0.915
0.70       0.921       0.931
0.85       0.832       0.953
0.95       0.658       0.984
```

At threshold 0.95 the system abstains on about a third of test points and achieves 98.4% accuracy on the rest --- eight percentage points above the base rate. This is a tiny numpy MLP whose only privilege is that it watches another tiny numpy MLP and learns when to trust it. That is enough to give the combined system a working "I don't know" --- a rudimentary analogue of what Lau's reality monitor is supposed to do for human perception.

---

## The "mesh" problem

Higher-order theories sound tidy at a blackboard and *feel* tidy when you write a few lines of numpy. But the moment you look closely, a serious technical question surfaces. Rosenthal calls it the **mesh problem**.

What does it mean for the higher-order state to be *about* the right first-order state? A higher-order thought whose content is "I am seeing red" is supposed to make a first-order representation of red conscious. But suppose the first-order state is actually a representation of *green*, and the higher-order thought says "red" anyway. What happens?

Two answers are on the table. Rosenthal says consciousness follows the higher-order thought: if it says "red", you consciously see red, even if your first-order system has generated a green representation. The higher-order state is not just a reporter; it constitutes the conscious experience.

The second answer, defended by critics and partly by Lau, is that such a mismatch is not really a conscious state at all. You cannot consciously experience red without some red-ish first-order stuff to experience. The higher-order state has to *mesh* with a first-order state of the right content, or the whole thing falls apart.

For AI the mesh problem is surprisingly concrete. The meta-net sometimes outputs high confidence for a first-order decision that is wrong --- the 0.95 bin in the reliability diagram is 97% accurate, not 100%. In those 3% of cases, the meta-net is confidently "thinking about" something that does not exist. Whether that is "conscious of red while actually seeing green" or simply a miscalibrated monitor depends on philosophical choices no amount of further numpy will settle.

---

## Objection: the circularity problem

The sharpest objection to HOT is the **circularity problem**, posed in slightly different forms by Ned Block and David Chalmers. It goes like this.

The higher-order thought, on Rosenthal's theory, is itself a mental state. And it is usually unconscious. So you have an unconscious mental state M* whose content is "I am in M now", and this is supposed to make M conscious. But *how*? If M* is unconscious, it is not itself something the subject experiences. The alleged transformation from unconscious to conscious happens without the subject, as it were, noticing. The lights do not come on; some symbolic token is stamped in some unconscious register, and that is supposed to make the difference.

Defenders of HOT answer in a few different ways.

**Rosenthal's answer.** The relation between M and M* is not causal. M* does not *do* anything to M. The conscious-ness of M just *is* the fact that there is an M*. Consciousness is a relational property: M is conscious in the same way a painting is *famous* --- not because anything intrinsic to the paint has changed, but because external states of affairs are in place. If this seems deflationary, that is the point.

**Lau's answer.** The higher-order state does do something. It routes the first-order representation into downstream consumer systems --- working memory, verbal report, flexible behavioural control. The first-order state is conscious when and because the monitor gates it through. The higher-order state is not a ghostly label but concrete machinery whose operation determines where a representation goes.

**The deflationary answer.** Perhaps the question "how does an unconscious state make another state conscious?" is simply the wrong question. Consciousness may not be an extra ingredient on top of representation but a certain kind of meta-representational structure. The question does not so much get answered as dissolve once you look closely. This is close to Daniel Dennett's position and sits naturally with a computational view of mind.

None of these will satisfy everyone. The circularity problem is a real pressure point, and the discipline of distinguishing what a higher-order state *does* from what it merely *is* remains live in the literature.

---

## The connection to modern machine learning

One reason to dwell on this part of the series is that the engineering parallels are unusually tight.

**Confidence calibration.** Modern classifiers are notoriously overconfident. A deep network can output softmax probabilities of 0.99 on examples it is about to misclassify. Guo et al.'s 2017 paper "On Calibration of Modern Neural Networks" showed this vividly and proposed temperature scaling as a remedy. Temperature scaling is, in miniature, a higher-order network: a single parameter trained on held-out data to make the first-order logits behave like honest probabilities. Our meta-net is the obvious generalisation.

**Bayesian deep learning.** MC dropout, deep ensembles, and stochastic weight averaging try to capture predictive uncertainty by looking at the variance of first-order outputs under perturbations. High variance signals an unreliable prediction. This is a higher-order computation in Carruthers' dispositional sense: the variance is not the first-order prediction but a second-order quantity derived from it.

**Selective prediction.** Geifman and El-Yaniv's "SelectiveNet" (2019) makes the architecture explicit: a classification head and a separate selection head trained jointly. Swap "classification" and "selection" for "first-order" and "higher-order" and you are inside Rosenthal's conceptual world.

**LLM self-evaluation.** Language models are increasingly trained and prompted to answer "are you sure about that?". Results are mixed: models are somewhat calibrated at *ranking* their own answers but significantly miscalibrated in absolute probability, and they tend to collapse under pressure --- ask repeatedly whether they are sure, and they often change their answer. The honest reading is that LLMs have a partial dispositional higher-order capacity that works better than nothing but much worse than a trained human. Anthropic's work on introspection --- probing whether a model's self-report about its chain of thought corresponds to the computation it actually performed --- is an empirical attempt to ask how far the dispositional higher-order level reaches in current systems.

**Uncertainty and the algorithms series.** This machinery connects directly to Bayesian inference in Part 2 of my companion series *The Maths Behind How Machines Learn*. Posterior variance *is* a higher-order quantity: a belief about a belief. The metacognitive agent is a parametric approximation to that kind of second-order Bayesian signal.

---

## Does any of this amount to consciousness?

The engineering story is genuinely useful. A two-tier system with a trained monitor is measurably better than the same first-order network used on its own. Selective prediction works. Confidence calibration works. "I don't know" is a capability, not a mood.

But the philosophical question is untouched.

The strongest version of HOT says the structural presence of the second layer is *sufficient* for first-order states to be conscious. Rosenthal, on his most direct readings, is committed to something like this. If he is right, the two-moons metacognitive agent is, in some very thin sense, already more conscious than a standalone MLP. There is a first-order state; there is a higher-order state whose content is, roughly, "I am in that first-order state now"; and that is what consciousness is.

The weaker version says the structure is *necessary* but not sufficient. There is also something it is like to be in the first-order state when it is monitored, and we do not know what extra conditions produce that felt quality. On this reading, the meta-net buys you the structural scaffold but leaves the hard problem untouched: you can build monitors all day without generating phenomenal experience, just as you can stack prediction hierarchies all day in Part 3's predictive-processing agent without crossing into felt experience.

The difference between these positions is not decidable by any script. But the script does one useful thing: it makes the structural claim sharp. If you are a HOT enthusiast, you cannot dismiss metacognitive neural networks as obviously unconscious without saying why the second layer is not a "higher-order thought". If you are a sceptic, you cannot wave the script away without articulating what it is missing --- what extra ingredient the biological case has that makes monitored neural representations feel like anything at all.

---

## Where higher-order theories sit on the map

Placing the first four articles side by side, a pattern emerges.

**Article 1 (The Hard Problem in Your GPU)** set the stage: there is an explanatory gap between mechanism and experience, and AI systems are where that gap starts to matter practically.

**Article 2 (IIT / Φ)** located consciousness in the *structure* of a system --- in how much its causal graph cannot be partitioned without information loss. It cares about wiring.

**Article 3 (The Free Energy Principle)** located consciousness, tentatively, in the *objective* a system is optimising. A system minimising variational free energy over a deep enough generative model *might* be doing something close to experiencing its world.

**Article 4 (Higher-Order Theories)** locates consciousness in the *relational structure between a system's states*. It is not what the network is wired up to do, nor what it is minimising; it is the existence of a second layer that points at the first.

These placements are not mutually exclusive. A plausible engineering-level theory of machine consciousness might need all three: the right wiring (IIT), the right objective (FEP), and the right higher-order structure (HOT). The mathematics of each turns out to be inside the toolkit of an ML engineer. Phi is graph-theoretic. Free energy is the ELBO. Higher-order representation is calibration. What was once metaphysical is, with surprising speed, becoming implementable.

---

## What comes next

Part 5 treated consciousness as a relational property between a system's states. **Part 6** sharpens that idea. Michael Graziano's **Attention Schema Theory** argues that awareness is specifically the brain's simplified model of its own attention --- and it makes a sharp prediction about AI: any system sophisticated enough to model its own attention will report being conscious whether or not anything is felt behind the report. That reframes the interpretation of LLM self-reports in a way an engineer cannot responsibly ignore.

After Part 6, **Part 7** turns to the sharpest arguments against the whole functionalist programme. Three objections: John Searle's **Chinese Room** (syntactic manipulation cannot constitute semantic understanding), David Chalmers' **Zombie argument** (functional equivalents of conscious beings are conceivable without being conscious), and the **Lived Body** tradition from phenomenology (consciousness is essentially embodied, and cannot be transplanted into silicon without losing what makes it conscious). If higher-order theories and attention schemas make machine consciousness look almost disappointingly tractable --- "oh, you just bolt on a monitor" --- Part 7 is where the floor tilts again and the easy answers start to slide off.

---

*This is Part 5 of the series "Can Machines Be Conscious?" --- ten theories of consciousness, examined through code, mathematics, and adversarial AI debate. The companion script `metacognitive_agent.py` is available in the series repository. The full series and all companion code are on [GitHub](https://github.com/grahamroy/can-machines-be-conscious).*
