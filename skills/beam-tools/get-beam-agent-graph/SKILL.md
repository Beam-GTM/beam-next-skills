---
name: get-beam-agent-graph
version: '1.0'
description: Fetch and save Beam.ai agent graph JSON via API. Load when user says
  "get agent graph", "fetch beam graph", "download agent graph", "beam agent graph",
  "get graph for agent", or provides a workspace ID and agent ID to retrieve the graph
  structure.
author: Safi Haider
category: general
tags:
- api
- beam-ai
platform: Beam AI
updated: '2026-01-05'
visibility: team
---
# Get Beam Agent Graph

Fetch agent graph JSON from Beam.ai API and save to local storage with meaningful filename.

## Purpose

This skill retrieves the complete agent graph structure from Beam.ai including nodes, edges, configurations, and metadata. It authenticates with the Beam API, fetches the graph for a specific agent, and stores it locally for analysis, backup, or documentation purposes.

**Key Features**:
- Two-step authentication (API key → access token → graph data)
- Automatic meaningful filename generation (includes agent name if available)
- Organized storage in `04-workspace/beam-graphs/`
- Full graph structure preserved in JSON format

**Time Estimate**: 1-2 minutes

---

## Workflow

### Step 1: Verify Configuration

**Check if BEAM_API_KEY exists in .env:**

```bash
grep "BEAM_API_KEY" ../.env
```

**If missing:**
```
[ERROR] BEAM_API_KEY not found in .env

Please add your Beam API key to .env:
BEAM_API_KEY=your-key-here
```

Ask user to provide their Beam API key and add it to `.env` file.

---

### Step 2: Get Required Parameters

**Required inputs:**
- Workspace ID (UUID format)
- Agent ID (UUID format)

**Ask user if not provided:**
```
To fetch the agent graph, I need:
1. Workspace ID: <uuid>
2. Agent ID: <uuid>

Please provide both IDs.
```

---

### Step 3: Execute Fetch Script

**Run the get_agent_graph.py script:**

```bash
python3 03-skills/get-beam-agent-graph/scripts/get_agent_graph.py <workspace_id> <agent_id>
```

**Optional: Specify custom output directory:**
```bash
python3 03-skills/get-beam-agent-graph/scripts/get_agent_graph.py <workspace_id> <agent_id> --output ./custom/path
```

**The script will:**
1. Load BEAM_API_KEY from .env
2. Call `/auth/access-token` to get access token
3. Call `/agent-graphs/{agentId}` to fetch graph
4. Save to `04-workspace/beam-graphs/{filename}.json`

---

### Step 4: Verify and Report Success

**On success:**
```
[SUCCESS] Agent graph saved to: 04-workspace/beam-graphs/AgentName_162e7c30_graph_20260105_143022.json
```

**Read the saved file to confirm:**
```bash
cat 04-workspace/beam-graphs/<filename>.json | head -20
```

Show user:
- File path
- Agent name (if extracted from graph)
- File size
- Brief summary of graph structure (node count, etc.)

---

## API Reference

For detailed API documentation, see [references/api-reference.md](references/api-reference.md).

**Quick reference:**

**Step 1: Get Access Token**
- Endpoint: `POST https://api.beamstudio.ai/auth/access-token`
- Header: `x-api-key: <BEAM_API_KEY>`
- Returns: `access_token`

**Step 2: Get Agent Graph**
- Endpoint: `GET https://api.beamstudio.ai/agent-graphs/{agentId}`
- Headers: `Authorization: Bearer <token>`, `x-workspace-id: <workspace_id>`
- Returns: Complete agent graph JSON

---

## Output Format

**Filename pattern:**
- With agent name: `{AgentName}_{agentId_first8}graph_{timestamp}.json`
- Without name: `{agentId}_graph_{timestamp}.json`

**Example filenames:**
```
TrueSearch_Scheduler_162e7c30_graph_20260105_143022.json
162e7c30-0d95-49ab-af99-7eef872a2d0d_graph_20260105_143022.json
```

**Storage location:**
```
04-workspace/beam-graphs/
```

---

## Error Handling

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| BEAM_API_KEY not found | Missing from .env | Add to .env file |
| 401 Unauthorized | Invalid API key | Check BEAM_API_KEY value |
| 404 Not Found | Invalid agent ID | Verify agent ID is correct |
| 403 Forbidden | No workspace access | Check workspace ID and permissions |

**For API details:** See [references/api-reference.md](references/api-reference.md)

---

## Resources

### scripts/

**scripts/get_agent_graph.py** - Main script to fetch and save agent graphs
- Handles authentication flow
- Fetches graph via Beam API
- Saves with meaningful filename
- Supports custom output directory

### references/

**references/api-reference.md** - Beam API documentation
- Authentication endpoints
- Agent graph endpoints
- Error codes and responses

---

## Notes

**About Beam API Authentication:**
- Access tokens are short-lived (typically 1 hour)
- The script requests a new token for each execution
- API key is stored in .env and never logged

**About Storage:**
- Graphs are timestamped to prevent overwrites
- Default location: `04-workspace/beam-graphs/`
- Custom output directory supported via `--output` flag

**About Graph Data:**
- Complete graph structure including nodes, edges, configs
- JSON format for easy parsing and analysis
- Preserves all metadata from Beam API
