---
name: create-deal
version: '1.0'
description: Create a new HubSpot deal after a successful sales call where a demo has
  been committed. Use this skill whenever the user says a call went well and a demo
  was booked, or asks to "log a deal", "create a deal from this call", "add to HubSpot",
  or "turn this into a deal". Only trigger when there's a clear signal that a demo or
  next commitment was secured — do NOT trigger for exploratory calls with no outcome,
  post-demo follow-ups, or existing deals being updated. Pulls notes from Granola
  automatically, extracts key fields, asks the user for any missing info, and creates
  the deal in HubSpot with all required fields and associations.
category: integrations
tags:
- granola
- hubspot
- deal
- crm
platform: Granola
updated: '2026-02-27'
visibility: public
---
# Create Deal from Call

You've just had a successful call with a prospect and they've committed to a demo. This skill will pull the call notes from Granola, extract everything needed, ask you a few quick questions, and create a fully populated deal in HubSpot.

## Step 1: Find the Call in Granola

If the user references a specific company or person, search Granola for this week's meetings and identify the relevant one. If the call was today and the company is obvious from context, grab it directly. Use `list_meetings` with `time_range: "this_week"` then `get_meetings` to retrieve the full notes.

Extract the following from the call notes:
- **Company name** and **contact name + email**
- **Use case** — what problem are they trying to solve?
- **Next step** — specifically what was committed (demo date/time if mentioned)
- **Collaborators** from Beam who were on the call or involved

## Step 2: Ask the User for Missing Fields

Before creating anything, ask the user for the fields you can't reliably extract from notes. Present what you've already inferred so they can confirm or correct, and ask only for what's genuinely missing.

Always ask for:
- **Amount** — estimated deal value in USD (you won't find this in call notes)
- **Deal type** — must be one of: `New Business`, `POC`, or `Partnership`
- **Collaborators** — any Beam teammates to add (Mo Bekdache, etc.) — confirm even if inferred from notes

Pre-fill and show for confirmation (extracted from notes):
- **Deal name** — format: `[Company] - [Use Case]` (e.g. "Al Ghandi Auto - Invoice & Document Automation")
- **Use case name** — concise label for the use case
- **Next step** — what was committed on the call
- **Deal stage** — always `Demo Call` (since a demo was committed)
- **Deal owner** — always Sufyaan Jogee by default

## Step 3: Show Confirmation Table

Always show a confirmation table before creating anything. Wait for explicit user approval.

| Field         | Value                                        |
|---------------|----------------------------------------------|
| Deal Name     | Acme Corp - Invoice Automation               |
| Use Case Name | Invoice Processing                           |
| Amount        | $25,000                                      |
| Deal Type     | New Business                                 |
| Deal Stage    | Demo Call                                    |
| Deal Owner    | Sufyaan Jogee                                |
| Next Step     | Demo Wednesday 2pm — send pricing beforehand |
| Collaborators | Mo Bekdache                                  |
| Company       | Acme Corp                                    |
| Contact       | Jane Smith (jane@acme.com)                   |

Then ask: **Approve? ✅ Yes / ❌ No**

## Step 4: Create the Deal in HubSpot

Once approved, do the following in order:

### 4a. Look up company and contact
Search HubSpot for the company and contact by name/email. They may already exist — if so, use the existing IDs. If not, create them first.

### 4b. Create the deal
Use these HubSpot property names:

| Field         | HubSpot Property                  | Notes                               |
|---------------|-----------------------------------|-------------------------------------|
| Deal Name     | `dealname`                        |                                     |
| Pipeline      | `pipeline`                        | Always `40552678` (New Deal Pipeline) |
| Deal Stage    | `dealstage`                       | Always `2019735762` (Demo Call)     |
| Amount        | `amount`                          | Numeric, no $ symbol                |
| Deal Owner    | `hubspot_owner_id`                | Sufyaan Jogee = `29290056`          |
| Use Case Name | `use_case_name`                   |                                     |
| Next Step     | `hs_next_step`                    |                                     |
| Deal Type     | `dealtype`                        | `newbusiness`, `existingbusiness`, or use closest match |
| Collaborators | `hs_all_collaborator_owner_ids`   | Comma-separated owner IDs           |

**Known owner IDs:**
- Sufyaan Jogee: `29290056`
- Mo Bekdache: `997717413`
- Brad Kelly: `29360610`
- Jonas Diezun: `516475085`
- Quentin Di Silvestro: `1367857294`

### 4c. Associate company and contact
After creating the deal, associate it with both the company and the contact records.

### 4d. Handle the Demo Call stage issue
HubSpot sometimes rejects direct creation into the `Demo Call` stage. If this happens, create the deal in the `New Deal` stage (`683908047`) first, then immediately update it to `Demo Call` (`2019735762`).

## Step 5: Confirm and Share Link

Once done, confirm success and share the HubSpot deal link so the user can verify.

---

## Important Notes

- **Always confirm before creating** — never skip the approval step
- **Deal stage is always Demo Call** — this skill is only for calls where a demo was secured
- **Default owner is always Sufyaan Jogee** — unless the user says otherwise
- **Deal type options are fixed:** New Business, POC, or Partnership — always ask
- **Amount is always required** — don't skip it or leave it blank
