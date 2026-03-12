#!/usr/bin/env python3
"""
List Items on a Miro Board

Get all items on a board (any type).

Usage:
    python list_items.py --board BOARD_ID [--type sticky_note] [--limit 50] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def list_items(board_id, item_type=None, limit=50):
    """List items on a board"""
    client = get_client()

    params = {'limit': min(limit, 50)}
    if item_type:
        params['type'] = item_type

    if limit > 50:
        return client.paginate(f'boards/{encode_board_id(board_id)}/items', params, limit=limit)
    else:
        response = client.get(f'boards/{encode_board_id(board_id)}/items', params)
        return response.get('data', [])


def main():
    parser = argparse.ArgumentParser(description='List items on a Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--type', help='Filter by type (sticky_note, card, shape, text, frame, image, document, embed, connector)')
    parser.add_argument('--limit', type=int, default=50, help='Max items')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        items = list_items(args.board, item_type=args.type, limit=args.limit)

        if args.json:
            print(json.dumps({
                'success': True,
                'board_id': args.board,
                'count': len(items),
                'items': items
            }, indent=2))
        else:
            if not items:
                print("No items found.")
                return

            print(f"\nFound {len(items)} item(s):\n")
            for item in items:
                item_type = item.get('type', 'unknown')
                item_id = item.get('id', '')
                content = ''
                if 'data' in item:
                    content = item['data'].get('content', item['data'].get('title', ''))
                content_preview = content[:60] + '...' if len(content) > 60 else content
                print(f"  [{item_id}] {item_type}: {content_preview}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
