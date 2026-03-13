# Agent & Graph Endpoints

## List Agents

Retrieve a paginated list of agents available in your workspace.

**Endpoint:** `GET /agent`
**Base URL:** `https://api.beamlearning.io`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pageNum` | number | No | Page number (min: 1) |
| `pageSize` | number | No | Items per page (min: 1, max: 100) |
| `type` | string | No | `beam-os`, `user-agent`, `pre-configured-agent` |
| `searchQuery` | string | No | Search by name/description |
| `agentCategoryId` | string | No | Filter by category ID |

### Response (200 OK)

```json
{
  "agents": [
    {
      "id": "agent-uuid",
      "name": "Customer Support Agent",
      "description": "Handles customer inquiries",
      "themeIconUrl": "https://...",
      "agentCategoryId": "cat_123456",
      "category": { "id": "cat_123456", "title": "Support" },
      "type": "beam-os",
      "workspaceId": "workspace-id",
      "creatorId": "user-id",
      "order": 1
    }
  ],
  "count": 25
}
```

### Example

```bash
curl -X GET "https://api.beamlearning.io/agent?pageNum=1&pageSize=10&type=beam-os" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

---

## Get Agent Graph

Retrieve the full workflow graph configuration for an agent including nodes, edges, and tool configurations.

**Endpoint:** `GET /agent-graphs/{agentId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `graphId` | string | No | Specific graph version ID |

### Response (200 OK)

Returns a `graph` object with: `id`, `agentId`, `isActive`, `isDraft`, `isPublished`, `publishedAt`, `nodes[]` (with objectives, tool configs, edges), and `agent` summary.

```bash
curl -X GET "https://api.beamlearning.io/agent-graphs/YOUR_AGENT_ID" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

---

## Get Agent Graph with Nodes (Lite)

Retrieve graph and its nodes without full tool configuration details. Lighter response for overview purposes.

**Endpoint:** `GET /agent-graphs/{agentId}/nodes/lite`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `graphId` | string | No | Specific graph version |

### Response (200 OK)

```json
{
  "graphId": "graph-uuid",
  "agentId": "agent-uuid",
  "agentName": "Agent Name",
  "nodes": [
    { "id": "node-uuid", "objective": "Extract parameters" }
  ]
}
```

---

## Get Node Details

Retrieve comprehensive details of a specific node including tool configuration, input/output parameters, and execution settings.

**Endpoint:** `GET /agent-graphs/{agentId}/nodes/{nodeId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `nodeId` | string | Yes | Node UUID |

### Response (200 OK)

Returns full node object with: `objective`, `evaluationCriteria`, `toolConfiguration` (with `inputParams`, `outputParams`, `originalTool`), coordinates, retry settings, edge connections, and timestamps.

---

## Create Complete Agent Graph

Creates a new agent with its complete graph structure including nodes, edges, and tool configurations. Both an active/published graph and a draft graph are created.

**Endpoint:** `POST /agent-graphs/complete`

### Request Body

```json
{
  "agentName": "Bitcoin Price Agent",
  "agentDescription": "Fetches real-time cryptocurrency prices",
  "settings": {
    "prompts": ["What is the current Bitcoin price?"],
    "agentPersonality": "Friendly financial assistant",
    "agentRestrictions": "Do not provide investment advice."
  },
  "nodes": [
    {
      "id": "node-uuid",
      "objective": "Fetch the current Bitcoin price",
      "evaluationCriteria": ["Response contains a valid price"],
      "isEntryNode": true,
      "isExitNode": false,
      "xCoordinate": 116,
      "yCoordinate": 150,
      "isEvaluationEnabled": false,
      "isAttachmentDataPulledIn": true,
      "onError": "STOP",
      "autoRetryCountWhenFailure": 1,
      "autoRetryWaitTimeWhenFailureInMs": 1000,
      "enableAutoRetryWhenFailure": false,
      "toolConfiguration": {
        "toolFunctionName": "GPTAction_Custom_Tool",
        "toolName": "Bitcoin Price Fetcher",
        "description": "Fetches Bitcoin price from API",
        "requiresConsent": false,
        "isMemoryTool": false,
        "isBackgroundTool": false,
        "isBatchExecutionEnabled": false,
        "isCodeExecutionEnabled": false,
        "preferredModel": "gpt-4o",
        "fallbackModels": "DEEP_SEEK,BEDROCK_CLAUDE_3_7_SONNET",
        "prompt": "Fetch the current Bitcoin price.",
        "inputParams": [],
        "outputParams": []
      },
      "childEdges": [
        {
          "sourceAgentGraphNodeId": "node-uuid",
          "targetAgentGraphNodeId": "next-node-uuid",
          "condition": "price > 0",
          "isAttachmentDataPulledIn": true
        }
      ],
      "parentEdges": []
    }
  ]
}
```

### Response (201 Created)

```json
{
  "agentId": "f47ac10b-...",
  "agentName": "My AI Agent",
  "activeGraphId": "a1b2c3d4-...",
  "draftGraphId": "b2c3d4e5-..."
}
```

---

## Update Agent and Draft Graph

Updates an existing agent (name, description, settings) and replaces all nodes and edges in its draft graph.

**Endpoint:** `PUT /agent-graphs/{agentId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `saveAndPublish` | boolean | No | If true, publishes draft as active. Default: false |

### Request Body

Same structure as Create Complete Agent Graph — includes `agentName`, `agentDescription`, `settings`, and `nodes[]`.

### Response (200 OK)

```json
{
  "draftGraphId": "graph-uuid",
  "agentId": "agent-uuid",
  "agentName": "Updated Agent Name"
}
```

---

## Update Graph Node

Modify an existing node's objectives, retry behavior, evaluation settings, and tool configurations. **Use this when updating node details.**

**Endpoint:** `PATCH /agent-graphs/update-node`

### Request Body

```json
{
  "agentId": "agent-uuid",
  "graphId": "graph-uuid",
  "node": {
    "id": "existing-node-uuid",
    "customId": "step-1",
    "objective": "Verify user identity and gather account information",
    "evaluationCriteria": ["User identity verified", "Account status is active"],
    "isAttachmentDataPulledIn": true,
    "isExitNode": false,
    "xCoordinate": 250,
    "yCoordinate": 100,
    "onError": "STOP",
    "isEvaluationEnabled": true,
    "autoRetryWhenAccuracyLessThan": 80,
    "autoRetryLimitWhenAccuracyIsLow": 1,
    "enableAutoRetryWhenAccuracyIsLow": false,
    "enableAutoRetryWhenFailure": true,
    "autoRetryCountWhenFailure": 2,
    "autoRetryWaitTimeWhenFailureInMs": 1000,
    "autoRetryDescription": null,
    "enableAutoRetryDescription": false,
    "toolConfiguration": {
      "toolFunctionName": "GPTAction_Custom_Tool",
      "toolName": "Customer Lookup",
      "shortDescription": "Fetches customer data",
      "description": "Fetches customer data from the database",
      "prompt": "You are a helpful assistant. Look up the customer record.",
      "preferredModel": "gpt-4o",
      "fallbackModels": "DEEP_SEEK,BEDROCK_CLAUDE_3_7_SONNET",
      "iconSrc": null,
      "requiresConsent": false,
      "isMemoryTool": false,
      "memoryLookupInstruction": null,
      "isBackgroundTool": false,
      "isBatchExecutionEnabled": false,
      "isCodeExecutionEnabled": false,
      "isAvailableToWorkspace": false,
      "dynamicPropsId": null,
      "integrationProviderId": null,
      "inputParams": [
        {
          "position": 0,
          "paramName": "customerId",
          "fillType": "ai_fill",
          "question": "What is the customer ID?",
          "paramDescription": "The unique customer identifier",
          "paramTip": "Enter the customer ID",
          "required": true,
          "dataType": "string",
          "outputExample": "CUST-12345"
        }
      ],
      "outputParams": [
        {
          "position": 0,
          "paramName": "customerData",
          "paramDescription": "Retrieved customer record",
          "dataType": "string",
          "isArray": false,
          "paramPath": "response.data",
          "outputExample": "{\"name\": \"John Doe\"}"
        }
      ]
    }
  }
}
```

### Node Fields Reference

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | No | — | Existing node UUID (for updates) |
| `customId` | string | No | — | Custom identifier |
| `objective` | string | Yes | — | Node's purpose/goal |
| `evaluationCriteria` | string[] | Yes | — | Criteria for evaluating output |
| `isAttachmentDataPulledIn` | boolean | Yes | — | Whether to pull attachment data |
| `isExitNode` | boolean | No | `false` | Last node in workflow |
| `xCoordinate` | number | No | — | Canvas X position |
| `yCoordinate` | number | No | — | Canvas Y position |
| `onError` | enum | No | `STOP` | `CONTINUE` or `STOP` |
| `isEvaluationEnabled` | boolean | No | `false` | Enable evaluation scoring |
| `autoRetryWhenAccuracyLessThan` | number | No | `80` | Retry threshold (50-100) |
| `autoRetryLimitWhenAccuracyIsLow` | number | No | `1` | Max retries for low accuracy |
| `enableAutoRetryWhenAccuracyIsLow` | boolean | No | `false` | Enable accuracy-based retry |
| `enableAutoRetryWhenFailure` | boolean | No | `false` | Enable failure-based retry |
| `autoRetryCountWhenFailure` | number | No | `1` | Max retries on failure |
| `autoRetryWaitTimeWhenFailureInMs` | number | No | `1000` | Wait time between retries (ms) |
| `autoRetryDescription` | string | No | `null` | Custom retry instructions |
| `enableAutoRetryDescription` | boolean | No | `false` | Use custom retry instructions |

### Tool Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `toolFunctionName` | string | Yes | Tool function identifier |
| `toolName` | string | No | Display name (max 200 chars) |
| `shortDescription` | string | No | Short desc (max 200 chars) |
| `description` | string | No | Full description |
| `prompt` | string | No | Tool prompt text |
| `preferredModel` | string | No | Preferred LLM model |
| `fallbackModels` | string | No | Comma-separated fallback models |
| `requiresConsent` | boolean | No | Requires user approval |
| `isMemoryTool` | boolean | No | Uses agent memory |
| `memoryLookupInstruction` | string | No | Memory search instruction |
| `isBackgroundTool` | boolean | No | Runs in background |
| `isBatchExecutionEnabled` | boolean | No | Batch processing mode |
| `isCodeExecutionEnabled` | boolean | No | Code interpreter mode |
| `integrationProviderId` | string | No | Integration provider UUID |
| `inputParams` | array | No | Input parameter definitions |
| `outputParams` | array | No | Output parameter definitions |

### Response (200 OK)

Returns updated `MinimalAgentGraphNodeDto` with all node fields, tool configuration, child/parent edges, and timestamps.

### Example

```bash
curl -X PATCH "https://api.beamlearning.io/agent-graphs/update-node" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": "YOUR_AGENT_ID",
    "graphId": "YOUR_GRAPH_ID",
    "node": {
      "id": "NODE_ID",
      "objective": "Updated objective",
      "evaluationCriteria": ["Criteria 1"],
      "isAttachmentDataPulledIn": false,
      "onError": "CONTINUE"
    }
  }'
```

---

## Update Node Prompt

Update the prompt text of the tool used in a specific node.

**Endpoint:** `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/prompt`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `nodeId` | string | Yes | Node UUID |

### Request Body

```json
{
  "prompt": "You are a helpful assistant. Extract the customer name and email from the input."
}
```

### Response (200 OK)

Returns full updated `AgentGraphNode` object with the new prompt in `toolConfiguration`.

### Example

```bash
curl -X PATCH "https://api.beamlearning.io/agent-graphs/YOUR_AGENT_ID/nodes/YOUR_NODE_ID/prompt" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Extract customer name and email from the input."}'
```

---

## Update Node Input/Output Parameters

Update the input and/or output parameters of a tool configuration on a specific node.

**Endpoint:** `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/input-output-params`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `nodeId` | string | Yes | Node UUID |

### Request Body

```json
{
  "inputParams": [
    {
      "position": 1,
      "paramName": "customerId",
      "fillType": "ai_fill",
      "paramDescription": "Customer identifier",
      "required": true,
      "dataType": "string",
      "question": "What is the customer ID?"
    }
  ],
  "outputParams": [
    {
      "position": 1,
      "paramName": "customerData",
      "paramDescription": "Retrieved customer data",
      "dataType": "string",
      "isArray": false,
      "paramPath": "response.data.customer"
    }
  ]
}
```

### Fill Types

| fillType | Description |
|----------|-------------|
| `ai_fill` | AI extracts value from context |
| `static` | Fixed value provided in `staticValue` |
| `user_fill` | User provides value at runtime |
| `from_memory` | Retrieved from agent memory |
| `linked` | Linked from another node's output via `linkParamOutputId` |

### Response (200 OK)

Returns updated `AgentGraphNode` object.

---

## Update Edge in Graph

Update an existing edge's condition or properties.

**Endpoint:** `PUT /agent-graphs/update-edge/{edgeId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `edgeId` | string | Yes | Edge UUID |

### Request Body

```json
{
  "condition": "score > 0.8",
  "isAttachmentDataPulledIn": true
}
```

### Response (200 OK)

```json
{
  "sourceAgentGraphNodeId": "source-node-uuid",
  "targetAgentGraphNodeId": "target-node-uuid",
  "condition": "score > 0.8",
  "isAttachmentDataPulledIn": true,
  "id": "edge-uuid",
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z"
}
```

---

## Test Graph Node

Test a specific node in isolation to validate its configuration and behavior.

**Endpoint:** `POST /agent-graphs/test-node`

### Request Body

```json
{
  "agentId": "agent-uuid",
  "nodeId": "node-uuid",
  "graphId": "graph-uuid",
  "params": {}
}
```

### Response (201 Created)

Returns test execution results.

---

## Publish Agent Graph

Publish a draft agent graph, making it the active/live version. Call this after making changes to push the draft to production.

**Endpoint:** `PATCH /agent-graphs/{graphId}/publish`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `graphId` | string | Yes | Draft graph UUID to publish |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `x-api-key` | Yes | Your Beam AI API key |
| `current-workspace-id` | Yes | Your workspace identifier |

### Response (200 OK)

Returns the published agent graph object with:
- `id`, `agentId` — graph and agent identifiers
- `isPublished: true`, `isDraft: false` — publication status
- `isEdited: false` — reset after publish
- Full node configuration (objectives, tool configs, edges, retry settings, evaluation criteria)
- `isEverExecuted`, `isEverUsedForTemplate` — execution history flags
- Associated `agent` summary

### Example

```bash
curl -X PATCH "https://api.beamlearning.io/agent-graphs/YOUR_GRAPH_ID/publish" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

### When to Use

Call this after any of the following to push changes live:
- Creating a new agent via `POST /agent-graphs/complete`
- Updating the draft graph via `PUT /agent-graphs/{agentId}`
- Modifying nodes via `PATCH /agent-graphs/update-node`

---

## Get Task Nodes by Tool

Retrieve task execution nodes that used a specific tool function. Useful for analysis and optimization.

**Endpoint:** `GET /agent-graphs/agent-task-nodes/{toolFunctionName}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `toolFunctionName` | string | Yes | Tool function identifier |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `isRated` | boolean | Yes | Filter by rating status |
| `pageNum` | number | No | Page number (min: 1) |
| `pageSize` | number | No | Items per page (min: 1, max: 100) |

### Response (200 OK)

```json
{
  "agentTaskNodes": [
    {
      "id": "node-exec-uuid",
      "agentTaskId": "task-uuid",
      "agentGraphNodeId": "graph-node-uuid",
      "status": "COMPLETED",
      "input": {},
      "output": {},
      "toolData": {},
      "userFeedback": "",
      "rating": "positive",
      "evaluationScore": 0.92,
      "agentTask": {},
      "agentGraphNode": {}
    }
  ],
  "count": 50
}
```

---

## Complex Graph Patterns & Examples

This section documents real-world complex graph patterns for creating agents with the Complete Graph API.

### Pattern 1: Conditional Fan-Out (1-to-Many Routing)

A single router node inspects extracted data and branches to N specialized processors, each terminating at its own Send Data node.

#### Example: BID Debt Collection (9 nodes, 4 conditions)

```
Entry Node
    │
    ▼ (unconditional)
0. Receptionist (router + initial extraction, 8 eval criteria, 6 outputs)
    │
    ├── "subfolder = Schreiben Schuldner" → Schreiben Schuldner (37 eval criteria, 3 outputs) → Send Data
    ├── "subfolder = Schreiben Bank" → Schreiben Bank (4 eval criteria, 3 outputs) → Send Data
    ├── "sub_folder contains 'Zurück' or 'zurück'" → TZV Zurück (3 eval criteria, 3 outputs, 1 linked param) → Send Data
    └── "sub_folder is not matched to any criteria" → Send Data (fallback)
```

**Key details:**
- Receptionist outputs: `case_id`, `output_receptionist` (object), `contact_array` (array), `debtor_information` (object), `debtorActivityStates` (array), `bankInformation` (array)
- Schreiben Schuldner has 18 reasoning+value pairs in a single `output_schreiben_schuldner` object + `keyIndicators` array + `cClassificationDecision` object
- TZV Zurück has a **linked param** `bank_information` → linked to Receptionist's `bankInformation` via `linkedOutputParamNodeId` pointing to the **tool config ID**
- All 4 Send Data nodes are identical: `CustomApiTool_SendData-Ratenzuhlung` with 44 ai_fill input params
- All prompts are **empty** — nodes rely on `toolFunctionName`, `paramDescriptions`, and `evaluationCriteria`

### Pattern 2: Multi-Level Routing (Nested Sub-Routers)

A main router fans out to branches, some of which contain their own sub-routers for further conditional branching.

#### Example: E-commerce Order Processing (16 nodes, 8 conditions)

```
Entry Node
    │
    ▼ (unconditional)
Order Intake (main router, 6 eval criteria, 4 outputs)
    │
    ├── "order_type = subscription"
    │       ▼
    │   Subscription Processor (5 eval) ──linked──→ Payment Validator (4 eval) → Send Data
    │
    ├── "order_type = one_time"
    │       ▼
    │   Inventory Checker (4 eval, sub-router)
    │       ├── "in_stock = true"  → Shipping Calculator (4 eval, linked) → Send Data
    │       └── "in_stock = false" → Backorder Handler (4 eval) → Send Data
    │
    ├── "order_type = return"
    │       ▼
    │   Return Analyzer (5 eval, sub-router)
    │       ├── "return_eligible = true"  → Refund Processor (4 eval, linked) → Send Data
    │       └── "return_eligible = false" → Rejection Notifier (3 eval) → Send Data
    │
    └── "order_type not matched" → Send Data (fallback)
```

**Key details:**
- 3 linked params: Payment Validator←Subscription Processor, Shipping Calculator←Inventory Checker, Refund Processor←Return Analyzer
- 2-level routing depth (main router + 2 sub-routers)
- 6 Send Data terminal nodes with 17 shared input params each
- 39 total evaluation criteria across 10 processing nodes

### Critical Implementation Rules

#### Linked Parameters
- `linkedOutputParamNodeId` must point to the **tool configuration ID** (NOT the node ID)
- Use `fillType: "linked"` + `linkedOutputParamName` (name of the output param on parent) + `linkedOutputParamNodeId` (parent's tool config UUID)

#### Edge Mirroring
- Every edge must appear in BOTH the source node's `childEdges[]` AND the target node's `parentEdges[]` with identical condition and `isAttachmentDataPulledIn`

#### Terminal Nodes
- Send Data leaf nodes do NOT need `isExitNode: true` — empty `childEdges: []` is sufficient
- Multiple Send Data nodes can share the same `toolFunctionName`

#### Evaluation Criteria Scale
- Processing nodes can have 3-37+ evaluation criteria
- Entry nodes and Send Data nodes typically have 0 criteria with `isEvaluationEnabled: false`
- Each criterion should be a specific, testable statement about the expected output

#### Output Parameter Patterns
- Position 0 is NOT always `reasoning_steps` — can be domain-specific (e.g., `output_schreiben_schuldner`)
- Complex nested objects: use JSON-stringified schemas in `paramDescription`
- Arrays: set `isArray: true` with schema in `paramDescription`
- Reasoning+value pairs: `"reasoning_fieldName": "<string, 5-7 sentences>"` + `"fieldName": "<type or null>"`

#### Required Fields on Every Node
- `memoryLookupInstruction`: `""` (empty string, required)
- `reloadProps`: `false` (required on all input params)
- `remoteOptions`: `false` (required on all input params)
- `isAttachmentDataPulledIn`: `true` (on nodes and edges)

#### Free Plan Limitations
- Max 3 agents per workspace
- `fallbackModels` must be empty string `""` (not allowed on free plan)
- `preferredModel` can be `null`

### Send Data Node Template (BID Standard — 44 fields)

```
CaseMetaData: case_id, main_folder, sub_folder, receptionist_beam_task_id, cBeamAgentVersion
Letter info: dLetterDate, cLetterLanguage
Death flags: bIsDead, dDeathDate
Debtor details: nDebtorIncome, cDebtorEmployer, nDebtorChildrenCount, dDebtorBirthDate, cDebtorMaritalStatus, cDebtorCountry
TZV fields: bIsSignatureTZV, cFrequencyInstalments, nClaimAmount
Payment amounts: nAmountFirstInstalment, nAmountFurtherInstalments, dDateFirstInstalment
Comparison/depositor: dDateComparisonPayment, bIsDepositorEqualsDebtor, bIsBankersOrderStatus
Payment booleans: bIsOfferedTotalPayment, bIsInstallmentOffered, bPayIn2Rates, bIsDeferment, bIsFoa, bIsPaymentDate, bIsBankDetailsRequest, bIsPaypal
Payment dates: dExactTotalPaymentDate, dDefermentDate, nDefermentDurationMonths
Dispute flags: bIsClaimDisputed, bIsPaymentCompleted
Classification: cCaseClassification, cClassificationReasoning, cClassificationDecisionVariables
Complex arrays: contacts[], debtorActivityStates[], bankInformation[], keyIndicators[]
```

All fields use `fillType: "ai_fill"`, `dataType: "string"` (or `"array"` for complex arrays), `required: false`.
