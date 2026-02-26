---
name: happenstance-connect
version: '1.0'
description: 'Search and research LinkedIn connections via Happenstance API. Use when
  user says: ''search my network'', ''find someone on LinkedIn'', ''research a person'',
  ''who do I know that...'', ''happenstance search'', ''look up a contact''.'
category: integrations
tags:
- api
- connector
- happenstance
platform: Happenstance
updated: '2026-02-16'
visibility: public
---
# Happenstance Connect

Search your LinkedIn network and research people using the Happenstance API.

## Quick Reference

| Action | Endpoint | Method | Credits |
|--------|----------|--------|---------|
| **Search network** | `/v1/search` | POST → poll GET | Yes |
| **Research person** | `/v1/research` | POST → poll GET | Yes |
| **Find more results** | `/v1/search/{id}/find-more` | POST | Yes |
| **List groups** | `/v1/groups` | GET | No |
| **Check credits** | `/v1/usage` | GET | No |

**Base URL**: `https://api.happenstance.ai`
**Auth**: `Authorization: Bearer $HAPPENSTANCE_API_KEY`
**API Key Location**: `02-projects/Personal/projects/04-personal-crm/.env`

---

## Workflows

### 1. Search Your Network

Find people matching a description within your LinkedIn connections.

**When to use**: "Find AI engineers I know", "Who in my network works in VC?", "Find Berlin-based founders"

**Step 1: Submit search**
```bash
curl -X POST https://api.happenstance.ai/v1/search \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "engineers who have worked on AI infrastructure",
    "include_my_connections": true
  }'
```

Response: `{ "id": "search-uuid", "url": "https://happenstance.ai/search/search-uuid" }`

**Step 2: Poll for results** (every 5-10 seconds, typically 30-60 sec)
```bash
curl -X GET https://api.happenstance.ai/v1/search/{search_id} \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

Poll until `status` = `COMPLETED`. Results include:
```json
{
  "results": [
    {
      "id": "person-uuid",
      "name": "Jane Smith",
      "current_title": "Staff Engineer",
      "current_company": "OpenAI",
      "summary": "Led infrastructure team...",
      "weighted_traits_score": 2.5,
      "socials": {
        "happenstance_url": "https://happenstance.ai/u/person-uuid",
        "linkedin_url": "https://linkedin.com/in/janesmith"
      }
    }
  ],
  "has_more": true
}
```

**Step 3: Get more results** (if `has_more` = true)
```bash
curl -X POST https://api.happenstance.ai/v1/search/{search_id}/find-more \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```
Then poll again. Returns up to 30 results per page.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Natural language search query |
| `include_my_connections` | boolean | false | Search your own LinkedIn connections |
| `include_friends_connections` | boolean | false | Search your friends' connections too |
| `group_ids` | string[] | null | Search within specific groups |

---

### 2. Research a Person

Generate a detailed profile about a specific person.

**When to use**: "Research Garry Tan", "Get details on this person before a meeting", "What does [name] do?"

**Step 1: Submit research request**
```bash
curl -X POST https://api.happenstance.ai/v1/research \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Garry Tan Y Combinator CEO"
  }'
```

**Tips for better results**: Include full name, company, title, location, social handles.

Response: `{ "id": "research-uuid" }`

**Step 2: Poll for results** (every 5-10 sec, typically 1-3 min)
```bash
curl -X GET https://api.happenstance.ai/v1/research/{research_id} \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

Status can be: `RUNNING`, `COMPLETED`, `FAILED`, `FAILED_AMBIGUOUS`

Completed response includes:
```json
{
  "profile": {
    "person_metadata": {
      "full_name": "Garry Tan",
      "alternate_names": [],
      "profile_urls": ["linkedin_url", "twitter_url"],
      "current_locations": [{ "location": "San Francisco, CA" }],
      "tagline": "President and CEO of Y Combinator"
    },
    "employment": [
      {
        "company_name": "Y Combinator",
        "job_title": "President and CEO",
        "start_date": "2022",
        "end_date": null,
        "description": "Leads YC..."
      }
    ],
    "summary": {
      "text": "Detailed bio summary...",
      "urls": ["source_urls"]
    }
  }
}
```

**Max concurrent research**: 10 requests (429 if exceeded)

---

### 3. Check Credits

```bash
curl -X GET https://api.happenstance.ai/v1/usage \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

Returns credit balance, purchase history, and usage.

---

### 4. List Groups

```bash
curl -X GET https://api.happenstance.ai/v1/groups \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

Returns group IDs that can be used in search queries.

---

## Integration with Attio CRM

When using Happenstance results to populate Attio:

### Search → Import to Attio
1. Run Happenstance search for a category (e.g., "Berlin founders")
2. Review results — select relevant contacts
3. For each selected contact, use `attio-connect` skill to:
   - Assert person record (upsert by email or LinkedIn URL)
   - Set custom attributes (Type, Tier, Connection Story, etc.)
   - Add note with Happenstance research data

### Research → Enrich Attio Contact
1. Run Happenstance research on a person
2. Extract: current title, company, location, social URLs
3. Update Attio record with fresh data via `attio-connect`
4. Add note: "Enriched via Happenstance on [date]"

---

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Bad request | Check query format |
| 401 | Unauthorized | Check API key |
| 402 | Insufficient credits | Check balance, purchase more |
| 429 | Too many requests | Wait for existing research to complete (max 10 concurrent) |
| 500 | Server error | Retry after 30 seconds |

---

## Tips

- **Search queries are natural language** — be descriptive: "investors who focus on AI startups in Europe" works better than "AI investors"
- **Research needs detail** — include full name + company + title for best results
- **Searches are async** — submit, then poll every 5-10 seconds
- **Credits are consumed** — check balance before bulk operations
- **Results max 30 per page** — use find-more for additional results

---

## Related Skills

- `attio-connect` — Create/update contacts in Attio CRM after searching
- `lead-research` — Full lead research workflow (can use Happenstance as a source)
