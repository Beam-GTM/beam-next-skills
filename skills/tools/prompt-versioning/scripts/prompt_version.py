#!/usr/bin/env python3
"""
Create a new version of an existing prompt.

Usage:
    python prompt_version.py --name <prompt-name> --ticket <LINEAR-ID> --change "description"
"""

import argparse
import os
import sys
import shutil
from datetime import datetime
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


def save_config(prompts_dir: Path, config: dict):
    """Save the prompt config."""
    config_file = prompts_dir / ".prompt-config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def regenerate_registry(prompts_dir: Path, config: dict):
    """Regenerate the REGISTRY.md file."""
    from prompt_create import regenerate_registry as regen
    regen(prompts_dir, config)


def create_version(prompts_dir: Path, name: str, ticket: str, change: str, set_current: bool = False) -> str:
    """Create a new version of a prompt."""
    config = load_config(prompts_dir)
    if not config:
        print("[ERROR] Prompt versioning not initialized.")
        sys.exit(1)

    if name not in config.get('prompts', {}):
        print(f"[ERROR] Prompt '{name}' not found. Use prompt_create.py first.")
        sys.exit(1)

    prompt_data = config['prompts'][name]
    versions = prompt_data.get('versions', {})

    # Determine new version number
    version_nums = [int(v.replace('v', '')) for v in versions.keys() if v.startswith('v')]
    new_version_num = max(version_nums) + 1 if version_nums else 1
    new_version = f"v{new_version_num}"

    # Get current version to copy from
    current_version = prompt_data.get('current', 'v1')
    prompt_dir = prompts_dir / name

    current_file = prompt_dir / f"{current_version}.md"
    new_file = prompt_dir / f"{new_version}.md"

    if not current_file.exists():
        print(f"[ERROR] Current version file not found: {current_file}")
        sys.exit(1)

    # Copy current to new
    shutil.copy(current_file, new_file)

    # Update the header in new file
    today = datetime.now().strftime('%Y-%m-%d')
    with open(new_file, 'r') as f:
        content = f.read()

    # Update version info in header
    content = content.replace(f"**Version**: {current_version}", f"**Version**: {new_version}")
    content = content.replace(f"**Created**: ", f"**Created**: {today}\n> **Previous**: ")
    content = content.replace("**Ticket**: -", f"**Ticket**: {ticket or '-'}")
    content = content.replace("**Ticket**: None", f"**Ticket**: {ticket or '-'}")
    content = content.replace("**Change**: Initial version", f"**Change**: {change}")

    # If there was a previous ticket, update it
    import re
    content = re.sub(r'\*\*Ticket\*\*: [^\n]+', f'**Ticket**: {ticket or "-"}', content, count=1)
    content = re.sub(r'\*\*Change\*\*: [^\n]+', f'**Change**: {change}', content, count=1)
    content = re.sub(r'\*\*Version\*\*: v\d+', f'**Version**: {new_version}', content, count=1)

    with open(new_file, 'w') as f:
        f.write(content)

    # Update config
    prompt_data['versions'][new_version] = {
        'date': today,
        'ticket': ticket,
        'change': change
    }

    if set_current:
        prompt_data['current'] = new_version

    save_config(prompts_dir, config)

    # Regenerate registry
    try:
        regenerate_registry(prompts_dir, config)
    except:
        # Fallback: inline regeneration
        pass

    return new_version


def main():
    parser = argparse.ArgumentParser(description='Create a new version of a prompt')
    parser.add_argument('--name', required=True, help='Prompt name')
    parser.add_argument('--ticket', help='Linear ticket ID (e.g., CLI-4442)')
    parser.add_argument('--change', required=True, help='Description of changes')
    parser.add_argument('--project', help='Project name (optional)')
    parser.add_argument('--set-current', action='store_true', help='Set as current production version')
    args = parser.parse_args()

    prompts_dir = find_prompts_dir(args.project)

    if not prompts_dir or not prompts_dir.exists():
        print("[ERROR] Prompts directory not found.")
        sys.exit(1)

    print(f"[INFO] Creating new version of '{args.name}'")

    new_version = create_version(
        prompts_dir,
        args.name,
        args.ticket,
        args.change,
        args.set_current
    )

    print(f"\n[SUCCESS] Created {new_version}")
    print(f"   File: {prompts_dir / args.name / f'{new_version}.md'}")

    if args.set_current:
        print(f"   Set as current: Yes")
    else:
        print(f"\nTo set as production:")
        print(f"   python prompt_set_current.py --name {args.name} --version {new_version}")


if __name__ == "__main__":
    main()
