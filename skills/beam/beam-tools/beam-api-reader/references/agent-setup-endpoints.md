# Agent Setup Endpoints

Endpoints for creating and configuring agents through the guided setup flow.

**Setup Flow Order:** Upload Context → Submit Context Feedback → Process Setup Steps (GENERATE_SOP → GRAPH_GENERATION → TOOL_MATCHING → TOOL_GENERATION → TOOL_INTEGRATION → UPDATE_AGENT)

---

## Upload Context Files

Upload files (up to 10) to provide context during agent setup.

**Endpoint:** `POST /agent-setup/upload`
**Content-Type:** `multipart/form-data`

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `threadId` | string (UUID) | Yes | Setup thread identifier |
| `files` | file[] | Yes | Up to 10 files |

**Supported file types:** txt, csv, pdf, xls, xlsx, docx, doc, ppt, pptx, png, jpeg, jpg, tiff, heif, bmp

### Response (201 Created)

```json
[
  {
    "name": "document.pdf",
    "src": "https://storage.example.com/...",
    "fileKey": "files/document.pdf",
    "threadId": "thread-uuid",
    "url": "https://...",
    "mimeType": "application/pdf",
    "uploadStatus": "processing",
    "uploadSource": "file_upload",
    "id": "file-uuid",
    "createdAt": "2023-11-07T05:31:56Z"
  }
]
```

---

## Add Context Files to Existing Agent

Upload context files to an agent that already exists.

**Endpoint:** `POST /agent-setup/{agentId}/context-file`
**Content-Type:** `multipart/form-data`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `files` | file[] | Yes | Up to 10 files |

### Response (201 Created)

```json
[
  {
    "id": "file-uuid",
    "name": "document.pdf",
    "src": "https://...",
    "agentId": "agent-uuid",
    "fileKey": "files/document.pdf",
    "uploadStatus": "processing",
    "uploadSource": "file_upload",
    "createdAt": "2023-11-07T05:31:56Z"
  }
]
```

---

## Submit Context Feedback

Provide feedback on uploaded context to refine agent configuration.

**Endpoint:** `POST /agent-setup/agent-context/feedback`

### Request Body

```json
{
  "query": "I want to create an agent for invoice reconciliation",
  "threadId": "1a2036c0-d533-4636-8f51-2a811763ef5c"
}
```

### Response (201 Created)

```json
{
  "threadId": "1a2036c0-d533-...",
  "response": {
    "name": "Customer Support Agent",
    "description": "An AI agent that handles customer inquiries.",
    "agentWelcomeMessage": "Hello! How can I help you today?",
    "agentSetupMessage": "Configured for billing and technical support.",
    "agentPersonality": "Friendly, professional",
    "agentCategory": { "id": "cat-uuid", "title": "Support" },
    "themeIconUrl": "https://..."
  }
}
```

---

## Get Agent Setup Session

Retrieve the current setup session state for an agent, including configuration progress.

**Endpoint:** `GET /agent-setup/session/{agentId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Response (200 OK)

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
| `TOOL_MATCHING` | Matching existing tools to agent needs |
| `TOOL_GENERATION` | Generating new custom tools |
| `TOOL_INTEGRATION` | Integrating tools with the agent |
| `UPDATE_AGENT` | Finalizing agent configuration |
| `AGENT_UPDATED` | Setup complete |

---

## Process Agent Setup Steps

Multi-step agent configuration endpoint. Steps are executed sequentially.

**Endpoint:** `POST /agent-setup`

### Request Body

```json
{
  "query": "I want to create an agent for customer support",
  "contextFileIds": ["file-uuid-1", "file-uuid-2"],
  "agentId": "agent-uuid",
  "agentSetupStep": "GENERATE_SOP"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes (for GENERATE_SOP) | Agent description |
| `contextFileIds` | string[] | No | Uploaded context file IDs |
| `agentId` | string | Yes | Agent UUID |
| `agentSetupStep` | string | Yes | Current step to execute |

### Step Flow

| Current Step | Returns `nextStep` |
|-------------|-------------------|
| `GENERATE_SOP` | `GRAPH_GENERATION` |
| `GRAPH_GENERATION` | `TOOL_MATCHING` |
| `TOOL_MATCHING` | `TOOL_GENERATION` |
| `TOOL_GENERATION` | `TOOL_INTEGRATION` |
| `TOOL_INTEGRATION` | `UPDATE_AGENT` |
| `UPDATE_AGENT` | `AGENT_UPDATED` |

### Response (200 OK)

```json
{
  "nextStep": "GRAPH_GENERATION",
  "agentResponse": {
    "agent": {
      "id": "agent-uuid",
      "name": "Customer Support Agent",
      "description": "...",
      "settings": {
        "prompts": ["You are a helpful customer support agent."],
        "agentPersonality": "Friendly, professional",
        "agentRestrictions": "Do not provide financial advice.",
        "preferredModel": "gpt-4"
      }
    },
    "contextFiles": ["file-uuid"]
  }
}
```
