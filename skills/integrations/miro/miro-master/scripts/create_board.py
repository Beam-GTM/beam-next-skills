#!/usr/bin/env python3
"""
Create Miro Board

Create a new board.

Usage:
    python create_board.py --name "My Board" [--description "Board desc"] [--team TEAM_ID] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error


def create_board(name, description=None, team_id=None):
    """Create a new board"""
    client = get_client()

    data = {'name': name}
    if description:
        data['description'] = description
    if team_id:
        data['teamId'] = team_id

    return client.post('boards', data)


def main():
    parser = argparse.ArgumentParser(description='Create a Miro board')
    parser.add_argument('--name', required=True, help='Board name')
    parser.add_argument('--description', help='Board description')
    parser.add_argument('--team', help='Team ID')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        board = create_board(args.name, description=args.description, team_id=args.team)

        if args.json:
            print(json.dumps({'success': True, 'board': board}, indent=2))
        else:
            print(f"\nBoard created: {board.get('name')}")
            print(f"  ID: {board.get('id')}")
            print(f"  View: {board.get('viewLink', 'N/A')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
