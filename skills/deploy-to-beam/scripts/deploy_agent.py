#!/usr/bin/env python3
"""
Deploy Agent — Main orchestrator for deploying Beam Next skills to Beam Platform.

Reads a skill's SKILL.md (and optional beam-agent.yaml), then deploys
as a Beam Platform agent via the appropriate path.

Usage:
    # AI-guided (reads SKILL.md, generates agent automatically)
    python deploy_agent.py --skill-path 01-skills/outbound-sales

    # Spec-based (uses beam-agent.yaml for precise control)
    python deploy_agent.py --skill-path 01-skills/outbound-sales --mode spec

    # Quick deploy from description
    python deploy_agent.py --query "Create an agent that processes invoices from Gmail"

    # Dry-run (show what would be deployed)
    python deploy_agent.py --skill-path 01-skills/outbound-sales --dry-run
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BEAM_MASTER_SCRIPTS = SCRIPT_DIR.parent.parent / "beam-master" / "scripts"
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent


def read_skill_md(skill_path):
    """Read and parse a SKILL.md file to extract agent-relevant info."""
    skill_file = Path(skill_path) / "SKILL.md"
    if not skill_file.exists():
        skill_file = PROJECT_ROOT / skill_path / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found at {skill_path}")

    content = skill_file.read_text()

    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, _, val = line.partition(':')
                    frontmatter[key.strip()] = val.strip().strip("'\"")
            content = parts[2]

    return {
        "name": frontmatter.get("name", ""),
        "description": frontmatter.get("description", ""),
        "content": content.strip(),
        "frontmatter": frontmatter,
        "path": str(skill_file),
    }


def compose_deployment_query(skill_info):
    """Transform skill info into a deployment query for AI-guided creation."""
    name = skill_info["name"]
    desc = skill_info["description"]
    content = skill_info["content"]

    sections = []
    if name:
        sections.append(f"Create an agent called '{name}'.")
    if desc:
        sections.append(f"Purpose: {desc}")

    for heading in ["## Purpose", "## Workflow", "## Steps", "## What It Does"]:
        if heading.lower().replace("## ", "") in content.lower():
            start = content.lower().index(heading.lower().replace("## ", ""))
            end = content.find("\n## ", start + len(heading))
            section = content[start:end if end > 0 else start + 2000].strip()
            sections.append(section)

    if not sections:
        sections.append(content[:3000])

    return "\n\n".join(sections)


def find_beam_agent_yaml(skill_path):
    """Look for beam-agent.yaml in the skill directory."""
    for name in ["beam-agent.yaml", "beam-agent.yml", "beam-agent.json"]:
        p = Path(skill_path) / name
        if p.exists():
            return p
        p = PROJECT_ROOT / skill_path / name
        if p.exists():
            return p
    return None


def run_script(script_name, args_list):
    """Run a beam-master script and return output."""
    script = BEAM_MASTER_SCRIPTS / script_name
    cmd = [sys.executable, str(script)] + args_list
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BEAM_MASTER_SCRIPTS))
    if result.returncode != 0:
        raise Exception(f"Script failed: {result.stderr or result.stdout}")
    return result.stdout


def check_config():
    """Validate Beam configuration."""
    output = run_script("check_beam_config.py", ["--json"])
    config = json.loads(output)
    return config


def deploy_guided(query, verbose=True):
    """Deploy via AI-guided path."""
    args = ["--query", query, "--json"]
    output = run_script("create_agent_guided.py", args)
    return json.loads(output)


def deploy_spec(spec_path, dry_run=False):
    """Deploy via spec file."""
    args = ["--spec", str(spec_path)]
    if dry_run:
        args.append("--dry-run")
    else:
        args.append("--json")
    output = run_script("create_agent_complete.py", args)
    if dry_run:
        return {"dry_run": True, "payload": json.loads(output)}
    return json.loads(output)


def main():
    parser = argparse.ArgumentParser(description='Deploy skill to Beam Platform')
    parser.add_argument('--skill-path', help='Path to skill directory (relative or absolute)')
    parser.add_argument('--query', help='Direct deployment query (skip skill reading)')
    parser.add_argument('--mode', choices=['auto', 'guided', 'spec'],
                        default='auto',
                        help='Deployment mode: auto (detect), guided (AI), spec (yaml)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without deploying')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--skip-config-check', action='store_true')
    args = parser.parse_args()

    if not args.skill_path and not args.query:
        parser.error("Either --skill-path or --query is required")

    verbose = not args.json

    try:
        if not args.skip_config_check:
            if verbose:
                print("Checking Beam configuration...")
            config = check_config()
            status = config.get("status", "")
            if status != "configured":
                print(json.dumps({"error": "Beam not configured", "config": config}) if args.json
                      else f"Error: Beam not configured. Run check_beam_config.py for details.")
                sys.exit(1)
            if verbose:
                print("  ✓ Beam configuration valid\n")

        mode = args.mode
        spec_path = None
        query = args.query
        skill_info = None

        if args.skill_path:
            skill_info = read_skill_md(args.skill_path)
            spec_path = find_beam_agent_yaml(args.skill_path)

            if mode == 'auto':
                mode = 'spec' if spec_path else 'guided'

            if verbose:
                print(f"Skill:  {skill_info['name']}")
                print(f"Path:   {skill_info['path']}")
                print(f"Mode:   {mode}")
                if spec_path:
                    print(f"Spec:   {spec_path}")
                print()

        if mode == 'guided':
            if not query:
                query = compose_deployment_query(skill_info)

            if args.dry_run:
                result = {"dry_run": True, "query": query, "mode": "guided"}
            else:
                if verbose:
                    print("Deploying via AI-guided setup...\n")
                result = deploy_guided(query)

        elif mode == 'spec':
            if not spec_path:
                print("Error: No beam-agent.yaml found. Use --mode guided or create a spec file."
                      if not args.json else json.dumps({"error": "No beam-agent.yaml found"}))
                sys.exit(1)
            if verbose:
                print(f"Deploying via spec: {spec_path}\n")
            result = deploy_spec(spec_path, dry_run=args.dry_run)

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            if args.dry_run:
                print("DRY RUN — would deploy:")
                print(json.dumps(result, indent=2, default=str))
            elif result.get('error'):
                print(f"Error: {result['error']}")
            else:
                agent_id = result.get('agentId', 'N/A')
                agent_name = result.get('agentName', skill_info.get('name', 'N/A') if skill_info else 'N/A')
                print("✅ Agent deployed to Beam Platform!")
                print("━" * 45)
                print(f"Agent:     {agent_name}")
                print(f"Agent ID:  {agent_id}")
                if agent_id != 'N/A':
                    print(f"Dashboard: https://app.beam.ai/agent/{agent_id}")
                print("\nNext steps:")
                print("  1. Review the graph in Beam dashboard")
                print("  2. Configure triggers (webhook, timer, integration)")
                print(f"  3. Test: create a task from beam-connect")

    except FileNotFoundError as e:
        msg = str(e)
        print(json.dumps({"error": msg}) if args.json else f"Error: {msg}")
        sys.exit(1)
    except Exception as e:
        msg = str(e)
        print(json.dumps({"error": msg}) if args.json else f"Error: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
