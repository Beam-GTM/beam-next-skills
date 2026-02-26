---
name: 1on1-review
description: "Deep expert coaching review of a 1-on-1 meeting. Triggers: '1on1 review', 'review my 1on1 with [name]', 'coach me on my 1on1', 'how did my 1on1 go', 'deep review my 1on1', 'expert feedback on my meeting with [name]'."
---

# 1on1 Review

Deep coaching analysis of a 1-on-1 meeting using 5 expert personas. Scores your meeting, identifies patterns, and gives you specific improvement actions with rewritten examples from the actual transcript.

> **When to use**: Weekly or bi-weekly. Pick your most important 1-on-1 and get thorough coaching.
> **Time**: ~5 minutes
> **Output**: Expert reviews + score + improvement roadmap
> **Prerequisite**: Transcript in `04-workspace/ceo-office/1on1s/{person}/transcripts/`

---

## When to Use

| Use This | Not This |
|----------|----------|
| "Review my 1on1 with Saqib" | "Quick debrief" → use `1on1-followup` |
| "Coach me on my meeting" | "Just capture action items" → use `1on1-followup` |
| Weekly/bi-weekly deep dive | After every single meeting |
| Want to improve as a manager | Just need commitments list |

---

## Expert Panel

5 perspectives that cover the full spectrum of 1-on-1 excellence:

| Expert | Lens | Looks For |
|--------|------|-----------|
| **Kim Scott** | Radical Candor | Feedback quality, care vs challenge, SBI specificity, asking for feedback |
| **Andy Grove** | High Output Management | Output vs activity, OKRs, action item review, key results with deadlines |
| **Claire Hughes Johnson** | Scaling People | Development conversations, trajectory, written documentation, role clarity |
| **Frank Slootman** | Amp It Up | Urgency, directness, timeline compression, zero tolerance for vagueness |
| **Keith Rabois** | Barrels & Operations | Barrel assessment, simplification, forcing functions, ownership clarity |

---

## Workflow

### Step 1: Identify the Meeting

Same as `1on1-followup` — find or fetch the transcript.

If user says "review my 1on1 with Brad", look in:
`04-workspace/ceo-office/1on1s/brad/transcripts/` for the most recent file.

### Step 2: Load Expert Personas

Load these 5 persona files:
```
00-system/expert-personas/personas/kim-scott.md
00-system/expert-personas/personas/andy-grove.md
00-system/expert-personas/personas/claire-hughes-johnson.md
00-system/expert-personas/personas/frank-slootman.md
00-system/expert-personas/personas/keith-rabois.md
```

### Step 3: Run 5 Expert Reviews

For each persona, generate a review block:

```
═══════════════════════════════════════
{PERSONA NAME} REVIEW — {Their Domain}
═══════════════════════════════════════

VERDICT: {👍 Strong | 👌 Solid | ⚠️ Needs Work | ❌ Rethink}

CORE REACTION:
"{1-2 sentences IN THEIR VOICE — what would they actually say?}"

STRENGTHS:
• {Specific strength with transcript evidence}
• {Specific strength with transcript evidence}

GAPS:
• {Issue they'd flag} → {Concrete fix}
• {Issue they'd flag} → {Concrete fix}

ONE THING TO CHANGE:
{Their single most impactful recommendation — specific and actionable}
```

### Step 4: Summary + Score

```
════════════════════════════════════════════════════════════════
📊 EXPERT REVIEW SUMMARY
════════════════════════════════════════════════════════════════

| Expert | Verdict | Key Insight |
|--------|---------|-------------|
| Kim Scott | {emoji} | {1-line} |
| Andy Grove | {emoji} | {1-line} |
| Claire Hughes Johnson | {emoji} | {1-line} |
| Frank Slootman | {emoji} | {1-line} |
| Keith Rabois | {emoji} | {1-line} |

────────────────────────────────────────────────────────────────
🎯 TOP 5 ACTIONS (consensus)
────────────────────────────────────────────────────────────────

1. {Action} — Flagged by {Expert A, B}
2. {Action} — {Expert C} strongly recommends
3. {Action} — Consensus across {N} experts
4. {Action} — Quick win from {Expert D}
5. {Action} — {Expert E} key insight

────────────────────────────────────────────────────────────────
⭐ WHAT WOULD MAKE THIS EXCELLENT
────────────────────────────────────────────────────────────────

Current Score: {X/10} — {One-line assessment}

The Gap to Excellence:

| Aspect | What You Did | What Excellence Looks Like |
|--------|--------------|---------------------------|
| {Area} | {Current} | {Excellent} |
| {Area} | {Current} | {Excellent} |
| {Area} | {Current} | {Excellent} |

Specific Moments That Could Be Elevated:

Instead of: "{Actual quote from transcript}"
Excellence: "{Rewritten version at 9/10 level}"

Instead of: "{Actual quote}"
Excellence: "{Rewritten version}"
```

### Step 5: Save

Save to: `02-projects/Beam/10-1on1-excellence/04-outputs/{person}/{date}-coaching-review.md`

Include YAML frontmatter with date, person, experts, score, source transcript path.

---

## Scoring Guide

| Score | Meaning | What the Experts See |
|-------|---------|---------------------|
| 9-10 | Exceptional | Structured, direct, developmental, commitments with deadlines, barrel-building |
| 7-8 | Strong | Good instincts, mostly focused, minor gaps in structure or follow-through |
| 5-6 | Needs Work | Right direction but too conversational, vague commitments, no review of prior items |
| 3-4 | Weak | No structure, no accountability, all agreement, no challenge |
| 1-2 | Not a 1-on-1 | Status update disguised as meeting, no coaching or development |

---

## Pattern Detection

When reviewing, also look for patterns from PRIOR reviews (if they exist in `04-outputs/{person}/`):

- **Recurring gaps**: Does the same issue keep appearing? (e.g., "no deadline" flagged 3 times in a row)
- **Improvement trends**: Is the score going up or down?
- **Cross-person patterns**: Do the same issues show up across different people?

If prior reviews exist, add a section:

```
────────────────────────────────────────────────────────────────
📈 PATTERN WATCH
────────────────────────────────────────────────────────────────

vs. last review ({date}): Score {X} → {Y} ({+/-Z})

Recurring: {Issue that keeps appearing}
Improved: {Issue that got better}
New: {Issue appearing for the first time}
```

---

## Difference from 1on1-followup

| Aspect | `1on1-followup` | `1on1-review` |
|--------|-----------------|---------------|
| Purpose | Capture commitments | Improve as manager |
| Speed | 2 minutes | 5 minutes |
| Experts | None | 5 expert personas |
| Output | Commitments + 3 coaching notes | Full analysis + score + rewritten examples |
| When | After every 1-on-1 | Weekly/bi-weekly deep dive |
| Saves to | `1on1s/{person}/followups/` | `10-1on1-excellence/04-outputs/{person}/` |

---

## Example Usage

```
User: "review my 1on1 with Saqib"

AI: [Loads latest Saqib transcript]
    [Loads 5 expert persona files]
    [Generates full review]
    [Saves to 04-outputs/saqib/{date}-coaching-review.md]

    Shows: 5 expert reviews → summary → score → improvement roadmap
```

---

*Deep coaching through expert lenses. Score, learn, improve.*
