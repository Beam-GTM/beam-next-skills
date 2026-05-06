---
name: beam-api-reader
version: '2.0'
description: Comprehensive Beam AI API reference with all endpoints, authentication,
  request/response schemas, usage examples, and full agent creation workflow. Load
  when user says "beam api", "api reference", "beam endpoints", "how to call beam
  api", "beam api docs", "create beam agent", "deploy beam agent", "build a beam agent",
  "create agent from yaml", or needs to interact with the Beam AI REST API or deploy
  a new agent.
author: Danyal Sandeelo
category: integrations
tags:
- api
- beam-ai
- reference
- create
- agent
platform: Beam AI
updated: '2026-04-06'
visibility: team
---
# Beam API Reader

**Complete reference for the Beam AI REST API — all endpoints, authentication, schemas, examples, and agent creation workflow.**

## When to Use

- Look up Beam AI API endpoints and their parameters
- Understand authentication requirements for API calls
- Create, list, or inspect agent tasks via the API
- Build, update, or configure agents and workflows programmatically
- **Create a new Beam agent from a YAML description**
- Manage agent setup, views, context files, and tool optimization
- Connect via MCP (Model Context Protocol)

---

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Enterprise (Americana) | `https://api.enterprise.beamstudio.ai` |
| Standard   | `https://api.beamstudio.ai` |
| BID (Dev)   | `https://api.bid.beamstudio.ai` |
| MCP Server  | `https://api.beamstudio.ai/mcp` |

> **CRITICAL**: Always use `BEAM_API_URL` from `.env` as the base URL. Do NOT hardcode `api.beamlearning.io` — it no longer resolves. Americana Foods workspace is on the **enterprise** instance (`api.enterprise.beamstudio.ai`). Using the wrong base URL returns a different agent with the same ID.

---

## Authentication

All requests require:

| Header | Description |
|--------|-------------|
| `x-api-key` | Your Beam AI API key |
| `current-workspace-id` | Your workspace identifier |

See [authentication.md](references/authentication.md) for setup details and code examples.

---

## API Endpoints Summary

### User

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/user/me` | Get current authenticated user and workspaces |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agent` | List agents in workspace (paginated, filterable) |

### Agent Graph (Workflow)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agent-graphs/{agentId}` | Get full agent workflow graph |
| GET | `/agent-graphs/{agentId}/nodes/lite` | Get graph nodes (without tool config) |
| GET | `/agent-graphs/{agentId}/nodes/{nodeId}` | Get detailed node information |
| POST | `/agent-graphs/complete` | Create new agent with complete graph |
| PUT | `/agent-graphs/{agentId}` | Update agent and its draft graph |
| PATCH | `/agent-graphs/update-node` | Update a graph node |
| PATCH | `/agent-graphs/{graphId}/publish` | Publish draft graph as active |
| PATCH | `/agent-graphs/{agentId}/nodes/{nodeId}/prompt` | Update node tool prompt |
| PATCH | `/agent-graphs/{agentId}/nodes/{nodeId}/input-output-params` | Update node I/O parameters |
| POST | `/agent-graphs/add-node` | Add a new node to draft graph |
| POST | `/agent-graphs/add-edge` | Add a new edge between nodes |
| PUT | `/agent-graphs/update-edge/{edgeId}` | Update edge condition |
| POST | `/agent-graphs/test-node` | Test a node in isolation |
| GET | `/agent-graphs/agent-task-nodes/{toolFunctionName}` | Get task nodes by tool |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent-tasks` | Create a new agent task |
| GET | `/agent-tasks` | List tasks (paginated, filterable, groupable) |
| GET | `/agent-tasks/{taskId}` | Get detailed task information |
| GET | `/agent-tasks/{taskId}/updates` | Subscribe to real-time task updates (SSE) |
| GET | `/agent-tasks/iterate` | Navigate through tasks (next/previous) |
| POST | `/agent-tasks/retry` | Retry a failed task |
| PATCH | `/agent-tasks/execution/{taskId}/user-input` | Submit user input for paused task |
| POST | `/agent-tasks/execution/{taskId}/user-consent` | Approve task (HITL) |
| POST | `/agent-tasks/execution/{taskId}/rejection` | Reject task (HITL) |
| PATCH | `/agent-tasks/execution/{taskId}/output-rating` | Rate task output |
| GET | `/agent-tasks/analytics` | Get agent analytics and metrics |

### Agent Setup

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent-setup/upload` | Upload context files during setup |
| POST | `/agent-setup/{agentId}/context-file` | Add context files to existing agent |
| POST | `/agent-setup/agent-context/feedback` | Submit context feedback |
| GET | `/agent-setup/session/{agentId}` | Get setup session state |
| POST | `/agent-setup` | Process setup steps (multi-step) |

### Agent Views

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agent-views` | List all views |
| GET | `/agent-views/{viewId}/records` | List records from a view |
| GET | `/agent-views/{viewId}/columns/{columnId}/links/{recordId}` | List linked records |

### Context Files

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/context/agent/{agentId}/file/{fileId}/download` | Download a context file |

### Tools, Optimization & Models

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tool/active-tools` | Search/list active tools (filter by type, keyword) |
| GET | `/custom-tool/preferred-models` | Get list of available/preferred LLM models |
| POST | `/tool/optimize/{toolFunctionName}` | Optimize tool performance |
| POST | `/tool/optimization-status/thread/{threadId}` | Check optimization status |

---

## Reference Documents

| Document | Contents |
|----------|----------|
| [authentication.md](references/authentication.md) | API key setup, headers, code examples |
| [user-endpoints.md](references/user-endpoints.md) | User profile and workspace endpoint |
| [agent-endpoints.md](references/agent-endpoints.md) | Agent listing + all graph/workflow endpoints |
| [task-endpoints.md](references/task-endpoints.md) | Task CRUD, SSE, HITL, rating, analytics |
| [agent-setup-endpoints.md](references/agent-setup-endpoints.md) | Agent setup flow and configuration |
| [agent-views-endpoints.md](references/agent-views-endpoints.md) | Structured data views and records |
| [tool-endpoints.md](references/tool-endpoints.md) | Tool search, attach to node, optimization |
| [context-files-endpoints.md](references/context-files-endpoints.md) | Context file download |
| [mcp-connection.md](references/mcp-connection.md) | MCP server connection and available tools |
| [response-schemas.md](references/response-schemas.md) | Common response objects and status codes |

---

## Quick Example

```python
import requests

API_KEY = "your-api-key"
WORKSPACE_ID = "your-workspace-id"
BASE_URL = os.getenv("BEAM_API_URL", "https://api.enterprise.beamstudio.ai")

headers = {
    "x-api-key": API_KEY,
    "current-workspace-id": WORKSPACE_ID,
    "Content-Type": "application/json"
}

# List agents
response = requests.get(f"{BASE_URL}/agent", headers=headers)
agents = response.json()

# Create a task
task_payload = {
    "agentId": "your-agent-id",
    "taskQuery": { "query": "Process this request" }
}
response = requests.post(f"{BASE_URL}/agent-tasks", headers=headers, json=task_payload)
task = response.json()

# Update a node prompt
prompt_payload = { "prompt": "Extract customer name and email." }
response = requests.patch(
    f"{BASE_URL}/agent-graphs/AGENT_ID/nodes/NODE_ID/prompt",
    headers=headers, json=prompt_payload
)
```

---

---

## Create Agent from YAML

Deploy a new Beam agent from a YAML description using `scripts/create_agent_from_prompt.py`.

### Key Rules

1. **Entry node is always bare** — no tool config, no params, no prompt. Objective = `"Entry Node"`. If the YAML marks a processing node as `is_entry: true`, prepend a separate bare entry node and connect it to that processing node.
2. **`toolFunctionName` is auto-generated** by the script as `GPTAction_Custom_{CamelCaseName}` — never set manually.
3. **Linked params use `linked_node` + `linked_param`** in the spec. `linked_node` = the `key` of the source node (= YAML `id` value). YAML may call this field `linked_node_id` — remap it.
4. **No UUIDs in the spec** — the script generates all UUIDs.
5. **`on_error: "CONTINUE"`** only for non-critical nodes (e.g. Slack notifications). All others: `"STOP"`.
6. **Loop nodes** (`node_type: "loopingNode"`) must have ≥1 child. Children set `parent_node: "<loop-key>"`; the script resolves it to `parentNodeId`.

### Spec Format

```json
{
  "agentName": "string",
  "agentDescription": "string",
  "personality": "string",
  "restrictions": "string",
  "prompts": ["example prompt 1"],
  "nodes": [
    {
      "key": "entry",
      "objective": "Entry Node",
      "is_entry": true,
      "x": 250, "y": 0,
      "edges": [{ "target": "first-node-key", "name": "", "condition": "" }]
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
          "fill_type": "user_fill",
          "fill_type_options": "user_fill (default)|ai_fill|static|linked|from_memory",
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
      "edges": [{ "target": "next-key", "name": "Edge label", "condition": "" }]
    }
  ]
}
```

**Positioning:** entry at `y=0`, processing nodes at `y=200`, x increments by 300 per step.
**Models:** `BEDROCK_CLAUDE_SONNET_4` (default) or `BEDROCK_CLAUDE_OPUS_4_5` (complex generation).
**Conditional edges:** `"condition": ""` = unconditional; `"condition": "sum is odd"` = conditional branch.

### Loop Nodes

A loop node (`node_type: "loopingNode"`) has no `toolConfiguration`. Its children live alongside it in the top-level `nodes[]` array, but each child carries `"parent_node": "<loop-key>"` so the script sets `parentNodeId` to the loop's UUID.

**Auto-assigned by the script — do not set manually:**
- Loop `objective` is always `"N: Loop"` (1-based across all loops in the agent; first loop → `"1: Loop"`, second → `"2: Loop"`, …). Any `objective` you put on a loop is overwritten.
- Child nodes inside a loop get a numeric `alias` (`"1"`, `"2"`, `"3"`, …) in the order they appear in the spec, stored on the child's `nodeConfigurations.alias`. The loop itself has no alias.

**Rules:**
- A loop must have at least one child (validated).
- Loops cannot be nested — a `loopingNode` cannot have `parent_node` set (validated).

```json
{
  "key": "my-loop",
  "node_type": "loopingNode",
  "x": 250, "y": 200,
  "loop_config": {
    "iteration_count": 3,
    "linked_variable_node": null,
    "linked_variable_param": null
  },
  "edges": [{ "target": "after-loop", "name": "", "condition": "" }]
},
{
  "key": "loop-body",
  "name": "Process Item",
  "objective": "Process a single iteration",
  "parent_node": "my-loop",
  "x": 550, "y": 200,
  "tool_name": "Process Item",
  "prompt": "…",
  "input_params": [...],
  "output_params": [...],
  "edges": []
}
```

Use `iteration_count` for count-based loops, or `linked_variable_node` + `linked_variable_param` for variable-based loops (the script resolves these to `linkedVariableId` + `linkedAgentGraphNodeId`).

### Workflow

**Step 1: Parse YAML**
Extract agent metadata and all node definitions. Map YAML `linked_node_id` → spec `linked_node`.

**Step 2: Build spec JSON**
- Prepend a bare entry node connecting to the first processing node
- All processing nodes: `is_entry: false`
- Write to `/tmp/beam_agent_spec.json`

**Step 3: Dry run**
```bash
python3 scripts/create_agent_from_prompt.py --spec-file /tmp/beam_agent_spec.json --dry-run 2>&1 | head -30
```
Verify node names, input/output counts, and linked params look correct.

**Step 4: Create agent**
```bash
python3 scripts/create_agent_from_prompt.py --spec-file /tmp/beam_agent_spec.json
```
Report Agent ID and Draft Graph ID to the user.

### Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Linked param 'node.param' not found` | `linked_node`/`linked_param` typo | Check source node `key` and output param `name` match exactly |
| `API Error 400` | Malformed payload | Run `--dry-run`, inspect JSON |
| `API Error 401` | Bad API key | Check `BEAM_API_KEY` in `.env` |
| Agent created but nodes empty | Wrong tool function prefix | Ensure `tool_name` is set on every non-entry node |

---

## Related Skills

- `beam-get-agent-analytics` — Get agent performance metrics
- `beam-get-task-details` — Get details for a specific task
- `beam-debug-issue-tasks` — Debug failed tasks
- `beam-retry-tasks` — Retry failed tasks
