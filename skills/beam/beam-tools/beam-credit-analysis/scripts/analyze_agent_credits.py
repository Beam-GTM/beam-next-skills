#!/usr/bin/env python3
"""
Beam Agent Credit Consumption Analyzer

Fetches an agent graph from Beam API, traces all execution paths,
and calculates credit consumption and cost per path.

Usage:
    python analyze_agent_credits.py <agent_url_or_id> [options]

Examples:
    python analyze_agent_credits.py https://app.enterprise.beam.ai/WORKSPACE/AGENT/flow
    python analyze_agent_credits.py --workspace-id WS_ID --agent-id AGENT_ID
    python analyze_agent_credits.py --graph-file ./path/to/graph.json
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import requests
except ImportError:
    print("[ERROR] Missing 'requests' library. Install: pip install requests", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_nexus_root():
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / "CLAUDE.md").exists():
            return path
    return current


def load_env_file(env_path):
    env_vars = {}
    if not env_path.exists():
        return env_vars
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars


def _notion_model_to_keys(display_name):
    """Convert Notion display name (e.g. 'Gemini 3 Flash') to graph-style keys."""
    # Canonical UPPER_SNAKE: "Gemini 3 Flash" -> "GEMINI_3_FLASH"
    upper = display_name.upper().replace(" ", "_").replace("-", "_").replace(".", "_")
    # Lower-kebab: "gemini-3-flash"
    lower = display_name.lower().replace(" ", "-")
    return [upper, lower]


def fetch_pricing_from_notion(env_vars):
    """Try to fetch live pricing from Saqib's Notion page. Returns pricing dict or None."""
    api_key = env_vars.get("NOTION_API_KEY")
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    PRICING_PAGE_ID = "3062cadfbbbc8198afeae750cb9e292f"

    try:
        # 1) Find child_database IDs under each section heading
        resp = requests.get(
            f"https://api.notion.com/v1/blocks/{PRICING_PAGE_ID}/children?page_size=100",
            headers=headers, timeout=15,
        )
        if resp.status_code != 200:
            return None
        blocks = resp.json().get("results", [])

        db_map = {}  # section_name -> database_id
        current_section = None
        last_updated = None
        for block in blocks:
            btype = block["type"]
            if btype == "paragraph" and current_section is None:
                texts = block["paragraph"].get("rich_text", [])
                text = "".join(t.get("plain_text", "") for t in texts)
                if "Last updated" in text or "updated" in text.lower():
                    # Extract date from "Last updated: Feb 13, 2026" etc.
                    last_updated = text.split(":")[-1].strip() if ":" in text else text
            if btype in ("heading_1", "heading_2", "heading_3"):
                texts = block[btype].get("rich_text", [])
                current_section = "".join(t.get("plain_text", "") for t in texts)
            elif btype == "child_database":
                db_map[current_section] = block["id"]

        # 2) Query LLM pricing database
        llm_db_id = None
        for section, dbid in db_map.items():
            if section and "LLM PRICING" in section.upper():
                llm_db_id = dbid
                break
        if not llm_db_id:
            return None

        resp = requests.post(
            f"https://api.notion.com/v1/databases/{llm_db_id}/query",
            headers=headers, json={}, timeout=15,
        )
        if resp.status_code != 200:
            return None

        llm_models = {}
        for row in resp.json().get("results", []):
            props = row.get("properties", {})
            model_name = "".join(t.get("plain_text", "") for t in props.get("Model", {}).get("title", []))
            credits_text = "".join(t.get("plain_text", "") for t in props.get("Credits", {}).get("rich_text", []))
            cost_text = "".join(t.get("plain_text", "") for t in props.get("What We Charge", {}).get("rich_text", []))
            margin_text = "".join(t.get("plain_text", "") for t in props.get("Our Margin", {}).get("rich_text", []))

            try:
                credits = int(credits_text)
                cost = float(cost_text.replace("$", ""))
            except (ValueError, TypeError):
                continue

            margin = margin_text or ""
            for key in _notion_model_to_keys(model_name):
                llm_models[key] = {"credits": credits, "cost_per_node": cost, "margin": margin}

        # 3) Query NON-LLM pricing database
        non_llm_db_id = None
        for section, dbid in db_map.items():
            if section and "NON-LLM" in section.upper():
                non_llm_db_id = dbid
                break

        non_llm = {
            "trigger": {"credits": 0.25, "cost_per_node": 0.025},
            "integration": {"credits": 0.25, "cost_per_node": 0.025},
        }
        if non_llm_db_id:
            resp = requests.post(
                f"https://api.notion.com/v1/databases/{non_llm_db_id}/query",
                headers=headers, json={}, timeout=15,
            )
            if resp.status_code == 200:
                for row in resp.json().get("results", []):
                    props = row.get("properties", {})
                    item = "".join(t.get("plain_text", "") for t in props.get("Item", {}).get("title", []))
                    credits_text = "".join(t.get("plain_text", "") for t in props.get("Credits", {}).get("rich_text", []))
                    try:
                        credits = float(credits_text)
                    except (ValueError, TypeError):
                        continue
                    cost = round(credits * 0.10, 4)
                    item_lower = item.lower()
                    if "trigger" in item_lower:
                        non_llm["trigger"] = {"credits": credits, "cost_per_node": cost}
                    elif "integration" in item_lower:
                        non_llm["integration"] = {"credits": credits, "cost_per_node": cost}

        # 4) Query SYSTEM FEATURES database
        sys_db_id = None
        for section, dbid in db_map.items():
            if section and "SYSTEM FEATURES" in section.upper():
                sys_db_id = dbid
                break

        system_features = {"eval": {"credits": 1, "cost_per_node": 0.10}}
        if sys_db_id:
            resp = requests.post(
                f"https://api.notion.com/v1/databases/{sys_db_id}/query",
                headers=headers, json={}, timeout=15,
            )
            if resp.status_code == 200:
                for row in resp.json().get("results", []):
                    props = row.get("properties", {})
                    feature = "".join(t.get("plain_text", "") for t in props.get("Feature", {}).get("title", []))
                    credits_text = "".join(t.get("plain_text", "") for t in props.get("Credits", {}).get("rich_text", []))
                    if feature.lower() == "eval":
                        try:
                            system_features["eval"] = {
                                "credits": int(credits_text),
                                "cost_per_node": round(int(credits_text) * 0.10, 2),
                            }
                        except (ValueError, TypeError):
                            pass

        from datetime import datetime as dt
        pricing = {
            "_meta": {
                "source": f"https://www.notion.so/joinbeam/Beam-Credits-New-Agent-OS-{PRICING_PAGE_ID.replace('-', '')}",
                "last_updated": last_updated or dt.now().strftime("%Y-%m-%d"),
                "base_credit_value": 0.10,
                "token_basis": "100k tokens average per execution",
                "fetched_live": True,
            },
            "llm_models": llm_models,
            "non_llm": non_llm,
            "system_features": system_features,
        }
        print(f"[INFO] Fetched live pricing from Notion ({len(llm_models)} LLM model entries)", file=sys.stderr)
        return pricing

    except Exception as e:
        print(f"[WARN] Failed to fetch Notion pricing: {e}", file=sys.stderr)
        return None


def load_pricing(pricing_path=None, env_vars=None):
    """Load pricing: try Notion live fetch first, fall back to pricing.json."""
    # Try live Notion fetch if no explicit pricing file was given
    if pricing_path is None and env_vars:
        live_pricing = fetch_pricing_from_notion(env_vars)
        if live_pricing:
            return live_pricing

    # Fallback to local pricing.json
    if pricing_path is None:
        pricing_path = Path(__file__).parent.parent / "references" / "pricing.json"
    with open(pricing_path, "r") as f:
        pricing = json.load(f)
    pricing["_meta"]["fetched_live"] = False
    print("[INFO] Using local pricing.json (Notion fetch unavailable)", file=sys.stderr)
    return pricing


def parse_beam_url(url):
    """Extract workspace_id and agent_id from a Beam URL."""
    patterns = [
        # https://app.beam.ai/WORKSPACE/AGENT/flow
        r"app\.(?:enterprise\.)?beam\.ai/([a-f0-9-]+)/([a-f0-9-]+)",
        # Just two UUIDs separated by /
        r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
    return None, None


def detect_base_url(url):
    """Detect API base URL from the app URL."""
    if "enterprise.beam" in url:
        return "https://api.enterprise.beamstudio.ai"
    elif "bid.beam" in url or "staging" in url:
        return "https://api.bid.beamstudio.ai"
    return "https://api.beamstudio.ai"


# ---------------------------------------------------------------------------
# Beam API
# ---------------------------------------------------------------------------

def get_access_token(api_key, base_url):
    url = f"{base_url}/auth/access-token"
    resp = requests.post(url, json={"apiKey": api_key}, headers={"Content-Type": "application/json"}, timeout=30)
    if resp.status_code in (200, 201):
        data = resp.json()
        return data.get("idToken") or data.get("access_token") or data.get("accessToken")
    print(f"[ERROR] Auth failed ({resp.status_code}): {resp.text}", file=sys.stderr)
    return None


def fetch_agent_graph(access_token, workspace_id, agent_id, base_url):
    url = f"{base_url}/agent-graphs/{agent_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "current-workspace-id": workspace_id,
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 200:
        return resp.json()
    print(f"[ERROR] Graph fetch failed ({resp.status_code}): {resp.text}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Graph Analysis
# ---------------------------------------------------------------------------

def resolve_model_name(model, pricing):
    """Resolve a model name to its canonical pricing key."""
    if not model:
        return model
    models = pricing.get("llm_models", {})
    if model in models:
        return model
    normalized = model.upper().replace("-", "_").replace(".", "_")
    if normalized in models:
        return normalized
    # Insert underscores between letters and digits (GPT5 → GPT_5)
    expanded = re.sub(r"([A-Za-z])(\d)", r"\1_\2", normalized)
    if expanded in models:
        return expanded
    # Version fallback: GPT_5_2 → GPT_5, CLAUDE_4_5_OPUS → CLAUDE_4_5_OPUS (no change)
    parts = expanded.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit() and parts[0] in models:
        return parts[0]
    return model


def classify_node(node, model_overrides=None, pricing=None):
    """Classify a node and return its type and model info."""
    tc = node.get("toolConfiguration") or {}
    func_name = tc.get("toolFunctionName") or ""
    tool_name = tc.get("toolName") or ""
    # preferredModel lives in originalTool, fallback to top-level toolConfiguration
    original_tool = tc.get("originalTool") or {}
    model = tc.get("preferredModel") or original_tool.get("preferredModel") or ""

    # Apply model overrides
    if model_overrides and model in model_overrides:
        model = model_overrides[model]

    # Normalize to canonical pricing key
    if model and pricing:
        model = resolve_model_name(model, pricing)

    is_entry = node.get("isEntryNode", False)
    is_exit = node.get("isExitNode", False)
    has_eval = node.get("isEvaluationEnabled", False)

    if not func_name and (is_entry or is_exit):
        return {
            "type": "trigger" if is_entry else "exit",
            "tool_name": tool_name or ("Entry Node" if is_entry else "Exit Node"),
            "model": None,
            "is_custom_gpt": False,
            "is_integration": False,
            "has_eval": False,
            "credits_category": "trigger" if is_entry else None,
        }

    if func_name.startswith("GPTAction_Custom_"):
        return {
            "type": "custom_gpt",
            "tool_name": tool_name,
            "model": model,
            "is_custom_gpt": True,
            "is_integration": False,
            "has_eval": has_eval,
            "credits_category": "llm",
        }

    # Integration or utility node
    return {
        "type": "integration",
        "tool_name": tool_name,
        "model": None,
        "is_custom_gpt": False,
        "is_integration": True,
        "has_eval": False,
        "credits_category": "integration",
    }


def get_node_credits(classification, pricing):
    """Return (credits, cost) for a node."""
    cat = classification["credits_category"]

    if cat is None:  # exit nodes
        return 0, 0.0

    if cat == "trigger":
        t = pricing["non_llm"]["trigger"]
        return t["credits"], t["cost_per_node"]

    if cat == "integration":
        t = pricing["non_llm"]["integration"]
        return t["credits"], t["cost_per_node"]

    if cat == "llm":
        model = classification["model"]
        if model:
            resolved = resolve_model_name(model, pricing)
            if resolved in pricing["llm_models"]:
                m = pricing["llm_models"][resolved]
                return m["credits"], m["cost_per_node"]
        # Default: 1 credit (flash-tier)
        return 1, 0.10

    return 0, 0.0


def build_graph(graph_data):
    """Build adjacency list and node lookup from graph data."""
    graph = graph_data.get("graph", graph_data)
    nodes = graph.get("nodes", [])
    agent = graph.get("agent", {})
    agent_name = agent.get("name", "Unknown Agent")

    node_map = {}
    adjacency = defaultdict(list)
    entry_nodes = []
    terminal_nodes = []

    for node in nodes:
        nid = node["id"]
        node_map[nid] = node

        if node.get("isEntryNode"):
            entry_nodes.append(nid)

        # Build edges from childEdges within each node
        child_edges = node.get("childEdges") or []
        for edge in child_edges:
            target = edge.get("targetAgentGraphNodeId")
            if target:
                adjacency[nid].append({
                    "target": target,
                    "name": edge.get("name", ""),
                    "condition": edge.get("condition", ""),
                })

    # Find terminal nodes (exit nodes or nodes with no outgoing edges)
    all_node_ids = set(node_map.keys())
    nodes_with_outgoing = set(adjacency.keys())
    for nid in all_node_ids:
        node = node_map[nid]
        if node.get("isExitNode") or nid not in nodes_with_outgoing:
            if not node.get("isEntryNode"):
                terminal_nodes.append(nid)

    return node_map, adjacency, entry_nodes, terminal_nodes, agent_name


def find_all_paths(adjacency, entry_nodes, terminal_nodes, node_map):
    """DFS to find all paths from entry to terminal nodes."""
    terminal_set = set(terminal_nodes)
    all_paths = []

    def dfs(current, path, visited, edges_taken):
        path.append(current)
        visited.add(current)

        # Terminal: exit node or no outgoing edges
        if current in terminal_set or current not in adjacency or not adjacency[current]:
            all_paths.append((list(path), list(edges_taken)))
        else:
            for edge in adjacency[current]:
                target = edge["target"]
                if target not in visited and target in node_map:
                    edges_taken.append(edge)
                    dfs(target, path, visited, edges_taken)
                    edges_taken.pop()

        path.pop()
        visited.discard(current)

    for entry in entry_nodes:
        dfs(entry, [], set(), [])

    return all_paths


def categorize_paths_into_branches(all_paths, node_map, adjacency, entry_nodes):
    """Group paths by the first edge taken from the entry node (= branch)."""
    branches = defaultdict(list)

    for path_nodes, edges in all_paths:
        if len(path_nodes) < 2:
            branches["Single Node"].append((path_nodes, edges))
            continue

        entry_id = path_nodes[0]
        if entry_id in adjacency and adjacency[entry_id]:
            first_target = path_nodes[1]
            # Find the edge name
            branch_name = "Default"
            for edge in adjacency[entry_id]:
                if edge["target"] == first_target:
                    branch_name = edge.get("name") or edge.get("condition") or "Default"
                    break
            branches[branch_name].append((path_nodes, edges))
        else:
            branches["Default"].append((path_nodes, edges))

    return dict(branches)


# ---------------------------------------------------------------------------
# Credit Calculation
# ---------------------------------------------------------------------------

def analyze_path(path_nodes, node_map, pricing, model_overrides=None):
    """Analyze a single path and return detailed breakdown."""
    steps = []
    totals = {"flash": 0, "premium": 0, "integration": 0, "trigger": 0}
    total_credits = 0.0
    total_cost = 0.0
    total_nodes = 0
    eval_count = 0

    for nid in path_nodes:
        node = node_map.get(nid)
        if not node:
            continue

        cls = classify_node(node, model_overrides, pricing)
        credits, cost = get_node_credits(cls, pricing)

        category = "other"
        if cls["credits_category"] == "trigger":
            category = "trigger"
            totals["trigger"] += 1
        elif cls["credits_category"] is None:
            category = "exit"
        elif cls["credits_category"] == "integration":
            category = "integration"
            totals["integration"] += 1
        elif cls["credits_category"] == "llm":
            if credits >= 2:
                category = "premium"
                totals["premium"] += 1
            else:
                category = "flash"
                totals["flash"] += 1

        if cls["has_eval"]:
            eval_count += 1

        if cls["credits_category"] is not None:
            total_nodes += 1

        total_credits += credits
        total_cost += cost

        steps.append({
            "node_id": nid,
            "tool_name": cls["tool_name"],
            "type": cls["type"],
            "model": cls["model"],
            "category": category,
            "credits": credits,
            "cost": cost,
            "has_eval": cls["has_eval"],
        })

    return {
        "steps": steps,
        "totals": totals,
        "total_nodes": total_nodes,
        "total_credits": round(total_credits, 2),
        "total_cost": round(total_cost, 4),
        "eval_nodes": eval_count,
    }


# ---------------------------------------------------------------------------
# Markdown Generation
# ---------------------------------------------------------------------------

def get_premium_label(pricing, model_overrides=None):
    """Determine the label for premium model column based on what's used."""
    # Default label
    return "Premium"


def generate_description(path_nodes, edges, node_map):
    """Generate a short description of a path based on key decision points."""
    parts = []
    for edge in edges:
        name = edge.get("name", "").strip()
        if name:
            parts.append(name)
    if parts:
        return " → ".join(parts[:4])
    # Fallback: use tool names
    tools = []
    for nid in path_nodes[1:4]:
        node = node_map.get(nid)
        if node:
            tc = node.get("toolConfiguration") or {}
            tools.append(tc.get("toolName", "")[:20])
    return " → ".join(t for t in tools if t) or "Direct path"


def generate_mermaid(branches, all_analyses, node_map, adjacency, entry_nodes):
    """Generate a mermaid flowchart showing all paths."""
    lines = ["```mermaid", "graph TD"]

    # Collect all unique nodes across all paths
    seen_nodes = set()
    seen_edges = set()

    for branch_name, paths in branches.items():
        for path_nodes, edges in paths:
            for i, nid in enumerate(path_nodes):
                if nid not in seen_nodes:
                    seen_nodes.add(nid)
                    node = node_map.get(nid, {})
                    tc = node.get("toolConfiguration") or {}
                    label = tc.get("toolName") or node.get("objective", "")[:30] or nid[:8]
                    label = label.replace('"', "'")

                    if node.get("isEntryNode"):
                        lines.append(f'    {nid[:8]}(("{label}"))')
                    elif node.get("isExitNode"):
                        lines.append(f'    {nid[:8]}[/"{label}"\\]')
                    else:
                        lines.append(f'    {nid[:8]}["{label}"]')

                if i < len(path_nodes) - 1:
                    src = nid[:8]
                    tgt = path_nodes[i + 1][:8]
                    edge_key = f"{src}->{tgt}"
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        # Find edge label
                        edge_label = ""
                        if i < len(edges):
                            edge_label = edges[i].get("name", "")
                        if edge_label:
                            edge_label = edge_label.replace('"', "'")[:30]
                            lines.append(f'    {src} -->|"{edge_label}"| {tgt}')
                        else:
                            lines.append(f'    {src} --> {tgt}')

    lines.append("```")
    return "\n".join(lines)


def generate_markdown(agent_name, agent_id, workspace_id, graph_id,
                      branches, all_analyses, pricing, node_map, adjacency,
                      entry_nodes, model_overrides=None, pricing_source=None):
    """Generate the complete markdown analysis document."""

    now = datetime.now().strftime("%Y-%m-%d")
    pricing_src = pricing_source or pricing["_meta"]["source"]

    lines = []
    lines.append(f"# {agent_name} — Credit Consumption Analysis\n")
    lines.append(f"**Agent ID:** `{agent_id}`")
    lines.append(f"**Graph ID:** `{graph_id}`")
    lines.append(f"**Analysis Date:** {now}")
    lines.append(f"**Pricing Source:** [Beam Credits (New Agent OS)]({pricing_src}) — Last updated {pricing['_meta']['last_updated']}")
    if not pricing["_meta"].get("fetched_live"):
        lines.append("")
        lines.append("> **Note:** Pricing was loaded from a local snapshot (pricing.json, dated 2026-02-20). "
                     "For the latest rates, add `NOTION_API_KEY` to your `.env` file to enable live pricing from the Notion page.")
    lines.append("")
    lines.append("---\n")

    # Credit rates
    lines.append("## Credit Rates\n")
    lines.append("| Node Type | Credits/Node | Cost/Node |")
    lines.append("|-----------|:------------:|:---------:|")
    lines.append(f"| Trigger (entry) | {pricing['non_llm']['trigger']['credits']} | ${pricing['non_llm']['trigger']['cost_per_node']} |")

    # Show unique LLM models actually used
    used_models = set()
    for branch_name, paths in branches.items():
        for path_nodes, edges in paths:
            for nid in path_nodes:
                node = node_map.get(nid, {})
                cls = classify_node(node, model_overrides, pricing)
                if cls["credits_category"] == "llm" and cls["model"]:
                    used_models.add(cls["model"])

    for model in sorted(used_models):
        # Use a dummy classification to reuse get_node_credits logic
        dummy_cls = {"credits_category": "llm", "model": model}
        credits, cost = get_node_credits(dummy_cls, pricing)
        lines.append(f"| Custom GPT — {model} | {credits} | ${cost} |")

    lines.append(f"| Integration (Airtable, Zendesk, Slack) | {pricing['non_llm']['integration']['credits']} | ${pricing['non_llm']['integration']['cost_per_node']} |")
    lines.append(f"| Eval (per node, if enabled) | {pricing['system_features']['eval']['credits']} | ${pricing['system_features']['eval']['cost_per_node']} |")
    lines.append("")
    lines.append("---\n")

    # Architecture overview
    total_paths = sum(len(paths) for paths in branches.values())
    lines.append(f"## Agent Architecture — {len(branches)} Branches, {total_paths} Paths\n")

    # Mermaid diagram
    lines.append("### Flow Diagram\n")
    lines.append(generate_mermaid(branches, all_analyses, node_map, adjacency, entry_nodes))
    lines.append("")
    lines.append("---\n")

    # Per-branch tables
    path_counter = 0
    summary_rows = []

    for branch_name, paths in branches.items():
        lines.append(f"## Branch: {branch_name}\n")

        # Determine premium model label for this branch
        premium_label = "Premium"
        for path_nodes, edges in paths:
            for nid in path_nodes:
                node = node_map.get(nid, {})
                cls = classify_node(node, model_overrides, pricing)
                if cls["credits_category"] == "llm" and cls["model"]:
                    credits, _ = get_node_credits(cls, pricing)
                    if credits >= 2:
                        premium_label = cls["model"]
                        break

        # --- Node Count Table ---
        lines.append("### Node Count\n")
        lines.append(f"| Path | Description | Flash | {premium_label} | Integration | Trigger | **Total Nodes** |")
        lines.append(f"|:----:|-------------|:-----:|:-------:|:-----------:|:-------:|:---------------:|")

        path_analyses = []
        for path_nodes, edges in paths:
            path_counter += 1
            analysis = analyze_path(path_nodes, node_map, pricing, model_overrides)
            desc = generate_description(path_nodes, edges, node_map)
            analysis["path_num"] = path_counter
            analysis["description"] = desc
            analysis["path_nodes"] = path_nodes
            analysis["edges"] = edges
            path_analyses.append(analysis)

            t = analysis["totals"]
            lines.append(f"| {path_counter} | {desc} | {t['flash']} | {t['premium']} | {t['integration']} | {t['trigger']} | **{analysis['total_nodes']}** |")

        lines.append("")

        # --- Credit Consumption Table ---
        lines.append("### Credit Consumption\n")

        # Get credit rates for column headers
        flash_rate = 1
        premium_rate = 2
        int_rate = pricing["non_llm"]["integration"]["credits"]
        trig_rate = pricing["non_llm"]["trigger"]["credits"]

        for pa in path_analyses:
            for step in pa["steps"]:
                if step["category"] == "premium":
                    premium_rate = step["credits"]
                    break

        lines.append(f"> Flash = count × {flash_rate} credit | {premium_label} = count × {premium_rate} credits | Integration = count × {int_rate} credits | Trigger = count × {trig_rate} credits\n")
        lines.append(f"| Path | Description | Flash | {premium_label} | Integration | Trigger | **Total Credits** |")
        lines.append(f"|:----:|-------------|:-----:|:-------:|:-----------:|:-------:|:-----------------:|")

        for pa in path_analyses:
            t = pa["totals"]
            fc = round(t["flash"] * flash_rate, 2)
            pc = round(t["premium"] * premium_rate, 2)
            ic = round(t["integration"] * int_rate, 2)
            tc = round(t["trigger"] * trig_rate, 2)
            lines.append(f"| {pa['path_num']} | {pa['description']} | {fc:.2f} | {pc:.2f} | {ic:.2f} | {tc:.2f} | **{pa['total_credits']:.2f}** |")

        lines.append("")

        # --- Cost Table ---
        flash_cost = 0.10
        premium_cost = 0.20
        int_cost = pricing["non_llm"]["integration"]["cost_per_node"]
        trig_cost = pricing["non_llm"]["trigger"]["cost_per_node"]

        for pa in path_analyses:
            for step in pa["steps"]:
                if step["category"] == "premium":
                    premium_cost = step["cost"]
                    break

        lines.append("### Cost\n")
        lines.append(f"> Flash = count × ${flash_cost} | {premium_label} = count × ${premium_cost} | Integration = count × ${int_cost} | Trigger = count × ${trig_cost}\n")
        lines.append(f"| Path | Description | Flash | {premium_label} | Integration | Trigger | **Total Cost** |")
        lines.append(f"|:----:|-------------|:-----:|:-------:|:-----------:|:-------:|:--------------:|")

        for pa in path_analyses:
            t = pa["totals"]
            fc = round(t["flash"] * flash_cost, 3)
            pc = round(t["premium"] * premium_cost, 3)
            ic = round(t["integration"] * int_cost, 3)
            tc = round(t["trigger"] * trig_cost, 3)
            total = round(fc + pc + ic + tc, 3)
            lines.append(f"| {pa['path_num']} | {pa['description']} | ${fc} | ${pc} | ${ic} | ${tc} | **${total}** |")

        lines.append("")
        lines.append("---\n")

        # Collect summary rows
        for pa in path_analyses:
            summary_rows.append(pa)

    # --- Summary Table ---
    lines.append("## Summary — All Paths\n")
    lines.append("| Path | Description | Total Nodes | Total Credits | Total Cost |")
    lines.append("|:----:|-------------|:-----------:|:------------:|:----------:|")
    for pa in summary_rows:
        lines.append(f"| {pa['path_num']} | {pa['description']} | {pa['total_nodes']} | {pa['total_credits']:.2f} | ${pa['total_cost']:.3f} |")
    lines.append("")
    lines.append("---\n")

    # --- Eval Impact Table ---
    lines.append("## Eval Impact (if enabled on all Custom GPT nodes)\n")
    lines.append("| Path | Base Credits | + Eval on GPT nodes | Total w/ Eval | Total Cost w/ Eval |")
    lines.append("|:----:|:-----------:|:-------------------:|:------------:|:------------------:|")
    for pa in summary_rows:
        gpt_count = pa["totals"]["flash"] + pa["totals"]["premium"]
        eval_credits = gpt_count * pricing["system_features"]["eval"]["credits"]
        total_w_eval = round(pa["total_credits"] + eval_credits, 2)
        cost_w_eval = round(total_w_eval * pricing["_meta"]["base_credit_value"], 3)
        lines.append(f"| {pa['path_num']} | {pa['total_credits']:.2f} | +{eval_credits} | {total_w_eval:.2f} | ${cost_w_eval} |")
    lines.append("")
    lines.append("---\n")

    # --- Step-by-step for longest paths ---
    lines.append("## Detailed Step-by-Step Breakdowns\n")

    # Show top 3 by total credits
    top_paths = sorted(summary_rows, key=lambda x: x["total_credits"], reverse=True)[:3]
    for pa in top_paths:
        lines.append(f"### Path {pa['path_num']} — {pa['description']} ({pa['total_credits']} credits / ${pa['total_cost']})\n")
        lines.append("| Step | Node | Type | Credits | Cost |")
        lines.append("|:----:|------|------|:-------:|:----:|")
        step_num = 0
        for step in pa["steps"]:
            if step["credits"] == 0 and step["category"] == "exit":
                continue
            model_note = f" (**{step['model']}**)" if step["model"] and step["category"] == "premium" else ""
            type_label = step["type"].replace("_", " ").title()
            if step["model"] and step["category"] == "flash":
                type_label = f"Custom GPT (Flash)"
            elif step["model"] and step["category"] == "premium":
                type_label = f"Custom GPT{model_note}"
            elif step["category"] == "trigger":
                type_label = "Entry"
            elif step["category"] == "integration":
                type_label = "Integration"
            lines.append(f"| {step_num} | {step['tool_name']} | {type_label} | {step['credits']:.2f} | ${step['cost']} |")
            step_num += 1
        lines.append(f"| | | **Total** | **{pa['total_credits']:.2f}** | **${pa['total_cost']}** |")
        lines.append("")

    lines.append("---\n")

    # --- Node Inventory ---
    lines.append("## Node Inventory\n")

    # Collect unique nodes
    all_nodes_seen = {}
    for branch_name, paths in branches.items():
        for path_nodes, edges in paths:
            for nid in path_nodes:
                if nid not in all_nodes_seen:
                    node = node_map.get(nid, {})
                    cls = classify_node(node, model_overrides, pricing)
                    credits, cost = get_node_credits(cls, pricing)
                    all_nodes_seen[nid] = {
                        "cls": cls,
                        "credits": credits,
                        "cost": cost,
                        "node": node,
                    }

    # Custom GPT nodes
    gpt_nodes = {k: v for k, v in all_nodes_seen.items() if v["cls"]["is_custom_gpt"]}
    if gpt_nodes:
        lines.append("### Custom GPT Nodes (LLM)\n")
        lines.append("| Node | Model | Credits | Cost |")
        lines.append("|------|-------|:-------:|:----:|")
        for nid, info in gpt_nodes.items():
            lines.append(f"| {info['cls']['tool_name']} | {info['cls']['model'] or 'N/A'} | {info['credits']} | ${info['cost']} |")
        lines.append("")

    # Integration nodes
    int_nodes = {k: v for k, v in all_nodes_seen.items() if v["cls"]["is_integration"]}
    if int_nodes:
        lines.append("### Integration Nodes\n")
        lines.append("| Node | Type | Credits | Cost |")
        lines.append("|------|------|:-------:|:----:|")
        for nid, info in int_nodes.items():
            tc = info["node"].get("toolConfiguration") or {}
            func = tc.get("toolFunctionName", "")
            lines.append(f"| {info['cls']['tool_name']} | {func} | {info['credits']} | ${info['cost']} |")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Beam agent credit consumption per execution path",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", nargs="?", help="Beam agent URL (e.g., https://app.beam.ai/WORKSPACE/AGENT/flow)")
    parser.add_argument("--workspace-id", help="Workspace ID (if not using URL)")
    parser.add_argument("--agent-id", help="Agent ID (if not using URL)")
    parser.add_argument("--graph-file", help="Path to a local graph JSON file (skip API fetch)")
    parser.add_argument("--base-url", help="API base URL override")
    parser.add_argument("--output", help="Output directory (default: 04-workspace/Smartly/docs)")
    parser.add_argument("--model-override", action="append", metavar="OLD=NEW",
                        help="Override model names, e.g., GEMINI_3_PRO=GPT_5_2")
    parser.add_argument("--pricing-file", help="Path to custom pricing.json")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")

    args = parser.parse_args()

    # Parse model overrides
    model_overrides = {}
    if args.model_override:
        for override in args.model_override:
            if "=" in override:
                old, new = override.split("=", 1)
                model_overrides[old.strip()] = new.strip()

    # Determine workspace/agent IDs
    workspace_id = args.workspace_id
    agent_id = args.agent_id
    base_url = args.base_url

    if args.url:
        ws, ag = parse_beam_url(args.url)
        if ws and ag:
            workspace_id = workspace_id or ws
            agent_id = agent_id or ag
        if not base_url:
            base_url = detect_base_url(args.url)

    base_url = base_url or "https://api.beamstudio.ai"

    # Load env for both Beam API and Notion pricing fetch
    project_root = find_nexus_root()
    env_vars = load_env_file(project_root / ".env")

    # Load pricing (tries live Notion first, falls back to pricing.json)
    pricing = load_pricing(args.pricing_file, env_vars)

    # Get graph data
    graph_data = None

    if args.graph_file:
        print(f"[INFO] Loading graph from file: {args.graph_file}", file=sys.stderr)
        with open(args.graph_file, "r") as f:
            graph_data = json.load(f)
    else:
        if not workspace_id or not agent_id:
            print("[ERROR] Provide a Beam URL or --workspace-id and --agent-id", file=sys.stderr)
            sys.exit(1)

        api_key = env_vars.get("BEAM_API_KEY") or os.getenv("BEAM_API_KEY")
        if not api_key:
            print("[ERROR] BEAM_API_KEY not found in .env or environment", file=sys.stderr)
            sys.exit(1)

        print(f"[INFO] Fetching graph for agent {agent_id}...", file=sys.stderr)
        print(f"  Workspace: {workspace_id}", file=sys.stderr)
        print(f"  Base URL: {base_url}", file=sys.stderr)

        access_token = get_access_token(api_key, base_url)
        if not access_token:
            sys.exit(1)

        graph_data = fetch_agent_graph(access_token, workspace_id, agent_id, base_url)
        if not graph_data:
            sys.exit(1)

    # Analyze
    print("[INFO] Analyzing graph paths...", file=sys.stderr)
    node_map, adjacency, entry_nodes, terminal_nodes, agent_name = build_graph(graph_data)
    all_paths = find_all_paths(adjacency, entry_nodes, terminal_nodes, node_map)
    branches = categorize_paths_into_branches(all_paths, node_map, adjacency, entry_nodes)

    print(f"[INFO] Found {len(all_paths)} paths across {len(branches)} branches", file=sys.stderr)

    graph = graph_data.get("graph", graph_data)
    graph_id = graph.get("id", "unknown")

    # Fallback agent_id from graph data when using --graph-file
    if not agent_id:
        agent_id = graph.get("agentId") or (graph.get("agent") or {}).get("id") or "unknown"

    # Compute all analyses for JSON output
    all_analyses = {}
    path_counter = 0
    for branch_name, paths in branches.items():
        branch_analyses = []
        for path_nodes, edges in paths:
            path_counter += 1
            analysis = analyze_path(path_nodes, node_map, pricing, model_overrides)
            analysis["path_num"] = path_counter
            analysis["description"] = generate_description(path_nodes, edges, node_map)
            branch_analyses.append(analysis)
        all_analyses[branch_name] = branch_analyses

    if args.json:
        output = {
            "agent_name": agent_name,
            "agent_id": agent_id,
            "graph_id": graph_id,
            "total_paths": len(all_paths),
            "branches": {},
        }
        for branch_name, analyses in all_analyses.items():
            output["branches"][branch_name] = [
                {
                    "path": a["path_num"],
                    "description": a["description"],
                    "total_nodes": a["total_nodes"],
                    "total_credits": a["total_credits"],
                    "total_cost": a["total_cost"],
                    "node_counts": a["totals"],
                    "eval_nodes": a["eval_nodes"],
                }
                for a in analyses
            ]
        print(json.dumps(output, indent=2))
    else:
        markdown = generate_markdown(
            agent_name, agent_id, workspace_id, graph_id,
            branches, all_analyses, pricing, node_map, adjacency,
            entry_nodes, model_overrides,
        )

        # Save to file
        output_dir = args.output
        if not output_dir:
            output_dir = str(find_nexus_root() / "04-workspace" / "Smartly" / "docs")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(c for c in agent_name if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
        filename = f"{safe_name}_CREDIT_ANALYSIS.md"
        file_path = output_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"\n[SUCCESS] Analysis saved to: {file_path}", file=sys.stderr)

        # Output JSON metadata for programmatic use
        print(json.dumps({
            "file_path": str(file_path),
            "agent_name": agent_name,
            "agent_id": agent_id,
            "total_paths": len(all_paths),
            "total_branches": len(branches),
        }, indent=2))


if __name__ == "__main__":
    main()
