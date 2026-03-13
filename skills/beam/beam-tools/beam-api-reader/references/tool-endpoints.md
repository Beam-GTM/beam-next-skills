# Tool Endpoints

Endpoints for optimizing tool performance.

---

## Get Preferred Models

Retrieve the list of LLM models available and preferred for the workspace. Use this to get valid model values for `preferredModel` and `fallbackModels` fields when creating or updating agent nodes.

**Endpoint:** `GET /custom-tool/preferred-models`

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `x-api-key` | Yes | Your Beam AI API key |
| `current-workspace-id` | Yes | Your workspace identifier |

### Response (200 OK)

Returns an array of model objects:

```json
[
  {
    "id": "model-uuid",
    "name": "Claude Sonnet 4",
    "value": "BEDROCK_CLAUDE_SONNET_4",
    "isDefault": true,
    "workspaceGroupId": "group-uuid",
    "isPremium": false,
    "creditsCost": 10,
    "inputTokenPrice": 0.000003,
    "outputTokenPrice": 0.000015,
    "isChatEnabled": true,
    "LlmsGroup": {
      "id": "group-uuid",
      "name": "Anthropic",
      "description": "Anthropic Claude models",
      "icon": "https://...",
      "isActive": true,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "models": [...]
    }
  }
]
```

### Key Fields

| Field | Description |
|-------|-------------|
| `value` | Use this as the `preferredModel` or in `fallbackModels` string |
| `isDefault` | Whether this is the workspace default model |
| `isPremium` | Premium models may have usage restrictions |
| `isChatEnabled` | Whether the model can be used for chat/agent tasks |
| `creditsCost` | Credits consumed per use |
| `LlmsGroup` | Parent model group (e.g. Anthropic, OpenAI, Google) |

### Example

```bash
curl -X GET "https://api.beamlearning.io/custom-tool/preferred-models" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

---

## Optimize Tool

Optimize a tool's prompt and configuration based on usage patterns and feedback from task executions.

**Endpoint:** `POST /tool/optimize/{toolFunctionName}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `toolFunctionName` | string | Yes | Tool function identifier |

### Request Body

```json
{
  "taskNodes": [
    {
      "feedback": "Output was missing email field",
      "positive": false,
      "expectedOutput": "Should include name and email",
      "id": "task-node-uuid"
    },
    {
      "feedback": "Good extraction",
      "positive": true,
      "expectedOutput": "",
      "id": "task-node-uuid-2"
    }
  ],
  "agentId": "agent-uuid",
  "autoUpdateTool": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `taskNodes` | array | Yes | Task node examples with feedback |
| `taskNodes[].id` | string | Yes | Task node UUID |
| `taskNodes[].feedback` | string | Yes | What went wrong/right |
| `taskNodes[].positive` | boolean | Yes | Whether output was good |
| `taskNodes[].expectedOutput` | string | No | Expected result |
| `agentId` | string | Yes | Agent UUID |
| `autoUpdateTool` | boolean | No | Auto-apply optimization |

### Response (201 Created)

```json
{
  "threadId": "optimization-thread-uuid"
}
```

Use the `threadId` to check optimization status.

---

## Get Tool Optimization Status

Check the status of an ongoing tool optimization process.

**Endpoint:** `POST /tool/optimization-status/thread/{threadId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `threadId` | string | Yes | Optimization thread ID (from optimize response) |

### Response (201)

```json
{
  "threadId": "optimization-thread-uuid"
}
```

Returns current status of the optimization process.

---

## Optimization Workflow

1. **Get task nodes by tool** — `GET /agent-graphs/agent-task-nodes/{toolFunctionName}` (see agent-endpoints.md)
2. **Rate outputs** — `PATCH /agent-tasks/execution/{taskId}/output-rating` (see task-endpoints.md)
3. **Submit for optimization** — `POST /tool/optimize/{toolFunctionName}`
4. **Check status** — `POST /tool/optimization-status/thread/{threadId}`
5. AI analyzes failures, rewrites prompts, and validates improvements
