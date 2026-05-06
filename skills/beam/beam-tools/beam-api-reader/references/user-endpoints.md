# User Endpoints

## Get Current User

Retrieve profile information of the currently authenticated user, including their workspaces and permissions.

**Endpoint:** `GET /v2/user/me`
**Base URL:** `https://api.beamlearning.io`

### Authentication

| Method | Header |
|--------|--------|
| API Key | `x-api-key: YOUR_API_KEY` |
| Bearer Token | `Authorization: Bearer YOUR_JWT_TOKEN` |

### Request

No query parameters or request body required.

### Response (200 OK)

```json
{
  "id": "string",
  "name": "John Doe",
  "email": "john@example.com",
  "avatarSrc": "https://example.com/avatars/user123.png",
  "emailVerified": true,
  "isInternalUser": false,
  "createdAt": "2023-11-07T05:31:56Z",
  "updatedAt": "2023-11-07T05:31:56Z",
  "workspaces": [
    {
      "id": "workspace-id",
      "name": "My Workspace",
      "domain": "example.com",
      "iconSrc": "https://...",
      "role": {
        "isOwner": true,
        "isAdmin": true
      },
      "creditBalance": {
        "totalCredits": 1000,
        "usedCredits": 250,
        "lastUpdatedAt": "2023-11-07T05:31:56Z"
      },
      "subscription": {
        "status": "active",
        "billingPeriod": "monthly",
        "paymentProvider": "stripe"
      }
    }
  ],
  "featureFlags": [
    {
      "name": "feature_name",
      "enabled": true
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | User identifier |
| `name` | string | User's full name |
| `email` | string | User's email address |
| `avatarSrc` | string | Avatar image URL |
| `emailVerified` | boolean | Whether email is verified |
| `isInternalUser` | boolean | Internal Beam user flag |
| `createdAt` | datetime | Account creation timestamp |
| `workspaces` | array | List of workspace memberships |
| `workspaces[].id` | string | Workspace identifier |
| `workspaces[].name` | string | Workspace name |
| `workspaces[].role.isOwner` | boolean | Whether user owns workspace |
| `workspaces[].role.isAdmin` | boolean | Whether user is admin |
| `workspaces[].creditBalance` | object | Credit usage information |
| `workspaces[].subscription` | object | Subscription details |
| `featureFlags` | array | Enabled feature flags |

### Example

```bash
curl -X GET "https://api.beamlearning.io/v2/user/me" \
  -H "x-api-key: YOUR_API_KEY"
```
