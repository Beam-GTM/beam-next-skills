#!/usr/bin/env python3
"""
List Amie Notes

Retrieves all meeting notes from Amie.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from amie_client import get_client


def list_notes(limit: int = None, sort: str = "-createdAt") -> dict:
    """
    List all notes from Amie.

    Args:
        limit: Maximum number of notes to return (optional)
        sort: Sort order (default: -createdAt for newest first, createdAt for oldest first)

    Returns:
        dict: API response with notes list
    """
    client = get_client()
    params = {'sort': sort}
    if limit:
        params['limit'] = limit
    
    return client.get('/notes', params=params)


def main():
    parser = argparse.ArgumentParser(description="List Amie notes")
    parser.add_argument('--limit', type=int, help='Maximum number of notes')
    parser.add_argument('--sort', default='-createdAt', help='Sort order (default: -createdAt for newest first)')
    parser.add_argument('--json', action='store_true', help='Output as JSON (default)')
    args = parser.parse_args()

    try:
        result = list_notes(limit=args.limit, sort=args.sort)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
