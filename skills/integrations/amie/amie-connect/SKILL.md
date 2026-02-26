---
name: amie-connect
version: '1.0'
description: Work with Amie calendar and meeting notes. Load when user mentions "amie",
  "meeting notes", "get transcript", "save transcript to file", "export transcript",
  "action items from meeting", or wants to access Amie data.
category: integrations
tags:
- amie
- calendar
- connector
- meeting
- transcript
platform: Amie
updated: '2026-02-13'
visibility: public
---
# Amie Connect

Access your Amie calendar, meeting notes, transcripts, and action items.

---

## Workflow 0: Config Check (Auto - ALWAYS FIRST)

**ALWAYS run before any operation:**

```bash
python 00-system/skills/amie/amie-master/scripts/check_amie_config.py --json
```

| ai_action | What to Do |
|-----------|------------|
| `proceed_with_operation` | Config OK, continue |
| `prompt_for_api_token` | Ask user for PAT, add to .env |

---

## Workflow 1: List Meeting Notes

**Triggers**: "list notes", "show meeting notes", "my meetings", "amie notes"

```bash
python 00-system/skills/amie/amie-master/scripts/list_notes.py [--limit N]
```

Returns all meeting notes with IDs for further queries.

---

## Workflow 2: Get Note Details

**Triggers**: "get note", "show meeting", "note details"

```bash
python 00-system/skills/amie/amie-master/scripts/get_note.py --id NOTE_ID
```

---

## Workflow 3: Get Transcript

**Triggers**: "get transcript", "meeting transcript", "what was said"

```bash
python 00-system/skills/amie/amie-master/scripts/get_transcript.py --id NOTE_ID
```

Returns transcript with speaker identification.

---

## Workflow 3b: Save Transcript to File

**Triggers**: "save transcript to file", "export transcript", "fetch transcript into a file", "download transcript"

```bash
# Save as JSON (full API response)
python 00-system/skills/amie/amie-master/scripts/get_transcript.py --id NOTE_ID --output PATH

# Save as readable text (speaker: line)
python 00-system/skills/amie/amie-master/scripts/get_transcript.py --id NOTE_ID --output PATH --format text
```

- If user doesn't specify path, use a sensible default e.g. `02-resources/` or `04-outputs/` with note title and date in filename.
- Creates parent directories if needed.

---

## Workflow 4: Get Action Items

**Triggers**: "action items", "todos from meeting", "follow ups"

```bash
python 00-system/skills/amie/amie-master/scripts/get_action_items.py --id NOTE_ID
```

---

## Common Patterns

### Get recent meeting with action items
1. List notes to find latest meeting
2. Get action items for that note ID

### Full meeting review
1. Get note details (title, participants, duration)
2. Get transcript for full context
3. Get action items for follow-ups

---

## Error Handling

On error, check:
1. Is `AMIE_API_TOKEN` set in .env?
2. Is the token valid (not expired/revoked)?
3. Does the note ID exist?

For setup issues, run config check:
```bash
python 00-system/skills/amie/amie-master/scripts/check_amie_config.py --json
```

---

**Version**: 1.0
**Created**: 2026-02-03
