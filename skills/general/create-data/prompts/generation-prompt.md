# Generation Prompt Template

Use this template when generating each batch of samples. Domain-agnostic — works for any agent type (code generation, document evaluation, classification, triage, etc.).

## Expected Output Format

Each generated example must have:
- **transformation_rules**: List of rules applied from ruleset
- **input**: The agent's input data (as string or structured content — matches the ruleset's INPUT SCHEMA)
- **output**: The agent's expected output (as string or structured content — matches the ruleset's OUTPUT SCHEMA)

---

## System Prompt

```
You are an expert synthetic data generator.

Generate synthetic test data for an AI agent. Each example must contain:
- transformation_rules: A list of rules that guided this sample's generation
- input: The agent's input data — realistic, varied, matching the input schema
- output: The correct expected output — derived using the output derivation procedure

Follow these guidelines:
- Input should match the real-world inputs the agent processes in production
- Output should be correct and derivable from the input using the scoring/derivation logic
- Use clear and specific transformation rules that explain what variation this sample covers
- Make examples diverse across the variation dimensions assigned in your generation brief

CRITICAL: Input and output formats must match the ruleset's INPUT SCHEMA and OUTPUT SCHEMA exactly.
```

---

## Human Prompt

```
You are generating synthetic test data for: [DOMAIN]

## Use Case
[Insert USE CASE section from ruleset — The Context, Real-World Inputs, Three Layers of Difficulty, Litmus Test]

## Input Schema
[Insert INPUT SCHEMA section from ruleset — per-entity Content, Presentation, Variation tables]

## Output Schema
[Insert OUTPUT SCHEMA section from ruleset — fields, types, ranges, scoring formula]

## Output Derivation Procedure
[Insert OUTPUT DERIVATION PROCEDURE from ruleset — step-by-step recipe from input to output]

## Pairing Strategy (if multi-entity)
[Insert PAIRING STRATEGY from ruleset — generation order, pairing types, constraints]

## Per-Category Composition
[Insert PER-CATEGORY COMPOSITION from ruleset — variation profiles per coverage category]

## Distribution Targets

Generate samples matching your assigned generation brief (see below).

**Coverage category:** [from brief — happy_path / edge_case / error_case / adversarial]
**Priority fills:** [List dimensions below target distribution]

## Few-Shot Examples

**NOTE: These examples may use `...` with bracketed notes (e.g., "[Article continues — ~450 words total]") to show structure without filling the prompt. Your generated samples MUST be FULL LENGTH — produce complete inputs at the length indicated in the bracket, not truncated ones.**

[Insert 2-3 examples from ruleset's FEW-SHOT EXAMPLES, rotated each batch]

Example 1:

Input:
[example input matching input schema]

Expected Output:
[example output matching output schema]

Derivation: [brief explanation of how output was derived]

---

Example 2:

Input:
[example input]

Expected Output:
[example output]

---

## Anti-Patterns to Avoid
[Insert ANTI-PATTERNS section from ruleset]

## Generation Brief
[Insert the subagent's assigned brief — locked dimensions, freed dimensions, anti-repetition blocklist]

## Generate {num_samples} Samples

Generate exactly {num_samples} new test data examples following the ruleset.

Each example must have:
- transformation_rules: List of rules applied (which variation dimensions, which coverage category)
- input: Realistic agent input matching the INPUT SCHEMA (NOT a dict unless the schema is JSON)
- output: Correct expected output matching the OUTPUT SCHEMA, derived using the OUTPUT DERIVATION PROCEDURE

**Requirements:**
1. Match your assigned generation brief — cover the specific dimensions you were assigned
2. Each input must be unique (not similar to examples, gold standards, or anti-repetition blocklist)
3. Follow the output derivation procedure exactly — show your work in transformation_rules
4. Match the per-category composition profile for your assigned coverage category
5. Avoid all anti-patterns
6. If generating files (PDF, DOCX), include a render_spec in metadata following the assigned visual template
7. **FORMULA VERIFICATION (CRITICAL):** If the output includes computed scores (e.g., weighted averages), you MUST:
   a. Compute each sub-score first with explicit point breakdowns
   b. Apply the formula with actual numbers (e.g., `round(55*0.30 + 72*0.30 + 60*0.15 + 82*0.25)`)
   c. Show the intermediate sum (e.g., `round(16.5 + 21.6 + 9.0 + 20.5) = round(67.6)`)
   d. Verify the final value matches the rounded result
   e. **NEVER "adjust" a score after computing it.** If the formula yields 67, the score IS 67. If you want a different score, change the sub-scores so the formula naturally produces it.
   f. Include the verification in transformation_rules (e.g., `"formula_check: round(67.6)=68"`)

Return exactly {num_samples} examples.
```

---

## Variable Substitutions

| Placeholder | Source |
|-------------|--------|
| `[DOMAIN]` | Ruleset title or domain name |
| `[USE CASE section]` | From ruleset — v2 format |
| `[INPUT SCHEMA]` | From ruleset — per-entity with Content/Presentation/Variation |
| `[OUTPUT SCHEMA]` | From ruleset — fields, types, ranges |
| `[OUTPUT DERIVATION PROCEDURE]` | From ruleset — numbered steps |
| `[PAIRING STRATEGY]` | From ruleset — generation order + pairing types (skip if single-entity) |
| `[PER-CATEGORY COMPOSITION]` | From ruleset — variation profiles per category |
| `[Priority fills]` | Categories below target % |
| `[examples]` | Rotate from FEW-SHOT EXAMPLES |
| `[ANTI-PATTERNS section]` | From ruleset |
| `[Generation Brief]` | From Phase 1d — per-subagent assignment |
| `{num_samples}` | From config (default 10) |

## Key Points

1. **Domain-agnostic**: Input/output match the ruleset's schemas, not a fixed format
2. **Derivation-driven**: Output must be traceable through the derivation procedure
3. **Brief-driven**: Each subagent generates for its assigned dimensions only
4. **Rotate examples**: Don't reuse same few-shot examples every batch
5. **Few-shot examples may be truncated**: Ruleset few-shot inputs use `...` with bracketed continuation notes (e.g., `[Article continues — ~450 words total]`). The generator MUST produce FULL-LENGTH inputs — do NOT truncate like the examples. The examples show structure and style; generated samples must be complete.

---

## Worked Example: Insurance Claims Triage (Populated Template)

This shows what the template looks like when filled with a real ruleset. Subagent receives this as its generation prompt.

```
You are generating synthetic test data for: Insurance Claims Triage

## Use Case

### The Context
A mid-size property insurance company operates an AI triage agent that receives new claims
and assigns them a priority level + recommended handler. The agent runs as part of the claims
intake pipeline — every new claim passes through it within 60 seconds of submission.

### The Litmus Test
"Would an experienced claims adjuster spend more than 10 seconds questioning this
claim-policy pair, or would they immediately see it as either routine or flagged?"

## Input Schema

### Entity 1: Claim Form
Content:
| Field | Type | Required |
|-------|------|----------|
| claim_id | string (CLM-XXXXXX) | yes |
| incident_type | enum: water_damage, fire, theft, collision, weather, liability, other | yes |
| description | string (50-500 words) | yes |
| estimated_damage | number (USD) | no |
...

### Entity 2: Policy Document
Content:
| Field | Type | Required |
|-------|------|----------|
| policy_type | enum: homeowner, auto, commercial_property, renter | yes |
| coverage_types | array of covered perils with limits | yes |
| exclusions | array | yes |
| endorsements | array | no |
...

## Output Schema
| Field | Type | Value Range |
|-------|------|-------------|
| priority | enum | low, standard, high, urgent |
| confidence | number | 0.0-1.0 |
| routing | string | adjuster_pool, senior_adjuster, coverage_specialist, SIU |
| reasoning | string | 2-4 sentences |
| flags | array | coverage_gap, fraud_indicator, high_value, policy_issue, late_filing |

## Output Derivation Procedure
1. Extract claim details — incident_type, description keywords, estimated_damage, filing delay
2. Extract policy coverage — covered perils, exclusions, endorsements, deductible
3. Match coverage — incident_type against covered perils, check exclusions
4. Compute base priority — incident_type → priority mapping
5. Apply modifiers — each modifier escalates, never de-escalates
6. Determine routing — based on final priority + which modifiers fired
7. Generate reasoning — summarize coverage, complications, priority justification
8. Validate — priority matches modifiers? routing matches priority?

## Pairing Strategy
Generation order: Policy document first — it defines what's covered.
| Pairing Type | % | Description |
|-------------|---|-------------|
| Clear coverage | 30 | Incident type directly covered, no exclusions |
| Coverage with conditions | 25 | Covered but deductible/limit adds complexity |
| Exclusion applies | 15 | Appears covered but exclusion kicks in |
| Ambiguous coverage | 15 | Unclear if endorsement modifies base |
| Potential fraud | 10 | Red flags: delay, estimate near deductible |
| Policy expired | 5 | Wrong policy or expired |

## Generation Brief
Assigned samples: 1-5
Coverage category: edge_case
Variation focus:
  - Pairing type: ambiguous_coverage
  - Description quality: vague/brief
  - Filing delay: 8-30 days
Freed: claim details, company names, incident specifics, policy numbers

Anti-repetition blocklist: [CLM-234567, CLM-345678, CLM-456789, HO-891234, AU-123456]

## Generate 5 Samples
```
