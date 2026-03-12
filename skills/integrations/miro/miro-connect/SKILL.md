---
name: miro-connect
version: '1.0'
description: Connect to Miro for board management, sticky notes, cards, shapes, frames,
  connectors, and collaboration. Load when user mentions 'miro', 'miro board', 'sticky
  note', 'whiteboard', or any Miro operations. Meta-skill that validates config and
  routes to appropriate operations.
author: Mujtaba
category: integrations
tags:
- connector
- miro
platform: Miro
updated: '2026-03-12'
visibility: public
---
# Miro Connect

**Entry point for all Miro operations.** Validates configuration and routes requests to appropriate scripts.

## Trigger Phrases

Load this skill when user says:
- "miro" / "connect miro" / "miro connect"
- "miro board" / "list boards" / "create board"
- "sticky note" / "add sticky" / "create card on miro"
- "whiteboard" / "miro frame"
- Any reference to Miro operations

---

## Quick Reference

**Check configuration:**
```bash
python3 00-system/skills/miro/miro-master/scripts/check_miro_config.py --json
```

---

## Workflow

### Step 1: Validate Configuration

**Always run first:**

```bash
python3 00-system/skills/miro/miro-master/scripts/check_miro_config.py --json
```

**If `ai_action` is `proceed_with_operation`:**
- Continue to Step 2

**If `ai_action` is `add_access_token`:**
1. Tell user: "Miro needs an access token. Add MIRO_ACCESS_TOKEN to your .env file."
2. Guide them to https://developers.miro.com to create an app and get a token

**If `ai_action` is `refresh_token`:**
1. Tell user: "Your Miro token may be expired. Please generate a new one."

---

### Step 2: Identify User Intent

| User Says | Route To |
|-----------|----------|
| "list miro boards" | Boards > list_boards.py |
| "get board details" | Boards > get_board.py |
| "create a board" | Boards > create_board.py |
| "delete board" | Boards > delete_board.py |
| "copy board" | Boards > copy_board.py |
| "list items on board" | Items > list_items.py |
| "add sticky note" | Items > create_sticky_note.py |
| "create card" | Items > create_card.py |
| "add shape" | Items > create_shape.py |
| "add text" | Items > create_text.py |
| "create frame" | Items > create_frame.py |
| "connect items" | Items > create_connector.py |
| "add image" | Items > create_image.py |
| "embed URL" | Items > create_embed.py |
| "move/update item" | Items > update_item.py |
| "delete item" | Items > update_item.py --delete |
| "board members" | Members > board_members.py --list |
| "invite to board" | Members > board_members.py --add |
| "manage tags" | Tags > tags.py |

---

### Step 3: Execute Operation

Use the appropriate script from `miro-master/scripts/`:

#### Board Operations

**List boards:**
```bash
python3 00-system/skills/miro/miro-master/scripts/list_boards.py --limit 20 --json
```

**Get board:**
```bash
python3 00-system/skills/miro/miro-master/scripts/get_board.py --board "BOARD_ID" --json
```

**Create board:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_board.py --name "Board Name" --description "Description" --json
```

**Delete board:**
```bash
python3 00-system/skills/miro/miro-master/scripts/delete_board.py --board "BOARD_ID" --json
```

**Copy board:**
```bash
python3 00-system/skills/miro/miro-master/scripts/copy_board.py --board "BOARD_ID" --json
```

#### Item Operations

**List items:**
```bash
python3 00-system/skills/miro/miro-master/scripts/list_items.py --board "BOARD_ID" --type sticky_note --json
```

**Create sticky note:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_sticky_note.py --board "BOARD_ID" --content "Note text" --color yellow --x 0 --y 0 --json
```

**Create card:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_card.py --board "BOARD_ID" --title "Title" --description "Desc" --json
```

**Create shape:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_shape.py --board "BOARD_ID" --content "Text" --shape rectangle --width 200 --height 200 --json
```

**Create text:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_text.py --board "BOARD_ID" --content "Text here" --font-size 24 --json
```

**Create frame:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_frame.py --board "BOARD_ID" --title "Section" --width 800 --height 600 --json
```

**Create connector:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_connector.py --board "BOARD_ID" --start-item "ITEM1" --end-item "ITEM2" --shape curved --json
```

**Create image:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_image.py --board "BOARD_ID" --url "https://example.com/img.png" --json
```

**Create embed:**
```bash
python3 00-system/skills/miro/miro-master/scripts/create_embed.py --board "BOARD_ID" --url "https://example.com" --json
```

**Update/move item:**
```bash
python3 00-system/skills/miro/miro-master/scripts/update_item.py --board "BOARD_ID" --item "ITEM_ID" --x 100 --y 200 --json
```

**Delete item:**
```bash
python3 00-system/skills/miro/miro-master/scripts/update_item.py --board "BOARD_ID" --item "ITEM_ID" --delete --json
```

**Get item details:**
```bash
python3 00-system/skills/miro/miro-master/scripts/update_item.py --board "BOARD_ID" --item "ITEM_ID" --get --json
```

#### Member Operations

**List members:**
```bash
python3 00-system/skills/miro/miro-master/scripts/board_members.py --board "BOARD_ID" --list --json
```

**Add member:**
```bash
python3 00-system/skills/miro/miro-master/scripts/board_members.py --board "BOARD_ID" --add "email@example.com" --role editor --json
```

#### Tag Operations

**List tags:**
```bash
python3 00-system/skills/miro/miro-master/scripts/tags.py --board "BOARD_ID" --list --json
```

**Create tag:**
```bash
python3 00-system/skills/miro/miro-master/scripts/tags.py --board "BOARD_ID" --create "Tag Name" --color red --json
```

**Attach tag to item:**
```bash
python3 00-system/skills/miro/miro-master/scripts/tags.py --board "BOARD_ID" --attach TAG_ID --item ITEM_ID --json
```

---

### Step 4: Handle Results

**Success:**
- Display relevant information to user
- Format board names, item IDs, member names nicely

**Error:**
- Common errors:
  - `401` > Token expired or invalid
  - `403` > Insufficient permissions
  - `404` > Board or item not found
  - `429` > Rate limited, wait and retry

---

## Board ID Resolution

When user references a board by name:
1. List boards: `list_boards.py --json`
2. Find matching board in response
3. Use the board ID for operations

---

## Environment Variables

Required in `.env`:
```
MIRO_ACCESS_TOKEN=your-access-token
```

Optional (for OAuth refresh):
```
MIRO_CLIENT_ID=your-client-id
MIRO_CLIENT_SECRET=your-client-secret
```

---

## Related Resources

- **API Reference**: `miro-master/references/api-reference.md`
- **Scripts**: `miro-master/scripts/`

---

**Version**: 1.0
**Created**: 2026-03-12
**Status**: Production Ready
