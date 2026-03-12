#!/usr/bin/env python3
"""
Create Sticky Note on Miro Board

Usage:
    python create_sticky_note.py --board BOARD_ID --content "Note text" [--color yellow] [--x 0] [--y 0] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id

VALID_COLORS = ['gray', 'light_yellow', 'yellow', 'orange', 'light_green', 'green',
                'dark_green', 'cyan', 'light_pink', 'pink', 'violet', 'red',
                'light_blue', 'blue', 'dark_blue', 'black']


def create_sticky_note(board_id, content, color='yellow', x=0, y=0, width=None):
    """Create a sticky note"""
    client = get_client()

    data = {
        'data': {'content': content, 'shape': 'square'},
        'position': {'x': x, 'y': y, 'origin': 'center'}
    }
    if color:
        data['style'] = {'fillColor': color}
    if width:
        data['geometry'] = {'width': width}

    return client.post(f'boards/{encode_board_id(board_id)}/sticky_notes', data)


def main():
    parser = argparse.ArgumentParser(description='Create sticky note on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--content', required=True, help='Note text (supports HTML)')
    parser.add_argument('--color', default='yellow', choices=VALID_COLORS, help='Note color')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, help='Width in pixels')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_sticky_note(args.board, args.content, color=args.color,
                                  x=args.x, y=args.y, width=args.width)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Sticky note created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
