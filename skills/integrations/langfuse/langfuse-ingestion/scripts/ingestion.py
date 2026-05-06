#!/usr/bin/env python3
"""Langfuse Ingestion — batch ingest, OTEL, comments, and media."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("batch", "otel", "comments", "media")


def require(args, attr: str, ctx: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {ctx}", file=sys.stderr)
        sys.exit(1)


def load_json_data(args) -> list | dict:
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            return json.load(f)
    if args.data:
        return json.loads(args.data)
    print("ERROR: provide --file or --data", file=sys.stderr)
    sys.exit(1)


# ── Batch ────────────────────────────────────────────────────────────────────

def batch_ingest(args):
    payload = load_json_data(args)
    batch = payload if isinstance(payload, list) else payload.get("batch", [payload])
    return get_client().post("/ingestion", data={"batch": batch})


# ── OTEL ─────────────────────────────────────────────────────────────────────

def otel_ingest(args):
    payload = load_json_data(args)
    if isinstance(payload, list):
        body = {"resourceSpans": payload}
    elif "resourceSpans" in payload:
        body = payload
    else:
        body = {"resourceSpans": [payload]}
    return get_client().post("/otel/v1/traces", data=body)


# ── Comments ─────────────────────────────────────────────────────────────────

def comments_list(args):
    params: dict = {}
    if args.type:
        params["objectType"] = args.type
    if args.object_id:
        params["objectId"] = args.object_id
    if args.page:
        params["page"] = args.page
    if args.limit:
        params["limit"] = min(args.limit, 100)
    return get_client().get("/comments", params=params)

def comments_get(args):
    require(args, "id", "comments get")
    return get_client().get(f"/comments/{args.id}")

def comments_create(args):
    require(args, "type", "comments create")
    require(args, "object_id", "comments create")
    require(args, "content", "comments create")
    body: dict = {"objectType": args.type, "objectId": args.object_id, "content": args.content}
    if args.author:
        body["authorUserId"] = args.author
    return get_client().post("/comments", data=body)


# ── Media ────────────────────────────────────────────────────────────────────

def media_get(args):
    require(args, "id", "media get")
    return get_client().get(f"/media/{args.id}")

def media_update(args):
    require(args, "id", "media update")
    body: dict = {}
    if args.uploaded:
        body["uploadedToGcs"] = True
    return get_client().patch(f"/media/{args.id}", data=body)

def media_upload_url(args):
    require(args, "trace", "media upload-url")
    require(args, "field", "media upload-url")
    require(args, "content_type", "media upload-url")
    body: dict = {"traceId": args.trace, "field": args.field, "contentType": args.content_type}
    if args.observation:
        body["observationId"] = args.observation
    return get_client().post("/media", data=body)


DISPATCH = {
    ("batch", "ingest"): batch_ingest,
    ("otel", "ingest"): otel_ingest,
    ("comments", "list"): comments_list,
    ("comments", "get"): comments_get,
    ("comments", "create"): comments_create,
    ("media", "get"): media_get,
    ("media", "update"): media_update,
    ("media", "upload-url"): media_upload_url,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse ingestion — batch, OTEL, comments, media")
    parser.add_argument("--resource", required=True, choices=RESOURCES)
    parser.add_argument("--action", required=True)
    parser.add_argument("--id", help="Comment/media ID")
    parser.add_argument("--file", help="JSON file for ingest")
    parser.add_argument("--data", help="JSON string for ingest")
    parser.add_argument("--type", help="Object type (TRACE/OBSERVATION) for comments; content type for media")
    parser.add_argument("--content-type", dest="content_type", help="MIME content type (media upload-url)")
    parser.add_argument("--object-id", help="Object ID (comments)")
    parser.add_argument("--content", help="Comment content")
    parser.add_argument("--author", help="Author user ID (comments)")
    parser.add_argument("--trace", help="Trace ID (media)")
    parser.add_argument("--observation", help="Observation ID (media)")
    parser.add_argument("--field", help="Field name (media)")
    parser.add_argument("--uploaded", action="store_true", help="Mark uploaded (media update)")
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
