---
name: deploy-to-beam
version: '1.0'
description: Deploy Beam Next skills as Beam Platform agents. Load when user mentions
  'deploy to beam', 'create beam agent', 'deploy agent', 'skill to agent', 'push
  to beam', 'beam deploy', or 'deploy-to-beam'.
category: system
tags:
- beam-ai
- deployment
- agents
platform: Beam AI
created: '2026-02-27'
updated: '2026-02-27'
visibility: public
---
# Deploy to Beam

Deploy Beam Next skills as live Beam Platform agents — from Cursor to production in one step.

## Purpose

Bridge between Beam Next (design) and Beam Platform (execution):
- **Design** a workflow as a Beam Next skill (SKILL.md, scripts, references)
- **Deploy** it as a Beam Platform agent with a single command
- **Monitor** and update from Beam Next

---

## Trigger Phrases

Load this skill when user says:
- "deploy to beam" / "push to beam" / "deploy agent"
- "create beam agent from skill"
- "skill to agent"
- "beam deploy"
- "deploy-to-beam"

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python3 00-system/skills/beam/beam-master/scripts/check_beam_config.py --json
```

If not configured → follow beam-connect setup flow.

---

## Two Deployment Paths

### Path 1: AI-Guided (recommended for most cases)

**Best for**: New agents, when you don't know exact tool names, conversational workflows.

The Platform AI handles SOP generation, graph creation, and tool matching automatically.

**Input**: A natural language description (from SKILL.md or user input).

```bash
python3 00-system/skills/beam/beam-master/scripts/create_agent_guided.py \
  --query "SKILL_DESCRIPTION_HERE" \
  --json
```

### Path 2: Complete Graph (advanced, full control)

**Best for**: Precise workflows with known tools, re-deploying existing agents, CI/CD.

You define every node, tool, edge, and parameter in a `beam-agent.yaml`.

```bash
python3 00-system/skills/beam/beam-master/scripts/create_agent_complete.py \
  --spec path/to/beam-agent.yaml \
  --json
```

**Dry-run** (preview payload without deploying):
```bash
python3 00-system/skills/beam/beam-master/scripts/create_agent_complete.py \
  --spec path/to/beam-agent.yaml \
  --dry-run
```

---

## Workflows

### Workflow 1: Quick Deploy (AI-Guided)

**When**: User wants to deploy a skill and doesn't have a `beam-agent.yaml`.

**Steps**:

1. **Identify the skill** to deploy — by name, path, or current context
2. **Read the skill's SKILL.md** to extract:
   - Purpose/description
   - Workflow steps
   - Tools/integrations needed
   - Input/output patterns
3. **Compose a deployment query** — transform the skill description into a clear agent request:
   ```
   Create an agent that [skill purpose].
   
   Workflow:
   1. [Step 1 from skill]
   2. [Step 2 from skill]
   ...
   
   Tools needed: [extracted from skill references/scripts]
   
   The agent should [personality/constraints from skill].
   ```
4. **Deploy**:
   ```bash
   python3 00-system/skills/beam/beam-master/scripts/create_agent_guided.py \
     --query "COMPOSED_QUERY" \
     --json
   ```
5. **Report** the agent ID, dashboard URL, and next steps

**Output format**:
```
✅ Agent deployed to Beam Platform!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent:     [name]
Agent ID:  [id]
Dashboard: https://app.beam.ai/agent/[id]

AI generated:
  ✓ SOP from skill description
  ✓ Workflow graph with [N] nodes
  ✓ Tools matched from 1500+ connectors

Next steps:
  1. Review the graph in Beam dashboard
  2. Configure triggers (webhook, timer, integration)
  3. Test: create a task from Beam Next
```

---

### Workflow 2: Spec Deploy (Complete Graph)

**When**: User has a `beam-agent.yaml` or wants precise graph control.

**Steps**:

1. **Locate the spec file** — check for `beam-agent.yaml` in the skill directory
2. **Validate the spec** (dry-run):
   ```bash
   python3 00-system/skills/beam/beam-master/scripts/create_agent_complete.py \
     --spec SPEC_PATH --dry-run
   ```
3. **Deploy**:
   ```bash
   python3 00-system/skills/beam/beam-master/scripts/create_agent_complete.py \
     --spec SPEC_PATH --json
   ```
4. **Report** results

---

### Workflow 3: Update Existing Agent

**When**: Skill definition changed, need to sync to Platform.

```bash
python3 00-system/skills/beam/beam-master/scripts/update_agent_graph.py \
  --agent-id AGENT_ID \
  --spec SPEC_PATH \
  --json
```

---

### Workflow 4: Deploy + Test

**When**: Deploy and immediately verify with a test task.

1. Deploy via Workflow 1 or 2
2. Create test task:
   ```bash
   python3 00-system/skills/beam/beam-master/scripts/create_task.py \
     --agent-id AGENT_ID \
     --query "TEST_QUERY" \
     --json
   ```
3. Monitor:
   ```bash
   python3 00-system/skills/beam/beam-master/scripts/get_task.py \
     --task-id TASK_ID \
     --json
   ```

---

### Workflow 5: Generate beam-agent.yaml

**When**: User wants to create a spec file for precise control or version-controlled deployments.

**Steps**:

1. Read the skill's SKILL.md
2. Analyze workflow steps, tools, and data flow
3. Generate a `beam-agent.yaml` in the skill directory
4. User reviews and adjusts
5. Deploy via Workflow 2

See `references/beam-agent-schema.md` for the full schema.

---

## beam-agent.yaml Schema (Quick Reference)

```yaml
agent:
  name: "Agent Name"
  description: "What the agent does"
  personality: "How the agent communicates"
  restrictions: "What the agent should NOT do"
  prompts:
    - "Example input 1"
    - "Example input 2"

nodes:
  - id: "node-1"
    objective: "What this node accomplishes"
    is_entry: true
    is_exit: false
    evaluation_criteria:
      - "Output contains X"
    tool:
      name: "Tool Name"
      function_name: "tool_function_identifier"
      description: "What the tool does"
      model: "gpt-4o"
      prompt: "System prompt for this node"
      input_params:
        - name: "param_name"
          description: "What this parameter is"
          type: "string"
          fill_type: "ai_fill"  # ai_fill | static | linked
      output_params:
        - name: "output_name"
          description: "What this output contains"
          type: "string"
    edges:
      - target: "node-2"
        condition: ""
        name: "Next Step"
```

---

## Integration with Existing Beam Skills

| Need | Use Skill | Script |
|------|-----------|--------|
| Check config | beam-connect | `check_beam_config.py` |
| List agents | beam-connect | `list_agents.py` |
| Design agent graph | design-beam-agent | — |
| Get existing graph | get-beam-agent-graph | `get_agent_graph.py` |
| Edit graph nodes | beam-graph-edit | `push_graph.py` |
| Create tasks | beam-connect | `create_task.py` |
| Monitor analytics | beam-get-agent-analytics | `get_analytics.py` |
| Retry failed tasks | beam-retry-tasks | `retry_task.py` |
| Calculate pricing | calculate-beam-agent-pricing | — |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-run check_beam_config.py |
| 400 Bad Request | Invalid spec/payload | Use --dry-run to inspect |
| 409 Conflict | Agent name exists | Use different name or update existing |
| Tool not found | Invalid function_name | Check Beam's tool catalog |

---

## Example: Deploy outbound sales skill

```
User: "deploy the outbound-sales skill to beam"

AI:
1. Reading 01-skills/outbound-sales/SKILL.md...
2. Composing deployment query from skill definition...
3. Deploying to Beam Platform (AI-guided)...

   Step 1/7: Submitting context...
   Step 2/7: Creating agent...
   Step 3/7: Generate SOP...
   Step 4/7: Graph Generation...
   Step 5/7: Tool Matching...
   Step 6/7: Tool Integration...
   Step 7/7: Finalizing...

✅ Agent deployed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent:     Outbound Sales Pipeline
Agent ID:  abc-123-def
Dashboard: https://app.beam.ai/agent/abc-123-def

Next steps:
  1. Review graph in Beam dashboard
  2. Add timer trigger (weekday 9 AM)
  3. Test with sample HubSpot data
```
