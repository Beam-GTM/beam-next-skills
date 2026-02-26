---
name: langfuse-delete-dataset-run
version: '1.0'
description: Delete a dataset run. Load when user says 'delete dataset run', 'remove
  run'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Dataset Run

Delete a specific evaluation run from a dataset.

## Usage

### CLI
```bash
uv run python scripts/delete_dataset_run.py --dataset "my-dataset" --run "run-2024-01"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | **Required**. Dataset name |
| --run | string | **Required**. Run name to delete |

## API Reference

```
DELETE /api/public/datasets/{datasetName}/runs/{runName}
```
