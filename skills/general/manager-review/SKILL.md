---
name: manager-review
description: "Generate a structured manager review briefing for a team member. Load when user says 'manager review - [name]', 'prepare manager review', 'review prep for [name]', 'manager briefing', or '1:1 prep for [name]'. Pulls OKRs from Notion and cross-references with BEO data, Fathom meetings, and chat logs to produce an actionable, conversation-ready performance briefing with prioritized questions, risks, appreciation points, and suggested actions."
---

# Manager Review

## Purpose

Generate a concise, actionable, conversation-ready performance briefing for a specific team member. Analyzes OKRs, updates, and evidence to produce a structured manager co-pilot output — not just a question list.

> **Trigger**: `manager review - {name}` or `review prep for {name}`
>
> **Output**: Structured manager briefing (conversation response)
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

### Check 2: Team Member's Notion Page ID

Ask the manager for the team member's Notion page URL or ID. Extract and store if needed.

### Check 3: Data Source Availability

Scan and report:

```
Data sources for {name}'s review:
  [x] Notion — {N} databases found
  [x] BEO progress data — {N} entries
  [ ] Fathom meetings — not configured
  [x] Chat logs — {N} days
```

---

## Workflow

### Step 0: Parse Command

Extract team member name from trigger (e.g., `manager review - Sarah`).

**Default period**: Current quarter (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec).

### Step 1: Fetch All Data from Notion

```bash
python3 03-skills/okr-self-review/scripts/fetch_okrs.py \
  --page-id <NOTION_PAGE_ID> \
  --include-done \
  --json
```

Returns JSON with: `functional_okrs`, `ai_native_okrs`, `key_projects`, `functional_skills`, `core_behaviours`. Each entry includes `page_id`, `text`, `status`, `self_rating`, `checkin_6months`, `checkin_3months`, `quarter`, `year`.

**If zero data returned**: Notify manager and proceed with available evidence sources only. Flag low confidence in output.

### Step 2: Gather Evidence

From all available sources in parallel:

- **BEO data** (if `BEO_SHEET_ID` in `.env`):
  ```bash
  python3 03-skills/okr-self-review/scripts/fetch_beo_data.py \
    --name "{name}" \
    --start-date {quarter_start} \
    --end-date {quarter_end} \
    --json
  ```
- **Fathom** (if `FATHOM_API_KEY` in `.env`): Fetch meetings via API
- **Chat logs**: Read `01-memory/chat/*.md` within review period
- **Local context**: `04-workspace/` artifacts

### Step 3: Analyze & Synthesize

Cross-reference all data sources. Identify:

- **Progress & achievements** — what shipped, measurable outcomes, completed OKRs
- **Gaps & risks** — stalled OKRs, missing updates, dropped projects
- **Update freshness** — when was each OKR last updated? Flag stale items
- **Self vs evidence misalignment** — self-ratings that don't match observed output
- **Behavioural signals** — core behaviours demonstrated (or absent) in evidence

### Step 4: Generate Briefing

Produce the output using the template below.

---

## Analysis Guidelines

### Evidence Weighting

| Source | Weight | Rationale |
|--------|--------|-----------|
| BEO data | Highest | Self-reported progress with timestamps |
| Workspace artifacts | High | Tangible deliverables |
| Fathom meetings | High | Discussions, decisions, action items |
| Chat logs | Medium | Day-to-day activity signals |
| Absence of data | Signal | Missing updates = visibility gap |

### Detecting Misalignment

| Pattern | Signal |
|---------|--------|
| Self-rating 4-5 but no shipped deliverables | Overconfidence — probe for impact |
| Self-rating 2-3 but strong evidence trail | Underconfidence — reinforce and explore |
| OKR "In Progress" but no updates in 4+ weeks | Stalled — ask directly |
| BEO update says "on track" but Notion status unchanged | Update hygiene gap |
| Key Project with no related OKR | Misaligned priorities |

### Question Design Rules

Every question must be:

- **Specific** — reference actual OKR text, project name, or data point
- **Evidence-backed** — cite the source (BEO, Fathom, Notion, Chat)
- **Outcome-oriented** — ask about results, impact, decisions — not feelings
- **Actionable** — the answer should clarify status, unblock, or align

**Cap at 5 questions total** — 3 Critical, 2 Important. No Optional tier. Force-rank by impact.

**Never generate generic questions.** If there's not enough data to make a specific question, flag the data gap instead.

---

## Output Template

```
# Manager Review Briefing
## {name} — {quarter} {year}

**Review Period**: {start_date} to {end_date}
**Data Sources**: {list with entry counts}
**Data Confidence**: {High | Medium | Low — based on source availability}

---

## 1. Manager Brief (TL;DR)

**Overall Signal**: {On Track | At Risk | Exceeding | Unclear}

- **Biggest Win**: {specific achievement with evidence source}
- **Biggest Concern**: {specific risk or gap with evidence source}
- **Visibility Gaps**: {areas where data is missing or stale}

---

## 2. Key Focus Areas (Top 3)

The most important topics to prioritize in this conversation:

1. **{Topic}** — {why this matters, what data shows}
2. **{Topic}** — {why this matters, what data shows}
3. **{Topic}** — {why this matters, what data shows}

---

## 3. Risks & Gaps

- {risk/gap} — {evidence} [{source tag}]
- {risk/gap} — {evidence} [{source tag}]
- {risk/gap} — {evidence} [{source tag}]

---

## 4. Where to Appreciate

- {specific achievement or behaviour} — {evidence} [{source tag}]
- {specific achievement or behaviour} — {evidence} [{source tag}]

---

## 5. Questions (Max 5)

Generate exactly 5 questions. Prioritize by impact.

### 🔴 Critical (Must Ask)

1. "{specific question referencing data}"
   *Evidence*: {what triggered this question} [{source}]
   *Tone*: {direct | curious | supportive}

2. "{specific question}"
   *Evidence*: {data point} [{source}]
   *Tone*: {recommended tone}

3. "{specific question}"
   *Evidence*: {data point} [{source}]
   *Tone*: {tone}

### 🟡 Important (If Time Permits)

4. "{question}"
   *Evidence*: {data point} [{source}]
   *Tone*: {tone}

5. "{question}"
   *Evidence*: {data point} [{source}]
   *Tone*: {tone}

---

## 6. Self vs Evidence Insights

| Area | Self-Rating | Evidence Signal | Gap |
|------|------------|-----------------|-----|
| {OKR/Skill/Behaviour} | {N}/5 | {what evidence shows} | {Over / Under / Aligned} |

**Notable patterns**:
- {pattern — e.g., "Consistently rates execution high but key projects lack completion evidence"}

---

## 7. Suggested Manager Actions

Post-conversation next steps:

- [ ] {action — e.g., "Align on realistic Q2 target for OKR X"}
- [ ] {action — e.g., "Request weekly async update on stalled Project Y"}
- [ ] {action — e.g., "Acknowledge strong delivery on Z in team standup"}

---

## 8. Data Confidence Notes

| Source | Status | Note |
|--------|--------|------|
| Notion OKRs | {Available / Partial / Missing} | {detail} |
| BEO Updates | {Available / Partial / Missing} | {detail} |
| Fathom | {Available / Partial / Missing} | {detail} |
| Chat Logs | {Available / Partial / Missing} | {detail} |

**Assumptions made**: {list any inferences made due to missing data}
```

---

## Style Guidelines

- Concise, structured, skimmable — bullet points over paragraphs
- Objective and evidence-based — no assumptions without signals
- Balance constructive feedback with recognition
- Avoid harsh or interrogative phrasing — this helps managers have good conversations
- Use source tags: `[Notion]`, `[BEO]`, `[Fathom]`, `[Chat]`, `[Workspace]`

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| **No Notion page ID** | Ask manager for team member's page URL |
| **Zero OKRs found** | Proceed with evidence-only analysis. Flag in Data Confidence. Generate questions about OKR setup |
| **No BEO/Fathom data** | Skip gracefully. Note in Data Confidence. Increase weight on available sources |
| **All OKRs rated 5** | Flag for calibration discussion. Cross-check against evidence |
| **No updates in 4+ weeks** | Escalate as 🔴 Critical question about status and blockers |
| **Team member is new** | Adjust expectations. Focus on onboarding, ramp-up signals, early wins |

---

## Integration

| Skill | Relationship |
|-------|-------------|
| `okr-self-review` | Shares fetch scripts and Notion data model |
| `notion-connect` | Config check, API access |
| `fathom-fetch-meetings` | Meeting data source |
| `google-sheets` | BEO progress data source |

---

**Version**: 1.0 | **Updated**: 2026-03-18
