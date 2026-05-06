#!/usr/bin/env python3
"""Langfuse Admin — unified projects, API keys, and organization management."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError

RESOURCES = ("projects", "api-keys", "org")


def require(args, attr: str, ctx: str):
    if not getattr(args, attr.replace("-", "_"), None):
        print(f"ERROR: --{attr} is required for {ctx}", file=sys.stderr)
        sys.exit(1)


# ── Projects ─────────────────────────────────────────────────────────────────

def projects_get(args):
    return get_client().get("/projects")

def projects_create(args):
    require(args, "name", "projects create")
    body: dict = {"name": args.name}
    if args.org:
        body["orgId"] = args.org
    return get_client().post("/v2/projects", data=body)

def projects_update(args):
    require(args, "project", "projects update")
    body: dict = {}
    if args.name:
        body["name"] = args.name
    return get_client().put(f"/v2/projects/{args.project}", data=body)

def projects_delete(args):
    require(args, "project", "projects delete")
    return get_client().delete(f"/v2/projects/{args.project}")


# ── API Keys ─────────────────────────────────────────────────────────────────

def api_keys_list(args):
    require(args, "project", "api-keys list")
    return get_client().get(f"/v2/projects/{args.project}/api-keys")

def api_keys_create(args):
    require(args, "project", "api-keys create")
    body: dict = {}
    if args.note:
        body["note"] = args.note
    return get_client().post(f"/v2/projects/{args.project}/api-keys", data=body)

def api_keys_delete(args):
    require(args, "project", "api-keys delete")
    require(args, "key", "api-keys delete")
    return get_client().delete(f"/v2/projects/{args.project}/api-keys/{args.key}")


# ── Organization ─────────────────────────────────────────────────────────────

def org_list_memberships(args):
    require(args, "org", "org list-memberships")
    return get_client().get(f"/v2/organizations/{args.org}/memberships")

def org_update_membership(args):
    require(args, "org", "org update-membership")
    require(args, "membership", "org update-membership")
    require(args, "role", "org update-membership")
    return get_client().put(f"/v2/organizations/{args.org}/memberships/{args.membership}", data={"role": args.role})

def org_delete_membership(args):
    require(args, "org", "org delete-membership")
    require(args, "membership", "org delete-membership")
    return get_client().delete(f"/v2/organizations/{args.org}/memberships/{args.membership}")

def org_list_projects(args):
    require(args, "org", "org list-projects")
    return get_client().get(f"/v2/organizations/{args.org}/projects")

def org_list_api_keys(args):
    require(args, "org", "org list-api-keys")
    return get_client().get(f"/v2/organizations/{args.org}/api-keys")


DISPATCH = {
    ("projects", "get"): projects_get,
    ("projects", "create"): projects_create,
    ("projects", "update"): projects_update,
    ("projects", "delete"): projects_delete,
    ("api-keys", "list"): api_keys_list,
    ("api-keys", "create"): api_keys_create,
    ("api-keys", "delete"): api_keys_delete,
    ("org", "list-memberships"): org_list_memberships,
    ("org", "update-membership"): org_update_membership,
    ("org", "delete-membership"): org_delete_membership,
    ("org", "list-projects"): org_list_projects,
    ("org", "list-api-keys"): org_list_api_keys,
}


def main():
    parser = argparse.ArgumentParser(description="Langfuse admin — projects, API keys, org")
    parser.add_argument("--resource", required=True, choices=RESOURCES)
    parser.add_argument("--action", required=True)
    parser.add_argument("--project", help="Project ID")
    parser.add_argument("--org", help="Organization ID")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--key", help="API key ID")
    parser.add_argument("--note", help="API key note")
    parser.add_argument("--membership", help="Membership ID")
    parser.add_argument("--role", choices=["OWNER", "ADMIN", "MEMBER", "VIEWER"])
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
