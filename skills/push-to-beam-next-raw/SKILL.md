---
name: push-to-beam-next-raw
version: '1.0'
description: 'Push a filtered copy of this repo to beam-next-raw (no projects, memory,
  apps, workspace). Triggers: ''push to beam next raw'', ''release beam next raw'', ''sync
  beam-next-raw'', ''publish upstream''.'
category: system
tags:
- release
- upstream
- beam-next-raw
updated: '2026-02-27'
visibility: public
---
# Push to Beam Next Raw

Publish the **system-only** view of this instance to the upstream [beam-next-raw](https://github.com/Beam-GTM/beam-next-raw) repository. Keeps full commit history but only these paths: `00-system/`, root config files (e.g. `CLAUDE.md`, `README.md`, `pyproject.toml`, `justfile`, `.gitattributes`, `.gitignore`). Excludes all user content: projects, memory, apps, workspace, custom skills, IDE settings.

Use this when you maintain beam-next-raw from this repo (e.g. nexus-jbd) and want to push a new release after bumping version and updating CHANGELOG.

## Versioning and releases

We use **semantic versioning** `MAJOR.MINOR.PATCH` (e.g. `2.5.2`).

| Bump | When to use | Examples |
|------|-------------|----------|
| **PATCH** (2.5.2 → 2.5.3) | Bug fixes, small docs/UX tweaks, backward-compatible tweaks that don’t change existing behavior. | Fix trigger menu drop, clarify README, typo in skill description. |
| **MINOR** (2.5 → 2.6) | New features, new skills, new config options, or behavioral changes that are additive. Anything that adds capability without breaking existing setups. | New TRIGGERS section, new `skill_directories` config, new system skill, new loader behavior. |
| **MAJOR** (2 → 3) | Breaking changes: removed APIs, changed required config, folder layout changes, or changes that require user action to keep working. | Rename/remove core paths, change required fields in user-config, drop deprecated features. |

**Release checklist before pushing:**

1. Bump **`00-system/VERSION`** to the new version (e.g. `2.5.3` or `2.6.0`).
2. Add a **`00-system/CHANGELOG.md`** entry at the top with the new version, date, and a short bullet list of changes.
3. Run the push script with the same tag:  
   `python3 00-system/skills/system/push-to-beam-next-raw/scripts/push_to_beam_next_raw.py --tag v2.5.3`
4. The script **creates the GitHub Release** for the tag automatically, using the matching section from `00-system/CHANGELOG.md` as the release notes. If the release already exists, it updates the notes.

## What Gets Pushed

| Included | Description |
|----------|-------------|
| `00-system/` | Core framework, skills, triggers, docs |
| `CLAUDE.md`, `GEMINI.md`, `README.md`, `RELEASE_NOTES.md` | Entry points and docs |
| `justfile`, `pyproject.toml` | Tooling |
| `.gitattributes`, `.gitignore` | Git config |

## What Is Never Pushed

| Excluded | Description |
|----------|-------------|
| `01-skills/` | Custom skills |
| `02-memory/` | Goals, config, learnings |
| `03-projects/` | Projects |
| `04-apps/` | Electron/web apps (Beam Prism etc.) |
| `04-workspace/` | Workspace content |
| `apps/` | Legacy apps |
| `.claude/`, `.cursor/`, `.github/`, `.sync-backup/`, `99-helper/` | IDE settings, CI workflows, backups |

## Script

| Script | Purpose |
|--------|---------|
| `scripts/push_to_beam_next_raw.py` | Clone, filter history, push to upstream (and optionally tag) |

## Workflow

### Push current branch to beam-next-raw

From the **repository root** (e.g. nexus-jbd):

```bash
# Preview only
python3 00-system/skills/system/push-to-beam-next-raw/scripts/push_to_beam_next_raw.py --dry-run

# Push filtered main to upstream
python3 00-system/skills/system/push-to-beam-next-raw/scripts/push_to_beam_next_raw.py
```

### Push and tag a release

After bumping `00-system/VERSION` and updating `00-system/CHANGELOG.md` (see **Versioning and releases** above for patch vs minor vs major):

```bash
python3 00-system/skills/system/push-to-beam-next-raw/scripts/push_to_beam_next_raw.py --tag v2.5.3
```

This pushes the filtered branch, creates/force-pushes the tag, and **creates or updates the GitHub Release** with notes taken from the matching `## vX.Y.Z` section in `00-system/CHANGELOG.md`.

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` | — | Print what would be done; do not clone or push |
| `--repo PATH` | git root | Path to repo root (default: current dir or git root) |
| `--branch NAME` | `main` | Branch to filter and push |
| `--remote-name NAME` | `upstream` | Remote name to add or use |
| `--remote-url URL` | Beam-GTM/beam-next-raw | Remote URL (default: https://github.com/Beam-GTM/beam-next-raw.git) |
| `--tag TAG` | — | Create/update tag at filtered tip and force-push to remote |

## How It Works

0. **Commits and pushes to origin/main** — stages all changes, commits (if any), and pushes to `origin/main` so the clone used for filtering is fully up to date.
1. Resolves repo root (current dir or `--repo`; must be a git repo).
2. Clones the repo with `--no-hardlinks` into a temporary directory.
3. Runs `git filter-branch` to remove the excluded paths from **all** history and prunes empty commits.
4. Adds the remote (if not present) and force-pushes the filtered branch.
5. If `--tag` is set, tags the filtered tip and force-pushes the tag.
6. If `--tag` is set, creates (or updates) the **GitHub Release** for that tag with notes from the matching version section in `00-system/CHANGELOG.md`.
7. Removes the temporary clone.

Because history is rewritten, commit hashes on beam-next-raw will not match this repo. Each run re-filters from the current repo state.

## Requirements

- Git
- Push access to the remote (e.g. GitHub token or SSH)
- Run from repo root or set `--repo`

## AI Instructions

When the user asks to push to beam-next-raw, release to beam-next-raw, or sync upstream:

1. **Dry-run first**: Run `push_to_beam_next_raw.py --dry-run` from repo root to confirm paths and remote.
2. **Choosing a version**: If releasing, use the **Versioning and releases** section: patch (2.5.x) for fixes/small tweaks, minor (2.6.0) for new features/capabilities, major (3.0.0) for breaking changes. Ensure `00-system/VERSION` and a CHANGELOG entry are updated first.
3. **Push**: Run `push_to_beam_next_raw.py` (and `--tag vX.Y.Z` if releasing a version).
4. With `--tag`, the script creates/updates the GitHub Release and fills notes from CHANGELOG automatically.
