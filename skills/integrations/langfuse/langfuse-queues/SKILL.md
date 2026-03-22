---
name: langfuse-queues
type: skill
version: '1.0'
description: Manage Langfuse annotation queues, items, and assignments. Load when user says
  'list queues', 'create queue', 'annotation queues', 'queue items', 'assign reviewer',
  'unassign reviewer', 'annotate item'.
category: integrations
tags:
- langfuse
- annotation
- queues
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Annotation Queues

Unified skill for annotation queues, queue items, and reviewer assignments.

## Usage

```bash
uv run python scripts/queues.py --resource <resource> --action <action> [options]
```

### Queues

```bash
uv run python scripts/queues.py --resource queues --action list --limit 50
uv run python scripts/queues.py --resource queues --action create --name "review-queue" --description "Human review"
uv run python scripts/queues.py --resource queues --action get --id "queue-uuid"
```

### Queue Items

```bash
uv run python scripts/queues.py --resource items --action list --queue "queue-uuid"
uv run python scripts/queues.py --resource items --action create --queue "queue-uuid" --trace "trace-uuid"
uv run python scripts/queues.py --resource items --action get --queue "queue-uuid" --item "item-uuid"
uv run python scripts/queues.py --resource items --action update --queue "queue-uuid" --item "item-uuid" --status COMPLETED
uv run python scripts/queues.py --resource items --action delete --queue "queue-uuid" --item "item-uuid"
```

### Assignments

```bash
uv run python scripts/queues.py --resource assignments --action create --queue "queue-uuid" --user "user@example.com"
uv run python scripts/queues.py --resource assignments --action delete --queue "queue-uuid" --user "user@example.com"
```

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| queues | list | GET | `/api/public/annotation-queues` |
| queues | create | POST | `/api/public/annotation-queues` |
| queues | get | GET | `/api/public/annotation-queues/{id}` |
| items | list | GET | `/api/public/annotation-queues/{id}/items` |
| items | create | POST | `/api/public/annotation-queues/{id}/items` |
| items | get | GET | `/api/public/annotation-queues/{id}/items/{itemId}` |
| items | update | PATCH | `/api/public/annotation-queues/{id}/items/{itemId}` |
| items | delete | DELETE | `/api/public/annotation-queues/{id}/items/{itemId}` |
| assignments | create | POST | `/api/public/annotation-queues/{id}/assignments` |
| assignments | delete | DELETE | `/api/public/annotation-queues/{id}/assignments` |
