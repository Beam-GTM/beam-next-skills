---
name: langfuse-list-models
version: '1.0'
description: List Langfuse models. Load when user says 'list models', 'show models',
  'model costs'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Models

Get list of configured models (for cost tracking).

## Usage

### CLI
```bash
uv run python scripts/list_models.py
uv run python scripts/list_models.py --limit 20
```

### Python
```python
from list_models import list_models

models = list_models()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/models
```

See: `langfuse-master/references/api-reference.md`
