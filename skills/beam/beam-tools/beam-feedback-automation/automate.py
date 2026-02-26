#!/usr/bin/env python3
"""
Beam Feedback Automation - Main Entry Point
Universal feedback collection automation for ANY Beam agent.

Usage:
    # Full workflow
    python automate.py agent_xyz789 --tasks 50

    # Individual steps
    python automate.py analyze --agent-id agent_xyz789
    python automate.py generate-fields --agent-id agent_xyz789
    python automate.py deploy --agent-id agent_xyz789
    python automate.py create-sheets --agent-id agent_xyz789 --tasks 50
    python automate.py aggregate --sheet-id abc123
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


class FeedbackAutomation:
    """Main automation orchestrator."""

    def __init__(self):
        self.skill_dir = Path(__file__).parent
        self.scripts_dir = self.skill_dir / 'scripts'
        self.analysis_dir = self.skill_dir / 'analysis'

        # Create directories
        self.analysis_dir.mkdir(exist_ok=True)

    def run_full_workflow(self, agent_id: str, task_count: int = 50, reviewer_email: str = None):
        """Run the complete feedback automation workflow."""
        print("🚀 Starting Full Feedback Automation Workflow\n")

        # Step 1: Analyze agent
        print("=" * 60)
        print("Step 1/6: Analyzing Agent")
        print("=" * 60)
        self.analyze_agent(agent_id)

        # Step 2: Generate feedback fields
        print("\n" + "=" * 60)
        print("Step 2/6: Generating Feedback Fields")
        print("=" * 60)
        self.generate_fields(agent_id)

        # Step 3: Generate Apps Script
        print("\n" + "=" * 60)
        print("Step 3/6: Generating Apps Script")
        print("=" * 60)
        self.generate_apps_script(agent_id)

        # Step 4: Deploy to Google Sheets
        print("\n" + "=" * 60)
        print("Step 4/6: Deploying to Google Sheets")
        print("=" * 60)
        print("\n⚠️  Manual step required:")
        print("   1. Create a new Google Sheet")
        print("   2. Open Extensions > Apps Script")
        print(f"   3. Copy the script from: scripts/{agent_id}_apps_script.js")
        print("   4. Save and authorize the script")
        print("   5. Run the 'onOpen' function to create the menu")
        print("\n   Once deployed, run the 'Pre-fill Agent Data' menu item")
        print(f"   or use: python automate.py create-sheets --agent-id {agent_id} --tasks {task_count}")

        print("\n" + "=" * 60)
        print("✅ Workflow Complete!")
        print("=" * 60)
        print(f"\n📁 Files generated:")
        print(f"   - Schema: analysis/{agent_id}_schema.json")
        print(f"   - Fields: analysis/{agent_id}_feedback_fields.json")
        print(f"   - Script: scripts/{agent_id}_apps_script.js")
        print("\n💡 Next steps:")
        print("   1. Deploy the Apps Script to Google Sheets (see instructions above)")
        print("   2. Run 'Pre-fill Agent Data' from the Google Sheets menu")
        print("   3. Send feedback emails to reviewers")
        print("   4. Aggregate results when reviews are complete")

    def analyze_agent(self, agent_id: str, url: str = None, name: str = None):
        """Analyze Beam agent structure."""
        cmd = [
            'python3',
            str(self.scripts_dir / 'analyze_agent.py'),
            '--output-dir', str(self.analysis_dir)
        ]

        if url:
            cmd.extend(['--url', url])
        elif name:
            cmd.extend(['--name', name])
        else:
            cmd.extend(['--agent-id', agent_id])

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("❌ Agent analysis failed")
            sys.exit(1)

    def generate_fields(self, agent_id: str):
        """Generate feedback fields from schema."""
        schema_file = self.analysis_dir / f"{agent_id}_schema.json"

        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            print("   Run: python automate.py analyze --agent-id {agent_id}")
            sys.exit(1)

        cmd = [
            'python3',
            str(self.scripts_dir / 'generate_feedback_fields.py'),
            '--schema', str(schema_file),
            '--output-dir', str(self.analysis_dir)
        ]

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("❌ Field generation failed")
            sys.exit(1)

    def generate_apps_script(self, agent_id: str):
        """Generate Google Apps Script."""
        fields_file = self.analysis_dir / f"{agent_id}_feedback_fields.json"

        if not fields_file.exists():
            print(f"❌ Fields file not found: {fields_file}")
            print(f"   Run: python automate.py generate-fields --agent-id {agent_id}")
            sys.exit(1)

        output_file = self.scripts_dir / f"{agent_id}_apps_script.js"

        cmd = [
            'python3',
            str(self.scripts_dir / 'generate_apps_script.py'),
            '--agent-id', agent_id,
            '--fields', str(fields_file),
            '--output', str(output_file)
        ]

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("❌ Apps Script generation failed")
            sys.exit(1)

    def show_usage_examples(self):
        """Show usage examples."""
        examples = """
📚 Usage Examples

1. Full workflow (recommended):
   python automate.py agent_xyz789 --tasks 50

2. Step-by-step workflow:
   python automate.py analyze --agent-id agent_xyz789
   python automate.py generate-fields --agent-id agent_xyz789
   python automate.py deploy --agent-id agent_xyz789

3. Analyze by URL:
   python automate.py analyze --url https://beam.ai/agent/xyz789

4. Analyze by name:
   python automate.py analyze --name "TA Interview Agent"

5. Generate fields without overall feedback fields:
   python automate.py generate-fields --agent-id agent_xyz789 --skip-overall

For full documentation, see: SKILL.md
        """
        print(examples)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Universal Beam Feedback Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full workflow
  python automate.py agent_xyz789 --tasks 50

  # Analyze agent
  python automate.py analyze --agent-id agent_xyz789
  python automate.py analyze --url https://beam.ai/agent/xyz789
  python automate.py analyze --name "TA Interview Agent"

  # Generate feedback fields
  python automate.py generate-fields --agent-id agent_xyz789

  # Show examples
  python automate.py examples
        """
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze Beam agent')
    analyze_parser.add_argument('--agent-id', help='Agent ID')
    analyze_parser.add_argument('--url', help='Agent URL')
    analyze_parser.add_argument('--name', help='Agent name (fuzzy search)')

    # Generate fields command
    fields_parser = subparsers.add_parser('generate-fields', help='Generate feedback fields')
    fields_parser.add_argument('--agent-id', required=True, help='Agent ID')
    fields_parser.add_argument('--skip-overall', action='store_true', help='Skip overall fields')

    # Deploy command (just an alias for generate-apps-script)
    deploy_parser = subparsers.add_parser('deploy', help='Generate Apps Script')
    deploy_parser.add_argument('--agent-id', required=True, help='Agent ID')

    # Examples command
    subparsers.add_parser('examples', help='Show usage examples')

    # Positional argument for quick start (agent ID)
    parser.add_argument('agent_id', nargs='?', help='Agent ID (for full workflow)')
    parser.add_argument('--tasks', type=int, default=50, help='Number of tasks to process')
    parser.add_argument('--reviewer-email', help='Reviewer email address')

    args = parser.parse_args()

    automation = FeedbackAutomation()

    # Handle commands
    if args.command == 'analyze':
        if not any([args.agent_id, args.url, args.name]):
            print("❌ Error: Must provide --agent-id, --url, or --name")
            analyze_parser.print_help()
            sys.exit(1)

        automation.analyze_agent(
            agent_id=args.agent_id or '',
            url=args.url,
            name=args.name
        )

    elif args.command == 'generate-fields':
        automation.generate_fields(args.agent_id)

    elif args.command == 'deploy':
        automation.generate_apps_script(args.agent_id)

    elif args.command == 'examples':
        automation.show_usage_examples()

    elif args.agent_id:
        # Full workflow
        automation.run_full_workflow(
            agent_id=args.agent_id,
            task_count=args.tasks,
            reviewer_email=args.reviewer_email
        )

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
