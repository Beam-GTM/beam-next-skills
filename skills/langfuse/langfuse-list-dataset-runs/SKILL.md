---
name: langfuse-list-dataset-runs
version: '1.0'
description: List dataset runs. Load when user says 'list dataset runs', 'show runs',
  'dataset experiments'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Dataset Runs

Get list of evaluation runs for a dataset.

## Usage

### CLI
```bash
uv run python scripts/list_dataset_runs.py --name "my-dataset"
uv run python scripts/list_dataset_runs.py --name "my-dataset" --limit 10
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Dataset name |
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/datasets/{datasetName}/runs
```
