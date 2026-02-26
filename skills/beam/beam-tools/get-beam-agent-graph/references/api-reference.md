# Beam.ai API Reference

## Authentication

### Get Access Token

**Endpoint:** `POST https://api.beamstudio.ai/auth/access-token`

**Headers:**
```
x-api-key: <your-beam-api-key>
Content-Type: application/json
```

**Response:**
```json
{
  "access_token": "eyJhbGc..."
}
```

## Agent Graphs

### Get Agent Graph

**Endpoint:** `GET https://api.beamstudio.ai/agent-graphs/{agentId}`

**Headers:**
```
Authorization: Bearer <access-token>
x-workspace-id: <workspace-id>
Content-Type: application/json
```

**Response:**
```json
{
  "id": "agent-id",
  "name": "Agent Name",
  "graph": {
    "nodes": [...],
    "edges": [...]
  },
  ...
}
```

## Error Responses

| Status Code | Meaning |
|-------------|---------|
| 401 | Unauthorized - Invalid API key or token |
| 404 | Not Found - Agent ID doesn't exist |
| 403 | Forbidden - No access to workspace |
| 500 | Server Error - Beam API issue |
