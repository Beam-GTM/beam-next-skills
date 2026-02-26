---
name: langfuse-create-queue-item
version: '1.0'
description: Add item to queue. Load when user says 'add to queue', 'queue trace for
  review'.
category: integrations
tags:
- create
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Create Queue Item

Add a trace/observation to an annotation queue.

## Usage

```bash
uv run python scripts/create_queue_item.py --queue "queue-abc" --trace "trace-xyz"
```

## API Reference

```
POST /api/public/annotation-queues/{id}/items
```
