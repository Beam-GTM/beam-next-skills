---
name: langfuse-get-score
version: '1.0'
description: Get specific Langfuse score. Load when user says 'get score', 'score
  details', 'show score {id}'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Score

Get detailed view of a specific score.

## Usage

### CLI
```bash
uv run python scripts/get_score.py --id <score_id>
```

### Python
```python
from get_score import get_score

score = get_score("score-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Score ID (required) |

## API Reference

```
GET /api/public/v2/scores/{scoreId}
```

See: `langfuse-master/references/api-reference.md`
