---
name: langfuse-admin
type: skill
version: '1.0'
description: Langfuse project and organization administration. Load when user says
  'create project', 'delete project', 'api keys', 'org members', 'list projects',
  'update project', 'manage members'.
category: integrations
tags:
- langfuse
- admin
- projects
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Admin

Unified admin for projects, API keys, and organization management.

## Usage

```bash
uv run python scripts/admin.py --resource <resource> --action <action> [options]
```

### Projects

```bash
uv run python scripts/admin.py --resource projects --action get
uv run python scripts/admin.py --resource projects --action create --name "new-project" --org "org-uuid"
uv run python scripts/admin.py --resource projects --action update --project "proj-uuid" --name "renamed"
uv run python scripts/admin.py --resource projects --action delete --project "proj-uuid"
```

### API Keys

```bash
uv run python scripts/admin.py --resource api-keys --action list --project "proj-uuid"
uv run python scripts/admin.py --resource api-keys --action create --project "proj-uuid" --note "CI key"
uv run python scripts/admin.py --resource api-keys --action delete --project "proj-uuid" --key "key-uuid"
```

### Organization

```bash
uv run python scripts/admin.py --resource org --action list-memberships --org "org-uuid"
uv run python scripts/admin.py --resource org --action update-membership --org "org-uuid" --membership "m-uuid" --role ADMIN
uv run python scripts/admin.py --resource org --action delete-membership --org "org-uuid" --membership "m-uuid"
uv run python scripts/admin.py --resource org --action list-projects --org "org-uuid"
uv run python scripts/admin.py --resource org --action list-api-keys --org "org-uuid"
```

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| projects | get | GET | `/api/public/projects` |
| projects | create | POST | `/api/public/v2/projects` |
| projects | update | PUT | `/api/public/v2/projects/{id}` |
| projects | delete | DELETE | `/api/public/v2/projects/{id}` |
| api-keys | list | GET | `/api/public/v2/projects/{id}/api-keys` |
| api-keys | create | POST | `/api/public/v2/projects/{id}/api-keys` |
| api-keys | delete | DELETE | `/api/public/v2/projects/{id}/api-keys/{keyId}` |
| org | list-memberships | GET | `/api/public/v2/organizations/{id}/memberships` |
| org | update-membership | PUT | `/api/public/v2/organizations/{id}/memberships/{mId}` |
| org | delete-membership | DELETE | `/api/public/v2/organizations/{id}/memberships/{mId}` |
| org | list-projects | GET | `/api/public/v2/organizations/{id}/projects` |
| org | list-api-keys | GET | `/api/public/v2/organizations/{id}/api-keys` |
