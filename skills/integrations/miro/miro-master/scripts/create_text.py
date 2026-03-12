#!/usr/bin/env python3
"""
Create Text Item on Miro Board

Usage:
    python create_text.py --board BOARD_ID --content "Text here" [--x 0] [--y 0] [--font-size 14] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def create_text(board_id, content, x=0, y=0, width=None, font_size=None, color=None):
    """Create a text item"""
    client = get_client()

    data = {
        'data': {'content': content},
        'position': {'x': x, 'y': y, 'origin': 'center'}
    }

    style = {}
    if font_size:
        style['fontSize'] = str(font_size)
    if color:
        style['color'] = color
    if style:
        data['style'] = style

    if width:
        data['geometry'] = {'width': width}

    return client.post(f'boards/{encode_board_id(board_id)}/texts', data)


def main():
    parser = argparse.ArgumentParser(description='Create text on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--content', required=True, help='Text content (supports HTML)')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, help='Width')
    parser.add_argument('--font-size', type=int, help='Font size (10-288)')
    parser.add_argument('--color', help='Text color (hex)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_text(args.board, args.content, x=args.x, y=args.y,
                          width=args.width, font_size=args.font_size, color=args.color)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Text created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
