# Context Files Endpoints

## Upload Context File

Upload context files for an agent.

**Endpoint:** `POST /context/agent/{agentId}/file`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uploadSource` | string | Yes | Source designation (use `FILE_UPLOAD`) |
| `taskId` | string | Yes | Associated task identifier (use `""` for direct uploads) |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `x-api-key` | Yes | Your Beam AI API key |
| `current-workspace-id` | Yes | Your workspace identifier |

### Response (201 Created)

Context file uploaded successfully.

### Example

```bash
curl -X POST "https://api.beamlearning.io/context/agent/YOUR_AGENT_ID/file?uploadSource=FILE_UPLOAD&taskId=" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID" \
  -F "file=@/path/to/document.pdf"
```

---

## Download Context File

Generate a download link for an agent context file.

**Endpoint:** `GET /context/agent/{agentId}/file/{fileId}/download`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | Yes | Agent UUID |
| `fileId` | string | Yes | File UUID |

### Response (200 OK)

```json
{
  "downloadUrl": "https://storage.example.com/files/document.pdf?token=..."
}
```

### Example

```bash
curl -X GET "https://api.beamlearning.io/context/agent/YOUR_AGENT_ID/file/YOUR_FILE_ID/download" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```
