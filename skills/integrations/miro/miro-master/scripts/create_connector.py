#!/usr/bin/env python3
"""
Create Connector on Miro Board

Connect two items with a line/arrow.

Usage:
    python create_connector.py --board BOARD_ID --start-item ITEM_ID --end-item ITEM_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id

VALID_STROKE_STYLES = ['normal', 'dotted', 'dashed']
VALID_SHAPES = ['straight', 'elbowed', 'curved']


def create_connector(board_id, start_item_id, end_item_id, shape='curved',
                     stroke_style='normal', stroke_color=None, caption=None):
    """Create a connector between two items"""
    client = get_client()

    data = {
        'startItem': {'id': start_item_id},
        'endItem': {'id': end_item_id},
        'shape': shape
    }

    style = {}
    if stroke_style:
        style['strokeStyle'] = stroke_style
    if stroke_color:
        style['strokeColor'] = stroke_color
    if style:
        data['style'] = style

    if caption:
        data['captions'] = [{'content': caption}]

    return client.post(f'boards/{encode_board_id(board_id)}/connectors', data)


def list_connectors(board_id, limit=50):
    """List connectors on a board"""
    client = get_client()
    params = {'limit': min(limit, 50)}
    response = client.get(f'boards/{encode_board_id(board_id)}/connectors', params)
    return response.get('data', [])


def main():
    parser = argparse.ArgumentParser(description='Create connector on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--start-item', help='Start item ID')
    parser.add_argument('--end-item', help='End item ID')
    parser.add_argument('--shape', default='curved', choices=VALID_SHAPES, help='Connector shape')
    parser.add_argument('--stroke-style', default='normal', choices=VALID_STROKE_STYLES)
    parser.add_argument('--stroke-color', help='Stroke color (hex)')
    parser.add_argument('--caption', help='Connector label text')
    parser.add_argument('--list', action='store_true', help='List connectors instead of creating')
    parser.add_argument('--limit', type=int, default=50, help='Max connectors to list')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        if args.list:
            connectors = list_connectors(args.board, limit=args.limit)
            if args.json:
                print(json.dumps({'success': True, 'count': len(connectors), 'connectors': connectors}, indent=2))
            else:
                print(f"Found {len(connectors)} connector(s)")
                for c in connectors:
                    start = c.get('startItem', {}).get('id', '?')
                    end = c.get('endItem', {}).get('id', '?')
                    print(f"  [{c.get('id')}] {start} -> {end}")
        else:
            if not args.start_item or not args.end_item:
                parser.error("--start-item and --end-item required when creating")

            item = create_connector(args.board, args.start_item, args.end_item,
                                   shape=args.shape, stroke_style=args.stroke_style,
                                   stroke_color=args.stroke_color, caption=args.caption)
            if args.json:
                print(json.dumps({'success': True, 'connector': item}, indent=2))
            else:
                print(f"Connector created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
