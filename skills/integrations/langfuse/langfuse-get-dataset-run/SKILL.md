---
name: langfuse-get-dataset-run
version: '1.0'
description: Get a dataset run by name. Load when user says 'get dataset run', 'show
  run', 'run details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Dataset Run

Retrieve a specific evaluation run from a dataset.

## Usage

### CLI
```bash
uv run python scripts/get_dataset_run.py --dataset "my-dataset" --run "run-2024-01"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | **Required**. Dataset name |
| --run | string | **Required**. Run name |

## API Reference

```
GET /api/public/datasets/{datasetName}/runs/{runName}
```
