---
name: linear-create-tickets
version: '1.0'
description: Create Linear tickets from action items or task lists. Load when user
  says "create linear tickets", "add tickets to linear", "create tickets from meeting",
  "linear ticket for [task]", or wants to convert action items into Linear issues.
author: Hassaan Ahmed
category: general
tags:
- create
- linear
- meeting
platform: Linear
updated: '2025-12-23'
visibility: team
---
# Linear Create Tickets

Batch create Linear tickets from action items using the GraphQL API.

## Purpose

Convert action items (from meetings, planning sessions, or direct input) into Linear tickets with proper formatting, project assignment, and priority.

## Quick Setup

**Requirements**: Linear API key in `.env`

```bash
# Add to .env (NO Bearer prefix when using!)
LINEAR_API_KEY=lin_api_xxxxx
```

Get your API key: Linear Settings → API → Personal API Keys

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

## Workflow

### Step 1: Get Action Items

Accept from:
1. Output of `create-meeting-minutes`
2. User-provided list
3. Direct input

### Step 2: Filter Items

**Include**:
- Tasks with specific deliverables
- Technical implementation tasks
- Research or documentation tasks

**Exclude**:
- Scheduling tasks ("set up meeting")
- External/client-owned tasks
- Vague items

### Step 3: Get Project Info

Ask user or infer:
- Team name (e.g., "Clients", "Engineering")
- Project name (e.g., "Smartly", "Internal")

### Step 4: Create Tickets

**GraphQL Mutation**:
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

### Step 5: Report Results

```
Created 3 tickets:

1. CLI-456 - Implement data validation logic
   URL: https://linear.app/team/issue/CLI-456

2. CLI-457 - Update documentation for new API
   URL: https://linear.app/team/issue/CLI-457
```

## Ticket Format

**Title Rules**:
- Good: "Implement data validation logic"
- Bad: "[Project] Implement validation" (no project prefix)

**Description Template**:
```markdown
## Context
[Reference to source - meeting, discussion, etc.]

## Description
[What needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## Useful Queries

**Get Teams**:
```graphql
query { teams { nodes { id name } } }
```

**Get Projects in Team**:
```graphql
query($teamId: String!) {
  team(id: $teamId) {
    projects { nodes { id name } }
  }
}
```

**Get States**:
```graphql
query($teamId: String!) {
  team(id: $teamId) {
    states { nodes { id name } }
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Wrong auth format | Use key directly, NO "Bearer" prefix |
| Project not found | Invalid project ID | Query projects first |
| Invalid state | Wrong state ID | Query team states |

## Related Skills

- `create-meeting-minutes` - Source of action items
- `linear-update-tickets` - Update existing tickets
- `create-weekly-update` - Report on Linear activity
- `process-client-meeting` - Full workflow

---

**Version**: 1.0
**Integration**: Linear GraphQL API
**Owner**: Hassaan Ahmed
