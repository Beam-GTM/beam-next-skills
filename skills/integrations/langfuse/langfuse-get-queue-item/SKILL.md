---
name: langfuse-get-queue-item
version: '1.0'
description: Get a queue item. Load when user says 'get queue item', 'item details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Queue Item

Get a specific queue item.

## Usage

```bash
uv run python scripts/get_queue_item.py --queue "queue-abc" --item "item-xyz"
```

## API Reference

```
GET /api/public/annotation-queues/{id}/items/{itemId}
```
