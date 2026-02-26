---
name: langfuse-delete-score
version: '1.0'
description: Delete a score. Load when user says 'delete score', 'remove evaluation'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Score

Delete a score by ID.

## Usage

```bash
uv run python scripts/delete_score.py --id "score-abc123"
```

## API Reference

```
DELETE /api/public/scores/{id}
```
