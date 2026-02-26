---
name: beam-get-agent-analytics
version: 1.0
description: Get analytics for a Beam.ai agent including task counts, completion rates,
  evaluation scores, and performance trends. Load when user says "agent analytics",
  "beam analytics", "agent performance", "task stats for agent", "how is agent performing",
  or needs agent metrics.
author: Hassaan Ahmed
category: integrations
tags:
- analytics
- beam-ai
platform: Beam AI
updated: '2026-01-02'
visibility: team
---
# Beam Get Agent Analytics

**Retrieve analytics and performance metrics for a Beam.ai agent.**

## When to Use

- Check agent performance over a time period
- View task completion rates and failure rates
- Analyze evaluation scores and trends
- Compare current period with previous period (deltas)
- Generate performance reports

---

## Prerequisites

`.env` file at project root:

```
# Beam.ai - BID instance (default)
BEAM_API_KEY=your_bid_api_key
BEAM_WORKSPACE_ID=your_bid_workspace_id

# Beam.ai - Production instance
BEAM_API_KEY_PROD=your_prod_api_key
BEAM_WORKSPACE_ID_PROD=your_prod_workspace_id
```

**Dependencies**: `pip install requests python-dotenv`

---

## Quick Start

```bash
# Get analytics for last 7 days
python 03-skills/beam-get-agent-analytics/scripts/get_agent_analytics.py <agent_id>

# Get analytics for specific date range
python 03-skills/beam-get-agent-analytics/scripts/get_agent_analytics.py <agent_id> \
  --start 2024-01-01 --end 2024-01-31

# Get analytics for last 30 days
python 03-skills/beam-get-agent-analytics/scripts/get_agent_analytics.py <agent_id> --days 30

# Use production workspace
python 03-skills/beam-get-agent-analytics/scripts/get_agent_analytics.py <agent_id> --workspace prod

# Output as JSON
python 03-skills/beam-get-agent-analytics/scripts/get_agent_analytics.py <agent_id> --json
```

---

## Workspaces

| Workspace | API Endpoint | Default |
|-----------|--------------|---------|
| `bid` | api.bid.beamstudio.ai | Yes |
| `prod` | api.beamstudio.ai | No |

---

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `agent_id` | Agent ID (required) | - |
| `--start`, `-s` | Start date (YYYY-MM-DD) | 7 days ago |
| `--end`, `-e` | End date (YYYY-MM-DD) | today |
| `--days`, `-d` | Look back N days (1,7,14,30,90) | 7 |
| `--workspace`, `-w` | Workspace: bid or prod | bid |
| `--json` | Output as JSON | false |
| `--output`, `-o` | Save to file | - |

---

## Response Fields

### Current Period Metrics

| Field | Description |
|-------|-------------|
| `totalTasks` | Total tasks in period |
| `completedTasks` | Successfully completed tasks |
| `failedTasks` | Failed tasks |
| `averageEvaluationScore` | Average eval score (0-100) |
| `averageRuntimeSeconds` | Avg task runtime |
| `totalRuntimeSeconds` | Total runtime |
| `positiveFeedbackCount` | Tasks with positive feedback |
| `negativeFeedbackCount` | Tasks with negative feedback |
| `consentRequiredCount` | Tasks requiring user consent |

### Period Deltas (vs previous period)

| Field | Description |
|-------|-------------|
| `totalTasksDelta` | Change in total tasks |
| `completedTasksDelta` | Change in completed tasks |
| `failedTasksDelta` | Change in failed tasks |
| `averageEvaluationScoreDelta` | Change in eval score |
| `averageRuntimeSecondsDelta` | Change in runtime |

### Daily Chart Data

Array of daily stats with:
- `date`: Date (YYYY-MM-DD)
- `completedCount`: Completed tasks that day
- `failedCount`: Failed tasks that day
- `averageEvaluationScore`: Avg score that day

---

## Example Output

```
Agent Analytics: My Agent
Period: 2024-01-01 to 2024-01-31
Workspace: prod

=== CURRENT PERIOD ===
Total Tasks:     150
Completed:       135 (90.0%)
Failed:          15 (10.0%)
Avg Eval Score:  87.5
Avg Runtime:     45.7s
Total Runtime:   6,855s (1.9 hrs)

Feedback:
  Positive: 120
  Negative: 10
  Consent Required: 25

=== VS PREVIOUS PERIOD ===
Total Tasks:     +15.5%
Completed:       +12.3%
Failed:          -5.2%
Eval Score:      +4.5%
Runtime:         -8.7%

=== DAILY TREND (last 7 days) ===
Date       | Completed | Failed | Eval Score
-----------+-----------+--------+-----------
2024-01-25 |        42 |      8 |      87.5
2024-01-26 |        38 |      5 |      89.2
2024-01-27 |        45 |      3 |      91.0
...
```

---

## API Details

Uses Beam.ai analytics endpoint:
- **Endpoint**: `GET /agent-tasks/analytics`
- **Required params**: `agentId`, `startDate`, `endDate`
- **Response**: HTTP 200 with JSON body

---

## Error Handling

| Error | Solution |
|-------|----------|
| `BEAM_API_KEY not found` | Add to .env file |
| `401 Unauthorized` | Verify API key is valid |
| `404 Not Found` | Agent ID doesn't exist |
| `400 Bad Request` | Check date format (YYYY-MM-DD) |

---

## Related Skills

- `beam-debug-issue-tasks` - Debug failed tasks
- `beam-retry-tasks` - Retry failed tasks
- `beam-get-task-details` - Get details for a specific task
