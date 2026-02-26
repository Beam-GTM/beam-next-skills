---
name: learn-integrations
version: '1.0'
description: 'Learn about Beam Next integrations and MCP. Load when user mentions:
  learn integrations, what is MCP, connect tools, integration tutorial, add integration,
  external tools, API connections, third party, how to integrate. 10-12 min.'
category: learning
tags:
- api
updated: '2026-02-25'
visibility: public
onboarding: true
priority: high
---
## [TARGET] AI Proactive Triggering (ONBOARDING SKILL)

**This is an ONBOARDING skill with HIGH PRIORITY for proactive suggestion.**

### When to Proactively Suggest (AI MUST check user-config.yaml)

Check `learning_tracker.completed.learn_integrations` in user-config.yaml. If `false`:

**PROACTIVELY SUGGEST when user:**
1. Mentions ANY external tool (GitHub, Slack, Notion, Airtable, Google Drive, Linear, etc.)
2. Says "I use..." or "I work with..." followed by a tool name
3. Asks about connecting, syncing, or automating with external services
4. Expresses frustration about copying data between tools
5. Asks "can you access..." or "can you connect to..."
6. Mentions MCP, API, or integration in any context
7. At the END of completing another onboarding skill (suggest as next step)

**Suggestion Pattern:**
```
💡 I notice you haven't learned about integrations yet. Understanding how Beam Next
connects to external tools (like [tool they mentioned]) takes about 10 minutes
and will help you work more efficiently.

Would you like to run 'learn integrations' now? (You can always do it later)
```

**DO NOT suggest if:**
- `learning_tracker.completed.learn_integrations: true`
- User explicitly dismissed learning skills
- User is mid-task and focused on something else

---

# Learn Integrations

Learn how to connect external tools to Beam Next via MCP (Model Context Protocol).

## Purpose

This skill teaches you how integrations work in Beam Next — what they are, which ones are available, and when/how to add them. By the end, you'll understand:

- What MCP is and why it matters
- Which integrations are available
- When to add integrations vs work standalone
- How to set up your first integration

**Time Estimate**: 10-12 minutes

---

## Workflow

### Step 1: Why Integrations?

**Ask**: "Before we dive in — do you currently use any external tools for your work? Things like GitHub, Notion, Slack, Airtable, Google Drive, or Linear?"

**Listen for**: Tools they already use, how they use them, pain points.

**Respond based on answer**:
- If they mention tools → "Perfect! Integrations let me work directly with those tools."
- If they're unsure → "That's fine! Let's explore what's possible."

---

### Step 2: What is MCP?

**Display**:
```
--- WHAT IS MCP? -------------------------------------------

MCP (Model Context Protocol) is like a universal adapter.
It lets me connect to your external tools and work with them directly.

WITHOUT MCP:
  You: "Check my GitHub issues"
  Me: "I can't access GitHub directly. Please copy-paste the info."
  You: [manually copies data]

WITH MCP:
  You: "Check my GitHub issues"
  Me: [directly queries GitHub] "You have 5 open issues..."

Think of MCP as building bridges between Beam Next and your tools.
------------------------------------------------------------
```

**Ask**: "Does that make sense? Any questions about what MCP does?"

---

### Step 3: Available Integrations

**Display**:
```
--- CORE INTEGRATIONS --------------------------------------

Beam Next includes master skills for these integrations:

🔷 BUILT-IN (Ready to Configure)
   • Notion     → "connect notion"     → Databases, pages, search
   • Airtable   → "connect airtable"   → Bases, records, automation
   • Slack      → "connect slack"      → Messages, channels, team comms
   • Google     → "connect google"     → Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides
   • HubSpot    → "connect hubspot"    → CRM, contacts, deals
   • Beam.ai    → "beam" commands      → AI agent workflows

[PLUG] MCP SERVERS (Via add-integration skill)
   • GitHub     → Repos, issues, PRs, actions
   • Linear     → Issues, projects, roadmaps
   • PostgreSQL → Direct database queries
   • Filesystem → Local file operations
   • And 50+ more via MCP directory

------------------------------------------------------------
```

**Ask**: "Any of these tools sound relevant to your work?"

---

### Step 4: When to Integrate

**Display**:
```
--- INTEGRATION DECISION FRAMEWORK -------------------------

[OK] ADD AN INTEGRATION WHEN:
   • You frequently copy-paste data from a tool
   • You want automated workflows (e.g., create GitHub issue from task)
   • You need real-time data (e.g., check Slack messages)
   • The tool is central to your daily work

[ERROR] SKIP INTEGRATION WHEN:
   • You rarely use the tool
   • Manual copy-paste is fast enough
   • The tool doesn't have MCP support
   • You prefer keeping systems separate

REMEMBER: Beam Next works perfectly standalone!
Integrations are power-ups, not requirements.
------------------------------------------------------------
```

**Confirm**: "Make sense? The key is: integrate what adds value to YOUR workflow."

---

### Step 5: How to Add Integrations

**Display**:
```
--- ADDING INTEGRATIONS ------------------------------------

METHOD 1: Built-in Master Skills
   Just say the command:
   • "connect notion"    → Notion setup wizard
   • "connect airtable"  → Airtable setup wizard

METHOD 2: MCP Server Setup
   Say "add integration" → I'll guide you through:
   1. Installing the MCP server
   2. Getting API credentials
   3. Configuring the connection
   4. Testing it works
   5. Documenting in your Memory

TIME: 10-20 minutes per integration

------------------------------------------------------------
```

---

### Step 6: Quick Example

**Display**:
```
--- EXAMPLE: NOTION INTEGRATION ----------------------------

BEFORE (No Integration):
  You: "Add this task to my Notion board"
  Me: "I can't access Notion. Here's the formatted text to copy..."
  You: [Opens Notion, manually adds task]

AFTER (With Integration):
  You: "Add this task to my Notion board"
  Me: [Directly creates task in Notion] "Done! Added to your Tasks database."

OTHER USE CASES:
  • "Query my projects database in Notion"
  • "Sync session report to Notion"
  • "Search my notes for [topic]"

------------------------------------------------------------
```

---

### Step 7: What's Next?

**Ask**: "Would you like to set up an integration now, or save it for later?"

**IF YES** (wants to integrate now):
- "Which tool would you like to connect?"
- Based on response:
  - Notion → Load `notion-connect` skill
  - Airtable → Load `airtable-connect` skill
  - Slack → Load `slack` skill (from google folder)
  - Google/Gmail/Docs/Sheets/Calendar/Drive/Tasks/Slides → Load `google` skill
  - Other → Load `add-integration` skill
- Skip Step 8, proceed to finalization after integration complete

**IF NO** (save for later):
- "No problem! When you're ready, just say:"
  - `'connect notion'` for Notion
  - `'connect airtable'` for Airtable
  - `'connect slack'` for Slack
  - `'connect google'` for Google Workspace (Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides)
  - `'add integration'` for any other tool
- Proceed to Step 8

---

### Step 8: Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       learn_integrations: true  # ADD THIS LINE
   ```

2. **Display completion**:
   ```
   [OK] Learn Integrations Complete!

   You now understand:
   • What MCP is (universal adapter for tools)
   • Available integrations (Notion, Airtable, Slack, Google, etc.)
   • When to integrate (adds value) vs skip (overhead)
   • How to add them (built-in skills or 'add integration')

   Next steps:
   • 'connect notion' - Set up Notion
   • 'connect airtable' - Set up Airtable
   • 'connect slack' - Set up Slack
   • 'connect google' - Set up Google Workspace (7 services)
   • 'add integration' - Any other tool
   • 'learn projects' or 'learn skills' - Continue learning
   ```

3. **Session ending tip**:
   ```
   💡 When you're done, open a NEW chat for your next topic.
   ```

---

## Success Criteria

- [ ] User understands what MCP is
- [ ] User knows which integrations are available
- [ ] User understands when to integrate vs work standalone
- [ ] User knows commands to add integrations
- [ ] `learning_tracker.completed.learn_integrations: true` in user-config.yaml

---

## Notes

**Key Messages**:
- Integrations are optional power-ups, not requirements
- Beam Next works perfectly standalone
- Add integrations that save YOU time
- Start with one, add more as needed

**Related Skills**:
- `add-integration` - General MCP server setup
- `notion-connect` - Notion-specific setup
- `airtable-connect` - Airtable-specific setup
- `notion-master` - Shared Notion resources
- `airtable-master` - Shared Airtable resources

**Resources**:
- MCP Documentation: https://modelcontextprotocol.io/
- MCP Server Directory: https://github.com/modelcontextprotocol/servers
