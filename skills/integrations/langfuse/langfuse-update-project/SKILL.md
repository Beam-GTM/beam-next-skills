---
name: langfuse-update-project
version: '1.0'
description: Update project settings. Load when user says 'update project', 'rename
  project'.
category: integrations
tags:
- langfuse
- update
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Update Project

Update project settings.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/update_project.py --project "proj-abc" --name "New Name"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |
| `--name` | No | New project name |

## API Reference

```
PUT /api/public/v2/projects/{projectId}
```
