#!/usr/bin/env python3
"""
Delete (archive) a HubSpot CRM record by object type and ID.

Uses DELETE /crm/v3/objects/{objectType}/{objectId} — archives the record by default.

Usage:
    python delete_crm_object.py --object-type TYPE --id ID --yes [--json]

Examples:
    python delete_crm_object.py --object-type contacts --id 12345 --yes
    python delete_crm_object.py --object-type deals --id 67890 --yes --json
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import HubSpotError, get_client


def delete_object(object_type: str, object_id: str):
    client = get_client()
    return client.delete(f"/crm/v3/objects/{object_type}/{object_id}")


def main():
    parser = argparse.ArgumentParser(description="Delete (archive) a HubSpot CRM record")
    parser.add_argument("--object-type", required=True, help="Object type (contacts, companies, deals, …)")
    parser.add_argument("--id", required=True, dest="object_id", help="Record ID to delete")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Required confirmation flag (destructive operation)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not args.yes:
        print(
            "ERROR: Refusing to delete without --yes. Example:\n"
            f"  uv run python delete_crm_object.py --object-type contacts --id {args.object_id} --yes",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        result = delete_object(args.object_type, args.object_id)
        if args.json:
            print(json.dumps(result if result else {"status": "deleted"}, indent=2))
        else:
            print(f"Deleted (archived) {args.object_type}:{args.object_id}")
    except HubSpotError as e:
        if args.json:
            print(json.dumps({"error": True, "status_code": e.status_code, "message": e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
