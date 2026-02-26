#!/usr/bin/env python3
"""
Beam.ai Retry Tasks

Retry failed or stopped tasks in Beam.ai using the retry API.

Usage:
    # Retry a single task
    python retry_tasks.py --task-id <task_id>

    # Retry all FAILED tasks from an agent (last 1 day)
    python retry_tasks.py --agent <agent_id>

    # Retry tasks from a JSON file (output from debug_issue_tasks.py)
    python retry_tasks.py --file failed_tasks.json

    # Retry with specific statuses
    python retry_tasks.py --agent <agent_id> --status FAILED --status STOPPED

    # Dry run (show what would be retried)
    python retry_tasks.py --agent <agent_id> --dry-run
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add parent directories to path for shared module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from _shared.beam_api import BeamClient
except ImportError as e:
    print(f"Error: Could not import shared modules: {e}")
    print("Ensure 03-skills/_shared/beam_api.py exists")
    sys.exit(1)


# Default statuses to retry
DEFAULT_RETRY_STATUSES = ["FAILED", "ERROR", "STOPPED", "TIMEOUT"]


def retry_task(client: BeamClient, task_id: str, max_retries: int = 3) -> dict:
    """
    Retry a single task with automatic retries on transient errors.

    Args:
        client: BeamClient instance
        task_id: Task ID to retry
        max_retries: Maximum retry attempts for API errors

    Returns:
        dict with 'success' bool, 'status_code', and optional 'error'
    """
    for attempt in range(max_retries):
        try:
            # POST /agent-tasks/retry with taskId in body
            # Note: BeamClient.request() calls response.json() which fails on empty body
            # So we need to handle the 201 response with empty body specially
            import requests

            url = f"{client.base_url}/agent-tasks/retry"
            headers = client._get_headers()
            response = requests.post(url, json={"taskId": task_id}, headers=headers)

            if response.status_code in [200, 201]:
                return {"success": True, "status_code": response.status_code}
            elif response.status_code in [502, 503, 504]:
                # Transient error, retry
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue

            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text[:200]
            }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "Max retries exceeded"}


def get_issue_tasks(
    client: BeamClient,
    agent_id: str,
    statuses: list,
    days: int = 1,
    limit: int = 100
) -> list:
    """
    Get tasks with specified statuses from an agent.

    Args:
        client: BeamClient instance
        agent_id: Agent ID to query
        statuses: List of statuses to include
        days: Look back period in days
        limit: Max tasks to return

    Returns:
        List of task dicts with id, customId, status, etc.
    """
    # Calculate time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    # Beam API uses ISO format with Z suffix
    from_ts = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    to_ts = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    all_tasks = []
    page = 1

    while len(all_tasks) < limit:
        params = {
            "agentId": agent_id,
            "from": from_ts,
            "to": to_ts,
            "page": page,
            "limit": min(50, limit - len(all_tasks))
        }

        try:
            result = client.get("/agent-tasks", params=params)
            tasks = result.get("data", [])

            if not tasks:
                break

            # Filter by status
            for task in tasks:
                if task.get("status") in statuses:
                    all_tasks.append(task)
                    if len(all_tasks) >= limit:
                        break

            page += 1

            # Break if we got fewer than requested (no more pages)
            if len(tasks) < params["limit"]:
                break

        except Exception as e:
            print(f"Error fetching tasks: {e}")
            break

    return all_tasks


def load_tasks_from_file(filepath: str) -> list:
    """
    Load task IDs from a JSON file.

    Supports formats:
    - Array of task objects with 'task_id' or 'id' field
    - Array of task ID strings

    Args:
        filepath: Path to JSON file

    Returns:
        List of task dicts with 'task_id' and optional 'custom_id'
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    tasks = []
    for item in data:
        if isinstance(item, str):
            tasks.append({"task_id": item})
        elif isinstance(item, dict):
            task_id = item.get("task_id") or item.get("id")
            if task_id:
                tasks.append({
                    "task_id": task_id,
                    "custom_id": item.get("custom_id") or item.get("customId")
                })

    return tasks


def main():
    parser = argparse.ArgumentParser(
        description="Retry failed Beam.ai tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Retry a single task
    python retry_tasks.py --task-id abc123

    # Retry all FAILED tasks from agent
    python retry_tasks.py --agent abc123-def456

    # Retry from JSON file
    python retry_tasks.py --file /tmp/failed_tasks.json

    # Dry run
    python retry_tasks.py --agent abc123 --dry-run

Environment Variables (in .env at project root):
    BEAM_API_KEY        Your Beam.ai API key (BID instance)
    BEAM_WORKSPACE_ID   Your Beam.ai workspace ID
    BEAM_API_KEY_PROD   Production API key
    BEAM_WORKSPACE_ID_PROD  Production workspace ID
"""
    )

    # Input sources (mutually exclusive)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--task-id", "-t",
        help="Single task ID to retry"
    )
    source.add_argument(
        "--agent", "-a",
        help="Agent ID - retry all issue tasks from this agent"
    )
    source.add_argument(
        "--file", "-f",
        help="JSON file with task IDs to retry"
    )

    # Filters
    parser.add_argument(
        "--status", "-s",
        action="append",
        default=[],
        help="Task statuses to retry (can specify multiple). Default: FAILED, ERROR, STOPPED, TIMEOUT"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=1,
        choices=[1, 3, 7, 14, 30],
        help="Look back period in days (default: 1)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="Max tasks to retry (default: 100)"
    )

    # Options
    parser.add_argument(
        "--workspace", "-w",
        default="bid",
        choices=["bid", "prod"],
        help="Beam workspace (default: bid)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be retried without actually retrying"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between retries in seconds (default: 0.2)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save results to JSON file"
    )

    args = parser.parse_args()

    # Use default statuses if none specified
    statuses = args.status if args.status else DEFAULT_RETRY_STATUSES

    # Initialize client
    client = BeamClient(workspace=args.workspace)
    print(f"Workspace: {args.workspace}")
    print(f"API Base: {client.base_url}")
    print()

    # Get tasks to retry
    tasks = []

    if args.task_id:
        tasks = [{"task_id": args.task_id}]
        print(f"Retrying single task: {args.task_id}")

    elif args.agent:
        print(f"Fetching {', '.join(statuses)} tasks from agent {args.agent}...")
        print(f"Look back: {args.days} day(s)")
        print()

        agent_tasks = get_issue_tasks(
            client,
            args.agent,
            statuses,
            days=args.days,
            limit=args.limit
        )

        for t in agent_tasks:
            tasks.append({
                "task_id": t.get("id"),
                "custom_id": t.get("customId"),
                "status": t.get("status")
            })

        print(f"Found {len(tasks)} tasks to retry")

    elif args.file:
        tasks = load_tasks_from_file(args.file)
        print(f"Loaded {len(tasks)} tasks from {args.file}")

    if not tasks:
        print("No tasks to retry")
        return

    print()
    print("=" * 60)

    # Dry run mode
    if args.dry_run:
        print("DRY RUN - Would retry these tasks:")
        print()
        for i, task in enumerate(tasks, 1):
            custom_id = task.get("custom_id") or "-"
            status = task.get("status") or "-"
            print(f"  [{i:3d}] {task['task_id'][:8]}... ({custom_id}) [{status}]")
        print()
        print(f"Total: {len(tasks)} tasks")
        return

    # Execute retries
    print(f"Retrying {len(tasks)} tasks...")
    print(f"Started: {datetime.now().isoformat()}")
    print()

    results = {
        "success": [],
        "failed": [],
        "started_at": datetime.now().isoformat(),
        "workspace": args.workspace
    }

    for i, task in enumerate(tasks, 1):
        task_id = task["task_id"]
        custom_id = task.get("custom_id") or "-"

        result = retry_task(client, task_id)

        if result["success"]:
            results["success"].append({
                "task_id": task_id,
                "custom_id": custom_id,
                "status_code": result.get("status_code")
            })
            print(f"[{i:3d}/{len(tasks)}] OK {custom_id} ({task_id[:8]}...)")
        else:
            results["failed"].append({
                "task_id": task_id,
                "custom_id": custom_id,
                "error": result.get("error") or f"HTTP {result.get('status_code')}"
            })
            error_msg = result.get("error", "")[:50]
            print(f"[{i:3d}/{len(tasks)}] FAIL {custom_id} ({task_id[:8]}...) - {error_msg}")

        # Delay between requests
        if i < len(tasks):
            time.sleep(args.delay)

    results["completed_at"] = datetime.now().isoformat()

    print()
    print("=" * 60)
    print()
    print("=== SUMMARY ===")
    print(f"Total tasks: {len(tasks)}")
    print(f"Successfully retried: {len(results['success'])}")
    print(f"Failed to retry: {len(results['failed'])}")

    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    # Show failed tasks
    if results["failed"]:
        print()
        print("=== FAILED RETRIES ===")
        for item in results["failed"][:10]:  # Show first 10
            print(f"  {item.get('custom_id', item['task_id'][:8])}: {item['error'][:60]}")
        if len(results["failed"]) > 10:
            print(f"  ... and {len(results['failed']) - 10} more")


if __name__ == "__main__":
    main()
