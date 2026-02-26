---
name: setup-linear-onboarding-template
version: '1.0'
description: Interactive assistant to fill Linear onboarding template projects with
  content from user's workspace. Load when user mentions "setup linear template",
  "fill linear project", "onboard client in linear", or provides a Linear project
  URL. Guides user through each task, suggests content from workspace folders, and
  updates Linear issues with approved content.
author: Jack Li
category: general
tags:
- linear
platform: Linear
updated: '2025-12-10'
visibility: team
---
# Setup Linear Onboarding Template

Interactive assistant that helps fill Linear template projects with actual content by suggesting relevant information from your workspace and updating issues with your approval.

## Purpose

This skill helps you quickly populate Linear onboarding template projects (like client onboarding checklists) by:
- Walking through each task one by one
- Asking what information is needed for each task
- Searching your workspace folders for relevant content
- Suggesting content to fill in the task
- Updating Linear issues only after your confirmation

**Key Features**:
- Interactive task-by-task guidance
- Intelligent content suggestions from workspace
- Safety checks before updating Linear
- Maintains context across all issues
- Reduces manual copy-paste work

**Time Estimate**: Varies (5-30 minutes depending on project size)

---

## Workflow

### Step 1: Get Project Link

Ask the user for the Linear project URL:
- "Please provide the Linear project URL you want to fill in"
- Example: `https://linear.app/beam-ai/project/client-name-20bd4dc0dc9f/issues`

Extract the project ID from the URL and confirm with user:
- Show project name, status, and issue count
- Ask: "Is this the correct project?"

**Mark this todo complete before proceeding.**

---

### Step 2: Check Linear MCP Setup

Verify Linear MCP integration is configured:

1. Try to fetch the project using `mcp__linear__get_project`
2. If it fails, guide user to setup Linear MCP:
   - "Linear MCP is not configured. Would you like me to help you set it up?"
   - If yes, trigger the `add-integration` skill for Linear
   - If no, pause and wait for user to configure manually
3. If successful, proceed to next step

**Mark this todo complete before proceeding.**

---

### Step 3: Fetch Project Data

Use Linear MCP to get complete project information:

1. Fetch project details: `mcp__linear__get_project`
2. Fetch all issues: `mcp__linear__list_issues` (with project filter, limit=250)
3. Display summary to user:
   - Project name and description
   - Total number of issues
   - Current status of issues (how many backlog, in progress, etc.)

**Mark this todo complete before proceeding.**

---

### Step 4: Ask User for Content Sources

Ask user to point to folders or files that contain relevant information:

"Where should I look for content to fill in these tasks? You can specify:
- Folder paths (e.g., `04-workspace/Workflow/`)
- Specific files (e.g., `04-workspace/Workflow/client-proposal.md`)
- Multiple locations (comma-separated)"

Store the user's response as the content search locations.

**Mark this todo complete before proceeding.**

---

### Step 5: Update Project Overview (Section by Section)

Update the project description with content from your workspace. Use the template structure from `references/client-name-template.md` as a guide.

**Template Sections to Fill:**
1. **Project Overview** - Main description of the project
2. **Client Use Case** - Primary use case and key objectives
3. **Client Requirements Overview** - Outcomes and workflows
4. **Workflows to be built** - Detailed workflow steps
5. **Software to be integrated** - List of platforms and actions
6. **Deliverables** - Phase timeline and deliverables table

For each section:

**5a. Display Section**
- Show: Section name and current content (if any)
- Show: Progress (e.g., "Section 1 of 6")

**5b. Search User's Folders**
- Look for relevant content in specified folders/files
- Search for keywords related to the section (e.g., "workflow", "use case", "deliverables")
- Find the most relevant information

**5c. Suggest Content**
- Present findings: "I found this content in [file/location]:"
- Show relevant snippets or summaries
- If nothing found, say: "I couldn't find content for this section. Would you like to:"
  - Provide content manually
  - Skip this section
  - Search in different locations

**5d. Ask for Confirmation**
- "Would you like me to update this section with the suggested content?"
- Options: Yes / Edit first / Skip / Cancel process
- If "Edit first", ask user to provide modified content

**5e. Update Section (if approved)**
- Build complete project description with all approved sections
- After ALL sections are reviewed, update project using `mcp__linear__update_project`
- Show: "✅ Project overview updated"

**Mark this step complete before proceeding.**

---

### Step 6: Process Issues One by One

Go through each issue/task in the project:

**IMPORTANT: Always fetch current content FIRST**
- Use `mcp__linear__get_issue` to get current description
- Show user what's already there before suggesting updates
- Never overwrite without showing comparison

**6a. Display Current Issue**
- Show: Issue ID, Title, Current Status, Description (fetched from Linear)
- Show: Current task number (e.g., "Task 5 of 18")
- Show: Any existing content that's already filled in

**6b. Ask What's Required**
- "What information do you need for this task?"
- "What should I look for in your workspace?"
- Allow user to skip if task doesn't need content updates
- Allow user to pause workflow and create new related issues if needed

**6c. Search User's Folders**
- Use Grep/Read to search specified folders/files for relevant content
- Look for keywords from the issue title and user's requirements
- Find the most relevant sections or files

**6d. Suggest Content**
- Present findings: "I found this content in [file/location]:"
- Show 2-3 relevant snippets or summaries
- If nothing found, say: "I couldn't find relevant content. Would you like to:"
  - Provide content manually
  - Skip this task
  - Search in different locations

**6e. Ask for Confirmation**
- "Would you like me to update this issue with the suggested content?"
- Options:
  - Yes - Update with suggested content
  - Edit first - Let user modify content before updating
  - Skip - Move to next task without updating
  - Mark as done - Mark complete and optionally assign
  - Create related issues - Pause to create additional tasks
  - Cancel entire process - Stop the workflow
- If "Edit first", ask user to provide modified content
- If "Mark as done", ask who to assign it to (or leave unassigned)
- If "Create related issues", pause workflow to create new Linear issues, then resume

**6f. Update Issue (if approved)**
- Use `mcp__linear__update_issue` to update the issue description or create comment
- **IMPORTANT:** When user provides real content, remove template/placeholder content
  - Example: Remove template links when adding actual client-specific links
  - Keep only the real, actionable content
- **Status & Assignment:** Can also mark as Done and assign to team members
  - Use status ID for "Done" status
  - Use assignee parameter with user ID or email
- Confirm update was successful
- Show updated issue URL

**Mark each issue as complete before moving to next one.**

---

### Step 7: Summary and Completion

After processing all issues:

1. Display completion summary:
   - Total issues processed
   - Issues updated
   - Issues skipped
   - Time saved estimate
2. Ask user: "Would you like to review the project in Linear?"
3. Provide project URL for final review

**Mark this todo complete before proceeding.**

---

### Step 8: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

**This is the final mandatory step.**

---

## Example Interaction Flow

```
AI: "Please provide the Linear project URL you want to fill in"
User: "https://linear.app/beam-ai/project/client-name-20bd4dc0dc9f/issues"

AI: "Found project: [Client Name] with 18 issues. Is this correct?"
User: "yes"

AI: "Where should I look for content? (folders or files)"
User: "04-workspace/Workflow/"

AI: "Let's fill in the project overview first. Section 1 of 6: Project Overview"
AI: "I found this content in 04-workspace/Workflow/client-proposal.md:
[Shows snippet]
Would you like me to use this for the Project Overview section?"
User: "yes"

AI: "Section 2 of 6: Client Use Case"
AI: "I found this content in 04-workspace/Workflow/use-case-document.md:
[Shows snippet]
Would you like me to use this?"
User: "edit first"
AI: "Please provide the content you'd like to use:"
User: "[provides edited content]"

[Continues through all 6 sections...]

AI: "✅ All sections reviewed. Updating project overview in Linear..."
AI: "✅ Project overview updated!"

AI: "Now let's go through the tasks. Task 1 of 18: CLI-3933 - Setup Client Notion"
AI: "What information do you need for this task?"
User: "client's notion page URL and workspace setup details"

AI: "I found relevant content in 04-workspace/Workflow/client-onboarding-guide.md:
[Shows snippet]
Would you like me to update the issue with this?"
User: "yes"

AI: "✅ Updated CLI-3933. Moving to next task..."
[Continues through all issues]
```

---

## Resources

### references/client-name-template.md

Example template project structure for reference. Shows typical onboarding project format.

---

## Notes

**About Linear MCP Integration:**
- Requires `mcp__linear__get_project`, `mcp__linear__list_issues`, `mcp__linear__update_project`, `mcp__linear__update_issue`
- Project description updated via `mcp__linear__update_project`
- Issue updates can be made to description or as comments
- Always confirm before updating to prevent accidental changes

**Best Practices:**
- **ALWAYS fetch current content first** - Use `mcp__linear__get_issue` before suggesting updates
- Process issues in order (helps maintain context)
- Ask user before making ANY Linear updates
- Allow user to skip tasks that don't need updates
- Search workspace thoroughly before suggesting "not found"
- Keep user informed of progress (task X of Y)
- Support workflow interruption - user may need to pause and create related issues

**Safety Features:**
- No updates without explicit user confirmation
- Always show current content before overwriting
- User can cancel process at any time
- All changes are reversible in Linear
- Clear visibility of what will be updated

**Workflow Flexibility:**
- User can pause midway to create new issues
- Workflow can be resumed or stopped at any point
- Support creating related/dependent issues during execution
- Allow partial completion (e.g., process 9 of 18 tasks, then stop)
