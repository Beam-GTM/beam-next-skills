#!/usr/bin/env python3
"""
Manage Miro Board Members

List, add, update, or remove board members.

Usage:
    python board_members.py --board BOARD_ID --list [--json]
    python board_members.py --board BOARD_ID --add EMAIL --role viewer [--json]
    python board_members.py --board BOARD_ID --update MEMBER_ID --role commenter [--json]
    python board_members.py --board BOARD_ID --remove MEMBER_ID [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from miro_client import get_client, MiroAPIError, explain_error, encode_board_id

VALID_ROLES = ['viewer', 'commenter', 'editor', 'coowner', 'owner', 'guest']


def list_members(board_id, limit=50):
    """List board members"""
    client = get_client()
    params = {'limit': min(limit, 50)}
    response = client.get(f'boards/{encode_board_id(board_id)}/members', params)
    return response.get('data', [])


def add_member(board_id, email, role='viewer'):
    """Add member to board"""
    client = get_client()
    data = {'emails': [email], 'role': role}
    return client.post(f'boards/{encode_board_id(board_id)}/members', data)


def update_member(board_id, member_id, role):
    """Update member role"""
    client = get_client()
    data = {'role': role}
    return client.patch(f'boards/{encode_board_id(board_id)}/members/{member_id}', data)


def remove_member(board_id, member_id):
    """Remove member from board"""
    client = get_client()
    return client.delete(f'boards/{encode_board_id(board_id)}/members/{member_id}')


def main():
    parser = argparse.ArgumentParser(description='Manage Miro board members')
    parser.add_argument('--board', required=True, help='Board ID')
    parser.add_argument('--list', action='store_true', help='List members')
    parser.add_argument('--add', metavar='EMAIL', help='Add member by email')
    parser.add_argument('--update', metavar='MEMBER_ID', help='Update member')
    parser.add_argument('--remove', metavar='MEMBER_ID', help='Remove member')
    parser.add_argument('--role', choices=VALID_ROLES, default='viewer', help='Member role')
    parser.add_argument('--limit', type=int, default=50, help='Max members to list')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    try:
        if args.list:
            members = list_members(args.board, limit=args.limit)
            if args.json:
                print(json.dumps({'success': True, 'count': len(members), 'members': members}, indent=2))
            else:
                print(f"\nBoard members ({len(members)}):\n")
                for m in members:
                    name = m.get('name', 'Unknown')
                    role = m.get('role', 'unknown')
                    mid = m.get('id', '')
                    print(f"  [{mid}] {name} ({role})")

        elif args.add:
            result = add_member(args.board, args.add, role=args.role)
            if args.json:
                print(json.dumps({'success': True, 'result': result}, indent=2))
            else:
                print(f"Invited {args.add} as {args.role}")

        elif args.update:
            result = update_member(args.board, args.update, role=args.role)
            if args.json:
                print(json.dumps({'success': True, 'result': result}, indent=2))
            else:
                print(f"Updated member {args.update} to {args.role}")

        elif args.remove:
            remove_member(args.board, args.remove)
            if args.json:
                print(json.dumps({'success': True, 'removed': args.remove}, indent=2))
            else:
                print(f"Removed member {args.remove}")
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
