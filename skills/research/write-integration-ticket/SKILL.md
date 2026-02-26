---
name: write-integration-ticket
version: '1.0'
description: Write API integration tickets in structured specification format. Load
  when user mentions 'write integration ticket', 'create integration spec', 'integration
  specification', 'API action ticket', or wants to document an API integration with
  endpoints, parameters, acceptance criteria, and error handling. Creates Linear tickets
  with Integration label assigned to Adeel Akram.
author: Saqib
category: general
tags:
- api
updated: '2026-01-19'
visibility: public
---
# Write Integration Ticket

Create structured API integration specifications ready for Linear import.

## Purpose

Transform API documentation into actionable integration tickets with clear endpoints, parameters, acceptance criteria, and error messages. Output follows a standardized table format for developer clarity.

---

## CRITICAL: Before Starting

**ALWAYS ask the user first:**

> "Please share the API documentation or endpoint details for this integration before I begin writing the specification."

Do **NOT** proceed with creating the spec until documentation is provided.

---

## Output Format

Every integration ticket MUST follow this structure:

```markdown
## [Action Number]. Action Title: [Action Name]

**Objective:** [One sentence describing what this action accomplishes]

| Field | Details |
|-------|---------|
| **Endpoint** | - Discovery: `GET /path` (if applicable)<br>- Action: `POST /path/{id}/action` |
| **Input Parameters** | - `paramName` (type, required/optional): Description.<br>- `paramName2` (type, required/optional): Description. |
| **Internal Parameters** | - `internalParam` (type): Description of resolved/computed values. |
| **Acceptance Criteria** | 1. Step one of the workflow.<br>2. Step two.<br>3. On success, return `{ field1, field2 }`. |
| **Error Messages** | - **Condition**: "Error message text."<br>- **Condition2**: "Error message text." |
```

---

## Field Definitions

### Endpoint
- List all API endpoints required for the action
- Include discovery/lookup endpoints if needed
- Use exact paths with placeholders for IDs

### Input Parameters
- Parameters the user provides when invoking the action
- Include type, required/optional status, and clear description
- Use exact API field names

### Internal Parameters
- Values computed or resolved during execution
- Not provided by user, derived from API responses
- Example: IDs resolved from lookups

### Acceptance Criteria
- Numbered steps describing the exact workflow
- Include pagination handling if applicable
- Include filtering/matching logic
- Specify success response format

### Error Messages
- User-friendly error messages for each failure mode
- Use placeholders for dynamic values: `{paramName}`
- Cover: not found, validation, auth, API errors

---

## Standard Error Categories

Include these error types as applicable:

| Category | Template |
|----------|----------|
| Not found | "No [resource] found with [identifier]. Please verify the [field]." |
| Validation | "[Field] is required and must be [constraint]." |
| Auth failure | "Access denied. Verify [permission type] permissions." |
| API error | "Failed to [action]: {statusCode} - {errorMessage}." |
| Rate limit | "Rate limit exceeded. Please try again in {seconds} seconds." |

---

## Workflow

### Step 1: Gather API Documentation

Ask user for:
- API documentation URL or content
- Endpoint details (method, path, parameters)
- Authentication requirements
- Any specific business logic

**Do not proceed without documentation.**

### Step 2: Identify Actions

From the documentation, identify distinct actions. Each action should be:
- **Single purpose** - One API operation per ticket
- **Self-contained** - All info needed to implement
- **Testable** - Clear success/failure criteria

### Step 3: Write Each Specification

For each action:
1. **Action Title** - Clear, verb-first name (e.g., "Send Message to 1-on-1 Teams Chat")
2. **Objective** - One sentence explaining the user value
3. **Endpoint** - All required API paths
4. **Input Parameters** - User-provided values
5. **Internal Parameters** - Computed/resolved values
6. **Acceptance Criteria** - Step-by-step implementation workflow
7. **Error Messages** - All failure scenarios

### Step 4: Review & Refine

Present specs to user for review. Ask:
- "Does this capture the API behavior correctly?"
- "Any edge cases I should add?"
- "Any parameters I missed?"

### Step 5: Create in Linear

After user approval, create ticket in Linear:

```bash
python3 03-skills/linear-connect/scripts/manage_issue.py create \
  --team "Platform Squad" \
  --title "[Action Title]" \
  --description "[Full specification in markdown]" \
  --project "[User's project or default]" \
  --labels "Integration" \
  --assignee "adeel.akram@beam.ai"
```

**Default settings:**
- Label: `Integration`
- Assignee: Adeel Akram (adeel.akram@beam.ai)

---

## Example

### Input
User provides Microsoft Graph API docs for sending Teams messages.

### Output

## 1. Action Title: Send Message to 1-on-1 Teams Chat

**Objective:** Send a plain-text message to a one-on-one Microsoft Teams chat by automatically resolving the chat using the authenticated user's email and the recipient's email.

| Field | Details |
|-------|---------|
| **Endpoint** | - Discovery: `GET /v1.0/me/chats?$filter=chatType eq 'oneOnOne'&$expand=members&$top=100`<br>- Send: `POST /v1.0/chats/{chatId}/messages` |
| **Input Parameters** | - `recipientEmail` (string, required): The userPrincipalName of the other participant in the one-on-one chat.<br>- `messageContent` (string, required): Text body of the message. |
| **Internal Parameters** | - `resolvedChatId` (string): ID of the chat matching exactly `recipientEmail` from members in chats list. |
| **Acceptance Criteria** | 1. Call `GET /me/chats` to retrieve all chats.<br>2. Check for `@odata.nextLink` to resolve pagination (max 3 pages).<br>3. Filter to chats where members' email exactly matches `recipientEmail`.<br>4. If none found, return error and stop.<br>5. Take first match, set `resolvedChatId` to its `id`.<br>6. POST to `/chats/{resolvedChatId}/messages` with constructed body.<br>7. On HTTP 201, return `{ id, createdDateTime, body.content }`. |
| **Error Messages** | - **Chat not found**: "No one-on-one chat found with user {recipientEmail}. Please verify the email."<br>- **Empty/oversized content**: "Message content is required and must be under service limits."<br>- **Auth failure**: "Access denied. Verify Graph permissions."<br>- **API error**: "Failed to send message: {statusCode} - {errorMessage}." |

---

## Tips

- **Be precise with endpoints** - Include query parameters, filters, expansions
- **Document pagination** - Many APIs require handling nextLink/cursors
- **Include all HTTP methods** - GET for discovery, POST/PUT/DELETE for actions
- **Error messages should be actionable** - Tell user what to fix
- **Use consistent naming** - camelCase for parameters, match API docs
