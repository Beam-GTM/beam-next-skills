---
name: linkedin-outbounding-automation
version: '1.0'
description: Automate LinkedIn outbound from HubSpot company lists. Load when user
  says "linkedin outbounding automation", "linkedin outreach from hubspot", "hubspot
  to heyreach", "prospect C-levels", "run linkedin campaign", or wants to push HubSpot
  segments to LinkedIn outreach via HeyReach.
category: general
tags:
- automation
updated: '2026-02-27'
visibility: public
---
# Skill: LinkedIn Outbounding Automation

**Purpose**: Fully automated LinkedIn outbound — from HubSpot company lists to personalized C-level outreach via HeyReach.

**Load When**:
- User says: "hubspot to heyreach", "linkedin outreach"
- User says: "outbound [company]", "prospect C-levels"
- User says: "run linkedin campaign from hubspot"
- User says: "roll out to [list name]"

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  HUBSPOT → APOLLO → HEYREACH PIPELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HubSpot List  →  Apollo Search  →  HeyReach Campaign       │
│  (Companies)      (Find C-levels)   (LinkedIn Outreach)     │
│                                                             │
│  Mode A: Single company test                                │
│  Mode B: Full list rollout                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

| Tool | Required | Config Location |
|------|----------|-----------------|
| HubSpot | ✅ | `HUBSPOT_ACCESS_TOKEN` in `.env` |
| Apollo | ✅ | `APOLLO_API_KEY` in `.env` |
| HeyReach | ✅ | MCP Server configured |

---

## Workflow

### Step 1: Select HubSpot List

**Find available lists:**
```bash
python3 00-system/skills/hubspot/hubspot-master/scripts/query_list.py --show-lists
```

**For DYNAMIC lists (not shown by default):**
```python
# Search all list types including DYNAMIC
POST https://api.hubapi.com/crm/v3/lists/search
{
    "listIds": [],
    "offset": 0,
    "query": "",
    "count": 500,
    "additionalProperties": ["hs_list_size"]
}
```

---

### Step 2: Extract Companies from HubSpot

```python
# Get list members
GET /crm/v3/lists/{list_id}/memberships?limit=120

# Get company details (batch)
POST /crm/v3/objects/companies/batch/read
{
    "inputs": [{"id": "company_id_1"}, {"id": "company_id_2"}],
    "properties": ["name", "domain", "industry", "linkedin_company_page"]
}
```

**Output**: List of companies with names and domains

---

### Step 3: Find C-Levels via Apollo

**API Endpoint**: `POST https://api.apollo.io/v1/people/search`

**Headers**:
```
Content-Type: application/json
X-Api-Key: {APOLLO_API_KEY}
```

**Request Body**:
```json
{
    "q_organization_name": "Bank Aljazira",
    "person_titles": ["CEO", "CFO", "CIO", "COO", "CMO", "CTO", "Chief", "Managing Director", "VP", "Head"],
    "page": 1,
    "per_page": 25
}
```

**Response Fields**:
- `name` - Full name
- `title` - Job title
- `linkedin_url` - LinkedIn profile URL ← **Key for HeyReach**
- `email` - Email address
- `organization.name` - Company name

---

### Step 4: Add Leads to HeyReach

**Option A: Add to existing campaign**
```
Use: mcp_heyreach_add_leads_to_campaign_v2
Note: Campaign must NOT be in DRAFT status
```

**Option B: Add to lead list (for DRAFT campaigns)**
```
Use: mcp_heyreach_add_leads_to_list_v2
```

**Lead Format**:
```json
{
    "firstName": "Naif",
    "lastName": "Abdulkareem",
    "profileUrl": "https://www.linkedin.com/in/naif-al-abdulkareem-90619283",
    "position": "CEO & Managing Director",
    "companyName": "Bank Aljazira"
}
```

---

### Step 5: Configure Sequence in HeyReach

**3-Touch Sequence Template**:

#### Touch 1: Connection Request (Day 0)
```
{first_name} — researching digital transformation leaders in Saudi banking. 
Impressive what {company} is doing in the region. Would be great to connect.
```

**Fallback (no variables)**:
```
Hi there,

Researching digital transformation leaders in Saudi banking and came 
across your profile. Impressive work. Would be great to connect.
```

#### Touch 2: Intro Message (Day 1-2 after accept)
```
Thanks for connecting, {first_name}!

Quick context — I'm with [YOUR COMPANY]. We [VALUE PROP].

Curious if [PAIN POINT] is on {company}'s radar this year?

Happy to share how [CUSTOMER] approached it — no pitch, just insights.
```

**Fallback**:
```
Thanks for connecting!

I'm with [YOUR COMPANY] — we [VALUE PROP].

Curious if [PAIN POINT] is on the radar this year? Happy to 
share how [CUSTOMER] approached it.
```

#### Touch 3: Follow-Up (Day 5-7 if no response)
```
{first_name} — circling back briefly.

Is [PAIN POINT] a priority for 2025?

We've helped [CUSTOMER] [RESULT].

Worth a 15-min call? If timing's off, just let me know.
```

**Fallback**:
```
Circling back briefly.

Is [PAIN POINT] a priority for 2025?

We've helped [CUSTOMER] [RESULT].

Worth a 15-min call? If timing's off, just let me know.
```

---

## Full Automation Script

For batch processing entire lists:

```python
# Pseudocode for full rollout
for company in hubspot_list:
    # 1. Search Apollo for C-levels
    prospects = apollo_search(
        company_name=company.name,
        titles=["CEO", "CFO", "CIO", "VP", "Head"]
    )
    
    # 2. Filter to those with LinkedIn URLs
    valid_prospects = [p for p in prospects if p.linkedin_url]
    
    # 3. Add to HeyReach
    heyreach_add_leads(
        campaign_id=CAMPAIGN_ID,
        leads=valid_prospects,
        sender_account_id=SENDER_ID
    )
    
    # 4. Rate limit (respect API limits)
    sleep(1)
```

---

## Configuration

### Sender Accounts (HeyReach)

| Name | Account ID | Has Sales Nav |
|------|------------|---------------|
| Karim Daoui | 111643 | No |
| Sara Intikhab | 40189 | Yes |
| Quentin Silvestro | 39960 | No |

### Target Titles (Apollo)

```python
C_LEVEL_TITLES = [
    "CEO", "CFO", "CIO", "COO", "CMO", "CTO",
    "Chief Executive", "Chief Financial", "Chief Information",
    "Chief Operating", "Chief Marketing", "Chief Technology",
    "Managing Director", "General Manager",
    "VP", "Vice President",
    "Head of", "Director"
]
```

---

## Success Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Connection Accept Rate | >30% | Industry avg: 20-40% |
| Reply Rate | >10% | Industry avg: 5-15% |
| Positive Response Rate | >3% | Interested/meeting booked |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Apollo returns 0 results | Try `q_organization_name` instead of `q_organization_domains` |
| HeyReach "fetch failed" | Check MCP server connection, retry |
| "Can't add to DRAFT campaign" | Add leads to the campaign's list instead |
| Missing fallback error | Add fallback message (no variables) to every Send Message node |

---

## Example Usage

**Single Company Test**:
```
User: "outbound Bank Aljazira"
AI: Finds 5 C-levels via Apollo → Adds to HeyReach → Ready to send
```

**Full List Rollout**:
```
User: "roll out to Top 100 - KD"
AI: Pulls 108 companies → Finds ~500 C-levels → Adds to campaign
```

---

**Version**: 1.0
**Created**: 2025-12-17
**Author**: Karim + Nexus
**Integrations**: HubSpot, Apollo, HeyReach

