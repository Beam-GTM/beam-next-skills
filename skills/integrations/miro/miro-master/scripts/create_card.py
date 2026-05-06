#!/usr/bin/env python3
"""
Create Card on Miro Board

Usage:
    python create_card.py --board BOARD_ID --title "Card title" [--description "desc"] [--x 0] [--y 0] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id


def create_card(board_id, title, description=None, due_date=None, assignee_id=None, x=0, y=0):
    """Create a card"""
    client = get_client()

    card_data = {'title': title}
    if description:
        card_data['description'] = description
    if due_date:
        card_data['dueDate'] = due_date
    if assignee_id:
        card_data['assigneeId'] = assignee_id

    data = {
        'data': card_data,
        'position': {'x': x, 'y': y, 'origin': 'center'}
    }

    return client.post(f'boards/{encode_board_id(board_id)}/cards', data)


def main():
    parser = argparse.ArgumentParser(description='Create card on Miro board')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--title', required=True, help='Card title')
    parser.add_argument('--description', help='Card description')
    parser.add_argument('--due-date', help='Due date (ISO 8601)')
    parser.add_argument('--assignee', help='Assignee user ID')
    parser.add_argument('--x', type=float, default=0, help='X position')
    parser.add_argument('--y', type=float, default=0, help='Y position')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        item = create_card(args.board, args.title, description=args.description,
                          due_date=args.due_date, assignee_id=args.assignee,
                          x=args.x, y=args.y)

        if args.json:
            print(json.dumps({'success': True, 'item': item}, indent=2))
        else:
            print(f"Card created: {item.get('id')}")

    except MiroAPIError as e:
        if args.json:
            print(json.dumps({'success': False, **e.to_dict()}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
