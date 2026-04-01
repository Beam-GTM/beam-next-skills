---
name: create-data
description: Generate synthetic training data from a ruleset file. Use when the user wants to create training examples, generate augmented data, or produce samples following defined rules.
argument-hint: [optional context from user message]
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
---

# Generate Synthetic Data from Ruleset

## Why This Skill Exists

AI agents need test data to evaluate whether they work correctly. But real production data is scarce, sensitive, or doesn't cover edge cases. This skill generates **synthetic test data** that mimics production reality — including the messy, broken, and deceptive inputs the agent will face.

The key insight: **a ruleset defines WHAT to generate, this skill executes HOW.** The ruleset is the blueprint (created by `/create-ruleset`). This skill reads the blueprint and produces concrete input/output pairs the agent can be tested against.

**Why not just generate data directly?** Without a ruleset, generated data lacks diversity (all happy path), realism (artificial inputs), and coverage (misses edge cases). The ruleset-first approach ensures every generated sample serves a specific testing purpose.

## Core Principles

1. **Ruleset is mandatory.** No ruleset → no generation. Direct user to `/create-ruleset`. **Why:** The ruleset is the contract between what to generate and what quality looks like. Without it, the skill has no spec to follow.
2. **Step-by-step review with the user.** Never jump straight to generation. Walk through Task → Input → Output → Scenarios → Gold Standards → Plan → Generate. **Why:** Each step is a correction window. The user spots issues when they see ruleset content presented in a data-generation context. Fixing at Step 2 costs 1 edit; fixing after 12 samples costs 12 regenerations.
3. **ASCII diagrams + emojis.** Use templates from [create-ruleset/resources/presentation-templates.md](../create-ruleset/resources/ascii-box-templates.md) for all proposals. **Why:** Visual structure makes complex information scannable — the user can spot issues faster than in prose.
4. **Footnote citations + hypothesis flagging.** Superscript numbers (¹ ² ³) with Sources footer. Flag inferences in 🔶 Hypotheses footer. **Why:** The user needs to know which claims come from the ruleset vs. which are inferred. Unflagged hypotheses become invisible assumptions in the generated data.
5. **Schema version check.** Verify the ruleset has `schema_version: "2.0"`. If v1 or missing, warn and suggest `/create-ruleset` upgrade. **Why:** v2.0 introduced Test Scenarios with What/Why/Varies cards. Older formats lack the structure needed for generation briefs.
6. **Ground in the ruleset.** Use the ruleset's OUTPUT DERIVATION PROCEDURE to generate correct outputs. Don't guess. **Why:** The derivation procedure is the step-by-step recipe for producing correct outputs. Skipping it means the generator invents its own logic, which may contradict the agent's actual behavior.
7. **Subagents are context-blind.** Subagents have no access to skill files, the ruleset, previous conversation, or shared renderers. Everything a subagent needs to do its job — ruleset sections, quality constraints, scoring formulas, file format specs, JSON schemas — must be included in its prompt. If a subagent needs to produce rendered files, include the **full source code of the reference renderer** (`scripts/file_renderer.py`) plus its assigned visual archetype description, so it can write a custom renderer. If it needs to score, include the scoring formula. Don't assume shared context.

## Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Context Discovery | [context-discovery.md](context-discovery.md) | Auto-discovery of client/project files |
| Expert 1: The Practitioner | [experts/expert-1-production-fidelity.md](experts/expert-1-production-fidelity.md) | Production fidelity critic (Taleb's antifragility). Gold standard + batch review. |
| Expert 2: The Calibrator | [experts/expert-2-derivation-auditor.md](experts/expert-2-derivation-auditor.md) | Statistical & derivation auditor (Kahneman's dual-process). Gold standard + batch review. |
| Batch Review Persona | [experts/expert-persona.md](experts/expert-persona.md) | Generic batch review rubric (Phase 3b post-batch) |
| Review Protocol | [experts/review-loop.md](experts/review-loop.md) | Two-phase review, variation matrix, generation briefs |
| Generation Prompt | [prompts/generation-prompt.md](prompts/generation-prompt.md) | Domain-agnostic generation prompt blueprint |
| Verification Prompt | [prompts/verification-prompt.md](prompts/verification-prompt.md) | Domain-agnostic evaluation prompt blueprint |
| Coverage Report | [experts/coverage-report-template.md](experts/coverage-report-template.md) | Coverage matrix format and classification logic |
| File Generation | [scripts/file-generation.md](scripts/file-generation.md) | Render spec schema, layouts, section types |
| File Renderer | [scripts/file_renderer.py](scripts/file_renderer.py) | Universal renderer for all document types |
| Gold Standard Review | [experts/gold-standard-review-template.html](experts/gold-standard-review-template.html) | HTML template for gold standard review reports |
| Post-Gen Feedback | [../create-ruleset/generation/feedback-loop-format.md](../create-ruleset/generation/feedback-loop-format.md) | Feedback loop back to ruleset |
| Interface Contract | [../shared/interface-contract.md](../shared/interface-contract.md) | What sections to read from ruleset, YAML blocks, feedback protocol |

**Export scripts:** `scripts/export.py` (dispatcher), `scripts/csv_export.py`, `scripts/xlsx_export.py`, `scripts/pdf_export.py`, `scripts/docx_export.py`.

**Parsers:** `parsers/pdf_parser.py`, `parsers/pdf_to_images.py`, `parsers/csv_reader.py`, `parsers/pptx_parser.py`. For scanned PDFs: convert to images with `pdf_to_images.py`, then `Read` visually.

---

## Configuration Defaults

| Setting | Default |
|---------|---------|
| Samples per batch | 10 |
| Min consensus score | 0.8 (80/100) |
| Require unanimous validity | true |
| Minimum evaluators | 3 |
| Schema pre-check | true (for JSON/structured output) |

---

## Step-by-Step User Interaction Protocol

**The steps are a RULESET REVIEW with the user.** The purpose is NOT to present information you already have — it's to walk the user through the ruleset's content so they can spot errors, correct assumptions, and refine the rules BEFORE any data is generated. Fixing a ruleset issue at Step 2 costs 1 edit; fixing it after generating 12 samples costs 12 regenerations.

**CRITICAL: Never jump straight to generation, even if the user just created the ruleset in the same session.** The user may have approved the ruleset at a high level during create-ruleset but will notice issues when they see the specifics presented back to them in a data-generation context. Every step is a correction window.

**CRITICAL: Wait for user confirmation at EVERY step.** Do not present Step 2 until the user confirms Step 1. Do not batch steps unless the user explicitly says "looks good, keep going" or "skip ahead." Silence is not confirmation.

### Conflict Detection

When user feedback conflicts with the ruleset, flag it:
```
⚠️ CONFLICT: [dimension]
📄 Ruleset says: [what the ruleset defines]
🗣️ You said:     [what the user requested]
💡 Recommendation: [update ruleset or treat as exception]
```
Ask: *"Update the ruleset or keep as exception for this batch?"*

### Ruleset Update on User Correction

When the user changes input format, output format, fields, or file types during Steps 1-4 → **update the ruleset HTML file in-place**. The ruleset is the source of truth. Briefly mention: *"Updated the ruleset to reflect this."*

Do NOT update for batch-only preferences (fewer samples, skip a dimension this run).

### The Steps

Each step has a **what** (what you present), a **why** (why this step exists), and a **question** (what you ask the user). Never skip the question.

**Step 1: The Task**
- **What:** Present a one-sentence agent summary from the ruleset's USE CASE section.
- **Why:** The user may have created the ruleset days ago, or someone else created it. This grounds the conversation — if the task description is wrong, everything downstream is wrong. This is the cheapest place to catch a fundamental misunderstanding.
- **Ask:** *"Does this match what the agent does?"*

**Step 2: Input**
- **What:** Present what the agent receives: **file type per entity** (PDF, JSON, text string, etc.), content fields, content texture, entity structure. From INPUT SCHEMA. **File type is mandatory** — always show it prominently in the entity header (e.g., "📥 INPUT ENTITY 1: Resume — PDF file"). Without explicit file types, the user cannot evaluate whether the generation plan makes sense.
- **Why:** The user sees concrete file formats, field names, types, and constraints — they may realize a field is missing, misnamed, has wrong constraints, or the file type is wrong (e.g., "these are individual .md files, not a JSON array"). File format corrections are trivial now but would invalidate every generated sample if caught later.
- **Ask:** *"Anything to add or change about the input?"*
- **If user corrects:** Update the ruleset HTML in-place. Mention: *"Updated the ruleset to reflect this."*

**Step 3: Output**
- **What:** Present what the agent produces: **file type per output** (JSON field in index.json, separate rendered file, text string, etc.), format, fields, quality constraints, derivation procedure. From OUTPUT SCHEMA. **File type is mandatory** — always show it prominently in the output header (e.g., "📤 OUTPUT 1: SMS Messages — JSON strings in index.json").
- **Why:** The user sees the exact file format and output structure — they may want to adjust the format (e.g., recruiter summary as a separate .txt instead of a JSON field), field names, constraints, or the derivation logic. Output schema issues are the second most common correction point. A wrong constraint or file type here means every gold standard and sample will be wrong.
- **Ask:** *"Does this output structure match what you expect?"*
- **If user corrects:** Update the ruleset HTML in-place.

**Step 4: Test Scenarios**
- **What:** Present the scenario cards (What/Why it's hard/Varies) from TEST SCENARIOS section, including sample counts per scenario.
- **Why:** The user sees exactly what difficulty levels will be tested. They may want to rename scenarios (names should be self-descriptive to non-technical readers), adjust the sample mix, add a scenario they hadn't considered, or change distributions within a scenario.
- **Ask:** *"Are these the right scenarios? Adjust the mix?"*
- **If user corrects:** Update the ruleset HTML in-place.

**Step 5: Gold Standard (3 examples)**
- **What:** Generate 3 sample pairs covering different scenarios. Write to disk, present summaries in chat.
- **Why:** This is the quality gate. The user sees ACTUAL generated data for the first time — not descriptions, not schemas, but real input/output pairs. This is where quality expectations are calibrated. If the gold standards don't feel right, the remaining samples won't either. Iterating here is 10x cheaper than iterating after full generation.
- **Rules:**
  - Each must use DIFFERENT scenarios from the ruleset
  - If input includes PDFs → at least one gold standard includes a rendered PDF
  - If output is a document → generate in target format, not .txt
  - Use `scripts/file_renderer.py` for realistic files
- **5a.** Generate I/O pair JSONs + render spec JSONs (via subagents if 3+). Gold standards use the **reference renderer** (`scripts/file_renderer.py`) for fast iteration — visual archetype diversity is enforced in batch generation (Phase 2), not here.
- **5b.** Render files: `python scripts/file_renderer.py spec.json --output sample.pdf`
- **5c.** Visually verify each rendered file (Read the PDF). If broken or incomplete → fix the render spec and re-render before presenting to the user.
- **5d.** Present summary table with file paths to user.
- **5e.** Ask: *"Review the 3 examples. Does the quality feel right?"*
- **5f.** Iterate on feedback until user says *"this is the quality I want."*
- **5g.** Lock gold standards as quality anchors.
- **NEVER skip Step 5** — quality alignment is non-negotiable.

**Step 6: Sample Plan**
- **What:** Show the plan for remaining samples as an ASCII table mapping each sample to a scenario and variation slot.
- **Why:** The user can see the full generation plan at a glance — spot imbalances, swap slots, or adjust before committing to generation. Cheaper than regenerating after the fact.
- **Ask:** *"Does this plan look right? Swap anything?"*

**Step 7: Generate & Review**
- **What:** Generate remaining samples. ≤10 inline, 11+ via subagents with generation briefs.
- **Why:** This is the execution step — it follows the plan approved in Step 6.

**Collapsing:** You may batch Steps 2+3 ONLY if the user explicitly says "looks good, keep going" after Step 1. NEVER skip Step 5 (Gold Standards). NEVER batch Steps 1-4 — the whole point is the correction window.

**Why this order matters:** Each step narrows the scope. Step 1 confirms the agent's purpose. Step 2 confirms what goes in. Step 3 confirms what comes out. Step 4 confirms how we test it. Step 5 confirms the quality bar. By Step 7, there should be zero surprises — every decision was made and confirmed incrementally.

---

## Workflow

### Phase 0: Ask & Gather Context

If `$ARGUMENTS` has context, use it. Otherwise ask: *"What data do you want to generate?"*

Then launch **parallel subagents**:

**a) Ruleset + data scan:**
- Locate ruleset in `dataset/**/rulesets/*.html`. If none → **STOP**, direct to `/create-ruleset`.
- **Check schema_version.** If missing or < "2.0", warn user and suggest upgrading via `/create-ruleset`.
- Scan existing data: sample count, coverage scores, gold standards, index files.
- Infer data structure from 2-3 existing samples (schema summary only, not full content).
- Check for `_feedback.md` — post-generation feedback from previous runs.

**b) Context discovery** (if client mentioned): Follow [context-discovery.md](context-discovery.md).

Present ONE unified summary. Smart defaults:
- **No ruleset but client context exists** → **STOP generation**, but don't just say "go create a ruleset." First, do context discovery (search account folders, proposals, transcripts, workstreams). Read key docs. Then present what use cases could be built as a grounded table with recommendations — same format as create-ruleset Phase 0b. This gives the user an actionable next step instead of a dead end.
- **No ruleset and no client context** → **STOP.** Direct to `/create-ruleset`.
- **Gold standards exist** → reuse (skip Phase 1a) unless user says "regenerate fresh"
- **Existing data found** → run coverage analysis (Phase 0.5) to find gaps
- **Feedback file found** → mention known issues from previous runs
- **Multiple rulesets match** → ask which one

### Phase 0.5: Coverage Analysis (when existing data found)

**Skip if no existing data.** Map all existing I/O pairs against the ruleset's edge cases and variation dimensions. Only generate what's missing.

**Steps:**
1. **Load existing I/O pairs** — accepts JSON array, CSV, or folder of files. Track source (client-provided vs generated).
2. **Extract targets from ruleset** — TEST SCENARIOS (each scenario's Varies dimensions and distributions).
3. **Classify each sample via subagent** — which scenario it covers, which variation slots it fills, coverage quality (full/partial/none).
4. **Build coverage matrix** — per scenario and per variation dimension. Additive-only: every suggestion verified against existing samples to prevent duplicates.
5. **Generate coverage report** per [experts/coverage-report-template.md](experts/coverage-report-template.md). Save to `dataset/[client]/[use-case]/augmented/coverage-report.md`.

Present summary: "Analyzed N samples against M edge cases. Coverage: X%. Missing: [list]. Generate only gaps?"

If `--analyze-only`: present report and STOP.

### Phase 1: Initialization

1. **Load ruleset.** Verify `schema_version: "2.0"`. See [interface contract](../shared/interface-contract.md) for which sections to extract.
2. **Parse YAML blocks** — extract `planning` (from hidden PLANNING YAML comment) and `test_scenarios` (from TEST SCENARIOS section — each scenario's Varies chips provide the variation dimensions and distributions). These machine-readable blocks drive generation briefs.
3. **Extract litmus test** from USE CASE section — used in all verification prompts.
4. **Extract few-shot examples** from FEW-SHOT EXAMPLES section. Add seed data as additional anchors if found.
5. **Pre-populate tracking** from coverage report if Phase 0.5 ran.

### Phase 1a: Gold Standard — Co-Create with User

**Skip if approved gold standards exist and user agreed to reuse.**

This follows the Step 5 mini-conversation from the protocol:

**1.** Generate one realistic input (targeting the most common scenario). Present to user. Iterate until input feels right.

**2.** Ask user to rate BEFORE showing output: *"What rating would YOU give this?"* This catches scoring calibration issues early.

**3.** Generate output using the ruleset's OUTPUT DERIVATION PROCEDURE. Compare with user's expected rating. Resolve disagreements now.

**4.** Iterate until locked. **Run 2-expert review via parallel subagents** (mandatory — both must pass). Save to `[output_dir]/gold-standards/`.

For 2+ gold standards: second targets a different category (edge case or adversarial).

#### Mandatory 2-Expert Gold Standard Review

Every gold standard MUST be reviewed by **both** expert personas before approval. Launch as **2 parallel subagents**, each receiving the gold standard samples + full ruleset + their persona file:

| Expert | Persona File | Focus | Mental Model |
|--------|-------------|-------|--------------|
| **Expert 1: The Practitioner** | [expert-1-production-fidelity.md](experts/expert-1-production-fidelity.md) | Production realism, structural fidelity, fragility | Taleb's antifragility — stress-tests against production messiness |
| **Expert 2: The Calibrator** | [expert-2-derivation-auditor.md](experts/expert-2-derivation-auditor.md) | Derivation correctness, scoring calibration, bias detection | Kahneman's dual-process — catches confabulation and anchoring |

**Pass criteria:** Both experts must return PASS (avg >= 7.5, no dimension < 6.0). If either fails:
1. Apply the failing expert's fixes
2. Re-run BOTH experts (a fix for one may break the other's criteria)
3. Max 3 iterations — if still failing after 3 rounds, surface unresolved issues to user

**Why two experts, not one:** A single reviewer conflates production realism with derivation correctness. The Practitioner catches "this doesn't look like production data." The Calibrator catches "the output wasn't actually derived from the input." These are orthogonal failure modes — a sample can look realistic but have a confabulated output, or be correctly derived but unrealistically clean.

### Phase 1b: Dataset Plan — Co-Confirm with User

Present full plan referencing the gold standard: *"44 more like that, across these scenarios..."*

Show as ASCII table. User confirms.

**Do NOT proceed to generation until user approves both gold standard AND plan.**

### Phase 1c: Variation Matrix & Generation Briefs

Follow [experts/review-loop.md](experts/review-loop.md) variation matrix spec.

**If coverage report exists** → incremental matrix targeting gaps only:
- Remove already-covered slots
- Assign only uncovered/underrepresented slots to subagents

**If no coverage report** → full cross-product.

Also include:
- **Scenario profiles** from TEST SCENARIOS (each scenario's What/Why/Varies)
- **Content texture** from INPUT SCHEMA Content Texture descriptions
- **Visual archetype assignments** (if file rendering) — one archetype per subagent from the list in `scripts/file-generation.md`. Never assign the same archetype twice in one batch.

### Phase 1d: Generation Briefs & Anti-Repetition

Each subagent receives THREE things:

**1. Gold Standard** — quality bar (realism, specificity, depth). Defines "good," NOT content.

**2. Generation Brief** — specific assignment locking structural dimensions (scenario, industry, geography, format) and freeing content dimensions (names, companies, stories, skills, dates, wording). The brief maps directly to one TEST SCENARIO card — it locks the scenario's Varies dimensions and frees content details. **MUST include the ruleset's content length constraints** (e.g., "articles must be 400-1200 words per the INPUT SCHEMA") and content texture descriptions (e.g., "wire-service style: 400-700 words" vs "analytical: 700-1200 words"). Without explicit length requirements, subagents default to artificially short content that doesn't match production reality.

**3. Anti-Repetition Blocklist** — names/companies/titles from previous batches. "Do NOT reuse these."

**4. Visual Archetype Assignment** (if file rendering) — a visual archetype describing the target software system the document should appear to come from (e.g., "ATS Export," "Canva Modern," "LaTeX Academic"). Each subagent gets a DIFFERENT archetype from the list in `scripts/file-generation.md`. The subagent writes a **custom renderer script** based on the reference renderer (`scripts/file_renderer.py`), produces files with genuinely different visual DNA, and runs the renderer as part of generation — not as a separate post-processing step.

**Blocklist accumulation protocol:** After gold standards are locked, extract all person names, company names, university names, and job titles used. This forms the initial blocklist. After each batch of subagents completes, scan their outputs and append new names/companies to the blocklist before launching the next batch. For parallel subagents within the same batch, pre-assign distinct name pools (e.g., "subagent 1: use names starting A-F, subagent 2: G-L") to prevent collisions without blocking.

**Batch sizing:**

| Total | Strategy |
|-------|----------|
| ≤10 | Inline (no subagents) |
| 11-30 | 3 subagents |
| 31-50 | 5 subagents |
| 51-100 | 10 subagents |
| 100+ | 10 subagents × multiple rounds with blocklist accumulation |

### Phase 2: Generation

**Small batches (≤10):** Generate inline per plan.

**Large batches (11+):** Subagents with briefs write files to disk, return 1-line summaries.

For each sample:
1. Follow generation brief — assigned variation dimensions
2. Use [generation prompt blueprint](prompts/generation-prompt.md) with ruleset sections
3. **Validate content length against INPUT SCHEMA constraints.** If the ruleset says "400-1200 words" and a generated input is 250 words, regenerate it. This is the #1 cause of unrealistic data — LLMs default to brevity unless explicitly constrained.
4. If file generation requested → include render spec (see [scripts/file-generation.md](scripts/file-generation.md)). **CRITICAL: Follow the Visual Diversity Protocol** — each subagent writes its own **custom renderer script** based on the reference renderer + its assigned visual archetype. Every rendered file must have genuinely different visual DNA (different spacing algorithms, border treatments, font sizing ratios, decorative elements — not just different parameter values on the same renderer). See `scripts/file-generation.md#visual-diversity-protocol-critical` for archetypes, rendering dimensions to vary, and anti-patterns.
5. **Respect conditional outputs.** Many agents have pipeline stages that only execute under certain conditions (e.g., SMS only sent if score ≥ 70, interview questions only generated if proceeding to interview). When the generation brief assigns a scenario where a pipeline stage is skipped, set those output fields to null — don't generate placeholder content. The OUTPUT DERIVATION PROCEDURE defines when each output is produced; follow it exactly, including the conditions where outputs are absent.
6. Deduplicate against all existing data (gold standards, client I/O pairs, previous batches). Reject if >80% similarity.
7. Update diversity tracking (content diversity + visual archetype usage for rendered files). Log which archetype each subagent used; flag if a custom renderer fell back to the reference renderer.

**Sample format:**
```json
{
  "transformation_rules": ["scenario: rich_batch_clean_data", "industry: tech"],
  "input": "agent input matching INPUT SCHEMA",
  "output": "expected output matching OUTPUT SCHEMA",
  "metadata": {
    "coverage_category": "happy_path",
    "variation_slots": {"industry": "tech", "format": "pdf"},
    "quality_score": 87,
    "consensus_scores": [85, 88, 88],
    "generated_at": "2026-03-31T10:30:00Z"
  }
}
```

### Phase 3: Verification (via subagents)

For each sample, launch **3 parallel evaluator subagents** using [verification prompt](prompts/verification-prompt.md).

**Schema pre-check (for structured output):** Before 3-LLM consensus, validate:
- Required fields exist
- Field types match schema
- Numeric values in declared ranges
- Enum values from allowed set

If pre-check fails → auto-reject (saves 3 LLM calls).

**Consensus pass criteria:**
- All 3 agree `is_valid: true`
- Average `quality_score` >= 80
- All 3 agree `passes_ruleset: true`

### Phase 3b: Post-Batch Expert Review

Launch review subagents (10 samples each) with rubric from [experts/expert-persona.md](experts/expert-persona.md).

1. Score every sample across 5 rubric dimensions
2. Write `review-status.md` with PASS/FAIL per sample
3. Regenerate failed samples (max 3 rounds)
4. Surface unresolved issues to user

### Phase 4: Output

Save to: `dataset/[client]/[use-case]/augmented/index.json`
Fallback: `dataset/augmented/[ruleset_name]/`

**Phase 4a: File Generation** (if requested) — for batch generation (11+ files), each subagent already wrote and ran its own custom renderer during Phase 2 (files are on disk). For gold standards and small inline batches (≤10), use the reference renderer `scripts/file_renderer.py`. For non-PDF formats (DOCX, XLSX, PPTX, HTML), the same principle applies: subagents write custom styling code, not just different parameters on shared scripts. See [scripts/file-generation.md](scripts/file-generation.md) for visual archetypes, rendering dimensions to vary, and domain-specific guidance.

**Phase 4b: Export** (if requested):
```bash
python 01-skills/create-data/scripts/export.py dataset/[path]/index.json --format csv,pdf,docx,xlsx
```
Same principle: the existing export dispatcher and format scripts are **reference implementations**. For different tasks, rework them to fit the actual data schema.

### Phase 4c: Post-Generation Feedback

**After generation completes**, scan for patterns and write feedback for the ruleset:

1. **Ambiguities** — rules that subagents interpreted differently
2. **Coverage gaps** — categories underrepresented vs planned
3. **Missing rules** — situations with no corresponding ruleset rule
4. **Formula issues** — scoring that produced unexpected results
5. **Litmus test failures** — samples that failed the litmus test (why?)

Save to: `dataset/[client]/[use-case]/rulesets/[domain]_feedback.md`

See [post-generation-feedback.md](../create-ruleset/generation/feedback-loop-format.md) for format.

**Before writing**, check if a `_feedback.md` already exists with an `acknowledged` block. If so, only report NEW issues — skip items that were already acknowledged by create-ruleset. See [interface contract](../shared/interface-contract.md#how-create-data-uses-acknowledgments) for the protocol.

This file is read by `create-ruleset` on the next run, closing the improvement loop.

### Phase 5: Summary Report

```
=== Data Generation Summary ===
Ruleset: [name] (schema v2.0)
Generated: [total] | Verified: [passed] | Pass Rate: [X]%
Duplicates Removed: [count]

Diversity Distribution:
┌─────────────────┬──────────┬──────────┐
│ Dimension       │ Target   │ Actual   │
├─────────────────┼──────────┼──────────┤
│ [dimension]     │          │          │
└─────────────────┴──────────┴──────────┘

Quality: Avg [X] | Min [X] | Max [X]
Output: dataset/[path]/index.json
Feedback: dataset/[path]/rulesets/[domain]_feedback.md
```

---

## Parsing Non-Markdown Files

| File Type | Tool | Fallback |
|-----------|------|----------|
| PDF (text) | `parsers/pdf_parser.py` | If garbled → `parsers/pdf_to_images.py` + Read visually |
| PDF (scanned) | `parsers/pdf_to_images.py` → Read each image | — |
| CSV | `parsers/csv_reader.py` | — |
| PPTX | `parsers/pptx_parser.py` | — |
| Images | Claude's native Read (visual) | — |

Dependencies: `pdfplumber`, `python-pptx`.

---

## Error Handling

| Error | Action |
|-------|--------|
| No ruleset found | **STOP.** Direct to `/create-ruleset`. |
| Ruleset schema < v2.0 | Warn user, suggest `/create-ruleset` upgrade. Proceed only if user overrides. |
| No examples in ruleset | Ask user for 2-3 examples |
| High rejection (>50%) | Pause, ask user to review ruleset |
| Low diversity | Explicitly target underrepresented categories |
| Consensus failure | Log scores, use for prompt improvement |
| **Subagent API error (500/timeout)** | Auto-retry the failed subagent up to 2 times with a 10s delay. If still failing after 2 retries, log which sample IDs failed and continue with successful subagents. After the batch completes, relaunch failed samples as a recovery batch. Never silently drop samples — the user must see the full count. |
| **Subagent produces invalid output** | If output JSON is malformed or missing required fields, treat as a generation failure — re-run with the same brief. Do not attempt to fix malformed output manually. |
| **Formula mismatch detected** | If ai_rating ≠ round(weighted sum of sub-scores), auto-reject the sample. Log the discrepancy. Regenerate with explicit formula verification instruction. This is the #1 defect in scored datasets. |

## Tips

1. **Rotate examples** — don't reuse same few-shot every batch
2. **Track gaps** — fill diversity gaps each batch
3. **Learn from failures** — rejection reasons improve prompts
4. **Edge cases ~10%** — for production realism
5. **Feedback loop** — always write `_feedback.md` so the ruleset improves
