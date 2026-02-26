#!/usr/bin/env python3
"""
LLM Tool Analyzer

Analyze Beam AI task data to identify LLM tools and recommend optimal models.

Usage:
    # Analyze task from saved JSON file
    python analyze_llm_tools.py --file /tmp/beam_task_xxx.json

    # Analyze task directly by ID
    python analyze_llm_tools.py --task-id abc123-def456

    # Manual analysis from prompt
    python analyze_llm_tools.py --manual --prompt "Your prompt here" --input-example '{"field": "value"}'
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

# Add parent directories for shared module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# LLM Model specifications
MODELS = {
    # GPT Models
    "gpt-4o-mini": {
        "name": "GPT-4o-mini",
        "provider": "OpenAI",
        "input_price": 0.15,
        "output_price": 0.60,
        "context_window": 128000,
        "max_output": 16000,
        "speed": "fast",
        "quality": "good",
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "provider": "OpenAI",
        "input_price": 2.50,
        "output_price": 10.00,
        "context_window": 128000,
        "max_output": 16000,
        "speed": "medium",
        "quality": "very good",
    },
    "gpt-4.1": {
        "name": "GPT-4.1",
        "provider": "OpenAI",
        "input_price": 2.00,
        "output_price": 8.00,
        "context_window": 1000000,
        "max_output": 32000,
        "speed": "medium",
        "quality": "very good",
    },
    "gpt-5": {
        "name": "GPT-5",
        "provider": "OpenAI",
        "input_price": 1.25,
        "output_price": 10.00,
        "context_window": 400000,
        "max_output": 128000,
        "speed": "medium",
        "quality": "excellent",
    },
    "gpt-5.2": {
        "name": "GPT-5.2",
        "provider": "OpenAI",
        "input_price": 1.75,
        "output_price": 14.00,
        "context_window": 400000,
        "max_output": 128000,
        "speed": "variable",
        "quality": "best",
    },
    # Claude Models
    "claude-3-sonnet": {
        "name": "Claude 3 Sonnet",
        "provider": "Anthropic",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 200000,
        "max_output": 4000,
        "speed": "medium",
        "quality": "good",
    },
    "claude-3-5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 200000,
        "max_output": 8000,
        "speed": "medium",
        "quality": "very good",
    },
    "claude-3-7-sonnet": {
        "name": "Claude 3.7 Sonnet",
        "provider": "Anthropic",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 200000,
        "max_output": 128000,
        "speed": "medium",
        "quality": "very good",
    },
    "claude-4-sonnet": {
        "name": "Claude 4 Sonnet",
        "provider": "Anthropic",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 200000,
        "max_output": 8000,
        "speed": "medium",
        "quality": "very good",
    },
    "claude-4.5-sonnet": {
        "name": "Claude 4.5 Sonnet",
        "provider": "Anthropic",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 200000,
        "max_output": 64000,
        "speed": "medium",
        "quality": "excellent",
    },
    "claude-4.5-opus": {
        "name": "Claude 4.5 Opus",
        "provider": "Anthropic",
        "input_price": 5.00,
        "output_price": 25.00,
        "context_window": 200000,
        "max_output": 64000,
        "speed": "slow",
        "quality": "best",
    },
    # Gemini Models
    "gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "input_price": 1.25,
        "output_price": 10.00,
        "context_window": 1000000,
        "max_output": 64000,
        "speed": "medium",
        "quality": "excellent",
    },
    "gemini-3-pro": {
        "name": "Gemini 3 Pro",
        "provider": "Google",
        "input_price": 3.00,
        "output_price": 15.00,
        "context_window": 1000000,
        "max_output": 64000,
        "speed": "variable",
        "quality": "excellent",
    },
    "gemini-3-flash": {
        "name": "Gemini 3 Flash",
        "provider": "Google",
        "input_price": 0.50,
        "output_price": 3.00,
        "context_window": 1000000,
        "max_output": 64000,
        "speed": "very fast",
        "quality": "good",
    },
}


def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text.
    Rough estimate: ~4 characters per token for English text.
    """
    if not text:
        return 0

    # More accurate for code/JSON: ~1.5 tokens per word
    # For plain English: ~0.75 tokens per word

    # Count characters and estimate
    char_count = len(str(text))

    # If it looks like JSON/code (has braces, quotes)
    if any(c in str(text) for c in ['{', '[', '"', ':']):
        return int(char_count / 3.5)  # More tokens for structured data

    return int(char_count / 4)


def extract_task_id_from_url(url: str) -> Optional[str]:
    """Extract task ID from Beam task URL."""
    # Pattern: .../tasks/{uuid}
    match = re.search(r'/tasks/([a-f0-9-]{36})', url, re.IGNORECASE)
    if match:
        return match.group(1)

    # Check if it's already a UUID
    if re.match(r'^[a-f0-9-]{36}$', url, re.IGNORECASE):
        return url

    return None


def identify_llm_tools(task_data: dict) -> list:
    """
    Identify LLM-based tools from task data.

    Returns list of dicts with tool info.
    """
    llm_tools = []
    nodes = task_data.get("agentTaskNodes", [])

    for i, node in enumerate(nodes):
        tool = node.get("tool", {})
        tool_config = tool.get("toolConfiguration", {})
        original_tool = tool_config.get("originalTool", {})
        tool_type = original_tool.get("type", "")

        # Check if it's an LLM tool
        if tool_type in ["gpt_tool", "custom_gpt_tool"]:
            tool_data = node.get("toolData", {})

            llm_tools.append({
                "index": i + 1,
                "name": tool.get("name", f"Tool {i + 1}"),
                "type": tool_type,
                "current_model": original_tool.get("preferredModel", "unknown"),
                "prompt": tool_data.get("filled_prompt", ""),
                "input": node.get("input", []),
                "output": node.get("output", {}),
                "status": node.get("status", ""),
            })

    return llm_tools


def analyze_tool(tool: dict) -> dict:
    """
    Analyze a tool and calculate token requirements.
    """
    # Get prompt and estimate tokens
    prompt = tool.get("prompt", "")
    prompt_tokens = estimate_tokens(prompt)

    # Calculate input tokens from input parameters
    input_data = tool.get("input", [])
    input_text = json.dumps(input_data) if input_data else ""
    input_tokens = estimate_tokens(input_text)

    # Calculate output tokens
    output_data = tool.get("output", {})
    output_text = json.dumps(output_data) if output_data else ""
    output_tokens = estimate_tokens(output_text)

    # Total context needed (prompt is often included in input)
    total_input = prompt_tokens + input_tokens

    # Add 20% buffer
    total_input_buffered = int(total_input * 1.2)
    output_tokens_buffered = int(max(output_tokens, 500) * 1.2)  # Minimum 500 output

    return {
        "prompt_tokens": prompt_tokens,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_input_buffered": total_input_buffered,
        "output_tokens_buffered": output_tokens_buffered,
        "total_context_needed": total_input_buffered + output_tokens_buffered,
    }


def recommend_models(analysis: dict, top_n: int = 3) -> list:
    """
    Recommend models based on analysis.

    Returns sorted list of recommendations.
    """
    context_needed = analysis["total_context_needed"]
    output_needed = analysis["output_tokens_buffered"]

    recommendations = []

    for model_id, specs in MODELS.items():
        # Check if model can handle the context
        if specs["context_window"] < context_needed:
            continue

        # Check if model can handle the output
        if specs["max_output"] < output_needed:
            continue

        # Calculate cost per 1K calls
        cost_per_call = (
            (analysis["total_input_buffered"] / 1_000_000 * specs["input_price"]) +
            (analysis["output_tokens_buffered"] / 1_000_000 * specs["output_price"])
        )
        cost_per_1k = cost_per_call * 1000

        recommendations.append({
            "model_id": model_id,
            "name": specs["name"],
            "provider": specs["provider"],
            "cost_per_1k": cost_per_1k,
            "context_window": specs["context_window"],
            "max_output": specs["max_output"],
            "speed": specs["speed"],
            "quality": specs["quality"],
            "input_price": specs["input_price"],
            "output_price": specs["output_price"],
        })

    # Sort by cost
    recommendations.sort(key=lambda x: x["cost_per_1k"])

    return recommendations[:top_n]


def format_report(tool: dict, analysis: dict, recommendations: list) -> str:
    """Format the analysis as a report."""
    lines = []
    lines.append("=" * 60)
    lines.append("LLM Model Recommendation Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Tool: {tool.get('name', 'Unknown')}")
    lines.append(f"Current Model: {tool.get('current_model', 'Not set')}")
    lines.append(f"Tool Type: {tool.get('type', 'Unknown')}")
    lines.append("")
    lines.append("--- Token Analysis ---")
    lines.append(f"Prompt tokens: ~{analysis['prompt_tokens']:,}")
    lines.append(f"Input tokens: ~{analysis['input_tokens']:,}")
    lines.append(f"Output tokens: ~{analysis['output_tokens']:,}")
    lines.append(f"Total (with 20% buffer): ~{analysis['total_context_needed']:,} tokens")
    lines.append("")
    lines.append("--- Recommendations (by cost) ---")

    for i, rec in enumerate(recommendations, 1):
        lines.append("")
        lines.append(f"{i}. {rec['name']} ({rec['provider']})")
        lines.append(f"   Cost: ${rec['cost_per_1k']:.2f} per 1K calls")
        lines.append(f"   Context: {rec['context_window']:,} | Output: {rec['max_output']:,}")
        lines.append(f"   Speed: {rec['speed']} | Quality: {rec['quality']}")
        lines.append(f"   Pricing: ${rec['input_price']}/M in, ${rec['output_price']}/M out")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze LLM tools and recommend optimal models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Path to saved task JSON file")
    group.add_argument("--task-id", "-t", help="Beam task ID to fetch")
    group.add_argument("--manual", "-m", action="store_true", help="Manual analysis mode")

    parser.add_argument("--prompt", help="Prompt text for manual analysis")
    parser.add_argument("--input-example", help="Input example JSON for manual analysis")
    parser.add_argument("--output-example", help="Output example JSON for manual analysis")
    parser.add_argument("--workspace", "-w", default="bid", choices=["bid", "prod"])
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--tool-index", type=int, help="Analyze specific tool by index (1-based)")

    args = parser.parse_args()

    if args.manual:
        # Manual analysis
        if not args.prompt:
            print("Error: --prompt required for manual analysis")
            sys.exit(1)

        tool = {
            "name": "Manual Analysis",
            "type": "manual",
            "current_model": "N/A",
            "prompt": args.prompt,
            "input": json.loads(args.input_example) if args.input_example else [],
            "output": json.loads(args.output_example) if args.output_example else {},
        }

        analysis = analyze_tool(tool)
        recommendations = recommend_models(analysis)

        if args.json:
            print(json.dumps({
                "tool": tool,
                "analysis": analysis,
                "recommendations": recommendations
            }, indent=2))
        else:
            print(format_report(tool, analysis, recommendations))

    elif args.file:
        # Load from file
        try:
            with open(args.file) as f:
                task_data = json.load(f)
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

        llm_tools = identify_llm_tools(task_data)

        if not llm_tools:
            print("No LLM tools found in task data.")
            print("\nTools found:")
            for node in task_data.get("agentTaskNodes", []):
                tool = node.get("tool", {})
                tool_type = tool.get("toolConfiguration", {}).get("originalTool", {}).get("type", "unknown")
                print(f"  - {tool.get('name', 'Unknown')}: {tool_type}")
            sys.exit(0)

        print(f"Found {len(llm_tools)} LLM tool(s):\n")
        for tool in llm_tools:
            print(f"  [{tool['index']}] {tool['name']} (type: {tool['type']})")

        # Analyze specific tool or all
        tools_to_analyze = llm_tools
        if args.tool_index:
            tools_to_analyze = [t for t in llm_tools if t['index'] == args.tool_index]

        print("\n")

        all_results = []
        for tool in tools_to_analyze:
            analysis = analyze_tool(tool)
            recommendations = recommend_models(analysis)

            if args.json:
                all_results.append({
                    "tool": tool,
                    "analysis": analysis,
                    "recommendations": recommendations
                })
            else:
                print(format_report(tool, analysis, recommendations))
                print("\n")

        if args.json:
            print(json.dumps(all_results, indent=2))

    elif args.task_id:
        # Fetch from Beam API
        try:
            from _shared.beam_api import BeamClient

            client = BeamClient(workspace=args.workspace)
            task_data = client.get(f"/agent-tasks/{args.task_id}")

            # Save to temp file
            temp_file = f"/tmp/beam_task_{args.task_id}.json"
            with open(temp_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            print(f"Task data saved to: {temp_file}\n")

            # Now analyze
            llm_tools = identify_llm_tools(task_data)

            if not llm_tools:
                print("No LLM tools found in task.")
                sys.exit(0)

            print(f"Found {len(llm_tools)} LLM tool(s):\n")
            for tool in llm_tools:
                analysis = analyze_tool(tool)
                recommendations = recommend_models(analysis)
                print(format_report(tool, analysis, recommendations))
                print("\n")

        except ImportError:
            print("Error: Could not import BeamClient. Run from project root.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
