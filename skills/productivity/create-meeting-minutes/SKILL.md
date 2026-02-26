---
name: create-meeting-minutes
version: '1.0'
description: Transform a meeting transcript into formatted meeting minutes. Load when
  user says "create meeting minutes", "format meeting notes", "generate minutes from
  transcript", "meeting minutes from recording", or provides a transcript to format.
author: Hassaan Ahmed
category: general
tags:
- create
- meeting
- transcript
updated: '2025-12-23'
visibility: team
---
# Create Meeting Minutes

Transform raw meeting transcripts into structured, professional meeting minutes.

## Purpose

Takes a meeting transcript (from Fathom or pasted text) and extracts:
- Key discussion points
- Action items (categorized by owner)
- Decisions made
- Follow-up items

Outputs formatted markdown ready for sharing or archiving.

## Workflow

### Step 1: Get Transcript

Accept from:
1. Output from `fathom-fetch-meetings` or `fathom-get-transcript`
2. User-pasted transcript text
3. File path to transcript

### Step 2: Extract Information

**Discussion Points** (include):
- Key topics and decisions
- Technical details explained
- Blockers or dependencies
- Timeline discussions

**Action Items** (include):
- Tasks with specific deliverables
- Clear ownership (internal vs client)
- Due dates if mentioned

**Action Items** (exclude):
- "Schedule next meeting" (scheduling tasks)
- Vague items without deliverables
- Already completed items

### Step 3: Format Minutes

```markdown
# Meeting Minutes: [Client] — [Topic]

**Date:** [Month Day, Year]
**Attendees:** [Name] (Company), [Name] (Company)
**Recording:** [Fathom link if available]

---

## Discussion Points

- [Topic with context and decisions made]
- [Technical details or process explanations]
- [Blockers, dependencies, or waiting items]

---

## Action Items

### Internal Team
- [Person] to [specific task with deliverable]
- [Person] to [specific task with deliverable]

### Client Actions
- [Person] to [specific task]

---

## Decisions Made

- [Decision 1]
- [Decision 2]

---

## Next Meeting
[Date/time if discussed]
```

### Step 4: Save (Optional)

If save location specified:
```
[project-folder]/meetings/YYYY-MM-DD-Meeting-Minutes.md
```

### Step 5: Return Action Items

Separate action items by owner for downstream use:
- **Internal team actions** → For Linear ticket creation
- **External/client actions** → For client communication

## Output Format

```json
{
  "file_saved": "path/to/minutes.md",
  "date": "2025-12-20",
  "attendees": ["John Smith", "Jane Doe"],
  "discussion_points": ["Point 1", "Point 2"],
  "action_items": {
    "internal": [
      {"owner": "Team", "task": "Implement validation", "due": null}
    ],
    "external": [
      {"owner": "Client", "task": "Provide test data", "due": "EOW"}
    ]
  },
  "decisions": ["Decision 1", "Decision 2"]
}
```

## Action Item Extraction Rules

| Include | Exclude |
|---------|---------|
| Tasks with specific deliverables | "Set up next meeting" |
| Tasks with clear ownership | Vague items without deliverables |
| Follow-up items with deadlines | Already completed items |

## Related Skills

- `fathom-fetch-meetings` - Source transcripts from Fathom
- `fathom-get-transcript` - Get transcript by ID
- `linear-create-tickets` - Create tickets from action items
- `process-client-meeting` - Full workflow

---

**Version**: 1.0
**Owner**: Hassaan Ahmed
