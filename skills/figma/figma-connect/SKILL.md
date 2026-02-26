---
name: figma-connect
version: '1.0'
description: Connect to any Figma file for data extraction and asset export. Load
  when user mentions 'connect figma', 'get figma file', 'figma URL', 'export from
  figma', 'figma assets', or provides a Figma file URL.
author: Mo Bekdache
category: general
tags:
- connector
- figma
platform: Figma
updated: '2025-12-24'
visibility: public
---
# Figma Connect

> **Purpose**: Connect to any Figma file and perform operations
>
> **Trigger**: "connect figma", "get figma file", Figma URL provided
>
> **Duration**: 1-2 minutes

---

## Prerequisites

1. `FIGMA_ACCESS_TOKEN` must be set in `.env`
2. Token must have access to the target file

---

## Workflow

### Step 1: Validate Configuration

Check that Figma token is configured:

```bash
python 00-system/skills/figma/figma-master/scripts/fetch_file.py --check-config
```

If not configured, guide user to:
1. Get token from Figma Settings → Account → Personal access tokens
2. Add to `.env`: `FIGMA_ACCESS_TOKEN=figd_xxxxx`

---

### Step 2: Parse File URL

Extract file key from Figma URL:
- URL format: `https://www.figma.com/design/FILE_KEY/File-Name`
- Extract: `FILE_KEY`

---

### Step 3: Fetch File Data

```bash
python 00-system/skills/figma/figma-master/scripts/fetch_file.py --file-key FILE_KEY --depth 2
```

Returns:
- File name and last modified date
- Page list with IDs
- Top-level frame structure

---

### Step 4: User Action Selection

Present options:
1. **Get styles** - Extract colors, typography, effects
2. **List components** - Show all components
3. **Export assets** - Download images/icons
4. **Create snapshot** - Full design system dump

Execute selected action using figma-master scripts.

---

## Available Operations

| Operation | Script | Description |
|-----------|--------|-------------|
| Fetch file | `fetch_file.py` | Get file structure |
| Get styles | `get_styles.py` | Extract design tokens |
| Get components | `get_components.py` | List components |
| Export assets | `export_assets.py` | Download images |
| Snapshot | `snapshot_design_system.py` | Full JSON export |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Token doesn't have file access | Share file with integration |
| 404 Not Found | Invalid file key | Check URL is correct |
| 429 Rate Limited | Too many requests | Wait and retry |

---

**Version**: 1.0
**Created**: 2025-12-24

