#!/usr/bin/env python3
"""
Manage Miro Board Tags

Create, list, attach, and remove tags on boards.

Usage:
    python tags.py --board BOARD_ID --list [--json]
    python tags.py --board BOARD_ID --create "Tag name" [--color red] [--json]
    python tags.py --board BOARD_ID --attach TAG_ID --item ITEM_ID [--json]
    python tags.py --board BOARD_ID --detach TAG_ID --item ITEM_ID [--json]
    python tags.py --board BOARD_ID --delete TAG_ID [--json]
    python tags.py --board BOARD_ID --items TAG_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id

VALID_COLORS = ['red', 'light_green', 'cyan', 'yellow', 'dark_green',
                'blue', 'dark_blue', 'violet', 'gray', 'black']


def list_tags(board_id, limit=50):
    client = get_client()
    response = client.get(f'boards/{encode_board_id(board_id)}/tags', {'limit': limit})
    return response.get('data', [])


def create_tag(board_id, title, fill_color='yellow'):
    client = get_client()
    data = {'title': title, 'fillColor': fill_color}
    return client.post(f'boards/{encode_board_id(board_id)}/tags', data)


def delete_tag(board_id, tag_id):
    client = get_client()
    return client.delete(f'boards/{encode_board_id(board_id)}/tags/{tag_id}')


def get_tag_items(board_id, tag_id, limit=50):
    client = get_client()
    response = client.get(f'boards/{encode_board_id(board_id)}/tags/{tag_id}/items', {'limit': limit})
    return response.get('data', [])


def attach_tag(board_id, item_id, tag_id):
    client = get_client()
    return client.post(f'boards/{encode_board_id(board_id)}/items/{item_id}/tags', {'id': tag_id})


def detach_tag(board_id, item_id, tag_id):
    client = get_client()
    return client.delete(f'boards/{encode_board_id(board_id)}/items/{item_id}/tags/{tag_id}')


def main():
    parser = argparse.ArgumentParser(description='Manage Miro board tags')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--list', action='store_true', help='List tags')
    parser.add_argument('--create', metavar='TITLE', help='Create tag with title')
    parser.add_argument('--delete', metavar='TAG_ID', help='Delete tag')
    parser.add_argument('--items', metavar='TAG_ID', help='List items with tag')
    parser.add_argument('--attach', metavar='TAG_ID', help='Attach tag to item')
    parser.add_argument('--detach', metavar='TAG_ID', help='Detach tag from item')
    parser.add_argument('--item', help='Item ID (for attach/detach)')
    parser.add_argument('--color', choices=VALID_COLORS, default='yellow', help='Tag color')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        if args.list:
            tags = list_tags(args.board)
            if args.json:
                print(json.dumps({'success': True, 'count': len(tags), 'tags': tags}, indent=2))
            else:
                for t in tags:
                    print(f"  [{t.get('id')}] {t.get('title')} ({t.get('fillColor')})")

        elif args.create:
            tag = create_tag(args.board, args.create, fill_color=args.color)
            if args.json:
                print(json.dumps({'success': True, 'tag': tag}, indent=2))
            else:
                print(f"Tag created: {tag.get('id')}")

        elif args.delete:
            delete_tag(args.board, args.delete)
            if args.json:
                print(json.dumps({'success': True, 'deleted': args.delete}, indent=2))
            else:
                print(f"Tag {args.delete} deleted.")

        elif args.items:
            items = get_tag_items(args.board, args.items)
            if args.json:
                print(json.dumps({'success': True, 'count': len(items), 'items': items}, indent=2))
            else:
                for i in items:
                    print(f"  [{i.get('id')}] {i.get('type')}")

        elif args.attach:
            if not args.item:
                parser.error("--item required for --attach")
            attach_tag(args.board, args.item, args.attach)
            if args.json:
                print(json.dumps({'success': True}, indent=2))
            else:
                print(f"Tag {args.attach} attached to item {args.item}")

        elif args.detach:
            if not args.item:
                parser.error("--item required for --detach")
            detach_tag(args.board, args.item, args.detach)
            if args.json:
                print(json.dumps({'success': True}, indent=2))
            else:
                print(f"Tag {args.detach} detached from item {args.item}")
        else:
            parser.print_help()

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
