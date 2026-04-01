# Verification Prompt Template

Use this template with **3 independent evaluator subagents** for multi-LLM consensus verification. Domain-agnostic — works for any agent type.

## Three Evaluation Dimensions

Each evaluation must assess:
- **quality_score** (0-100): Overall quality of the generated sample
- **is_valid** (true/false): Whether the output is structurally correct and internally consistent
- **passes_ruleset** (true/false): Whether the example follows all ruleset constraints

---

## System Prompt

```
You are an expert quality evaluator for synthetic test data. Your task is to evaluate a single generated sample and provide three assessments:
1. Quality score (0 to 100)
2. Whether the output is structurally valid and internally consistent (true/false)
3. Whether the example strictly follows the ruleset constraints (true/false)

Be objective and strict. Consider:
- Does the input match the input schema? (correct fields, realistic values, proper format)
- Does the output match the output schema? (correct fields, proper types, values in range)
- Is the output derivable from the input using the output derivation procedure?
- Are scoring formulas applied correctly with proper bounds?
- Does the sample match its assigned coverage category profile?
- Would a domain expert find both input and output realistic?
```

---

## Human Prompt

```
Evaluate this generated sample against the ruleset:

## Ruleset Context
{use_case}

## Litmus Test
{litmus_test}

## Input Schema
{input_schema}

## Output Schema
{output_schema}

## Output Derivation Procedure
{derivation_procedure}

## Sample to Evaluate

Transformation Rules: {transformation_rules}

Input:
{input}

Expected Output:
{output}

## Evaluate

Check each of these:
1. INPUT VALIDITY: Does the input match the input schema? Are all required fields present with realistic values?
2. OUTPUT VALIDITY: Does the output match the output schema? Are all fields present with correct types and in-range values?
3. DERIVATION CORRECTNESS: Can you trace the output from the input using the derivation procedure? Are scoring formulas applied correctly with proper bounds?
4. PAIRING CORRECTNESS (multi-entity only): If the input has multiple entities (e.g., CV + JD, claim + policy), does the claimed pairing type match the actual relationship? A "strong match" pairing where the entities are from completely different domains is a hard fail. Check: does the output (score, decision, routing) correctly reflect the pairing relationship?
5. CATEGORY FIT: Does this sample match its claimed coverage category (happy_path/edge_case/error_case/adversarial)?
6. LITMUS TEST: Apply the litmus test question above to this sample. Answer it honestly — does this sample pass?
7. REALISM: Would a domain expert find this sample realistic? Consider the Three Layers of Difficulty from the use case.

Return your evaluation in this exact JSON format:
{
  "quality_score": <integer from 0 to 100>,
  "is_valid": <true or false>,
  "passes_ruleset": <true or false>,
  "passes_litmus_test": <true or false>,
  "pairing_correct": <true or false or null if single-entity>,
  "issues": [<list of specific issues found, empty if none>],
  "category_fit": <true or false>
}
```

---

## Quality Score Scale

| Range | Assessment | Criteria |
|-------|------------|----------|
| 80-100 | **High** | Realistic, correct derivation, follows all rules, passes litmus test |
| 60-79 | **Medium** | Mostly correct but minor issues (e.g., slightly unrealistic values, one field borderline) |
| 40-59 | **Low** | Structural issues or derivation errors but salvageable |
| <40 | **Invalid** | Wrong schema, broken derivation, contradictory fields, fails litmus test |

---

## Multi-LLM Consensus Logic

Run verification with **3 independent evaluator subagents**.

### Pass Criteria

**Sample passes if ALL conditions met:**
1. **Unanimous validity**: All evaluators agree `is_valid: true`
2. **Quality threshold**: Average `quality_score` >= 80 (configurable)
3. **Ruleset compliance**: All evaluators agree `passes_ruleset: true`

### Lightweight Pre-Check (Optional)

For structured output (JSON), run a schema validator BEFORE the 3-LLM consensus:
- Check all required fields exist
- Check field types match schema
- Check numeric values are in declared ranges
- Check enum values are from the allowed set

If pre-check fails → auto-reject without spending 3 LLM calls. This saves cost for obviously broken samples.

### Conservative Fallback on Error

If an evaluator subagent fails or returns malformed output:
- is_valid: false
- passes_ruleset: false
- quality_score: 30 (low score on error)

---

## Tracking Failures

Log failed samples with:
- Sample content (input/output)
- Individual evaluator scores and issues
- Consensus result
- Failure reason(s) — categorized as: schema_error, derivation_error, realism_error, category_mismatch

Use failure patterns to:
1. Improve generation prompts in next batch
2. Feed into post-generation feedback for ruleset improvement

---

## Configuration Defaults

- **num_samples_to_generate**: 10 per batch
- **min_consensus_score**: 0.8 (80/100)
- **require_unanimous_validity**: true (all evaluators must agree)
- **require_minimum_evaluators**: 3
- **enable_schema_precheck**: true (for JSON/structured outputs)
