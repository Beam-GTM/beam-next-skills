"""CSV reader with column type inference.

Reads a CSV file and returns column names, inferred types
(string/number/date/enum), and the first 5 sample rows.

Usage:
    python csv_reader.py <path_to_csv> [--sample-rows 5]

No external dependencies required (stdlib only).
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# Common date patterns
_DATE_PATTERNS = [
    re.compile(r"^\d{4}-\d{2}-\d{2}$"),  # 2024-01-15
    re.compile(r"^\d{2}/\d{2}/\d{4}$"),  # 01/15/2024
    re.compile(r"^\d{2}\.\d{2}\.\d{4}$"),  # 15.01.2024
    re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}"),  # ISO datetime
]

# Max unique values to consider a column an enum
_ENUM_THRESHOLD = 20
# Min ratio of repeated values to consider enum
_ENUM_REPEAT_RATIO = 0.5


def _is_number(value: str) -> bool:
    """Check if a string represents a number."""
    try:
        float(value.replace(",", ""))
        return True
    except ValueError:
        return False


def _is_date(value: str) -> bool:
    """Check if a string matches common date patterns."""
    return any(p.match(value) for p in _DATE_PATTERNS)


def _infer_column_type(values: list[str]) -> str:
    """Infer the type of a column from its non-empty values."""
    non_empty = [v.strip() for v in values if v.strip()]
    if not non_empty:
        return "string"

    # Check number
    if all(_is_number(v) for v in non_empty):
        return "number"

    # Check date
    if all(_is_date(v) for v in non_empty):
        return "date"

    # Check enum: few unique values relative to total
    unique = set(non_empty)
    if (
        len(unique) <= _ENUM_THRESHOLD
        and len(non_empty) > 1
        and len(unique) / len(non_empty) <= _ENUM_REPEAT_RATIO
    ):
        return f"enum({', '.join(sorted(unique))})"

    return "string"


def read_csv(csv_path: str | Path, sample_rows: int = 5) -> dict:
    """Read a CSV and return structured summary with type inference.

    Args:
        csv_path: Path to the CSV file.
        sample_rows: Number of sample rows to include (default: 5).

    Returns:
        Dict with keys: file, columns, row_count, sample_rows.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    # Detect delimiter by sniffing
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(8192)
        try:
            dialect = csv.Sniffer().sniff(sample)
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ","

    # Read all rows
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        columns = reader.fieldnames or []
        rows = list(reader)

    # Infer types from all values
    column_info = []
    for col in columns:
        col_values = [row.get(col, "") for row in rows]
        inferred_type = _infer_column_type(col_values)
        column_info.append({"name": col, "type": inferred_type})

    return {
        "file": str(csv_path),
        "row_count": len(rows),
        "columns": column_info,
        "sample_rows": rows[:sample_rows],
    }


def format_summary(result: dict) -> str:
    """Format the CSV reading result as a readable markdown summary."""
    lines = [f"# {Path(result['file']).name}", f"\n**Rows:** {result['row_count']}\n"]

    # Column table
    lines.append("## Columns\n")
    lines.append("| Column | Type |")
    lines.append("| --- | --- |")
    for col in result["columns"]:
        lines.append(f"| {col['name']} | {col['type']} |")

    # Sample rows
    lines.append(f"\n## Sample Rows (first {len(result['sample_rows'])})\n")
    if result["sample_rows"]:
        col_names = [c["name"] for c in result["columns"]]
        lines.append("| " + " | ".join(col_names) + " |")
        lines.append("| " + " | ".join("---" for _ in col_names) + " |")
        for row in result["sample_rows"]:
            cells = [str(row.get(c, "")) for c in col_names]
            lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Read CSV with column type inference")
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("--sample-rows", type=int, default=5, help="Number of sample rows (default: 5)")
    args = parser.parse_args()

    result = read_csv(args.csv_path, args.sample_rows)
    print(format_summary(result))


if __name__ == "__main__":
    main()
