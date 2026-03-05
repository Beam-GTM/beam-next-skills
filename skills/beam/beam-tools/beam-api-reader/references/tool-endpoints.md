# Tool Endpoints

Endpoints for optimizing tool performance.

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
