# Node Spec Template

Use this format for each node in the agent graph.

---

```markdown
# [Number] [Node Name]

**Model**: [e.g., GEMINI_25_FLASH_LITE, BEDROCK_CLAUDE_SONNET_4]
**On Error**: STOP | CONTINUE

## Purpose

[One sentence describing what this node does]

## Input Parameters

| # | Param | Type | Fill Type | Source Node | Source Param | Required |
|---|-------|------|-----------|------------|--------------|----------|
| 0 | param_name | string | ai_fill | — | — | true |
| 1 | linked_param | string | linked | N1 | output_name | true |
| 2 | optional_param | string | linked | N3 | some_output | false |

Fill types:
- `ai_fill` — first processing node receives task data this way
- `linked` — connected to upstream node's output (specify source)
- `static` — hardcoded value
- `user_fill` — user provides at runtime
- `from_memory` — from agent memory

## Output Parameters

| # | Param | Type | Array | Description | Example |
|---|-------|------|-------|-------------|---------|
| 0 | result | string | false | The main result | "product_complaint" |
| 1 | confidence | number | false | Confidence score 0-1 | 0.85 |

## Prompt

[Full LLM instruction text here]

Use Beam prompt rules:
- `{{variable}}` for template variables
- Escape literal braces as `{{` and `}}`
- No "output format" as section header
- Don't duplicate output schema in prompt body
- Markdown format, use `@topic` for unique keywords

## Edges (Outgoing)

| Target | Condition | Description |
|--------|-----------|-------------|
| N5 | `classification == "product_complaint"` | Product complaint path |
| N13 | `confidence < 0.70` | Low confidence → manual review |

## Notes

[Any special behavior, known issues, or implementation notes]
```
