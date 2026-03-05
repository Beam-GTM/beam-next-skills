#!/usr/bin/env python3
"""
Push a filtered copy of this repo to beam-next-raw.

Keeps only system paths (00-system/, root config files). Excludes:
01-skills, 02-memory, 03-projects, 04-apps, 04-workspace, apps,
.claude, .cursor, .github, .sync-backup, 99-helper, 00-system/.cache.

Usage:
    python3 push_to_beam_next_raw.py [--dry-run] [--tag v2.5.3]
    python3 push_to_beam_next_raw.py --repo /path/to/nexus-jbd --tag v2.5.3
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_REMOTE_URL = "https://github.com/Beam-GTM/beam-next-raw.git"
DEFAULT_REMOTE_NAME = "upstream"
DEFAULT_BRANCH = "main"

# Repo slug for gh release create (no .git)
BEAM_NEXT_RAW_REPO = "Beam-GTM/beam-next-raw"

# Paths to remove from history (beam-next-raw = system only, no user content)
PATHS_TO_EXCLUDE = [
    # Current paths
    "01-skills",
    "02-memory",
    "03-projects",
    "04-apps",
    "04-workspace",
    ".claude",
    ".cursor",
    ".github",
    ".sync-backup",
    "99-helper",
    "00-system/.cache",
    # Old/renamed paths (still in git history)
    "01-memory",
    "02-projects",
    "03-skills",
    "apps",
    "beam-next-personas",
    "db-wrapped-public",
    "lead-research.skill",
    "nexus-template-main",
    "wrapped-app-private",
]


def run(cmd, cwd=None, check=True, capture=False, timeout=None, env=None):
    opts = {"cwd": str(cwd) if cwd else None, "text": True, "timeout": timeout}
    if capture:
        opts["capture_output"] = True
    if env is not None:
        opts["env"] = env
    r = subprocess.run(cmd, **opts)
    if check and r.returncode != 0:
        raise RuntimeError(f"Command failed (exit {r.returncode}): {' '.join(cmd)}")
    return r


def get_repo_root(path: Path) -> Path:
    r = run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=path,
        capture=True,
    )
    root = Path(r.stdout.strip())
    if not (root / ".git").exists():
        raise RuntimeError(f"Not a git repository: {root}")
    return root


def extract_changelog_for_tag(repo_root: Path, tag: str) -> str | None:
    """Extract the CHANGELOG section for the given tag (e.g. v2.6.0). Returns None if not found."""
    changelog_path = repo_root / "00-system" / "CHANGELOG.md"
    if not changelog_path.exists():
        return None
    text = changelog_path.read_text(encoding="utf-8")
    # Match ## tag (optional date) — optional title
    tag_escaped = re.escape(tag)
    pattern = rf"^## {tag_escaped}\s*(?:\([^)]*\))?\s*(?:—\s*.*)?$"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line.strip()):
            start = i
            break
    if start is None:
        return None
    # Collect until next ## or --- separator
    out = []
    for i in range(start, len(lines)):
        line = lines[i]
        if i > start and (line.strip() == "---" or (line.startswith("## ") and not line.startswith("## ["))):
            break
        out.append(line)
    return "\n".join(out).strip() if out else None


def main():
    parser = argparse.ArgumentParser(
        description="Push filtered (system-only) history to beam-next-raw"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would be done",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Repo root (default: current dir or git root)",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help=f"Branch to filter and push (default: {DEFAULT_BRANCH})",
    )
    parser.add_argument(
        "--remote-name",
        default=DEFAULT_REMOTE_NAME,
        help=f"Remote name (default: {DEFAULT_REMOTE_NAME})",
    )
    parser.add_argument(
        "--remote-url",
        default=DEFAULT_REMOTE_URL,
        help="Remote URL to push to",
    )
    parser.add_argument(
        "--tag",
        metavar="TAG",
        default=None,
        help="Tag the filtered tip and force-push tag (e.g. v2.5.3)",
    )
    args = parser.parse_args()

    start_dir = Path(args.repo).resolve() if args.repo else Path.cwd()
    try:
        repo_root = get_repo_root(start_dir)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("Dry run — would:")
        print(f"  0. Commit all staged+unstaged changes and push {args.branch} to origin")
        print(f"  1. Use repo root: {repo_root}")
        print(f"  2. Clone to temp dir with --no-hardlinks")
        print(f"  3. filter-branch: exclude {PATHS_TO_EXCLUDE}")
        print(f"  4. Add remote '{args.remote_name}' -> {args.remote_url}")
        print(f"  5. Push {args.branch} -> {args.remote_name}/{args.branch} (force)")
        if args.tag:
            print(f"  6. Tag tip as {args.tag} and force-push tag")
            print(f"  7. Create GitHub Release {args.tag} with notes from 00-system/CHANGELOG.md")
        return 0

    # Step 0: Commit all changes and push to origin/main so the clone is up to date
    print(f"Committing and pushing to origin/{args.branch}...")
    status = run(["git", "status", "--porcelain"], cwd=repo_root, capture=True)
    if status.stdout.strip():
        run(["git", "add", "-A"], cwd=repo_root)
        tag_label = args.tag or "update"
        run(
            ["git", "commit", "-m", f"chore: pre-release commit for {tag_label}"],
            cwd=repo_root, check=False,
        )
    run(
        ["git", "push", "origin", args.branch],
        cwd=repo_root, timeout=60, check=False,
    )

    with tempfile.TemporaryDirectory(prefix="beam-next-raw-push-", ignore_cleanup_errors=True) as tmpdir:
        clone_dir = Path(tmpdir) / "clone"
        print(f"Cloning {repo_root} to temporary directory...")
        run(
            [
                "git", "clone",
                "--no-hardlinks",
                "--branch", args.branch,
                str(repo_root),
                str(clone_dir),
            ],
            timeout=120,
        )

        # Ensure clone is clean; use env that pins git to the clone so filter-branch never sees main repo
        clone_env = dict(os.environ)
        clone_env.pop("GIT_DIR", None)
        clone_env.pop("GIT_WORK_TREE", None)
        clone_env["FILTER_BRANCH_SQUELCH_WARNING"] = "1"
        clone_env["GIT_DIR"] = str(clone_dir / ".git")
        clone_env["GIT_WORK_TREE"] = str(clone_dir)

        run(["git", "reset", "--hard", "HEAD"], cwd=clone_dir, env=clone_env)
        run(["git", "clean", "-fdx"], cwd=clone_dir, env=clone_env)
        # Fix CRLF/eol phantom diffs: renormalize and commit so worktree+index are clean
        run(["git", "add", "--renormalize", "."], cwd=clone_dir, env=clone_env)
        run(["git", "commit", "--allow-empty", "-m", "normalize"],
            cwd=clone_dir, env=clone_env, check=False)

        # filter-branch: remove excluded paths from branch history (main only).
        # Use index-filter (much faster than tree-filter — no checkout needed).
        exclude_args = " ".join(PATHS_TO_EXCLUDE)
        index_filter = f"git rm -rf --cached --ignore-unmatch {exclude_args}"
        print("Filtering history (excluding user content paths)...")
        run(
            [
                "git", "filter-branch",
                "--prune-empty",
                "--index-filter", index_filter,
                "--tag-name-filter", "cat",
                "--", args.branch,
            ],
            cwd=clone_dir,
            timeout=1200,
            env=clone_env,
        )

        # Add remote (ignore if already exists)
        run(
            ["git", "remote", "add", args.remote_name, args.remote_url],
            cwd=clone_dir,
            check=False,
            env=clone_env,
        )
        # If add failed, remote may already exist — continue

        print(f"Pushing {args.branch} to {args.remote_name}...")
        run(
            ["git", "push", args.remote_name, f"{args.branch}:{args.branch}", "--force"],
            cwd=clone_dir,
            timeout=120,
            env=clone_env,
        )

        if args.tag:
            tip = run(
                ["git", "rev-parse", args.branch],
                cwd=clone_dir,
                capture=True,
                env=clone_env,
            ).stdout.strip()
            run(["git", "tag", args.tag, tip, "-f"], cwd=clone_dir, env=clone_env)
            print(f"Pushing tag {args.tag}...")
            run(
                ["git", "push", args.remote_name, args.tag, "--force"],
                cwd=clone_dir,
                timeout=60,
                env=clone_env,
            )

            # Create or update GitHub Release with notes from CHANGELOG
            notes = extract_changelog_for_tag(repo_root, args.tag)
            if notes:
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".md", delete=False, encoding="utf-8"
                ) as f:
                    f.write(notes)
                    notes_file = f.name
                try:
                    print(f"Creating release {args.tag} with notes from CHANGELOG...")
                    run(
                        [
                            "gh", "release", "create", args.tag,
                            "--repo", BEAM_NEXT_RAW_REPO,
                            "--notes-file", notes_file,
                        ],
                        timeout=30,
                    )
                except RuntimeError:
                    # Release may already exist (e.g. re-run); update notes
                    run(
                        [
                            "gh", "release", "edit", args.tag,
                            "--repo", BEAM_NEXT_RAW_REPO,
                            "--notes-file", notes_file,
                        ],
                        timeout=30,
                    )
                finally:
                    os.unlink(notes_file)
            else:
                print(f"No CHANGELOG section for {args.tag}; skipping release notes.", file=sys.stderr)

    print("Done. beam-next-raw updated with system-only history.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)
