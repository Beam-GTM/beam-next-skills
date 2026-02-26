#!/usr/bin/env python3
"""
Get Amie Note Transcript

Retrieves the transcript with speaker identification for a meeting note.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from amie_client import get_client


def get_transcript(note_id: str) -> dict:
    """
    Get transcript for a specific note.

    Args:
        note_id: The ID of the note

    Returns:
        dict: Transcript with speakers
    """
    client = get_client()
    return client.get(f'/notes/{note_id}/transcript')


def main():
    parser = argparse.ArgumentParser(description="Get Amie note transcript")
    parser.add_argument('--id', required=True, help='Note ID')
    parser.add_argument('--output', '-o', metavar='PATH', help='Save transcript to file (JSON)')
    parser.add_argument('--format', choices=('json', 'text'), default='json',
                        help='When using --output: json (full data) or text (readable by speaker)')
    parser.add_argument('--json', action='store_true', help='Output as JSON to stdout (default if no --output)')
    args = parser.parse_args()

    try:
        result = get_transcript(args.id)
        out_str = json.dumps(result, indent=2)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if args.format == 'text':
                lines = []
                segments = result.get('transcript_detailed', {}).get('segments', [])
                for s in segments:
                    lines.append(f"{s.get('speakerName', 'Unknown')}: {s.get('text', '')}")
                out_str = '\n\n'.join(lines)
            out_path.write_text(out_str, encoding='utf-8')
            print(json.dumps({"saved": str(out_path.resolve()), "format": args.format}))
        else:
            print(out_str)
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
