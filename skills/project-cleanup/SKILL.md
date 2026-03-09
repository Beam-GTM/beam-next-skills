---
name: project-cleanup
version: '2.0'
description: 'Audit and fix Beam Next project references after archiving. Also: archive completed docs within a project. Triggers: ''project cleanup'', ''fix project links'', ''audit projects'', ''update archive references'', ''check project refs'', ''docs cleanup'', ''clean up docs'', ''archive done docs''.'
category: system
tags:
  - projects
  - archive
  - cleanup
  - references
  - docs
updated: '2026-03-05'
visibility: public
---
# Project Cleanup

Two modes: **project-level** archival (move completed projects to archive/) and **docs-level** archival (move completed docs within a project's `docs/` to `docs/archive/`).

---

## Mode 1: Project Reference Cleanup (original)

After moving a project into an `archive/` subfolder under your **projects root**, other files may still reference the old path. This skill finds those references and optionally updates them so links and paths stay correct.

**Projects root**: The folder that contains project folders (and optionally `archive/`). In this repo it is often `03-projects/Beam-Next/`, but the location can vary (e.g. another workspace or folder). Only the structure is fixed: `<projects-root>/<id>/` for active projects, `<projects-root>/archive/<id>/` for archived.

### What It Does

1. **Discover** — Lists all projects under the projects root (top-level and `archive/`), reads status from each project (overview/planning file location varies by project).
2. **Check** — Scans markdown, YAML, and key docs for references to project paths; reports references that point to the wrong location (e.g. missing `archive/` for archived projects).
3. **Fix** — Optionally replaces outdated paths with the correct path (adds or removes `archive/` as needed).

### Usage

**Check only (report outdated references):**
```
Say: "project cleanup" or "audit project references"
```
```bash
python3 00-system/skills/system/project-cleanup/scripts/run_cleanup.py --base-path . --check
```

**Check and fix (update references in place):**
```
Say: "fix project links" or "update archive references"
```
```bash
python3 00-system/skills/system/project-cleanup/scripts/run_cleanup.py --base-path . --fix
```

**List project locations and status:**
```bash
python3 00-system/skills/system/project-cleanup/scripts/run_cleanup.py --base-path . --list
```

### Workflow: When You Archive a Project

1. **Move** the project folder: `<projects-root>/<id>/` → `<projects-root>/archive/<id>/` (projects root may be e.g. `03-projects/Beam-Next/` or elsewhere).
2. **In the project's overview or main planning file** (subfolders and filenames vary by project — locate the file that has `status` and `project_path` in frontmatter):
   - Set `status: ARCHIVED` and `archived: YYYY-MM-DD`
   - Set `project_path` to the new path (e.g. `<projects-root>/archive/<id>/`)
   - Add a one-line archive banner linking to any remaining-work/backlog doc (e.g. in a sibling project or app docs)
3. **Fix relative links inside the archived project**: any link from that project to something outside it (sibling project, app docs, etc.) gains one extra `../` because the project is now one level deeper under `archive/`. Exact paths depend on the project's own subfolder layout and where the repo keeps those siblings.
4. **If there is "remaining work" or "consider later"**: create a short doc wherever the repo tracks follow-up work (e.g. a "prism" or "app" project folder) and add a pointer in app docs (e.g. README) so it's discoverable; exact paths depend on the repo.
5. Run **project cleanup** with `--check` to see which files outside the project still reference the old path; run with `--fix` to update them (or edit manually).

### Script Options (run_cleanup.py)

| Option | Description |
|--------|-------------|
| `--check` | Report only: list outdated references, no edits |
| `--fix` | Update references in place (adds `archive/` or removes it as needed) |
| `--list` | List all projects and their location (active vs archive) and status |
| `--base-path` | Beam Next repo root (default: current directory) |
| `--dry-run` | With `--fix`, print what would be changed without writing |

### What Gets Scanned

- **Dirs**: The script or run determines which dirs to scan (often the projects root, app docs, and system docs; exact paths depend on the repo). In this repo: e.g. `03-projects/Beam-Next/`, `04-apps/beam-prism-electron/docs/`, `00-system/documentation/`.
- **Extensions**: `.md`, `.yaml`, `.yml`
- **Excluded**: Cache dirs, `node_modules/`, `.git/`, and optionally the `archive/` folder when searching for "wrong" refs (so we don't change content inside archived projects unless needed)

---

## Mode 2: Docs Cleanup (archive completed docs)

Scans a project's `docs/` directory for `.md` files that appear "done" based on content signals, then archives them.

### What It Does

1. **Scan** — Reads the first ~80 lines of each `.md` file in `docs/` root for completion signals ("Status: DONE", "ALL COMPLETE", "SHIPPED", "None are V1 blockers", etc.)
2. **Report** — Shows which files are done, active, mixed, or already bannered
3. **Archive** — Moves done files to `docs/archive/`, adds `> **Status**: DONE — archived` banner
4. **Fix redirects** — Updates redirect/stub files (e.g. in `02-resources/`) that pointed to the old path
5. **README update** — Reminds the AI to update `docs/README.md` index (move rows from active → archive table)

### Usage

**Scan and report (no changes):**
```
Say: "docs cleanup" or "clean up docs" or "archive done docs"
```
```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path 04-apps/beam-prism-electron/docs
```

**Scan and archive:**
```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path 04-apps/beam-prism-electron/docs --archive
```

**Dry run (preview):**
```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path 04-apps/beam-prism-electron/docs --archive --dry-run
```

**Fix redirect files after archiving:**
```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path 04-apps/beam-prism-electron/docs --fix-redirects
```

**JSON output (for AI consumption):**
```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path 04-apps/beam-prism-electron/docs --json
```

### Script Options (docs_cleanup.py)

| Option | Description |
|--------|-------------|
| `--docs-path` | Path to the docs directory (required) |
| `--base-path` | Repo root (default: current directory) |
| `--archive` | Move done files to `docs/archive/` + add DONE banner |
| `--fix-redirects` | Fix redirect files in `02-resources/` pointing to moved docs |
| `--dry-run` | With `--archive`, show what would happen without making changes |
| `--date` | Date for DONE banner (default: today) |
| `--json` | Output as JSON for AI consumption |

### Completion Signal Detection

The script scans for these patterns in the first 80 lines:

**Done signals** (any match → candidate for archival):
- `Status: DONE` / `**Status**: DONE`
- `ALL PHASES COMPLETE` / `ALL COMPLETE`
- `Phases N-M DONE/COMPLETE`
- `SHIPPED`
- `V1 + V2 DONE`
- `None are V1 blockers`

**Active signals** (override done signals):
- `In Progress` / `Status: Active`
- `Next Steps:`
- `Phase X in progress`

**Protected files** (never archived):
- `README.md`, `plan.md`, `backlog.md`

### Workflow: When You Archive Docs

1. **Run scan**: `docs_cleanup.py --docs-path <path>` to see what's done
2. **Review** the "DONE" and "MIXED" lists — confirm with user if uncertain
3. **Archive**: `docs_cleanup.py --docs-path <path> --archive` (or `--dry-run` first)
4. **Fix redirects**: `docs_cleanup.py --docs-path <path> --fix-redirects`
5. **Update README.md**: Move archived file rows from Active/Specs/Bug/Cross-Project tables to the Archive table. Update links to use `archive/` prefix. This step is manual (AI-assisted) because table structure varies.
6. **Verify**: Check that no broken links remain in README.md

---

## AI Instructions

When the user asks to clean up projects, audit references, fix project links, or clean up docs:

### For project reference cleanup:
1. Run `run_cleanup.py --check` from repo root and show the report.
2. If references are found: explain what's wrong and offer to run `--fix` (or `--fix --dry-run` first).
3. If the user confirms, run `--fix` and then run `--check` again to confirm no outdated refs remain.
4. If the user only wants to see project locations and status, run `--list`.
5. When **archiving** a project (not just fixing refs), follow the "When You Archive a Project" workflow above, including relative-link fixes inside the project and creating a 07 doc + README line when there is remaining work.

### For docs cleanup:
1. Run `docs_cleanup.py --docs-path <path>` to scan and report.
2. Show the user the DONE files and ask for confirmation.
3. If confirmed, run with `--archive` (optionally `--dry-run` first).
4. Run with `--fix-redirects` to update any redirect/stub files.
5. **Manually update `docs/README.md`** — move archived rows from active tables to archive table. This is the most important step and requires understanding the README structure.
6. Run `--fix-redirects` again to catch any remaining stale paths.

### Combined workflow:
If both projects AND docs need cleanup, run project-level first, then docs-level. Project archival may create new docs that need archival themselves.

---

## Learnings from practice (archive sessions)

- **Relative links inside archived projects**: After moving into `archive/`, every link from that project to something outside it (sibling project, app docs, etc.) needs one more `../` because the project is one level deeper. Subfolder layout and repo structure vary; adjust the number of `../` accordingly. The script may not edit inside archived projects; do this manually or extend the script.
- **Remaining-work pattern**: When archiving a project that has unfinished or "consider later" work, create a short doc in whatever place tracks follow-up work (e.g. a "beam-prism" or "app" project folder) and add a pointer in app docs (e.g. README) so it's discoverable later. Exact paths depend on the repo.
- **Overview frontmatter**: In whatever file holds the project's status and path, set `project_path` to the new path and add a short banner with the link to the remaining-work doc; this keeps the archived project self-describing.
- **README.md index is king**: After docs archival, the README update is the most critical step. A file in archive/ without a README row is invisible. A README row pointing to a deleted file is a broken link.
- **Cross-project backlogs**: Files like `memory-layer-remaining-work.md` that track deferred work from other projects — archive these when all items are confirmed post-V1 deferred, not when the parent project is archived.
- **Redirect files**: When a canonical doc moves to `archive/`, any thin redirect files in `02-resources/` must be updated too. The `--fix-redirects` flag handles this.
