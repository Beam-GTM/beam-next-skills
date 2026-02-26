---
name: langfuse-delete-dataset-item
version: '1.0'
description: Delete a dataset item. Load when user says 'delete dataset item', 'remove
  item'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Dataset Item

Delete a dataset item by ID.

## Usage

### CLI
```bash
uv run python scripts/delete_dataset_item.py --id "item-abc123"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | **Required**. Item ID to delete |

## API Reference

```
DELETE /api/public/dataset-items/{id}
```
