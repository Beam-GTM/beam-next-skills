#!/usr/bin/env python3
"""
Beam.ai Get Task Details

Retrieve detailed information about specific Beam.ai tasks.

Usage:
    # Get details for a single task
    python get_task_details.py <task_id>

    # Get details for multiple tasks
    python get_task_details.py <task_id1> <task_id2>

    # Output as JSON
    python get_task_details.py <task_id> --json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directories to path for shared module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from _shared.beam_api import BeamClient
except ImportError as e:
    print(f"Error: Could not import shared modules: {e}")
    print("Ensure 03-skills/_shared/beam_api.py exists")
    sys.exit(1)


def get_task_details(client: BeamClient, task_id: str) -> dict:
    """
    Get details for a specific task.

    Args:
        client: BeamClient instance
        task_id: Task ID (UUID)

    Returns:
        Task details dict
    """
    return client.get(f"/agent-tasks/{task_id}")


def calculate_duration(created: str, completed: str) -> str:
    """Calculate duration between two timestamps."""
    if not created or not completed:
        return "N/A"

    try:
        start = datetime.fromisoformat(created.replace("Z", "+00:00"))
        end = datetime.fromisoformat(completed.replace("Z", "+00:00"))
        delta = end - start
        seconds = delta.total_seconds()

        if seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} minutes"
        else:
            return f"{seconds / 3600:.1f} hours"
    except Exception:
        return "N/A"


def get_status_indicator(status: str) -> str:
    """Get a visual indicator for task status."""
    indicators = {
        "COMPLETED": "[OK]",
        "COMPLETE": "[OK]",
        "FAILED": "[FAIL]",
        "ERROR": "[ERR]",
        "IN_PROGRESS": "[...]",
        "RUNNING": "[...]",
        "QUEUED": "[Q]",
        "STOPPED": "[STOP]",
        "TIMEOUT": "[TIME]",
        "USER_INPUT_REQUIRED": "[INPUT]",
        "CANCELLED": "[X]"
    }
    return indicators.get(status.upper(), f"[{status}]")


def print_task_details(task: dict, show_full: bool = False):
    """Print task details in human-readable format."""
    task_id = task.get("id", "unknown")
    custom_id = task.get("customId", "")
    status = task.get("status", "UNKNOWN")
    created = task.get("createdAt", task.get("created_at", ""))
    updated = task.get("updatedAt", task.get("updated_at", ""))
    completed = task.get("completedAt", task.get("completed_at", ""))

    # Header
    print("\nTask Details")
    print("=" * 60)
    print()
    print(f"Task ID:     {task_id}")
    if custom_id:
        print(f"Custom ID:   {custom_id}")
    print(f"Status:      {status} {get_status_indicator(status)}")
    print(f"Created:     {created}")
    if updated:
        print(f"Updated:     {updated}")
    if completed:
        print(f"Completed:   {completed}")
        print(f"Duration:    {calculate_duration(created, completed)}")

    # Agent info
    agent_id = task.get("agentId", task.get("agent_id"))
    if agent_id:
        print(f"Agent ID:    {agent_id}")

    # Error info
    error = task.get("error") or task.get("errorMessage")
    if error:
        print()
        print("=== ERROR ===")
        print(error[:500])

    # Node execution details
    nodes = task.get("agentTaskNodes", [])
    if nodes:
        print()
        print(f"=== NODE DETAILS ({len(nodes)} nodes) ===")

        for i, node in enumerate(nodes, 1):
            node_name = node.get("name", f"Node {i}")
            tool = node.get("tool", {})
            tool_name = tool.get("name", "unknown")
            node_status = node.get("status", "")

            print(f"\n[{i}] {node_name}")
            if tool_name != "unknown":
                print(f"    Tool: {tool_name}")
            if node_status:
                print(f"    Status: {node_status}")

            # Tool data and reasoning
            tool_data = node.get("toolData", {})
            if tool_data and show_full:
                reasoning = tool_data.get("reasoning", {})
                if reasoning:
                    print("    Reasoning:")
                    for param, reason in list(reasoning.items())[:3]:
                        reason_short = reason[:100].replace("\n", " ")
                        print(f"      - {param}: {reason_short}...")

            # User questions (required inputs)
            user_questions = node.get("userQuestions", [])
            if user_questions:
                print("    Required Inputs:")
                for q in user_questions:
                    param = q.get("parameter", "unknown")
                    answer = q.get("answer")
                    status_str = "provided" if answer else "awaiting"
                    print(f"      - {param}: [{status_str}]")

    # Graph state
    graph_state = task.get("graphState", {})
    if graph_state and show_full:
        current = graph_state.get("current", {})
        if current:
            print()
            print("=== GRAPH STATE ===")
            current_tool = current.get("tool", {})
            print(f"Current Node: {current_tool.get('name', 'unknown')}")
            on_error = current.get("on_error", "N/A")
            print(f"On Error: {on_error}")

    # Result/Output
    result = task.get("result") or task.get("output")
    if result:
        print()
        print("=== RESULT ===")
        if isinstance(result, dict):
            print(json.dumps(result, indent=2)[:500])
        else:
            print(str(result)[:500])

    # Input data
    input_data = task.get("input") or task.get("inputData")
    if input_data and show_full:
        print()
        print("=== INPUT DATA ===")
        if isinstance(input_data, dict):
            print(json.dumps(input_data, indent=2)[:300])
        else:
            print(str(input_data)[:300])

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Get detailed information about Beam.ai tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Get details for a task
    python get_task_details.py abc123-def456

    # Get details for multiple tasks
    python get_task_details.py task1 task2 task3

    # Output as JSON
    python get_task_details.py abc123 --json

    # Show full details including graph state
    python get_task_details.py abc123 --full

    # Use production workspace
    python get_task_details.py abc123 --workspace prod

Environment Variables (in .env at project root):
    BEAM_API_KEY           Beam.ai API key (BID)
    BEAM_WORKSPACE_ID      Beam.ai workspace ID (BID)
    BEAM_API_KEY_PROD      Beam.ai API key (Production)
    BEAM_WORKSPACE_ID_PROD Beam.ai workspace ID (Production)
"""
    )

    parser.add_argument(
        "task_ids",
        nargs="+",
        help="One or more task IDs to fetch"
    )
    parser.add_argument(
        "--workspace", "-w",
        default="bid",
        choices=["bid", "prod"],
        help="Beam workspace (default: bid)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Show full response including all fields"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save output to file"
    )

    args = parser.parse_args()

    try:
        # Initialize client
        client = BeamClient(workspace=args.workspace)

        all_tasks = []

        for task_id in args.task_ids:
            try:
                task = get_task_details(client, task_id)
                all_tasks.append(task)

                if not args.json:
                    print_task_details(task, show_full=args.full)

            except Exception as e:
                if hasattr(e, 'response'):
                    print(f"Error fetching {task_id}: {e.response.status_code} - {e.response.text[:100]}")
                else:
                    print(f"Error fetching {task_id}: {e}")

        # JSON output
        if args.json:
            if len(all_tasks) == 1:
                print(json.dumps(all_tasks[0], indent=2))
            else:
                print(json.dumps(all_tasks, indent=2))

        # Save to file
        if args.output:
            output_data = all_tasks if len(all_tasks) > 1 else all_tasks[0] if all_tasks else {}
            Path(args.output).write_text(json.dumps(output_data, indent=2))
            print(f"\nResults saved to: {args.output}")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if hasattr(e, 'response'):
            print(f"API error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
