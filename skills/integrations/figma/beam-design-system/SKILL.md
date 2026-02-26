---
name: beam-design-system
version: '1.0'
description: Access Beam's cached design system tokens and components. Load when user
  mentions 'beam design system', 'beam colors', 'beam typography', 'design tokens',
  'brand colors', 'beam fonts', or asks about Beam's design standards.
author: Mo Bekdache
category: integrations
tags:
- figma
platform: Figma
updated: '2025-12-24'
visibility: public
---
# Beam Design System

> **Purpose**: Instant access to Beam's design tokens without API calls
>
> **Trigger**: "beam colors", "beam typography", "design tokens", "brand guidelines"
>
> **Source**: Figma Slides - Design System

---

## Quick Access

The design system is cached locally in `design-system.json`. No API calls needed for lookups.

### Available Data

| Category | Examples |
|----------|----------|
| **Colors** | Primary, secondary, semantic colors |
| **Typography** | Font families, sizes, weights |
| **Effects** | Shadows, blurs |
| **Components** | Buttons, cards, inputs, etc. |
| **Grids** | Layout grids, spacing |

---

## Usage

### Get Colors
```
User: "What are Beam's brand colors?"
AI: [Reads design-system.json → styles.colors]
```

### Get Typography
```
User: "What fonts does Beam use?"
AI: [Reads design-system.json → styles.typography]
```

### Get Components
```
User: "What components are in the design system?"
AI: [Reads design-system.json → components]
```

---

## Files

| File | Purpose |
|------|---------|
| `design-system.json` | Full cached snapshot |
| `design-tokens.md` | Human-readable token reference |
| `refresh.md` | How to update the snapshot |

---

## Refresh Snapshot

To pull latest from Figma:

```bash
python 00-system/skills/figma/figma-master/scripts/snapshot_design_system.py \
  --file-key NKGz63c6mGJSDadOzaU3oJ \
  --output 00-system/skills/figma/beam-design-system/design-system.json
```

---

## Source File

- **Name**: Figma Slides - Design System
- **Key**: `NKGz63c6mGJSDadOzaU3oJ`
- **URL**: https://www.figma.com/design/NKGz63c6mGJSDadOzaU3oJ

---

**Version**: 1.0
**Created**: 2025-12-24
**Last Snapshot**: See design-system.json → meta.snapshot_date

