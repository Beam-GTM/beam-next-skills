---
name: 1on1-prep
description: "Prepare for an upcoming 1-on-1. Triggers: 'prep my 1on1 with [name]', '1on1 prep', 'prepare for my meeting with [name]', 'what should I cover with [name]', 'get ready for 1on1'."
category: micro
---

# 1on1 Prep

Generate a sharp prep sheet before a 1-on-1. Pulls open commitments, unresolved loops, and patterns from prior meetings so you walk in with a plan, not an improvisation.

> **When to use**: 5-10 minutes before a 1-on-1
> **Time**: ~2 minutes
> **Output**: 1-page prep sheet with opener, accountability check, and push topics
> **Inputs**: Prior transcripts, follow-ups, coaching reviews for that person

---

## Workflow

### Step 1: Identify the Person

```
User: "prep my 1on1 with Brad"
→ Look in 04-workspace/ceo-office/1on1s/brad/
```

If no name: ask "Who's the 1-on-1 with?"

### Step 2: Load Context

Pull from these sources in order:

1. **Latest follow-up**: `04-workspace/ceo-office/1on1s/{person}/followups/` — most recent file
   - Open commitments (yours and theirs)
   - Open loops
   - "Ask next time" question

2. **Last 2-3 transcripts**: `04-workspace/ceo-office/1on1s/{person}/transcripts/` — most recent 2-3 files
   - Topics covered, tone, recurring themes
   - Promises made — were they kept?

3. **Latest coaching review** (if exists): `02-projects/Beam/10-1on1-excellence/04-outputs/{person}/`
   - Expert-flagged gaps
   - Top actions you were supposed to work on

### Step 3: Generate Prep Sheet

```
═══════════════════════════════════════
1ON1 PREP — {Person}, {Date}
═══════════════════════════════════════

Last meeting: {date} ({days} days ago) | {1-line summary}

────────────────────────────────────────
🎯 OPEN WITH
────────────────────────────────────────

"{Specific opening question — based on their biggest
open commitment from last time. Not 'how are things?'
but 'Show me X that you committed to.'}"

Why this opener: {1 sentence — what it tests or unblocks}

────────────────────────────────────────
📋 ACCOUNTABILITY CHECK
────────────────────────────────────────

THEIR open commitments (from last meeting):
- [ ] {Commitment} — status: {Unknown/Overdue/Due}
- [ ] {Commitment} — status: {Unknown/Overdue/Due}

YOUR open commitments (from last meeting):
- [ ] {Commitment} — have you done this? {Yes/No/Partial}
- [ ] {Commitment}

💀 DEAD ITEMS (committed but never followed up):
- {Item from 2+ meetings ago that was never revisited}

────────────────────────────────────────
🔥 PUSH TOPICS
────────────────────────────────────────

1. {Topic to push on} — Why: {context from transcripts}
   → Ask: "{Specific question}"

2. {Topic to push on} — Why: {context}
   → Ask: "{Specific question}"

3. {Topic to push on} — Why: {context}
   → Ask: "{Specific question}"

────────────────────────────────────────
⚡ COACHING FOCUS (for yourself)
────────────────────────────────────────

Based on your last review/follow-up, focus on:
• {One behaviour to practice in THIS meeting}

Avoid:
• {One pattern to break — from prior coaching notes}

────────────────────────────────────────
```

### Step 4: Save

Save to: `04-workspace/ceo-office/1on1s/{person}/preps/{date}-prep.md`

If the `preps/` subfolder doesn't exist, create it.

---

## Prep Sheet Guidelines

### OPEN WITH

The opener is the most important line. It sets the tone for the entire meeting.

- Always accountability-first. Lead with their biggest commitment.
- Never open with small talk or "how are things." That's how 1-on-1s become status updates.
- Good: "Last time you said you'd pick the ONE product. What is it?"
- Good: "You committed to the product strategy doc. Show me."
- Bad: "So what's new?"
- Bad: "How's the team doing?"

### ACCOUNTABILITY CHECK

- Pull ALL open commitments from the last follow-up
- Check: did YOU deliver on your commitments? Be honest. If you didn't, acknowledge it — don't just skip it.
- DEAD ITEMS are critical: things committed 2+ meetings ago that were never revisited. These are trust killers. Either close them or explicitly cancel them.

### PUSH TOPICS

- Max 3. You won't cover more in a 30-minute meeting.
- Each needs a specific question, not a topic label. "Ask about hiring" is useless. "How many candidates in pipeline for head of ops? Show me the tracker." is useful.
- Prioritize: what has the highest impact if unblocked THIS week?

### COACHING FOCUS

- Pull from the latest coaching review or follow-up notes
- ONE thing to practice, ONE thing to avoid
- This is for YOU, not for them. Private.
- Good: "Practice: set a deadline on every commitment before the call ends."
- Good: "Avoid: taking work onto yourself ('I'll figure out the makeup part')."
- Bad: "Be a better listener."

---

## How This Connects to Other Skills

```
BEFORE meeting:  1on1-prep     ← you are here
AFTER meeting:   1on1-followup ← capture commitments + coaching notes
WEEKLY/BIWEEKLY: 1on1-review   ← deep expert analysis
```

The prep skill feeds from follow-up outputs. The follow-up feeds into the next prep. The review catches patterns the cycle misses.

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐
│  PREP   │────→│   MEETING    │────→│  FOLLOW-UP  │
│ (before)│     │  (the 1on1)  │     │  (after)    │
└────▲────┘     └──────────────┘     └──────┬──────┘
     │                                       │
     └───────────────────────────────────────┘
                    feeds into

         ┌─────────────┐
         │   REVIEW    │ (weekly/biweekly deep dive)
         │ (5 experts) │
         └─────────────┘
```

---

## Example

```
User: "prep my 1on1 with Brad"

AI: [Loads brad/followups/2026-02-05-followup.md]
    [Loads last 2 brad transcripts]
    [Loads brad coaching review if exists]

═══════════════════════════════════════
1ON1 PREP — Brad, 2026-02-10
═══════════════════════════════════════

Last meeting: 2026-02-05 (5 days ago) | ONE repeatable product, makeup/funnel

────────────────────────────────────────
🎯 OPEN WITH
────────────────────────────────────────

"Last time I asked you to pick the ONE workflow we sell
100 times. What is it? Show me the plan."

Why: This was the central commitment. If he doesn't
have it, nothing else matters.

────────────────────────────────────────
📋 ACCOUNTABILITY CHECK
────────────────────────────────────────

THEIR open commitments:
- [ ] Pick the ONE repeatable product — status: Unknown
- [ ] UNLEASH messaging/materials — status: Unknown
- [ ] Accenture finance/banking scoping — status: Unknown

YOUR open commitments:
- [ ] Landing page / funnel / "makeup" — have you done this?
- [ ] Chat about meetings to set up — did this happen?

💀 DEAD ITEMS: None (first follow-up cycle)

────────────────────────────────────────
🔥 PUSH TOPICS
────────────────────────────────────────

1. The ONE product — Why: Brad agreed but didn't explicitly
   name it. He drifted to "suite" thinking multiple times.
   → Ask: "Name it. One sentence. What do we sell 100x?"

2. UNLEASH prep — Why: Event date unknown, materials unstarted
   → Ask: "When is UNLEASH? What's ready? What's not?"

3. Pipeline — Why: Brad said most prospects are "middle of
   nowhere America." NYC is covered.
   → Ask: "How many meetings this week? Show me the list."

────────────────────────────────────────
⚡ COACHING FOCUS (for yourself)
────────────────────────────────────────

Practice: End every commitment with a deadline. Don't let
"I'll do it" fly without "by when?"

Avoid: Taking work onto yourself. Last time you said
"I'll figure out the makeup part." Push it down.

────────────────────────────────────────
```

---

*Micro-skill: Walk in with a plan. Open with accountability. Push on 3 things. Get out.*
