#!/usr/bin/env python3
"""
Delete Miro Board

Delete a board by ID.

Usage:
    python delete_board.py --board BOARD_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def delete_board(board_id):
    """Delete a board"""
    client = get_client()
    return client.delete(f'boards/{encode_board_id(board_id)}')


def main():
    parser = argparse.ArgumentParser(description='Delete a Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        result = delete_board(args.board)

        if args.json:
            print(json.dumps({'success': True, 'board_id': args.board}, indent=2))
        else:
            print(f"Board {args.board} deleted.")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
