#!/usr/bin/env python3
"""
Fetch Beam.ai agent graph via API

Usage:
    python get_agent_graph.py <workspace_id> <agent_id> [--output <path>]

Example:
    python get_agent_graph.py 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 162e7c30-0d95-49ab-af99-7eef872a2d0d
    python get_agent_graph.py 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 162e7c30-0d95-49ab-af99-7eef872a2d0d --output ./graphs
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] Missing 'requests' library")
    print("Install with: pip install requests")
    sys.exit(1)


def load_env_file(env_path):
    """Load .env file and return dict of environment variables"""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def find_nexus_root():
    """Find Nexus root directory by looking for CLAUDE.md"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def get_access_token(api_key):
    """
    Step 1: Get access token from Beam API

    Args:
        api_key: Beam API key

    Returns:
        Access token string or None on error
    """
    url = "https://api.beamstudio.ai/auth/access-token"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token") or data.get("accessToken")
        else:
            print(f"[ERROR] Failed to get access token: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def get_agent_graph(access_token, workspace_id, agent_id):
    """
    Step 2: Get agent graph from Beam API

    Args:
        access_token: Access token from step 1
        workspace_id: Beam workspace ID
        agent_id: Agent ID to fetch

    Returns:
        Agent graph JSON dict or None on error
    """
    url = f"https://api.beamstudio.ai/agent-graphs/{agent_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-workspace-id": workspace_id,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed to get agent graph: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def save_graph(graph_data, agent_id, output_dir):
    """
    Save agent graph to JSON file

    Args:
        graph_data: Agent graph JSON data
        agent_id: Agent ID for filename
        output_dir: Directory to save the file

    Returns:
        Path to saved file or None on error
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Try to extract agent name from graph data
    agent_name = None
    if isinstance(graph_data, dict):
        agent_name = (
            graph_data.get("name") or
            graph_data.get("agentName") or
            graph_data.get("agent_name")
        )

    # Create meaningful filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if agent_name:
        # Sanitize agent name for filename
        safe_name = "".join(c for c in agent_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}_{agent_id[:8]}_graph_{timestamp}.json"
    else:
        filename = f"{agent_id}_graph_{timestamp}.json"

    file_path = output_path / filename

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        return file_path
    except Exception as e:
        print(f"[ERROR] Failed to save file: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Fetch Beam.ai agent graph and save to JSON file",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("workspace_id", help="Beam workspace ID")
    parser.add_argument("agent_id", help="Agent ID to fetch")
    parser.add_argument("--output", default="04-workspace/beam-graphs",
                       help="Output directory (default: 04-workspace/beam-graphs)")

    args = parser.parse_args()

    # Find Nexus root and load .env
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API key from .env or environment
    api_key = env_vars.get('BEAM_API_KEY') or os.getenv('BEAM_API_KEY')

    if not api_key:
        print("[ERROR] BEAM_API_KEY not found in .env or environment", file=sys.stderr)
        print("Add to .env: BEAM_API_KEY=your-key-here", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Fetching agent graph...", file=sys.stderr)
    print(f"  Workspace: {args.workspace_id}", file=sys.stderr)
    print(f"  Agent ID: {args.agent_id}", file=sys.stderr)

    # Step 1: Get access token
    print("[1/3] Getting access token...", file=sys.stderr)
    access_token = get_access_token(api_key)

    if not access_token:
        sys.exit(1)

    print("[OK] Access token obtained", file=sys.stderr)

    # Step 2: Get agent graph
    print("[2/3] Fetching agent graph...", file=sys.stderr)
    graph_data = get_agent_graph(access_token, args.workspace_id, args.agent_id)

    if not graph_data:
        sys.exit(1)

    print("[OK] Agent graph fetched", file=sys.stderr)

    # Step 3: Save to file
    print("[3/3] Saving to file...", file=sys.stderr)
    file_path = save_graph(graph_data, args.agent_id, args.output)

    if not file_path:
        sys.exit(1)

    print(f"\n[SUCCESS] Agent graph saved to: {file_path}", file=sys.stderr)

    # Output JSON for programmatic use
    print(json.dumps({
        "file_path": str(file_path),
        "agent_id": args.agent_id,
        "workspace_id": args.workspace_id
    }, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
