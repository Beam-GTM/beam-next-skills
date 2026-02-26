---
name: fathom-get-transcript
version: '1.0'
description: Fetch full transcript from Fathom using a meeting/recording ID. Load
  when user says "get transcript", "fetch transcript for [ID]", "fathom transcript",
  "download meeting transcript", or has a meeting ID and wants the full conversation
  text.
author: Hassaan Ahmed
category: general
tags:
- fathom
- meeting
- transcript
platform: Fathom
updated: '2025-12-23'
visibility: team
---
# Fathom Get Transcript

Fetch the complete transcript for a specific Fathom meeting using its recording ID.

## Purpose

Retrieves the full speaker-attributed transcript from a Fathom recording. Use this when you have a meeting ID (from `fathom-fetch-meetings` or direct input) and need the complete conversation text for processing.

## Quick Setup

**Requirements**: Fathom API key in `.env`

```bash
# Add to .env
FATHOM_API_KEY=your-api-key-here
```

Get your API key: Fathom Settings → API

## Package Contents

```
fathom-get-transcript/
├── SKILL.md              # This file
└── scripts/
    └── get_transcript.py # Fetch transcript by recording ID
```

## Workflow

### Step 1: Get Recording ID

Accept recording ID from:
1. Output of `fathom-fetch-meetings` (recording_id field)
2. User-provided ID
3. Fathom meeting URL (extract ID from URL)

```
Enter recording ID (or paste Fathom URL):
> abc123-def456-789
```

### Step 2: Fetch Transcript

```bash
python scripts/get_transcript.py --recording-id {ID}
```

**API Call**:
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/recordings/{RECORDING_ID}/transcript' \
  --header 'X-Api-Key: {FATHOM_API_KEY}'
```

### Step 3: Format Output

**Raw Response**:
```json
{
  "transcript": [
    {
      "speaker": {
        "display_name": "John Smith",
        "matched_calendar_invitee_email": "john@company.com"
      },
      "text": "Let's start with the agenda...",
      "timestamp": "00:01:23"
    }
  ]
}
```

**Formatted Output**:
```
TRANSCRIPT: Meeting Title
Duration: 45 minutes
Speakers: John Smith, Jane Doe

---

[00:01:23] John Smith:
Let's start with the agenda...

[00:01:45] Jane Doe:
Thanks John. First item is the technical review...
```

### Step 4: Return for Processing

Returns structured transcript data for downstream skills:
- Speaker-separated text blocks
- Timestamps for reference
- Raw text for analysis

## Example Usage

```bash
# Fetch transcript by ID
python scripts/get_transcript.py --recording-id abc123-def456

# Fetch and save to file
python scripts/get_transcript.py --recording-id abc123 --output transcript.md

# Get JSON output for processing
python scripts/get_transcript.py --recording-id abc123 --json
```

## Output Format

```json
{
  "recording_id": "abc123-def456",
  "duration_seconds": 2700,
  "speakers": ["John Smith", "Jane Doe"],
  "transcript": [
    {
      "timestamp": "00:01:23",
      "speaker": "John Smith",
      "email": "john@company.com",
      "text": "Let's start with the agenda..."
    }
  ],
  "full_text": "John Smith: Let's start...\n\nJane Doe: Thanks John..."
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check FATHOM_API_KEY in .env |
| 404 Not Found | Invalid recording ID | Verify ID from fathom-fetch-meetings |
| 403 Forbidden | No access to recording | Ensure you have access in Fathom |

## Related Skills

- `fathom-fetch-meetings` - Get recording IDs by filtering meetings
- `create-meeting-minutes` - Process transcript into formatted minutes
- `process-client-meeting` - Full meeting workflow

---

**Version**: 1.0
**Integration**: Fathom API
**Owner**: Hassaan Ahmed
