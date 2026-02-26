---
name: langfuse-get-annotation-queue
version: '1.0'
description: Get an annotation queue. Load when user says 'get queue', 'queue details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Annotation Queue

Get an annotation queue by ID.

## Usage

```bash
uv run python scripts/get_annotation_queue.py --id "queue-abc"
```

## API Reference

```
GET /api/public/annotation-queues/{id}
```
