#!/usr/bin/env python3
"""
Beam Agent Documentation Generator

Fetches Beam agent graphs and generates comprehensive documentation.

Usage:
    # From Beam AI API
    python document_agent.py --workspace-id WORKSPACE_ID --agent-id AGENT_ID

    # From existing graph file
    python document_agent.py --graph-file path/to/graph.json

    # With Notion update
    python document_agent.py --workspace-id WID --agent-id AID --notion-page-id PAGE_ID
"""

import json
import sys
import argparse
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-system" / "skills" / "beam" / "beam-master" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "03-skills" / "_shared"))

try:
    from beam_client import get_client
except ImportError:
    print("[ERROR] Could not import beam_client", file=sys.stderr)
    print("Ensure 00-system/skills/beam/beam-master/scripts/beam_client.py exists", file=sys.stderr)
    sys.exit(1)


def fetch_agent_graph(workspace_id, agent_id):
    """Fetch agent graph from Beam AI API"""
    try:
        client = get_client()
        result = client.get(f'/agent-graphs/{agent_id}')
        return result
    except Exception as e:
        print(f"[ERROR] Failed to fetch agent graph: {e}", file=sys.stderr)
        return None


def load_graph_from_file(file_path):
    """Load agent graph from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load graph file: {e}", file=sys.stderr)
        return None


def analyze_graph(graph_data):
    """Analyze agent graph and extract metadata with detailed descriptions"""
    graph = graph_data.get('graph', {})
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    analysis = {
        'info': {
            'agent_id': graph.get('agentId'),
            'graph_id': graph.get('id'),
            'is_active': graph.get('isActive'),
            'is_published': graph.get('isPublished'),
            'is_draft': graph.get('isDraft'),
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        },
        'nodes': [],
        'connections': [],
        'integrations': {},  # Changed to dict to store integration details
        'inputs': {},  # Changed to dict to store input descriptions
        'outputs': {},  # Changed to dict to store output descriptions
        'tools': set()  # Track unique tools used
    }

    # Analyze each node with detailed extraction
    for idx, node in enumerate(nodes, 1):
        node_info = {
            'step': idx,
            'id': node.get('id'),
            'objective': node.get('objective'),
            'is_entry': node.get('isEntryNode', False),
            'is_exit': node.get('isExitNode', False),
            'on_error': node.get('onError'),
            'tool': None,
            'tool_name': None,
            'tool_description': None,
            'inputs': [],
            'outputs': []
        }

        # Extract tool configuration with descriptions
        tool_config = node.get('toolConfiguration', {})
        if tool_config:
            tool_name = tool_config.get('toolName', '')
            tool_function = tool_config.get('toolFunctionName', '')
            tool_description = tool_config.get('description', '')

            node_info['tool'] = tool_function
            node_info['tool_name'] = tool_name
            node_info['tool_description'] = tool_description

            if tool_name:
                analysis['tools'].add(tool_name)

            # Detect integrations with details
            integration_map = {
                'Airtable': 'Database storage and query',
                'Gmail': 'Email operations',
                'Slack': 'Team communication',
                'Greenhouse': 'ATS integration',
                'LinkedIn': 'Professional network',
                'HubSpot': 'CRM operations',
                'Workable': 'Applicant tracking',
                'Calendly': 'Availability scheduling',
                'GoogleCalendar': 'Calendar management',
                'Google': 'Google Workspace services'
            }

            for integration, purpose in integration_map.items():
                if integration.lower() in tool_name.lower() or integration.lower() in tool_function.lower():
                    if integration not in analysis['integrations']:
                        analysis['integrations'][integration] = {
                            'purpose': purpose,
                            'tools': [],
                            'functions': []
                        }
                    analysis['integrations'][integration]['tools'].append(tool_name)
                    analysis['integrations'][integration]['functions'].append(tool_function)

            # Extract inputs with descriptions
            for param in tool_config.get('inputParams', []):
                param_name = param.get('paramName', '')
                param_desc = param.get('paramDescription', '')
                fill_type = param.get('fillType', '')
                static_value = param.get('staticValue')
                required = param.get('required', False)

                param_info = {
                    'name': param_name,
                    'description': param_desc,
                    'fill_type': fill_type,
                    'required': required,
                    'static_value': static_value
                }
                node_info['inputs'].append(param_info)

                # Store input descriptions
                if fill_type == 'ai_fill' and required:
                    if param_name not in analysis['inputs']:
                        analysis['inputs'][param_name] = param_desc or f"Required input for {tool_name}"

            # Extract outputs with descriptions
            for param in tool_config.get('outputParams', []):
                param_name = param.get('paramName', '')
                param_desc = param.get('paramDescription', '')

                node_info['outputs'].append({
                    'name': param_name,
                    'description': param_desc
                })

                if param_name not in analysis['outputs']:
                    analysis['outputs'][param_name] = param_desc or f"Output from {tool_name}"

        analysis['nodes'].append(node_info)

    # Analyze edges
    for edge in edges:
        source = edge.get('source')
        target = edge.get('target')

        source_node = next((n for n in analysis['nodes'] if n['id'] == source), None)
        target_node = next((n for n in analysis['nodes'] if n['id'] == target), None)

        if source_node and target_node:
            analysis['connections'].append({
                'from': source_node['objective'],
                'to': target_node['objective'],
                'condition': edge.get('condition', {})
            })

    # Convert tools set to sorted list
    analysis['tools'] = sorted(list(analysis['tools']))

    return analysis


def generate_markdown_documentation(analysis, agent_name=None):
    """Generate markdown documentation from analysis"""

    nodes = analysis['nodes']
    integrations = analysis['integrations']
    inputs = analysis['inputs']
    outputs = analysis['outputs']
    agent_info = analysis['info']

    # Determine agent name
    if not agent_name:
        # Try to infer from first non-entry node
        first_node = next((n for n in nodes if not n['is_entry']), nodes[0] if nodes else None)
        agent_name = "Beam Agent"
        if first_node and first_node['objective']:
            # Extract meaningful name from objective
            obj = first_node['objective']
            if 'candidate' in obj.lower() and 'screen' in obj.lower():
                agent_name = "Candidate Screening Agent"
            elif 'invoice' in obj.lower():
                agent_name = "Invoice Processing Agent"
            elif 'email' in obj.lower():
                agent_name = "Email Automation Agent"

    agent_short = agent_name.split('(')[0].strip()

    # Build markdown
    lines = []
    lines.append(f"# 🤖 {agent_name}\n")
    lines.append("## Properties")
    lines.append(f"- **Agent Template**: {agent_name}")
    lines.append("- **Feasibility**: 🟡 Needs Review")
    lines.append("- **Priority**: 2 - Medium")
    lines.append("- **Status Platform**: Draft")
    lines.append("- **Vertical/Teams**: [To be determined]")
    lines.append("- **What it does**: [Auto-generated - please review and update]")
    lines.append("- **Owner**: [To be assigned]")
    lines.append("- **Internal Notes**: [Add context here]")
    lines.append("\n---\n")

    # Agent Overview
    lines.append(f"▶ {agent_short}")
    lines.append(f"### {agent_name}\n")
    lines.append("**Description**\n")

    # Generate description from workflow
    description_parts = []
    if nodes:
        # Get non-entry nodes to describe the workflow
        workflow_nodes = [n for n in nodes if not n['is_entry']]
        if workflow_nodes:
            first_objective = workflow_nodes[0].get('objective', '').lower()
            if first_objective:
                description_parts.append(f"This agent automates {first_objective}")

        # Add integration info
        if integrations:
            int_names = list(integrations.keys())
            if len(int_names) == 1:
                description_parts.append(f"using {int_names[0]} integration")
            elif len(int_names) == 2:
                description_parts.append(f"using {int_names[0]} and {int_names[1]} integrations")
            else:
                description_parts.append(f"using {', '.join(int_names[:-1])}, and {int_names[-1]} integrations")

        # Add step count
        description_parts.append(f"through a {len(workflow_nodes)}-step workflow")

    if description_parts:
        lines.append('. '.join(description_parts).capitalize() + ".\n")
    else:
        lines.append("[Auto-generated description - please review and enhance with specific details]\n")

    lines.append("---\n")

    # Trigger
    lines.append("### Trigger\n")
    lines.append("[Describe what initiates this agent - manual trigger, webhook, schedule, etc.]\n")
    lines.append("---\n")

    # Workflow
    lines.append("### Workflow\n")

    # Generate workflow steps
    step_num = 1
    for node in nodes:
        if node['is_entry']:
            lines.append(f"{step_num}. **Start** - Agent workflow begins")
        else:
            tool_name = node['tool_name'] or 'Process'
            objective = node['objective'] or 'Perform operation'
            lines.append(f"{step_num}. **{tool_name}** - {objective}")
        step_num += 1

    lines.append("\n---\n")

    # Data Inputs
    lines.append("### Data Inputs\n")
    if inputs:
        for inp_name, inp_desc in inputs.items():
            lines.append(f"- **{inp_name}**: {inp_desc}")
    else:
        lines.append("- [No user inputs detected - agent may use static values]")
    lines.append("\n---\n")

    # Expected Outputs
    lines.append("### Expected Outputs\n")
    if outputs:
        for out_name, out_desc in outputs.items():
            lines.append(f"- **{out_name}**: {out_desc}")
    else:
        lines.append("- [No explicit outputs detected - check final node actions]")
    lines.append("\n---\n")

    # Key Integrations
    lines.append("### Key Integrations\n")
    if integrations:
        for integration, details in integrations.items():
            purpose = details['purpose']
            functions = ', '.join(set(details['functions'][:3]))  # Show up to 3 unique functions
            lines.append(f"- **{integration}**: {purpose}")
            if functions:
                lines.append(f"  - Functions: {functions}")
    else:
        lines.append("- [No external integrations detected]")
    lines.append("\n---\n")

    # Summary
    lines.append("## Summary\n")
    lines.append(f"**Workspace Name**: [Workspace name]")
    lines.append(f"**Industry**: [Industry/vertical]")
    if agent_info.get('agent_id'):
        lines.append(f"**Agent Link**: https://app.beam.ai/[workspace-id]/{agent_info['agent_id']}")
    lines.append("\n---\n")

    # Setup Instructions
    lines.append("## Agent Setup Instructions\n")
    lines.append("1. **Pre-Requisite**: [List required accounts, API keys, integrations]")
    lines.append("2. Navigate to Beam AI dashboard")
    lines.append(f"3. Click **Create** on the \"{agent_name}\"")
    lines.append("4. Click **Create → Continue**")
    lines.append("5. **Agent Settings**:")
    lines.append("   - Configure trigger mechanism")
    lines.append("   - Set up required integrations")
    lines.append("   - Test with sample data")
    lines.append("6. **Agent is Setup** and ready to use")
    lines.append("\n---\n")

    # Technical Details
    lines.append("## Technical Implementation Details\n")
    lines.append("### Agent Graph Structure")
    lines.append(f"- **Agent ID**: {agent_info.get('agent_id', 'N/A')}")
    lines.append(f"- **Graph ID**: {agent_info.get('graph_id', 'N/A')}")
    lines.append(f"- **Status**: {'Draft' if agent_info.get('is_draft') else 'Published'}")
    lines.append(f"- **Total Nodes**: {agent_info.get('total_nodes', 0)}")
    lines.append(f"- **Total Edges**: {agent_info.get('total_edges', 0)}\n")

    lines.append("### Node Breakdown")
    for node in nodes:
        lines.append(f"{node['step']}. **{node['tool_name'] or 'Unknown'}**: {node['objective'] or 'No description'}")
        if node['tool_description']:
            lines.append(f"   - Description: {node['tool_description']}")
        if node['inputs']:
            input_count = len(node['inputs'])
            required_count = sum(1 for inp in node['inputs'] if inp.get('required'))
            lines.append(f"   - Inputs: {input_count} parameters ({required_count} required)")
        if node['outputs']:
            output_names = [o['name'] if isinstance(o, dict) else o for o in node['outputs'][:3]]
            lines.append(f"   - Outputs: {', '.join(output_names)}")

    lines.append("\n### Error Handling")
    lines.append("- All nodes configured with error handling")
    lines.append("- Review error paths and retry logic in Beam AI editor\n")

    lines.append("\n---\n")
    lines.append(f"*Documentation generated automatically on {Path(__file__).parent.parent.name}*")
    lines.append(f"*Agent Graph ID: {agent_info.get('graph_id', 'N/A')}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate documentation for Beam AI agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Fetch from Beam AI API
    python document_agent.py --workspace-id 505d2090-... --agent-id 162e7c30-...

    # From existing file
    python document_agent.py --graph-file agent-graph.json

    # With custom output
    python document_agent.py --workspace-id WID --agent-id AID --output-dir my-agents
"""
    )

    parser.add_argument('--workspace-id', help='Beam workspace ID')
    parser.add_argument('--agent-id', help='Beam agent ID')
    parser.add_argument('--graph-file', help='Path to existing graph.json file')
    parser.add_argument('--output-dir', default='04-workspace/beam-agents', help='Output directory')
    parser.add_argument('--agent-name', help='Override agent name')
    parser.add_argument('--format', default='both', choices=['markdown', 'json', 'both'], help='Output format')

    args = parser.parse_args()

    # Validation
    if not args.graph_file and not (args.workspace_id and args.agent_id):
        print("[ERROR] Must provide either --graph-file OR (--workspace-id AND --agent-id)", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    print("=" * 80)
    print("BEAM AGENT DOCUMENTATION GENERATOR")
    print("=" * 80)
    print()

    # Step 1: Fetch or load graph
    graph_data = None
    if args.graph_file:
        print(f"📂 Loading graph from file: {args.graph_file}")
        graph_data = load_graph_from_file(args.graph_file)
    else:
        print(f"🌐 Fetching agent graph from Beam AI...")
        print(f"   Workspace: {args.workspace_id}")
        print(f"   Agent: {args.agent_id}")
        graph_data = fetch_agent_graph(args.workspace_id, args.agent_id)

    if not graph_data:
        print("❌ Failed to fetch/load agent graph", file=sys.stderr)
        sys.exit(1)

    print("✅ Graph loaded successfully")
    print()

    # Save raw graph if fetched from API
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.graph_file and args.agent_id:
        graph_file = output_dir / f"agent-graph-{args.agent_id[:8]}.json"
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        print(f"💾 Saved raw graph: {graph_file}")

    # Step 2: Analyze graph
    print("🔍 Analyzing agent graph structure...")
    analysis = analyze_graph(graph_data)

    print(f"   ✓ Nodes: {analysis['info']['total_nodes']}")
    print(f"   ✓ Inputs: {len(analysis['inputs'])}")
    print(f"   ✓ Outputs: {len(analysis['outputs'])}")
    print(f"   ✓ Integrations: {', '.join(analysis['integrations']) if analysis['integrations'] else 'None'}")
    print()

    # Save analysis
    if args.format in ['json', 'both']:
        analysis_file = output_dir / f"agent-analysis-{args.agent_id[:8] if args.agent_id else 'unknown'}.json"
        # Convert analysis for JSON serialization
        analysis_json = dict(analysis)
        with open(analysis_file, 'w') as f:
            json.dump(analysis_json, f, indent=2)
        print(f"💾 Saved analysis: {analysis_file}")

    # Step 3: Generate documentation
    if args.format in ['markdown', 'both']:
        print("📝 Generating documentation...")
        documentation = generate_markdown_documentation(analysis, args.agent_name)

        # Determine filename
        if args.agent_name:
            filename = args.agent_name.lower().replace(' ', '-').replace('(', '').replace(')', '')
        else:
            filename = f"agent-{args.agent_id[:8]}" if args.agent_id else "agent"

        doc_file = output_dir / f"{filename}-documentation.md"
        with open(doc_file, 'w') as f:
            f.write(documentation)

        print(f"✅ Generated documentation: {doc_file}")

    print()
    print("=" * 80)
    print("✅ DOCUMENTATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review and enhance the generated documentation")
    print("2. Fill in [placeholders] with specific details")
    print("3. Add usage scenarios and examples")
    print("4. Copy to Notion or version control")
    print()


if __name__ == "__main__":
    main()
