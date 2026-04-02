# PUT & GET Reference

Information specific to the GET→PUT transformation workflow. Last updated 2026-04-02.

For full API behavior reference (PATCH, publishing, entry nodes, etc.), see `04-workspace/clients/wunsche/agents/plan/beam-api-issues-and-suggestions.md`.

## PUT Does Not Propagate to `originalTool` (B1/B2/B3)

PUT accepts fields per the Swagger DTO (`CompleteAgentGraphNodeToolConfigurationDto`) and stores them in `toolConfiguration`, but the server does not propagate changes to `originalTool`, which is the effective configuration. Affects:

| Field | PUT DTO Location | Stored in GET? | Propagated to `originalTool`? | Workaround |
|-------|-----------------|----------------|------------------------------|------------|
| `prompt` (B1) | `toolConfiguration.prompt` | Yes (`toolConfiguration.prompt`) | No | `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/prompt` |
| `preferredModel` (B2) | `toolConfiguration.preferredModel` | Yes (`toolConfiguration.preferredModel`) | No | `PATCH /agent-graphs/update-node` with `preferredModel` in `toolConfiguration` |
| `inputParams` / `outputParams` (B3) | `toolConfiguration.inputParams` / `.outputParams` | Yes (`toolConfiguration.inputParams/outputParams`) | No | `PATCH /agent-graphs/{agentId}/nodes/{nodeId}/input-output-params` |

## PATCH `update-node` Wipes Output Params

`PATCH /agent-graphs/update-node` replaces the entire `toolConfiguration` object — including `outputParams`. Even when passing through the existing tool config, output params are wiped because their `id` fields (which are read-only) cannot be included in the request.

**Impact:** After any `update-node` PATCH (e.g. updating objectives, evaluation criteria, retry settings), all output params on the node are silently deleted.

**Workaround:** Always follow `update-node` with a separate call to restore outputs:

```
1. PATCH /agent-graphs/update-node              → update node settings
2. PATCH /agent-graphs/{agentId}/nodes/{nodeId}/input-output-params  → restore outputs
```

**Discovered:** 2026-04-02 (Novus Pricing Matrix agent — all 8 nodes affected twice before identifying the pattern).

---

## Other PUT Limitations

| Issue | Impact | Workaround |
|-------|--------|------------|
| PUT with empty `inputParams: []` | Silently deletes ALL inputs | Always include full input array from GET |
| PUT with empty edges arrays | Silently destroys all edges | Always include full `childEdges`/`parentEdges` from GET |
| `toolFunctionName` auto-renamed after PUT | Node identifiers change | Always re-fetch after PUT; identify by `toolName` |
| `autoRetryWhenAccuracyLessThan` must be >= 50 | API rejects values below 50 with 400 error | Always use 50 or higher (default: 80) |

## GET Quirks (relevant to GET→PUT)

| Issue | Notes |
|-------|-------|
| `graph.edges` always empty | Edges stored in node-level `childEdges`/`parentEdges` — script extracts from nodes |
| GET always returns draft (`isPublished=false`) | By design — draft is copy of published |
| Publishing regenerates node UUIDs | Always GET fresh graph after any publish |
| Prompts live at `originalTool.prompt` | NOT at top-level `toolConfiguration.prompt` — script reads from `originalTool` |
| Models live at `originalTool.preferredModel` | Same as prompts — script reads from `originalTool` |

## Source of Truth

- **Swagger JSON**: `beam-api-swagger.json` — authoritative for request body schemas
- **Never build PUT from GET blindly** — field locations and link formats differ
- **Never use `graph.edges`** — always use node-level edge arrays
