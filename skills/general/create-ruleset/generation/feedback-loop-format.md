# Post-Generation Feedback Loop

Captures what `create-data` learned while generating from the ruleset, so the ruleset improves over each generation cycle.

---

## When to Run

After `create-data` completes a generation batch, before the user moves on. This is NOT a blocking step — it runs automatically and writes annotations to the ruleset folder.

---

## What to Capture

### 1. Ambiguity Log

Rules that subagents interpreted differently, producing inconsistent outputs.

```yaml
ambiguities:
  - rule: "Score 7-9 for strong experience match"
    issue: "Subagents disagreed on what counts as 'strong' — some required 80% keyword overlap, others accepted 50% with related experience"
    suggestion: "Define 'strong match' as: ≥70% of must-have requirements met OR ≥50% with demonstrably related experience"
    samples_affected: [sample_12, sample_27, sample_33]

  - rule: "Generate realistic company names"
    issue: "3 subagents used the same company name 'TechCorp Solutions'"
    suggestion: "Add anti-repetition constraint or provide a company name seed list"
    samples_affected: [sample_05, sample_18, sample_41]
```

### 2. Coverage Gaps

Categories or variation dimensions that were underrepresented in the generated data.

```yaml
coverage_gaps:
  - dimension: "input_format"
    expected: "PDF 65%, DOCX 20%, TXT 10%, Other 5%"
    actual: "PDF 82%, DOCX 15%, TXT 3%, Other 0%"
    suggestion: "Lock format distribution in generation briefs rather than leaving it to subagent discretion"

  - dimension: "adversarial"
    expected: "5% of samples"
    actual: "2% (1 of 44)"
    suggestion: "Adversarial samples need explicit few-shot examples in ruleset — subagents default to happy path without them"
```

### 3. Missing Rules

Situations the subagents encountered that had no corresponding rule in the ruleset.

```yaml
missing_rules:
  - situation: "Candidate CV had a career gap of 3+ years"
    question: "How should the agent score career gaps? No rule covers this."
    default_used: "Subagent penalized by 1 point — may not match production behavior"

  - situation: "JD listed 'equivalent experience' as alternative to degree"
    question: "How much extra experience counts as equivalent? No threshold defined."
    default_used: "Subagent used 2 years per degree level — arbitrary"
```

### 4. Scoring Formula Issues

For rulesets with scoring/evaluation logic — cases where formulas produced unexpected results.

```yaml
formula_issues:
  - formula: "role_fit = industry + location + culture"
    issue: "Sub-scores summed to 14 but dimension max is 10 — missing min(10, ...) bound"
    fix: "role_fit = min(10, industry + location + culture)"

  - formula: "final_rating = round(weighted_score / 20)"
    issue: "Scores of 0-3 all map to rating 0, but rating scale starts at 1"
    fix: "final_rating = max(1, round(weighted_score / 20))"
```

---

## Output Format

Save to: the same directory as the ruleset file, named `[domain]_feedback.md`

```markdown
# Generation Feedback — [Domain] — [Date]

**Generated from:** [ruleset file path]
**Samples generated:** [N]
**Subagents used:** [N]

## Ambiguities
[List from above]

## Coverage Gaps
[List from above]

## Missing Rules
[List from above]

## Scoring Formula Issues
[List from above, if applicable]

## Recommended Ruleset Updates
1. [Concrete change to make]
2. [Concrete change to make]
3. [Concrete change to make]
```

---

## How to Use

### In `create-data`
After generation completes, the main agent scans for the patterns above by:
1. Reading all generated outputs and checking for inconsistencies across subagent batches
2. Comparing actual coverage distribution against the ruleset's planned distribution
3. Logging any situations where the subagent had to improvise (no matching rule)
4. Checking scoring formulas against actual computed values

### In `create-ruleset`
When creating or updating a ruleset, check for an existing `_feedback.md` file:
1. If found, read it and pre-apply the recommended updates
2. Flag any ambiguities that were logged — these are priority fixes
3. Use coverage gaps to adjust distribution weights
4. Add missing rules to fill documented gaps

### Iteration Cycle

```
create-ruleset → ruleset.md
    ↓
create-data → generated samples + _feedback.md
    ↓
create-ruleset (update) → ruleset_v2.md (incorporates feedback)
    ↓
create-data → better samples + less feedback
```

Each cycle should produce fewer feedback items. If feedback stabilizes at zero, the ruleset is mature.
