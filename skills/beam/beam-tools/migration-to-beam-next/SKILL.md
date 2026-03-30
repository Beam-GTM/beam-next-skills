---
name: migration-to-beam-next
description: Migrate Nexus skills to Beam Next. Package a Nexus skill as a .skill zip and upload it to a Beam agent via the import skill API. Use when migrating, importing, or uploading skills from Nexus to Beam.
---

# Migration To Beam Next

Migrate Nexus skills into Beam Next by packaging them and uploading via the Beam import skill API.

## Purpose

- Package an existing Nexus skill directory into a `.skill` zip file
- Upload the packaged skill to a target Beam agent using `POST /agent/{agentId}/skills/import`
- Supports dry-run mode to verify before uploading

## Workflow

### Step 1: Identify the Nexus Skill

Locate the Nexus skill directory to migrate. Verify it follows the required zip structure:

```
skill-name/
├── SKILL.md          (required — instructions and metadata)
├── references/       (optional — supporting documentation)
├── scripts/          (optional — executable scripts)
└── assets/           (optional — images and other files)
```

### Step 2: Package the Skill

Package the Nexus skill into a `.skill` zip file using the existing packaging script:

```bash
python3 skills/general/create-skill/scripts/package_skill.py <path/to/nexus-skill>
```

This validates the structure and creates a `.skill` zip file preserving the folder layout above.

If the skill is already packaged as a `.skill` or `.zip` file with the correct structure, skip this step.

### Step 3: Upload to Beam

The script fetches the user's workspaces on the fly via `GET /v2/user/me`, presents them for selection, then uses the chosen workspace's `id` and `agent.id` to upload.

```bash
python3 skills/beam/beam-tools/migration-to-beam-next/scripts/upload_skill.py <path-to-file.skill>
```

The script will:
1. Fetch workspaces using `BEAM_API_KEY`
2. Display available workspaces for selection
3. Extract `workspace.id` (for auth header) and `workspace.agent.id` (for URL path)
4. Upload the `.skill` file to `POST /agent/{agentId}/skills/import`

**Flags:**
- `--dry-run` — print request details without calling the API
- `--base-url` — override API base URL (default: `https://api.beamstudio.ai`)

**Required environment variable** (in `.env`):
- `BEAM_API_KEY`

### Step 4: Verify

Confirm the API response shows `success: true` and note the `destination` value.

## API Reference

**Workspace fetch:** `GET /v2/user/me`
- Returns `workspaces[]` array, each with `id`, `name`, and nested `agent.id`

**Skill import:** `POST /agent/{agentId}/skills/import`

| Detail | Value |
|--------|-------|
| Content-Type | multipart/form-data |
| Auth headers | `x-api-key`, `current-workspace-id` |
| Body field | `file` (binary zip) |
| Success | 201 Created |
| Errors | 400 (invalid file), 401 (auth required) |
