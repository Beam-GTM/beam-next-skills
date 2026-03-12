# Miro REST API v2 Reference

## Base URL
```
https://api.miro.com/v2
```

## Authentication
```
Authorization: Bearer {MIRO_ACCESS_TOKEN}
Content-Type: application/json
```

---

## Boards

| Method | Path | Description |
|--------|------|-------------|
| GET | /boards | List boards (requires team_id or returns all) |
| POST | /boards | Create board |
| GET | /boards/{board_id} | Get board |
| PATCH | /boards/{board_id} | Update board |
| DELETE | /boards/{board_id} | Delete board |
| PUT | /boards/{board_id}/copy | Copy board |

## Board Members

| Method | Path | Description |
|--------|------|-------------|
| GET | /boards/{board_id}/members | List members |
| POST | /boards/{board_id}/members | Share/invite member |
| GET | /boards/{board_id}/members/{member_id} | Get member |
| PATCH | /boards/{board_id}/members/{member_id} | Update role |
| DELETE | /boards/{board_id}/members/{member_id} | Remove member |

## Items (Generic)

| Method | Path | Description |
|--------|------|-------------|
| GET | /boards/{board_id}/items | List all items |
| GET | /boards/{board_id}/items/{item_id} | Get item |
| PATCH | /boards/{board_id}/items/{item_id} | Update position/parent |
| DELETE | /boards/{board_id}/items/{item_id} | Delete item |

## Sticky Notes

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/sticky_notes | Create |
| GET | /boards/{board_id}/sticky_notes/{item_id} | Get |
| PATCH | /boards/{board_id}/sticky_notes/{item_id} | Update |
| DELETE | /boards/{board_id}/sticky_notes/{item_id} | Delete |

**Colors**: gray, light_yellow, yellow, orange, light_green, green, dark_green, cyan, light_pink, pink, violet, red, light_blue, blue, dark_blue, black

## Cards

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/cards | Create |
| GET | /boards/{board_id}/cards/{item_id} | Get |
| PATCH | /boards/{board_id}/cards/{item_id} | Update |
| DELETE | /boards/{board_id}/cards/{item_id} | Delete |

## Shapes

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/shapes | Create |
| GET | /boards/{board_id}/shapes/{item_id} | Get |
| PATCH | /boards/{board_id}/shapes/{item_id} | Update |
| DELETE | /boards/{board_id}/shapes/{item_id} | Delete |

**Shape types**: rectangle, round_rectangle, circle, triangle, rhombus, parallelogram, trapezoid, pentagon, hexagon, octagon, star, cloud, cross, can, right_arrow, left_arrow, left_right_arrow, left_brace, right_brace

## Text Items

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/texts | Create |
| GET | /boards/{board_id}/texts/{item_id} | Get |
| PATCH | /boards/{board_id}/texts/{item_id} | Update |
| DELETE | /boards/{board_id}/texts/{item_id} | Delete |

## Images

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/images | Create (via URL) |
| GET | /boards/{board_id}/images/{item_id} | Get |
| PATCH | /boards/{board_id}/images/{item_id} | Update |
| DELETE | /boards/{board_id}/images/{item_id} | Delete |

## Documents

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/documents | Create (via URL) |
| GET | /boards/{board_id}/documents/{item_id} | Get |
| PATCH | /boards/{board_id}/documents/{item_id} | Update |
| DELETE | /boards/{board_id}/documents/{item_id} | Delete |

## Embeds

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/embeds | Create |
| GET | /boards/{board_id}/embeds/{item_id} | Get |
| PATCH | /boards/{board_id}/embeds/{item_id} | Update |
| DELETE | /boards/{board_id}/embeds/{item_id} | Delete |

## Frames

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/frames | Create |
| GET | /boards/{board_id}/frames/{item_id} | Get |
| PATCH | /boards/{board_id}/frames/{item_id} | Update |
| DELETE | /boards/{board_id}/frames/{item_id} | Delete |
| GET | /boards/{board_id}/frames/{frame_id}/items | Get items in frame |

## Connectors

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/connectors | Create |
| GET | /boards/{board_id}/connectors | List all |
| GET | /boards/{board_id}/connectors/{id} | Get |
| PATCH | /boards/{board_id}/connectors/{id} | Update |
| DELETE | /boards/{board_id}/connectors/{id} | Delete |

**Shapes**: straight, elbowed, curved

## Tags

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/tags | Create tag |
| GET | /boards/{board_id}/tags | List tags |
| GET | /boards/{board_id}/tags/{tag_id} | Get tag |
| PATCH | /boards/{board_id}/tags/{tag_id} | Update tag |
| DELETE | /boards/{board_id}/tags/{tag_id} | Delete tag |
| GET | /boards/{board_id}/tags/{tag_id}/items | Get items by tag |
| POST | /boards/{board_id}/items/{item_id}/tags | Attach tag |
| GET | /boards/{board_id}/items/{item_id}/tags | Get item tags |
| DELETE | /boards/{board_id}/items/{item_id}/tags/{tag_id} | Detach tag |

**Colors**: red, light_green, cyan, yellow, dark_green, blue, dark_blue, violet, gray, black

## Groups

| Method | Path | Description |
|--------|------|-------------|
| POST | /boards/{board_id}/groups | Create group |
| GET | /boards/{board_id}/groups | List groups |
| GET | /boards/{board_id}/groups/{id} | Get group |
| GET | /boards/{board_id}/groups/{id}/items | Get items in group |
| PUT | /boards/{board_id}/groups/{id} | Update group |
| DELETE | /boards/{board_id}/groups/{id} | Ungroup |

---

## Common Patterns

### Pagination
Miro uses offset-based pagination:
```json
{
  "size": 20,
  "offset": 0,
  "limit": 20,
  "total": 45,
  "data": [...]
}
```

### Position
```json
{
  "position": {
    "x": 0,
    "y": 0,
    "origin": "center"
  }
}
```

### Geometry
```json
{
  "geometry": {
    "width": 200,
    "height": 200
  }
}
```

### Style (varies by item type)
```json
{
  "style": {
    "fillColor": "#FF0000",
    "borderColor": "#000000",
    "fontSize": "14"
  }
}
```

---

## Rate Limits

Credit-based per user per app (100,000 credits/min):

| Level | Credits/Call | Effective RPM |
|-------|-------------|---------------|
| Level 1 (light) | 50 | ~2,000 |
| Level 2 (medium) | 100 | ~1,000 |
| Level 3 (heavy) | 500 | ~200 |
| Level 4 (very heavy) | 2,000 | ~50 |

Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## OAuth Scopes

| Scope | Description |
|-------|-------------|
| boards:read | Read boards, members, items |
| boards:write | Create/update/delete boards, members, items |
| identity:read | Read user profile |
| team:read | Read team info |
| team:write | Manage team |
| projects:read | Read projects |
| projects:write | Manage projects |
