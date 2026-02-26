---
name: fathom
version: '1.2'
description: Complete Fathom integration skill. Load when user wants to fetch meetings,
  get transcripts, list recordings, or interact with Fathom meeting data. Supports
  filtering by attendee domain and extracting summaries/action items.
author: Hassaan Ahmed
category: general
tags:
- fathom
- meeting
- transcript
platform: Fathom
updated: '2025-12-24'
visibility: team
---
# Fathom Integration

Complete Fathom API integration for meeting recordings and transcripts.

## Purpose

Provides full Fathom meeting interaction:
- List and filter meetings by attendee domain
- Fetch AI-generated summaries
- Extract action items with assignees
- Download full speaker-attributed transcripts
- Filter by date range

## Quick Setup (30 seconds)

1. Get your API key from Fathom Settings → API

2. Add to `.env`:
```bash
FATHOM_API_KEY=your-api-key-here
```

3. Test connection:
```bash
python3 00-system/skills/fathom/fathom-master/scripts/fathom_client.py
```

Expected output:
```
Fathom client initialized successfully
Found X meetings
```

## Package Contents

```
fathom/
├── SKILL.md                     # This file (main entry point)
├── credentials/
│   └── README.md                # How to get your API key
├── fathom-connect/              # Connection setup skill
│   └── SKILL.md
└── fathom-master/               # Scripts and references
    ├── scripts/
    │   ├── fathom_client.py     # Shared API client (reusable)
    │   ├── list_meetings.py     # List meetings with filters
    │   └── get_transcript.py    # Get transcript by ID
    └── references/
        ├── authentication.md    # API key setup
        ├── api-reference.md     # Endpoints and parameters
        └── error-handling.md    # Common errors and solutions
```

## Available Operations

| Category | Operations |
|----------|------------|
| Meetings | list, filter by domain, filter by date range |
| Transcripts | get full transcript, speaker attribution |
| Summaries | AI-generated meeting summaries |
| Action Items | extracted tasks with assignees |

## Example Usage

```bash
# List all recent meetings
python3 fathom-master/scripts/list_meetings.py

# List meetings for a client domain
python3 fathom-master/scripts/list_meetings.py --domain smartly.io

# List meetings from last 7 days with summaries
python3 fathom-master/scripts/list_meetings.py --days 7 --verbose

# Get transcript for a specific recording
python3 fathom-master/scripts/get_transcript.py --recording-id abc123-def456

# Get transcript as JSON (for processing)
python3 fathom-master/scripts/get_transcript.py --recording-id abc123 --json

# Save transcript to file
python3 fathom-master/scripts/get_transcript.py --recording-id abc123 --output meeting.txt
```

## Known Client Domains

| Client | Domain |
|--------|--------|
| Smartly | smartly.io |
| Rivertrace | rivertrace.com |
| Moverii | moverii.de |
| Doula Givers | doulagivers.com |

## Authentication

Uses **API Key** authentication via `X-Api-Key` header. Keys don't expire but can be rotated in Fathom Settings → API.

## Troubleshooting

| Error | Solution |
|-------|----------|
| FATHOM_API_KEY not found | Add key to `.env` file |
| 401 Unauthorized | API key is invalid - regenerate in Fathom |
| 403 Forbidden | API not enabled on your Fathom plan |
| 404 Not Found | Recording ID doesn't exist or still processing |

---

**Version**: 1.1
**Integration**: Fathom API
**Tested**: Scripts verified working
**Owner**: Hassaan Ahmed
