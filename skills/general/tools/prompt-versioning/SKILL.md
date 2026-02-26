---
name: prompt-versioning
version: '1.0'
description: Manage AI prompts with version control, rollback, and Linear integration.
  Load when user mentions 'prompt versioning', 'version prompt', 'rollback prompt',
  'prompt history', 'create prompt version', or needs to manage prompts across client
  projects.
author: Anas Duksi
category: general
updated: '2026-01-12'
visibility: team
---
# Prompt Versioning Skill

> Standardized prompt management for client projects with version control, rollback, and Linear integration.

## Overview

This skill provides a consistent way to manage AI prompts across client projects. It tracks versions, links changes to Linear tickets, and enables easy rollback when needed.

## Commands

| Command | Description |
|---------|-------------|
| `prompt init` | Initialize prompt versioning in current project |
| `prompt create <name>` | Create a new prompt |
| `prompt version <name>` | Create new version of existing prompt |
| `prompt list` | List all prompts and their versions |
| `prompt get <name> [version]` | Get prompt content |
| `prompt diff <name> <v1> <v2>` | Compare two versions |
| `prompt set-current <name> <version>` | Set production version |
| `prompt rollback <name> <version>` | Rollback to previous version |

## Usage Examples

### Initialize in a project
```bash
python prompt_init.py --project americana
```

### Create a new prompt
```bash
python prompt_create.py --name consolidation --description "Merge email data with Airtable state"
```

### Create a new version
```bash
python prompt_version.py --name consolidation --ticket CLI-4442 --change "Fixed dash to minus extraction"
```

### List all prompts
```bash
python prompt_list.py
```

### Get current production prompt
```bash
python prompt_get.py --name consolidation
```

### Get specific version
```bash
python prompt_get.py --name consolidation --version v1
```

### Compare versions
```bash
python prompt_diff.py --name consolidation --v1 v1 --v2 v2
```

### Set production version
```bash
python prompt_set_current.py --name consolidation --version v2
```

## File Structure

```
{project}/02-resources/prompts/
├── .prompt-config.yaml      ← Configuration and version tracking
├── REGISTRY.md              ← Auto-generated human-readable index
└── {prompt-name}/
    ├── v1.md                ← Version 1
    ├── v2.md                ← Version 2
    └── ...
```

## Configuration

The `.prompt-config.yaml` file tracks all prompts and versions:

```yaml
project: americana
created: 2026-01-12
prompts:
  consolidation:
    description: "Merge email data with Airtable state"
    current: v2
    beam_node_id: null
    versions:
      v1:
        date: 2026-01-05
        ticket: null
        change: "Initial version"
      v2:
        date: 2026-01-12
        ticket: CLI-4442
        change: "Added dash fix"
```

## Integration

- **Linear**: Link version changes to tickets for traceability
- **Beam**: Optionally track which Beam node uses which prompt
- **Nexus**: Works with any Nexus project structure

## Best Practices

1. **Always create a new version** before making changes
2. **Link to Linear tickets** for audit trail
3. **Write clear change descriptions** for future reference
4. **Test before setting current** - use `prompt get` to review
5. **Use diff** to compare before rollback
