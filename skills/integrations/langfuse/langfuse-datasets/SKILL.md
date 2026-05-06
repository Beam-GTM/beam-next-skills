---
name: langfuse-datasets
type: skill
version: '1.0'
description: Manage Langfuse datasets, items, runs, and run-items. Load when user says
  'list datasets', 'create dataset', 'get dataset', 'dataset items', 'dataset runs',
  'add test case', 'evaluation results', 'delete dataset item', 'delete dataset run'.
category: integrations
tags:
- datasets
- langfuse
- evaluation
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Datasets

Unified skill for Langfuse dataset management — datasets, items, runs, and run-items.

Replaces: `langfuse-list-datasets`, `langfuse-create-dataset`, `langfuse-get-dataset`, `langfuse-list-dataset-items`, `langfuse-create-dataset-item`, `langfuse-get-dataset-item`, `langfuse-delete-dataset-item`, `langfuse-list-dataset-runs`, `langfuse-get-dataset-run`, `langfuse-delete-dataset-run`, `langfuse-list-dataset-run-items`, `langfuse-create-dataset-run-item`.

## Usage

All operations go through a single script with `--resource` and `--action`:

```bash
uv run python scripts/datasets.py --resource <resource> --action <action> [options]
```

### Datasets

```bash
# List datasets
uv run python scripts/datasets.py --resource datasets --action list --limit 50

# List all datasets (paginated)
uv run python scripts/datasets.py --resource datasets --action list --all

# Create a dataset
uv run python scripts/datasets.py --resource datasets --action create --name "my-eval-set" --description "Regression tests"

# Get a dataset by name
uv run python scripts/datasets.py --resource datasets --action get --name "my-eval-set"
```

### Dataset Items

```bash
# List items (optionally filter by dataset)
uv run python scripts/datasets.py --resource items --action list --dataset "my-eval-set"

# Create an item (test case)
uv run python scripts/datasets.py --resource items --action create \
  --dataset "my-eval-set" \
  --input '{"query": "What is LangChain?"}' \
  --expected '{"answer": "A framework for LLM apps"}'

# Get item by ID
uv run python scripts/datasets.py --resource items --action get --id "item-uuid"

# Delete item
uv run python scripts/datasets.py --resource items --action delete --id "item-uuid"
```

### Dataset Runs

```bash
# List runs for a dataset
uv run python scripts/datasets.py --resource runs --action list --dataset "my-eval-set"

# Get a specific run
uv run python scripts/datasets.py --resource runs --action get --dataset "my-eval-set" --run "run-name"

# Delete a run
uv run python scripts/datasets.py --resource runs --action delete --dataset "my-eval-set" --run "run-name"
```

### Dataset Run Items

```bash
# List run items (filter by dataset and/or run)
uv run python scripts/datasets.py --resource run-items --action list --dataset "my-eval-set" --run "run-name"

# Create a run item (log an evaluation result)
uv run python scripts/datasets.py --resource run-items --action create \
  --run "run-name" --dataset-item "item-uuid" --trace "trace-uuid"
```

## Common Options

| Option | Description |
|--------|-------------|
| `--limit` | Max results per page (default 50, max 100) |
| `--page` | Page number (default 1) |
| `--all` | Fetch all pages (for list actions) |
| `--max-pages` | Stop after N pages with `--all` |
| `--output`, `-o` | Write JSON to file instead of stdout |

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| datasets | list | GET | `/api/public/v2/datasets` |
| datasets | create | POST | `/api/public/v2/datasets` |
| datasets | get | GET | `/api/public/v2/datasets/{name}` |
| items | list | GET | `/api/public/dataset-items` |
| items | create | POST | `/api/public/dataset-items` |
| items | get | GET | `/api/public/dataset-items/{id}` |
| items | delete | DELETE | `/api/public/dataset-items/{id}` |
| runs | list | GET | `/api/public/datasets/{name}/runs` |
| runs | get | GET | `/api/public/datasets/{name}/runs/{run}` |
| runs | delete | DELETE | `/api/public/datasets/{name}/runs/{run}` |
| run-items | list | GET | `/api/public/dataset-run-items` |
| run-items | create | POST | `/api/public/dataset-run-items` |
