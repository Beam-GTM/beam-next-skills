---
name: hubspot-crm
type: skill
version: '1.0'
description: All HubSpot CRM operations — contacts, companies, deals, engagements, search,
  and associations. Load when user says 'list contacts', 'create deal', 'search companies',
  'log call', 'log email', 'create note', 'create meeting', 'get associations',
  'update contact', 'update deal', 'hubspot search'.
category: integrations
tags:
- hubspot
- crm
platform: HubSpot
updated: '2026-03-23'
visibility: public
---
# HubSpot CRM

Unified reference for all HubSpot CRM operations. All scripts live in `hubspot-master/scripts/`.

Replaces: `hubspot-list-contacts`, `hubspot-create-contact`, `hubspot-update-contact`,
`hubspot-search-contacts`, `hubspot-list-companies`, `hubspot-create-company`,
`hubspot-search-companies`, `hubspot-list-deals`, `hubspot-create-deal`, `hubspot-update-deal`,
`hubspot-search-deals`, `hubspot-create-deal-from-transcript`, `hubspot-list-emails`,
`hubspot-log-email`, `hubspot-list-calls`, `hubspot-log-call`, `hubspot-list-notes`,
`hubspot-create-note`, `hubspot-list-meetings`, `hubspot-create-meeting`,
`hubspot-get-associations`.

## Contacts

```bash
# List contacts (paginated)
uv run python hubspot-master/scripts/list_contacts.py --limit 20
uv run python hubspot-master/scripts/list_contacts.py --limit 50 --properties email,firstname,lastname,company

# Create contact
uv run python hubspot-master/scripts/create_contact.py --email "jane@example.com" --firstname Jane --lastname Doe --company "Acme"

# Update contact
uv run python hubspot-master/scripts/update_contact.py --id 12345 --email "new@example.com" --company "NewCorp"

# Search contacts
uv run python hubspot-master/scripts/search_contacts.py --email "jane@example.com"
uv run python hubspot-master/scripts/search_contacts.py --name "Jane Doe"
uv run python hubspot-master/scripts/search_contacts.py --company "Acme" --limit 10
```

## Companies

```bash
# List companies
uv run python hubspot-master/scripts/list_companies.py --limit 20

# Create company
uv run python hubspot-master/scripts/create_company.py --name "Acme Corp" --domain "acme.com" --industry "Technology"

# Search companies
uv run python hubspot-master/scripts/search_companies.py --name "Acme"
uv run python hubspot-master/scripts/search_companies.py --domain "acme.com"
```

## Deals

```bash
# List deals
uv run python hubspot-master/scripts/list_deals.py --limit 20

# Create deal
uv run python hubspot-master/scripts/create_deal.py --name "Enterprise License" --amount 50000 --stage "appointmentscheduled"

# Update deal
uv run python hubspot-master/scripts/update_deal.py --id 67890 --stage "closedwon" --amount 55000

# Search deals
uv run python hubspot-master/scripts/search_deals.py --name "Enterprise"
uv run python hubspot-master/scripts/search_deals.py --stage "closedwon" --min-amount 10000
```

### Create deal from transcript

Workflow (no dedicated script — compose from existing scripts):

1. Search for contact/company from transcript participants
2. Create deal with extracted details (name, value, stage)
3. Associate deal with contact and company via `get_associations.py`

## Engagements

### Emails

```bash
uv run python hubspot-master/scripts/list_emails.py --limit 20
uv run python hubspot-master/scripts/log_email.py --subject "Follow-up" --body "Thanks for the meeting" --direction EMAIL
```

### Calls

```bash
uv run python hubspot-master/scripts/list_calls.py --limit 20
uv run python hubspot-master/scripts/log_call.py --title "Discovery call" --body "Discussed pricing" --duration 30
```

### Notes

```bash
uv run python hubspot-master/scripts/list_notes.py --limit 20
uv run python hubspot-master/scripts/create_note.py --body "Key decision: proceeding with Enterprise plan"
```

### Meetings

```bash
uv run python hubspot-master/scripts/list_meetings.py --limit 20
uv run python hubspot-master/scripts/create_meeting.py --title "Quarterly review" --start "2026-04-01T10:00:00Z" --end "2026-04-01T11:00:00Z"
```

## Associations

```bash
# Get records associated with an object
uv run python hubspot-master/scripts/get_associations.py --object-type contacts --object-id 12345 --to-type deals
uv run python hubspot-master/scripts/get_associations.py --object-type deals --object-id 67890 --to-type companies
```

## API Reference

All endpoints use `https://api.hubapi.com` with Bearer token auth.

| Resource | Operation | Method | Endpoint |
|----------|-----------|--------|----------|
| Contacts | list | GET | `/crm/v3/objects/contacts` |
| Contacts | create | POST | `/crm/v3/objects/contacts` |
| Contacts | update | PATCH | `/crm/v3/objects/contacts/{id}` |
| Contacts | search | POST | `/crm/v3/objects/contacts/search` |
| Companies | list | GET | `/crm/v3/objects/companies` |
| Companies | create | POST | `/crm/v3/objects/companies` |
| Companies | search | POST | `/crm/v3/objects/companies/search` |
| Deals | list | GET | `/crm/v3/objects/deals` |
| Deals | create | POST | `/crm/v3/objects/deals` |
| Deals | update | PATCH | `/crm/v3/objects/deals/{id}` |
| Deals | search | POST | `/crm/v3/objects/deals/search` |
| Emails | list | GET | `/crm/v3/objects/emails` |
| Emails | log | POST | `/crm/v3/objects/emails` |
| Calls | list | GET | `/crm/v3/objects/calls` |
| Calls | log | POST | `/crm/v3/objects/calls` |
| Notes | list | GET | `/crm/v3/objects/notes` |
| Notes | create | POST | `/crm/v3/objects/notes` |
| Meetings | list | GET | `/crm/v3/objects/meetings` |
| Meetings | create | POST | `/crm/v3/objects/meetings` |
| Associations | get | GET | `/crm/v4/objects/{type}/{id}/associations/{toType}` |

## Pagination

All list endpoints support cursor-based pagination via `--after`. The scripts handle `paging.next` automatically when using `--limit`.

## Search behavior

Search scripts use a smart fallback: when no filters are provided, they fall back to `GET` on the list endpoint (recent results). When filters are provided, they `POST` to the `/search` endpoint with `filterGroups`.
