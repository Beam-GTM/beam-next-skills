---
name: setup-notion-customer-onboarding
version: '1.0'
description: Setup and fill Notion customer onboarding template pages by updating
  Overview sections, Quick Links, and database tasks. Load when user mentions "setup
  notion onboarding", "fill customer template", "update onboarding tasks", or provides
  a Notion onboarding page URL. Uses Notion MCP for all content updates.
author: Jack Li
category: general
tags:
- notion
platform: Notion
updated: '2025-12-10'
visibility: team
---
# Setup Notion Customer Onboarding

Automate filling and updating Notion customer onboarding template pages with project content.

## Purpose

This skill helps you populate Notion customer onboarding templates by:
- Filling Overview section (Project Summary, Documentation, Flow) from project files
- Updating Quick Links with customer-specific URLs
- Updating 18 onboarding tasks one-by-one with content from your project folder

Uses **Notion MCP** for all content operations.

**Key Features**:
- Direct Notion MCP integration
- Interactive task-by-task updates with user
- Reads project folder structure automatically
- Handles markdown content via MCP

**Time Estimate**: 30-60 minutes (depending on content availability)

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Check/Setup Notion MCP access
- [ ] Get project folder location from user
- [ ] Update Overview section (Project Summary, Documentation, Flow)
- [ ] Update Quick Links section (4 links)
- [ ] Update database tasks one-by-one (18 tasks)
- [ ] Verify all updates completed
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: Check/Setup Notion MCP Access

**First, check if Notion MCP is available:**

Test: `mcp__notion__notion-search` with a simple query.

**If MCP is NOT available:**
1. Load [references/notion-mcp-setup.md](references/notion-mcp-setup.md)
2. Guide user through MCP installation:
   - Create Notion integration
   - Configure Claude Code config
   - Grant integration access to template page
   - Restart Claude Code
3. Verify setup works

**Get Project Page URL (CRITICAL):**
Ask user: "Please provide the URL of your Notion customer onboarding PROJECT page."
- ⚠️ **IMPORTANT**: This should be the ACTUAL project page (e.g., "Favorite Staffing - Onboarding"), NOT the template page
- Example: `https://www.notion.so/joinbeam/Customer-Name-Onboarding-...`
- **Store this URL** - all updates will be made to THIS page and its database

**Verify correct page and get database collection URL:**
1. **Fetch the project page**: `mcp__notion__notion-fetch` with user-provided URL
2. **Verify title**: Check the title matches the customer name (not "Customer Onboarding Template")
3. **Get database URL**: Look for `<database url="...">` in the page content
4. **Fetch the database**: `mcp__notion__notion-fetch` with the database URL
5. **Extract collection URL**: From database response, find `<data-source url="collection://...">`
6. **Store both URLs**:
   - Project page URL: `https://www.notion.so/...`
   - Database collection URL: `collection://...`

**Example verification:**
```
✅ Page title: "Favorite Staffing - Onboarding..."
✅ Database URL: https://www.notion.so/2a72cadf...
✅ Collection URL: collection://2a72cadf-bbbc-815c-aae0-000b4ba10232
```

**⚠️ COMMON MISTAKE TO AVOID:**
- Do NOT use template URLs (these have different IDs)
- Template page: `2a92cadf...` ❌
- Project page: `2a72cadf...` ✅
- Each customer project has unique page and database IDs

**Mark this todo complete before proceeding.**

---

### Step 3: Get Project Folder Location

Ask user: "Where is your project folder with content for this onboarding?"

Example response: `04-workspace/Workflow/customer-x-project/`

**Store this path** - it will be used for all content lookups in subsequent steps.

**Optional**: Ask user if they have specific files for certain sections:
- "Do you have a project summary document?"
- "Where are the documentation files?"
- "Where is the agent flow diagram?"

**Mark this todo complete before proceeding.**

---

### Step 4: Update Overview Section

Load [references/template-structure.md](references/template-structure.md) to see structure.

Fetch the main template page using `mcp__notion__notion-fetch` to see current content.

**IMPORTANT: Keep Overview section HIGH-LEVEL and CONCISE**
- This section is rarely updated after initial setup
- Focus on: scope, project description, problem statement, and goals
- Avoid detailed content - save that for the database tasks
- Maximum 3-5 bullet points per subsection

**CRITICAL: This page is CLIENT-FACING**
- DO NOT reference local file paths (e.g., `04-workspace/doc/file.md`)
- DO NOT expose internal file names or folder structures
- If content needs to be shared: Create Notion sub-pages and copy client-appropriate content
- Remove any internal notes, credentials, or sensitive information
- Only include client-relevant information

**For each subsection:**

#### 4.1: Project Summary
1. Look in project folder for: `*summary*`, `*overview*`, `*objectives*`, `README.md`
2. Extract only: scope, problem statement, main goal, success criteria (1-2 sentences each)
3. Ask user: "Use this concise summary for Project Summary?"
4. **Update via MCP:**
   - Use `mcp__notion__notion-update-page` to update content
   - Update the placeholder `[Enter Project Summary here along with Objectives/ Success Criteria]`
   - Keep it to 3-5 bullet points maximum

#### 4.2: Documentation
1. Look in project folder for: `*doc*`, `*spec*`, `*requirements*`
2. Ask user: "Which documents should be shared with client? Should I create Notion sub-pages for them?"
3. **Options:**
   - Create Notion sub-pages and copy client-appropriate content
   - Link to external documents (Google Docs, shared PDFs)
   - Provide high-level description without file references
4. **NEVER** include local file paths or internal file names
5. List 3-5 most important documents maximum

#### 4.3: Flow
1. Look in project folder for: `*flow*`, `*diagram*`, `*architecture*`, `*.png`, `*.jpg`
2. Ask user: "Which file/image is the agent flow?"
3. For text descriptions: Keep to 3-5 high-level steps only
4. For images: Link or embed the diagram directly

**Mark this todo complete before proceeding.**

---

### Step 5: Update Quick Links Section

Fetch the current Quick Links from the template page.

Ask user for each link (skip Beam Academy - line 39 in template structure says "no need to update"):

1. **Beam Platform Login**: "What's the customer's Beam platform workspace URL?"
2. **Template Agent Workshop** (Miro): "What's the Miro board URL for this customer?"
3. **Test Case Database** (Airtable): "What's the Airtable URL for test cases?"
4. **Integration Input** (Google Sheets): "What's the Google Sheets URL for integrations?"

**Update callouts** using `mcp__notion__notion-update-page` to replace the generic template URLs.

**Mark this todo complete before proceeding.**

---

### Step 6: Update Database Tasks One-by-One

Load [references/template-structure.md](references/template-structure.md) for complete task list.

**Get all tasks from database:**
1. **Use the collection URL from Step 2** (stored earlier when you verified the project page)
2. Use `mcp__notion__notion-search` with `data_source_url: <collection URL>`
3. ⚠️ **DO NOT use hardcoded collection URL** - each project has its own database

**Example search:**
```
mcp__notion__notion-search
query: "onboarding task"
data_source_url: "collection://2a72cadf-bbbc-815c-aae0-000b4ba10232"
```

**Task count may vary:** Most projects have ~18 tasks, but actual count depends on the specific onboarding plan.

**For EACH task:**

**Step 1: Fetch & Analyze**
1. **Fetch task page**: `mcp__notion__notion-fetch` with task URL
2. **Check Status from properties**: Look at the `Status` field in the fetched page properties
   - If Status = "Done" OR "Complete" → **SKIP automatically** (task already complete)
   - Only proceed if Status = "To-Do" OR "In progress" OR similar incomplete status
3. **Analyze current content**: What's already in the task? Is it template content or real content?

**Step 2: Check Folders**
4. **Search project folders** for relevant content:
   - 04-workspace/meeting/ - meeting notes, kick-off materials
   - 04-workspace/doc/ - documentation, specifications, proposals
   - 04-workspace/Workflow/ - workflow diagrams, agent designs, critical questions
5. **Match task name with folder content**: Look for keywords, related topics

**Step 3: Make Recommendation**
6. **Determine if update needed**:
   - Current content is template → Found relevant files → **RECOMMEND UPDATE**
   - Current content is template → No relevant files → **RECOMMEND SKIP** (leave as template)
   - Current content has real data → Found different files → **RECOMMEND UPDATE** (ask first!)
   - Current content has real data → No new files → **RECOMMEND SKIP** (already complete)
7. **Show suggestion**:
   - "Task X: [Current content summary]"
   - "Found: [files or 'nothing']"
   - "Recommendation: [Update/Skip] because [reason]"
8. **Ask confirmation**: "Proceed with [recommendation]?"

**Step 4: Execute (only if approved)**
9. **WAIT FOR USER CONFIRMATION** before any update
10. **If approved**: Update via `mcp__notion__notion-update-page`
11. **Show progress**: "Task X/18 complete"
7. **If approved**:
   - Use `mcp__notion__notion-update-page` to update task page content
8. **If content NOT found**:
   - Ask: "Where can I find content for this task, or should we skip it?"
9. **Update task status** if needed (with user confirmation)
10. **Show progress**: "Task X/18 complete"

**CRITICAL SAFETY RULES:**
- ⚠️ NEVER overwrite existing content without explicit user confirmation
- ⚠️ ALWAYS fetch and show current content first
- ⚠️ Tasks may have been manually updated - respect existing work
- ⚠️ SKIP tasks with Status = "Done" automatically
- ⚠️ When in doubt, ask before updating

**Process by stage** (helps user follow along):
- Discovery Stage: ~9 tasks
- Build Stage: ~5 tasks
- Optimize Stage: ~3 tasks
- Go-Live Testing Stage: ~1 task

**Common task patterns across projects:**
- **Meeting tasks**: Usually have booking templates ready - recommend skip unless custom content needed
- **Already completed tasks** (Status = "Done"): Auto-skip per safety rules
- **In progress tasks**: Check if they already have real content before updating
- **Blank pages**: Good candidates for updates if relevant content exists

**Efficiency tips:**
- Many tasks will be skipped (meetings, already done, already have content)
- Focus updates on tasks that need project-specific content
- Typical projects: Update 3-5 tasks, skip 13-15 tasks

**Mark this todo complete when all tasks processed.**

---

### Step 7: Verify All Updates Completed

Summarize what was updated:
```
✅ Overview Section:
   - Project Summary: Updated
   - Documentation: Updated
   - Flow: Updated

✅ Quick Links:
   - Beam Platform: Updated
   - Miro Workshop: Updated
   - Airtable Database: Updated
   - Google Sheets: Updated

✅ Database Tasks: 18/18 updated
   - Discovery: 9 tasks
   - Build: 5 tasks
   - Optimize: 3 tasks
   - Go-Live Testing: 1 task
```

Ask user: "Would you like to review any specific section before we close?"

**Mark this todo complete before proceeding.**

---

### Step 8: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

The close-session skill will:
- Update system memory with this session's work
- Save context for next session
- Create session report
- Clean up temporary files

**This is the final mandatory step.** Do not skip - it ensures all progress is preserved.

---

## Resources

### references/notion-mcp-setup.md
Complete guide for installing and configuring Notion MCP server.

### references/template-structure.md
Complete structure of the customer onboarding template with all 18 tasks, URLs, and sections to fill.

---

## Notes

**About MCP Updates**:
- All content updates use Notion MCP directly
- MCP handles markdown content automatically
- Works with content of any length

**About Task Updates**:
- Tasks are processed one-by-one interactively with user
- This ensures quality and gives user control over content
- User can skip tasks if content isn't ready

**Common Pitfalls & Solutions**:
1. **Wrong database**: Always verify you're using the PROJECT page URL, not template
   - Symptom: Updates don't appear in user's page
   - Fix: Fetch project page → Get database URL → Get collection URL

2. **Hardcoded URLs**: Never hardcode page/database/collection URLs
   - Each project has unique IDs
   - Always fetch and extract URLs dynamically

3. **Over-updating**: Many tasks are already complete or are meeting templates
   - Most projects: 3-5 tasks need updates, 13-15 can be skipped
   - Check Status field and existing content first

**Troubleshooting**:
- If MCP fails: Check references/notion-mcp-setup.md
- Verify integration has access to all pages you want to update
- Restart Claude Code if MCP connection issues occur
- If updates don't appear: Verify you're using correct project page URL (not template)
