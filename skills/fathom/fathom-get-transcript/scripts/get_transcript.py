#!/usr/bin/env python3
"""
Fathom Get Transcript

Fetch the complete transcript for a Fathom recording by ID.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add fathom-master to path for shared client
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
SKILLS_DIR = SKILL_DIR.parent
SYSTEM_SKILLS = SKILLS_DIR.parent / "00-system" / "skills"
FATHOM_MASTER = SYSTEM_SKILLS / "fathom" / "fathom-master" / "scripts"

if FATHOM_MASTER.exists():
    sys.path.insert(0, str(FATHOM_MASTER))
    from fathom_client import get_client, FathomError
else:
    # Fallback: direct implementation
    import requests

    PROJECT_ROOT = SKILLS_DIR.parent
    ENV_FILE = PROJECT_ROOT / ".env"

    def load_api_key():
        env_vars = {}
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        env_vars[key.strip()] = value.strip().strip('"\'')
        return env_vars.get('FATHOM_API_KEY') or os.getenv('FATHOM_API_KEY')


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    if isinstance(seconds, str):
        return seconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def fetch_transcript(recording_id):
    """Fetch transcript from Fathom API."""
    try:
        client = get_client()
        return client.get_transcript(recording_id)
    except NameError:
        # Fallback implementation
        api_key = load_api_key()
        if not api_key:
            print("[ERROR] FATHOM_API_KEY not found in .env")
            sys.exit(1)

        url = f"https://api.fathom.ai/external/v1/recordings/{recording_id}/transcript"
        headers = {"X-Api-Key": api_key}

        response = requests.get(url, headers=headers, timeout=60)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Check your FATHOM_API_KEY")
            sys.exit(1)
        elif response.status_code == 404:
            print(f"[ERROR] 404 Not Found - Recording ID '{recording_id}' not found")
            sys.exit(1)
        else:
            print(f"[ERROR] API returned {response.status_code}: {response.text}")
            sys.exit(1)


def format_transcript(data, output_format="text"):
    """Format transcript data for output."""
    transcript = data.get("transcript", [])

    if output_format == "json":
        # Structure for downstream processing
        speakers = list(set(
            entry.get("speaker", {}).get("display_name", "Unknown")
            for entry in transcript
        ))

        formatted_entries = []
        full_text_parts = []

        for entry in transcript:
            speaker_info = entry.get("speaker", {})
            speaker_name = speaker_info.get("display_name", "Unknown")
            text = entry.get("text", "")
            timestamp = entry.get("timestamp", "00:00")

            formatted_entries.append({
                "timestamp": timestamp,
                "speaker": speaker_name,
                "email": speaker_info.get("matched_calendar_invitee_email", ""),
                "text": text
            })
            full_text_parts.append(f"{speaker_name}: {text}")

        return {
            "speakers": speakers,
            "transcript": formatted_entries,
            "full_text": "\n\n".join(full_text_parts)
        }

    else:
        # Human-readable text format
        lines = []
        speakers = set()

        for entry in transcript:
            speaker_info = entry.get("speaker", {})
            speaker_name = speaker_info.get("display_name", "Unknown")
            speakers.add(speaker_name)
            text = entry.get("text", "")
            timestamp = entry.get("timestamp", "00:00")

            lines.append(f"[{timestamp}] {speaker_name}:")
            lines.append(text)
            lines.append("")

        header = f"Speakers: {', '.join(sorted(speakers))}\n"
        header += "-" * 50 + "\n\n"

        return header + "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch Fathom transcript by recording ID")
    parser.add_argument("--recording-id", "-r", required=True, help="Fathom recording ID")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    print(f"[INFO] Fetching transcript for: {args.recording_id}")

    # Fetch from API
    data = fetch_transcript(args.recording_id)

    # Format output
    output_format = "json" if args.json else "text"
    formatted = format_transcript(data, output_format)

    # Output
    if args.json:
        output_str = json.dumps(formatted, indent=2)
    else:
        output_str = formatted

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_str)
        print(f"[OK] Transcript saved to: {args.output}")
    else:
        print("\n" + output_str)

    # Summary
    if args.json:
        print(f"\n[OK] Retrieved {len(formatted['transcript'])} entries from {len(formatted['speakers'])} speakers")
    else:
        entry_count = len(data.get("transcript", []))
        print(f"\n[OK] Retrieved {entry_count} transcript entries")


if __name__ == "__main__":
    main()
