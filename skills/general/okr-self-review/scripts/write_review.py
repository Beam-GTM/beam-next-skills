#!/usr/bin/env python3
"""
Write review data back to Notion database rows.

Pushes progress (checkin_6months) and self_rating back into
the Notion database after a review is generated.

Usage:
    python3 write_review.py --input review_updates.json [--dry-run]

Input JSON format:
    [
        {
            "page_id": "abc123-...",
            "text": "OKR title (for display only)",
            "updates": {
                "self_rating": {"value": "4", "prop_name": "Self Rating", "prop_type": "select"},
                "checkin_6months": {"value": "- Built X\n- Delivered Y", "prop_name": "Checkin Remarks (6months)", "prop_type": "rich_text"},
                "self_remarks": {"value": "Summary text", "prop_name": "Self Remarks", "prop_type": "rich_text"}
            }
        }
    ]

Returns:
    Exit code 0 on success, 1 on error
"""

import sys
import os
import json
import argparse
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


NOTION_VERSION = "2022-06-28"


def find_nexus_root():
    """Find Nexus root directory (contains CLAUDE.md)"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file and return as dict"""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")

    return env_vars


def build_property_value(prop_type, value):
    """Build a Notion API property value from type and value."""
    if prop_type == "rich_text":
        return {"rich_text": [{"text": {"content": str(value)}}]}
    elif prop_type == "select":
        return {"select": {"name": str(value)}}
    elif prop_type == "status":
        return {"status": {"name": str(value)}}
    elif prop_type == "number":
        return {"number": float(value) if value else None}
    elif prop_type == "checkbox":
        return {"checkbox": str(value).lower() in ("true", "yes", "1")}
    else:
        print(f"[WARN] Unsupported property type '{prop_type}', using rich_text", file=sys.stderr)
        return {"rich_text": [{"text": {"content": str(value)}}]}


def update_page(api_key, page_id, properties):
    """Update a Notion page's properties via PATCH."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    body = {"properties": properties}

    try:
        response = requests.patch(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return True, None
        elif response.status_code == 400:
            error_msg = response.json().get("message", response.text[:200])
            return False, f"400 Bad Request: {error_msg}"
        elif response.status_code == 401:
            return False, "401 Unauthorized - Invalid NOTION_API_KEY"
        elif response.status_code == 404:
            return False, f"404 Not Found - Page {page_id} not accessible"
        else:
            return False, f"{response.status_code}: {response.text[:200]}"

    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {e}"


def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Write review data back to Notion database rows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 write_review.py --input review_updates.json
  python3 write_review.py --input review_updates.json --dry-run
  echo '[...]' | python3 write_review.py --input -
        """
    )
    parser.add_argument("--input", required=True, help="JSON file with updates (use '-' for stdin)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")

    args = parser.parse_args()

    # Load API key
    root = find_nexus_root()
    env_vars = load_env_file(root / '.env')
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        sys.exit(1)

    # Load input JSON
    try:
        if args.input == '-':
            updates = json.load(sys.stdin)
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                updates = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[ERROR] Could not read input: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(updates, list):
        print("[ERROR] Input must be a JSON array of update objects", file=sys.stderr)
        sys.exit(1)

    # Process updates
    success_count = 0
    error_count = 0

    for item in updates:
        page_id = item.get("page_id")
        text = item.get("text", "Unknown")
        item_updates = item.get("updates", {})

        if not page_id:
            print(f"  [SKIP] No page_id for '{text}'", file=sys.stderr)
            error_count += 1
            continue

        if not item_updates:
            print(f"  [SKIP] No updates for '{text}'", file=sys.stderr)
            continue

        # Build Notion properties payload
        properties = {}
        for field_key, field_data in item_updates.items():
            prop_name = field_data.get("prop_name")
            prop_type = field_data.get("prop_type")
            value = field_data.get("value")

            if not prop_name or value is None:
                continue

            properties[prop_name] = build_property_value(prop_type, value)

        if not properties:
            print(f"  [SKIP] No valid properties for '{text}'")
            continue

        if args.dry_run:
            print(f"  [DRY RUN] {text}")
            for prop_name, prop_value in properties.items():
                display_val = str(prop_value)[:80]
                print(f"    -> {prop_name}: {display_val}")
            success_count += 1
            continue

        # Execute update
        ok, error = update_page(api_key, page_id, properties)
        if ok:
            print(f"  [OK] {text}")
            success_count += 1
        else:
            print(f"  [ERROR] {text}: {error}", file=sys.stderr)
            error_count += 1

    # Summary
    print(f"\nDone: {success_count} updated, {error_count} errors")

    if error_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
