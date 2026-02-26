---
name: beam-feedback-automation
version: '1.0'
description: Universal feedback collection automation for ANY Beam agent. Load when
  user mentions 'feedback automation', 'create feedback sheet', 'agent feedback',
  'evaluation sheet', 'feedback for [agent-name]', or provides a Beam agent ID/URL.
  Dynamically analyzes agents via API, generates smart feedback fields, creates Google
  Apps Script, deploys to Sheets, and manages complete feedback workflow.
category: integrations
tags:
- api
- automation
- beam-ai
platform: Beam AI
updated: '2026-02-02'
visibility: team
---
# Beam Feedback Automation

**Universal feedback collection system for ANY Beam agent.**

## Purpose

Automate the complete feedback collection workflow you manually created for TA Interview Agent - but make it work for ANY Beam agent by dynamically analyzing the agent structure via API.

**What it automates:**
1. ✅ Agent analysis via Beam API (fetch graph, understand inputs/outputs)
2. ✅ Smart feedback field generation (based on agent output schema)
3. ✅ Google Apps Script template generation (customized per agent)
4. ✅ Google Sheets deployment (pre-filled with task data)
5. ✅ Batch feedback sheet creation (multiple tasks at once)
6. ✅ Email distribution (send to reviewers)
7. ✅ Results aggregation (collect and analyze feedback)

---

## Core Workflow

### Input Options
User can provide:
- **Agent ID**: `agent_xyz789`
- **Agent URL**: `https://beam.ai/agent/xyz789`
- **Agent name**: "TA Interview Agent" (will search via API)

### Process Flow
```
1. Analyze Agent (via Beam API)
   ↓
2. Generate Feedback Fields (smart logic based on outputs)
   ↓
3. Create Apps Script Template (customized)
   ↓
4. Deploy to Google Sheets
   ↓
5. Fetch Tasks & Pre-fill Sheets
   ↓
6. Send Email Requests
   ↓
7. Monitor & Aggregate Results
```

---

## Workflow 1: Analyze Agent

**Trigger**: User provides agent ID/URL or name

**Steps**:
1. Extract agent ID from input (URL, direct ID, or search by name)
2. Fetch agent graph from Beam API:
   ```bash
   python scripts/analyze_agent.py --agent-id <agent_id>
   ```
3. Parse graph to extract:
   - Agent name and description
   - Input fields (data types, required/optional)
   - Output fields (data types, structure)
   - Node sequence (for understanding workflow)
4. Save analysis to `analysis/<agent_id>_schema.json`
5. Display summary:
   ```
   Agent: TA Interview Agent
   Inputs: 3 fields (candidate_email, job_title, resume_url)
   Outputs: 5 fields (overall_score, technical_skills[], soft_skills[], strengths, weaknesses)

   Ready to generate feedback fields!
   ```

**API Endpoint**: `GET https://api.beam.ai/v1/agent/{agent_id}`

---

## Workflow 2: Generate Feedback Fields

**Trigger**: After successful agent analysis

**Steps**:
1. Run smart field generator:
   ```bash
   python scripts/generate_feedback_fields.py --schema analysis/<agent_id>_schema.json
   ```
2. Logic applies these rules:

   **For NUMBER outputs** (e.g., `overall_score`):
   - Generate: `{field_name} Accuracy` (rating 1-5)
   - Generate: `{field_name} Comments` (text feedback)

   **For ARRAY outputs** (e.g., `technical_skills[]`):
   - Generate: `{field_name} Extraction Accuracy` (rating 1-5)
   - Generate: `Missing {field_name}` (checkbox list)
   - Generate: `Incorrect {field_name}` (checkbox list)

   **For TEXT outputs** (e.g., `strengths`):
   - Generate: `{field_name} Quality` (rating 1-5)
   - Generate: `{field_name} Accuracy` (Yes/No/Partial)
   - Generate: `{field_name} Comments` (text feedback)

   **For BOOLEAN outputs**:
   - Generate: `{field_name} Correct?` (Yes/No)

3. Save to `analysis/<agent_id>_feedback_fields.json`
4. Display preview:
   ```
   Generated 12 feedback fields:

   ✓ Overall Score Accuracy (Rating 1-5)
   ✓ Overall Score Comments (Text)
   ✓ Technical Skills Extraction Accuracy (Rating 1-5)
   ✓ Missing Technical Skills (Checkbox)
   ✓ Incorrect Technical Skills (Checkbox)
   ...

   Approve? (y/n)
   ```
5. Allow user to customize/approve before proceeding

---

## Workflow 3: Create Apps Script Template

**Trigger**: After feedback fields approved

**Steps**:
1. Run Apps Script generator:
   ```bash
   python scripts/generate_apps_script.py \
     --agent-id <agent_id> \
     --fields analysis/<agent_id>_feedback_fields.json \
     --output scripts/<agent_id>_apps_script.js
   ```
2. Generator creates customized Apps Script with:
   - `onOpen()` trigger → Custom menu
   - `prefillAgentData()` → Fetch from Beam API
   - `sendFeedbackEmail()` → Email template
   - `aggregateResults()` → Collect all feedback
   - `highlightIncomplete()` → Visual indicators
   - Dynamic field references (based on generated fields)

3. Display script preview and save to `scripts/<agent_id>_apps_script.js`

**Template Base**: `templates/apps_script_template.js`

---

## Workflow 4: Deploy to Google Sheets

**Trigger**: After Apps Script generated

**Steps**:
1. Run Google Sheets deployment:
   ```bash
   python scripts/deploy_to_sheets.py \
     --agent-id <agent_id> \
     --template-id <google_sheets_template_id> \
     --script scripts/<agent_id>_apps_script.js
   ```
2. Script performs:
   - Create new Google Sheet (from template or blank)
   - Set up header row with:
     - Task ID
     - Task URL
     - All agent output fields
     - All generated feedback fields
     - Reviewer Email
     - Status
   - Deploy Apps Script to sheet
   - Configure triggers and permissions
3. Return Sheet URL:
   ```
   ✅ Sheet deployed successfully!

   Sheet: https://docs.google.com/spreadsheets/d/abc123

   Ready to create feedback requests!
   ```

---

## Workflow 5: Batch Create Feedback Sheets

**Trigger**: "Create feedback sheets for [N] tasks" or "Create sheets for task IDs [...]"

**Steps**:
1. Run batch sheet creator:
   ```bash
   python scripts/create_feedback_sheets.py \
     --agent-id <agent_id> \
     --sheet-id <sheet_id> \
     --task-count 50 \
     # OR
     --task-ids task_abc,task_def,task_ghi
   ```
2. Script performs:
   - Fetch latest N tasks from Beam API (or specific task IDs)
   - For each task:
     - Extract all output data from task result
     - Create new row in sheet
     - Pre-fill with task data
     - Set status to "Pending Review"
   - Generate unique review links per task
3. Display progress:
   ```
   Creating feedback sheets...
   ✓ Task task_abc123 → Row 2
   ✓ Task task_def456 → Row 3
   ✓ Task task_ghi789 → Row 4
   ...

   Created 50 feedback requests!
   ```

**Beam API Endpoint**: `GET https://api.beam.ai/v1/task?agent_id={agent_id}&limit=50&status=completed`

---

## Workflow 6: Send Email Requests

**Trigger**: "Send feedback requests" (after sheets created)

**Steps**:
1. Run email sender:
   ```bash
   python scripts/send_emails.py \
     --sheet-id <sheet_id> \
     --reviewer-email reviewer@example.com \
     --template templates/email_template.html
   ```
2. Script performs:
   - Read all rows with status "Pending Review"
   - For each row:
     - Generate review link (direct to specific row)
     - Populate email template with:
       - Agent name
       - Task summary
       - Review link
       - Instructions
     - Send via Gmail API or SMTP
     - Update status to "Email Sent"
3. Display progress:
   ```
   Sending feedback requests...
   ✓ Task task_abc123 → reviewer@example.com
   ✓ Task task_def456 → reviewer@example.com
   ...

   Sent 50 email requests!
   ```

**Email Template**: `templates/email_template.html`

---

## Workflow 7: Aggregate Results

**Trigger**: "Aggregate feedback results" or "Show feedback summary"

**Steps**:
1. Run results aggregator:
   ```bash
   python scripts/aggregate_results.py \
     --sheet-id <sheet_id> \
     --output reports/<agent_id>_feedback_report.json
   ```
2. Script performs:
   - Read all completed feedback rows
   - Calculate metrics:
     - Average accuracy scores per field
     - Most common issues/missing items
     - Completion rate
     - Response time distribution
   - Generate insights:
     - Identify lowest-scoring fields
     - Flag patterns in feedback comments
     - Suggest agent improvements
3. Display summary:
   ```
   📊 Feedback Results Summary

   Responses: 47/50 (94% completion)

   Average Scores:
   - Overall Score Accuracy: 4.2/5
   - Technical Skills Extraction: 3.8/5 ⚠️
   - Soft Skills Extraction: 4.5/5

   Top Issues:
   - Missing Technical Skills: "Python" (12 occurrences)
   - Incorrect assessment of leadership (8 occurrences)

   💡 Suggested Improvements:
   1. Enhance technical skills extraction prompt
   2. Add leadership evaluation criteria
   ```

4. Save detailed report to `reports/<agent_id>_feedback_report.json`

---

## Command Reference

### Quick Start (Full Workflow)
```bash
$ beam-feedback-automation agent_xyz789 --tasks 50
```

This runs the complete workflow:
1. Analyze agent
2. Generate feedback fields
3. Create Apps Script
4. Deploy to Sheets
5. Create 50 feedback sheets
6. Send email requests
7. Generate summary report

### Individual Commands

**Analyze Agent**:
```bash
$ beam-feedback-automation analyze --agent-id agent_xyz789
$ beam-feedback-automation analyze --url https://beam.ai/agent/xyz789
$ beam-feedback-automation analyze --name "TA Interview Agent"
```

**Generate Feedback Fields**:
```bash
$ beam-feedback-automation generate-fields --agent-id agent_xyz789
```

**Deploy to Sheets**:
```bash
$ beam-feedback-automation deploy --agent-id agent_xyz789
```

**Create Feedback Sheets**:
```bash
$ beam-feedback-automation create-sheets --agent-id agent_xyz789 --tasks 50
$ beam-feedback-automation create-sheets --agent-id agent_xyz789 --task-ids task_a,task_b,task_c
```

**Send Emails**:
```bash
$ beam-feedback-automation send-emails --sheet-id abc123 --reviewer reviewer@example.com
```

**Aggregate Results**:
```bash
$ beam-feedback-automation aggregate --sheet-id abc123
```

---

## Configuration

**Required Environment Variables**:
```bash
BEAM_API_KEY=your_beam_api_key
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
```

**Optional Settings** (`config.yaml`):
```yaml
default_reviewer_email: "team@example.com"
email_template: "templates/custom_email.html"
sheets_template_id: "1abc123_template_id"
batch_size: 50
auto_send_emails: true
```

---

## File Structure

```
beam-feedback-automation/
├── SKILL.md                        # This file
├── config.yaml                     # Configuration
├── scripts/
│   ├── analyze_agent.py           # Fetch & parse agent graph
│   ├── generate_feedback_fields.py # Smart field generation logic
│   ├── generate_apps_script.py    # Apps Script generator
│   ├── deploy_to_sheets.py        # Google Sheets deployment
│   ├── create_feedback_sheets.py  # Batch sheet creator
│   ├── send_emails.py             # Email distribution
│   └── aggregate_results.py       # Results analysis
├── templates/
│   ├── apps_script_template.js    # Base Apps Script
│   └── email_template.html        # Email template
├── analysis/                       # Generated agent schemas
│   ├── agent_xyz_schema.json
│   └── agent_xyz_feedback_fields.json
├── reports/                        # Feedback reports
│   └── agent_xyz_feedback_report.json
└── examples/
    └── usage.md                    # Usage examples
```

---

## Examples

### Example 1: TA Interview Agent Feedback
```bash
$ beam-feedback-automation agent_ta_interview --tasks 50

✅ Analyzed agent: TA Interview Agent
✅ Generated 12 feedback fields
✅ Created Apps Script
✅ Deployed to Google Sheets
✅ Created 50 feedback requests
✅ Sent 50 emails to reviewer@booth.com
📊 View results: https://docs.google.com/spreadsheets/d/abc123
```

### Example 2: Custom Agent with Specific Tasks
```bash
$ beam-feedback-automation analyze --name "Email Classifier"
$ beam-feedback-automation generate-fields --agent-id agent_email_classifier
$ beam-feedback-automation deploy --agent-id agent_email_classifier
$ beam-feedback-automation create-sheets --agent-id agent_email_classifier --task-ids task_1,task_2,task_3
$ beam-feedback-automation send-emails --sheet-id xyz789 --reviewer qa@company.com
```

### Example 3: Aggregate Results After Manual Review
```bash
$ beam-feedback-automation aggregate --sheet-id abc123

📊 Feedback Results Summary
Responses: 48/50 (96% completion)
Average Accuracy: 4.3/5
Top Issue: Missing email categories (15 occurrences)

💡 Suggested Improvements:
1. Expand category taxonomy
2. Add confidence scores to classifications
```

---

## Smart Field Generation Logic

### Field Type Mappings

| Agent Output Type | Generated Feedback Fields |
|-------------------|---------------------------|
| `number` (score) | Accuracy (rating 1-5), Comments (text) |
| `array` (list) | Extraction Accuracy (rating 1-5), Missing Items (checkbox), Incorrect Items (checkbox) |
| `text` (long) | Quality (rating 1-5), Accuracy (Yes/No/Partial), Comments (text) |
| `boolean` | Correct? (Yes/No) |
| `object` (structured) | Per-field breakdown (recursive logic) |

### Example Output Schema → Feedback Fields

**Agent Output**:
```json
{
  "overall_score": 85,
  "technical_skills": ["Python", "SQL", "React"],
  "strengths": "Strong problem-solving abilities...",
  "hire_recommendation": true
}
```

**Generated Feedback Fields**:
```json
[
  {"name": "Overall Score Accuracy", "type": "rating", "scale": 5},
  {"name": "Overall Score Comments", "type": "text"},
  {"name": "Technical Skills Extraction Accuracy", "type": "rating", "scale": 5},
  {"name": "Missing Technical Skills", "type": "checkbox_list"},
  {"name": "Incorrect Technical Skills", "type": "checkbox_list"},
  {"name": "Strengths Quality", "type": "rating", "scale": 5},
  {"name": "Strengths Accuracy", "type": "select", "options": ["Yes", "No", "Partial"]},
  {"name": "Strengths Comments", "type": "text"},
  {"name": "Hire Recommendation Correct?", "type": "select", "options": ["Yes", "No"]}
]
```

---

## Integration Points

### Beam API
- `GET /v1/agent/{agent_id}` - Fetch agent graph
- `GET /v1/task?agent_id={id}&limit=N` - Fetch tasks for feedback

### Google Sheets API
- Create/update spreadsheets
- Deploy Apps Script
- Read/write cell data

### Gmail API (Optional)
- Send feedback request emails
- Track email delivery

### Airtable/Notion (Optional)
- Push aggregated results to project tracking
- Link feedback to recruitment pipeline

---

## Error Handling

| Error | Solution |
|-------|----------|
| Agent not found | Verify agent ID or search by name |
| No completed tasks | Wait for tasks or use different agent |
| Google Sheets auth failed | Re-authenticate with `gcloud auth` |
| Email sending failed | Check SMTP credentials or use Gmail API |
| Invalid output schema | Manually define feedback fields |

---

## Future Enhancements

**Phase 2**:
- [ ] Multi-reviewer support (assign different reviewers per task)
- [ ] Confidence intervals on aggregate scores
- [ ] Auto-retry agent with low-scoring feedback
- [ ] Slack notifications for feedback requests
- [ ] Real-time dashboard (Google Data Studio)

**Phase 3**:
- [ ] AI-powered feedback analysis (summarize comments with LLM)
- [ ] Automatic agent improvement suggestions
- [ ] Integration with Linear (create issues from feedback)
- [ ] Feedback loop back to agent prompts

---

**Version**: 1.0
**Created**: 2025-02-02
**Author**: AI Agent Engineer at Beam AI

---

*This skill automates everything you manually did for TA Interview Agent feedback - but works for ANY agent!*
