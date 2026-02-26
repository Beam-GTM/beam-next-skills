---
name: langfuse-get-dataset
version: '1.0'
description: Get a Langfuse dataset by name. Load when user says 'get dataset', 'show
  dataset', 'dataset details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Dataset

Retrieve a specific dataset from Langfuse by name.

## Usage

### CLI
```bash
uv run python scripts/get_dataset.py --name "my-dataset"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Dataset name |

## API Reference

```
GET /api/public/v2/datasets/{datasetName}
```
