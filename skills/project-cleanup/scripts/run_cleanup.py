#!/usr/bin/env python3
"""
Project Cleanup — Find and fix references to Beam Next projects after archiving.

After moving a project to 03-projects/Beam-Next/archive/, other files may still
reference the old path. This script checks for outdated references and optionally
updates them.

Usage:
    python run_cleanup.py --check          # report only
    python run_cleanup.py --fix            # update references in place
    python run_cleanup.py --fix --dry-run # show what would be changed
    python run_cleanup.py --list           # list projects and locations
"""

import argparse
import sys
from pathlib import Path


BEAM_NEXT_DIR = "03-projects/Beam-Next"
ARCHIVE_SUBDIR = "archive"
OVERVIEW_NAMES = ("01-overview.md", "overview.md")


def get_projects(base_path: str) -> tuple[list[str], list[str]]:
    """Return (active_slugs, archived_slugs). Slug = folder name (e.g. 05-next-self-learning-platform)."""
    root = Path(base_path).resolve()
    beam_next = root / "03-projects" / "Beam-Next"
    if not beam_next.exists():
        return [], []

    active = []
    for d in beam_next.iterdir():
        if d.is_file() or d.name == ARCHIVE_SUBDIR:
            continue
        if _has_overview(d):
            active.append(d.name)

    archived = []
    archive_dir = beam_next / ARCHIVE_SUBDIR
    if archive_dir.exists():
        for d in archive_dir.iterdir():
            if d.is_dir() and _has_overview(d):
                archived.append(d.name)

    return active, archived


def _has_overview(project_dir: Path) -> bool:
    planning = project_dir / "01-planning"
    if not planning.exists():
        return False
    for name in OVERVIEW_NAMES:
        if (planning / name).exists():
            return True
    return False


def get_files_to_scan(base_path: str) -> list[Path]:
    """Return list of .md and .yaml files to scan for project path references."""
    root = Path(base_path).resolve()
    candidates = []
    dirs_to_scan = [
        root / "03-projects" / "Beam-Next",
        root / "04-apps" / "beam-prism-electron" / "docs",
        root / "00-system" / "documentation",
    ]
    skip_dirs = {".cache", "node_modules", ".git", "__pycache__"}
    for dir_path in dirs_to_scan:
        if not dir_path.exists():
            continue
        for f in dir_path.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in (".md", ".yaml", ".yml"):
                continue
            if any(s in f.parts for s in skip_dirs):
                continue
            candidates.append(f)
    return candidates


def find_outdated_references(
    base_path: str,
    active_slugs: list[str],
    archived_slugs: list[str],
) -> list[tuple[Path, str, str, str]]:
    """
    Find (file, line_content, old_substring, new_substring) where a reference
    should be updated. Archived projects: path should include archive/; active: should not.
    """
    root = Path(base_path).resolve()
    beam_prefix = "03-projects/Beam-Next/"
    beam_prefix_archive = "03-projects/Beam-Next/archive/"
    replacements = []

    for f in get_files_to_scan(base_path):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        # References that look like Beam-Next project paths (allow trailing slash or not)
        for slug in archived_slugs:
            old_path = beam_prefix + slug
            new_path = beam_prefix_archive + slug
            if new_path in text:
                continue  # already correct
            if old_path in text:
                # Replace all occurrences in this file
                count = text.count(old_path)
                replacements.append((f, old_path, new_path, f"archived project {slug}"))

        for slug in active_slugs:
            old_path = beam_prefix_archive + slug
            new_path = beam_prefix + slug
            if old_path in text:
                count = text.count(old_path)
                replacements.append((f, old_path, new_path, f"active project {slug} (remove archive/)"))

    # Dedupe by (file, old, new) and aggregate
    seen = set()
    out = []
    for f, old, new, reason in replacements:
        key = (f, old, new)
        if key in seen:
            continue
        seen.add(key)
        out.append((f, old, new, reason))
    return out


def apply_fixes(
    base_path: str,
    replacements: list[tuple[Path, str, str, str]],
    dry_run: bool,
) -> None:
    """Apply replacements per file (all replacements in a file in one write). If dry_run, only print."""
    base = Path(base_path).resolve()
    by_file: dict[Path, list[tuple[str, str, str]]] = {}
    for f, old, new, reason in replacements:
        by_file.setdefault(f, []).append((old, new, reason))
    for f in sorted(by_file):
        items = by_file[f]
        if dry_run:
            for old, new, reason in items:
                print(f"  [dry-run] {f.relative_to(base)}: {old!r} -> {new!r} ({reason})")
            continue
        text = f.read_text(encoding="utf-8")
        for old, new, reason in items:
            if old in text:
                text = text.replace(old, new)
                print(f"  Updated {f.relative_to(base)}: {reason}")
        f.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check/fix Beam Next project path references after archiving.")
    parser.add_argument("--base-path", default=".", help="Beam Next repo root")
    parser.add_argument("--check", action="store_true", help="Report outdated references only")
    parser.add_argument("--fix", action="store_true", help="Update references in place")
    parser.add_argument("--dry-run", action="store_true", help="With --fix: show what would be changed")
    parser.add_argument("--list", action="store_true", help="List projects and locations")
    args = parser.parse_args()

    base = Path(args.base_path).resolve()
    if not (base / "03-projects" / "Beam-Next").exists():
        print("Error: 03-projects/Beam-Next not found. Run from repo root or set --base-path.")
        return 1

    active, archived = get_projects(args.base_path)

    if args.list:
        print("Projects (active):")
        for s in sorted(active):
            print(f"  {BEAM_NEXT_DIR}/{s}")
        print("Projects (archived):")
        for s in sorted(archived):
            print(f"  {BEAM_NEXT_DIR}/{ARCHIVE_SUBDIR}/{s}")
        return 0

    replacements = find_outdated_references(args.base_path, active, archived)

    if args.check:
        if not replacements:
            print("No outdated project references found.")
            return 0
        print("Outdated references (run with --fix to update):")
        by_file = {}
        for f, old, new, reason in replacements:
            by_file.setdefault(f, []).append((old, new, reason))
        for f in sorted(by_file):
            print(f"  {f.relative_to(base)}")
            for old, new, reason in by_file[f]:
                print(f"    -> {reason}: {old!r} -> {new!r}")
        return 0

    if args.fix:
        if not replacements:
            print("No references to fix.")
            return 0
        apply_fixes(args.base_path, replacements, args.dry_run)
        return 0

    # Default: same as --check
    if not replacements:
        print("No outdated project references found.")
        return 0
    print("Outdated references (use --fix to update, --check to only report):")
    by_file = {}
    for f, old, new, reason in replacements:
        by_file.setdefault(f, []).append((old, new, reason))
    for f in sorted(by_file):
        print(f"  {f.relative_to(base)}")
        for old, new, reason in by_file[f]:
            print(f"    -> {reason}: {old!r} -> {new!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
