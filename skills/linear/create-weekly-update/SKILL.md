---
name: create-weekly-update
version: '1.0'
description: Generate weekly status update based on Linear ticket activity and project
  progress. Load when user says "weekly update", "weekly status", "create weekly report",
  "status update for [project]", "what got done this week". Fetches ticket changes
  and generates formatted summary.
category: general
tags:
- create
- linear
- update
platform: Linear
updated: '2026-02-09'
visibility: team
---
# Create Weekly Update

Generate weekly status update from Linear activity.

## Workflow

### Step 1: Identify Scope

Ask if not clear:
- Project name in Linear
- Team name
- Time period (default: 7 days)

### Step 2: Fetch Ticket Changes

**Query tickets updated in period**:
```graphql
query($teamId: String!, $updatedAfter: DateTime!) {
  team(id: $teamId) {
    projects {
      nodes {
        name
        issues(filter: { updatedAt: { gte: $updatedAfter } }) {
          nodes {
            identifier
            title
            state { name }
            completedAt
            updatedAt
          }
        }
      }
    }
  }
}
```

### Step 3: Categorize Tickets

**Done This Period**:
- Tickets marked Done with completedAt in range

**In Progress**:
- Tickets in "In Progress" or "In Review" state

**To Do**:
- Tickets in "Todo" state

### Step 4: Display Current State

```
📊 Status for [Project] (Last 7 Days)

✅ Completed (3):
- CLI-400: Data pipeline setup
- CLI-401: Integration testing
- CLI-402: Documentation

🔄 In Progress (2):
- CLI-456: Validation implementation
- CLI-457: API integration

📋 Todo (4):
- CLI-458: Architecture review
- CLI-459: Performance testing
- CLI-460: UAT
- CLI-461: Deployment
```

### Step 5: Ask for Updates (Optional)

```
Would you like to update any tickets?
1. Update status (e.g., move CLI-456 to Done)
2. Continue without changes
```

If updates requested, use `linear-update-tickets`.

### Step 6: Generate Summary

**Weekly Update Format**:
```markdown
# [Project] Weekly Update - [Date]

## Done Last Week
- [Action-oriented description with context] - https://linear.app/beam-ai/issue/CLI-XXXX
- [Action-oriented description with context] - https://linear.app/beam-ai/issue/CLI-XXXX

## To be Done This Week
- [Action-oriented description with context] - https://linear.app/beam-ai/issue/CLI-XXXX
- [Action-oriented description with context] - https://linear.app/beam-ai/issue/CLI-XXXX

## Technical Dependencies (if any)
https://linear.app/beam-ai/issue/CLI-XXXX (P[N], assigned to [Name])
- What it blocks and why
- Key technical details (APIs, scopes, implementation notes)

## Client Notes (if any)
- [Notable client feedback, timeline changes, or new contacts]
```

**Format Rules**:
- NO project prefixes in titles
- 1-line descriptions only, but action-oriented with context (not just ticket titles)
  - Good: "Discussed and aligned with Ross on Slack fallback mechanisms"
  - Bad: "Add Slack search fallback when no Zendesk conversations are found"
- Describe what was DONE, not just what the ticket says
- Always reference tickets using **full Linear URLs** (not plain identifiers like `CLI-XXXX`)
  - The Linear API only renders rich inline issue badges when the full URL is used
  - Format: `https://linear.app/beam-ai/issue/CLI-XXXX`
  - Plain text identifiers (e.g., `CLI-4478`) will NOT auto-link when posted via API

**Optional Sections** (include when relevant):
- **Technical Dependencies**: When a ticket is blocked by another team's work (e.g., platform actions, integrations). Include the blocker ticket, who owns it, and key technical details.
- **Client Notes**: When there's been client communication that affects timeline, scope, or introduces new stakeholders. Summarize key takeaways.

### Step 7: Post to Linear

**Post as Linear Project Update** using `projectUpdateCreate` mutation:

```graphql
mutation {
  projectUpdateCreate(input: {
    projectId: "PROJECT_UUID"
    body: "...markdown body with full issue URLs..."
    health: onTrack
  }) {
    success
    projectUpdate { id url }
  }
}
```

**Health values**: `onTrack`, `atRisk`, `offTrack`

**To edit an existing update**, use `projectUpdateUpdate`:

```graphql
mutation($input: ProjectUpdateUpdateInput!) {
  projectUpdateUpdate(id: "UPDATE_UUID", input: $input) {
    success
    projectUpdate { id url }
  }
}
```

### Step 8: Save/Share (Optional)

Options:
- Save to file: `[folder]/weekly-updates/YYYY-MM-DD-Update.md`
- Post to Slack
- Copy to clipboard

---

## Output

```json
{
  "project": "Project Name",
  "period": "2025-12-09 to 2025-12-15",
  "completed": [...],
  "in_progress": [...],
  "todo": [...],
  "summary_markdown": "..."
}
```

---

## Related Skills

- `linear-update-tickets` - Update ticket status
- `update-project-context` - Sync after generating
- `send-internal-update` - Share with team
