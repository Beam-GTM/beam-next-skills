---
name: workable-push-assessment
description: Push interview assessments and candidate evaluations to Workable ATS. Load when user says "push assessment to workable", "post evaluation to workable", "send assessment to workable", "update workable with assessment", "push to workable", or after interview-coach completes an evaluation.
version: 1.0
---

# Workable Push Assessment

*Post your interview assessments directly to candidate profiles in Workable.*

> **When to use**: After completing an interview review (via `interview-coach`) or candidate comparison (via `candidate-compare`), push the evaluation to Workable so it's visible to the whole hiring team.
>
> **Prerequisites**:
> - `WORKABLE_API_KEY` in `.env`
> - `WORKABLE_SUBDOMAIN` in `.env`
>
> **Output**: Assessment posted as comment on candidate's Workable profile

---

## Setup (One-Time)

Add these to your `.env` file:

```
WORKABLE_API_KEY=your_api_key_here
WORKABLE_SUBDOMAIN=your_subdomain
```

**Get your API key**: Workable → Settings → Integrations → Apps → Generate API token

**Your subdomain**: The part before `.workable.com` in your Workable URL (e.g., if you use `beam.workable.com`, your subdomain is `beam`)

---

## Workflow

### Step 1: Get the Assessment

This skill is typically triggered **after** `interview-coach` or `candidate-compare` produces output.

**Option A — After interview-coach** (recommended):
```
User: "review my interview with Sarah"
→ interview-coach produces evaluation
→ AI: "Want me to push this assessment to Workable?"
→ User: "yes"
→ workable-push-assessment posts it
```

**Option B — Manual push**:
```
User: "push assessment to workable for Sarah Chen"
→ AI: "What assessment should I post? Paste it or point me to a file."
→ User provides assessment text or file path
→ AI posts to Workable
```

**Option C — From file**:
```bash
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --candidate "Sarah Chen" \
  --file 04-workspace/ceo-office/interviews/sarah-chen-review.md
```

### Step 2: Find the Candidate

The script searches Workable by candidate name:

```bash
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --search "Sarah"
```

If multiple matches are found, the AI will ask you to confirm which candidate.

### Step 3: Post the Assessment

```bash
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --candidate "Sarah Chen" \
  --assessment "Assessment text here..."
```

The assessment is formatted for Workable's comment field (markdown converted to basic HTML) and posted as a public comment visible to the hiring team.

---

## Integration with Interview Coach

After `interview-coach` produces an evaluation, it should offer:

```
💡 Push this assessment to Workable? Say 'push to workable' to post it to Sarah's profile.
```

When the user confirms:
1. Save the assessment output to a temp file
2. Search for the candidate in Workable
3. Post the assessment as a comment
4. Confirm success

---

## CLI Reference

```bash
# Search for a candidate
python3 03-skills/workable-push-assessment/scripts/push_assessment.py --search "Sarah"

# Push assessment with text
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --candidate "Sarah Chen" --assessment "Assessment text..."

# Push assessment from file
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --candidate "Sarah Chen" --file path/to/assessment.md

# Push to a specific candidate ID (skip search)
python3 03-skills/workable-push-assessment/scripts/push_assessment.py \
  --candidate-id abc123 --assessment "Assessment text..."

# List open jobs
python3 03-skills/workable-push-assessment/scripts/push_assessment.py --list-jobs

# Output as JSON
python3 03-skills/workable-push-assessment/scripts/push_assessment.py --search "Sarah" --json
```

---

## Triggers

| User Says | Action |
|-----------|--------|
| "push assessment to workable" | Ask for candidate name + assessment |
| "post evaluation to workable" | Same |
| "send assessment to workable for [name]" | Search candidate, ask for assessment |
| "push to workable" | Post last interview-coach output |
| "update workable with assessment" | Same |
| After interview-coach completes | Offer to push automatically |

---

## Integration

**Connected skills**:
| Skill | Purpose |
|-------|---------|
| `interview-coach` | Produces interview evaluations to push |
| `candidate-compare` | Produces comparison reports to push |
| `workable-fetch-jd` | Fetches job descriptions from same Workable account |

---

**Version**: 1.0 | **Created**: 2026-02-16

**Changelog**:
- v1.0: Initial creation — search candidates, post assessments as comments
