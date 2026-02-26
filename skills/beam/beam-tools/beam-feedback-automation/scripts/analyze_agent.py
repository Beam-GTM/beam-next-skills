#!/usr/bin/env python3
"""
Beam Agent Analyzer
Fetches agent graph from Beam API and extracts schema for feedback generation.
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path


class BeamAgentAnalyzer:
    """Analyzes Beam agents via API to extract input/output schema."""

    def __init__(self, api_key: Optional[str] = None, workspace_id: Optional[str] = None):
        """Initialize analyzer with Beam API key."""
        self.api_key = api_key or os.getenv('BEAM_API_KEY')
        self.workspace_id = workspace_id or os.getenv('BEAM_WORKSPACE_ID')

        if not self.api_key:
            raise ValueError("BEAM_API_KEY environment variable not set")
        if not self.workspace_id:
            raise ValueError("BEAM_WORKSPACE_ID environment variable not set")

        self.base_url = "https://api.beamstudio.ai"

        # Get access token
        self.access_token = self._get_access_token()

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "current-workspace-id": self.workspace_id,
            "Content-Type": "application/json"
        }

    def _get_access_token(self) -> str:
        """Exchange API key for access token."""
        url = f"{self.base_url}/auth/access-token"

        try:
            response = requests.post(url, json={"apiKey": self.api_key})
            response.raise_for_status()
            return response.json()['idToken']
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting access token: {e}")
            sys.exit(1)

    def fetch_agent(self, agent_id: str) -> Dict[str, Any]:
        """Fetch agent graph from Beam API."""
        url = f"{self.base_url}/agent-graphs/{agent_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('graph', {})
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching agent graph: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            sys.exit(1)

    def search_agent_by_name(self, name: str) -> Optional[str]:
        """Search for agent by name and return agent ID."""
        url = f"{self.base_url}/agent"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            agents = response.json()

            # agents is a list, not a dict with 'agents' key
            if isinstance(agents, list):
                # Fuzzy match on name
                for agent in agents:
                    if name.lower() in agent.get('name', '').lower():
                        return agent.get('id')

            print(f"❌ No agent found matching name: {name}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching agents: {e}")
            return None

    def extract_schema(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract input/output schema from agent graph."""
        schema = {
            "agent_id": agent_data.get('agentId'),
            "agent_name": agent_data.get('name', 'Unknown Agent'),
            "description": agent_data.get('description', ''),
            "inputs": [],
            "outputs": [],
            "nodes": []
        }

        # Extract nodes from graph
        nodes = agent_data.get('nodes', [])

        for node in nodes:
            node_info = {
                "id": node.get('id'),
                "name": node.get('name', 'Unknown Node'),
                "type": node.get('type', 'unknown'),
                "objective": node.get('objective', '')
            }
            schema['nodes'].append(node_info)

        # For Beam, we need to infer inputs/outputs from task data
        # Since we don't have that here, we'll note that outputs should be
        # fetched from actual task executions
        print("   ℹ️  Note: Output schema will be inferred from task executions")

        # Get a sample task to infer outputs
        sample_outputs = self._get_sample_task_outputs(schema['agent_id'])
        if sample_outputs:
            for key, value in sample_outputs.items():
                schema['outputs'].append({
                    "name": key,
                    "type": self._infer_type(value),
                    "description": ""
                })

        return schema

    def _get_sample_task_outputs(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a sample completed task to infer output schema."""
        url = f"{self.base_url}/agent-tasks"

        params = {
            "agentId": agent_id,
            "statuses": "COMPLETED",
            "pageSize": 1,
            "ordering": "createdAt:desc"
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            tasks = data.get('data', [])
            if tasks:
                task_id = tasks[0].get('id')
                # Get task details
                task_url = f"{self.base_url}/agent-tasks/{task_id}"
                task_response = requests.get(task_url, headers=self.headers)
                task_response.raise_for_status()
                task_data = task_response.json()

                # Extract outputs from task
                outputs = task_data.get('outputs', {})
                return outputs

            return None
        except Exception as e:
            print(f"   ⚠️  Could not fetch sample task: {e}")
            return None

    def _infer_type(self, value: Any) -> str:
        """Infer data type from value."""
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int) or isinstance(value, float):
            return 'number'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'string'

    def analyze(self, agent_identifier: str, is_url: bool = False, is_name: bool = False) -> Dict[str, Any]:
        """
        Analyze agent and return schema.

        Args:
            agent_identifier: Agent ID, URL, or name
            is_url: True if identifier is a URL
            is_name: True if identifier is a name

        Returns:
            Agent schema dictionary
        """
        # Extract agent ID
        if is_url:
            # Extract ID from URL (e.g., https://beam.ai/agent/xyz789)
            agent_id = agent_identifier.split('/')[-1]
        elif is_name:
            # Search by name
            agent_id = self.search_agent_by_name(agent_identifier)
            if not agent_id:
                sys.exit(1)
        else:
            # Direct ID
            agent_id = agent_identifier

        print(f"🔍 Fetching agent: {agent_id}")

        # Fetch agent data
        agent_data = self.fetch_agent(agent_id)

        # Extract schema
        schema = self.extract_schema(agent_data)

        return schema

    def save_schema(self, schema: Dict[str, Any], output_dir: str = "analysis") -> str:
        """Save schema to JSON file."""
        # Create analysis directory
        analysis_dir = Path(output_dir)
        analysis_dir.mkdir(exist_ok=True)

        # Save schema
        agent_id = schema['agent_id']
        output_file = analysis_dir / f"{agent_id}_schema.json"

        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=2)

        return str(output_file)

    def display_summary(self, schema: Dict[str, Any]):
        """Display schema summary."""
        print(f"\n✅ Agent Analysis Complete")
        print(f"\n📋 Agent: {schema['agent_name']}")
        print(f"   ID: {schema['agent_id']}")

        if schema['description']:
            print(f"   Description: {schema['description']}")

        print(f"\n📥 Inputs: {len(schema['inputs'])} fields")
        for inp in schema['inputs']:
            required = "required" if inp.get('required') else "optional"
            print(f"   - {inp['name']} ({inp['type']}, {required})")

        print(f"\n📤 Outputs: {len(schema['outputs'])} fields")
        for out in schema['outputs']:
            print(f"   - {out['name']} ({out['type']})")

        print(f"\n🔗 Nodes: {len(schema['nodes'])} nodes in graph")
        for node in schema['nodes'][:5]:  # Show first 5 nodes
            print(f"   - {node['name']}")
        if len(schema['nodes']) > 5:
            print(f"   ... and {len(schema['nodes']) - 5} more")

        print("\n💡 Ready to generate feedback fields!")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Analyze Beam agent structure')
    parser.add_argument('--agent-id', help='Beam agent ID')
    parser.add_argument('--url', help='Beam agent URL')
    parser.add_argument('--name', help='Agent name (fuzzy search)')
    parser.add_argument('--output-dir', default='analysis', help='Output directory for schema')
    parser.add_argument('--api-key', help='Beam API key (or use BEAM_API_KEY env var)')
    parser.add_argument('--workspace-id', help='Beam workspace ID (or use BEAM_WORKSPACE_ID env var)')

    args = parser.parse_args()

    # Validate input
    if not any([args.agent_id, args.url, args.name]):
        print("❌ Error: Must provide --agent-id, --url, or --name")
        parser.print_help()
        sys.exit(1)

    try:
        # Initialize analyzer
        analyzer = BeamAgentAnalyzer(api_key=args.api_key, workspace_id=args.workspace_id)

        # Determine input type
        if args.url:
            schema = analyzer.analyze(args.url, is_url=True)
        elif args.name:
            schema = analyzer.analyze(args.name, is_name=True)
        else:
            schema = analyzer.analyze(args.agent_id)

        # Display summary
        analyzer.display_summary(schema)

        # Save schema
        output_file = analyzer.save_schema(schema, args.output_dir)
        print(f"\n💾 Schema saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
