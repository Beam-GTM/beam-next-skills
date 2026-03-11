---
name: create-beam-agent
version: '1.0'
description: Create a Beam AI agent from a YAML description by generating a JSON spec
  and deploying it via the complete graph API. Load when user says "create beam agent",
  "deploy beam agent", "build a beam agent", "create agent from yaml", or provides
  a YAML agent spec and wants it deployed to Beam.
author: Danyal Sandeelo
category: integrations
tags:
- beam-ai
- create
- agent
- graph
platform: Beam AI
updated: '2026-03-11'
visibility: team
---
# Create Beam Agent

Deploy a Beam agent from a YAML description using `scripts/create_agent_from_prompt.py`.
The skill translates the YAML into a typed JSON spec and calls the Beam complete graph API.

---

## Prerequisites

- `BEAM_API_KEY` and `BEAM_WORKSPACE_ID` set in `.env`
- `requests` Python package installed (`pip3 install requests`)
- Script at `scripts/create_agent_from_prompt.py` (in project root)

---

## Key Rules (must follow every time)

1. **Entry node is always bare** — no `toolConfiguration`, no params, no prompt. Objective = `"Entry Node"`. If the YAML marks a processing node as `is_entry: true`, create a **separate** bare entry node and connect it to that processing node.

2. **`toolFunctionName` is auto-generated** by the script as `GPTAction_Custom_{CamelCaseName}` from the `tool_name`. Never set it manually in the spec.

3. **Linked params use `linked_node` + `linked_param`** in the spec (not `linked_node_id` as YAML may use). `linked_node` = the `key` of the source node in the spec.

4. **Spec node keys** = snake-case IDs matching the YAML `id` fields. The script generates all UUIDs — never put UUIDs in the spec.

5. **`on_error: "CONTINUE"`** only for non-critical nodes (e.g. Slack notifications). All others use `"STOP"`.

---

## Spec Format

```json
{
  "agentName": "string",
  "agentDescription": "string",
  "personality": "string",
  "restrictions": "string",
  "prompts": ["example prompt 1", "example prompt 2"],
  "nodes": [
    {
      "key": "entry",
      "objective": "Entry Node",
      "is_entry": true,
      "x": 250, "y": 0,
      "edges": [{ "target": "first-processing-node", "name": "", "condition": "" }]
    },
    {
      "key": "node-key",
      "name": "Tool Display Name",
      "objective": "What this node does",
      "is_entry": false,
      "x": 250, "y": 200,
      "model": "BEDROCK_CLAUDE_SONNET_4",
      "tool_name": "Tool Display Name",
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
          "description": "what this param is",
          "type": "string|object|number|boolean",
          "is_array": false,
          "fill_type": "static|linked|user_fill|ai_fill",
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
          "description": "what this output contains",
          "type": "string|object|number|boolean",
          "is_array": false,
          "output_example": null,
          "position": 0
        }
      ],
      "edges": [
        { "target": "next-node-key", "name": "Edge label", "condition": "" }
      ]
    }
  ]
}
```

### Positioning
- Linear flow: entry at `y=0`, processing nodes at `y=200`, x increases by 300 per step
- Conditional branches: fan out with y offsets (e.g. y=0 / y=300 / y=600)

### fill_type values
| Value | When to use |
|---|---|
| `static` | Fixed hardcoded value — set `static_value` |
| `linked` | Flows from a parent node's output — set `linked_node` + `linked_param` |
| `user_fill` | User provides at runtime (first processing node inputs) |
| `ai_fill` | AI extracts from conversation context automatically |

### Available models
- `BEDROCK_CLAUDE_SONNET_4` — default, fast, most tasks
- `BEDROCK_CLAUDE_OPUS_4_5` — complex generation/reasoning

### Conditional edges
- Unconditional: `"condition": ""`
- Conditional: `"condition": "sum is odd"` / `"condition": "status is approved"` etc.

---

## Workflow

### Step 1: Parse the YAML

Read the YAML agent spec and extract:
- Agent-level: `name`, `description`, `personality`, `restrictions`, `prompts`
- For each node: `id` (→ key), `objective`, `x/y`, `on_error`, retry settings, `tool.*`, `edges`
- For each input param: `name`, `description`, `type`, `fill_type`, `static_value`, `linked_node_id` (→ `linked_node`), `linked_param`, `required`, `position`, `is_array`
- For each output param: `name`, `description`, `type`, `is_array`, `position`

### Step 2: Build the Spec JSON

Apply the rules:
- Prepend a bare entry node that connects to the first processing node
- Set `is_entry: false` on all processing nodes (even if YAML said `is_entry: true`)
- Map YAML `linked_node_id` → spec `linked_node` (uses the `key` / YAML `id` value)
- Set positions: entry at y=0, processing nodes at y=200, x increments by 300

### Step 3: Write Spec to Temp File

Write the spec JSON to `/tmp/beam_agent_spec.json`.

### Step 4: Dry Run

```bash
python3 scripts/create_agent_from_prompt.py --spec-file /tmp/beam_agent_spec.json --dry-run 2>&1 | head -30
```

Verify the node summary output looks correct (node names, input/output counts, linked params).

### Step 5: Create Agent

```bash
python3 scripts/create_agent_from_prompt.py --spec-file /tmp/beam_agent_spec.json
```

Report the Agent ID and Draft Graph ID to the user.

---

## Example: 4-node linear agent

Given YAML with nodes: extract → transform → generate-report → notify

Spec nodes:
```
entry (bare, y=0) → extract-yardi-data (y=200, x=250) → transform-validate (y=200, x=550) → generate-report (y=200, x=850) → notify-team (y=200, x=1150)
```

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Linked param 'node.param' not found` | `linked_node` or `linked_param` typo | Check the source node's `key` and output param `name` match exactly |
| `API Error 400` | Malformed payload | Run `--dry-run`, inspect JSON for missing fields |
| `API Error 401` | Bad API key | Check `BEAM_API_KEY` in `.env` |
| Agent created but nodes empty | Wrong `toolFunctionName` prefix | Script auto-handles — ensure `tool_name` is set on every non-entry node |

---

## Script Reference

**[create_agent_from_prompt.py](../../../../scripts/create_agent_from_prompt.py)**

```
Usage:
  python3 scripts/create_agent_from_prompt.py --spec-file FILE
  python3 scripts/create_agent_from_prompt.py --spec-file FILE --dry-run
  echo '<json>' | python3 scripts/create_agent_from_prompt.py

What it does:
  - Pre-generates UUIDs for all nodes, tool configs, output params
  - Resolves linked params by UUID lookup
  - Builds originalTool block (required by API)
  - POSTs to /agent-graphs/complete (draft status)
  - Returns Agent ID, Draft Graph ID, Active Graph ID
```
