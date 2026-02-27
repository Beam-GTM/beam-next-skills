#!/usr/bin/env python3
"""
Create Agent (AI-Guided Setup)

Multi-step agent creation using Beam's AI-guided setup flow:
  1. POST /agent-setup/agent-context/feedback → get threadId + agent config
  2. POST /agent-setup (with contextFileIds + query) → create + configure agent
     Steps: GENERATE_SOP → GRAPH_GENERATION → TOOL_MATCHING →
            TOOL_GENERATION → TOOL_INTEGRATION → UPDATE_AGENT

Usage:
    python create_agent_guided.py --query "Create an agent that processes invoices from Gmail"
    python create_agent_guided.py --query "..." --context-files doc1.pdf doc2.txt
    python create_agent_guided.py --query "..." --step-by-step
    python create_agent_guided.py --query "..." --json
"""

import sys
import json
import time
import argparse
from beam_client import get_client

SETUP_STEPS = [
    "GENERATE_SOP",
    "GRAPH_GENERATION",
    "TOOL_MATCHING",
    "TOOL_GENERATION",
    "TOOL_INTEGRATION",
    "UPDATE_AGENT",
]


def submit_context(client, query):
    """Step 1: Submit context to get agent configuration suggestion."""
    result = client.post('/agent-setup/agent-context/feedback', data={
        "query": query
    })
    return result


def run_setup_step(client, agent_id, step, query=None, context_file_ids=None):
    """Run a single agent setup step."""
    data = {
        "agentId": agent_id,
        "agentSetupStep": step,
    }
    if query:
        data["query"] = query
    if context_file_ids:
        data["contextFileIds"] = context_file_ids
    return client.post('/agent-setup', data=data)


def run_full_setup(client, query, context_file_ids=None, step_by_step=False, verbose=True):
    """Run the complete agent creation flow."""
    if verbose:
        print("Step 1/7: Submitting context...")
    ctx = submit_context(client, query)
    thread_id = ctx.get('threadId')
    response = ctx.get('response', {})
    agent_name = response.get('name', 'New Agent')

    if verbose:
        print(f"  → Agent suggestion: {agent_name}")
        print(f"  → Thread: {thread_id}")

    if verbose:
        print("Step 2/7: Creating agent...")
    create_data = {"query": query}
    if thread_id:
        create_data["threadId"] = thread_id
    if context_file_ids:
        create_data["contextFileIds"] = context_file_ids
    create_result = client.post('/agent-setup', data={
        **create_data,
        "agentSetupStep": "GENERATE_SOP",
    })

    agent_id = None
    agent_response = create_result.get('agentResponse', {})
    agent = agent_response.get('agent', {})
    agent_id = agent.get('id') or create_result.get('agentId')
    next_step = create_result.get('nextStep')

    if verbose and agent_id:
        print(f"  → Agent ID: {agent_id}")

    if not agent_id:
        return {"error": "Failed to get agent ID from setup", "raw": create_result}

    for step in SETUP_STEPS[1:]:
        if next_step and step != next_step and SETUP_STEPS.index(step) < SETUP_STEPS.index(next_step):
            continue

        step_num = SETUP_STEPS.index(step) + 3
        if verbose:
            print(f"Step {step_num}/7: {step.replace('_', ' ').title()}...")

        if step_by_step:
            input(f"  Press Enter to proceed with {step}...")

        result = run_setup_step(client, agent_id, step, query=query)
        next_step = result.get('nextStep')

        if verbose:
            print(f"  → Done. Next: {next_step or 'COMPLETE'}")

        if next_step == 'AGENT_UPDATED' or not next_step:
            break

        time.sleep(1)

    return {
        "agentId": agent_id,
        "agentName": agent_name,
        "threadId": thread_id,
        "status": "created",
        "setup": create_result,
    }


def main():
    parser = argparse.ArgumentParser(description='Create agent via AI-guided setup')
    parser.add_argument('--query', required=True, help='Natural language description of the agent')
    parser.add_argument('--context-files', nargs='*', help='Context file IDs to upload')
    parser.add_argument('--step-by-step', action='store_true', help='Pause between steps')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        verbose = not args.json

        result = run_full_setup(
            client,
            query=args.query,
            context_file_ids=args.context_files,
            step_by_step=args.step_by_step,
            verbose=verbose,
        )

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("\n" + "=" * 50)
            if result.get('error'):
                print(f"Error: {result['error']}")
            else:
                agent_id = result.get('agentId', 'N/A')
                print(f"Agent created: {result.get('agentName', 'N/A')}")
                print(f"Agent ID:      {agent_id}")
                print(f"\nDashboard:     https://app.beam.ai/agent/{agent_id}")
                print("\nThe agent has been created with AI-generated:")
                print("  - SOP (standard operating procedure)")
                print("  - Workflow graph")
                print("  - Tool matching & integration")
                print("\nNext steps:")
                print("  - Review the agent graph in the Beam dashboard")
                print("  - Configure triggers (webhook, timer, integration)")
                print(f"  - Test: python create_task.py --agent-id {agent_id} --query 'test'")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
