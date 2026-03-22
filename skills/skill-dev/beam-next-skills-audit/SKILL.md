---
name: beam-next-skills-audit
type: skill
version: '1.0'
description: Audit registry.yaml against disk, validate SKILL.md frontmatter, find duplicates
  and orphans. Load when user says 'audit skills registry', 'validate beam-next-skills',
  'registry drift', 'skills catalog audit', 'check registry yaml'.
category: skill-dev
tags:
- audit
- registry
- maintenance
- beam-next
updated: '2026-03-23'
visibility: public
---
# Beam Next Skills Registry Audit

You are auditing this **beam-next-skills** repository: the canonical index is [`registry.yaml`](https://github.com/beam-ai-team/beam-next-skills/blob/main/registry.yaml) at the repo root; each skill is a folder under `skills/` containing at least `SKILL.md` with YAML frontmatter.

**Goal:** Find drift (registry vs filesystem), bad or missing metadata, duplicates, and content quality issues that hurt discovery in Beam Next / Prism.

---

## Architecture (what you are auditing)

```
beam-next-skills/
├── registry.yaml          # Machine-readable index (skill_count, name, path, version, …)
├── README.md              # Human overview (counts can drift from registry)
├── scripts/
│   └── validate_skill_frontmatter.py   # Phase-1 frontmatter rules
└── skills/
    ├── {category}/
    │   └── {skill-name}/
    │       └── SKILL.md   # Source of truth for description triggers; frontmatter required
```

**Beam Next:** A local workspace may mirror these under `00-system/skills/`; this audit is for **this Git repo** unless another root is given.

---

## Step 0: Resolve repository root

- **Default:** the root of the **beam-next-skills** clone (directory that contains `registry.yaml` and `skills/`).
- Set `SKILLS_ROOT` to that path for all commands below.

Verify:

```bash
test -f "$SKILLS_ROOT/registry.yaml" && test -d "$SKILLS_ROOT/skills" && echo OK
```

---

## Step 1: Gather audit scope

| Scope | What you run |
|-------|----------------|
| **Full** | Everything below (default) |
| **Registry + disk** | Steps 2–4 only (drift, orphans, phantoms) |
| **Frontmatter** | Step 3 script + Step 5 |
| **Quality / consolidation** | Steps 6–7 |

If unspecified, run **full**.

---

## Step 2: Registry internal consistency

From `$SKILLS_ROOT`:

1. **`skill_count` vs actual entries**

   ```bash
   grep -E "^skill_count:" registry.yaml
   grep -c "^- name:" registry.yaml
   ```

   The count of `- name:` lines under `skills:` must match `skill_count`. If not, registry is stale.

2. **Duplicate skill names**

   ```bash
   grep "^- name:" registry.yaml | sed 's/.*name: //' | sort | uniq -d
   ```

   Any output = duplicate names (must fix).

3. **Duplicate paths**

   ```bash
   grep "path: skills/" registry.yaml | sort | uniq -d
   ```

4. **Missing `path` or broken paths**

   For each `path:` in `registry.yaml`, verify the folder exists and contains `SKILL.md`:

   ```bash
   while read -r p; do
     test -f "$SKILLS_ROOT/$p/SKILL.md" || echo "MISSING: $p"
   done < <(grep "path: skills/" registry.yaml | sed 's/.*path: //')
   ```

---

## Step 3: Automated frontmatter validation

```bash
cd "$SKILLS_ROOT" && python3 scripts/validate_skill_frontmatter.py
```

CI-style failure:

```bash
python3 scripts/validate_skill_frontmatter.py --strict
```

**Rules enforced (summary):**

- `SKILL.md` must start with `---` frontmatter.
- Prefer `type: skill` (or `agent` per project conventions).
- `tags`: 2–5 items.
- `category` must be one of the allowed set in the script.

---

## Step 4: Disk vs registry (orphans and phantoms)

1. **Phantom registry entries** — `path` in `registry.yaml` but no `SKILL.md` on disk (Step 2.4).

2. **Orphan skills** — folder with `SKILL.md` under `skills/` but **no** matching `path` in `registry.yaml`.

   ```bash
   find "$SKILLS_ROOT/skills" -name SKILL.md -print | sed "s|$SKILLS_ROOT/||; s|/SKILL.md||" | sort > /tmp/disk-skills.txt
   # Diff against paths extracted from registry.yaml
   ```

   Report: **orphans** (on disk only) and **phantoms** (registry only).

---

## Step 5: Metadata drift (registry vs SKILL.md)

For a **sample** of skills (or all on a full audit), compare:

- `name` in registry vs `name` in frontmatter — must match.
- `version` / `updated` — flag large drift.
- **`visibility`** — must be `public` or `team` in SKILL.md and should match `registry.yaml` (`team` = internal-only, e.g. ROI/costs; `public` = catalog-safe).

**Skills missing `type:` in frontmatter:**

```bash
grep -L "^type:" $(find "$SKILLS_ROOT/skills" -name SKILL.md) 2>/dev/null | head
```

**Align visibility from registry into SKILL.md** (optional bulk fix):

```bash
python3 scripts/sync_visibility_from_registry.py --dry-run
python3 scripts/sync_visibility_from_registry.py
```

---

## Step 6: Description & trigger quality (spot audit)

For each **category** or a random sample of **15–20** skills, open `SKILL.md` and check:

| Check | Pass |
|-------|------|
| **Trigger clarity** | `description` in frontmatter says *when* to load (phrases, user intent). |
| **Not a stub** | Body is not only a title; has workflow or clear instructions. |
| **Connector skills** | `*-connect` skills explain setup + link to `*-master` or product skills when relevant. |
| **Consolidated skills** | Large integrations describe CLI/resources instead of duplicating many endpoints. |

---

## Step 7: Structural anti-patterns

- **Script-only folders** — scripts under `skills/` but no `SKILL.md`.
- **Empty or stub SKILL.md** — placeholder only.
- **Broken relative paths** in docs — old folder names vs current `skills/…` layout.

---

## Step 8: Generate audit report

```markdown
# Beam Next Skills Registry Audit — {date}

## Summary
- Registry path: `{SKILLS_ROOT}`
- `skill_count` in YAML: {n}
- `- name:` entries: {n}  → MATCH / MISMATCH
- Duplicate names: {n}
- validate_skill_frontmatter.py issues: {n}
- Orphan skills (disk, not registry): {n}
- Phantom entries (registry, no SKILL.md): {n}

## Critical issues
{Duplicates, phantoms, skill_count mismatch}

## Warnings
{Frontmatter warnings, missing type, tag/category count}

## Description quality (sample)
| Skill | Trigger clarity | Notes |
|-------|-----------------|-------|
| ... | Good / Needs work / Bad | ... |

## Structural notes
{Script-only, outdated paths, consolidation candidates}

## Recommended actions
1. {Highest priority}
2. ...
```

---

## Verification

1. Duplicate check: `grep "^- name:" registry.yaml | sed 's/.*name: //' | sort | uniq -d` — must be empty.
2. If registry was edited: `skill_count` matches entry count.

Optional:

```bash
cd "$SKILLS_ROOT" && python3 build_registry.py .   # if build_registry.py exists
```

---

## Guidelines

- **Read real files** — README skill counts can drift from `registry.yaml`.
- **Actionable only** — prioritize phantoms, duplicates, and `skill_count` mismatch.
- **Align with** `scripts/validate_skill_frontmatter.py` — extend that script if you add new automated rules.

---

## Gotchas

1. **`skill_count` is manual** — easy to forget after adding a skill.
2. **Nested skill folders** — resolve orphans using full `path:` strings, not only top-level names.
3. **Registry `description` may be shorter than SKILL.md** — OK unless triggers are wrong.
4. **`validate_skill_frontmatter.py`** does not validate description length or trigger phrases — spot-audit only (Step 6).
