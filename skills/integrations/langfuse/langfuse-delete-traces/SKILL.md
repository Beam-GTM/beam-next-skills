---
name: langfuse-delete-traces
type: skill
version: '1.1'
description: Delete one trace or bulk-delete traces. Load when user says 'delete trace',
  'remove trace', 'bulk delete traces', 'delete multiple traces', 'purge traces'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Delete Traces

Delete a **single** trace by ID, or **multiple** traces by ID list or filter.

## Usage

**Single trace** (same as former `langfuse-delete-trace`):

```bash
uv run python scripts/delete_traces.py --id "trace-abc123"
```

**Bulk** — comma-separated IDs:

```bash
uv run python scripts/delete_traces.py --ids "trace-1,trace-2,trace-3"
```

**Bulk** — JSON filter:

```bash
uv run python scripts/delete_traces.py --filter '{"name": "test-trace"}'
```

Add `--confirm` for non-interactive scripts.

## Parameters

| Mode | Parameters | API |
|------|------------|-----|
| Single | `--id` (required) | `DELETE /api/public/traces/{traceId}` |
| Bulk | `--ids` and/or `--filter` | `DELETE /api/public/traces` |

## API Reference

```
DELETE /api/public/traces/{traceId}
DELETE /api/public/traces
```
