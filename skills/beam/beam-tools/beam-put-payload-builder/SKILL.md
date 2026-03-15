---
name: beam-put-payload-builder
version: '1.0'
description: Build valid PUT payloads for Beam agent graphs by transforming GET responses
  into Swagger-DTO-compliant format. Handles link translation (linkParamOutputId UUID
  → linkedOutputParamNodeId + linkedOutputParamName), field remapping, and computed
  field stripping. Load when user says "build put payload", "put beam graph",
  "rebuild graph payload", "transform graph", "put payload builder", "restore beam graph",
  "get to put", or needs to send a PUT to /agent-graphs/{agentId}.
author: Abdul Rafay
category: integrations
tags:
- api
- beam-ai
- graph
- payload
platform: Beam AI
updated: '2026-03-15'
visibility: team
---

# Beam PUT Payload Builder

Build valid PUT payloads for Beam agent graphs by transforming GET responses into Swagger-DTO-compliant format with automatic link translation.

## When to Use

- Building a PUT payload from a GET graph response
- Restoring a graph from a backup JSON file
- Making structural changes to an agent graph (add/remove nodes, edges)
- Debugging link translation issues between GET and PUT formats

## Core Script

**`scripts/build_put_payload.py`** — Transforms GET response into valid PUT payload.

```bash
# Dry-run: fetch graph, build payload, show summary
python3 scripts/build_put_payload.py --agent-id <UUID> --dry-run

# From saved file
python3 scripts/build_put_payload.py --from-file backup.json --output put_payload.json

# Build, send PUT, and publish (uses saveAndPublish query param)
python3 scripts/build_put_payload.py --agent-id <UUID> --publish

# From modified file with new nodes (detects new nodes, skips saveAndPublish, guides PATCH workflow)
python3 scripts/build_put_payload.py --from-file modified.json --agent-id <UUID> --publish
```

Requires `BEAM_API_KEY` and `BEAM_WORKSPACE_ID` in `.env`.

### What the Script Does

1. Fetches (or loads) the GET graph response
2. Builds reverse lookup: output param UUID → (node ID, param name)
3. Translates every linked input param from UUID-based to name-based format
4. Maps field locations (prompt, model from `originalTool` to `toolConfiguration`)
5. Strips computed fields, includes all required Swagger DTO fields
6. Outputs summary with link translation stats

## Workflow

1. **GET** current graph (or use backup file)
2. **Build PUT payload**: `python3 build_put_payload.py --agent-id <UUID> --dry-run`
3. **Verify**: check summary — all links should be translated (0 FAILED)
4. **Send PUT with `--publish`**: the script auto-detects the right publish strategy:

### No new nodes (rebuild, restore, or node deletion)
PUT with `?saveAndPublish=true` — publishes in the same request. No PATCH needed.

### New nodes added
PUT saves as draft. The script prints the PATCH steps needed before publishing:
1. `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/prompt` — set prompt for each new node
2. `PATCH /agent-graphs/update-node` — set `preferredModel` in `toolConfiguration` for each new node
3. `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/input-output-params` — set params for each new node
4. `PATCH /agent-graphs/{graphId}/publish` — publish after all PATCHes

## Critical Rules

- **Never build PUT from GET blindly** — field locations differ. Always use `build_put_payload.py`.
- **Never send empty arrays** — `inputParams: []` deletes all inputs, empty edges destroy topology.
- **Do NOT add fallbackModels** — not settable via API.
- **PUT is for structure only** — do NOT use PUT to update prompts, input/output params, or preferred models on existing nodes. Use PATCH endpoints for those (see `beam-agent-manager`).

## References

- **[field-mapping.md](references/field-mapping.md)** — Complete GET→PUT field mapping table, Swagger DTO required fields, link translation algorithm
- **[known-issues.md](references/known-issues.md)** — PUT & GET specific behavior and limitations

## Related Skills

- `beam-api-reader` — Full Beam API endpoint reference (authentication, task creation, agent setup)
- `beam-agent-manager` — Parent skill with full API behavioral knowledge, PATCH workflows, publishing rules
