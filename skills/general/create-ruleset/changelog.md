# Create Ruleset Skill — Changelog

## 2026-03-31: Mandatory file type declaration per entity and output

**Problem:** The skill described content fields and texture for each input entity and output, but never required specifying the file type (PDF, JSON, CSV, text string, etc.). During FHS candidate outreach ruleset creation, the user had to ask "which file type will you generate?" because the presentation showed field structures without ever saying "this is a PDF" or "this lives as a JSON field in index.json." Without explicit file types, create-data cannot generate samples — it doesn't know whether to render a file, write a JSON field, or create a separate document.

**Changes:**
- **SKILL.md**: Added "Every Entity and Output Must Declare a File Type" as a new Design Principle. Updated "Input Schema = Structure + Texture" to "Input Schema = File Type + Structure + Texture." Added file type to Step 2 and Step 3 in Phase 2 instructions. Added file type to the Step-by-Step Protocol summary table. Added as hard gate condition #5 in Enough Context definition.
- **template.md**: Added `File Type:` line to Entity and Output templates — mandatory field before content tables.
- **Single Source of Truth table**: Added file types row (lives in INPUT/OUTPUT SCHEMA, not in Test Scenarios or Planning).

**Also updated create-data/SKILL.md**: Steps 2 and 3 now require presenting file type prominently in entity/output headers.

---

## 2026-03-30: Step-by-step presentation, production grounding, client-scoped folders

Major UX and quality improvements based on real-world usage with Booth & Partners CV Screening dataset:

### Step-by-Step Presentation Protocol
- **Problem:** Presenting task + input + output + complexity + sizing in one message overwhelmed the user. They couldn't validate each decision individually.
- **Fix:** Added 5-step incremental presentation protocol. Each step presents ONE concept as an ASCII diagram, waits for user confirmation, then proceeds. Minimum 2 interaction rounds.
- **Templates:** Added ASCII box diagram templates for Agent Task, Input Entity, Complexity Assessment, and Dataset Composition — with emojis for visual hierarchy.

### Ground in Production Data
- **Problem:** Generic domain knowledge produced a ruleset with wrong scoring weights (40/30/15/15 from spec vs 30/30/15/25 in production), wrong output format (JSON vs markdown+rating), and generic examples instead of real Booth data.
- **Fix:** Added Key Insight #10 requiring reading actual agent specs, sample data, production configs, and BUILD_TRACKERs BEFORE writing rules. Includes specific search patterns for finding production data.

### Client-Scoped Folder Structure
- **Problem:** Flat `dataset/rulesets/` doesn't scale for multi-client datasets.
- **Fix:** Changed to `dataset/[client]/[use-case]/{rulesets,seed,augmented}/` structure. Falls back to flat for generic domains.

### Airtight Scoring Formulas
- **Problem:** Expert reviewers caught scoring formulas that could exceed dimension bounds (Role Fit sub-scores summing past 10), unclear multipliers, and missing edge case behavior.
- **Fix:** Added Key Insight #11 requiring explicit bounds (`min(10, ...)`), clear composition formulas, deal-breaker short-circuits, and no ambiguous ranges.

### HTML Review Checkpoint Prominence
- **Problem:** HTML review step was buried in Output Instructions and easy to skip.
- **Fix:** Marked as `⚠️ MANDATORY — DO NOT SKIP` and moved to step 6 with stronger emphasis.

### create-data: Two-Layer File Diversity (Structural + Visual)
- **Problem:** Generated CVs looked visually different (different colors/fonts) but were structurally identical — same section ordering, same bullet depth, same skills format. Varying the "paint" without varying the "architecture" produces monotonous datasets.
- **Fix:** Added "File Diversity — Two Layers" section to create-data skill. Layer 1 (Structural): how the document is organized — section ordering, skills format, bullet style, length, sections included. Domain-specific, defined as templates in the ruleset. Layer 2 (Visual): how it looks — layout, color, font, bullet style. Handled by renderer. Both assigned in the generation brief per sample.
- **Ruleset update:** Added 6 structural templates (Classic, Skills-First, Minimal, Executive, Two-Column Modern, Academic/Cert-Heavy) to CV screening ruleset under Entity 1.
- **Diversity check:** Step 7 (Review) verifies no two samples share the same structural + visual combination.

### create-data: Conflict Detection Between User Feedback and Ruleset
- **Problem:** When user gives feedback that conflicts with the ruleset (e.g., "CV should be PDF" when ruleset says .txt, or "output should be JSON" when ruleset says .md), silently accommodating the change creates a drift between the ruleset (source of truth) and the actual data being generated. Future runs would use the stale ruleset.
- **Fix:** Added Conflict Detection section to create-data skill. Agent MUST flag every conflict with: what the ruleset says, what the user said, the implication, a recommendation, and the question "update the ruleset or treat as exception?"
- **Common conflicts:** input/output formats, scoring weights, field names, distribution percentages, irrelevant industries/roles.

### create-data: Top-Down Conversation Flow (GOAL → SHAPE → EXAMPLE → PLAN → GENERATE → REVIEW)
- **Problem:** Previous protocol was bottom-up and checklist-y — asked user to approve a sample plan before they'd seen what a single sample looks like. The plan was abstract and meaningless without a concrete example.
- **Fix:** Reordered to top-down funnel. Gold standard (Step 3) now comes BEFORE the sample plan (Step 4). User sees a real example first, then evaluates the plan concretely ("44 more like that but across these scenarios").
- **Gold standard is a mini-conversation:** (a) show input first, (b) ask user to rate BEFORE showing output (creates engagement, catches calibration issues), (c) show output and compare, (d) iterate until user says "this is the quality I want." User is a co-creator, not an approver.
- **Phase 1a rewritten:** "Gold Standard — Co-Create with User" replaces the old "Generate + Expert Review" pattern. Expert review still runs but after user approval, not as a gate before the user sees anything.
- **Phase 1b rewritten:** "Dataset Plan — Co-Confirm with User" — plan presented AFTER the gold standard, referencing it concretely.

### create-data: Step-by-Step Protocol, Generation Briefs, Anti-Repetition
- **Step-by-step protocol:** Added 7-step user interaction protocol to create-data skill matching create-ruleset's pattern: ruleset check → sample plan → shared understanding → folder structure → gold standard (iterate) → generate → review together. Never jump straight to generation.
- **Generation briefs:** Each subagent receives a brief that LOCKS structural dimensions (category, industry, geography, format) and FREES content dimensions (names, companies, career stories). No two subagents get the same brief → structural diversity guaranteed.
- **Anti-repetition blocklist:** After each batch, main agent reads index.json and builds a blocklist of names/companies/JD titles already used. Next batch receives blocklist → content diversity guaranteed.
- **Batch sizing:** ≤10 inline, 11-30 = 3 subagents, 31-50 = 5, 51-100 = 10, 100+ = multiple rounds.
- **Client-scoped paths:** Output uses `dataset/[client]/[use-case]/augmented/` with `input/` and `output/` subfolders per sample.

### Narrative Use Case Replaces Validation Rules
- **Problem:** Validation rules are rigid checklists that constrain generation. "Career timeline must be plausible" blocks the contradictory-timeline adversarial test case. "Skills count must match career stage" blocks the keyword-stuffed CV. Rules assume all data should be "correct" — but adversarial data is intentionally wrong.
- **Fix:** Removed VALIDATION RULES section entirely. Expanded DOMAIN CONTEXT into a narrative Use Case with universal 4-part structure: (1) The Context — company, agent, production environment; (2) Real-World Inputs — what the agent actually receives; (3) Three Layers of Difficulty — realistic → challenging → deceptive, with quality guidance embedded per layer; (4) The Litmus Test — one question to check any sample against.
- **Impact:** Quality guidance now lives inside the narrative, not as rigid rules. Happy path data is guided toward realism. Adversarial data is explicitly encouraged to break realism. Both coexist naturally.
- **Template:** Structure is domain-agnostic — works for CV screening, insurance claims, customer support, code generation, anything.

### Variation Dimensions Folded Into Per-Category Composition
- **Problem:** Variation Dimensions section duplicated information already in Composition by Coverage Category. Some dimensions appeared in both, with conflicting values.
- **Fix:** Removed standalone Variation Dimensions section. All dimensions now live in the per-category tables, showing how each dimension shifts per category (happy path = clean, edge = messy, adversarial = deceptive-but-clean). YAML block in ruleset preserved for machine-readable access.

### Two-Dimension Complexity Framework
- **Problem:** Old framework conflated agent logic complexity with input variety. CV screening scored "Hard" because it has many input formats — but the agent's logic is a simple linear pipeline. A simple agent processing 10 file formats is still a simple agent.
- **Fix:** Split into two separate dimensions:
  - **Agent Complexity** (4 signals: Logic Depth, Output Complexity, JTBD, Domain Judgment) → determines test case DEPTH
  - **Input Surface Area** (3 factors: Format variety, Structural variety, Language) → determines test case BREADTH via ×1.25 multiplier
- **Impact:** CV Screening went from Hard (50 samples) to Medium complexity + High surface (35 base × 1.25 = 45 samples). Same ballpark, but correctly justified.

### 4-Layer Validation Rules
- **Problem:** All validation rules were mechanical (score math, rating mapping). None checked whether the data was REALISTIC — whether a CV looked like a real person's career, whether a JD would actually get posted, whether the evaluation showed real recruiter expertise.
- **Fix:** Added 4 layers:
  - Layer 1: CV Realism (8 rules — career timeline, skills count, progression, metrics, company-role fit)
  - Layer 2: JD Realism (6 rules — must-have count, tech age, seniority-requirements match, salary-geography)
  - Layer 3: Evaluation Quality (8 rules — requirement coverage, semantic matches, recruiter judgment, specificity)
  - Layer 4: Mechanical Correctness (7 rules — existing score math, rating mapping, etc.)

### Human-Readable Planning Section
- **Problem:** Complexity assessment and dataset sizing were buried in a machine-readable YAML block. The HTML review just said "50 samples" with no reasoning visible.
- **Fix:** PLANNING section now has 4 human-readable subsections: Purpose (why `score`), Complexity Assessment (4-signal table with evidence), Dataset Size (sizing table lookup), Coverage Distribution (base + adjustments). YAML metadata preserved at the bottom for `create-data` to read.

### Per-Category Composition
- **Problem:** Variation dimensions were defined globally but each coverage category (happy/edge/error/adversarial) needs DIFFERENT dimension profiles. Happy path should use clean data; edge cases should use messy data; adversarial should use clean-but-deceptive data.
- **Fix:** Added "Composition by Coverage Category" section to ruleset, HTML review, and skill instructions. Each category specifies its typical format mix, completeness, text quality, and expected ratings.

### Expert Reviewer Enhancement
- **Problem:** Completeness reviewer didn't cross-reference source documents.
- **Fix:** Completeness reviewer subagent now receives source document paths alongside the ruleset and rubric.

### Variation Dimensions Completeness
- **Problem:** Diversity reviewer found dimensions in Input Framework tables that were missing from the YAML block.
- **Fix:** Added explicit rule: "Every dimension that appears in any table MUST also appear in the YAML block."

## 2026-03-30: Add schema inference from existing data (LAB-115)

- Created `resources/schema-inference.md` — documents how to detect input/output structure from existing samples: file types, field patterns, nesting level, document count per sample
- Added Step 1b (schema inference) to Phase 1 in SKILL.md — runs silently after data discovery, reads 2-3 samples to detect structure
- Added inferred data structure to the Phase 1 Step 2 unified summary — presented side-by-side for user confirmation before proceeding
- Updated "How to use findings" section to trigger schema inference for seed, augmented, and gold standard data
- Also updated create-data SKILL.md Phase 0 with matching schema inference step (step d) and updated smart defaults

## 2026-03-27: Add dataset consultation workflow (LAB-116)

- Created `resources/best-practices.md` — concrete sizing table (purpose x complexity), coverage distributions, 5 complexity signals with thresholds, 5 anti-patterns with remediation
- Added "Dataset Planning Consultation" workflow to SKILL.md between Phase 1 (agent task) and Phase 2 (structure proposal): purpose -> complexity -> sizing -> optional research -> approval gate
- Updated `template.md` with `PLANNING` section in ruleset output (purpose, complexity, signals, size, coverage split, research file, approval metadata)
- All planning values reference best-practices.md — no hardcoded numbers in the skill
