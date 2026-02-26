#!/usr/bin/env python3.13
"""
Push Beam Agent Graph

Pushes a cleaned graph payload to PUT /agent-graphs/{agentId}.
Supports dry-run mode, save-and-publish, and automatic verification.

Usage:
    # Dry run — validate and show what would be pushed
    python push_graph.py --agent-id ID --payload-file payload.json --dry-run

    # Push as draft
    python push_graph.py --agent-id ID --payload-file payload.json

    # Push and publish immediately
    python push_graph.py --agent-id ID --payload-file payload.json --save-and-publish

    # Clean a raw GET response before pushing
    python push_graph.py --agent-id ID --payload-file raw_get.json --clean
"""

import sys
import json
import argparse
from pathlib import Path

# Add beam-master scripts to path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
BEAM_SCRIPTS = PROJECT_ROOT / '00-system' / 'skills' / 'beam' / 'beam-master' / 'scripts'
sys.path.insert(0, str(BEAM_SCRIPTS))

from beam_client import get_client
from beam_graph_utils import prepare_graph_for_put, summarize_graph


def main():
    parser = argparse.ArgumentParser(description='Push cleaned graph payload to Beam API')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--payload-file', help='Path to JSON file with graph payload')
    parser.add_argument('--payload-data', help='Inline JSON graph payload')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate and show summary without pushing')
    parser.add_argument('--save-and-publish', action='store_true',
                        help='Publish graph immediately after saving')
    parser.add_argument('--clean', action='store_true',
                        help='Run prepare_graph_for_put on payload before pushing')
    parser.add_argument('--no-verify', action='store_true',
                        help='Skip post-push verification')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        # Load payload
        if args.payload_file:
            with open(args.payload_file, 'r') as f:
                payload = json.load(f)
        elif args.payload_data:
            payload = json.loads(args.payload_data)
        else:
            print("Error: Either --payload-file or --payload-data is required",
                  file=sys.stderr)
            sys.exit(1)

        # Optionally clean the payload
        if args.clean:
            payload = prepare_graph_for_put(payload)

        # Validate structure
        if 'nodes' not in payload:
            print("Error: Payload must have a 'nodes' key", file=sys.stderr)
            sys.exit(1)

        nodes = payload['nodes']
        node_count = len(nodes)

        # Validate isArray on all output params
        issues = []
        for i, node in enumerate(nodes):
            tc = node.get('toolConfiguration', {})
            for op in tc.get('outputParams', []):
                if 'isArray' not in op:
                    issues.append(
                        f"Node {i} ({tc.get('toolFunctionName', '?')}): "
                        f"outputParam '{op.get('paramName', '?')}' missing isArray"
                    )

        if issues and not args.dry_run:
            print("WARNING: Payload validation issues:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            print("Fix these before pushing, or use --clean to auto-fix.",
                  file=sys.stderr)
            sys.exit(1)

        # Dry run
        if args.dry_run:
            summary = summarize_graph(nodes)
            result = {
                "mode": "dry_run",
                "agent_id": args.agent_id,
                "node_count": node_count,
                "would_publish": args.save_and_publish,
                "validation_issues": issues,
                "nodes": summary,
            }
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n=== DRY RUN ===")
                print(f"Agent ID: {args.agent_id}")
                print(f"Nodes: {node_count}")
                print(f"Would publish: {args.save_and_publish}")
                if issues:
                    print(f"Issues: {len(issues)}")
                    for issue in issues:
                        print(f"  - {issue}")
                print(f"\nNode summary:")
                for s in summary:
                    print(f"  {s['index']:2d}. {s['objective'][:60]}")
                    print(f"      tool: {s['toolFunctionName']}")
                    print(f"      params: {s['input_count']} in / {s['output_count']} out")
                print(f"\n=== No changes pushed (dry run) ===")
            return

        # Push
        params = {}
        if args.save_and_publish:
            params['saveAndPublish'] = 'true'

        if not args.json:
            print(f"Pushing to PUT /agent-graphs/{args.agent_id}...")

        result = client.put(
            f'/agent-graphs/{args.agent_id}',
            data=payload,
            params=params if params else None,
        )

        push_result = {
            "status": "success",
            "agent_id": args.agent_id,
            "published": args.save_and_publish,
            "node_count": node_count,
        }

        if not args.json:
            print(f"SUCCESS! Graph updated.")
            print(f"  Agent: {args.agent_id}")
            print(f"  Nodes pushed: {node_count}")
            print(f"  Published: {'Yes' if args.save_and_publish else 'No (draft)'}")

        # Verify
        if not args.no_verify:
            if not args.json:
                print(f"\nVerifying...")

            verify_response = client.get(f'/agent-graphs/{args.agent_id}')
            verify_graph = verify_response.get('graph', verify_response)
            verify_nodes = verify_graph.get('nodes', [])

            push_result['verification'] = {
                "node_count_after": len(verify_nodes),
                "match": len(verify_nodes) == node_count,
            }

            if not args.json:
                if len(verify_nodes) == node_count:
                    print(f"  Verified: {len(verify_nodes)} nodes (matches)")
                else:
                    print(f"  WARNING: Expected {node_count} nodes, "
                          f"found {len(verify_nodes)}")

                if not args.save_and_publish:
                    print(f"\n  NOTE: Graph saved as draft. Open Beam UI to "
                          f"re-link any LINKED inputs if needed.")

        if args.json:
            print(json.dumps(push_result, indent=2))

    except json.JSONDecodeError as e:
        error = f"Invalid JSON: {e}"
        if args.json:
            print(json.dumps({"error": error}))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError:
        error = f"File not found: {args.payload_file}"
        if args.json:
            print(json.dumps({"error": error}))
        else:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
