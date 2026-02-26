---
name: extract-requirements
version: '1.0'
description: Extract and organize requirements from meeting transcripts, documents,
  and other sources into structured domain files. Load when user says 'extract requirements',
  'gather requirements', 'requirements from meetings', 'document requirements', or
  needs to consolidate requirements from multiple sources into organized documentation.
author: Sven Djokic
category: general
tags:
- beam-ai
- meeting
- transcript
platform: Beam AI
updated: '2026-01-07'
visibility: team
---
# Extract Requirements

Extract requirements from source materials (meeting transcripts, documents, emails, wikis) and organize them into structured, traceable requirement domain files.

---

## Purpose

This skill helps teams consolidate scattered requirements from various sources into well-organized, traceable documentation. It:

- Reads source materials chronologically
- Extracts requirements per project/agent/product
- Clusters requirements into logical domains
- Generates structured files with full source traceability
- Includes quotes and speaker attribution

---

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. DISCOVERY                                               │
│     • What projects to extract requirements for?            │
│     • Where are the source materials?                       │
│     • Any additional sources to consider?                   │
│     • Where to save output?                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. PROCESSING                                              │
│     • Read all sources chronologically                      │
│     • Extract requirements per project                      │
│     • Identify speakers/attributions                        │
│     • Note source file and date for each requirement        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. DOMAIN PROPOSAL                                         │
│     • Cluster requirements into logical domains             │
│     • Present proposed domains to user                      │
│     • User confirms, adjusts, or requests changes           │
│     • Iterate until user approves                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. GENERATION                                              │
│     • Create folder structure per project                   │
│     • Generate numbered domain files                        │
│     • Include source references, quotes, speakers           │
│     • Create README index for each project                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Discovery

### Questions to Ask User

**MANDATORY** - Ask these questions before starting extraction:

#### 1.1 Projects/Products

```
What projects, agents, or products should I extract requirements for?

Examples:
- "B2B Check Agent and Email Triage Agent"
- "Mobile App v2"
- "Customer Portal redesign"

You can specify multiple - I'll create separate folders for each.
```

#### 1.2 Source Materials

```
Where can I find the source materials?

Please provide:
- Folder path(s) containing meeting transcripts, documents, etc.
- File types to include (e.g., .md, .txt, .pdf)

Example: "04-workspace/client-meetings/"
```

#### 1.3 Additional Sources (Optional)

```
Are there any additional sources I should consider?

Options:
- Additional folders with documents
- Specific files to include
- None - just the main folder

Example: "Also check 04-workspace/project-docs/ for technical specs"
```

#### 1.4 Output Location

```
Where should I save the extracted requirements?

Default: 04-workspace/project-requirements/
Custom: Specify your preferred path
```

---

## Step 2: Processing

### 2.1 Read Sources Chronologically

- Sort all source files by date (from filename or metadata)
- Process oldest to newest to capture requirement evolution
- Use parallel agents for efficiency when processing many files

### 2.2 Extract Per Project

For each source file, extract:

| Element | Description |
|---------|-------------|
| Requirement | The specific requirement or detail |
| Project | Which project it applies to |
| Context | Why this requirement exists |
| Constraints | Any limitations or edge cases |
| Source file | Path to source document |
| Date | Meeting/document date |
| Speaker | Who stated this (if available) |
| Quote | Exact quote from source |

### 2.3 Handling Multiple Projects

When extracting, tag each requirement with the relevant project:
- Some requirements may apply to multiple projects
- Some sources may only discuss one project
- Keep requirements separated by project for output

---

## Step 3: Domain Proposal

### 3.1 Clustering Logic

Group requirements into domains based on:
- Functional area (e.g., "Authentication", "Data Validation")
- Integration type (e.g., "Jira Integration", "API Connections")
- Workflow stage (e.g., "Trigger & Input", "Processing", "Output")
- Technical concern (e.g., "Error Handling", "Testing")

### 3.2 Present to User

For each project, present:

```markdown
## [Project Name] - Proposed Requirement Domains

| # | Domain | Description | Est. Requirements |
|---|--------|-------------|-------------------|
| 1 | [Domain Name] | [Brief description] | ~X |
| 2 | [Domain Name] | [Brief description] | ~X |
...

Questions:
1. Does this domain structure make sense?
2. Should any domains be merged or split?
3. Any domains to add or rename?
```

### 3.3 Iterate Until Approved

- Accept user feedback
- Adjust domain structure
- Re-present if significant changes
- Proceed only after user confirms

---

## Step 4: Generation

### 4.1 Folder Structure

```
{output-path}/
├── {project-1-slug}/
│   ├── README.md
│   ├── 01-{domain-1-slug}.md
│   ├── 02-{domain-2-slug}.md
│   └── ...
├── {project-2-slug}/
│   ├── README.md
│   ├── 01-{domain-1-slug}.md
│   └── ...
```

### 4.2 Output Format Example

**Domain file structure:**

```markdown
# {Domain Name}

> **Project**: {Project Name}
> **Domain**: {Domain Name}
> **Last Updated**: {YYYY-MM-DD}

---

## Overview

{Brief description of what this domain covers}

---

## 1. {Section Name}

| Requirement | Details |
|-------------|---------|
| {Requirement} | {Description} |

**Source**: [2025-09-29 Meeting Title](relative/path/to/file.md)
> "Exact quote from source." — Speaker Name

---

## Open Questions / Blockers

| Item | Owner | Status |
|------|-------|--------|
| {Question} | {Person} | {Status} |
```

**README structure:**

```markdown
# {Project Name} - Requirements Documentation

> **Generated**: {YYYY-MM-DD}
> **Source**: {N} files from {date range}

## Requirement Domains

| # | Domain | Description |
|---|--------|-------------|
| 1 | [{Domain}](01-domain.md) | {Brief description} |

## Key Metrics / Integrations / Timeline / Contacts
(Include sections as relevant based on extracted content)
```

---

## Supported Source Types

| Type | Extensions | Notes |
|------|------------|-------|
| Meeting transcripts | `.md`, `.txt` | Primary source type |
| Documents | `.md`, `.txt`, `.pdf` | Technical specs, PRDs |
| Emails | `.md`, `.txt`, `.eml` | If exported as text |
| Wiki exports | `.md`, `.html` | Confluence, Notion exports |

---

## Best Practices

### For Source Materials

- Use consistent date format in filenames (YYYY-MM-DD)
- Include speaker names in transcripts when possible
- Store related documents in date-based folders

### For Extraction

- Process chronologically to capture requirement evolution
- Tag requirements that changed over time
- Note superseded requirements

### For Domain Organization

- Aim for 5-15 domains per project
- Each domain should be cohesive
- Avoid too many small domains or too few large ones

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Empty source folder | Inform user, ask for correct path |
| No requirements found for a project | Confirm project name, suggest alternatives |
| Speaker not identifiable | Use "— Source document" instead |
| Ambiguous project assignment | Ask user to clarify |

---

## Example Usage

**User**: "Extract requirements from our client meetings"

**AI Response**:
```
I'll help you extract and organize requirements. Let me ask a few questions:

1. What projects should I extract requirements for?
   (e.g., "API Gateway" and "Admin Dashboard")

2. Where are your meeting transcripts?
   (e.g., "04-workspace/client-meetings/")

3. Any additional sources to include?
   (e.g., technical docs, emails)

4. Where should I save the output?
   Default: 04-workspace/project-requirements/
```

---

## Integration

- Works with any project structure
- Output compatible with other Nexus skills
- Can be re-run to update requirements as new sources are added
