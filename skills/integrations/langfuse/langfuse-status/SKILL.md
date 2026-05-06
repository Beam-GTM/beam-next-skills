---
name: langfuse-status
type: skill
version: '1.0'
description: Check Langfuse health and usage metrics. Load when user says 'health check',
  'is langfuse up', 'metrics', 'usage stats', 'check status'.
category: integrations
tags:
- langfuse
- monitoring
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Status

Health checks and usage metrics (v1 + v2).

## Usage

```bash
uv run python scripts/status.py --action health
uv run python scripts/status.py --action metrics
```

## API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| health | GET | `/api/public/health` |
| metrics | GET | `/api/public/metrics` |
