---
name: beam-credit-analysis
version: '1.1'
description: Analyze Beam.ai agent credit consumption per execution path. Load when
  user says 'credit analysis', 'beam credit analysis', 'agent credit consumption',
  'how many credits does this agent use', 'cost per path', 'analyze agent credits',
  'credit breakdown', or provides a Beam agent URL and asks about credits or cost.
author: Hassaan Ahmed
category: general
tags:
- beam-ai
- pricing
- analytics
platform: Beam AI
updated: '2026-03-11'
visibility: team
---

# Beam Credit Analysis

Analyze a Beam.ai agent's credit consumption and cost across all execution paths, based on the latest Beam pricing model.

## Purpose

Given a Beam agent URL (or graph JSON), this skill:
1. Fetches the agent graph from the Beam API
2. Traces all possible execution paths from entry to exit
3. Generates a mermaid flow diagram of the architecture
4. Calculates node counts, credit consumption, and cost per path
5. Produces a structured markdown report with per-branch breakdowns

**Pricing source:** [Beam Credits (New Agent OS)](https://www.notion.so/joinbeam/Beam-Credits-New-Agent-OS-3062cadfbbbc8198afeae750cb9e292f)

**Time Estimate**: 2-3 minutes

---

## Workflow

### Step 1: Get Agent URL

Ask user for the Beam agent URL. Accepted formats:

- `https://app.beam.ai/{workspace_id}/{agent_id}/flow`
- `https://app.enterprise.beam.ai/{workspace_id}/{agent_id}/flow`
- Or separate workspace ID + agent ID
- Or a path to an already-downloaded graph JSON file

**If URL contains `enterprise.beam`**, the script auto-detects and uses `https://api.enterprise.beamstudio.ai`.

---

### Step 2: Check for Model Overrides

Ask if any models in the agent have been changed from their defaults. Common scenario: a node originally using Gemini 3 Pro was switched to GPT 5.2.

**If overrides exist**, pass them to the script as `--model-override OLD=NEW`.

Example: `--model-override GEMINI_3_PRO=GPT_5_2`

---

### Step 3: Verify Configuration

Check that `BEAM_API_KEY` exists in `.env`:

```bash
grep "BEAM_API_KEY" .env
```

If missing, ask user to provide it and add to `.env`.

**Skip this step if user provides a `--graph-file` instead of a URL.**

---

### Step 4: Run Analysis Script

Execute the analysis script:

**From URL:**
```bash
python3 03-skills/beam-credit-analysis/scripts/analyze_agent_credits.py "AGENT_URL" --model-override GEMINI_3_PRO=GPT_5_2
```

**From local graph file:**
```bash
python3 03-skills/beam-credit-analysis/scripts/analyze_agent_credits.py --graph-file ./path/to/graph.json
```

**With custom output directory:**
```bash
python3 03-skills/beam-credit-analysis/scripts/analyze_agent_credits.py "AGENT_URL" --output ./custom/path
```

**For JSON output (programmatic):**
```bash
python3 03-skills/beam-credit-analysis/scripts/analyze_agent_credits.py "AGENT_URL" --json
```

---

### Step 5: Review Output

The script generates a markdown file containing:

1. **Credit Rates** — Rates used for calculation with source reference
2. **Architecture Overview** — Branch descriptions and mermaid flow diagram
3. **Per-Branch Tables** (for each branch):
   - **Node Count** — Flash, Premium, Integration, Trigger counts per path
   - **Credit Consumption** — Credits per node type per path
   - **Cost** — Dollar cost per node type per path (using actual model rates from Notion pricing)
4. **Summary** — All paths with total nodes, credits, and cost
5. **Eval Impact** — Credits and cost if eval is enabled on all GPT nodes
6. **Step-by-Step Breakdowns** — Top 3 most expensive paths with per-node detail
7. **Node Inventory** — All Custom GPT and Integration nodes with models and rates

---

### Step 6: Present Results to User

Show the user:
- File path of the generated analysis
- Summary table (all paths with total nodes, credits, cost)
- The mermaid diagram (renders in GitHub markdown)
- Highlight the cheapest and most expensive paths
- Note any assumptions (e.g., GPT 5.2 pricing estimated from GPT 5)

---

## Script Reference

### analyze_agent_credits.py

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes* | Beam agent URL |
| `--workspace-id` | Alt* | Workspace ID (if not using URL) |
| `--agent-id` | Alt* | Agent ID (if not using URL) |
| `--graph-file` | Alt* | Path to local graph JSON (skip API) |
| `--base-url` | No | API base URL override |
| `--output` | No | Output directory |
| `--model-override` | No | Model name override (repeatable) |
| `--pricing-file` | No | Custom pricing.json path |
| `--json` | No | Output raw JSON instead of markdown |

*One of: URL, workspace+agent IDs, or graph-file is required.

**Exit codes:**
- `0` = Success
- `1` = Error (auth, network, missing config)

---

## Pricing Updates

The pricing reference is stored at `references/pricing.json`. To update:

1. Check the [Beam Credits Notion page](https://www.notion.so/joinbeam/Beam-Credits-New-Agent-OS-3062cadfbbbc8198afeae750cb9e292f) for changes
2. Update `references/pricing.json` with new rates
3. Update the `last_updated` field in `_meta`

The script supports both `UPPER_CASE` and `lower-case` model name formats for flexibility.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| BEAM_API_KEY not found | Missing from .env | Add to .env file |
| Auth failed (401) | Invalid or expired API key | Check BEAM_API_KEY |
| Graph fetch failed (404) | Invalid agent/workspace ID | Verify URL is correct |
| No paths found | Graph has no entry nodes | Check agent is properly configured |
| Model not in pricing | New model not yet in pricing.json | Update pricing.json or use --model-override |

---

## Resources

### scripts/
- **analyze_agent_credits.py** — Main analysis engine (fetch, trace, calculate, generate)

### references/
- **pricing.json** — Beam credit rates per model and node type (from Notion)

---

## Related Skills

- `get-beam-agent-graph` — Fetch and save agent graph JSON (used internally)
- `calculate-beam-agent-pricing` — Design node architecture and calculate pricing from requirements
