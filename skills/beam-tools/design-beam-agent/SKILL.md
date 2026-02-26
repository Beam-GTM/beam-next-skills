---
name: design-beam-agent
version: '1.0'
description: Design complete Beam.ai agent node architecture from a scoping document.
  Load when user says "design beam agent", "create beam agent", "agent design for
  [name]", or needs to plan a multi-node Beam.ai agent workflow. Requires a completed
  agent-scoping document as input.
category: general
updated: '2025-12-10'
visibility: team
---
# Design Beam Agent

Create complete Beam.ai agent architecture with node definitions, prompts, and data flow from a structured scoping document.

## Prerequisites

**Before running this skill**, user must have a completed Agent Scoping Document containing:
- Agent name and purpose
- Input/output specifications
- Processing rules with severities
- Node architecture (phases, node inventory, data flow)
- At least one example input

**Template**: See [agent-scoping-template.md](references/agent-scoping-template.md)

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with workflow steps:
```
- [ ] Validate scoping document completeness
- [ ] Create project structure in 04-workspace/agents/
- [ ] Generate GRAPH.md overview
- [ ] Generate extraction nodes (Level 1)
- [ ] Generate processing/validation nodes (Level 2)
- [ ] Generate output node (Level 3)
- [ ] Create README.md
- [ ] Validate rule coverage
```

---

### Step 2: Validate Scoping Document

1. **Locate scoping document** - Ask user for path or check:
   - `04-workspace/agents/{agent-name}/scoping.md`
   - Current project's `02-resources/`
   - User-provided path

2. **Validate required sections**:
   - [ ] Agent Overview (name, purpose, constraints)
   - [ ] Input Specification (format, structure, fields)
   - [ ] Output Specification (schema, requirements)
   - [ ] Processing Rules (categories, rule definitions, severities)
   - [ ] Node Architecture (phases, inventory, data flow)
   - [ ] Example Input

3. **If incomplete**: Guide user to complete missing sections using [agent-scoping-template.md](references/agent-scoping-template.md).

**Mark this todo complete before proceeding.**

---

### Step 3: Create Project Structure

Create agent project in workspace:

```
04-workspace/agents/{agent-name}/
├── scoping.md              # Copy/link scoping document
├── nodes/
│   ├── GRAPH.md            # Agent topology overview
│   ├── 1.1-{Name}.md       # Extraction nodes
│   ├── 2.1-{Name}.md       # Processing/validation nodes
│   └── 3.1-{Name}.md       # Output node
└── README.md               # Agent summary
```

```bash
mkdir -p "04-workspace/agents/{agent-name}/nodes"
```

**Mark this todo complete before proceeding.**

---

### Step 4: Generate GRAPH.md

Create agent overview using [node-standard.md](references/node-standard.md) GRAPH.md template:

1. Extract from scoping document:
   - Agent name and purpose
   - Node inventory table
   - Mermaid flowchart from data flow section
   - External dependencies

2. Generate `nodes/GRAPH.md` with:
   - Agent metadata (name, node count, date)
   - Mermaid topology diagram
   - Node index with links to node files
   - Data flow summary
   - External dependencies table

**Mark this todo complete before proceeding.**

---

### Step 5: Generate Node Files

For each node in the inventory, create a node file following [node-standard.md](references/node-standard.md).

#### Extraction Nodes (Level 1)
- Purpose: Parse input and extract structured data
- Output: JSON with extracted fields + `reasoning_extraction`
- Include: Field definitions, location hints, format rules

**Prompt structure**:
```
# Role
You are a precise data extraction specialist...

# Document Context
You are processing {input type} containing {sections}...

# Extraction Rules
1. Extract ONLY what is explicitly stated
2. {Format conversions}
3. {Field-specific rules}

# Variables
### {field_name}
**Definition**: {what it is}
**Location**: {where to find}
**Format**: {expected format}

# Data
{input_variable}
```

#### Processing/Validation Nodes (Level 2)
- Purpose: Apply rules from scoping document
- Output: Array of validation results with `reasoning` first
- Include: Rule table, severity definitions, policy references

**Prompt structure**:
```
# Role
You are a {domain} compliance specialist...

# Task
Validate the following rules against the extracted data:
{rule table}

# Validation Logic
For each rule:
1. State the rule requirement
2. Identify relevant data
3. Apply the logic
4. Determine result (PASS/FAIL/WARNING/SKIP/NEEDS_REVIEW)

# Data
{previous_node_outputs}
```

#### Output Nodes (Level 3)
- Purpose: Aggregate results into final output
- Output: Report with `human_readable_report` + structured data
- Include: Status determination logic, summary statistics

**Status logic**:
```
IF any Critical FAIL → REJECTED
ELSE IF any NEEDS_REVIEW → NEEDS_REVIEW
ELSE → APPROVED
```

**Mark this todo complete before proceeding.**

---

### Step 6: Create README

Generate `README.md` summarizing:
- Agent purpose
- Node count and architecture
- Input requirements
- Output format
- How to deploy to Beam.ai

**Mark this todo complete before proceeding.**

---

### Step 7: Validate Coverage

Cross-check that all rules from scoping document are covered:

1. List all rules from scoping `Processing Rules` section
2. For each node, list rules it implements
3. Create coverage matrix
4. Flag any uncovered rules

Output validation summary:
```
Total Rules: {N}
Covered: {N}
Uncovered: {list any gaps}
```

**Mark this todo complete before proceeding.**

---

## Output Checklist

After completing this skill, verify:
- [ ] `04-workspace/agents/{agent-name}/` directory exists
- [ ] `scoping.md` present
- [ ] `nodes/GRAPH.md` with topology
- [ ] All node files created per inventory
- [ ] Each node has: Purpose, Input, Prompt, Output, Examples
- [ ] All rules from scoping covered
- [ ] README.md with summary

---

## Beam.ai Documentation

- Variables & State: https://docs.beam.ai/02-building-agents/agent-configuration/variables-state/variables-state
- Structured Outputs: https://docs.beam.ai/02-building-agents/agent-configuration/structured-outputs/structured-outputs
- Agent Configuration: https://docs.beam.ai/02-building-agents/agent-configuration
