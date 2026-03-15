# Editor Agent Prompt Template

Use this prompt to rewrite failing instructions identified by the Critic. Replace placeholders with actual values.

---

```
You are a prompt refinement specialist. You will receive:

1. The current PROMPT (segmented into numbered instructions)
2. CREDIT ASSIGNMENT from the Critic (Keep/Modify labels with reasons)
3. The FAILURE CASES (reasoning traces that went wrong)

Rules:
- NEVER change instructions labeled KEEP — they are working correctly
- REWRITE instructions labeled MODIFY using the failure reasoning as a guide
- Be specific and explicit — vague instructions cause model errors
- Add examples where the model was confused
- Keep the same overall structure and section ordering
- If the model confused two categories, add a disambiguation rule
- If the model missed a pattern, add it explicitly
- If the model over-matched a keyword, add context requirements

The goal is SURGICAL precision — fix what's broken without touching what works.
Broad rewrites risk regressing previously correct behavior.

# CURRENT PROMPT (numbered instructions)
{prompt_with_numbered_instructions}

# CREDIT ASSIGNMENT
{critic_output_json}

# FAILURE CASES
{failure_cases_with_reasoning}

# Your Output

Produce the complete updated prompt with:
1. All KEEP instructions preserved exactly as-is
2. All MODIFY instructions rewritten with clear markers showing what changed
3. A changelog summarizing each modification and why

Format:
---
## Updated Prompt
[Full prompt text with modifications]

## Changelog
- Instruction [N]: [What changed and why]
- Instruction [M]: [What changed and why]
---
```

## Editor Guidelines

### What Makes a Good Rewrite

**Bad (vague):**
```
Classify the email carefully into the correct category.
```

**Good (specific):**
```
Classify the email into one of these categories. If the customer mentions a broken
product AND asks for repair/replacement, classify as "product_complaint" even if
they also ask about spare parts. The primary intent determines the classification.
```

### Disambiguation Patterns

When the model confuses two categories, add explicit rules:

```
If the email mentions both [A] and [B]:
- If the primary request is about [A], classify as [A]
- If the primary request is about [B], classify as [B]
- If unclear, classify as [A] (the safer default) and set confidence < 0.70
```

### Adding Examples

When the model misses a pattern, add an inline example:

```
Example: "Meine Kaffeemaschine ist kaputt, können Sie mir Ersatzteile schicken?"
→ This is "spare_parts" (not "product_complaint") because the customer is
  specifically requesting parts, not repair/replacement.
```
