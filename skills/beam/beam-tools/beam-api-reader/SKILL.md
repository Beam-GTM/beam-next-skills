---
name: beam-api-reader
version: '1.0'
description: Comprehensive Beam AI API reference with all endpoints, authentication,
  request/response schemas, and usage examples. Load when user says "beam api", "api
  reference", "beam endpoints", "how to call beam api", "beam api docs", or needs
  to interact with the Beam AI REST API.
author: Danyal Sandeelo
category: integrations
tags:
- api
- beam-ai
- reference
platform: Beam AI
updated: '2026-03-05'
visibility: team
---
# Beam API Reader

**Complete reference for the Beam AI REST API — all endpoints, authentication, schemas, and examples.**

## When to Use

- Look up Beam AI API endpoints and their parameters
- Understand authentication requirements for API calls
- Create, list, or inspect agent tasks via the API
- Build, update, or configure agents and workflows programmatically
- Manage agent setup, views, context files, and tool optimization
- Connect via MCP (Model Context Protocol)

---

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Production  | `https://api.beamlearning.io` |
| BID (Dev)   | `https://api.bid.beamstudio.ai` |
| MCP Server  | `https://api.beamstudio.ai/mcp` |

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
| PATCH | `/agent-graphs/{agentId}/nodes/{nodeId}/prompt` | Update node tool prompt |
| PATCH | `/agent-graphs/{agentId}/nodes/{nodeId}/input-output-params` | Update node I/O parameters |
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

### Tool Optimization

| Method | Endpoint | Description |
|--------|----------|-------------|
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
| [tool-endpoints.md](references/tool-endpoints.md) | Tool optimization endpoints |
| [context-files-endpoints.md](references/context-files-endpoints.md) | Context file download |
| [mcp-connection.md](references/mcp-connection.md) | MCP server connection and available tools |
| [response-schemas.md](references/response-schemas.md) | Common response objects and status codes |

---

## Quick Example

```python
import requests

API_KEY = "your-api-key"
WORKSPACE_ID = "your-workspace-id"
BASE_URL = "https://api.beamlearning.io"

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

## Related Skills

- `beam-get-agent-analytics` — Get agent performance metrics
- `beam-get-task-details` — Get details for a specific task
- `beam-debug-issue-tasks` — Debug failed tasks
- `beam-retry-tasks` — Retry failed tasks
