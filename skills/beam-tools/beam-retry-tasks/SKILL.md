---
name: beam-retry-tasks
version: '1.0'
description: Retry failed Beam.ai tasks. Load when user says "retry tasks", "rerun
  failed tasks", "retry beam tasks", "resubmit tasks", or needs to re-execute failed
  agent tasks.
author: Jack Li
category: integrations
tags:
- beam-ai
platform: Beam AI
updated: '2025-12-15'
visibility: public
---
# Beam Retry Tasks

**Retry failed or stopped Beam.ai tasks using the retry API.**

## When to Use

- Retry tasks that failed due to transient errors (API timeouts, 400/500 errors)
- Re-execute tasks after fixing underlying issues
- Batch retry multiple failed tasks from an agent

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
# Retry a single task
python 03-skills/beam-retry-tasks/scripts/retry_tasks.py --task-id <task_id>

# Retry all FAILED tasks from an agent (last 1 day)
python 03-skills/beam-retry-tasks/scripts/retry_tasks.py --agent <agent_id>

# Retry from JSON file (output from debug_issue_tasks.py)
python 03-skills/beam-retry-tasks/scripts/retry_tasks.py --file /tmp/failed_tasks.json

# Dry run (preview without executing)
python 03-skills/beam-retry-tasks/scripts/retry_tasks.py --agent <agent_id> --dry-run
```

---

## Workspaces

| Workspace | API Endpoint | Default |
|-----------|--------------|---------|
| `bid` | api.bid.beamstudio.ai | Yes |
| `prod` | api.beamstudio.ai | No |

---

## Retryable Statuses

By default, retries these statuses:
- `FAILED` - Task execution failed
- `ERROR` - Processing error
- `STOPPED` - Condition failed
- `TIMEOUT` - Execution timeout

Use `--status` to customize:
```bash
python retry_tasks.py --agent abc123 --status FAILED --status STOPPED
```

---

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--task-id`, `-t` | Single task ID to retry | - |
| `--agent`, `-a` | Agent ID - retry all issue tasks | - |
| `--file`, `-f` | JSON file with task IDs | - |
| `--status`, `-s` | Status to include (repeatable) | FAILED, ERROR, STOPPED, TIMEOUT |
| `--days`, `-d` | Look back period (1,3,7,14,30) | 1 |
| `--limit`, `-l` | Max tasks to retry | 100 |
| `--workspace`, `-w` | Workspace: bid or prod | bid |
| `--dry-run` | Preview without executing | false |
| `--delay` | Delay between retries (seconds) | 0.2 |
| `--output`, `-o` | Save results to JSON file | - |

---

## Input Formats

### Single Task
```bash
python retry_tasks.py --task-id abc123-def456-...
```

### From Agent
```bash
python retry_tasks.py --agent 455269b0-4d8d-4071-a8a0-6b07450462aa --days 7
```

### From JSON File

Supports multiple formats:

**Array of task objects:**
```json
[
  {"task_id": "abc123", "custom_id": "INS-001"},
  {"task_id": "def456", "custom_id": "INS-002"}
]
```

**Array of strings:**
```json
["abc123", "def456", "ghi789"]
```

---

## Example Output

```
Workspace: bid
API Base: https://api.bid.beamstudio.ai

Fetching FAILED, ERROR, STOPPED, TIMEOUT tasks from agent 455269b0...
Look back: 1 day(s)

Found 55 tasks to retry

============================================================
Retrying 55 tasks...
Started: 2025-12-15T09:22:31

[  1/55] OK INS-29980 (0351632e...)
[  2/55] OK INS-30137 (289bbb78...)
[  3/55] OK INS-30138 (e5b5aa28...)
...
[ 55/55] OK INS-30298 (678327b2...)

============================================================

=== SUMMARY ===
Total tasks: 55
Successfully retried: 55
Failed to retry: 0
```

---

## Integration with Debug Skill

Use with `beam-debug-issue-tasks` for a complete workflow:

```bash
# 1. Debug and identify failed tasks
python 03-skills/beam-debug-issue-tasks/scripts/debug_issue_tasks.py <agent_id> \
  --days 7 --output /tmp/failed_tasks.json

# 2. Review the output
cat /tmp/failed_tasks.json

# 3. Retry all failed tasks
python 03-skills/beam-retry-tasks/scripts/retry_tasks.py \
  --file /tmp/failed_tasks.json --output /tmp/retry_results.json
```

---

## API Details

Uses Beam.ai retry endpoint:
- **Endpoint**: `POST /agent-tasks/retry`
- **Body**: `{"taskId": "<task_id>"}`
- **Response**: HTTP 201 (success, empty body)

**Rate limiting**: Built-in 0.2s delay between requests (configurable with `--delay`)

**Retry logic**: Automatically retries on 502, 503, 504 errors

---

## Error Handling

| Error | Solution |
|-------|----------|
| `BEAM_API_KEY not found` | Add to .env file |
| `401 Unauthorized` | Verify API key is valid |
| `404 Not Found` | Task ID doesn't exist |
| `503 Service Unavailable` | Transient error, will auto-retry |

---

## Related Skills

- `beam-debug-issue-tasks` - Find failed tasks and diagnose root cause
- `beam-create-agent-task` - Create new tasks
- `beam-list-agents` - List available agents
