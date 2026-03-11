#!/usr/bin/env python3
"""
create_agent_from_prompt.py

Accepts a node spec as JSON and deploys it via POST /agent-graphs/complete (draft).

The spec JSON is generated externally (e.g. by the Claude Code skill) and passed
to this script — no LLM is invoked here.

Usage:
    # Pipe spec JSON from stdin
    echo '{...}' | python3 scripts/create_agent_from_prompt.py

    # Read spec from a file
    python3 scripts/create_agent_from_prompt.py --spec-file my-spec.json

    # Dry run — print full Beam payload without calling API
    python3 scripts/create_agent_from_prompt.py --spec-file my-spec.json --dry-run

Auth (set in .env or environment):
    BEAM_API_KEY, BEAM_WORKSPACE_ID

Spec format:
{
  "agentName": "string",
  "agentDescription": "string",
  "personality": "string",
  "restrictions": "string",
  "prompts": ["example prompt 1", ...],
  "nodes": [
    {
      "key": "unique-snake-case-key",
      "name": "Human readable name",
      "objective": "What this node does",
      "is_entry": false,
      "x": 250, "y": 150,
      "model": "BEDROCK_CLAUDE_SONNET_4",
      "tool_name": "Tool display name",
      "tool_description": "One-line description",
      "prompt": "Full LLM instruction prompt",
      "on_error": "STOP",
      "enable_retry": false,
      "retry_count": 1,
      "retry_wait_ms": 1000,
      "fallback_models": null,
      "evaluation_criteria": [],
      "input_params": [
        {
          "name": "param_name",
          "description": "...",
          "type": "string|object|number|boolean",
          "is_array": false,
          "fill_type": "user_fill|static|linked|ai_fill",
          "static_value": null,
          "linked_node": null,
          "linked_param": null,
          "output_example": null,
          "required": true,
          "position": 0
        }
      ],
      "output_params": [
        {
          "name": "param_name",
          "description": "...",
          "type": "string|object|number|boolean",
          "is_array": false,
          "output_example": null,
          "position": 0
        }
      ],
      "edges": [
        {"target": "next-node-key", "name": "Edge label", "condition": ""}
      ]
    }
  ]
}
"""

import os
import re
import sys
import json
import uuid
import argparse
import requests
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_FILE     = PROJECT_ROOT / ".env"
BASE_URL     = "http://localhost:4000"


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip("\"'")
    return env


def to_camel(name: str) -> str:
    """'Sum Calculator' → 'SumCalculator'"""
    return re.sub(r"[^a-zA-Z0-9]", " ", name).title().replace(" ", "")


def tool_function_name(tool_name: str) -> str:
    """'Sum Calculator' → 'GPTAction_Custom_SumCalculator'"""
    return f"GPTAction_Custom_{to_camel(tool_name)}"


# ── UUID helpers ───────────────────────────────────────────────────────────────
def g(): return str(uuid.uuid4())


# ── Build Beam API payload from spec ──────────────────────────────────────────
def build_payload(spec: dict) -> dict:
    nodes_spec = spec["nodes"]
    node_keys  = [n["key"] for n in nodes_spec]

    NODE = {k: g() for k in node_keys}
    TC   = {k: g() for k in node_keys}

    # Pre-generate output param UUIDs: "node_key.param_name" → UUID
    OP = {}
    for ns in nodes_spec:
        for op in ns.get("output_params", []):
            OP[f"{ns['key']}.{op['name']}"] = g()

    # Pre-build edge objects keyed by "src→tgt"
    EDGES = {}
    for ns in nodes_spec:
        for e in ns.get("edges", []):
            k = f"{ns['key']}→{e['target']}"
            EDGES[k] = {
                "sourceAgentGraphNodeId": NODE[ns["key"]],
                "targetAgentGraphNodeId": NODE[e["target"]],
                "condition": e.get("condition", ""),
                "name": e.get("name", ""),
                "isAttachmentDataPulledIn": True,
            }

    def child_edges(src):
        return [v for k, v in EDGES.items() if k.startswith(f"{src}→")]

    def parent_edges(tgt):
        return [v for k, v in EDGES.items() if k.endswith(f"→{tgt}")]

    def build_input_param(ip):
        ft = ip["fill_type"]
        base = {
            "position":          ip["position"],
            "paramName":         ip["name"],
            "paramDescription":  ip["description"],
            "fillType":          ft,
            "required":          ip.get("required", True),
            "dataType":          ip["type"],
            "isArray":           ip.get("is_array", False),
            "outputExample":     ip.get("output_example", None),
            "reloadProps":       False,
            "remoteOptions":     False,
            "question":          None,
            "options":           None,
            "paramTip":          None,
            "staticValue":       None,
            "linkParamOutputId": None,
        }
        if ft == "static":
            base["staticValue"] = ip.get("static_value", "")
        elif ft == "linked":
            op_key = f"{ip['linked_node']}.{ip['linked_param']}"
            if op_key not in OP:
                raise ValueError(
                    f"Linked param '{op_key}' not found in output params.\n"
                    f"Available: {list(OP.keys())}"
                )
            base["linkParamOutputId"] = OP[op_key]
        return base

    def build_output_param(op, node_key):
        return {
            "id":                       OP[f"{node_key}.{op['name']}"],
            "position":                 op["position"],
            "paramName":                op["name"],
            "paramDescription":         op["description"],
            "dataType":                 op["type"],
            "isArray":                  op.get("is_array", False),
            "outputExample":            op.get("output_example", None),
            "agentToolConfigurationId": TC[node_key],
            "parentId":                 None,
            "paramPath":                None,
            "typeOptions":              None,
        }

    def build_original_tool(ns):
        fn = tool_function_name(ns.get("tool_name", ns["name"]))
        return {
            "toolName":               ns.get("tool_name", ns["name"]),
            "toolFunctionName":       fn,
            "iconSrc":                None,
            "type":                   "custom_gpt_tool",
            "prompt":                 ns.get("prompt", ""),
            "description":            ns.get("tool_description", ""),
            "preferredModel":         ns.get("model", None),
            "meta": {
                "type":            "custom_gpt_tool",
                "prompt":          ns.get("prompt", ""),
                "content":         ns.get("tool_description", ""),
                "icon_src":        None,
                "tool_name":       ns.get("tool_name", ns["name"]),
                "description":     ns.get("tool_description", ""),
                "function_name":   fn,
                "preferred_model": ns.get("model", None),
            },
            "integrationId":          None,
            "isIntegrationRequired":  False,
            "isIntegrationConnected": False,
            "inputParams": [
                {
                    "dataType":         ip["type"],
                    "fillType":         ip["fill_type"],
                    "position":         ip["position"],
                    "required":         ip.get("required", True),
                    "paramName":        ip["name"],
                    "reloadProps":      False,
                    "outputExample":    ip.get("output_example", None),
                    "remoteOptions":    False,
                    "paramDescription": ip["description"],
                    "isArray":          ip.get("is_array", False),
                    "staticValue":      ip.get("static_value", None),
                    "linkParamOutputId": (
                        OP.get(f"{ip['linked_node']}.{ip['linked_param']}")
                        if ip["fill_type"] == "linked" else None
                    ),
                    "options":  None,
                    "paramTip": None,
                }
                for ip in ns.get("input_params", [])
            ],
            "outputParams": [
                {
                    "id":              OP[f"{ns['key']}.{op['name']}"],
                    "isArray":         op.get("is_array", False),
                    "dataType":        op["type"],
                    "position":        op["position"],
                    "paramName":       op["name"],
                    "outputExample":   op.get("output_example", None),
                    "paramDescription": op["description"],
                    "typeOptions":     None,
                }
                for op in ns.get("output_params", [])
            ],
        }

    def build_tool_config(ns):
        fn = tool_function_name(ns.get("tool_name", ns["name"]))
        return {
            "id":               TC[ns["key"]],
            "toolFunctionName": fn,
            "toolName":         ns.get("tool_name", ns["name"]),
            "iconSrc":          None,
            "description":      ns.get("tool_description", ""),
            "prompt":           ns.get("prompt", ""),
            "preferredModel":   ns.get("model", "BEDROCK_CLAUDE_SONNET_4"),
            "fallbackModels":   ns.get("fallback_models", None),
            "accuracyScore":    None,
            "requiresConsent":  False,
            "isMemoryTool":     False,
            "memoryLookupInstruction": "",
            "isBackgroundTool":        False,
            "isBatchExecutionEnabled": False,
            "isCodeExecutionEnabled":  False,
            "isAvailableToWorkspace":  False,
            "dynamicPropsId":          None,
            "integrationProviderId":   None,
            "inputParams":  [build_input_param(ip) for ip in ns.get("input_params", [])],
            "outputParams": [build_output_param(op, ns["key"]) for op in ns.get("output_params", [])],
            "originalTool": build_original_tool(ns),
        }

    def build_node(ns):
        is_entry = ns.get("is_entry", False)
        criteria = ns.get("evaluation_criteria", [])
        node = {
            "id":               NODE[ns["key"]],
            "objective":        ns["objective"],
            "evaluationCriteria": criteria,
            "isEntryNode":      is_entry,
            "isExitNode":       ns.get("is_exit", False),
            "xCoordinate":      ns.get("x", 250),
            "yCoordinate":      ns.get("y", 150),
            "isEvaluationEnabled":      bool(criteria),
            "isAttachmentDataPulledIn": True,
            "onError":          ns.get("on_error", "STOP"),
            "enableAutoRetryWhenFailure": ns.get("enable_retry", False),
            "autoRetryCountWhenFailure":  ns.get("retry_count", 1),
            "autoRetryWaitTimeWhenFailureInMs": ns.get("retry_wait_ms", 1000),
            "autoRetryWhenAccuracyLessThan":    80,
            "autoRetryLimitWhenAccuracyIsLow":  1,
            "enableAutoRetryWhenAccuracyIsLow": False,
            "autoRetryDescription":      None,
            "enableAutoRetryDescription": False,
            "isEdited":         False,
            "childEdges":  child_edges(ns["key"]),
            "parentEdges": parent_edges(ns["key"]),
        }
        # Entry nodes are always bare — no toolConfiguration
        if not is_entry:
            node["toolConfiguration"] = build_tool_config(ns)
        return node

    return {
        "agentName":        spec["agentName"],
        "agentDescription": spec.get("agentDescription", ""),
        "settings": {
            "prompts":           spec.get("prompts", []),
            "agentPersonality":  spec.get("personality", ""),
            "agentRestrictions": spec.get("restrictions", ""),
        },
        "nodes": [build_node(ns) for ns in nodes_spec],
    }


# ── API call ───────────────────────────────────────────────────────────────────
def create_agent(payload: dict, api_key: str, workspace_id: str) -> dict:
    headers = {
        "x-api-key":            api_key,
        "current-workspace-id": workspace_id,
        "Content-Type":         "application/json",
    }
    resp = requests.post(
        f"{BASE_URL}/agent-graphs/complete",
        headers=headers,
        json=payload,
        timeout=60,
    )
    if resp.status_code in (200, 201):
        return resp.json()
    print(f"API Error {resp.status_code}:", file=sys.stderr)
    print(resp.text, file=sys.stderr)
    sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Deploy a Beam agent from a JSON spec via POST /agent-graphs/complete"
    )
    parser.add_argument("--spec-file", help="Path to JSON spec file (default: read from stdin)")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without calling API")
    args = parser.parse_args()

    env          = load_env()
    beam_api_key = env.get("BEAM_API_KEY")     or os.getenv("BEAM_API_KEY")
    workspace_id = env.get("BEAM_WORKSPACE_ID") or os.getenv("BEAM_WORKSPACE_ID")

    if not beam_api_key:
        sys.exit("ERROR: BEAM_API_KEY not set in .env or environment")
    if not workspace_id:
        sys.exit("ERROR: BEAM_WORKSPACE_ID not set in .env or environment")

    # Read spec
    if args.spec_file:
        raw = Path(args.spec_file).read_text()
    else:
        if sys.stdin.isatty():
            print("Paste spec JSON then press Ctrl+D:")
        raw = sys.stdin.read()

    if not raw.strip():
        sys.exit("ERROR: No spec provided")

    spec = json.loads(raw)

    # Build payload
    payload = build_payload(spec)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        print(f"\n=== DRY RUN — {len(payload['nodes'])} nodes, no API call ===", file=sys.stderr)
        return

    # Summary
    print(f"Creating: {payload['agentName']}  ({len(payload['nodes'])} nodes)")
    for n in payload["nodes"]:
        tc     = n.get("toolConfiguration") or {}
        role   = "ENTRY" if n["isEntryNode"] else tc.get("toolName", "?")
        ins    = len(tc.get("inputParams", []))
        outs   = len(tc.get("outputParams", []))
        linked = [p["paramName"] for p in tc.get("inputParams", []) if p.get("fillType") == "linked"]
        print(f"  [{role:35s}]  {ins} in / {outs} out"
              + (f"  linked={linked}" if linked else ""))

    result = create_agent(payload, beam_api_key, workspace_id)
    print("\nAgent created!")
    print(f"  Agent ID:    {result.get('agentId')}")
    print(f"  Agent Name:  {result.get('agentName')}")
    print(f"  Draft Graph: {result.get('draftGraphId')}")
    print(f"  Active Graph:{result.get('activeGraphId')}")


if __name__ == "__main__":
    main()
