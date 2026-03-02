---
name: sentry-triage
version: '2.0'
description: Triage, analyze, and resolve Sentry errors for any project. Connects directly to the Sentry API — no MCP needed. Load when user says "check sentry", "sentry errors", "triage errors", "resolve sentry issues", "error report", or "what's broken".
author: JBD
category: devops
tags:
- sentry
- errors
- triage
- monitoring
updated: '2026-03-02'
visibility: personal
---
# Sentry Triage

Query, analyze, and resolve Sentry issues for any project using the Sentry API directly.

## Inputs

When the user invokes this skill, determine two things:

| Input | How to resolve |
|-------|---------------|
| **Project** | If user specifies a project (e.g. "check sentry for electron"), use it. Otherwise list projects (Step 0) and ask, or default to the project matching the cwd. |
| **Scope** | `all` (default), `new` (firstSeen last 24h), `regressions`, or a specific issue ID. |

## Config

All orgs share a single auth token stored in the workspace root `.env`:
```
SENTRY_AUTH_TOKEN=sntryu_...
```

| Setting | Value |
|---------|-------|
| **Region** | `de.sentry.io` (EU data residency) |
| **Auth token** | `SENTRY_AUTH_TOKEN` — check `04-apps/beam-prism-electron/.env` first, fall back to root `.env` |
| **Token management** | https://beam-ai.sentry.io/settings/auth-tokens/ |

### Known projects

| Slug | Org | Platform | Codebase path |
|------|-----|----------|--------------|
| `electron` | `beam-ai` | Electron/React | `04-apps/beam-prism-electron/` |

> Add rows here as new projects are onboarded to Sentry.

## API Reference

All endpoints use:
- **Base URL**: `https://de.sentry.io/api/0`
- **Auth**: `Authorization: Bearer $SENTRY_AUTH_TOKEN`
- **Content-Type** (for writes): `application/json`

In all examples below, `$ORG` and `$PROJECT` are placeholders — substitute with the actual org slug and project slug.

### Discovery

#### List organizations
```bash
curl -s "https://de.sentry.io/api/0/organizations/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

#### List projects in an org
```bash
curl -s "https://de.sentry.io/api/0/organizations/$ORG/projects/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

### Read

#### List unresolved issues
```bash
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is%3Aunresolved&limit=100" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

#### Search issues (Sentry query syntax)
```bash
# Useful queries: is:unresolved, is:regressed, assigned:me, level:error,
# firstSeen:>2026-03-01, times_seen:>10, !title:"known noise"
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=QUERY&limit=100" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

#### Get issue details
```bash
curl -s "https://de.sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

#### Get latest event for an issue
```bash
curl -s "https://de.sentry.io/api/0/issues/$ISSUE_ID/events/latest/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

#### Get event count (daily stats)
```bash
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/stats/?stat=received&resolution=1d" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

### Write

#### Resolve a single issue
```bash
curl -s -X PUT "https://de.sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

#### Bulk resolve issues
```bash
curl -s -X PUT "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?id=ID1&id=ID2&id=ID3" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

#### Ignore an issue (with optional threshold)
```bash
curl -s -X PUT "https://de.sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "ignored", "statusDetails": {"ignoreCount": 100}}'
```

#### Assign an issue
```bash
curl -s -X PUT "https://de.sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assignedTo": "user:EMAIL_OR_ID"}'
```

## Workflow

### Step 0: Resolve project

If the user didn't specify a project, determine it:
1. Check the **Known projects** table above — match by cwd or context.
2. If ambiguous, list all projects:
   ```bash
   source 04-apps/beam-prism-electron/.env 2>/dev/null || source .env
   curl -s "https://de.sentry.io/api/0/organizations/beam-ai/projects/" \
     -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
   import json, sys
   projects = json.load(sys.stdin)
   for p in projects:
       print(f'  {p[\"organization\"][\"slug\"]}/{p[\"slug\"]} ({p[\"platform\"] or \"unknown\"})')
   "
   ```
3. Ask the user which project to triage.

Set `$ORG` and `$PROJECT` for the rest of the workflow.

### Step 1: Load the auth token
```bash
source 04-apps/beam-prism-electron/.env 2>/dev/null || source .env
```

### Step 2: Fetch unresolved issues
```bash
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is%3Aunresolved&limit=100" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
import json, sys
issues = json.load(sys.stdin)
print(f'Found {len(issues)} unresolved issues\n')
for i in issues:
    events = i.get('count', '?')
    users = i.get('userCount', '?')
    title = i['title'][:90]
    print(f'  [{i[\"shortId\"]}] ({events} events, {users} users) {title}')
"
```

### Step 3: Analyze and categorize

For each issue, fetch the latest event stacktrace to understand the root cause:
```bash
curl -s "https://de.sentry.io/api/0/issues/$ISSUE_ID/events/latest/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
import json, sys
event = json.load(sys.stdin)
for entry in event.get('entries', []):
    if entry['type'] == 'exception':
        for val in entry['data'].get('values', []):
            print(f'Type: {val.get(\"type\")}')
            print(f'Value: {val.get(\"value\", \"\")[:200]}')
            for frame in (val.get('stacktrace') or {}).get('frames', [])[-5:]:
                print(f'  {frame.get(\"filename\")}:{frame.get(\"lineNo\")} in {frame.get(\"function\")}')
"
```

Group into categories and prioritize:
- **P0** — crashes, data loss, auth failures
- **P1** — broken features, API errors, missing functionality
- **P2** — cosmetic, dev-only noise, warnings

### Step 4: Fix code, then resolve

After applying fixes, bulk-resolve the fixed issues:
```bash
IDS=$(curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is%3Aunresolved&limit=100" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
import json, sys
ids = [i['id'] for i in json.load(sys.stdin)]
print('&id='.join(ids))
")

curl -s -X PUT "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?id=$IDS" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

### Step 5: Verify clean slate
```bash
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is%3Aunresolved&limit=10" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
import json, sys
issues = json.load(sys.stdin)
print(f'Remaining unresolved: {len(issues)}')
"
```

### Step 6: Monitor regressions

Sentry auto-reopens resolved issues if they recur. Check for regressions:
```bash
curl -s "https://de.sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is%3Aregressed&limit=25" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | python3 -c "
import json, sys
issues = json.load(sys.stdin)
if not issues:
    print('No regressions — all clear.')
else:
    print(f'{len(issues)} regressions:')
    for i in issues:
        print(f'  [{i[\"shortId\"]}] ({i.get(\"count\",\"?\")} events) {i[\"title\"][:80]}')
"
```

## Project-Specific Patterns

### Electron (beam-ai/electron)

| Pattern | Root Cause | Fix Location |
|---------|-----------|--------------|
| `Refused to load... CSP directive` | Missing domain in CSP | `src/main/index.ts` CSP headers |
| `window.electron.X.Y is not a function` | Missing IPC method | Check all 7 IPC layers |
| `Cannot read properties of undefined` in stores | Bridge not ready during HMR | Add `window.electron?.ns?.method` guard |
| `[vite] Failed to reload` | Dev-only HMR noise | Filtered in console-message handler |
| `Encountered two children with the same key` | Duplicate React keys | Use `` key={`${item}-${index}`} `` |
| `Renderer process gone` | Crash in main or renderer | Check main process logs |

> Add new project pattern tables here as projects are onboarded.

## Notes

- The Sentry MCP (`mcp.sentry.dev`) is read-only — it cannot resolve, ignore, or assign issues. This skill fills that gap.
- Issues resolved via API auto-reopen if the error recurs (Sentry regression detection).
- The auth token has org-wide scope — it works across all projects in the org without per-project tokens.
- For EU-hosted orgs, always use `de.sentry.io`. For US-hosted orgs, use `sentry.io`.
