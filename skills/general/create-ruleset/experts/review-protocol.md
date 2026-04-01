# Expert Review: Ruleset Quality Gate

Three expert personas review the ruleset via parallel subagents BEFORE presenting it to the user. Each expert has a dedicated persona file with identity, mental model, framework, and scoring rubric.

## Why This Matters

A flawed ruleset multiplies errors across every sample generated from it. Catching "article lengths too short" at the ruleset level costs 1 fix; catching it after generating 35 samples costs 35 regenerations.

---

## Expert Personas

| Expert | Persona File | Lens | What they catch |
|--------|-------------|------|-----------------|
| **1. Priya Narayan** | [experts/expert-1-production-realism.md](experts/expert-1-production-realism.md) | Does the ruleset match production reality? | Content lengths too short, bundled vs individual files, vague constraints, missing content texture |
| **2. James Whitfield** | [experts/expert-2-internal-consistency.md](experts/expert-2-internal-consistency.md) | Does the ruleset contradict itself? | Examples not matching schema, derivation producing invalid output, composition numbers not adding up |
| **3. Tomoko Hayashi** | [experts/expert-3-generative-readiness.md](experts/expert-3-generative-readiness.md) | Will this produce diverse data on first pass? | Not enough variation axes, unnamed slots, monotonous examples, missing anti-patterns |

Each expert scores 5 dimensions (0-10). **Pass: avg >= 7.0, no dim < 5.0.**

---

## Execution Protocol

### How to launch (subagent instructions)

Launch **3 parallel subagents**. Each subagent receives:

**Expert 1 subagent:**
1. The full ruleset markdown (read path)
2. The persona file: `experts/expert-1-production-realism.md` (read this FIRST — it defines identity, mental model, framework, and output format)
3. Source documents: production samples, agent specs, corporate profiles, call transcripts (read paths)
4. Instruction: "Adopt the persona in the persona file. Follow the mental model and framework exactly. Score all 5 dimensions. Return the review in the specified format."

**Expert 2 subagent:**
1. The full ruleset markdown (read path)
2. The persona file: `experts/expert-2-internal-consistency.md` (read this FIRST)
3. No source documents needed — this expert only checks internal consistency
4. Instruction: "Adopt the persona in the persona file. Follow the cross-reference graph. Score all 5 dimensions. Return the review in the specified format."

**Expert 3 subagent:**
1. The full ruleset markdown (read path)
2. The persona file: `experts/expert-3-generative-readiness.md` (read this FIRST)
3. (Optional) index.json of any already-generated samples
4. Instruction: "Adopt the persona in the persona file. Follow the diversity funnel model. Score all 5 dimensions. Return the review in the specified format."

### Decision logic

| Result | Action |
|--------|--------|
| All 3 PASS | Present ruleset to user |
| 1-2 FAIL | Apply fixes from failed experts, re-run ONLY failed experts (max 3 iterations total) |
| All 3 FAIL | Apply highest-priority fixes, re-run all 3 |
| 3 iterations exhausted, still failing | Present to user with remaining issues clearly listed |

### Fix priority (when multiple issues found)

1. **Contradictions** — produce incorrect data. Fix immediately.
2. **Schema <> Example mismatches** — generator will produce wrong output format.
3. **Missing variation dimensions** — generator will produce monotonous data.
4. **Unrealistic constraints** — data won't match production.
5. **Missing anti-patterns** — common failures won't be caught.

---

## Exit Conditions

| Condition | Action |
|-----------|--------|
| Ruleset passes review (avg >= 7.0, no dim < 5.0) | Present to user as ready |
| 3 iterations exhausted, still failing | Present to user with remaining issues clearly listed |
| User says "generate now" during review | Stop review, proceed with current state + warnings |
| Contradiction found in source docs themselves | Flag to user — cannot resolve without clarification |

---

## Review Metadata

After review passes, append to the bottom of the ruleset:

```yaml
review:
  verdict: PASS
  iterations: 1
  timestamp: 2026-03-31T14:00:00Z
  experts:
    production_realism: {score: 8.2, verdict: PASS}
    internal_consistency: {score: 7.8, verdict: PASS}
    generative_readiness: {score: 7.4, verdict: PASS}
  fixes_applied:
    - "Increased article length range from 200-800 to 400-1200 words (production realism)"
    - "Added audio.style field to example JSONs (internal consistency)"
  unresolved: []
```

### Location

The review metadata lives at the bottom of the ruleset file itself:
- The ruleset file itself (at the path resolved during output generation) — review appended as hidden YAML comment

No separate `_review-status.md` file is created.

### Resumability

A new subagent can resume by reading the `_REVIEW METADATA` section at the bottom of the ruleset to understand:
- What issues were already found and fixed
- What issues remain unresolved
- The current score state
- Whether to continue fixing or escalate to user

### Integration with Post-Generation Feedback

After `create-data` runs, a `_feedback.md` file may be created alongside the ruleset (see [../generation/feedback-loop-format.md](../generation/feedback-loop-format.md)). When re-reviewing or updating a ruleset:
1. Check for an existing `_feedback.md`
2. Treat feedback items as additional review inputs
3. Prioritize fixing ambiguities that caused inconsistent generation
