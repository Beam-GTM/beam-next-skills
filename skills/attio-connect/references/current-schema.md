# Attio Current Schema - People Object

**Last synced**: 2026-02-16
**Workspace ID**: `05fcbc91-0166-4a34-a699-da111a13f782`

## Existing Attributes (System)

| Slug | Type | Multi | Description |
|------|------|-------|-------------|
| `record_id` | text | No | Unique record ID |
| `name` | personal-name | No | First + last name |
| `email_addresses` | email-address | Yes | Email (unique, dedup key) |
| `description` | text | No | General description |
| `company` | record-reference | No | Link to company record |
| `job_title` | text | No | Current job title |
| `avatar_url` | text | No | Profile picture (read-only via API) |
| `phone_numbers` | phone-number | Yes | Phone numbers |
| `primary_location` | location | No | City, region, country |
| `linkedin` | text | No | LinkedIn URL |
| `twitter` | text | No | Twitter handle |
| `instagram` | text | No | Instagram handle |
| `facebook` | text | No | Facebook URL |
| `angellist` | text | No | AngelList URL |
| `twitter_follower_count` | number | No | Twitter followers |

## Interaction Tracking (System - Auto)

| Slug | Type | Description |
|------|------|-------------|
| `first_interaction` | interaction | First ever interaction (auto) |
| `last_interaction` | interaction | Most recent interaction (auto) |
| `next_interaction` | interaction | Next scheduled interaction (auto) |
| `first_calendar_interaction` | interaction | First calendar event |
| `last_calendar_interaction` | interaction | Last calendar event |
| `next_calendar_interaction` | interaction | Next calendar event |
| `first_email_interaction` | interaction | First email |
| `last_email_interaction` | interaction | Last email |
| `strongest_connection_strength` | select | Connection strength (auto-calculated) |
| `strongest_connection_user` | actor-reference | Strongest connection (workspace member) |

## WhatsApp Integration (Already Connected!)

| Slug | Type | Description |
|------|------|-------------|
| `whatsapp_phone_number` | text | WhatsApp phone number |
| `whatsapp_last_inbound_message` | text | Last message FROM them |
| `whatsapp_last_inbound_date` | date | When they last messaged |
| `whatsapp_last_outbound_message` | text | Last message TO them |
| `whatsapp_last_outbound_date` | date | When you last messaged |
| `whatsapp_total_messages` | number | Total message count |
| `whatsapp_first_contact_date` | date | When conversation started |
| `whatsapp_conversation_link` | text | Direct link to WhatsApp chat |

## Custom Attributes (CRM - Created 2026-02-16)

| Slug | Type | Multi | Description |
|------|------|-------|-------------|
| `group` | select | Yes | Group categorization (pre-existing) |
| `relationship_type` | select | Yes | Investor, Customer, Founder/Peer, Team, Advisor, Friend, Date |
| `crm_status` | select | No | Active, Prospect, Dormant, Stale |
| `proximity_tier` | select | No | T1-Inner Circle, T2-Active, T3-Warm, T4-Network, T5-Archive |
| `relationship_quality` | select | No | High, Neutral, Low |
| `connection_story` | text | No | How you met and why they matter |
| `how_can_i_help` | text | No | Value you can create for them |
| `last_helped` | date | No | When you last helped them |
| `contact_source` | select | Yes | LinkedIn, WhatsApp, Instagram, Notion, Event, Intro, Google |
| `city_tags` | select | Yes | Berlin, Munich, SF, NYC, London, Dubai |
| `context_tags` | select | Yes | Beam, YC, University, Hyrox, Conference |
| `special_tags` | select | Yes | Bridge, Aspirational, Lifeline, Dormant-Reconnect |

## Dedup System (Auto)

| Slug | Type | Description |
|------|------|-------------|
| `nddl_last_duplicate_check` | timestamp | Last dedup check |
| `nddl_duplicate_check_status` | text | Dedup status |

## Existing Lists

| Name | Slug | List ID | Parent | Purpose |
|------|------|---------|--------|---------|
| Duplicate Companies | `company_deduplication_history` | `e6a1214f-5894-42f9-83cd-99b51dd49d44` | companies | Auto-dedup |
| Duplicate People | `person_deduplication_history` | `25c7bd67-ba6f-42e1-a1c5-7087719a81e5` | people | Auto-dedup |
| Weekly Ping Queue | `weekly_ping_queue` | `ebe582c9-fdb9-475b-ad6e-8fe31c5ca444` | people | Contacts to ping this week |
| Dormant Reconnect | `dormant_reconnect` | `64d2580e-93f1-4338-a4ca-f244ced442a8` | people | High-value dormant ties |
| Aspirational | `aspirational` | `db28302a-1815-4311-bf40-876ac4a287aa` | people | People to build relationships with |

---

**Note**: `last_interaction` already exists as a system attribute (auto-tracked from email/calendar). WhatsApp interactions also tracked natively. For in-person meetings not captured automatically, add notes or update `last_helped` manually.

**All custom attributes and lists are now LIVE in Attio.** Schema last synced: 2026-02-16.
