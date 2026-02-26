---
name: langfuse-list-queue-items
version: '1.0'
description: List queue items. Load when user says 'list queue items', 'show review
  items'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Queue Items

Get items in an annotation queue.

## Usage

```bash
uv run python scripts/list_queue_items.py --queue "queue-abc"
```

## API Reference

```
GET /api/public/annotation-queues/{id}/items
```
