# Tool Endpoints

Endpoints for fetching tools, attaching tools to nodes, and optimizing tool performance.

---

## Get Active Tools

Search and retrieve tools available in your workspace. Use this to find integration tools (e.g. Gmail, Slack, Google Drive) that can be attached to agent nodes.

**Endpoint:** `GET /tool/active-tools`

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `x-api-key` | Yes | Your Beam AI API key |
| `current-workspace-id` | Yes | Your workspace identifier |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Filter by tool type. Use `custom_integration_tool` for integration tools (Gmail, Slack, etc.) |
| `searchKeyword` | string | No | Search tools by name (e.g. `gmail`, `slack`, `google`) |

### Example

```bash
curl -X GET "https://api.beamlearning.io/tool/active-tools?type=custom_integration_tool&searchKeyword=gmail" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

### Response (200 OK)

Returns an object with a `tools` array:

```json
{
  "tools": [
    {
      "id": "tool-uuid",
      "toolFunctionName": "gmail-send-email",
      "toolName": "Send Email",
      "type": "beam_tool",
      "iconSrc": "https://cdn.staging.beamstudio.ai/gmail.png",
      "isActive": true,
      "integrationId": "integration-uuid",
      "requiresConsent": false,
      "isBackgroundTool": false,
      "isMemoryTool": false,
      "isBatchExecutionEnabled": false,
      "preferredModel": "GPT40",
      "description": "Send an email from your Google Workspace email account.",
      "meta": {
        "type": "beam_tool",
        "description": "Send an email from your Google Workspace email account.",
        "tool_name": "Send Email",
        "function_name": "gmail-send-email",
        "preferred_model": "GPT40",
        "requires_consent": false,
        "integrationIdentifier": "gmail",
        "required_extracted_args": [
          "to: string[]",
          "subject: string",
          "body: string"
        ],
        "optional_extracted_args": [
          "cc: string[]",
          "bcc: string[]",
          "bodyType: string"
        ],
        "integration_provider_auth": "pipedream",
        "integration_provider_executor": "pipedream",
        "integration_provider_details": {
          "request": {
            "body": { "to": "{{string[]}}", "subject": "{{string}}", "body": "{{string}}" },
            "method": "post",
            "endpoint": "https://api.pipedream.com/v1/connect/{{PROJECT_ID}}/actions/run"
          },
          "response": { "result": "{{result.data?.result}}" }
        }
      },
      "inputParams": [
        {
          "paramName": "to",
          "fillType": "ai_fill",
          "required": true,
          "dataType": "string[]",
          "paramDescription": "Enter a single recipient's email or multiple emails as items in an array."
        }
      ],
      "outputParams": [
        {
          "paramName": "result",
          "paramDescription": "The result of the operation",
          "dataType": "string",
          "isArray": false,
          "position": 0
        }
      ]
    }
  ]
}
```

### Key Response Fields

| Field | Description |
|-------|-------------|
| `toolFunctionName` | Function identifier — use this when attaching the tool to a node |
| `toolName` | Human-readable display name |
| `type` | Tool type (e.g. `beam_tool`) |
| `meta` | Rich metadata: description, args, integration provider details |
| `meta.required_extracted_args` | Required input parameters with types |
| `meta.optional_extracted_args` | Optional input parameters with types |
| `meta.integrationIdentifier` | Integration name (e.g. `gmail`, `slack`) |
| `inputParams` | Input parameter definitions (paramName, fillType, dataType, required) |
| `outputParams` | Output parameter definitions (paramName, dataType, isArray) |
| `iconSrc` | Tool icon URL |
| `preferredModel` | Default model for this tool |

---

## Attach a Tool to a Node

To attach an integration tool (e.g. Gmail Send Email) to an existing agent node, use `PATCH /agent-graphs/update-node`. This replaces the node's current tool configuration with the integration tool.

**Endpoint:** `PATCH /agent-graphs/update-node` (see [agent-endpoints.md](agent-endpoints.md) for full reference)

### Workflow

1. **Find the tool** — `GET /tool/active-tools?type=custom_integration_tool&searchKeyword=gmail`
2. **Get the node details** — `GET /agent-graphs/{agentId}/nodes/{nodeId}`
3. **Update the node** — `PATCH /agent-graphs/update-node` with the tool's configuration

### Example: Attach Gmail Send Email to a Node

```bash
curl -X PATCH "https://api.beamlearning.io/agent-graphs/update-node" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": "agent-uuid",
    "graphId": "graph-uuid",
    "node": {
      "id": "node-uuid",
      "objective": "Send a celebration email for even sums",
      "isAttachmentDataPulledIn": true,
      "evaluationCriteria": [],
      "toolConfiguration": {
        "toolFunctionName": "gmail-send-email",
        "toolName": "Send Email",
        "shortDescription": "Send an email from your Google Workspace email account.",
        "description": "Send an email from your Google Workspace email account.",
        "iconSrc": "https://cdn.staging.beamstudio.ai/gmail.png",
        "preferredModel": "GPT40",
        "requiresConsent": false,
        "isMemoryTool": false,
        "isBackgroundTool": false,
        "isBatchExecutionEnabled": false,
        "integrationProviderId": null,
        "inputParams": [
          {
            "position": 0,
            "paramName": "to",
            "fillType": "ai_fill",
            "paramDescription": "Enter a single recipient email or multiple emails as items in an array.",
            "required": true,
            "dataType": "string[]"
          },
          {
            "position": 1,
            "paramName": "subject",
            "fillType": "ai_fill",
            "paramDescription": "Specify a subject for the email.",
            "required": true,
            "dataType": "string"
          },
          {
            "position": 2,
            "paramName": "body",
            "fillType": "ai_fill",
            "paramDescription": "Include an email body as either plain text or HTML.",
            "required": true,
            "dataType": "string"
          }
        ],
        "outputParams": [
          {
            "position": 0,
            "paramName": "result",
            "paramDescription": "The result of the email send operation",
            "dataType": "string",
            "isArray": false
          }
        ]
      }
    }
  }'
```

### Key Rules

- **`isAttachmentDataPulledIn`** is required on the node — omitting it causes a 400 error
- **`evaluationCriteria`** is required — use `[]` if not needed
- **`toolFunctionName`** must match exactly what the `GET /tool/active-tools` response returns (e.g. `gmail-send-email`, not `GmailAction_SendEmail`)
- **`inputParams`** — map from the tool's `meta.required_extracted_args` and `meta.optional_extracted_args`; set `fillType` as appropriate (`ai_fill`, `static`, `linked`, `user_fill`)
- **`outputParams`** — typically a single `result` param for integration tools
- The node's `objective` should describe what the node does with the tool
- The update is applied to the **draft graph** — publish separately via `PATCH /agent-graphs/{graphId}/publish`

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
