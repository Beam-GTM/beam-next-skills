# Two-Phase Expert Review Protocol

This document defines the review protocol for synthetic data generation, including the gold standard phase, variation matrix orchestration, generation briefs, and review tracking.

## Phase 1: Gold Standard Generation & 2-Expert Review

### Purpose

Generate 2-3 high-quality samples that serve as quality anchors for the full batch. These must pass review by **both expert personas** before any batch generation begins.

### Expert Reviewers

Gold standards are reviewed by **two distinct expert personas** running as **parallel subagents**:

| Expert | File | Lens | Inspired By |
|--------|------|------|-------------|
| **The Practitioner** | `experts/expert-1-production-fidelity.md` | Would this survive production? Stress-tests realism, structural fidelity, fragility. | Nassim Taleb — antifragility, via negativa, barbell strategy |
| **The Calibrator** | `experts/expert-2-derivation-auditor.md` | Was the output actually derived? Checks derivation correctness, scoring calibration, bias. | Daniel Kahneman — System 1/2 thinking, anchoring, base rate neglect |

**Why two, not one:** These are orthogonal failure modes. A sample can look realistic but have a confabulated output (Practitioner passes, Calibrator fails). Or it can be correctly derived but unrealistically clean (Calibrator passes, Practitioner fails). Both must pass.

### Process

```
1. Generate 2-3 samples from the ruleset
2. Launch 2 PARALLEL expert subagents — each receives:
   - The gold standard samples (input + output files)
   - The full ruleset
   - Their persona file (expert-1 or expert-2)
   - (Expert 1 only) Production samples if available
3. BOTH experts must return PASS:
   - Expert 1 (Practitioner): avg >= 7.5, no dimension < 6.0
   - Expert 2 (Calibrator): avg >= 7.5, no dimension < 6.0, derivation trace >= 5.0
4. If either fails:
   a. Apply BOTH experts' feedback (a fix for one may affect the other)
   b. Re-run BOTH experts on the fixed samples
   c. Max 3 iterations per gold standard run
5. If both pass → present gold standards to user with file paths + review summaries
6. If 3 iterations exhausted with failures → surface to user, do NOT proceed
```

### Gold Standard Requirements

- Both experts return PASS (avg >= 7.5, no dimension < 6.0)
- Expert 2 hard fail: Derivation Trace < 5.0 is an automatic rejection
- Each gold standard should cover a different variation slot
- Gold standards are saved to: `[output_dir]/gold-standards/`

### Gold Standard Fix Loop

```
iteration = 0
while iteration < 3:
    # Launch BOTH experts in parallel
    review_1 = expert_1_review(gold_standards, ruleset, production_samples)
    review_2 = expert_2_review(gold_standards, ruleset)

    if all_pass(review_1) and all_pass(review_2):
        break
    else:
        # Merge feedback from both experts before fixing
        combined_feedback = merge(review_1.feedback, review_2.feedback)
        for sample in combined_feedback.failures:
            apply_feedback(sample, combined_feedback)
        iteration += 1

if iteration == 3 and not (all_pass(review_1) and all_pass(review_2)):
    surface_to_user(review_1.remaining_issues + review_2.remaining_issues)
    STOP — do not proceed to Phase 2
```

### Review Output

After both experts pass, present a combined summary:

```
┌─────────────────────────────────────────────────────┐
│ GOLD STANDARD REVIEW — [ruleset name]               │
├─────────────────────────────────────────────────────┤
│ Expert 1 (Practitioner): PASS — avg 8.2/10          │
│   Input realism: 8 | Derivation: 9 | Structure: 8  │
│   Edge case stress: 7 | Pairing: 9                  │
│   Fragility warnings: [none or brief list]          │
│                                                     │
│ Expert 2 (Calibrator): PASS — avg 7.8/10            │
│   Derivation trace: 8 | Scoring cal: 7 | Distrib: 8│
│   Category fit: 8 | Independence: 8                 │
│   Bias warnings: [none or brief list]               │
├─────────────────────────────────────────────────────┤
│ Combined verdict: PASS — proceed to batch gen?      │
└─────────────────────────────────────────────────────┘
```

## Human Review Checkpoint

After gold standards pass both expert reviews, present them to the user in chat with file paths and the combined expert summary. The gold standard files on disk (in `[output_dir]/gold-standards/`) are the review artifacts — no separate review document needed.

### User Decision Points

- **Approve**: Proceed to batch generation (Phase 2)
- **Provide feedback**: Incorporate feedback → regenerate gold standards → re-review (both experts)
- **Reject**: Stop generation, user provides direction

**CRITICAL: Batch generation MUST NOT start until user explicitly approves the gold standards AND both experts have passed.**

## Variation Matrix

### Purpose

Ensure deterministic diversity by pre-assigning variation slots to each batch subagent, preventing accidental overlap.

### Computing the Matrix

Extract `variation_dimensions` from the ruleset. Each dimension has named slots with target distributions.

Example ruleset dimensions:
```yaml
variation_dimensions:
  edge_case_type: [missing_fields, conflicting_values, ambiguous_fields, boundary_conditions]
  format: [pdf, csv, pptx, docx]
  complexity: [simple, medium, complex]
```

### Matrix Format

Compute the cross-product of dimensions, then assign slots to subagents:

| Subagent | Samples | Edge Case Type | Format | Complexity |
|----------|---------|----------------|--------|------------|
| A | 1-10 | missing_fields | PDF | simple |
| B | 11-20 | conflicting_values | CSV | complex |
| C | 21-30 | ambiguous_fields | PPTX | medium |

### Assignment Rules

1. Each subagent gets a unique combination of primary variation dimensions
2. If more subagents than unique combinations, allow overlap on secondary dimensions
3. Balance sample counts evenly across subagents
4. Ensure every slot in every dimension is covered by at least one subagent

## Generation Brief

### Purpose

Each batch subagent receives a focused brief that tells it exactly what variation to produce. This replaces vague "be diverse" instructions.

### Format

```markdown
## Generation Brief — Subagent [ID]

**Assigned samples:** [start]-[end] (N samples)
**Variation focus:**
- Edge case type: [assigned type]
- Format: [assigned format]
- Complexity: [assigned complexity]

**Gold standard examples:**
[Include 2-3 gold standard samples as quality anchors]

**Instructions:**
- Generate [N] samples matching your assigned variation focus
- Use the gold standards as quality anchors — match their structural accuracy and content realism
- Do NOT duplicate the gold standards' exact scenarios
- Each sample must be unique within your batch
- Follow all ruleset constraints
```

## Phase 2: Batch Review & Tracking

### review-status.md Specification

After full batch generation, the expert reviews ALL samples and writes results to `review-status.md`.

### File Format

```markdown
## Review Status — Run [ISO timestamp]

### Summary
- Total samples: [N]
- Passed: [N]
- Failed: [N]
- Pending: [N]

### Results
- [x] sample-01 — PASS (avg: 8.2/10)
- [ ] sample-02 — FAIL: allergen form has 2 columns, production uses 3
- [x] sample-03 — PASS (avg: 7.5/10)
- [ ] sample-04 — FAIL: missing chemical control section
- [ ] sample-05 — PENDING

### Failed Sample Details

#### sample-02
- **File:** sample-02/spec.pdf
- **Issue:** allergen form has 2 columns, production uses 3
- **Dimension scores:** Structural Accuracy: 3/10, Content Realism: 7/10, Format Fidelity: 4/10, Rule Compliance: 5/10, Diversity: 8/10
- **Fix suggestion:** Add third column for [specific field]

#### sample-04
- **File:** sample-04/safety_doc.pdf
- **Issue:** missing chemical control section
- **Dimension scores:** Structural Accuracy: 4/10, Content Realism: 8/10, Format Fidelity: 7/10, Rule Compliance: 3/10, Diversity: 7/10
- **Fix suggestion:** Add chemical control section between [section A] and [section B]
```

### Location

Save to: `[output_dir]/review-status.md`

### Resumability

A new subagent can resume review by:

1. Reading `review-status.md`
2. Finding all entries marked `PENDING` or not yet listed
3. Continuing review from where the previous subagent left off
4. Appending results to the same file

### Failed Sample Regeneration

```
round = 0
while round < 3 and has_failures(review_status):
    failed_samples = get_failures(review_status)
    regenerate(failed_samples, using=gold_standards + expert_feedback)
    re_review(regenerated_samples)
    update_review_status(results)
    round += 1

if round == 3 and has_failures:
    surface_unresolved_to_user(review_status)
```

## Exit Conditions

| Condition | Action |
|-----------|--------|
| All gold standards pass + user approves | Proceed to batch generation |
| Gold standards fail after 3 iterations | Stop, surface issues to user |
| User rejects gold standards | Incorporate feedback, restart Phase 1 |
| All batch samples pass | Complete — output final dataset |
| Batch failures after 3 fix rounds | Complete with partial results, surface unresolved issues |
| Expert subagent hits context limit | New subagent resumes from review-status.md |
