---
name: dealroom-creation
version: '1.0'
description: Quick company folder setup for sales prospects. Load when user mentions
  "create company", "new company", "create dealroom", "company folder", or "setup
  [company name]". Creates simple folder structure for organizing company documents,
  call transcripts, and emails.
author: Quentin
category: general
tags:
- email
- sales
- transcript
updated: '2025-12-12'
visibility: team
---
# Company Folder Creation

Quick folder setup for new sales prospects and clients.

## Purpose

Creates a simple, organized folder structure for each company:
- **01-docs**: Store SOWs, proposals, contracts, presentations
- **02-transcripts**: Store call recordings and meeting notes
- **03-emails**: Store email threads and communication drafts

**Time Estimate**: < 1 minute

---

## Workflow

### Step 1: Get Company Name

Ask user for company name if not provided.

**Format company name**:
- Lowercase
- Replace spaces with hyphens
- Example: "Sunday Natural" → "sunday-natural"

---

### Step 2: Create Folder Structure

Create folders in `04-workspace/companies/`:

```bash
mkdir -p 04-workspace/companies/{company-name}/01-docs
mkdir -p 04-workspace/companies/{company-name}/02-transcripts
mkdir -p 04-workspace/companies/{company-name}/03-emails
```

**Result**:
```
04-workspace/companies/
  └── {company-name}/
      ├── 01-docs/
      ├── 02-transcripts/
      └── 03-emails/
```

---

### Step 3: Update Workspace Map

Add the new company to `04-workspace/workspace-map.md`:

1. Add company folder to structure diagram
2. Add brief description to folder descriptions section
3. Add navigation reference

**Example entry**:
```markdown
├── {company-name}/           # [Brief description - e.g., "New prospect - AI automation"]
```

---

### Step 4: Confirm & Close

Confirm folder creation with user:
```
✅ Company folder created: {company-name}
   - 01-docs/
   - 02-transcripts/
   - 03-emails/
```

Then trigger close-session to save workspace map updates.

---

## Usage Examples

**Simple creation**:
```
User: "create company Acme Corp"
→ Creates: 04-workspace/companies/acme-corp/
```

**With context**:
```
User: "setup folder for new prospect Tesla"
→ Creates: 04-workspace/companies/tesla/
```

---

## Notes

- Keep company names lowercase with hyphens
- No complex permissions or access controls needed
- Add more folders manually later if needed (e.g., 04-contracts/, 05-demos/)
- Workspace map updated automatically for AI navigation
