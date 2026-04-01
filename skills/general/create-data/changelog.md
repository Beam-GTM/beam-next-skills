# create-data Skill Changelog

## 2026-03-31 — 2-Expert Gold Standard Review + Skill Reorganization

### 2-Expert Review System

**Problem:** Gold standard review used a single generic expert persona that tried to cover realism, coverage, and adversarial in one pass. This conflated two orthogonal failure modes: (1) "looks realistic but output was confabulated" and (2) "correctly derived but unrealistically clean." create-ruleset already had 3 distinct expert personas; create-data had none.

**Changes:**
- **experts/expert-1-production-fidelity.md**: New. "The Practitioner" — production fidelity critic inspired by Nassim Taleb's antifragility framework. Uses a "Fragility Scan" to stress-test gold standards against production messiness. 5-point audit: input realism, output derivation correctness, structural fidelity, edge case stress test, pairing correctness.
- **experts/expert-2-derivation-auditor.md**: New. "The Calibrator" — statistical & derivation auditor inspired by Daniel Kahneman's dual-process theory. Uses an "Output Trace" to independently re-derive outputs and catch confabulation, anchoring bias, and base rate neglect. 5-point audit: derivation trace, scoring calibration, distribution alignment, category fit, cross-sample independence.
- **SKILL.md**: Updated Phase 1a to mandate 2 parallel expert subagents for gold standard review. Both must pass (avg >= 7.5, no dim < 6.0). Added expert table with persona files, focus areas, and mental models.
- **resources/review-loop.md**: Rewrote Phase 1 to reflect 2-expert parallel review protocol. Updated fix loop to merge feedback from both experts before fixing. Updated pass criteria and review output format.
- **resources/expert-persona.md**: Retained as the generic batch reviewer for Phase 3b (post-batch review). Not used for gold standard review.

### Skill Reorganization

**Changes:**
- **Moved** `scripts/anthropic-api-benchmark.py` and `scripts/cost-model.py` → `04-workspace/benchmarks/`. These are API performance testing tools unrelated to data generation.
- **Flattened** `memories/changelog.md` → `changelog.md` at skill root. Single file didn't need a folder.

---

## 2026-03-31 — Mandatory file type in Steps 2 and 3

**Problem:** Steps 2 (Input) and 3 (Output) presented content fields and texture but did not require showing the file type per entity/output. During FHS candidate outreach data generation, the user had to ask "which file type will you generate?" because the presentation showed field structures without saying "this is a PDF" or "this is a JSON string in index.json."

**Changes:**
- **SKILL.md**: Updated Step 2 to require file type per entity in the header (e.g., "📥 INPUT ENTITY 1: Resume — PDF file"). Updated Step 3 to require file type per output in the header (e.g., "📤 OUTPUT 1: SMS Messages — JSON strings in index.json"). Both steps now state file type is mandatory.

**Root cause:** create-ruleset also lacked this requirement — fixed in parallel (see create-ruleset changelog).

---

## 2026-03-31 — Visual Diversity Protocol for Rendered PDFs

**Added Visual Diversity Protocol** — enforces that every rendered PDF in a dataset is visually unique, not just content-unique.

**Problem solved:** When generating batches of PDFs (CVs, invoices, etc.), all files used similar render spec compositions (same layout structure, same section ordering, same visual elements) despite different colors/fonts. This produced unrealistic datasets — production documents come from hundreds of different templates and look wildly different from each other.

**Changes:**
- **resources/file-generation.md**: Added "Visual Diversity Protocol (CRITICAL)" section with mandatory 6-dimension diversity matrix (layout, color, font, section order, visual elements, header style). Each PDF must differ on 3+ dimensions. Includes diversity tracker requirement, anti-patterns, and 8 example structurally different templates.
- **SKILL.md**: Updated Phase 2 step 4 to reference the Visual Diversity Protocol with explicit cross-reference to the resource file. Updated step 6 to track visual diversity alongside content diversity.

**Key design decisions:**
- 6 diversity dimensions identified: layout, color_scheme, font, section_order, visual_elements, header_style
- Minimum 3 of 6 must differ between any two PDFs in the same batch
- Diversity tracker maintained across the batch (list of used combinations)
- 8 concrete template examples provided as composition references (corporate sidebar, messy plain text, classic academic, modern creative, executive, two-column split, infographic-style, skills-first)

---

## 2026-03-30 — Coverage Analysis Phase (LAB-90)

**Added Phase 0.5: Coverage Analysis** — maps existing client I/O pairs against ruleset edge cases and variation dimensions before generation.

**Problem solved:** The skill previously generated synthetic data from scratch even when clients provided real examples (~50% of clients do). This caused duplicate data and wasted generation cycles. Discovered during Betterment test run by Hassaan.

**Changes:**
- **SKILL.md**: Added Phase 0.5 between Phase 0 (context gathering) and Phase 1 (initialization). Accepts client I/O pairs in 3 formats: JSON array, CSV, folder of files. Uses a classification subagent to map each sample against the ruleset's edge cases and variation dimension slots. Produces a coverage report with a gap matrix and additive generation brief.
- **SKILL.md**: Updated Phase 1c to be coverage-aware — variation matrix now subtracts covered slots and only targets gaps when a coverage report exists.
- **SKILL.md**: Updated Phase 2 deduplication to explicitly check against client I/O pairs, not just gold standards.
- **resources/coverage-report-template.md**: Created template for coverage matrix output — defines report structure (summary, edge case matrix, variation dimension tables, additive brief), classification logic, and input format support.

**Key design decisions:**
- Analysis-only mode (`--analyze-only`) stops after producing the coverage report — no generation
- Coverage report is saved to `dataset/augmented/[domain]/coverage-report.md` for downstream consumption
- Additive-only constraint: every suggestion is verified against existing samples to guarantee zero duplication
- Classification uses subagents (not inline) for fresh-context evaluation of each sample

**Dependencies:** LAB-87 (data discovery) provides input paths. LAB-112 (downstream) consumes coverage report for gap-targeted generation. LAB-116 consumes coverage report for complexity assessment.
