#!/usr/bin/env python3
"""
List Miro Boards

List all boards accessible to the authenticated user.

Usage:
    python list_boards.py [--limit 20] [--json]
    python list_boards.py --team TEAM_ID --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error


def list_boards(team_id=None, limit=20):
    """List boards"""
    client = get_client()

    params = {'limit': min(limit, 50)}
    if team_id:
        params['team_id'] = team_id

    if limit > 50:
        return client.paginate('boards', params, limit=limit)
    else:
        response = client.get('boards', params)
        return response.get('data', [])


def main():
    parser = argparse.ArgumentParser(description='List Miro boards')
    parser.add_argument('--team', help='Filter by team ID')
    parser.add_argument('--limit', type=int, default=20, help='Max boards to return')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        boards = list_boards(team_id=args.team, limit=args.limit)

        if args.json:
            print(json.dumps({
                'success': True,
                'count': len(boards),
                'boards': boards
            }, indent=2))
        else:
            if not boards:
                print("No boards found.")
                return

            print(f"\nFound {len(boards)} board(s):\n")
            for b in boards:
                name = b.get('name', 'Untitled')
                board_id = b.get('id', '')
                modified = b.get('modifiedAt', '')[:10]
                created_by = b.get('createdBy', {}).get('name', 'Unknown')
                print(f"  [{board_id}] {name}")
                print(f"    Created by: {created_by} | Modified: {modified}")
                print()

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
            if e.status_code:
                print(f"  {explain_error(e.status_code)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
