---
name: langfuse-get-observation
version: '1.0'
description: Get specific Langfuse observation. Load when user says 'get observation',
  'observation details', 'show span {id}'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Observation

Get detailed view of a specific observation.

## Usage

### CLI
```bash
uv run python scripts/get_observation.py --id <observation_id>
```

### Python
```python
from get_observation import get_observation

obs = get_observation("obs-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Observation ID (required) |

## API Reference

```
GET /api/public/observations/{observationId}
```

See: `langfuse-master/references/api-reference.md`
