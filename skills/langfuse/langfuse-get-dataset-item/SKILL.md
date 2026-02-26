---
name: langfuse-get-dataset-item
version: '1.0'
description: Get a dataset item by ID. Load when user says 'get dataset item', 'show
  item', 'item details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Dataset Item

Retrieve a specific dataset item by ID.

## Usage

### CLI
```bash
uv run python scripts/get_dataset_item.py --id "item-abc123"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | **Required**. Item ID |

## API Reference

```
GET /api/public/dataset-items/{id}
```
