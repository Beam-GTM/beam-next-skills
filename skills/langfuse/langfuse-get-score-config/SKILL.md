---
name: langfuse-get-score-config
version: '1.0'
description: Get a score config by ID. Load when user says 'get score config', 'show
  metric'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Score Config

Get a specific score configuration by ID.

## Usage

```bash
uv run python scripts/get_score_config.py --id "config-abc123"
```

## API Reference

```
GET /api/public/score-configs/{id}
```
