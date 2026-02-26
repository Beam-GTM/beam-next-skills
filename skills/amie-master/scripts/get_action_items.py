#!/usr/bin/env python3
"""
Get Amie Note Action Items

Retrieves action items extracted from a meeting note.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from amie_client import get_client


def get_action_items(note_id: str) -> dict:
    """
    Get action items for a specific note.

    Args:
        note_id: The ID of the note

    Returns:
        dict: Action items from the meeting
    """
    client = get_client()
    return client.get(f'/notes/{note_id}/action-items')


def main():
    parser = argparse.ArgumentParser(description="Get Amie note action items")
    parser.add_argument('--id', required=True, help='Note ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON (default)')
    args = parser.parse_args()

    try:
        result = get_action_items(args.id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
