"""Main dispatcher and CLI entry point for dataset export.

Usage:
    python export.py data_generated.json --format csv,pdf,docx,xls

Dependencies: openpyxl, fpdf2, python-docx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure sibling modules are importable when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import load_json
from csv_export import export_to_csv
from xlsx_export import export_to_xlsx
from pdf_export import export_to_pdf
from docx_export import export_to_docx

_FORMAT_MAP = {
    "csv": export_to_csv,
    "xlsx": export_to_xlsx,
    "xls": export_to_xlsx,
    "pdf": export_to_pdf,
    "docx": export_to_docx,
}


def export_generated(
    json_path: str | Path,
    output_path: str | Path | None = None,
    fmt: str = "csv",
) -> list[Path]:
    """Export a generated JSON dataset to one or more formats.

    Args:
        json_path: Path to the generated JSON file.
        output_path: Base output path (without extension). Defaults to same
            directory/name as json_path.
        fmt: Comma-separated formats: csv, xlsx/xls, pdf, docx.

    Returns:
        List of created file paths.
    """
    data = load_json(json_path)
    base = Path(output_path) if output_path else Path(json_path).with_suffix("")

    formats = [f.strip().lower() for f in fmt.split(",")]
    results: list[Path] = []

    for f in formats:
        exporter = _FORMAT_MAP.get(f)
        if exporter is None:
            raise ValueError(f"Unsupported format: {f!r}. Choose from: {', '.join(_FORMAT_MAP)}")
        result = exporter(data, base)
        results.append(result)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export generated JSON to various formats")
    parser.add_argument("json_path", help="Path to generated JSON file")
    parser.add_argument("--output", "-o", help="Base output path (without extension)")
    parser.add_argument(
        "--format", "-f",
        default="csv",
        help="Comma-separated formats: csv, xlsx, xls, pdf, docx (default: csv)",
    )

    args = parser.parse_args()
    paths = export_generated(args.json_path, args.output, args.format)
    for p in paths:
        print(f"Created: {p}")
