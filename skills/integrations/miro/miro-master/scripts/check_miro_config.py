#!/usr/bin/env python3
"""
Check Miro Configuration

Validate that Miro API credentials are configured and working.

Usage:
    python check_miro_config.py [--json]
"""

import sys
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

ENV_FILE = SCRIPT_DIR.parent.parent.parent.parent.parent / ".env"


def check_config():
    """Check Miro configuration"""
    result = {
        'status': 'not_configured',
        'exit_code': 2,
        'ai_action': 'add_access_token',
        'missing': [],
        'found': []
    }

    # Check .env for token
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')

    token = env_vars.get('MIRO_ACCESS_TOKEN') or os.getenv('MIRO_ACCESS_TOKEN')

    if not token:
        result['missing'].append({
            'item': 'MIRO_ACCESS_TOKEN',
            'required': True,
            'location': '.env'
        })
        result['fix_instructions'] = [
            'Add MIRO_ACCESS_TOKEN to your .env file',
            'Get a token from https://miro.com/app/settings/user-profile/ (API tokens section)',
            'Or create an app at https://developers.miro.com and use OAuth'
        ]
        return result

    result['found'].append('MIRO_ACCESS_TOKEN')

    # Test the token
    try:
        from miro_client import get_client
        client = get_client()
        boards = client.get('boards', {'limit': 1})
        result['status'] = 'configured'
        result['exit_code'] = 0
        result['ai_action'] = 'proceed_with_operation'
        result['boards_accessible'] = boards.get('total', 0)
    except Exception as e:
        result['status'] = 'token_invalid'
        result['exit_code'] = 1
        result['ai_action'] = 'refresh_token'
        result['error'] = str(e)
        result['fix_instructions'] = [
            'Your MIRO_ACCESS_TOKEN may be expired or invalid',
            'Generate a new token and update .env'
        ]

    return result


def main():
    parser_json = '--json' in sys.argv

    result = check_config()

    if parser_json:
        print(json.dumps(result, indent=2))
    else:
        status = result['status']
        if status == 'configured':
            print(f"Miro: Configured ({result.get('boards_accessible', 0)} boards accessible)")
        elif status == 'token_invalid':
            print(f"Miro: Token invalid - {result.get('error', 'unknown')}")
        else:
            print("Miro: Not configured")
            for instruction in result.get('fix_instructions', []):
                print(f"  - {instruction}")

    sys.exit(result['exit_code'])


if __name__ == '__main__':
    main()
