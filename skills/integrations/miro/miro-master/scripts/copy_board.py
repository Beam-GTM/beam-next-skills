#!/usr/bin/env python3
"""
Copy Miro Board

Create a copy of an existing board.

Usage:
    python copy_board.py --board BOARD_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def copy_board(board_id):
    """Copy a board"""
    client = get_client()
    return client.put(f'boards/{encode_board_id(board_id)}/copy')


def main():
    parser = argparse.ArgumentParser(description='Copy a Miro board')
    parser.add_argument('--board', required=True, help='Board ID to copy')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        board = copy_board(args.board)

        if args.json:
            print(json.dumps({'success': True, 'board': board}, indent=2))
        else:
            print(f"\nBoard copied: {board.get('name', 'Copy')}")
            print(f"  New ID: {board.get('id')}")
            print(f"  View: {board.get('viewLink', 'N/A')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
