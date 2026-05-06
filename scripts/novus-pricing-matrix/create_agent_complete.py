#!/usr/bin/env python3
"""
Create Novus Pricing Matrix Report Agent

Reads beam-agent.yaml and calls POST /agent-graphs/complete to create
the agent with its full 4-node graph.

Linked params use pre-generated tool config UUIDs so connections resolve
immediately without manual re-linking in the UI.

Usage:
    # Dry run — print payload without calling API
    python create_agent_complete.py --dry-run

    # Create agent (draft)
    python create_agent_complete.py

Auth:
    Requires BEAM_API_KEY and BEAM_WORKSPACE_ID in project root .env
"""

import os
import sys
import json
import uuid
import argparse
import requests
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "http://localhost:4000"


def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env_vars[k.strip()] = v.strip().strip("\"'")
    return env_vars


def get_headers(api_key, workspace_id):
    return {
        "x-api-key": api_key,
        "current-workspace-id": workspace_id,
        "Content-Type": "application/json",
    }


# ── Pre-generate UUIDs ─────────────────────────────────────────────────────────
# UUIDs are stable within a single run so linked params resolve correctly.
# linkedOutputParamNodeId must point to the tool config ID (NOT the node ID).

def gen():
    return str(uuid.uuid4())


# Node UUIDs
NODE = {
    "extract":   gen(),
    "transform": gen(),
    "report":    gen(),
    "notify":    gen(),
}

# Tool configuration UUIDs — referenced by linked input params
TC = {
    "extract":   gen(),
    "transform": gen(),
    "report":    gen(),
    "notify":    gen(),
}

# Output param UUIDs — stored on outputParams so the API can resolve links
OP = {
    "extract.rent_increases":       gen(),
    "extract.car_park_schedule":    gen(),
    "extract.storage_schedule":     gen(),
    "extract.extraction_summary":   gen(),
    "transform.report_data":        gen(),
    "transform.anomalies":          gen(),
    "transform.validation_summary": gen(),
    "report.report_html":           gen(),
    "report.report_summary":        gen(),
    "notify.notification_status":   gen(),
}


# ── Edge definitions (mirrored into childEdges + parentEdges) ──────────────────

EDGE_EXTRACT_TRANSFORM = {
    "sourceAgentGraphNodeId": NODE["extract"],
    "targetAgentGraphNodeId": NODE["transform"],
    "condition": "",
    "name": "Raw data extracted",
    "isAttachmentDataPulledIn": True,
}

EDGE_TRANSFORM_REPORT = {
    "sourceAgentGraphNodeId": NODE["transform"],
    "targetAgentGraphNodeId": NODE["report"],
    "condition": "",
    "name": "Data validated",
    "isAttachmentDataPulledIn": True,
}

EDGE_REPORT_NOTIFY = {
    "sourceAgentGraphNodeId": NODE["report"],
    "targetAgentGraphNodeId": NODE["notify"],
    "condition": "",
    "name": "Report generated",
    "isAttachmentDataPulledIn": True,
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def static_param(position, name, description, data_type, static_value, required=True, is_array=False):
    return {
        "position": position,
        "paramName": name,
        "paramDescription": description,
        "fillType": "static",
        "staticValue": static_value,
        "required": required,
        "dataType": data_type,
        "isArray": is_array,
        "reloadProps": False,
        "remoteOptions": False,
        "question": "",
    }


def linked_param(position, name, description, data_type, source_tc_key, source_param_name,
                 required=True, is_array=False):
    return {
        "position": position,
        "paramName": name,
        "paramDescription": description,
        "fillType": "linked",
        "linkedOutputParamNodeId": TC[source_tc_key],   # tool config UUID of source node
        "linkedOutputParamName": source_param_name,
        "required": required,
        "dataType": data_type,
        "isArray": is_array,
        "reloadProps": False,
        "remoteOptions": False,
        "question": "",
    }


def output_param(op_key, position, name, description, data_type, tc_key, is_array=False):
    return {
        "id": OP[op_key],
        "position": position,
        "paramName": name,
        "paramDescription": description,
        "dataType": data_type,
        "isArray": is_array,
        "agentToolConfigurationId": TC[tc_key],
    }


def base_node_fields(node_key, objective, x, y, on_error="STOP", is_entry=False, is_exit=False,
                     retry_count=1, retry_wait_ms=1000, enable_retry=False):
    return {
        "id": NODE[node_key],
        "objective": objective,
        "evaluationCriteria": [],
        "isEntryNode": is_entry,
        "isExitNode": is_exit,
        "xCoordinate": x,
        "yCoordinate": y,
        "isEvaluationEnabled": False,
        "isAttachmentDataPulledIn": True,
        "onError": on_error,
        "enableAutoRetryWhenFailure": enable_retry,
        "autoRetryCountWhenFailure": retry_count,
        "autoRetryWaitTimeWhenFailureInMs": retry_wait_ms,
        "autoRetryWhenAccuracyLessThan": 80,
        "autoRetryLimitWhenAccuracyIsLow": 1,
        "enableAutoRetryWhenAccuracyIsLow": False,
        "autoRetryDescription": None,
        "enableAutoRetryDescription": False,
    }


def base_tool_config(tc_key, function_name, name, description, prompt, model,
                     input_params, output_params):
    return {
        "id": TC[tc_key],
        "toolFunctionName": function_name,
        "toolName": name,
        "description": description,
        "prompt": prompt,
        "preferredModel": model,
        "fallbackModels": "",
        "requiresConsent": False,
        "isMemoryTool": False,
        "memoryLookupInstruction": "",
        "isBackgroundTool": False,
        "isBatchExecutionEnabled": False,
        "isCodeExecutionEnabled": False,
        "isAvailableToWorkspace": False,
        "dynamicPropsId": None,
        "integrationProviderId": None,
        "inputParams": input_params,
        "outputParams": output_params,
    }


# ── Build payload ──────────────────────────────────────────────────────────────

def build_payload():

    # ── Node 1: Extract Yardi Data ─────────────────────────────────────────────
    node_extract = {
        **base_node_fields(
            "extract",
            objective=(
                "Extract the three source data files from the Yardi SharePoint export folder: "
                "rent_increases.csv, car_park_schedule.csv, and storage_schedule.csv. "
                "Read each CSV file and return the raw data as structured records. "
                "Report the number of records found in each file."
            ),
            x=250, y=150,
            is_entry=True,
            enable_retry=True,
            retry_count=2,
            retry_wait_ms=3000,
        ),
        "toolConfiguration": base_tool_config(
            "extract",
            function_name="GPTAction_EmptyTool",
            name="SharePoint File Reader",
            description="Reads CSV files from the Yardi SharePoint export folder",
            prompt=(
                "Read the three Yardi export CSV files from the SharePoint folder:\n"
                "1. rent_increases.csv — contains unit_id, property, unit_number, tenant_name,\n"
                "   lease_start, lease_end, current_rent_weekly, proposed_rent_weekly,\n"
                "   increase_pct, increase_status, effective_date, notice_sent\n"
                "2. car_park_schedule.csv — contains bay_id, property, bay_number, bay_type,\n"
                "   tenant_name, unit_id, monthly_rate, lease_start, lease_end, status\n"
                "3. storage_schedule.csv — contains storage_id, property, cage_number, size_sqm,\n"
                "   tenant_name, unit_id, monthly_rate, lease_start, lease_end, status\n\n"
                "Return all records as structured JSON grouped by source file."
            ),
            model="BEDROCK_CLAUDE_SONNET_4",
            input_params=[
                static_param(
                    0, "folder_path",
                    "SharePoint folder path containing Yardi CSV exports",
                    "string",
                    "/sites/NovusManagement/Shared Documents/Yardi Exports/Daily",
                ),
                static_param(
                    1, "file_names",
                    "CSV files to extract",
                    "string",
                    "rent_increases.csv, car_park_schedule.csv, storage_schedule.csv",
                ),
            ],
            output_params=[
                output_param(
                    "extract.rent_increases", 0, "rent_increases",
                    "Rent increase records from Yardi — unit details, current vs proposed rent, increase status",
                    "object", "extract", is_array=True,
                ),
                output_param(
                    "extract.car_park_schedule", 1, "car_park_schedule",
                    "Car park bay records — bay details, tenant assignments, monthly rates, occupancy status",
                    "object", "extract", is_array=True,
                ),
                output_param(
                    "extract.storage_schedule", 2, "storage_schedule",
                    "Storage cage records — cage details, tenant assignments, monthly rates, occupancy status",
                    "object", "extract", is_array=True,
                ),
                output_param(
                    "extract.extraction_summary", 3, "extraction_summary",
                    "Summary of extraction: record counts per file, any missing or malformed files",
                    "string", "extract",
                ),
            ],
        ),
        "childEdges": [EDGE_EXTRACT_TRANSFORM],
        "parentEdges": [],
    }

    # ── Node 2: Transform & Validate ───────────────────────────────────────────
    node_transform = {
        **base_node_fields(
            "transform",
            objective=(
                "Transform and validate the raw Yardi data into report-ready structures.\n\n"
                "For each property, calculate:\n"
                "- Rent increases: count by status (Approved/Pending/Declined),\n"
                "  average increase %, total current vs proposed weekly rent,\n"
                "  weekly and annual uplift amounts\n"
                "- Car park: total bays, occupied vs vacant, occupancy %,\n"
                "  total monthly revenue from occupied bays\n"
                "- Storage: total cages, occupied vs vacant, occupancy %,\n"
                "  total monthly revenue from occupied cages\n\n"
                "Also calculate portfolio-wide totals across all properties.\n\n"
                "Flag any anomalies:\n"
                "- Increase % above 10% (unusually high)\n"
                "- Lease end dates in the past (expired leases)\n"
                "- Occupied bays/cages with no monthly rate"
            ),
            x=550, y=150,
        ),
        "toolConfiguration": base_tool_config(
            "transform",
            function_name="GPTAction_EmptyTool",
            name="Data Transformer",
            description="Transforms raw CSV data into aggregated report metrics per property and portfolio-wide",
            prompt=(
                "You are a data transformation agent for property management reporting.\n\n"
                "Process the three input datasets and produce structured output with:\n\n"
                "1. Per-property breakdown (grouped by property name):\n"
                "   - Rent: unit count, approved/pending/declined counts, avg increase %,\n"
                "     total current weekly, total proposed weekly, weekly uplift, annual uplift\n"
                "   - Car park: total bays, occupied, vacant, occupancy %, monthly revenue\n"
                "   - Storage: total cages, occupied, vacant, occupancy %, monthly revenue\n\n"
                "2. Portfolio totals (all properties combined):\n"
                "   - Same metrics aggregated across all properties\n\n"
                "3. Anomalies (flag but don't block):\n"
                "   - Rent increases > 10%\n"
                "   - Expired leases (end date before today)\n"
                "   - Occupied units with missing rates\n\n"
                "Return as structured JSON with keys: properties, portfolio, anomalies, validation_summary."
            ),
            model="BEDROCK_CLAUDE_SONNET_4",
            input_params=[
                linked_param(
                    0, "rent_increases",
                    "Raw rent increase records from extraction",
                    "object", "extract", "rent_increases", is_array=True,
                ),
                linked_param(
                    1, "car_park_schedule",
                    "Raw car park records from extraction",
                    "object", "extract", "car_park_schedule", is_array=True,
                ),
                linked_param(
                    2, "storage_schedule",
                    "Raw storage records from extraction",
                    "object", "extract", "storage_schedule", is_array=True,
                ),
            ],
            output_params=[
                output_param(
                    "transform.report_data", 0, "report_data",
                    "Transformed report data: per-property metrics and portfolio totals",
                    "object", "transform",
                ),
                output_param(
                    "transform.anomalies", 1, "anomalies",
                    "List of flagged anomalies found during validation",
                    "object", "transform", is_array=True,
                ),
                output_param(
                    "transform.validation_summary", 2, "validation_summary",
                    "Summary: total records processed, properties found, anomalies flagged",
                    "string", "transform",
                ),
            ],
        ),
        "childEdges": [EDGE_TRANSFORM_REPORT],
        "parentEdges": [EDGE_EXTRACT_TRANSFORM],
    }

    # ── Node 3: Generate Report ────────────────────────────────────────────────
    node_report = {
        **base_node_fields(
            "report",
            objective=(
                "Generate the Pricing Matrix Report as a formatted document.\n\n"
                "The report should include:\n"
                "1. Header: \"Pricing Matrix Report\" with today's date and Novus Management branding\n"
                "2. Portfolio KPIs: total units, approved/pending/declined counts,\n"
                "   average increase %, weekly uplift, annual uplift,\n"
                "   car park occupancy & revenue, storage occupancy & revenue\n"
                "3. Per-property sections, each containing:\n"
                "   - Property KPI summary row\n"
                "   - Rent increase table (unit, tenant, current, proposed, increase %, status, effective date, notice sent)\n"
                "   - Car park schedule table (bay, type, tenant, rate, status)\n"
                "   - Storage schedule table (cage, size, tenant, rate, status)\n"
                "   - Occupancy and revenue footer\n"
                "4. Any anomalies flagged during validation\n"
                "5. Footer: Beam AI x Novus, report date, agent version\n\n"
                "Use a clean, professional layout suitable for executive review."
            ),
            x=850, y=150,
        ),
        "toolConfiguration": base_tool_config(
            "report",
            function_name="GPTAction_EmptyTool",
            name="Report Generator",
            description="Generates a formatted Pricing Matrix report from transformed data",
            prompt=(
                "You are a report generation agent for Novus Management property reporting.\n\n"
                "Generate a professional Pricing Matrix Report from the provided data.\n"
                "The report should be clear, data-dense, and suitable for executive review.\n\n"
                "Structure:\n"
                "- Portfolio-wide KPI dashboard at the top\n"
                "- Per-property sections with detailed tables\n"
                "- Anomaly callouts if any exist\n"
                "- Clean professional formatting\n\n"
                "Output the report as formatted HTML that can be viewed in a browser."
            ),
            model="BEDROCK_CLAUDE_OPUS_4_5",
            input_params=[
                linked_param(
                    0, "report_data",
                    "Transformed report data with per-property and portfolio metrics",
                    "object", "transform", "report_data",
                ),
                linked_param(
                    1, "anomalies",
                    "Validation anomalies to include in the report",
                    "object", "transform", "anomalies", is_array=True,
                ),
            ],
            output_params=[
                output_param(
                    "report.report_html", 0, "report_html",
                    "Complete HTML pricing matrix report",
                    "string", "report",
                ),
                output_param(
                    "report.report_summary", 1, "report_summary",
                    "One-paragraph executive summary of the report contents",
                    "string", "report",
                ),
            ],
        ),
        "childEdges": [EDGE_REPORT_NOTIFY],
        "parentEdges": [EDGE_TRANSFORM_REPORT],
    }

    # ── Node 4: Notify Team ────────────────────────────────────────────────────
    node_notify = {
        **base_node_fields(
            "notify",
            objective=(
                "Send a Slack notification to the #novus-reports channel confirming "
                "the Pricing Matrix Report has been generated. Include key metrics "
                "from the portfolio summary: total units, approved/pending counts, "
                "weekly and annual uplift, car park and storage occupancy rates. "
                "If any anomalies were flagged, mention the count."
            ),
            x=1150, y=150,
            on_error="CONTINUE",  # Slack failure should not block
        ),
        "toolConfiguration": base_tool_config(
            "notify",
            function_name="GPTAction_EmptyTool",
            name="Slack Notifier",
            description="Sends report completion notification to Slack",
            prompt=(
                "Send a concise Slack notification about the completed Pricing Matrix Report.\n\n"
                "Format the message as:\n"
                "\u2705 *Pricing Matrix Report \u2014 [today's date]*\n\n"
                "\ud83d\udcca *Portfolio Summary*\n"
                "\u2022 [total units] units | [approved] approved | [pending] pending\n"
                "\u2022 Weekly uplift: $[amount] | Annual: $[amount]\n"
                "\u2022 Car park: [X]% occupied | Storage: [X]% occupied\n\n"
                "[If anomalies: \u26a0\ufe0f [N] anomalies flagged \u2014 review report for details]\n\n"
                "_Report generated by Beam AI agent_"
            ),
            model="BEDROCK_CLAUDE_SONNET_4",
            input_params=[
                static_param(
                    0, "channel",
                    "Slack channel to post notification",
                    "string", "#novus-reports",
                ),
                linked_param(
                    1, "report_summary",
                    "Executive summary from report generation",
                    "string", "report", "report_summary",
                ),
                linked_param(
                    2, "anomalies",
                    "Anomalies to mention in notification",
                    "object", "transform", "anomalies",
                    required=False, is_array=True,
                ),
            ],
            output_params=[
                output_param(
                    "notify.notification_status", 0, "notification_status",
                    "Confirmation that Slack notification was sent",
                    "string", "notify",
                ),
            ],
        ),
        "childEdges": [],
        "parentEdges": [EDGE_REPORT_NOTIFY],
    }

    return {
        "agentName": "Novus Pricing Matrix Report",
        "agentDescription": (
            "Daily automated report agent for Novus Management. Extracts rent increase, "
            "car park, and storage schedule data from Yardi SharePoint exports, "
            "validates and transforms records, generates a Pricing Matrix report, "
            "and notifies the team on Slack."
        ),
        "settings": {
            "prompts": [
                "Generate today's Pricing Matrix Report",
                "Run the daily pricing matrix update",
                "Pull the latest Yardi data and build the pricing matrix",
            ],
            "agentPersonality": (
                "Professional, precise, data-focused. Reports findings clearly with "
                "numbers and percentages. Flags anomalies proactively."
            ),
            "agentRestrictions": (
                "Never modify source data. Never send reports externally. "
                "Always validate data before generating reports."
            ),
        },
        "nodes": [node_extract, node_transform, node_report, node_notify],
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create Novus Pricing Matrix Report agent")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print payload as JSON without calling the API")
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("BEAM_API_KEY") or os.getenv("BEAM_API_KEY")
    workspace_id = env.get("BEAM_WORKSPACE_ID") or os.getenv("BEAM_WORKSPACE_ID")

    if not api_key:
        print("ERROR: BEAM_API_KEY not set in .env or environment", file=sys.stderr)
        sys.exit(1)
    if not workspace_id:
        print("ERROR: BEAM_WORKSPACE_ID not set in .env or environment", file=sys.stderr)
        sys.exit(1)

    payload = build_payload()

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        print(f"\n=== DRY RUN — {len(payload['nodes'])} nodes, no API call made ===", file=sys.stderr)
        return

    print(f"Creating: {payload['agentName']}")
    print(f"Nodes:    {len(payload['nodes'])}")
    print(f"Endpoint: POST {BASE_URL}/agent-graphs/complete\n")

    response = requests.post(
        f"{BASE_URL}/agent-graphs/complete",
        headers=get_headers(api_key, workspace_id),
        json=payload,
        timeout=60,
    )

    if response.status_code in (200, 201):
        result = response.json()
        print("Agent created successfully!")
        print(f"  Agent ID:     {result.get('agentId')}")
        print(f"  Agent Name:   {result.get('agentName')}")
        print(f"  Active Graph: {result.get('activeGraphId')}")
        print(f"  Draft Graph:  {result.get('draftGraphId')}")
    else:
        print(f"Error: {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
