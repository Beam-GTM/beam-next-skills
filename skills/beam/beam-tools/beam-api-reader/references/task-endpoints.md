# Task Endpoints

## Create Agent Task

Create a new task for an agent to execute. Queued and processed according to the agent workflow.

**Endpoint:** `POST /agent-tasks`

### Request Body

```json
{
  "agentId": "agent-uuid",
  "taskQuery": {
    "query": "Process this customer inquiry",
    "additionalInfo": "Optional supplementary context"
  },
  "parsingUrls": ["https://example.com/data"],
  "encodedContextFiles": [
    {
      "data": "base64-encoded-content",
      "mimeType": "application/pdf",
      "fileName": "document.pdf",
      "fileSize": 12345
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agentId` | string | Yes | Target agent UUID |
| `taskQuery.query` | string | Yes | Main task query text |
| `taskQuery.additionalInfo` | string | No | Supplementary information |
| `parsingUrls` | array | No | URLs to parse as input |
| `encodedContextFiles` | array | No | Base64-encoded file attachments |

### Response (201 Created)

```json
{
  "id": "task-uuid",
  "status": "QUEUED",
  "agentGraphId": "graph-uuid",
  "taskObjective": "Process customer inquiry",
  "tokensUsed": 0,
  "totalCost": 0,
  "createdAt": "2024-01-15T10:00:00Z",
  "updatesUrl": "/agent-tasks/task-uuid/updates"
}
```

### Example

```bash
curl -X POST "https://api.beamlearning.io/agent-tasks" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "your-agent-id", "taskQuery": {"query": "Generate Q4 sales report"}}'
```

---

## List Agent Tasks

Retrieve a paginated list of agent tasks with filtering and grouping options.

**Endpoint:** `GET /agent-tasks`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pageNum` | number | No | Page number |
| `pageSize` | number | No | Items per page |
| `agentId` | string | No | Filter by agent ID |
| `statuses` | string | No | Filter by status (e.g. `"COMPLETED"`) |
| `searchQuery` | string | No | Search task content |
| `ordering` | string | No | Sort order |
| `startDate` | string | No | Filter from date |
| `endDate` | string | No | Filter to date |
| `grouping` | enum | No | Group results by (`"status"`) |

### Response (200 OK)

```json
{
  "data": [
    {
      "tasks": [
        {
          "id": "task-uuid",
          "agentGraphId": "graph-uuid",
          "customId": "TASK-001",
          "tokensUsed": 15000,
          "totalCost": 0.0225,
          "taskSummary": "Successfully processed inquiry",
          "status": "COMPLETED",
          "rating": "positive",
          "averageEvaluationScore": 0.85,
          "createdAt": "2024-01-15T10:00:00Z",
          "agentTaskNodes": [],
          "contextFiles": [],
          "agentGraph": {}
        }
      ],
      "groupName": "COMPLETED",
      "groupCount": 150
    }
  ],
  "totalCount": 150
}
```

### Example

```bash
curl -X GET "https://api.beamlearning.io/agent-tasks?agentId=ID&statuses=FAILED&startDate=2024-01-01" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

---

## Get Task Details

Retrieve detailed information about a specific task including execution nodes, graph state, and cost data.

**Endpoint:** `GET /agent-tasks/{taskId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Response (200 OK)

Returns full task object: metadata, execution details (`tokensUsed`, `totalCost`), task content (`objective`, `query`, `summary`), `agentTaskNodes[]`, `contextFiles[]`, `creditTransactions[]`, `agentGraph`, and `graphState`.

---

## Get Task Updates (SSE)

Subscribe to real-time updates for a task using Server-Sent Events.

**Endpoint:** `GET /agent-tasks/{taskId}/updates`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Response (200 OK)

Returns `text/event-stream` with real-time status changes and node execution progress.

```python
import requests

url = "https://api.beamlearning.io/agent-tasks/YOUR_TASK_ID/updates"
headers = {"x-api-key": "YOUR_API_KEY"}

with requests.get(url, headers=headers, stream=True) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode())
```

---

## Get Next Task (Iterate)

Navigate through tasks based on filters. Useful for task queue processing.

**Endpoint:** `GET /agent-tasks/iterate`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | No | Filter by agent |
| `taskId` | string | No | Current task (find next/previous) |
| `statuses` | string | No | Filter by status |
| `searchQuery` | string | No | Search query |
| `grouping` | enum | No | Group by: `"status"` |

### Response (200 OK)

```json
{
  "previous": { "id": "prev-task-id", "agentGraph": { "agentId": "agent-id" } },
  "next": { "id": "next-task-id", "agentGraph": { "agentId": "agent-id" } }
}
```

---

## Retry Task Execution

Retry a failed or incomplete task with optional feedback modifications.

**Endpoint:** `POST /agent-tasks/retry`

### Request Body

```json
{
  "taskId": "task-uuid",
  "taskNodeId": "node-uuid",
  "taskNodeFeedbackAsText": "Please use the correct email format",
  "taskNodeFeedbackPerKeys": [
    { "outputKey": "email", "description": "Must be a valid email address" }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `taskId` | string | Yes | Task to retry |
| `taskNodeId` | string | Yes | Node to retry from |
| `taskNodeFeedbackAsText` | string | No | General feedback |
| `taskNodeFeedbackPerKeys` | array | No | Per-output-key feedback |

### Response (201 Created)

Empty response body. Task re-queued for execution.

---

## Submit User Input

Provide user input for a task paused at `USER_INPUT_REQUIRED` status.

**Endpoint:** `PATCH /agent-tasks/execution/{taskId}/user-input`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Request Body

```json
{
  "taskNodeId": "node-uuid",
  "userInputs": [
    {
      "question": "What is the customer ID?",
      "answer": "CUST-12345",
      "parameter": "customerId"
    }
  ]
}
```

### Response (200 OK)

Returns updated `MinimalAgentTaskDto` with new status and execution details.

---

## Approve Task Execution

Approve a task that requires user consent to continue (HITL workflow).

**Endpoint:** `POST /agent-tasks/execution/{taskId}/user-consent`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Request Body

```json
{
  "taskNodeId": "node-uuid",
  "consent": true,
  "taskId": "task-uuid",
  "feedback": "Looks good, proceed",
  "toolId": "tool-uuid",
  "toolParameters": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `taskNodeId` | string | Yes | Node requiring consent |
| `consent` | boolean | Yes | Approval decision |
| `taskId` | string | Yes | Task UUID |
| `feedback` | string | No | Optional feedback |

### Response (201 Created)

Returns updated `MinimalAgentTaskDto`.

---

## Reject Task Execution

Reject a task that requires user consent. Task stops execution.

**Endpoint:** `POST /agent-tasks/execution/{taskId}/rejection`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Request Body

```json
{
  "taskNodeId": "node-uuid",
  "taskId": "task-uuid",
  "userFeedback": ["Output quality too low", "Missing required fields"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `taskNodeId` | string | Yes | Node being rejected |
| `taskId` | string | Yes | Task UUID |
| `userFeedback` | string[] | Yes | Rejection reasons |

### Response (201 Created)

Returns updated `MinimalAgentTaskDto`.

---

## Rate Task Output

Submit a rating for task execution output to improve agent performance.

**Endpoint:** `PATCH /agent-tasks/execution/{taskId}/output-rating`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | Task UUID |

### Request Body

```json
{
  "rating": "positive",
  "taskNodeId": "node-uuid",
  "userFeedback": "Great output, very accurate",
  "expectedOutput": "Expected result description"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rating` | string | Yes | `"positive"` or `"negative"` |
| `taskNodeId` | string | No | Specific node to rate |
| `userFeedback` | string | No | Feedback text |
| `expectedOutput` | string | No | What was expected |

### Response (200 OK)

Returns updated `MinimalAgentTaskDto`.

---

## Get Agent Analytics

Retrieve analytics data for agent task execution including success rates and performance metrics.

**Endpoint:** `GET /agent-tasks/analytics`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `startDate` | string | Yes | Start date (YYYY-MM-DD) |
| `endDate` | string | Yes | End date (YYYY-MM-DD) |

### Response (200 OK)

```json
{
  "currentPeriod": {
    "totalTasks": 150,
    "completedTasks": 135,
    "failedTasks": 15,
    "averageEvaluationScore": 87.5,
    "averageRuntimeSeconds": 45.7,
    "totalRuntimeSeconds": 6855,
    "positiveFeedbackCount": 120,
    "negativeFeedbackCount": 10,
    "consentRequiredCount": 25
  },
  "metricsDelta": {
    "totalTasksDelta": "+15.5%",
    "completedTasksDelta": "+12.3%",
    "failedTasksDelta": "-5.2%",
    "averageEvaluationScoreDelta": "+4.5%",
    "averageRuntimeSecondsDelta": "-8.7%"
  },
  "taskAndEvaluationChart": [
    {
      "date": "2024-01-25",
      "completedCount": 42,
      "failedCount": 8,
      "averageEvaluationScore": 87.5
    }
  ]
}
```

### Example

```bash
curl -X GET "https://api.beamlearning.io/agent-tasks/analytics?agentId=ID&startDate=2024-01-01&endDate=2024-01-31" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```
