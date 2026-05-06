---
name: create-ruleset
description: Create a ruleset for synthetic data generation. Use when the user wants to define rules for generating training data, create a new dataset domain, or set up data augmentation guidelines.
argument-hint: [optional context from user message]
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Agent, AskUserQuestion
---

# Create Ruleset for Synthetic Data Generation

## Why This Skill Exists

AI agents need test data, but crafting test data by hand is slow, biased toward happy paths, and misses edge cases. A **ruleset** is the blueprint that tells `create-data` exactly what to generate — what the agent receives, what it should produce, and what makes each test scenario hard.

**Why a ruleset instead of just "generate some test data"?** Without a ruleset, generated data lacks three things: (1) **coverage** — it misses the scenarios that break agents in production, (2) **realism** — inputs are artificially short and clean, and (3) **consistency** — each generation run produces different quality levels. The ruleset solves all three by encoding what "production-realistic" means for this specific agent.

**Why HTML?** The ruleset is a single self-contained HTML file that is human-readable in a browser AND machine-readable by `create-data`. No external dependencies, no build step. A stakeholder can open it in Chrome and understand what data will be generated. The agent can parse its structured sections to build generation briefs.

**Domain-agnostic** — works for any use case: refund analysis, insurance claims, customer service, code generation, document creation, financial analysis, vehicle telemetry, etc.

## Core Principles

1. **Agent-first framing.** The domain name alone (e.g., "CV generation") is ambiguous. Clarify the agent's task before proposing content. Think: agent input → agent processing → agent output. **Why:** The same domain can have completely different agents. "CV generation" could mean "generate a CV from a profile" or "screen a CV against a job description." The task determines what the ruleset covers.

2. **Step-by-step presentation.** Never dump everything at once. Walk through each concept incrementally and get alignment before moving on. See the [Step-by-Step Protocol](#step-by-step-presentation-protocol). **Why:** Users can't evaluate 5 dimensions at once. Presenting one at a time with a confirmation question catches errors early — a wrong assumption at Step 1 cascades through the entire ruleset if not caught.

3. **Ground in production data.** Read the actual agent spec, sample inputs/outputs, production scoring weights, and integration details BEFORE writing rules. Generic assumptions produce rulesets that don't match reality. Search the workspace for agent specifications, build trackers, sample data, and client-specific working documents — discover their locations rather than assuming fixed paths. **Why:** A ruleset built from generic domain knowledge produces generic test data. A ruleset built from real samples produces data that matches what the agent actually encounters. The difference shows up immediately in generation quality.

4. **Be opinionated.** For well-known domains, propose reasonable defaults. Only ask when you genuinely cannot infer the answer from domain knowledge or discovered data. **Why:** Asking too many questions slows the user down and makes them feel like they're doing the work. Propose a default with rationale — the user corrects if wrong, confirms if right. Either way, faster.

5. **Hypothesis-driven.** Explore before proposing. Ask when you lack information. Propose hypotheses when you have information. Never generate until you have "enough context" (see [Generation Gate](#enough-context-definition)). **Why:** Flagging hypotheses (🔶) makes assumptions visible. The user can confirm or correct. Unflagged assumptions become invisible errors in the ruleset that surface as bad data during generation.

6. **ASCII diagrams + emojis.** Use the templates in [resources/ascii-box-templates.md](resources/ascii-box-templates.md) for all proposals. Add footnote citations and flag hypotheses (see [Presentation Rules](#presentation-rules)). **Why:** Visual structure makes complex information scannable. The user processes a box diagram in 5 seconds vs. 30 seconds for equivalent prose. Footnotes and hypothesis flags add traceability without cluttering the content.

## Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Context Discovery | [context-discovery.md](context-discovery.md) | Auto-discovery of client/project files |
| Schema Inference | [generation/schema-inference.md](generation/schema-inference.md) | Detect input/output structure from existing data |
| Template | [resources/ruleset-section-structure.md](resources/ruleset-section-structure.md) | Exact output format (schema v2.0) |
| Examples | [resources/few-shot-examples.md](resources/few-shot-examples.md) | Complete production-quality sample rulesets |
| Best Practices | [generation/sizing-and-coverage.md](generation/sizing-and-coverage.md) | Sizing, coverage, complexity classification |
| Review Protocol | [experts/review-protocol.md](experts/review-protocol.md) | 3-expert review system, iteration protocol, exit conditions |
| Expert 1: Priya | [experts/expert-1-production-realism.md](experts/expert-1-production-realism.md) | Data Quality Lead — spec-vs-reality audit, content length, file structure, texture, source fidelity |
| Expert 2: James | [experts/expert-2-internal-consistency.md](experts/expert-2-internal-consistency.md) | Solutions Architect — cross-reference audit, schema↔examples, derivation↔output, composition math |
| Expert 3: Tomoko | [experts/expert-3-generative-readiness.md](experts/expert-3-generative-readiness.md) | Data Generation Engineer — pipeline feasibility, variation axes, named slots, anti-patterns |
| Presentation Templates | [resources/ascii-box-templates.md](resources/ascii-box-templates.md) | ASCII box diagram templates |
| Post-Generation Feedback | [generation/feedback-loop-format.md](generation/feedback-loop-format.md) | Feedback loop from create-data |
| HTML Review Template | [resources/ruleset-review-template.html](resources/ruleset-review-template.html) | Human-readable review document template |
| Input Parsers | [parsers/](parsers/) | PDF, CSV, PPTX extraction scripts |
| Interface Contract | [../shared/interface-contract.md](../shared/interface-contract.md) | What create-data expects from the ruleset |

**Parsers:** `parsers/pdf_parser.py` (text), `parsers/pdf_to_images.py` (visual), `parsers/csv_reader.py`, `parsers/pptx_parser.py`. For scanned PDFs: convert to images then `Read` visually.

---

## Phase 0: Resolve What to Build

**Start here. Always.** Determine what you're building before searching.

**Three entry states:**

| User provides | Action |
|---------------|--------|
| Client + specific use case (e.g., "Booth, CV screening") | Skip to Phase 1 with both |
| Client only, no use case (e.g., "create ruleset for Volkswagen") | → **Phase 0b: Use Case Discovery** |
| No client, no use case | Ask: *"What data do you want to create a ruleset for? Which client or domain?"* |

### Phase 0b: Use Case Discovery (client mentioned, no specific use case)

**Goal:** Exhaust all available repo context, then present grounded use case options with a recommendation. Do NOT ask the user to pick before you've done the research.

**Step 1: Silent deep-dive** — Launch parallel subagents:

**a) Account context** — Explore subagent:
- Search the workspace for the client's project folder. Look for directories or files named after the client (case-insensitive) that contain project artifacts: overview docs, strategy docs, proposals, workstream folders, meeting notes, transcripts.
- Also grep the entire repo for the client name (case-insensitive) to catch mentions in multi-client docs, transcripts, and other accounts.
- Check for partnership or integration docs mentioning the client.

**b) Existing data** — Explore subagent:
- Find any existing rulesets for this client — look for `*.html` files with `schema_version` in their frontmatter, scoped to client-named directories.
- Find any existing dataset directories for this client — look for folders containing `rulesets/`, `seed/`, or `augmented/` subdirectories under client-named paths.
- Also scan for rulesets from other clients (for pattern reference) — any `*.html` files with `schema_version` frontmatter.

**c) Web research** (if external company): Search for the company's products, AI initiatives, and public information relevant to agent use cases. Save as `notes/{company-slug}-research.md`.

**Step 2: Read key docs** — After subagents return, read the **most important files yourself** (proposals, agent specs, technical docs). Don't rely solely on subagent summaries for documents that describe the agent's architecture, input/output, or technical behavior. The subagent finds them; you read them.

**Step 3: Synthesize and present use cases** — Present a table of grounded use case options:

```
┌───┬──────────────────────────┬──────────────────────────────────────┬──────────┐
│ # │ Use Case                 │ What the Agent Does                  │ Fit      │
├───┼──────────────────────────┼──────────────────────────────────────┼──────────┤
│ 1 │ [name]                   │ [receives X → produces Y]            │ [rating] │
│ 2 │ [name]                   │ [receives X → produces Y]            │ [rating] │
│ 3 │ [name]                   │ [receives X → produces Y]            │ [rating] │
└───┴──────────────────────────┴──────────────────────────────────────┴──────────┘
```

**Requirements for each use case:**
- Grounded in specific repo files (cite which doc it comes from)
- Concrete enough to define input/output (not vague labels)
- Rated by fit: how well-documented is this agent in the repo? How concrete are the I/O specs?

**Step 4: Recommend one** — State which use case to build first and why. Structure the reasoning:
- Why this one first (most concrete I/O, feeds other use cases, closest to production)
- Why not the others first (too abstract, depends on this one, less documented)

**Step 5: Wait for user confirmation** — User picks a use case (or accepts recommendation). THEN proceed to Phase 1 with the chosen use case.

**CRITICAL:** Do not present Step 1 (Agent Task) until the use case is chosen. Phase 0b resolves WHAT to build; Phase 1+ resolves HOW to build it.

---

## Phase 1: Gather Context

**Goal:** Do all searching silently, then present ONE cohesive summary. By this point, the use case is already chosen (from Phase 0 or Phase 0b).

### Step 1: Search via subagents (silent — no user interaction)

Launch these **in parallel**:

**a) Repo scan** — Explore subagent (scoped to client):
- Find existing rulesets for this client — `*.html` files with `schema_version` frontmatter in client-scoped directories. Note: domain, agent task, has planning section?
- Find seed data — `*.json` files in directories named `seed/` under the client's dataset path. Note: topics, example counts, read 1-2 representative entries.
- Find augmented data — directories named `augmented/` under the client's dataset path. Note: domains, sample counts, gold standards, coverage from any `index.json`.
- Find feedback files — `*_feedback.md` files alongside rulesets. Note: any post-generation feedback from previous runs.

**b) Context discovery** (if client name mentioned): Follow [context-discovery.md](context-discovery.md).

**c) Web research** (if company name mentioned and not already done in Phase 0b): Search and save as `notes/{company-slug}-research.md`. Skip if already done or no company name.

**Note:** If Phase 0b already ran, much of this context is already loaded. Don't re-search what you already have — just supplement with any use-case-specific files not yet read (e.g., agent specs, sample data for the chosen use case).

### Step 1b: Schema inference (silent)

If Step 1 found existing samples, infer input/output schema per [generation/schema-inference.md](generation/schema-inference.md). Read 2-3 samples, detect structure, apply defaults.

### Step 2: Present findings + Step 1 of Protocol

**First message covers:**
1. **What exists** — "Found existing ruleset X, 50 augmented samples, seed data for Y." If a related ruleset exists, ask if this is a replacement, extension, or new thing.
2. **Inferred schema** (if data found) — briefly show what you detected.
3. **Step 1: Agent Task** — Present as ASCII box (see templates). Ask user to confirm.

**Do NOT present input structure, output structure, complexity, or sizing yet.** Those come in subsequent steps.

### Step 3: Fill gaps (only if needed)

If critical gaps remain after the user responds, ask targeted questions. If you have enough context, proceed directly to Phase 2.

### How to use findings

- **Existing ruleset**: Pre-populate from it. Don't re-ask answered questions.
- **Feedback file** (`_feedback.md`): Pre-apply recommended fixes. If an `acknowledged` block already exists, skip those items — they were applied in a previous cycle. After incorporating new feedback, append an acknowledgment block per [../shared/interface-contract.md](../shared/interface-contract.md#direction-create-ruleset--create-data).
- **Seed/augmented data**: Infer schema. Ground proposals in real values.
- **Gold standards**: Use as quality anchors.
- **Nothing found**: New domain — ask more from the user.

---

## Phase 2: Walk Through Steps 2-4

Continue through the [Step-by-Step Protocol](#step-by-step-presentation-protocol). Each step is a separate message with an ASCII diagram from [resources/ascii-box-templates.md](resources/ascii-box-templates.md).

**Step 2 (Input):** Each entity with **File Type** (what format in production AND in the generated dataset — e.g., "PDF file rendered per sample" or "JSON object in index.json") + Content fields + Content Texture (what the data looks like in production — styles, lengths, structural characteristics). NO presentation/variation distributions here — those live exclusively in Test Scenarios. **File type is mandatory per entity** — without it, create-data cannot generate samples.

**Step 3 (Output):** **File Type per output** (same as input — specify exact format in the dataset) + fields, scoring dimensions, constraints. Include Output Derivation Procedure if scoring is involved. **File type is mandatory per output** — the generator needs to know whether to write a rendered file, a JSON field, or a separate document.

**Step 4 (Test Scenarios & Sizing):** Present ALL 3 purposes (flow_check/score/battle_test), then for the chosen purpose show the scenario cards: each with What (the setup), Why it's hard (the challenge), Varies (parameter distributions). This replaces the old separate Complexity, Sizing, Pairing Strategy, and Per-Category Composition steps.

**After Step 4 approval → generate the ruleset.** No further interaction needed until the review.

**CRITICAL:** Before presenting input/output, READ the actual agent spec and sample data. Use real field names, scoring weights, and format distributions. If spec and deployment differ, use deployment values and document the deviation.

---

## Phase 3: Refine (if needed)

If the user provides corrections:
1. Incorporate feedback
2. Propose remaining gaps as recommendations ("I'd also recommend including X — sound good?")
3. Only ask open-ended questions for truly user-specific context

---

## Step-by-Step Presentation Protocol

**Never present the full proposal in one message.** Minimum 2 interaction rounds.

| Step | Present | Wait for |
|------|---------|----------|
| **1. Agent Task** | What the agent receives, does, produces. One ASCII box. | Confirm or correct |
| **2. Input Structure** | Entities with **File Type** + Content fields + Content Texture. ASCII boxes per entity. | Confirm or add |
| **3. Output Structure** | **File Type per output** + fields, scoring, constraints, derivation procedure. ASCII box. | Confirm |
| **4. Test Scenarios & Sizing** | All 3 purposes first. Then for the chosen purpose: scenario cards with What/Why it's hard/Varies. | Pick purpose, confirm scenarios |

**Collapsing:** If user moves fast ("looks good"), batch Steps 2+3. Never batch all 4.

**"Generate now" override:** Proceed with smart defaults for remaining steps. Mention what you assumed.

---

## Presentation Rules

**Use ASCII box diagrams** from [resources/ascii-box-templates.md](resources/ascii-box-templates.md) for ALL proposals.

### Citation Style: Footnotes

- Superscript numbers (¹ ² ³) next to claims in the content area
- `Sources` footer section inside the same box (separated by `├───┤`)
- One line per source: footnote number + short label + file name
- Only cite when provenance matters

### Hypothesis Flagging

- A hypothesis is any claim NOT directly stated in a source document
- `🔶 Hypotheses` section below Sources (or as sole footer if no sources)
- Each bullet: the claim + why you assumed it
- Once user confirms, promote to grounded fact in subsequent steps

### Three-Tier Box Structure

1. **Content** — the proposal (facts with footnotes)
2. **Sources** — footnoted references
3. **Hypotheses** — flagged inferences to confirm

---

## Expert Readiness Evaluation

Run internally after each user response. Three experts evaluate gathered context:

**1. Domain Expert** — Are business rules specific enough? (concrete thresholds, not vague principles)
**2. Data Engineer** — Can I build diverse data? (clear input/output patterns, 3-4 distinct scenarios)
**3. Quality Evaluator** — Can I judge good from bad? (unambiguous correctness criteria, known edge cases)

**Decision logic:**

| Experts satisfied | Action |
|---|---|
| 0-1 | Well-known domain: fill gaps with recommendations. Unfamiliar: ask about critical gap. |
| 2 (one has concerns) | Present concerns as recommendations with defaults. Proceed unless user objects. |
| All 3 | Proceed to generation. |

Frame concerns as recommendations, not questions. "I'd recommend these edge cases: [list]" not "What edge cases should I include?"

---

## Enough Context Definition

**Hard gate — do NOT generate until ALL conditions are met:**

| # | Condition | How to verify |
|---|-----------|---------------|
| 1 | Agent task is unambiguous | Confirmed with user in Step 1 |
| 2 | Existing project data checked | Ran Explore subagent to find client's dataset directory |
| 3 | Relationship to existing data clear | Asked user if replacement/extension/new |
| 4 | Input structure concrete (fields + value ranges) | Have example or user described it |
| 5 | File type declared for every input entity and output | Each has explicit format (PDF, JSON, text string, etc.) |
| 6 | Output structure concrete | Have example or user confirmed |
| 7 | Core business rules specific (thresholds, not platitudes) | Rules say "reject if < 60%" not "reject if low" |
| 8 | At least 3 distinct scenarios defined | Discussed categories with user |
| 9 | User-specific context captured | Asked about unique constraints or confirmed N/A |

**Soft conditions** (aim for, can proceed without): edge cases (3-5), distributions, anti-patterns, few-shot examples, quality criteria.

**User override:** "generate now" with 0-1 experts → use defaults + mention assumptions. With 2+ experts → proceed immediately.

---

## Interview Principles

1. Use AskUserQuestion for structured choices (task type, output format)
2. Assume first, ask second — propose defaults for well-known domains
3. Batch assumptions — let user approve/override in one go
4. Recommendations, not open-ended questions
5. Allow multi-part responses; skip answered questions

**Override keywords:** "generate now" → proceed. "skip"/"defaults" → use defaults. "looks good" → accept.

---

## Smart Defaults

| Field | Default |
|-------|---------|
| Context Levels | Minimal 20%, Standard 50%, Detailed 25%, Full 5% |
| Complexity | Simple 40%, Standard 40%, Complex 20% |
| Edge Cases | ~10% of dataset |
| Tone | Formal 60%, Conversational 40% |
| Code Styles | Compact 20%, Standard 30%, Detailed 30%, Error Handling 20% |

---

## Design Principles

These principles govern the structure and content of every ruleset. They emerged from production use and iteration — follow them strictly.

### Single Source of Truth (No Duplication)

Each piece of information appears in exactly ONE section. If it appears in two places, consolidate it.

| Information | Lives in | NOT in |
|---|---|---|
| File types (per entity and output) | INPUT SCHEMA + OUTPUT SCHEMA (File Type line) | Test Scenarios, Planning |
| Field names, types, constraints | INPUT SCHEMA | Test Scenarios |
| Content styles, lengths, structural characteristics | INPUT SCHEMA (Content Texture) | Test Scenarios |
| Variation dimensions and distributions | TEST SCENARIOS (Varies chips) | Input Schema |
| Sample counts per scenario | TEST SCENARIOS (card headers) | Separate Planning section |
| Complexity/sizing metadata | Hidden YAML comment | Visible section |

**Why:** Duplication causes drift. When two sections define the same dimension with different distributions, the generator doesn't know which to trust.

### Every Entity and Output Must Declare a File Type

Each input entity and each output must specify its **file type** — the exact format in production AND in the generated dataset. This is non-negotiable.

Examples:
- "PDF file (rendered per sample via file_renderer.py)"
- "JSON object in index.json"
- "text string in index.json"
- "CSV file per sample"
- "DOCX file (rendered per sample)"
- "XLSX file (rendered per sample)"
- "separate .md file per sample"

**Any file type is valid.** create-data has pre-made reference scripts for PDF, DOCX, XLSX, CSV, JSON, and TXT. For other formats (PPTX, HTML, ODF, RTF, etc.), create-data will write a task-specific generation script using the PDF renderer pattern as a structural template. **Do not limit file types to what the renderer currently supports** — if the agent processes DOCX files in production, the ruleset should say DOCX. create-data handles the generation.

**Why:** Without an explicit file type, create-data cannot generate samples. It doesn't know whether to render a PDF, write a JSON field, or create a separate file. This was the #1 source of ambiguity in early rulesets — the skill described fields and texture but never said "this is a PDF." The user had to ask, and every answer changed the generation plan.

**Where it lives:** In the INPUT SCHEMA and OUTPUT SCHEMA sections, as a `File Type:` line immediately after each entity/output header — before the content fields table. See [ruleset-section-structure.md](resources/ruleset-section-structure.md) for exact format.

### File Generation Must Produce Production-Realistic Visual Diversity

When a file type is declared (PDF, DOCX, XLSX, etc.), the ruleset should describe what that file looks like **in production** — not just the content, but the visual characteristics that vary across real-world sources. This helps create-data generate files that look like they came from different templates, tools, and people — not a uniform batch.

Include in the INPUT SCHEMA's Content Texture (or OUTPUT SCHEMA for output files):
- What visual variations exist in production (e.g., "CVs come from Word, Canva, LaTeX, LinkedIn export, ATS systems — wildly different layouts")
- What structural characteristics vary (e.g., "invoices range from 3-line to 50-line items, some have logos, some are plain text")
- What formatting conventions exist (e.g., "spreadsheets use different header styles, column widths, color schemes depending on the department")

**Why:** create-data applies a visual diversity protocol where every generated file must differ on 3+ dimensions (layout, color, font, structure, spacing, etc.). The more production context the ruleset provides about what real files look like, the more realistic the generated diversity will be.

### Input Schema = File Type + Structure + Texture (Not Variation)

Input Schema answers: **"What format is it, what does it contain, and what does it look like?"**
- File Type: the exact file format (PDF, JSON, CSV, text string, etc.)
- Content fields (table): field names, types, constraints
- Content Texture: what the content actually looks and feels like in production — writing styles, typical lengths, structural characteristics (subheadings, quotes, data tables)

Input Schema does NOT answer: "How does it vary across scenarios?" — that's Test Scenarios.

**Why:** Mixing structure and variation in one section forces the reader to mentally separate "what exists" from "how it shifts." Keeping them apart means each section has one job.

### Test Scenarios = What / Why / Varies

Each scenario card has three parts:
- **What**: The setup — what inputs land on the agent's desk (1-3 sentences)
- **Why it's hard**: The specific challenge this scenario tests (1-3 sentences)
- **Varies**: Parameter distributions as chips with percentages — the machine-readable part

**Why:** "What" and "Why" give the human reader context. "Varies" gives the generator instructions. Three questions, three sections — no ambiguity about what each part does.

### Scenario Names Must Be Self-Descriptive

A non-technical person should understand the scenario from its title alone, without reading the description.

| Bad | Good | Why |
|---|---|---|
| "Broken Input" | "Missing & Corrupted Articles" | Names what's actually wrong |
| "Sparse & Noisy Batch" | "Gaps, Paywalls & Stale Articles" | Names the specific challenges |
| "Edge Case" | "Low-Visibility Executive, Vague Purpose" | Names the difficulty factors |
| "Happy Path" | "Known Partner, Rich Data" | Names what makes it easy |

**Why:** Scenario names are the first thing a reader scans. Generic labels like "Edge Case #2" force them to read the description. Descriptive names make the scenario table self-documenting.

### Anti-Patterns: Domain + Generic LLM

Every ruleset must include BOTH types of anti-patterns:

**Domain-specific** (unique to this agent): e.g., "generic implications that don't name AF divisions"

**Generic LLM failures** (apply to any generated data):
- Under-target sizing (fewer items/shorter content than schema requires)
- Hallucinated sources (fabricating URLs, quotes, statistics)
- Placeholder content ("[TBD]", "Company X", "John Doe")
- Repetitive structure (every sample follows identical patterns)
- Monotonous recommendations (every implication says "monitor developments")

**Why:** Domain anti-patterns prevent wrong data. Generic anti-patterns prevent lazy data. Most generation failures are in the generic bucket — LLMs optimize for brevity and template-following unless explicitly told not to.

### Planning is Metadata, Not a Section

Complexity signals, surface area factors, and sizing calculations are planning artifacts used during the step-by-step protocol. They don't belong in the final ruleset as a visible section — they clutter the document.

**Keep as:** Hidden YAML comment in the HTML (machine-readable for create-data)
**Show instead:** Sample counts in Test Scenario card headers (e.g., "7 samples")

**Why:** The reader of a ruleset cares about WHAT to generate (scenarios + distributions), not HOW the sizing was calculated.

---

## Output Instructions

After Step 4 approval, generate **a single HTML ruleset file**. This is the only output — no separate `.md` file.

### Folder Structure (Client-Scoped)

**Discover, don't assume.** Before creating output directories, find where this client's data lives:

1. Search the workspace for an existing dataset directory for this client (e.g., a folder named after the client containing `rulesets/`, `seed/`, or `augmented/` subdirectories).
2. If found, use that location. Create the use-case subfolder within it.
3. If not found, search for a top-level datasets directory in the workspace (common names: `dataset/`, `datasets/`, `data/`, `training-data/`). Create the client folder there.
4. If no datasets directory exists at all, create `dataset/` at the workspace root as the default.

**Expected structure once resolved:**

```
[datasets-root]/
└── [client-name]/              # e.g., booth-and-partners
    └── [use-case]/             # e.g., cv-screening
        ├── rulesets/
        │   └── [domain].html   # The ruleset (ONLY OUTPUT)
        ├── seed/               # Populated later
        └── augmented/          # Populated by create-data
```

If no client specified (generic domain), save to `[datasets-root]/rulesets/[domain].html`.

### Generation Steps

1. **Resolve output path** — Follow the folder structure discovery above, then `mkdir -p [resolved-path]/{rulesets,seed,augmented}`

2. **Generate the ruleset HTML** using [resources/ruleset-review-template.html](resources/ruleset-review-template.html) (schema_version: "2.0"). Follow the section structure from [ruleset-section-structure.md](resources/ruleset-section-structure.md) for content guidance. Must include:
   - USE CASE narrative (4-part: Context, Real-World Inputs, Three Layers of Difficulty, Litmus Test)
   - INPUT SCHEMA (per-entity: Content field tables + Content Texture description. NO presentation/variation chips — those live in Test Scenarios)
   - OUTPUT SCHEMA + DERIVATION PROCEDURE (fields table + quality constraints + numbered derivation steps)
   - TEST SCENARIOS (scenario cards with What/Why it's hard/Varies — each card includes parameter distributions as chips. This replaces the old Pairing Strategy + Per-Category Composition)
   - PLANNING (hidden YAML comment with machine-readable sizing data — NOT a visible section)
   - FEW-SHOT EXAMPLES (3-5 example cards with input/output/derivation). See Few-Shot Example Rules below.
   - ANTI-PATTERNS (3+ domain-specific + 3+ generic LLM anti-patterns)
   - OPEN QUESTIONS (only if uncertainties exist — omit entirely if none)

**Few-Shot Example Rules (CRITICAL):**
   - **Input articles/documents must be realistic length.** Do NOT write artificially short 3-sentence inputs. Include 3-4 substantial paragraphs showing the real structure (quotes, data points, analyst reactions), then use `...` followed by a bracketed note indicating the full article length and what the remaining content covers. Example: `...\n\n[Article continues with state incentives and union negotiations — ~450 words total]`
   - **Input specifications must be visible.** Each few-shot input should demonstrate the structural characteristics described in the INPUT SCHEMA (e.g., wire-service vs analytical style, presence of inline quotes, data tables, bullet points). The bracketed continuation note should mention the article style.
   - **Output specifications must match OUTPUT SCHEMA exactly.** Every field, constraint, and format rule in the schema should be exercised in at least one example.
   - **Vary article styles across examples.** If the input schema defines multiple article styles (wire-service, analytical, regional), the few-shot examples should collectively demonstrate all of them.

3. **Run 3-expert review (MANDATORY — do not skip).** Launch **3 parallel subagents** per [experts/review-protocol.md](experts/review-protocol.md):

   | Expert | Lens | Catches |
   |--------|------|---------|
   | **1. Priya (Data Quality Lead)** | Does the ruleset match production reality? | Content lengths too short, bundled vs individual files, vague constraints, missing content texture |
   | **2. James (Solutions Architect)** | Does the ruleset contradict itself? | Examples not matching schema, derivation producing invalid output, composition numbers not adding up |
   | **3. Tomoko (Generation Engineer)** | Will this produce diverse data on first pass? | Not enough variation axes, unnamed slots, monotonous examples, missing anti-patterns |

   Each expert scores 5 dimensions (0-10). **Pass: avg >= 7.0, no dim < 5.0.**

   **Protocol:**
   - All 3 PASS → proceed to save
   - 1-2 FAIL → apply fixes, re-run failed experts only (max 3 iterations total)
   - 3 iterations exhausted → present to user with remaining issues listed
   - Append review metadata YAML to bottom of ruleset

   **Each subagent receives a dedicated persona file** that defines their identity, mental model, framework, and output format. The subagent MUST read the persona file FIRST, then the ruleset.

   | Subagent | Persona file | Also receives |
   |----------|-------------|---------------|
   | Expert 1 | `experts/expert-1-production-realism.md` | Ruleset + source docs (production samples, agent specs, corporate profiles) |
   | Expert 2 | `experts/expert-2-internal-consistency.md` | Ruleset only (checks internal consistency, no external sources needed) |
   | Expert 3 | `experts/expert-3-generative-readiness.md` | Ruleset + index.json of generated samples (if any exist) |

   **Subagent prompt template:** "Read the persona file at [path] FIRST — it defines your identity, mental model, and scoring framework. Adopt this persona. Then read the ruleset at [path]. Follow the framework exactly, score all 5 dimensions, and return your review in the specified output format."

   **Why mandatory:** A flawed ruleset multiplies errors across every sample. Catching "article lengths too short" here costs 1 fix; catching it after generating 35 samples costs 35 regenerations.

4. **Scoring formulas must be airtight** (when applicable):
   - Explicit bounds (`min(10, ...)`)
   - Unambiguous operators
   - Edge case behavior defined
   - Final validation checklist

5. **Save the ruleset** to the resolved output path: `[datasets-root]/[client]/[use-case]/rulesets/[domain].html`

6. **HALT** — Present the file path and ask the user to open it in their browser. Do NOT proceed until user responds. If feedback, update and re-present.

7. **After approval** — Conversationally mention what was used vs defaulted, suggest next step (`/create-data`).

---

## Example Conversation Flows

### Full Step-by-Step (Booth CV Screening)

**User:** "Booth, CV screening"
**Assistant:** *[Searches — finds agent spec, sample CVs, BUILD_TRACKER]*

**Step 1:** Agent Task ASCII box → User: "yes"
**Step 2:** Input entities (CV + JD) with Content fields + Content Texture → User: "yes"
**Step 3:** Output structure + derivation → User: "love it"
**Step 4:** Test Scenarios with What/Why/Varies cards → User: "great"
→ *[Generates ruleset.html, runs expert review, presents for approval]*

### Quick Override

**User:** "insurance claims triage agent — generate now"
*[No existing data found]*
**Assistant:** "No existing data. Two things I can't assume: (1) Insurance type? (2) Triage only or approval too?"
*[After answer, collapses Steps 1-4 into one confirmation, generates with smart defaults]*

### Existing Data + Feedback

**User:** "customer support classification"
*[Finds existing ruleset + 152 examples + feedback file]*
**Assistant:** "Found ruleset + 152 examples. Previous generation feedback suggests 3 ambiguous rules. Is this a replacement or update?"
*[Pre-applies feedback, proceeds through Steps 1-4 with pre-populated values]*
