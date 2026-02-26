---
name: langfuse-delete-prompt
version: '1.0'
description: Delete a Langfuse prompt. Load when user says 'delete prompt', 'remove
  prompt'.
category: integrations
tags:
- delete
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Delete Prompt

Delete a prompt from Langfuse by name. This deletes all versions of the prompt.

## Usage

### CLI
```bash
uv run python scripts/delete_prompt.py --name "my-prompt"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Prompt name to delete |

## API Reference

```
DELETE /api/public/v2/prompts/{promptName}
```

**Warning**: This deletes all versions of the prompt. This action cannot be undone.
