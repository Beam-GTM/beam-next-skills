---
name: langfuse-list-annotation-queues
version: '1.0'
description: List annotation queues. Load when user says 'list queues', 'annotation
  queues', 'review queues'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Annotation Queues

Get list of annotation queues for human review.

## Usage

```bash
uv run python scripts/list_annotation_queues.py
```

## API Reference

```
GET /api/public/annotation-queues
```
