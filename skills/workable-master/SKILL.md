---
name: workable-master
description: All Workable ATS operations — fetch JDs, search candidates, post assessments/reviews. Load when user says "fetch JD", "search workable", "push to workable", "post review", "rate candidate", "workable", "push assessment", "list jobs", or after interview-coach completes an evaluation. Replaces workable-fetch-jd and workable-push-assessment.
version: 2.0
---

# Workable Master

*Single skill for all Workable ATS operations — JDs, candidates, assessments, and reviews.*

> **When to use**: Any Workable interaction — fetching JDs before interviews, searching candidates, posting assessments/reviews after evaluation.
>
> **Prerequisites**:
> - `WORKABLE_API_KEY` in `.env`
> - `WORKABLE_SUBDOMAIN` in `.env`
>
> **Output**: JD data, candidate info, or confirmation of posted assessment/review

---

## Setup (One-Time)

Add these to your `.env` file:

```
WORKABLE_API_KEY=your_api_key_here
WORKABLE_SUBDOMAIN=your_subdomain
```

**Get your API key**: Workable → Settings → Integrations → Apps → Generate API token
**Your subdomain**: The part before `.workable.com` (e.g., `joinbeam`)

---

## Operations

### 1. Fetch Job Description

```bash
# By title search
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd "Product Manager"

# By shortcode
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd-code 435CFC6C38

# JSON output (for programmatic use)
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd "Product Manager" --json
```

Returns: title, department, location, full description, requirements, benefits.

### 2. Search Candidates

```bash
# Global search
python3 03-skills/workable-master/scripts/workable_client.py --search "Sarah"

# Within a specific job
python3 03-skills/workable-master/scripts/workable_client.py --find-candidate-in-job 435CFC6C38 --candidate "Sarah"
```

### 3. Post Assessment (Comment)

```bash
# By name
python3 03-skills/workable-master/scripts/workable_client.py \
  --candidate "Sarah Chen" --assessment "Assessment text..."

# From file
python3 03-skills/workable-master/scripts/workable_client.py \
  --candidate "Sarah Chen" --file path/to/assessment.md

# By candidate ID
python3 03-skills/workable-master/scripts/workable_client.py \
  --candidate-id abc123 --assessment "Assessment text..."
```

### 4. Post Review (Formal Evaluation with Grade)

```bash
python3 03-skills/workable-master/scripts/workable_client.py \
  --candidate "Sarah Chen" \
  --review --grade 2 \
  --assessment "Full review text..."
```

Grade scale: `0` = No (thumbs down), `1` = Maybe (neutral), `2` = Yes (thumbs up)

**Note**: Only one review per member per candidate stage is allowed. Delete existing reviews from the Workable UI before re-posting.

### 5. List Open Jobs

```bash
python3 03-skills/workable-master/scripts/workable_client.py --list-jobs
```

---

## Review Template (Standard Output)

After an interview evaluation, the review pushed to Workable should follow this template. This is the standard format for all candidate reviews.

### Structure

```
CEO Interview Assessment — [Candidate Name] ([Role])
Date: [Date] | Stage: [Stage] | Duration: ~[X] min

━━━ EXPERT PANEL ASSESSMENT ━━━

[Expert 1 Name] ([Domain]) — X/10
• Strong: [observation with evidence]
• Strong: [observation with evidence]
• Concern: [observation with evidence]
• Concern: [observation with evidence]

[Expert 2 Name] ([Domain]) — X/10
• Strong: [observation with evidence]
• Strong: [observation with evidence]
• Concern: [observation with evidence]
• Concern: [observation with evidence]

[Expert 3 Name] ([Domain]) — X/10
• Strong: [observation with evidence]
• Strong: [observation with evidence]
• Concern: [observation with evidence]
• Concern: [observation with evidence]

━━━ BARREL SCORING (Keith Rabois Framework) ━━━

• Ownership Language (25%): X/10
• Specificity (25%): X/10
• Failure Stories (15%): X/10 — [brief note]
• Speed Instinct (20%): X/10 — [brief note]
• Hard Decisions (15%): X/10 — [brief note]

BARREL SCORE: X.X/10 → [BARREL / POTENTIAL BARREL / AMMUNITION / PASS]
[1-2 sentence barrel summary — what type of operator is this person?]

━━━ CANDIDATE SCORECARD ━━━

• Role-Specific Expertise: X/10 — [what was assessed: e.g. product thinking, sales methodology, ops systems]
• Execution Track Record: X/10
• Problem Solving: X/10
• AI Nativeness: X/10 — [how deeply do they use/build with AI today?]
• Communication: X/10
• Leadership / People: X/10
• Cultural Fit: X/10

Overall: X.X/10

━━━ INTERVIEW QUALITY ━━━

• Questions matched JD: [Yes/Partially/No] — [brief note]
• Failure probing: [Strong/Adequate/Weak] — [brief note]
• Case question quality: [Strong/Adequate/Weak] — [brief note]
• Time management: [Good/Okay/Poor] — [brief note]

━━━ RECOMMENDATION ━━━

[STRONG YES / YES / PROCEED WITH CAUTION / NO]
[2-4 sentence recommendation with clear next steps and comparison context.]
```

---

## Expert Selection by Role

The 3 experts are selected based on the role being hired for. Always include perspectives that cover: (a) domain expertise, (b) operational/scaling lens, (c) people/culture lens.

| Role Category | Expert 1 (Domain) | Expert 2 (Ops/Scaling) | Expert 3 (People/Culture) |
|--------------|-------------------|----------------------|--------------------------|
| **Product** | Marty Cagan | Shreyas Doshi | Claire Hughes Johnson |
| **Engineering** | Will Larson | Camille Fournier | Keith Rabois |
| **Sales** | Mark Roberge | Jacco van der Kooij | Claire Hughes Johnson |
| **Marketing** | Emily Kramer | April Dunford | Seth Godin |
| **Operations** | Keith Rabois | Frank Slootman | Andy Grove |
| **Design/UX** | Julie Zhuo | Don Norman | Steve Jobs |
| **AI/ML** | Andrew Ng | Andrej Karpathy | Cassie Kozyrkov |
| **Customer Success** | Lincoln Murphy | Elena Verna | Claire Hughes Johnson |
| **Executive/C-Suite** | Ben Horowitz | Keith Rabois | Claire Hughes Johnson |
| **SDR/BDR** | Aaron Ross | Meka Asonye | Mark Roberge |
| **Finance** | Charlie Munger | Ray Dalio | Warren Buffett |
| **General/Other** | Keith Rabois | Claire Hughes Johnson | Andy Grove |

**Override**: If a specific domain expert is more relevant (e.g., hiring for a PLG role → swap in Elena Verna), adapt the panel. The table is a starting point, not a constraint.

**Barrel scoring** (Keith Rabois framework) is **always included** regardless of role — it evaluates the universal ability to ship independently.

---

## Grading to Workable Rating

Map the expert consensus + barrel score to the Workable thumbs scale:

| Expert Consensus | Barrel Score | Workable Grade | Meaning |
|-----------------|-------------|---------------|---------|
| Majority "Strong Hire" or "Hire" | 7.0+ | `2` (Yes) | Advance — strong candidate |
| Mixed / "Lean Hire" | 5.0 - 6.9 | `1` (Maybe) | Needs more signal — next round or debrief |
| Majority "No Hire" or "Lean No" | Below 5.0 | `0` (No) | Do not advance |

---

## End-to-End Workflow

```
User: "review my interview with Sarah"

→ AI fetches transcript (Amie or Fathom)
→ AI: "What role was this for?"
→ User: "Product Manager"
→ AI fetches JD: workable_client.py --fetch-jd "Product Manager"
→ AI selects expert panel: Marty Cagan, Shreyas Doshi, Claire Hughes Johnson
→ AI runs expert assessments + barrel scoring
→ AI generates review in standard template
→ AI: "Push this to Sarah's Workable profile? (Grade: Yes/Maybe/No)"
→ User: "yes"
→ AI runs: workable_client.py --candidate "Sarah" --review --grade 2 --assessment "..."
→ "Review posted to Sarah's Workable profile."
```

---

## Triggers

| User Says | Action |
|-----------|--------|
| "fetch JD for [role]" | Run `--fetch-jd` |
| "search workable for [name]" | Run `--search` |
| "push to workable" | Post last evaluation as review |
| "push assessment to workable" | Post as comment |
| "post review for [name]" | Post as review with grade |
| "list jobs" / "open positions" | Run `--list-jobs` |
| After interview-coach completes | Offer to push automatically |

---

## Integration

**Connected skills**:
| Skill | Relationship |
|-------|-------------|
| `interview-coach` | Produces evaluations → pushes via this skill |
| `candidate-compare` | Produces comparisons → pushes via this skill |
| Amie / Fathom skills | Provides transcripts for evaluation |

**Replaces**: `workable-fetch-jd` (never created), `workable-push-assessment` (merged)

---

**Version**: 2.0 | **Created**: 2026-02-16

**Changelog**:
- v2.0: Unified skill combining JD fetching, candidate search, assessments, and reviews. Added standard review template with expert panel selection, barrel scoring, and grading matrix.
- v1.0: Initial push assessment skill (as `workable-push-assessment`)
