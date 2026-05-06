---
name: beam-ape-optimizer
version: '1.0'
description: Automated Prompt Engineering (APE) optimization loop for Beam agent nodes.
  Adds reasoning traces, runs test batches against a golden dataset, uses 3-agent
  credit assignment (Doer/Critic/Editor) to identify and fix failing prompt instructions,
  and redeploys improved prompts. Use when user says "optimize prompts", "APE loop",
  "improve beam agent accuracy", "prompt engineering", "test and fix prompts",
  "run APE", "credit assignment", or when agent accuracy needs systematic improvement
  rather than manual prompt editing.
author: Abdul Rafay
category: integrations
tags:
- api
- beam-ai
- optimization
- prompt-engineering
platform: Beam AI
updated: '2026-03-15'
visibility: team
---

# Beam APE Optimizer

Systematic prompt optimization for Beam agent nodes using Automated Prompt Engineering (APE). Runs test batches, identifies which prompt instructions cause failures, and surgically rewrites only the failing parts.

## Prerequisites

- A deployed Beam agent with nodes to optimize
- A test dataset with ground truth (e.g., golden dataset with verified classifications)
- Agent ID and node IDs for target nodes
- Beam API credentials in `.env`

## Workflow

### Step 1: Add Reasoning to Target Nodes

For each node being optimized, add a `reasoning` output parameter:

| Param | Type | Description |
|-------|------|-------------|
| `reasoning` | string | Step-by-step chain-of-thought explaining each decision |

Append reasoning instructions to the node's prompt (before the Input section):

```
# Reasoning
Before producing your outputs, think through each step:
1. [Step specific to this node's task]
2. [Another step]
3. [Final decision step]
Write your full reasoning in the 'reasoning' output.
```

**Why reasoning only (no combined_output):** APE analyzes each node's prompt independently. We need to see WHY the model made each decision, then compare individual outputs against ground truth. Aggregating outputs at the exit node adds complexity without value — each node is analyzed separately.

Deploy reasoning additions:
1. PATCH prompt with appended reasoning instructions
2. PATCH input-output-params to add `reasoning` output
3. Publish

### Step 2: Analyze Test Dataset for Coverage

Before running tests, analyze the dataset to ensure maximum coverage with minimum samples:

1. **Map categories** — list all classifications, edge types, and routing paths in the agent
2. **Count samples per category** — how many test cases cover each path
3. **Select minimum representative sample** — pick the fewest samples that cover ALL categories
4. **If minimum > 15 samples**: split into chunks of 10-15
   - Chunk 1: run first, iterate prompts based on results
   - Chunk 2+: run with updated prompts (fresh samples prevent overfitting)

Output a coverage table:

```markdown
| Category | Count | Selected Samples |
|----------|-------|-----------------|
| product_complaint | 12 | GD-44, GD-52 |
| spare_parts | 8 | GD-88, GD-91 |
| missing_info | 5 | GD-38 |
| ... | ... | ... |
```

### Step 3: Run Test Batch

Run selected samples one at a time (concurrent tasks cause input corruption):

```bash
python3 04-workspace/scripts/trigger_beam_task.py \
  --agent {AGENT_ID} \
  --msg "path/to/sample.msg" \
  --poll --poll-timeout 600
```

For each completed task, collect:
- Node-level outputs (the fields being validated)
- `reasoning` output (the chain-of-thought trace)
- Task ID for reference

**CRITICAL: Never rerun tasks without explicit user approval.** Present all results first, report stuck/failed tasks, and wait for the user to say "rerun".

### Step 4: Compare Against Ground Truth

For each test case, compare node outputs against ground truth:

**Ground truth precedence (if using reviewed dataset):**
1. Review comments that correct the original → corrected value is ground truth
2. Review comments that confirm "CORRECT" → original value is ground truth
3. No review → original value is ground truth (flag as unverified)

Create a results table:

```markdown
| Sample | Expected | Got | Match | Node | Reasoning Summary |
|--------|----------|-----|-------|------|-------------------|
| GD-44 | product_complaint | product_complaint | PASS | N4 | — |
| GD-38 | missing_info | spare_parts | FAIL | N4 | "Found product ref..." |
```

### Step 5: Credit Assignment — 3-Agent System

For each MISMATCH, run the Critic and Editor agents.

#### Agent 1: Doer (Already Done)

The Beam agent itself is the Doer. The `reasoning` output is the chain-of-thought trace.

#### Agent 2: Critic

A Claude prompt that takes the failing node's prompt + reasoning + output + ground truth, and assigns credit to each instruction:

**Input:**
- Node prompt (segmented into numbered instructions)
- Reasoning trace from the test run
- Model output (what it produced)
- Ground truth (correct answer)

**Output:** Per-instruction labels:
- `KEEP` — instruction followed correctly
- `MODIFY` — instruction contributed to the error (with explanation)
- `NEUTRAL` — instruction not relevant to this error

See [references/critic-prompt.md](references/critic-prompt.md) for the full Critic prompt template.

#### Agent 3: Editor

Takes the Critic's output and rewrites ONLY the `MODIFY` instructions:

**Rules:**
- Never change `KEEP` instructions
- Rewrite `MODIFY` instructions using failure reasoning as guide
- Be specific — vague instructions cause model errors
- Add examples where the model was confused
- Keep the same overall structure and section ordering

See [references/editor-prompt.md](references/editor-prompt.md) for the full Editor prompt template.

### Step 6: Redeploy and Retest

1. PATCH updated prompt to Beam
2. Publish
3. Run the SAME test cases again (to verify fix, not regression)
4. Also run next chunk of fresh samples (to verify generalization)
5. Compare accuracy: did it improve without regression?

### Step 7: Iterate Until Convergence

**Convergence criteria:**
- Target accuracy: 90%+ correct on test batch
- No regressions: previously correct cases must stay correct
- Max iterations: 5 per node (diminishing returns after that)

**Iteration order:**
1. Start with the node that has the most impact on final output
2. Then upstream nodes (errors propagate downstream)
3. After individual nodes stabilize, check for cross-node propagation errors

**Prompt versioning:** Save each version:
```
plan/prompt-versions/
  n1-v1.txt, n1-v2.txt, ...
  n4-v1.txt, n4-v2.txt, ...
```

**Results tracking:**
```markdown
| Iteration | Node | Accuracy | Changes | Regressions |
|-----------|------|----------|---------|-------------|
| v1 (baseline) | N4 | 7/10 | — | — |
| v2 | N4 | 8/10 | Rule 2 rewrite | 0 |
| v3 | N4 | 9/10 | Added examples | 0 |
```

## References

- **[critic-prompt.md](references/critic-prompt.md)** — Full Critic agent prompt template
- **[editor-prompt.md](references/editor-prompt.md)** — Full Editor agent prompt template
- **beam-agent-manager** — PATCH workflows, publishing rules, API behavioral rules
- **beam-get-task-details** — Fetch detailed task output for analysis

## Related Skills

- `beam-graph-creator` — Create and deploy the agent graph (do this before APE)
- `beam-agent-manager` — API rules and PATCH/publish workflows
