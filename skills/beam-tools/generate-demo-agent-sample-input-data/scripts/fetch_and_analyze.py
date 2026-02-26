#!/usr/bin/env python3
"""
Fetch and Analyze Beam Agent

Fetches agent graph from Beam API and extracts key information
for generating sample input data.

Usage:
    python fetch_and_analyze.py <workspace_id> <agent_id>
    python fetch_and_analyze.py --url "https://app.beam.ai/workspace/agent"

Output:
    JSON with agent analysis including:
    - Agent metadata
    - Trigger type
    - Input parameters
    - Data sources
    - Decision paths
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] Missing 'requests' library", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory by looking for CLAUDE.md"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file and return dict"""
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


def parse_beam_url(url):
    """
    Parse Beam agent URL to extract workspace_id and agent_id.

    Formats:
        https://app.beam.ai/{workspace_id}/{agent_id}
        https://app.beam.ai/{workspace_id}/{agent_id}/flow
    """
    pattern = r'app\.beam\.ai/([a-f0-9-]+)/([a-f0-9-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def get_access_token(api_key):
    """Get access token from Beam API"""
    resp = requests.post(
        "https://api.beamstudio.ai/auth/access-token",
        headers={"Content-Type": "application/json"},
        json={"apiKey": api_key},
        timeout=30
    )
    if resp.status_code in [200, 201]:
        return resp.json().get("idToken")
    print(f"[ERROR] Auth failed: {resp.status_code} - {resp.text}", file=sys.stderr)
    return None


def fetch_agent_graph(token, workspace_id, agent_id):
    """Fetch agent graph from Beam API"""
    resp = requests.get(
        f"https://api.beamstudio.ai/agent-graphs/{agent_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "current-workspace-id": workspace_id,
            "Content-Type": "application/json"
        },
        timeout=30
    )
    if resp.status_code == 200:
        return resp.json()
    print(f"[ERROR] Fetch failed: {resp.status_code} - {resp.text}", file=sys.stderr)
    return None


def analyze_agent(data):
    """
    Analyze agent graph and extract key information.

    Returns dict with:
    - metadata: Basic agent info
    - trigger_type: How agent is triggered
    - input_params: Expected input parameters
    - data_sources: External data sources used
    - decision_paths: Branching logic
    - tools_used: List of tools in workflow
    """
    graph = data.get("graph", data)
    nodes = graph.get("nodes", [])

    analysis = {
        "metadata": {
            "agent_id": graph.get("agentId"),
            "graph_id": graph.get("id"),
            "is_published": graph.get("isPublished", False),
            "is_active": graph.get("isActive", False),
            "published_at": graph.get("publishedAt"),
            "node_count": len(nodes)
        },
        "trigger_type": "unknown",
        "input_params": [],
        "data_sources": [],
        "decision_paths": [],
        "tools_used": [],
        "workflow_summary": []
    }

    # Analyze each node
    for node in nodes:
        tool_config = node.get("toolConfiguration", {})
        tool_name = tool_config.get("toolName", "")
        objective = node.get("objective", "")

        # Detect trigger type from first node after entry
        if node.get("isEntryNode"):
            analysis["workflow_summary"].append({
                "step": 0,
                "type": "entry",
                "name": "Entry Node",
                "objective": objective
            })
            continue

        # Collect tool info
        if tool_name:
            tool_info = {
                "name": tool_name,
                "objective": objective[:100],
                "node_id": node.get("id", "")[:8]
            }
            analysis["tools_used"].append(tool_info)
            analysis["workflow_summary"].append({
                "step": len(analysis["workflow_summary"]),
                "type": "tool",
                "name": tool_name,
                "objective": objective[:80]
            })

        # Detect trigger type
        if "email" in tool_name.lower() or "gmail" in tool_name.lower():
            if analysis["trigger_type"] == "unknown":
                analysis["trigger_type"] = "email"

        # Extract input parameters from first processing node
        if not analysis["input_params"]:
            inputs = tool_config.get("inputParams", [])
            for param in inputs:
                analysis["input_params"].append({
                    "name": param.get("paramName", ""),
                    "description": param.get("paramDescription", ""),
                    "required": param.get("required", False),
                    "data_type": param.get("dataType", "string"),
                    "fill_type": param.get("fillType", "")
                })

        # Detect data sources
        tool_lower = tool_name.lower()
        if "retrieve all rows" in tool_lower or "google sheets" in tool_lower:
            analysis["data_sources"].append({
                "type": "google_sheets",
                "tool": tool_name,
                "node_id": node.get("id", "")[:8]
            })
        elif "airtable" in tool_lower:
            analysis["data_sources"].append({
                "type": "airtable",
                "tool": tool_name,
                "node_id": node.get("id", "")[:8]
            })
        elif "database" in tool_lower or "sql" in tool_lower:
            analysis["data_sources"].append({
                "type": "database",
                "tool": tool_name,
                "node_id": node.get("id", "")[:8]
            })

        # Detect decision paths (nodes with multiple child edges)
        child_edges = node.get("childEdges", [])
        if len(child_edges) > 1:
            conditions = []
            for edge in child_edges:
                condition = edge.get("condition", "")
                if condition:
                    conditions.append(condition)
            analysis["decision_paths"].append({
                "node_id": node.get("id", "")[:8],
                "tool": tool_name,
                "branches": len(child_edges),
                "conditions": conditions
            })

    # Detect trigger type from tools if still unknown
    if analysis["trigger_type"] == "unknown":
        for tool in analysis["tools_used"]:
            if "email" in tool["name"].lower():
                analysis["trigger_type"] = "email"
                break
            elif "webhook" in tool["name"].lower():
                analysis["trigger_type"] = "webhook"
                break
        else:
            analysis["trigger_type"] = "manual"

    return analysis


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze Beam.ai agent for test data generation"
    )
    parser.add_argument("workspace_id", nargs="?", help="Beam workspace ID")
    parser.add_argument("agent_id", nargs="?", help="Beam agent ID")
    parser.add_argument("--url", help="Full Beam agent URL (alternative to IDs)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", help="Save analysis to file")

    args = parser.parse_args()

    # Get workspace and agent IDs
    if args.url:
        workspace_id, agent_id = parse_beam_url(args.url)
        if not workspace_id:
            print("[ERROR] Could not parse Beam URL", file=sys.stderr)
            sys.exit(1)
    elif args.workspace_id and args.agent_id:
        workspace_id = args.workspace_id
        agent_id = args.agent_id
    else:
        print("[ERROR] Provide workspace_id and agent_id, or --url", file=sys.stderr)
        sys.exit(1)

    # Load API key
    root = find_nexus_root()
    env_vars = load_env_file(root / '.env')
    api_key = env_vars.get('BEAM_API_KEY') or os.getenv('BEAM_API_KEY')

    if not api_key:
        print("[ERROR] BEAM_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Fetching agent: {agent_id}", file=sys.stderr)
    print(f"[INFO] Workspace: {workspace_id}", file=sys.stderr)

    # Get token
    token = get_access_token(api_key)
    if not token:
        sys.exit(1)
    print("[OK] Authenticated", file=sys.stderr)

    # Fetch graph
    data = fetch_agent_graph(token, workspace_id, agent_id)
    if not data:
        sys.exit(1)
    print("[OK] Graph fetched", file=sys.stderr)

    # Analyze
    analysis = analyze_agent(data)
    print("[OK] Analysis complete", file=sys.stderr)

    # Output
    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        print("\n" + "=" * 60)
        print("AGENT ANALYSIS")
        print("=" * 60)

        meta = analysis["metadata"]
        print(f"\nAgent ID: {meta['agent_id']}")
        print(f"Status: {'Published' if meta['is_published'] else 'Draft'}")
        print(f"Nodes: {meta['node_count']}")
        print(f"Trigger Type: {analysis['trigger_type'].upper()}")

        if analysis["input_params"]:
            print(f"\nInput Parameters:")
            for p in analysis["input_params"][:5]:
                req = "*" if p["required"] else ""
                print(f"  - {p['name']}{req}: {p['description'][:50]}")

        if analysis["data_sources"]:
            print(f"\nData Sources:")
            for ds in analysis["data_sources"]:
                print(f"  - {ds['type']}: {ds['tool']}")

        if analysis["decision_paths"]:
            print(f"\nDecision Points: {len(analysis['decision_paths'])}")
            for dp in analysis["decision_paths"]:
                print(f"  - {dp['tool']}: {dp['branches']} branches")

        print(f"\nTools Used ({len(analysis['tools_used'])}):")
        for t in analysis["tools_used"]:
            print(f"  - {t['name']}")

    # Save if requested
    if args.save:
        with open(args.save, 'w') as f:
            json.dump({"raw_graph": data, "analysis": analysis}, f, indent=2)
        print(f"\n[SAVED] {args.save}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
