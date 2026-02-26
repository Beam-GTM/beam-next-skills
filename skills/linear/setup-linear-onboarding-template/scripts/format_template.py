#!/usr/bin/env python3
"""
Format Linear project data into an onboarding template markdown file.

Usage:
    python format_template.py <project_json_file> <issues_json_file> <output_file>

Example:
    python format_template.py project.json issues.json client-template.md
"""

import json
import sys
from datetime import datetime


def format_project_template(project_data, issues_data):
    """Format Linear project and issues data into markdown template."""

    # Extract project information
    project_name = project_data.get('name', 'N/A')
    project_url = project_data.get('url', '')
    project_description = project_data.get('description', '')
    project_status = project_data.get('status', {}).get('name', 'N/A')
    created_at = project_data.get('createdAt', 'N/A')
    updated_at = project_data.get('updatedAt', 'N/A')

    # Format lead information
    lead = project_data.get('lead', {})
    lead_name = lead.get('name', 'N/A') if lead else 'N/A'

    # Format labels
    labels = project_data.get('labels', [])
    labels_str = ', '.join([label.get('name', '') for label in labels]) if labels else 'None'

    # Build markdown content
    markdown = f"""# {project_name} - Onboarding Template

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Project Overview

{project_description}

---

## Project Properties

| Property | Value |
|----------|-------|
| **Name** | {project_name} |
| **Status** | {project_status} |
| **Lead** | {lead_name} |
| **Labels** | {labels_str} |
| **Created** | {created_at} |
| **Updated** | {updated_at} |
| **Linear URL** | {project_url} |

---

## Issues List

Total Issues: {len(issues_data)}

"""

    # Add issues table
    if issues_data:
        markdown += "| # | Issue | Status | Link |\n"
        markdown += "|---|-------|--------|------|\n"

        for idx, issue in enumerate(issues_data, 1):
            title = issue.get('title', 'N/A')
            identifier = issue.get('identifier', 'N/A')
            status = issue.get('status', 'N/A')
            url = issue.get('url', '')

            markdown += f"| {idx} | {identifier}: {title} | {status} | [Link]({url}) |\n"
    else:
        markdown += "*No issues found in this project.*\n"

    markdown += "\n---\n\n*This template was generated from Linear project data.*\n"

    return markdown


def main():
    if len(sys.argv) != 4:
        print("Usage: python format_template.py <project_json_file> <issues_json_file> <output_file>")
        sys.exit(1)

    project_file = sys.argv[1]
    issues_file = sys.argv[2]
    output_file = sys.argv[3]

    # Read input files
    try:
        with open(project_file, 'r') as f:
            project_data = json.load(f)

        with open(issues_file, 'r') as f:
            issues_data = json.load(f)

        # Format the template
        markdown_content = format_project_template(project_data, issues_data)

        # Write output file
        with open(output_file, 'w') as f:
            f.write(markdown_content)

        print(f"✅ Template generated successfully: {output_file}")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
