# Agent Views Endpoints

Endpoints for managing structured data views associated with agents (table-like data).

---

## List All Views

Retrieve all views, optionally filtered by agent.

**Endpoint:** `GET /agent-views`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | string | No | Filter by agent ID |
| `search` | string | No | Filter by view name/description |
| `pageNum` | number | No | Page number (min: 1) |
| `pageSize` | number | No | Items per page (1-100) |

### Response (200 OK)

```json
{
  "views": [
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
  ],
  "total": 5
}
```

---

## List Records from a View

Retrieve paginated records from a specific view with filtering and sorting.

**Endpoint:** `GET /agent-views/{viewId}/records`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `viewId` | string | Yes | View UUID |

### Query Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `pageNum` | number | No | Page number (default: 1) | `1` |
| `pageSize` | number | No | Records per page (default: 25, max: 100) | `25` |
| `fields` | string | No | Comma-separated field names to include | `"field1,field2"` |
| `sort` | string | No | Sort fields (prefix `-` for DESC) | `"createdAt,-priority"` |
| `where` | string | No | Filter conditions | `"(status,eq,active)"` |

### Filter Operators

| Operator | Description |
|----------|-------------|
| `eq` | Equals |
| `gt` | Greater than |
| `lt` | Less than |
| `like` | Pattern match |

### Combining Filters

Use `~and` or `~or` to combine: `(status,eq,active)~and(priority,gt,5)`

### Response (200 OK)

```json
{
  "list": [{}],
  "pageInfo": {
    "totalRows": 123,
    "page": 1,
    "pageSize": 25,
    "isFirstPage": true,
    "isLastPage": false
  }
}
```

---

## List Linked Records for a Link Column

Retrieve records linked through a relationship column.

**Endpoint:** `GET /agent-views/{viewId}/columns/{columnId}/links/{recordId}`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `viewId` | string | Yes | View UUID |
| `columnId` | string | Yes | Link column UUID |
| `recordId` | number | Yes | Source record ID |

### Query Parameters

Same as List Records: `pageNum`, `pageSize`, `fields`, `sort`, `where`.

### Response (200 OK)

```json
{
  "list": [{}],
  "pageInfo": {
    "totalRows": 123,
    "page": 1,
    "pageSize": 25,
    "isFirstPage": true,
    "isLastPage": true
  }
}
```
