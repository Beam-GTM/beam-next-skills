# Context Files Endpoint

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
