---
name: create-beam-task-auto-trigger
version: 1.4
description: Create an auto-trigger webhook script for a Beam.ai agent task. Supports
  simple query-based, query with attachments/data (base64-encoded), and email-triggered
  (Gmail/Workable) agents. Load when user says "create auto trigger", "create task
  auto trigger", "convert task to webhook", "create beam webhook", "automate beam
  task", or provides a Beam task URL to create a webhook trigger script.
author: Safi Haider
category: general
tags:
- create
- email
updated: '2026-01-06'
visibility: team
---
# Create Beam Task Auto-Trigger

Convert a Beam.ai task into an auto-trigger webhook script for scheduled execution.

## Purpose

This skill automates the process of:
1. Fetching task details from a Beam.ai task URL
2. Extracting the original task payload
3. Detecting payload type (query-based vs email-triggered)
4. Creating a bash webhook script with the correct payload structure
5. Saving it to the webhook-scheduler for automated rotation

**Time saved**: ~15 minutes of manual work per webhook script

## Supported Agent Types

The skill intelligently detects and handles three types of agent triggers:

### 1. Simple Query-Based Agents
Agents triggered by simple text queries with no additional data. The webhook sends:
```json
{
  "query": "summarize the document",
  "timestamp": "2026-01-02T13:00:13Z"
}
```

### 2. Query-Based Agents with Attachments/Data
Agents triggered by queries that require attachments or additional context. The webhook sends:
```json
{
  "query": "analyze the attached resume",
  "additionalInfo": "",
  "beamAgentOSTaskID": "7c516cc3-f8fa-4ffc-af65-5eee0aa2792a",
  "beamTaskId": "CAN-3",
  "beamTaskTimestamp": "2025-12-05T07:55:48Z",
  "attachments": [
    {
      "name": "Marcus_Chen_Resume.pdf",
      "type": "file",
      "key": "53919651-bb7a-44de-9d94-6cf540ff640f_7bba5443-4ef2-432b-b256-7a00ba6da373_Marcus_Chen_Resume.pdf"
    }
  ],
  "timestamp": "2026-01-02T13:00:13Z"
}
```

### 3. Email-Triggered Agents (Gmail/Workable Integration)
Agents triggered by email messages. The webhook sends the full email payload:
```json
{
  "id": "196a54bba916edc4",
  "messageId": "196a54bba916edc4",
  "threadId": "196a54bba916edc4",
  "labelIds": ["UNREAD", "CATEGORY_PERSONAL", "INBOX"],
  "snippet": "email preview text",
  "headers": {
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email Subject"
  },
  "attachments": [...],
  "textPlain": "email body text",
  "textHtml": "<div>email body html</div>",
  "timestamp": "2026-01-02T13:00:13Z"
}
```

The skill automatically detects which type based on the task payload structure.

## When to Use

- Convert an existing Beam task into a recurring webhook
- Create auto-trigger scripts for agent tasks
- Add tasks to the webhook scheduler rotation
- Reproduce task execution with the same payload

## Prerequisites

`.env` file at project root with:
```bash
BEAM_API_KEY=your_beam_api_key
BEAM_WORKSPACE_ID=your_workspace_id
```

**Dependencies**: `requests`, `python-dotenv` (already installed)

## Quick Start

```bash
# Interactive mode (recommended)
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py

# With task URL
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py \
  --task-url "https://app.beam.ai/{workspace}/{agent}/tasks/{task-id}"

# With all parameters
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py \
  --task-url "https://app.beam.ai/..." \
  --webhook-url "https://api.beamstudio.ai/agent-tasks/{agent}/webhook/{webhook-id}" \
  --script-name "my-agent-task.sh"

# With file attachment (base64 encoded)
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py \
  --task-url "https://app.beam.ai/..." \
  --webhook-url "https://api.beamstudio.ai/..." \
  --script-name "resume-screening.sh" \
  --attachment-file "/path/to/resume.pdf"
```

## Workflow

### Step 1: Provide Task URL
The task URL from Beam.ai (from the browser address bar):
```
https://app.beam.ai/505d2090-2b5d-4e45-b0f4-cc3a0b299aa8/8cb86b50-aa8f-4876-a3cb-7eb62e910528/tasks/1c08f856-d1a2-47c4-a62a-01ff7d24b3df
```

### Step 2: Provide Webhook URL
The agent webhook URL (get from Beam agent settings):
```
https://api.beamstudio.ai/agent-tasks/{agent-id}/webhook/{webhook-id}
```

### Step 3: Script Name
Choose a descriptive name for the webhook script:
```
interview-scheduling-agent.sh
data-processing-task.sh
```

### Step 4: Script Generation
The skill will:
- Fetch the task details using the Beam API
- Extract the original task payload
- Create a bash script with:
  - Correct webhook URL
  - Original task payload
  - Dynamic timestamp
- Save to `04-workspace/scripts/webhook-scheduler/webhooks/`

## Output

**Created Script**:
```bash
04-workspace/scripts/webhook-scheduler/webhooks/{script-name}.sh
```

**Script Content**:
```bash
#!/bin/bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TASK_PAYLOAD='{"id":"...","messageId":"...","timestamp":"__TIMESTAMP_PLACEHOLDER__",...}'
TASK_WITH_TIMESTAMP=$(echo "$TASK_PAYLOAD" | sed "s/__TIMESTAMP_PLACEHOLDER__/$TIMESTAMP/g")

curl --location 'https://api.beamstudio.ai/agent-tasks/{agent}/webhook/{webhook-id}' \
--form 'task="'"$TASK_WITH_TIMESTAMP"'"' \
--form 'encodedContextFiles="[{\"mimeType\":\"application/pdf\",\"fileType\":\"document\",\"fileExtension\":\"pdf\",\"data\":\"<base64-encoded-content>\"}]"'
```

## Examples

### Example 1: Interactive Mode
```bash
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py

# Prompts:
# Task URL: https://app.beam.ai/.../tasks/abc123
# Webhook URL: https://api.beamstudio.ai/agent-tasks/.../webhook/xyz789
# Script name: my-task.sh

# Output:
# ✅ Created: 04-workspace/scripts/webhook-scheduler/webhooks/my-task.sh
```

### Example 2: Command Line
```bash
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py \
  --task-url "https://app.beam.ai/505d.../tasks/1c08f856..." \
  --webhook-url "https://api.beamstudio.ai/agent-tasks/8cb86.../webhook/17f4e..." \
  --script-name "interview-scheduling.sh"
```

### Example 3: With File Attachment
```bash
python 03-skills/create-beam-task-auto-trigger/scripts/create_auto_trigger.py \
  --task-url "https://app.beam.ai/505d.../tasks/7c516cc3..." \
  --webhook-url "https://api.beamstudio.ai/agent-tasks/53919651.../webhook/36bf660f..." \
  --script-name "resume-screening.sh" \
  --attachment-file "/Users/yourname/Documents/Marcus_Chen_Resume.pdf"

# Output:
# ✅ Created: 04-workspace/scripts/webhook-scheduler/webhooks/resume-screening.sh
# 📎 Attachment: Marcus_Chen_Resume.pdf (base64 encoded)
```

### Example 4: Test the Created Script
```bash
# Test the webhook immediately
bash 04-workspace/scripts/webhook-scheduler/webhooks/interview-scheduling.sh
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-url` | Yes* | Beam.ai task URL from browser |
| `--webhook-url` | Yes* | Agent webhook URL from Beam settings |
| `--script-name` | Yes* | Name for the webhook script (must end in .sh) |
| `--attachment-file` | No | Path to file to attach (e.g., resume.pdf). Will be base64 encoded and included in payload |
| `--output-dir` | No | Output directory (default: webhook-scheduler/webhooks) |
| `--workspace` | No | Beam workspace: bid or prod (default: bid) |

\* Required in CLI mode, prompted in interactive mode

## How It Works

1. **Parse Task URL** - Extract workspace, agent, and task IDs
2. **Fetch Task Details** - Use Beam API with authentication
3. **Extract Payload** - Get `taskQuery` or `originalTaskQuery` from task
4. **Encode Attachments** (if --attachment-file provided) - Read file and encode to base64
5. **Separate Payload Components** - Split task payload and encoded context files
6. **Generate Script** - Create bash script using --form format with:
   - `task` field: Task payload with dynamic timestamp
   - `encodedContextFiles` field: Array of base64-encoded files
   - Proper JSON escaping for bash (`\"` instead of `"`)
   - Compact JSON format (no spaces after colons)
7. **Save Script** - Write to webhook-scheduler folder
8. **Set Permissions** - Make script executable

**Format Details**:
- Uses `--form` multipart format instead of `--data` JSON
- JSON is escaped for bash: `{\"key\":\"value\"}` becomes `{\\\"key\\\":\\\"value\\\"}`
- Compact JSON with `separators=(',', ':')` - no spaces
- Two separate form fields: `task` and `encodedContextFiles`

## Integration with Webhook Scheduler

The created script is automatically added to the webhook rotation:
- Runs every 47 minutes (Monday-Saturday)
- Rotates through all scripts alphabetically
- Each script runs ~20-21 times per week (with 9 total scripts)

## Error Handling

**Common Issues**:

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid task URL | URL format incorrect | Use full URL from Beam browser |
| Task not found | Task ID doesn't exist | Verify task ID in Beam dashboard |
| Authentication failed | API key invalid | Check `.env` file credentials |
| Webhook URL invalid | Missing agent/webhook ID | Get URL from Beam agent settings |

## Tips

**Finding Webhook URL**:
1. Go to Beam agent settings
2. Navigate to "Webhooks" section
3. Copy the webhook URL

**Script Naming**:
- Use descriptive names: `customer-onboarding.sh`
- Use hyphens, not spaces: `invoice-processing.sh`
- Must end with `.sh`: `my-task.sh`

**Testing**:
- Always test the script after creation
- Check Beam dashboard for task creation
- Verify payload is correct

## Notes

- Created scripts are executable by default
- Scripts use dynamic timestamps (current time when run)
- Payload structure is preserved from original task
- Automatically detects and handles both query-based and email-triggered agents
- For email-triggered agents, preserves full Gmail message payload including headers, attachments, and content
- Scripts can be edited manually after creation
- Compatible with GitHub Actions webhook scheduler

---

**Version**: 1.4
**Created**: 2026-01-02
**Updated**: 2026-01-05
**Status**: Production Ready

## Changelog

### v1.4 (2026-01-05)
- **BREAKING CHANGE**: Switched to `--form` multipart format (matches Beam API requirements)
- **NEW**: Separates `task` and `encodedContextFiles` into two form fields
- **IMPROVED**: Proper JSON escaping for bash (`\"` instead of `"`)
- **IMPROVED**: Compact JSON format with `separators=(',', ':')` (no spaces)
- **IMPROVED**: Only includes `encodedContextFiles` field when attachments exist
- **FIXED**: Scripts now match ground truth format from working webhooks
- All generated scripts use the correct format that Beam API expects

### v1.3 (2026-01-05)
- **NEW**: Added `--attachment-file` parameter to attach files (PDFs, etc.)
- Files are automatically base64-encoded and included in webhook payload
- Supports custom file attachments that override task-extracted files
- Enhanced attachment format with proper mimeType and content fields

### v1.2 (2026-01-05)
- Added support for query-based agents with attachments/data
- Enhanced detection logic to handle three agent types
- Preserves attachment metadata and task IDs for agents that need them
- Fixed candidate-screening-agent to include resume attachments

### v1.1 (2026-01-02)
- Added support for email-triggered agents (Gmail/Workable integration)
- Automatic detection of payload type (query-based vs email-triggered)
- Full email payload preservation for Gmail-triggered agents
- Enhanced documentation with payload type examples

### v1.0 (2026-01-02)
- Initial release
- Support for simple query-based agents
- Beam API authentication
- Webhook script generation
