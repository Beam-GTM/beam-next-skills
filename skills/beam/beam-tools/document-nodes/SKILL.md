---
name: document-nodes
version: '1.0'
description: Generate human-readable documentation and checklists from Node JSON files.
  Use when asked to document nodes, create checklists for node processing, or explain
  node extraction logic. Processes all nodes in the Nodes directory systematically.
category: general
updated: '2025-12-10'
visibility: team
---
# Document Nodes

Generate human-readable English documentation with execution checklists from Node JSON files containing AI extraction prompts.

## When to Use

- User asks to "document nodes" or "create documentation for nodes"
- User wants checklists for processing documents through nodes
- User needs to explain node extraction logic to non-technical staff
- After creating or updating node JSON files

## Workflow

### 1. Find All Nodes

Glob for all JSON files in the Nodes directory:
```
C:\Users\dsber\BID\Nodes\*.json
```

Read each node file to get:
- Node name (filename without extension)
- Full prompt text (inside `prompt` field)
- Output schema structure

### 2. Process Each Node

For each node, analyze the prompt to extract:

**Core Information:**
- Node purpose (what it does, metaphor/analogy)
- Document type it processes (bank letters, TZV forms, debtor letters, etc.)
- Input requirements
- Output variables (count and types)
- Next routing destination

**Extraction Logic:**
- Variables to extract with descriptions
- Critical disambiguation rules (edge cases, common mistakes)
- Keywords for status determination
- Format transformations (German → English formats, dates, amounts)
- Hierarchies or ordering requirements
- Percentage/frequency notes (e.g., "80% of forms have empty field")

**Decision Patterns:**
- IF-THEN logic
- Keyword matching rules
- Validation criteria
- Special cases

### 3. Generate English Documentation

Create markdown file in `Documentation/` folder with this structure:

#### Part 1: Overview Section

```markdown
# Node X: [Name]

## Description

[2-3 sentence description of what this node does]

**Metaphor:** [Simple analogy to explain the role]

## System Flow

[Mermaid diagram showing input → node → output]

## Input and Output

**Input:**
- [List inputs]

**Output:**
- [List output variables with brief descriptions]

**Comes from:** [Previous node]

**Goes to:** [Next node or "End"]

---

## Extracted Variables

[Table with: Variable | Description | Possible Values]

---

## [Specific Logic Sections]

[Flowcharts and explanations of key decision logic]

### Critical Distinction Rules

[Any disambiguation rules, edge cases, or common mistakes]

---

## Validation Examples

[2-3 examples showing expected inputs and outputs]

---

## Technical Reference

**Node File:** `[filename].json`

**Input:** [List]

**Output:** [List]

**Routes to:** [Next node]

**Special notes:**
- [Key characteristics, complexity notes, critical rules]

---
```

#### Part 2: Processing Checklist

Append a comprehensive checklist following the pattern in [references/checklist-pattern.md](references/checklist-pattern.md).

The checklist MUST include:

**Standard Structure:**
1. 🎯 **Application** section - How to use the checklist
2. 📝 **Step-by-step sections** with:
   - Emoji headers for each major step
   - Checkbox format: `- [ ] Description`
   - Clear decision points with **"IF THIS, STOP HERE"** instructions
   - Examples with ✓/✗ notation
3. 🔍 **Validation section** - Critical checkpoints
4. 📋 **"TOP X Errors" section** - Most common mistakes
5. ✅ **Final Confirmation** - Summary checklist before completion
6. 📞 **"When Uncertain" section** - What to do if unclear

**Checklist Guidelines:**
- Write in imperative form
- Use blockquotes `>` for critical warnings: `> **⚠️ CRITICAL:** [rule]`
- Include fill-in blanks: `Variable = ________`
- Show format transformations: Input → Output
- Provide concrete examples for each decision branch
- Number subsections when there are multiple options (S1, S2, S3 or B1, B2, B3)

### 4. Save Documentation

Save to: `C:\Users\dsber\BID\Documentation\[node-number]-[node-name].md`

Naming pattern:
- `00-System-Overview.md`
- `01-Node-0-Receptionist.md`
- `02-Node-1a-Bank-Correspondence.md`
- `03-Node-1b-TZV-Form.md`
- etc.

## Output Language

**All documentation MUST be in ENGLISH**, even if the source prompts or example content are in German. Translate:
- Section headers
- Instructions
- Examples
- Variable descriptions
- Error messages

German proper nouns (e.g., "TZV", "Dauerauftrag") can be kept with English explanation in parentheses.

## Processing Multiple Nodes

When processing all nodes:
1. Use TodoWrite to track progress (one todo per node)
2. Process nodes in order (0, 1a, 1b, 1c, 2c1, 2c2)
3. Mark each complete after saving documentation
4. Report summary at end: "Documented X nodes: [list]"

## Quality Checks

Before completing each node documentation:

- [ ] Overview section clearly explains purpose
- [ ] All variables from prompt are documented
- [ ] Critical rules are highlighted in checklist
- [ ] Examples show expected inputs/outputs
- [ ] Checklist follows proven pattern (emojis, checkboxes, STOP HERE, TOP errors)
- [ ] Language is English throughout
- [ ] File saved with correct naming pattern
