#!/usr/bin/env python3
"""
Validate SKILL.md frontmatter across skills/ (Phase 1 rules).

  python3 scripts/validate_skill_frontmatter.py [--strict] [--require-visibility]

Default: print warnings, exit 0.
--strict: exit 1 if any skill fails (for CI once the repo is fully migrated).
--require-visibility: treat missing `visibility:` as an error (public | team).

`visibility`: `public` = catalog / external distribution; `team` = internal-only (ROI, pricing, ops).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED_CATEGORIES = frozenset(
    {
        "productivity",
        "meetings",
        "analysis",
        "export",
        "knowledge",
        "integrations",
        "general",
        "learning",
        "projects",
        "skill-dev",
        "system",
        "tools",
        "experts",
    }
)

# Distribution: public = catalog / external; team = internal (Beam team, ROI, pricing, etc.)
ALLOWED_VISIBILITY = frozenset({"public", "team"})


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[4:end]


def parse_tags_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Parse YAML list-style tags after `tags:` line. Returns (tags, next_index)."""
    tags: list[str] = []
    i = start
    if i < len(lines) and "[" in lines[i - 1]:
        m = re.search(r"\[(.*)\]", lines[i - 1])
        if m:
            return [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()], i
    while i < len(lines) and lines[i].strip().startswith("-"):
        item = lines[i].strip()[1:].strip()
        tags.append(item.strip("'\""))
        i += 1
    return tags, i


def parse_frontmatter(block: str) -> dict[str, str | list[str]]:
    fm: dict[str, str | list[str]] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        m = re.match(r"^type:\s*(.+)$", stripped)
        if m:
            fm["type"] = m.group(1).strip().strip("'\"")
            i += 1
            continue

        m = re.match(r"^category:\s*(.+)$", stripped)
        if m:
            fm["category"] = m.group(1).strip().strip("'\"")
            i += 1
            continue

        m = re.match(r"^visibility:\s*(.+)$", stripped)
        if m:
            fm["visibility"] = m.group(1).strip().strip("'\"")
            i += 1
            continue

        if stripped.startswith("tags:") and "[" in stripped:
            m = re.search(r"\[(.*)\]", stripped)
            if m:
                fm["tags"] = [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]
            i += 1
            continue

        if stripped == "tags:" or (stripped.startswith("tags:") and "[" not in stripped):
            i += 1
            tags, i = parse_tags_block(lines, i)
            if tags:
                fm["tags"] = tags
            continue

        i += 1

    return fm


def validate_file(path: Path, require_visibility: bool) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    block = extract_frontmatter(text)
    if block is None:
        issues.append(f"{path}: no YAML frontmatter")
        return issues

    fm = parse_frontmatter(block)

    if "type" not in fm:
        issues.append(f"{path}: missing `type` (use skill | agent per skills-architecture)")

    tags = fm.get("tags")
    if isinstance(tags, list):
        n = len(tags)
        if n < 2 or n > 5:
            issues.append(f"{path}: tags should have 2–5 entries, got {n}")

    cat = fm.get("category")
    if isinstance(cat, str) and cat and cat not in ALLOWED_CATEGORIES:
        issues.append(f"{path}: category {cat!r} not in allowed set")

    vis = fm.get("visibility")
    if isinstance(vis, str) and vis and vis not in ALLOWED_VISIBILITY:
        issues.append(f"{path}: visibility must be public or team, got {vis!r}")
    elif require_visibility and not vis:
        issues.append(
            f"{path}: missing `visibility` (use `public` for catalog-wide; `team` for internal-only)"
        )

    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any validation issue is found",
    )
    parser.add_argument(
        "--require-visibility",
        action="store_true",
        help="Fail if visibility: is missing (use after all SKILL.md files include it)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        print("skills/ not found; run from beam-next-skills repo root", file=sys.stderr)
        sys.exit(2)

    all_issues: list[str] = []
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        all_issues.extend(validate_file(skill_md, require_visibility=args.require_visibility))

    for line in all_issues:
        print(line, file=sys.stderr)

    if all_issues:
        print(f"\n{len(all_issues)} issue(s).", file=sys.stderr)
        if args.strict:
            sys.exit(1)
    else:
        print("All checked SKILL.md files passed validation rules.")


if __name__ == "__main__":
    main()
