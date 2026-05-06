#!/usr/bin/env python3
"""
Get Miro Board Details

Get details of a specific board.

Usage:
    python get_board.py --board BOARD_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def get_board(board_id):
    """Get board details"""
    client = get_client()
    return client.get(f'boards/{encode_board_id(board_id)}')


def main():
    parser = argparse.ArgumentParser(description='Get Miro board details')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        board = get_board(args.board)

        if args.json:
            print(json.dumps({'success': True, 'board': board}, indent=2))
        else:
            print(f"\nBoard: {board.get('name', 'Untitled')}")
            print(f"  ID: {board.get('id')}")
            print(f"  Description: {board.get('description', 'None')}")
            print(f"  Created: {board.get('createdAt', '')[:10]}")
            print(f"  Modified: {board.get('modifiedAt', '')[:10]}")
            print(f"  Created by: {board.get('createdBy', {}).get('name', 'Unknown')}")
            print(f"  View link: {board.get('viewLink', 'N/A')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
