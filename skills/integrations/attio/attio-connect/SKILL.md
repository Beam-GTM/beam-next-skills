---
name: attio-connect
version: '1.0'
description: 'Manage contacts, notes, and lists in Attio CRM. Use when user says:
  ''add contact'', ''update CRM'', ''attio'', ''create note'', ''search contacts'',
  ''add to list'', ''look up in CRM'', ''manage contacts'', or references the Personal
  CRM project.'
category: integrations
tags:
- attio
- connector
- crm
platform: Attio
updated: '2026-02-16'
visibility: public
---
# Attio Connect

Create, read, update, and manage contacts, notes, and lists in Attio CRM via the REST API v2.

## Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| **Create/update person** | `/v2/objects/people/records` | PUT (assert) |
| **Create person** | `/v2/objects/people/records` | POST |
| **Get person** | `/v2/objects/people/records/{id}` | GET |
| **Search people** | `/v2/objects/people/records/query` | POST |
| **Create note** | `/v2/notes` | POST |
| **List notes** | `/v2/notes` | GET |
| **List attributes** | `/v2/objects/people/attributes` | GET |
| **Create attribute** | `/v2/objects/people/attributes` | POST |
| **Create select option** | `/v2/objects/people/attributes/{attr}/options` | POST |
| **List all lists** | `/v2/lists` | GET |
| **Create list** | `/v2/lists` | POST |
| **Add to list** | `/v2/lists/{list_id}/entries` | POST |
| **Query list entries** | `/v2/lists/{list_id}/entries/query` | POST |

**Base URL**: `https://api.attio.com`
**Auth**: `Authorization: Bearer $ATTIO_API_KEY`
**API Key Location**: `02-projects/Personal/projects/04-personal-crm/.env`

---

## Workflows

### 1. Create or Update a Person (Assert/Upsert)

**The most important endpoint.** Creates a new person OR updates an existing one, matched by email.

**When to use**: Adding a contact, importing from another source, updating stale data.

```bash
curl -X PUT "https://api.attio.com/v2/objects/people/records?matching_attribute=email_addresses" \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "values": {
        "email_addresses": ["jane@example.com"],
        "name": [{ "first_name": "Jane", "last_name": "Smith", "full_name": "Jane Smith" }],
        "job_title": ["Staff Engineer"],
        "description": ["Met at YC dinner 2024, works on AI infra"],
        "linkedin": ["https://linkedin.com/in/janesmith"],
        "twitter": ["@janesmith"],
        "primary_location": [{
          "locality": "San Francisco",
          "region": "California",
          "country_code": "US"
        }],
        "CUSTOM_ATTRIBUTE_SLUG": ["value"]
      }
    }
  }'
```

**Key points:**
- `matching_attribute` is a **query parameter** (not in the body)
- `name` requires `full_name` field alongside `first_name`/`last_name`
- LinkedIn field slug is `linkedin` (not `linkedin_url`)
- If found: updates the record
- If not found: creates a new record
- Multiselect values are ADDED (not replaced) when using assert
- `avatar_url` cannot be set via API

**Custom attributes** use their slug (e.g., `relationship_type`, `proximity_tier`). Discover slugs with the List Attributes endpoint.

---

### 2. Search / Query People

Find contacts by filtering on any attribute.

```bash
curl -X POST https://api.attio.com/v2/objects/people/records/query \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "name": { "contains": "Jane" }
    },
    "sorts": [
      { "attribute": "name", "field": "last_name", "direction": "asc" }
    ],
    "limit": 25,
    "offset": 0
  }'
```

**Filter examples:**

```json
// Filter by custom select attribute
{ "ATTRIBUTE_SLUG": { "contains": "value" } }

// Filter by email
{ "email_addresses": { "contains": "jane@example.com" } }
```

**Pagination:** Use `limit` and `offset`. Response includes `next_page_offset` if more results.

---

### 3. Get a Single Person

```bash
curl -X GET https://api.attio.com/v2/objects/people/records/{record_id} \
  -H "Authorization: Bearer $ATTIO_API_KEY"
```

---

### 4. Create a Note on a Contact

Rich text notes attached to a person record.

```bash
curl -X POST https://api.attio.com/v2/notes \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent_object": "people",
      "parent_record_id": "RECORD_ID",
      "title": "Meeting Notes - Feb 2026",
      "format": "plaintext",
      "content": "Discussed AI infrastructure roadmap. Jane is interested in Beam for document processing automation. Follow up in 2 weeks with demo."
    }
  }'
```

**Note fields:**
- `parent_object`: `"people"` or `"companies"`
- `parent_record_id`: The record ID to attach the note to
- `title`: Note title
- `format`: `"plaintext"` or `"html"`
- `content`: The note body

---

### 5. List Notes for a Contact

```bash
curl -X GET "https://api.attio.com/v2/notes?parent_object=people&parent_record_id=RECORD_ID" \
  -H "Authorization: Bearer $ATTIO_API_KEY"
```

---

### 6. Discover Attributes (Schema Discovery)

**Run this first** to learn what custom attributes exist and their slugs.

```bash
curl -X GET https://api.attio.com/v2/objects/people/attributes \
  -H "Authorization: Bearer $ATTIO_API_KEY"
```

Returns all attributes on the People object with their:
- `api_slug` — use this in API calls
- `title` — human-readable name
- `type` — text, select, number, date, etc.
- `is_multiselect` — true/false
- `config.options` — for select/status attributes, the available options

---

### 7. Create a Custom Attribute

```bash
curl -X POST https://api.attio.com/v2/objects/people/attributes \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "title": "Relationship Type",
      "api_slug": "relationship_type",
      "type": "select",
      "is_multiselect": true
    }
  }'
```

**Attribute types:** `text`, `number`, `checkbox`, `currency`, `date`, `timestamp`, `select`, `status`, `rating`, `location`, `domain`, `email-address`, `phone-number`, `record-reference`

---

### 8. Add Select Options to an Attribute

After creating a select attribute, add its options:

```bash
curl -X POST https://api.attio.com/v2/objects/people/attributes/relationship_type/options \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "title": "Investor"
    }
  }'
```

Repeat for each option (Customer, Founder/Peer, Team, Advisor, Friend, Date).

---

### 9. Work with Lists

**List all lists:**
```bash
curl -X GET https://api.attio.com/v2/lists \
  -H "Authorization: Bearer $ATTIO_API_KEY"
```

**Create a new list:**
```bash
curl -X POST https://api.attio.com/v2/lists \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Weekly Ping Queue",
      "parent_object": "people",
      "workspace_access": "full-access"
    }
  }'
```

**Add a person to a list:**
```bash
curl -X POST https://api.attio.com/v2/lists/{list_id}/entries \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "parent_record_id": "RECORD_ID",
      "attribute_values": {
        "ATTRIBUTE_SLUG": "value"
      }
    }
  }'
```

**Query list entries:**
```bash
curl -X POST https://api.attio.com/v2/lists/{list_id}/entries/query \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {},
    "limit": 50
  }'
```

---

## CRM Data Model Reference

These are the custom attributes to create for the Personal CRM (see plan.md):

### Select Attributes

| Attribute | Slug | Type | Options |
|-----------|------|------|---------|
| Relationship Type | `relationship_type` | multi-select | Investor, Customer, Founder/Peer, Team, Advisor, Friend, Date |
| Status | `crm_status` | select | Active, Prospect, Dormant, Stale |
| Proximity Tier | `proximity_tier` | select | T1-Inner Circle, T2-Active, T3-Warm, T4-Network, T5-Archive |
| Relationship Quality | `relationship_quality` | select | ⭐ High, Neutral, 🚩 Low |
| Source | `contact_source` | multi-select | LinkedIn, WhatsApp, Instagram, Notion, Event, Intro, Google |
| City | `city_tags` | multi-select | Berlin, Munich, SF, NYC, London, Dubai |
| Context | `context_tags` | multi-select | Beam, YC, University, Hyrox, Conference |
| Special | `special_tags` | multi-select | Bridge, Aspirational, Lifeline, Dormant-Reconnect |

### Text/Date Attributes

| Attribute | Slug | Type |
|-----------|------|------|
| Connection Story | `connection_story` | text |
| How Can I Help | `how_can_i_help` | text |
| Last Interaction | `last_interaction` | date |
| Last Helped | `last_helped` | date |

### Lists

| List | Parent Object | Purpose |
|------|---------------|---------|
| Weekly Ping Queue | People | Contacts to reach out to this week |
| Dormant Reconnect | People | High-value dormant ties to re-engage |
| Aspirational | People | People to build relationships with |

---

## Common Patterns

### Add a New Contact with Full Context
```
1. Assert person (PUT /v2/objects/people/records)
   - Set: name, email, phone, linkedin, company, title, location
   - Set: relationship_type, crm_status, proximity_tier, relationship_quality
   - Set: connection_story, how_can_i_help, contact_source, city_tags, context_tags
   - Set: last_interaction = today
2. Create note (POST /v2/notes)
   - Add detailed context: how you met, topics discussed, personal details
3. Add to list if applicable (POST /v2/lists/{list_id}/entries)
   - Weekly Ping Queue if T1-T2
   - Aspirational if they're a target connection
```

### Search and Filter Contacts
```
1. Query people (POST /v2/objects/people/records/query)
   - Filter by proximity_tier + city_tags = "T1 friends in Berlin"
   - Filter by relationship_type + crm_status = "Active investors"
   - Filter by special_tags = "Bridge contacts"
   - Sort by last_interaction (ascending) = "Who haven't I talked to recently?"
```

### Update Stale Contact Info
```
1. Research via happenstance-connect (get current job, company, etc.)
2. Update person (PUT /v2/objects/people/records, match by email)
   - Update: job_title, company, location
   - Set: crm_status from "Stale" to "Active"
   - Set: last_interaction = today
3. Add note: "Updated info via Happenstance on [date]. Was at [old company], now at [new company]."
```

### Weekly Ping Ritual via API
```
1. Query Weekly Ping Queue list entries
2. For each entry, get the parent person record
3. Check: How Can I Help? Last Interaction? Connection Story?
4. After sending pings, update: last_interaction, last_helped
5. Remove from queue (or mark done)
```

---

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Bad request | Check payload format, attribute slugs |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check token scopes or billing plan |
| 404 | Not found | Check record_id, list_id, attribute slug |
| 409 | Conflict | Record with same unique attribute exists — use assert (PUT) instead of create (POST) |
| 422 | Validation error | Check attribute types and values |
| 429 | Rate limited | Back off and retry |

---

## Tips

- **Always use Assert (PUT) over Create (POST)** — prevents duplicates, auto-merges by email
- **Discover slugs first** — run List Attributes before trying to write custom fields
- **Multiselect behavior differs**: Assert (PUT) overwrites, Update (PATCH) appends
- **Notes are rich text** — can use HTML format for formatting
- **Lists need a parent_object** — usually `"people"` for this CRM
- **Pagination**: Default limit varies, always check for `next_page_offset`

---

## Related Skills

- `happenstance-connect` — Search/research people before adding to Attio
- `lead-research` — Full lead research workflow using Attio as destination
