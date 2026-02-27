# Beam API Reference

Complete API documentation for Beam AI platform.

## Base URL

```
https://api.beamstudio.ai
```

## Authentication

All requests require:
- `Authorization: Bearer {access_token}` - Token from /auth/access-token
- `current-workspace-id: {workspace_id}` - Your workspace ID

---

## Authentication Endpoints (2)

### POST /auth/access-token
Exchange API key for access token.

**Request:**
```json
{"apiKey": "bm_key_xxxxxxxxxxxxx"}
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### POST /auth/refresh-token
Refresh an expired access token.

**Request:**
```json
{"refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## User Endpoints (1)

### GET /v2/user/me
Get current user profile.

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```

---

## Agent Endpoints (1)

### GET /agent
List all agents in workspace.

**Note:** To create agents programmatically, see **Agent Setup** and **Agent Graph** endpoints below.

**Query Parameters:**
- None required

**Response:**
```json
[
  {
    "id": "agent-uuid",
    "name": "Customer Support Agent",
    "description": "Handles customer inquiries",
    "type": "beam-os",
    "createdAt": "2024-01-15T10:30:00Z"
  }
]
```

---

## Agent Context Files (1)

### GET /agent/{agentId}/context/file/{fileId}/download
Download agent context file.

**Path Parameters:**
- `agentId` - Agent UUID
- `fileId` - File UUID

**Response:** File binary data

---

## Agent Setup Endpoints (4)

### POST /agent-setup/agent-context/feedback
Submit context to get agent configuration suggestion (name, description, personality, category).

**Request:**
```json
{
  "query": "I want to create an agent that processes invoices",
  "threadId": "optional-existing-thread-id"
}
```

**Response:**
```json
{
  "threadId": "1a2036c0-d533-4636-8f51-2a811763ef5c",
  "response": {
    "name": "Invoice Processing Agent",
    "description": "An AI agent that processes invoices...",
    "agentWelcomeMessage": "Hello! I can help process invoices.",
    "agentPersonality": "Professional and detail-oriented",
    "agentCategory": {"id": "...", "title": "..."},
    "themeIconUrl": "https://..."
  }
}
```

### POST /agent-setup/agent-context/file
Upload context files (up to 10) during agent setup. Multipart form data.

**Supported types:** txt, csv, pdf, xls, xlsx, docx, doc, ppt, pptx, png, jpeg, jpg, tiff, heif, bmp

### POST /agent-setup/{agentId}/context-file
Add context files to an existing agent. Same file type support.

### POST /agent-setup
Multi-step agent configuration. Run steps sequentially after creating via /agent-context.

**Steps** (in order):

| Step | Required Fields | Returns |
|------|----------------|---------|
| `GENERATE_SOP` | agentId, query | nextStep: GRAPH_GENERATION |
| `GRAPH_GENERATION` | agentId | nextStep: TOOL_MATCHING |
| `TOOL_MATCHING` | agentId | nextStep: TOOL_GENERATION |
| `TOOL_GENERATION` | agentId | nextStep: TOOL_INTEGRATION |
| `TOOL_INTEGRATION` | agentId | nextStep: UPDATE_AGENT |
| `UPDATE_AGENT` | agentId | nextStep: AGENT_UPDATED |

**Request:**
```json
{
  "query": "Create an agent for customer support",
  "contextFileIds": ["file-uuid-1"],
  "agentId": "agent-uuid",
  "agentSetupStep": "GENERATE_SOP"
}
```

**Response (200):**
```json
{
  "nextStep": "GRAPH_GENERATION",
  "agentResponse": {
    "agent": {
      "id": "agent-uuid",
      "name": "Customer Support Agent",
      "description": "...",
      "workspaceId": "...",
      "type": "beam-os"
    }
  }
}
```

---

## Agent Graph Endpoints (6)

### GET /agent-graphs/{agentId}
Get agent workflow graph.

**Path Parameters:**
- `agentId` - Agent UUID

**Query Parameters:**
- `graphId` (optional) - Specific graph version

**Response:**
```json
{
  "graph": {
    "agentId": "agent-uuid",
    "nodes": [...],
    "isActive": true,
    "isPublished": true
  }
}
```

### POST /agent-graphs/test-node
Test a specific graph node.

**Request:**
```json
{
  "agentId": "agent-uuid",
  "nodeId": "node-uuid",
  "graphId": "graph-uuid",
  "params": {
    "input": "test data"
  }
}
```

### PATCH /agent-graphs/update-node
Update node configuration.

**Request:**
```json
{
  "nodeId": "node-uuid",
  "objective": "New objective",
  "evaluationCriteria": ["Criteria 1", "Criteria 2"],
  "onError": "STOP"
}
```

### POST /agent-graphs/complete
Create a new agent with complete graph structure in one call.

**Request:**
```json
{
  "agentName": "My Agent",
  "agentDescription": "Agent description",
  "settings": {
    "prompts": ["Example input 1"],
    "agentPersonality": "Friendly and helpful",
    "agentRestrictions": "Do not share PII"
  },
  "nodes": [
    {
      "id": "node-uuid",
      "objective": "What this node does",
      "isEntryNode": true,
      "isExitNode": false,
      "xCoordinate": 116,
      "yCoordinate": 150,
      "onError": "STOP",
      "toolConfiguration": {
        "toolFunctionName": "tool_function_name",
        "toolName": "Tool Name",
        "description": "Tool description",
        "preferredModel": "gpt-4o",
        "prompt": "System prompt",
        "inputParams": [],
        "outputParams": []
      },
      "childEdges": [
        {
          "sourceAgentGraphNodeId": "node-uuid",
          "targetAgentGraphNodeId": "next-node-uuid",
          "condition": "",
          "name": "Next Step"
        }
      ]
    }
  ]
}
```

**Response (201):**
```json
{
  "agentId": "agent-uuid",
  "agentName": "My Agent",
  "activeGraphId": "graph-uuid",
  "draftGraphId": "draft-graph-uuid"
}
```

### PUT /agent-graphs/complete/{agentId}
Update an existing agent and replace its draft graph. Same request body as POST.

### GET /agent-graphs/agent-task-nodes/{toolFunctionName}
Get nodes using a specific tool.

**Path Parameters:**
- `toolFunctionName` - Tool function name (e.g., "send_email")

**Query Parameters:**
- `agentId` (optional) - Filter by agent
- `isRated` (optional) - Filter rated nodes only
- `pageNum`, `pageSize` - Pagination

---

## Agent Task Endpoints (13)

### GET /agent-tasks
List tasks with filtering.

**Query Parameters:**
- `pageNum` - Page number (default: 1)
- `pageSize` - Items per page (default: 10)
- `agentId` - Filter by agent
- `statuses` - Comma-separated statuses (e.g., "QUEUED,COMPLETED,FAILED")
- `searchQuery` - Search in task names
- `ordering` - Sort order (e.g., "createdAt:desc")
- `startDate`, `endDate` - Date range filter
- `grouping` - Group results (e.g., "status")

### POST /agent-tasks
Create new task.

**Request:**
```json
{
  "agentId": "agent-uuid",
  "taskQuery": "Send email to john@example.com with meeting notes",
  "parsingUrls": ["https://example.com/notes.pdf"],
  "encodedContextFiles": []
}
```

**Response:**
```json
{
  "id": "task-uuid",
  "customId": "AGE-785",
  "status": "QUEUED",
  "updatesUrl": "https://api.beamstudio.ai/agent-tasks/task-uuid/updates"
}
```

### GET /agent-tasks/{taskId}
Get task details.

### GET /agent-tasks/{taskId}/updates
Stream task updates (SSE).

**Note:** Returns Server-Sent Events for real-time updates.

### GET /agent-tasks/analytics
Get agent analytics.

**Query Parameters:**
- `agentId` - Agent to analyze
- `startDate`, `endDate` - Analysis period

**Response:**
```json
{
  "currentPeriod": {
    "totalTasks": 150,
    "completedTasks": 135,
    "failedTasks": 15,
    "averageEvaluationScore": 87.5,
    "averageRuntimeSeconds": 45.7
  },
  "metricsDelta": {
    "totalTasksDelta": "+15.5%"
  }
}
```

### GET /agent-tasks/latest-executions
Get recent task executions.

### GET /agent-tasks/iterate
Iterate through tasks (cursor-based pagination).

### GET /agent-tasks/tool-output-schema/{graphNodeId}
Get expected output schema for a tool node.

### POST /agent-tasks/retry
Retry a failed task.

**Request:**
```json
{
  "taskId": "task-uuid"
}
```

### PATCH /agent-tasks/execution/{taskId}/user-input
Provide user input for HITL task.

**Request:**
```json
{
  "input": "User's response to agent question"
}
```

### POST /agent-tasks/execution/{taskId}/rejection
Reject a task execution.

### POST /agent-tasks/execution/{taskId}/user-consent
Approve a HITL task.

### PATCH /agent-tasks/execution/{taskId}/output-rating
Rate task output quality.

**Request:**
```json
{
  "taskNodeId": "node-uuid",
  "rating": "positive",
  "userFeedback": "Task completed correctly",
  "expectedOutput": "Optional expected output"
}
```

---

## Tool Endpoints (2)

### POST /tool/optimize/{toolFunctionName}
Start tool optimization.

**Path Parameters:**
- `toolFunctionName` - Tool to optimize

### POST /tool/optimization-status/thread/{threadId}
Check optimization status.

**Path Parameters:**
- `threadId` - Optimization thread ID

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Rate Limited - Too many requests |
| 500 | Server Error |

---

## Rate Limits

- Default: 100 requests/minute per workspace
- Burst: Up to 10 requests/second
- Long-running operations may have lower limits

---

## Python Example

```python
import requests

# Get access token
auth = requests.post(
    'https://api.beamstudio.ai/auth/access-token',
    json={'apiKey': 'bm_key_xxx'}
)
token = auth.json()['idToken']

# Make API request
headers = {
    'Authorization': f'Bearer {token}',
    'current-workspace-id': 'workspace-uuid'
}

# List agents
agents = requests.get(
    'https://api.beamstudio.ai/agent',
    headers=headers
)
print(agents.json())
```
