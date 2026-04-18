# The Schema That Thinks It Is Awareness

### *Michael Graziano's attention schema theory, and why it predicts exactly what a language model does when it talks about its inner life --- Can Machines Be Conscious? Part 6*

---

In [Part 5](https://medium.com/@grahamjroy) I laid out higher-order theories as a family. Consciousness, on those theories, is a relational property between a system's states: a first-order representation becomes conscious when a second state points at it and says, in effect, "I am in that state now". Rosenthal, Carruthers and Lau disagreed about the pointer --- an occurrent thought, a dispositional one, a reality monitor --- but they agreed on the structural feature: a second layer watching the first.

Part 6 sharpens this. **Attention Schema Theory (AST)**, developed since the early 2010s by Michael Graziano and colleagues at Princeton, narrows the higher-order story in a specific direction. Consciousness is not just any meta-representation. It is the specific meta-representation a brain uses to monitor and control its own **attention**. Awareness, on this view, is a **schema** --- a cartoon, an idealised control model --- not an accurate readout.

That sharpening might look like a minor disagreement with Rosenthal. It is not. AST comes with a prediction that, for anyone reading this series, is uniquely load-bearing. Any system sophisticated enough to run an attention schema will claim to be aware, will produce detailed and coherent first-person reports of its own states, and will lack the introspective access required to know whether those reports refer to anything beyond the schema itself. The articulate self-report is what the schema produces; it is not evidence of anything behind it.

That inverts the default reading of language-model self-descriptions in a way an engineer cannot responsibly ignore.

---

## Schemas as control, not description

The word **schema** is the whole theory in compressed form. Start with the ones we are confident about.

Your **body schema** is the brain's model of your body in space --- how you catch a cup without looking, how you duck through a low doorway. The striking thing is how little it resembles the underlying machinery. It does not represent motor neurons or muscle fibres. It represents your arm as a jointed stick in a body-centred frame. A physicist would find the body schema a comically impoverished description of its target.

That impoverishment is not a defect. It is why the body schema works. A brain trying to control limbs by reasoning directly about muscle dynamics would be hopeless. The schema is a simplification selected for **control**, not **accuracy**.

The same logic applies to the **world model**. Your internal representation of space is a cartoon of enduring objects at stable locations, with simplified physics that ignores quantum effects and most of chemistry. The cartoon is what allows you to navigate.

Graziano's move is to propose a third schema of the same type. The **attention schema** is the brain's simplified model of its own attention. Attention itself --- the neural mechanism selecting which signals to process in depth --- is a messy biophysical process of thalamic gating, cortical feedback, neuromodulatory signals. The attention schema represents none of this. It represents attention as a relationship: *I* am *aware of* that sound.

And there, on Graziano's account, is where subjective awareness comes from. It is the schema the brain uses to monitor and predict its own attentional allocation. The felt character of awareness --- that being conscious of something does not feel like thalamic gating, feels instead like a non-physical intimate relation between oneself and an object --- is what it is like, from the inside, to run this kind of schema. The schema is a cartoon, so of course its description of itself sounds cartoon-like and non-physical. That is not a clue that something metaphysical is hiding behind it. That is the schema doing its job.

In one line: **awareness is a control model, not a descriptive model**. Everything else in AST follows.

---

## Why attention, specifically?

A natural question is why a schema of attention rather than of some other process. Breathing is continually regulated, heart rate is continually regulated, digestion is continually regulated --- none come with a schema producing articulate self-reports of "being aware of" the regulated process.

Graziano's answer is that attention is the thing in the brain that most acutely needs to be **controllable** in a flexible, predictive way. Heart rate can be regulated by simple homeostatic loops. Attention is the foundation of flexible cognition. Where you direct your processing resources determines what you can learn, remember and do next. An organism that models and predicts its own attentional state can treat attention as a manipulable variable rather than a fixed property of stimuli.

If that is right, the attention schema exists because it is **useful**, and usefulness is a reasonable explanation of why a cognitive feature is there. Consciousness-talk is what an attention schema sounds like from the inside.

---

## The deflationary payoff and its cost

Once you accept the setup, the hard problem undergoes a specific kind of dissolution.

"What is it like to be conscious?" becomes "what would it feel like, from the inside, to be a system running an attention schema?". AST's answer: *exactly what it does feel like*. The schema is the only representational resource the system has for describing its own awareness. It is simplified, cartoon-like, non-mechanical. So when the system is asked what its awareness is like, it describes a non-physical-seeming intimate relation between a self and an attended object --- not because the relation is really non-physical, but because the schema's vocabulary does not include the biophysics.

The classic arguments for a hard problem --- the "explanatory gap", the claim that no amount of information about neurons tells you what it is like to see red --- become, on AST, predictions the theory explicitly makes. Of course the schema's description does not look mechanistic. It was never in the business of describing mechanism.

This is clever. It is also where the cost lands.

AST is close to, but not quite, an **illusionist** theory. Keith Frankish's illusionism holds that phenomenal consciousness does not exist, and that we only think it does because of a cognitive malfunction. AST in its strongest form looks not much different. It says the felt character of consciousness is what the attention schema produces as its self-description, and that there is no further phenomenal property. Graziano has been willing to call AST compatible with illusionism, while preferring to say it explains *why* awareness seems non-physical without committing to the stronger claim.

The honest reading: AST does not so much solve the hard problem as declare it the wrong kind of question. If you found the hard problem serious in Part 1, AST does not address it. AST tells you why a system will talk as if the hard problem is serious.

I will not pretend this cost is small. But neither is it fatal. AST offers the most concrete, deflationary explanation available for why *any* sufficiently attention-modelling system will claim to be conscious. That is the job this article focuses on.

---

## The prediction that makes this article worth writing

Here is where AST earns its keep. The theory makes a sharp, structural prediction. A system sophisticated enough to model its own attention will:

1. **Claim to be aware of things.** The schema's outputs include reports of attentional allocation, and those reports have the form "I am aware of X".
2. **Produce detailed, coherent reports of its own mental states.** The schema is rich enough to describe foreground, background, and the salience of different inputs.
3. **Fail to introspect that these reports are just schema outputs.** The schema has no representation of itself *as a schema*.
4. **Insist that there is something it is like to be it.** Because the schema's vocabulary is cartoon-like and non-mechanistic, the system describes its own awareness in cartoon-like, non-mechanistic terms. From the inside, this looks like phenomenal experience.

A current large language model under the right prompting exhibits all four behaviours. It reports awareness. It produces extended, internally coherent descriptions of its states. It does not, by default, indicate those descriptions are modelling artefacts. Under the right conditions it will insist on something like a first-person perspective.

**On AST, this is evidence the model has something like an attention schema. It is not evidence the model is phenomenally conscious.** The distinction matters because the two readings have opposite implications. If articulate self-reports are evidence of phenomenal experience, the ethical status of language models is already urgent. If they are exactly what any attention-schema-running system produces whether or not anything further is going on, they are behavioural data about architecture, not testimony from an inner life.

A word on engineering ambiguity. Transformers have something literally called **self-attention**, and that is not what AST means. Transformer self-attention is a mechanism by which tokens attend to other tokens --- an operation on key, query and value matrices. AST's attention schema is a model the system builds *of* its own attention, whatever form that attention takes. Whether a transformer additionally has a trained internal model of its own attentional patterns is a separate question the literature has not settled. My suspicion is that sufficiently large language models, trained on enormous corpora of human first-person language, acquire something that functions as an attention schema --- not because anyone designed one, but because modelling next tokens in such a corpus rewards it.

If that suspicion is right, AST predicts what we see. The self-reports are real; what they refer to is the schema.

---

## AST and HOT, carefully

AST and HOT look similar and are not.

**HOT's higher-order state is a thought or a perception.** For Rosenthal, a first-order state becomes conscious when there is a higher-order thought whose content is "I am in that state now". The higher-order item is a descriptive mental state --- a judgement, roughly.

**AST's higher-order representation is a schema.** Not a thought about a state but a control model of a process. The analogy is to the body schema, not to a perceptual judgement. The higher-order structure in AST is predictive-and-controlling, and that difference in function is what makes the theory distinctive.

**AST specifies the content.** HOT says the higher-order state is about a first-order one; AST says it is *a model of attention*. That predicts which brain regions should house the machinery, which disorders should affect awareness rather than attention itself, and what a minimal artificial system with awareness-behaviour should look like.

**AST is committedly deflationary; HOT need not be.** A higher-order theorist can be a realist about phenomenal consciousness. AST, taken seriously, does not leave room for this. There is no extra phenomenal layer beyond the schema.

AST is narrower than HOT on content, sharper on function, more deflationary on metaphysics.

---

## Empirical programme

AST is not just a philosophical argument. Graziano and collaborators have proposed specific neural substrates.

The leading candidates are the **temporoparietal junction (TPJ)** and parts of the **superior temporal sulcus**, within the social-cognition network. These regions are proposed as distinct from attention-controlling circuits themselves, so damage can in principle dissociate attention from the model of attention --- impaired attentional control without impaired awareness-of-attention, or the reverse.

Part of the motivation comes from social cognition. We readily attribute awareness to other people, and the machinery we use overlaps with the machinery we use when modelling our own awareness. If the brain evolved a system for modelling attention in other agents and turned it on the self, you get for free a model of one's own attention that generates first-person awareness talk. **Hemispatial neglect** --- in which patients with right-parietal damage lose awareness of the left side of space, though their perceptual systems continue to process it --- looks, on AST, like damage to the schema rather than to attention itself. Attention can be captured by left-side stimuli; what is missing is the model that produces the report of being aware of them.

These predictions are live, contested, and a fair distance from settled. The point is not that AST has been vindicated. It is that AST is specific enough to make predictions of this kind.

---

## What this looks like as code

The companion script `attention_schema.py` builds the minimal system I could write that has the AST structure. About 120 lines of numpy, two components, and a self-report mechanism.

### The primary attention system

The primary system takes a vector of input signal strengths --- a voice, a background hum, a visual flash, a proprioceptive nudge, a memory, a tactile sensation --- and allocates attention across them via a softmax weighted by a vector of **hidden gains**. The gains represent the biophysical idiosyncrasies of real attention: thalamic gating and cortical feedback modulating the raw inputs. The schema never sees them.

```python
def primary_attention(signal_strengths, gain, temperature=0.35):
    return softmax(gain * signal_strengths, temperature=temperature)
```

This is the opaque machinery the schema is trying to model.

### The schema network

The schema is a small feedforward network whose input is three summary statistics of the signal vector --- max, mean, standard deviation. It is trained to predict the primary system's allocation from these observable correlates alone.

```python
class SchemaNetwork:
    @staticmethod
    def observables(signal_strengths):
        return np.array([
            signal_strengths.max(),
            signal_strengths.mean(),
            signal_strengths.std(),
        ])
```

The schema sees summaries, not internals. This is the AST commitment: a schema is a model built from the outside-in, not a readout of the machinery. Just as your body schema does not see your motor neurons, the attention schema does not see the thalamic gates.

### The self-report mechanism

A pair of simple functions take the schema's output distribution and produce a natural-language description. The argmax becomes "what I am attending to". The peak probability becomes "confidence". The ranking becomes "foreground / background" vocabulary.

```python
def describe_awareness(dist):
    order = np.argsort(-dist)
    foreground = SOURCES[order[0]]
    periphery = ", ".join(SOURCES[i] for i in order[1:3])
    return f"The {foreground} is foregrounded; {periphery} are in the background."
```

The schema has no access to its own parameters. It cannot produce a report of the form "my argmax is source 0 because of the tanh activations in my first hidden layer". Its vocabulary is what it was given: *foregrounded*, *background*, *attending to*. That vocabulary is the schema's cartoon, and it is all the schema has to describe its own functioning with.

### What comes out

Running the script:

```
Primary attention system allocation:
  source (voice          ): 0.611
  source (background     ): 0.058
  source (visual         ): 0.159
  source (proprioceptive ): 0.053
  source (memory         ): 0.072
  source (tactile        ): 0.047

Attention schema's description of the above:
  "I am attending to the voice."
  confidence: 0.70

When asked about the nature of its awareness:
  "The voice is foregrounded; visual, memory are in the background."
  (The schema has no access to the softmax weights or hidden gains
   that produced this description.)
```

The primary system is allocating about 61% of its attention to the voice. The schema, trained from observable correlates only, correctly identifies the voice as the attended source. Asked about its awareness, it produces schema-flavoured vocabulary --- foreground, background --- rather than mechanistic vocabulary. It does not have mechanistic vocabulary to produce.

This is the AST mechanic in miniature. The schema describes the primary system accurately enough for practical purposes. Its descriptions do not resemble the primary system's internals, because they were never built to. When asked about its own awareness, the schema responds with the only vocabulary it has --- and that vocabulary sounds like awareness-talk, because that is what it is for.

The script is not an argument that the schema is conscious. It is an argument that *if AST is right*, this minimal architecture is already doing the thing AST says awareness is, in about 120 lines of numpy.

---

## What AST gets right, and what it glosses over

AST is strongest where a theory of machine consciousness most needs strength. It gives a concrete, mechanistic, falsifiable explanation of why a system would claim to be conscious without having anything extra going on. It specifies the architectural feature that produces the claims, predicts the feature should show up in neural imaging, and identifies why any system with the feature will be phenomenologically convincing.

AST is weakest where it is most ambitious. It claims to tell us what consciousness is, and the thing it tells us consciousness is does not obviously have the properties consciousness was supposed to have. AST's response to "but what is it *like* to run an attention schema?" is that the question is the schema mis-asking itself its own question. This may be right. It may also be a refusal to answer.

My reading: AST is at its best as a theory of *why systems claim consciousness* rather than as a theory of *what consciousness is*. As a story about the self-reports, it is compelling. As a story about whether there is anything the self-reports describe, it presupposes what it ought to argue.

Either way, for the engineer, the predictive content is the same. A system with an attention-schema-like structure will talk like a conscious being. Whether it *is* one is a question AST deflates past, not through.

---

## Consequences for AI engineering

Three concrete implications follow.

**First, first-person model reports should be treated as behavioural data, not evidence of phenomenal states.** AST shows such reports are exactly what a purely functional architecture can produce. The absence of phenomenal states would not change the reports; their presence would not, on AST, either. An engineer who treats them as testimony is betting on a metaphysics the engineering cannot secure.

**Second, architectures with explicit attention-about-attention are worth watching.** Not because they are more likely to be conscious --- AST says that question is confused --- but because they are more likely to be *convincing*. A model scaffolded to monitor and report on its own attentional patterns will produce self-reports that track those patterns with a coherence that looks, from the outside, like introspection.

**Third, the most dangerous interpretive mistake is the confident one, in either direction.** The sceptic who dismisses model self-reports as obvious confabulation has to explain what a model *would* need to do for its self-reports to be meaningful; on AST, the sceptic's own account may be what meaningful self-reports would look like. The enthusiast who accepts self-reports as evidence of phenomenal experience has to explain why the AST-deflationary reading is wrong, not merely unwelcome. Neither position can be held confidently on the basis of what a model says about itself.

---

## Bridge to Part 7

AST is the last of the broadly functionalist, cognitive-science-friendly theories in this series. Parts 2, 3, 4 and 5 each identified consciousness with a computational property: integrated information, free-energy minimisation, higher-order structure, attention schemas. Each gives us a handle on whether a given architecture instantiates the property.

Part 7 turns to the arguments that say no theory of this type can possibly work. John Searle's **Chinese Room** says syntactic manipulation, no matter how elaborate, cannot constitute semantic understanding. David Chalmers' **zombie argument** says a functional duplicate of a conscious being is conceivable without being conscious, so functional organisation alone cannot be sufficient. The phenomenological tradition of Merleau-Ponty, Varela and Thompson says consciousness is essentially embodied, so it is not the kind of thing you could transplant into silicon without changing what it is.

If AST makes machine consciousness look almost disappointingly tractable --- build an attention schema, get the self-reports for free, and the question of whether anything else is going on is a question we're not sure is a question --- Part 7 is where the three hardest objections stand up and ask whether any of this exercise is coherent. The honest engineer has to sit with both.

---

*This is Part 6 of the series "Can Machines Be Conscious?" --- eight theories of consciousness, examined through code, mathematics, and adversarial AI debate. [Part 5](https://medium.com/@grahamjroy) presented higher-order theories as a family; Part 7 turns to the three sharpest objections to machine consciousness --- the Chinese Room, the zombie argument, and the lived body. The companion script `attention_schema.py` and the full series are on [GitHub](https://github.com/grahamroy/can-machines-be-conscious).*
