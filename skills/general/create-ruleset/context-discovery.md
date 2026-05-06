# Context Discovery

Discovery logic for the `create-ruleset` skill. Runs as a subagent to keep main skill context clean.

## Purpose

Given a client/project name, automatically discover and load all relevant context so the user can jump straight into ruleset creation without manually supplying file paths.

---

## Discovery Procedure

### Step 1: Accept Client/Project Name

Extract the client or project name from the user's input. This could be:
- Explicit: "Coolback", "Betterment", "Booth", "BID Coburg"
- Implied from the ruleset domain or file path
- Asked for if not provided

### Step 2: Spawn Discovery Subagent

Launch an **Explore subagent** with the following task. The subagent must search — never hardcode paths.

```
Subagent prompt:
Discover all context files relevant to the client/project "{CLIENT_NAME}" across the workspace.

Discovery strategy (discover paths, don't assume them):

1. Find the client's project/account folder:
   - Glob for directories named after the client (case-insensitive) anywhere in the workspace
   - Look for project artifacts inside: overview docs, PROJECT.md, strategy docs, proposals, workstream folders
   - IMPORTANT: Some clients are nested under parent accounts (e.g., a subsidiary under a parent company's folder). Search recursively, not just top-level matches.

2. Find the client's dataset directory:
   - Search for directories containing `rulesets/`, `seed/`, or `augmented/` subdirectories scoped to the client name
   - Also check for a workspace-level datasets directory (common names: `dataset/`, `datasets/`, `data/`, `training-data/`) and look for a client subfolder within it

3. Broad content search:
   - Grep the entire workspace for the client name (case-insensitive) to catch mentions in multi-client docs, transcripts, meeting notes, and other accounts
   - Search for known aliases (e.g., "Booth" = "Booth & Partners", "BID" = "BID Coburg")
   - Look for customer notes, workspace folders, and partnership docs mentioning the client

4. Sibling repos:
   - Check sibling directories under the same parent for related repos containing dataset/, test-cases/, or skill definitions

For each discovered file, determine:
- File path (relative to workspace root)
- File type (markdown, PDF, CSV, JSON, etc.)
- Category: "project_context" or "test_data_sample"
  - project_context: specs, requirements, meeting notes, analysis, agent descriptions, process docs
  - test_data_sample: example inputs/outputs, seed data, generated datasets, test cases, scenario specs
- Brief description (1 line) of what the file contains based on filename and first few lines
- If the file is a multi-client document (like test-cases.md), note which section is relevant

Return results as two sections:
1. PROJECT CONTEXT — files describing the domain, agent, business rules, processes
2. TEST DATA SAMPLES — files containing example data, test cases, seed datasets
```

### Step 3: Present Discovery Summary

After the subagent returns, present the results to the user in two clearly separated sections:

```
## Discovered Context for {CLIENT_NAME}

### Project Context
Summary of what was found — descriptions, specs, requirements, meeting notes, etc.

| File | Description |
|------|-------------|
| path/to/file.md | Brief description |
| ... | ... |

### Test Data Samples
List of example/test data files found.

| File | Description |
|------|-------------|
| path/to/data.json | Brief description |
| ... | ... |
```

If either section is empty, explicitly note it: "No project context files found" or "No test data samples found."

### Step 4: Confirm or Flag Gaps

After presenting the summary, ask the user:

> "Does this cover what you need, or is there anything missing? You can point me to additional files or directories if needed."

The user can:
- **Confirm** — proceed with discovered context
- **Add files** — provide additional file paths to include
- **Remove files** — exclude irrelevant files from the set
- **Skip discovery** — proceed without context (manual mode)

### Step 5: Load Relevant Context

Once confirmed, read the discovered files and make their content available to the calling skill. Only read files that are:
- Markdown (`.md`) — read directly
- JSON (`.json`) — read directly
- CSV (`.csv`) — read directly

For unsupported formats (PDF, XLSX, DOCX, PPTX), use the parsers in `parsers/` directory:
- PDF: `parsers/pdf_parser.py` for text extraction, `parsers/pdf_to_images.py` for visual reading
- CSV: `parsers/csv_reader.py` with column type inference
- PPTX: `parsers/pptx_parser.py` for slide-by-slide extraction

---

## Local Repo Data (Always Available — No Client Name Needed)

The discovery subagent should ALSO report what exists locally in this repo, regardless of client name. This data is always relevant:

### Local scan targets:
Discover these by searching the workspace — don't assume fixed paths:
- **Rulesets**: Find all `*.html` files with `schema_version` frontmatter (list domain names and agent tasks)
- **Seed data**: Find `*.json` files inside directories named `seed/` (list topic names and example counts)
- **Augmented data**: Find directories named `augmented/` containing sample subdirectories (list domain names, sample counts, whether gold standards exist)

### What to report:
For each local resource, include:
- Domain name
- What data types exist (ruleset, seed, augmented, gold standards)
- Sample count where applicable
- One-line summary of the agent task (from ruleset or inferred from data)

This gives the calling skill a **complete map of what's already in the repo** so it can reference existing patterns, reuse structures, and avoid duplicating work — even without a client name.

## Integration Notes

- The discovery step runs **before** the main skill workflow begins
- Discovery results stay in the subagent — only the structured summary and confirmed file contents are passed back
- If the user doesn't provide a client name, the skill should ask for one before running discovery
- Discovery is optional — if the user describes a new domain from scratch, bypass discovery
- **Local repo scanning is NOT optional** — it always runs as part of Phase 0.5, even without discovery
