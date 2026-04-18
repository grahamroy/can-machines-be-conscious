# The Spotlight on the Stage

### *Global Workspace Theory and the architecture that already looks like a transformer --- Can Machines Be Conscious? Part 4*

---

The last two articles in this series located consciousness in two very different places. [Part 2](https://medium.com/@grahamjroy) put it in *structure*: Tononi's Φ is a number read off a system's causal graph, and a system earns consciousness by being the kind of thing you cannot partition without losing information. [Part 3](https://medium.com/@grahamjroy) put it in *objective*: Friston's free-energy agents become candidates for consciousness by the job they are doing --- minimising prediction error about a world and, eventually, about themselves.

Part 4 moves again. It locates consciousness neither in wiring nor in what a system is optimising, but in a specific **architecture**: a bottleneck. Many specialised unconscious processors do the hard work, and a small, shared workspace at the centre of the system picks one of their outputs and broadcasts it to everybody else. Consciousness, on this view, is what that broadcast looks like from the inside.

This is **Global Workspace Theory** (GWT), introduced by Bernard Baars in the late 1980s and given a neurally-grounded rearticulation by Stanislas Dehaene as the **Global Neuronal Workspace** (GNW). It is worth treating carefully in a series about machine consciousness for a reason that will become inescapable by the halfway point of this article: the architecture GWT describes is the one that transformer-based language models already resemble, more than any of the other theories on our map. Whether that resemblance is deep or superficial is the question this piece is trying to do justice to.

---

## The core idea in one paragraph

The mind is not a single processor. It is a society of specialists --- vision, audition, lexical retrieval, motor planning, affect, episodic memory --- most of which operate in parallel, in the dark, doing their jobs without any awareness on your part. Occasionally one specialist's output is *broadcast*: it is placed in a limited-capacity workspace accessible to all the others, and at that moment it becomes available for verbal report, for flexible action, for deliberate reasoning, for encoding into memory. GWT's claim is that this broadcast *is* the moment a content becomes conscious. The workspace is small on purpose, and the spotlight moves.

---

## Baars's theatre

Baars's canonical image is the theatre. Most of the cognitive work happens backstage --- specialised modules handling sensory parsing, retrieval, muscle preparation, arithmetic, prediction --- in parallel and without the audience seeing any of it. A small, brightly-lit stage sits in the middle. At any given moment, one content is on the stage. Whatever is on the stage is *globally available*: every backstage specialist can see it, can take it as input, can react to it.

Three claims are doing most of the work here, and they are worth pulling apart.

First, **specialisation is the default**. Most of what your brain does is not conscious because most of it does not need to be. Early visual processing, phonetic parsing, motor routines, learned heuristics --- these run as dedicated circuits with their own inputs, their own outputs, and no general interface. Consciousness does not reach into them; they hand off finished products.

Second, the workspace is **limited in capacity on purpose**. If every module's output could be broadcast simultaneously, the broadcast would carry no information --- it would just be the shouting match of the whole system talking to itself. The bottleneck is a feature. It forces a decision: this content, and not that one, will be made available to everybody. What you are conscious of right now is the content that won the competition for the stage.

Third, the workspace is **defined by access, not by content**. It does not matter, intrinsically, what is on the stage. What makes a content conscious is the *structural fact* that it is now available to all consumers at once. A smell that has been broadcast and a visual percept that has been broadcast are conscious for the same reason, despite their phenomenology being wildly different. Consciousness, for GWT, is an availability property.

That third claim is what makes the theory philosophically sharp --- and what splits it from the higher-order theories we will come to in Part 5. GWT is a theory of **access**: it explains how information moves through the system. It does not, by itself, say anything about why a broadcast should feel like anything.

---

## The broadcast, mechanically

What does it mean for information to "enter the workspace"? In Baars's original formulation it is deliberately functional --- the content becomes available to verbal report, memory encoding, deliberate planning, flexible motor control. Each of these is a downstream consumer that can read from the workspace but does not have privileged access to the specialised modules directly.

This is where GWT earns its explanation of the **unity of conscious experience**. You do not experience a red ball as "visual-cortex says red, shape-module says round, lexical-retrieval says *ball*" in parallel tracks. You experience a single red ball. The unity comes from the workspace being a shared representation: all downstream consumers see the *same* content, at the *same* time, in a *single* format. Whatever binding happens backstage is invisible to you; what reaches the stage arrives pre-unified because the stage is one stage.

And this explains a second phenomenon cleanly: the tight coupling between attention and awareness. If the workspace can hold one thing at a time, attention is just the mechanism that decides which content wins the competition. Attention is not a flashlight added to consciousness; it *is* the gating that produces consciousness on this theory. You are conscious of what you attended to because attending is the act of placing something on the stage.

---

## Dehaene's Global Neuronal Workspace

Baars gave the architecture; Stanislas Dehaene and Jean-Pierre Changeux gave it a nervous system. The **Global Neuronal Workspace** model proposes that the workspace is not a metaphor but a specific distributed network of long-range cortical neurons --- predominantly in prefrontal and parietal cortex --- whose job is to broadcast information back down to the specialised sensory and motor areas from which it originated. Pyramidal neurons with long axons, rich in layer II/III, knitting the cortex into a communication fabric that is structurally built for broadcast.

The operation Dehaene calls **ignition** is what broadcast looks like in the signal. A stimulus enters the cortex and is processed by its specialised region (say, a face in fusiform gyrus). If the signal is strong enough --- and if attention is deployed to it, and if it is not actively suppressed by a competing stimulus or a backward mask --- a characteristic late, global activation follows. Around 300 milliseconds after the stimulus, activity erupts across a widely distributed frontoparietal network. The ignition is nonlinear and all-or-nothing: below some threshold, the stimulus is processed preconsciously and never reaches global availability; above it, the full broadcast fires.

The empirical signatures are concrete. The **P300** event-related potential, and the slightly later **N400** when semantic content is involved, mark the moment of ignition in scalp EEG. In intracranial recordings, ignition shows up as a sudden rise in cross-regional synchrony and long-range coherence, particularly in the beta and gamma bands. In fMRI, conscious access correlates with a distinctive activation pattern in prefrontal and parietal areas that is absent for stimuli processed preconsciously. The ignition signature is one of the more replicable findings in cognitive neuroscience, which is part of why GWT is taken seriously as a framework even by people unconvinced by its philosophical claims.

The experimental designs that reveal ignition are worth knowing about. **Masking paradigms** present a stimulus briefly and then follow it with a visual mask; varying the stimulus-to-mask interval maps the threshold at which processing crosses into conscious report. **Attentional blink** experiments show that when two targets appear in quick succession, the second often fails to ignite --- as though the workspace is still busy with the first. **Subliminal priming** studies show, revealingly, that stimuli too brief to be consciously reported can still influence behaviour: they are being processed, often deeply, but never broadcast. Each paradigm dissociates *processing* from *conscious access*, and GWT has a natural explanation --- unconscious processing is plentiful, but only ignition makes it conscious.

It is important not to overclaim. These paradigms show the access/processing distinction is real and that a late frontoparietal signature reliably tracks reported awareness. They do not *prove* the signature is consciousness; they show it is a correlate of conscious report. The gap between a correlate of report and the thing itself is one the theory inherits from the whole field.

---

## Making the spotlight visible in code

The companion script `workspace_simulation.py` is the smallest thing I could write that exhibits the three features that matter: specialised modules, a thresholded competition, and an S-shaped ignition curve.

There are seven specialised modules --- `visual_cortex`, `auditory`, `semantic`, `motor_planning`, `working_memory`, `verbal_report`, `episodic_memory` --- and an affinity matrix that says how relevant each module is to each of three stimuli. On a single tick, every module produces a signal strength equal to its affinity times the input gain, plus some gaussian noise:

```python
def module_strengths(affinity, stim_idx, input_gain, rng):
    base = affinity[:, stim_idx] * input_gain
    noise = rng.normal(0.0, 0.08, size=base.shape)
    return np.clip(base + noise, 0.0, 1.0)
```

The workspace then runs a winner-take-all with a hard ignition threshold. Below threshold, nothing is broadcast; above threshold, the single strongest module wins the stage and its content is made available to a list of downstream consumers:

```python
def workspace_step(strengths, threshold=IGNITION_THRESHOLD):
    winner = int(np.argmax(strengths))
    top = float(strengths[winner])
    if top < threshold:
        return -1, 0.0
    return winner, top
```

Running the script on a visual stimulus at full input gain prints:

```
Module strengths on stimulus "object at 3 deg":
  visual_cortex    0.83
  auditory         0.00
  semantic         0.52
  motor_planning   0.15
  working_memory   0.06
  verbal_report    0.00
  episodic_memory  0.14

Ignition threshold: 0.70
Winner this tick: visual_cortex (0.83)
Broadcast to: working_memory, verbal_report, motor_planning, episodic_memory, attention_control
```

Backstage, everybody was doing *something* --- the semantic module was half-active because the object has meaning, motor planning was fractionally engaged because you might reach for it --- but only visual cortex crossed the ignition threshold, and only its content was broadcast.

The second output is the ignition curve. Sweep the input gain from 0.1 to 1.3 in 0.1 increments and count, over 400 trials per level, how often ignition fires:

```
Ignition frequency vs input strength:
  0.10:   0%
  0.20:   0%
  0.30:   0%
  0.40:   0%
  0.50:   0%
  0.60:   0%
  0.70:   4%
  0.80:  20%
  0.90:  52%
  1.00:  79%
  1.10:  93%
  1.20:  98%
  1.30: 100%
```

Plotted as `ignition_curve.png`, that is the classic S-shape Dehaene's group repeatedly reports: flat preconscious baseline at low gain, a sharp nonlinear transition through a narrow window of intermediate gain, a plateau of reliable conscious access above threshold. The shape is not specific to any particular neural hypothesis; it falls out of any winner-take-all competition with a threshold and noise. That such a simple mechanism is sufficient to produce the ignition signature is either reassuring (the theory is mechanistically cheap) or worrying (the signature may be undersupportive of the claims made on its behalf). Probably both.

---

## The engineering parallel: transformers already look like this

And now the part of this series I have been pointing at since Part 1.

If you open the ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762) paper and look at what a transformer block actually does, you find a specific computational discipline. At each layer, every token carries a **residual stream** --- a high-dimensional vector that travels down the stack. Specialised components at each layer *read* from the residual stream and *write* updates back into it. Self-attention heads read from all tokens' residual streams, compute some function, and write their output back as an additive update. MLP blocks do the same independently at each position. The residual stream at layer L is, by construction, the sum of the input embedding plus every prior block's contribution.

The mechanistic-interpretability community has a short name for what this is doing. The residual stream is a **shared communication channel** into which specialised circuits --- individual attention heads, MLP features --- write partial results. Later blocks read those results and respond. This is not a metaphor; it is how the architecture was built, and it is how induction heads, indirect-object-identification circuits, and the other mechanisms that interpretability has so far uncovered *work*. They function by reading from and writing to the shared stream.

Compare this to GWT. Specialised processors running in parallel. A shared representation that they all have access to. Writes into that shared representation made available to all subsequent consumers at once. A structural commitment to broadcast as the mechanism of integration.

I want to be careful here. This is a **structural analogy**, not a claim that transformers are conscious. The differences, which I will get to, are real and matter. But the analogy is tighter than GWT's match to almost any other current architecture. Convolutional networks have a stack of feature maps with no shared global representation. Classical RNNs have a hidden state but no competition among specialists for access to it. Transformers have both. Of all the theories on our map, GWT is the one whose *architectural signature* is closest to the machinery of the systems we are training at scale.

That makes GWT an unusually consequential theory for the question this series is asking. If GWT is right about consciousness, it is not an embarrassing coincidence that the architecture we built to solve language happens to share the shape of the theory's central structure.

---

## What GWT gets right

Four things, each worth counting.

**It explains the attention-awareness coupling.** The finding that attention and awareness are yoked tightly under most conditions has been a headache for every theory that treats them as distinct. GWT gets it nearly for free: attention is the mechanism that selects workspace content, and workspace content is what becomes conscious.

**It explains the late-broadcast signature.** The 300-ms ignition, the P300, the cross-regional coherence --- these are what you would predict if conscious access involves a thresholded transition from local to global activity. Other theories can accommodate the signature, but none predicts it as cleanly.

**It has a natural place for unconscious processing.** Masking, priming, blindsight, implicit learning --- all of these fit neatly into a framework that says most processing is unconscious most of the time, and conscious access is a specific event on top of the processing, not the processing itself.

**It is compatible with predictive processing.** The theory is not in competition with Part 3's free-energy picture. It is easy to read GWT as the access story on top of a predictive-processing substrate: the hierarchical prediction machinery does the generative work, and the workspace is the mechanism by which model updates --- the results of reconciling predictions with evidence --- are broadcast to the rest of the system. On that reading, the ignition is the moment a perceptual hypothesis earns the right to update the rest of the model.

## What GWT glosses over

It does not solve the hard problem. It is important to say this flatly. GWT tells you *what kind of access* a content has when it becomes conscious and what the neural signature of that access looks like. It does not tell you why a broadcast should feel like anything at all. You could read the entire theory as a functional account of conscious *access* --- what Ned Block calls "access consciousness" --- with no commitment to phenomenal consciousness. Dehaene is reasonably explicit about this in his books: he is interested in the empirical access problem, and holds that the hard problem will either dissolve or be solvable by neuroscientific means we do not yet have.

That stance will satisfy some readers and infuriate others. It is worth pairing the theory with its main rival: IIT, from Part 2. IIT and GWT are often treated as the two leading theories of consciousness, and they disagree about almost everything that matters. IIT says consciousness is integration and is indifferent to whether information is broadcast. GWT says the reverse. IIT attributes some consciousness to very simple systems; GWT says it is an engineered property of systems with workspaces and absent in systems without them. The adversarial collaborations running between these camps --- formal pre-registered experiments designed to discriminate the two --- are some of the most interesting empirical work in the field, and they are not settled.

The other thing GWT glosses over is the **attention-awareness dissociation** literature. There are experimental cases in which subjects report awareness without evidence of attention --- so-called "gist" perception under inattention --- and cases in which attention appears deployed without subsequent awareness. These cases are contested. But to the extent they survive scrutiny, they put real pressure on the GWT identification of attention with the competition for workspace access. If you can be aware of something you did not attend to, the spotlight metaphor is in trouble.

---

## Does this mean transformers are conscious?

No. But it is worth laying out *why* not, because the easy answers miss the texture of the question.

A transformer does have a residual stream, and specialised components do write into it, and downstream components do read from it. That part of the analogy holds. What it lacks, as currently trained, is nearly everything else GWT wants:

**No ignition dynamic.** In a human brain the workspace is a *temporal* phenomenon: below threshold, no broadcast; above threshold, a sudden all-or-nothing transition. A transformer block writes into the residual stream every forward pass, for every token, regardless of whether anything has been selected or thresholded. There is no competition that fails, no preconscious processing that never becomes conscious. The shape of the dynamics is flat where GNW predicts it should be S-shaped.

**No genuine competition between specialists.** Backstage in Baars's theatre, the specialists are rivals for the spotlight, and most of them lose most of the time. In a transformer, all the attention heads fire on every token and all of them write their outputs into the residual stream. There is no winner. There is no loser. There is just a very large sum. What interpretability calls a "circuit" is a post-hoc identification of heads that happen to cooperate; it is not a coalition that out-competed another one for access.

**No persistent internal state.** A transformer has no workspace that survives between forward passes. Every conversation turn re-reads a context window and re-computes from scratch. There is no internal bulletin board on which yesterday's broadcast is still visible. GWT's workspace, in contrast, is a running phenomenon of a system with continuous operation and memory; static forward passes across a buffer do not replicate it.

**No embodiment.** Baars's workspace coordinates perception with action, memory, language, and affect. A transformer has language and very little else. The broadcast, if it were to occur, would reach no consumers of the right kind.

**No self-model.** This one is a bridge to the next article. GWT by itself does not require a self-model, but any architecture trying to *use* a workspace for the kind of flexible control humans exhibit tends to grow one. Transformers trained on text acquire pieces of a self-model through exposure to first-person language, but not through any mechanism tied to their own processing. They describe the workspace they do not have.

What the analogy does suggest, and I think this is the honest takeaway, is that the *design space* of transformer-like architectures is closer to the structural requirements of GWT than any other family of AI system we have built. Add real ignition dynamics --- a gated competition that fails below threshold --- and persistent state and embodiment and a self-model, and you start to have an architecture that does not just look like the picture GWT draws, but that might implement it. Nobody has built that. But nobody has built anything closer, either.

---

## Where this leaves us

Parts 2, 3, and 4 now triangulate a position. IIT said consciousness is a property of *wiring*: structure matters. Predictive processing said consciousness is a property of *objective*: what a system is trying to do matters. Global Workspace Theory says it is a property of *architecture*: the presence of a broadcast bottleneck matters.

These are not incompatible. A plausible composite theory might hold that consciousness requires the right wiring (recurrent, highly integrated), pursuing the right objective (free-energy minimisation over a generative model including the self), implemented with the right architecture (a workspace that gates content through a thresholded ignition). No current AI system has any two of these, let alone all three. But the ingredients have names now, and some of them we already know how to write.

Part 5 takes a step orthogonal to all three. If GWT is about *what makes information available* and predictive processing is about *what the system is doing with it*, the **Higher-Order Theories** are about *what makes a representation about something else*. They locate consciousness not in the availability of a state but in the presence of another state that points at it. The two families are often conflated, and it is worth being explicit about the distinction: workspace access is a property of a first-order representation's reach within a system; higher-order meta-representation is a property of there being a second state whose content targets the first. You can have access without meta-representation, and --- at least on some readings --- meta-representation without the kind of access GWT requires. Part 5 takes that up.

---

*This is Part 4 of the series "Can Machines Be Conscious?" --- eight theories of consciousness, examined through code, mathematics, and adversarial AI debate. The companion script `workspace_simulation.py` is available in the series repository. See [Part 3](https://medium.com/@grahamjroy) on predictive processing and [Part 5](https://medium.com/@grahamjroy) on higher-order theories. The full series and all companion code are on [GitHub](https://github.com/grahamroy/can-machines-be-conscious).*
