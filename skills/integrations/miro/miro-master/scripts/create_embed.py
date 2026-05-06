#!/usr/bin/env python3
"""
Create Embed on Miro Board

Embed external content (URL) on a board.

Usage:
    python create_embed.py --board BOARD_ID --url "https://example.com" [--x 0] [--y 0] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def create_embed(board_id, url, x=0, y=0, width=None, height=None, mode='inline'):
    """Create an embed"""
    client = get_client()

    data = {
        'data': {'url': url, 'mode': mode},
        'position': {'x': x, 'y': y, 'origin': 'center'}
    }
    geometry = {}
    if width:
        geometry['width'] = width
    if height:
        geometry['height'] = height
    if geometry:
        data['geometry'] = geometry

    return client.post(f'boards/{encode_board_id(board_id)}/embeds', data)


def main():
    parser = argparse.ArgumentParser(description='Create embed on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--url', required=True, help='URL to embed')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, help='Width')
    parser.add_argument('--height', type=float, help='Height')
    parser.add_argument('--mode', default='inline', choices=['inline', 'modal'], help='Display mode')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_embed(args.board, args.url, x=args.x, y=args.y,
                           width=args.width, height=args.height, mode=args.mode)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Embed created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
