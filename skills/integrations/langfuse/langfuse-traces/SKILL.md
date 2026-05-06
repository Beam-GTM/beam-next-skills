---
name: langfuse-traces
type: skill
version: '1.0'
description: Query and manage Langfuse traces, observations, and sessions. Load when user says
  'list traces', 'get trace', 'delete traces', 'list observations', 'list sessions',
  'show spans', 'session details'.
category: integrations
tags:
- langfuse
- traces
- observability
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Traces

Unified skill for traces, observations, and sessions (all read-query + trace deletion).

## Usage

```bash
uv run python scripts/traces.py --resource <resource> --action <action> [options]
```

### Traces

```bash
uv run python scripts/traces.py --resource traces --action list --limit 20
uv run python scripts/traces.py --resource traces --action list --session-id "sess-123" --all
uv run python scripts/traces.py --resource traces --action get --id "trace-uuid"
uv run python scripts/traces.py --resource traces --action delete --id "trace-uuid" --confirm
uv run python scripts/traces.py --resource traces --action delete --ids "t1,t2,t3" --confirm
uv run python scripts/traces.py --resource traces --action delete --filter '{"name":"test"}' --confirm
```

### Observations

```bash
uv run python scripts/traces.py --resource observations --action list --trace-id "trace-uuid"
uv run python scripts/traces.py --resource observations --action get --id "obs-uuid"
```

### Sessions

```bash
uv run python scripts/traces.py --resource sessions --action list --limit 20
uv run python scripts/traces.py --resource sessions --action get --id "session-uuid"
```

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| traces | list | GET | `/api/public/traces` |
| traces | get | GET | `/api/public/traces/{id}` |
| traces | delete | DELETE | `/api/public/traces/{id}` or `/api/public/traces` |
| observations | list | GET | `/api/public/v2/observations` (fallback: `/observations`) |
| observations | get | GET | `/api/public/observations/{id}` |
| sessions | list | GET | `/api/public/sessions` |
| sessions | get | GET | `/api/public/sessions/{id}` |
