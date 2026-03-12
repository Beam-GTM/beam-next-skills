#!/usr/bin/env python3
"""
Create Image on Miro Board

Add an image from URL.

Usage:
    python create_image.py --board BOARD_ID --url "https://example.com/image.png" [--title "Image"] [--x 0] [--y 0] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def create_image(board_id, url, title=None, x=0, y=0, width=None):
    """Create an image from URL"""
    client = get_client()

    data = {
        'data': {'url': url},
        'position': {'x': x, 'y': y, 'origin': 'center'}
    }
    if title:
        data['data']['title'] = title
    if width:
        data['geometry'] = {'width': width}

    return client.post(f'boards/{encode_board_id(board_id)}/images', data)


def main():
    parser = argparse.ArgumentParser(description='Create image on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--url', required=True, help='Image URL')
    parser.add_argument('--title', help='Image title')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--width', type=float, help='Width')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_image(args.board, args.url, title=args.title,
                           x=args.x, y=args.y, width=args.width)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Image created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
