#!/usr/bin/env python3
"""
Retry Task(s)

POST /agent-tasks/retry - Retry failed/stopped tasks.

Usage:
    python retry_task.py --task-id TASK_ID
    python retry_task.py --agent-id AGENT --statuses FAILED,STOPPED
    python retry_task.py --agent-id AGENT --statuses FAILED --days 3 --dry-run
    python retry_task.py --file failed_tasks.json
"""

import sys
import json
import time
import argparse
from datetime import datetime, timedelta, timezone
from beam_client import get_client


DEFAULT_STATUSES = ["FAILED", "ERROR", "STOPPED", "TIMEOUT"]


def retry_single(client, task_id):
    """Retry one task, returns dict with success/error."""
    try:
        result = client.post('/agent-tasks/retry', data={"taskId": task_id})
        return {"success": True, "task_id": task_id, "result": result}
    except Exception as e:
        return {"success": False, "task_id": task_id, "error": str(e)}


def fetch_issue_tasks(client, agent_id, statuses, days=1, limit=100):
    """Get tasks matching given statuses from an agent within a time window."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    all_tasks = []
    page = 1

    while len(all_tasks) < limit:
        params = {
            "agentId": agent_id,
            "statuses": ",".join(statuses),
            "startDate": start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "endDate": end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "pageNum": page,
            "pageSize": min(50, limit - len(all_tasks)),
            "ordering": "createdAt:desc",
        }
        result = client.get('/agent-tasks', params=params)
        tasks = result if isinstance(result, list) else result.get('data', result.get('tasks', []))

        if not tasks:
            break

        for t in tasks:
            if t.get('status') in statuses:
                all_tasks.append(t)

        if len(tasks) < params['pageSize']:
            break
        page += 1

    return all_tasks[:limit]


def load_tasks_from_file(filepath):
    """Load task IDs from JSON file (array of IDs or objects with id/task_id)."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    tasks = []
    for item in data:
        if isinstance(item, str):
            tasks.append({"id": item})
        elif isinstance(item, dict):
            tid = item.get("task_id") or item.get("id")
            if tid:
                tasks.append({"id": tid, "customId": item.get("custom_id") or item.get("customId")})
    return tasks


def main():
    parser = argparse.ArgumentParser(description='Retry failed Beam task(s)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--task-id', help='Single task ID to retry')
    group.add_argument('--agent-id', help='Agent ID — retry all matching tasks')
    group.add_argument('--file', help='JSON file with task IDs')

    parser.add_argument('--statuses', default=','.join(DEFAULT_STATUSES),
                        help=f'Comma-separated statuses (default: {",".join(DEFAULT_STATUSES)})')
    parser.add_argument('--days', type=int, default=1, help='Lookback days (default: 1)')
    parser.add_argument('--limit', type=int, default=100, help='Max tasks (default: 100)')
    parser.add_argument('--delay', type=float, default=0.3, help='Delay between retries (seconds)')
    parser.add_argument('--dry-run', action='store_true', help='Show tasks without retrying')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        statuses = [s.strip() for s in args.statuses.split(',')]

        if args.task_id:
            if args.dry_run:
                print(json.dumps({"dry_run": True, "task_id": args.task_id}) if args.json
                      else f"DRY RUN: Would retry task {args.task_id}")
                return

            result = retry_single(client, args.task_id)
            if args.json:
                print(json.dumps(result, indent=2))
            elif result['success']:
                print(f"Task {args.task_id} retry initiated!")
            else:
                print(f"Error: {result['error']}", file=sys.stderr)
                sys.exit(1)
            return

        if args.agent_id:
            tasks = fetch_issue_tasks(client, args.agent_id, statuses,
                                       days=args.days, limit=args.limit)
        elif args.file:
            tasks = load_tasks_from_file(args.file)
        else:
            tasks = []

        if not tasks:
            msg = "No matching tasks found"
            print(json.dumps({"message": msg}) if args.json else msg)
            return

        if args.dry_run:
            if args.json:
                print(json.dumps({"dry_run": True, "count": len(tasks),
                                   "tasks": [{"id": t.get("id"), "status": t.get("status"),
                                              "customId": t.get("customId")} for t in tasks]}, indent=2))
            else:
                print(f"DRY RUN — would retry {len(tasks)} tasks:\n")
                for i, t in enumerate(tasks, 1):
                    cid = t.get('customId', '-')
                    st = t.get('status', '-')
                    print(f"  [{i:3d}] {t.get('id', '?')[:12]}... ({cid}) [{st}]")
            return

        succeeded, failed = 0, 0
        results = []

        for i, t in enumerate(tasks, 1):
            tid = t.get('id') or t.get('task_id')
            cid = t.get('customId', '-')
            r = retry_single(client, tid)
            results.append(r)

            if r['success']:
                succeeded += 1
                if not args.json:
                    print(f"[{i:3d}/{len(tasks)}] OK  {cid} ({tid[:12]}...)")
            else:
                failed += 1
                if not args.json:
                    print(f"[{i:3d}/{len(tasks)}] FAIL {cid} — {r.get('error', '')[:50]}")

            if i < len(tasks):
                time.sleep(args.delay)

        if args.json:
            print(json.dumps({"total": len(tasks), "succeeded": succeeded,
                               "failed": failed, "results": results}, indent=2, default=str))
        else:
            print(f"\nDone: {succeeded} retried, {failed} failed (of {len(tasks)} total)")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
