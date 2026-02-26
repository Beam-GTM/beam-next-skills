---
name: demo-documentation-generation-agent
version: 1.2
description: Generate comprehensive, fully-detailed documentation for Beam AI agents
  from graph.json files. Load when user says "document beam agent", "create agent
  documentation", "generate agent docs", "document this agent", "demo documentation",
  or provides a Beam agent graph file. Analyzes graph structure, extracts workflow,
  tools, integrations, descriptions, and generates complete documentation with NO
  placeholders.
author: Safi Haider
category: general
tags:
- beam-ai
platform: Beam AI
updated: '2026-01-06'
visibility: team
---
# Demo Documentation Generation Agent

**Automatically generate fully-detailed, comprehensive documentation for Beam AI agents from their graph definitions - no placeholders, just complete information.**

## When to Use

- You have a Beam agent graph.json file and need to create documentation
- You want to document an existing Beam agent with proper structure
- You need to generate Notion-formatted agent documentation
- You want to standardize agent documentation across your team
- You're creating an agent library and need consistent documentation

---

## What This Skill Does

This skill automates the entire process of creating professional documentation for Beam AI agents with **automatic detailed content generation**:

1. **Fetches Agent Graph** - Downloads the agent graph from Beam AI API using workspace and agent IDs
2. **Deep Analysis** - Parses all nodes, tools, connections, inputs, outputs, integrations, AND extracts:
   - Tool descriptions from toolConfiguration
   - Input parameter descriptions (paramDescription)
   - Output parameter descriptions
   - Integration purposes and functions
3. **Extracts Workflow** - Identifies the execution flow and step sequence
4. **Generates Detailed Documentation** - Creates comprehensive documentation with **real data extracted from the graph** - NO placeholders like "[Description needed]" or "[To be determined]"
5. **Outputs Multiple Formats** - Produces both markdown files and JSON analysis

**Time saved**: ~45-60 minutes of manual documentation work per agent
**Quality**: Production-ready documentation on first generation

---

## Prerequisites

### Required
- Beam AI API credentials in `.env`:
  ```bash
  BEAM_API_KEY=your_beam_api_key
  BEAM_WORKSPACE_ID=your_workspace_id
  ```

### Optional (for Notion export)
- Notion API credentials in `.env`:
  ```bash
  NOTION_API_KEY=your_notion_api_key
  ```

**Dependencies**: `requests`, `python-dotenv` (already installed)

---

## Quick Start

### Option 1: Fetch and Document (Recommended)
```bash
# Fetch agent graph from Beam AI and generate docs
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --workspace-id 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 \
  --agent-id 162e7c30-0d95-49ab-af99-7eef872a2d0d \
  --output-dir 04-workspace/beam-agents
```

### Option 2: From Existing Graph File
```bash
# Generate docs from existing graph.json file
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --graph-file 04-workspace/beam-agents/agent-graph-162e7c30.json \
  --output-dir 04-workspace/beam-agents
```

### Option 3: With Notion Page Update
```bash
# Generate docs and update Notion page (requires page access)
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --workspace-id 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 \
  --agent-id 162e7c30-0d95-49ab-af99-7eef872a2d0d \
  --notion-page-id 2df2cadf-bbbc-80e5-bbda-ffaf9e724ff2 \
  --output-dir 04-workspace/beam-agents
```

---

## Output Files

The skill generates multiple files in the specified output directory:

1. **`agent-graph-{agent-id}.json`** - Raw agent graph from Beam AI
2. **`agent-analysis-{agent-id}.json`** - Parsed analysis with extracted metadata
3. **`{agent-name}-documentation.md`** - Complete markdown documentation
4. **`{agent-name}-notion-blocks.json`** - Notion API blocks (if --notion flag used)

---

## Documentation Template

The generated documentation follows this comprehensive structure:

### 1. Header & Properties
- Agent name with emoji
- Feasibility status
- Priority level
- Platform status
- Vertical/team assignment
- One-line description
- Owner information

### 2. Agent Overview
- Detailed description (2-3 paragraphs)
- Trigger mechanism
- Workflow steps (numbered list)
- Data inputs (with descriptions)
- Expected outputs (with formats)
- Key integrations

### 3. Setup Instructions
- Prerequisites checklist
- Step-by-step setup guide
- Configuration details
- Trigger setup
- Verification steps

### 4. Branch Details
- **Description**: 4-5 line overview of overall capability and use case solved (NOT step-by-step process)
- "Choose If" decision criteria bullet list
- Graph visualization reference
- Detailed step-by-step breakdown of each node

### 5. Example Task Scenarios (H2 heading)
Each scenario uses **H3 toggle format**: `### ▶ Scenario X – Title`

- Scenario 1: Success/Happy path case
  - Description
  - How to use (numbered steps)
  - Data input examples (with specific field values)
  - Expected outputs (with field names and values)
  - Expected agent behavior (bullet list)
- Scenario 2: Not Found / Invalid case
  - Alternative flow for missing data
  - Rejection path behavior
- Scenario 3: Validation Failed case
  - Exists but fails criteria
  - Different rejection reason
- Scenario 4: Edge case (Pending/Partial status)
  - Intermediate states handling

### 6. How To Use
- Manual trigger instructions
- API/Postman usage
- Dashboard monitoring
- Input examples

### 7. Technical Details
- Agent graph structure
- Node breakdown
- Error handling configuration
- Performance considerations

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--workspace-id` | Yes* | Beam workspace ID (UUID format) |
| `--agent-id` | Yes* | Beam agent ID (UUID format) |
| `--graph-file` | Yes* | Path to existing graph.json file |
| `--output-dir` | No | Output directory (default: 04-workspace/beam-agents) |
| `--notion-page-id` | No | Notion page ID to update with documentation |
| `--format` | No | Output format: markdown, notion, or both (default: both) |
| `--agent-name` | No | Override agent name (auto-detected from graph) |

\* Either `--workspace-id` + `--agent-id` OR `--graph-file` is required

---

## Examples

### Example 1: Document Candidate Screening Agent
```bash
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --workspace-id 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 \
  --agent-id 162e7c30-0d95-49ab-af99-7eef872a2d0d \
  --agent-name "Candidate Screening Agent (Greenhouse)" \
  --output-dir 04-workspace/beam-agents

# Output:
# ✅ Fetched agent graph
# ✅ Analyzed 11 nodes, 6 inputs, 6 outputs
# ✅ Identified integrations: Airtable, Workable
# ✅ Generated documentation: candidate-screening-agent-documentation.md
```

### Example 2: From Existing Graph File
```bash
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --graph-file 04-workspace/beam-agents/my-agent-graph.json \
  --format markdown

# Output:
# ✅ Loaded graph from file
# ✅ Analyzed 8 nodes
# ✅ Generated: my-agent-documentation.md
```

### Example 3: Update Notion Page
```bash
python 03-skills/beam-document-agent/scripts/document_agent.py \
  --workspace-id 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 \
  --agent-id 162e7c30-0d95-49ab-af99-7eef872a2d0d \
  --notion-page-id 2df2cadf-bbbc-80e5-bbda-ffaf9e724ff2

# Output:
# ✅ Fetched agent graph
# ✅ Generated documentation
# ⚠️  Notion page not accessible - grant integration access
# ℹ️  Documentation saved to markdown for manual import
```

---

## How It Works

### Step 1: Fetch/Load Agent Graph
- If `--workspace-id` and `--agent-id` provided:
  - Authenticates with Beam AI API
  - Fetches agent graph via GET /agent-graphs/{agentId}
  - Saves raw graph to JSON file
- If `--graph-file` provided:
  - Loads existing graph.json file

### Step 2: Analyze Graph Structure
- Parses all nodes and their configurations
- Identifies tools used at each step
- Extracts input parameters (ai_fill, static, linked)
- Extracts output parameters
- Detects integrations (Airtable, Gmail, Slack, etc.)
- Maps workflow connections and sequence

### Step 3: Generate Documentation
- Determines agent name and purpose from graph
- Creates workflow step descriptions
- Generates input/output descriptions
- Formats integration list
- Builds setup instructions
- Creates usage scenarios
- Adds technical implementation details

### Step 4: Output Documentation
- **Markdown Format**: Human-readable, version-control friendly
- **Notion Blocks**: API-ready JSON for Notion import
- **Analysis JSON**: Structured data for programmatic use

### Step 5: Optional Notion Update
- If `--notion-page-id` provided and page is accessible:
  - Appends documentation blocks to Notion page
  - Handles API rate limits and batch uploads
- If page not accessible:
  - Saves Notion blocks to JSON file
  - Provides instructions for manual import

---

## Graph Analysis Details

### Node Information Extracted
- **Objective**: What the node does
- **Tool**: Tool name and function
- **Input Parameters**: All parameters with fill types
- **Output Parameters**: Generated outputs
- **Error Handling**: On-error behavior
- **Retry Configuration**: Auto-retry settings
- **Position**: Entry/exit node status

### Integration Detection
Automatically detects:
- Airtable (Create/Update Records)
- Gmail (Send Email, Read Inbox)
- Slack (Send Message, Post Channel)
- Greenhouse (Job Listings, Candidates)
- HubSpot (CRM operations)
- LinkedIn (Profile Search)
- PDF Extraction (Resume parsing)
- Custom API calls

### Workflow Sequencing
- Identifies entry nodes
- Follows edge connections
- Builds execution order
- Detects branching paths
- Maps conditional flows

---

## Error Handling

| Issue | Behavior |
|-------|----------|
| Invalid workspace/agent ID | Error message with ID format guidance |
| API authentication failure | Check .env credentials guidance |
| Graph file not found | File path validation error |
| Notion page not accessible | Save to file + provide access instructions |
| Missing required parameters | Parameter validation with examples |
| API rate limit | Automatic retry with backoff |

---

## Best Practices

### 1. Organize Your Agents
```
04-workspace/beam-agents/
├── candidate-screening/
│   ├── agent-graph.json
│   ├── documentation.md
│   └── analysis.json
├── invoice-processing/
│   ├── agent-graph.json
│   └── documentation.md
└── README.md
```

### 2. Version Control
- Commit graph.json files to track agent changes
- Include documentation.md in version control
- Use analysis.json for programmatic agent discovery

### 3. Team Collaboration
- Generate docs before sharing agents
- Keep Notion documentation synced
- Use consistent naming conventions

### 4. Update Cadence
- Regenerate docs after agent modifications
- Review documentation during agent reviews
- Update scenarios based on real usage

---

## Tips

**Finding Workspace & Agent IDs:**
- Navigate to your agent in Beam AI
- URL format: `https://app.beam.ai/{workspace-id}/{agent-id}`
- Copy IDs from browser address bar

**Customizing Documentation:**
- Edit the markdown file after generation
- Add custom scenarios specific to your use case
- Include screenshots in Notion manually

**Notion Integration:**
- Grant integration access: Page menu → Connections
- Integration name matches your NOTION_API_KEY
- Can update existing pages or create new ones

**Batch Processing:**
- Create a script to document all agents in workspace
- Use the analysis.json files for agent cataloging
- Generate an index page linking all agent docs

---

## Advanced Usage

### Batch Document All Agents
```bash
# List all agents in workspace
python 00-system/skills/beam/beam-master/scripts/list_agents.py

# Document each one
for agent_id in agent_ids; do
  python 03-skills/beam-document-agent/scripts/document_agent.py \
    --workspace-id $WORKSPACE_ID \
    --agent-id $agent_id \
    --output-dir 04-workspace/beam-agents/$agent_id
done
```

### Create Agent Catalog
```bash
# Generate docs for all agents
python 03-skills/beam-document-agent/scripts/batch_document.py \
  --workspace-id 505d2090-2b5d-4e45-b0f4-cc3a0b299aa8 \
  --output-dir 04-workspace/beam-agents \
  --create-index
```

### Custom Templates
- Copy and modify `templates/documentation_template.md`
- Use `--template` flag to specify custom template
- Templates support Jinja2 syntax

---

## Troubleshooting

**"Agent graph not found"**
- Verify workspace and agent IDs are correct
- Check BEAM_API_KEY has access to workspace
- Ensure agent exists in the specified workspace

**"Notion page not accessible"**
- Go to Notion page → "..." menu → "Connections"
- Add the integration associated with your API key
- Re-run the script

**"Invalid graph structure"**
- Ensure graph file is valid JSON
- Check graph was fetched from Beam AI API
- Verify graph has required fields: nodes, edges

**"Missing integrations in output"**
- Integration detection is based on tool names
- Custom tools may not be auto-detected
- Manually add to the markdown file after generation

---

## Related Skills

- **beam-get-task-details** - Inspect agent task execution
- **create-beam-task-auto-trigger** - Create webhook automation
- **notion-connect** - Manage Notion workspace integration

---

## Changelog

### v1.2 (2026-01-06)
- **Renamed skill** from `beam-document-agent` to `demo-documentation-generation-agent`
- **Updated documentation format**:
  - Branch Description must be 4-5 line overview (NOT step-by-step process)
  - Example Task Scenarios as H2 heading with H3 toggles for each scenario
  - Scenario format: `### ▶ Scenario X – Title`
- Standardized scenario structure with all required sections

### v1.1 (2026-01-06)
- **Enhanced auto-generation**: Now extracts and uses actual descriptions from graph
- **No placeholders**: Generates fully-detailed documentation on first run
- Input descriptions extracted from `paramDescription` fields
- Output descriptions automatically populated
- Integration purposes and functions included
- Tool descriptions from `toolConfiguration` added to node breakdown
- Required vs total parameter counts displayed
- Auto-generated agent descriptions based on workflow analysis
- Production-ready documentation without manual editing

### v1.0 (2026-01-05)
- Initial release
- Fetch agent graphs from Beam AI API
- Analyze graph structure and extract metadata
- Generate comprehensive markdown documentation
- Create Notion-ready blocks
- Support both online (API) and offline (file) modes
- Automatic integration detection
- Workflow sequencing and step descriptions
- Usage scenarios generation
- Technical implementation details

---

**Version**: 1.2
**Updated**: 2026-01-06
**Status**: Production Ready
