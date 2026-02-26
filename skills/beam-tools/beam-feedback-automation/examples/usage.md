# Beam Feedback Automation - Usage Examples

## Quick Start

### Example 1: TA Interview Agent Feedback (Full Workflow)

```bash
# Set your Beam API key
export BEAM_API_KEY="your_beam_api_key_here"

# Run full workflow for TA Interview Agent
cd 03-skills/beam-feedback-automation
python automate.py agent_ta_interview_123 --tasks 50
```

**What happens:**
1. ✅ Fetches agent graph from Beam API
2. ✅ Analyzes 5 output fields (overall_score, technical_skills, soft_skills, strengths, weaknesses)
3. ✅ Generates 15 feedback fields automatically
4. ✅ Creates customized Google Apps Script
5. ✅ Provides deployment instructions

**Output:**
```
🚀 Starting Full Feedback Automation Workflow

============================================================
Step 1/6: Analyzing Agent
============================================================
🔍 Fetching agent: agent_ta_interview_123

✅ Agent Analysis Complete

📋 Agent: TA Interview Agent
   ID: agent_ta_interview_123
   Description: Screen technical candidates via structured interviews

📥 Inputs: 3 fields
   - candidate_email (string, required)
   - job_title (string, required)
   - resume_url (string, required)

📤 Outputs: 5 fields
   - overall_score (number)
   - technical_skills (array)
   - soft_skills (array)
   - strengths (string)
   - weaknesses (string)

🔗 Nodes: 8 nodes in graph
   - Resume Parser (Level 0)
   - Technical Evaluator (Level 1)
   - Soft Skills Analyzer (Level 2)
   - Overall Scorer (Level 3)
   - Report Generator (Level 4)

💡 Ready to generate feedback fields!

💾 Schema saved to: analysis/agent_ta_interview_123_schema.json

============================================================
Step 2/6: Generating Feedback Fields
============================================================

🎯 Generating feedback fields for 5 outputs...

   Analyzing: overall_score (number)
      ✓ Generated 2 fields (accuracy + comments)

   Analyzing: technical_skills (array)
      ✓ Generated 3 fields (extraction accuracy + missing + incorrect)

   Analyzing: soft_skills (array)
      ✓ Generated 3 fields (extraction accuracy + missing + incorrect)

   Analyzing: strengths (string)
      ✓ Generated 3 fields (quality + accuracy + comments)

   Analyzing: weaknesses (string)
      ✓ Generated 3 fields (quality + accuracy + comments)

   Adding overall feedback fields...
      ✓ Generated 3 overall fields

✅ Feedback Field Generation Complete

📊 Generated 17 feedback fields:

   ✓ Overall Score Accuracy
      Type: rating
      Description: How accurate is the overall_score? (1=Very Inaccurate, 5=Very Accurate)

   ✓ Overall Score Comments
      Type: text
      Description: Additional feedback on overall_score

   ✓ Technical Skills Extraction Accuracy
      Type: rating
      Description: How accurate is the extraction of technical_skills? (1=Very Inaccurate, 5=Very Accurate)

   ... and 14 more fields

💡 Ready to create Apps Script template!

💾 Feedback fields saved to: analysis/agent_ta_interview_123_feedback_fields.json

============================================================
Step 3/6: Generating Apps Script
============================================================
🔨 Generating Apps Script for: TA Interview Agent
   Fields: 17

✅ Apps Script generated successfully!
💾 Saved to: scripts/agent_ta_interview_123_apps_script.js

💡 Next step: Deploy this script to Google Sheets

============================================================
✅ Workflow Complete!
============================================================

📁 Files generated:
   - Schema: analysis/agent_ta_interview_123_schema.json
   - Fields: analysis/agent_ta_interview_123_feedback_fields.json
   - Script: scripts/agent_ta_interview_123_apps_script.js

💡 Next steps:
   1. Deploy the Apps Script to Google Sheets (see instructions below)
   2. Run 'Pre-fill Agent Data' from the Google Sheets menu
   3. Send feedback emails to reviewers
   4. Aggregate results when reviews are complete
```

---

## Step-by-Step Workflow

### Step 1: Analyze Agent

```bash
# By agent ID
python automate.py analyze --agent-id agent_xyz789

# By URL
python automate.py analyze --url https://beam.ai/agent/xyz789

# By name (fuzzy search)
python automate.py analyze --name "TA Interview"
```

### Step 2: Generate Feedback Fields

```bash
python automate.py generate-fields --agent-id agent_xyz789
```

### Step 3: Deploy to Google Sheets

```bash
python automate.py deploy --agent-id agent_xyz789
```

**Manual deployment steps:**
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it: "Feedback - [Agent Name]"
4. Click **Extensions > Apps Script**
5. Delete the default code
6. Copy the entire contents of `scripts/agent_xyz789_apps_script.js`
7. Paste into the Apps Script editor
8. Click **Save** (💾 icon)
9. Click **Run** > Select "onOpen" function
10. Authorize the script (first time only)
11. Refresh the spreadsheet
12. You'll see a new menu: **Feedback Automation**

### Step 4: Pre-fill Feedback Sheets

**Option A: Using Google Sheets Menu (Recommended)**
1. Click **Feedback Automation > Pre-fill Agent Data**
2. Enter number of tasks (e.g., 50)
3. Click OK
4. Wait for pre-fill to complete

**Option B: Using Python Script**
```bash
python scripts/create_feedback_sheets.py \
  --agent-id agent_xyz789 \
  --sheet-id 1abc123_your_sheet_id \
  --tasks 50
```

### Step 5: Send Feedback Requests

**Option A: Using Google Sheets Menu**
1. Click **Feedback Automation > Send Feedback Emails**
2. Enter reviewer email
3. Click OK

**Option B: Using Python Script**
```bash
python scripts/send_emails.py \
  --sheet-id 1abc123_your_sheet_id \
  --reviewer reviewer@example.com
```

### Step 6: Aggregate Results

**Using Google Sheets Menu:**
1. Click **Feedback Automation > Aggregate Results**
2. View summary in popup
3. Check detailed results in Apps Script logs (View > Logs)

---

## Advanced Examples

### Example 2: Email Classifier Agent

```bash
# Analyze custom agent
python automate.py agent_email_classifier_456 --tasks 100

# Generated fields for email outputs:
# - category (string) → Quality, Accuracy, Comments
# - priority (string) → Correctness, Comments
# - sentiment (string) → Correctness, Comments
# - suggested_response (string) → Quality, Accuracy, Comments
```

### Example 3: Resume Screener Agent

```bash
python automate.py agent_resume_screener_789 --tasks 25

# Generated fields:
# - qualification_score (number) → Accuracy, Comments
# - matched_skills (array) → Extraction Accuracy, Missing, Incorrect
# - experience_summary (string) → Quality, Accuracy, Comments
# - hire_recommendation (boolean) → Correct?, Comments
```

### Example 4: Custom Batch Processing

```bash
# Process specific task IDs
python scripts/create_feedback_sheets.py \
  --agent-id agent_xyz789 \
  --sheet-id 1abc123 \
  --task-ids task_001,task_002,task_003,task_004,task_005
```

---

## Tips & Best Practices

### 1. Pre-fill in Batches
- Start with 10-20 tasks for initial testing
- Scale up to 50-100 after validation
- Use `--tasks` parameter to control batch size

### 2. Review Field Customization
- Generated fields are saved to `analysis/{agent_id}_feedback_fields.json`
- Edit this file to customize before deploying
- Re-run `deploy` command after edits

### 3. Email Distribution Strategy
- Send to one reviewer first for pilot testing
- Use Gmail filters to track feedback responses
- Consider using Google Forms for external reviewers

### 4. Results Analysis
- Run aggregation weekly to track trends
- Export results to Notion/Airtable for tracking
- Create Linear issues for low-scoring fields

### 5. Agent Improvement Loop
1. Aggregate feedback results
2. Identify lowest-scoring output fields
3. Improve agent prompts/logic
4. Re-test with new feedback round
5. Compare metrics over time

---

## Troubleshooting

### Error: "BEAM_API_KEY not set"
```bash
export BEAM_API_KEY="your_api_key_here"
```

### Error: "Agent not found"
```bash
# Verify agent ID
curl -H "Authorization: Bearer $BEAM_API_KEY" \
  https://api.beam.ai/v1/agent/your_agent_id
```

### Error: "No outputs found in schema"
```bash
# Check agent has completed tasks
# Outputs are inferred from task results
# Run at least 1 task before generating feedback
```

### Error: "Google Sheets authorization failed"
```bash
# Re-authenticate
gcloud auth application-default login
```

---

## Integration with Other Tools

### Export to Notion
```bash
# After aggregation, push results to Notion
python scripts/export_to_notion.py \
  --results reports/agent_xyz_feedback_report.json \
  --database "Feedback Tracking"
```

### Create Linear Issues
```bash
# Create issues for low-scoring fields
python scripts/create_linear_issues.py \
  --results reports/agent_xyz_feedback_report.json \
  --threshold 3.0
```

### Slack Notifications
```bash
# Send summary to Slack
python scripts/notify_slack.py \
  --results reports/agent_xyz_feedback_report.json \
  --channel "#agent-feedback"
```

---

## FAQ

**Q: Can I customize the generated feedback fields?**
A: Yes! Edit `analysis/{agent_id}_feedback_fields.json` before deploying.

**Q: How do I use this for multiple agents?**
A: Run the full workflow for each agent. Each gets its own schema, fields, and Apps Script.

**Q: Can I use a different email provider?**
A: Yes. Configure SMTP settings in `config.yaml` or use Gmail API.

**Q: What if my agent has 20+ output fields?**
A: The generator handles any number of fields. Feedback sheets may be wide - consider grouping related fields.

**Q: Can reviewers edit the agent output data?**
A: No. Output columns are pre-filled from Beam API. Only feedback columns are editable.

**Q: How do I track completion rate?**
A: Use the "Aggregate Results" function - it shows completion percentage.

---

For more details, see [SKILL.md](../SKILL.md)
