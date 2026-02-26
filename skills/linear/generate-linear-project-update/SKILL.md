---
name: generate-linear-project-update
version: '1.0'
description: Generate concise Linear project status updates with issues grouped by
  status, sub-issue links, and metrics. Load when user mentions "generate project
  update", "weekly update for [project]", "Linear project summary", "status update",
  or provides a Linear project URL.
author: Jack Li
category: general
tags:
- linear
- update
platform: Linear
updated: '2025-12-10'
visibility: team
---
# Generate Linear Project Update

Generate concise weekly/periodic status updates for Linear projects with issues organized by status.

## Purpose

This skill creates shareable project updates by:
- Querying Linear issues updated within a specified timeframe (default: last week)
- Organizing issues by status (completed, in progress, in review, pending)
- Including issue links, sub-issue details, and external references
- Formatting as a short, shareable update with key metrics

**Time Estimate**: 2-3 minutes

---

## Workflow

### Step 1: Gather Requirements

Ask user for (if not already provided):
- **Project name or URL** (e.g., "BID Coburg" or Linear project URL)
- **Timeframe** (default: last 7 days / `-P7D`)

### Step 2: Query Linear Issues

Use `mcp__linear__list_issues` with these parameters:
```
project: [project-name]
updatedAt: -P7D (or user-specified timeframe)
orderBy: updatedAt
limit: 50
```

### Step 3: Organize Issues by Status

Group the results into:
1. **Newly Created** (created this period)
2. **Recently Completed** (status: Done)
3. **In Progress** (status: In Progress)
4. **In Review** (status: In Review)
5. **Todo/Backlog** (status: Todo/Backlog)

For each issue, include:
- Issue identifier and title
- Issue URL
- Status
- Brief description or key detail
- Sub-issues if parent issue
- External links from description (Notion, Airtable, etc.)

### Step 4: Extract Key Metrics

If available from context or dashboard links, include:
- Completion stats (e.g., "9 issues completed")
- Accuracy metrics (if from feedback dashboards)
- Progress indicators

### Step 5: Format Update

Use this concise format:

```markdown
## [Project Name] Update - Week of [Date Range]

### ✅ Completed ([N] issues)
- **[CLI-XXX]** - [Title] | [One-line summary]
  [Link if relevant]

### 🚀 [Current Focus Section Name]
**[CLI-XXX]** - [Parent Issue Title]
[Brief context]

**Sub-issues:**
1. **[CLI-XXX]** - [Sub-issue title] | [Status]
   [One-line description]

### 📊 In Review
- **[CLI-XXX]** - [Title]: [One-line summary]

### 📈 Metrics
[Any relevant metrics]

### Next Week
[Brief priorities]
```

**Key formatting rules:**
- Keep descriptions to 1 sentence max
- Include all relevant URLs inline
- Use emojis for visual structure (✅ 🚀 📊 📈)
- Group related sub-issues under parent
- Prioritize links over verbose descriptions

### Step 6: Present Update

Show the formatted update to user with:
"Here's your project update - you can copy and paste this into Linear project updates."

---

## Example Triggers

- "Generate project update for BID Coburg"
- "What's the weekly update for [project]?"
- "Create Linear project summary"
- "Project status update"
- "Weekly Linear update"

---

## Notes

**Timeframe Formats:**
- `-P7D` = last 7 days
- `-P14D` = last 14 days
- `-P1M` = last month
- Specific date: `2025-11-10` (YYYY-MM-DD)

**When External Links Present:**
Always include dashboard, Notion, Airtable, or other external URLs mentioned in issue descriptions.

**Sub-Issues:**
When a parent issue has sub-issues, list them indented under the parent for context.
