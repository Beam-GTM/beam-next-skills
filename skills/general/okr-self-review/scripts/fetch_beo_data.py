#!/usr/bin/env python3
"""
Fetch BEO progress and update data from Google Sheets.

Reads Progress_Log and Update_Log sheets from the BEO Google Sheet
and filters by user name and date range.

Usage:
    python3 fetch_beo_data.py --sheet-id <SHEET_ID> --name "Name" --start-date 2026-01-01 --end-date 2026-03-31 [--json]

Returns:
    Exit code 0 on success, 1 on error, 2 if no data found
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path


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


def setup_google_imports():
    """Set up sys.path for Google auth imports."""
    root = find_nexus_root()
    google_scripts = root / "00-system" / "skills" / "google" / "google-master" / "scripts"
    sheets_scripts = root / "00-system" / "skills" / "google" / "google-sheets" / "scripts"

    if str(google_scripts) not in sys.path:
        sys.path.insert(0, str(google_scripts))
    if str(sheets_scripts) not in sys.path:
        sys.path.insert(0, str(sheets_scripts))


def parse_timestamp(value):
    """Parse a timestamp string into a datetime, trying multiple formats."""
    if not value:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(str(value), fmt)
        except ValueError:
            continue

    return None


def fetch_progress_log(sheets_read_fn, sheet_id, name, start_date, end_date):
    """
    Fetch and filter Progress_Log data.

    Columns: Timestamp, SlackUserId, Name, OKR Text, OKR Database, Progress %, Notes, Week, Month
    """
    try:
        rows = sheets_read_fn(sheet_id, "Progress_Log!A:I")
    except Exception as e:
        print(f"[WARN] Could not read Progress_Log: {e}", file=sys.stderr)
        return []

    if not rows or len(rows) < 2:
        return []

    entries = []
    for row in rows[1:]:  # skip header
        if len(row) < 7:
            continue

        row_name = str(row[2]).strip() if len(row) > 2 else ""
        if row_name.lower() != name.lower():
            continue

        ts = parse_timestamp(row[0]) if row[0] else None
        if ts and start_date and ts < start_date:
            continue
        if ts and end_date and ts > end_date:
            continue

        entries.append({
            "timestamp": str(row[0]) if row[0] else "",
            "okr_text": str(row[3]) if len(row) > 3 else "",
            "okr_database": str(row[4]) if len(row) > 4 else "",
            "progress_pct": str(row[5]) if len(row) > 5 else "",
            "notes": str(row[6]) if len(row) > 6 else "",
            "week": str(row[7]) if len(row) > 7 else "",
            "month": str(row[8]) if len(row) > 8 else "",
        })

    return entries


def fetch_update_log(sheets_read_fn, sheet_id, name, start_date, end_date):
    """
    Fetch and filter Update_Log data.

    Columns: Timestamp, SlackUserId, Name, Email, Message, Week, Month
    """
    try:
        rows = sheets_read_fn(sheet_id, "Update_Log!A:G")
    except Exception as e:
        print(f"[WARN] Could not read Update_Log: {e}", file=sys.stderr)
        return []

    if not rows or len(rows) < 2:
        return []

    entries = []
    for row in rows[1:]:  # skip header
        if len(row) < 5:
            continue

        row_name = str(row[2]).strip() if len(row) > 2 else ""
        if row_name.lower() != name.lower():
            continue

        ts = parse_timestamp(row[0]) if row[0] else None
        if ts and start_date and ts < start_date:
            continue
        if ts and end_date and ts > end_date:
            continue

        entries.append({
            "timestamp": str(row[0]) if row[0] else "",
            "message": str(row[4]) if len(row) > 4 else "",
            "week": str(row[5]) if len(row) > 5 else "",
            "month": str(row[6]) if len(row) > 6 else "",
        })

    return entries


def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Fetch BEO progress and update data from Google Sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fetch_beo_data.py --sheet-id abc123 --name "Manahil Shaikh" --start-date 2026-01-01 --end-date 2026-03-31 --json
  python3 fetch_beo_data.py --sheet-id abc123 --name "Manahil Shaikh" --json
        """
    )
    parser.add_argument("--sheet-id", help="BEO Google Sheet ID (overrides .env BEO_SHEET_ID)")
    parser.add_argument("--name", required=True, help="User's name to filter by")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Resolve sheet ID
    root = find_nexus_root()
    env_vars = load_env_file(root / '.env')
    sheet_id = args.sheet_id or env_vars.get('BEO_SHEET_ID') or os.getenv('BEO_SHEET_ID')

    if not sheet_id:
        print("[ERROR] No sheet ID provided. Use --sheet-id or set BEO_SHEET_ID in .env", file=sys.stderr)
        sys.exit(1)

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59) if args.end_date else None

    # Import Google Sheets functions
    setup_google_imports()
    try:
        from sheets_operations import read_range
    except ImportError as e:
        print(f"[ERROR] Could not import Google Sheets operations: {e}", file=sys.stderr)
        print("[HINT] Ensure Google integration is configured. Run 'google-connect' skill.", file=sys.stderr)
        sys.exit(1)

    # Fetch data
    progress = fetch_progress_log(read_range, sheet_id, args.name, start_date, end_date)
    updates = fetch_update_log(read_range, sheet_id, args.name, start_date, end_date)

    result = {
        "name": args.name,
        "sheet_id": sheet_id,
        "period": {
            "start": args.start_date or "unspecified",
            "end": args.end_date or "unspecified"
        },
        "progress_log": progress,
        "update_log": updates,
        "progress_count": len(progress),
        "update_count": len(updates)
    }

    if len(progress) == 0 and len(updates) == 0:
        print(f"[INFO] No BEO data found for '{args.name}' in the specified period", file=sys.stderr)
        if args.json:
            print(json.dumps(result, indent=2))
        sys.exit(2)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"BEO data for {args.name}:\n")

        if progress:
            print(f"== Progress Log ({len(progress)} entries) ==")
            for entry in progress:
                print(f"  [{entry['timestamp']}] {entry['okr_text'][:60]}... -> {entry['progress_pct']}%")
                if entry['notes']:
                    print(f"    Notes: {entry['notes'][:80]}")
            print()

        if updates:
            print(f"== Update Log ({len(updates)} entries) ==")
            for entry in updates:
                print(f"  [{entry['timestamp']}] {entry['message'][:100]}")

    sys.exit(0)


if __name__ == "__main__":
    main()
