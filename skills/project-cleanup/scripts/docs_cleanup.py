#!/usr/bin/env python3
"""
Docs Cleanup — Detect completed docs, archive them, add banners, update README index.

Scans a docs directory for .md files that appear to be "done" based on content signals,
then optionally archives them (move to archive/, add DONE banner, update README.md).

Usage:
    python docs_cleanup.py --docs-path <path>                   # scan and report
    python docs_cleanup.py --docs-path <path> --archive         # scan, report, and archive
    python docs_cleanup.py --docs-path <path> --archive --dry-run  # show what would happen
    python docs_cleanup.py --docs-path <path> --fix-redirects   # fix redirect files pointing to moved docs

Examples:
    python docs_cleanup.py --docs-path 04-apps/beam-prism-electron/docs
    python docs_cleanup.py --docs-path 04-apps/beam-prism-electron/docs --archive
"""

import argparse
import re
import sys
from pathlib import Path


# Signals that a doc is "done" — checked against the first 80 lines of each file
DONE_PATTERNS = [
    re.compile(r"status[:\s]*done", re.IGNORECASE),
    re.compile(r"status[:\s]*complete", re.IGNORECASE),
    re.compile(r"all\s+phases?\s+complete", re.IGNORECASE),
    re.compile(r"all\s+complete", re.IGNORECASE),
    re.compile(r"phases?\s+\d+[-–]\d+\s+(done|complete)", re.IGNORECASE),
    re.compile(r"status[:\s]*shipped", re.IGNORECASE),
    re.compile(r"\*\*.*shipped\*\*", re.IGNORECASE),
    re.compile(r"Status:\s*DONE", re.IGNORECASE),
    re.compile(r"\*\*Status\*\*:\s*DONE", re.IGNORECASE),
    re.compile(r"V1\s*\+?\s*V2.*DONE", re.IGNORECASE),
    # Only match "archived" when it's clearly a status (not a link/path)
    re.compile(r"status[:\s]*archived", re.IGNORECASE),
    re.compile(r"\*\*Status\*\*.*archived", re.IGNORECASE),
]

# Signals that a doc is still active — overrides done signals
ACTIVE_PATTERNS = [
    re.compile(r"in\s*progress", re.IGNORECASE),
    re.compile(r"status[:\s]*active", re.IGNORECASE),
    re.compile(r"status[:\s]*in.progress", re.IGNORECASE),
    re.compile(r"next\s+steps?[:\s]", re.IGNORECASE),
    re.compile(r"phase\s+\w+\s+in\s+progress", re.IGNORECASE),
]

# Files that should never be archived (core docs)
PROTECTED_FILES = {
    "README.md",
    "plan.md",
    "backlog.md",
}

DONE_BANNER = '> **Status**: DONE — archived {date}\n'
SCAN_LINES = 80  # How many lines to scan for signals


def scan_doc(filepath: Path) -> dict:
    """Scan a single .md file for completion signals. Returns analysis dict."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"file": filepath, "error": str(e)}

    lines = text.split("\n")
    head = "\n".join(lines[:SCAN_LINES])

    done_matches = []
    for pat in DONE_PATTERNS:
        m = pat.search(head)
        if m:
            done_matches.append(m.group())

    active_matches = []
    for pat in ACTIVE_PATTERNS:
        m = pat.search(head)
        if m:
            active_matches.append(m.group())

    has_done_banner = bool(re.search(r"Status.*DONE.*archived", head))

    # Cross-project backlog files with "None are V1 blockers" are also done
    if re.search(r"none\s+are\s+v1\s+blockers?", head, re.IGNORECASE):
        done_matches.append("None are V1 blockers")

    status = "unknown"
    if done_matches and not active_matches:
        status = "done"
    elif active_matches:
        status = "active"
    elif done_matches and active_matches:
        status = "mixed"  # has both signals — needs manual review

    return {
        "file": filepath,
        "status": status,
        "done_signals": done_matches,
        "active_signals": active_matches,
        "has_done_banner": has_done_banner,
        "title": _extract_title(lines),
    }


def _extract_title(lines: list[str]) -> str:
    """Extract the first # heading from lines."""
    for line in lines[:10]:
        if line.startswith("# "):
            return line[2:].strip()
    return "(no title)"


def scan_docs_dir(docs_path: Path) -> list[dict]:
    """Scan all .md files in docs root (not archive/) for completion signals."""
    results = []
    for f in sorted(docs_path.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue
        if f.name in PROTECTED_FILES:
            continue
        results.append(scan_doc(f))
    return results


def archive_file(filepath: Path, archive_dir: Path, date: str, dry_run: bool) -> str:
    """Move file to archive dir and add DONE banner. Returns action description."""
    dest = archive_dir / filepath.name
    if dest.exists():
        return f"  SKIP {filepath.name} — already exists in archive/"

    if dry_run:
        return f"  [dry-run] Would move {filepath.name} → archive/{filepath.name} + add DONE banner"

    # Read content, add banner after first heading
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Find first heading line
    banner = DONE_BANNER.format(date=date)
    inserted = False
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, banner)
            inserted = True
            break

    if not inserted:
        lines.insert(0, banner)

    # Write to archive
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines), encoding="utf-8")

    # Remove original
    filepath.unlink()

    return f"  Archived {filepath.name} → archive/{filepath.name}"


def find_redirect_files(base_path: Path, docs_path: Path) -> list[tuple[Path, str, str]]:
    """Find redirect files that point to docs that have been moved to archive/.
    Returns list of (redirect_file, old_target, new_target)."""
    archive_dir = docs_path / "archive"
    if not archive_dir.exists():
        return []

    archived_names = {f.name for f in archive_dir.iterdir() if f.is_file() and f.suffix == ".md"}
    results = []

    # Scan common redirect locations
    redirect_dirs = list(base_path.glob("03-projects/**/02-resources"))
    for rdir in redirect_dirs:
        if not rdir.is_dir():
            continue
        for f in rdir.iterdir():
            if not f.is_file() or f.suffix != ".md":
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue

            # Check if this redirect points to a file now in archive/
            for name in archived_names:
                # Match paths like docs/filename.md but NOT docs/archive/filename.md
                old_pattern = f"docs/{name}"
                new_pattern = f"docs/archive/{name}"
                if old_pattern in text and new_pattern not in text:
                    results.append((f, old_pattern, new_pattern))

    return results


def fix_redirects(redirects: list[tuple[Path, str, str]], base_path: Path, dry_run: bool) -> list[str]:
    """Fix redirect files to point to archive/ paths."""
    actions = []
    for filepath, old, new in redirects:
        rel = filepath.relative_to(base_path)
        if dry_run:
            actions.append(f"  [dry-run] {rel}: {old!r} → {new!r}")
            continue
        text = filepath.read_text(encoding="utf-8")
        text = text.replace(old, new)
        filepath.write_text(text, encoding="utf-8")
        actions.append(f"  Fixed {rel}: {old!r} → {new!r}")
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan docs for completed files and optionally archive them."
    )
    parser.add_argument(
        "--docs-path",
        required=True,
        help="Path to the docs directory (e.g. 04-apps/beam-prism-electron/docs)",
    )
    parser.add_argument("--base-path", default=".", help="Repo root (default: .)")
    parser.add_argument("--archive", action="store_true", help="Move done files to archive/")
    parser.add_argument("--fix-redirects", action="store_true", help="Fix redirect files pointing to moved docs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")
    parser.add_argument("--date", default=None, help="Date for DONE banner (default: today)")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for AI consumption)")
    args = parser.parse_args()

    base = Path(args.base_path).resolve()
    docs = base / args.docs_path if not Path(args.docs_path).is_absolute() else Path(args.docs_path)

    if not docs.exists():
        print(f"Error: docs path not found: {docs}")
        return 1

    # Scan
    results = scan_docs_dir(docs)
    done_files = [r for r in results if r["status"] == "done" and not r.get("has_done_banner")]
    active_files = [r for r in results if r["status"] == "active"]
    mixed_files = [r for r in results if r["status"] == "mixed"]
    already_done = [r for r in results if r.get("has_done_banner")]

    if args.json:
        import json
        output = {
            "docs_path": str(docs),
            "done": [{"file": str(r["file"].name), "signals": r["done_signals"], "title": r["title"]} for r in done_files],
            "active": [{"file": str(r["file"].name), "title": r["title"]} for r in active_files],
            "mixed": [{"file": str(r["file"].name), "done_signals": r["done_signals"], "active_signals": r["active_signals"], "title": r["title"]} for r in mixed_files],
            "already_archived_banner": [{"file": str(r["file"].name)} for r in already_done],
        }
        print(json.dumps(output, indent=2))
        return 0

    # Report
    try:
        display_path = docs.relative_to(base)
    except ValueError:
        display_path = docs
    print(f"Docs cleanup scan: {display_path}")
    print(f"  Total .md files scanned: {len(results)}")
    print()

    if done_files:
        print(f"DONE ({len(done_files)} files — ready to archive):")
        for r in done_files:
            signals = ", ".join(r["done_signals"][:3])
            print(f"  {r['file'].name:<45} [{signals}]")
        print()

    if mixed_files:
        print(f"MIXED ({len(mixed_files)} files — needs manual review):")
        for r in mixed_files:
            print(f"  {r['file'].name:<45} done={r['done_signals']}, active={r['active_signals']}")
        print()

    if active_files:
        print(f"ACTIVE ({len(active_files)} files — keep in root):")
        for r in active_files:
            print(f"  {r['file'].name}")
        print()

    if already_done:
        print(f"ALREADY BANNERED ({len(already_done)} files — have DONE banner but still in root):")
        for r in already_done:
            print(f"  {r['file'].name}")
        print()

    if not done_files and not already_done:
        print("No files to archive.")
        return 0

    # Archive
    if args.archive:
        from datetime import date as dt_date
        archive_date = args.date or dt_date.today().isoformat()
        archive_dir = docs / "archive"

        to_archive = done_files + already_done
        print(f"\nArchiving {len(to_archive)} files:")
        for r in to_archive:
            action = archive_file(r["file"], archive_dir, archive_date, args.dry_run)
            print(action)

        if not args.dry_run:
            print(f"\nMoved {len(to_archive)} files to archive/.")
            print("IMPORTANT: Update README.md index manually (move rows from active → archive table).")
    else:
        if done_files or already_done:
            total = len(done_files) + len(already_done)
            print(f"Run with --archive to move {total} files to archive/.")
            print("Run with --archive --dry-run to preview changes first.")

    # Fix redirects
    if args.fix_redirects:
        redirects = find_redirect_files(base, docs)
        if not redirects:
            print("\nNo redirect files need updating.")
        else:
            print(f"\nFixing {len(redirects)} redirect files:")
            actions = fix_redirects(redirects, base, args.dry_run)
            for a in actions:
                print(a)

    return 0


if __name__ == "__main__":
    sys.exit(main())
