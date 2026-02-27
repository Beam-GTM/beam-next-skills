---
name: deep-thinking
version: '1.0'
description: Structured deep thinking for hard problems. Load when user says "deep
  think", "think deeply", "frame this", "what's the real question", "eigenquestion",
  "challenge this", "ultrathink", "stress test this", "apply a framework", "get expert
  feedback on this". Frames the problem (one-sentence problem, binding constraint,
  eigenquestion), then runs either stress-test (multi-perspective critique), mental
  framework (pre-mortem, decision-matrix, etc.), or expert review (persona-based feedback).
category: tools
tags:
- thinking
- strategy
- critique
visibility: public
updated: '2026-02-27'
---
# Deep thinking

One entry point for rigorous thinking: **frame** the problem, then choose **stress-test**, **framework**, or **expert feedback**, and synthesize.

## Purpose

Hard problems benefit from (1) a clear frame — one-sentence problem, binding constraint, eigenquestion — and (2) a structured lens: multi-perspective stress-test, a mental model, or expert personas. This skill does both: it frames first, then runs the chosen path and synthesizes.

**Use when**: Messy context, important decision, or content you want to validate before shipping.

**Time**: 3–8 minutes depending on path.

---

## Workflow

### Step 0: Frame (always)

Before any analysis, produce:

1. **One-sentence problem** — The core issue in a single sentence.
2. **Binding constraint** — The limiting factor that shapes what’s possible.
3. **Eigenquestion** — The question whose answer determines the answers to the other questions.

Output these clearly so the user (and the rest of the workflow) can stay aligned.

---

### Step 1: Choose path

Offer the user (or infer from their request):

- **Stress-test** — Multi-perspective critique (recipient POV, critic, devil’s advocate, first principles, risk). Use the **ultrathink** workflow: run the same five-perspective dialogue and synthesis as in the ultrathink skill. Load `01-skills/ultrathink/SKILL.md` and follow its Step 2 and Step 3.
- **Framework** — Apply a structured model (pre-mortem, decision matrix, inversion, etc.). Run **mental-models**: `uv run beam-next-mental-models --format brief`, pick 1–2 models that fit the frame, load the model file from `00-system/mental-models/models/{category}/{slug}.md`, and apply it.
- **Expert feedback** — Get persona-based review. Run **expert-review**: detect work type, pick 2–3 personas, load persona files from `00-system/expert-personas/`, and produce verdict + strengths + gaps + one thing to change per persona.

If the user said "ultrathink" or "stress test", default to **Stress-test**. If they said "apply a framework" or "mental model", default to **Framework**. If they said "expert feedback" or "what would X think", default to **Expert feedback**. Otherwise offer the three options and let them pick.

---

### Step 2: Run the path

- **Stress-test**: Execute the ultrathink multi-perspective dialogue and synthesis (see ultrathink SKILL.md).
- **Framework**: Execute the chosen mental model’s process (questions, steps) and summarize.
- **Expert feedback**: Execute expert-review (personas, verdicts, recommendations).

---

### Step 3: Synthesize

After the path, produce a short synthesis:

- How the frame (eigenquestion, constraint) connects to the findings.
- Top 2–3 actionable takeaways.
- Optional: "Want to run another path? (e.g. stress-test after framework)"

---

## Triggers

- "deep think", "think deeply", "frame this", "what’s the real question", "eigenquestion"
- "ultrathink", "stress test this", "challenge this" → default to Stress-test
- "apply a framework", "mental model", "pre-mortem" → default to Framework
- "expert feedback", "what would [persona] think" → default to Expert feedback

---

## Relationship to other skills

- **ultrathink** — Implements the stress-test path; can be loaded directly for "ultrathink this" or invoked from deep-thinking.
- **mental-models** — Provides the framework path; use its scanner and model files.
- **expert-review** — Provides the expert path; use its persona selection and review format.

Deep-thinking is the umbrella; those three remain available for direct use when the user wants only one path.
