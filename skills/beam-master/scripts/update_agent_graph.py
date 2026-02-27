#!/usr/bin/env python3
"""
Update Agent Graph

PUT /agent-graphs/complete - Update agent and replace draft graph.

Usage:
    python update_agent_graph.py --agent-id AGENT --spec beam-agent.yaml
    python update_agent_graph.py --agent-id AGENT --graph graph.json
    python update_agent_graph.py --agent-id AGENT --graph graph.json --publish
"""

import sys
import json
import argparse
from pathlib import Path
from beam_client import get_client
from create_agent_complete import build_payload_from_spec, load_yaml, load_json


def main():
    parser = argparse.ArgumentParser(description='Update agent and its draft graph')
    parser.add_argument('--agent-id', required=True, help='Agent ID to update')
    parser.add_argument('--spec', help='Path to beam-agent.yaml spec file')
    parser.add_argument('--graph', help='Path to graph JSON file (raw API format)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--dry-run', action='store_true', help='Show payload without sending')
    args = parser.parse_args()

    if not args.spec and not args.graph:
        parser.error("Either --spec or --graph is required")

    try:
        if args.spec:
            spec_path = Path(args.spec)
            if spec_path.suffix in ('.yaml', '.yml'):
                spec = load_yaml(spec_path)
            else:
                spec = load_json(spec_path)
            payload = build_payload_from_spec(spec)
        else:
            payload = load_json(args.graph)

        if args.dry_run:
            print(json.dumps(payload, indent=2))
            return

        client = get_client()
        result = client.put(f'/agent-graphs/complete/{args.agent_id}', data=payload)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\nAgent updated successfully!")
            print("=" * 50)
            print(f"Agent ID:     {args.agent_id}")
            print(f"Draft graph updated. Review in Beam dashboard before publishing.")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
