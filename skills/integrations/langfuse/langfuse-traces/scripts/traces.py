#!/usr/bin/env python3
"""Langfuse Traces — unified query/delete for traces, observations, and sessions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("traces", "observations", "sessions")


def require(args, attr: str, ctx: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {ctx}", file=sys.stderr)
        sys.exit(1)


def paginate_all(fetch_page, limit=100, max_pages=None, cursor_mode=False):
    all_data, page, cursor = [], 1, None
    while True:
        result = fetch_page(limit, page if not cursor_mode else cursor)
        data = result.get("data", [])
        all_data.extend(data)
        meta = result.get("meta", {})
        if cursor_mode:
            cursor = meta.get("nextCursor")
            if not cursor:
                break
        else:
            if page >= meta.get("totalPages", 1):
                break
            page += 1
        if max_pages and (page if not cursor_mode else len(all_data) // limit) > max_pages:
            break
        print(f"Fetched {len(all_data)} items...", file=sys.stderr)
    return all_data


def output_result(result, args):
    if result is None:
        return
    payload = json.dumps(result, indent=2, default=str, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(payload)


# ── Traces ───────────────────────────────────────────────────────────────────

def traces_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.page:
        params["page"] = args.page
    for k, v in [("userId", args.user_id), ("sessionId", args.session_id),
                 ("name", args.name), ("orderBy", args.order_by), ("order", args.order)]:
        if v:
            params[k] = v
    for k, v in [("fromTimestamp", args.from_ts), ("toTimestamp", args.to_ts)]:
        if v:
            params[k] = v
    if args.all:
        data = paginate_all(
            lambda lim, pg: client.get("/traces", params={**params, "limit": min(lim, 100), "page": pg}),
            limit=args.limit, max_pages=args.max_pages,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/traces", params=params)

def traces_get(args):
    require(args, "id", "traces get")
    return get_client().get(f"/traces/{args.id}")

def traces_delete(args):
    client = get_client()
    if args.id:
        if not args.confirm:
            resp = input(f"Delete trace {args.id}? Type 'DELETE' to confirm: ")
            if resp != "DELETE":
                print("Aborted.")
                return None
        result = client.delete(f"/traces/{args.id}")
        print("Deletion queued (~5s to take effect).", file=sys.stderr)
        return result
    ids = args.ids.split(",") if args.ids else None
    filter_obj = json.loads(args.filter) if args.filter else None
    if not ids and not filter_obj:
        print("ERROR: provide --id, --ids, or --filter for traces delete", file=sys.stderr)
        sys.exit(1)
    if not args.confirm:
        resp = input("Type 'DELETE' to confirm bulk delete: ")
        if resp != "DELETE":
            print("Aborted.")
            return None
    data: dict = {}
    if ids:
        data["traceIds"] = ids
    if filter_obj:
        data["filter"] = filter_obj
    result = client.delete("/traces", params=data)
    print("Deletion queued.", file=sys.stderr)
    return result


# ── Observations ─────────────────────────────────────────────────────────────

def observations_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.cursor:
        params["cursor"] = args.cursor
    for k, v in [("traceId", args.trace_id), ("type", args.type), ("name", args.name)]:
        if v:
            params[k] = v
    for k, v in [("fromStartTime", args.from_ts), ("toStartTime", args.to_ts)]:
        if v:
            params[k] = v
    try:
        if args.all:
            data = paginate_all(
                lambda lim, cur: client.get("/v2/observations", params={**params, "limit": min(lim, 100), **({"cursor": cur} if cur else {})}),
                limit=args.limit, max_pages=args.max_pages, cursor_mode=True,
            )
            return {"data": data, "meta": {"totalItems": len(data)}}
        return client.get("/v2/observations", params=params)
    except LangfuseAPIError:
        return client.get("/observations", params={"limit": params.get("limit", 50)})

def observations_get(args):
    require(args, "id", "observations get")
    return get_client().get(f"/observations/{args.id}")


# ── Sessions ─────────────────────────────────────────────────────────────────

def sessions_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.page:
        params["page"] = args.page
    for k, v in [("fromCreatedAt", args.from_ts), ("toCreatedAt", args.to_ts)]:
        if v:
            params[k] = v
    if args.all:
        data = paginate_all(
            lambda lim, pg: client.get("/sessions", params={**params, "limit": min(lim, 100), "page": pg}),
            limit=args.limit, max_pages=args.max_pages,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/sessions", params=params)

def sessions_get(args):
    require(args, "id", "sessions get")
    return get_client().get(f"/sessions/{args.id}")


DISPATCH = {
    ("traces", "list"): traces_list,
    ("traces", "get"): traces_get,
    ("traces", "delete"): traces_delete,
    ("observations", "list"): observations_list,
    ("observations", "get"): observations_get,
    ("sessions", "list"): sessions_list,
    ("sessions", "get"): sessions_get,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse traces — unified query/delete")
    parser.add_argument("--resource", required=True, choices=RESOURCES)
    parser.add_argument("--action", required=True)
    parser.add_argument("--id", help="Trace/observation/session ID")
    parser.add_argument("--ids", help="Comma-separated trace IDs (bulk delete)")
    parser.add_argument("--filter", help="JSON filter (bulk delete)")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    parser.add_argument("--trace-id", help="Filter by trace ID (observations)")
    parser.add_argument("--user-id", help="Filter by user ID (traces)")
    parser.add_argument("--session-id", help="Filter by session ID (traces)")
    parser.add_argument("--name", help="Filter by name")
    parser.add_argument("--type", help="Observation type filter")
    parser.add_argument("--order-by", help="Order by field")
    parser.add_argument("--order", choices=["ASC", "DESC"])
    parser.add_argument("--from", dest="from_ts", help="From timestamp (ISO8601)")
    parser.add_argument("--to", dest="to_ts", help="To timestamp (ISO8601)")
    parser.add_argument("--cursor", help="Pagination cursor")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    key = (args.resource, args.action)
    if key not in DISPATCH:
        print(f"ERROR: invalid action '{args.action}' for {args.resource}", file=sys.stderr)
        sys.exit(1)

    try:
        result = DISPATCH[key](args)
        output_result(result, args)
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
