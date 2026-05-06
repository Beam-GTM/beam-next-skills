---
type: skill
author: Jonas Diezun
name: project-cleanup
version: '4.0'
description: 'Project and docs cleanup with confidence-based decisions. Three modes: archive done docs, fix broken project references, and compress docs (merge related files, distill verbose content to rules-only, rename for clarity). Triggers: ''project cleanup'', ''docs cleanup'', ''clean up docs'', ''archive done docs'', ''fix project links'', ''audit projects'', ''compress docs'', ''merge docs''.'
category: system
tags:
  - projects
  - archive
  - cleanup
  - references
  - docs
updated: '2026-03-31'
visibility: public
---
# Project Cleanup v4

**Script paths:** Commands below use `scripts/...` relative to this skill’s root (the folder that contains this `SKILL.md`). In a full Nexus checkout, the same scripts also live under `00-system/skills/system/project-cleanup/scripts/` from the repo root.

Three modes:
- **Mode 1**: Project-level archival — move completed projects to `archive/`, fix references.
- **Mode 2**: Docs-level cleanup — archive done/superseded docs within a project using confidence scoring.
- **Mode 3**: Compress — merge related docs, distill verbose content to rules-only, rename files for clarity. More aggressive than archival; changes what lives in the active set, not just what gets removed.

---

## Decision Framework

The script (`docs_cleanup.py`) scores each file into confidence tiers. The AI uses these scores plus its own reading to decide what to do.

### Confidence Tiers

| Tier | Script detects | AI action |
|------|---------------|-----------|
| **HIGH** | Explicit "Status: DONE", "Superseded by X", all checkboxes done, DONE banner | **Auto-archive.** No user confirmation needed. Move to `archive/`, add DONE banner, fix references. |
| **MEDIUM** | Completion hints ("implemented in session X", "no remaining work"), no open TODOs | **Read file, then archive or keep.** Skim 50 lines. If content confirms done → archive. If ambiguous → downgrade to LOW. |
| **LOW** | Mixed signals (done + active), open TODOs/TBDs, unclear status | **Read file, propose to user.** Present finding with reasoning. Wait for confirmation. |
| **UNKNOWN** | No signals detected | **Read file and assess.** Many files lack markers but are clearly done or active from context. Decide based on content. |
| **ACTIVE** | "Status: active/in-progress", "Next Steps" section, "currently working" | **Keep.** Do not propose archival. |
| **PROTECTED** | README.md, plan.md, backlog.md, SKILL.md | **Never archive.** |

### When to archive (rules the AI follows)

Archive when ANY of these are true:
1. **Explicit done marker** — "Status: DONE/COMPLETE/SHIPPED/ARCHIVED" in first 100 lines
2. **Superseded** — "Superseded", "Replaced by", "Old approach" with pointer to replacement
3. **All work complete** — "All phases complete", every checkbox checked (3+ boxes), no open TODOs
4. **Project itself is done** — If the parent project is archived/done, all its docs are done too (unless they're cross-project backlogs for active work)
5. **Historical reference** — Call notes, meeting transcripts, research for a completed phase — if no open action items remain

Keep when ANY of these are true:
1. **Active signals** — "in progress", "next steps", "currently working on"
2. **Open items** — Unchecked checkboxes for work that's still planned
3. **Living doc** — README, plan, backlog, or doc that gets updated regularly
4. **Active project** — The project is being worked on and this doc is referenced from plan/README

### Handling different folder structures

| Folder type | Convention | Cleanup approach |
|-------------|-----------|-----------------|
| `docs/` (in apps) | Has `archive/`, `README.md` index | Move done → `archive/`, update README |
| `01-planning/` | Overview, discovery, plan, steps | Rarely archived — these define the project. Archive only if project itself is done. |
| `02-resources/` | Reference docs, research, specs | Archive superseded/completed specs. Keep active references. Create `archive/` if needed. |
| `03-working/` | Scripts, WIP, scratch files | Clean aggressively. Archive completed work. Delete true scratch files (with user OK). |
| `04-outputs/` | Deliverables, reports | Archive when delivered/final. Keep if iterating. |
| Flat folder | No convention | Suggest creating `archive/` if >5 done files. Otherwise just flag. |

---

## Mode 1: Project Reference Cleanup

After moving a project into `archive/`, fix references elsewhere that still point to the old path.

### Usage

```bash
# Auto-discover project roots and check for broken refs
python3 scripts/run_cleanup.py --base-path . --check

# Fix broken refs
python3 scripts/run_cleanup.py --base-path . --fix

# List all projects and their locations
python3 scripts/run_cleanup.py --base-path . --list
```

### Workflow: Archiving a Project

1. **Move** folder: `<root>/<id>/` → `<root>/archive/<id>/`
2. **Update overview**: Set `status: ARCHIVED`, add archive banner
3. **Fix internal links**: Files inside gain one extra `../` for sibling references
4. **Extract remaining work**: Create pointer doc in active project if there's deferred work
5. **Run** `--check` then `--fix` to update external references

---

## Mode 2: Docs Cleanup

Audit and clean up documentation within any project or app folder.

### Quick start

```bash
# Scan a single docs directory
python3 scripts/docs_cleanup.py \
  --path 04-apps/beam-prism-electron/docs --json

# Scan an entire project (all subdirs)
python3 scripts/docs_cleanup.py \
  --project 03-projects/Beam-Next/13-beam-prism-agents-platform --json

# Scan recursively (includes subdirectories)
python3 scripts/docs_cleanup.py \
  --path 03-projects/Beam-Next/09-ai-venture-studio/02-resources --recursive --json

# Archive HIGH-confidence files automatically
python3 scripts/docs_cleanup.py \
  --path <dir> --archive --dry-run   # preview first
python3 scripts/docs_cleanup.py \
  --path <dir> --archive             # execute

# Fix links to moved files
python3 scripts/docs_cleanup.py \
  --path <dir> --fix-redirects
```

### Workflow: Full docs cleanup

**Step 1 — Triage (script)**

Run the script on each target. It returns confidence-scored results:
```json
{
  "summary": {"HIGH": 3, "MEDIUM": 2, "ACTIVE": 5, "UNKNOWN": 4},
  "results": {
    "HIGH": [{"file": "sentry-fix-plan.md", "action": "archive", "reason": "Explicitly done: Status: DONE"}],
    "MEDIUM": [{"file": "old-research.md", "action": "archive", "reason": "Completion hints: implemented in session 47; no open TODOs"}]
  }
}
```

**Step 2 — AI reads MEDIUM + UNKNOWN files**

For each MEDIUM and UNKNOWN file, read the first 50–100 lines. Classify:
- If content confirms done → upgrade to HIGH, archive
- If content is ambiguous → present to user with reasoning
- If content is active → keep

**Step 3 — Execute**

1. Archive all confirmed-done files (HIGH + upgraded MEDIUM)
2. Add DONE banner to archived files
3. Fix redirects/references
4. Update README.md index (if exists) — move archived file rows to archive table
5. Present LOW/UNKNOWN findings to user for remaining decisions

**Step 4 — Verify**

Run the script again on the same path. Should show 0 HIGH, 0 MEDIUM.

### Multi-project sweep

To clean up across all projects at once:

```bash
# 1. List all projects
python3 scripts/run_cleanup.py --base-path . --list

# 2. For each project, scan and triage
python3 scripts/docs_cleanup.py \
  --project <project-path> --json

# 3. For app docs
python3 scripts/docs_cleanup.py \
  --path 04-apps/<app>/docs --json
```

---

## Script Reference (docs_cleanup.py)

| Option | Description |
|--------|-------------|
| `--path <dir>` | Scan a directory (mutually exclusive with `--project`) |
| `--project <dir>` | Scan full project (01-planning, 02-resources, etc.) |
| `--recursive` | With `--path`: include subdirectories |
| `--json` | Machine-readable output with confidence scores |
| `--archive` | Move HIGH-confidence files to `archive/` |
| `--fix-redirects` | Fix links to docs that moved to `archive/` |
| `--dry-run` | Preview without writing |
| `--base-path` | Workspace root (default: `.`) |
| `--date` | Date for DONE banner (default: today) |

### Signal detection

The script checks for:
- **Done markers**: "Status: DONE/COMPLETE/SHIPPED/ARCHIVED" in headers/frontmatter/banners
- **Superseded markers**: "superseded", "replaced by", "old approach", "deprecated"
- **All-complete markers**: "all phases complete", "phases 1-6 done"
- **Completion hints**: "implemented in", "shipped on", "no remaining work"
- **Active markers**: "status: active/in-progress", "Next Steps" sections, "currently working"
- **Checkbox ratios**: checked vs unchecked `- [x]` / `- [ ]`
- **TODO/TBD counts**: open action items
- **Redirect detection**: short files with "canonical location" / "see instead"

---

## AI Instructions

### For docs cleanup:
1. **Run the script** with `--json` to get confidence-scored triage
2. **AUTO-ARCHIVE HIGH confidence** — these have explicit done markers, no ambiguity
3. **READ MEDIUM files** — skim 50 lines, upgrade to archive or keep
4. **READ UNKNOWN files** — no signals means the AI must decide from content
5. **PRESENT LOW files** — mixed signals need user input
6. **Leave ACTIVE and PROTECTED alone**
7. **After archiving**: fix redirects, update README index, verify with re-scan

### For project reference cleanup:
1. Run `run_cleanup.py --check` and show report
2. If broken refs found → explain and offer `--fix`
3. After fixing → re-run `--check` to verify

### For multi-project sweep:
1. List all projects with `--list`
2. For each project: run `--project <path> --json`
3. Process findings per the confidence framework above
4. Group all findings into a single summary table for the user
5. Execute approved changes project by project

### Critical rules:
- **HIGH confidence = act.** Don't ask. Archive, banner, fix refs.
- **MEDIUM = read then act.** Quick skim to confirm. If confirmed → archive. If not → ask.
- **LOW/UNKNOWN = read then propose.** Present reasoning. Wait for user.
- **Always fix references** after moving files.
- **Always update README** index if one exists.
- **Never archive protected files** (README.md, plan.md, backlog.md).
- **Adapt to structure** — not every project has `archive/`. Create it when needed. Some projects use different conventions.

---

## Mode 3: Compress

Reduce file count and total content weight in a docs directory by merging related files, distilling verbose content to rules-only, and renaming for clarity. Use after Mode 2 archival, or independently when the active set is too large to be useful.

### When to compress

Apply Mode 3 when a docs directory has:
- Multiple short files (< 100 lines each) that cover the same system or audience
- Files with long investigation/narrative sections where only the conclusions matter
- Files named with verbose, dated, or unclear names
- A README that is hard to navigate because too many files exist

### The three compression actions

#### 1. Merge

Merge two or more files into one when they share the **same audience** (always read together), cover **complementary not duplicated** content (rules vs. inventory, or two subsystems of one domain), and the combined result stays under ~300 lines.

**Merge candidates to look for:**
- A "rules" file + an "inventory/reference" file for the same system
- Two files covering different parts of the same feature (e.g., `copilot-tool-ui.md` + `copilot-message-history.md` → `copilot-engineering.md`)
- Files that are short enough individually that splitting creates more navigation overhead than value

**How to merge:**
1. Identify the natural section structure of the combined doc
2. Write it fresh — do not concatenate. Each source becomes a `##` section.
3. Keep: rules, patterns, anti-patterns, code examples (one per rule), quick-ref tables
4. Cut from the merge: content already in `CLAUDE.md`/`README.md`/a rule file; verbose explanations that restate what the code shows; history/changelog tails
5. Delete the source files after the merged file is written
6. Update all index files (README, ROADMAP, etc.)

#### 2. Distill

Rewrite a single file to remove content weight without changing its purpose. Target: 40–60% of original length.

**Distill candidates:**
- Investigation logs ("What Was Tried" sections, session-by-session narratives) → replace with a "Gotchas" section of 3–7 named rules
- Historical checklists where all items are ticked Done → remove the checklist, keep only the rule it produced
- Long code examples that just illustrate a prose rule → one concise example max
- "History / Changelog" sections at the bottom → cut entirely (that's what git is for)
- Verbose prose explanations of patterns that are enforced by a linter or already in `CLAUDE.md`

**How to distill:**
1. Read the full file and identify the "keep kernel" — the 20% of content that an AI or engineer would actually use when coding
2. Rewrite, not trim: produce a clean short version, not the original with lines deleted
3. Structure: summary line → rules/gotchas → code example (if needed) → key files table

#### 3. Rename

Rename a file when the current name is verbose, has a stale date, or uses a suffix that adds no information.

**Rename candidates:**
- Date-stamped names (`architecture-review-2026-03-16.md`) — the date belongs in the content, not the filename
- `-learnings` / `-guide` / `-plan` suffixes when the content is reference material, not a plan
- Multi-word names where the core noun is sufficient (`board-room-expert-panel-architecture.md` → `board-room.md`)
- Names with 4+ hyphenated tokens when 1–2 would be unambiguous in context

After renaming: fix all references (README index, ROADMAP, internal doc links) with a grep sweep.

---

### Mode 3 Workflow

**Step 1 — Survey**

List all files in the target directory with line counts:
```bash
wc -l docs/reference/*.md | sort -n
```
Note: total lines, number of files, and any obvious pairs/groups.

**Step 2 — Categorize each file**

For each file, assign it to one or more buckets:
- `ARCHIVE` — done/historical (use Mode 2 decision framework)
- `MERGE` — belongs with another file
- `DISTILL` — has narrative/investigation weight to shed
- `RENAME` — name is verbose or stale
- `KEEP` — clean, correctly named, right size

**Step 3 — Propose to user**

Present a table:

| File | Action | Rationale |
|------|--------|-----------|
| `copilot-tool-ui.md` | Merge → `copilot-engineering.md` | Same audience as `copilot-message-history.md`; 67 + 85 lines = 152 combined |
| `streaming-smoothness-learnings.md` | Merge + distill | Investigation log; 5 gotchas are the real value; merge into `copilot-engineering.md` |
| `board-room-expert-panel-architecture.md` | Rename → `board-room.md` | 4-token verbose name |
| `design-rulebook.md` | Merge → `design-system.md` | Pairs naturally with `design-guide-building-blocks.md` |

Show the target file count: Before → After.

**Step 4 — Execute (after user approval)**

For each merge group (in order, largest first):
1. Read all source files fully
2. Write the merged + distilled file (new name, clean structure)
3. Delete source files
4. Fix all references to source files

For renames:
1. `mv old-name.md new-name.md`
2. Grep for references to old name and fix them

**Step 5 — Update indexes**

Rewrite the README index (or equivalent) to reflect the final file set with one-line descriptions.

**Step 6 — Verify**

```bash
ls -la docs/reference/ | wc -l   # file count
wc -l docs/reference/*.md | tail -1  # total lines
```
Report: Before (N files, X total lines) → After (M files, Y total lines).

---

### Mode 3 AI Instructions

- **Never concatenate — always rewrite.** A merged file written fresh is a better artifact than two files stapled together.
- **Distill to rules, not history.** The value of a learnings doc is the gotchas, not the story of how they were discovered.
- **One code example per rule** is enough. Two is often one too many.
- **Short names win.** If the reader knows the domain, `board-room.md` needs no further qualification.
- **Fix every reference** after renaming or merging — a broken link in a README destroys the value of the cleanup.
- **Update the index** (README/ROADMAP) as the last step of every compression run.
- **Present before executing** — Mode 3 changes content, not just file locations. Always show the proposed action table and get user approval before writing.

---

## Coordination with project-restructure

After a cleanup run (any mode), **optionally** suggest the `project-restructure` skill if you surfaced structural pain that hygiene alone will not fix:

- Very large or flat directories with no grouping
- Mixed concerns in one folder (e.g. strategy, execution, and final outputs together)
- Repeated naming without thematic subfolders, or ownership boundaries that are unclear
- Multiple workstreams in one project that look like separate goals or weakly coupled deliverables

This is a **suggestion, not a requirement**: many cleanups are done without layout changes. When the user only asked for cleanup, mention restructure in closing **only** when the scan clearly showed one or more of the above.

`project-restructure` expects hygiene first (this skill), then design/moves. If the user later runs restructure, they should **not** skip prior cleanup of done docs and dead ends.

---

## Learnings

- **Regex is not intelligence**: A script flagging "Status: DONE" in link text is a false positive. The confidence scoring helps, but AI must verify MEDIUM/UNKNOWN.
- **Structure varies wildly**: Beam Prism has `docs/archive/` + README index. Other projects have flat folders. Adapt.
- **Relative links break on move**: `archive/` adds one `../` level. Check and fix.
- **README index is king**: A file in `archive/` without a README row is invisible. Always update the index.
- **"Done" is contextual**: A testing doc with "Phase 1 open" might be archive-worthy if Phase 1 is deprioritized. AI reads the project state to decide.
- **Superseded is the strongest signal**: A doc that says "superseded by X" is always archivable, regardless of other content.
- **Cross-project backlogs**: Archive only when all items are confirmed deferred or done, not when the parent project is archived.
