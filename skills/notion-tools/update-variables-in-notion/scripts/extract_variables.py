#!/usr/bin/env python3
"""
Extract variables from Beam prompt chain files.

Extracts JSON schema fields from output format specifications in .md files.
Parses JSON structures to identify field names, data types, and descriptions.
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


def extract_json_blocks(content: str) -> List[tuple]:
    """Extract all JSON code blocks from markdown content."""
    # Pattern to match ```json ... ``` blocks
    pattern = r'```json\s*\n(.*?)\n```'
    matches = []

    for match in re.finditer(pattern, content, re.DOTALL):
        json_str = match.group(1)
        start_pos = match.start()
        matches.append((json_str, start_pos))

    return matches


def infer_type_from_value(value: Any, comment: str = "") -> tuple:
    """
    Infer data type and possible values from JSON value or comment.

    Returns: (data_type, possible_values)
    """
    possible_values = ""

    # Check comment first for type hints
    comment_lower = comment.lower()

    if 'string' in comment_lower:
        data_type = 'string'
    elif 'number' in comment_lower or 'integer' in comment_lower:
        data_type = 'number'
    elif 'boolean' in comment_lower or 'bool' in comment_lower:
        data_type = 'boolean'
    elif 'array' in comment_lower or 'list' in comment_lower or '[' in comment:
        data_type = 'array'
    elif 'object' in comment_lower or '{' in comment:
        data_type = 'object'
    # Infer from value type
    elif isinstance(value, str):
        # Check for type indicators in string value
        if 'null' in value.lower():
            data_type = 'string or null'
            possible_values = value  # Capture full string like "string or null"
        elif '|' in value:  # Enum type like "CNA | RN | LPN"
            data_type = 'string (enum)'
            possible_values = value  # Capture enum values
        elif 'YYYY-MM-DD' in value or 'YYYY-MM' in value:
            data_type = 'string (date)'
            possible_values = value  # Capture format
        elif 'boolean' in value.lower():
            data_type = 'boolean'
            if 'null' in value.lower():
                possible_values = "true | false | null"
        elif value.lower() in ['true', 'false']:
            data_type = 'boolean'
        else:
            data_type = 'string'
    elif isinstance(value, (int, float)):
        data_type = 'number'
    elif isinstance(value, bool):
        data_type = 'boolean'
    elif isinstance(value, list):
        data_type = 'array'
        # Check if it's an array with example values
        if len(value) > 0 and isinstance(value[0], str):
            possible_values = f"Array of: {value[0]}"
    elif isinstance(value, dict):
        data_type = 'object'
    else:
        data_type = 'unknown'

    return (data_type, possible_values)


def extract_description_from_context(field_name: str, content: str) -> str:
    """
    Extract description for a field from prompt content.

    Searches for explanations of the field in the surrounding text,
    focusing on step-by-step instructions and explanatory sections.
    """
    # Clean up field name for matching (remove parent prefixes)
    clean_field = field_name.split('.')[-1].replace('_', ' ')

    # Also try partial matches for compound fields
    # e.g., "location_city" -> also search for "location"
    partial_terms = []
    if '_' in field_name.split('.')[-1]:
        parts = field_name.split('.')[-1].split('_')
        partial_terms = [p for p in parts if len(p) > 3]  # Skip short words like "has", "is"

    # Search for mentions of this field in the content (only in non-JSON sections)
    lines = content.split('\n')
    description_parts = []
    in_json_block = False

    for i, line in enumerate(lines):
        # Track JSON code blocks
        if line.strip().startswith('```'):
            in_json_block = not in_json_block
            continue

        # Skip lines inside JSON blocks
        if in_json_block:
            continue

        # Skip lines that look like JSON (contain ":", "{", "}", "[", "]", etc.)
        if any(char in line for char in ['{', '}', '":', '",', '[']):
            continue

        # Look for lines that mention this field (exact or partial match)
        field_mentioned = clean_field.lower() in line.lower()
        partial_mentioned = any(term.lower() in line.lower() for term in partial_terms) if partial_terms else False

        if field_mentioned or partial_mentioned:
            # Skip if we've passed the instructions section
            section_check = '\n'.join(lines[max(0, i-50):i])
            if '## Output Format' in section_check and '## Step' not in section_check:
                continue

            # Check if this is an explanatory line (bullet points)
            line_stripped = line.strip()
            if line_stripped.startswith('-') or (line.startswith('  -') and not line.startswith('    -')):
                # Extract the explanation part
                explanation = line_stripped.lstrip('- ').strip()

                # Clean up: remove field name from beginning if it's there
                for term in [clean_field] + partial_terms:
                    if explanation.lower().startswith(term.lower()):
                        explanation = explanation[len(term):].strip(':- ').strip()
                        break

                # For nested items, also look at the parent bullet context
                # e.g., "License type (CNA, RN, LPN)" under "Extract license information:"
                if line.startswith('  -') and i > 0:
                    # Look back for parent bullet
                    for j in range(i-1, max(0, i-5), -1):
                        parent_line = lines[j].strip()
                        if parent_line.startswith('-') and parent_line.endswith(':'):
                            # Found parent context, prepend it
                            parent_text = parent_line.rstrip(':').lstrip('- ').strip()
                            explanation = f"{parent_text}: {explanation}"
                            break

                # Filter out generic/unhelpful descriptions
                generic_patterns = [
                    '**Well-formatted resumes**',
                    '**Poorly-formatted resumes**',
                    'Clear sections',
                    'Missing sections'
                ]

                # Accept if it looks like a real explanation and isn't too generic
                is_generic = any(pattern in explanation for pattern in generic_patterns)
                is_specific = field_mentioned  # Exact field name match = specific

                if explanation and len(explanation) > 15 and not explanation.startswith('{'):
                    if is_specific or not is_generic:
                        description_parts.append(explanation)
                        if field_mentioned:  # Exact match, stop here
                            break

    # Return the first description found
    if description_parts:
        result = description_parts[0][:250]  # Limit to 250 chars
        # Clean up trailing incomplete sentences
        if '(' in result and ')' not in result:
            result = result.split('(')[0].strip()
        return result

    return ""


def extract_description(key: str, value: Any, parent_desc: str = "") -> str:
    """Extract description from value or comments."""
    # If value is a string that looks like a description/comment
    if isinstance(value, str):
        # Check if it's a descriptive string (not a placeholder value)
        if len(value) > 50 or any(word in value.lower() for word in ['explaining', 'describing', 'sentences', 'documenting']):
            return value[:200]  # Truncate long descriptions

    return ""


def flatten_json_schema(data: Any, parent_key: str = '', separator: str = '.') -> List[Dict[str, Any]]:
    """
    Recursively flatten nested JSON schema into list of fields.

    Returns list of dicts with: name, data_type, possible_values, description
    """
    fields = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key

            # Determine data type and possible values
            data_type, possible_values = infer_type_from_value(value)

            # Extract description
            description = extract_description(key, value)

            # For objects and arrays, generate description about nested structure
            nested_info = ""
            if isinstance(value, dict) and len(value) > 0:
                # Object type - list child fields
                child_keys = list(value.keys())[:5]  # First 5 fields
                nested_info = f"Object with fields: {', '.join(child_keys)}"
                if len(value) > 5:
                    nested_info += f" (and {len(value) - 5} more)"
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                # Array of objects - list fields in each object
                child_keys = list(value[0].keys())[:5]
                nested_info = f"Array of objects, each with: {', '.join(child_keys)}"
                if len(value[0]) > 5:
                    nested_info += f" (and {len(value[0]) - 5} more)"

            # Combine description with nested info
            if nested_info:
                if description:
                    description = f"{description} | {nested_info}"
                else:
                    description = nested_info

            # Add this field
            fields.append({
                'name': new_key,
                'data_type': data_type,
                'possible_values': possible_values,
                'description': description
            })

            # Recursively process nested objects (but not if it's a descriptive string)
            if isinstance(value, dict):
                nested_fields = flatten_json_schema(value, new_key, separator)
                fields.extend(nested_fields)
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                # Handle arrays of objects
                nested_fields = flatten_json_schema(value[0], f"{new_key}[]", separator)
                fields.extend(nested_fields)

    return fields


def extract_variables_from_json_schema(json_str: str, file_path: Path, block_start_pos: int, full_content: str = "") -> List[Dict[str, Any]]:
    """Parse JSON schema and extract all fields."""
    try:
        # Try to parse as JSON
        # First, remove comments and clean up
        cleaned = re.sub(r'//.*', '', json_str)  # Remove // comments
        cleaned = re.sub(r',\s*}', '}', cleaned)  # Remove trailing commas
        cleaned = re.sub(r',\s*]', ']', cleaned)  # Remove trailing commas in arrays

        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # If parsing fails, try to extract fields manually
        print(f"Warning: Could not parse JSON in {file_path}: {e}", file=sys.stderr)
        return []

    # Flatten the schema
    fields = flatten_json_schema(data)

    # Extract descriptions from prompt content
    if full_content:
        for field in fields:
            if not field['description']:  # Only if no description from JSON
                field['description'] = extract_description_from_context(field['name'], full_content)

    # Add metadata
    node_name = file_path.stem

    variables = []
    for field in fields:
        # Skip fields that are just descriptions (reasoning fields often contain long text)
        if len(field['description']) > 100:
            continue

        variables.append({
            'name': field['name'],
            'node': node_name,
            'file_path': str(file_path),
            'data_type': field['data_type'],
            'possible_values': field['possible_values'],
            'description': field['description'],
            'context': ''  # Context not applicable for JSON schema fields
        })

    return variables


def extract_variables_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """Extract all variables from a single .md file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return []

    all_variables = []

    # Extract JSON blocks
    json_blocks = extract_json_blocks(content)

    if not json_blocks:
        print(f"No JSON blocks found in {file_path}", file=sys.stderr)
        return []

    # Process each JSON block
    for json_str, block_start_pos in json_blocks:
        variables = extract_variables_from_json_schema(json_str, file_path, block_start_pos, content)
        all_variables.extend(variables)

    # Remove duplicates by name (keep first occurrence)
    seen = set()
    unique_variables = []
    for var in all_variables:
        if var['name'] not in seen:
            seen.add(var['name'])
            unique_variables.append(var)

    return unique_variables


def scan_directory(dir_path: Path) -> List[Dict[str, Any]]:
    """Scan directory for all .md files and extract variables."""
    all_variables = []

    # Find all .md files
    md_files = list(dir_path.rglob('*.md'))

    if not md_files:
        print(f"No .md files found in {dir_path}", file=sys.stderr)
        return []

    print(f"Found {len(md_files)} .md files", file=sys.stderr)

    for md_file in md_files:
        variables = extract_variables_from_file(md_file)
        all_variables.extend(variables)

    return all_variables


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python extract_variables.py <file_or_directory_path>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: Path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Extract variables
    if input_path.is_file():
        if not input_path.suffix == '.md':
            print(f"Error: File must be .md format: {input_path}", file=sys.stderr)
            sys.exit(1)
        variables = extract_variables_from_file(input_path)
    elif input_path.is_dir():
        variables = scan_directory(input_path)
    else:
        print(f"Error: Invalid path: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Output JSON
    output = {
        'source': str(input_path),
        'variables_count': len(variables),
        'variables': variables
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
