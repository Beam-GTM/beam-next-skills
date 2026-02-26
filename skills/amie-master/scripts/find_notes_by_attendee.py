#!/usr/bin/env python3
"""Find Amie notes where a given attendee email (or domain) joined."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from amie_client import get_client
from list_notes import list_notes
from get_note import get_note


def main():
    parser = argparse.ArgumentParser(description="Find notes by attendee email or domain")
    parser.add_argument("attendee", help="Email or domain to search (e.g. bennet.adelhelm@adelhelm.de or adelhelm.de)")
    parser.add_argument("--limit", type=int, default=200, help="Max notes to scan (default 200)")
    parser.add_argument("--title-contains", type=str, help="Only consider notes whose title contains this (case-insensitive)")
    args = parser.parse_args()

    needle = args.attendee.lower()
    if "@" in needle:
        def matches(attendee_list):
            return any((a.get("email") or "").lower() == needle for a in attendee_list)
    else:
        def matches(attendee_list):
            return any(needle in (a.get("email") or "").lower() for a in attendee_list)

    client = get_client()
    result = list_notes(limit=args.limit)
    notes = result.get("data") or []
    # Pre-filter by title if requested (avoids fetching every note)
    if args.title_contains:
        notes = [n for n in notes if args.title_contains.lower() in ((n.get("title") or "").lower())]
    found = []

    for i, n in enumerate(notes):
        nid = n.get("id")
        title = (n.get("title") or "(no title)").strip()
        try:
            detail = get_note(nid)
            attendees = (detail.get("meeting") or {}).get("attendees") or []
            if matches(attendees):
                start = (detail.get("meeting") or {}).get("startAt") or ""
                found.append({
                    "id": nid,
                    "title": title,
                    "startAt": start,
                    "webUrl": detail.get("webUrl"),
                    "shortSummary": detail.get("shortSummary"),
                })
        except Exception as e:
            print(json.dumps({"error": str(e), "note_id": nid}), file=sys.stderr)

    print(json.dumps({"matches": found}, indent=2))


if __name__ == "__main__":
    main()
