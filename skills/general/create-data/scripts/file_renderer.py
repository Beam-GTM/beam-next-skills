"""Render structured content into realistic PDF/CSV/JSON/TXT files.

This is the SINGLE renderer for all document types. It takes a render spec
(JSON) describing document content and layout, and produces actual files with
realistic styling. Domain-agnostic — works for CVs, invoices, lab reports,
property listings, legal documents, etc.

The LLM generates the spec on demand. The renderer just executes it. No
domain-specific renderer scripts needed — all variety comes from the spec.

Usage:
    python file_renderer.py spec.json --output path/to/file.pdf
    python file_renderer.py spec.json --output path/to/file.csv
    python file_renderer.py spec.json --output path/to/file.json
    python file_renderer.py spec.json --output path/to/file.txt

Render spec format:
{
  "layout": "single_column|two_column|sidebar|tabular",
  "color_scheme": "blue|green|gold|red|purple",
  "font": "Helvetica|Courier|Times",
  "page_header": "Optional header text",
  "page_footer": true,
  "sections": [
    {"type": "header", "content": "DOCUMENT TITLE"},
    {"type": "contact", "content": "Address | Email | Phone"},
    {"type": "heading", "content": "SECTION HEADING"},
    {"type": "subheading", "content": "Subsection heading"},
    {"type": "text", "content": "Paragraph text..."},
    {"type": "entry", "title": "Role", "subtitle": "Company | Date", "bullets": ["..."]},
    {"type": "table", "headers": ["Col1", "Col2"], "rows": [["a", "b"]], "aligns": ["L", "R"]},
    {"type": "list", "items": ["item1", "item2"]},
    {"type": "keyvalue", "pairs": [["Key", "Value"], ...]},
    {"type": "columns", "widths": [0.55, 0.40], "gap": 0.05, "columns": [[sections...], [sections...]]},
    {"type": "totals", "rows": [{"label": "Subtotal:", "value": "$1,234.56"}, ...], "bold_last": true},
    {"type": "accent_bar", "position": "left", "width": 4},
    {"type": "divider"},
    {"type": "spacer", "height": 10}
  ]
}
"""

from __future__ import annotations

import csv
import io
import json
import random
import sys
import textwrap
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Color schemes — RGB tuples
# ---------------------------------------------------------------------------
COLOR_SCHEMES = {
    "blue": {
        "primary": (31, 78, 121),
        "secondary": (68, 114, 196),
        "accent": (180, 198, 231),
        "text": (30, 30, 30),
        "light_bg": (234, 240, 248),
    },
    "green": {
        "primary": (84, 130, 53),
        "secondary": (112, 173, 71),
        "accent": (198, 224, 180),
        "text": (30, 30, 30),
        "light_bg": (235, 245, 228),
    },
    "gold": {
        "primary": (191, 143, 0),
        "secondary": (218, 170, 32),
        "accent": (255, 230, 153),
        "text": (30, 30, 30),
        "light_bg": (255, 248, 225),
    },
    "red": {
        "primary": (192, 0, 0),
        "secondary": (218, 55, 55),
        "accent": (248, 203, 203),
        "text": (30, 30, 30),
        "light_bg": (253, 237, 237),
    },
    "purple": {
        "primary": (112, 48, 160),
        "secondary": (149, 79, 201),
        "accent": (216, 191, 236),
        "text": (30, 30, 30),
        "light_bg": (242, 234, 250),
    },
}

FONTS = ["Helvetica", "Courier", "Times"]
LAYOUTS = ["single_column", "two_column", "sidebar", "tabular"]


# ---------------------------------------------------------------------------
# Safe text encoding for built-in fpdf2 fonts (latin-1)
# ---------------------------------------------------------------------------

def _safe(text: str) -> str:
    """Make text safe for fpdf2 built-in fonts (latin-1 encoding).

    Latin-1 natively covers Western European characters: e-acute, u-umlaut,
    c-cedilla, n-tilde, etc. Only truly out-of-range chars get replaced.
    """
    if not text:
        return ""
    # Map common Unicode chars to latin-1 equivalents
    _MAP = {
        "\u2013": "-", "\u2014": "--", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u20ac": "EUR",
    }
    for char, repl in _MAP.items():
        text = text.replace(char, repl)
    try:
        text.encode("latin-1")
        return text
    except UnicodeEncodeError:
        return text.encode("latin-1", errors="replace").decode("latin-1")


# ---------------------------------------------------------------------------
# Text-to-sections parser (backward compat with plain text)
# ---------------------------------------------------------------------------

def text_to_sections(text: str) -> list[dict[str, Any]]:
    """Parse plain text into render spec sections by detecting structure."""
    sections: list[dict[str, Any]] = []
    lines = text.strip().split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # All-caps lines with 3+ chars -> heading
        if line.isupper() and len(line) >= 3 and not line.startswith("-"):
            if not sections:
                sections.append({"type": "header", "content": line})
            else:
                sections.append({"type": "heading", "content": line})
            i += 1
            continue

        # Lines with pipes -> contact info
        if "|" in line and len(line.split("|")) >= 3:
            sections.append({"type": "contact", "content": line})
            i += 1
            continue

        # Bullet points (- or bullet)
        if line.startswith("- ") or line.startswith("\u2022 "):
            bullets = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "\u2022 ")):
                bullets.append(lines[i].strip().lstrip("-\u2022").strip())
                i += 1
            sections.append({"type": "list", "items": bullets})
            continue

        # Key: Value patterns on consecutive lines
        if ": " in line and len(line.split(": ", 1)[0]) < 40:
            pairs = []
            while i < len(lines) and ": " in lines[i].strip() and len(lines[i].strip().split(": ", 1)[0]) < 40:
                parts = lines[i].strip().split(": ", 1)
                pairs.append(parts)
                i += 1
            if len(pairs) >= 2:
                sections.append({"type": "keyvalue", "pairs": pairs})
                continue
            else:
                sections.append({"type": "text", "content": lines[i - 1].strip()})
                continue

        # Default: paragraph text
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
            next_line = lines[i].strip()
            if next_line.startswith(("- ", "\u2022 ")) or ("|" in next_line and len(next_line.split("|")) >= 3):
                break
            para_lines.append(next_line)
            i += 1
        sections.append({"type": "text", "content": " ".join(para_lines)})

    return sections


# ---------------------------------------------------------------------------
# PDF Renderer
# ---------------------------------------------------------------------------

def render_pdf(spec: dict[str, Any], output_path: Path) -> Path:
    """Render a spec as a styled PDF."""
    from fpdf import FPDF, XPos, YPos

    layout = spec.get("layout", random.choice(LAYOUTS))
    scheme_name = spec.get("color_scheme", random.choice(list(COLOR_SCHEMES)))
    font = spec.get("font", random.choice(FONTS))
    colors = COLOR_SCHEMES[scheme_name]
    sections = spec.get("sections", [])
    page_header = spec.get("page_header")
    page_footer = spec.get("page_footer", False)

    class DocPDF(FPDF):
        def __init__(self):
            super().__init__()
            self._font = font
            self._colors = colors
            self._page_header = page_header
            self._page_footer = page_footer

        def header(self):
            if self._page_header and self.page_no() > 1:
                self.set_font(self._font, "I", 8)
                self.set_text_color(*self._colors["secondary"])
                self.cell(0, 5, self._page_header, align="R")
                self.ln(8)

        def footer(self):
            if self._page_footer:
                self.set_y(-15)
                self.set_font(self._font, "I", 8)
                self.set_text_color(150, 150, 150)
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = DocPDF()
    if page_footer:
        pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    if layout == "single_column":
        _render_single_column(pdf, sections, colors, font)
    elif layout == "two_column":
        _render_two_column(pdf, sections, colors, font)
    elif layout == "sidebar":
        _render_sidebar(pdf, sections, colors, font)
    elif layout == "tabular":
        _render_tabular(pdf, sections, colors, font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return output_path


def _set_color(pdf, rgb: tuple[int, int, int]):
    pdf.set_text_color(*rgb)


def _render_section(pdf, section: dict, colors: dict, font: str,
                    max_width: float | None = None, x_offset: float = 0):
    """Render a single section. Used by all layouts."""
    from fpdf import XPos, YPos

    stype = section.get("type", "text")
    w = max_width or (pdf.w - pdf.l_margin - pdf.r_margin)

    if stype == "header":
        size = section.get("size", 20)
        pdf.set_font(font, "B", size)
        _set_color(pdf, colors["primary"])
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.cell(w, size * 0.6, _safe(section.get("content", "")),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    elif stype == "contact":
        pdf.set_font(font, "", 9)
        _set_color(pdf, colors["secondary"])
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.multi_cell(w, 5, _safe(section.get("content", "")))
        pdf.ln(4)

    elif stype == "heading":
        pdf.ln(3)
        pdf.set_font(font, "B", 13)
        _set_color(pdf, colors["primary"])
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.cell(w, 8, _safe(section.get("content", "")),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Underline
        pdf.set_draw_color(*colors["secondary"])
        pdf.line(x_offset + pdf.l_margin, pdf.get_y(),
                 x_offset + pdf.l_margin + w, pdf.get_y())
        pdf.ln(4)

    elif stype == "subheading":
        pdf.set_font(font, "B", 11)
        _set_color(pdf, colors["secondary"])
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.cell(w, 7, _safe(section.get("content", "")),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    elif stype == "text":
        size = section.get("size", 10)
        style = section.get("style", "")
        color = section.get("color", "text")
        pdf.set_font(font, style, size)
        _set_color(pdf, colors.get(color, colors["text"]))
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.multi_cell(w, size * 0.5, _safe(section.get("content", "")))
        pdf.ln(2)

    elif stype == "entry":
        pdf.set_font(font, "B", 11)
        _set_color(pdf, colors["text"])
        pdf.set_x(x_offset + pdf.l_margin)
        pdf.cell(w, 6, _safe(section.get("title", "")),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        subtitle = section.get("subtitle")
        if subtitle:
            pdf.set_font(font, "I", 9)
            _set_color(pdf, colors["secondary"])
            pdf.set_x(x_offset + pdf.l_margin)
            pdf.cell(w, 5, _safe(subtitle),
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        for bullet in section.get("bullets", []):
            pdf.set_font(font, "", 9)
            _set_color(pdf, colors["text"])
            pdf.set_x(x_offset + pdf.l_margin + 4)
            pdf.multi_cell(w - 4, 4.5, _safe(f"- {bullet}"))
        pdf.ln(3)

    elif stype == "table":
        headers = section.get("headers", [])
        rows = section.get("rows", [])
        aligns = section.get("aligns")  # Optional per-column alignment
        col_widths = section.get("col_widths")  # Optional explicit widths
        if not headers and not rows:
            return
        num_cols = len(headers) if headers else len(rows[0])

        # Calculate column widths
        if col_widths:
            # col_widths as fractions of table width
            cw = [f * w for f in col_widths]
        else:
            cw = [min(w / num_cols, 60)] * num_cols

        # Default alignments
        if not aligns:
            aligns = ["L"] * num_cols

        if headers:
            pdf.set_font(font, "B", 9)
            pdf.set_fill_color(*colors["primary"])
            pdf.set_text_color(255, 255, 255)
            pdf.set_x(x_offset + pdf.l_margin)
            for i, h in enumerate(headers):
                pdf.cell(cw[i], 7, _safe(str(h)), border=1, fill=True,
                         align=aligns[i] if i < len(aligns) else "L")
            pdf.ln()

        pdf.set_font(font, "", 9)
        _set_color(pdf, colors["text"])
        for row_idx, row in enumerate(rows):
            if row_idx % 2 == 0:
                pdf.set_fill_color(*colors["light_bg"])
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_x(x_offset + pdf.l_margin)
            for i, cell in enumerate(row):
                pdf.cell(cw[i] if i < len(cw) else cw[0], 6, _safe(str(cell)),
                         border=1, fill=True,
                         align=aligns[i] if i < len(aligns) else "L")
            pdf.ln()
        pdf.ln(3)

    elif stype == "list":
        pdf.set_font(font, "", 9)
        _set_color(pdf, colors["text"])
        for item in section.get("items", []):
            pdf.set_x(x_offset + pdf.l_margin + 4)
            pdf.multi_cell(w - 4, 4.5, _safe(f"- {item}"))
        pdf.ln(2)

    elif stype == "keyvalue":
        pdf.set_font(font, "", 9)
        for pair in section.get("pairs", []):
            if len(pair) >= 2:
                pdf.set_x(x_offset + pdf.l_margin)
                pdf.set_font(font, "B", 9)
                _set_color(pdf, colors["text"])
                key_text = _safe(str(pair[0]))
                key_w = min(pdf.get_string_width(key_text) + 4, w * 0.4)
                pdf.cell(key_w, 5, key_text)
                pdf.set_font(font, "", 9)
                _set_color(pdf, colors["secondary"])
                pdf.multi_cell(w - key_w, 5, _safe(str(pair[1])))
        pdf.ln(2)

    elif stype == "columns":
        # Render N blocks side-by-side. Each column is an array of sections.
        # widths: fractional widths (e.g., [0.55, 0.40])
        # gap: fractional gap between columns (default 0.05)
        col_specs = section.get("columns", [])
        widths = section.get("widths", [1.0 / len(col_specs)] * len(col_specs))
        gap = section.get("gap", 0.05) * w

        y_start = pdf.get_y()
        max_y = y_start

        x = x_offset
        for col_idx, col_sections in enumerate(col_specs):
            col_w = widths[col_idx] * w
            pdf.set_y(y_start)
            for s in col_sections:
                _render_section(pdf, s, colors, font, max_width=col_w, x_offset=x)
            max_y = max(max_y, pdf.get_y())
            x += col_w + gap

        pdf.set_y(max_y + 2)

    elif stype == "totals":
        # Right-aligned totals block for invoices, purchase orders, etc.
        # rows: [{"label": "Subtotal:", "value": "$1,234.56"}, ...]
        # bold_last: true to bold the last row (grand total)
        totals_rows = section.get("rows", [])
        bold_last = section.get("bold_last", True)
        totals_w = w * 0.45
        totals_x = x_offset + pdf.l_margin + w - totals_w
        label_w = totals_w * 0.55
        val_w = totals_w * 0.45

        for i, row in enumerate(totals_rows):
            is_last = (i == len(totals_rows) - 1)
            is_bold = is_last and bold_last
            size = 11 if is_bold else 9
            style = "B" if is_bold else ""

            if is_bold:
                # Draw separator line before grand total
                pdf.set_draw_color(*colors["primary"])
                pdf.set_line_width(0.6)
                pdf.line(totals_x, pdf.get_y(), totals_x + totals_w, pdf.get_y())
                pdf.set_line_width(0.2)
                pdf.ln(1)

            pdf.set_font(font, style, size)
            _set_color(pdf, colors["primary"] if is_bold else colors["text"])
            pdf.set_x(totals_x)
            pdf.cell(label_w, 6, _safe(str(row.get("label", ""))), align="R")
            pdf.cell(val_w, 6, _safe(str(row.get("value", ""))), align="R")
            pdf.ln()
        pdf.ln(3)

    elif stype == "accent_bar":
        # Draw a colored vertical bar (e.g., left accent for modern layouts)
        position = section.get("position", "left")
        bar_w = section.get("width", 4)
        pdf.set_fill_color(*colors["primary"])
        if position == "left":
            pdf.rect(0, 0, bar_w, pdf.h, "F")
        elif position == "top":
            bar_h = section.get("height", 35)
            pdf.rect(0, 0, pdf.w, bar_h, "F")

    elif stype == "colored_box":
        # Draw a colored background box behind content
        box_h = section.get("height", 30)
        pdf.set_fill_color(*colors["light_bg"])
        pdf.set_draw_color(*colors["accent"])
        pdf.rect(x_offset + pdf.l_margin, pdf.get_y(), w, box_h, "DF")
        # Render inner sections on top of the box
        inner_y = pdf.get_y() + 2
        for s in section.get("sections", []):
            pdf.set_y(inner_y)
            _render_section(pdf, s, colors, font, max_width=w - 4,
                            x_offset=x_offset + 2)
            inner_y = pdf.get_y()
        pdf.set_y(pdf.get_y() + 4)

    elif stype == "divider":
        pdf.ln(2)
        pdf.set_draw_color(*colors["accent"])
        pdf.line(x_offset + pdf.l_margin, pdf.get_y(),
                 x_offset + pdf.l_margin + w, pdf.get_y())
        pdf.ln(4)

    elif stype == "spacer":
        pdf.ln(section.get("height", 10))


# ---------------------------------------------------------------------------
# Layout: Single Column
# ---------------------------------------------------------------------------

def _render_single_column(pdf, sections, colors, font):
    for section in sections:
        _render_section(pdf, section, colors, font)


# ---------------------------------------------------------------------------
# Layout: Two Column
# ---------------------------------------------------------------------------

def _render_two_column(pdf, sections, colors, font):
    """Render with two equal-width columns. Header/contact span full width,
    then remaining sections alternate between left and right columns."""
    full_w = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = (full_w - 8) / 2  # 8mm gutter
    right_x = col_w + 8

    # Render full-width header sections first
    full_width_types = {"header", "contact", "divider", "spacer", "columns",
                        "totals", "accent_bar", "table"}
    body_sections = []
    for s in sections:
        if s.get("type") in full_width_types and not body_sections:
            _render_section(pdf, s, colors, font)
        else:
            body_sections.append(s)

    if not body_sections:
        return

    # Split remaining sections into two columns
    mid = len(body_sections) // 2
    left_sections = body_sections[:mid]
    right_sections = body_sections[mid:]

    y_start = pdf.get_y() + 4

    # Render left column
    pdf.set_y(y_start)
    for s in left_sections:
        _render_section(pdf, s, colors, font, max_width=col_w, x_offset=0)

    left_end_y = pdf.get_y()

    # Render right column
    pdf.set_y(y_start)
    for s in right_sections:
        _render_section(pdf, s, colors, font, max_width=col_w, x_offset=right_x)

    right_end_y = pdf.get_y()
    pdf.set_y(max(left_end_y, right_end_y))


# ---------------------------------------------------------------------------
# Layout: Sidebar
# ---------------------------------------------------------------------------

def _render_sidebar(pdf, sections, colors, font):
    """Narrow left sidebar (skills, contact, etc.) + wide main column."""
    full_w = pdf.w - pdf.l_margin - pdf.r_margin
    sidebar_w = full_w * 0.3
    main_w = full_w * 0.65
    main_x = sidebar_w + full_w * 0.05

    # Categorize sections: sidebar gets compact data, main gets content.
    # Sections can override with "sidebar": true/false in the spec.
    sidebar_types = {"contact", "list", "keyvalue"}
    main_types = {"header", "heading", "subheading", "entry", "text",
                  "columns", "totals", "accent_bar", "colored_box"}

    sidebar_sections = []
    main_sections = []

    for s in sections:
        # Explicit override
        if "sidebar" in s:
            (sidebar_sections if s["sidebar"] else main_sections).append(s)
            continue
        stype = s.get("type", "text")
        if stype == "table":
            # Wide tables (3+ cols or explicit widths) go to main
            num_cols = len(s.get("headers", s.get("rows", [[]])[0]))
            if num_cols > 2 or s.get("col_widths"):
                main_sections.append(s)
            else:
                sidebar_sections.append(s)
        elif stype in sidebar_types:
            sidebar_sections.append(s)
        elif stype in main_types:
            main_sections.append(s)
        else:
            main_sections.append(s)

    # Draw sidebar background
    y_start = pdf.get_y()
    pdf.set_fill_color(*colors["light_bg"])
    pdf.rect(pdf.l_margin, y_start, sidebar_w, pdf.h - y_start - 15, "F")

    # Render sidebar
    pdf.set_y(y_start + 4)
    for s in sidebar_sections:
        _render_section(pdf, s, colors, font, max_width=sidebar_w - 4, x_offset=0)

    sidebar_end_y = pdf.get_y()

    # Render main column
    pdf.set_y(y_start)
    for s in main_sections:
        _render_section(pdf, s, colors, font, max_width=main_w, x_offset=main_x)

    main_end_y = pdf.get_y()
    pdf.set_y(max(sidebar_end_y, main_end_y))


# ---------------------------------------------------------------------------
# Layout: Tabular
# ---------------------------------------------------------------------------

def _render_tabular(pdf, sections, colors, font):
    """Table-heavy layout for invoices, spec sheets, purchase orders.
    Renders tables prominently and wraps other sections normally."""
    for section in sections:
        stype = section.get("type", "text")
        if stype == "table":
            pdf.ln(2)
            _render_section(pdf, section, colors, font)
            pdf.ln(2)
        elif stype == "header":
            from fpdf import XPos, YPos
            pdf.set_font(font, "B", 22)
            _set_color(pdf, colors["primary"])
            pdf.cell(0, 14, _safe(section.get("content", "")),
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
            # Thick line under header
            pdf.set_draw_color(*colors["primary"])
            pdf.set_line_width(0.8)
            w = pdf.w - pdf.l_margin - pdf.r_margin
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + w, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.ln(6)
        else:
            _render_section(pdf, section, colors, font)


# ---------------------------------------------------------------------------
# CSV Renderer
# ---------------------------------------------------------------------------

def render_csv(spec: dict[str, Any], output_path: Path) -> Path:
    """Render spec sections as CSV. Best for tabular data."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    delimiter = random.choice([",", ";", "\t", "|"])
    quoting = random.choice([csv.QUOTE_ALL, csv.QUOTE_MINIMAL, csv.QUOTE_NONNUMERIC])

    sections = spec.get("sections", [])
    rows_to_write: list[list[str]] = []

    for section in sections:
        stype = section.get("type", "text")
        if stype == "table":
            headers = section.get("headers", [])
            if headers:
                rows_to_write.append(headers)
            rows_to_write.extend(section.get("rows", []))
        elif stype == "keyvalue":
            for pair in section.get("pairs", []):
                rows_to_write.append([str(p) for p in pair])
        elif stype in ("header", "heading"):
            rows_to_write.append([section.get("content", "")])

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter, quoting=quoting)
        for row in rows_to_write:
            writer.writerow(row)

    return output_path


# ---------------------------------------------------------------------------
# JSON Renderer
# ---------------------------------------------------------------------------

def render_json(spec: dict[str, Any], output_path: Path) -> Path:
    """Render spec content as structured JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content: dict[str, Any] = {}
    sections = spec.get("sections", [])

    for section in sections:
        stype = section.get("type", "text")
        if stype == "header":
            content["title"] = section.get("content", "")
        elif stype == "table":
            headers = section.get("headers", [])
            rows = section.get("rows", [])
            if headers:
                table_data = [dict(zip(headers, row)) for row in rows]
                key = f"table_{len([k for k in content if k.startswith('table_')])}"
                content[key] = table_data
        elif stype == "keyvalue":
            for pair in section.get("pairs", []):
                if len(pair) >= 2:
                    content[str(pair[0])] = pair[1]
        elif stype == "entry":
            entries = content.setdefault("entries", [])
            entries.append({
                "title": section.get("title", ""),
                "subtitle": section.get("subtitle", ""),
                "details": section.get("bullets", []),
            })

    with open(output_path, "w") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    return output_path


# ---------------------------------------------------------------------------
# TXT Renderer
# ---------------------------------------------------------------------------

def render_txt(spec: dict[str, Any], output_path: Path) -> Path:
    """Render spec as plain text with section headers."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    sections = spec.get("sections", [])

    for section in sections:
        stype = section.get("type", "text")

        if stype == "header":
            lines.append(section.get("content", "").upper())
            lines.append("")

        elif stype == "contact":
            lines.append(section.get("content", ""))
            lines.append("")

        elif stype == "heading":
            lines.append("")
            content = section.get("content", "")
            lines.append(content.upper())
            lines.append("=" * len(content))
            lines.append("")

        elif stype == "subheading":
            lines.append(section.get("content", ""))
            lines.append("-" * len(section.get("content", "")))
            lines.append("")

        elif stype == "text":
            for wrapped in textwrap.wrap(section.get("content", ""), 80):
                lines.append(wrapped)
            lines.append("")

        elif stype == "entry":
            lines.append(section.get("title", ""))
            if section.get("subtitle"):
                lines.append(section["subtitle"])
            for bullet in section.get("bullets", []):
                lines.append(f"  - {bullet}")
            lines.append("")

        elif stype == "table":
            headers = section.get("headers", [])
            rows = section.get("rows", [])
            all_rows = ([headers] if headers else []) + rows
            if all_rows:
                col_widths = [max(len(str(row[i])) for row in all_rows)
                              for i in range(len(all_rows[0]))]
                for row_idx, row in enumerate(all_rows):
                    line = " | ".join(str(cell).ljust(col_widths[i])
                                      for i, cell in enumerate(row))
                    lines.append(line)
                    if row_idx == 0 and headers:
                        lines.append("-+-".join("-" * w for w in col_widths))
            lines.append("")

        elif stype == "list":
            for item in section.get("items", []):
                lines.append(f"  - {item}")
            lines.append("")

        elif stype == "keyvalue":
            for pair in section.get("pairs", []):
                if len(pair) >= 2:
                    lines.append(f"{pair[0]}: {pair[1]}")
            lines.append("")

        elif stype == "totals":
            for row in section.get("rows", []):
                lines.append(f"  {row.get('label', ''):>30s}  {row.get('value', '')}")
            lines.append("")

        elif stype == "divider":
            lines.append("-" * 60)
            lines.append("")

        elif stype == "spacer":
            lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------

RENDERERS = {
    ".pdf": render_pdf,
    ".csv": render_csv,
    ".json": render_json,
    ".txt": render_txt,
}


def render_file(spec: dict[str, Any], output_path: str | Path) -> Path:
    """Render a spec to a file, choosing renderer by extension."""
    path = Path(output_path)
    suffix = path.suffix.lower()

    renderer = RENDERERS.get(suffix)
    if not renderer:
        raise ValueError(f"Unsupported format: {suffix}. Supported: {list(RENDERERS)}")

    # If sections are missing but raw_text is provided, parse it
    if "sections" not in spec and "raw_text" in spec:
        spec["sections"] = text_to_sections(spec["raw_text"])

    return renderer(spec, path)


def render_from_text(text: str, output_path: str | Path,
                     layout: str | None = None,
                     color_scheme: str | None = None,
                     font: str | None = None) -> Path:
    """Convenience: render plain text to a file with auto-parsed sections."""
    spec: dict[str, Any] = {
        "sections": text_to_sections(text),
    }
    if layout:
        spec["layout"] = layout
    if color_scheme:
        spec["color_scheme"] = color_scheme
    if font:
        spec["font"] = font
    return render_file(spec, output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render structured content into files")
    parser.add_argument("spec", help="Path to render spec JSON file, or '-' for stdin")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--layout", choices=LAYOUTS, help="Override layout")
    parser.add_argument("--color-scheme", choices=list(COLOR_SCHEMES), help="Override color scheme")
    parser.add_argument("--font", choices=FONTS, help="Override font")

    args = parser.parse_args()

    if args.spec == "-":
        spec_data = json.load(sys.stdin)
    else:
        with open(args.spec) as f:
            spec_data = json.load(f)

    if args.layout:
        spec_data["layout"] = args.layout
    if args.color_scheme:
        spec_data["color_scheme"] = args.color_scheme
    if args.font:
        spec_data["font"] = args.font

    result = render_file(spec_data, args.output)
    print(f"Rendered: {result}")
