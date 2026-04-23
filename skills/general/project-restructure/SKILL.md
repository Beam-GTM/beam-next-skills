---
type: skill
author: Jonas Diezun
name: project-restructure
version: '1.0'
description: 'Advisory-first project structure pass. Recommends and optionally applies folder taxonomy improvements, subfolder grouping, and subproject boundaries after cleanup. Triggers: ''project restructure'', ''restructure project'', ''organize project structure'', ''improve folder structure'', ''structure pass''.'
category: system
tags:
  - projects
  - structure
  - taxonomy
  - organization
  - refactor
updated: '2026-03-08'
visibility: public
---
# Project Restructure

Purpose: Improve project structure after hygiene cleanup by proposing clearer folder taxonomy, ownership boundaries, and optional file moves.

This skill is separate from `project-cleanup` by design:

- `project-cleanup` = archive/reference hygiene
- `project-restructure` = architecture and layout decisions

---

## Scope

### What this skill does

- Audits current structure (planning/resources/working/outputs/docs/app folders)
- Proposes target layout and naming conventions
- Suggests subfolder boundaries for large flat directories
- Suggests subproject splits when one project contains multiple independent streams
- Produces an explicit move plan before making any file changes

### What this skill does not do

- Archive done docs by confidence scoring (use `project-cleanup`)
- Change content semantics unless needed for link integrity
- Force a migration without user confirmation

---

## Default Mode: Advisory First

Always start with a **dry proposal**:

1. Map the current structure
2. Identify pain points:
  - large flat folders
  - mixed concerns (strategy + execution + output in one place)
  - repeated naming patterns without grouping
  - duplicate or ambiguous ownership
3. Propose 1 recommended taxonomy plus up to 2 alternatives
4. Show move impact:
  - files/folders to move
  - likely link updates needed
  - risks and rollback notes
5. Ask for confirmation before any writes

---

## Suggested Taxonomy (Default)

Use this as a baseline when no better local convention exists:

- `01-planning/` — goals, overview, roadmap, decisions
- `02-resources/` — references, research, source material
- `03-working/` — active drafts, scripts, temporary WIP
- `04-outputs/` — finalized or distributed deliverables
- `archive/` — historical and superseded artifacts

Within large folders, prefer thematic subfolders:

- `transcripts/`, `research/`, `specs/`, `status/`, `handoffs/`, `assets/`

---

## Execution Workflow

### Step 1: Baseline scan

- Enumerate key folders and file volume by directory
- Detect oversized directories and mixed-content hotspots

### Step 2: Boundary design

- Propose clear folder boundaries
- Flag candidates for separate subprojects when:
  - workstreams have separate goals and timelines
  - ownership differs across teams
  - dependencies are weak and coupling is low

### Step 3: Migration plan

- Produce a concrete move table:
  - source path
  - destination path
  - reason
  - link-update needs

### Step 4: Confirm + apply (optional)

- Only apply after explicit user approval
- Move files in small batches
- Fix references and indexes after each batch

### Step 5: Verify

- Re-scan for broken links
- Check key index files (README, planning overviews)
- Report before/after structure

### Step 6: Reconcile references (with project-cleanup)

Path moves can leave stale links that point at old locations. Reuse **project-cleanup** Mode 1: discover and fix broken refs project-wide, same as after archiving a project. Paths below assume the **project-cleanup** skill is co-installed as a sibling of this skill (see `../project-cleanup/`). In Nexus, the same files live at `00-system/skills/system/project-cleanup/scripts/` from the repo root.

```bash
# Discover broken refs
python3 ../project-cleanup/scripts/run_cleanup.py --base-path . --check

# Fix (after user approval, if issues exist)
python3 ../project-cleanup/scripts/run_cleanup.py --base-path . --fix
```

If the user already has a different link-check or cleanup routine for the repo, use that instead, but the goal is the same: no dangling paths after a restructure.

---

## AI Instructions

- Prefer minimal-disruption moves that improve discoverability.
- Keep canonical docs in their source-of-truth locations.
- Do not introduce deep nesting unless it solves a real retrieval problem.
- If uncertainty is high, present options and ask before applying.
- **Order:** run `project-cleanup` first (hygiene, archive, compress as needed), then restructure. After applying moves, run **Mode 1** ref check/fix (Step 6) or the project’s equivalent so links match the new layout.

---

## Trigger Phrases

Load this skill when user says:

- "project restructure"
- "restructure project"
- "organize project structure"
- "improve folder structure"
- "structure pass"
- "split into subprojects"