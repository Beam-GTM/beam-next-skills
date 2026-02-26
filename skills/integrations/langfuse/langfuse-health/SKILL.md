---
name: langfuse-health
version: '1.0'
description: Check Langfuse health status. Load when user says 'health check', 'is
  langfuse up', 'check status'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Health Check

Check the health status of the Langfuse instance.

## Usage

```bash
uv run python scripts/health.py
```

## Parameters

None required.

## API Reference

```
GET /api/public/health
```
