---
name: generate-demo-agent-sample-input-data
version: 1.0
description: Generate sample test inputs and expected results for Beam.ai agents.
  Load when user says "generate demo data", "create sample inputs for agent", "demo
  data for beam agent", "test data for agent", "sample input data", or provides a
  Beam agent URL asking for test cases.
author: Hassaan Ahmed, Safi Haider
category: general
tags:
- beam-ai
platform: Beam AI
updated: '2026-01-06'
visibility: team
---
# Generate Demo Agent Sample Input Data

Analyze a Beam.ai agent's workflow and generate realistic sample input data with expected results for demos and testing.

## Purpose

This skill automates the creation of demo/test data for Beam.ai agents by:
1. Fetching the agent graph from Beam API
2. Analyzing workflow nodes, inputs, and decision logic
3. Identifying data sources (Google Sheets, Airtable, etc.)
4. Generating sample inputs that cover different scenarios
5. Creating expected results summary table

**Use Cases:**
- QA testing of new agents
- Creating demo/sample data for client presentations
- Documenting agent behavior with examples
- Onboarding team members to understand agent logic

**Time Estimate**: 5-10 minutes

---

## Inputs Required

| Input | Required | Description |
|-------|----------|-------------|
| Beam Agent URL | Yes | Full URL like `https://app.beam.ai/{workspace_id}/{agent_id}` |
| Reference Data | Optional | Master dataset the agent checks against (Google Sheets data, Airtable records, etc.) |
| Number of Samples | Optional | How many test cases to generate (default: 5) |

---

## Workflow

### Step 1: Parse Agent URL

Extract workspace_id and agent_id from the provided URL.

**URL Format:**
```
https://app.beam.ai/{workspace_id}/{agent_id}
https://app.beam.ai/{workspace_id}/{agent_id}/flow
```

**Example:**
```
URL: https://app.beam.ai/12172090-4128-4dbb-ace2-0d60af617cb4/3aa08542-6f71-43e6-9120-72d78015e7ab
Workspace ID: 12172090-4128-4dbb-ace2-0d60af617cb4
Agent ID: 3aa08542-6f71-43e6-9120-72d78015e7ab
```

---

### Step 2: Fetch Agent Graph

Use the Beam API to fetch the agent's graph structure.

**Run the fetch script:**
```bash
python3 03-skills/generate-demo-agent-sample-input-data/scripts/fetch_and_analyze.py <workspace_id> <agent_id>
```

**Or manually via API:**
```python
# Step 1: Get access token
auth_resp = requests.post(
    "https://api.beamstudio.ai/auth/access-token",
    headers={"Content-Type": "application/json"},
    json={"apiKey": "<BEAM_API_KEY from .env>"}
)
token = auth_resp.json().get("idToken")

# Step 2: Fetch graph
graph_resp = requests.get(
    f"https://api.beamstudio.ai/agent-graphs/{agent_id}",
    headers={
        "Authorization": f"Bearer {token}",
        "current-workspace-id": workspace_id,
        "Content-Type": "application/json"
    }
)
```

---

### Step 3: Analyze Agent Structure

Extract key information from the graph:

**3a. Identify Entry Point & Trigger Type**
- Email trigger (Gmail integration)
- Webhook trigger
- Manual trigger
- Scheduled trigger

**3b. Extract Input Parameters**
Look at first non-entry node's `toolConfiguration.inputParams`:
```python
for node in graph["nodes"]:
    if not node.get("isEntryNode"):
        tool_config = node.get("toolConfiguration", {})
        inputs = tool_config.get("inputParams", [])
        for param in inputs:
            print(f"- {param['paramName']}: {param['paramDescription']}")
```

**3c. Identify Data Sources**
Look for nodes with tools like:
- "Retrieve All Rows" → Google Sheets
- "Retrieve Airtable Records" → Airtable
- "Query Database" → SQL

**3d. Map Decision Logic**
Identify nodes that branch (have multiple childEdges with conditions):
- Approval/Rejection paths
- Validation pass/fail
- Error handling

---

### Step 4: Request Reference Data (If Applicable)

If the agent checks against a master dataset, ask user:

```
I see this agent validates against a data source (Google Sheets/Airtable).

To generate accurate test data, please provide the reference dataset.
You can:
1. Paste the data directly (CSV or table format)
2. Provide the spreadsheet/database URL
3. Skip (I'll generate generic samples)
```

---

### Step 5: Generate Sample Test Inputs

Based on analysis, create test cases covering:

| Scenario Type | Description |
|---------------|-------------|
| **Happy Path** | Valid input that should succeed |
| **Not Found** | ID/record doesn't exist in source |
| **Validation Fail** | Exists but fails criteria |
| **Pending/Incomplete** | Edge case - partial status |
| **Minimal Input** | Tests handling of sparse data |

**For Email-Triggered Agents:**
Generate realistic email samples with:
- From address
- Subject line
- Body with required fields
- Proper formatting

**For Webhook/API Agents:**
Generate JSON payloads matching expected schema.

---

### Step 6: Create Expected Results Summary

Generate a table summarizing each test case:

```markdown
| # | Sample | Key Input | Expected Outcome | Reason |
|---|--------|-----------|------------------|--------|
| 1 | Valid customer | ID: PROP001 | ✅ Accept | Exists + Passed |
| 2 | Unknown ID | ID: PROP999 | ❌ Reject | Not in database |
| 3 | Failed status | ID: PROP004 | ❌ Reject | Inspection failed |
```

---

### Step 7: Output & Save

Present the generated test data to user and optionally save:

```
Save test data to: 04-workspace/beam-demo-data/{agent-name}/
   ├── sample-inputs/
   │   ├── sample-1-valid.txt
   │   ├── sample-2-not-found.txt
   │   └── ...
   ├── expected-results.md
   └── agent-analysis.md
```

---

## Example Output

### Agent Analysis
```
Agent: Property Eligibility Checker
Trigger: Email
Data Source: Google Sheets (Property Master)

Input Fields Expected:
- Property_ID (required)
- Property_Address
- Owner_Name
- Property_Type
- Coverage_Limit

Decision Logic:
1. Check if Property_ID exists in master sheet
2. Check if Inspection_Status = "Passed"
3. Accept if both conditions met, else reject
```

### Generated Test Cases
[5 sample emails/inputs with expected outcomes table]

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired API key | Check BEAM_API_KEY in .env |
| 404 Not Found | Invalid agent ID | Verify URL is correct |
| Empty graph | Agent has no nodes | Agent may be empty/draft |
| No reference data | User didn't provide dataset | Generate generic samples |

---

## Notes

- This skill works best when reference data is provided
- For complex agents with many branches, focus on main happy/unhappy paths
- Generated samples are starting points - user should customize for specific edge cases
- Always verify generated data makes sense for the specific domain

---

**Version**: 1.0
**Created**: 2026-01-06
**Author**: Nexus
