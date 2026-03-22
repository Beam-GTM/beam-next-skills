#!/usr/bin/env python3
"""Langfuse delete traces — single ID or bulk/filter.

WARNING: This is a DESTRUCTIVE operation. Deleted traces cannot be recovered.
Deletion is QUEUED - traces may take several seconds to actually disappear.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def delete_single_trace(trace_id: str) -> dict:
    """Delete one trace by ID (DELETE /traces/{id})."""
    client = get_client()
    return client.delete(f"/traces/{trace_id}")


def delete_traces_bulk(trace_ids: list = None, filter_obj: dict = None) -> dict:
    """Delete multiple traces by IDs or filter (DELETE /traces with body)."""
    if not trace_ids and not filter_obj:
        raise ValueError("Must provide either trace_ids or filter_obj")

    client = get_client()
    data = {}
    if trace_ids:
        data["traceIds"] = trace_ids
    if filter_obj:
        data["filter"] = filter_obj
    return client.delete("/traces", params=data)


def main():
    parser = argparse.ArgumentParser(
        description="Delete trace(s) (DESTRUCTIVE - cannot be undone). "
        "Use --id for one trace, or --ids/--filter for bulk."
    )
    parser.add_argument(
        "--id",
        type=str,
        help="Single trace ID (DELETE /traces/{id}). Mutually exclusive with --ids/--filter.",
    )
    parser.add_argument("--ids", type=str, help="Comma-separated trace IDs (bulk)")
    parser.add_argument("--filter", type=str, help='JSON filter object (e.g., \'{"sessionId": "abc"}\')')
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt (for scripting)",
    )
    args = parser.parse_args()

    if args.id:
        if args.ids or args.filter:
            parser.error("Use either --id for a single trace, or --ids/--filter for bulk — not both.")
        print(f"Will delete trace: {args.id}")
        if not args.confirm:
            response = input("Type 'DELETE' to confirm: ")
            if response != "DELETE":
                print("Aborted.")
                sys.exit(0)
        try:
            result = delete_single_trace(args.id)
            print(json.dumps(result, indent=2, default=str))
            print("\nNote: Deletion is QUEUED. Trace may take ~5s to disappear.")
            print("Warning: API returns success even for nonexistent IDs.")
        except LangfuseAPIError as e:
            print(f"API ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if not args.ids and not args.filter:
        parser.error("Must provide --id for a single trace, or --ids and/or --filter for bulk")

    trace_ids = args.ids.split(",") if args.ids else None
    filter_obj = json.loads(args.filter) if args.filter else None

    if trace_ids:
        print(f"Will delete {len(trace_ids)} trace(s): {trace_ids[:5]}{'...' if len(trace_ids) > 5 else ''}")
    if filter_obj:
        print(f"Will delete traces matching filter: {filter_obj}")

    if not args.confirm:
        response = input("Type 'DELETE' to confirm: ")
        if response != "DELETE":
            print("Aborted.")
            sys.exit(0)

    try:
        result = delete_traces_bulk(trace_ids=trace_ids, filter_obj=filter_obj)
        print(json.dumps(result, indent=2, default=str))
        print("\nNote: Deletion is QUEUED. Traces may take ~5s to disappear.")
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
