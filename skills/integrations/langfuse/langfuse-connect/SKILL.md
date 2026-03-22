---
name: langfuse-connect
type: skill
version: '2.0'
description: langfuse, traces, observations, llm tracing.
category: integrations
tags:
- connector
- langfuse
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Connect

User-facing entry point for Langfuse integration. Routes to consolidated operation skills.

## Context reference

For score config IDs and API patterns, see **Patterns & score config reference** below. For shared client, references, and error handling, load `langfuse-master/`.

---

## Pre-Flight Check (ALWAYS FIRST)

Before any operation, run config check:

```bash
uv run python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --json
```

**If `ai_action` is:**
- `proceed_with_operation` → Continue with requested operation
- `prompt_for_api_key` → Ask user for credentials, guide to setup

---

## Routing Table

All Langfuse operations are consolidated into 11 skills. Each uses `--resource` and `--action` arguments for dispatch.

### Traces, Observations & Sessions → `langfuse-traces`

| User Says | Resource | Action |
|-----------|----------|--------|
| "list traces", "show traces" | traces | list |
| "get trace {id}", "trace details" | traces | get |
| "delete trace", "bulk delete traces" | traces | delete |
| "list observations", "show spans" | observations | list |
| "get observation {id}" | observations | get |
| "list sessions", "show sessions" | sessions | list |
| "get session {id}" | sessions | get |

### Datasets, Items, Runs → `langfuse-datasets`

| User Says | Resource | Action |
|-----------|----------|--------|
| "list datasets", "show datasets" | datasets | list |
| "create dataset", "new dataset" | datasets | create |
| "get dataset {name}" | datasets | get |
| "list dataset items", "show items" | items | list |
| "create dataset item", "add item" | items | create |
| "get dataset item {id}" | items | get |
| "delete dataset item" | items | delete |
| "list runs", "show runs" | runs | list |
| "get run" | runs | get |
| "delete run" | runs | delete |
| "list run items", "show results" | run-items | list |
| "create run item", "log evaluation" | run-items | create |

### Scores & Score Configs → `langfuse-scores`

| User Says | Resource | Action |
|-----------|----------|--------|
| "list scores", "show evaluations" | scores | list |
| "get score {id}" | scores | get |
| "create score", "add score" | scores | create |
| "delete score", "remove score" | scores | delete |
| "list score configs", "show config" | configs | list |
| "get score config {id}" | configs | get |
| "create score config", "new config" | configs | create |
| "update score config", "archive config" | configs | update |

### Annotation Queues → `langfuse-queues`

| User Says | Resource | Action |
|-----------|----------|--------|
| "list queues", "annotation queues" | queues | list |
| "create queue", "new queue" | queues | create |
| "get queue {id}" | queues | get |
| "list queue items" | items | list |
| "add to queue" | items | create |
| "get queue item" | items | get |
| "update queue item", "annotate" | items | update |
| "remove from queue" | items | delete |
| "assign reviewer" | assignments | create |
| "unassign reviewer" | assignments | delete |

### Prompts → `langfuse-prompts`

| User Says | Action |
|-----------|--------|
| "list prompts", "show prompts" | list |
| "get prompt {name}" | get |
| "create prompt", "new prompt" | create |
| "delete prompt" | delete |
| "update prompt version", "set labels" | update-version |

### Models → `langfuse-models`

| User Says | Action |
|-----------|--------|
| "list models", "model costs" | list |
| "get model {id}" | get |
| "create model" | create |
| "delete model" | delete |

### Projects & Org Admin → `langfuse-admin`

| User Says | Resource | Action |
|-----------|----------|--------|
| "current project", "get project" | projects | get |
| "create project" | projects | create |
| "update project", "rename project" | projects | update |
| "delete project" | projects | delete |
| "list api keys" | api-keys | list |
| "create api key" | api-keys | create |
| "delete api key" | api-keys | delete |
| "list members", "org members" | org | list-memberships |
| "change role", "update member" | org | update-membership |
| "remove member" | org | delete-membership |
| "list org projects" | org | list-projects |
| "org api keys" | org | list-api-keys |

### Ingestion, Comments & Media → `langfuse-ingestion`

| User Says | Resource | Action |
|-----------|----------|--------|
| "batch ingest", "bulk import" | batch | ingest |
| "otel ingest", "opentelemetry" | otel | ingest |
| "list comments" | comments | list |
| "get comment" | comments | get |
| "create comment", "add comment" | comments | create |
| "get media" | media | get |
| "update media" | media | update |
| "upload url", "media upload" | media | upload-url |

### Health & Metrics → `langfuse-status`

| User Says | Action |
|-----------|--------|
| "health check", "is langfuse up" | health |
| "metrics", "usage stats" | metrics |

---

## Quick Start

```bash
# Check config
uv run python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --test

# List recent traces
uv run python scripts/traces.py --resource traces --action list --limit 10

# Get specific trace
uv run python scripts/traces.py --resource traces --action get --id abc123

# Create a score
uv run python scripts/scores.py --resource scores --action create --trace {id} --name tool_efficiency --value 0.85
```

---

## Patterns & score config reference

### Critical patterns

#### Observations require individual fetch

```python
# GET /sessions/{id} does NOT include observations
# Must call GET /traces/{id} for each trace
for trace in session["traces"]:
    full = client.get(f"/traces/{trace['id']}")
    obs = full.get("observations", [])
```

#### CATEGORICAL scores use string value

```python
# CORRECT
{"value": "archive", "configId": "..."}

# WRONG (400 error)
{"value": 2, "stringValue": "archive"}
```

### Score config IDs

```python
CONFIG_IDS = {
    # Quality Dimensions (NUMERIC 0-1 unless noted)
    "goal_achievement": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",      # CATEGORICAL
    "tool_efficiency": "84965473-0f54-4248-999e-7b8627fc9c29",
    "process_adherence": "651fc213-4750-4d4e-8155-270235c7cad8",
    "context_efficiency": "ae22abed-bd4a-4926-af74-8d71edb1925d",
    "error_handling": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",        # CATEGORICAL
    "output_quality": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
    "overall_quality": "793f09d9-0053-4310-ad32-00dc06c69a71",
    # Meta Scores
    "root_cause_issues": "669bead7-1936-4fc4-bae8-e7814c9eab04",     # CATEGORICAL
    "session_improvements": "2e87193b-c853-4955-b2f0-9fa572531681",  # CATEGORICAL
    "session_notes": "67640329-0c03-4be6-bc9f-49765a0462b5",         # NUMERIC (value=1 + comment/metadata)
}
```

#### CATEGORICAL labels

| Score | Labels |
|-------|--------|
| goal_achievement | failed, partial, complete, exceeded |
| error_handling | poor, struggled, recovered, prevented |
| root_cause_issues | none, tool_misuse, process_violation, context_waste, error_cascade, output_quality, multiple |
| session_improvements | none, minor, moderate, significant, critical |

---

## Error Handling

On error, load: `langfuse-master/references/error-handling.md`

Common issues:
- **401**: Check API keys
- **404**: Resource not found
- **429**: Rate limited, wait and retry

---

## References

- Master skill: `langfuse-master/`
- Setup guide: `langfuse-master/references/setup-guide.md`
- API reference: `langfuse-master/references/api-reference.md`
