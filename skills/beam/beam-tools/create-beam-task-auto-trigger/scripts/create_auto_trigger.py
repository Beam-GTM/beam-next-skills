#!/usr/bin/env python3
"""
Create Beam Task Auto-Trigger Script

Converts a Beam.ai task into an auto-trigger webhook script for scheduled execution.
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

# Add parent directories to path for shared module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from _shared.beam_api import BeamClient
except ImportError as e:
    print(f"Error: Could not import shared modules: {e}")
    print("Ensure 03-skills/_shared/beam_api.py exists")
    sys.exit(1)


def parse_task_url(task_url):
    """
    Parse Beam task URL to extract workspace, agent, and task IDs.

    Example URL:
    https://app.beam.ai/505d2090-2b5d-4e45-b0f4-cc3a0b299aa8/8cb86b50-aa8f-4876-a3cb-7eb62e910528/tasks/1c08f856-d1a2-47c4-a62a-01ff7d24b3df

    Returns:
        dict: {workspace_id, agent_id, task_id}
    """
    pattern = r'https://app\.beam\.ai/([a-f0-9-]+)/([a-f0-9-]+)/tasks/([a-f0-9-]+)'
    match = re.match(pattern, task_url)

    if not match:
        raise ValueError(f"Invalid Beam task URL format: {task_url}")

    return {
        'workspace_id': match.group(1),
        'agent_id': match.group(2),
        'task_id': match.group(3)
    }


def fetch_task_details(client, task_id):
    """Fetch task details from Beam API."""
    try:
        task = client.get(f"/agent-tasks/{task_id}")
        return task
    except Exception as e:
        print(f"Error fetching task details: {e}")
        sys.exit(1)


def extract_payload(task):
    """
    Extract the original task payload from task details.

    Returns:
        dict: Parsed taskQuery payload
    """
    task_query_str = task.get('taskQuery') or task.get('originalTaskQuery')

    if not task_query_str:
        raise ValueError("No task query found in task details")

    try:
        task_payload = json.loads(task_query_str)
        return task_payload
    except json.JSONDecodeError as e:
        print(f"Error parsing task query JSON: {e}")
        sys.exit(1)


def encode_file_to_base64(file_path):
    """
    Read a file and encode it to base64.

    Args:
        file_path: Path to the file to encode

    Returns:
        str: Base64-encoded file content
    """
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            return base64.b64encode(file_content).decode('utf-8')
    except Exception as e:
        print(f"Error encoding file: {e}")
        sys.exit(1)


def is_simple_query_payload(payload):
    """
    Detect if payload is a simple query-based agent (no attachments needed).

    Simple payloads typically have: query, task, additionalInfo, customerQuery, etc.
    Complex payloads have: email fields (id, messageId, headers, textPlain, etc.)

    Returns:
        bool: True if simple query, False if complex (email/attachments)
    """
    # Email-triggered agents have these characteristic fields
    email_fields = {'id', 'messageId', 'threadId', 'headers', 'textPlain', 'textHtml', 'snippet'}

    # Check if this is an email payload
    if any(field in payload for field in email_fields):
        return False

    # Check if there are attachment references (not base64 data, just references)
    if 'attachments' in payload and payload.get('attachments'):
        # If attachments have 'key' field, they're references (need encodedContextFiles)
        attachments = payload.get('attachments', [])
        if attachments and isinstance(attachments, list) and len(attachments) > 0:
            if any('key' in att or 'data' in att for att in attachments):
                return False

    # Simple query fields
    simple_fields = {'query', 'task', 'additionalInfo', 'customerQuery', 'beamAgentOSTaskID', 'timestamp'}
    payload_fields = set(payload.keys())

    # If only contains simple fields, it's a simple query
    if payload_fields.issubset(simple_fields):
        return True

    return False


def create_webhook_script(webhook_url, payload, script_name, output_dir, attachment_file=None):
    """
    Create bash webhook script with auto-detected format (--data JSON or --form multipart).

    Auto-detects:
    - Simple query-based agents → --data with JSON (cleaner)
    - Email-triggered or attachment agents → --form multipart

    Args:
        webhook_url: Agent webhook URL
        payload: Task payload (dict)
        script_name: Name for the script file
        output_dir: Directory to save the script
        attachment_file: Optional path to file to attach (will be base64 encoded)
    """
    # Ensure script name ends with .sh
    if not script_name.endswith('.sh'):
        script_name += '.sh'

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    script_path = output_path / script_name

    # Detect if this is a simple query or complex payload
    is_simple = is_simple_query_payload(payload) and not attachment_file

    # Separate task payload and encoded context files
    task_payload = {k: v for k, v in payload.items() if k != "timestamp"}

    # Extract or build encoded context files
    encoded_context_files = []

    # If attachment file is provided, encode it and create encodedContextFiles
    if attachment_file:
        attachment_path = Path(attachment_file)
        if not attachment_path.exists():
            raise ValueError(f"Attachment file not found: {attachment_file}")

        # Encode file to base64
        file_content_base64 = encode_file_to_base64(attachment_file)

        # Determine mime type and extension
        mime_type = "application/pdf" if attachment_path.suffix.lower() == '.pdf' else "application/octet-stream"
        file_extension = attachment_path.suffix.lstrip('.')

        # Get file size
        file_size_bytes = attachment_path.stat().st_size
        if file_size_bytes < 1024:
            file_size = f"{file_size_bytes} B"
        else:
            file_size = f"{file_size_bytes // 1024} KB"

        # Create encoded context file object
        encoded_file = {
            "mimeType": mime_type,
            "fileType": "document",
            "fileExtension": file_extension,
            "data": file_content_base64,
            "fileName": attachment_path.name,
            "fileSize": file_size
        }

        encoded_context_files = [encoded_file]

    # Check if payload already has attachments that need to be converted to encodedContextFiles
    elif "attachments" in payload and payload.get("attachments"):
        # For now, keep attachments in task payload as references
        # In future, we could extract and encode them here
        pass

    # Generate script based on payload type
    if is_simple:
        # Simple query-based agent: Use --data with JSON (cleaner format)
        # Remove timestamp field for now, will be added dynamically
        task_payload_without_ts = {k: v for k, v in task_payload.items() if k != "timestamp"}

        # Pretty-print JSON for readability in script
        task_json = json.dumps(task_payload_without_ts, ensure_ascii=False, indent=4)

        script_content = f'''#!/bin/bash
curl --location '{webhook_url}' \\
--header 'Content-Type: application/json' \\
--data '{{
{chr(10).join(f"    {line}" for line in task_json.split(chr(10))[1:-1])}
}}'
'''
    else:
        # Complex payload (email/attachments): Use --form multipart format
        task_payload["timestamp"] = "__TIMESTAMP_PLACEHOLDER__"

        # Escape JSON for bash --form format
        # Use compact JSON for task field and escape quotes
        task_json_escaped = json.dumps(task_payload, ensure_ascii=False, separators=(',', ':')).replace('"', '\\"')

        if encoded_context_files:
            # Include encodedContextFiles field only if there are files
            context_json_escaped = json.dumps(encoded_context_files, ensure_ascii=False, separators=(',', ':')).replace('"', '\\"')

            script_content = f'''#!/bin/bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TASK_PAYLOAD='{task_json_escaped}'
TASK_WITH_TIMESTAMP=$(echo "$TASK_PAYLOAD" | sed "s/__TIMESTAMP_PLACEHOLDER__/$TIMESTAMP/g")

curl --location '{webhook_url}' \\
--form 'task="'"$TASK_WITH_TIMESTAMP"'"' \\
--form 'encodedContextFiles="{context_json_escaped}"'
'''
        else:
            # No attachments - only send task field with --form
            script_content = f'''#!/bin/bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TASK_PAYLOAD='{task_json_escaped}'
TASK_WITH_TIMESTAMP=$(echo "$TASK_PAYLOAD" | sed "s/__TIMESTAMP_PLACEHOLDER__/$TIMESTAMP/g")

curl --location '{webhook_url}' \\
--form 'task="'"$TASK_WITH_TIMESTAMP"'"'
'''

    # Write script file
    script_path.write_text(script_content)

    # Make script executable
    os.chmod(script_path, 0o755)

    return script_path


def main():
    parser = argparse.ArgumentParser(
        description="Create auto-trigger webhook script from a Beam.ai task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode
    python create_auto_trigger.py

    # With task URL
    python create_auto_trigger.py --task-url "https://app.beam.ai/.../tasks/abc123"

    # With all parameters
    python create_auto_trigger.py \\
        --task-url "https://app.beam.ai/.../tasks/abc123" \\
        --webhook-url "https://api.beamstudio.ai/agent-tasks/.../webhook/xyz" \\
        --script-name "my-task.sh"

    # Custom output directory
    python create_auto_trigger.py \\
        --task-url "..." \\
        --output-dir "/custom/path"
"""
    )

    parser.add_argument(
        '--task-url',
        help='Beam.ai task URL (from browser)'
    )
    parser.add_argument(
        '--webhook-url',
        help='Agent webhook URL'
    )
    parser.add_argument(
        '--script-name',
        help='Name for the webhook script (e.g., my-task.sh)'
    )
    parser.add_argument(
        '--output-dir',
        default='04-workspace/scripts/webhook-scheduler/webhooks',
        help='Output directory (default: webhook-scheduler/webhooks)'
    )
    parser.add_argument(
        '--workspace',
        default='bid',
        choices=['bid', 'prod'],
        help='Beam workspace (default: bid)'
    )
    parser.add_argument(
        '--attachment-file',
        help='Path to file to attach (e.g., resume.pdf). Will be base64 encoded and included in payload.'
    )

    args = parser.parse_args()

    # Interactive mode if arguments not provided
    task_url = args.task_url
    if not task_url:
        task_url = input("Beam task URL: ").strip()

    webhook_url = args.webhook_url
    if not webhook_url:
        webhook_url = input("Webhook URL: ").strip()

    script_name = args.script_name
    if not script_name:
        script_name = input("Script name (e.g., my-task.sh): ").strip()

    try:
        # Parse task URL
        print("\n[1/5] Parsing task URL...")
        url_parts = parse_task_url(task_url)
        task_id = url_parts['task_id']
        print(f"  ✓ Task ID: {task_id}")

        # Initialize Beam client
        print("\n[2/5] Authenticating with Beam API...")
        client = BeamClient(workspace=args.workspace)
        print("  ✓ Authenticated")

        # Fetch task details
        print(f"\n[3/5] Fetching task details...")
        task = fetch_task_details(client, task_id)
        print(f"  ✓ Task status: {task.get('status', 'unknown')}")

        # Extract payload
        print("\n[4/5] Extracting task payload...")
        payload = extract_payload(task)
        print(f"  ✓ Payload extracted ({len(str(payload))} chars)")

        # Create webhook script
        print(f"\n[5/5] Creating webhook script...")
        script_path = create_webhook_script(
            webhook_url=webhook_url,
            payload=payload,
            script_name=script_name,
            output_dir=args.output_dir,
            attachment_file=args.attachment_file
        )

        print(f"\n✅ SUCCESS! Webhook script created:")
        print(f"   📄 {script_path}")
        if args.attachment_file:
            print(f"   📎 Attachment: {Path(args.attachment_file).name} (base64 encoded)")
        print(f"\n💡 Test it:")
        print(f"   bash {script_path}")
        print(f"\n🔄 Webhook Rotation:")
        print(f"   This script will run every ~47 minutes as part of the rotation")

    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
