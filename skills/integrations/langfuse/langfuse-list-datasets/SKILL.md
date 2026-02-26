---
name: langfuse-list-datasets
version: '1.0'
description: List Langfuse datasets. Load when user says 'list datasets', 'show datasets',
  'get datasets'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Datasets

Get list of datasets from Langfuse for experiment evaluation.

## Usage

### CLI
```bash
uv run python scripts/list_datasets.py
uv run python scripts/list_datasets.py --limit 20
uv run python scripts/list_datasets.py --page 2
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number for pagination |

## API Reference

```
GET /api/public/v2/datasets
```
