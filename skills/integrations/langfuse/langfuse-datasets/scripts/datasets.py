#!/usr/bin/env python3
"""Langfuse Datasets — unified CRUD for datasets, items, runs, and run-items.

Usage:
    uv run python datasets.py --resource datasets --action list [--limit N] [--all]
    uv run python datasets.py --resource items --action create --dataset NAME --input '{...}'
    uv run python datasets.py --resource runs --action get --dataset NAME --run RUN
    uv run python datasets.py --resource run-items --action list --dataset NAME --run RUN
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("datasets", "items", "runs", "run-items")
ACTIONS_BY_RESOURCE = {
    "datasets": ("list", "create", "get"),
    "items": ("list", "create", "get", "delete"),
    "runs": ("list", "get", "delete"),
    "run-items": ("list", "create"),
}


def parse_json_arg(value: str, arg_name: str) -> dict:
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        print(f"JSON ERROR in --{arg_name}: {e}", file=sys.stderr)
        print(f"Value was: {value[:100]}{'...' if len(value) > 100 else ''}", file=sys.stderr)
        sys.exit(1)


def paginate_all(fetch_page, limit: int = 100, max_pages: int | None = None) -> list:
    """Generic paginator: calls fetch_page(limit, page) until done."""
    all_data = []
    page = 1
    while True:
        result = fetch_page(limit, page)
        data = result.get("data", [])
        all_data.extend(data)
        meta = result.get("meta", {})
        total_pages = meta.get("totalPages", 1)
        print(f"Fetched page {page}/{total_pages} ({len(data)} items)", file=sys.stderr)
        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}", file=sys.stderr)
            break
        page += 1
    print(f"Total: {len(all_data)} items", file=sys.stderr)
    return all_data


# ── Datasets ─────────────────────────────────────────────────────────────────

def datasets_list(args):
    client = get_client()
    if args.all:
        data = paginate_all(
            lambda lim, pg: client.get("/v2/datasets", params={"limit": min(lim, 100), "page": pg}),
            limit=args.limit, max_pages=args.max_pages,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/v2/datasets", params={"limit": min(args.limit, 100), "page": args.page})


def datasets_create(args):
    require(args, "name", "datasets create")
    client = get_client()
    body: dict = {"name": args.name}
    if args.description:
        body["description"] = args.description
    if args.metadata:
        body["metadata"] = parse_json_arg(args.metadata, "metadata")
    return client.post("/v2/datasets", data=body)


def datasets_get(args):
    require(args, "name", "datasets get")
    return get_client().get(f"/v2/datasets/{args.name}")


# ── Items ────────────────────────────────────────────────────────────────────

def items_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.dataset:
        params["datasetName"] = args.dataset
    if args.page:
        params["page"] = args.page
    if args.all:
        data = paginate_all(
            lambda lim, pg: client.get("/dataset-items", params={**params, "limit": min(lim, 100), "page": pg}),
            limit=args.limit, max_pages=args.max_pages,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/dataset-items", params=params)


def items_create(args):
    require(args, "dataset", "items create")
    require(args, "input", "items create")
    client = get_client()
    body: dict = {"datasetName": args.dataset, "input": parse_json_arg(args.input, "input")}
    if args.expected:
        body["expectedOutput"] = parse_json_arg(args.expected, "expected")
    if args.metadata:
        body["metadata"] = parse_json_arg(args.metadata, "metadata")
    if args.id:
        body["id"] = args.id
    return client.post("/dataset-items", data=body)


def items_get(args):
    require(args, "id", "items get")
    return get_client().get(f"/dataset-items/{args.id}")


def items_delete(args):
    require(args, "id", "items delete")
    return get_client().delete(f"/dataset-items/{args.id}")


# ── Runs ─────────────────────────────────────────────────────────────────────

def runs_list(args):
    require(args, "dataset", "runs list")
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.page:
        params["page"] = args.page
    return client.get(f"/datasets/{args.dataset}/runs", params=params)


def runs_get(args):
    require(args, "dataset", "runs get")
    require(args, "run", "runs get")
    return get_client().get(f"/datasets/{args.dataset}/runs/{args.run}")


def runs_delete(args):
    require(args, "dataset", "runs delete")
    require(args, "run", "runs delete")
    return get_client().delete(f"/datasets/{args.dataset}/runs/{args.run}")


# ── Run Items ────────────────────────────────────────────────────────────────

def run_items_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.dataset:
        params["datasetName"] = args.dataset
    if args.run:
        params["runName"] = args.run
    if args.page:
        params["page"] = args.page
    return client.get("/dataset-run-items", params=params)


def run_items_create(args):
    require(args, "run", "run-items create")
    require(args, "dataset_item", "run-items create")
    body: dict = {"runName": args.run, "datasetItemId": args.dataset_item}
    if args.trace:
        body["traceId"] = args.trace
    if args.observation:
        body["observationId"] = args.observation
    return get_client().post("/dataset-run-items", data=body)


# ── Dispatch ─────────────────────────────────────────────────────────────────

DISPATCH = {
    ("datasets", "list"): datasets_list,
    ("datasets", "create"): datasets_create,
    ("datasets", "get"): datasets_get,
    ("items", "list"): items_list,
    ("items", "create"): items_create,
    ("items", "get"): items_get,
    ("items", "delete"): items_delete,
    ("runs", "list"): runs_list,
    ("runs", "get"): runs_get,
    ("runs", "delete"): runs_delete,
    ("run-items", "list"): run_items_list,
    ("run-items", "create"): run_items_create,
}


def require(args, attr: str, context: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {context}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Langfuse datasets — unified CRUD for datasets, items, runs, run-items"
    )
    parser.add_argument("--resource", required=True, choices=RESOURCES, help="Resource type")
    parser.add_argument("--action", required=True, help="Action (list, get, create, delete)")

    parser.add_argument("--name", help="Dataset name (datasets create/get)")
    parser.add_argument("--dataset", help="Dataset name (items/runs/run-items)")
    parser.add_argument("--run", help="Run name")
    parser.add_argument("--id", help="Item ID")
    parser.add_argument("--dataset-item", help="Dataset item ID (run-items create)")
    parser.add_argument("--trace", help="Trace ID (run-items create)")
    parser.add_argument("--observation", help="Observation ID (run-items create)")
    parser.add_argument("--input", help="Input JSON (items create)")
    parser.add_argument("--expected", help="Expected output JSON (items create)")
    parser.add_argument("--description", help="Description (datasets create)")
    parser.add_argument("--metadata", help="Metadata JSON")

    parser.add_argument("--limit", type=int, default=50, help="Max results per page (max 100)")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--all", action="store_true", help="Fetch all pages")
    parser.add_argument("--max-pages", type=int, help="Stop after N pages with --all")
    parser.add_argument("--output", "-o", help="Write JSON to file instead of stdout")
    args = parser.parse_args()

    key = (args.resource, args.action)
    if key not in DISPATCH:
        valid = ", ".join(ACTIONS_BY_RESOURCE.get(args.resource, ()))
        print(f"ERROR: invalid action '{args.action}' for {args.resource}. Valid: {valid}", file=sys.stderr)
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
