---
name: langfuse-list-org-projects
version: '1.0'
description: List projects in org. Load when user says 'list org projects', 'org projects',
  'all projects'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Organization Projects

List all projects in an organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/list_org_projects.py --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |

## API Reference

```
GET /api/public/v2/organizations/{orgId}/projects
```
