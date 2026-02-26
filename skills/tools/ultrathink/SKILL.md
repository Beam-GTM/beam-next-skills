---
name: ultrathink
version: '1.0'
description: Critical analysis that stress-tests content from multiple perspectives
  before shipping. Load when user says "ultrathink", "ultrathink this", "stress test
  this", "challenge this content", "validate this", "critique this from different
  angles", or provides content (email, document, strategy, proposal, paper) asking
  for critical review. Examines content through recipient POV, critic lens, devil's
  advocate, first principles, and risk analysis, then synthesizes findings into actionable
  report.
author: Quentin
category: general
tags:
- email
updated: '2025-12-12'
visibility: public
---
# Ultrathink

Stress-test any content through multi-perspective critical analysis before you ship it.

## Purpose

Ultrathink prevents costly mistakes by challenging your content from multiple angles before it goes out. Whether it's an email, strategy doc, proposal, or paper, this skill runs a rigorous self-dialogue examining assumptions, clarity, persuasiveness, and risks.

**Use when**: You've drafted something important and want to validate it's solid before sending/publishing.

**Time Estimate**: 2-5 minutes

---

## Workflow

### Step 1: Receive Content

User provides content to analyze with trigger phrase:
- "ultrathink this email"
- "stress test this proposal"
- "challenge this strategy"
- "validate this document"

Content can be:
- Emails (follow-ups, pitches, announcements)
- Documents (strategies, proposals, reports)
- Papers (research, analysis, thought pieces)
- Copy (marketing, landing pages, product descriptions)

---

### Step 2: Multi-Perspective Analysis (Internal Dialogue)

Engage in self-dialogue examining the content from **all five perspectives**. Output the dialogue visibly so the user sees the reasoning process.

Format the dialogue section clearly:

```markdown
🧠 ULTRATHINK ANALYSIS

RECIPIENT'S POV:
[Examine as if receiving this content. What would they think/feel? 
Will they read it all? Is the ask clear? Does it respect their time?]

CRITIC'S POV:
[Identify weaknesses, unclear sections, missing elements, logical gaps.
What's confusing? What assumptions are made? What's unnecessary?]

DEVIL'S ADVOCATE:
[Challenge core assumptions. What if the opposite is true?
What context is missing? What could the recipient misunderstand?]

FIRST PRINCIPLES:
[Strip away assumptions to examine fundamentals. What's the core goal?
Does this content achieve that goal? What's essential vs. noise?]

RISK ANALYSIS:
[What could go wrong? What unintended consequences? What's the downside?
How might this backfire? What vulnerabilities exist?]
```

**Guidelines for the dialogue:**

**Recipient's POV**:
- Read as if you're the target audience
- Consider their context, time constraints, priorities
- Will they skim or read deeply?
- Is the value/ask immediately clear?

**Critic's POV**:
- Identify structural weaknesses
- Spot vague language, jargon, assumptions
- Look for missing information or context
- Find logical inconsistencies

**Devil's Advocate**:
- Challenge every assumption explicitly
- Ask "what if we're wrong about X?"
- Identify gaps in reasoning
- Consider alternative interpretations

**First Principles**:
- What's the fundamental goal?
- Does the content achieve that goal directly?
- What's essential vs. decoration?
- Are we solving the right problem?

**Risk Analysis**:
- Technical risks (spam filters, broken links, etc.)
- Perception risks (seems pushy, confusing, inappropriate)
- Strategic risks (wrong timing, wrong audience, wrong message)
- Opportunity cost (better alternatives?)

---

### Step 3: Synthesize Report

After the dialogue, output a **short, actionable report** with findings and recommendations.

Format:

```markdown
────────────────────────────────────

📊 SYNTHESIS REPORT

⚠️ CRITICAL ISSUES:
• [Issue 1: specific, actionable]
• [Issue 2: specific, actionable]
• [Issue 3: specific, actionable]

💡 STRENGTHS:
• [Strength 1]
• [Strength 2]

🔧 RECOMMENDATIONS:
1. [Priority 1: specific action to fix critical issue]
2. [Priority 2: specific action to fix critical issue]
3. [Priority 3: improvement suggestion]
4. [Priority 4: improvement suggestion]

✅ SHIP WHEN: [Clear condition - e.g., "After addressing critical issues" or "Ready to ship"]
```

**Report Guidelines:**

**Critical Issues** (max 3-5):
- Issues that would significantly harm effectiveness
- Must be fixed before shipping
- Specific, not vague (bad: "unclear", good: "CTA buried in paragraph 3")

**Strengths** (max 2-3):
- What's working well that should be preserved
- Elements that are effective and shouldn't be changed
- Brief but specific

**Recommendations** (max 4-6):
- Prioritized by impact
- Specific and actionable
- Top items address critical issues
- Lower items are improvements/optimizations

**Ship When**:
- Clear gate: "After fixing X" or "Ready to ship" or "Needs major revision"

---

### Step 4: Offer Iteration

After presenting the report, offer:

"Would you like me to:
1. Apply these recommendations and revise the content?
2. Dig deeper into any specific issue?
3. Run ultrathink again after you make changes?"

Let the user decide next steps.

---

## Output Quality Standards

**Dialogue section must:**
- Show actual reasoning, not generic observations
- Reference specific parts of the content
- Challenge real assumptions (not strawmen)
- Be concise - each perspective is 2-4 sentences max

**Report must:**
- Be actionable (clear what to do)
- Be specific (reference actual content issues)
- Be concise (user should read it in 30 seconds)
- Prioritize ruthlessly (what matters most?)

**Common Pitfalls to Avoid:**
- ❌ Generic critiques that could apply to anything
- ❌ Overly long dialogue (keep each perspective brief)
- ❌ Vague recommendations ("make it clearer")
- ❌ Too many issues (focus on what matters)
- ❌ Missing the fundamental purpose/goal

---

## Perspective Question Banks

Use these questions to guide each perspective:

### Recipient's POV
- If I received this, would I read it all?
- Is the value prop clear in first 10 seconds?
- Does this respect my time?
- Is the ask/CTA obvious?
- Would I know what to do next?

### Critic's POV
- What's confusing or unclear?
- What assumptions are unstated?
- What's missing for full understanding?
- What could be cut without losing value?
- Where is the logic weak?

### Devil's Advocate
- What if our core assumption is wrong?
- What context does the recipient lack?
- How could this be misinterpreted?
- What are we taking for granted?
- What's the alternative explanation?

### First Principles
- What's the fundamental goal here?
- Does this achieve that goal?
- What's essential vs. nice-to-have?
- Are we solving the right problem?
- What would a blank-slate approach look like?

### Risk Analysis
- What could go wrong technically?
- How might this damage the relationship?
- What's the worst-case interpretation?
- What unintended consequences?
- What's the opportunity cost?

---

## Examples

### Example 1: Follow-up Email

**Input**: "ultrathink this email" + [4-paragraph follow-up email]

**Dialogue** (abbreviated):
```
RECIPIENT'S POV:
"This is 4 paragraphs. Will they read it all? The ask is buried in 
paragraph 3. If I'm skimming, I miss the CTA entirely."

CRITIC'S POV:
"Opening is generic ('Hope you're doing well'). Value prop doesn't 
appear until paragraph 2. Why should they care RIGHT NOW?"

DEVIL'S ADVOCATE:
"Assumes they remember our conversation. What if they took 10 calls 
this week? We're providing zero context refresh."

FIRST PRINCIPLES:
"Goal: Get a meeting. Does this email achieve that? It explains WHAT 
we do, not WHY they should meet. Missing the hook."

RISK ANALYSIS:
"Could land in spam (too long, multiple links). Multiple CTAs might 
confuse. References 3 different products - cognitive overload."
```

**Report**:
```
📊 SYNTHESIS REPORT

⚠️ CRITICAL ISSUES:
• CTA buried in paragraph 3 - will be missed if skimming
• Zero context refresh from last conversation
• Value prop appears too late (paragraph 2)

💡 STRENGTHS:
• Professional tone maintained
• Specific next steps provided

🔧 RECOMMENDATIONS:
1. Lead with value hook: "Quick win for [their pain point]"
2. One clear CTA at top AND bottom
3. Cut to 2 short paragraphs maximum
4. Add context anchor: "Following up on our chat about X..."

✅ SHIP WHEN: After addressing critical issues 1-3
```

### Example 2: Strategy Document

**Input**: "stress test this strategy" + [strategy proposal]

**Dialogue** (abbreviated):
```
RECIPIENT'S POV:
"This is dense - 12 pages. What's the executive summary? I need 
the decision and reasoning up front, not buried on page 8."

CRITIC'S POV:
"The strategy has three goals but they're in tension. Which is 
priority 1? Success metrics are vague ('improve engagement')."

DEVIL'S ADVOCATE:
"Assumes we have resources to execute all three initiatives 
simultaneously. What if we can only do one well? No prioritization."

FIRST PRINCIPLES:
"Goal: Align team on next quarter's focus. Does this do that? 
No - it provides options without a clear recommended path."

RISK ANALYSIS:
"Without prioritization, teams will self-interpret leading to 
misaligned execution. Resource conflicts likely. No failure modes considered."
```

**Report**:
```
📊 SYNTHESIS REPORT

⚠️ CRITICAL ISSUES:
• No executive summary - decision buried on page 8
• Three competing goals without clear prioritization
• Success metrics too vague to measure ("improve engagement")
• Missing resource requirements and trade-offs

💡 STRENGTHS:
• Thorough market analysis (pages 3-5)
• Clear competitive positioning

🔧 RECOMMENDATIONS:
1. Add 1-page executive summary with recommended path
2. Rank the three goals as P0, P1, P2 with rationale
3. Define specific success metrics (X% growth in Y metric)
4. Add resource section: what each option costs in people/time
5. Include pre-mortem: what could go wrong for each option

✅ SHIP WHEN: After adding exec summary and prioritization
```

---

## Notes

**Tone**: The dialogue should be honest and direct, but not harsh. We're helping improve content, not tearing it down.

**Adaptability**: While we analyze from all 5 perspectives by default, some may be more relevant than others depending on content type. It's fine to spend more depth on the most critical perspectives.

**Speed**: Keep the entire analysis (dialogue + report) concise. Aim for 200-400 words total. User should be able to read and act on it quickly.

**Follow-through**: Always offer to help implement the recommendations. The goal is improved content, not just critique.

---

**This is a thinking tool, not a judgment tool.** Use it to strengthen your work before it ships.
