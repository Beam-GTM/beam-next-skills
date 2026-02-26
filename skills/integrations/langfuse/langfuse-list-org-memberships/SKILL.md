---
name: langfuse-list-org-memberships
version: '1.0'
description: List organization members. Load when user says 'list members', 'org members',
  'who has access'.
category: integrations
tags:
- langfuse
- query
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# List Organization Memberships

List all members of an organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/list_org_memberships.py --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |

## API Reference

```
GET /api/public/v2/organizations/{orgId}/memberships
```
