---
name: langfuse-delete-project
version: '1.0'
description: Delete a project. Load when user says 'delete project', 'remove project'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Project

Delete a Langfuse project.

**Warning**: This is a destructive operation and cannot be undone.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/delete_project.py --project "proj-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |

## API Reference

```
DELETE /api/public/v2/projects/{projectId}
```
