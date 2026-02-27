---
name: slack-cleanup
version: '1.0'
description: Suggest which Slack channels to leave or archive. Load when user says
  "slack cleanup", "clean up my channels", "which channels should I leave", "slack channel
  audit". Lists channels, checks recent activity (e.g. last 6 months), optionally
  cross-references CRM (HubSpot/Salesforce) for relevance, then outputs a recommendation
  list with rationale. Does not auto-leave channels.
category: productivity
tags:
- slack
- cleanup
- channels
visibility: public
updated: '2026-02-27'
---
# Slack Cleanup

Recommend which Slack channels to leave or archive based on activity and optional CRM relevance.

## Purpose

Reduce noise by identifying channels you can safely leave or archive. The skill composes Slack (list channels, channel activity) and optionally CRM (HubSpot or Salesforce) to produce a clear recommendation list. You decide what to do; the skill does not leave or archive anything.

**Use when**: You have many channels and want a data-driven suggestion for which to keep vs leave.

**Time**: ~2–5 minutes depending on channel count and CRM lookup.

---

## Workflow

### Step 1: List channels and activity

- Load **slack-connect** or use Slack master scripts: list channels, then for each channel (or a sample) get recent activity (e.g. `channel_history.py` with `--oldest` set to ~6 months ago, or use `conversations.history`).
- If the workspace has a script that returns last-activity per channel, use it. Otherwise: list channels with `list_channels.py --json`, then for channels the user is in, optionally sample activity (e.g. last message date) via `channel_history.py --channel ID --limit 1` to infer recency.

### Step 2: Optional CRM cross-reference

- If user has HubSpot or Salesforce connected: for each channel name or topic, check whether it maps to active deals, accounts, or contacts (e.g. channel named after a customer or deal). Use **hubspot-connect** / hubspot-list-deals, hubspot-list-companies, or the relevant CRM skill to see if the channel is tied to current work.
- Add a simple relevance flag: e.g. "CRM tie" (channel name/topic matches active deal or account) vs "no CRM tie".

### Step 3: Build recommendation list

Produce a short report:

- **Leave (recommended)** — low or no activity in the lookback window and no CRM tie. Short rationale per channel.
- **Review** — some activity or possible CRM tie; user may want to keep or leave.
- **Keep** — high activity or clear CRM relevance.

Output as a clear list (table or bullets) with channel name, last activity (if available), CRM tie (if checked), and recommendation.

### Step 4: Confirm

- Remind user the skill only recommends; they can leave/archive channels manually in Slack.
- Optionally: "I can open the Slack channel list for you" or point to where to manage membership.

---

## Prerequisites

- **Slack**: slack-connect (or Slack master scripts) configured with `list_channels` and channel history access.
- **CRM** (optional): HubSpot or Salesforce connected if you want "CRM relevance" in the report.

---

## Triggers

- "slack cleanup", "clean up my channels", "which channels should I leave", "slack channel audit", "channel cleanup"

---

## Output

- Markdown or structured list: channel name, last activity, CRM tie (if any), recommendation (Leave / Review / Keep), one-line rationale.
- No automatic actions; user applies changes in Slack.
