#!/usr/bin/env python3
"""
Push Novus Pricing Matrix Graph

Uses PUT /agent-graphs/{agentId} to explicitly replace the draft graph
with all 4 nodes fully wired — linked params use real output param UUIDs
so linkParamOutputId is set correctly (not null).

Pre-generates UUIDs for nodes, tool configs, and output params so that
linked input params can reference output params within the same payload.

Usage:
    python push_graph.py            # push to draft
    python push_graph.py --dry-run  # print payload only
    python push_graph.py --publish  # push and publish
"""

import os
import sys
import json
import uuid
import argparse
import requests
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ENV_FILE     = PROJECT_ROOT / ".env"
BASE_URL     = "http://localhost:4000"
AGENT_ID     = "1c395bed-8072-4eef-a22e-bd4ab259dab7"


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip("\"'")
    return env


def headers(api_key, workspace_id):
    return {
        "x-api-key": api_key,
        "current-workspace-id": workspace_id,
        "Content-Type": "application/json",
    }


# ── UUID pre-generation ────────────────────────────────────────────────────────
# All IDs are pre-generated so linked params can reference output param UUIDs
# within the same payload — this is what sets linkParamOutputId correctly.

def g(): return str(uuid.uuid4())

# Node IDs
N = dict(extract=g(), transform=g(), report=g(), notify=g())

# Tool configuration IDs
TC = dict(extract=g(), transform=g(), report=g(), notify=g())

# Output parameter IDs — referenced by linked input params via linkParamOutputId
OP = {
    # extract outputs
    "extract.rent_increases":       g(),
    "extract.car_park_schedule":    g(),
    "extract.storage_schedule":     g(),
    "extract.extraction_summary":   g(),
    # transform outputs
    "transform.report_data":        g(),
    "transform.anomalies":          g(),
    "transform.validation_summary": g(),
    # report outputs
    "report.report_html":           g(),
    "report.report_summary":        g(),
    # notify outputs
    "notify.notification_status":   g(),
}


# ── Edge helpers ───────────────────────────────────────────────────────────────

def edge(src_key, tgt_key, name):
    return {
        "sourceAgentGraphNodeId": N[src_key],
        "targetAgentGraphNodeId": N[tgt_key],
        "condition": "",
        "name": name,
        "isAttachmentDataPulledIn": True,
    }

E_ET = edge("extract",   "transform", "Raw data extracted")
E_TR = edge("transform", "report",    "Data validated")
E_RN = edge("report",    "notify",    "Report generated")


# ── Param builders ─────────────────────────────────────────────────────────────

def p_static(pos, name, desc, dtype, value, required=True):
    return {
        "position": pos,
        "paramName": name,
        "paramDescription": desc,
        "fillType": "static",
        "staticValue": value,
        "linkParamOutputId": None,
        "required": required,
        "dataType": dtype,
        "isArray": False,
        "question": "",
        "reloadProps": False,
        "remoteOptions": False,
    }


def p_linked(pos, name, desc, dtype, op_key, required=True, is_array=False):
    """Linked input param — linkParamOutputId points to an output param UUID."""
    return {
        "position": pos,
        "paramName": name,
        "paramDescription": desc,
        "fillType": "linked",
        "staticValue": None,
        "linkParamOutputId": OP[op_key],      # ← key: real output param UUID
        "required": required,
        "dataType": dtype,
        "isArray": is_array,
        "question": "",
        "reloadProps": False,
        "remoteOptions": False,
    }


def p_out(op_key, pos, name, desc, dtype, is_array=False):
    return {
        "id": OP[op_key],
        "position": pos,
        "paramName": name,
        "paramDescription": desc,
        "dataType": dtype,
        "isArray": is_array,
        "agentToolConfigurationId": TC[op_key.split(".")[0]],
        "paramPath": None,
        "outputExample": None,
    }


def tool_config(key, fn_name, tool_name, desc, prompt, model, inputs, outputs):
    return {
        "id": TC[key],
        "toolFunctionName": fn_name,
        "toolName": tool_name,
        "description": desc,
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
        "inputParams": inputs,
        "outputParams": outputs,
    }


def node(key, objective, x, y, tc, child_edges, parent_edges,
         is_entry=False, is_exit=False, on_error="STOP",
         enable_retry=False, retry_count=1, retry_wait_ms=1000):
    return {
        "id": N[key],
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
        "toolConfiguration": tc,
        "childEdges": child_edges,
        "parentEdges": parent_edges,
    }


# ── Node definitions ───────────────────────────────────────────────────────────

def build_nodes():

    # ── Node 1: Extract Yardi Data ─────────────────────────────────────────────
    tc_extract = tool_config(
        "extract",
        fn_name="GPTAction_EmptyTool",
        tool_name="SharePoint File Reader",
        desc="Reads CSV files from the Yardi SharePoint export folder",
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
        inputs=[
            p_static(0, "folder_path",
                     "SharePoint folder path containing Yardi CSV exports",
                     "string",
                     "/sites/NovusManagement/Shared Documents/Yardi Exports/Daily"),
            p_static(1, "file_names",
                     "Comma-separated list of CSV files to extract from the folder",
                     "string",
                     "rent_increases.csv, car_park_schedule.csv, storage_schedule.csv"),
        ],
        outputs=[
            p_out("extract.rent_increases",     0, "rent_increases",
                  "Array of rent increase records — unit_id, property, unit_number, tenant_name, "
                  "lease_start, lease_end, current_rent_weekly, proposed_rent_weekly, "
                  "increase_pct, increase_status, effective_date, notice_sent",
                  "object", is_array=True),
            p_out("extract.car_park_schedule",   1, "car_park_schedule",
                  "Array of car park bay records — bay_id, property, bay_number, bay_type, "
                  "tenant_name, unit_id, monthly_rate, lease_start, lease_end, status",
                  "object", is_array=True),
            p_out("extract.storage_schedule",    2, "storage_schedule",
                  "Array of storage cage records — storage_id, property, cage_number, size_sqm, "
                  "tenant_name, unit_id, monthly_rate, lease_start, lease_end, status",
                  "object", is_array=True),
            p_out("extract.extraction_summary",  3, "extraction_summary",
                  "Plain-text summary: record counts per file, any missing or malformed files detected",
                  "string"),
        ],
    )

    n_extract = node(
        "extract",
        objective=(
            "Extract the three source data files from the Yardi SharePoint export folder: "
            "rent_increases.csv, car_park_schedule.csv, and storage_schedule.csv. "
            "Read each CSV file and return the raw data as structured records. "
            "Report the number of records found in each file."
        ),
        x=250, y=150,
        tc=tc_extract,
        child_edges=[E_ET], parent_edges=[],
        is_entry=True,
        enable_retry=True, retry_count=2, retry_wait_ms=3000,
    )

    # ── Node 2: Transform & Validate ───────────────────────────────────────────
    tc_transform = tool_config(
        "transform",
        fn_name="GPTAction_EmptyTool",
        tool_name="Data Transformer",
        desc="Transforms raw CSV data into aggregated report metrics per property and portfolio-wide",
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
        inputs=[
            p_linked(0, "rent_increases",
                     "Raw rent increase records from Node 1 (extract-yardi-data). "
                     "Array of objects with fields: unit_id, property, unit_number, tenant_name, "
                     "lease_start, lease_end, current_rent_weekly, proposed_rent_weekly, "
                     "increase_pct, increase_status, effective_date, notice_sent.",
                     "object", "extract.rent_increases", is_array=True),
            p_linked(1, "car_park_schedule",
                     "Raw car park bay records from Node 1 (extract-yardi-data). "
                     "Array of objects with fields: bay_id, property, bay_number, bay_type, "
                     "tenant_name, unit_id, monthly_rate, lease_start, lease_end, status.",
                     "object", "extract.car_park_schedule", is_array=True),
            p_linked(2, "storage_schedule",
                     "Raw storage cage records from Node 1 (extract-yardi-data). "
                     "Array of objects with fields: storage_id, property, cage_number, size_sqm, "
                     "tenant_name, unit_id, monthly_rate, lease_start, lease_end, status.",
                     "object", "extract.storage_schedule", is_array=True),
        ],
        outputs=[
            p_out("transform.report_data",        0, "report_data",
                  "Transformed report data structured as: { properties: { <property_name>: { "
                  "rent: { unit_count, approved, pending, declined, avg_increase_pct, "
                  "total_current_weekly, total_proposed_weekly, weekly_uplift, annual_uplift }, "
                  "car_park: { total, occupied, vacant, occupancy_pct, monthly_revenue }, "
                  "storage: { total, occupied, vacant, occupancy_pct, monthly_revenue } } }, "
                  "portfolio: { <same aggregated totals> } }",
                  "object"),
            p_out("transform.anomalies",           1, "anomalies",
                  "Array of anomaly objects flagged during validation. Each object: "
                  "{ type: string, property: string, description: string, value: any }. "
                  "Types: HIGH_INCREASE (>10%), EXPIRED_LEASE, MISSING_RATE.",
                  "object", is_array=True),
            p_out("transform.validation_summary",  2, "validation_summary",
                  "Plain-text summary: total records processed, number of properties found, "
                  "count of anomalies flagged, any data quality issues.",
                  "string"),
        ],
    )

    n_transform = node(
        "transform",
        objective=(
            "Transform and validate the raw Yardi data into report-ready structures.\n\n"
            "For each property, calculate:\n"
            "- Rent increases: count by status (Approved/Pending/Declined), average increase %,\n"
            "  total current vs proposed weekly rent, weekly and annual uplift amounts\n"
            "- Car park: total bays, occupied vs vacant, occupancy %,\n"
            "  total monthly revenue from occupied bays\n"
            "- Storage: total cages, occupied vs vacant, occupancy %,\n"
            "  total monthly revenue from occupied cages\n\n"
            "Also calculate portfolio-wide totals across all properties.\n\n"
            "Flag anomalies: rent increases > 10%, expired leases, occupied units missing rates."
        ),
        x=550, y=150,
        tc=tc_transform,
        child_edges=[E_TR], parent_edges=[E_ET],
    )

    # ── Node 3: Generate Report ────────────────────────────────────────────────
    tc_report = tool_config(
        "report",
        fn_name="GPTAction_EmptyTool",
        tool_name="Report Generator",
        desc="Generates a formatted Pricing Matrix HTML report from transformed data",
        prompt=(
            "You are a report generation agent for Novus Management property reporting.\n\n"
            "Generate a professional Pricing Matrix Report from the provided data.\n"
            "The report should be clear, data-dense, and suitable for executive review.\n\n"
            "Structure:\n"
            "1. Header: 'Pricing Matrix Report' with today's date and Novus Management branding\n"
            "2. Portfolio KPI dashboard: total units, approved/pending/declined counts,\n"
            "   average increase %, weekly uplift, annual uplift,\n"
            "   car park occupancy & revenue, storage occupancy & revenue\n"
            "3. Per-property sections:\n"
            "   - Property KPI summary row\n"
            "   - Rent increase table: unit, tenant, current rent, proposed rent, increase %, status, effective date, notice sent\n"
            "   - Car park table: bay, type, tenant, rate, status\n"
            "   - Storage table: cage, size, tenant, rate, status\n"
            "   - Occupancy and revenue footer\n"
            "4. Anomaly callouts if any exist\n"
            "5. Footer: Beam AI x Novus, report date, agent version\n\n"
            "Output the report as formatted HTML that can be viewed in a browser."
        ),
        model="BEDROCK_CLAUDE_OPUS_4_5",
        inputs=[
            p_linked(0, "report_data",
                     "Transformed report data from Node 2 (transform-validate). "
                     "Object with keys: properties (per-property breakdown with rent/car_park/storage metrics) "
                     "and portfolio (same metrics aggregated across all properties).",
                     "object", "transform.report_data"),
            p_linked(1, "anomalies",
                     "Array of anomaly objects from Node 2 (transform-validate). "
                     "Each: { type, property, description, value }. "
                     "Include in report as a flagged section if array is non-empty.",
                     "object", "transform.anomalies", is_array=True),
        ],
        outputs=[
            p_out("report.report_html",    0, "report_html",
                  "Complete HTML document for the Pricing Matrix Report. "
                  "Self-contained with inline CSS, suitable for browser viewing or PDF export.",
                  "string"),
            p_out("report.report_summary", 1, "report_summary",
                  "One-paragraph executive summary of the report: total units reviewed, "
                  "approved/pending counts, average increase %, total weekly and annual uplift, "
                  "car park and storage occupancy rates, and anomaly count if any.",
                  "string"),
        ],
    )

    n_report = node(
        "report",
        objective=(
            "Generate the Pricing Matrix Report as a formatted HTML document.\n\n"
            "Include: header with date and branding, portfolio KPI dashboard, "
            "per-property sections (rent table, car park table, storage table, occupancy footer), "
            "anomaly callouts, and footer. Suitable for executive review."
        ),
        x=850, y=150,
        tc=tc_report,
        child_edges=[E_RN], parent_edges=[E_TR],
    )

    # ── Node 4: Notify Team ────────────────────────────────────────────────────
    tc_notify = tool_config(
        "notify",
        fn_name="GPTAction_EmptyTool",
        tool_name="Slack Notifier",
        desc="Sends Pricing Matrix Report completion notification to #novus-reports Slack channel",
        prompt=(
            "Send a concise Slack notification about the completed Pricing Matrix Report.\n\n"
            "Format the message as:\n"
            "\u2705 *Pricing Matrix Report \u2014 [today's date]*\n\n"
            "\ud83d\udcca *Portfolio Summary*\n"
            "\u2022 [total units] units | [approved] approved | [pending] pending\n"
            "\u2022 Weekly uplift: $[amount] | Annual: $[amount]\n"
            "\u2022 Car park: [X]% occupied | Storage: [X]% occupied\n\n"
            "[If anomalies array is non-empty: \u26a0\ufe0f [N] anomalies flagged \u2014 review report for details]\n\n"
            "_Report generated by Beam AI agent_\n\n"
            "Post to the channel specified in the channel input param."
        ),
        model="BEDROCK_CLAUDE_SONNET_4",
        inputs=[
            p_static(0, "channel",
                     "Slack channel to post the notification to",
                     "string", "#novus-reports"),
            p_linked(1, "report_summary",
                     "One-paragraph executive summary from Node 3 (generate-report). "
                     "Use this to extract portfolio metrics for the Slack message body.",
                     "string", "report.report_summary"),
            p_linked(2, "anomalies",
                     "Array of anomaly objects from Node 2 (transform-validate). "
                     "If non-empty, include anomaly count warning in Slack message.",
                     "object", "transform.anomalies",
                     required=False, is_array=True),
        ],
        outputs=[
            p_out("notify.notification_status", 0, "notification_status",
                  "Confirmation that the Slack notification was sent. "
                  "Includes channel name, timestamp, and message ID if available.",
                  "string"),
        ],
    )

    n_notify = node(
        "notify",
        objective=(
            "Send a Slack notification to the #novus-reports channel confirming "
            "the Pricing Matrix Report has been generated. Include key portfolio metrics: "
            "total units, approved/pending counts, weekly and annual uplift, "
            "car park and storage occupancy rates. "
            "Mention anomaly count if any were flagged."
        ),
        x=1150, y=150,
        tc=tc_notify,
        child_edges=[], parent_edges=[E_RN],
        on_error="CONTINUE",   # Slack failure must not block the workflow
    )

    return [n_extract, n_transform, n_report, n_notify]


# ── Payload ────────────────────────────────────────────────────────────────────

def build_payload():
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
        "nodes": build_nodes(),
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Push Novus Pricing Matrix graph to draft")
    parser.add_argument("--dry-run",  action="store_true", help="Print payload without calling API")
    parser.add_argument("--publish",  action="store_true", help="Publish after pushing")
    args = parser.parse_args()

    env = load_env()
    api_key      = env.get("BEAM_API_KEY")      or os.getenv("BEAM_API_KEY")
    workspace_id = env.get("BEAM_WORKSPACE_ID") or os.getenv("BEAM_WORKSPACE_ID")

    if not api_key:
        sys.exit("ERROR: BEAM_API_KEY not set")
    if not workspace_id:
        sys.exit("ERROR: BEAM_WORKSPACE_ID not set")

    payload = build_payload()
    nodes   = payload["nodes"]

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        print(f"\n=== DRY RUN — {len(nodes)} nodes, no API call ===", file=sys.stderr)
        # Print link summary
        print("\nLink summary:", file=sys.stderr)
        for n in nodes:
            tc = n.get("toolConfiguration", {})
            for ip in tc.get("inputParams", []):
                if ip["fillType"] == "linked":
                    print(f"  {tc['toolName']}.{ip['paramName']} "
                          f"← linkParamOutputId={ip['linkParamOutputId']}", file=sys.stderr)
        return

    params = {"saveAndPublish": "true"} if args.publish else {}
    url    = f"{BASE_URL}/agent-graphs/{AGENT_ID}"

    print(f"Pushing {len(nodes)}-node graph to {url}")
    for n in nodes:
        tc = n.get("toolConfiguration", {})
        linked = [ip["paramName"] for ip in tc.get("inputParams", []) if ip["fillType"] == "linked"]
        print(f"  {tc['toolName']:30s}  {len(tc.get('inputParams',[]))} in / "
              f"{len(tc.get('outputParams',[]))} out"
              + (f"  linked={linked}" if linked else ""))

    resp = requests.put(url, headers=headers(api_key, workspace_id),
                        json=payload, params=params, timeout=60)

    if resp.status_code in (200, 201):
        r = resp.json()
        print("\nGraph pushed successfully!")
        print(f"  Agent ID:    {r.get('agentId')}")
        print(f"  Draft Graph: {r.get('draftGraphId')}")
        print(f"  Published:   {'Yes' if args.publish else 'No (draft)'}")
    else:
        print(f"\nError {resp.status_code}:", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
