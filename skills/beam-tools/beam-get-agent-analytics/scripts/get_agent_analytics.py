#!/usr/bin/env python3
"""
Beam.ai Get Agent Analytics

Retrieve analytics and performance metrics for a Beam.ai agent.

Usage:
    # Get analytics for last 7 days
    python get_agent_analytics.py <agent_id>

    # Get analytics for specific date range
    python get_agent_analytics.py <agent_id> --start 2024-01-01 --end 2024-01-31

    # Get analytics for last 30 days
    python get_agent_analytics.py <agent_id> --days 30
"""

import argparse
import json
import sys
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


def get_agent_analytics(
    client: BeamClient,
    agent_id: str,
    start_date: str,
    end_date: str
) -> dict:
    """
    Get analytics for an agent.

    Args:
        client: BeamClient instance
        agent_id: Agent ID (UUID)
        start_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
        end_date: End date in ISO format (YYYY-MM-DDTHH:MM:SSZ)

    Returns:
        Analytics response dict
    """
    params = {
        "agentId": agent_id,
        "startDate": start_date,
        "endDate": end_date
    }
    return client.get("/agent-tasks/analytics", params=params)


def format_percentage(value: float, total: float) -> str:
    """Format a value as percentage of total."""
    if total == 0:
        return "0.0%"
    return f"{(value / total * 100):.1f}%"


def format_delta(delta: str) -> str:
    """Format a delta string with color indicators."""
    if not delta:
        return "N/A"
    # Add visual indicator
    if delta.startswith("+"):
        return f"{delta}"
    elif delta.startswith("-"):
        return f"{delta}"
    return delta


def format_seconds(seconds: float) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hrs"


def print_analytics(data: dict, agent_name: str, start_date: str, end_date: str, workspace: str):
    """Print analytics in human-readable format."""
    current = data.get("currentPeriod", {})
    deltas = data.get("metricsDelta", {})
    chart = data.get("taskAndEvaluationChart", [])

    # Header
    print(f"\nAgent Analytics: {agent_name}")
    print(f"Period: {start_date[:10]} to {end_date[:10]}")
    print(f"Workspace: {workspace}")
    print()

    # Current Period
    print("=== CURRENT PERIOD ===")
    total = current.get("totalTasks", 0)
    completed = current.get("completedTasks", 0)
    failed = current.get("failedTasks", 0)

    print(f"Total Tasks:     {total}")
    print(f"Completed:       {completed} ({format_percentage(completed, total)})")
    print(f"Failed:          {failed} ({format_percentage(failed, total)})")

    avg_score = current.get("averageEvaluationScore")
    if avg_score is not None:
        print(f"Avg Eval Score:  {avg_score:.1f}")

    avg_runtime = current.get("averageRuntimeSeconds", 0)
    total_runtime = current.get("totalRuntimeSeconds", 0)
    print(f"Avg Runtime:     {format_seconds(avg_runtime)}")
    print(f"Total Runtime:   {total_runtime:,}s ({format_seconds(total_runtime)})")

    # Feedback
    pos_feedback = current.get("positiveFeedbackCount", 0)
    neg_feedback = current.get("negativeFeedbackCount", 0)
    consent = current.get("consentRequiredCount", 0)

    if pos_feedback or neg_feedback or consent:
        print()
        print("Feedback:")
        print(f"  Positive: {pos_feedback}")
        print(f"  Negative: {neg_feedback}")
        print(f"  Consent Required: {consent}")

    # Deltas vs previous period
    print()
    print("=== VS PREVIOUS PERIOD ===")
    print(f"Total Tasks:     {format_delta(deltas.get('totalTasksDelta', 'N/A'))}")
    print(f"Completed:       {format_delta(deltas.get('completedTasksDelta', 'N/A'))}")
    print(f"Failed:          {format_delta(deltas.get('failedTasksDelta', 'N/A'))}")
    print(f"Eval Score:      {format_delta(deltas.get('averageEvaluationScoreDelta', 'N/A'))}")
    print(f"Runtime:         {format_delta(deltas.get('averageRuntimeSecondsDelta', 'N/A'))}")

    # Daily chart (last 7 days)
    if chart:
        print()
        print(f"=== DAILY TREND (last {min(7, len(chart))} days) ===")
        print("Date       | Completed | Failed | Eval Score")
        print("-----------+-----------+--------+-----------")

        for entry in chart[-7:]:
            date = entry.get("date", "")[:10]
            completed_count = entry.get("completedCount", 0)
            failed_count = entry.get("failedCount", 0)
            score = entry.get("averageEvaluationScore")
            score_str = f"{score:.1f}" if score is not None else "N/A"
            print(f"{date} | {completed_count:>9} | {failed_count:>6} | {score_str:>10}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Get analytics for a Beam.ai agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Get analytics for last 7 days
    python get_agent_analytics.py abc123-def456

    # Get analytics for specific date range
    python get_agent_analytics.py abc123 --start 2024-01-01 --end 2024-01-31

    # Get analytics for last 30 days on production
    python get_agent_analytics.py abc123 --days 30 --workspace prod

    # Output as JSON
    python get_agent_analytics.py abc123 --json

Environment Variables (in .env at project root):
    BEAM_API_KEY           Beam.ai API key (BID)
    BEAM_WORKSPACE_ID      Beam.ai workspace ID (BID)
    BEAM_API_KEY_PROD      Beam.ai API key (Production)
    BEAM_WORKSPACE_ID_PROD Beam.ai workspace ID (Production)
"""
    )

    parser.add_argument("agent_id", help="Agent ID (UUID)")

    # Date options
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        choices=[1, 7, 14, 30, 90],
        help="Look back N days (default: 7)"
    )

    parser.add_argument(
        "--start", "-s",
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end", "-e",
        help="End date (YYYY-MM-DD)"
    )

    # Options
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
        "--output", "-o",
        help="Save output to file"
    )

    args = parser.parse_args()

    try:
        # Initialize client
        client = BeamClient(workspace=args.workspace)

        # Calculate date range
        if args.start and args.end:
            # Use provided dates
            start_date = f"{args.start}T00:00:00Z"
            end_date = f"{args.end}T23:59:59Z"
        else:
            # Calculate from days
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=args.days)
            start_date = start.strftime("%Y-%m-%dT00:00:00Z")
            end_date = end.strftime("%Y-%m-%dT23:59:59Z")

        # Get agent info for display
        try:
            agent_info = client.get(f"/agent/{args.agent_id}")
            agent_name = agent_info.get("name", args.agent_id)
        except Exception:
            agent_name = args.agent_id

        # Get analytics
        analytics = get_agent_analytics(
            client,
            args.agent_id,
            start_date,
            end_date
        )

        # Output
        if args.json:
            output = json.dumps(analytics, indent=2)
            print(output)
        else:
            print_analytics(analytics, agent_name, start_date, end_date, args.workspace)

        # Save to file
        if args.output:
            output_data = {
                "agent_id": args.agent_id,
                "agent_name": agent_name,
                "start_date": start_date,
                "end_date": end_date,
                "workspace": args.workspace,
                "analytics": analytics
            }
            Path(args.output).write_text(json.dumps(output_data, indent=2))
            print(f"Results saved to: {args.output}")

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
