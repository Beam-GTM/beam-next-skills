#!/usr/bin/env python3
"""
Sales Call Prep — PDF Generator

Generates a polished, printable call prep PDF from structured data.
Uses the Beam brand system (BEAM_BLUE, BEAM_ACCENT) and shared logo assets.

Usage:
    python generate_call_prep_pdf.py --data call_prep_data.json --output "Call Prep - Client.pdf"

Or import and call build_call_prep_pdf() directly with a data dict.

Data format: see SAMPLE_DATA at bottom of file for full schema.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
except ImportError:
    print("Missing dependency: reportlab")
    print("Run: pip install reportlab")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
#  BRAND SYSTEM
# ═══════════════════════════════════════════════════════════════

BEAM_BLUE = HexColor("#1a1a2e")
BEAM_ACCENT = HexColor("#4361ee")
BEAM_ACCENT_LIGHT = HexColor("#e8edff")

BLACK = HexColor("#1a1a1a")
CHARCOAL = HexColor("#2d2d2d")
BODY = HexColor("#3a3a3a")
MID = HexColor("#5a5a5a")
CAPTION = HexColor("#888888")
LGRAY = HexColor("#d0d0d0")
ZEBRA = HexColor("#f7f7f7")
WHITE = HexColor("#ffffff")
RED = HexColor("#c00000")
GREEN_V = HexColor("#007a33")

W, H = A4
MARGIN = 50
RMG = 50
CW = W - MARGIN - RMG


def _find_beam_next_root():
    """Walk up from this file to find the Beam Next root (has CLAUDE.md)."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return None


def _find_logo():
    """Find the Beam logo from the shared assets folder."""
    root = _find_beam_next_root()
    if root:
        candidates = [
            root / "00-system" / "assets" / "logos" / "beam-logo-flat.png",
            root / "00-system" / "assets" / "logos" / "beam-logo.png",
        ]
        for c in candidates:
            if c.exists():
                return c
    return None


def _find_client_logo(client_name):
    """Find a client/lead logo from project folders or shared assets."""
    root = _find_beam_next_root()
    if not root or not client_name:
        return None

    client_lower = client_name.lower().replace(" ", "-").replace("_", "-")

    # Check shared assets first
    assets_dir = root / "00-system" / "assets" / "logos"
    if assets_dir.exists():
        for f in assets_dir.iterdir():
            if client_lower in f.name.lower() and f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                if "white" not in f.name.lower():
                    return f

    # Search project folders
    projects_dir = root / "02-projects"
    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            if client_lower in project_dir.name.lower() or any(
                part in project_dir.name.lower() for part in client_lower.split("-") if len(part) > 3
            ):
                for sub in ["04-outputs", "01-planning", "02-resources"]:
                    sub_dir = project_dir / sub
                    if sub_dir.exists():
                        for f in sub_dir.iterdir():
                            if "logo" in f.name.lower() and f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                                if "white" not in f.name.lower():
                                    return f
    return None


def _fetch_logo_from_web(company_name, save_dir=None):
    """
    Fetch a company logo from Clearbit's logo API (free, no auth needed).
    Falls back to Google's favicon service.
    Returns path to saved logo or None.
    """
    if not company_name:
        return None

    if save_dir is None:
        root = _find_beam_next_root()
        if root:
            save_dir = root / "00-system" / "assets" / "logos"
        else:
            save_dir = Path(".")

    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    slug = company_name.lower().replace(" ", "-").replace("_", "-")
    save_path = save_dir / f"{slug}-logo.png"

    if save_path.exists():
        return save_path

    # Build likely domain from company name
    domain_guesses = [
        f"{company_name.lower().replace(' ', '')}.com",
        f"{company_name.lower().replace(' ', '-')}.com",
    ]

    try:
        import requests
    except ImportError:
        return None

    for domain in domain_guesses:
        # Try Clearbit Logo API (high quality, free)
        url = f"https://logo.clearbit.com/{domain}"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200 and len(resp.content) > 500:
                save_path.write_bytes(resp.content)
                return save_path
        except Exception:
            pass

        # Fallback: Google favicon service (lower quality but reliable)
        url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200 and len(resp.content) > 500:
                save_path.write_bytes(resp.content)
                return save_path
        except Exception:
            pass

    return None


def find_or_fetch_client_logo(client_name):
    """
    Find a client logo locally, or fetch from the web if not found.
    Returns path to logo file or None.
    """
    logo = _find_client_logo(client_name)
    if logo:
        return logo
    return _fetch_logo_from_web(client_name)


# ═══════════════════════════════════════════════════════════════
#  DRAWING PRIMITIVES
# ═══════════════════════════════════════════════════════════════

def clean(t):
    return (t.replace("\u2014", " -- ").replace("\u2013", " - ")
             .replace("\u2018", "'").replace("\u2019", "'")
             .replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2026", "...").replace("\u2192", "->")
             .replace("\u2190", "<-").replace("\u2194", "<->"))


def txt(cv, x, y, s, f="Helvetica", sz=10, c=BLACK):
    cv.setFont(f, sz); cv.setFillColor(c); cv.drawString(x, y, clean(s))


def txtr(cv, x, y, s, f="Helvetica", sz=10, c=BLACK):
    cv.setFont(f, sz); cv.setFillColor(c); cv.drawRightString(x, y, clean(s))


def para(cv, x, y, s, f="Helvetica", sz=9.5, c=BODY, mw=400, ld=None):
    if ld is None:
        ld = sz * 1.5
    cv.setFont(f, sz); cv.setFillColor(c)
    s = clean(s)
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if cv.stringWidth(t, f, sz) <= mw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        cv.drawString(x, y, ln)
        y -= ld
    return y


def rule(cv, x, y, w, c=LGRAY, lw=0.5):
    cv.setStrokeColor(c); cv.setLineWidth(lw); cv.line(x, y, x + w, y)


def accent_line(cv, x, y, length=45):
    cv.setStrokeColor(BEAM_ACCENT); cv.setLineWidth(2.5); cv.line(x, y, x + length, y)


def bullet(cv, x, y, text, sz=8.5, mw=None):
    if mw is None:
        mw = CW - (x - MARGIN) - 10
    cv.setFillColor(BEAM_ACCENT)
    cv.circle(x + 3, y + 2.5, 2, fill=1, stroke=0)
    y = para(cv, x + 12, y, text, sz=sz, c=BODY, mw=mw, ld=12)
    return y - 2


def _draw_logo_img(cv, path, x, y, height):
    """Draw a logo image, return the width used."""
    try:
        img = ImageReader(str(path))
        iw, ih = img.getSize()
        w = iw * (height / ih)
        cv.drawImage(str(path), x, y, width=w, height=height, mask='auto')
        return w
    except Exception:
        return 0


def hdr(cv, subtitle="", confidential=True, client_logo=None):
    logo = _find_logo()
    cv.setFillColor(BEAM_BLUE)
    cv.rect(0, H - 8, W, 8, fill=1, stroke=0)
    y = H - 28
    x_cursor = MARGIN
    logo_h = 12

    if logo and logo.exists():
        bw = _draw_logo_img(cv, logo, x_cursor, y - 2, logo_h)
        if bw > 0:
            x_cursor += bw + 6
            if client_logo and Path(client_logo).exists():
                cv.setFont("Helvetica", 8); cv.setFillColor(CAPTION)
                cv.drawString(x_cursor, y, "x")
                x_cursor += 12
                cw = _draw_logo_img(cv, client_logo, x_cursor, y - 2, logo_h)
                x_cursor += cw + 6 if cw > 0 else 0
            txt(cv, x_cursor, y, "|  Call Prep  |  INTERNAL", "Helvetica", 7, CAPTION)
        else:
            txt(cv, MARGIN, y, "BEAM AI", "Helvetica-Bold", 8, BEAM_ACCENT)
            txt(cv, MARGIN + 48, y, "|  Call Prep  |  INTERNAL", "Helvetica", 7, CAPTION)
    else:
        txt(cv, MARGIN, y, "BEAM AI", "Helvetica-Bold", 8, BEAM_ACCENT)
        txt(cv, MARGIN + 48, y, "|  Call Prep  |  INTERNAL", "Helvetica", 7, CAPTION)
    if confidential:
        txtr(cv, W - RMG, y, "DO NOT SHARE", "Helvetica-Bold", 6.5, RED)
    rule(cv, MARGIN, y - 8, CW)
    return y - 22


def ftr(cv, pg, client_name="", person_name="", date_str=""):
    cv.setFillColor(BEAM_BLUE)
    cv.rect(0, 0, W, 4, fill=1, stroke=0)
    cv.setFont("Helvetica", 6.5); cv.setFillColor(CAPTION)
    parts = [p for p in [client_name, person_name, "Call Prep", date_str, "INTERNAL"] if p]
    cv.drawString(MARGIN, 14, "  |  ".join(parts))
    cv.drawRightString(W - RMG, 14, f"Page {pg}")


def check_page_space(cv, y, needed, pg_num, data, new_page_fn=None):
    """If not enough space, start a new page and return new y."""
    if y - needed < 60:
        ftr(cv, pg_num, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))
        cv.showPage()
        pg_num += 1
        y = hdr(cv)
    return y, pg_num


# ═══════════════════════════════════════════════════════════════
#  PAGE BUILDERS
# ═══════════════════════════════════════════════════════════════

def page_attendees(cv, data, client_logo=None):
    """Page 1: Title + Attendee Profiles"""
    y = hdr(cv, client_logo=client_logo)

    title = f"Call Prep: {data.get('primary_contact', 'Client')}"
    txt(cv, MARGIN, y, title, "Helvetica-Bold", 22, BEAM_BLUE)
    y -= 14
    subtitle = f"{data.get('company', '')}  |  {data.get('date', '')}"
    txt(cv, MARGIN, y, subtitle, "Helvetica", 10, CAPTION)
    y -= 8; accent_line(cv, MARGIN, y, 50)
    y -= 18

    for attendee in data.get("attendees", []):
        name = attendee.get("name", "")
        txt(cv, MARGIN, y, name, "Helvetica-Bold", 13, BEAM_BLUE)
        y -= 16

        for label, key in [("Title", "title"), ("Company", "company"),
                           ("Background", "background"), ("In Role Since", "in_role_since")]:
            val = attendee.get(key, "")
            if val:
                txt(cv, MARGIN, y, f"{label}:", "Helvetica-Bold", 8, CHARCOAL)
                txt(cv, MARGIN + 80, y, val, "Helvetica", 8, BODY)
                y -= 13

        if attendee.get("what_makes_them_tick"):
            y -= 4
            txt(cv, MARGIN, y, "What Makes Them Tick", "Helvetica-Bold", 10, BEAM_BLUE)
            y -= 14
            for tick in attendee["what_makes_them_tick"]:
                y = bullet(cv, MARGIN, y, tick)

        if attendee.get("speak_their_language"):
            y -= 4
            txt(cv, MARGIN, y, "Speak Their Language", "Helvetica-Bold", 10, BEAM_ACCENT)
            y -= 14
            y = para(cv, MARGIN, y, attendee["speak_their_language"], sz=8.5, c=BODY, mw=CW, ld=12)

        y -= 12

    # Team roles
    roles = data.get("team_roles")
    if roles and y > 200:
        txt(cv, MARGIN, y, "Our Team: Roles on the Call", "Helvetica-Bold", 13, BEAM_BLUE)
        y -= 6; accent_line(cv, MARGIN, y, CW)
        y -= 16

        cv.setFillColor(BEAM_BLUE)
        cv.roundRect(MARGIN, y - 3, CW, 18, 2, fill=1, stroke=0)
        cols = [MARGIN + 4] + [MARGIN + CW * (i + 1) / (len(roles) + 1) for i in range(len(roles))]
        txt(cv, cols[0], y, "", "Helvetica-Bold", 7, WHITE)
        for i, role in enumerate(roles):
            txt(cv, cols[i + 1] if i + 1 < len(cols) else cols[-1], y, role.get("name", ""), "Helvetica-Bold", 7, WHITE)
        y -= 18

        aspects = ["role", "opens_with", "jumps_in_when", "owns", "closes_with"]
        aspect_labels = ["Role", "Opens with", "Jumps in", "Owns", "Closes"]
        rh = 16
        for i, (aspect, label) in enumerate(zip(aspects, aspect_labels)):
            ry = y - 2
            if i % 2 == 0:
                cv.setFillColor(ZEBRA); cv.rect(MARGIN, ry, CW, rh, fill=1, stroke=0)
            txt(cv, cols[0], y, label, "Helvetica-Bold", 7.5, CHARCOAL)
            for j, role in enumerate(roles):
                val = role.get(aspect, "")
                col_x = cols[j + 1] if j + 1 < len(cols) else cols[-1]
                txt(cv, col_x, y, val, "Helvetica", 7, BODY)
            y -= rh

    if data.get("handoff_note"):
        y -= 8
        cv.setFillColor(BEAM_ACCENT_LIGHT)
        cv.roundRect(MARGIN, y - 28, CW, 36, 4, fill=1, stroke=0)
        cv.setFillColor(BEAM_ACCENT); cv.rect(MARGIN, y - 28, 4, 36, fill=1, stroke=0)
        txt(cv, MARGIN + 14, y, "The Handoff", "Helvetica-Bold", 8.5, BEAM_BLUE)
        para(cv, MARGIN + 14, y - 13, data["handoff_note"], sz=8, c=BODY, mw=CW - 24, ld=11)

    ftr(cv, 1, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))


def page_company_intel(cv, data, pg, client_logo=None):
    """Page 2: Company Context & Pressures"""
    y = hdr(cv, client_logo=client_logo)

    txt(cv, MARGIN, y, f"{data.get('company', 'Company')}: Context & Pressures", "Helvetica-Bold", 18, BEAM_BLUE)
    y -= 8; accent_line(cv, MARGIN, y, 50)
    y -= 16

    # Key numbers (two-column)
    key_numbers = data.get("key_numbers", [])
    if key_numbers:
        col1_x = MARGIN
        col2_x = MARGIN + CW * 0.52
        for i, kv in enumerate(key_numbers):
            col = col1_x if i % 2 == 0 else col2_x
            txt(cv, col, y, f"{kv['label']}:", "Helvetica-Bold", 8, CHARCOAL)
            lw = cv.stringWidth(f"{kv['label']}: ", "Helvetica-Bold", 8)
            txt(cv, col + lw, y, kv["value"], "Helvetica", 8, BODY)
            if i % 2 == 1:
                y -= 14
        if len(key_numbers) % 2 == 1:
            y -= 14

    # Pressures table
    pressures = data.get("pressures", [])
    if pressures:
        y -= 8
        txt(cv, MARGIN, y, "The Pressures (Your Opening)", "Helvetica-Bold", 12, RED)
        y -= 14

        cv.setFillColor(BEAM_BLUE)
        cv.roundRect(MARGIN, y - 3, CW, 18, 2, fill=1, stroke=0)
        pc1 = MARGIN + 4
        pc2 = MARGIN + CW * 0.22
        pc3 = MARGIN + CW * 0.58
        txt(cv, pc1, y, "Pressure", "Helvetica-Bold", 7, WHITE)
        txt(cv, pc2, y, "Detail", "Helvetica-Bold", 7, WHITE)
        txt(cv, pc3, y, "Why It Matters", "Helvetica-Bold", 7, WHITE)
        y -= 18

        rh = 26
        for i, p in enumerate(pressures):
            ry = y - 2
            if i % 2 == 0:
                cv.setFillColor(ZEBRA); cv.rect(MARGIN, ry, CW, rh, fill=1, stroke=0)
            txt(cv, pc1, y + 4, p.get("pressure", ""), "Helvetica-Bold", 7.5, RED)
            para(cv, pc2, y + 4, p.get("detail", ""), sz=7, c=BODY, mw=CW * 0.34, ld=10)
            para(cv, pc3, y + 4, p.get("why_it_matters", ""), sz=7, c=BODY, mw=CW * 0.40, ld=10)
            y -= rh

    # Their initiatives
    initiatives = data.get("their_initiatives", [])
    if initiatives:
        y -= 6
        txt(cv, MARGIN, y, f"{data.get('company', '')}: Their Own Initiatives", "Helvetica-Bold", 12, BEAM_BLUE)
        y -= 14
        for item in initiatives:
            y = bullet(cv, MARGIN, y, item, sz=8)

    # The gap callout
    gap = data.get("gap_callout")
    if gap:
        y -= 8
        cv.setFillColor(GREEN_V)
        cv.roundRect(MARGIN, y - 18, CW, 26, 4, fill=1, stroke=0)
        txt(cv, MARGIN + 10, y - 6, gap, "Helvetica-Bold", 9.5, WHITE)

    ftr(cv, pg, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))


def page_talking_points(cv, data, pg, client_logo=None):
    """Page 3: Talking Points Cheat Sheet"""
    y = hdr(cv, client_logo=client_logo)

    txt(cv, MARGIN, y, "Talking Points (Print This)", "Helvetica-Bold", 18, BEAM_BLUE)
    y -= 8; accent_line(cv, MARGIN, y, 50)
    y -= 14

    for section in data.get("talking_points", []):
        title = section.get("title", "")
        owner = section.get("owner", "")
        is_proof = section.get("is_proof_point", False)
        is_close = section.get("is_close", False)
        color = GREEN_V if (is_proof or is_close) else BEAM_ACCENT

        cv.setFillColor(color)
        cv.roundRect(MARGIN, y - 3, CW, 16, 2, fill=1, stroke=0)
        txt(cv, MARGIN + 6, y, title, "Helvetica-Bold", 8, WHITE)
        if owner:
            txtr(cv, W - RMG - 6, y, owner, "Helvetica", 7, WHITE)
        y -= 20

        for point in section.get("points", []):
            cv.setFillColor(color)
            cv.circle(MARGIN + 8, y + 2, 1.5, fill=1, stroke=0)
            y = para(cv, MARGIN + 16, y, point, sz=7.5, c=BODY, mw=CW - 20, ld=10)
            y -= 2

        y -= 6

        if y < 80:
            ftr(cv, pg, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))
            cv.showPage()
            pg += 1
            y = hdr(cv, client_logo=client_logo)

    ftr(cv, pg, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))
    return pg


def page_objections(cv, data, pg, client_logo=None):
    """Page 4: Objection Handling + Killer Line + Post-Call"""
    y = hdr(cv, client_logo=client_logo)

    txt(cv, MARGIN, y, "Objection Handling", "Helvetica-Bold", 18, BEAM_BLUE)
    y -= 8; accent_line(cv, MARGIN, y, 50)
    y -= 14

    for obj in data.get("objections", []):
        objection = obj.get("objection", "")
        response = obj.get("response", "")
        txt(cv, MARGIN + 4, y, objection, "Helvetica-Bold", 8, RED)
        y -= 13
        y = para(cv, MARGIN + 4, y, response, sz=7.5, c=BODY, mw=CW - 8, ld=10)
        y -= 4
        rule(cv, MARGIN, y, CW, LGRAY, 0.3)
        y -= 8

        if y < 120:
            ftr(cv, pg, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))
            cv.showPage()
            pg += 1
            y = hdr(cv)

    # The killer line
    killer = data.get("killer_line", "")
    if killer:
        y -= 6
        line_count = len(killer) // 70 + 1
        box_h = 30 + line_count * 12
        cv.setFillColor(BEAM_BLUE)
        cv.roundRect(MARGIN, y - box_h + 12, CW, box_h, 6, fill=1, stroke=0)
        txt(cv, MARGIN + 12, y + 2, "THE ONE LINE THAT WINS THE CALL", "Helvetica-Bold", 9, BEAM_ACCENT)
        para(cv, MARGIN + 12, y - 14, killer, f="Helvetica-Bold", sz=8.5, c=WHITE, mw=CW - 24, ld=12)
        y -= box_h + 6

    # Post-call actions
    actions = data.get("post_call_actions", [])
    if actions and y > 100:
        y -= 12
        txt(cv, MARGIN, y, "Post-Call Actions", "Helvetica-Bold", 12, BEAM_BLUE)
        y -= 14
        for a in actions:
            txt(cv, MARGIN + 4, y, "[ ]", "Helvetica", 8, LGRAY)
            txt(cv, MARGIN + 22, y, a, "Helvetica", 8, BODY)
            y -= 14

    ftr(cv, pg, data.get("company", ""), data.get("primary_contact", ""), data.get("date", ""))
    return pg


# ═══════════════════════════════════════════════════════════════
#  MAIN BUILDER
# ═══════════════════════════════════════════════════════════════

def build_call_prep_pdf(data, output_path=None):
    """
    Build a complete call prep PDF from structured data.

    Args:
        data: dict with keys matching the schema (see SAMPLE_DATA)
        output_path: Path for the output PDF. If None, auto-generates.

    Returns:
        Path to the generated PDF
    """
    if output_path is None:
        company = data.get("company", "Client").replace(" ", "-")
        contact = data.get("primary_contact", "").replace(" ", "-")
        date = data.get("date", datetime.now().strftime("%b%d"))
        output_path = Path(f"Call Prep - {contact} - {company} - {date}.pdf")

    output_path = Path(output_path)

    # Find or fetch client/lead logo
    client_logo = find_or_fetch_client_logo(data.get("company", ""))
    if client_logo:
        print(f"Client logo: {client_logo}")

    cv = canvas.Canvas(str(output_path), pagesize=A4)

    pg = 1
    page_attendees(cv, data, client_logo=client_logo)
    cv.showPage()

    pg += 1
    page_company_intel(cv, data, pg, client_logo=client_logo)
    cv.showPage()

    pg += 1
    pg = page_talking_points(cv, data, pg, client_logo=client_logo)
    cv.showPage()

    pg += 1
    page_objections(cv, data, pg, client_logo=client_logo)
    cv.showPage()

    cv.save()
    print(f"PDF generated: {output_path}")
    print(f"Pages: {pg}")
    return output_path


# ═══════════════════════════════════════════════════════════════
#  SAMPLE DATA SCHEMA
# ═══════════════════════════════════════════════════════════════

SAMPLE_DATA = {
    "company": "Lulu Group International",
    "primary_contact": "Arvind Kumar",
    "date": "February 24, 2026",
    "call_type": "Sales / FP&A Agent Pitch",

    "attendees": [
        {
            "name": "Arvind Kumar",
            "title": "General Manager, Corporate Strategy and FP&A",
            "company": "Lulu Group International",
            "background": "IIT Roorkee -> IIM Indore -> EXL (Six Sigma) -> ARDENT Advisory (M&A) -> Lulu",
            "in_role_since": "May 2024 (~10 months)",
            "what_makes_them_tick": [
                "Transaction advisory DNA -- thinks in deal value and ROI, not monthly close cycles",
                "Process excellence background -- reduced man-hours by 50% through automation at EXL",
                "Relatively new to GM/FP&A role -- still shaping the function, looking to make his mark",
            ],
            "speak_their_language": "Frame everything in ROI and strategic impact. He's not a traditional FP&A person -- he came from M&A. Show him the deal value, not the reporting improvement.",
        }
    ],

    "team_roles": [
        {"name": "Mo", "role": "Relationship lead", "opens_with": "Context, discovery", "jumps_in_when": "Pain points surface", "owns": "Vision, narrative", "closes_with": "Next steps"},
        {"name": "Karim", "role": "Technical credibility", "opens_with": "Listens, takes notes", "jumps_in_when": "Technical questions", "owns": "Architecture, how", "closes_with": "Technical deep-dive offer"},
    ],
    "handoff_note": "Mo leads first 15 min. When it gets technical, Mo says: 'Karim built the Anova agent -- Karim, walk them through how it works.' Natural handoff signals depth.",

    "key_numbers": [
        {"label": "Revenue", "value": "$7.9B (FY2025, +4.1% YoY)"},
        {"label": "Net Profit", "value": "$205M (down 18% YoY)"},
        {"label": "Stores", "value": "267 across 6 GCC countries"},
        {"label": "EBITDA Margin", "value": "~9.8%"},
    ],

    "pressures": [
        {"pressure": "Profit -18%", "detail": "Net profit $205M vs $249M", "why_it_matters": "Board scrutinizing every cost line"},
        {"pressure": "Expansion", "detail": "50 new stores 2026-2028", "why_it_matters": "Every store needs ROI tracking"},
    ],

    "their_initiatives": [
        "SAP S/4HANA migration completed",
        "Agentic Commerce launched with Mastercard",
        "Predictive AI in supply chain and demand forecasting",
    ],
    "gap_callout": "FP&A has NOT been touched by AI yet. That's your lane.",

    "talking_points": [
        {"title": "1. OPEN -- Set Context", "owner": "Mo, 2 min", "points": [
            "\"I run Beam AI's Middle East operations. This is Karim, my co-founder.\"",
            "\"Our biggest deployment is with Americana Foods on FP&A.\"",
        ]},
        {"title": "2. DISCOVER -- Smart Questions", "owner": "Mo, 5-8 min", "points": [
            "\"How is FP&A structured at Lulu? How many people?\"",
            "\"What's the biggest time sink -- consolidation or variance analysis?\"",
        ]},
        {"title": "3. AMERICANA STORY", "owner": "Mo, 3-4 min", "is_proof_point": True, "points": [
            "Americana = largest food company in ME, 50% KIA-owned",
            "AI FP&A agent deployed in under 30 days, 728 hours/year saved",
        ]},
        {"title": "4. CLOSE", "owner": "Mo, 2 min", "is_close": True, "points": [
            "Don't quote a price. Don't try to close.",
            "\"Can we schedule the workflow mapping session for next week?\"",
        ]},
    ],

    "objections": [
        {"objection": "\"We just migrated to SAP\"", "response": "\"That's exactly why this works. The agent sits on top of SAP and makes your investment more valuable.\""},
        {"objection": "\"What about data security?\"", "response": "\"SOC2 Type II certified. Enterprise LLM endpoints -- no data retention, no model training on your data.\""},
    ],

    "killer_line": "\"Americana -- the largest food company in the Middle East, with a 30-year-old Oracle ERP -- deployed an AI FP&A agent in under 30 days. It saves them 728 hours a year. Lulu is bigger, more complex, and under more investor scrutiny. Imagine what this does for you.\"",

    "post_call_actions": [
        "Send thank-you note within 2 hours",
        "Propose FP&A workflow mapping session",
        "Send sample FP&A report as follow-up",
        "Log notes and next steps immediately",
    ],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a call prep PDF")
    parser.add_argument("--data", help="Path to JSON data file")
    parser.add_argument("--output", help="Output PDF path")
    parser.add_argument("--sample", action="store_true", help="Generate sample PDF using built-in data")
    args = parser.parse_args()

    if args.sample:
        build_call_prep_pdf(SAMPLE_DATA, args.output)
    elif args.data:
        with open(args.data, "r") as f:
            data = json.load(f)
        build_call_prep_pdf(data, args.output)
    else:
        print("Usage: --data <file.json> or --sample")
        print("Run with --sample to see an example output.")
