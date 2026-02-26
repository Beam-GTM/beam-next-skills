---
name: candidate-compare
version: 1.0
description: Compare multiple candidates for a role and recommend the best fit. Load
  when user says "compare candidates", "select best candidate", "who should we hire",
  "compare [names] for [role]", "rank candidates", or "best candidate for [role]".
author: Manahil Shaikh
category: general
updated: '2026-02-16'
visibility: public
---
# Candidate Compare

*Data-driven candidate selection based on interview performance.*

> **When to use**: After interviewing multiple candidates for the same role, compare them objectively
>
> **Prerequisites**:
> - `fathom-fetch-meetings` or Amie — Get interview transcripts
> - `workable-master` — Pull job description + push results to Workable
>
> **Output**: Ranked candidates with scores, strengths/gaps analysis, hiring recommendation

---

## Workflow

### Step 1: Parse Input

**Expected format**:
```
User: "compare Sarah, John, Ahmed for Product Manager"
```

Extract:
- Candidate names: `["Sarah", "John", "Ahmed"]`
- Role: `Product Manager`

**Alternative triggers**:
- "select best candidate for [role]" → ask for names
- "who should we hire for [role]" → ask for names
- "rank candidates" → ask for role and names

### Step 2: Fetch Job Description

```bash
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd "[role]"
```

Extract key requirements from JD:
- Required experience (years, type)
- Technical skills
- Soft skills
- Nice-to-haves

### Step 3: Fetch Transcripts

For each candidate, search Fathom:

```bash
# Search for meetings containing candidate name
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?include_summary=true&include_transcript=true' \
  --header 'X-Api-Key: {FATHOM_API_KEY}' \
  | jq '.items[] | select(.title | ascii_downcase | contains("{candidate_name}"))'
```

If multiple meetings found for a candidate, pick the most recent or ask user to select.

**Fallback**: If Fathom unavailable, ask user to paste transcripts.

### Step 4: Evaluate Each Candidate

Score each candidate on JD requirements:

| Dimension | Weight | What to Look For |
|-----------|--------|------------------|
| **Experience Match** | 25% | Years, industry, relevant projects |
| **Technical Skills** | 25% | Demonstrated competency in required skills |
| **Problem Solving** | 20% | How they approached challenges, structured thinking |
| **Communication** | 15% | Clarity, conciseness, ability to explain complex ideas |
| **Culture Fit** | 15% | Values alignment, work style, collaboration signals |

**Scoring**: 1-5 scale per dimension
- 5: Exceeds requirements
- 4: Meets requirements strongly
- 3: Meets requirements adequately
- 2: Partially meets requirements
- 1: Does not meet requirements

### Step 5: Compare & Rank

Calculate weighted score for each candidate:
```
Total = (Experience × 0.25) + (Technical × 0.25) + (Problem Solving × 0.20) + (Communication × 0.15) + (Culture × 0.15)
```

Rank candidates by total score.

---

## Output Format

```
# Candidate Comparison: [Role]

## Summary

| Rank | Candidate | Score | Recommendation |
|------|-----------|-------|----------------|
| 1 | [Name] | X.X/5 | **Hire** |
| 2 | [Name] | X.X/5 | Strong backup |
| 3 | [Name] | X.X/5 | Pass |

---

## Detailed Analysis

### 1. [Top Candidate Name] — X.X/5 ⭐ Recommended

**Scores**:
| Dimension | Score | Notes |
|-----------|-------|-------|
| Experience Match | /5 | [brief note] |
| Technical Skills | /5 | [brief note] |
| Problem Solving | /5 | [brief note] |
| Communication | /5 | [brief note] |
| Culture Fit | /5 | [brief note] |

**Strengths**:
- [Strength 1 with evidence from transcript]
- [Strength 2 with evidence]

**Gaps/Risks**:
- [Gap 1 — and how to mitigate]

**Key Quote**:
> "[memorable quote from interview]"

---

### 2. [Second Candidate Name] — X.X/5

[Same format]

---

### 3. [Third Candidate Name] — X.X/5

[Same format]

---

## Recommendation

**Hire**: [Name]

**Rationale**: [2-3 sentences on why this candidate stands out]

**Next Steps**:
- [ ] [Action item 1]
- [ ] [Action item 2]

---

## Comparison Matrix

| Requirement (from JD) | [Candidate 1] | [Candidate 2] | [Candidate 3] |
|-----------------------|---------------|---------------|---------------|
| [Req 1] | ✅ Strong | ⚠️ Partial | ❌ Gap |
| [Req 2] | ✅ Strong | ✅ Strong | ⚠️ Partial |
| [Req 3] | ⚠️ Partial | ✅ Strong | ✅ Strong |
```

---

## Triggers

| User Says | Action |
|-----------|--------|
| "compare [name1], [name2], [name3] for [role]" | Full workflow |
| "compare candidates for [role]" | Ask for candidate names |
| "select best candidate" | Ask for role and names |
| "who should we hire for [role]" | Ask for names |
| "rank candidates for [role]" | Ask for names |
| "best candidate for [role]" | Ask for names |

---

## Integration

**Connected skills**:
| Skill | Purpose |
|-------|---------|
| `fathom-fetch-meetings` | Get interview transcripts by candidate name |
| Amie notes/transcripts | Get interview transcripts (Amie) |
| `workable-master` | Fetch JD + push results to Workable |

**Example Flow**:
```
Manager: "compare Sarah Chen, John Smith, Ahmed Hassan for Product Manager"
→ AI fetches Product Manager JD from Workable
→ AI searches Fathom for "Sarah Chen", "John Smith", "Ahmed Hassan"
→ AI evaluates each against JD requirements
→ AI outputs ranked comparison with recommendation
```

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Candidate not found in Fathom | Ask user to paste transcript or skip candidate |
| Multiple meetings for same candidate | Use most recent, or ask user to select |
| JD not found in Workable | Ask user to paste JD or describe role requirements |
| Only 2 candidates | Run comparison with 2 |
| Tie in scores | Break tie with qualitative analysis, highlight trade-offs |

---

## Bias Mitigation

- Evaluate all candidates against the **same criteria** (JD requirements)
- Use **specific evidence** from transcripts, not impressions
- Flag when a dimension lacks data: "Insufficient evidence to score"
- Present **trade-offs**, not just a winner

---

**Version**: 1.0 | **Created**: 2026-02-06

**Changelog**:
- v1.0: Initial creation — compare up to 5 candidates, weighted scoring, JD-based evaluation
