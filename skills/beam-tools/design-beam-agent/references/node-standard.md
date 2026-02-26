# Beam.ai Node Standard Template

**Purpose**: Standard format for all Beam.ai agent node definitions.

---

## Node File Structure

Each node file follows this structure:

```markdown
# {Node ID} - {Node Name}

**Level**: {topological level in graph}
**Branch**: {branch number if parallel nodes}
**Tool Name**: {BeamToolIdentifier}

## Purpose

{1-2 sentence description of what this node does}

## Input Parameters

**{parameter_name}**: {description}
- Source: `${source_node.field}` or "User Input"
- Type: {string | number | boolean | object | array}

## Prompt

\`\`\`
{Complete prompt text with variables in {curly_braces}}
\`\`\`

## Output Parameters

**{output_name}**:
\`\`\`json
{
  "reasoning": "<string, Step-by-step analysis BEFORE extraction/conclusion>",
  "field_name": "<type, description>",
  ...
}
\`\`\`

## Rules (if validation node)

| ID | Name | Severity | Logic |
|----|------|----------|-------|
| X-001 | Rule Name | Critical/Warning/etc | Brief logic description |

## Examples

**Input**: {sample input}
**Expected Output**: {sample output}
```

---

## Prompt Design Principles

### 1. Reason-First Pattern (CRITICAL)
Always structure outputs with reasoning BEFORE conclusions:
```json
{
  "reasoning_for_field_x": "First explain the analysis",
  "field_x": "Then provide the extracted/calculated value"
}
```

### 2. Role Definition
Start every prompt with clear role:
```
# Role
You are a {specific expertise} specialist with deep knowledge of {domain}.
Your task is to {specific action}.
```

### 3. Context Section
Explain input structure:
```
# Document Context
This node receives {description of input}.
The data contains {key sections/fields}.
```

### 4. Rules Section
Define logic clearly:
```
# Rules
1. {Rule with specific instructions}
2. {Another rule with edge cases}
```

### 5. Variable Definitions
For each output field, include:
- Definition (what it means)
- Location (where to find in input)
- Format requirements
- Edge cases / disambiguation

### 6. Data Section
Reference input variables:
```
# Data
{variable_name}
```

---

## Node Linking Patterns

### Accessing Previous Node Output
```
${node_1_1.header.field_name}
${node_1_2.items[0].amount}
${node_2_1.validations[0].result}
```

### Accessing Arrays
```
${node_1_1.items}           // Full array
${node_1_1.items[0]}        // First item
${node_1_1.items[*].amount} // All amounts
```

---

## Standard Output Schemas

### Extraction Node Output
```json
{
  "reasoning_extraction": "<string, describe document structure and approach>",
  "extracted_data": {
    "field_1": "<value>",
    "field_2": "<value>"
  },
  "extraction_metadata": {
    "items_found": "<number>",
    "extraction_complete": "<boolean>",
    "warnings": ["<any issues encountered>"]
  }
}
```

### Validation Node Output
```json
{
  "validations": [
    {
      "reasoning": "<string, step-by-step analysis - MUST come first>",
      "rule_id": "<string, e.g., V-001>",
      "rule_name": "<string>",
      "result": "<enum: PASS | FAIL | WARNING | SKIP | NEEDS_REVIEW>",
      "severity": "<enum: Critical | Warning | Requires Approval | Info | Automatic>",
      "message": "<string, clear explanation>",
      "data_used": {},
      "failure_reason": "<string | null>",
      "suggested_action": "<string | null>",
      "adjusted_amount": "<number | null, for automatic calculations>"
    }
  ]
}
```

### Output/Report Node Output
```json
{
  "human_readable_report": "<string, formatted report for display>",
  "report_metadata": {
    "report_id": "<string>",
    "generated_at": "<ISO timestamp>",
    "processing_time_ms": "<number>"
  },
  "summary": {
    "overall_status": "<enum: APPROVED | NEEDS_REVIEW | REJECTED>",
    "total_rules": "<number>",
    "passed": "<number>",
    "failed": "<number>"
  },
  "details": {}
}
```

---

## Result Definitions

| Result | Meaning | Next Step |
|--------|---------|-----------|
| **PASS** | Validation passed | Continue |
| **FAIL** | Validation failed | Apply severity action |
| **WARNING** | Minor issue | Log and continue |
| **SKIP** | Not applicable | Skip this rule |
| **NEEDS_REVIEW** | Manual review needed | Route to reviewer |

---

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Must reject/block | Stop processing, notify |
| **Requires Approval** | Cannot auto-approve | Route to approver |
| **Warning** | Policy concern | Process but flag |
| **Info** | Informational | Log only |
| **Automatic** | System handles | Apply calculation |

---

## File Naming Convention

Nodes are named with level and sequence:
- `1.1-{Node-Name}.md` (first extraction node)
- `1.2-{Node-Name}.md` (parallel extraction node)
- `2.1-{Node-Name}.md` (first processing node)
- `3.1-{Node-Name}.md` (output node)

---

## GRAPH.md Template

Every agent needs a `GRAPH.md` overview file:

```markdown
# {Agent Name} - Graph Overview

**Agent Name**: {name}
**Total Nodes**: {N}
**Created**: {date}

---

## Agent Topology

\`\`\`mermaid
flowchart TD
    subgraph Input["Input"]
        IN["Input Data"]
    end

    subgraph L1["Level 1: Extraction"]
        N1_1["1.1 {Node Name}"]
    end

    subgraph L2["Level 2: Processing"]
        N2_1["2.1 {Node Name}"]
    end

    subgraph L3["Level 3: Output"]
        N3_1["3.1 {Node Name}"]
    end

    IN --> N1_1
    N1_1 --> N2_1
    N2_1 --> N3_1
\`\`\`

---

## Node Index

| Node | Name | Level | Type | File |
|------|------|-------|------|------|
| 1.1 | {Name} | 1 | Extraction | [1.1-{Name}.md](1.1-{Name}.md) |

---

## Data Flow

\`\`\`
node_1_1.output → node_2_1
node_2_1.output → node_3_1
\`\`\`

---

## External Dependencies

| Rule/Node | External System | Data Needed |
|-----------|-----------------|-------------|
| {rule} | {system} | {data} |
```

---

*Use this standard for all node definitions in Beam.ai agents.*
