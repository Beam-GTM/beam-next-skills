---
name: langfuse-delete-queue-assignment
version: '1.0'
description: Remove reviewer from queue. Load when user says 'remove assignment',
  'unassign reviewer'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Queue Assignment

Remove a user assignment from annotation queue.

## Usage

```bash
uv run python scripts/delete_queue_assignment.py --queue "queue-abc" --user "user@email.com"
```

## API Reference

```
DELETE /api/public/annotation-queues/{id}/assignments
```
