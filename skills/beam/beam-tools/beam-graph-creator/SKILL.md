---
name: beam-graph-creator
version: '1.0'
description: Build and deploy complete Beam agent graphs with conditional branching,
  convergence nodes, and multi-path routing. Takes a specification document and flowchart
  (builds flowchart on Miro if not provided), designs all nodes/edges/params, deploys
  via PUT/PATCH, and validates with test data. Use when user says "create beam agent
  graph", "build beam graph", "deploy agent", "new beam agent", "build graph from
  spec", "create nodes and edges", or needs to go from a specification document to
  a working deployed agent on Beam.
author: Abdul Rafay
category: integrations
tags:
- api
- beam-ai
- graph
- create
platform: Beam AI
updated: '2026-03-15'
visibility: team
---

# Beam Graph Creator

Build and deploy complete Beam agent graphs from a specification document and flowchart. Handles the full lifecycle: flowchart → node design → API deployment → validation.

## Prerequisites

- A specification document describing business rules, classifications, routing logic
- A flowchart on Miro (or the skill builds one from the spec)
- Beam API credentials in `.env` (`BEAM_API_KEY`, `BEAM_WORKSPACE_ID`)
- Optional: existing node specs (if modifying an existing agent)
- Optional: test dataset for validation (golden dataset with ground truth)

## Workflow

### Step 1: Review Specification Document

Read the specification document and extract:

1. **Business rules** — what rules drive routing decisions
2. **Classifications/categories** — what types of input exist and how they're categorized
3. **Routing logic** — which classification leads to which action
4. **Data requirements** — what fields need to flow between nodes
5. **External dependencies** — DB lookups, API calls, email sending, etc.

If the spec is incomplete, ask the user to fill gaps before proceeding.

### Step 2: Build or Verify Flowchart

**If flowchart exists on Miro:**
- Read the Miro board using Miro MCP tools
- Verify it matches the specification (all rules covered, all paths represented)
- Note any gaps between spec and flowchart

**If no flowchart exists:**
- Build one from the specification using Miro MCP `diagram_create`
- Use the DSL format: nodes (`n# label object color`), connectors (`c src text tgt`), clusters
- Include all conditional branches, convergence points, and exit paths
- Present to user for review before proceeding

The flowchart is the source of truth for graph topology. Every node and edge in the final agent must trace back to this flowchart.

### Step 3: Design Node Registry

From the flowchart, create a node registry table:

```markdown
| Node | Name | Type | Description | Model |
|------|------|------|-------------|-------|
| N0 | Entry | Entry | Auto-created by Beam | — |
| N1 | [Name] | Processing | [What it does] | [Model] |
| ... | ... | ... | ... | ... |
```

For each processing node, define:
- **Objective** — one sentence describing purpose
- **Input params** — name, type, fillType (ai_fill for first node, linked for downstream)
- **Output params** — name, type, description
- **Prompt** — full LLM instruction text
- **Model** — selected via `select-llm-model` or user preference

Use `references/node-template.md` for the node spec format.

### Step 4: Design Edge Registry

From the flowchart, create an edge registry with conditions:

```markdown
| # | From | To | Condition | Description |
|---|------|----|-----------|-------------|
| E1 | N0 | N1 | always | Entry → first processing node |
| E2 | N1 | N2 | `field == "value"` | Conditional branch |
```

Rules for edges:
- Every edge must appear in BOTH source's `childEdges[]` AND target's `parentEdges[]`
- Conditions must be mutually exclusive or have evaluation priority
- Convergence nodes (multiple parents) should use `required: false` on path-dependent inputs
- Identify convergence nodes explicitly (nodes with 2+ parent edges)

### Step 5: Create Node Spec Files

Write each node's spec as a markdown file following this structure:

```markdown
# [Node Number] [Node Name]

## Purpose
[One sentence]

## Input Parameters
| Param | Type | Fill Type | Source | Required |
|-------|------|-----------|--------|----------|

## Output Parameters
| Param | Type | Array | Description |
|-------|------|-------|-------------|

## Prompt
[Full LLM instruction text]

## Edges
| Target | Condition |
|--------|-----------|
```

Store in `04-workspace/clients/{client}/agents/{agent-name}/nodes/`.

### Step 6: Deploy to Beam API

**6a. Build PUT payload:**
- If creating from scratch: use `beam-api-reader` → `create_agent_from_prompt.py`
- If modifying existing agent: use `beam-put-payload-builder` to transform GET→PUT

**6b. Send PUT:**
- PUT `/agent-graphs/{agentId}` with full graph payload
- Verify response — GET graph to confirm all nodes and edges persisted

**6c. PATCH prompts, models, params:**
- PUT does NOT propagate to `originalTool` — must PATCH each node
- Order: PATCH prompts first, then models, then params
- For params: go upstream → downstream (UUIDs regenerate on each PATCH)
- Re-fetch graph between each PATCH

**6d. Publish:**
- `PATCH /agent-graphs/{graphId}/publish`
- GET fresh graph after publish (all UUIDs regenerated)

Consult `beam-agent-manager` → `references/api-rules.md` for all API behavioral rules.

### Step 7: Validate with Test Data

If a test dataset is available (e.g., golden dataset with ground truth):

1. **Analyze dataset coverage** — map which classifications/paths each sample covers
2. **Select minimum representative sample** — cover all categories with fewest samples
3. **Run test batch** — trigger tasks one at a time (concurrent tasks cause corruption)
4. **Compare outputs vs ground truth** — classification, key fields, routing decisions
5. **Report accuracy** — pass/fail per category, overall accuracy percentage
6. **If failures detected**: note which nodes/prompts need adjustment (use `beam-ape-optimizer` for systematic prompt improvement)

## Common Patterns

### Conditional Branching

When a node routes to different targets based on output:
- Add a `routing_decision` output param that encodes the combined logic
- Each edge condition checks this single field
- Example: `routing_decision == "classify"` → N4, `routing_decision == "manual_review"` → N13

### Convergence Nodes

When multiple paths merge into one node:
- Mark path-dependent inputs as `required: false`
- The node prompt should handle missing inputs gracefully
- Example: N12 (Response Assembly) receives from N6, N7, N8, N9, N10, N11

### Mock Nodes

For dependencies not yet available (DB lookups, external APIs):
- Create a mock node with static/happy-path outputs
- Mark as `MOCK` in the node registry
- Replace with real implementation in Phase 2

## References

- **[node-template.md](references/node-template.md)** — Standard node spec format
- **beam-agent-manager** — API rules, PUT vs PATCH decision, publishing workflow
- **beam-put-payload-builder** — GET→PUT payload transformation
- **beam-api-reader** — Full API endpoint reference and agent creation from YAML
- **select-llm-model** — Model selection guidance
- **graph-slicer** — Extract deployed nodes back to files for review

## Related Skills

- `beam-ape-optimizer` — Systematic prompt optimization after initial deployment
- `design-beam-agent` — Simpler design-only tool for linear 3-level agents (no API deployment)
