---
name: analyze-competitors
version: '1.0'
description: Conduct competitor analysis for product design. Load when user says 'analyze
  competitors', 'competitor research', 'competitive analysis', 'check how [competitor]
  does this'. Guides exploration of Zapier, n8n, Lindy, Relevance.ai and other automation
  platforms.
author: Mahnoor Jawed
category: general
tags:
- api
- automation
updated: '2026-02-24'
visibility: team
---
# Analyze Competitors

Systematically research competitor products to identify feature implementations, UX patterns, gaps, and opportunities.

## Purpose

This skill is the second step in the design cycle. It:
- Guides exploration of competitor products (Zapier, n8n, Lindy, Relevance.ai, etc.)
- Documents feature implementations and UX patterns
- Identifies gaps and opportunities for differentiation
- Creates a structured analysis for wireframing reference

---

## Workflow

### Step 1: Initialize TodoWrite

```
- [ ] Load requirements from previous step
- [ ] Identify relevant competitors for this feature
- [ ] Research each competitor (hands-on exploration)
- [ ] Document findings per competitor
- [ ] Identify patterns, gaps, opportunities
- [ ] Create analysis summary
```

---

### Step 2: Load Context

Load the requirements synthesis from Step 1:
```
02-resources/requirements-synthesis.md
```

Identify the core feature/functionality to research.

**Mark this todo complete before proceeding.**

---

### Step 3: Select Competitors

Present the known competitor list from [references/competitor-list.md](references/competitor-list.md):

```
Which competitors should we analyze for this feature?

Automation Platforms:
1. Zapier
2. n8n
3. Make (Integromat)

AI Agent Platforms:
4. Lindy
5. Relevance.ai
6. Crew.ai

Other:
7. Custom competitor (specify)

Select by number (e.g., "1, 2, 4") or "all"
```

**Mark this todo complete before proceeding.**

---

### Step 4: Research Each Competitor

For each selected competitor, guide the user through exploration:

```
Let's analyze {COMPETITOR}.

Please navigate to {competitor URL} and explore how they implement {feature}.

When ready, describe what you see or share a screenshot. I'll help document:
- How they approach this feature
- Key UI elements and patterns
- User flow steps
- What works well / what doesn't
```

**Documentation template per competitor:**
```markdown
## {Competitor Name}

### Feature Implementation
- How it works: {description}
- Entry point: {where users access it}
- Key steps: {1, 2, 3...}

### UI Patterns
- Layout: {sidebar, modal, wizard, etc.}
- Components used: {buttons, cards, inputs}
- Visual style: {minimal, feature-rich, etc.}

### Strengths
- {what they do well}

### Weaknesses
- {pain points or gaps}

### Screenshots/Notes
- {user observations}
```

Repeat for each competitor.

**Mark this todo complete after ALL competitors are researched.**

---

### Step 5: Identify Patterns & Opportunities

Analyze findings across all competitors:

**Common Patterns** (most competitors do this):
- {pattern 1}
- {pattern 2}

**Differentiators** (unique approaches):
- {competitor}: {unique approach}

**Gaps** (nobody does this well):
- {gap 1}
- {gap 2}

**Opportunities** (how we can be better):
- {opportunity 1}
- {opportunity 2}

**Mark this todo complete before proceeding.**

---

### Step 6: Create Analysis Summary

Generate the final analysis document:

```markdown
# Competitor Analysis: {Feature Name}

## Executive Summary
{2-3 sentence overview of findings}

## Competitors Analyzed
| Competitor | Focus Area | Account Type |
|------------|------------|--------------|
| Zapier | {area} | Free/Premium |
| ... | ... | ... |

## Feature Comparison Matrix
| Capability | Zapier | n8n | Lindy | Ours |
|------------|--------|-----|-------|------|
| {cap 1} | Yes | Yes | No | TBD |
| ... | ... | ... | ... | ... |

## Key Findings

### What Works Well (Industry Standard)
{patterns to adopt}

### Gaps & Opportunities
{where we can differentiate}

### Recommended Approach
{synthesis for wireframing}

## Detailed Analysis
{per-competitor sections}

## References
- Screenshots: {location}
- Research date: {date}
```

Save to: `02-resources/competitor-analysis.md`

**Mark this todo complete before proceeding.**

---

### Step 7: Proceed to Wireframing

```
Competitor analysis complete!

Key insights:
- {insight 1}
- {insight 2}
- {insight 3}

Ready to create wireframes?
Say 'create wireframe' or 'continue design cycle'
```

---

## Resources

### references/
- `competitor-list.md` - Known competitors with URLs and account status
- `analysis-framework.md` - What to look for when analyzing
- `documentation-template.md` - Standard format for capturing findings

### assets/
- `competitor-analysis-template.md` - Full template for analysis output

---

## Notes

**About Account Access:**
- Free accounts are sufficient for most feature exploration
- Premium accounts may be needed for advanced features
- User should indicate which account type they're using

**About Screenshots:**
- Encourage capturing key screens for reference
- Store in project assets folder
- Reference in analysis document
