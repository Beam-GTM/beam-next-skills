---
name: langfuse-delete-traces
version: '1.0'
description: Bulk delete traces. Load when user says 'bulk delete traces', 'delete
  multiple traces', 'purge traces'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Bulk Delete Traces

Delete multiple traces matching filter criteria.

## Usage

```bash
uv run python scripts/delete_traces.py --ids "trace-1,trace-2,trace-3"
uv run python scripts/delete_traces.py --filter '{"name": "test-trace"}'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--ids` | No | Comma-separated trace IDs |
| `--filter` | No | JSON filter object |

## API Reference

```
DELETE /api/public/traces
```
