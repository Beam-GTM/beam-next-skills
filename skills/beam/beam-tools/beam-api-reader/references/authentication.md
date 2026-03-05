# Beam AI API Authentication

## Overview

The Beam AI API uses API key authentication. Every request must include two headers.

## Required Headers

| Header | Description | Required |
|--------|-------------|----------|
| `x-api-key` | Your Beam AI API key | Yes (all endpoints) |
| `current-workspace-id` | Your workspace identifier | Yes (most endpoints) |

Some endpoints also accept `Authorization: Bearer <jwt_token>` as an alternative to `x-api-key`.

## Obtaining Credentials

1. Log into the [Beam AI Dashboard](https://app.beam.ai)
2. Go to **Workspace Settings**
3. Navigate to the **API Keys** section
4. Create a new API key or copy an existing one
5. Copy your **Workspace ID** from the same settings page

## Environment Variables

Store credentials in a `.env` file:

```
# Beam.ai - BID instance (development)
BEAM_API_KEY=your_bid_api_key
BEAM_WORKSPACE_ID=your_bid_workspace_id

# Beam.ai - Production instance
BEAM_API_KEY_PROD=your_prod_api_key
BEAM_WORKSPACE_ID_PROD=your_prod_workspace_id
```

## Code Examples

### cURL

```bash
curl -X GET "https://api.beamlearning.io/v2/user/me" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "current-workspace-id: YOUR_WORKSPACE_ID"
```

### Python

```python
import requests

headers = {
    "x-api-key": "YOUR_API_KEY",
    "current-workspace-id": "YOUR_WORKSPACE_ID",
    "Content-Type": "application/json"
}

response = requests.get("https://api.beamlearning.io/v2/user/me", headers=headers)
print(response.json())
```

### JavaScript

```javascript
const response = await fetch("https://api.beamlearning.io/v2/user/me", {
  method: "GET",
  headers: {
    "x-api-key": "YOUR_API_KEY",
    "current-workspace-id": "YOUR_WORKSPACE_ID",
    "Content-Type": "application/json"
  }
});
const data = await response.json();
```

## Base URLs

| Environment | Base URL | Use Case |
|-------------|----------|----------|
| Production  | `https://api.beamlearning.io` | Live production workspaces |
| BID (Dev)   | `https://api.bid.beamstudio.ai` | Development/testing |

## Security Notes

- Never commit API keys to version control
- Store keys in environment variables or secret managers
- Rotate keys periodically
- Use the minimum permissions required
