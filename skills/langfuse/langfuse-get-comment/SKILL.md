---
name: langfuse-get-comment
version: '1.0'
description: Get comment by ID. Load when user says 'get comment', 'show comment',
  'comment details'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Comment

Retrieve a specific comment by ID.

## Usage

```bash
uv run python scripts/get_comment.py --comment "comment-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--comment` | Yes | Comment ID |

## API Reference

```
GET /api/public/comments/{commentId}
```
