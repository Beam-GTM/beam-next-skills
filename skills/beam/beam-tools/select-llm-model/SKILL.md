---
name: select-llm-model
version: 1.3
description: Select optimal LLM model for Beam AI tools based on cost, context, and
  performance. Load when user says "select llm model", "choose model", "optimize llm",
  "which model for", "model recommendation", "best model for agent", "llm cost optimization",
  or needs help selecting the right AI model for their Beam tools.
category: general
tags:
- beam-ai
platform: Beam AI
updated: '2026-02-03'
visibility: team
---
# Select LLM Model

**Find the most cost-effective LLM model for your Beam AI tools without sacrificing reliability.**

## When to Use

- Optimizing agent costs by selecting cheaper models where possible
- Ensuring context window fits your prompts and outputs
- Comparing LLM options for a new tool design
- Auditing existing agents for cost savings

---

## Prerequisites

### Option 1: Beam Task Analysis

**Required**: Your Beam.ai personal API key

Add to `.env` file at project root:

```env
# Your Beam.ai Personal API Key (from Beam Settings → API)
BEAM_API_KEY=your_personal_api_key_here

# Workspace ID is extracted from task URLs automatically
# Or set it manually if preferred:
# BEAM_WORKSPACE_ID=your_workspace_id
```

**Don't have an API key?** Get it from: Beam Settings → API → Create Personal API Key

### Option 2: Manual Analysis

No prerequisites - just provide your prompt and examples directly.

**Dependencies**: `pip install requests python-dotenv`

---

## Authentication Flow (Beam API)

Beam uses a two-step authentication:

1. **Exchange API Key for Access Token**:
```bash
curl -X POST https://api.beamstudio.ai/auth/access-token \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "YOUR_PERSONAL_API_KEY"}'
```

Response:
```json
{
  "idToken": "eyJhbG...",    // Use this as Bearer token
  "refreshToken": "eyJhbG...",
  "expiresIn": 600           // Token lasts 10 minutes
}
```

2. **Use Access Token for API Calls**:
```bash
curl -X GET "https://api.beamstudio.ai/agent-tasks/{TASK_ID}" \
  -H "Authorization: Bearer {idToken}" \
  -H "current-workspace-id: {WORKSPACE_ID}"
```

**Workspace ID**: First UUID in the task URL
Example: `https://app.beam.ai/0853f6d5-c912-4a47-8101.../tasks/...`
Workspace ID = `0853f6d5-c912-4a47-8101-c965c282d46f`

---

## Workflow

### Step 1: Gather Input

Ask the user which input method they prefer:

**Option A: Beam Task URL/ID**
- User provides a Beam task URL like: `https://app.beam.ai/{workspace_id}/{agent_id}/tasks/{task_id}`
- Or just the task ID: `783221fe-fdde-4086-987e-544ca216a31c`
- Extract UUIDs from URL:
  - **Workspace ID**: First UUID after `app.beam.ai/`
  - **Task ID**: UUID after `/tasks/`

**Option B: Manual Input**
- User provides:
  - The prompt template (with variable placeholders like `{{input_data}}`)
  - Example input parameter values
  - Expected output format/schema

---

### Step 2: Fetch & Save Task Data

If using Beam Task:

1. **Get Access Token**:
```bash
ACCESS_TOKEN=$(curl -s -X POST "https://api.beamstudio.ai/auth/access-token" \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "YOUR_API_KEY"}' | jq -r '.idToken')
```

2. **Fetch Task Details** (save to file - responses are often 1-3MB):
```bash
curl -s -X GET "https://api.beamstudio.ai/agent-tasks/{TASK_ID}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "current-workspace-id: {WORKSPACE_ID}" \
  -o /tmp/beam_task_{TASK_ID}.json
```

3. **Identify LLM Tools**: Parse `agentTaskNodes` and filter by type:

| Tool Type | `originalTool.type` | Action |
|-----------|---------------------|--------|
| `custom_gpt_tool` | Custom LLM tool | **Analyze** |
| `gpt_tool` | Built-in LLM tool | **Analyze** |
| `beam_tool` | System tool | Skip |
| `custom_integration_tool` | API integration | Skip |

---

### Step 3: Extract Tool Details

For each LLM tool, extract from task JSON using these **correct paths**:

| Data Point | JSON Path |
|------------|-----------|
| **Tool Name** | `agentTaskNodes[].agentGraphNode.toolConfiguration.toolName` |
| **Template Prompt** | `agentTaskNodes[].agentGraphNode.toolConfiguration.originalTool.prompt` |
| **Filled Prompt** | `agentTaskNodes[].toolData.filled_prompt` |
| **Output** | `agentTaskNodes[].output.value` |
| **Current Model** | `agentTaskNodes[].agentGraphNode.toolConfiguration.originalTool.preferredModel` |

**Important**: Use `filled_prompt` for token calculation - this is what actually gets sent to the LLM (template + substituted variable values).

---

### Step 4: Token Analysis

Calculate tokens for each tool:

```
Input Tokens  = len(filled_prompt) / 3.5
Output Tokens = len(json.dumps(output)) / 3.5
Total Context = Input + Output
Buffer        = Total × 1.2  (20% safety margin)
```

**Token estimation by content type**:
| Content Type | Chars per Token |
|--------------|-----------------|
| JSON/Code | ~3.5 |
| Plain English | ~4.0 |
| Mixed content | ~3.7 |

---

### Step 5: Task Complexity Assessment (CRITICAL)

**Don't just recommend the cheapest model that fits the context.** Assess task complexity to ensure quality:

#### Complexity Levels

| Level | Characteristics | Recommended Model |
|-------|-----------------|-------------------|
| **LOW** | Boolean output, simple ID consolidation | GPT-4o-mini |
| **LOW-MEDIUM** | Data extraction (accuracy-critical) | Gemini 3 Flash |
| **MEDIUM** | Classification, basic analysis, structured reasoning | Gemini 3 Flash |
| **MEDIUM-HIGH** | Pattern recognition, sentiment analysis, multi-factor reasoning | Gemini 3 Flash |
| **HIGH** | Customer-facing content generation, complex reasoning, nuanced writing | Gemini 3 Flash or GPT-5 |

#### Task Type Indicators

Analyze the prompt and output to classify:

| Task Type | Prompt Keywords | Output Type | Complexity | Notes |
|-----------|-----------------|-------------|------------|-------|
| **Data Extraction** | "extract", "parse", "get fields" | JSON fields | LOW-MEDIUM | **Use Gemini 3 Flash** - GPT-4o-mini has accuracy issues |
| **Consolidation** | "consolidate", "combine", "merge" | Lists, aggregated data | LOW | GPT-4o-mini OK for simple lists |
| **Classification** | "classify", "categorize", "determine" | Category/label | MEDIUM | Gemini 3 Flash recommended |
| **Evaluation** | "evaluate", "compare", "assess" | Boolean or score | LOW | GPT-4o-mini OK for yes/no |
| **Analysis** | "analyze", "identify patterns", "risk factors" | Rich insights | MEDIUM-HIGH | Gemini 3 Flash |
| **Content Generation** | "generate email", "write", "compose" | Customer-facing text | HIGH | Gemini 3 Flash or GPT-5 |

#### Accuracy vs Cost Tradeoff

**Key Learning**: GPT-4o-mini is cheap but may miss extraction details. For business-critical data extraction, use **Gemini 3 Flash** - it's only ~$0.50/$3.00 per 1M tokens and significantly more accurate.

| Scenario | GPT-4o-mini | Gemini 3 Flash |
|----------|-------------|----------------|
| Boolean decisions | OK | Overkill |
| ID list consolidation | OK | Overkill |
| Field extraction from structured data | **Accuracy issues** | Recommended |
| Multi-field extraction | **Not recommended** | Recommended |
| Pattern analysis | Not recommended | Recommended |

#### Output Quality Indicators

Examine the actual output to verify complexity:

| Output Type | Example | Safe for GPT-4o-mini? |
|-------------|---------|----------------------|
| Boolean | `{"should_update": false}` | YES |
| ID List | `{"ticket_ids": "123, 456, 789"}` | YES |
| Simple JSON (1-2 fields) | `{"status": "active"}` | MAYBE - test first |
| Multi-field extraction | `{"name": "...", "email": "...", "date": "..."}` | **NO - use Gemini 3 Flash** |
| Rich Analysis | `{"risk_factors": [...], "sentiment": "..."}` | NO - use Gemini 3 Flash |
| Generated Text | `{"email_body": "Dear customer..."}` | NO - use better model |

---

### Step 6: Generate Recommendations

For each tool, provide:

```
TOOL: {tool_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Model: {current_model}
Input Tokens:  {input_tokens}
Output Tokens: {output_tokens}
Total Context: {total_tokens}

Task Analysis:
  Type: {extraction|consolidation|classification|analysis|generation}
  Complexity: {LOW|MEDIUM|MEDIUM-HIGH|HIGH}
  Output: {description of output type}

RECOMMENDED: {model_name}
  Confidence: {HIGH|MEDIUM|LOW}
  Reason: {why this model fits the task}
  Cost: ${cost}/1K calls

Current vs Recommended:
  Current:     ${current_cost}/1K
  Recommended: ${new_cost}/1K
  Savings:     {percentage}%
```

---

### Step 7: Summary Table

Present final recommendations in a table:

| Tool | Tokens (in/out) | Complexity | Recommended | Confidence | Cost/1K | Savings |
|------|-----------------|------------|-------------|------------|---------|---------|
| Tool A | 1,000 / 200 | LOW | GPT-4o-mini | HIGH | $0.27 | 94% |
| Tool B | 76,000 / 600 | MEDIUM-HIGH | Gemini 3 Flash | MEDIUM | $40.00 | 83% |

---

### Step 8: Cleanup

Ask user:
> "Would you like me to delete the temporary task data file? (y/n)"

If yes: `rm /tmp/beam_task_<task_id>.json`

---

## Research-Backed Model Recommendations

### Why Gemini 3 Flash for Extraction (Benchmark Evidence)

| Finding | Source |
|---------|--------|
| Gemini 3 Flash has **15% better extraction accuracy** than Gemini 2.5 Flash on hard tasks | Artificial Analysis |
| Gemini 3 Flash **competes with GPT-5.2** in benchmarks; GPT-4o-mini is 17 months older | Engadget |
| For document extraction, Gemini Flash "extracts the most detailed information and achieves the best accuracy" | Medium - UnderDoc |
| GPT-4o-mini hallucination rate: ~1.69% on simple tasks, but **higher on extraction** | All About AI |
| Gemini 3 Flash: 218 tokens/sec vs GPT-4o-mini: 85 tokens/sec | DocsBot |

### Best Model by Task Type (Research-Validated)

| Task Type | Best Model | Why | Cost/1M (in/out) |
|-----------|------------|-----|------------------|
| **Boolean decisions** | GPT-4o-mini | Simple, cheap, sufficient | $0.15/$0.60 |
| **ID list consolidation** | GPT-4o-mini | Simple aggregation | $0.15/$0.60 |
| **Data extraction** | **Gemini 3 Flash** | 15% better accuracy, handles complex docs | $0.50/$3.00 |
| **Classification** | Gemini 3 Flash | Good reasoning at low cost | $0.50/$3.00 |
| **Pattern analysis** | Gemini 3 Flash | Strong on complex reasoning | $0.50/$3.00 |
| **Content generation** | GPT-5 or Gemini 3 Flash | Best writing quality | $1.25/$10 or $0.50/$3.00 |
| **Complex reasoning** | GPT-5.2 or Gemini 3 Pro | Highest benchmark scores | $1.75/$14 or $3.00/$15 |
| **Very large context (>200K)** | Gemini 2.5 Pro or GPT-4.1 | 1M context window | $1.25/$10 or $2.00/$8.00 |

### Cost vs Accuracy Tradeoff

**Example**: Data Extraction Tool (946 input / 210 output tokens)

| Model | Cost per 1K calls | Accuracy |
|-------|-------------------|----------|
| GPT-4o-mini | $0.27 | Lower (fields missed) |
| Gemini 3 Flash | $1.10 | Higher (15%+ improvement) |

**Delta: $0.83 per 1K calls** for significantly better accuracy - worth it for business-critical extraction.

### Key Insight

GPT-4o-mini is **17 months older** than Gemini 3 Flash (Oct 2023 vs Jan 2025 training data). Gemini 3 Flash now competes with GPT-5.2 level performance at Flash pricing, making it the best value for most tasks except simple boolean/list operations.

---

## Model Selection Matrix

### By Task Complexity

| Complexity | Primary Choice | Alternative | Avoid |
|------------|----------------|-------------|-------|
| **LOW** (boolean, ID lists) | GPT-4o-mini | Gemini 3 Flash | Opus, GPT-5 (overkill) |
| **LOW-MEDIUM** (extraction) | Gemini 3 Flash | GPT-5 | GPT-4o-mini (accuracy issues) |
| **MEDIUM** | Gemini 3 Flash | GPT-5 | GPT-4o-mini |
| **MEDIUM-HIGH** | Gemini 3 Flash | GPT-5 | GPT-4o-mini (quality risk) |
| **HIGH** | Gemini 3 Flash | GPT-5, Claude 4.5 Sonnet | GPT-4o-mini (quality risk) |

### When to Use GPT-4o-mini

Only use GPT-4o-mini for:
- Simple boolean decisions (`should_update: true/false`)
- ID/ticket list consolidation
- Very high volume, low-accuracy-tolerance tasks

**Do NOT use GPT-4o-mini for**:
- Data extraction (fields get missed or incorrectly parsed)
- Multi-field JSON outputs
- Anything requiring consistent accuracy

### By Context Size

| Context Need | Best Options |
|--------------|--------------|
| **<50K tokens** | GPT-4o-mini, Gemini 3 Flash |
| **50K-128K** | GPT-4o-mini, Gemini 3 Flash, Claude 4.5 Sonnet |
| **128K-200K** | Claude 4.5 Sonnet, GPT-5, Gemini 2.5 Pro |
| **200K-1M** | GPT-4.1, Gemini 2.5 Pro, Gemini 3 Pro |

### Cost Quick Reference

| Model | Input/1M | Output/1M | Context | Best For |
|-------|----------|-----------|---------|----------|
| **GPT-4o-mini** | $0.15 | $0.60 | 128K | Low complexity, high volume |
| **Gemini 3 Flash** | $0.50 | $3.00 | 1M | Medium-high complexity, fast |
| **GPT-5** | $1.25 | $10.00 | 400K | High complexity, best value |
| **Claude 4.5 Sonnet** | $3.00 | $15.00 | 200K | Balanced, caching available |
| **Gemini 3 Pro** | $3.00 | $15.00 | 1M | Large context analysis |

---

## Beam Model Identifiers

| Beam ID | Model Name |
|---------|------------|
| `GPT4O_MINI` | GPT-4o-mini |
| `GPT40` | GPT-4o |
| `GPT41` | GPT-4.1 |
| `GPT5` | GPT-5 |
| `GPT52` | GPT-5.2 |
| `GEMINI_3_FLASH` | Gemini 3 Flash |
| `GEMINI_25_PRO` | Gemini 2.5 Pro |
| `GEMINI_3_PRO` | Gemini 3 Pro |
| `CLAUDE_35_SONNET` | Claude 3.5 Sonnet |
| `CLAUDE_45_SONNET` | Claude 4.5 Sonnet |
| `CLAUDE_45_OPUS` | Claude 4.5 Opus |

---

## Troubleshooting

### "401 Unauthorized" Error
- Access token expired (10 min lifetime). Get a fresh token.
- Check workspace ID matches the task's workspace.

### "Task not found" Error
- Verify task ID is correct (UUID after `/tasks/` in URL).
- Use production API (`api.beamstudio.ai`), not BID staging.

### API Key Not Working
- Must be a **Personal API Key** from Beam Settings → API.
- Personal API keys are exchanged for access tokens; they don't work directly.

---

## Related Skills

- `beam-get-task-details` - Fetch task data from Beam
- `design-beam-agent` - Design new agent architecture
- `beam-get-agent-analytics` - Analyze agent performance

---

## Model Reference

See [references/llm-models.md](references/llm-models.md) for complete specifications including:
- Pricing details (Feb 2026)
- Context windows
- Speed benchmarks
- Known limitations
- Best use cases
