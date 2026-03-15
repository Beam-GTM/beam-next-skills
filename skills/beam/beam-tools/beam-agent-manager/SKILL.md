---
name: beam-agent-manager
version: '1.0'
description: Orchestrate Beam agent graph operations — create, modify, and optimize
  agent graphs via the right child skill. Covers graph creation (from YAML, from spec,
  or simple POST), structural changes (PUT), prompt/model/param updates (PATCH),
  prompt optimization (APE), and publishing. Use when user says "beam agent manager",
  "create beam agent", "build beam graph", "update beam graph", "patch and publish",
  "structural change", "add nodes", "optimize prompts", "APE loop", or any graph
  modification task. Do NOT use for runtime operations (tasks, analytics, HITL,
  debugging) — those are handled by beam-connect.
author: Abdul Rafay
category: integrations
tags:
- api
- beam-ai
- orchestration
- graph
platform: Beam AI
updated: '2026-03-15'
visibility: team
---

# Beam Agent Manager

Orchestrate Beam agent **graph operations** — creation, structural changes, prompt optimization, and deployment. Routes to the right child skill based on user intent. For **runtime** operations (tasks, analytics, HITL, debugging), use `beam-connect` instead.

## Decision Tree — What Does the User Want?

```
User wants to...
│
├── CREATE a new agent
│   ├── From YAML/JSON spec (quick deploy, spec already defined)
│   │   └── create-beam-agent (POST /agent-graphs/complete)
│   │
│   ├── From business requirements (full lifecycle: design → deploy → validate)
│   │   └── beam-graph-creator (spec → Miro flowchart → nodes → PUT/PATCH → test)
│   │       Handles any topology: linear, branching, convergence
│   │       Also use for design-only (Steps 1-5, skip deployment)
│   │
│   └── Simple POST with prompt only
│       └── beam-api-reader (create_agent_from_prompt.py)
│
├── MODIFY graph structure (add/remove nodes or edges)
│   └── 1. get-beam-agent-graph (fetch + backup)
│       2. beam-put-payload-builder (GET→PUT payload)
│       3. PUT /agent-graphs/{agentId}
│       4. PATCH prompts/models/params
│       5. Publish
│
├── UPDATE prompts, models, or params (no structural change)
│   └── PATCH directly (see Workflows below) → Publish
│
├── OPTIMIZE prompts via APE loop
│   └── beam-ape-optimizer (test → critique → edit → redeploy)
│
├── EXTRACT nodes to files
│   └── graph-slicer
│
└── CHOOSE a model for a node
    └── select-llm-model
```

## Skill Priority Rules

| Scenario | Use This | NOT This | Why |
|----------|----------|----------|-----|
| User has YAML spec, wants to deploy | `create-beam-agent` | `beam-graph-creator` | No design phase needed |
| User has business requirements | `beam-graph-creator` | `create-beam-agent` | Needs design phase |
| User wants design files only, no API | `beam-graph-creator` Steps 1-5 | `create-beam-agent` | No deployment |
| User wants to improve prompt accuracy | `beam-ape-optimizer` | Manual PATCH | Systematic with test data |

## Relationship to beam-connect

| Domain | Skill | Examples |
|--------|-------|---------|
| **Build-time** (graph ops) | `beam-agent-manager` | Create agent, add nodes, update prompts, optimize, publish |
| **Runtime** (task ops) | `beam-connect` | Create tasks, check status, analytics, HITL, debugging, retry |

## Core Rule: PUT vs PATCH

This is the most important decision in any Beam graph operation:

| I want to... | Use | Why |
|--------------|-----|-----|
| Add/remove nodes or edges | **PUT** (full graph) | Only way to change structure |
| Update a prompt | **PATCH** `/nodes/{nodeId}/prompt` | Propagates to effective config |
| Update a model | **PATCH** `/agent-graphs/update-node` | Set `preferredModel` in `toolConfiguration` |
| Update params | **PATCH** `/nodes/{nodeId}/input-output-params` | Propagates correctly |
| Publish | **PATCH** `/agent-graphs/{graphId}/publish` | Always required after any change |

PUT does NOT propagate prompts/models/params to `originalTool`. Always PATCH after PUT.

## Workflows

### Update Prompt/Model/Params

```
1. PATCH prompt/model/params
2. Publish: PATCH /agent-graphs/{graphId}/publish
3. GET fresh graph (UUIDs regenerated after publish)
```

### Structural Change (Add Nodes/Edges)

```
1. GET current graph → save backup
2. Build PUT payload: use beam-put-payload-builder
3. PUT /agent-graphs/{agentId}
4. PATCH prompts, models, params for changed nodes
5. Publish
6. GET fresh graph
```

### Multi-Node Param Update

```
1. Order: upstream → downstream (UUIDs regenerate on each PATCH)
2. PATCH node A params → GET fresh graph → PATCH node B params → ...
3. Publish
```

### Backup & Restore

```
1. GET graph → save as backup JSON
2. Make changes
3. Rollback: beam-put-payload-builder --from-file backup.json
```

## API Rules Quick Reference

Key rules to remember (full details in [references/api-rules.md](references/api-rules.md)):

- **Publishing regenerates all node UUIDs** — always GET fresh graph after publish
- **Empty arrays destroy data** — `inputParams: []` deletes all inputs, empty edges destroy topology
- **Edge mirroring required** — every edge in source's `childEdges[]` AND target's `parentEdges[]`
- **No fallback models via API** — only settable in Beam UI
- **`autoRetryWhenAccuracyLessThan` >= 50** — API rejects lower values
- **Filter signature images from .msg files** — small images cause tasks to hang

For node configuration rules, linking formats, GET quirks, prompt authoring rules, and authentication: consult [references/api-rules.md](references/api-rules.md).

## Error Handling

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| PUT returns 400 | Missing required fields on node (retry/batch fields, `reloadProps`, `remoteOptions`) | Consult api-rules.md → Node Configuration |
| PATCH returns 200 but no effect | Patching auto-created entry node (silently ignored) | Don't PATCH entry nodes — they're structural markers |
| GET crashes with `Cannot set properties of null` | `toolFunctionName` doesn't match registered tool | Use `GPTAction_EmptyTool` as base tool |
| Node prompt is empty after PUT | PUT doesn't propagate to `originalTool` | PATCH prompt after PUT |
| Task stuck in IN_PROGRESS | Signature images in attachments | Filter `image001.png` etc. from `.msg` files |
| Model silently changed to Gemini 3 PRO | Invalid model string | Use exact enterprise model names |

## References

- **[api-rules.md](references/api-rules.md)** — Full API behavioral rules, constraints, and gotchas
- **beam-api-swagger.json** — Source of truth for request body schemas (in workspace `plan/` folder)
