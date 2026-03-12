#!/usr/bin/env python3
"""
Update or Delete Item on Miro Board

Generic update/delete for any item type. For type-specific updates,
use the dedicated scripts.

Usage:
    python update_item.py --board BOARD_ID --item ITEM_ID [--x 100] [--y 200] [--json]
    python update_item.py --board BOARD_ID --item ITEM_ID --delete [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def get_item(board_id, item_id):
    """Get item details"""
    client = get_client()
    return client.get(f'boards/{encode_board_id(board_id)}/items/{item_id}')


def update_item(board_id, item_id, x=None, y=None, parent_id=None):
    """Update item position or parent"""
    client = get_client()

    data = {}
    position = {}
    if x is not None:
        position['x'] = x
    if y is not None:
        position['y'] = y
    if position:
        position['origin'] = 'center'
        data['position'] = position

    if parent_id:
        data['parent'] = {'id': parent_id}

    return client.patch(f'boards/{encode_board_id(board_id)}/items/{item_id}', data)


def delete_item(board_id, item_id):
    """Delete an item"""
    client = get_client()
    return client.delete(f'boards/{encode_board_id(board_id)}/items/{item_id}')


def main():
    parser = argparse.ArgumentParser(description='Update or delete item on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--item', required=True, help='Item ID')
    parser.add_argument('--x', type=float, help='New X position')
    parser.add_argument('--y', type=float, help='New Y position')
    parser.add_argument('--parent', help='Parent frame ID')
    parser.add_argument('--delete', action='store_true', help='Delete the item')
    parser.add_argument('--get', action='store_true', help='Get item details')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        if args.delete:
            delete_item(args.board, args.item)
            if args.json:
                print(json.dumps({'success': True, 'deleted': args.item}, indent=2))
            else:
                print(f"Item {args.item} deleted.")
        elif args.get:
            item = get_item(args.board, args.item)
            if args.json:
                print(json.dumps({'success': True, 'item': item}, indent=2))
            else:
                print(json.dumps(item, indent=2))
        else:
            item = update_item(args.board, args.item, x=args.x, y=args.y, parent_id=args.parent)
            if args.json:
                print(json.dumps({'success': True, 'item': item}, indent=2))
            else:
                print(f"Item {args.item} updated.")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
