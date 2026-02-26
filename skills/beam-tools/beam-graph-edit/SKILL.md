---
name: beam-graph-edit
version: '1.0'
description: Edit Beam agent graph nodes — update prompts, input/output param descriptions,
  and push changes via PUT. Load when user says 'edit beam graph', 'update beam node',
  'change beam prompt', 'push graph changes', 'modify agent graph', 'update param
  description', or needs to modify a live Beam agent's graph configuration. Uses the
  proven GET-clean-modify-PUT cycle that bypasses the unreliable PATCH endpoint.
author: Anas Duksi
category: integrations
tags:
- beam-ai
- update
platform: Beam AI
updated: '2026-02-19'
visibility: team
---
# Beam Graph Edit

Edit Beam agent graph nodes and push changes reliably via the PUT full-graph approach.

## Purpose

Modify prompts, input/output parameter descriptions, and node configurations on live Beam agents. Uses the safe GET-clean-modify-PUT cycle.

---

## Prerequisites

- Beam configured (`.env` has `BEAM_API_KEY` and `BEAM_WORKSPACE_ID`)
- Agent name or ID
- What to change (prompt text, param description, etc.)

---

## Workflow

### Step 0: Pre-Flight

```bash
/usr/local/bin/python3.13 00-system/skills/beam/beam-master/scripts/check_beam_config.py --json
```

If not configured, follow beam-master setup.

### Step 1: Identify Agent

If user provides name but not ID:

```bash
/usr/local/bin/python3.13 00-system/skills/beam/beam-master/scripts/list_agents.py --json
```

Match by name, confirm with user, note the agent ID.

### Step 2: GET Graph and Show Summary

```bash
/usr/local/bin/python3.13 00-system/skills/beam/beam-master/scripts/get_agent_graph.py --agent-id AGENT_ID --json
```

Parse the response. Show user a summary:

```
Graph for: [Agent Name]
Nodes: [count]

 #  | Objective                    | toolFunctionName
----|------------------------------|---------------------------
 1  | Identify department          | GPTAction_Custom_Dept_Xxx
 2  | Process email input          | GPTAction_Custom_Proc_Yyy
 3  | Send escalation email        | MicrosoftOutlookCC_Zzz
```

Use `beam_graph_utils.summarize_graph()` for this.

### Step 3: Confirm Target and Changes

Ask user:
- Which node(s) to modify (by # or toolFunctionName)
- What to change: prompt, input param description, or output param description

### Step 4: Load Gotchas

Before making changes, read:
```
00-system/skills/beam/beam-master/references/graph-push-gotchas.md
```

### Step 5: Apply Changes

Write a Python snippet using beam_graph_utils:

```python
import sys, json
sys.path.insert(0, '00-system/skills/beam/beam-master/scripts')
from beam_client import get_client
from beam_graph_utils import (
    prepare_graph_for_put,
    find_node_by_tool_function,
    update_node_prompt,
    update_param_description,
)

AGENT_ID = "..."
client = get_client()

# GET and clean
response = client.get(f'/agent-graphs/{AGENT_ID}')
payload = prepare_graph_for_put(response)
nodes = payload['nodes']

# Find target node (ALWAYS by toolFunctionName, never by ID)
node = find_node_by_tool_function(nodes, 'TOOL_FUNCTION_NAME')

# Apply change (one of):
update_node_prompt(node, NEW_PROMPT_TEXT)
update_param_description(node, 'output', 'param_name', NEW_DESC)
update_param_description(node, 'input', 'param_name', NEW_DESC)

# Save payload
with open('/tmp/beam_graph_payload.json', 'w') as f:
    json.dump(payload, f, indent=2)
```

**Show the diff to user before pushing** (old vs new values).

### Step 6: Push

Dry-run first:
```bash
/usr/local/bin/python3.13 03-skills/beam-graph-edit/scripts/push_graph.py \
  --agent-id AGENT_ID --payload-file /tmp/beam_graph_payload.json --dry-run
```

Then push:
```bash
/usr/local/bin/python3.13 03-skills/beam-graph-edit/scripts/push_graph.py \
  --agent-id AGENT_ID --payload-file /tmp/beam_graph_payload.json
```

Add `--save-and-publish` to publish immediately.

### Step 7: Verify

The push script auto-verifies node count. For detailed verification, GET the graph again and check specific fields by matching on `toolFunctionName`.

If saved as draft: "Changes saved as draft. Open Beam UI to re-link any LINKED inputs if needed."

---

## Common Edit Patterns

### Update a Prompt
```python
update_node_prompt(node, """Your new prompt here...""")
```

### Update an Output Param Description
```python
update_param_description(node, 'output', 'identification_result', """{
  "field": "new schema description"
}""")
```

### Update an Input Param Description
```python
update_param_description(node, 'input', 'email_address', """New description...""")
```

### Batch Edit Multiple Nodes
```python
edits = {
    'GPTAction_Custom_Tool1': {'prompt': 'new prompt...'},
    'GPTAction_Custom_Tool2': {'params': [
        {'type': 'output', 'name': 'result', 'description': 'new desc'}
    ]},
}
for fn_name, changes in edits.items():
    node = find_node_by_tool_function(nodes, fn_name)
    if changes.get('prompt'):
        update_node_prompt(node, changes['prompt'])
    for pc in changes.get('params', []):
        update_param_description(node, pc['type'], pc['name'], pc['description'])
```

---

## Scripts

**[push_graph.py](scripts/push_graph.py)** — CLI for pushing cleaned graph payloads
```bash
python push_graph.py --agent-id ID --payload-file FILE [--dry-run] [--clean] [--save-and-publish] [--json]
```

## External References (from beam-master)

- **[beam_graph_utils.py](../../00-system/skills/beam/beam-master/scripts/beam_graph_utils.py)** — Shared cleaning and modification functions
- **[graph-push-gotchas.md](../../00-system/skills/beam/beam-master/references/graph-push-gotchas.md)** — All known API quirks
- **[api-reference.md](../../00-system/skills/beam/beam-master/references/api-reference.md)** — Full Beam API docs

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|---------|
| PATCH "Cannot read properties of undefined" | Unreliable PATCH endpoint | Use this skill's PUT workflow |
| PUT 400 validation errors | Unstripped server fields | Use `prepare_graph_for_put()` |
| Prompt not updating | GET/PUT path asymmetry | Use `update_node_prompt()` |
| Node ID not found after push | IDs regenerate on PUT | Match by `toolFunctionName` |
| Output param validation error | Missing `isArray` | `clean_output_param()` auto-adds it |

---

## Related Skills

- **beam-connect** — General Beam operations
- **beam-prompt-builder** — Build prompt configurations from scratch
- **graph-slicer** — Read-only graph documentation (complements this edit skill)
