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
      "node_type": "executionNode|conditionNode|loopingNode",
      "parent_node": null,
      "x": 250, "y": 150,
      "model": "BEDROCK_CLAUDE_SONNET_4",
      "tool_name": "Tool display name",
      "tool_description": "One-line description",
      "prompt": "Full LLM instruction prompt",
      "code": null,
      "code_language": null,
      "integration_provider_id": null,
      "on_error": "STOP",
      "enable_retry": false,
      "retry_count": 1,
      "retry_wait_ms": 1000,
      "fallback_models": null,
      "evaluation_criteria": [],
      "loop_config": {
        "iteration_count": 3,
        "linked_variable_node": null,
        "linked_variable_param": null,
        "alias": "item"
      },
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

Loop nodes:
  - Set "node_type": "loopingNode". No toolConfiguration.
  - Must have at least one child (another spec node with "parent_node": "<loop-key>").
  - "loop_config.iteration_count" for count-based loops.
  - "loop_config.linked_variable_node" + "linked_variable_param" for variable-based loops.
"""

import os
import re
import sys
import json
import copy
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
def _resolve_node_type(ns: dict) -> str:
    nt = ns.get("node_type")
    if nt:
        return nt
    if ns.get("is_entry"):
        return "entryNode"
    if ns.get("is_exit"):
        return "exitNode"
    return "executionNode"


def _validate_loops(nodes_spec: list) -> None:
    """Every loopingNode must have at least one child. No nested loops allowed."""
    loop_keys = {ns["key"] for ns in nodes_spec if _resolve_node_type(ns) == "loopingNode"}
    children_by_parent = {}
    for ns in nodes_spec:
        parent = ns.get("parent_node")
        if parent:
            children_by_parent.setdefault(parent, []).append(ns["key"])
    for lk in loop_keys:
        if not children_by_parent.get(lk):
            raise ValueError(
                f"Loop node '{lk}' has no children. A loopingNode must have at least one "
                f"child node (set \"parent_node\": \"{lk}\" on the inner nodes)."
            )
    for ns in nodes_spec:
        parent = ns.get("parent_node")
        if parent and parent not in loop_keys:
            raise ValueError(
                f"Node '{ns['key']}' has parent_node='{parent}', but '{parent}' is not a "
                f"loopingNode in the spec."
            )
        # No nested loops
        if _resolve_node_type(ns) == "loopingNode" and parent:
            raise ValueError(
                f"Loop node '{ns['key']}' has parent_node='{parent}'. Nested loops are "
                f"not supported — a loop cannot live inside another loop."
            )
        # No waiting nodes inside a loop
        if _resolve_node_type(ns) == "waitingNode" and parent:
            raise ValueError(
                f"Waiting node '{ns['key']}' has parent_node='{parent}'. Waiting nodes "
                f"are not allowed inside a loop."
            )


def _compute_loop_metadata(nodes_spec: list) -> tuple:
    """Derive auto-assigned loop objectives and child aliases from spec order.

    Returns (loop_objectives, child_aliases):
      - loop_objectives: {loop_key: "N: Loop"} — 1-based, by spec order of loops
      - child_aliases:   {child_key: "N"}      — 1-based, per-loop, by spec order
    """
    loop_objectives = {}
    child_aliases = {}
    loop_idx = 0
    children_counter = {}
    for ns in nodes_spec:
        if _resolve_node_type(ns) == "loopingNode":
            loop_idx += 1
            loop_objectives[ns["key"]] = f"{loop_idx}: Loop"
        parent = ns.get("parent_node")
        if parent:
            children_counter[parent] = children_counter.get(parent, 0) + 1
            child_aliases[ns["key"]] = str(children_counter[parent])
    return loop_objectives, child_aliases


def build_payload(spec: dict) -> dict:
    nodes_spec = spec["nodes"]
    node_keys  = [n["key"] for n in nodes_spec]

    _validate_loops(nodes_spec)
    loop_objectives, child_aliases = _compute_loop_metadata(nodes_spec)

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
            edge = {
                "sourceAgentGraphNodeId": NODE[ns["key"]],
                "targetAgentGraphNodeId": NODE[e["target"]],
                "condition": e.get("condition", ""),
                "name": e.get("name", ""),
                "isAttachmentDataPulledIn": True,
            }
            # Support conditionGroups for rule-based conditions
            if "condition_groups" in e:
                edge["conditionGroups"] = e["condition_groups"]
            EDGES[k] = edge

    def child_edges(src):
        return [v for k, v in EDGES.items() if k.startswith(f"{src}→")]

    def parent_edges(tgt):
        return [v for k, v in EDGES.items() if k.endswith(f"→{tgt}")]

    def build_input_param(ip):
        ft = ip.get("fill_type", "user_fill")
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
                    "fillType":         ip.get("fill_type", "user_fill"),
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
                        if ip.get("fill_type") == "linked" else None
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
            "code":             ns.get("code"),
            "codeLanguage":     ns.get("code_language"),
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
            "integrationProviderId":   ns.get("integration_provider_id"),
            "inputParams":  [build_input_param(ip) for ip in ns.get("input_params", [])],
            "outputParams": [build_output_param(op, ns["key"]) for op in ns.get("output_params", [])],
            "originalTool": build_original_tool(ns),
        }

    def build_wait_config(ns):
        """Build nodeConfigurations for a waitingNode from spec wait_config."""
        wc = ns.get("wait_config", {}) or {}
        cfg = {"waitType": wc.get("wait_type", "time_based")}
        if cfg["waitType"] == "time_based":
            cfg["timeToWaitValue"] = wc.get("time_to_wait_value", 5)
            cfg["timeToWaitUnit"]  = wc.get("time_to_wait_unit", "minutes")
        else:  # condition_based
            if wc.get("linked_node"):
                cfg["linkedAgentGraphNodeId"] = NODE[wc["linked_node"]]
            if wc.get("rule") is not None:
                cfg["rule"] = wc["rule"]
            if wc.get("conditions"):
                cfg["conditions"] = wc["conditions"]
        cfg["timeoutType"] = wc.get("timeout_type", "no_timeout")
        if cfg["timeoutType"] == "set_timeout":
            cfg["timeoutValue"] = wc.get("timeout_value")
            cfg["timeoutUnit"]  = wc.get("timeout_unit", "minutes")
            cfg["onTimeout"]    = wc.get("on_timeout", "continue")
        return cfg

    def build_loop_config(ns):
        """Build nodeConfigurations for a loopingNode from spec loop_config.

        Loop itself does NOT carry an alias; aliases are assigned to child nodes.
        """
        lc = ns.get("loop_config", {}) or {}
        cfg = {}
        if lc.get("iteration_count") is not None:
            cfg["iterationCount"] = lc["iteration_count"]
        if lc.get("linked_variable_node") and lc.get("linked_variable_param"):
            op_key = f"{lc['linked_variable_node']}.{lc['linked_variable_param']}"
            if op_key not in OP:
                raise ValueError(
                    f"Loop '{ns['key']}' linked_variable '{op_key}' not found in output params.\n"
                    f"Available: {list(OP.keys())}"
                )
            cfg["linkedVariableId"]       = OP[op_key]
            cfg["linkedAgentGraphNodeId"] = NODE[lc["linked_variable_node"]]
        return cfg

    def build_node(ns):
        is_entry = ns.get("is_entry", False)
        is_exit  = ns.get("is_exit", False)
        node_type = _resolve_node_type(ns)
        criteria = ns.get("evaluation_criteria", [])

        # Loops have auto-assigned objective "N: Loop"
        objective = (
            loop_objectives[ns["key"]]
            if node_type == "loopingNode"
            else ns["objective"]
        )

        node = {
            "id":               NODE[ns["key"]],
            "objective":        objective,
            "evaluationCriteria": criteria,
            "isEntryNode":      is_entry,
            "isExitNode":       is_exit,
            "nodeType":         node_type,
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

        # parentNodeId — set when this node lives inside a loop
        parent_key = ns.get("parent_node")
        if parent_key:
            node["parentNodeId"] = NODE[parent_key]

        # nodeConfigurations — required for conditionNode
        if node_type == "conditionNode":
            node["nodeConfigurations"] = ns.get("node_configurations", {
                "conditionType": "llm_based",
                "llmModel": "GPT40",
                "fallbackModels": None,
            })

        # loopingNode config (iteration / linked variable — no alias on the loop itself)
        if node_type == "loopingNode":
            node["nodeConfigurations"] = build_loop_config(ns)

        # waitingNode config
        if node_type == "waitingNode":
            node["nodeConfigurations"] = build_wait_config(ns)

        # Auto-assigned numeric alias on child-of-loop nodes
        if parent_key:
            cfg = node.get("nodeConfigurations")
            if cfg is None:
                cfg = {}
                node["nodeConfigurations"] = cfg
            cfg["alias"] = child_aliases[ns["key"]]

        # toolConfiguration: only for executionNode (not entry/exit/condition/loop)
        if node_type == "executionNode":
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


# ── Merge-update: GET existing graph then overlay spec changes ─────────────────
def get_agent_graph(agent_id: str, api_key: str, workspace_id: str) -> dict:
    headers = {"x-api-key": api_key, "current-workspace-id": workspace_id}
    resp = requests.get(f"{BASE_URL}/agent-graphs/{agent_id}", headers=headers, timeout=30)
    if resp.status_code == 200:
        return resp.json()
    print(f"GET Error {resp.status_code}: {resp.text}", file=sys.stderr)
    sys.exit(1)


def build_payload_update(spec: dict, existing_graph_resp: dict) -> dict:
    """
    Build PUT payload by merging spec onto the existing graph.

    Strategy:
      - Spec node matches existing node (by toolFunctionName) → keep existing node
        object verbatim (preserves static values, linked params, etc.), update edges only.
      - Spec node has no match in existing → build fresh from spec.
      - Existing node not referenced in spec → dropped.
    """
    nodes_spec     = spec["nodes"]
    existing_nodes = existing_graph_resp["graph"]["nodes"]

    _validate_loops(nodes_spec)
    loop_objectives, child_aliases = _compute_loop_metadata(nodes_spec)

    # Types that don't carry a toolConfiguration / toolFunctionName
    NON_EXEC_TYPES = {"conditionNode", "loopingNode", "entryNode", "exitNode", "waitingNode"}

    def get_fn(node):
        tc = node.get("toolConfiguration") or {}
        return tc.get("toolFunctionName", "")

    existing_by_fn = {
        get_fn(n): n for n in existing_nodes
        if not n.get("isEntryNode") and n.get("nodeType") not in NON_EXEC_TYPES
    }
    existing_entry = next((n for n in existing_nodes if n.get("isEntryNode")), None)
    existing_conditions = [n for n in existing_nodes if n.get("nodeType") == "conditionNode"]
    existing_loops      = [n for n in existing_nodes if n.get("nodeType") == "loopingNode"]

    def _find_existing(spec_fn_name):
        """Find existing node by toolFunctionName, handling API-appended suffixes."""
        if spec_fn_name in existing_by_fn:
            return existing_by_fn[spec_fn_name]
        for fn_key, node in existing_by_fn.items():
            if fn_key.startswith(spec_fn_name + '_'):
                return node
        return None

    # Compute toolFunctionName for every spec node that actually has a tool
    spec_fn = {
        ns["key"]: tool_function_name(ns.get("tool_name", ns.get("name", "")))
        for ns in nodes_spec
        if not ns.get("is_entry") and _resolve_node_type(ns) not in NON_EXEC_TYPES
    }

    # ── Assign node UUIDs: reuse existing where matched ────────────────────────
    NODE = {}
    _remaining_conditions = list(existing_conditions)
    _remaining_loops      = list(existing_loops)
    for ns in nodes_spec:
        k  = ns["key"]
        nt = _resolve_node_type(ns)
        if ns.get("is_entry"):
            NODE[k] = existing_entry["id"] if existing_entry else g()
        elif nt == "conditionNode":
            NODE[k] = _remaining_conditions.pop(0)["id"] if _remaining_conditions else g()
        elif nt == "loopingNode":
            NODE[k] = _remaining_loops.pop(0)["id"] if _remaining_loops else g()
        else:
            fn = spec_fn[k]
            ex = _find_existing(fn)
            NODE[k] = ex["id"] if ex else g()

    # ── For NEW nodes only: generate TC + OP UUIDs ─────────────────────────────
    TC = {}
    OP = {}
    for ns in nodes_spec:
        nt = _resolve_node_type(ns)
        if ns.get("is_entry") or nt in NON_EXEC_TYPES:
            continue
        k  = ns["key"]
        fn = spec_fn[k]
        ex = _find_existing(fn)
        if ex:
            # Reuse existing IDs so linked params remain valid
            ex_tc = ex.get("toolConfiguration") or {}
            TC[k] = ex_tc.get("id", g())
            for op in ex_tc.get("outputParams", []):
                OP[f"{k}.{op['paramName']}"] = op["id"]
        else:
            TC[k] = g()
            for op in ns.get("output_params", []):
                OP[f"{k}.{op['name']}"] = g()

    # ── Build edge objects ──────────────────────────────────────────────────────
    EDGES = {}
    for ns in nodes_spec:
        for e in ns.get("edges", []):
            ek = f"{ns['key']}→{e['target']}"
            EDGES[ek] = {
                "sourceAgentGraphNodeId": NODE[ns["key"]],
                "targetAgentGraphNodeId": NODE[e["target"]],
                "condition":              e.get("condition", ""),
                "name":                   e.get("name", ""),
                "isAttachmentDataPulledIn": True,
            }

    def child_edges(src):
        return [v for k, v in EDGES.items() if k.startswith(f"{src}→")]

    def parent_edges(tgt):
        return [v for k, v in EDGES.items() if k.endswith(f"→{tgt}")]

    # ── Helpers for building NEW nodes ─────────────────────────────────────────
    def build_ip(ip):
        ft = ip.get("fill_type", "user_fill")
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
            "linkedOutputParamNodeId": None,
            "linkedOutputParamName":   None,
        }
        if ft == "static":
            base["staticValue"] = ip.get("static_value", "")
        elif ft == "linked":
            linked_node_key = ip['linked_node']
            linked_param    = ip['linked_param']
            op_key = f"{linked_node_key}.{linked_param}"
            if op_key not in OP:
                raise ValueError(f"Linked param '{op_key}' not found.\nAvailable: {list(OP.keys())}")
            base["linkParamOutputId"]      = OP[op_key]
            base["linkedOutputParamNodeId"] = NODE[linked_node_key]
            base["linkedOutputParamName"]   = linked_param
        return base

    def build_op(op, nk):
        return {
            "id":                       OP[f"{nk}.{op['name']}"],
            "position":                 op["position"],
            "paramName":                op["name"],
            "paramDescription":         op["description"],
            "dataType":                 op["type"],
            "isArray":                  op.get("is_array", False),
            "outputExample":            op.get("output_example", None),
            "agentToolConfigurationId": TC[nk],
            "parentId":                 None,
            "paramPath":                None,
            "typeOptions":              None,
        }

    def build_original_tool_new(ns):
        fn  = spec_fn[ns["key"]]
        ips = ns.get("input_params", [])
        ops = ns.get("output_params", [])
        return {
            "toolName":         ns.get("tool_name", ns["name"]),
            "toolFunctionName": fn,
            "iconSrc":          None,
            "type":             "custom_gpt_tool",
            "prompt":           ns.get("prompt", ""),
            "description":      ns.get("tool_description", ""),
            "preferredModel":   ns.get("model", None),
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
                    "dataType":          ip["type"],
                    "fillType":          ip.get("fill_type", "user_fill"),
                    "position":          ip["position"],
                    "required":          ip.get("required", True),
                    "paramName":         ip["name"],
                    "reloadProps":       False,
                    "outputExample":     ip.get("output_example", None),
                    "remoteOptions":     False,
                    "paramDescription":  ip["description"],
                    "isArray":           ip.get("is_array", False),
                    "staticValue":       ip.get("static_value", None),
                    "linkParamOutputId": (
                        OP.get(f"{ip['linked_node']}.{ip['linked_param']}")
                        if ip.get("fill_type") == "linked" else None
                    ),
                    "linkedOutputParamNodeId": (
                        NODE.get(ip['linked_node'])
                        if ip.get("fill_type") == "linked" else None
                    ),
                    "linkedOutputParamName": (
                        ip['linked_param']
                        if ip.get("fill_type") == "linked" else None
                    ),
                    "options":  None,
                    "paramTip": None,
                }
                for ip in ips
            ],
            "outputParams": [
                {
                    "id":               OP[f"{ns['key']}.{op['name']}"],
                    "isArray":          op.get("is_array", False),
                    "dataType":         op["type"],
                    "position":         op["position"],
                    "paramName":        op["name"],
                    "outputExample":    op.get("output_example", None),
                    "paramDescription": op["description"],
                    "typeOptions":      None,
                }
                for op in ops
            ],
        }

    def build_new_condition_node(ns):
        """Build a new conditionNode (no toolConfiguration)."""
        return {
            "id":               NODE[ns["key"]],
            "objective":        ns.get("objective", ""),
            "evaluationCriteria": [],
            "isEntryNode":      False,
            "isExitNode":       False,
            "nodeType":         "conditionNode",
            "nodeConfigurations": ns.get("node_configurations", {
                "conditionType": "llm_based",
                "llmModel": "GPT40",
                "fallbackModels": None,
            }),
            "xCoordinate":      ns.get("x", 0),
            "yCoordinate":      ns.get("y", 300),
            "isEvaluationEnabled": False,
            "isAttachmentDataPulledIn": True,
            "onError":          "STOP",
            "autoRetryWhenAccuracyLessThan":    80,
            "autoRetryLimitWhenAccuracyIsLow":  1,
            "autoRetryCountWhenFailure":        1,
            "autoRetryWaitTimeWhenFailureInMs":  1000,
            "enableAutoRetryWhenAccuracyIsLow": False,
            "enableAutoRetryWhenFailure":       False,
            "isEdited":         False,
            "childEdges":  child_edges(ns["key"]),
            "parentEdges": parent_edges(ns["key"]),
        }

    def _build_loop_config_update(ns):
        """Loop config only — alias is for children, never the loop itself."""
        lc = ns.get("loop_config", {}) or {}
        cfg = {}
        if lc.get("iteration_count") is not None:
            cfg["iterationCount"] = lc["iteration_count"]
        if lc.get("linked_variable_node") and lc.get("linked_variable_param"):
            op_key = f"{lc['linked_variable_node']}.{lc['linked_variable_param']}"
            if op_key not in OP:
                raise ValueError(
                    f"Loop '{ns['key']}' linked_variable '{op_key}' not found.\n"
                    f"Available: {list(OP.keys())}"
                )
            cfg["linkedVariableId"]       = OP[op_key]
            cfg["linkedAgentGraphNodeId"] = NODE[lc["linked_variable_node"]]
        return cfg

    def build_new_loop_node(ns):
        """Build a new loopingNode (no toolConfiguration)."""
        return {
            "id":               NODE[ns["key"]],
            "objective":        ns.get("objective", ""),
            "evaluationCriteria": [],
            "isEntryNode":      False,
            "isExitNode":       False,
            "nodeType":         "loopingNode",
            "nodeConfigurations": _build_loop_config_update(ns),
            "xCoordinate":      ns.get("x", 0),
            "yCoordinate":      ns.get("y", 300),
            "isEvaluationEnabled": False,
            "isAttachmentDataPulledIn": True,
            "onError":          ns.get("on_error", "STOP"),
            "autoRetryWhenAccuracyLessThan":    80,
            "autoRetryLimitWhenAccuracyIsLow":  1,
            "autoRetryCountWhenFailure":        ns.get("retry_count", 1),
            "autoRetryWaitTimeWhenFailureInMs":  ns.get("retry_wait_ms", 1000),
            "enableAutoRetryWhenAccuracyIsLow": False,
            "enableAutoRetryWhenFailure":       ns.get("enable_retry", False),
            "isEdited":         False,
            "childEdges":  child_edges(ns["key"]),
            "parentEdges": parent_edges(ns["key"]),
        }

    def build_new_node(ns):
        fn       = spec_fn[ns["key"]]
        criteria = ns.get("evaluation_criteria", [])
        tc = {
            "id":               TC[ns["key"]],
            "toolFunctionName": fn,
            "toolName":         ns.get("tool_name", ns["name"]),
            "iconSrc":          None,
            "description":      ns.get("tool_description", ""),
            "prompt":           ns.get("prompt", ""),
            "code":             ns.get("code"),
            "codeLanguage":     ns.get("code_language"),
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
            "integrationProviderId":   ns.get("integration_provider_id"),
            "inputParams":  [build_ip(ip)       for ip in ns.get("input_params",  [])],
            "outputParams": [build_op(op, ns["key"]) for op in ns.get("output_params", [])],
            "originalTool": build_original_tool_new(ns),
        }
        return {
            "id":               NODE[ns["key"]],
            "objective":        ns["objective"],
            "evaluationCriteria": criteria,
            "isEntryNode":      False,
            "isExitNode":       ns.get("is_exit", False),
            "nodeType":         "executionNode",
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
            "toolConfiguration": tc,
            "childEdges":  child_edges(ns["key"]),
            "parentEdges": parent_edges(ns["key"]),
        }

    # ── Rebuild linkParamOutputId on reused nodes ────────────────────────────────
    def _rebuild_linked_params(node, spec_node):
        """Rebuild linked param references on an existing node using spec's linked info.

        Sets linkedOutputParamNodeId (node ID from this payload) +
        linkedOutputParamName (output param name) which the API uses to
        resolve linkParamOutputId on PUT.
        """
        tc = node.get("toolConfiguration")
        if not tc:
            return
        spec_ips = {ip["name"]: ip for ip in spec_node.get("input_params", [])}
        # Patch toolConfiguration.inputParams
        for ip in tc.get("inputParams", []):
            spec_ip = spec_ips.get(ip.get("paramName"))
            if spec_ip and spec_ip.get("fill_type") == "linked":
                linked_node_key = spec_ip['linked_node']
                linked_param    = spec_ip['linked_param']
                op_key = f"{linked_node_key}.{linked_param}"
                ip["linkParamOutputId"]      = OP.get(op_key)
                ip["linkedOutputParamNodeId"] = NODE.get(linked_node_key)
                ip["linkedOutputParamName"]   = linked_param
                ip["fillType"] = "linked"
        # Patch originalTool.inputParams
        ot = tc.get("originalTool")
        if ot:
            for ip in ot.get("inputParams", []):
                spec_ip = spec_ips.get(ip.get("paramName"))
                if spec_ip and spec_ip.get("fill_type") == "linked":
                    linked_node_key = spec_ip['linked_node']
                    linked_param    = spec_ip['linked_param']
                    op_key = f"{linked_node_key}.{linked_param}"
                    ip["linkParamOutputId"]      = OP.get(op_key)
                    ip["linkedOutputParamNodeId"] = NODE.get(linked_node_key)
                    ip["linkedOutputParamName"]   = linked_param
                    ip["fillType"] = "linked"

    # ── Assemble final nodes ────────────────────────────────────────────────────
    final_nodes = []
    _reused_condition_ids = set()
    _reused_loop_ids = set()
    for ns in nodes_spec:
        k  = ns["key"]
        nt = _resolve_node_type(ns)
        ce = child_edges(k)
        pe = parent_edges(k)

        if ns.get("is_entry"):
            node = dict(existing_entry) if existing_entry else {
                "id": NODE[k], "objective": "Entry Node",
                "evaluationCriteria": [], "isEntryNode": True, "isExitNode": False,
                "nodeType": "entryNode",
                "xCoordinate": ns.get("x", 250), "yCoordinate": ns.get("y", 0),
                "isEvaluationEnabled": False, "isAttachmentDataPulledIn": True,
                "onError": "STOP", "enableAutoRetryWhenFailure": False,
                "autoRetryCountWhenFailure": 1, "autoRetryWaitTimeWhenFailureInMs": 1000,
                "autoRetryWhenAccuracyLessThan": 80, "autoRetryLimitWhenAccuracyIsLow": 1,
                "enableAutoRetryWhenAccuracyIsLow": False,
                "autoRetryDescription": None, "enableAutoRetryDescription": False,
                "isEdited": False,
            }
            node["childEdges"]  = ce
            node["parentEdges"] = pe
            final_nodes.append(node)
        elif nt == "conditionNode":
            node_id = NODE[k]
            existing_cond = next(
                (n for n in existing_conditions if n["id"] == node_id),
                None,
            )
            if existing_cond and node_id not in _reused_condition_ids:
                node = dict(existing_cond)
                node["childEdges"]  = ce
                node["parentEdges"] = pe
                _reused_condition_ids.add(node_id)
                final_nodes.append(node)
            else:
                final_nodes.append(build_new_condition_node(ns))
        elif nt == "loopingNode":
            node_id = NODE[k]
            existing_loop = next(
                (n for n in existing_loops if n["id"] == node_id),
                None,
            )
            if existing_loop and node_id not in _reused_loop_ids:
                node = copy.deepcopy(existing_loop)
                # Refresh loop config from spec
                loop_cfg = _build_loop_config_update(ns)
                if loop_cfg:
                    node["nodeConfigurations"] = loop_cfg
                # Server returns GPTAction_LoopingNodeTool with description/prompt = null,
                # but PUT validator requires strings. Coerce here.
                tc = node.get("toolConfiguration") or {}
                if tc:
                    if tc.get("description") is None:
                        tc["description"] = ""
                    if tc.get("prompt") is None:
                        tc["prompt"] = ""
                    ot = tc.get("originalTool") or {}
                    if ot:
                        if ot.get("description") is None:
                            ot["description"] = ""
                        if ot.get("prompt") is None:
                            ot["prompt"] = ""
                        if ot.get("toolName") is None:
                            ot["toolName"] = ""
                node["childEdges"]  = ce
                node["parentEdges"] = pe
                _reused_loop_ids.add(node_id)
                final_nodes.append(node)
            else:
                final_nodes.append(build_new_loop_node(ns))
        else:
            fn = spec_fn[k]
            ex = _find_existing(fn)
            if ex:
                node = copy.deepcopy(ex)
                node["childEdges"]  = ce
                node["parentEdges"] = pe
                _rebuild_linked_params(node, ns)
                final_nodes.append(node)
            else:
                final_nodes.append(build_new_node(ns))

        # parentNodeId — set/refresh on every node that lives inside a loop
        parent_key = ns.get("parent_node")
        if parent_key:
            final_nodes[-1]["parentNodeId"] = NODE[parent_key]
        elif "parentNodeId" in final_nodes[-1]:
            # Spec says this node is no longer inside a loop → clear stale value
            final_nodes[-1]["parentNodeId"] = None

        # Auto-override: loopingNode objective is always "N: Loop"
        if nt == "loopingNode":
            final_nodes[-1]["objective"] = loop_objectives[k]

        # Auto-assign numeric alias to every loop child
        if parent_key:
            cfg = final_nodes[-1].get("nodeConfigurations")
            if cfg is None:
                cfg = {}
                final_nodes[-1]["nodeConfigurations"] = cfg
            cfg["alias"] = child_aliases[k]

    return {
        "agentName":        spec["agentName"],
        "agentDescription": spec.get("agentDescription", ""),
        "settings": {
            "prompts":           spec.get("prompts", []),
            "agentPersonality":  spec.get("personality", ""),
            "agentRestrictions": spec.get("restrictions", ""),
        },
        "nodes": final_nodes,
    }


# ── API calls ──────────────────────────────────────────────────────────────────
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


def update_agent(agent_id: str, payload: dict, api_key: str, workspace_id: str) -> dict:
    headers = {
        "x-api-key":            api_key,
        "current-workspace-id": workspace_id,
        "Content-Type":         "application/json",
    }
    resp = requests.put(
        f"{BASE_URL}/agent-graphs/{agent_id}",
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
    parser.add_argument("--agent-id", help="Existing agent UUID — uses PUT to update instead of POST to create")
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

    # Build payload — GET existing graph first when updating (preserves manual changes)
    if args.agent_id:
        print(f"Fetching existing graph for {args.agent_id}...", file=sys.stderr)
        existing_graph = get_agent_graph(args.agent_id, beam_api_key, workspace_id)
        payload = build_payload_update(spec, existing_graph)
    else:
        payload = build_payload(spec)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        print(f"\n=== DRY RUN — {len(payload['nodes'])} nodes, no API call ===", file=sys.stderr)
        return

    # Summary
    action = f"Updating [{args.agent_id}]" if args.agent_id else "Creating"
    print(f"{action}: {payload['agentName']}  ({len(payload['nodes'])} nodes)")
    for n in payload["nodes"]:
        tc     = n.get("toolConfiguration") or {}
        nt     = n.get("nodeType", "")
        if n.get("isEntryNode"):
            role = "ENTRY"
        elif nt == "conditionNode":
            role = "CONDITION"
        else:
            role = tc.get("toolName", "?")
        ins    = len(tc.get("inputParams", []))
        outs   = len(tc.get("outputParams", []))
        linked = [p["paramName"] for p in tc.get("inputParams", []) if p.get("fillType") == "linked"]
        print(f"  [{role:35s}]  {ins} in / {outs} out"
              + (f"  linked={linked}" if linked else ""))

    if args.agent_id:
        result = update_agent(args.agent_id, payload, beam_api_key, workspace_id)
        print("\nAgent updated!")
        print(f"  Agent ID:    {result.get('agentId')}")
        print(f"  Agent Name:  {result.get('agentName')}")
        print(f"  Draft Graph: {result.get('draftGraphId')}")
    else:
        result = create_agent(payload, beam_api_key, workspace_id)
        print("\nAgent created!")
        print(f"  Agent ID:    {result.get('agentId')}")
        print(f"  Agent Name:  {result.get('agentName')}")
        print(f"  Draft Graph: {result.get('draftGraphId')}")
        print(f"  Active Graph:{result.get('activeGraphId')}")


if __name__ == "__main__":
    main()
