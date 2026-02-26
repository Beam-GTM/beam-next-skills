# Email Automation Skill

AI-powered inbox triage that classifies emails, drafts responses, and recommends actions.

## Quick Start

```bash
# Process last 24 hours of unread emails
python 03-skills/email-automation/scripts/email_triage.py

# Process last 50 emails from last 3 days
python 03-skills/email-automation/scripts/email_triage.py --max-emails 50 --hours-back 72

# Test mode (dry run, no changes)
python 03-skills/email-automation/scripts/email_triage.py --test
```

Or use natural language:
```
"Process my emails"
"Triage my inbox"
"Check emails from last 3 days"
```

## What It Does

1. **Fetches** unread emails from Gmail
2. **Classifies** each email:
   - 🔴 URGENT - Needs immediate response
   - 💬 RESPONSE_NEEDED - Reply required
   - 📋 TASK - Create Notion task
   - 📥 ARCHIVE - No action needed
   - ⏰ SNOOZE - Review later
3. **Drafts** responses for emails needing replies
4. **Recommends** actions for you to approve

## Output Example

```
📊 EMAIL TRIAGE RESULTS

🔴 URGENT (2 emails)
   ├─ Christian Engnath | When can we start? ✅ DRAFT
   └─ Fred Medjifa | Exec meeting agenda needed ✅ DRAFT

💬 RESPONSE_NEEDED (5 emails)
   ├─ Sarah | RPO pipeline update ✅ DRAFT
   └─ ... 4 more

📥 ARCHIVE (12 emails)
   ├─ LinkedIn | Job recommendations
   └─ ... 11 more

📈 SUMMARY:
   Total processed: 19
   Needs attention: 7
   Can archive: 12
   Time saved: ~38 minutes
```

## Setup

### 1. Gmail API Access

Make sure you have Gmail API set up via google-master:

```bash
# Test Gmail connection
python 00-system/skills/google/google-master/scripts/gmail_list.py
```

If not set up, follow google-master setup instructions.

### 2. AI Model Access

The skill uses:
- **GPT-4o-mini** for classification (fast, cheap)
- **Claude Sonnet 4.5** for draft generation (high quality)

Make sure you have API keys in environment or config.

## Advanced Usage

### Review Drafts

After processing, review drafts:
```
"Show urgent drafts"
"Show all drafts"
"Show draft for email #3"
```

### Execute Actions

Approve recommendations:
```
"Execute all archives"  # Archive all ARCHIVE category emails
"Execute all"           # Execute all recommendations
"Approve draft #1"      # Send specific draft
```

### Customize Rules

Edit classification rules in:
```
03-skills/email-automation/references/classification_rules.yaml
```

## Cost

Estimated costs per run:
- 50 emails: ~$0.10 (2x per day = $6/month)
- 200 emails: ~$0.40 (2x per day = $24/month)

## Privacy

- **Read-only by default**: No emails sent without approval
- **Drafts only**: Responses saved to Gmail drafts folder
- **No auto-send**: You must explicitly approve each action
- **Local processing**: Email content not stored permanently

## Roadmap

- [ ] **Phase 1**: Basic triage + classification ← YOU ARE HERE
- [ ] **Phase 2**: AI draft generation (Claude integration)
- [ ] **Phase 3**: Notion task creation integration
- [ ] **Phase 4**: Learning preferences over time
- [ ] **Phase 5**: Bulk operations (archive all newsletters)
- [ ] **Phase 6**: Thread context analysis
- [ ] **Phase 7**: Calendar integration for scheduling

## Troubleshooting

### "Gmail utils not found"
```bash
# Make sure google-master is set up
ls 00-system/skills/google/google-master/scripts/gmail_utils.py
```

### "Failed to connect to Gmail"
```bash
# Re-authenticate with Gmail
python 00-system/skills/google/google-master/scripts/gmail_auth.py
```

### "No emails found"
Your inbox is empty or all emails are already read. Great job! 🎉

## Integration with CEO Office

This skill is part of the CEO Office Automation System:
- **Project**: `02-projects/Beam/02-ceo-office-automation-system`
- **Phase**: 2.1 - Communication Automation
- **Dependencies**: Gmail API, Notion API (for task creation)

Related skills:
- `slack-review` - Daily Slack message triage
- `whatsapp-assistant` - WhatsApp message automation
- `ceo-office-daily` - Orchestrates all daily automations
