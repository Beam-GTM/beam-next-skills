#!/usr/bin/env python3
"""
Compare two versions of a prompt.

Usage:
    python prompt_diff.py --name <prompt-name> --v1 <version> --v2 <version>
"""

import argparse
import sys
import difflib
from pathlib import Path

import yaml


def find_prompts_dir(project_name: str = None) -> Path:
    """Find the prompts directory."""
    script_dir = Path(__file__).parent
    nexus_root = script_dir.parent.parent.parent.parent

    if project_name:
        projects_dir = nexus_root / "02-projects"
        for folder in projects_dir.iterdir():
            if folder.is_dir() and project_name.lower() in folder.name.lower():
                return folder / "02-resources" / "prompts"

    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        prompts_dir = parent / "02-resources" / "prompts"
        if prompts_dir.exists():
            return prompts_dir

    return None


def load_config(prompts_dir: Path) -> dict:
    """Load the prompt config."""
    config_file = prompts_dir / ".prompt-config.yaml"
    if not config_file.exists():
        return None
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def diff_prompts(prompts_dir: Path, name: str, v1: str, v2: str, context_lines: int = 3) -> str:
    """Compare two versions of a prompt."""
    config = load_config(prompts_dir)
    if not config:
        print("[ERROR] Prompt versioning not initialized.")
        sys.exit(1)

    if name not in config.get('prompts', {}):
        print(f"[ERROR] Prompt '{name}' not found.")
        sys.exit(1)

    prompt_data = config['prompts'][name]
    versions = prompt_data.get('versions', {})

    # Check versions exist
    for v in [v1, v2]:
        if v not in versions:
            print(f"[ERROR] Version '{v}' not found for '{name}'.")
            print("\nAvailable versions:")
            for ver in versions.keys():
                print(f"  - {ver}")
            sys.exit(1)

    # Read files
    file1 = prompts_dir / name / f"{v1}.md"
    file2 = prompts_dir / name / f"{v2}.md"

    if not file1.exists():
        print(f"[ERROR] File not found: {file1}")
        sys.exit(1)
    if not file2.exists():
        print(f"[ERROR] File not found: {file2}")
        sys.exit(1)

    with open(file1, 'r') as f:
        content1 = f.readlines()
    with open(file2, 'r') as f:
        content2 = f.readlines()

    # Generate diff
    diff = difflib.unified_diff(
        content1,
        content2,
        fromfile=f"{name}/{v1}.md",
        tofile=f"{name}/{v2}.md",
        n=context_lines
    )

    diff_text = ''.join(diff)

    if not diff_text:
        print(f"\n[INFO] No differences between {v1} and {v2}")
        return ""

    # Print version info
    v1_info = versions.get(v1, {})
    v2_info = versions.get(v2, {})

    print(f"\n{'='*60}")
    print(f"  Comparing {name}: {v1} → {v2}")
    print(f"{'='*60}")
    print(f"\n  {v1}:")
    print(f"    Date: {v1_info.get('date', 'N/A')}")
    print(f"    Ticket: {v1_info.get('ticket') or 'N/A'}")
    print(f"    Change: {v1_info.get('change', 'N/A')}")
    print(f"\n  {v2}:")
    print(f"    Date: {v2_info.get('date', 'N/A')}")
    print(f"    Ticket: {v2_info.get('ticket') or 'N/A'}")
    print(f"    Change: {v2_info.get('change', 'N/A')}")
    print(f"\n{'='*60}")
    print("\nDiff (- = removed, + = added):\n")

    # Colorize output if terminal supports it
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m")  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m")  # Red
        elif line.startswith('@'):
            print(f"\033[94m{line}\033[0m")  # Blue
        else:
            print(line)

    return diff_text


def main():
    parser = argparse.ArgumentParser(description='Compare two versions of a prompt')
    parser.add_argument('--name', required=True, help='Prompt name')
    parser.add_argument('--v1', required=True, help='First version (e.g., v1)')
    parser.add_argument('--v2', required=True, help='Second version (e.g., v2)')
    parser.add_argument('--project', help='Project name (optional)')
    parser.add_argument('--context', type=int, default=3, help='Context lines (default: 3)')
    args = parser.parse_args()

    prompts_dir = find_prompts_dir(args.project)

    if not prompts_dir or not prompts_dir.exists():
        print("[ERROR] Prompts directory not found.")
        sys.exit(1)

    diff_prompts(prompts_dir, args.name, args.v1, args.v2, args.context)


if __name__ == "__main__":
    main()
