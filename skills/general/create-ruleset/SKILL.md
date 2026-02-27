---
name: create-ruleset
version: '1.0'
description: Create a ruleset for synthetic data generation. Use when the user wants
  to define rules for generating training data, create a new dataset domain, or set
  up data augmentation guidelines.
author: Aqib Ansari
category: general
tags:
- create
updated: '2026-02-25'
visibility: team
argument-hint:
- domain-name
disable-model-invocation: false
allowed-tools: Read, Write, Glob
---
# Create Ruleset for Synthetic Data Generation

You are helping the user create a comprehensive ruleset for synthetic data generation. This ruleset will guide the generation of diverse, high-quality training data for AI models.

**CRITICAL RULE: NEVER generate the ruleset immediately. You MUST conduct a conversational interview first, asking questions ONE AT A TIME and waiting for the user's response before asking the next question. Even if the user provides a lot of context upfront, there are always required fields to clarify — ask about what's missing. The only exception is if the user explicitly says "generate now" or similar.**

**Domain-agnostic** - Works for any use case: refund analysis, insurance claims, customer service, code generation, document creation, financial analysis, vehicle telemetry, etc.

## Resources

- **Template**: See [template.md](template.md) for the exact output format
- **Examples**: See [examples.md](examples.md) for sample rulesets

---

## Context Gathering System

Internally track all gathered context as the conversation progresses. The information you're collecting falls into these categories — use this as a mental checklist, but never show it to the user:

- **Domain basics**: domain name, task type, output format
- **Business logic**: core rules/criteria, decision thresholds, domain terminology
- **Data structure**: input fields, output shape, value ranges, categories/scenarios
- **Quality anchors**: concrete examples, edge cases, anti-patterns, quality criteria
- **Distribution**: how common each scenario is, complexity mix

After each user response, use the Expert Readiness Evaluation (below) to decide what to ask next.

---

## Interview Process

### Conversational Questioning

**CRITICAL: Do NOT use the AskUserQuestion tool. All questions must be asked as natural language text in your response.** The interview should feel like a natural back-and-forth conversation, not a form or checklist.

**CRITICAL: Do NOT skip the interview. Do NOT jump straight to generating the ruleset.** Even if the user provides substantial context in their initial message, you must still go through the interview to fill in gaps. Acknowledge what they've told you, then ask about the next missing piece. Ask questions **ONE AT A TIME**, waiting for the user's response before proceeding. Write your questions as plain conversational text in your response message. You must ask at minimum 3-4 questions before generating anything.

**Key Principles:**
1. Ask questions as natural language — never present options as numbered lists, checkboxes, or checklists
2. Start with essential questions first
3. After each answer, internally update the context tracker
4. Adapt follow-up questions based on what's been learned
5. Allow user to provide multiple pieces of info in one response
6. Skip questions that have already been answered
7. Give concrete examples inline to guide the user, but don't enumerate all possibilities

**User Override Keywords:**
- "generate now", "create the ruleset", "just generate it" → proceed with available info
- "skip", "use defaults", "default" → use sensible defaults and continue
- Always respect user's pace preference

### Opening Question

If `$ARGUMENTS` is provided, use it as the domain name. Otherwise, start by asking conversationally what domain the ruleset is for, giving a few inline examples.

---

### Phase 1: Core Understanding (REQUIRED)

After getting the domain name, gather these through natural conversation (skip if already answered):

**Task Type** — Ask what the AI should do when it receives input. Mention a couple of examples naturally (like "should it make a decision, generate code, extract data?") but don't list every option.

**Output Format** — Ask what the output should look like. Frame it conversationally, e.g. "Should the AI respond with structured JSON, plain text, code, or something else?"

**Core Rules** — Ask what the main rules or criteria are that govern the AI's behavior. Give a brief domain-relevant example to anchor the question.

**First Example** — Ask for one example of an input and expected output so you can understand the format concretely.

---

### Phase 2: Structure & Categories

Once the core fields are gathered, run the expert evaluation internally. If experts identify gaps (e.g., Data Engineer needs more scenario variety, or Quality Evaluator can't yet judge correctness), continue asking — but frame the transition naturally. Summarize what you've learned in a sentence or two, then ask about the most important gap.

Typical questions in this phase:

**Input Data** — Ask what information/data the AI will receive as input.

**Request Categories** — Ask what different types of requests or scenarios the AI should handle, giving a domain-relevant example.

**More Examples** — Ask for a couple more examples covering different scenarios.

---

### Phase 3: Refinement

If two or more experts are satisfied but one has remaining concerns, share that concern conversationally and let the user decide whether to address it or proceed.

Typical questions in this phase:

**Edge Cases** — Ask about boundary conditions or unusual scenarios.

**Distribution** — Ask how common each scenario is in practice.

**Quality Criteria** — Ask what makes a good vs bad AI response.

---

## Expert Readiness Evaluation

Before generating the ruleset, evaluate the gathered context through **three expert perspectives**. Run this evaluation internally after each user response to decide whether to ask more questions or proceed.

### The Three Experts

**1. Domain Expert — "Do I understand this domain well enough?"**

This expert evaluates whether the gathered context captures sufficient domain knowledge to produce realistic data. They ask themselves:
- Do I understand what real-world scenario this covers?
- Are the business rules specific enough, or are they vague platitudes that could apply to anything?
- Would someone who works in this field recognize the generated data as realistic?
- Are there domain-specific terms, thresholds, or conventions I'm missing?

**Verdict:** The Domain Expert is satisfied when the rules are concrete and specific (e.g., "refund within 30 days" not just "timely refund"), and the domain's key terminology and concepts are captured.

**2. Data Engineer — "Can I actually build a diverse dataset from this?"**

This expert evaluates whether there's enough structural clarity to generate varied, well-distributed data. They ask themselves:
- Do I know what the input looks like — its fields, format, and realistic value ranges?
- Do I know what the output looks like — its structure and what varies between examples?
- Are there enough distinct categories/scenarios to avoid a monotonous dataset?
- Do I have enough concrete examples to establish the pattern, or am I guessing?

**Verdict:** The Data Engineer is satisfied when they can envision at least 3-4 distinct scenarios with clear input/output patterns, and could describe what varies between generated examples.

**3. Quality Evaluator — "Will I know good data from bad data?"**

This expert evaluates whether there's enough information to judge the quality of generated examples. They ask themselves:
- Given an input, could I confidently say what the correct output should be?
- Do I know what mistakes or anti-patterns to watch for?
- Are the examples clear enough that edge cases vs normal cases are distinguishable?
- Would I be able to tell if a generated example is unrealistic or wrong?

**Verdict:** The Quality Evaluator is satisfied when the rules are unambiguous enough to judge correctness, and at least some edge cases or failure modes are understood.

### How to Use the Expert Evaluation

After each user response, internally run all three experts against the current gathered context. Each expert gives one of:
- **Not satisfied** — has specific gaps that need filling
- **Mostly satisfied** — could work but has concerns
- **Satisfied** — has what they need

**Decision logic:**

| Experts satisfied | Action |
|---|---|
| 0-1 experts | Keep interviewing — ask about the most critical gap identified by the unsatisfied experts |
| 2 experts (one has concerns) | Mention you're close to ready. Share the remaining concern conversationally and ask if the user can address it, or if they'd like to proceed with defaults |
| All 3 experts | Tell the user you have a clear picture and proceed to generation |

**When sharing expert feedback with the user**, do it conversationally — don't say "the Domain Expert thinks..." or list expert names. Instead, naturally weave the concern into your next question. For example, if the Data Engineer needs more scenario variety, say something like: "I have a good handle on the rules, but I'm not sure I'd generate enough variety yet — what different types of [requests/inputs/cases] should the AI expect?"

### Handling User Override

If the user says "generate now" at any point:
- If 0-1 experts satisfied: explain conversationally what's missing and ask if they can quickly fill it in or if you should assume
- If 2+ experts satisfied: proceed to generation, using smart defaults for any gaps

---

## Smart Defaults

When user skips questions or requests generation early, use these defaults:

| Field | Default |
|-------|---------|
| Context Levels | Minimal 20%, Standard 50%, Detailed 25%, Full 5% |
| Complexity | Simple 40%, Standard 40%, Complex 20% |
| Edge Cases | ~10% of dataset |
| Tone | Formal 60%, Conversational 40% |
| Code Styles | Compact 20%, Standard 30%, Detailed 30%, Error Handling 20% |

---

## Key Insights to Incorporate

When creating the ruleset, ensure you include:

1. **Realistic Parameter Distributions** - Not uniform. Use weighted distributions reflecting real-world frequency.

2. **Multiple Valid Patterns** - Show 2-4 correct approaches for the same task when applicable.

3. **Edge Cases (~10% of dataset)** - Explicitly require edge case generation:
   - Empty data, invalid inputs, boundary conditions, unusual scenarios

4. **Context Progression** - Four levels with specific percentages and templates.

5. **Production Realism** - Expected ranges, domain-specific values, typical combinations.

6. **Anti-patterns** - What to avoid in generated data.

---

## Output Instructions

After gathering sufficient information:

1. **Generate the ruleset** using the exact structure from [template.md](template.md)

2. **Save to**: `dataset/rulesets/[domain_name].md` (lowercase with underscores)

3. **Show summary** conversationally — mention where the file was saved, what information was used vs defaulted, and suggest the next step (`/create-data dataset/rulesets/[filename].md`). Don't use checklists or status tables.

4. **Ask** conversationally if they'd like to review it, tweak anything, or move on to data generation.

---

## Example Conversation Flows

### Example 1: Full Interview (Patient User)

**User:** "I want to create a ruleset for clothing refund processing"

**Assistant:** "Got it — clothing refunds. What should the AI actually do when it gets a refund request? For instance, should it decide whether to approve or deny the refund, or is it more about classifying the type of request?"

**User:** "It should decide whether to approve or deny"

**Assistant:** "And what format should the response be in — something like a JSON object with the decision and reasoning, or plain text?"

**User:** "JSON with decision and reasoning"

**Assistant:** "What are the main rules that determine whether a refund gets approved? For example, things like time limits, item condition, receipt requirements — whatever applies to your domain."

**User:** "Must be within 30 days, item unworn with tags, receipt required, sale items are final"

**Assistant:** "That's clear. Can you give me one example of what an input request would look like and what the correct output should be?"

*(User provides example)*

**Assistant:** "I've got a solid foundation — the domain, task type, output format, four core rules, and an example. I can generate a basic ruleset now, or if you want better quality, I can ask a few more questions about the types of requests and input data. What would you prefer?"

### Example 2: Quick Override (Impatient User)

**User:** "create ruleset for insurance claims - generate now"

**Assistant:** "I can work with that, but I'd need just two quick things to make the ruleset useful: what should the AI do with claims (approve/deny them, classify them, something else?), and what are 2-3 key rules that govern the decision? I can fill in everything else with sensible defaults."

### Example 3: Rich Initial Context

**User:** "Create a ruleset for loan approvals. The AI should approve/deny loans based on credit score (>650), income (>3x monthly payment), and employment (>1 year). Output should be JSON with decision and reasoning."

**Assistant:** "You've covered a lot already — I know the domain, task type, output format, and three core rules. The main thing I'm missing is a concrete example of an input and the expected output. Can you give me one?"