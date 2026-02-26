---
name: langfuse-metrics
version: '1.0'
description: Get Langfuse metrics. Load when user says 'metrics', 'usage stats', 'langfuse
  usage'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Metrics

Get metrics and usage statistics from Langfuse.

## Usage

```bash
uv run python scripts/metrics.py
```

## Parameters

None required.

## API Reference

```
GET /api/public/metrics
```
