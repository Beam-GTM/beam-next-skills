---
name: langfuse-scores
type: skill
version: '1.0'
description: Manage Langfuse scores and score configs. Load when user says 'list scores',
  'create score', 'delete score', 'score configs', 'evaluation scores', 'add score'.
category: integrations
tags:
- langfuse
- scores
- evaluation
platform: Langfuse
updated: '2026-03-23'
visibility: public
---
# Langfuse Scores

Unified skill for scores (v2 reads, v1 writes) and score configurations.

## Usage

```bash
uv run python scripts/scores.py --resource <resource> --action <action> [options]
```

### Scores

```bash
uv run python scripts/scores.py --resource scores --action list --limit 50
uv run python scripts/scores.py --resource scores --action get --id "score-uuid"
uv run python scripts/scores.py --resource scores --action create --trace "trace-id" --name tool_efficiency --value 0.85
uv run python scripts/scores.py --resource scores --action create --trace "trace-id" --name goal_achievement --string-value complete --config-id "uuid"
uv run python scripts/scores.py --resource scores --action delete --id "score-uuid"
uv run python scripts/scores.py --resource scores --action list-configs
```

### Score Configs

```bash
uv run python scripts/scores.py --resource configs --action list
uv run python scripts/scores.py --resource configs --action get --id "config-uuid"
uv run python scripts/scores.py --resource configs --action create --name "my-metric" --data-type NUMERIC --min 0 --max 1
uv run python scripts/scores.py --resource configs --action create --name "quality" --data-type CATEGORICAL --categories "bad,ok,good"
uv run python scripts/scores.py --resource configs --action update --id "config-uuid" --archive
```

## API Endpoints

| Resource | Action | Method | Endpoint |
|----------|--------|--------|----------|
| scores | list | GET | `/api/public/v2/scores` (fallback: `/scores`) |
| scores | get | GET | `/api/public/v2/scores/{id}` |
| scores | create | POST | `/api/public/scores` (v1) |
| scores | delete | DELETE | `/api/public/scores/{id}` (v1) |
| configs | list | GET | `/api/public/score-configs` |
| configs | get | GET | `/api/public/score-configs/{id}` |
| configs | create | POST | `/api/public/score-configs` |
| configs | update | PATCH | `/api/public/score-configs/{id}` |
