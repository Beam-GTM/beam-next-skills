#!/usr/bin/env python3
"""
Project Cleanup — Find and fix references to projects after archiving.

Auto-discovers project roots (directories containing project folders with
01-planning/ subfolders). Works with any workspace structure, not just
a specific layout.

After moving a project to <projects-root>/archive/, other files may still
reference the old path. This script checks for outdated references and
optionally updates them.

Usage:
    python run_cleanup.py --check                          # auto-discover + report
    python run_cleanup.py --fix                            # update references in place
    python run_cleanup.py --fix --dry-run                  # show what would be changed
    python run_cleanup.py --list                           # list projects and locations
    python run_cleanup.py --projects-root 03-projects/X    # explicit root
"""

import argparse
import sys
from pathlib import Path


ARCHIVE_SUBDIR = "archive"
OVERVIEW_NAMES = ("01-overview.md", "overview.md")
SKIP_DIRS = {".cache", "node_modules", ".git", "__pycache__", "dist", "build", ".sync-backup"}
SCAN_EXTENSIONS = {".md", ".yaml", ".yml"}


def discover_project_roots(base_path: Path) -> list[Path]:
    """Auto-discover project root directories.

    A project root is a directory that contains subdirectories which themselves
    have a 01-planning/ subfolder (i.e. the parent of project folders).
    Also requires an archive/ subfolder to be meaningful for cleanup.

    Common patterns:
    - 03-projects/Beam-Next/  (contains 01-foo/, 02-bar/, archive/)
    - 03-projects/01-xeterna/ (if it has sub-projects with 01-planning/)
    """
    roots = []
    # Look for directories that contain project-like children
    # A project-like child has 01-planning/ inside it
    for projects_dir in base_path.glob("*-projects"):
        if not projects_dir.is_dir():
            continue
        # Check each subdirectory of the projects dir
        for candidate in projects_dir.iterdir():
            if not candidate.is_dir() or candidate.name.startswith("."):
                continue
            if _is_project_root(candidate):
                roots.append(candidate)

    # Also check the base itself (if it directly contains project folders)
    if _is_project_root(base_path):
        roots.append(base_path)

    return roots


def _is_project_root(directory: Path) -> bool:
    """Check if directory is a project root (contains project folders with 01-planning/)."""
    has_projects = False
    for child in directory.iterdir():
        if not child.is_dir() or child.name.startswith(".") or child.name == ARCHIVE_SUBDIR:
            continue
        if _has_overview(child):
            has_projects = True
            break
    return has_projects


def get_projects(project_root: Path) -> tuple[list[str], list[str]]:
    """Return (active_slugs, archived_slugs) for a given project root."""
    if not project_root.exists():
        return [], []

    active = []
    for d in project_root.iterdir():
        if d.is_file() or d.name == ARCHIVE_SUBDIR or d.name.startswith("."):
            continue
        if _has_overview(d):
            active.append(d.name)

    archived = []
    archive_dir = project_root / ARCHIVE_SUBDIR
    if archive_dir.exists():
        for d in archive_dir.iterdir():
            if d.is_dir() and _has_overview(d):
                archived.append(d.name)

    return active, archived


def _has_overview(project_dir: Path) -> bool:
    """Check if a directory looks like a project (has 01-planning/ with overview)."""
    planning = project_dir / "01-planning"
    if not planning.exists():
        return False
    for name in OVERVIEW_NAMES:
        if (planning / name).exists():
            return True
    return False


def get_files_to_scan(base_path: Path) -> list[Path]:
    """Return list of .md and .yaml files to scan for project path references.

    Scans all top-level directories in the workspace, skipping known non-content dirs.
    """
    candidates = []
    for child in base_path.iterdir():
        if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
            continue
        for f in child.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in SCAN_EXTENSIONS:
                continue
            if any(s in f.parts for s in SKIP_DIRS):
                continue
            candidates.append(f)
    return candidates


def find_outdated_references(
    base_path: Path,
    project_root: Path,
    active_slugs: list[str],
    archived_slugs: list[str],
) -> list[tuple[Path, str, str, str]]:
    """Find references that point to the wrong location (missing/extra archive/)."""
    try:
        root_rel = str(project_root.relative_to(base_path))
    except ValueError:
        root_rel = str(project_root)

    prefix = root_rel + "/"
    prefix_archive = root_rel + f"/{ARCHIVE_SUBDIR}/"
    replacements = []

    for f in get_files_to_scan(base_path):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        for slug in archived_slugs:
            old_path = prefix + slug
            new_path = prefix_archive + slug
            if new_path in text:
                continue  # already correct
            if old_path in text:
                replacements.append((f, old_path, new_path, f"archived project {slug}"))

        for slug in active_slugs:
            old_path = prefix_archive + slug
            new_path = prefix + slug
            if old_path in text:
                replacements.append((f, old_path, new_path, f"active project {slug} (remove archive/)"))

    # Dedupe
    seen = set()
    out = []
    for f, old, new, reason in replacements:
        key = (f, old, new)
        if key not in seen:
            seen.add(key)
            out.append((f, old, new, reason))
    return out


def apply_fixes(
    base_path: Path,
    replacements: list[tuple[Path, str, str, str]],
    dry_run: bool,
) -> None:
    """Apply replacements per file. If dry_run, only print."""
    by_file: dict[Path, list[tuple[str, str, str]]] = {}
    for f, old, new, reason in replacements:
        by_file.setdefault(f, []).append((old, new, reason))
    for f in sorted(by_file):
        items = by_file[f]
        try:
            rel = f.relative_to(base_path)
        except ValueError:
            rel = f
        if dry_run:
            for old, new, reason in items:
                print(f"  [dry-run] {rel}: {old!r} -> {new!r} ({reason})")
            continue
        text = f.read_text(encoding="utf-8")
        for old, new, reason in items:
            if old in text:
                text = text.replace(old, new)
                print(f"  Updated {rel}: {reason}")
        f.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check/fix project path references after archiving. "
        "Auto-discovers project roots or accepts an explicit --projects-root."
    )
    parser.add_argument("--base-path", default=".", help="Workspace root (default: .)")
    parser.add_argument(
        "--projects-root",
        default=None,
        help="Explicit project root path (e.g. 03-projects/Beam-Next). "
        "If not provided, auto-discovers all project roots.",
    )
    parser.add_argument("--check", action="store_true", help="Report outdated references only")
    parser.add_argument("--fix", action="store_true", help="Update references in place")
    parser.add_argument("--dry-run", action="store_true", help="With --fix: show what would be changed")
    parser.add_argument("--list", action="store_true", help="List projects and locations")
    args = parser.parse_args()

    base = Path(args.base_path).resolve()

    # Discover or use explicit project roots
    if args.projects_root:
        pr = base / args.projects_root if not Path(args.projects_root).is_absolute() else Path(args.projects_root)
        if not pr.exists():
            print(f"Error: projects root not found: {pr}")
            return 1
        project_roots = [pr]
    else:
        project_roots = discover_project_roots(base)
        if not project_roots:
            print("No project roots found. Use --projects-root to specify one explicitly.")
            print("A project root contains subdirectories with 01-planning/ folders.")
            return 1

    all_replacements = []

    for pr in project_roots:
        try:
            pr_rel = pr.relative_to(base)
        except ValueError:
            pr_rel = pr

        active, archived = get_projects(pr)

        if args.list:
            print(f"Project root: {pr_rel}")
            if active:
                print("  Active:")
                for s in sorted(active):
                    print(f"    {pr_rel}/{s}")
            if archived:
                print("  Archived:")
                for s in sorted(archived):
                    print(f"    {pr_rel}/{ARCHIVE_SUBDIR}/{s}")
            if not active and not archived:
                print("  (no projects found)")
            print()
            continue

        replacements = find_outdated_references(base, pr, active, archived)
        all_replacements.extend(replacements)

    if args.list:
        return 0

    if args.check or (not args.fix):
        if not all_replacements:
            print("No outdated project references found.")
            return 0
        label = "Outdated references (run with --fix to update):" if args.check else \
                "Outdated references (use --fix to update, --check to only report):"
        print(label)
        by_file: dict[Path, list[tuple[str, str, str]]] = {}
        for f, old, new, reason in all_replacements:
            by_file.setdefault(f, []).append((old, new, reason))
        for f in sorted(by_file):
            try:
                rel = f.relative_to(base)
            except ValueError:
                rel = f
            print(f"  {rel}")
            for old, new, reason in by_file[f]:
                print(f"    -> {reason}: {old!r} -> {new!r}")
        return 0

    if args.fix:
        if not all_replacements:
            print("No references to fix.")
            return 0
        apply_fixes(base, all_replacements, args.dry_run)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
