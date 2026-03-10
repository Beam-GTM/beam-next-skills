#!/usr/bin/env python3
"""
Fetch all performance review data from a user's Notion page.

Reads all 5 child databases: Functional OKRs, AI Native OKRs,
Key Projects, Functional Skills, and Core Behaviours.

Usage:
    python3 fetch_okrs.py --page-id <NOTION_PAGE_ID> [--quarter Q1] [--year 2026] [--include-done] [--json]

Returns:
    Exit code 0 on success, 1 on error, 2 if no data found
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
ALL_DATABASE_NAMES = [
    "Functional OKRs", "AI Native OKRs",
    "Key Projects", "Functional Skills", "Core Behaviours"
]
EXCLUDED_STATUSES = ["stopped", "cancelled"]


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


def notion_request(api_key, method, url, body=None):
    """Make an authenticated Notion API request."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    try:
        if method.lower() == "get":
            response = requests.get(url, headers=headers, timeout=30)
        elif method.lower() == "post":
            response = requests.post(url, headers=headers, json=body or {}, timeout=30)
        else:
            print(f"[ERROR] Unsupported method: {method}", file=sys.stderr)
            return None

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid NOTION_API_KEY", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] 404 Not Found - Check the page ID", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Notion API error {response.status_code}: {response.text[:200]}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def extract_text_from_property(prop):
    """
    Extract plain text from a Notion property value.
    Mirrors extractTextFromProperty_() from beo-v2.gs.
    """
    if not prop:
        return ""

    prop_type = prop.get("type", "")

    if prop_type == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    elif prop_type == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    elif prop_type == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    elif prop_type == "status":
        st = prop.get("status")
        return st.get("name", "") if st else ""
    elif prop_type == "multi_select":
        return ", ".join(m.get("name", "") for m in prop.get("multi_select", []))
    elif prop_type == "number":
        num = prop.get("number")
        return str(num) if num is not None else ""

    return ""


def get_page_children(api_key, page_id):
    """Fetch all child blocks of a Notion page."""
    all_blocks = []
    cursor = None

    while True:
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        if cursor:
            url += f"?start_cursor={cursor}"

        result = notion_request(api_key, "get", url)
        if not result:
            break

        all_blocks.extend(result.get("results", []))

        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    return all_blocks


def find_databases(blocks, db_names=None):
    """
    Find child_database blocks matching expected database names.
    Uses stripped comparison to handle trailing whitespace in Notion titles.
    Returns list of {id, title} dicts.
    """
    if db_names is None:
        db_names = ALL_DATABASE_NAMES

    db_names_stripped = [n.strip() for n in db_names]

    databases = []
    for block in blocks:
        if block.get("type") != "child_database":
            continue
        title = block.get("child_database", {}).get("title", "Untitled")
        if title.strip() in db_names_stripped:
            databases.append({"id": block["id"], "title": title.strip()})

    return databases


def query_database(api_key, database_id):
    """Query all rows from a Notion database."""
    all_rows = []
    cursor = None

    while True:
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        body = {}
        if cursor:
            body["start_cursor"] = cursor

        result = notion_request(api_key, "post", url, body)
        if not result:
            break

        all_rows.extend(result.get("results", []))

        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    return all_rows


def extract_rows_from_database(rows, database_name, include_done=False):
    """
    Extract structured data from database rows.
    Handles all 5 database types by reading all properties generically.
    """
    entries = []

    for row in rows:
        properties = row.get("properties", {})
        entry = {"database": database_name, "page_id": row.get("id", "")}

        # Track actual Notion property names and types for write-back
        prop_map = {}

        # Extract all properties into the entry
        title_text = ""
        for prop_name, prop_value in properties.items():
            text = extract_text_from_property(prop_value)
            lower = prop_name.lower()
            prop_type = prop_value.get("type", "")

            # Identify the title/name field (varies by database)
            if prop_type == "title":
                title_text = text
                entry["text"] = text
            elif "status" in lower and prop_type in ("status", "select"):
                entry["status"] = text
                prop_map["status"] = {"name": prop_name, "type": prop_type}
            elif "quarter" in lower:
                entry["quarter"] = text
            elif "year" in lower:
                entry["year"] = text
            elif "self rating" in lower or "self_rating" in lower:
                entry["self_rating"] = text
                prop_map["self_rating"] = {"name": prop_name, "type": prop_type}
            elif "lead" in lower and "rating" in lower:
                entry["lead_rating"] = text
                prop_map["lead_rating"] = {"name": prop_name, "type": prop_type}
            elif "cadence" in lower:
                entry["cadence"] = text
            elif "checkin" in lower and "6" in lower:
                entry["checkin_6months"] = text
                prop_map["checkin_6months"] = {"name": prop_name, "type": prop_type}
            elif "checkin" in lower and "3" in lower:
                entry["checkin_3months"] = text
                prop_map["checkin_3months"] = {"name": prop_name, "type": prop_type}
            elif "self remark" in lower or "self_remark" in lower:
                entry["self_remarks"] = text
                prop_map["self_remarks"] = {"name": prop_name, "type": prop_type}
            elif "lead" in lower and "remark" in lower:
                entry["lead_remarks"] = text

        entry["_prop_map"] = prop_map

        if not title_text or not title_text.strip():
            continue

        status = entry.get("status", "").lower()
        if status in EXCLUDED_STATUSES:
            continue
        if not include_done and status == "done":
            continue

        entries.append(entry)

    return entries


def fetch_all_data(api_key, page_id, filter_quarter=None, filter_year=None, include_done=False):
    """
    Main fetch function: get all performance review data from a user's Notion page.
    Reads all 5 databases: Functional OKRs, AI Native OKRs, Key Projects,
    Functional Skills, Core Behaviours.
    """
    # Step 1: Get page children
    blocks = get_page_children(api_key, page_id)
    if not blocks:
        print("[ERROR] No blocks found on page (page may be empty or inaccessible)", file=sys.stderr)
        return None

    # Step 2: Find all databases
    databases = find_databases(blocks)
    if not databases:
        found_dbs = [
            b.get("child_database", {}).get("title", "Untitled")
            for b in blocks if b.get("type") == "child_database"
        ]
        print(f"[ERROR] No matching databases found. Expected: {ALL_DATABASE_NAMES}", file=sys.stderr)
        if found_dbs:
            print(f"[INFO] Child databases found: {found_dbs}", file=sys.stderr)
        return None

    # Step 3: Query each database
    result = {
        "functional_okrs": [],
        "ai_native_okrs": [],
        "key_projects": [],
        "functional_skills": [],
        "core_behaviours": [],
        "databases_found": [db["title"] for db in databases]
    }

    db_key_map = {
        "Functional OKRs": "functional_okrs",
        "AI Native OKRs": "ai_native_okrs",
        "Key Projects": "key_projects",
        "Functional Skills": "functional_skills",
        "Core Behaviours": "core_behaviours",
    }

    for db in databases:
        rows = query_database(api_key, db["id"])
        entries = extract_rows_from_database(rows, db["title"], include_done=include_done)

        # Apply quarter/year filter for OKR and project databases
        if filter_quarter or filter_year:
            if db["title"] in ("Functional OKRs", "AI Native OKRs", "Key Projects"):
                filtered = []
                for e in entries:
                    if filter_quarter and e.get("quarter") and filter_quarter.upper() not in e["quarter"].upper():
                        continue
                    if filter_year and e.get("year") and filter_year not in e["year"]:
                        continue
                    filtered.append(e)
                entries = filtered

        key = db_key_map.get(db["title"])
        if key:
            result[key].extend(entries)

    # Add counts
    result["total_okrs"] = len(result["functional_okrs"]) + len(result["ai_native_okrs"])
    result["functional_count"] = len(result["functional_okrs"])
    result["ai_native_count"] = len(result["ai_native_okrs"])
    result["projects_count"] = len(result["key_projects"])
    result["skills_count"] = len(result["functional_skills"])
    result["behaviours_count"] = len(result["core_behaviours"])

    return result


def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Fetch all performance review data from a Notion page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fetch_okrs.py --page-id abc123 --include-done --json
  python3 fetch_okrs.py --page-id abc123 --quarter Q1 --year 2026 --include-done --json
        """
    )
    parser.add_argument("--page-id", required=True, help="Notion page ID containing review databases")
    parser.add_argument("--quarter", help="Filter OKRs/projects by quarter (e.g., Q1, Q2)")
    parser.add_argument("--year", help="Filter OKRs/projects by year (e.g., 2026)")
    parser.add_argument("--include-done", action="store_true", help="Include items with 'Done' status (needed for reviews)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (default: formatted text)")

    args = parser.parse_args()

    # Load API key
    root = find_nexus_root()
    env_vars = load_env_file(root / '.env')
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        sys.exit(1)

    # Fetch all data
    result = fetch_all_data(api_key, args.page_id, args.quarter, args.year, include_done=args.include_done)

    if result is None:
        sys.exit(1)

    total = result["total_okrs"] + result["projects_count"] + result["skills_count"] + result["behaviours_count"]
    if total == 0:
        print("[INFO] No data found on page", file=sys.stderr)
        if args.json:
            print(json.dumps(result, indent=2))
        sys.exit(2)

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Databases found: {', '.join(result['databases_found'])}\n")

        for section, key, label in [
            ("Functional OKRs", "functional_okrs", "text"),
            ("AI Native OKRs", "ai_native_okrs", "text"),
            ("Key Projects", "key_projects", "text"),
            ("Functional Skills", "functional_skills", "text"),
            ("Core Behaviours", "core_behaviours", "text"),
        ]:
            items = result.get(key, [])
            if items:
                print(f"== {section} ({len(items)}) ==")
                for i, item in enumerate(items, 1):
                    status_str = f" [{item.get('status', '')}]" if item.get("status") else ""
                    rating_str = f" | Self: {item['self_rating']}" if item.get("self_rating") else ""
                    print(f"  {i}. {item.get('text', '?')}{status_str}{rating_str}")
                print()

    sys.exit(0)


if __name__ == "__main__":
    main()
