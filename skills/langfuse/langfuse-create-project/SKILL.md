---
name: langfuse-create-project
version: '1.0'
description: Create a new project. Load when user says 'create langfuse project',
  'new project'.
category: integrations
tags:
- create
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Create Project

Create a new Langfuse project.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/create_project.py --name "My Project" --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name` | Yes | Project name |
| `--org` | Yes | Organization ID |

## API Reference

```
POST /api/public/v2/projects
```
