# Beam AI Agent Building Guide

Best practices and gotchas for creating agents on the Beam AI platform — via API or dashboard.

---

## Node Configuration

### Tool Name (max 40 characters)
- The **tool name** (display name) must be **40 characters or fewer**
- The **node objective** can be longer — it's the description shown in the node card
- If you hit the limit, use abbreviations or shorter synonyms

| Too Long (56 chars) | Fixed (35 chars) |
|---------------------|------------------|
| "Generate structured correspondence brief from extracted data" | "Structure correspondence Generation" |
| "Extract structured information from government correspondence" | "Information Extraction" |
| "Parse brief approval and extract additional instructions" | "Brief Approval Parser" |
| "Fetch and summarize prior correspondence history for context" | "Correspondence History Fetch" |
| "Generate context-aware draft response to original sender" | "Draft Response Generation" |

### Prompts — Curly Brace Rules
- **Parameter reference**: Use `` ```{param_name}``` `` (triple backticks + single curly braces) to inject an input parameter's value into the prompt
- **Literal curly braces** (JSON examples, templates): Use `{{double_curly_braces}}` — Beam passes these through as-is
- **Single `{anything}` NOT wrapped in triple backticks**: Beam tries to resolve it as a parameter. If it doesn't match an input param, **the task will fail**

```
CORRECT:   The sender is ```{email_from}```
CORRECT:   Example JSON: {{"date": "2026-04-15", "context": "deadline"}}
WRONG:     Example JSON: {"date": "2026-04-15"}     ← Beam tries to resolve {date} as param
WRONG:     The sender is {email_from}                ← Not wrapped in triple backticks
```

### Input Parameters
Every input parameter defined on a node should be referenced in the prompt using the `` ```{param_name}``` `` syntax. Parameters that exist but aren't referenced in the prompt won't be passed to the LLM.

### Output Parameters
- Always set `isArray: false` unless the output is genuinely an array
- Use `enum` type with `typeOptions.enumValues` for classification outputs (better than free-text string)
- Output param descriptions help the LLM understand what format to produce

---

## API Patterns

### Creating a New Agent (full graph)
```
POST /agent-graphs/complete
```
Creates agent + graph in one call. Good for initial setup.

### Updating an Existing Agent (full graph replacement)
```
PUT /agent-graphs/{agentId}
```
Replaces the entire draft graph. **Dangerous** — can overwrite UI changes (conditions, integration configs). Use only for initial deployment.

### Updating Node Prompts (safe, surgical)
```
PATCH /agent-graphs/{agentId}/nodes/{nodeId}/prompt
Body: {"prompt": "new prompt text"}
```
Only touches the prompt. Does not affect edges, conditions, params, or integrations. **Preferred for iterative updates.**

### Updating Node Input/Output Params
```
PATCH /agent-graphs/{agentId}/nodes/{nodeId}/input-output-params
Body: {"inputParams": [...], "outputParams": [...]}
```

### Adding Nodes Incrementally
```
POST /agent-graphs/add-node
POST /agent-graphs/add-edge
```
Better than PUT for adding to an existing graph.

### When to Use What

| Task | Method | Why |
|------|--------|-----|
| First-time agent creation | `POST /agent-graphs/complete` or `PUT` | One-shot setup |
| Update prompts only | `PATCH .../nodes/{id}/prompt` | Safe, no side effects |
| Update params only | `PATCH .../nodes/{id}/input-output-params` | Safe, no side effects |
| Add a new node | `POST /agent-graphs/add-node` + `add-edge` | Incremental, doesn't touch existing |
| Full graph rewrite | `PUT /agent-graphs/{agentId}` | Nuclear option — use sparingly |

---

## Payload Requirements

### Input Params (required fields)
```json
{
  "fillType": "ai_fill",
  "position": 0,
  "required": true,
  "dataType": "string",
  "paramName": "email_from",
  "paramDescription": "Sender email address",
  "outputExample": "ahmed@adec.gov.ae",
  "reloadProps": false,
  "remoteOptions": false
}
```
- `reloadProps` and `remoteOptions` are **required booleans** — omitting them causes a 400 error
- `fillType` options: `ai_fill`, `static`, `user_fill`, `linked`, `from_memory`, `from_task_attachment`

### Output Params (required fields)
```json
{
  "isArray": false,
  "paramName": "classification",
  "position": 0,
  "paramDescription": "Description of output",
  "dataType": "string",
  "outputExample": "new_request"
}
```
- `isArray` is **required** — omitting it causes validation errors on push

### Edges with Conditions
- `condition` field must be a **string** (not null) — use empty string `""` if no condition
- For enum-based routing, use `conditionGroups` with `rules` that reference output param IDs
- When re-pushing a graph fetched from GET, conditionGroups may have null `sourceNodeId`/`sourceOutputParamName` — these cause 400 errors on PUT. Use PATCH per-node instead.

---

## Authentication

### Token Flow
1. Exchange API key for access token: `POST /auth/access-token` with `{"apiKey": "..."}` → returns `idToken`
2. Use `idToken` as `Authorization: Bearer {token}`
3. Include `current-workspace-id` header on all requests
4. Tokens expire in ~60 minutes — refresh via `POST /auth/refresh-token`

### Workspace ID
- The workspace ID comes from the agent URL: `https://app.beam.ai/{workspaceId}/{agentId}/flow`
- It's NOT the same as BEAM_WORKSPACE_ID in .env (that's the BID/staging workspace)
- Must match the workspace where the agent lives

---

## Integration Nodes (Airtable, Outlook, Gmail, etc.)

- Integration tool nodes (e.g. `AirtableAction_RecordCreate`, `MicrosoftOutlookAction_DraftMessageReply`) come with pre-defined input params — don't try to set custom ones
- Integration connections must be configured in the Beam dashboard — can't be set via API
- When creating integration nodes via API, set `isIntegrationRequired: true` on the originalTool
- The `integrationProviderId` is assigned by Beam when the user connects the integration in the UI

---

## Common Gotchas

1. **Tool name > 40 chars** → Silent UI truncation, may cause confusion
2. **Single curly braces in prompts** → Task fails at runtime (Beam tries to resolve as param)
3. **Missing `reloadProps`/`remoteOptions` on input params** → 400 error on PUT
4. **Missing `isArray` on output params** → Validation error on push
5. **PUT full graph after UI edits** → Overwrites conditionGroups, integration configs, edge conditions
6. **`condition: null` in edges** → 400 error. Must be empty string `""`
7. **Re-pushing GET response directly** → conditionGroups have null FK fields that fail on PUT
8. **Entry node prompt** → The trigger/entry node is for input config only, not LLM processing. Add a separate GPT node after it for any classification/processing logic.

---

## Testing

### Via Dashboard
- Click "Run Test" on the agent page
- Fill in entry node inputs manually
- Watch execution node-by-node

### Via API
```
POST /agent-tasks
Body: {"agentId": "...", "taskQuery": {"query": "your input text"}}
```
- `taskQuery` must be an object with a `query` string property (not a plain string)
- The entry node's AI fills will extract params from the query text
- Monitor: `GET /agent-tasks/{taskId}` for status and node outputs
- Real-time: `GET /agent-tasks/{taskId}/updates` (SSE stream)

### Consent Gates
- Nodes with `requiresConsent: true` pause execution
- Approve via: `POST /agent-tasks/execution/{taskId}/user-consent`
- Or approve in the dashboard UI

---

**Last updated**: 2026-03-29
**Source**: Learned from building the SGO Correspondence Brief & Response Agent
