---
name: 1on1-followup
version: '1.0'
description: 'Quick post-meeting follow-up for 1-on-1s. Triggers: ''1on1 followup'',
  ''follow up on my 1on1'', ''1on1 with [name]'', ''debrief my 1on1'', ''process my
  1on1 with [name]''.'
author: Jonas Diezun
category: productivity
tags:
- meeting
updated: '2026-02-10'
visibility: public
---
# 1on1 Follow-Up

Quick debrief after any 1-on-1. Fetches the latest transcript, extracts commitments, and gives you 3 sharp coaching notes. Takes 2 minutes.

## When to Use

Run this right after a 1-on-1 ends. It's the "close the loop" skill — capture what happened before you forget.

| Use This | Not This |
|----------|----------|
| "Just finished my 1on1 with Saqib" | "Deep review of my meeting" → use `1on1-review` |
| "Process my 1on1 with Brad" | "How am I doing overall?" → use `1on1-review` |
| Quick debrief, action capture | Full expert coaching analysis |

---

## Workflow

### Step 1: Identify the Meeting

**Option A — Name provided**:
```
User: "1on1 followup with Brad"
→ Look in 04-workspace/ceo-office/1on1s/brad/transcripts/ for latest file
→ If not found, fetch from Amie using fetch_1on1s.py --person Brad --since [today]
```

**Option B — No name**:
```
User: "1on1 followup"
→ AI asks: "Who was the 1-on-1 with?"
```

**Option C — Fetch fresh**:
If the transcript isn't saved yet, run:
```bash
python3 02-projects/Beam/10-1on1-excellence/02-resources/scripts/fetch_1on1s.py --person [name] --since [today's date]
```

### Step 2: Read Transcript

Load the transcript from `04-workspace/ceo-office/1on1s/{person}/transcripts/`.

### Step 3: Generate Follow-Up

Output this format — short, sharp, actionable:

```
═══════════════════════════════════════
1ON1 FOLLOW-UP — {Person}, {Date}
═══════════════════════════════════════

⏱ {Duration} min | {1-line topic summary}

────────────────────────────────────────
📋 COMMITMENTS
────────────────────────────────────────

YOUR commitments:
- [ ] {What you promised} — by {date if mentioned, else "TBD"}
- [ ] {What you promised}

THEIR commitments:
- [ ] {What they promised} — by {date if mentioned, else "TBD"}
- [ ] {What they promised}

⚠️ OPEN LOOPS (mentioned but no owner/deadline):
- {Topic that was discussed but not resolved}

────────────────────────────────────────
💡 3 COACHING NOTES
────────────────────────────────────────

✅ WORKED: {One specific thing you did well — with quote}

⚠️ IMPROVE: {One specific thing to do differently next time — with concrete alternative}

❓ ASK NEXT TIME: {One specific question to open the next 1-on-1 with this person}

────────────────────────────────────────
✉️ SEND TO {Person}
────────────────────────────────────────

{Short follow-up message to send directly to the person.
Casual, warm, their tone. Summarizes what was agreed,
lists their commitments, and sets the next checkpoint.
No coaching language — this is peer-to-peer, not manager notes.
2-4 short paragraphs max. Ready to paste into Slack/chat.}

────────────────────────────────────────
```

### Step 4: Save

Save to: `04-workspace/ceo-office/1on1s/{person}/followups/{date}-followup.md`

If the `followups/` subfolder doesn't exist, create it.

---

## Coaching Notes Guidelines

Keep each note to 1-2 sentences max. Be specific — quote the transcript.

**WORKED** — Pick ONE moment. Not generic praise. Reference what was said.
- Good: "You challenged Brad directly: 'Sell me one thing 100 times.' Clear, no hedging."
- Bad: "Good meeting overall, nice rapport."

**IMPROVE** — Pick ONE thing. Give the alternative phrasing.
- Good: "When you said 'we need to figure this out' — try instead: 'You own this. Deliverable by Friday.'"
- Bad: "Could be more structured."

**ASK NEXT TIME** — Based on unresolved topics or commitments from THIS meeting.
- Good: "Open with: 'Last time you committed to the pricing one-pager. Show me.'"
- Bad: "Ask how they're doing."

**SEND MESSAGE** — A short message to send to the person after the meeting.
- Tone: casual, warm, peer-to-peer. Match the relationship dynamic from the transcript.
- Content: recap what you agreed on, list their action items, set a checkpoint.
- No coaching language, no manager speak, no "as discussed" corporate filler.
- Ready to copy-paste into Slack or chat. 2-4 short paragraphs.
- Good: "Hey, good chat. So the play is: you pick the ONE workflow we sell 100x. I'll sort the landing page / funnel. Let's regroup Thursday — show me what you've got."
- Bad: "Hi Brad, as per our discussion today, please find below a summary of agreed action items..."

---

## Key Principles

1. **Speed over depth** — This is a 2-minute skill, not a 10-minute analysis
2. **Commitments are king** — The most valuable output is the commitment list
3. **One of each** — One thing that worked, one to improve, one question. Not three of each.
4. **Quote the transcript** — Specificity beats generality every time
5. **Open loops matter** — Things discussed without resolution tend to die. Flag them.

---

## Example

```
User: "1on1 followup with Brad"

AI: [Fetches latest Brad transcript]

═══════════════════════════════════════
1ON1 FOLLOW-UP — Brad, 2026-02-05
═══════════════════════════════════════

⏱ 9 min | Repeatable recruitment workflow, beachhead strategy

────────────────────────────────────────
📋 COMMITMENTS
────────────────────────────────────────

YOUR commitments:
- [ ] Figure out landing page / funnel / "makeup" for recruitment suite — TBD
- [ ] Chat tomorrow re: meetings to set up

THEIR commitments:
- [ ] Identify the ONE recruitment workflow to sell 100 times — TBD
- [ ] Complete messaging/materials for UNLEASH — TBD
- [ ] Coordinate with Accenture on finance/banking needs — TBD

⚠️ OPEN LOOPS:
- No deadline on "the ONE thing" — when does Brad decide?
- UNLEASH timeline not specified — what's the event date?

────────────────────────────────────────
💡 3 COACHING NOTES
────────────────────────────────────────

✅ WORKED: Direct challenge — "Sell me resume screening 100 times.
   That's all I care about." Clear, specific, no hedging.

⚠️ IMPROVE: You took the "makeup" work onto yourself ("I'll figure
   out the makeup part"). Push it down: "You own the positioning.
   Show me a one-pager by Thursday."

❓ ASK NEXT TIME: "What's the ONE product? Show me the plan."
   — This is your barrel test.

────────────────────────────────────────
✉️ SEND TO Brad
────────────────────────────────────────

Hey, good chat. So the play is clear — you pick the ONE
workflow we can sell 100 times. Resume screening, whatever
it is, but pick it. I'll sort the landing page and funnel
so we look the part.

Your side:
• Decide the one repeatable product
• UNLEASH messaging/materials
• Accenture — scope what finance/banking needs

Let's regroup Thursday — show me what you've got.

────────────────────────────────────────
```

---

*Micro-skill: Capture fast, coach in 3 bullets, send the message, move on.*
