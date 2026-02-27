#!/usr/bin/env python3
"""
List all prompts and their versions.

Usage:
    python prompt_list.py [--project <project>] [--json]
"""

import argparse
import json
import sys
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


def list_prompts(prompts_dir: Path, as_json: bool = False) -> dict:
    """List all prompts."""
    config = load_config(prompts_dir)
    if not config:
        print("[ERROR] Prompt versioning not initialized.")
        sys.exit(1)

    if as_json:
        print(json.dumps(config, indent=2, default=str))
        return config

    project = config.get('project', 'Unknown')
    prompts = config.get('prompts', {})

    print(f"\n{'='*60}")
    print(f"  {project} - Prompt Registry")
    print(f"{'='*60}\n")

    if not prompts:
        print("  No prompts found.")
        print("\n  Create one with:")
        print("    python prompt_create.py --name <name> --description \"...\"")
        return config

    print(f"  {'Prompt':<25} {'Current':<10} {'Versions':<10} {'Last Updated':<12}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*12}")

    for name, data in prompts.items():
        current = data.get('current', 'v1')
        versions = data.get('versions', {})
        version_count = len(versions)

        # Get last updated date
        last_date = "N/A"
        if versions:
            dates = [v.get('date', '') for v in versions.values()]
            last_date = max(dates) if dates else "N/A"

        print(f"  {name:<25} {current:<10} {version_count:<10} {last_date:<12}")

    print(f"\n  Total: {len(prompts)} prompt(s)")
    print()

    return config


def main():
    parser = argparse.ArgumentParser(description='List all prompts')
    parser.add_argument('--project', help='Project name (optional)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    prompts_dir = find_prompts_dir(args.project)

    if not prompts_dir or not prompts_dir.exists():
        print("[ERROR] Prompts directory not found.")
        sys.exit(1)

    list_prompts(prompts_dir, args.json)


if __name__ == "__main__":
    main()
