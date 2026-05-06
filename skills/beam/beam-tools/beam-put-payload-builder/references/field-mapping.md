# GET→PUT Field Mapping

Field locations differ between `GET /agent-graphs/{agentId}` response and `PUT /agent-graphs/{agentId}` request body. This document maps every difference.

## Critical Mapping Differences

| Field | GET Location | PUT Location |
|-------|-------------|-------------|
| Prompt | `toolConfiguration.originalTool.prompt` | `toolConfiguration.prompt` |
| Model | `toolConfiguration.originalTool.preferredModel` | `toolConfiguration.preferredModel` |
| Description | `toolConfiguration.originalTool.description` | `toolConfiguration.description` |
| Input links | `linkParamOutputId` (UUID) | `linkedOutputParamNodeId` + `linkedOutputParamName` |
| Edges | `node.childEdges[]` / `node.parentEdges[]` | Same (NOT `graph.edges[]` — always empty) |

## Link Translation Algorithm

GET uses UUID-based linking (`linkParamOutputId` = UUID of the source output param).
PUT uses name-based linking (`linkedOutputParamNodeId` = source node UUID + `linkedOutputParamName` = output param name).

### Translation steps

1. **Build reverse lookup**: scan ALL nodes' output params (both `toolConfiguration.outputParams` and `originalTool.outputParams`), mapping each output param `id` → `(node_id, paramName)`
2. **For each linked input param**: look up `linkParamOutputId` in the reverse lookup to get `(node_id, paramName)`
3. **Set PUT fields**: `linkedOutputParamNodeId` = node_id, `linkedOutputParamName` = paramName

### Example

```
GET input param:
  { "paramName": "email_body", "fillType": "linked", "linkParamOutputId": "abc-123" }

Lookup: "abc-123" → (node_id="def-456", paramName="raw_email")

PUT input param:
  { "paramName": "email_body", "fillType": "linked",
    "linkedOutputParamNodeId": "def-456", "linkedOutputParamName": "raw_email" }
```

## Required Swagger DTO Fields

### CompleteAgentGraphNodeDto (node)

| Field | Type | Default |
|-------|------|---------|
| `id` | string (UUID) | from GET |
| `objective` | string | "" |
| `evaluationCriteria` | array | [] |
| `isEntryNode` | boolean | false |
| `isExitNode` | boolean | false |
| `xCoordinate` | number | 0 |
| `yCoordinate` | number | 0 |
| `isEvaluationEnabled` | boolean | false |
| `isAttachmentDataPulledIn` | boolean | true |
| `onError` | "STOP"\|"CONTINUE" | "STOP" |
| `autoRetryWhenAccuracyLessThan` | number | 80 |
| `autoRetryLimitWhenAccuracyIsLow` | number | 1 |
| `autoRetryCountWhenFailure` | number | 1 |
| `autoRetryWaitTimeWhenFailureInMs` | number | 1000 |
| `enableAutoRetryWhenAccuracyIsLow` | boolean | false |
| `enableAutoRetryWhenFailure` | boolean | false |
| `childEdges` | array | [] |
| `parentEdges` | array | [] |
| `toolConfiguration` | object | omit if no tool |

### CompleteAgentGraphNodeToolConfigurationDto (tool config)

| Field | Type | Required |
|-------|------|----------|
| `toolFunctionName` | string | YES |
| `toolName` | string | no (max 200 chars, no `.` `!`) |
| `description` | string | no |
| `requiresConsent` | boolean | no |
| `isMemoryTool` | boolean | no |
| `memoryLookupInstruction` | string | no |
| `isBackgroundTool` | boolean | no |
| `isBatchExecutionEnabled` | boolean | no |
| `isCodeExecutionEnabled` | boolean | no |
| `inputParams` | array | no (WARNING: `[]` deletes all) |
| `outputParams` | array | no |
| `prompt` | string | no |
| `preferredModel` | string | no |

### Input Param DTO

| Field | Required | Notes |
|-------|----------|-------|
| `fillType` | YES | "ai_fill"\|"static"\|"linked"\|"user_input"\|"from_memory" |
| `position` | YES | 0-indexed |
| `required` | YES | boolean |
| `dataType` | YES | "string"\|"number"\|"boolean"\|"object" |
| `reloadProps` | YES | always false |
| `remoteOptions` | YES | always false |
| `paramName` | YES | |
| `paramDescription` | YES | |
| `linkedOutputParamNodeId` | if linked | source node UUID |
| `linkedOutputParamName` | if linked | source output param name |
| `staticValue` | if static | |

### Output Param DTO

| Field | Required |
|-------|----------|
| `isArray` | YES |
| `paramName` | YES |
| `position` | YES |
| `paramDescription` | YES |
| `dataType` | YES |
| `outputExample` | no |

### Edge DTO

| Field | Required |
|-------|----------|
| `sourceAgentGraphNodeId` | YES |
| `targetAgentGraphNodeId` | YES |
| `condition` | YES (empty string for unconditional) |
| `isAttachmentDataPulledIn` | YES |
