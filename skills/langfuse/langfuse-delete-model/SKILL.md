---
name: langfuse-delete-model
version: '1.0'
description: Delete a model definition. Load when user says 'delete model', 'remove
  model'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Model

Delete a model definition by ID.

## Usage

```bash
uv run python scripts/delete_model.py --id "model-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--id` | Yes | Model ID |

## API Reference

```
DELETE /api/public/models/{modelId}
```
