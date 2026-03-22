---
name: langfuse-models
type: skill
version: '1.0'
description: Manage Langfuse model definitions for cost tracking. Load when user says
  'list models', 'create model', 'get model', 'delete model', 'model costs'.
category: integrations
tags:
- langfuse
- models
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Models

Unified CRUD for model definitions (cost tracking, tokenizer config).

## Usage

```bash
uv run python scripts/models.py --action <action> [options]
```

```bash
uv run python scripts/models.py --action list
uv run python scripts/models.py --action get --id "model-uuid"
uv run python scripts/models.py --action create --name "gpt-4o" --match-pattern "gpt-4o.*" --unit TOKENS --input-price 0.0025 --output-price 0.01
uv run python scripts/models.py --action delete --id "model-uuid"
```

## API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| list | GET | `/api/public/models` |
| get | GET | `/api/public/models/{id}` |
| create | POST | `/api/public/models` |
| delete | DELETE | `/api/public/models/{id}` |
