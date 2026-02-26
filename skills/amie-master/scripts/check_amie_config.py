#!/usr/bin/env python3
"""
Check Amie API Configuration

Validates that AMIE_API_TOKEN is set up correctly.
Returns JSON output for AI consumption.
"""

import argparse
import json
import os
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def check_config():
    """Check Amie configuration status"""
    result = {
        "status": "not_configured",
        "exit_code": 2,
        "ai_action": "prompt_for_api_token",
        "missing": [],
        "configured": [],
        "fix_instructions": []
    }

    # Load .env
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')

    # Check for AMIE_API_TOKEN
    api_token = env_vars.get('AMIE_API_TOKEN') or os.getenv('AMIE_API_TOKEN')

    if api_token and api_token.startswith('amie_pat_'):
        result["configured"].append({
            "item": "AMIE_API_TOKEN",
            "value": f"{api_token[:20]}...",
            "location": ".env"
        })
        result["status"] = "configured"
        result["exit_code"] = 0
        result["ai_action"] = "proceed_with_operation"
    else:
        result["missing"].append({
            "item": "AMIE_API_TOKEN",
            "required": True,
            "location": ".env"
        })
        result["fix_instructions"].append(
            "Get your Personal Access Token from Amie settings"
        )
        result["fix_instructions"].append(
            "Add to .env: AMIE_API_TOKEN=amie_pat_live_xxx"
        )

    return result


def main():
    parser = argparse.ArgumentParser(description="Check Amie API configuration")
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    result = check_config()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\nAmie Configuration Status: {result['status'].upper()}")
        print("=" * 50)

        if result['configured']:
            print("\nConfigured:")
            for item in result['configured']:
                print(f"  - {item['item']}: {item['value']}")

        if result['missing']:
            print("\nMissing:")
            for item in result['missing']:
                print(f"  - {item['item']} (in {item['location']})")

            print("\nTo fix:")
            for instruction in result['fix_instructions']:
                print(f"  {instruction}")

    sys.exit(result['exit_code'])


if __name__ == '__main__':
    main()
