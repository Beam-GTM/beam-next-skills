#!/usr/bin/env python3
"""Langfuse Models — unified CRUD for model definitions."""

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


def models_list(args):
    return get_client().get("/models", params={"limit": min(args.limit, 100), "page": args.page or 1})

def models_get(args):
    require(args, "id", "get")
    return get_client().get(f"/models/{args.id}")

def models_create(args):
    require(args, "name", "create")
    body: dict = {"modelName": args.name}
    if args.match_pattern:
        body["matchPattern"] = args.match_pattern
    if args.unit:
        body["unit"] = args.unit
    if args.input_price is not None:
        body["inputPrice"] = args.input_price
    if args.output_price is not None:
        body["outputPrice"] = args.output_price
    if args.total_price is not None:
        body["totalPrice"] = args.total_price
    if args.tokenizer:
        body["tokenizerId"] = args.tokenizer
    return get_client().post("/models", data=body)

def models_delete(args):
    require(args, "id", "delete")
    return get_client().delete(f"/models/{args.id}")


DISPATCH = {"list": models_list, "get": models_get, "create": models_create, "delete": models_delete}


def main():
    parser = argparse.ArgumentParser(description="Langfuse models — unified CRUD")
    parser.add_argument("--action", required=True, choices=list(DISPATCH.keys()))
    parser.add_argument("--id", help="Model ID")
    parser.add_argument("--name", help="Model name (create)")
    parser.add_argument("--match-pattern", help="Regex match pattern")
    parser.add_argument("--unit", help="Pricing unit (e.g. TOKENS)")
    parser.add_argument("--input-price", type=float)
    parser.add_argument("--output-price", type=float)
    parser.add_argument("--total-price", type=float)
    parser.add_argument("--tokenizer", help="Tokenizer ID")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    try:
        result = DISPATCH[args.action](args)
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
