# Beam API Behavioral Rules

Detailed API behavior, constraints, and gotchas for the Beam Enterprise API. Consult this when building payloads, debugging unexpected behavior, or before any API operation.

## Table of Contents

- [PUT Propagation Issue](#put-propagation-issue)
- [PATCH Behavior](#patch-behavior)
- [Publishing](#publishing)
- [Entry Nodes](#entry-nodes)
- [Node Configuration](#node-configuration)
- [Linking Formats](#linking-formats)
- [GET Response Quirks](#get-response-quirks)
- [Edge Rules](#edge-rules)
- [Model Configuration](#model-configuration)
- [Prompt Authoring](#prompt-authoring)
- [Authentication](#authentication)
- [Task Attachments](#task-attachments)

---

## PUT Propagation Issue

PUT accepts `prompt`, `preferredModel`, `inputParams`, and `outputParams` per Swagger DTO and stores them in `toolConfiguration`, but does NOT propagate to `originalTool` (the effective configuration). This means:

- PUT is only for structural changes (adding nodes, edges, topology)
- Always PATCH after PUT for prompt, model, and param updates
- This is how the API works — not a bug

## PATCH Behavior

- All PATCH endpoints save to draft only — must publish for changes to take effect
- `PATCH input-output-params` regenerates output param UUIDs — if patching multiple nodes, go upstream → downstream and re-fetch between each
- `PATCH update-node` requires the full node object wrapped in `{agentId, graphId, node: AgentGraphNodeDto}`
- `PATCH prompt` is simple: `{prompt: "..."}` body
- Fallback models cannot be set via API — only via Beam UI

## Publishing

- Endpoint: `PATCH /agent-graphs/{graphId}/publish`
- Always publish after PATCH — changes are draft-only until published
- Publishing regenerates all node UUIDs — always GET fresh graph after publish before any further PATCH
- GET always returns the draft version (`isPublished: false`) — by design, not a bug

## Entry Nodes

- Do not create entry nodes — Beam auto-creates an empty entry marker when no node has `isEntryNode: true`
- Auto-created entry node has 0 child edges — must manually connect Entry → first tool node
- PATCH is silently ignored on auto-created entry nodes (returns 200 OK, no effect)
- Setting `isEntryNode: true` on a tool node causes it to render as "Entry" in UI
- Correct approach: set `isEntryNode: false` on all tool nodes, let Beam auto-create entry marker, use `fillType: ai_fill` on first processing node

## Node Configuration

- Node IDs must be UUIDs — API rejects non-UUID node IDs
- Each node needs a unique `toolFunctionName` — duplicates cause shared config (last prompt overwrites all)
- `toolFunctionName` must match a registered tool — invalid names crash GET with `Cannot set properties of null`
- `toolName` cannot contain `.` or `!` — use "1 Email Intake" not "1. Email Intake"
- `reloadProps: false` and `remoteOptions: false` required on all input params
- `autoRetryWhenAccuracyLessThan` must be >= 50 — API rejects values below 50 with 400 error
- All retry/batch fields required on every node: `autoRetryWhenAccuracyLessThan`, `autoRetryLimitWhenAccuracyIsLow`, `autoRetryCountWhenFailure`, `autoRetryWaitTimeWhenFailureInMs`, `enableAutoRetryWhenAccuracyIsLow`, `enableAutoRetryWhenFailure`, `isBackgroundTool`, `isBatchExecutionEnabled`, `isCodeExecutionEnabled`
- Do NOT add `fallbackModels` — not settable via API

## Linking Formats

| Context | Format | Fields |
|---------|--------|--------|
| PUT payload | Name-based | `linkedOutputParamNodeId` (node UUID) + `linkedOutputParamName` (param name) |
| PATCH input-output-params | UUID-based | `linkParamOutputId` (output param UUID) |

Both work correctly for their respective endpoints.

## GET Response Quirks

- `graph.edges` is always empty — edges are in node-level `childEdges`/`parentEdges`
- Prompts live at `originalTool.prompt` — not at top-level `toolConfiguration.prompt`
- Models live at `originalTool.preferredModel` — same nesting as prompts
- Two field locations: `toolConfiguration` (reflects PUT input) vs `toolConfiguration.originalTool` (effective config) — may differ

## Edge Rules

- Edge mirroring required: every edge must appear in both source's `childEdges[]` AND target's `parentEdges[]`
- `childEdges`/`parentEdges` must be arrays — omitting returns 400
- Empty arrays `[]` are valid but silently destroy all edges — always include full arrays

## Model Configuration

- Valid enterprise models: `BEDROCK_CLAUDE_OPUS_4_5`, `BEDROCK_CLAUDE_SONNET_4`, `GEMINI_25_FLASH_LITE`, etc.
- Invalid model strings silently default to Gemini 3 PRO — no error
- Haiku is not available on enterprise instance

## Prompt Authoring

- Escape literal braces: `{{` and `}}` — Beam uses `{var}` for template interpolation
- No "output format" as section header — conflicts with Beam internals
- No duplicate output param names on a single node
- Don't duplicate output schema in prompt — use `paramDescription` on output params instead
- Avoid backticks in prompts — use single quotes

## Authentication

- Use `x-api-key` header (recommended) — Bearer token auth fails on some endpoints
- Headers: `x-api-key`, `current-workspace-id`, `Content-Type: application/json`

## Task Attachments

- Filter out signature images (`image001.png`, `logo.png`, <50KB) from `.msg` files — these can cause tasks to hang indefinitely
