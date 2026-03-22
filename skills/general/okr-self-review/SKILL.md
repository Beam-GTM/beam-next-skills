---
name: okr-self-review
visibility: public
description: Generate a structured performance self-review. Load when user says "review my performance - [name]", "review my performance", "self-review", "performance review", or "quarter review". Pulls all data from Notion (OKRs, Key Projects, Skills, Core Behaviours) and cross-references with Nexus chat logs, BEO Slack data, and Fathom meetings.
---

# OKR Self-Review

## Purpose

Generate evidence-backed performance self-reviews by pulling OKRs from Notion and cross-referencing with Fathom meetings, Nexus chat logs, BEO Slack data, and workspace artifacts. Produces ratings, progress bullets, and persona feedback — then writes results back to Notion.

> **Trigger**: `review my performance - {name}`
>
> **Output**: Performance review report (conversation response)
>
> **Required**: Notion page with child databases (Functional OKRs, AI Native OKRs, Key Projects, Functional Skills, Core Behaviours)
>
> **Enhanced by** (optional): BEO progress data, Fathom meeting transcripts, Nexus chat logs

---

## Pre-Flight Checks

### Check 1: Notion API

```bash
python3 00-system/skills/notion/notion-master/scripts/check_notion_config.py --json
```

- **Exit code 2**: Stop. Guide user to setup.
- **Exit code 0 or 1**: Proceed.

### Check 2: User Notion Page ID

Read `01-memory/user-config.yaml` for `notion_page_id`.

**If missing**: Ask user for their Notion page URL, extract ID, save to `user-config.yaml`.

### Check 3: Data Source Availability

Scan and report:

```
Data sources for your review:
  [x] Notion — {N} databases found
  [x] Nexus chat logs — {N} days
  [ ] BEO progress data — not configured
  [x] Fathom meetings — API key found
```

---

## Workflow

### Step 0: Parse Command

Extract name from `review my performance - {name}`.

**Default period**: Current quarter (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec).

### Step 1: Fetch All Data from Notion

```bash
python3 03-skills/okr-self-review/scripts/fetch_okrs.py \
  --page-id <NOTION_PAGE_ID> \
  --include-done \
  --json
```

Returns JSON with 5 sections: `functional_okrs`, `ai_native_okrs`, `key_projects`, `functional_skills`, `core_behaviours`. Each entry includes: `page_id`, `text`, `status`, `self_rating`, `checkin_6months`, `checkin_3months`, `quarter`, `year`, and `_prop_map` (actual Notion property names/types for write-back).

**If Step 1 returns zero OKRs** (exit code 2, empty databases, or no Notion page): proceed to Step 1.5.

### Step 1.5: Infer OKRs from Evidence (No-OKR Fallback)

Triggered when the individual has **no active OKRs** in Notion. Instead of stopping, the skill reverse-engineers objectives from activity data.

1. Notify the user:
   ```
   No active OKRs found in Notion for {name}. Switching to inference mode —
   I'll reverse-engineer objectives from your activity data across all available sources.
   ```

2. Proceed to Step 2 (Gather Evidence) as normal — collect all available sources

3. **Analyze evidence to extract work themes**:
   - From **Fathom meetings**: recurring topics, projects discussed, decisions made, action items owned by the individual
   - From **Chat logs**: tasks completed, skills used, tools built, problems solved
   - From **BEO data**: any OKR updates logged in Google Sheets (even if not in Notion)
   - From **Workspace artifacts**: deliverables produced (proposals, analyses, templates, code)

4. **Cluster themes into 3–6 inferred OKRs**:
   - Group related activities into objectives (e.g., "Improved onboarding process", "Built AI-powered automation tools")
   - Classify each as **Functional** or **AI Native** based on whether AI was the primary method
   - Extract key projects as standalone entries
   - Infer skills demonstrated and core behaviours from the evidence

5. **Flag as inferred**: All inferred items are marked `[Inferred]` in the output so the reviewer knows these were not from Notion

6. **Write-back handling**: Since there are no existing Notion rows, skip the normal write-back. Instead, after showing the review, offer:
   ```
   These OKRs were inferred from your activity data. Would you like me to:
   1. Create these as OKRs in your Notion page?
   2. Save the review as-is (no Notion changes)?
   ```

### Step 2: Gather Evidence

From all available sources in parallel:

- **Chat logs**: Read `01-memory/chat/*.md` within review period
- **BEO data** (if `BEO_SHEET_ID` in `.env`): Run `fetch_beo_data.py`
- **Fathom** (if `FATHOM_API_KEY` in `.env`): Fetch meetings via API
- **Local context**: `01-memory/goals.md`, `core-learnings.md`, `04-workspace/` artifacts

### Step 3: Map Evidence & Generate Review

For each item from Notion, map evidence from data sources and generate the review using the output template below.

### Step 4: Write Back to Notion

After the review is generated and shown to the user, ask:

```
Would you like me to push the ratings and progress back to your Notion databases?
```

**If yes**: Build a JSON array of updates from the review output:

```json
[
  {
    "page_id": "<from fetch_okrs.py output>",
    "text": "OKR title",
    "updates": {
      "self_rating": {
        "value": "<suggested rating, e.g. 4>",
        "prop_name": "<from _prop_map.self_rating.name>",
        "prop_type": "<from _prop_map.self_rating.type>"
      },
      "checkin_6months": {
        "value": "<progress bullets as text>",
        "prop_name": "<from _prop_map.checkin_6months.name>",
        "prop_type": "<from _prop_map.checkin_6months.type>"
      }
    }
  }
]
```

Save to a temp file and run:

```bash
python3 03-skills/okr-self-review/scripts/write_review.py \
  --input <temp_file.json>
```

The script updates each Notion row via `PATCH /v1/pages/{page_id}`. Supports `--dry-run` to preview changes without writing.

**Write-back fields**:
- `self_rating` → Suggested rating (written to Self Rating select property)
- `checkin_6months` → Progress bullets (written to Checkin Remarks (6months) rich_text property)
- `self_remarks` → Overall remarks if applicable

**Note**: Only write back to databases that have the relevant properties (e.g., Core Behaviours and Functional Skills may not have checkin columns).

---

## Rating Guidelines

| Rating | Meaning |
|--------|---------|
| 5 | Exceptional — significantly exceeded expectations |
| 4 | Strong — exceeded expectations in notable ways |
| 3 | Solid — met expectations consistently |
| 2 | Developing — partially met, clear gaps |
| 1 | Below — did not meet expectations |

Weight evidence: BEO data > workspace artifacts > chat logs > inferred.

---

## Persona Feedback

Use famous evaluators whose domain matches the work being reviewed. Keep feedback to **2-3 lines max**. Direct, specific, no fluff.

| Domain | Personas |
|--------|----------|
| **General / Execution** | Keith Rabois, Frank Slootman, Patty McCord |
| **People / HR / Culture** | Laszlo Bock, Patty McCord, Adam Grant |
| **Product / Customer** | Jeff Bezos, Marty Cagan |
| **Engineering / Technical** | Kelsey Hightower, Werner Vogels |
| **Marketing** | Seth Godin, April Dunford |
| **Strategy / Org Design** | Ram Charan, Roger Martin |

---

## Output Template

Use the standard template when OKRs exist in Notion. When OKRs are **inferred** (Step 1.5), use the `[Inferred]` variant below.

```
# Performance Review Cycle Ph {phase}, {year}
# Self-Review: {name}

**Review Period**: {start_date} to {end_date}
**Data Sources**: {list}
**Mode**: {Standard | Inferred — "Inferred" when no OKRs found in Notion}

---

## Functional OKRs

### OKR {N}: {text}
**Status**: {status} | **Self Rating**: {self_rating or "—"}

**Progress**:
- {bullet 1 — specific evidence with source tag [Chat], [BEO], [Fathom], [Workspace]}
- {bullet 2}
- {bullet 3}
- {bullet 4 — max 4-5 bullets}

**Suggested Rating**: {X}/5

**Feedback** *({Persona Name})*: "{2-3 lines. Direct, specific, actionable.}"

---

## AI Native OKRs

### AI Native OKR {N}: {text}
**Status**: {status} | **Self Rating**: {self_rating or "—"}

**Progress**:
- {4-5 bullets max}

**Suggested Rating**: {X}/5

**Feedback** *({Persona Name})*: "{2-3 lines.}"

---

### [Inferred] OKR Template (used when Step 1.5 is triggered)

### OKR {N}: {text} [Inferred]
**Source**: {Fathom, Chat, BEO, Workspace — primary evidence sources}

**Evidence**:
- {bullet 1 — specific evidence with source tag [Chat], [BEO], [Fathom], [Workspace]}
- {bullet 2}
- {bullet 3}
- {bullet 4 — max 4-5 bullets}

**Suggested Rating**: {X}/5

**Feedback** *({Persona Name})*: "{2-3 lines. Direct, specific, actionable.}"

---

## Key Projects

Use Key Projects from Notion. If the Notion list is incomplete,
supplement with major projects identified from evidence (chat logs,
workspace artifacts, Fathom meetings).
When in inference mode, extract all key projects from evidence.

### Project {N}: {text}
**Related OKRs**: {which OKRs this contributes to}
**Status**: {status} | **Self Rating**: {self_rating or "—"}

**Progress**:
- {4-5 bullets max}

**Suggested Rating**: {X}/5

**Feedback** *({Persona Name})*: "{2-3 lines.}"

---

## Functional Skills

Use Functional Skills from Notion as the base list.

### Skill {N}: {text}
**Self Rating**: {self_rating or "—"}
**Utilised in**: {OKR, project, or activity where demonstrated}
**Suggested Rating**: {X}/5

---

## Core Behaviours

Use Core Behaviours from Notion (the 7 Beam values).

### {N}. {behaviour text}
**Instance Displayed**:
- {bullet 1 — specific evidence}
- {bullet 2}
- {bullet 3 — max 3-4 bullets}
**Suggested Rating**: {X}/5

---

## Overall Feedback

{Crisp, direct. 1 short paragraph. No sugar coating.
What you shipped, where you fell short, what to fix.
Reference actual work. End with one clear action for next period.}
```

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| **No Notion page ID** | Ask user; save to user-config.yaml |
| **Database names differ** | List found databases; ask user |
| **All OKRs Done** | Include them (--include-done flag) |
| **No active OKRs in Notion** | Trigger Step 1.5: infer OKRs from evidence sources (Fathom, chat, BEO, workspace). Mark as `[Inferred]`. Offer to create in Notion. |
| **No Notion page at all** | Skip Step 1 entirely. Gather evidence from all other sources. Run full inference mode. |
| **Missing data sources** | Skip gracefully; note in sources list |
| **Key Projects list incomplete in Notion** | Supplement from evidence |
| **Core behaviours not in Notion** | Use defaults: Ownership, Execution, Collaboration, Growth, AI-Native, Quality, Experimentation |

---

## Integration

| Skill | Relationship |
|-------|-------------|
| `notion-connect` | Config check, API access |
| `fathom-fetch-meetings` | Meeting data source |
| `google-sheets` | BEO progress data source |
| `beo-okr-bot` | Shares Notion OKR data model |

---

**Version**: 2.2 | **Updated**: 2026-03-05
