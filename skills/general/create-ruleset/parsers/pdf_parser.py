"""PDF text extraction with layout awareness using pdfplumber.

Extracts text from PDFs preserving table structure (rows/columns intact).
Tables are output as markdown tables, regular text as paragraphs.

Usage:
    python pdf_parser.py <path_to_pdf> [--pages 1-5]

Dependencies:
    pip install pdfplumber
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is required. Install with: pip install pdfplumber")
    sys.exit(1)


def extract_tables_as_markdown(page: pdfplumber.page.Page) -> list[str]:
    """Extract all tables from a page as markdown tables."""
    markdown_tables = []
    for table in page.extract_tables():
        if not table or not table[0]:
            continue
        # Build markdown table
        lines = []
        headers = [str(cell or "").strip() for cell in table[0]]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in table[1:]:
            cells = [str(cell or "").strip() for cell in row]
            lines.append("| " + " | ".join(cells) + " |")
        markdown_tables.append("\n".join(lines))
    return markdown_tables


def get_table_bboxes(page: pdfplumber.page.Page) -> list[tuple]:
    """Get bounding boxes of all tables on a page."""
    bboxes = []
    for table in page.find_tables():
        bboxes.append(table.bbox)
    return bboxes


def extract_non_table_text(page: pdfplumber.page.Page, table_bboxes: list[tuple]) -> str:
    """Extract text from page regions outside of table bounding boxes."""
    if not table_bboxes:
        return (page.extract_text() or "").strip()

    # Crop out table regions and extract remaining text
    filtered_page = page
    for bbox in table_bboxes:
        # Filter out characters within table bounding boxes
        filtered_page = filtered_page.filter(
            lambda obj, bb=bbox: not (
                bb[0] <= obj.get("x0", 0) <= bb[2]
                and bb[1] <= obj.get("top", 0) <= bb[3]
            )
        )
    return (filtered_page.extract_text() or "").strip()


def parse_pdf(pdf_path: str | Path, pages: str | None = None) -> str:
    """Parse a PDF file and return structured markdown content.

    Args:
        pdf_path: Path to the PDF file.
        pages: Optional page range string (e.g., "1-5", "3", "1,3,5").

    Returns:
        Structured markdown string with tables and text.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    page_indices = _parse_page_range(pages) if pages else None

    sections = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        target_pages = page_indices if page_indices else range(total_pages)

        for i in target_pages:
            if i >= total_pages:
                continue
            page = pdf.pages[i]
            page_sections = []
            page_sections.append(f"## Page {i + 1}")

            # Extract tables and their bounding boxes
            table_bboxes = get_table_bboxes(page)
            tables_md = extract_tables_as_markdown(page)

            # Extract non-table text
            text = extract_non_table_text(page, table_bboxes)
            if text:
                page_sections.append(text)

            # Add tables
            for table_md in tables_md:
                page_sections.append(table_md)

            sections.append("\n\n".join(page_sections))

    return f"# {pdf_path.name}\n\n" + "\n\n---\n\n".join(sections)


def _parse_page_range(pages_str: str) -> list[int]:
    """Parse a page range string into a list of 0-based page indices.

    Supports: "1-5", "3", "1,3,5", "1-3,7,9-11"
    """
    indices = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            indices.extend(range(int(start) - 1, int(end)))
        else:
            indices.append(int(part) - 1)
    return sorted(set(indices))


def main():
    parser = argparse.ArgumentParser(description="Extract structured content from PDF files")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--pages", help="Page range (e.g., '1-5', '3', '1,3,5')", default=None)
    args = parser.parse_args()

    result = parse_pdf(args.pdf_path, args.pages)
    print(result)


if __name__ == "__main__":
    main()
