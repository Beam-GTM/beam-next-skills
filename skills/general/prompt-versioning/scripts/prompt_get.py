#!/usr/bin/env python3
"""
Get prompt content.

Usage:
    python prompt_get.py --name <prompt-name> [--version <vX>] [--raw]
"""

import argparse
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


def get_prompt(prompts_dir: Path, name: str, version: str = None, raw: bool = False) -> str:
    """Get prompt content."""
    config = load_config(prompts_dir)
    if not config:
        print("[ERROR] Prompt versioning not initialized.")
        sys.exit(1)

    if name not in config.get('prompts', {}):
        print(f"[ERROR] Prompt '{name}' not found.")
        print("\nAvailable prompts:")
        for p in config.get('prompts', {}).keys():
            print(f"  - {p}")
        sys.exit(1)

    prompt_data = config['prompts'][name]

    # Use current version if not specified
    if not version:
        version = prompt_data.get('current', 'v1')

    # Check version exists
    if version not in prompt_data.get('versions', {}):
        print(f"[ERROR] Version '{version}' not found for '{name}'.")
        print("\nAvailable versions:")
        for v in prompt_data.get('versions', {}).keys():
            print(f"  - {v}")
        sys.exit(1)

    # Read file
    prompt_file = prompts_dir / name / f"{version}.md"
    if not prompt_file.exists():
        print(f"[ERROR] Prompt file not found: {prompt_file}")
        sys.exit(1)

    with open(prompt_file, 'r') as f:
        content = f.read()

    if raw:
        # Extract just the prompt content (between ``` markers after "## Prompt")
        import re
        match = re.search(r'## Prompt\s+```\s*(.*?)\s*```', content, re.DOTALL)
        if match:
            print(match.group(1).strip())
        else:
            print(content)
    else:
        version_info = prompt_data['versions'].get(version, {})
        is_current = version == prompt_data.get('current')

        print(f"\n{'='*60}")
        print(f"  {name} - {version}" + (" [CURRENT]" if is_current else ""))
        print(f"{'='*60}")
        print(f"  Date: {version_info.get('date', 'N/A')}")
        print(f"  Ticket: {version_info.get('ticket') or 'N/A'}")
        print(f"  Change: {version_info.get('change', 'N/A')}")
        print(f"{'='*60}\n")
        print(content)

    return content


def main():
    parser = argparse.ArgumentParser(description='Get prompt content')
    parser.add_argument('--name', required=True, help='Prompt name')
    parser.add_argument('--version', help='Version (default: current)')
    parser.add_argument('--project', help='Project name (optional)')
    parser.add_argument('--raw', action='store_true', help='Output only the raw prompt content')
    args = parser.parse_args()

    prompts_dir = find_prompts_dir(args.project)

    if not prompts_dir or not prompts_dir.exists():
        print("[ERROR] Prompts directory not found.")
        sys.exit(1)

    get_prompt(prompts_dir, args.name, args.version, args.raw)


if __name__ == "__main__":
    main()
