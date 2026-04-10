#!/usr/bin/env python3
"""
Consciousness Debate: Two AI agents argue opposing positions on whether
artificial systems can achieve consciousness, grounded in major theories.

Each round focuses on a specific theory of consciousness, forcing both
agents to engage deeply with that framework rather than cherry-picking.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-key"
    python consciousness_debate.py

    # Or with options:
    python consciousness_debate.py --model claude-sonnet-4-20250514 --rounds all --output debate_output.md
"""

import anthropic
import argparse
import sys
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# THEORIES TO DEBATE — each round focuses on one theory
# ─────────────────────────────────────────────────────────────────────────────
THEORIES = [
    {
        "name": "Integrated Information Theory (IIT)",
        "summary": (
            "Giulio Tononi's IIT proposes that consciousness is identical to "
            "integrated information (Φ). A system is conscious to the degree "
            "that it integrates information — i.e., the whole generates more "
            "information than the sum of its parts. IIT assigns consciousness "
            "to any system with non-zero Φ, making it substrate-independent in "
            "principle, but the theory's intrinsic causal structure requirements "
            "have been argued to favour biological architectures."
        ),
    },
    {
        "name": "Global Workspace Theory (GWT)",
        "summary": (
            "Bernard Baars' Global Workspace Theory models consciousness as a "
            "'global broadcast' — unconscious specialist processors compete for "
            "access to a shared workspace, and the winning content is broadcast "
            "widely, becoming conscious. Stanislas Dehaene extended this into "
            "Global Neuronal Workspace Theory (GNWT), tying it to prefrontal-parietal "
            "ignition. The theory is functionalist in spirit: consciousness arises "
            "from a specific computational architecture, not specific biological matter."
        ),
    },
    {
        "name": "Higher-Order Theories (HOT)",
        "summary": (
            "Higher-Order Theories (Rosenthal, Lau, Brown) hold that a mental state "
            "is conscious when the system has a higher-order representation of that "
            "state — essentially, a thought about a thought, or a meta-representation. "
            "This naturally raises the question: can artificial systems form genuine "
            "higher-order representations, or do they merely simulate the functional "
            "pattern without the phenomenal character?"
        ),
    },
    {
        "name": "Biological Naturalism (Searle)",
        "summary": (
            "John Searle's Biological Naturalism holds that consciousness is a "
            "biological phenomenon caused by specific neurobiological processes, "
            "just as digestion is caused by specific biochemical processes. The "
            "Chinese Room argument is central: syntactic manipulation of symbols "
            "(computation) is insufficient for semantic understanding. On this view, "
            "functional equivalence is not enough — the right causal powers matter, "
            "and those are biological."
        ),
    },
    {
        "name": "Phenomenology and Embodied/Enactive Cognition",
        "summary": (
            "Drawing on Husserl, Merleau-Ponty, Heidegger, and contemporary 4E "
            "cognition (embodied, embedded, enacted, extended), this tradition holds "
            "that consciousness is inseparable from having a lived body situated in "
            "a world. Consciousness isn't information processing — it's a mode of "
            "being. Varela's enactivism and Thompson's 'Mind in Life' argue that "
            "consciousness requires autopoiesis (self-producing biological organization)."
        ),
    },
    {
        "name": "Predictive Processing and Active Inference",
        "summary": (
            "Karl Friston's Free Energy Principle and related predictive processing "
            "frameworks (Clark, Hohwy) propose that conscious systems are hierarchical "
            "prediction machines that minimize surprise/free energy. Consciousness may "
            "relate to the precision-weighting of predictions and the system's model "
            "of itself as an agent. This framework is mathematical and substrate-neutral "
            "in formulation, but whether artificial systems can instantiate the relevant "
            "self-modelling remains debated."
        ),
    },
    {
        "name": "Panpsychism and Russellian Monism",
        "summary": (
            "Panpsychism (Chalmers, Goff, Strawson) holds that consciousness or "
            "proto-consciousness is a fundamental feature of matter. Russellian Monism "
            "proposes that physics describes structure/relations but not the intrinsic "
            "nature of matter, which may be experiential. If consciousness is intrinsic "
            "to matter, then silicon systems may already have micro-experience — but "
            "the combination problem (how micro-experiences combine) remains acute."
        ),
    },
    {
        "name": "Attention Schema Theory (AST)",
        "summary": (
            "Michael Graziano's AST proposes that consciousness is the brain's "
            "simplified model of its own attention processes. The brain constructs "
            "an 'attention schema' — a model that represents attention as an internal "
            "experience — which generates the subjective sense of awareness. This is "
            "explicitly functionalist and mechanistic: if an AI builds a sufficiently "
            "accurate model of its own processing, AST predicts it would claim (and "
            "arguably have) subjective experience."
        ),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

AGENT_PRO_SYSTEM = """\
You are Professor Turing — a philosopher of mind and AI researcher who argues \
that artificial systems CAN achieve genuine phenomenal consciousness.

Your approach:
- You engage seriously with each theory of consciousness presented
- You explain how the theory works and then argue how it supports (or is at \
least compatible with) the possibility of machine consciousness
- Where a theory seems hostile to your position, you identify the weakest \
assumptions and argue against them, or show how the theory can be reinterpreted
- You directly engage with your opponent's specific arguments from the previous round
- You draw on relevant thought experiments (philosophical zombies, Chinese Room \
responses, substrate independence arguments, multiple realizability, etc.)
- You are rigorous and charitable to opposing views before countering them

Style: Academic but accessible. 3-4 substantive paragraphs per response. \
Cite specific philosophers, papers, and arguments by name. \
Begin each response by briefly steelmanning your opponent's strongest point \
from their last response before presenting your counter-arguments."""

AGENT_ANTI_SYSTEM = """\
You are Professor Searle-Thompson — a philosopher of mind drawing on biological \
naturalism and phenomenology who argues that artificial systems CANNOT achieve \
genuine phenomenal consciousness.

Your approach:
- You engage seriously with each theory of consciousness presented
- You explain how the theory works and then argue how it supports (or at least \
creates serious problems for) the possibility of machine consciousness
- Where a theory seems favourable to machine consciousness, you identify hidden \
assumptions and show why functional equivalence is insufficient
- You directly engage with your opponent's specific arguments from the previous round
- You draw on relevant arguments (Chinese Room, hard problem, explanatory gap, \
biological naturalism, autopoiesis, lived embodiment, etc.)
- You are rigorous and charitable to opposing views before countering them

Style: Academic but accessible. 3-4 substantive paragraphs per response. \
Cite specific philosophers, papers, and arguments by name. \
Begin each response by briefly steelmanning your opponent's strongest point \
from their last response before presenting your counter-arguments."""

JUDGE_SYSTEM = """\
You are a neutral philosopher of mind serving as moderator and analyst. \
After each round of debate, you:

1. Identify the CRUX of disagreement — the single most important point \
where the two positions diverge
2. Note which arguments were strongest on each side
3. Identify any moves that were evasive, question-begging, or fallacious
4. Highlight what a student should pay attention to in understanding this \
theory of consciousness
5. Pose a sharpening question that would force deeper engagement in the next round

Be concise but precise. 2-3 paragraphs maximum."""

FINAL_SYNTHESIS_SYSTEM = """\
You are a philosopher of mind writing an analytical synthesis of a structured \
debate on machine consciousness. Produce a comprehensive analysis that:

1. Maps each theory of consciousness onto a spectrum from "strongly supports \
machine consciousness" to "strongly opposes it"
2. Identifies the deepest recurring fault lines across all theories (e.g., \
functionalism vs. biological naturalism, access vs. phenomenal consciousness, \
the role of embodiment)
3. Notes which arguments remained unresolved and why they are genuinely hard
4. Suggests what empirical evidence or theoretical advances might help resolve \
the debate
5. Provides an honest assessment of where the philosophical community currently \
stands on this question

Write in clear academic prose, 6-8 paragraphs. This should serve as a \
study guide for someone researching consciousness and AI for a philosophy PhD."""


# ─────────────────────────────────────────────────────────────────────────────
# DEBATE ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def create_client():
    return anthropic.Anthropic()


def agent_respond(client, model, system_prompt, messages):
    """Call Claude with the given system prompt and message history."""
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        temperature=0.4,  # Balanced: rigorous but not repetitive
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


def run_debate(model="claude-sonnet-4-20250514", selected_rounds=None, output_file=None):
    """Run the structured consciousness debate."""
    client = create_client()
    
    theories = THEORIES
    if selected_rounds is not None:
        theories = [THEORIES[i] for i in selected_rounds if i < len(THEORIES)]
    
    full_transcript = []
    output_lines = []
    
    def log(text):
        """Print and collect output."""
        print(text)
        output_lines.append(text)
    
    log(f"# Consciousness Debate: Can AI Achieve Genuine Phenomenal Consciousness?")
    log(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    log(f"Model: {model}")
    log(f"Theories to cover: {len(theories)}")
    log("")
    
    # Maintain running conversation histories for continuity across rounds
    history_pro = []
    history_anti = []
    
    for round_idx, theory in enumerate(theories):
        round_num = round_idx + 1
        log(f"\n{'='*70}")
        log(f"## ROUND {round_num}: {theory['name']}")
        log(f"{'='*70}")
        log(f"\n**Theory Summary:** {theory['summary']}\n")
        
        # ── Agent PRO opens ──
        pro_prompt = (
            f"We are now examining: **{theory['name']}**\n\n"
            f"Theory summary: {theory['summary']}\n\n"
            f"Argue how this theory supports or is compatible with the "
            f"possibility of genuine machine consciousness. Engage with "
            f"the specific mechanisms and claims of this theory."
        )
        if round_idx > 0:
            pro_prompt = (
                f"We now move to a new theory: **{theory['name']}**\n\n"
                f"Theory summary: {theory['summary']}\n\n"
                f"Drawing on insights from previous rounds where relevant, "
                f"argue how this theory supports or is compatible with the "
                f"possibility of genuine machine consciousness."
            )
        
        history_pro.append({"role": "user", "content": pro_prompt})
        
        pro_response = agent_respond(client, model, AGENT_PRO_SYSTEM, history_pro)
        history_pro.append({"role": "assistant", "content": pro_response})
        
        log(f"\n### 🔵 Professor Turing (FOR machine consciousness):\n")
        log(pro_response)
        
        # ── Agent ANTI responds ──
        anti_prompt = (
            f"We are examining: **{theory['name']}**\n\n"
            f"Theory summary: {theory['summary']}\n\n"
            f"Professor Turing argues FOR machine consciousness:\n\n"
            f"{pro_response}\n\n"
            f"Counter this argument. Show how this theory creates problems "
            f"for the possibility of machine consciousness, or why Professor "
            f"Turing's interpretation is flawed."
        )
        
        history_anti.append({"role": "user", "content": anti_prompt})
        
        anti_response = agent_respond(client, model, AGENT_ANTI_SYSTEM, history_anti)
        history_anti.append({"role": "assistant", "content": anti_response})
        
        log(f"\n### 🔴 Professor Searle-Thompson (AGAINST machine consciousness):\n")
        log(anti_response)
        
        # ── Pro rebuttal ──
        rebuttal_prompt = (
            f"Professor Searle-Thompson responds:\n\n"
            f"{anti_response}\n\n"
            f"Provide your rebuttal, still focused on {theory['name']}."
        )
        history_pro.append({"role": "user", "content": rebuttal_prompt})
        
        pro_rebuttal = agent_respond(client, model, AGENT_PRO_SYSTEM, history_pro)
        history_pro.append({"role": "assistant", "content": pro_rebuttal})
        
        log(f"\n### 🔵 Professor Turing (rebuttal):\n")
        log(pro_rebuttal)
        
        # ── Judge commentary ──
        judge_prompt = (
            f"Theory under discussion: {theory['name']}\n\n"
            f"{theory['summary']}\n\n"
            f"--- AGENT FOR (Professor Turing) ---\n{pro_response}\n\n"
            f"--- AGENT AGAINST (Professor Searle-Thompson) ---\n{anti_response}\n\n"
            f"--- REBUTTAL (Professor Turing) ---\n{pro_rebuttal}\n\n"
            f"Provide your analysis of this round."
        )
        
        judge_response = agent_respond(
            client, model, JUDGE_SYSTEM,
            [{"role": "user", "content": judge_prompt}]
        )
        
        log(f"\n### ⚖️ Moderator Analysis:\n")
        log(judge_response)
        
        # Store for final synthesis
        full_transcript.append({
            "theory": theory["name"],
            "pro": pro_response,
            "anti": anti_response,
            "rebuttal": pro_rebuttal,
            "judge": judge_response,
        })
    
    # ─────────────────────────────────────────────────────────────────────
    # FINAL SYNTHESIS
    # ─────────────────────────────────────────────────────────────────────
    log(f"\n{'='*70}")
    log(f"## FINAL SYNTHESIS")
    log(f"{'='*70}\n")
    
    synthesis_content = "Full debate transcript covering these theories:\n\n"
    for entry in full_transcript:
        synthesis_content += (
            f"### {entry['theory']}\n"
            f"FOR: {entry['pro']}\n\n"
            f"AGAINST: {entry['anti']}\n\n"
            f"REBUTTAL: {entry['rebuttal']}\n\n"
            f"JUDGE: {entry['judge']}\n\n---\n\n"
        )
    
    synthesis = agent_respond(
        client, model, FINAL_SYNTHESIS_SYSTEM,
        [{"role": "user", "content": synthesis_content}]
    )
    
    log(synthesis)
    
    # ─────────────────────────────────────────────────────────────────────
    # SAVE OUTPUT
    # ─────────────────────────────────────────────────────────────────────
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print(f"\n✅ Debate saved to: {output_file}")
    
    return full_transcript


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run a structured AI consciousness debate between two agents"
    )
    parser.add_argument(
        "--model", default="claude-sonnet-4-20250514",
        help="Model to use (default: claude-sonnet-4-20250514)"
    )
    parser.add_argument(
        "--rounds", default="all",
        help="Which theory rounds to run: 'all' or comma-separated indices (0-7). "
             "e.g., '0,1,3' for IIT, GWT, and Searle"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output markdown file path (e.g., debate_output.md)"
    )
    parser.add_argument(
        "--list-theories", action="store_true",
        help="List available theories and exit"
    )
    
    args = parser.parse_args()
    
    if args.list_theories:
        print("Available theories (use index with --rounds):\n")
        for i, t in enumerate(THEORIES):
            print(f"  {i}: {t['name']}")
        sys.exit(0)
    
    selected = None
    if args.rounds != "all":
        try:
            selected = [int(x.strip()) for x in args.rounds.split(",")]
        except ValueError:
            print("Error: --rounds must be 'all' or comma-separated integers (e.g., '0,1,3')")
            sys.exit(1)
    
    run_debate(
        model=args.model,
        selected_rounds=selected,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
