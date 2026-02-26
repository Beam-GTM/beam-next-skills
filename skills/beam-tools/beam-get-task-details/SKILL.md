---
name: beam-get-task-details
version: 1.0
description: Get detailed information about a specific Beam.ai task including status,
  parameters, node execution, and graph state. Load when user says "get task details",
  "task info", "show task", "task status", "what happened with task", or needs to
  inspect a specific task.
author: Hassaan Ahmed
category: integrations
tags:
- beam-ai
platform: Beam AI
updated: '2026-01-02'
visibility: team
---
# Beam Get Task Details

**Retrieve detailed information about a specific Beam.ai task.**

## When to Use

- Check the current status of a task
- View task parameters and input data
- Inspect node execution details
- Debug task issues (parameter extraction, graph state)
- Get task metadata (timestamps, custom IDs)

---

## Prerequisites

`.env` file at project root:

```
# Beam.ai - BID instance (default)
BEAM_API_KEY=your_bid_api_key
BEAM_WORKSPACE_ID=your_bid_workspace_id

# Beam.ai - Production instance
BEAM_API_KEY_PROD=your_prod_api_key
BEAM_WORKSPACE_ID_PROD=your_prod_workspace_id
```

**Dependencies**: `pip install requests python-dotenv`

---

## Quick Start

```bash
# Get task details
python 03-skills/beam-get-task-details/scripts/get_task_details.py <task_id>

# Get task details from production
python 03-skills/beam-get-task-details/scripts/get_task_details.py <task_id> --workspace prod

# Output as JSON
python 03-skills/beam-get-task-details/scripts/get_task_details.py <task_id> --json

# Get multiple tasks
python 03-skills/beam-get-task-details/scripts/get_task_details.py <task_id1> <task_id2> <task_id3>

# Save output to file
python 03-skills/beam-get-task-details/scripts/get_task_details.py <task_id> --output task_details.json
```

---

## Workspaces

| Workspace | API Endpoint | Default |
|-----------|--------------|---------|
| `bid` | api.bid.beamstudio.ai | Yes |
| `prod` | api.beamstudio.ai | No |

---

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `task_ids` | One or more task IDs (required) | - |
| `--workspace`, `-w` | Workspace: bid or prod | bid |
| `--json` | Output as JSON | false |
| `--full` | Show full response (all fields) | false |
| `--output`, `-o` | Save to file | - |

---

## Response Fields

### Core Fields

| Field | Description |
|-------|-------------|
| `id` | Task ID (UUID) |
| `customId` | Custom identifier (if provided) |
| `status` | Task status (COMPLETED, FAILED, IN_PROGRESS, etc.) |
| `createdAt` | Task creation timestamp |
| `updatedAt` | Last update timestamp |
| `completedAt` | Completion timestamp (if completed) |

### Task Statuses

| Status | Description |
|--------|-------------|
| `QUEUED` | Task is queued for execution |
| `IN_PROGRESS` | Task is currently running |
| `COMPLETED` | Task completed successfully |
| `FAILED` | Task failed during execution |
| `ERROR` | Task encountered an error |
| `STOPPED` | Task was stopped (condition failed) |
| `TIMEOUT` | Task timed out |
| `USER_INPUT_REQUIRED` | Task waiting for user input |
| `CANCELLED` | Task was cancelled |

### Node Execution Details

| Field | Description |
|-------|-------------|
| `agentTaskNodes` | Array of node execution data |
| `agentTaskNodes[].toolData` | Node tool configuration and reasoning |
| `agentTaskNodes[].userQuestions` | Required user inputs |

### Graph State

| Field | Description |
|-------|-------------|
| `graphState.current` | Current node in execution |
| `graphState.variables` | Task variables and context |

---

## Example Output

```
Task Details
============================================================

Task ID:     abc123-def456-789...
Custom ID:   INS-12345
Status:      COMPLETED
Created:     2024-01-15T10:30:00Z
Updated:     2024-01-15T10:31:45Z
Completed:   2024-01-15T10:31:45Z

=== EXECUTION ===
Duration:    105 seconds
Nodes:       5 executed

=== NODE DETAILS ===
[1] ParameterExtraction
    Status: completed
    Parameters extracted: company_name, contact_email

[2] DataLookup
    Status: completed
    Tool: hubspot_search

[3] ProcessData
    Status: completed

[4] GenerateOutput
    Status: completed

[5] SendNotification
    Status: completed

=== RESULT ===
{
  "success": true,
  "output": "Task completed successfully"
}
```

---

## API Details

Uses Beam.ai task details endpoint:
- **Endpoint**: `GET /agent-tasks/{taskId}`
- **Response**: HTTP 200 with full task object

---

## Error Handling

| Error | Solution |
|-------|----------|
| `BEAM_API_KEY not found` | Add to .env file |
| `401 Unauthorized` | Verify API key is valid |
| `404 Not Found` | Task ID doesn't exist |

---

## Related Skills

- `beam-get-agent-analytics` - Get agent performance metrics
- `beam-debug-issue-tasks` - Debug failed tasks with Langfuse traces
- `beam-retry-tasks` - Retry failed tasks
