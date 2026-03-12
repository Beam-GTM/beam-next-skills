---
name: miro-master
version: '1.0'
description: Shared resource library for Miro integration skills. DO NOT load directly
  - provides common references and scripts used by miro-connect.
author: Mujtaba
category: integrations
tags:
- api
- master
- miro
platform: Miro
updated: '2026-03-12'
visibility: public
---
# Miro Master

**This is NOT a user-facing skill.** It's a shared resource library referenced by Miro integration skills.

## Purpose

Provides shared resources for:
- `miro-connect` - Meta-skill for all Miro operations

## Architecture

All scripts use `miro_client.py` as the shared API client, following the same pattern as the Slack integration.

---

## Authentication

Uses **Access Token** authentication:
- Token stored in `.env` as `MIRO_ACCESS_TOKEN`
- All requests use `Authorization: Bearer {token}` header
- Token can be obtained from Miro developer settings or via OAuth 2.0

---

## Scripts

### Configuration
| Script | Description |
|--------|-------------|
| check_miro_config.py | Pre-flight validation |
| miro_client.py | Shared API client |

### Board Operations
| Script | Description |
|--------|-------------|
| list_boards.py | List accessible boards |
| get_board.py | Get board details |
| create_board.py | Create new board |
| delete_board.py | Delete board |
| copy_board.py | Copy board |

### Item Operations
| Script | Description |
|--------|-------------|
| list_items.py | List items on board (filter by type) |
| create_sticky_note.py | Create sticky note |
| create_card.py | Create card |
| create_shape.py | Create shape |
| create_text.py | Create text item |
| create_frame.py | Create frame / list frame items |
| create_connector.py | Create connector / list connectors |
| create_image.py | Create image from URL |
| create_embed.py | Create embed from URL |
| update_item.py | Get, update position, or delete any item |

### Collaboration
| Script | Description |
|--------|-------------|
| board_members.py | List, add, update, remove members |
| tags.py | Create, list, attach, detach, delete tags |

---

## API Base URL

All API requests go to: `https://api.miro.com/v2/`

---

## Rate Limits

Credit-based system per user per application:
- ~2,000 light requests/min
- ~1,000 medium requests/min
- ~200 heavy requests/min
- HTTP 429 when exceeded (check Retry-After header)

---

## Environment Variables

Required in `.env`:
```
MIRO_ACCESS_TOKEN=your-access-token
```

---

**Version**: 1.0
**Created**: 2026-03-12
**Status**: Production Ready
