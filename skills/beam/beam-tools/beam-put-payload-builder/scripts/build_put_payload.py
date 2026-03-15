#!/usr/bin/env python3
"""
Build a Swagger-DTO-compliant PUT payload from a Beam API GET graph response.

Handles the critical GET→PUT field mapping differences:
  - Prompt: originalTool.prompt → toolConfiguration.prompt
  - Model: originalTool.preferredModel → toolConfiguration.preferredModel
  - Links: linkParamOutputId (UUID) → linkedOutputParamNodeId + linkedOutputParamName
  - Edges: extracted from node-level childEdges/parentEdges (graph.edges is always empty)
  - Strips computed/server-only fields

Usage:
  # Fetch graph from API and build PUT payload:
  python3 build_put_payload.py --agent-id <UUID> --dry-run

  # Build from a saved GET response JSON file:
  python3 build_put_payload.py --from-file graph.json --output put_payload.json

  # Build and send PUT:
  python3 build_put_payload.py --agent-id <UUID>

  # Build, send PUT, and publish:
  python3 build_put_payload.py --agent-id <UUID> --publish
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def load_env():
    """Load API credentials from .env file."""
    env = {}
    env_paths = ['.env', os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')]
    for p in env_paths:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            break
    return env


def api_request(method, url, headers, body=None):
    """Make an HTTP request and return parsed JSON."""
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ''
        print(f"API Error {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)


def get_graph(agent_id, api_key, workspace_id, base_url):
    """Fetch complete agent graph via GET."""
    url = f"{base_url}/agent-graphs/{agent_id}"
    headers = {
        'x-api-key': api_key,
        'current-workspace-id': workspace_id,
        'Content-Type': 'application/json',
    }
    return api_request('GET', url, headers)


def put_graph(agent_id, payload, api_key, workspace_id, base_url):
    """Send PUT to update agent graph."""
    url = f"{base_url}/agent-graphs/{agent_id}"
    headers = {
        'x-api-key': api_key,
        'current-workspace-id': workspace_id,
        'Content-Type': 'application/json',
    }
    return api_request('PUT', url, headers, payload)


def publish_graph(graph_id, api_key, workspace_id, base_url):
    """Publish draft graph via PATCH."""
    url = f"{base_url}/agent-graphs/{graph_id}/publish"
    headers = {
        'x-api-key': api_key,
        'current-workspace-id': workspace_id,
        'Content-Type': 'application/json',
    }
    return api_request('PATCH', url, headers)


# ---------------------------------------------------------------------------
# Link translation: linkParamOutputId (UUID) → name-based linking
# ---------------------------------------------------------------------------

def build_output_param_lookup(nodes):
    """
    Build a reverse lookup: output param UUID → (node_id, param_name).

    Scans both toolConfiguration.outputParams and originalTool.outputParams
    for each node, mapping each output param's 'id' to the node's 'id' and
    the param's 'paramName'.
    """
    lookup = {}
    for node in nodes:
        node_id = node.get('id', '')
        tc = node.get('toolConfiguration') or {}

        # Check toolConfiguration.outputParams
        for p in tc.get('outputParams', []):
            pid = p.get('id')
            if pid:
                lookup[pid] = (node_id, p.get('paramName', ''))

        # Check originalTool.outputParams (may have different/additional params)
        ot = tc.get('originalTool') or {}
        for p in ot.get('outputParams', []):
            pid = p.get('id')
            if pid and pid not in lookup:
                lookup[pid] = (node_id, p.get('paramName', ''))

    return lookup


def translate_link(param, lookup):
    """
    Translate a linked input param from UUID-based to name-based linking.

    GET format:  { "fillType": "linked", "linkParamOutputId": "<uuid>" }
    PUT format:  { "fillType": "linked", "linkedOutputParamNodeId": "<node-uuid>",
                   "linkedOutputParamName": "<param-name>" }
    """
    link_id = param.get('linkParamOutputId')
    if not link_id:
        return None, None

    if link_id in lookup:
        node_id, param_name = lookup[link_id]
        return node_id, param_name

    # Fallback: check linkOutputParam object (sometimes present in GET)
    link_obj = param.get('linkOutputParam') or {}
    if link_obj.get('paramName'):
        # We need to find which node owns this output param
        return None, link_obj.get('paramName')

    return None, None


# ---------------------------------------------------------------------------
# Payload builders (Swagger DTO compliant)
# ---------------------------------------------------------------------------

def build_input_param(p, lookup):
    """Build AgentGraphNodeToolConfigurationInputParamDto."""
    result = {
        'fillType': p.get('fillType', 'ai_fill'),
        'position': p.get('position', 0),
        'required': p.get('required', False),
        'dataType': p.get('dataType', 'string'),
        'reloadProps': p.get('reloadProps', False),
        'remoteOptions': p.get('remoteOptions', False),
        'paramName': p.get('paramName', ''),
        'paramDescription': p.get('paramDescription', ''),
    }

    # Handle linked params: translate UUID → name-based
    if p.get('fillType') == 'linked':
        node_id, param_name = translate_link(p, lookup)
        if node_id and param_name:
            result['linkedOutputParamNodeId'] = node_id
            result['linkedOutputParamName'] = param_name
        elif p.get('linkedOutputParamNodeId') and p.get('linkedOutputParamName'):
            # Already has name-based linking (rare but possible)
            result['linkedOutputParamNodeId'] = p['linkedOutputParamNodeId']
            result['linkedOutputParamName'] = p['linkedOutputParamName']
        else:
            print(f"  WARNING: Could not translate link for param '{p.get('paramName')}' "
                  f"(linkParamOutputId={p.get('linkParamOutputId')})", file=sys.stderr)

    # Optional fields
    if p.get('staticValue'):
        result['staticValue'] = p['staticValue']
    if p.get('outputExample'):
        result['outputExample'] = p['outputExample']
    if p.get('question'):
        result['question'] = p['question']
    if p.get('isArray'):
        result['isArray'] = p['isArray']

    return result


def build_output_param(p):
    """Build AgentGraphNodeToolConfigurationOutputParamDto."""
    result = {
        'isArray': p.get('isArray', False),
        'paramName': p.get('paramName', ''),
        'position': p.get('position', 0),
        'paramDescription': p.get('paramDescription', ''),
        'dataType': p.get('dataType', 'string'),
    }
    if p.get('outputExample'):
        result['outputExample'] = p['outputExample']
    return result


def build_edge(e):
    """Build CompleteAgentGraphEdgeDto."""
    return {
        'sourceAgentGraphNodeId': e.get('sourceAgentGraphNodeId', ''),
        'targetAgentGraphNodeId': e.get('targetAgentGraphNodeId', ''),
        'condition': e.get('condition', ''),
        'isAttachmentDataPulledIn': e.get('isAttachmentDataPulledIn', False),
    }


def build_tool_config(tc, lookup):
    """Build CompleteAgentGraphNodeToolConfigurationDto."""
    ot = tc.get('originalTool') or {}

    # Prompt: GET stores in originalTool.prompt, PUT expects toolConfiguration.prompt
    prompt = ot.get('prompt', '') or tc.get('prompt', '') or ''

    # Model: GET stores in originalTool.preferredModel, PUT expects toolConfiguration.preferredModel
    model = ot.get('preferredModel') or tc.get('preferredModel')

    # Input/output params: read from toolConfiguration (has linkParamOutputId for link translation
    # and includes params added via PUT that may not have propagated to originalTool due to B3 bug)
    input_params = tc.get('inputParams', [])
    output_params = tc.get('outputParams', [])

    config = {
        'toolFunctionName': tc.get('toolFunctionName') or ot.get('toolFunctionName', ''),
        'toolName': tc.get('toolName') or ot.get('toolName', ''),
        'description': ot.get('description') or tc.get('description', '') or '',
        'requiresConsent': ot.get('requiresConsent', False),
        'isMemoryTool': ot.get('isMemoryTool', False),
        'memoryLookupInstruction': ot.get('memoryLookupInstruction', '') or '',
        'isBackgroundTool': ot.get('isBackgroundTool', False),
        'isBatchExecutionEnabled': ot.get('isBatchExecutionEnabled', False),
        'isCodeExecutionEnabled': ot.get('isCodeExecutionEnabled', False),
        'inputParams': [build_input_param(p, lookup) for p in input_params],
        'outputParams': [build_output_param(p) for p in output_params],
        'prompt': prompt,
    }

    if model:
        config['preferredModel'] = model

    return config


def build_node(n, lookup):
    """Build CompleteAgentGraphNodeDto."""
    tc = n.get('toolConfiguration') or {}

    node = {
        'id': n['id'],
        'objective': n.get('objective', '') or '',
        'evaluationCriteria': n.get('evaluationCriteria') or [],
        'isEntryNode': n.get('isEntryNode', False),
        'isExitNode': n.get('isExitNode', False),
        'xCoordinate': n.get('xCoordinate', 0),
        'yCoordinate': n.get('yCoordinate', 0),
        'isEvaluationEnabled': n.get('isEvaluationEnabled', False),
        'isAttachmentDataPulledIn': n.get('isAttachmentDataPulledIn', True),
        'onError': n.get('onError', 'STOP') or 'STOP',
        'autoRetryWhenAccuracyLessThan': n.get('autoRetryWhenAccuracyLessThan', 80),
        'autoRetryLimitWhenAccuracyIsLow': n.get('autoRetryLimitWhenAccuracyIsLow', 1),
        'autoRetryCountWhenFailure': n.get('autoRetryCountWhenFailure', 1),
        'autoRetryWaitTimeWhenFailureInMs': n.get('autoRetryWaitTimeWhenFailureInMs', 1000),
        'enableAutoRetryWhenAccuracyIsLow': n.get('enableAutoRetryWhenAccuracyIsLow', False),
        'enableAutoRetryWhenFailure': n.get('enableAutoRetryWhenFailure', False),
        'childEdges': [build_edge(e) for e in n.get('childEdges', [])],
        'parentEdges': [build_edge(e) for e in n.get('parentEdges', [])],
    }

    # Only add toolConfiguration for nodes that have a tool
    ot = tc.get('originalTool') or {}
    if tc.get('toolFunctionName') or ot.get('toolFunctionName'):
        node['toolConfiguration'] = build_tool_config(tc, lookup)

    return node


def build_put_payload(get_response):
    """
    Transform a GET /agent-graphs/{agentId} response into a valid
    PUT /agent-graphs/{agentId} request body.

    Returns (payload_dict, stats_dict).
    """
    graph = get_response.get('graph', get_response)
    nodes_raw = graph.get('nodes', [])
    # Agent name: try top-level 'agentName' first (from saved payloads),
    # then 'graph.agent.name' (from GET response)
    agent_name = (get_response.get('agentName')
                  or graph.get('agent', {}).get('name')
                  or '')

    # Step 1: Build output param UUID → (node_id, param_name) lookup
    lookup = build_output_param_lookup(nodes_raw)

    # Step 2: Build Swagger-compliant payload
    payload = {
        'agentName': agent_name,
        'nodes': [build_node(n, lookup) for n in nodes_raw],
    }

    # Optional: include agentDescription if present
    if get_response.get('agentDescription'):
        payload['agentDescription'] = get_response['agentDescription']

    # Step 3: Collect stats
    total_links = 0
    translated_links = 0
    untranslated_links = 0
    for node in payload['nodes']:
        tc = node.get('toolConfiguration', {})
        for p in tc.get('inputParams', []):
            if p.get('fillType') == 'linked':
                total_links += 1
                if p.get('linkedOutputParamNodeId') and p.get('linkedOutputParamName'):
                    translated_links += 1
                else:
                    untranslated_links += 1

    stats = {
        'node_count': len(payload['nodes']),
        'lookup_entries': len(lookup),
        'total_links': total_links,
        'translated_links': translated_links,
        'untranslated_links': untranslated_links,
        'payload_chars': len(json.dumps(payload)),
    }

    return payload, stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_summary(payload, stats):
    """Print a human-readable summary of the built payload."""
    print(f"\nPayload: {stats['payload_chars']:,} chars, {stats['node_count']} nodes")
    print(f"Output param lookup: {stats['lookup_entries']} entries")
    print(f"Links: {stats['translated_links']}/{stats['total_links']} translated"
          + (f", {stats['untranslated_links']} FAILED" if stats['untranslated_links'] else ""))
    print()

    for n in payload['nodes']:
        tc = n.get('toolConfiguration', {})
        name = tc.get('toolName', 'NO_TOOL')
        prompt_len = len(tc.get('prompt', '') or '')
        model = tc.get('preferredModel', 'default')
        n_in = len(tc.get('inputParams', []))
        n_out = len(tc.get('outputParams', []))
        linked = sum(1 for p in tc.get('inputParams', [])
                     if p.get('fillType') == 'linked' and p.get('linkedOutputParamNodeId'))
        entry = ' [ENTRY]' if n.get('isEntryNode') else ''
        exit_flag = ' [EXIT]' if n.get('isExitNode') else ''
        print(f"  {name}: prompt={prompt_len}c, model={model}, "
              f"in={n_in}, out={n_out}, linked={linked}{entry}{exit_flag}")


def main():
    parser = argparse.ArgumentParser(
        description='Build Swagger-DTO-compliant PUT payload from Beam GET graph response')
    parser.add_argument('--agent-id', help='Agent UUID (fetches graph from API)')
    parser.add_argument('--from-file', help='Path to saved GET response JSON')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout summary + /tmp/beam_put_payload.json)')
    parser.add_argument('--dry-run', action='store_true', help='Build and display payload without sending PUT')
    parser.add_argument('--publish', action='store_true', help='Publish graph after successful PUT')
    parser.add_argument('--base-url', default='https://api.enterprise.beamstudio.ai',
                        help='Beam API base URL')
    args = parser.parse_args()

    if not args.agent_id and not args.from_file:
        parser.error('Either --agent-id or --from-file is required')

    # Load credentials
    env = load_env()
    api_key = env.get('BEAM_API_KEY', '')
    workspace_id = env.get('BEAM_WORKSPACE_ID', '')

    # Get graph data
    if args.from_file:
        with open(args.from_file) as f:
            get_response = json.load(f)
        print(f"Loaded graph from {args.from_file}")
    else:
        if not api_key or not workspace_id:
            print("Error: BEAM_API_KEY and BEAM_WORKSPACE_ID required in .env", file=sys.stderr)
            sys.exit(1)
        print(f"Fetching graph for agent {args.agent_id}...")
        get_response = get_graph(args.agent_id, api_key, workspace_id, args.base_url)
        print("Graph fetched successfully.")

    # Build payload
    payload, stats = build_put_payload(get_response)
    print_summary(payload, stats)

    if stats['untranslated_links'] > 0:
        print(f"\nWARNING: {stats['untranslated_links']} links could not be translated!")
        print("These params will lose their links after PUT.")
        if not args.dry_run:
            print("Use --dry-run first to inspect, or fix the source graph.")
            sys.exit(1)

    # Save payload
    output_path = args.output or '/tmp/beam_put_payload.json'
    with open(output_path, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"\nPayload saved to {output_path}")

    if args.dry_run:
        print("\n[DRY RUN] No API calls made.")
        return

    # Send PUT
    agent_id = args.agent_id
    if not agent_id:
        # Try to extract from the GET response
        agent_id = get_response.get('agentId') or get_response.get('id')
    if not agent_id:
        print("Error: --agent-id required for PUT", file=sys.stderr)
        sys.exit(1)

    print(f"\nSending PUT to /agent-graphs/{agent_id}...")
    result = put_graph(agent_id, payload, api_key, workspace_id, args.base_url)
    print("PUT successful.")

    # Publish if requested
    if args.publish:
        graph_id = result.get('graph', {}).get('id') or result.get('id')
        if not graph_id:
            print("Warning: Could not extract graph ID from PUT response for publishing.",
                  file=sys.stderr)
        else:
            print(f"\nPublishing graph {graph_id}...")
            publish_graph(graph_id, api_key, workspace_id, args.base_url)
            print("Graph published successfully.")


if __name__ == '__main__':
    main()
