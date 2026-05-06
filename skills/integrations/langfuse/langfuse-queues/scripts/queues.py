#!/usr/bin/env python3
"""Langfuse Annotation Queues — unified CRUD for queues, items, and assignments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("queues", "items", "assignments")


def require(args, attr: str, context: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {context}", file=sys.stderr)
        sys.exit(1)


# ── Queues ───────────────────────────────────────────────────────────────────

def queues_list(args):
    params = {"limit": min(args.limit, 100)}
    if args.page:
        params["page"] = args.page
    return get_client().get("/annotation-queues", params=params)

def queues_create(args):
    require(args, "name", "queues create")
    body: dict = {"name": args.name}
    if args.description:
        body["description"] = args.description
    return get_client().post("/annotation-queues", data=body)

def queues_get(args):
    require(args, "id", "queues get")
    return get_client().get(f"/annotation-queues/{args.id}")


# ── Items ────────────────────────────────────────────────────────────────────

def items_list(args):
    require(args, "queue", "items list")
    params = {"limit": min(args.limit, 100)}
    return get_client().get(f"/annotation-queues/{args.queue}/items", params=params)

def items_create(args):
    require(args, "queue", "items create")
    require(args, "trace", "items create")
    body: dict = {"traceId": args.trace}
    if args.observation:
        body["observationId"] = args.observation
    return get_client().post(f"/annotation-queues/{args.queue}/items", data=body)

def items_get(args):
    require(args, "queue", "items get")
    require(args, "item", "items get")
    return get_client().get(f"/annotation-queues/{args.queue}/items/{args.item}")

def items_update(args):
    require(args, "queue", "items update")
    require(args, "item", "items update")
    body: dict = {}
    if args.status:
        body["status"] = args.status
    return get_client().patch(f"/annotation-queues/{args.queue}/items/{args.item}", data=body)

def items_delete(args):
    require(args, "queue", "items delete")
    require(args, "item", "items delete")
    return get_client().delete(f"/annotation-queues/{args.queue}/items/{args.item}")


# ── Assignments ──────────────────────────────────────────────────────────────

def assignments_create(args):
    require(args, "queue", "assignments create")
    require(args, "user", "assignments create")
    return get_client().post(f"/annotation-queues/{args.queue}/assignments", data={"userEmail": args.user})

def assignments_delete(args):
    require(args, "queue", "assignments delete")
    require(args, "user", "assignments delete")
    return get_client().delete(f"/annotation-queues/{args.queue}/assignments", params={"userEmail": args.user})


DISPATCH = {
    ("queues", "list"): queues_list,
    ("queues", "create"): queues_create,
    ("queues", "get"): queues_get,
    ("items", "list"): items_list,
    ("items", "create"): items_create,
    ("items", "get"): items_get,
    ("items", "update"): items_update,
    ("items", "delete"): items_delete,
    ("assignments", "create"): assignments_create,
    ("assignments", "delete"): assignments_delete,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse annotation queues — unified CRUD")
    parser.add_argument("--resource", required=True, choices=RESOURCES)
    parser.add_argument("--action", required=True, help="list, get, create, update, delete")
    parser.add_argument("--id", help="Queue ID (queues get)")
    parser.add_argument("--queue", help="Queue ID (items/assignments)")
    parser.add_argument("--item", help="Queue item ID")
    parser.add_argument("--trace", help="Trace ID (items create)")
    parser.add_argument("--observation", help="Observation ID (items create)")
    parser.add_argument("--user", help="User email (assignments)")
    parser.add_argument("--name", help="Queue name (queues create)")
    parser.add_argument("--description", help="Queue description")
    parser.add_argument("--status", choices=["PENDING", "IN_PROGRESS", "COMPLETED"], help="Item status (items update)")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    key = (args.resource, args.action)
    if key not in DISPATCH:
        print(f"ERROR: invalid action '{args.action}' for {args.resource}", file=sys.stderr)
        sys.exit(1)

    try:
        result = DISPATCH[key](args)
        payload = json.dumps(result, indent=2, default=str, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(payload)
            print(f"Output written to {args.output}", file=sys.stderr)
        else:
            print(payload)
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
