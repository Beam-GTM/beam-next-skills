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
- Making structural changes to an agent graph (add/remove nodes, edges, params)
- Debugging link translation issues between GET and PUT formats
- Publishing a draft graph after changes

## Core Script

**`scripts/build_put_payload.py`** — Transforms GET response into valid PUT payload.

```bash
# Dry-run: fetch graph, build payload, show summary
python3 scripts/build_put_payload.py --agent-id <UUID> --dry-run

# From saved file
python3 scripts/build_put_payload.py --from-file backup.json --output put_payload.json

# Build, PUT, and publish
python3 scripts/build_put_payload.py --agent-id <UUID> --publish
```

Requires `BEAM_API_KEY` and `BEAM_WORKSPACE_ID` in `.env`.

### What the Script Does

1. Fetches (or loads) the GET graph response
2. Builds reverse lookup: output param UUID → (node ID, param name)
3. Translates every linked input param from UUID-based to name-based format
4. Maps field locations (prompt, model from `originalTool` to `toolConfiguration`)
5. Strips computed fields, includes all required Swagger DTO fields
6. Outputs summary with link translation stats

## Workflow: Structural Changes

1. **GET** current graph (or use backup file)
2. **Build PUT payload**: `python3 build_put_payload.py --agent-id <UUID> --dry-run`
3. **Verify**: check summary — all links should be translated (0 FAILED)
4. **Send PUT**: remove `--dry-run` flag
5. **PATCH prompts**: PUT may not persist prompt changes — use `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/prompt`
6. **PATCH models**: PUT ignores `preferredModel` changes — use `PATCH /agent-graphs/update-node`
7. **Publish**: `PATCH /agent-graphs/{graphId}/publish` or Beam UI

## Critical Rules

- **Never build PUT from GET blindly** — field locations differ. Always use `build_put_payload.py`.
- **Never send empty arrays** — `inputParams: []` deletes all inputs, empty edges destroy topology.
- **Do NOT add fallbackModels** — not settable via API.

## References

- **[field-mapping.md](references/field-mapping.md)** — Complete GET→PUT field mapping table, Swagger DTO required fields, link translation algorithm
- **[known-issues.md](references/known-issues.md)** — PUT & GET specific behavior and limitations

## Related Skills

- `beam-api-reader` — Full Beam API endpoint reference (authentication, task creation, agent setup)
- `beam-agent-manager` — Parent skill with full API behavioral knowledge, PATCH workflows, publishing rules
