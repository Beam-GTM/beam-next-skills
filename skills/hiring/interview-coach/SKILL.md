---
name: interview-coach
description: Analyze interview transcripts to help managers improve their interviewing skills. Load when user says "review my interview with [name]", "assess my interview", "how's the candidate", "interview feedback", "interview coach", "hr round review with [name]", "technical round review with [name]", "final round review with [name]", or provides an interview transcript. Supports 3 interview types - HR (cultural fit), Technical (skill assessment), Final (career aspirations).
version: 2.0
---

# Interview Coach

*Honest feedback to help you become a better interviewer.*

> **When to use**: After conducting an interview, get your transcript analyzed for actionable feedback
>
> **Prerequisites**:
> - `fathom-fetch-meetings` or Amie — Get interview transcript
> - `workable-master` — Pull job description + push review to Workable
>
> **Output**: Expert panel assessment, barrel score, Workable review

---

## Purpose

Help hiring managers become better interviewers through structured, evidence-based feedback. Instead of relying on gut feelings or informal peer reviews, this skill analyzes actual interview transcripts against the job description to identify specific patterns — what's working, what's missing, and how to improve. The goal is consistent, fair interviews that assess candidates accurately while creating a positive candidate experience.

---

## Workflow

### Step 1: Get the Transcript

**Option A — By candidate name** (recommended):
```
User: "review my interview with Sarah"
→ AI searches Fathom for meetings with "Sarah" in title
→ If multiple matches, shows list to pick from
→ Fetches transcript automatically
```

**Option B — Manual fetch**:
```
User: "fetch meetings from fathom"
→ Lists recent meetings
→ User selects one
→ Then says "review my interview"
```

**Fathom search by name**:
```bash
# Fetch recent meetings, filter by title containing candidate name
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?include_summary=true&created_after={30_DAYS_AGO}' \
  --header 'X-Api-Key: {FATHOM_API_KEY}' \
  | jq '.meetings[] | select(.title | ascii_downcase | contains("{candidate_name}"))'
```

**Link to prerequisite skill**: `fathom-fetch-meetings` fetches meetings filtered by attendee domain, returns transcripts.

### Step 2: Get the Job Description

Once transcript is available, fetch the JD from Workable:

**Ask**: "What role was this interview for?"

**Then run**:
```bash
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd "[role title]"
```

If multiple matches, show options and ask for shortcode:
```bash
python3 03-skills/workable-master/scripts/workable_client.py --fetch-jd-code [shortcode]
```

**Link to skill**: `workable-master` handles all Workable operations.

### Step 3: Interview Stage (REQUIRED)

**Ask**: "What type of interview was this?"

| Type | When to Use |
|------|-------------|
| `hr` | HR/Cultural round — soft skills, culture fit, resume validation |
| `technical` | Technical/Case Study round — in-depth skill assessment, problem solving |
| `final` | Final round — career aspirations, team fit, leadership potential |

**Triggers can specify type directly**:
```
"hr round review with Sarah"
"technical round review with John"
"final round review with Ahmed"
```

---

## Evaluation Frameworks

**Each interview type has its own evaluation criteria.** The framework ensures you're assessing what matters for that stage.

---

### 🟢 HR Round Framework

*Focus: Cultural fit, soft skills, resume-personality alignment*

| Dimension | Weight | What to Assess |
|-----------|--------|----------------|
| **Cultural Fit** | 25% | Values alignment, work style, company culture match |
| **Resume-Personality Match** | 20% | Does their presence match their paper claims? Authenticity check |
| **Soft Skills** | 20% | Communication clarity, adaptability, emotional intelligence |
| **Motivation & Fit** | 15% | Why this company? Career trajectory alignment |
| **Red Flag Detection** | 10% | Inconsistencies, concerning patterns, gaps explained |
| **Candidate Experience** | 10% | Did you create a positive first impression? |

**Key Questions for HR Round**:
- "What kind of work environment brings out your best?"
- "Tell me about a time you disagreed with a colleague"
- "What attracted you to this role specifically?"
- "Walk me through your career journey"
- "How do you handle feedback?"

**Red Flags to Probe**:
- Badmouthing previous employers
- Unexplained gaps or frequent job changes
- Vague answers about leaving previous roles
- Mismatches between resume claims and conversation

---

### 🔵 Technical/Case Study Round Framework

*Focus: Deep skill assessment, problem-solving ability, technical communication*

| Dimension | Weight | What to Assess |
|-----------|--------|----------------|
| **Technical Depth** | 25% | Did you probe actual skills at required depth? |
| **Problem-Solving Approach** | 25% | Did you assess methodology, not just answers? |
| **Skill Validation** | 20% | Did questions match JD requirements? Evidence-based assessment |
| **Technical Communication** | 15% | Can they explain complex concepts clearly? |
| **Real-World Application** | 10% | Did you test practical knowledge, not just theory? |
| **Assessment Fairness** | 5% | Equal opportunity to demonstrate, hints when stuck |

**Key Questions for Technical Round**:
- "Walk me through how you'd approach [specific problem]"
- "What's the trade-off between X and Y approach?"
- "Tell me about a technical challenge you solved recently"
- "How would you debug [scenario]?"
- "Explain [concept] to a non-technical stakeholder"

**Case Study Best Practices**:
- Give candidate time to think (don't rush)
- Probe reasoning, not just final answer
- Ask "what would you do differently?"
- Test both breadth and depth

---

### 🟣 Final Round Framework

*Focus: Career aspirations, team fit, leadership potential, mutual evaluation*

| Dimension | Weight | What to Assess |
|-----------|--------|----------------|
| **Career Aspirations Alignment** | 25% | Does their growth path match what you can offer? |
| **Team Fit** | 25% | How will they mesh with existing team dynamics? |
| **Leadership Potential** | 20% | Strategic thinking, influence, decision-making maturity |
| **Long-term Commitment Signals** | 15% | Are they building a career or just taking a job? |
| **Mutual Fit Exploration** | 10% | Did you honestly discuss role realities? Two-way evaluation |
| **Closing Effectiveness** | 5% | Did you sell the opportunity and address concerns? |

**Key Questions for Final Round**:
- "Where do you see yourself in 3 years?"
- "What would make you turn down this offer?"
- "How do you like to be managed?"
- "Tell me about a time you influenced without authority"
- "What questions do you have for me about the team?"

**Final Round Focus**:
- This is about mutual fit, not skills (already validated)
- Be honest about challenges and expectations
- Assess culture add, not just culture fit
- Leave time for their deep questions

---

## General Evaluation Framework

*For interviews not fitting the above categories, use the general 6-dimension framework:*

Analyze across **6 dimensions**, then calculate **overall score out of 5**:

### 1. Role Alignment
*Do questions match the JD?*

- Questions probe JD requirements
- Technical depth appropriate for role
- Scenarios match actual job challenges

### 2. Question Quality
*Open-ended, behavioral, good follow-ups?*

- Open vs closed questions ratio
- Behavioral questions (STAR-friendly)
- Follow-up probes ("Tell me more", "What happened next")
- **Flag**: Leading questions ("You're good with deadlines, right?")

### 3. Bias Signals
*Fair and consistent?*

**Red flags**:
- Assumptions based on background
- Interrupting candidate frequently
- Affinity bias ("Oh, you went to my school too!")
- Questions about protected characteristics

### 4. Structure & Flow
*Clear progression?*

- Opening: Set expectations, build rapport
- Middle: Logical topic flow
- Closing: Time for candidate questions, next steps explained
- Time management: Not rushed at end

### 5. Talk Ratio
*Candidate should talk 70-80%*

- Count interviewer vs candidate speaking time
- Flag if interviewer talks >40%
- Note long interviewer monologues

### 6. Candidate Experience
*Would they recommend interviewing here?*

- Warmth and rapport
- Active listening
- Selling the role appropriately
- Clear communication about process

---

## Scoring

**Overall Score: X/5**

| Score | Meaning |
|-------|---------|
| 5 | Excellent — nothing significant to improve |
| 4 | Good — minor refinements will make you great |
| 3 | Adequate — clear areas to work on |
| 2 | Needs improvement — several patterns to address |
| 1 | Significant concerns — fundamental issues to fix |

**Calculate**: Average across 6 dimensions, round to nearest 0.5

---

## Output Format

Uses the standard review template from `workable-master` SKILL.md — plain-text format with:

1. **Expert Panel Assessment** — 3 experts, bullet points (Strong/Concern), score per expert
2. **Barrel Scoring** — 5 dimensions, classification
3. **Candidate Scorecard** — 7 dimensions scored /10, overall average
4. **Interview Quality** — short assessment of whether the questions were good, time was managed well, and gaps were probed
5. **Recommendation** — clear verdict with next steps

The **Interview Quality** section is unique to this skill (not in candidate-compare). It evaluates the interviewer's performance:

~~~
━━━ INTERVIEW QUALITY ━━━

• Questions matched JD: [Yes/Partially/No] — [brief note]
• Failure probing: [Strong/Adequate/Weak] — [brief note]
• Case question quality: [Strong/Adequate/Weak] — [brief note]
• Time management: [Good/Okay/Poor] — [brief note]
~~~

This gives the interviewer quick feedback on their own performance alongside the candidate assessment.

---

## Best Practices Reference

### Strong Questions

**Behavioral (STAR)**:
- "Tell me about a time when..."
- "Describe a situation where you had to..."

**Situational**:
- "How would you handle..."
- "What would you do if..."

**Follow-ups**:
- "What was the result?"
- "What would you do differently?"

### Avoid These

| Avoid | Instead |
|-------|---------|
| "Are you a team player?" | "Tell me about a time you collaborated..." |
| "What's your greatest weakness?" | "What skill are you actively developing?" |
| "Can you work under pressure?" | "Describe a high-pressure situation you handled" |

### Ideal Structure

```
[0-5 min]   Welcome & rapport, explain format
[5-35 min]  Core questions with follow-ups
[35-45 min] Candidate questions
[45-50 min] Close — next steps, timeline, thank them
```

---

## Tone

Be a **coach, not a critic**:
- "Here's an opportunity..." not "You did this wrong"
- "Consider trying..." not "You should have..."
- Always quote the transcript
- Provide concrete alternatives

---

## Triggers

| User Says | Action |
|-----------|--------|
| "review my interview with [name]" | Search Fathom by name, fetch transcript, ask for interview type |
| "hr round review with [name]" | Fetch transcript, analyze with HR framework |
| "technical round review with [name]" | Fetch transcript, analyze with Technical framework |
| "final round review with [name]" | Fetch transcript, analyze with Final framework |
| "assess my interview with [name]" | Same as review |
| "how's the candidate [name]" | Same as review |
| "review my interview" | Ask for candidate name and interview type |
| "assess my interview" | Same |
| "interview feedback" | Same |
| "interview coach" | Same |
| "hr round review" | Ask for candidate, use HR framework |
| "technical round review" | Ask for candidate, use Technical framework |
| "final round review" | Ask for candidate, use Final framework |
| Pastes transcript | Ask for role and interview type, then analyze |

---

## Post-Evaluation: Expert Assessment + Push to Workable

After generating the interview coaching feedback, **always produce the candidate review** using the standard template from `workable-master`:

### Automatic Steps:
1. **Select 3 experts** based on the role (see `workable-master` SKILL.md for role→expert mapping)
2. **Run expert assessments** — each expert evaluates the candidate from their lens
3. **Run barrel scoring** — 5 dimensions, weighted total, classification
4. **Compile strengths, gaps, and follow-up questions**
5. **Determine grade** — map expert consensus + barrel score to Yes/Maybe/No

### Then offer to push:
```
💡 Push this review to Sarah's Workable profile? (Grade: Yes ✅)
```

**When user confirms**:
```bash
python3 03-skills/workable-master/scripts/workable_client.py \
  --candidate "{candidate_name}" \
  --review --grade {0|1|2} \
  --assessment "{full_review_text}"
```

**If user declines**: Still save the review locally but don't push.

---

## Integration

**Connected skills**:
| Skill | Purpose |
|-------|---------|
| `fathom-fetch-meetings` | Get interview transcript (Fathom) |
| Amie notes/transcripts | Get interview transcript (Amie) |
| `workable-master` | Fetch JD + push review to Workable |

**Full Workflow** (end-to-end):
```
Manager: "review my interview with Sarah"
→ AI searches Fathom for "Sarah" in meeting titles
→ AI: "What role was this interview for?"
Manager: "Product Manager"
→ AI fetches JD from Workable (workable-master)
→ AI selects 3 expert panel based on role
→ Expert assessments + barrel scoring
→ AI: "Push this review to Sarah's Workable profile? (Grade: Yes ✅)"
Manager: "yes"
→ Review posted to Workable with grade
```

**Alternative** (step-by-step):
```
Manager: "fetch meetings from fathom"
→ Lists recent meetings
Manager: picks meeting
Manager: "review my interview"
→ continues as above
```

No manual transcript or JD pasting required — everything pulls from your systems.

---

**Version**: 2.0 | **Updated**: 2026-02-16

**Changelog**:
 - v1.6: **Workable push integration** — after evaluation, offers to push assessment to candidate's Workable profile via `workable-push-assessment`
- v1.5: **Stage-specific evaluation** — added HR Round, Technical Round, and Final Round frameworks with tailored dimensions and weights
- v1.4: Added candidate name search — "review my interview with [name]" fetches transcript automatically
- v1.3: Integrated with workable-fetch-jd for automatic JD fetching
- v1.2: Added triggers "assess my interview", "how's the candidate"
- v1.1: Integrated with fathom-fetch-meetings, simplified to 5-point scale, removed letter grades
- v1.0: Initial creation
