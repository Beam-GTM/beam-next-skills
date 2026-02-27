# Email Automation - Setup Guide

## ✅ What's Built

The email automation skill is now created and ready to use once Gmail auth is set up.

**Created files:**
- `SKILL.md` - Skill description and documentation
- `README.md` - Usage guide
- `scripts/email_triage.py` - Main triage script
- `SETUP.md` - This file

## 🎯 What It Does

1. **Fetches** unread emails from Gmail (last 24 hours)
2. **Classifies** each email:
   - 🔴 URGENT - Client issues, investor questions, team blockers
   - 💬 RESPONSE_NEEDED - Direct questions, introductions
   - 📋 TASK - "Can you review...", actionable items
   - 📥 ARCHIVE - Newsletters, notifications, FYI emails
   - ⏰ SNOOZE - Non-urgent but important
3. **Drafts responses** (coming next - AI-powered)
4. **Recommends actions** (archive, snooze, create task)

## 🔧 Setup Required

### Step 1: Gmail OAuth Authentication

You need to authenticate once with your Google account:

```bash
# Option A: Re-authenticate (opens browser)
python3 00-system/skills/google/google-master/scripts/google_auth.py --login

# This will:
# 1. Open your browser to Google OAuth consent screen
# 2. Ask you to authorize Gmail access
# 3. Save token to 01-memory/integrations/google-token.json
```

**Required scopes** (already in credentials):
- ✅ `gmail.readonly` - Read emails
- ✅ `gmail.modify` - Archive/mark read
- ✅ `gmail.compose` - Create drafts
- ✅ `gmail.send` - Send emails (with approval)

### Step 2: Test the Connection

```bash
# Test Gmail connection
python3 00-system/skills/google/gmail/scripts/gmail_operations.py list --max 5

# Should show: Your 5 most recent emails
```

### Step 3: Run Email Triage

```bash
# Process last 24 hours of unread emails
python3 03-skills/email-automation/scripts/email_triage.py

# Or specify options
python3 03-skills/email-automation/scripts/email_triage.py --max-emails 50 --hours-back 72
```

## 📊 Expected Output

```
======================================================================
                  📧 EMAIL AUTOMATION - Inbox Triage                   
======================================================================

📥 Fetching unread emails (last 24 hours)...
📧 Found 23 unread emails
✅ Loaded 23 emails     

🤖 Classifying emails with AI...
✅ Processed 23 emails     

======================================================================
                      📊 EMAIL TRIAGE RESULTS                      
======================================================================

🔴 URGENT (2 emails)
   ├─ Christian Engnath | When can we start? ✅ DRAFT
   └─ Fred Medjifa | Exec meeting agenda needed ✅ DRAFT

💬 RESPONSE_NEEDED (5 emails)
   ├─ Sarah | RPO pipeline update ✅ DRAFT
   ├─ Giuseppe | Second interview availability ✅ DRAFT
   └─ ... (3 more)

📥 ARCHIVE (12 emails)
   ├─ LinkedIn | Job recommendations
   ├─ GitHub | Dependabot security alert
   └─ ... (10 more)

⏰ SNOOZE (4 emails)
   ├─ Investor | Q1 metrics → Snooze to Monday
   └─ ... (3 more)

────────────────────────────────────────────────────────────────────
📈 SUMMARY:
   Total processed: 23
   Needs attention: 7
   Can archive: 12
   Time saved: ~46 minutes (estimated)
────────────────────────────────────────────────────────────────────

💾 Full results saved to: email_triage_20260211_003045.json

💡 Next steps:
   1. Review urgent emails first (say 'show urgent drafts')
   2. Approve archive recommendations (say 'execute archives')
   3. Review/edit response drafts (say 'show drafts')

✅ Email triage complete!
```

## 🚀 Next Features to Build

### Phase 1: AI Draft Generation (HIGH PRIORITY)
- [ ] Integrate Claude Sonnet 4.5 for response drafting
- [ ] Learn your communication style from past sent emails
- [ ] Generate contextual responses (not just templates)

### Phase 2: Notion Integration
- [ ] Create tasks in Notion for TASK category emails
- [ ] Link to relevant projects automatically
- [ ] Set due dates based on email content

### Phase 3: Intelligent Learning
- [ ] Learn which emails you always archive vs respond to
- [ ] Adapt classification rules based on your actions
- [ ] Suggest response templates for common email types

### Phase 4: Bulk Operations
- [ ] "Archive all newsletters" in one click
- [ ] "Snooze all recruiting emails to next month"
- [ ] Batch approve drafts

## 💰 Cost Estimate

Once AI draft generation is added:
- **Classification**: GPT-4o-mini ($0.002/email)
- **Draft generation**: Claude Sonnet 4.5 ($0.005/email)
- **Total**: ~$0.007 per email

**Monthly estimate:**
- 50 emails/day: ~$10/month
- 100 emails/day: ~$21/month
- 200 emails/day: ~$42/month

## 🐛 Troubleshooting

### "OAuth credentials not found"
```bash
# Solution: Create credentials file (already done ✅)
# Or re-authenticate:
python3 00-system/skills/google/google-master/scripts/google_auth.py --login
```

### "Token refresh failed"
Your Gmail token expired. Re-authenticate:
```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --login
```

### "No emails found"
Great! Your inbox is empty. Or:
- Check if you have unread emails in Gmail
- Try increasing `--hours-back` (e.g., `--hours-back 168` for 1 week)
- Try removing `is:unread` filter to process all emails

## 📝 Usage in Beam Next

Natural language commands (coming soon):
```
"Process my emails"
"Triage my inbox"
"Check emails from last 3 days"
"Draft responses only"
"Show urgent emails"
"Archive all newsletters"
```

## 🔗 Related Skills

Part of CEO Office Automation System:
- `slack-review` - Daily Slack message triage (Phase 2.3)
- `whatsapp-assistant` - WhatsApp automation (Phase 2.2)
- `ceo-office-daily` - Orchestrates all daily automations (Phase 5)

## ✅ Current Status

- [x] Skill created
- [x] Gmail integration set up
- [x] Classification rules (heuristic)
- [ ] Gmail OAuth authentication ← **YOU ARE HERE**
- [ ] AI-powered classification
- [ ] AI draft generation
- [ ] Notion task creation
- [ ] Testing with real inbox

**Next step:** Authenticate Gmail and run first test!
