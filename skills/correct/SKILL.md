---
name: correct
description: "Capture a bad AI output and what was wrong. Use when AI produces something incorrect. Triggers: /correct, 'that was wrong', 'don't do that again', 'fix this pattern'."
category: micro
---

# /correct

Capture a mistake to avoid repeating it.

## Usage

User provides:
1. **Bad output** — the thing that was wrong
2. **What was wrong** — why it didn't work
3. **Correct approach** (optional) — how to do it right

## Workflow

### Step 1: Gather Information

Ask user (if not provided):
- "What did I get wrong?"
- "Why was it wrong?"
- "How should I have done it?"

### Step 2: Categorize

Determine which section in corrections.md:
- **Voice & Tone** — brand voice, personality, style issues
- **Content Patterns** — structure, format, messaging issues
- **Anti-Patterns** — things that definitely don't work
- **Technical Corrections** — code, implementation issues
- **Strategic Corrections** — decision-making, prioritization issues

### Step 3: Format & Append

Add to `01-memory/corrections.md` under appropriate section:

```markdown
### {DATE} - {Short Title}
**Bad**: {the problematic output}
**Why Wrong**: {explanation}
**Correct Approach**: {how to do it right}
```

### Step 4: Confirm

Tell user: "Got it. Added to corrections — won't make that mistake again."

## Example

**User**: "/correct"
**AI**: "What went wrong?"
**User**: "That LinkedIn post started with 'I am pleased to announce' — way too corporate"
**AI**: "Got it. How should I write openings instead?"
**User**: "Conversational, direct. Like 'We just shipped something big.'"

**Result** (added to corrections.md):
```markdown
### 2026-01-08 - Corporate LinkedIn Opening
**Bad**: "I am pleased to announce that our organization..."
**Why Wrong**: Too formal, corporate speak. Doesn't match Jonas's conversational voice.
**Correct Approach**: Direct, casual openings. "We just shipped..." or "Here's what I learned..."
```

---

*Micro-skill: Single-file, no folder needed. Fast capture, lasting improvement.*
