---
name: langfuse-prompts
type: skill
version: '1.0'
description: Manage Langfuse prompts and prompt versions. Load when user says 'list prompts',
  'create prompt', 'get prompt', 'delete prompt', 'update prompt version'.
category: integrations
tags:
- langfuse
- prompts
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Prompts

Unified CRUD for prompts and prompt version management.

## Usage

```bash
uv run python scripts/prompts.py --action <action> [options]
```

```bash
uv run python scripts/prompts.py --action list --limit 50
uv run python scripts/prompts.py --action get --name "my-prompt" --version 2
uv run python scripts/prompts.py --action create --name "my-prompt" --prompt "You are a helpful assistant" --type text
uv run python scripts/prompts.py --action create --name "chat-prompt" --prompt '[{"role":"system","content":"Hi"}]' --type chat
uv run python scripts/prompts.py --action delete --name "my-prompt"
uv run python scripts/prompts.py --action update-version --name "my-prompt" --version 1 --labels "production,latest"
```

## API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| list | GET | `/api/public/v2/prompts` |
| get | GET | `/api/public/v2/prompts/{name}` |
| create | POST | `/api/public/v2/prompts` |
| delete | DELETE | `/api/public/v2/prompts/{name}` |
| update-version | PATCH | `/api/public/v2/prompts/{name}/versions/{version}` |
