# Response Schemas & Status Codes

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST request (resource created) |
| 400 | Bad Request | Invalid parameters or malformed request |
| 401 | Unauthorized | Missing or invalid API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server-side error |

---

## Task Statuses

| Status | Description |
|--------|-------------|
| `QUEUED` | Task is queued for execution |
| `IN_PROGRESS` | Task is currently running |
| `COMPLETED` | Task completed successfully |
| `FAILED` | Task failed during execution |
| `ERROR` | Task encountered an error |
| `STOPPED` | Task was stopped (condition failed) |
| `TIMEOUT` | Task timed out |
| `USER_INPUT_REQUIRED` | Task waiting for user input |
| `USER_CONSENT_REQUIRED` | Task waiting for user consent |
| `AUTHENTICATION_REQUIRED` | Task needs authentication |
| `INSUFFICIENT_CREDITS` | Not enough credits to execute |
| `CANCELLED` | Task was cancelled by user |

---

## Common Object Schemas

### Agent Object

```json
{
  "id": "agent-123e4567-e89b-12d3-a456-426614174000",
  "name": "Customer Support Agent",
  "description": "Handles customer inquiries",
  "settings": {
    "prompts": ["You are a helpful customer support agent."],
    "agentPersonality": "Friendly, professional",
    "agentRestrictions": "Do not provide financial advice.",
    "preferredModel": "gpt-4",
    "instructions": "Focus on concise answers."
  },
  "config": {
    "restrictions": "",
    "taskTemplates": [],
    "tools": [],
    "llmTools": [],
    "sop": {},
    "defaultTaskId": "",
    "workspaceId": "workspace-id"
  },
  "workspaceId": "workspace-id",
  "creatorId": "user-id",
  "type": "beam-os",
  "themeIconUrl": "https://example.com/icons/agent.png",
  "agentCategoryId": "category-id",
  "creditUsage": 12.5,
  "order": 1,
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
```

### Agent Types

| Type | Description |
|------|-------------|
| `beam-os` | Standard Beam AI agent |
| `user-agent` | User-created custom agent |
| `pre-configured-agent` | Pre-built template agent |

---

### Task Object (Minimal)

```json
{
  "id": "task-uuid",
  "agentGraphId": "graph-uuid",
  "customId": "TASK-2024-001",
  "originalTaskQuery": "Generate a quarterly sales report",
  "taskObjective": "Analyze sales data and create report",
  "taskQuery": "Generate sales report for Q4 2024",
  "taskSummary": "Successfully generated Q4 sales report",
  "status": "COMPLETED",
  "rating": "positive",
  "averageEvaluationScore": 0.85,
  "tokensUsed": 15000,
  "totalCost": 0.0225,
  "isViewed": true,
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-15T10:05:30Z"
}
```

---

### Task Node Object

Represents execution of a single node/step within a task workflow.

```json
{
  "id": "node-execution-uuid",
  "agentGraphNodeId": "graph-node-uuid",
  "status": "COMPLETED",
  "retriedCountWhenFailure": 0,
  "retriedCountWhenAccuracyIsLow": 0,
  "manualRetryCount": 0,
  "isEverConsentRequired": false,
  "evaluationScore": 0.92,
  "rating": "positive",
  "userFeedback": "",
  "userQuestions": [
    {
      "question": "What is the customer ID?",
      "answer": "CUST-12345",
      "parameter": "customerId",
      "memoryAnswer": false,
      "foodForThought": []
    }
  ],
  "output": {
    "value": {}
  },
  "toolData": {
    "tool_id": "tool-uuid",
    "tool_parameters": [],
    "tool_output": [],
    "required_parameters": {},
    "optional_parameters": {},
    "reasoning": {},
    "filled_prompt": "",
    "integration_identifier": "",
    "integration_error": false
  },
  "agentGraphNode": {
    "id": "graph-node-uuid",
    "customId": "step-1",
    "objective": "Extract parameters",
    "isEntryNode": true,
    "isExitNode": false,
    "onError": "CONTINUE"
  },
  "edgeEvaluations": [
    {
      "target_node_id": "next-node-id",
      "eval_criteria": "Parameters extracted correctly",
      "branch_name": "On Success",
      "reason": "All required parameters found",
      "selected": true
    }
  ]
}
```

---

### Graph Object

```json
{
  "id": "graph-uuid",
  "agentId": "agent-uuid",
  "isActive": true,
  "isDraft": false,
  "isPublished": true,
  "isEdited": false,
  "isEverExecuted": true,
  "publishedAt": "2024-01-01T00:00:00Z",
  "nodes": [],
  "agent": {
    "id": "agent-uuid",
    "name": "Agent Name",
    "description": "Description",
    "type": "beam-os",
    "workspaceId": "workspace-id"
  }
}
```

---

### Graph Node Object

```json
{
  "id": "node-uuid",
  "customId": "step-1",
  "objective": "Verify user identity",
  "evaluationCriteria": ["User identity verified", "Account active"],
  "isEntryNode": true,
  "isExitNode": false,
  "xCoordinate": 250,
  "yCoordinate": 100,
  "isEvaluationEnabled": true,
  "autoRetryWhenAccuracyLessThan": 0.7,
  "autoRetryLimitWhenAccuracyIsLow": 3,
  "enableAutoRetryWhenAccuracyIsLow": true,
  "enableAutoRetryWhenFailure": true,
  "autoRetryCountWhenFailure": 2,
  "autoRetryWaitTimeWhenFailureInMs": 5000,
  "isAttachmentDataPulledIn": false,
  "onError": "CONTINUE",
  "createdAt": "2023-11-07T05:31:56Z",
  "toolConfiguration": {
    "id": "config-uuid",
    "toolFunctionName": "fetchCustomerData",
    "toolName": "Customer Lookup",
    "description": "Fetches customer data from database",
    "requiresConsent": false,
    "isMemoryTool": false,
    "isBackgroundTool": false,
    "isBatchExecutionEnabled": false,
    "isCodeExecutionEnabled": false,
    "inputParams": [],
    "outputParams": []
  },
  "childEdges": [],
  "parentEdges": []
}
```

---

### Credit Transaction Object

```json
{
  "id": "transaction-uuid",
  "transactionType": "subscription_purchase",
  "creditsAmount": 100,
  "tokensUsed": 15000,
  "costAmount": 0.0225,
  "usageCategory": "task_execution",
  "agentGraphNodeId": "node-uuid",
  "toolType": "llm",
  "modelName": "gpt-4"
}
```

---

### Context File Object

```json
{
  "name": "document.pdf",
  "userId": "user-uuid",
  "src": "https://storage.example.com/files/document.pdf",
  "fileKey": "files/document.pdf",
  "uploadStatus": "completed",
  "uploadSource": "file_upload",
  "mimeType": "application/pdf",
  "taskId": "task-uuid",
  "agentTaskId": "agent-task-uuid",
  "url": "https://storage.example.com/files/document.pdf",
  "id": "file-uuid",
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
```

### Upload Status Values

| Status | Description |
|--------|-------------|
| `processing` | File is being processed |
| `completed` | File ready for use |
| `failed` | Upload failed |

### Upload Source Values

| Source | Description |
|--------|-------------|
| `file_upload` | Direct file upload |
| `url_parse` | Parsed from URL |
| `datasource` | From connected datasource |

---

### Token Usage Object

```json
{
  "agentTaskId": "task-uuid",
  "agentGraphNodeId": "node-uuid",
  "executionStage": "QUERY_REFORMULATION",
  "model": "gpt-4",
  "operation": "NORMAL",
  "inputToken": 500,
  "outputToken": 200,
  "reasoningToken": 0,
  "totalToken": 700,
  "isLatest": true,
  "createdAt": "2023-11-07T05:31:56Z"
}
```

### Execution Stages

| Stage | Description |
|-------|-------------|
| `QUERY_REFORMULATION` | Reformulating the task query |
| `PARAMETER_EXTRACTION` | Extracting parameters |
| `TOOL_EXECUTION` | Running tool/integration |
| `EVALUATION` | Evaluating node output |
| `EDGE_EVALUATION` | Evaluating routing conditions |

---

### Rating Values

| Value | Description |
|-------|-------------|
| `positive` | Thumbs up / good result |
| `negative` | Thumbs down / bad result |
| `null` | Not rated |

---

### Edge Object

```json
{
  "id": "edge-uuid",
  "sourceAgentGraphNodeId": "source-node-uuid",
  "targetAgentGraphNodeId": "target-node-uuid",
  "condition": "score > 0.8",
  "name": "On Success",
  "isAttachmentDataPulledIn": true,
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
```

---

### Input Parameter Object

```json
{
  "id": "param-uuid",
  "position": 1,
  "paramName": "customerId",
  "fillType": "ai_fill",
  "question": "What is the customer ID?",
  "paramDescription": "The unique identifier for the customer record.",
  "paramTip": "Enter the 8-digit customer ID.",
  "staticValue": "default_value",
  "linkParamOutputId": "output-param-uuid",
  "required": true,
  "dataType": "string",
  "isArray": false,
  "typeOptions": {},
  "outputExample": "CUST-12345678",
  "reloadProps": false,
  "remoteOptions": false,
  "options": [{ "label": "Option A", "value": "a" }]
}
```

### Fill Types

| fillType | Description |
|----------|-------------|
| `ai_fill` | AI extracts value from context |
| `static` | Fixed value from `staticValue` |
| `user_fill` | User provides at runtime |
| `from_memory` | Retrieved from agent memory |
| `linked` | Linked from another node's output |

### Data Types

| dataType | Description |
|----------|-------------|
| `string` | Text value |
| `number` | Numeric value |
| `boolean` | True/false |
| `object` | JSON object |
| `enum` | Enumerated value from options |

---

### Output Parameter Object

```json
{
  "id": "param-uuid",
  "position": 1,
  "paramName": "customerData",
  "paramDescription": "Retrieved customer data",
  "dataType": "string",
  "isArray": false,
  "typeOptions": {},
  "parentId": null,
  "paramPath": "response.data.customer",
  "outputExample": "{\"name\": \"John Doe\"}",
  "agentToolConfigurationId": "config-uuid"
}
```

---

### Analytics Response Object

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

---

### Setup Session Object

```json
{
  "agentIntroMessage": "I am a customer support agent.",
  "processInstructions": "First gather info, then provide solutions.",
  "agentSop": "Step 1: Greet user. Step 2: Identify issue.",
  "status": "in_progress",
  "step": "GRAPH_GENERATION",
  "generatedGraph": {
    "preliminaryReasoning": "Agent needs multi-step verification.",
    "graphDescription": "Routes through identification and resolution.",
    "trigger": "User sends a message",
    "graphSummary": "5-node workflow from intake to resolution.",
    "mermaidGraph": "graph TD\n  A[Start] --> B[Process]\n  B --> C[End]",
    "graphNodes": []
  }
}
```

### Setup Steps

| Step | Description |
|------|-------------|
| `GENERATE_SOP` | Generating Standard Operating Procedures |
| `GRAPH_GENERATION` | Creating agent workflow graph |
| `TOOL_MATCHING` | Matching existing tools |
| `TOOL_GENERATION` | Generating new custom tools |
| `TOOL_INTEGRATION` | Integrating tools with agent |
| `UPDATE_AGENT` | Finalizing configuration |
| `AGENT_UPDATED` | Setup complete |

---

### View Object

```json
{
  "id": "view-uuid",
  "agentId": "agent-uuid",
  "name": "Customer Records",
  "description": "View of customer data",
  "isActive": true,
  "columns": [
    {
      "id": "col-uuid",
      "dataType": "string",
      "paramName": "customerName",
      "paramDescription": "Customer full name"
    }
  ],
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
```

### Page Info Object (Views)

```json
{
  "totalRows": 123,
  "page": 1,
  "pageSize": 25,
  "isFirstPage": true,
  "isLastPage": false
}
```

---

### Error Handling

| Scenario | HTTP Code | Solution |
|----------|-----------|----------|
| Missing API key | 401 | Add `x-api-key` header |
| Invalid API key | 401 | Verify key in workspace settings |
| Missing workspace ID | 400 | Add `current-workspace-id` header |
| No permissions | 403 | Check workspace role |
| Resource not found | 404 | Verify UUID is correct |
| Invalid parameters | 400 | Check request body format |
| Conflict (duplicate) | 409 | Resource already exists |
| Server error | 500 | Retry or contact support |
