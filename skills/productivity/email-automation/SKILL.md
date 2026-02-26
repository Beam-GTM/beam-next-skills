---
name: email-automation
version: '1.0'
description: Load when user says "process emails", "triage inbox", "email automation",
  "check emails", or "inbox zero"
author: Jonas Diezun
category: productivity
tags:
- automation
- email
updated: '2026-02-16'
visibility: public
priority: high
---
# Email Automation Skill

**Purpose**: Automatically triage your inbox, draft responses, and recommend actions (archive, snooze, create task).

---

## What This Skill Does

1. **Fetches unread emails** from Gmail
2. **Classifies each email** into categories:
   - 🔴 **URGENT** - Needs immediate response
   - 💬 **RESPONSE NEEDED** - Requires your reply
   - 📋 **TASK** - Creates a task in Notion
   - 📥 **ARCHIVE** - No action needed, can archive
   - ⏰ **SNOOZE** - Review later (suggest snooze date)
3. **Drafts responses** for emails that need replies
4. **Presents recommendations** for you to approve

---

## Usage

### Basic
```
"Process my emails"
"Triage my inbox"
"Help me with email zero"
```

### Advanced
```
"Process last 50 emails"
"Check emails from last 3 days"
"Draft responses only"
```

---

## How It Works

### CRITICAL: Messages vs Threads
The Gmail API returns **individual messages**, not threads. A 200-message inbox may only be ~70 unique threads. **Always deduplicate by `thread_id`** before presenting results or counting:
```python
from collections import defaultdict
threads = defaultdict(list)
for e in emails:
    threads[e['thread_id']].append(e)
# Use threads dict for counting and display
```

### Step 1: Fetch Emails
- Connects to Gmail API via google-master integration
- Fetches inbox emails (default: all inbox, max 100)
- Extracts: sender, subject, snippet, full body
- **Deduplicates by thread_id** to get unique conversations

### Step 2: AI-Powered Triage
For each email, AI analyzes:
- **Sender importance** (client, team, investor, recruiter, newsletter)
- **Urgency signals** (deadline mentions, "URGENT", meeting requests)
- **Action required** (question asked, decision needed, FYI only)
- **Context** (relates to projects, hiring, sales, operations)

### Step 3: Generate Recommendations
- **Draft response** if reply needed (using your tone and context)
- **Suggest archive** if no action needed
- **Suggest snooze** with date (e.g., "snooze until Monday")
- **Create Notion task** if actionable work item

### Step 4: Present for Approval
Shows summary table:
```
EMAIL TRIAGE RESULTS (25 emails processed)

│ # │ FROM              │ SUBJECT                    │ ACTION       │ DRAFT?  │
├───┼───────────────────┼────────────────────────────┼──────────────┼─────────┤
│ 1 │ sarah@beam.com    │ RPO Pipeline Update        │ RESPONSE     │ ✅ Ready │
│ 2 │ linkedin          │ Job recommendations        │ ARCHIVE      │         │
│ 3 │ investor@vc.com   │ Q1 metrics check-in        │ SNOOZE (Mon) │         │
```

User can then:
- Approve all actions
- Review/edit specific drafts
- Skip certain emails

---

## Configuration

### Email Classification Rules

**URGENT** (needs immediate response within 24h):
- Client escalation ("issue", "problem", "not working")
- Investor asking for metrics
- Team member blocked ("need your input", "waiting on")
- Meeting today/tomorrow

**RESPONSE NEEDED** (reply within 2-3 days):
- Direct questions to you
- Introduction requests
- Partnership discussions
- Interview scheduling

**TASK** (create Notion task):
- "Can you review..."
- "Need feedback on..."
- "When you have time..."
- Long-form work items

**ARCHIVE** (no action needed):
- Newsletters
- Automated notifications
- CC'd for FYI
- Already handled by someone else

**SNOOZE** (defer):
- Non-urgent but important
- "End of week" / "next month" mentions
- Events/deadlines in future

### Response Draft Style

Drafts use your communication style:
- **Concise** - 2-4 sentences max
- **Direct** - Clear yes/no, specific next steps
- **Professional but friendly** - Warm but efficient
- **Action-oriented** - Always include next step or deadline

Example draft:
```
Hi Sarah,

Great update on the RPO pipeline. The 3 new leads look promising.

Let's sync Friday 2pm to review the Zurich proposal. I'll send a calendar invite.

Jonas
```

---

## Workflow

### Full Inbox Triage
```bash
1. Run: "Process my emails"
2. Wait ~30-60 seconds (AI processes each email)
3. Review: Table with recommendations
4. Approve: "Execute all" or review individually
5. Done: Drafts saved, emails archived/snoozed
```

### Draft-Only Mode
```bash
1. Run: "Draft responses only"
2. AI generates drafts for emails needing replies
3. Review: Drafts shown one by one
4. Edit/approve each draft
5. Done: Drafts saved to Gmail drafts folder
```

### Quick Scan Mode
```bash
1. Run: "Quick email scan"
2. AI shows summary only (no drafts)
3. Highlights urgent items
4. Done: You decide what to action
```

---

## Integration with Notion

**Task Creation**:
- Emails marked as TASK → Create entry in Tasks JBD database
- Properties set: 
  - Action Zone: "Inbox Processing"
  - Status: "📥 Incoming"
  - Priority: Based on email urgency
  - Due date: Extracted from email if mentioned

**Project Linking**:
- If email relates to active project (detected by keywords), link task to project

---

## Privacy & Security

- **Read-only by default**: Only reads emails, doesn't send without approval
- **Draft folder**: All responses saved as Gmail drafts for review
- **No auto-send**: You must approve before any email is sent
- **Sensitive emails**: Can flag certain senders as "never auto-draft" (investors, board, personal)

---

## Superhuman Compatibility

### Snoozed Emails
Superhuman uses a custom Gmail label for snoozes — **not** Gmail's native snooze:
- Label: `[Superhuman]/Is Snoozed` (Gmail ID: `Label_3`)
- Query: `list_emails(label_ids=['Label_3'])` — do NOT use `in:snoozed`

### Superhuman AI Categories
Superhuman auto-categorizes emails with labels:
- `[Superhuman]/AI/Respond` (Label_29), `AI/Waiting` (Label_23), `AI/Meeting` (Label_24)
- `AI/News` (Label_25), `AI/Investors` (Label_30), `AI/AutoArchived` (Label_32)

### Creating Drafts — KNOWN LIMITATION
**Superhuman does NOT show drafts created via the Gmail API.** Superhuman has its own draft system that doesn't sync inbound from Gmail.

**Practical workflow:**
1. Create threaded draft via `create_threaded_draft()` — appears in **Gmail web** (mail.google.com)
2. **Or** show the draft text directly to the user so they can copy-paste into Superhuman's composer
3. Always use threaded drafts (with `threadId`, `In-Reply-To`, `References`) for proper Gmail web threading

```python
from gmail_operations import create_threaded_draft
create_threaded_draft(
    original_message_id='<msg-id>',
    to='recipient@example.com',
    subject='Re: Subject',
    body='Reply here'
)
```

---

## Bulk Archive Workflow

For cleaning up large inboxes, use this pattern:
1. Fetch all inbox messages: `list_emails(query='in:inbox', max_results=200)`
2. Group by `thread_id` to get unique conversations
3. Categorize threads by keywords/sender patterns
4. Archive all messages in a thread: `archive_email(msg_id)` for each message with INBOX label
5. Save a tracker file before archiving (for reference)

### Proven Category Keywords (from real triage)
- **Investor/VC**: ventures, capital, partners, fund, intro, catch-up, reconnect, beam <>
- **Notifications**: newsletter, no-reply, noreply, notification, amie
- **Superhuman reminders**: `reminder@superhuman.com` (these are unsnoozed emails)

---

## Advanced Features (Future)

- **Learning your preferences**: Over time, learns which emails you always archive vs respond to
- **Response templates**: Common responses ("Thanks, will review", "Let's schedule a call")
- **Thread context**: Analyzes full email thread, not just last message
- **Calendar integration**: When drafting meeting responses, checks your availability
- **Bulk operations**: "Archive all newsletters", "Snooze all recruiting emails to next month"

---

## Example Session

```
You: "Process my emails"

AI: Fetching unread emails from Gmail...
    Found 23 unread emails from last 24 hours.
    Analyzing with AI...
    
    EMAIL TRIAGE RESULTS
    
    🔴 URGENT (2 emails)
    ├─ Christian Engnath - "When can we start?" → DRAFT READY
    └─ Fred - "Exec meeting agenda approval needed" → DRAFT READY
    
    💬 RESPONSE NEEDED (5 emails)
    ├─ Sarah - "RPO pipeline update" → DRAFT READY
    ├─ Giuseppe - "Second interview availability" → DRAFT READY
    └─ ... (3 more)
    
    📥 ARCHIVE (12 emails)
    ├─ LinkedIn - "Job recommendations"
    ├─ GitHub - "Dependabot security alert"
    └─ ... (10 more)
    
    ⏰ SNOOZE (4 emails)
    ├─ Investor - "Q1 metrics" → Snooze to Monday
    └─ ... (3 more)
    
    Actions:
    1. Review urgent drafts first? (say "show urgent")
    2. Execute all recommendations? (say "execute all")
    3. Review each email? (say "review each")

You: "Show urgent"

AI: [Shows draft for Christian]
    ---
    Hi Christian,
    
    Great to hear you're ready to move forward! 
    
    Can you start Monday Feb 17? Fred will send you the onboarding details today.
    
    Looking forward to working together.
    
    Jonas
    ---
    
    Approve this draft? (yes/edit/skip)

You: "Yes"

AI: ✅ Draft saved to Gmail drafts
    [Shows next urgent draft...]
```

---

## Technical Implementation

### Gmail API Endpoints Used
- `users.messages.list` - Fetch unread emails
- `users.messages.get` - Get full email content
- `users.drafts.create` - Save response drafts
- `users.messages.modify` - Archive emails
- `users.threads.modify` - Mark as read/snooze

### AI Model
- **Classification**: GPT-4o-mini (fast, cost-effective for triage)
- **Draft generation**: Claude Sonnet 4.5 (better writing quality)

### Caching Strategy
- Cache email classifications for 24 hours (avoid re-processing)
- Cache common response templates

---

## Cost Estimation

- **Per email**: ~$0.002 (classification + draft if needed)
- **50 emails/day**: ~$0.10/day = ~$3/month
- **High volume (200 emails/day)**: ~$0.40/day = ~$12/month

---

## Success Metrics

Track these to measure effectiveness:
- **Time saved**: Before/after time spent on email
- **Inbox zero frequency**: How often you reach zero unread
- **Draft acceptance rate**: % of AI drafts you send with minimal edits
- **Archive accuracy**: % of auto-archived emails that didn't need action

---

**Status**: Ready to implement  
**Priority**: High (Phase 2.1 of CEO Office Automation)  
**Dependencies**: Gmail API access (via google-master), Notion API (via notion-master)
