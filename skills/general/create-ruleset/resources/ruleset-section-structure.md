# Ruleset Template

Use this exact structure when generating rulesets. Every section is required unless marked optional.

```markdown
---
schema_version: "2.0"
domain: [domain-name-slug]
created: [ISO 8601 date]
updated: [ISO 8601 date]
---

# Ruleset: [DOMAIN NAME]

## USE CASE

> Narrative description using the universal 4-part structure. This replaces rigid validation rules — quality guidance lives inside the narrative, not as a separate checklist.

### The Context

[Who operates this agent? What's the production environment? What problem does it solve? What company/team uses it?]

### Real-World Inputs

[What does the agent actually receive in production? Be specific — not "documents" but "PDF CVs extracted via ATS webhook + job descriptions from the careers page." Ground in reality.]

### Three Layers of Difficulty

**Realistic (bread-and-butter):** [What 70% of production inputs look like. Clean, well-structured, standard cases.]

**Challenging (messy but real):** [What 20% of production inputs look like. Missing fields, unusual formats, ambiguous content, multi-language, noisy extraction artifacts.]

**Deceptive (intentionally misleading):** [What adversarial inputs look like. Clean and well-formatted ON PURPOSE — keyword stuffing, contradictory information, inflated credentials, prompt injection attempts.]

### The Litmus Test

> **One question to check any generated sample against:**
> "[A single yes/no question that distinguishes good test data from bad. E.g., 'Would a recruiter with 5 years of experience find this CV-JD pair realistic enough to evaluate seriously?']"

---

## INPUT SCHEMA

> Input Schema defines **what the data is** — the fields, types, and constraints. It also describes Content Texture — what the content actually looks and feels like in production. It does NOT include variation distributions or presentation percentages. All variation lives in Test Scenarios.

### Entity 1: [NAME]

**File Type:** [PDF | JSON object | CSV | plain text string | rendered document | image | etc. — specify exactly what format this entity takes in production AND in the generated dataset. E.g., "PDF file (rendered per sample)" or "JSON object in index.json" or "text string in index.json"]

**Content** — what information the entity contains:

| Field | Type | Description | Constraints | Required |
|-------|------|-------------|-------------|----------|
| [field_name] | [string/number/date/enum] | [description] | [length range, format rules, valid values, edge cases] | [yes/no] |

> **Content Texture (CRITICAL):** Don't stop at field names and types. Describe what the content actually looks and feels like in production. For text fields: typical length range (e.g., "200-800 words"), structural characteristics (e.g., "may contain subheadings, bullet points, inline quotes, or data tables"), and stylistic variation (e.g., "wire-service style: short 1-2 sentence paragraphs, facts-first" vs "analytical style: longer paragraphs with market data and expert quotes"). For structured fields: value ranges with realistic distributions, not just the type. This texture is what the generator uses to produce realistic data — without it, all generated inputs look the same.

**Content characteristics** (if the entity has stylistic variation):

> Describe the distinct styles or formats the content can take in production. E.g., for news articles: wire-service (short, facts-first), analytical (longer, with quotes and data), regional (government quotes, local context). For CVs: chronological, functional, hybrid. For emails: formal, conversational, automated. This section is optional for entities with uniform content style.

### Entity 2: [NAME] (if multi-entity)

[Same structure as Entity 1 — including File Type declaration]

---

## OUTPUT SCHEMA

### Output: [NAME]

**File Type:** [PDF | JSON object in index.json | JSON string in index.json | separate .txt file per sample | CSV | rendered document | etc. — specify the exact file format for this output in the generated dataset]

**Format:** [JSON / plain text / markdown / code]

| Field | Type | Description | Constraints | Required |
|-------|------|-------------|-------------|----------|
| [field_name] | [type] | [description] | [operational constraints — see below] | [yes/no] |

> **Operational Constraints (CRITICAL):** Every constraint should help the generator produce correct data. Don't just specify types — specify rules the generator can check mechanically.
> - **Length constraints**: exact ranges, not vague ("800-2500 chars per message" not "medium length")
> - **Proportional rules**: formulas relating fields to each other ("~30-40s per item + 10s intro/outro" not "60-300 seconds")
> - **Format rules**: exact patterns ("daily_news_YYYY-MM-DD.mp3" not "descriptive filename")
> - **Splitting/grouping rules**: when and how to break content ("never split a single item across messages", "2-3 items per message")
> - **Enum values**: exhaustive lists, not "etc." ("news_anchor" not "professional style")

**Quality Constraints:**

| Constraint | Rule |
|-----------|------|
| [constraint_name] | [specific, machine-checkable rule] |

> Include output format specification (file format, filename pattern, delivery mechanism). Include constraints for specificity (e.g., "Each talking point must include at least one of: quantitative metric, named project, specific brand, or market reference").

**Scoring formula** (if applicable):

```
[Step-by-step formula with explicit bounds]
```

---

## OUTPUT DERIVATION PROCEDURE

> Step-by-step recipe for producing the correct expected output given an input. Without this, the generator is guessing.

1. **[Step name]** — [What to do. E.g., "Extract all requirements from the JD, categorize as must-have vs nice-to-have"]
2. **[Step name]** — [Next step]
3. **[Step name]** — [Continue]
4. **Validate** — [Final cross-check against all quality constraints]

**Intermediate artifact** (what the scoring worksheet looks like):

```
[Show an example of the intermediate calculation, not just input → output]
```

---

## TEST SCENARIOS

> Test Scenarios define **how the agent is tested** — what combinations of inputs it faces and why each is hard. Each scenario card has three parts:
> - **What**: The setup — what inputs land on the agent's desk
> - **Why it's hard**: The specific challenge this scenario tests
> - **Varies**: Parameter distributions within this scenario (as chips with percentages)
>
> This is the **single source of truth** for all variation dimensions and their distributions. No variation data lives elsewhere in the ruleset.
>
> **Dual-purpose format:** These cards are human-readable AND machine-parseable. create-data reads the Varies sections directly to build generation briefs.

### [Scenario Name] ([N] samples)

**What:** [1-3 sentences describing the setup — what the agent receives]

**Why it's hard:** [1-3 sentences describing the specific challenge this scenario tests]

**Varies:**

| Dimension | Options with distributions |
|-----------|--------------------------|
| [dimension_name] | [option_1] [X%], [option_2] [Y%], [option_3] [Z%] |

### [Scenario Name] ([N] samples)

[Same structure]

### [Scenario Name] ([N] samples)

[Same structure — typically 4 scenarios: happy path, edge case, error case, adversarial]

---

## FEW-SHOT EXAMPLES

> 3-5 examples covering different scenarios. Each example must match the output schema exactly.

**Few-Shot Rules:**
1. **Realistic length.** Input content must show the actual structure and depth of production data — multiple paragraphs with quotes, data points, and source attributions. Do NOT write artificially short 2-3 sentence inputs. For long content (articles, CVs, reports), show 3-4 substantial paragraphs, then use `...` followed by a bracketed note: `[Document continues with ... — ~N words total]`. The note should state (a) what remaining content covers and (b) total word count.
2. **Demonstrate content texture.** If the INPUT SCHEMA describes distinct content styles (e.g., wire-service vs analytical), the few-shot examples should collectively demonstrate all of them. Each example's continuation note should mention which style it uses.
3. **Demonstrate variation.** Across all examples, cover different scenarios (happy path + edge case + adversarial). Don't make all examples look the same.
4. **Output matches schema exactly.** Every field, constraint, and format rule in the OUTPUT SCHEMA must be exercised in at least one example. If the schema says "800-2500 chars per message," the example messages should be in that range.
5. **Derivation explains the mapping.** Not just "this is a happy path" — explain which scenario this example covers and how the output was derived from the input using the Output Derivation Procedure.

### Example 1: [Scenario Name — e.g., Happy Path / Rich Batch]

**Input:**
```
[3-4 substantial paragraphs of realistic content with quotes, data, attributions]

...

[Document continues with [remaining content summary] — ~N words total. Style: [content style from schema].]
```

**Expected Output:**
```
[Complete example output matching every OUTPUT SCHEMA constraint]
```

**Derivation:** [Which scenario this covers + how output was derived step-by-step]

### Example 2: [Scenario Name — e.g., Edge Case]

[Same structure, different scenario]

### Example 3: [Scenario Name — e.g., Adversarial]

[Same structure, different scenario]

---

## ANTI-PATTERNS

> What to avoid in generated data. Include BOTH domain-specific and generic LLM anti-patterns.

**Domain-specific** (unique to this agent):
1. **[Anti-pattern name]** — [What it looks like]. Why it's wrong: [explanation].
2. **[Anti-pattern name]** — [What it looks like]. Why it's wrong: [explanation].
3. **[Anti-pattern name]** — [What it looks like]. Why it's wrong: [explanation].

**Generic LLM failures** (apply to any generated data):
4. **Under-target sizing** — Generating fewer items/shorter content than the schema requires. Why it's wrong: LLMs optimize for brevity; production data is longer.
5. **Hallucinated sources** — Fabricating URLs, attributing quotes to wrong people, inventing statistics. Why it's wrong: a single fabrication destroys credibility.
6. **Placeholder content** — Using "[TBD]", "Company X", "John Doe" instead of realistic data. Why it's wrong: samples must be fully realized to test the agent.
7. **Repetitive structure** — Every sample follows identical patterns. Why it's wrong: production data varies in structure, not just content.

## OPEN QUESTIONS (optional)

> Only include if there ARE uncertainties. Omit entirely if none.

1. **[Question]** — [Context for why this matters]
```

---

## Planning YAML (hidden, machine-readable)

The planning data is embedded as a hidden HTML comment in the ruleset file, NOT as a visible section. It provides machine-readable metadata for create-data but should not clutter the human-readable document.

```yaml
<!-- PLANNING YAML (machine-readable, used by create-data) -->
<!--
planning:
  purpose: [flow_check | score | battle_test]
  agent_complexity: [easy | medium | hard]
  input_surface_area: [low | medium | high]
  surface_multiplier: [1.0 | 1.25]
  base_size: [number]
  final_size: [number]
  coverage_distribution:
    happy_path: [N]
    edge_case: [N]
    error_case: [N]
    adversarial: [N]
  approved_by: user
  approved_at: [ISO 8601 timestamp]
-->
```
