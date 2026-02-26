# Beam Feedback Automation

**Universal feedback collection automation for ANY Beam agent.**

Automate the complete feedback workflow you manually created for TA Interview Agent - but make it work for **any agent** by dynamically analyzing the agent structure via API.

---

## Quick Start

```bash
# 1. Set your Beam API key
export BEAM_API_KEY="your_beam_api_key_here"

# 2. Run full workflow
cd 03-skills/beam-feedback-automation
python automate.py agent_your_agent_id --tasks 50

# 3. Follow the deployment instructions
# 4. Done! 🎉
```

---

## What It Does

Takes this **manual process**:
1. ❌ Manually create Google Sheet with columns for agent outputs
2. ❌ Manually design feedback fields
3. ❌ Manually write Apps Script code
4. ❌ Manually fetch task data from Beam
5. ❌ Manually copy-paste data into sheet
6. ❌ Manually send feedback requests
7. ❌ Manually calculate aggregate scores

And turns it into this **automated workflow**:
1. ✅ `python automate.py agent_xyz --tasks 50`
2. ✅ Deploy generated script to Google Sheets (1-click)
3. ✅ Run "Pre-fill Agent Data" menu item
4. ✅ Run "Send Feedback Emails" menu item
5. ✅ Run "Aggregate Results" when complete
6. ✅ Done!

---

## Features

- **🔍 Smart Agent Analysis** - Fetches agent graph from Beam API, understands structure
- **🎯 Dynamic Field Generation** - Auto-generates appropriate feedback fields based on output types
- **📝 Apps Script Creation** - Creates customized Google Apps Script for each agent
- **📊 Google Sheets Integration** - Pre-fills sheets with task data
- **📧 Email Automation** - Sends feedback requests to reviewers
- **📈 Results Aggregation** - Calculates scores, identifies patterns, suggests improvements

---

## Architecture

```
User Input → Beam API → Agent Analysis → Field Generation → Apps Script
                ↓
           Task Data → Google Sheets → Email Requests → Feedback Collection → Aggregation
```

### Components

1. **analyze_agent.py** - Fetches agent from Beam API, extracts schema
2. **generate_feedback_fields.py** - Smart logic to create feedback fields
3. **generate_apps_script.py** - Creates customized Apps Script
4. **automate.py** - Main orchestrator (ties everything together)

---

## File Structure

```
beam-feedback-automation/
├── README.md                       # This file
├── SKILL.md                        # Complete documentation
├── automate.py                     # Main entry point
├── config.yaml                     # Configuration
├── scripts/
│   ├── analyze_agent.py           # Beam API integration
│   ├── generate_feedback_fields.py # Smart field generator
│   └── generate_apps_script.py    # Apps Script generator
├── analysis/                       # Generated schemas & fields
│   ├── {agent_id}_schema.json
│   └── {agent_id}_feedback_fields.json
├── templates/
│   └── email_template.html        # Email template
└── examples/
    └── usage.md                    # Detailed usage examples
```

---

## Requirements

- Python 3.7+
- Beam API key
- Google account (for Sheets)

**Python packages:**
```bash
pip install requests
```

---

## Usage

### Full Workflow (Recommended)
```bash
python automate.py agent_xyz789 --tasks 50
```

### Step-by-Step
```bash
# Analyze agent
python automate.py analyze --agent-id agent_xyz789

# Generate feedback fields
python automate.py generate-fields --agent-id agent_xyz789

# Generate Apps Script
python automate.py deploy --agent-id agent_xyz789

# See examples
python automate.py examples
```

---

## Examples

### TA Interview Agent
```bash
python automate.py agent_ta_interview --tasks 50

# Analyzes 5 outputs:
# - overall_score (number) → Accuracy, Comments
# - technical_skills (array) → Extraction Accuracy, Missing, Incorrect
# - soft_skills (array) → Extraction Accuracy, Missing, Incorrect
# - strengths (text) → Quality, Accuracy, Comments
# - weaknesses (text) → Quality, Accuracy, Comments

# Generates 15+ feedback fields automatically!
```

### Email Classifier Agent
```bash
python automate.py agent_email_classifier --tasks 100

# Analyzes outputs:
# - category (string) → Quality, Accuracy, Comments
# - priority (string) → Correctness, Comments
# - sentiment (string) → Correctness, Comments
# - suggested_response (string) → Quality, Accuracy, Comments
```

---

## Smart Field Generation Logic

The system automatically generates appropriate feedback fields based on output types:

| Output Type | Generated Fields |
|-------------|------------------|
| `number` (score) | Accuracy (rating 1-5), Comments |
| `array` (list) | Extraction Accuracy (rating), Missing Items, Incorrect Items |
| `string` (text) | Quality (rating), Accuracy (Yes/No/Partial), Comments |
| `boolean` | Correct? (Yes/No), Comments |
| `object` | Overall Accuracy (rating), Comments |

---

## Deployment Instructions

After running the automation:

1. **Create Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create new spreadsheet

2. **Deploy Apps Script**
   - Click **Extensions > Apps Script**
   - Copy script from `scripts/{agent_id}_apps_script.js`
   - Paste into editor
   - Save and authorize

3. **Use the Menu**
   - **Pre-fill Agent Data** - Fetches tasks from Beam
   - **Send Feedback Emails** - Emails reviewers
   - **Aggregate Results** - Shows summary stats
   - **Highlight Incomplete** - Visual indicators

---

## Configuration

Edit `config.yaml` to customize:

```yaml
beam:
  api_key_env: BEAM_API_KEY

feedback:
  rating_scale: 5
  include_comments: true

automation:
  batch_size: 50
  auto_send_emails: false
```

---

## Troubleshooting

**Error: "BEAM_API_KEY not set"**
```bash
export BEAM_API_KEY="your_key"
```

**Error: "Agent not found"**
- Verify agent ID is correct
- Check API key has access to agent

**Error: "No outputs found"**
- Ensure agent has completed at least 1 task
- Outputs are inferred from task results

---

## Next Steps

1. ✅ Run the full workflow for your agent
2. ✅ Deploy the Apps Script to Google Sheets
3. ✅ Pre-fill with task data
4. ✅ Send feedback requests
5. ✅ Aggregate results
6. ✅ Use insights to improve your agent
7. ✅ Repeat for continuous improvement

---

## Documentation

- **Full Documentation**: [SKILL.md](SKILL.md)
- **Usage Examples**: [examples/usage.md](examples/usage.md)
- **Configuration**: [config.yaml](config.yaml)

---

## Support

For issues or questions:
1. Check [SKILL.md](SKILL.md) for detailed documentation
2. Review [examples/usage.md](examples/usage.md) for common patterns
3. Check troubleshooting section above

---

**Version**: 1.0
**Created**: 2025-02-02
**Author**: AI Agent Engineer at Beam AI

*This skill automates everything you manually did for TA Interview Agent feedback - but works for ANY agent!*
