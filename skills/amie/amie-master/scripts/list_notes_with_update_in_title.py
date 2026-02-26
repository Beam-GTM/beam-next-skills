#!/usr/bin/env python3
"""
Paginate through Amie notes and list those with 'update' in the title.
Optionally filter by attendee (e.g. adelhelm.de) by fetching note details (with rate-limit delay).
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from amie_client import get_client
from get_note import get_note


def main():
    parser = argparse.ArgumentParser(description="List notes with 'update' in title, optionally filter by attendee")
    parser.add_argument("--attendee", type=str, help="Only include notes where this email/domain attended (e.g. adelhelm.de)")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pagination pages (default 50, ~5000 notes)")
    parser.add_argument("--delay", type=float, default=1.2, help="Seconds between get_note calls to avoid rate limit (default 1.2)")
    args = parser.parse_args()

    client = get_client()
    all_update_notes = []
    cursor = None
    page = 0

    while page < args.max_pages:
        params = {"sort": "-createdAt", "limit": 100}
        if cursor:
            params["after"] = cursor
        try:
            if page > 0:
                time.sleep(1.5)  # avoid list endpoint rate limit when paginating
            resp = client.get("/notes", params=params)
        except Exception as e:
            print(json.dumps({"error": str(e)}), file=sys.stderr)
            break
        data = resp.get("data") or []
        pagination = resp.get("pagination") or {}
        for n in data:
            title = (n.get("title") or "") or ""
            if "update" in title.lower():
                all_update_notes.append(
                    {"id": n.get("id"), "title": title, "startAt": (n.get("meeting") or {}).get("startAt"), "webUrl": n.get("webUrl")}
                )
        cursor = pagination.get("cursor") if pagination.get("hasMore") else None
        page += 1
        if not cursor:
            break

    if not args.attendee:
        print(json.dumps({"notes_with_update_in_title": all_update_notes, "total": len(all_update_notes)}, indent=2))
        return

    # Filter by attendee: fetch each note and check attendees (with delay)
    needle = args.attendee.lower()
    matches = []
    for i, n in enumerate(all_update_notes):
        time.sleep(args.delay)
        try:
            detail = get_note(n["id"])
            attendees = (detail.get("meeting") or {}).get("attendees") or []
            emails = [a.get("email") or "" for a in attendees]
            if any(needle in e.lower() for e in emails):
                matches.append(
                    {
                        "id": n["id"],
                        "title": n["title"],
                        "startAt": n["startAt"],
                        "webUrl": n["webUrl"],
                        "shortSummary": detail.get("shortSummary"),
                    }
                )
        except Exception as e:
            print(json.dumps({"error": str(e), "note_id": n["id"]}), file=sys.stderr)
    print(json.dumps({"matches": matches, "total_update_notes_checked": len(all_update_notes)}, indent=2))


if __name__ == "__main__":
    main()
