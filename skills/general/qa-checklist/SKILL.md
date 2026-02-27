---
name: qa-checklist
version: '1.0'
description: Transform technical agent/node documentation into business-owner cheatsheets.
  Use when asked to create "cheatsheet", "review guide", "QA checklist", "validation
  guide", or when business owners need to verify AI decisions. Applies better-doc
  principles. Outputs outcome-focused documents without technical/node details.
author: Jack Li
category: general
updated: '2025-12-17'
visibility: public
---
# QA Checklist

Transform technical AI documentation into simple cheatsheets for business process owners.

## Philosophy

**Business owners don't care about nodes, agents, or variables.**

They care about:
- "Is this outcome correct?"
- "What should I look for?"
- "When is it wrong?"

Output answers: **"I see outcome X. Was the AI right?"**

## When to Use

- Business owner needs to review AI decisions
- QA team needs validation checklist
- Anyone asks for "cheatsheet", "review guide", "validation guide"

## Workflow

### 1. Read Source Documentation

Accept any technical input:
- Agent node files (JSON/MD)
- Decision logic, routing rules
- Workflow diagrams
- Existing technical docs

### 2. Identify All Outcomes

List every possible final outcome the AI can produce:
- Classifications
- Extracted values
- Routing decisions
- Actions taken

**Flatten to outcomes only** - no node/step structure.

### 3. For Each Outcome, Extract

| From Technical Docs | Transform To |
|---------------------|--------------|
| Decision variables | "Must contain" conditions |
| Keywords/phrases | Direct quotes |
| IF-THEN logic | "When correct?" description |
| Edge cases, exclusions | "Wrong if" scenarios |

### 4. Apply Better-Doc Principles

Load [better-doc skill](../better-doc/SKILL.md) and apply:

**Classical Style:**
- Direct language, active voice
- Necessary content only
- Specific over abstract

**Smart Brevity:**
- Short words win
- Cut filler
- Scannable structure

**Remove:**
- Node numbers, agent names
- Variable names (bIsFoa, hasKeywords_tars)
- Technical flow descriptions
- Mermaid diagrams, JSON schemas

**Keep:**
- Keywords in original language (appear in real documents)
- Simple logic ("contains X AND Y")
- Concrete examples

### 5. Write Output

**Structure per outcome:**

```markdown
## [Outcome Name]

**When correct?** [One sentence - plain language]

**Must contain (at least one):**
- [Keyword/condition 1]
- [Keyword/condition 2]

**Wrong if:**
- [Scenario 1]
- [Scenario 2]
```

**End with quick lookup:**

```markdown
## Quick Check

| I see... | Expected Outcome |
|----------|------------------|
| [Trigger] | [Outcome] |
```

### 6. Language

**Match the user's language or business context.**

- If user speaks English → English cheatsheet
- If user speaks German → German cheatsheet
- If documents are in German but user wants English → English structure, quote German keywords

Keywords from source documents stay in original language (they appear in real documents users review).

## Quality Checklist

- [ ] Zero node/agent references
- [ ] Zero variable names
- [ ] Every outcome has: When correct? + Must contain + Wrong if
- [ ] Keywords quoted from source (original language)
- [ ] Quick reference table at end
- [ ] Better-doc applied (direct, scannable, necessary only)

## Example

**Technical Input:**
```
Node 3.1: hasKeywords_Nullplan_tars = true triggers Nullplan.
IF nInstalmentAmount = 0 AND NOT bIsFoa THEN Nullplan
```

**Business Output (English):**
```markdown
## Nullplan

**When correct?** Debtor cannot pay anything.

**Must contain (at least one):**
- "Nullplan" or "flexibler Nullplan"
- Payment amount = 0.00 EUR

**Wrong if:**
- Payment amount > 0 EUR
- Only a request for account statement
```

**Business Output (German):**
```markdown
## Nullplan

**Wann richtig?** Schuldner kann nichts zahlen.

**Muss enthalten (mindestens eines):**
- "Nullplan" oder "flexibler Nullplan"
- Zahlungsbetrag = 0,00 EUR

**Falsch wenn:**
- Zahlungsbetrag > 0 EUR
- Nur Anfrage nach Forderungsaufstellung
```
