---
name: langfuse-update-org-membership
version: '1.0'
description: Update member role. Load when user says 'update member', 'change role',
  'update membership'.
category: integrations
tags:
- langfuse
- update
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Update Organization Membership

Update a member's role in the organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/update_org_membership.py --org "org-abc123" --membership "mem-xyz" --role "ADMIN"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |
| `--membership` | Yes | Membership ID |
| `--role` | Yes | New role: OWNER, ADMIN, MEMBER, VIEWER |

## API Reference

```
PUT /api/public/v2/organizations/{orgId}/memberships/{membershipId}
```
