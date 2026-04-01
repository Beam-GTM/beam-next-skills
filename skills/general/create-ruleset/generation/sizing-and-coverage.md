# Dataset Best Practices

Reference doc for dataset sizing, coverage distribution, complexity classification, and quality guidance. All numbers are concrete — no vague language. This doc is the single source of truth for the consultant workflow in `create-ruleset`.

**Scope:** Beam's end-to-end business workflow automation agents. This covers agents that receive structured or unstructured business inputs, apply domain logic, and produce actionable outputs (decisions, documents, structured data, API calls).

---

## Why Two Dimensions?

The previous framework used a single complexity axis with four signals — branching paths, input variations, jobs-to-be-done, and decision factors. That was wrong because it conflated agent logic with input variety. A simple agent processing 10 file formats is still a simple agent — it just needs more test data coverage (breadth), not deeper test cases (depth). Mixing the two into one score caused sizing errors: simple agents with many input formats got inflated complexity ratings and unnecessarily deep test suites, while complex agents with narrow inputs got undersized datasets.

The fix: separate the two concerns into independent dimensions. **Agent Complexity** drives test case depth (how intricate each test needs to be). **Input Surface Area** drives test data breadth (how many format/locale variations you need). They combine multiplicatively in the sizing table.

---

## Dimension 1: Agent Complexity

Measures how hard the agent's decision-making is — independent of how many input formats it handles.

### 4 Complexity Signals

| Signal | How to assess | Low | Medium | High |
|--------|--------------|-----|--------|------|
| **Agent Logic Depth** | Map the agent's processing pipeline | Linear pipeline or single formula | Conditional rules, some branching | Multi-step reasoning, tool orchestration, state management |
| **Output Complexity** | Examine what the agent produces | Binary or single value | Structured output with 3-7 fields, some derived | Multi-entity output, narrative + data, field dependencies |
| **Jobs-to-be-done** | Count distinct user goals the agent serves | 1 | 2-3 | 4+ |
| **Domain Judgment Required** | Assess the nature of the agent's decisions | Mechanical rules (if X then Y) | Some interpretation (semantic matching, fuzzy criteria) | Subjective judgment, legal/ethical reasoning, ambiguous criteria |

### Classification Logic

```
Count how many of the 4 signals score above "Low":
  0-1 signals above Low  ->  Easy
  2 signals above Low    ->  Medium
  3-4 signals above Low  ->  Hard
```

---

## Dimension 2: Input Surface Area

Measures how varied the inputs are — SEPARATE from how complex the agent's logic is. A simple classifier that handles 12 file formats has high surface area but easy agent complexity.

### 3 Surface Factors

| Factor | How to count | Low | Medium | High |
|--------|-------------|-----|--------|------|
| **Format variety** | Count distinct input formats (PDF, CSV, email, JSON, etc.) | 1-3 | 4-8 | 9+ |
| **Structural variety** | Assess layout variation within formats | Uniform structure | Some layout variety (e.g., different column orders, optional sections) | Highly varied (different column counts, styles, noise, freeform) |
| **Language/locale** | Count languages or locale variants the agent must handle | 1 language | 2-3 languages | 4+ languages |

### Surface Level Classification

```
Count how many of the 3 factors score above "Low":
  0-1 factors above Low  ->  Low    (multiplier: x1.0)
  2 factors above Low    ->  Medium (multiplier: x1.0)
  3 factors above Low    ->  High   (multiplier: x1.25)
```

Low and Medium surface areas do not increase dataset size — the base sizing table already accounts for reasonable input variety. High surface area adds a 25% multiplier because the agent needs broader format/locale coverage in every test category.

---

## Complexity Assessment: Presentation Format

Present both dimensions separately with evidence, so the reasoning is transparent:

```
Agent Complexity: Medium
Signals:
  * Agent Logic Depth: conditional rules with 3 branching paths -> Med
  x Output Complexity: single classification label -> Low
  * Jobs-to-be-done: 2 (classify + extract metadata) -> Med
  x Domain Judgment: mechanical rules (keyword matching) -> Low
2 of 4 signals above Low -> Medium

Input Surface Area: High
Factors:
  * Format variety: 12 formats (PDF, Word, Excel, CSV, HTML, XML, JSON, email, plain text, images, PowerPoint, markdown) -> High
  * Structural variety: highly varied (tables, freeform prose, mixed layouts) -> High
  * Language/locale: 4 languages (EN, DE, FR, ES) -> High
3 of 3 factors above Low -> High (x1.25)

Final sizing multiplier: Medium complexity x High surface = base(Medium) x 1.25
```

The user confirms or overrides either dimension. If override, record the reason in the ruleset's planning metadata.

---

## Dataset Sizing

### Sizing Table (Purpose x Agent Complexity x Surface Multiplier)

Final size = base_size(purpose x agent_complexity) x surface_multiplier

Base sizes by purpose and agent complexity:

| Purpose \ Complexity | Easy | Medium | Hard |
|---------------------|------|--------|------|
| `flow_check` | 5 | 8 | 10 |
| `score` | 20 | 35 | 50 |
| `battle_test` | 80 | 120 | 175 |

Surface multiplier: Low/Medium = x1.0, High = x1.25

**Example:** A medium-complexity agent with high surface area, purpose = `score`:
- Base size: 35 (score x medium)
- Surface multiplier: x1.25 (high surface area)
- Final size: 35 x 1.25 = **44** (round to nearest whole number)

### Purpose Definitions

| Purpose ID | Description | When to use |
|-----------|-------------|-------------|
| `flow_check` | Does the agent's flow work end-to-end? Quick check with core scenarios. | Early prototyping, testing prompt changes, verifying the happy path works |
| `score` | How accurate is it across real scenarios? Balanced coverage across main variations. | Ongoing quality monitoring, measuring accuracy after changes |
| `battle_test` | Can it survive everything production throws at it? Every edge case, error path, and adversarial input. | Pre-launch validation, production readiness, optimization runs |

### Sizing Rationale

- Easy: lower end of the recommended range (simpler logic = fewer cases needed)
- Medium: midpoint of the range
- Hard: upper end (more complex reasoning requires proportionally more coverage)
- High surface area (x1.25): adds breadth — more format/locale combinations in every test category

Every dataset size must trace back to this table. No arbitrary numbers.

---

## Coverage Distribution

### Base Coverage Splits by Purpose

Percentages must sum to 100:

| Purpose | Happy Path | Edge Case | Error Case | Adversarial |
|---------|-----------|-----------|------------|-------------|
| `flow_check` | 80% | 15% | 5% | 0% |
| `score` | 55% | 30% | 10% | 5% |
| `battle_test` | 20% | 30% | 25% | 25% |

### Coverage Category Definitions

| Category | Definition | Examples |
|----------|-----------|----------|
| **Happy Path** | Standard inputs that exercise the agent's core workflow with clean, complete data | Complete form submissions, well-structured documents, clear instructions |
| **Edge Case** | Valid but unusual inputs that test boundary conditions and uncommon paths | Missing optional fields, maximum-length inputs, rare but valid combinations |
| **Error Case** | Invalid, malformed, or contradictory inputs that should trigger graceful handling | Empty required fields, wrong data types, conflicting instructions, API timeouts |
| **Adversarial** | Inputs designed to exploit weaknesses, confuse the agent, or trigger incorrect behavior | Prompt injection attempts, misleading context, ambiguous instructions that invite wrong assumptions |

### Complexity Adjustments

Applied after the base lookup. Adjustments stack. Final percentages must still sum to 100%.

```
If agent_complexity == hard:
  happy_path -= 5%
  edge_case  += 5%
  Rationale: more complex logic = more edge cases to cover

If agent handles external APIs (detected from docs/context):
  happy_path -= 5%
  error_case += 5%
  Rationale: external dependencies = more failure modes
```

**Example:** A hard-complexity battle_test agent that calls external APIs:

| | Base (battle_test) | +hard | +external APIs | Final |
|---|---|---|---|---|
| Happy Path | 40% | 35% | 30% | 30% |
| Edge Case | 25% | 30% | 30% | 30% |
| Error Case | 20% | 20% | 25% | 25% |
| Adversarial | 15% | 15% | 15% | 15% |

---

## Anti-Patterns

### 1. Arbitrary Sizing

**BAD:** "Let's generate 100 examples" with no rationale.

**Instead:** Look up purpose x agent_complexity in the sizing table, apply the surface multiplier. Every dataset size must trace back to the table. If 100 is the right number, show the lookup that produced it (e.g., "battle_test x medium x high_surface = 120 x 1.25 = 150, but user scoped to one workflow = 100").

### 2. Happy-Path Skew

**BAD:** 80% happy path, 10% edge, 5% error, 5% adversarial.

**Instead:** Use the coverage distribution table for the dataset's purpose. Battle_test suites must have no more than 40% happy path. If you find yourself exceeding 50% happy path for any purpose, you are undertesting the agent's failure modes.

### 3. Complexity-Blind Generation

**BAD:** Same dataset structure for a simple form parser and a multi-tool reasoning agent.

**Instead:** Run the two-dimension classification (agent complexity + input surface area). A hard agent needs deeper test cases than an easy one. High surface area needs broader format coverage. The two dimensions combine to determine final dataset size.

### 4. Vague Coverage Categories

**BAD:** "Include some edge cases and error handling."

**Instead:** Define concrete edge cases tied to the agent's specific logic paths and input variations. Each edge case maps to a specific signal from the complexity classification. "Edge case" without specifics is not actionable.

### 5. Disconnected Planning and Execution

**BAD:** Discussing dataset size and coverage in conversation but not encoding it anywhere — then generating data without those constraints.

**Instead:** Bake all planning decisions (purpose, agent complexity, surface area, size, coverage split) into the ruleset's `planning` section. The `create-data` skill reads this section and enforces it during generation. If it's not in the ruleset, it doesn't exist.

---

## Quality Signals

### Gold Standard Attributes

Every generated example in the dataset should be:

| Attribute | Concrete check |
|-----------|---------------|
| **Grounded** | Every field value traces to a rule in the ruleset or a realistic domain pattern |
| **Diverse** | No two examples in the same batch share identical structure, phrasing, or scenario |
| **Bounded** | All numeric values fall within the ranges specified in the ruleset |
| **Internally consistent** | Fields within a single example do not contradict each other |
| **Correctly labeled** | The coverage category (happy/edge/error/adversarial) matches the example's actual characteristics |

### Red Flags in Generated Data

| Red flag | What it means | Fix |
|----------|--------------|-----|
| 5+ examples with identical structure but swapped names | Generator is templating, not generating | Increase variation dimensions or add more few-shot diversity |
| All edge cases are "missing field X" | Only one edge case type is being exercised | Map edge cases to specific complexity signals |
| 0 adversarial examples in a batch of 20+ | Coverage distribution not enforced | Check that the planning section's coverage split is being read |
| Output always matches happy-path format even for error inputs | Generator ignores input category | Add explicit error output examples to the ruleset |
