---
name: langfuse-get-session
version: '1.0'
description: Get specific Langfuse session. Load when user says 'get session', 'session
  details', 'show session {id}'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Session

Get detailed view of a specific session with its traces.

## Usage

### CLI
```bash
uv run python scripts/get_session.py --id <session_id>
```

### Python
```python
from get_session import get_session

session = get_session("session-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Session ID (required) |

## API Reference

```
GET /api/public/sessions/{sessionId}
```

See: `langfuse-master/references/api-reference.md`
