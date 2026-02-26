---
name: langfuse-delete-queue-item
version: '1.0'
description: Delete a queue item. Load when user says 'delete queue item', 'remove
  from queue'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Queue Item

Remove an item from annotation queue.

## Usage

```bash
uv run python scripts/delete_queue_item.py --queue "queue-abc" --item "item-xyz"
```

## API Reference

```
DELETE /api/public/annotation-queues/{id}/items/{itemId}
```
