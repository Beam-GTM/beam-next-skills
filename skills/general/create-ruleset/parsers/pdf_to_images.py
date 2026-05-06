"""Convert PDF pages to images for visual reading by Claude.

When pdfplumber text extraction produces garbled output (design-heavy PDFs,
scanned documents, complex layouts), this script renders each page as a PNG
image that Claude can read visually via the Read tool.

Usage:
    python pdf_to_images.py <path_to_pdf> [--pages 1-5] [--output-dir /tmp/pdf_pages]
    python pdf_to_images.py <path_to_pdf> --dpi 200

Dependencies:
    pypdfium2 (already installed as a pdfplumber dependency)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pypdfium2 as pdfium
except ImportError:
    print("Error: pypdfium2 is required. It should already be installed with pdfplumber.")
    sys.exit(1)


def pdf_to_images(
    pdf_path: str | Path,
    output_dir: str | Path | None = None,
    pages: str | None = None,
    dpi: int = 150,
) -> list[Path]:
    """Render PDF pages as PNG images.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save images. Defaults to /tmp/pdf_pages/<pdf_stem>/
        pages: Optional page range string (e.g., "1-5", "3", "1,3,5").
        dpi: Resolution for rendering (default: 150, good balance of quality and size).

    Returns:
        List of paths to the generated PNG images.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if output_dir is None:
        output_dir = Path("/tmp/pdf_pages") / pdf_path.stem
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    page_indices = _parse_page_range(pages) if pages else None

    doc = pdfium.PdfDocument(str(pdf_path))
    total_pages = len(doc)
    target_pages = page_indices if page_indices else list(range(total_pages))

    image_paths = []
    scale = dpi / 72  # PDF points are 1/72 inch

    for i in target_pages:
        if i >= total_pages:
            continue
        page = doc[i]
        bitmap = page.render(scale=scale)
        image = bitmap.to_pil()

        image_path = output_dir / f"page_{i + 1:03d}.png"
        image.save(str(image_path))
        image_paths.append(image_path)

    doc.close()
    return image_paths


def _parse_page_range(pages_str: str) -> list[int]:
    """Parse a page range string into a list of 0-based page indices."""
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
    parser = argparse.ArgumentParser(description="Convert PDF pages to images for visual reading")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--pages", help="Page range (e.g., '1-5', '3', '1,3,5')", default=None)
    parser.add_argument("--output-dir", help="Output directory for images", default=None)
    parser.add_argument("--dpi", type=int, default=150, help="Resolution (default: 150)")
    args = parser.parse_args()

    image_paths = pdf_to_images(args.pdf_path, args.output_dir, args.pages, args.dpi)
    print(f"Generated {len(image_paths)} page images:")
    for p in image_paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
