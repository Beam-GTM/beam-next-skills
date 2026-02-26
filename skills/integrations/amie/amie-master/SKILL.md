---
name: amie-master
version: '1.0'
description: Shared resource library for Amie integration skills. DO NOT load directly
  - provides common references and scripts used by amie-connect and individual Amie
  skills.
category: integrations
tags:
- amie
- master
platform: Amie
updated: '2026-02-13'
visibility: public
---
# Amie Master

**This is NOT a user-facing skill.** It's a shared resource library referenced by Amie integration skills.

## Purpose

Provides shared resources for Amie calendar & meeting notes integration:
- `amie-connect` - Meta-skill for Amie operations
- Individual operation skills

## Authentication

Amie uses **Personal Access Token (PAT)** authentication:

```
Authorization: Bearer amie_pat_live_xxx
```

Token is stored in `.env` as `AMIE_API_TOKEN`.

---

## Shared Scripts

### Configuration

**[check_amie_config.py](scripts/check_amie_config.py)** - Pre-flight validation
```bash
python check_amie_config.py [--json]
```

Exit codes: 0=configured, 2=not configured

**When to Use:** Run FIRST before any Amie operation to verify token is set.

---

### API Operations

**[list_notes.py](scripts/list_notes.py)** - List meeting notes
```bash
python list_notes.py [--limit N] [--json]
```

**[get_note.py](scripts/get_note.py)** - Get note details
```bash
python get_note.py --id NOTE_ID [--json]
```

**[get_transcript.py](scripts/get_transcript.py)** - Get transcript with speakers
```bash
python get_transcript.py --id NOTE_ID [--json]
# Save to file:
python get_transcript.py --id NOTE_ID --output PATH [--format json|text]
```
- `--output PATH`: Save transcript locally (JSON or readable text)
- `--format text`: When using --output, write "Speaker: line" format instead of full JSON

**[get_action_items.py](scripts/get_action_items.py)** - Get action items
```bash
python get_action_items.py --id NOTE_ID [--json]
```

---

## Environment Variables

Required in `.env`:
```
# Amie Personal Access Token
AMIE_API_TOKEN=amie_pat_live_xxx
```

---

## API Base URL

All API requests go to: `https://calendar.amie.so/api/v1`

---

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| GET /notes | List all meeting notes |
| GET /notes/:id | Get note details |
| GET /notes/:id/transcript | Get transcript with speakers |
| GET /notes/:id/action-items | Get action items |

---

**Version**: 1.0
**Created**: 2026-02-03
**Status**: Ready
