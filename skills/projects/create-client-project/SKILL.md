---
name: create-client-project
version: '1.0'
description: Create a new client project folder with complete structure and templates.
  Load when user says "create client project", "new client", "add client [name]",
  "onboard new client", "setup client folder", or "create project for [client]".
author: Hassaan Ahmed
category: general
tags:
- create
updated: '2025-12-23'
visibility: team
---
# Create Client Project

Create a standardized client project folder structure with pre-configured templates.

## Purpose

Quickly onboard new clients with a complete folder structure including:
- Project context tracking files
- Documentation templates
- Meeting notes organization
- Communication archives

**Time saved**: ~20 minutes of manual setup per client

## Workflow

### Step 1: Gather Information

**Required**:
- Client name

**Optional** (improves templates):
- GTM documentation / scope
- Primary contact info
- Project description
- Email domain (for Fathom filtering)

```
What's the client name?
> Acme Corporation

Do you have any GTM documentation to include? (paste, file path, or 'skip')
```

### Step 2: Normalize Name

Convert to folder-safe format:
- Lowercase
- Replace spaces with hyphens
- Remove special characters

`"Acme Corporation"` → `acme-corporation`

### Step 3: Create Structure

**Base Location**: User specifies or use default project location

```
[location]/[client-name]/
├── PROJECT_CONTEXT.md         # Chronological update log
├── project-state.json         # Structured state data
├── README.md                  # Project overview
│
├── docs/
│   ├── SCOPE_OF_WORK.md       # Deliverables & timeline
│   ├── SOLUTION_WORKFLOW.md   # Operational procedures
│   ├── TECHNICAL_ARCHITECTURE.md  # System design
│   ├── LINEAR_TICKETS.md      # Ticket tracking
│   └── SLACK_CHANNELS_SETUP.md    # Communication
│
├── meetings/
│   └── transcripts/           # Raw transcripts
│
├── communications/            # Sent messages
│
└── weekly-updates/            # Status reports
```

### Step 4: Populate Templates

**PROJECT_CONTEXT.md**:
```markdown
# [Client Name] Project Context

> Quick-reference log of project changes. Newest entries at top.

---

## [Today's Date]

**Project Created**
- Initial setup and folder structure

**Links:**
- [Scope of Work](docs/SCOPE_OF_WORK.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
```

**project-state.json**:
```json
{
  "lastUpdated": "[timestamp]",
  "clientName": "[Client Name]",
  "clientDomain": "[domain.com]",
  "currentPhase": "DISCOVERY",
  "recentActivity": [{
    "date": "[today]",
    "type": "onboarding",
    "summary": "Project created"
  }],
  "nextSteps": [
    "Complete kickoff meeting",
    "Define scope of work",
    "Set up communication channels"
  ],
  "openIssues": [],
  "blockers": [],
  "team": {
    "internal": [],
    "client": []
  }
}
```

**README.md**:
```markdown
# [Client Name]

## Overview
[Description from GTM docs or placeholder]

## Quick Links
- [Scope of Work](docs/SCOPE_OF_WORK.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
- Linear Project: TBD
- Slack Channel: TBD

## Team
**Internal**: TBD
**Client**: [Contact info if provided]

## Status
- **Phase**: Discovery
- **Created**: [Date]
```

### Step 5: Extract from GTM Docs

If documentation provided, extract:
- Scope → `SCOPE_OF_WORK.md`
- Contacts → `README.md`
- Requirements → `TECHNICAL_ARCHITECTURE.md`
- Timeline → `SCOPE_OF_WORK.md`

### Step 6: Report Success

```
Client project created: [Client Name]

Location: [path]

Files Created:
- PROJECT_CONTEXT.md
- project-state.json
- README.md
- docs/SCOPE_OF_WORK.md
- docs/SOLUTION_WORKFLOW.md
- docs/TECHNICAL_ARCHITECTURE.md
- docs/LINEAR_TICKETS.md
- docs/SLACK_CHANNELS_SETUP.md

Next Steps:
1. Review and complete SCOPE_OF_WORK.md
2. Create Linear project
3. Set up Slack channels
4. Schedule kickoff meeting
```

## Package Contents

```
create-client-project/
├── SKILL.md                    # This file
└── templates/
    ├── PROJECT_CONTEXT.md      # Context template
    ├── project-state.json      # State template
    ├── README.md               # Overview template
    └── docs/
        ├── SCOPE_OF_WORK.md
        ├── SOLUTION_WORKFLOW.md
        ├── TECHNICAL_ARCHITECTURE.md
        ├── LINEAR_TICKETS.md
        └── SLACK_CHANNELS_SETUP.md
```

## Related Skills

- `process-client-meeting` - Use after kickoff meeting
- `update-project-context` - Keep context current
- `create-weekly-update` - Start weekly reporting
- `fathom-fetch-meetings` - Filter meetings by client domain

---

**Version**: 1.0
**Owner**: Hassaan Ahmed
