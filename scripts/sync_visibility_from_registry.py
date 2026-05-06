#!/usr/bin/env python3
"""
Insert or update `visibility: public|team` in each SKILL.md from registry.yaml.

Registry is the source of truth for visibility. Run from beam-next-skills repo root:

  python3 scripts/sync_visibility_from_registry.py [--dry-run]

Requires PyYAML (pip install pyyaml).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def insert_or_replace_visibility(
    frontmatter_body: str, visibility: str
) -> tuple[str, str]:
    """
    Returns (new_body, action) where action is 'unchanged'|'replaced'|'inserted'.
    """
    lines = frontmatter_body.splitlines()
    idx_vis = next(
        (i for i, ln in enumerate(lines) if ln.strip().startswith("visibility:")),
        None,
    )
    if idx_vis is not None:
        old = lines[idx_vis].split(":", 1)[1].strip().strip("'\"")
        if old == visibility:
            return frontmatter_body, "unchanged"
        lines = list(lines)
        lines[idx_vis] = f"visibility: {visibility}"
        return "\n".join(lines), "replaced"

    # Insert after `type:` if present, else after `name:`
    idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith("type:")), None)
    if idx is None:
        idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith("name:")), None)
    insert_at = (idx + 1) if idx is not None else 0
    new_lines = lines[:insert_at] + [f"visibility: {visibility}"] + lines[insert_at:]
    return "\n".join(new_lines), "inserted"


def patch_skill_md(path: Path, visibility: str, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return "no_frontmatter"
    end = text.find("\n---", 3)
    if end == -1:
        return "no_closing_frontmatter"
    fm_body = text[4:end]
    rest = text[end:]
    new_body, action = insert_or_replace_visibility(fm_body, visibility)
    if action == "unchanged":
        return "ok_unchanged"
    new_text = "---\n" + new_body + rest
    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return action


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    reg_path = root / "registry.yaml"
    data = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    skills = data.get("skills") or []

    stats: dict[str, int] = {}
    for entry in skills:
        name = entry.get("name")
        vis = entry.get("visibility")
        rel = entry.get("path")
        if not name or not rel or not vis:
            continue
        if vis not in ("public", "team"):
            print(f"SKIP {name}: invalid visibility {vis!r}", file=sys.stderr)
            continue
        md = root / rel / "SKILL.md"
        if not md.is_file():
            print(f"MISSING: {md}", file=sys.stderr)
            continue
        result = patch_skill_md(md, vis, args.dry_run)
        stats[result] = stats.get(result, 0) + 1

    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if args.dry_run:
        print("(dry-run: no files written)")


if __name__ == "__main__":
    main()
