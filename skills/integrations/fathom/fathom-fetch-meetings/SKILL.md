---
name: fathom-fetch-meetings
version: '1.0'
description: Fetch meeting recordings and transcripts from Fathom API filtered by
  attendee email domain. Load when user says "fetch meetings", "get fathom recordings",
  "fathom meetings for [domain]", "list meetings from fathom", "get transcripts",
  or mentions Fathom.
author: Hassaan Ahmed
category: general
tags:
- api
- email
- fathom
- meeting
- transcript
platform: Fathom
updated: '2025-12-23'
visibility: team
---
# Fathom Fetch Meetings

Fetch and filter meeting recordings from Fathom API by client domain.

## Purpose

Query Fathom to retrieve meetings filtered by attendee email domain. Returns meeting summaries, action items, and optionally full transcripts. Use this as the entry point for meeting processing workflows.

## Quick Setup

**Requirements**: Fathom API key in `.env`

```bash
# Add to .env
FATHOM_API_KEY=your-api-key-here
```

Get your API key: Fathom Settings → API

## Configuration

**API Endpoint**: `https://api.fathom.ai/external/v1`
**Auth Header**: `X-Api-Key: {FATHOM_API_KEY}`

**Known Client Domains**:
| Client | Domain |
|--------|--------|
| Smartly | smartly.io |
| Rivertrace | rivertrace.com |
| Moverii | moverii.de |
| Doula Givers | doulagivers.com |

## Workflow

### Step 1: Get Domain

Map client name to domain or ask user:
```
"Smartly" → smartly.io
"Rivertrace" → rivertrace.com
```

### Step 2: Fetch Meetings

```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?calendar_invitees_domains[]={DOMAIN}&include_summary=true&include_action_items=true' \
  --header 'X-Api-Key: {FATHOM_API_KEY}'
```

**Query Parameters**:
| Parameter | Description |
|-----------|-------------|
| `calendar_invitees_domains[]` | Filter by attendee email domain |
| `include_summary` | Include AI-generated summary |
| `include_transcript` | Include full transcript |
| `include_action_items` | Include extracted action items |
| `created_after` | ISO 8601 date filter (e.g., 2025-01-01) |
| `created_before` | ISO 8601 date filter |

### Step 3: Display Results

```
Found 3 meetings for smartly.io:

1. Weekly Sync - Dec 20, 2025
   Summary: Discussed pipeline progress...
   Recording ID: abc123-def456

2. Technical Review - Dec 18, 2025
   Summary: Reviewed architecture decisions...
   Recording ID: ghi789-jkl012

Select meeting to get full transcript (or 'skip'):
```

### Step 4: Fetch Transcript (Optional)

For a specific meeting:
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/recordings/{RECORDING_ID}/transcript' \
  --header 'X-Api-Key: {FATHOM_API_KEY}'
```

**Transcript Response**:
```json
{
  "transcript": [
    {
      "speaker": {"display_name": "Name", "matched_calendar_invitee_email": "email"},
      "text": "What they said",
      "timestamp": "HH:MM:SS"
    }
  ]
}
```

## Output

Returns meeting data including:
- Meeting title, date, duration
- AI-generated summary
- Action items with assignees
- Attendee list
- Full transcript (if requested)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check FATHOM_API_KEY in .env |
| No meetings found | Wrong domain or date range | Verify domain, adjust date filters |
| 403 Forbidden | API access disabled | Contact Fathom support |

## Related Skills

- `fathom-get-transcript` - Fetch transcript by recording ID
- `create-meeting-minutes` - Format transcript into minutes
- `process-client-meeting` - Full meeting workflow

---

**Version**: 1.0
**Integration**: Fathom API
**Owner**: Hassaan Ahmed
