---
name: expert-review
description: "Quick expert feedback on any work. Load when user says: 'expert review', 'what do experts think', 'get feedback', 'review this', 'is this good?', 'what's wrong with this?'"
---

# Expert Review

Get quick, directional feedback from expert perspectives. Single pass, no iteration — just insights.

## When to Use

| Use This | Not This |
|----------|----------|
| "What do experts think?" | "Make this better" → use `expert-improve` |
| "Is this on the right track?" | "Polish until ready" → use `expert-improve` |
| "Give me rough feedback" | "Iterate until 7+/10" → use `expert-improve` |
| Early drafts, sanity checks | Final deliverables |

---

## Quick Start

**User says**: "review my LinkedIn post" / "expert feedback on this strategy"

**AI does** (auto-run, no questions):
1. Detect work type
2. Select top 3 personas
3. Run reviews
4. Show summary with actionable insights

**User only confirms**: Which personas to use (or accepts default)

---

## Execution Flow

### Step 1: Receive & Detect (Auto)

When user provides content:

```
Got it. Let me get expert perspectives on this.

📋 Detected: [CONTENT TYPE] (e.g., LinkedIn post, GTM strategy, execution plan)

Recommended reviewers:
1. **[Persona 1]** — [Domain] | [1-line famous for]
2. **[Persona 2]** — [Domain] | [1-line famous for]  
3. **[Persona 3]** — [Domain] | [1-line famous for]

Running with these 3? (Enter = yes, or type numbers to change)
```

**Auto-detection rules**:

| Signals | Type | Default Personas |
|---------|------|------------------|
| LinkedIn, post, article | `content` | Justin Welsh, Ethan Mollick, Geoffrey Moore |
| GTM, strategy, positioning | `strategy` | Geoffrey Moore, Sequoia, Aaron Ross |
| Action items, OKRs, roadmap | `execution` | Andy Grove, Keith Rabois, Claire Hughes Johnson |
| Sales, outreach, pipeline | `sales` | Aaron Ross, Geoffrey Moore, Patrick Campbell |
| Pricing, packaging | `pricing` | Patrick Campbell, Geoffrey Moore, Sequoia |
| Product, PRD, features | `product` | Dan Horowitz, Nikita Bier, Geoffrey Moore |
| Hiring, org design, team | `hiring` | Claire Hughes Johnson, Keith Rabois |
| Operations, process, workflow | `operations` | Goldratt, Deming, Keith Rabois |

### Step 2: Run Reviews (Auto)

For each persona, load their file and generate review:

```
═══════════════════════════════════════
[PERSONA NAME] REVIEW
═══════════════════════════════════════

VERDICT: [👍 Strong | 👌 Solid | ⚠️ Needs Work | ❌ Rethink]

CORE REACTION:
"[1-2 sentences in their voice]"

STRENGTHS:
• [What works from their framework]
• [What works from their framework]

GAPS:
• [Issue they'd flag] → [Quick fix]
• [Issue they'd flag] → [Quick fix]

ONE THING TO CHANGE:
[Their single most important recommendation]
```

### Step 3: Summary (Auto)

After all reviews:

```
════════════════════════════════════════════════════════════════
📊 EXPERT REVIEW SUMMARY
════════════════════════════════════════════════════════════════

| Expert | Verdict | Key Insight |
|--------|---------|-------------|
| [Name] | 👍/👌/⚠️/❌ | [1-line summary] |
| [Name] | 👍/👌/⚠️/❌ | [1-line summary] |
| [Name] | 👍/👌/⚠️/❌ | [1-line summary] |

────────────────────────────────────────────────────────────────
🎯 TOP 3 ACTIONS (consensus)
────────────────────────────────────────────────────────────────

1. [Action] — Flagged by [Persona A, B]
2. [Action] — [Persona C] strongly recommends
3. [Action] — Quick win from [Persona D]

────────────────────────────────────────────────────────────────
⭐ WHAT WOULD MAKE THIS EXCELLENT
────────────────────────────────────────────────────────────────

**Current Score: [X/10]** — [One-line assessment]

**The Gap to Excellence:**

| Aspect | What You Did | What Excellence Looks Like |
|--------|--------------|---------------------------|
| [Area 1] | [Current approach] | [Excellent approach] |
| [Area 2] | [Current approach] | [Excellent approach] |
| [Area 3] | [Current approach] | [Excellent approach] |

**Specific Phrases/Actions That Would Elevate:**

Instead of: "[What was said/done]"
Excellence: "[What would be said/done at 9/10 level]"

Instead of: "[What was said/done]"
Excellence: "[What would be said/done at 9/10 level]"

**The Excellence Framework for [Content Type]:**
- [Principle 1 that defines excellence in this domain]
- [Principle 2 that defines excellence in this domain]
- [Principle 3 that defines excellence in this domain]

────────────────────────────────────────────────────────────────

Want me to apply these improvements? Say "improve this" or use `expert-improve` for iterative refinement.
```

---

## Verdict Scale

| Verdict | Meaning | Typical Action |
|---------|---------|----------------|
| 👍 **Strong** | Expert would endorse this | Ship it, minor polish optional |
| 👌 **Solid** | Good foundation, minor gaps | Apply quick fixes |
| ⚠️ **Needs Work** | Right direction, significant gaps | Use `expert-improve` for iteration |
| ❌ **Rethink** | Fundamental issues | Reconsider approach |

---

## Available Personas (12+)

### B2B Enterprise
- **Geoffrey Moore** — Crossing the chasm, beachhead strategy
- **Aaron Ross** — Predictable revenue, sales process
- **Patrick Campbell** — Value-based pricing, SaaS economics

### Operations & Leadership
- **Andy Grove** — High output management, OKRs, metrics
- **Keith Rabois** — How to operate, barrels vs ammunition
- **Claire Hughes Johnson** — Scaling people, org design

### Process Optimization
- **Eliyahu Goldratt** — Theory of constraints, bottlenecks
- **W. Edwards Deming** — Quality management, continuous improvement

### Content & Influence
- **Justin Welsh** — LinkedIn virality, personal brand
- **Ethan Mollick** — AI thought leadership, research-backed

### Product & Growth
- **Nikita Bier** — B2C virality, network effects
- **Dan Horowitz** — Product strategy, scaling

### Other
- **Sequoia Partners** — VC perspective, market timing
- **Elon Musk** — First principles, systems engineering
- **Esther Perel** — Relationship dynamics, communication

---

## Examples

### Quick Content Review

```
User: "review my LinkedIn post about AI automation"

AI: Got it. Let me get expert perspectives.

📋 Detected: CONTENT (LinkedIn post)

Recommended reviewers:
1. **Justin Welsh** — LinkedIn Virality | Built $5M+ solo creator business
2. **Ethan Mollick** — AI Thought Leadership | Wharton professor, research-backed
3. **Geoffrey Moore** — B2B Positioning | Crossing the Chasm author

Running with these 3? (Enter = yes)

[User presses Enter]

═══════════════════════════════════════
JUSTIN WELSH REVIEW
═══════════════════════════════════════

VERDICT: ⚠️ Needs Work

CORE REACTION:
"Good substance but the hook won't stop the scroll. You're burying the lead."

STRENGTHS:
• Specific example (Porsche case study) — builds credibility
• Teaching format with clear takeaway

GAPS:
• Hook is too generic ("I want to share...") → Start with the result
• No clear CTA → Add specific ask at end

ONE THING TO CHANGE:
Rewrite first line: "Porsche processed 1,247 invoices last month. Zero errors. Zero humans."

[... more reviews ...]

📊 EXPERT REVIEW SUMMARY

| Expert | Verdict | Key Insight |
|--------|---------|-------------|
| Justin Welsh | ⚠️ Needs Work | Hook doesn't stop scroll |
| Ethan Mollick | 👌 Solid | Good data, needs sharper frame |
| Geoffrey Moore | 👌 Solid | Clear problem, audience could be narrower |

🎯 TOP 3 ACTIONS

1. Rewrite hook with surprising result — Flagged by Welsh, Mollick
2. Add specific CTA — Welsh recommends
3. Narrow audience signal — Moore suggests

⭐ WHAT WOULD MAKE THIS EXCELLENT

**Current Score: 6/10** — Good substance, weak packaging

**The Gap to Excellence:**

| Aspect | What You Did | What Excellence Looks Like |
|--------|--------------|---------------------------|
| Hook | Generic opener ("I want to share...") | Lead with surprising result or tension |
| Specificity | General AI automation benefits | Name, number, timeframe ("Porsche, 1,247 invoices, zero errors") |
| CTA | No clear next step | Specific ask that matches reader intent |

**Specific Phrases That Would Elevate:**

Instead of: "I want to share how we're using AI for automation"
Excellence: "Porsche processed 1,247 invoices last month. Zero errors. Zero humans. Here's how."

Instead of: [No CTA]
Excellence: "DM me 'INVOICE' if you want the playbook we used."

**The Excellence Framework for LinkedIn Posts:**
- First line must stop the scroll (surprising stat, counterintuitive claim, or tension)
- One concrete example beats three abstract benefits
- Clear CTA that matches the content and reader's likely intent

Want me to apply these? Say "improve this"
```

---

## Difference from `expert-improve`

| Aspect | `expert-review` | `expert-improve` |
|--------|-----------------|------------------|
| Purpose | Get feedback | Actually improve |
| Passes | 1 | 2-3 until 7+/10 |
| Output | Insights + actions | Improved version |
| Speed | Fast (~1 min) | Thorough (~5 min) |
| When | Early drafts, sanity checks | Final deliverables |

---

## Integration

**After review, user can**:
- "Improve this" → Hand off to `expert-improve` with context
- Apply fixes manually
- Get a second opinion ("add April Dunford")
- Done (just wanted feedback)

---

*Single pass. Quick insights. Actionable summary.*
