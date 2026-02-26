---
name: process-client-meeting
version: '1.0'
description: Complete end-to-end workflow to process a client meeting. Load when user
  says "process meeting", "meeting workflow", "process client meeting", "full meeting
  processing", "handle meeting for [client]", or "post-meeting workflow". Handles
  transcript fetching, minutes creation, Linear tickets, client updates, internal
  updates, and project context sync.
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
# Process Client Meeting

Complete end-to-end workflow for processing client meetings from transcript to deliverables.

## Purpose

Automates the entire post-meeting workflow:
- Fetch meeting transcript from Fathom
- Generate formatted meeting minutes
- Create Linear tickets for action items
- Draft client-facing update message
- Post internal team update to Slack
- Update project context files

**Time saved**: ~45 minutes of manual work per meeting

## Quick Setup

**Required integrations** (add to `.env`):

```bash
# Fathom API - for meeting transcripts
FATHOM_API_KEY=your-fathom-key

# Linear API - for ticket management
LINEAR_API_KEY=lin_api_xxxxx

# Slack - for team notifications (run setup_slack.py first)
SLACK_USER_TOKEN=xoxp-xxxxx
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Fetch Meeting       [CHECKPOINT: Select meeting]   │
│  ↓                                                          │
│  STEP 2: Create Meeting Minutes                             │
│  ↓                                                          │
│  STEP 3: Create Linear Tickets (action items)               │
│  ↓                                                          │
│  STEP 4: Update Existing Tickets (if discussed)             │
│  ↓                                                          │
│  STEP 5: Draft Client Update  [CHECKPOINT: Approve draft]   │
│  ↓                                                          │
│  STEP 6: Send Internal Update (Slack)                       │
│  ↓                                                          │
│  STEP 7: Update Project Context                             │
└─────────────────────────────────────────────────────────────┘
```

---

# STEP 1: Fetch Meeting from Fathom

## Purpose
Retrieve meeting list and transcript from Fathom API filtered by client domain.

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

## Execution

### 1.1 List Meetings by Domain

```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?calendar_invitees_domains[]={DOMAIN}&include_summary=true&include_action_items=true' \
  --header 'X-Api-Key: {FATHOM_API_KEY}'
```

**Display**:
```
Found 3 meetings for smartly.io:

1. Weekly Sync - Dec 20, 2025
   Summary: Discussed pipeline progress and Q1 planning...
   Recording ID: abc123-def456

2. Technical Review - Dec 18, 2025
   Summary: Reviewed architecture decisions...
   Recording ID: ghi789-jkl012

Which meeting to process? (enter number)
```

### 1.2 Fetch Full Transcript

```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/recordings/{RECORDING_ID}/transcript' \
  --header 'X-Api-Key: {FATHOM_API_KEY}'
```

**Response Format**:
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

---

# STEP 2: Create Meeting Minutes

## Purpose
Transform raw transcript into structured meeting minutes with discussion points and action items.

## Extraction Rules

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

## Output Format

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

## Save Location
```
[project-folder]/meetings/YYYY-MM-DD-Meeting-Minutes.md
```

---

# STEP 3: Create Linear Tickets

## Purpose
Create Linear tickets from internal team action items.

## Configuration

**API Endpoint**: `https://api.linear.app/graphql`
**Auth Header**: `Authorization: {LINEAR_API_KEY}` (NO "Bearer" prefix!)

**Team IDs**:
| Team | ID |
|------|-----|
| Clients | 2686694f-6343-48a0-9efb-d69d77aaa621 |

**State IDs (Clients team)**:
| State | ID |
|-------|-----|
| Todo | d8899534-a204-4446-a06b-681cbc4c6e04 |
| In Progress | 9a2c9ba8-5931-491e-8298-c9fb761aab23 |
| In Review | 7866c5ad-5654-4516-849f-b3f7462613d6 |
| Done | 40112a2a-870e-48ca-aeff-7f16356acd90 |

**Priority Values**:
| Priority | Value |
|----------|-------|
| Urgent | 1 |
| High | 2 |
| Medium | 3 |
| Low | 4 |

## Create Ticket Mutation

```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
      url
    }
  }
}
```

**Variables**:
```json
{
  "input": {
    "title": "Task title (no project prefix)",
    "teamId": "2686694f-6343-48a0-9efb-d69d77aaa621",
    "projectId": "PROJECT_UUID",
    "stateId": "d8899534-a204-4446-a06b-681cbc4c6e04",
    "priority": 3,
    "description": "## Context\nFrom meeting: [date]\n\n## Description\n[Task details]"
  }
}
```

## Ticket Title Rules
- **Good**: "Implement data validation logic"
- **Bad**: "[Smartly] Implement validation" (no project prefix)

## Output
```
Created 3 tickets:
- CLI-456: Implement data validation logic
- CLI-457: Update documentation for new API
- CLI-458: Review architecture proposal
```

---

# STEP 4: Update Existing Tickets

## Purpose
Update tickets that were discussed in the meeting (status changes, comments).

## Identify Tickets
Look for ticket references in transcript:
- "CLI-123 is done"
- "We finished the pipeline work"
- "That ticket can be closed"

## Update Status Mutation

```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue {
      identifier
      title
      state { name }
    }
  }
}
```

**Variables (status change)**:
```json
{
  "id": "issue-uuid",
  "input": {
    "stateId": "40112a2a-870e-48ca-aeff-7f16356acd90"
  }
}
```

## Add Comment Mutation

```graphql
mutation AddComment($issueId: String!, $body: String!) {
  commentCreate(input: {
    issueId: $issueId,
    body: $body
  }) {
    success
    comment { id }
  }
}
```

## Output
```
Updated tickets:
- CLI-400: In Progress → Done (comment: "Completed per meeting discussion")
```

---

# STEP 5: Draft Client Update

## Purpose
Generate external client-facing summary for Slack or email.

## **CHECKPOINT**: Present draft for user approval before proceeding.

## Message Format (Slack)

```
Hey team! Quick update from today's call:

**What we covered:**
• [Key discussion point 1]
• [Key discussion point 2]
• [Decision made]

**Next steps:**
• [Our team]: [Action with timeline]
• [Your team]: [What we need from them]

**Next meeting:** [Date/time if scheduled]

Let me know if you have any questions!
```

## Message Format (Email)

```
Subject: [Client] Meeting Follow-up - [Date]

Hi [Name],

Thanks for the productive call today! Here's a quick summary:

**Discussion Highlights:**
- [Point 1]
- [Point 2]

**Action Items:**
Our team:
- [Action 1]
- [Action 2]

Your team:
- [Action if any]

**Next Steps:**
[Timeline and next meeting info]

Best regards,
[Name]
```

## Approval Flow
```
Draft client update:
---
[Content]
---

1. Approve and continue
2. Request changes
3. Skip client update

Choice:
```

---

# STEP 6: Send Internal Update

## Purpose
Post meeting summary to internal team Slack channel.

## Configuration

Uses Slack User OAuth token from `.env`:
```
SLACK_USER_TOKEN=xoxp-xxxxx
```

## API Call

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer {SLACK_USER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#client-updates",
    "text": "Meeting update message..."
  }'
```

## Message Format

```
*[Client] Meeting Summary* - [Date]

*Key Decisions:*
• [Decision 1]
• [Decision 2]

*Action Items Created:*
• CLI-456: [Task]
• CLI-457: [Task]

*Blockers/Risks:*
• [Any blockers identified]

*Next Meeting:* [Date]

Full notes: [link to minutes]
```

---

# STEP 7: Update Project Context

## Purpose
Sync PROJECT_CONTEXT.md and project-state.json with meeting outcomes.

## PROJECT_CONTEXT.md Update

Add new entry at TOP of file:

```markdown
## [Today's Date]

**Meeting: [Topic]**
- [Key outcome 1]
- [Key outcome 2]
- Action items: CLI-456, CLI-457, CLI-458
- Next meeting: [Date]

**Decisions:**
- [Decision 1]
- [Decision 2]
```

## project-state.json Update

```json
{
  "lastUpdated": "[timestamp]",
  "currentPhase": "[DISCOVERY|BUILD|REVIEW|COMPLETE]",
  "recentActivity": [
    {
      "date": "[today]",
      "type": "meeting",
      "summary": "[Meeting topic and key outcomes]",
      "tickets": ["CLI-456", "CLI-457"]
    }
  ],
  "nextSteps": [
    "[Updated next step 1]",
    "[Updated next step 2]"
  ],
  "openIssues": ["[Any new issues]"],
  "blockers": ["[Any blockers]"]
}
```

---

# Completion Summary

```
Meeting Processing Complete

Meeting Minutes
   Saved: [path/to/minutes.md]

Linear Tickets
   Created: CLI-456, CLI-457, CLI-458
   Updated: CLI-400 → Done

Client Update
   Status: Approved
   Format: Slack message

Internal Update
   Posted to: #client-updates

Project Context
   Updated: PROJECT_CONTEXT.md
   Updated: project-state.json

All steps completed successfully!
```

---

# Error Handling

| Step | Error | Recovery |
|------|-------|----------|
| 1 | No meetings found | Ask for different date range or domain |
| 1 | API 401 | Check FATHOM_API_KEY |
| 3 | Linear 401 | Check LINEAR_API_KEY (no Bearer prefix!) |
| 5 | User skips | Continue to step 6 |
| 6 | Slack fails | Offer to copy message manually |

**On any step failure**:
1. Report which step failed and why
2. Offer to retry or skip
3. Continue with remaining steps
4. Summarize successes/failures at end

---

# Customization

**Skip steps** based on context:
- No Fathom → User provides transcript directly
- No action items → Skip ticket creation
- Internal meeting → Skip client update
- No project folder → Skip context update

**Run individual steps**:
Each step can be executed independently via the component skills.

---

**Version**: 1.0
**Integration**: Fathom, Linear, Slack
**Owner**: Hassaan Ahmed
**Tested**: Full workflow validated
