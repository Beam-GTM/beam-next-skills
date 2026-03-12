#!/usr/bin/env python3
"""
Create Shape on Miro Board

Usage:
    python create_shape.py --board BOARD_ID --content "Text" [--shape rectangle] [--x 0] [--y 0] [--width 200] [--height 200] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id

VALID_SHAPES = ['rectangle', 'round_rectangle', 'circle', 'triangle', 'rhombus',
                'parallelogram', 'trapezoid', 'pentagon', 'hexagon', 'octagon',
                'wedge_round_rectangle_callout', 'star', 'flow_chart_predefined_process',
                'cloud', 'cross', 'can', 'right_arrow', 'left_arrow',
                'left_right_arrow', 'left_brace', 'right_brace']


def create_shape(board_id, content='', shape='rectangle', x=0, y=0, width=200, height=200,
                 fill_color=None, border_color=None):
    """Create a shape"""
    client = get_client()

    data = {
        'data': {'content': content, 'shape': shape},
        'position': {'x': x, 'y': y, 'origin': 'center'},
        'geometry': {'width': width, 'height': height}
    }

    style = {}
    if fill_color:
        style['fillColor'] = fill_color
    if border_color:
        style['borderColor'] = border_color
    if style:
        data['style'] = style

    return client.post(f'boards/{encode_board_id(board_id)}/shapes', data)


def main():
    parser = argparse.ArgumentParser(description='Create shape on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--content', default='', help='Shape text (supports HTML)')
    parser.add_argument('--shape', default='rectangle', help=f'Shape type: {", ".join(VALID_SHAPES[:8])}...')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, default=200, help='Width')
    parser.add_argument('--height', type=float, default=200, help='Height')
    parser.add_argument('--fill-color', help='Fill color (hex, e.g. #FF0000)')
    parser.add_argument('--border-color', help='Border color (hex)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_shape(args.board, content=args.content, shape=args.shape,
                           x=args.x, y=args.y, width=args.width, height=args.height,
                           fill_color=args.fill_color, border_color=args.border_color)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Shape created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
