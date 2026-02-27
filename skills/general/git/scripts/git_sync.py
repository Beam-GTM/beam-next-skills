#!/usr/bin/env python3
"""
Git Sync Script - Safely sync Nexus from upstream

Usage:
    git_sync.py [--check-only] [--show-protected]

Options:
    --check-only      Only show what would change, don't sync
    --show-protected  Show protected folders configuration

This script:
1. Fetches from upstream
2. Shows changes (warns about protected folders)
3. Returns status for AI to present to user
"""

import subprocess
import sys
import json
from pathlib import Path

# Protected folders that should NEVER be overwritten
PROTECTED_FOLDERS = [
    "01-memory/",
    "02-projects/",
    "03-skills/",
    "04-workspace/",
    "05-archived/",
    ".env",
]

# Files to merge carefully
CAREFUL_FILES = [
    "CLAUDE.md",
    "01-memory/user-config.yaml",
]

# Safe to sync
SAFE_FOLDERS = [
    "00-system/",
]

UPSTREAM_URL = "git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git"
UPSTREAM_NAME = "upstream"


def run_git(args, capture=True):
    """Run a git command and return output."""
    cmd = ["git"] + args
    try:
        if capture:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        return None


def check_upstream_configured():
    """Check if upstream remote is configured."""
    remotes = run_git(["remote", "-v"])
    if remotes and UPSTREAM_NAME in remotes:
        return True
    return False


def configure_upstream():
    """Configure upstream remote."""
    run_git(["remote", "add", UPSTREAM_NAME, UPSTREAM_URL])
    return check_upstream_configured()


def get_current_branch():
    """Get current branch name."""
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"])


def fetch_upstream():
    """Fetch from upstream."""
    result = run_git(["fetch", UPSTREAM_NAME])
    return result is not None or result == ""


def get_changed_files():
    """Get list of files that would change on merge."""
    branch = get_current_branch()
    output = run_git(["diff", "--name-only", f"HEAD..{UPSTREAM_NAME}/{branch}"])
    if output:
        return output.split("\n")
    return []


def categorize_changes(changed_files):
    """Categorize changed files by protection level."""
    protected = []
    careful = []
    safe = []

    for f in changed_files:
        is_protected = any(f.startswith(p.rstrip('/')) or f == p.rstrip('/') for p in PROTECTED_FOLDERS)
        is_careful = f in CAREFUL_FILES
        is_safe = any(f.startswith(p.rstrip('/')) for p in SAFE_FOLDERS)

        if is_protected:
            protected.append(f)
        elif is_careful:
            careful.append(f)
        elif is_safe:
            safe.append(f)
        else:
            # Unknown files - treat as careful
            careful.append(f)

    return {
        "protected": protected,
        "careful": careful,
        "safe": safe
    }


def check_conflicts():
    """Check if there are merge conflicts."""
    output = run_git(["diff", "--name-only", "--diff-filter=U"])
    if output:
        return output.split("\n")
    return []


def get_status():
    """Get current git status."""
    return {
        "branch": get_current_branch(),
        "upstream_configured": check_upstream_configured(),
        "has_uncommitted": bool(run_git(["status", "--porcelain"])),
        "conflicts": check_conflicts()
    }


def main():
    args = sys.argv[1:]

    if "--show-protected" in args:
        print(json.dumps({
            "protected_folders": PROTECTED_FOLDERS,
            "careful_files": CAREFUL_FILES,
            "safe_folders": SAFE_FOLDERS,
            "upstream_url": UPSTREAM_URL
        }, indent=2))
        return

    # Get current status
    status = get_status()

    # Configure upstream if needed
    if not status["upstream_configured"]:
        print(json.dumps({
            "status": "upstream_not_configured",
            "message": f"Upstream remote not configured. Will add: {UPSTREAM_URL}",
            "action_needed": "configure_upstream"
        }, indent=2))

        if "--check-only" not in args:
            if configure_upstream():
                print(json.dumps({"status": "upstream_configured", "url": UPSTREAM_URL}, indent=2))
            else:
                print(json.dumps({"status": "error", "message": "Failed to configure upstream"}, indent=2))
                sys.exit(1)
        return

    # Check for uncommitted changes
    if status["has_uncommitted"]:
        print(json.dumps({
            "status": "uncommitted_changes",
            "message": "You have uncommitted changes. Commit or stash them first.",
            "action_needed": "commit_or_stash"
        }, indent=2))
        return

    # Fetch upstream
    print(json.dumps({"status": "fetching", "message": "Fetching from upstream..."}), file=sys.stderr)
    if not fetch_upstream():
        print(json.dumps({
            "status": "error",
            "message": "Failed to fetch from upstream"
        }, indent=2))
        sys.exit(1)

    # Get changed files
    changed_files = get_changed_files()

    if not changed_files:
        print(json.dumps({
            "status": "up_to_date",
            "message": "Already up to date with upstream."
        }, indent=2))
        return

    # Categorize changes
    categories = categorize_changes(changed_files)

    # Build result
    result = {
        "status": "changes_available",
        "branch": status["branch"],
        "total_changes": len(changed_files),
        "categories": categories,
        "warnings": []
    }

    if categories["protected"]:
        result["warnings"].append({
            "level": "critical",
            "message": f"PROTECTED folders would be modified: {len(categories['protected'])} files",
            "files": categories["protected"],
            "recommendation": "DO NOT sync these - they contain your user data"
        })

    if categories["careful"]:
        result["warnings"].append({
            "level": "warning",
            "message": f"Files requiring careful review: {len(categories['careful'])} files",
            "files": categories["careful"],
            "recommendation": "Review changes before accepting"
        })

    if categories["safe"]:
        result["safe_to_sync"] = {
            "count": len(categories["safe"]),
            "files": categories["safe"],
            "recommendation": "Safe to sync - system updates"
        }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
