---
name: linear-update-tickets
version: '1.0'
description: Update Linear ticket status or add comments. Load when user says "update
  linear ticket", "mark ticket as done", "move CLI-XXX to [status]", "change ticket
  status", "add comment to ticket", or "close ticket".
author: Hassaan Ahmed
category: general
tags:
- linear
- update
platform: Linear
updated: '2025-12-23'
visibility: team
---
# Linear Update Tickets

Update existing Linear tickets - change status, add comments, or modify fields.

## Purpose

Modify Linear tickets discussed in meetings or that need status updates. Supports state changes, adding comments, and batch updates.

## Quick Setup

**Requirements**: Linear API key in `.env`

```bash
# Add to .env (NO Bearer prefix when using!)
LINEAR_API_KEY=lin_api_xxxxx
```

## Configuration

**API Endpoint**: `https://api.linear.app/graphql`
**Auth Header**: `Authorization: {LINEAR_API_KEY}` (NO "Bearer" prefix!)

**State IDs (Clients team)**:
| State | ID |
|-------|-----|
| Todo | d8899534-a204-4446-a06b-681cbc4c6e04 |
| In Progress | 9a2c9ba8-5931-491e-8298-c9fb761aab23 |
| In Review | 7866c5ad-5654-4516-849f-b3f7462613d6 |
| Done | 40112a2a-870e-48ca-aeff-7f16356acd90 |

## Workflow

### Step 1: Identify Ticket

Get ticket identifier:
- From user: "CLI-123" or "update ticket CLI-123"
- From context: Referenced in meeting discussion

### Step 2: Determine Update

Options:
- **Status change**: Todo → In Progress → In Review → Done
- **Add comment**: Context or update note
- **Both**: Change status with comment

### Step 3: Execute Update

**Update Status**:
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

**Variables**:
```json
{
  "id": "issue-uuid",
  "input": {
    "stateId": "40112a2a-870e-48ca-aeff-7f16356acd90"
  }
}
```

**Add Comment**:
```graphql
mutation AddComment($issueId: String!, $body: String!) {
  commentCreate(input: {
    issueId: $issueId,
    body: $body
  }) {
    success
    comment { id body }
  }
}
```

### Step 4: Confirm

```
Updated CLI-123:
  - Status: In Progress → Done
  - Comment added: "Completed per meeting discussion"
```

## Get Issue ID from Identifier

To update a ticket, you need its UUID (not the CLI-XXX identifier):

```graphql
query GetIssue($identifier: String!) {
  issue(id: $identifier) {
    id
    identifier
    title
    state { id name }
  }
}
```

## Query Team States

Get current state IDs for any team:
```graphql
query($teamId: String!) {
  team(id: $teamId) {
    states { nodes { id name type } }
  }
}
```

## Batch Updates

For multiple tickets:
```
Update tickets CLI-123, CLI-124, CLI-125 to Done
```

Process each sequentially and report results:
```
Updated 3 tickets:
- CLI-123: In Progress → Done
- CLI-124: Todo → Done
- CLI-125: In Review → Done
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Wrong auth format | NO "Bearer" prefix |
| Issue not found | Invalid identifier | Verify ticket exists |
| Invalid state | Wrong state ID | Query team states first |

## Related Skills

- `linear-create-tickets` - Create new tickets
- `create-weekly-update` - Report on ticket changes
- `process-client-meeting` - May update tickets from discussion

---

**Version**: 1.0
**Integration**: Linear GraphQL API
**Owner**: Hassaan Ahmed
