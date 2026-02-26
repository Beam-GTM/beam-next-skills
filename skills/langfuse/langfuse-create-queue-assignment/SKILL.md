---
name: langfuse-create-queue-assignment
version: '1.0'
description: Assign reviewer to queue. Load when user says 'assign reviewer', 'add
  to queue assignment'.
category: integrations
tags:
- create
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Create Queue Assignment

Assign a user to an annotation queue.

## Usage

```bash
uv run python scripts/create_queue_assignment.py --queue "queue-abc" --user "user@email.com"
```

## API Reference

```
POST /api/public/annotation-queues/{id}/assignments
```
