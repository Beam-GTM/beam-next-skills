#!/usr/bin/env python3
"""Langfuse Status — health checks and usage metrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def main():
    parser = argparse.ArgumentParser(description="Langfuse status — health and metrics")
    parser.add_argument("--action", required=True, choices=["health", "metrics"])
    parser.add_argument("--output", "-o", help="Write JSON to file")
    args = parser.parse_args()

    client = get_client()
    try:
        if args.action == "health":
            result = client.get("/health")
        else:
            result = client.get("/metrics")

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
