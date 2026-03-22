#!/usr/bin/env python3
"""Langfuse Scores — unified CRUD for scores (v2 reads, v1 writes) and score configs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("scores", "configs")

SCORE_CONFIGS = {
    "goal_achievement": {"id": "68cfd90c-8c9e-4907-808d-869ccd9a4c07", "type": "CATEGORICAL", "categories": ["failed", "partial", "complete", "exceeded"]},
    "tool_efficiency": {"id": "84965473-0f54-4248-999e-7b8627fc9c29", "type": "NUMERIC", "range": [0, 1]},
    "process_adherence": {"id": "651fc213-4750-4d4e-8155-270235c7cad8", "type": "NUMERIC", "range": [0, 1]},
    "context_efficiency": {"id": "ae22abed-bd4a-4926-af74-8d71edb1925d", "type": "NUMERIC", "range": [0, 1]},
    "error_handling": {"id": "96c290b7-e3a6-4caa-bace-93cf55f70f1c", "type": "CATEGORICAL", "categories": ["poor", "struggled", "recovered", "prevented"]},
    "output_quality": {"id": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed", "type": "NUMERIC", "range": [0, 1]},
    "overall_quality": {"id": "793f09d9-0053-4310-ad32-00dc06c69a71", "type": "NUMERIC", "range": [0, 1]},
    "root_cause_issues": {"id": "669bead7-1936-4fc4-bae8-e7814c9eab04", "type": "CATEGORICAL", "categories": ["none", "tool_misuse", "process_violation", "context_waste", "error_cascade", "output_quality", "multiple"]},
    "session_improvements": {"id": "2e87193b-c853-4955-b2f0-9fa572531681", "type": "CATEGORICAL", "categories": ["none", "minor", "moderate", "significant", "critical"]},
    "session_notes": {"id": "67640329-0c03-4be6-bc9f-49765a0462b5", "type": "NUMERIC", "range": [0, 1]},
}


def require(args, attr: str, ctx: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {ctx}", file=sys.stderr)
        sys.exit(1)


def paginate_all(fetch_page, limit=100, max_pages=None, cursor_mode=False):
    all_data, page, cursor = [], 1, None
    while True:
        if cursor_mode:
            result = fetch_page(limit, cursor)
        else:
            result = fetch_page(limit, page)
        data = result.get("data", [])
        all_data.extend(data)
        meta = result.get("meta", {})
        if cursor_mode:
            cursor = meta.get("nextCursor")
            if not cursor:
                break
        else:
            total_pages = meta.get("totalPages", 1)
            if page >= total_pages:
                break
            page += 1
        if max_pages and page > max_pages:
            break
        print(f"Fetched {len(all_data)} items so far...", file=sys.stderr)
    return all_data


# ── Scores ───────────────────────────────────────────────────────────────────

def scores_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.cursor:
        params["cursor"] = args.cursor
    for k, v in [("traceId", args.trace), ("observationId", args.observation),
                 ("name", args.name), ("source", args.source)]:
        if v:
            params[k] = v
    if args.all:
        data = paginate_all(
            lambda lim, cur: client.get("/v2/scores", params={**params, "limit": lim, **({"cursor": cur} if cur else {})}),
            limit=args.limit, max_pages=args.max_pages, cursor_mode=True,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/v2/scores", params=params)

def scores_get(args):
    require(args, "id", "scores get")
    return get_client().get(f"/v2/scores/{args.id}")

def scores_create(args):
    require(args, "trace", "scores create")
    require(args, "name", "scores create")
    body: dict = {"traceId": args.trace, "name": args.name}
    if args.value is not None:
        body["value"] = args.value
    if args.string_value:
        body["stringValue"] = args.string_value
    if args.data_type:
        body["dataType"] = args.data_type
    if args.observation:
        body["observationId"] = args.observation
    if args.comment:
        body["comment"] = args.comment
    if args.config_id:
        body["configId"] = args.config_id
    if args.metadata:
        body["metadata"] = json.loads(args.metadata) if isinstance(args.metadata, str) else args.metadata
    return get_client().post("/scores", data=body)

def scores_delete(args):
    require(args, "id", "scores delete")
    return get_client().delete(f"/scores/{args.id}")

def scores_list_configs_action(args):
    for name, cfg in SCORE_CONFIGS.items():
        t = cfg["type"]
        detail = cfg.get("categories", cfg.get("range", ""))
        print(f"  {name:25s} {t:12s} {cfg['id']}  {detail}")


# ── Score Configs ────────────────────────────────────────────────────────────

def configs_list(args):
    client = get_client()
    params = {"limit": min(args.limit, 100), "page": args.page or 1}
    if args.all:
        data = paginate_all(
            lambda lim, pg: client.get("/score-configs", params={"limit": min(lim, 100), "page": pg}),
            limit=args.limit, max_pages=args.max_pages,
        )
        return {"data": data, "meta": {"totalItems": len(data)}}
    return client.get("/score-configs", params=params)

def configs_get(args):
    require(args, "id", "configs get")
    return get_client().get(f"/score-configs/{args.id}")

def configs_create(args):
    require(args, "name", "configs create")
    require(args, "data_type", "configs create")
    body: dict = {"name": args.name, "dataType": args.data_type}
    if args.description:
        body["description"] = args.description
    if args.min_value is not None:
        body["minValue"] = args.min_value
    if args.max_value is not None:
        body["maxValue"] = args.max_value
    if args.categories:
        cats = [c.strip() for c in args.categories.split(",")]
        body["categories"] = [{"label": c, "value": i} for i, c in enumerate(cats)]
    return get_client().post("/score-configs", data=body)

def configs_update(args):
    require(args, "id", "configs update")
    body: dict = {}
    if args.description:
        body["description"] = args.description
    if args.archive:
        body["isArchived"] = True
    if args.unarchive:
        body["isArchived"] = False
    if not body:
        print("ERROR: provide --description, --archive, or --unarchive", file=sys.stderr)
        sys.exit(1)
    return get_client().patch(f"/score-configs/{args.id}", data=body)


DISPATCH = {
    ("scores", "list"): scores_list,
    ("scores", "get"): scores_get,
    ("scores", "create"): scores_create,
    ("scores", "delete"): scores_delete,
    ("scores", "list-configs"): scores_list_configs_action,
    ("configs", "list"): configs_list,
    ("configs", "get"): configs_get,
    ("configs", "create"): configs_create,
    ("configs", "update"): configs_update,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse scores — unified CRUD for scores and configs")
    parser.add_argument("--resource", required=True, choices=RESOURCES)
    parser.add_argument("--action", required=True)
    parser.add_argument("--id", help="Score or config ID")
    parser.add_argument("--trace", help="Trace ID (scores create)")
    parser.add_argument("--observation", help="Observation ID")
    parser.add_argument("--name", help="Score/config name")
    parser.add_argument("--value", type=float, help="Numeric score value")
    parser.add_argument("--string-value", help="Categorical score string value")
    parser.add_argument("--data-type", choices=["NUMERIC", "CATEGORICAL", "BOOLEAN"])
    parser.add_argument("--source", choices=["API", "EVAL", "ANNOTATION"])
    parser.add_argument("--comment", help="Score comment")
    parser.add_argument("--config-id", help="Score config ID")
    parser.add_argument("--metadata", help="Metadata JSON string")
    parser.add_argument("--description", help="Config description")
    parser.add_argument("--min", type=float, dest="min_value", help="Numeric min")
    parser.add_argument("--max", type=float, dest="max_value", help="Numeric max")
    parser.add_argument("--categories", help="Comma-separated category labels")
    parser.add_argument("--archive", action="store_true")
    parser.add_argument("--unarchive", action="store_true")
    parser.add_argument("--cursor", help="Pagination cursor (scores list)")
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
        if result is not None:
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
