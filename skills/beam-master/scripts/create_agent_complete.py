#!/usr/bin/env python3
"""
Create Agent (Complete Graph)

POST /agent-graphs/complete - Create agent with full graph in one call.

Usage:
    python create_agent_complete.py --name "My Agent" --description "Does X" --graph graph.json
    python create_agent_complete.py --spec beam-agent.yaml
    python create_agent_complete.py --spec beam-agent.yaml --json
"""

import sys
import json
import argparse
from pathlib import Path
from beam_client import get_client


def load_yaml(path):
    """Load YAML file, falling back to JSON."""
    import yaml
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def build_payload_from_spec(spec):
    """Transform beam-agent.yaml spec into API payload."""
    agent = spec.get('agent', {})
    payload = {
        "agentName": agent.get('name', 'Unnamed Agent'),
        "agentDescription": agent.get('description', ''),
        "settings": {
            "prompts": agent.get('prompts', []),
            "agentPersonality": agent.get('personality', ''),
            "agentRestrictions": agent.get('restrictions', ''),
        },
        "nodes": []
    }

    nodes_spec = spec.get('nodes', [])
    for node in nodes_spec:
        tool_cfg = node.get('tool', {})
        input_params = []
        for p in tool_cfg.get('input_params', []):
            input_params.append({
                "fillType": p.get('fill_type', 'ai_fill'),
                "position": p.get('position', 0),
                "required": p.get('required', True),
                "dataType": p.get('type', 'string'),
                "paramName": p['name'],
                "paramDescription": p.get('description', ''),
                "outputExample": p.get('example', ''),
                "staticValue": p.get('static_value', ''),
                "linkedOutputParamNodeId": p.get('linked_node_id', ''),
                "linkedOutputParamName": p.get('linked_param', ''),
            })

        output_params = []
        for p in tool_cfg.get('output_params', []):
            output_params.append({
                "isArray": p.get('is_array', False),
                "paramName": p['name'],
                "position": p.get('position', 0),
                "paramDescription": p.get('description', ''),
                "dataType": p.get('type', 'string'),
                "outputExample": p.get('example', ''),
            })

        child_edges = []
        for e in node.get('edges', []):
            child_edges.append({
                "sourceAgentGraphNodeId": node['id'],
                "targetAgentGraphNodeId": e['target'],
                "condition": e.get('condition', ''),
                "name": e.get('name', ''),
                "isAttachmentDataPulledIn": e.get('pull_attachments', True),
            })

        api_node = {
            "id": node['id'],
            "objective": node.get('objective', ''),
            "evaluationCriteria": node.get('evaluation_criteria', []),
            "isEntryNode": node.get('is_entry', False),
            "isExitNode": node.get('is_exit', False),
            "xCoordinate": node.get('x', 100),
            "yCoordinate": node.get('y', 150 + nodes_spec.index(node) * 200),
            "isEvaluationEnabled": node.get('evaluation_enabled', False),
            "isAttachmentDataPulledIn": node.get('pull_attachments', True),
            "onError": node.get('on_error', 'STOP'),
            "autoRetryCountWhenFailure": node.get('retry_count', 1),
            "autoRetryWaitTimeWhenFailureInMs": node.get('retry_wait_ms', 1000),
            "enableAutoRetryWhenFailure": node.get('auto_retry', False),
            "toolConfiguration": {
                "toolFunctionName": tool_cfg.get('function_name', ''),
                "toolName": tool_cfg.get('name', ''),
                "description": tool_cfg.get('description', ''),
                "requiresConsent": tool_cfg.get('requires_consent', False),
                "isMemoryTool": tool_cfg.get('is_memory_tool', False),
                "preferredModel": tool_cfg.get('model', 'gpt-4o'),
                "prompt": tool_cfg.get('prompt', ''),
                "inputParams": input_params,
                "outputParams": output_params,
            },
            "childEdges": child_edges,
            "parentEdges": [],
        }
        payload["nodes"].append(api_node)

    return payload


def main():
    parser = argparse.ArgumentParser(description='Create agent with complete graph')
    parser.add_argument('--spec', help='Path to beam-agent.yaml spec file')
    parser.add_argument('--graph', help='Path to graph JSON file (raw API format)')
    parser.add_argument('--name', help='Agent name (with --graph)')
    parser.add_argument('--description', help='Agent description (with --graph)')
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
            graph = load_json(args.graph)
            payload = graph
            if args.name:
                payload['agentName'] = args.name
            if args.description:
                payload['agentDescription'] = args.description

        if args.dry_run:
            print(json.dumps(payload, indent=2))
            return

        client = get_client()
        result = client.post('/agent-graphs/complete', data=payload)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\nAgent created successfully!")
            print("=" * 50)
            print(f"Agent ID:       {result.get('agentId', 'N/A')}")
            print(f"Agent Name:     {result.get('agentName', payload.get('agentName', 'N/A'))}")
            print(f"Active Graph:   {result.get('activeGraphId', 'N/A')}")
            print(f"Draft Graph:    {result.get('draftGraphId', 'N/A')}")
            agent_id = result.get('agentId', '')
            if agent_id:
                print(f"\nDashboard:      https://app.beam.ai/agent/{agent_id}")
                print(f"Public URL:     https://app.beam.ai/public/chat/{agent_id}")
            print("\nNext steps:")
            print("  - Configure triggers in the Beam dashboard")
            print("  - Test with: python create_task.py --agent-id <ID> --query 'test'")
            print("  - Monitor:   python get_analytics.py --agent-id <ID>")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
