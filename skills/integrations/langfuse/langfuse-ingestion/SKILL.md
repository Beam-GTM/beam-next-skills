---
name: langfuse-ingestion
type: skill
version: '1.0'
description: Langfuse data ingestion, comments, and media. Load when user says
  'batch ingest', 'otel ingest', 'opentelemetry', 'list comments', 'create comment',
  'get media', 'upload media', 'bulk import'.
category: integrations
tags:
- langfuse
- ingestion
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Ingestion

Unified skill for batch ingestion, OpenTelemetry ingest, comments, and media.

## Usage

```bash
uv run python scripts/ingestion.py --resource <resource> --action <action> [options]
```

### Batch Ingest

```bash
uv run python scripts/ingestion.py --resource batch --action ingest --file events.json
uv run python scripts/ingestion.py --resource batch --action ingest --data '[{"type":"trace-create",...}]'
```

### OpenTelemetry Ingest

```bash
uv run python scripts/ingestion.py --resource otel --action ingest --file spans.json
uv run python scripts/ingestion.py --resource otel --action ingest --data '[{"resource":...}]'
```

### Comments

```bash
uv run python scripts/ingestion.py --resource comments --action list --type TRACE --object-id "trace-uuid"
uv run python scripts/ingestion.py --resource comments --action get --id "comment-uuid"
uv run python scripts/ingestion.py --resource comments --action create --type TRACE --object-id "trace-uuid" --content "Looks good"
```

### Media

```bash
uv run python scripts/ingestion.py --resource media --action get --id "media-uuid"
uv run python scripts/ingestion.py --resource media --action update --id "media-uuid" --uploaded
uv run python scripts/ingestion.py --resource media --action upload-url --trace "trace-uuid" --field "input" --type "image/png"
```

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| batch | ingest | POST | `/api/public/ingestion` |
| otel | ingest | POST | `/api/public/otel/v1/traces` |
| comments | list | GET | `/api/public/comments` |
| comments | get | GET | `/api/public/comments/{id}` |
| comments | create | POST | `/api/public/comments` |
| media | get | GET | `/api/public/media/{id}` |
| media | update | PATCH | `/api/public/media/{id}` |
| media | upload-url | POST | `/api/public/media` |
