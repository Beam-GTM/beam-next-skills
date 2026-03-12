#!/usr/bin/env python3
"""
Create Frame on Miro Board

Usage:
    python create_frame.py --board BOARD_ID --title "Frame title" [--x 0] [--y 0] [--width 800] [--height 600] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def create_frame(board_id, title='', x=0, y=0, width=800, height=600, fill_color=None):
    """Create a frame"""
    client = get_client()

    data = {
        'data': {'title': title, 'format': 'custom'},
        'position': {'x': x, 'y': y, 'origin': 'center'},
        'geometry': {'width': width, 'height': height}
    }

    style = {}
    if fill_color:
        style['fillColor'] = fill_color
    if style:
        data['style'] = style

    return client.post(f'boards/{encode_board_id(board_id)}/frames', data)


def get_frame_items(board_id, frame_id, limit=50):
    """Get items within a frame"""
    client = get_client()
    params = {'limit': min(limit, 50)}
    response = client.get(f'boards/{encode_board_id(board_id)}/frames/{frame_id}/items', params)
    return response.get('data', [])


def main():
    parser = argparse.ArgumentParser(description='Create frame on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--title', default='', help='Frame title')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, default=800, help='Width')
    parser.add_argument('--height', type=float, default=600, help='Height')
    parser.add_argument('--fill-color', help='Fill color (hex)')
    parser.add_argument('--list-items', help='List items in frame ID instead of creating')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        if args.list_items:
            items = get_frame_items(args.board, args.list_items)
            if args.json:
                print(json.dumps({'success': True, 'count': len(items), 'items': items}, indent=2))
            else:
                print(f"Found {len(items)} items in frame")
                for item in items:
                    print(f"  [{item.get('id')}] {item.get('type')}")
        else:
            item = create_frame(args.board, title=args.title, x=args.x, y=args.y,
                               width=args.width, height=args.height, fill_color=args.fill_color)
            if args.json:
                print(json.dumps({'success': True, 'item': item}, indent=2))
            else:
                print(f"Frame created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
