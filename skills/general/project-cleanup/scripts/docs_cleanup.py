#!/usr/bin/env python3
"""
Docs Cleanup — Intelligent doc triage with confidence scoring.

Scans a directory (recursively or flat) for .md files, analyzes completion signals,
and produces a confidence-scored report the AI can act on.

Three confidence tiers:
  HIGH   — auto-archive: explicit "Status: DONE", "Superseded", all checkboxes done
  MEDIUM — propose: looks complete but no explicit marker, or stale with no TODOs
  LOW    — ask user: mixed signals, ambiguous status

Usage:
    python docs_cleanup.py --path <dir>                          # scan flat (root only)
    python docs_cleanup.py --path <dir> --recursive              # scan recursively
    python docs_cleanup.py --path <dir> --json                   # machine-readable output
    python docs_cleanup.py --path <dir> --archive                # move HIGH confidence → archive/
    python docs_cleanup.py --path <dir> --archive --dry-run      # preview archive actions
    python docs_cleanup.py --path <dir> --fix-redirects          # fix links to moved docs

    # Full project audit (scans 01-planning/, 02-resources/, 03-working/, docs/)
    python docs_cleanup.py --project <project-dir> --json

Examples:
    python docs_cleanup.py --path 04-apps/beam-prism-electron/docs
    python docs_cleanup.py --project 03-projects/Beam-Next/13-beam-prism-agents-platform --json
"""

import argparse
import json
import re
import sys
from datetime import date as dt_date
from pathlib import Path


# ─── Signal patterns ────────────────────────────────────────────────

# HIGH confidence "done" — explicit status markers
DONE_EXPLICIT = [
    re.compile(r"(?:^|\n)\s*>?\s*\*?\*?Status\*?\*?\s*[:]\s*(?:DONE|COMPLETE|SHIPPED|ARCHIVED)", re.IGNORECASE),
    re.compile(r"(?:^|\n)status:\s*(?:done|complete|shipped|archived)", re.IGNORECASE),  # frontmatter
    re.compile(r"(?:^|\n)\s*>.*Status.*DONE.*archived", re.IGNORECASE),  # banner
]

# HIGH confidence "done" — superseded markers
SUPERSEDED = [
    re.compile(r"superseded", re.IGNORECASE),
    re.compile(r"replaced\s+by\b", re.IGNORECASE),
    re.compile(r"deprecated\b.*(?:use|see|moved)", re.IGNORECASE),
    re.compile(r"(?:old|previous|legacy)\s+(?:approach|version|plan)", re.IGNORECASE),
]

# HIGH confidence "done" — all phases/steps complete
ALL_COMPLETE = [
    re.compile(r"all\s+(?:phases?|steps?|tasks?|items?)\s+(?:done|complete)", re.IGNORECASE),
    re.compile(r"phases?\s+\d+[-–]\d+\s*(?:[:]\s*)?(?:done|complete)", re.IGNORECASE),
    re.compile(r"(?:V1|V2|V1\s*\+\s*V2).*(?:DONE|COMPLETE)", re.IGNORECASE),
    re.compile(r"all\s+complete", re.IGNORECASE),
]

# MEDIUM confidence — content signals that suggest completion
COMPLETION_HINTS = [
    re.compile(r"(?:implemented|shipped|deployed|released|merged)\s+(?:in|on|at)", re.IGNORECASE),
    re.compile(r"session\s+\d+.*(?:done|complete)", re.IGNORECASE),
    re.compile(r"no\s+remaining\s+(?:work|items|tasks)", re.IGNORECASE),
    re.compile(r"none\s+are\s+v1\s+blockers?", re.IGNORECASE),
    re.compile(r"this\s+(?:plan|doc|document)\s+is\s+(?:complete|done|finished)", re.IGNORECASE),
]

# Active signals — override done signals
ACTIVE_SIGNALS = [
    re.compile(r"status\s*[:]\s*(?:active|in.progress|in progress|wip|draft)", re.IGNORECASE),
    re.compile(r"(?:^|\n)#+\s*(?:Next\s+Steps?|TODO|Action\s+Items?)\s*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"phase\s+\w+\s+in\s+progress", re.IGNORECASE),
    re.compile(r"currently\s+(?:working|building|implementing)", re.IGNORECASE),
    re.compile(r"status\s*[:]\s*(?:PLANNING|READY)", re.IGNORECASE),
]

# Protected files — never suggest archiving
PROTECTED_NAMES = {
    "README.md", "readme.md",
    "plan.md", "PLAN.md",
    "backlog.md", "BACKLOG.md",
    "SKILL.md", "CLAUDE.md",
    "index.md",
}

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".cache", "__pycache__",
             ".sync-backup", "archive", "Archive"}

DONE_BANNER = '> **Status**: DONE — archived {date}\n'


# ─── Analysis ───────────────────────────────────────────────────────

def analyze_file(filepath: Path) -> dict:
    """Deep analysis of a single .md file. Returns structured report."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"file": str(filepath), "error": str(e)}

    lines = text.split("\n")
    head = "\n".join(lines[:100])
    full = text

    result = {
        "file": str(filepath),
        "name": filepath.name,
        "title": _extract_title(lines),
        "line_count": len(lines),
        "signals": {},  # category → list of matched strings
        "counters": {},
        "confidence": "unknown",  # HIGH, MEDIUM, LOW, ACTIVE, PROTECTED
        "action": "unknown",  # archive, keep, review
        "reason": "",
    }

    # Protected check
    if filepath.name in PROTECTED_NAMES:
        result["confidence"] = "PROTECTED"
        result["action"] = "keep"
        result["reason"] = "Protected file (core doc)"
        return result

    # Already has archive banner
    if re.search(r"Status.*DONE.*archived", head):
        result["confidence"] = "HIGH"
        result["action"] = "archive"
        result["reason"] = "Already has DONE/archived banner but not in archive/"
        result["signals"]["done_banner"] = ["Has DONE archived banner"]
        return result

    # Collect signals
    done_explicit = _match_patterns(head, DONE_EXPLICIT)
    superseded = _match_patterns(full, SUPERSEDED)  # check full text for superseded
    all_complete = _match_patterns(head, ALL_COMPLETE)
    completion_hints = _match_patterns(full, COMPLETION_HINTS)
    active = _match_patterns(head, ACTIVE_SIGNALS)

    if done_explicit:
        result["signals"]["done_explicit"] = done_explicit
    if superseded:
        result["signals"]["superseded"] = superseded
    if all_complete:
        result["signals"]["all_complete"] = all_complete
    if completion_hints:
        result["signals"]["completion_hints"] = completion_hints
    if active:
        result["signals"]["active"] = active

    # Count TODOs and TBDs
    todo_count = len(re.findall(r"\bTODO\b", full, re.IGNORECASE))
    tbd_count = len(re.findall(r"\bTBD\b", full, re.IGNORECASE))
    result["counters"]["todos"] = todo_count
    result["counters"]["tbds"] = tbd_count

    # Count checkboxes
    checked = len(re.findall(r"- \[x\]", full, re.IGNORECASE))
    unchecked = len(re.findall(r"- \[ \]", full))
    total_boxes = checked + unchecked
    result["counters"]["checkboxes_checked"] = checked
    result["counters"]["checkboxes_unchecked"] = unchecked
    result["counters"]["checkboxes_total"] = total_boxes

    # Is this a redirect/stub file?
    is_redirect = (
        len(lines) < 15
        and any(re.search(r"canonical.*location|redirect|see\s+instead|moved\s+to", line, re.IGNORECASE) for line in lines[:10])
    )
    if is_redirect:
        result["signals"]["redirect"] = ["Appears to be a redirect/stub file"]

    # ── Decision logic ──

    has_done = bool(done_explicit or all_complete)
    has_superseded = bool(superseded)
    has_active = bool(active)
    has_hints = bool(completion_hints)
    has_open_items = (unchecked > 0) or (todo_count > 0) or (tbd_count > 0)

    # HIGH: explicit done/superseded, no active signals
    if (has_done or has_superseded) and not has_active:
        result["confidence"] = "HIGH"
        result["action"] = "archive"
        if has_superseded:
            result["reason"] = f"Superseded: {superseded[0]}"
        elif has_done:
            result["reason"] = f"Explicitly done: {(done_explicit or all_complete)[0]}"

    # HIGH: all checkboxes checked (>3 total), no active signals, no open TODOs
    elif total_boxes >= 3 and unchecked == 0 and not has_active and todo_count == 0:
        result["confidence"] = "HIGH"
        result["action"] = "archive"
        result["reason"] = f"All {checked} checkboxes complete, no open TODOs"

    # ACTIVE: has active signals
    elif has_active:
        if has_done:
            result["confidence"] = "LOW"
            result["action"] = "review"
            result["reason"] = f"Mixed signals: done ({(done_explicit or all_complete)[0]}) + active ({active[0]})"
        else:
            result["confidence"] = "ACTIVE"
            result["action"] = "keep"
            result["reason"] = f"Active: {active[0]}"

    # MEDIUM: completion hints but no explicit marker
    elif has_hints and not has_open_items:
        result["confidence"] = "MEDIUM"
        result["action"] = "archive"
        result["reason"] = f"Completion hints: {completion_hints[0]}; no open TODOs/TBDs"

    # MEDIUM: redirect file
    elif is_redirect:
        result["confidence"] = "MEDIUM"
        result["action"] = "review"
        result["reason"] = "Redirect/stub file — check if target still exists"

    # LOW: has open items
    elif has_open_items and not has_active:
        result["confidence"] = "LOW"
        result["action"] = "review"
        items = []
        if unchecked > 0:
            items.append(f"{unchecked} unchecked boxes")
        if todo_count > 0:
            items.append(f"{todo_count} TODOs")
        if tbd_count > 0:
            items.append(f"{tbd_count} TBDs")
        result["reason"] = f"Open items: {', '.join(items)}"

    # No signals at all — needs AI assessment
    else:
        result["confidence"] = "UNKNOWN"
        result["action"] = "review"
        result["reason"] = "No clear signals — AI should read and assess"

    return result


def _match_patterns(text: str, patterns: list) -> list[str]:
    """Return list of matched strings for the given patterns."""
    matches = []
    for pat in patterns:
        m = pat.search(text)
        if m:
            matches.append(m.group().strip()[:80])
    return matches


def _extract_title(lines: list[str]) -> str:
    """Extract the first # heading from lines."""
    for line in lines[:15]:
        if line.startswith("# "):
            return line[2:].strip()
    return "(no title)"


# ─── Directory scanning ─────────────────────────────────────────────

def scan_directory(path: Path, recursive: bool = False) -> list[dict]:
    """Scan a directory for .md files and analyze each one."""
    results = []

    if recursive:
        files = sorted(f for f in path.rglob("*.md")
                       if f.is_file() and not any(s in f.parts for s in SKIP_DIRS))
    else:
        files = sorted(f for f in path.iterdir()
                       if f.is_file() and f.suffix == ".md")

    for f in files:
        results.append(analyze_file(f))
    return results


def scan_project(project_path: Path) -> dict:
    """Scan an entire project directory for doc cleanup.

    Looks in standard subdirectories: 01-planning/, 02-resources/, 03-working/,
    04-outputs/, docs/. Also scans root-level .md files.
    """
    report = {
        "project_path": str(project_path),
        "project_name": project_path.name,
        "sections": {},
    }

    # Standard project subdirectories
    subdirs = ["01-planning", "02-resources", "03-working", "04-outputs", "docs"]

    for subdir_name in subdirs:
        subdir = project_path / subdir_name
        if subdir.exists() and subdir.is_dir():
            results = scan_directory(subdir, recursive=True)
            if results:
                report["sections"][subdir_name] = results

    # Root-level .md files
    root_files = [f for f in project_path.iterdir()
                  if f.is_file() and f.suffix == ".md"]
    if root_files:
        root_results = [analyze_file(f) for f in sorted(root_files)]
        report["sections"]["root"] = root_results

    return report


# ─── Archive operations ─────────────────────────────────────────────

def archive_file(filepath: Path, archive_dir: Path, date_str: str, dry_run: bool) -> str:
    """Move file to archive dir and add DONE banner."""
    filepath = Path(filepath)
    dest = archive_dir / filepath.name
    if dest.exists():
        return f"  SKIP {filepath.name} — already exists in archive/"

    if dry_run:
        return f"  [dry-run] Would move {filepath.name} → archive/{filepath.name}"

    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Add banner after first heading
    banner = DONE_BANNER.format(date=date_str)
    inserted = False
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, banner)
            inserted = True
            break
    if not inserted:
        lines.insert(0, banner)

    archive_dir.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines), encoding="utf-8")
    filepath.unlink()

    return f"  Archived {filepath.name} → archive/{filepath.name}"


def find_redirect_files(base_path: Path, docs_path: Path) -> list[tuple[Path, str, str]]:
    """Find .md files anywhere in workspace that link to docs moved to archive/."""
    archive_dir = docs_path / "archive"
    if not archive_dir.exists():
        return []

    archived_names = {f.name for f in archive_dir.iterdir()
                      if f.is_file() and f.suffix == ".md"}
    if not archived_names:
        return []

    results = []
    for f in base_path.rglob("*.md"):
        try:
            f.relative_to(docs_path)
            continue
        except ValueError:
            pass
        if any(s in f.parts for s in SKIP_DIRS):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for name in archived_names:
            old_pattern = f"docs/{name}"
            new_pattern = f"docs/archive/{name}"
            if old_pattern in text and new_pattern not in text:
                results.append((f, old_pattern, new_pattern))
    return results


def fix_redirects(redirects: list[tuple[Path, str, str]], base_path: Path, dry_run: bool) -> list[str]:
    """Fix redirect files to point to archive/ paths."""
    actions = []
    for filepath, old, new in redirects:
        try:
            rel = filepath.relative_to(base_path)
        except ValueError:
            rel = filepath
        if dry_run:
            actions.append(f"  [dry-run] {rel}: {old!r} → {new!r}")
            continue
        text = filepath.read_text(encoding="utf-8")
        text = text.replace(old, new)
        filepath.write_text(text, encoding="utf-8")
        actions.append(f"  Fixed {rel}: {old!r} → {new!r}")
    return actions


# ─── Output formatting ──────────────────────────────────────────────

def format_json(results: list[dict], path: str) -> str:
    """Format results as JSON for AI consumption."""
    grouped = {"HIGH": [], "MEDIUM": [], "LOW": [], "UNKNOWN": [],
               "ACTIVE": [], "PROTECTED": []}
    for r in results:
        if "error" in r:
            continue
        conf = r.get("confidence", "UNKNOWN")
        grouped.setdefault(conf, []).append({
            "file": r["name"],
            "title": r["title"],
            "action": r["action"],
            "reason": r["reason"],
            "signals": r.get("signals", {}),
            "counters": r.get("counters", {}),
        })
    return json.dumps({
        "path": path,
        "summary": {k: len(v) for k, v in grouped.items() if v},
        "results": {k: v for k, v in grouped.items() if v},
    }, indent=2)


def format_project_json(report: dict) -> str:
    """Format project scan as JSON."""
    output = {
        "project": report["project_name"],
        "project_path": report["project_path"],
        "sections": {},
    }
    for section_name, results in report["sections"].items():
        grouped = {}
        for r in results:
            if "error" in r:
                continue
            conf = r.get("confidence", "UNKNOWN")
            grouped.setdefault(conf, []).append({
                "file": r["name"],
                "title": r["title"],
                "action": r["action"],
                "reason": r["reason"],
                "signals": r.get("signals", {}),
                "counters": r.get("counters", {}),
            })
        if grouped:
            output["sections"][section_name] = {
                "summary": {k: len(v) for k, v in grouped.items()},
                "results": grouped,
            }
    return json.dumps(output, indent=2)


def print_report(results: list[dict], path: str) -> None:
    """Print human-readable report."""
    print(f"Docs cleanup scan: {path}")
    print(f"  Files scanned: {len(results)}")
    print()

    by_conf = {}
    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['file']}: {r['error']}")
            continue
        by_conf.setdefault(r["confidence"], []).append(r)

    order = ["HIGH", "MEDIUM", "LOW", "UNKNOWN", "ACTIVE", "PROTECTED"]
    labels = {
        "HIGH": "ARCHIVE (high confidence)",
        "MEDIUM": "LIKELY ARCHIVE (medium — AI should verify)",
        "LOW": "NEEDS REVIEW (mixed/unclear signals)",
        "UNKNOWN": "NO SIGNALS (AI must read and assess)",
        "ACTIVE": "KEEP (active signals detected)",
        "PROTECTED": "KEEP (protected file)",
    }

    for conf in order:
        items = by_conf.get(conf, [])
        if not items:
            continue
        print(f"{labels[conf]} ({len(items)}):")
        for r in items:
            print(f"  {r['name']:<45} {r['reason']}")
        print()


# ─── Main ───────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Intelligent docs triage with confidence scoring."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", help="Scan a single directory for .md files")
    group.add_argument("--project", help="Scan a full project (01-planning, 02-resources, etc.)")

    parser.add_argument("--recursive", action="store_true",
                        help="With --path: scan subdirectories too")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON (for AI consumption)")
    parser.add_argument("--archive", action="store_true",
                        help="Move HIGH-confidence done files to archive/")
    parser.add_argument("--fix-redirects", action="store_true",
                        help="Fix links to docs that moved to archive/")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without writing")
    parser.add_argument("--base-path", default=".",
                        help="Workspace root (default: .)")
    parser.add_argument("--date", default=None,
                        help="Date for DONE banner (default: today)")

    # Legacy compatibility
    parser.add_argument("--docs-path", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Legacy --docs-path support
    target = args.path or args.docs_path or args.project
    base = Path(args.base_path).resolve()

    if not Path(target).is_absolute():
        target_path = base / target
    else:
        target_path = Path(target)

    if not target_path.exists():
        print(f"Error: path not found: {target_path}")
        return 1

    # Run scan
    if args.project or args.docs_path:
        if args.project:
            report = scan_project(target_path)
            if args.json:
                print(format_project_json(report))
            else:
                for section_name, results in report["sections"].items():
                    print(f"\n{'='*60}")
                    print(f"Section: {section_name}/")
                    print(f"{'='*60}")
                    print_report(results, f"{target}/{section_name}")
            return 0
        else:
            # Legacy --docs-path mode
            results = scan_directory(target_path, recursive=False)
    else:
        results = scan_directory(target_path, recursive=args.recursive)

    if args.json:
        print(format_json(results, str(target)))
        return 0

    print_report(results, str(target))

    # Archive HIGH confidence files
    if args.archive:
        archive_date = args.date or dt_date.today().isoformat()
        archive_dir = target_path / "archive"
        high_done = [r for r in results
                     if r.get("confidence") == "HIGH" and r.get("action") == "archive"]
        if not high_done:
            print("No HIGH-confidence files to archive.")
        else:
            print(f"\nArchiving {len(high_done)} HIGH-confidence files:")
            for r in high_done:
                action = archive_file(Path(r["file"]), archive_dir, archive_date, args.dry_run)
                print(action)
            if not args.dry_run:
                print(f"\nMoved {len(high_done)} files to archive/.")
                print("IMPORTANT: Update README.md index if one exists.")

    # Fix redirects
    if args.fix_redirects:
        redirects = find_redirect_files(base, target_path)
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
