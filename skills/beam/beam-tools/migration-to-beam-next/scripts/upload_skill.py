#!/usr/bin/env python3
"""
Upload a .skill file to Beam AI via the import skill API.

Fetches the user's workspaces on the fly, lets the user pick one,
then uploads the skill to that workspace's agent.

Usage:
    python scripts/upload_skill.py <path-to-skill-file>
    python scripts/upload_skill.py <path-to-skill-file> --dry-run
    python scripts/upload_skill.py <path-to-skill-file> --base-url https://api.beamstudio.ai

Requires BEAM_API_KEY in .env file.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] 'requests' package required. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] 'python-dotenv' package required. Install with: pip install python-dotenv")
    sys.exit(1)

DEFAULT_BASE_URL = "https://api.beamstudio.ai"


def find_env_file():
    """Walk up from cwd to find .env file."""
    current = Path.cwd()
    while current != current.parent:
        env_path = current / ".env"
        if env_path.exists():
            return env_path
        current = current.parent
    return None


def fetch_workspaces(api_key: str, base_url: str):
    """Fetch current user's workspaces via GET /v2/user/me."""
    url = f"{base_url}/v2/user/me"
    headers = {"x-api-key": api_key}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch user info — HTTP {resp.status_code}")
        try:
            print(f"   Response: {resp.json()}")
        except Exception:
            print(f"   Response: {resp.text[:500]}")
        return None

    data = resp.json()
    workspaces = data.get("workspaces", [])
    if not workspaces:
        print("[ERROR] No workspaces found for this user.")
        return None

    return workspaces


def prompt_workspace_selection(workspaces: list) -> dict:
    """Display workspaces and let user pick one."""
    print("\n[SELECT] Available workspaces:\n")
    for i, ws in enumerate(workspaces, 1):
        agent = ws.get("agent", {})
        agent_name = agent.get("name", "N/A") if agent else "N/A"
        print(f"  {i}. {ws.get('name', 'Unnamed')} (agent: {agent_name})")

    print()
    while True:
        try:
            choice = input(f"Select workspace [1-{len(workspaces)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(workspaces):
                return workspaces[idx]
            print(f"  Please enter a number between 1 and {len(workspaces)}")
        except (ValueError, EOFError):
            print(f"  Please enter a number between 1 and {len(workspaces)}")
        except KeyboardInterrupt:
            print("\n[ABORT] Cancelled.")
            sys.exit(1)


def upload_skill(skill_file: str, base_url: str = DEFAULT_BASE_URL, dry_run: bool = False):
    """Fetch workspaces, let user pick, then upload the .skill file."""
    skill_path = Path(skill_file)

    if not skill_path.exists():
        print(f"[ERROR] File not found: {skill_path}")
        return False

    if skill_path.suffix != ".skill":
        print(f"[WARN] File does not have .skill extension: {skill_path.name}")

    env_file = find_env_file()
    if env_file:
        load_dotenv(env_file)

    api_key = os.getenv("BEAM_API_KEY")
    if not api_key:
        print("[ERROR] BEAM_API_KEY must be set in .env")
        return False

    # Fetch workspaces
    print("[FETCH] Getting workspaces...")
    workspaces = fetch_workspaces(api_key, base_url)
    if not workspaces:
        return False

    # Let user select
    workspace = prompt_workspace_selection(workspaces)
    workspace_id = workspace.get("id")
    agent = workspace.get("agent", {})
    agent_id = agent.get("id") if agent else None

    if not workspace_id or not agent_id:
        print("[ERROR] Selected workspace is missing id or agent.")
        return False

    print(f"\n[OK] Selected: {workspace.get('name')}")
    print(f"   Workspace ID: {workspace_id}")
    print(f"   Agent ID:     {agent_id}")

    # Upload
    url = f"{base_url}/agent/{agent_id}/skills/import"
    headers = {
        "x-api-key": api_key,
        "current-workspace-id": workspace_id,
    }

    print(f"\n[UPLOAD] Importing skill to agent {agent_id}")
    print(f"   File: {skill_path.name} ({skill_path.stat().st_size} bytes)")
    print(f"   URL:  {url}")

    if dry_run:
        print("[DRY RUN] Would upload — skipping actual API call.")
        return True

    with open(skill_path, "rb") as f:
        files = {"file": (skill_path.name, f, "application/zip")}
        resp = requests.post(url, headers=headers, files=files)

    if resp.status_code == 201:
        data = resp.json()
        print(f"[OK] Skill imported successfully.")
        print(f"   Destination: {data.get('destination', 'N/A')}")
        return True
    else:
        print(f"[ERROR] Import failed — HTTP {resp.status_code}")
        try:
            print(f"   Response: {resp.json()}")
        except Exception:
            print(f"   Response: {resp.text[:500]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload a .skill file to Beam AI")
    parser.add_argument("skill_file", help="Path to the .skill file")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"API base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--dry-run", action="store_true", help="Print request details without calling API")
    args = parser.parse_args()

    success = upload_skill(args.skill_file, args.base_url, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
