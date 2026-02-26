---
name: langfuse-otel-ingest
version: '1.0'
description: Ingest OpenTelemetry data. Load when user says 'otel ingest', 'opentelemetry',
  'otlp'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# OpenTelemetry Ingest

Ingest OpenTelemetry Protocol (OTLP) data into Langfuse.

## Usage

```bash
uv run python scripts/otel_ingest.py --file otel_spans.json
uv run python scripts/otel_ingest.py --spans '[...]'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--file` | No | JSON file with OTLP spans |
| `--spans` | No | JSON string of resource spans |

## OTLP Format

```json
{
  "resourceSpans": [
    {
      "resource": { "attributes": [...] },
      "scopeSpans": [
        {
          "spans": [...]
        }
      ]
    }
  ]
}
```

## API Reference

```
POST /api/public/otel/v1/traces
```
