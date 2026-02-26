---
name: langfuse-create-annotation-queue
version: '1.0'
description: Create an annotation queue. Load when user says 'create queue', 'new
  annotation queue'.
category: integrations
tags:
- create
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Create Annotation Queue

Create a new annotation queue for human review.

## Usage

```bash
uv run python scripts/create_annotation_queue.py --name "review-queue" --description "Production review"
```

## API Reference

```
POST /api/public/annotation-queues
```
