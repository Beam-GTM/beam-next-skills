#!/usr/bin/env python3
"""
Create a default association between two HubSpot CRM records.

Uses the v4 batch default association API (primary / generic label for the pair).

Usage:
    python create_association.py --from-type TYPE --from-id ID --to-type TYPE --to-id ID [--json]

Examples:
    python create_association.py --from-type contacts --from-id 12345 --to-type companies --to-id 67890
    python create_association.py --from-type deals --from-id 111 --to-type contacts --to-id 222 --json
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import HubSpotError, get_client


def create_default_association(from_type: str, from_id: str, to_type: str, to_id: str):
    client = get_client()
    endpoint = f"/crm/v4/associations/{from_type}/{to_type}/batch/associate/default"
    body = {"inputs": [{"from": {"id": str(from_id)}, "to": {"id": str(to_id)}}]}
    return client.post(endpoint, data=body)


def main():
    parser = argparse.ArgumentParser(description="Create default HubSpot association (v4 batch)")
    parser.add_argument("--from-type", required=True, help="Source object type (e.g. contacts, deals)")
    parser.add_argument("--from-id", required=True, help="Source record ID")
    parser.add_argument("--to-type", required=True, help="Target object type (e.g. companies, contacts)")
    parser.add_argument("--to-id", required=True, help="Target record ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = create_default_association(
            args.from_type,
            args.from_id,
            args.to_type,
            args.to_id,
        )
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            status = result.get("status", "UNKNOWN")
            print(f"Association request status: {status}")
            if result.get("results"):
                for r in result["results"]:
                    print(f"  from={r.get('from', {}).get('id')} to={r.get('to', {}).get('id')}")
    except HubSpotError as e:
        if args.json:
            print(json.dumps({"error": True, "status_code": e.status_code, "message": e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
