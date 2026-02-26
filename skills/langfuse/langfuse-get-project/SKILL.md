---
name: langfuse-get-project
version: '1.0'
description: Get Langfuse project info. Load when user says 'get project', 'current
  project', 'project info', 'langfuse project'.
category: integrations
tags:
- langfuse
platform: Langfuse
updated: '2026-02-24'
visibility: public
---
# Get Project

Get the project associated with the current API key.

## Usage

### CLI
```bash
uv run python scripts/get_project.py
```

### Python
```python
from get_project import get_project

project = get_project()
```

## API Reference

```
GET /api/public/projects
```

See: `langfuse-master/references/api-reference.md`
