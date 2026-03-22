#!/usr/bin/env python3
"""Langfuse Prompts — unified CRUD for prompts and prompt versions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def require(args, attr: str, ctx: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {ctx}", file=sys.stderr)
        sys.exit(1)


def prompts_list(args):
    client = get_client()
    params: dict = {"limit": min(args.limit, 100)}
    if args.page:
        params["page"] = args.page
    for k, v in [("name", args.name), ("label", args.label), ("tag", args.tag)]:
        if v:
            params[k] = v
    for k, v in [("fromUpdatedAt", args.from_ts), ("toUpdatedAt", args.to_ts)]:
        if v:
            params[k] = v
    return client.get("/v2/prompts", params=params)


def prompts_get(args):
    require(args, "name", "get")
    params: dict = {}
    if args.version:
        params["version"] = args.version
    if args.label:
        params["label"] = args.label
    return get_client().get(f"/v2/prompts/{args.name}", params=params)


def prompts_create(args):
    require(args, "name", "create")
    require(args, "prompt", "create")
    body: dict = {"name": args.name, "type": args.type or "text"}
    prompt_val = args.prompt
    if body["type"] == "chat":
        try:
            prompt_val = json.loads(prompt_val)
        except json.JSONDecodeError:
            pass
    body["prompt"] = prompt_val
    if args.labels:
        body["labels"] = [l.strip() for l in args.labels.split(",")]
    if args.config:
        body["config"] = json.loads(args.config)
    return get_client().post("/v2/prompts", data=body)


def prompts_delete(args):
    require(args, "name", "delete")
    return get_client().delete(f"/v2/prompts/{args.name}")


def prompts_update_version(args):
    require(args, "name", "update-version")
    require(args, "version", "update-version")
    body: dict = {}
    if args.labels:
        body["labels"] = [l.strip() for l in args.labels.split(",")]
    return get_client().patch(f"/v2/prompts/{args.name}/versions/{args.version}", data=body)


DISPATCH = {
    "list": prompts_list,
    "get": prompts_get,
    "create": prompts_create,
    "delete": prompts_delete,
    "update-version": prompts_update_version,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse prompts — unified CRUD")
    parser.add_argument("--action", required=True, choices=list(DISPATCH.keys()))
    parser.add_argument("--name", help="Prompt name")
    parser.add_argument("--prompt", help="Prompt content (text or JSON for chat)")
    parser.add_argument("--type", choices=["text", "chat"], default="text")
    parser.add_argument("--version", type=int, help="Prompt version")
    parser.add_argument("--label", help="Filter by label (list/get)")
    parser.add_argument("--labels", help="Comma-separated labels (create/update-version)")
    parser.add_argument("--tag", help="Filter by tag (list)")
    parser.add_argument("--config", help="Config JSON (create)")
    parser.add_argument("--from", dest="from_ts", help="From timestamp")
    parser.add_argument("--to", dest="to_ts", help="To timestamp")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    try:
        result = DISPATCH[args.action](args)
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
