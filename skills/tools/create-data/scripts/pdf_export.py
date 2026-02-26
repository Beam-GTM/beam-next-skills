"""PDF export with randomized layout and styling variations.

Variations per export:
- Layout: table-based, per-entry sections, compact overview
- Font: Helvetica, Courier, Times
- Optional: cover page with summary stats
- Optional: header/footer with page numbers
"""

from __future__ import annotations

import json
import random
import textwrap
from pathlib import Path
from typing import Any

from helpers import truncate

_FONTS = ["Helvetica", "Courier", "Times"]


def export_to_pdf(data: list[dict[str, Any]], path: str | Path) -> Path:
    """Export data to PDF with randomized layout and styling."""
    from fpdf import FPDF, XPos, YPos

    dest = Path(path).with_suffix(".pdf")
    dest.parent.mkdir(parents=True, exist_ok=True)

    layout = random.choice(["table", "sections", "compact"])
    font_family = random.choice(_FONTS)
    use_cover = random.choice([True, False])
    use_header_footer = random.choice([True, False])

    class StyledPDF(FPDF):
        def __init__(self, show_hf: bool, font_fam: str):
            super().__init__()
            self._show_hf = show_hf
            self._font_fam = font_fam

        def header(self):
            if self._show_hf and self.page_no() > (2 if use_cover else 1):
                self.set_font(self._font_fam, "I", 8)
                self.cell(0, 5, "Generated Dataset Export", align="C")
                self.ln(8)

        def footer(self):
            if self._show_hf:
                self.set_y(-15)
                self.set_font(self._font_fam, "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = StyledPDF(use_header_footer, font_family)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    if use_cover:
        pdf.add_page()
        pdf.set_font(font_family, "B", 24)
        pdf.ln(60)
        pdf.cell(0, 15, "Dataset Export Report", align="C")
        pdf.ln(15)
        pdf.set_font(font_family, "", 14)
        pdf.cell(0, 10, f"Total Entries: {len(data)}", align="C")
        pdf.ln(8)
        scores = [
            (e.get("metadata") or {}).get("quality_score")
            for e in data
            if (e.get("metadata") or {}).get("quality_score") is not None
        ]
        if scores:
            pdf.cell(0, 10, f"Avg Quality: {sum(scores) / len(scores):.1f}", align="C")

    if layout == "table":
        _table_layout(pdf, data, font_family)
    elif layout == "sections":
        _section_layout(pdf, data, font_family)
    else:
        _compact_layout(pdf, data, font_family)

    pdf.output(str(dest))
    return dest


def _table_layout(pdf, data: list[dict[str, Any]], font: str):
    from fpdf import XPos, YPos

    pdf.add_page()
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 10, "Dataset Entries", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    col_w = [15, 70, 70, 35]
    pdf.set_font(font, "B", 9)
    headers = ["#", "Input", "Output", "Score"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1)
    pdf.ln()

    pdf.set_font(font, "", 8)
    for idx, entry in enumerate(data, 1):
        inp = truncate(entry.get("input", ""), 200)
        out = truncate(entry.get("output", ""), 200)
        score = str((entry.get("metadata") or {}).get("quality_score", ""))
        row_h = max(pdf.get_string_width(inp) / col_w[1], pdf.get_string_width(out) / col_w[2], 1) * 4 + 4
        row_h = max(row_h, 8)
        row_h = min(row_h, 40)

        if pdf.get_y() + row_h > pdf.h - 25:
            pdf.add_page()
            pdf.set_font(font, "B", 9)
            for i, h in enumerate(headers):
                pdf.cell(col_w[i], 7, h, border=1)
            pdf.ln()
            pdf.set_font(font, "", 8)

        y_before = pdf.get_y()
        x_start = pdf.get_x()
        pdf.multi_cell(col_w[0], row_h, str(idx), border=1)
        pdf.set_xy(x_start + col_w[0], y_before)
        pdf.multi_cell(col_w[1], row_h, inp[:200], border=1)
        pdf.set_xy(x_start + col_w[0] + col_w[1], y_before)
        pdf.multi_cell(col_w[2], row_h, out[:200], border=1)
        pdf.set_xy(x_start + col_w[0] + col_w[1] + col_w[2], y_before)
        pdf.multi_cell(col_w[3], row_h, score, border=1)


def _section_layout(pdf, data: list[dict[str, Any]], font: str):
    from fpdf import XPos, YPos

    for idx, entry in enumerate(data, 1):
        pdf.add_page()
        pdf.set_font(font, "B", 16)
        pdf.cell(0, 10, f"Entry {idx}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        meta = entry.get("metadata") or {}
        if meta:
            pdf.set_font(font, "B", 10)
            pdf.cell(0, 7, "Metadata", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(font, "", 9)
            for k, v in meta.items():
                display = json.dumps(v) if isinstance(v, (list, dict)) else str(v)
                pdf.cell(0, 6, f"  {k}: {display}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)

        rules = entry.get("transformation_rules", [])
        if rules:
            pdf.set_font(font, "B", 10)
            pdf.cell(0, 7, "Transformation Rules", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(font, "", 9)
            for r in rules:
                pdf.cell(0, 6, f"  - {r}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)

        pdf.set_font(font, "B", 10)
        pdf.cell(0, 7, "Input", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(font, "", 9)
        for line in textwrap.wrap(entry.get("input", ""), 90):
            pdf.cell(0, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        pdf.set_font(font, "B", 10)
        pdf.cell(0, 7, "Output", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(font, "", 9)
        for line in textwrap.wrap(entry.get("output", ""), 90):
            pdf.cell(0, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def _compact_layout(pdf, data: list[dict[str, Any]], font: str):
    from fpdf import XPos, YPos

    pdf.add_page()
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 10, "Dataset Overview", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    for idx, entry in enumerate(data, 1):
        if pdf.get_y() > pdf.h - 60:
            pdf.add_page()

        meta = entry.get("metadata") or {}
        req_type = meta.get("request_type", "N/A")
        score = meta.get("quality_score", "N/A")

        pdf.set_font(font, "B", 10)
        pdf.cell(0, 7, f"{idx}. [{req_type}] (Score: {score})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(font, "", 8)
        inp = truncate(entry.get("input", ""), 300)
        for line in textwrap.wrap(inp, 110):
            pdf.cell(0, 4, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

        pdf.set_font(font, "I", 8)
        out = truncate(entry.get("output", ""), 300)
        for line in textwrap.wrap(out, 110):
            pdf.cell(0, 4, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(4)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
