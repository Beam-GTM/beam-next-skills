# File Generation Reference

When the skill generates data with `--files`, each sample produces actual files (PDF, CSV, JSON, TXT) instead of just text strings.

## Design Philosophy: Reference Renderer + Subagent-Written Variants

`scripts/file_renderer.py` is the **reference implementation** — it shows one way to produce styled PDFs with fpdf2. It is NOT the single renderer for all files. Instead, **each subagent writes its own custom renderer** for its batch, using the reference as a starting point but producing a visually distinct output style.

**Why:** A single renderer has a visual ceiling. No matter how you vary the spec (layout, color, font), every PDF shares the same spacing logic, line weights, cell padding, margin calculations, and decorative patterns. A human looking at 10 such files immediately recognizes they came from the same system. In production, documents come from Word, Canva, LaTeX, ATS exports, Google Docs, handmade HTML-to-PDF, etc. — they share NO rendering logic. Subagent-written renderers replicate this real-world diversity.

**How it works:**

1. Each subagent receives: the **reference renderer** (`file_renderer.py`), a **visual archetype** (e.g., "Canva-style modern with heavy color blocks"), and the **content to render** (render spec JSON with sections/data).
2. The subagent **writes a fresh renderer script** (`renderer_N.py`) that produces the assigned archetype's visual style — different spacing algorithms, border treatments, font sizing ratios, decorative elements, table styling, margin proportions, etc.
3. The subagent **runs its custom renderer** to produce the output file, then the skill verifies it visually (Read the PDF).

**The reference renderer is still useful for:**
- Gold standards (Phase 1a) — quick iteration before batch generation
- Small batches (≤10 inline) where visual diversity matters less
- Fallback when a custom renderer fails after 2 retries

**Building any document type from the reference renderer's section types:**

| Document Type | How to Build It |
|---------------|----------------|
| **Invoices/POs** | `columns` for vendor/meta side-by-side, `columns` for bill-to/ship-to, `table` with `aligns` + `col_widths` for line items, `totals` for subtotal/tax/total |
| **CVs/Resumes** | `header` + `contact`, `entry` for work experience, `keyvalue` for skills, `list` for certifications. Use `sidebar` layout for modern CVs |
| **Lab reports** | `keyvalue` for patient info, `table` for test results with reference ranges, `text` for narrative summary |
| **Legal docs** | `heading` for clause titles, `text` for clause bodies, `keyvalue` for signature blocks |
| **Property listings** | `columns` for specs/features side-by-side, `table` for comparable sales, `keyvalue` for property details |

---

## Render Spec Schema

Each file is described by a render spec JSON object:

```json
{
  "layout": "single_column",
  "color_scheme": "blue",
  "font": "Helvetica",
  "page_header": "Optional - Confidential",
  "page_footer": true,
  "sections": [...]
}
```

**Top-level fields:**

| Field | Required | Options | Default |
|-------|----------|---------|---------|
| `layout` | No | `single_column`, `two_column`, `sidebar`, `tabular` | Random |
| `color_scheme` | No | `blue`, `green`, `gold`, `red`, `purple` | Random |
| `font` | No | `Helvetica`, `Courier`, `Times` | Random |
| `page_header` | No | Any string | None |
| `page_footer` | No | `true`/`false` | `false` |
| `sections` | Yes | Array of section objects | — |

If layout/color_scheme/font are omitted, the renderer picks randomly for variety.

---

## Section Types

Each section in the `sections` array has a `type` field and type-specific content:

### `header` — Document title
```json
{"type": "header", "content": "PRIYA RAJAGOPAL"}
```
Renders as large bold text in the primary color. Use for document titles, candidate names, company names.

### `contact` — Contact information line
```json
{"type": "contact", "content": "Toronto, ON | priya@email.com | (416) 555-0187"}
```
Renders as smaller text in the secondary color. Use pipe-separated contact details.

### `heading` — Section heading
```json
{"type": "heading", "content": "PROFESSIONAL EXPERIENCE"}
```
Renders as bold text with an underline in the primary color. Use for major document sections.

### `subheading` — Subsection heading
```json
{"type": "subheading", "content": "Technical Skills"}
```
Renders as bold text in the secondary color, smaller than heading.

### `text` — Paragraph text
```json
{"type": "text", "content": "A paragraph of descriptive text..."}
```
Renders as normal body text. Auto-wraps.

### `entry` — Titled entry with optional bullets
```json
{
  "type": "entry",
  "title": "Senior Software Engineer",
  "subtitle": "Vantage Commerce | Toronto, ON | 2021-Present",
  "bullets": [
    "Led backend architecture for order management platform",
    "Redesigned inventory sync service reducing latency by 85%"
  ]
}
```
Renders title in bold, subtitle in italic secondary color, bullets indented. Use for work experience, education entries, project descriptions.

### `table` — Data table
```json
{
  "type": "table",
  "headers": ["Item", "Quantity", "Unit Price", "Total"],
  "rows": [
    ["Widget A", "100", "$12.50", "$1,250.00"],
    ["Widget B", "50", "$8.75", "$437.50"]
  ]
}
```
Renders as a styled table with colored header row and alternating row backgrounds.

### `list` — Bulleted list
```json
{"type": "list", "items": ["Python", "TypeScript", "Go", "SQL"]}
```
Renders as indented bullet points.

### `keyvalue` — Key-value pairs
```json
{
  "type": "keyvalue",
  "pairs": [
    ["Languages", "Python, TypeScript, Go"],
    ["Databases", "PostgreSQL, MongoDB, Redis"],
    ["Cloud", "AWS, GCP"]
  ]
}
```
Renders keys in bold, values in secondary color. Use for skills, metadata, summary fields.

### `columns` — Side-by-side blocks (NEW)
```json
{
  "type": "columns",
  "widths": [0.55, 0.40],
  "gap": 0.05,
  "columns": [
    [{"type": "header", "content": "Left Block"}, {"type": "text", "content": "..."}],
    [{"type": "header", "content": "Right Block"}, {"type": "keyvalue", "pairs": [...]}]
  ]
}
```
Renders N blocks side-by-side. Each column is an array of sections. `widths` are fractions of page width, `gap` is the fractional gap between columns. Use for: vendor info + invoice meta, bill-to + ship-to, property specs + features, patient info + specimen info.

### `totals` — Right-aligned totals block (NEW)
```json
{
  "type": "totals",
  "rows": [
    {"label": "Subtotal:", "value": "$1,234.56"},
    {"label": "Tax (13%):", "value": "$160.49"},
    {"label": "Grand Total:", "value": "$1,395.05"}
  ],
  "bold_last": true
}
```
Renders right-aligned label/value pairs with a separator line before the last row. Use for: invoice totals, order summaries, financial summaries.

### `accent_bar` — Colored decorative element (NEW)
```json
{"type": "accent_bar", "position": "left", "width": 4}
```
Draws a colored bar. `position`: "left" (vertical bar on left edge) or "top" (horizontal band across top, use `height` field). Use for: modern minimal layouts, branded headers.

### `colored_box` — Background box with nested content (NEW)
```json
{
  "type": "colored_box",
  "height": 30,
  "sections": [{"type": "keyvalue", "pairs": [["Invoice #", "INV-2026-001"]]}]
}
```
Draws a light-colored background box and renders inner sections on top. Use for: highlighted info blocks, callout boxes, metadata panels.

### `divider` — Horizontal line
```json
{"type": "divider"}
```

### `spacer` — Vertical whitespace
```json
{"type": "spacer", "height": 10}
```

---

## Layout Templates

### `single_column`
Classic top-to-bottom document. All sections render in sequence at full page width.

**Best for:** Job descriptions, letters, reports, plain CVs, contracts, policies.

### `two_column`
Header/contact sections span full width, then remaining sections split into two equal columns.

**Best for:** Modern CVs, newsletters, comparison documents, side-by-side content.

### `sidebar`
Narrow left column (30% width, shaded background) + wide main column (65% width). The renderer auto-routes section types:
- Sidebar gets: `contact`, `list`, `keyvalue`, `table`
- Main gets: `header`, `heading`, `subheading`, `entry`, `text`

**Best for:** Styled CVs, profile documents, product spec sheets.

### `tabular`
Emphasizes tables with extra spacing and a bolder document header with thick underline. Other sections render normally.

**Best for:** Invoices, purchase orders, spec sheets, data-heavy documents.

---

## Color Schemes

| Name | Primary | Use case |
|------|---------|----------|
| `blue` | Corporate blue (#1F4E79) | Professional docs, corporate reports |
| `green` | Forest green (#548235) | Environmental, health, fresh look |
| `gold` | Deep gold (#BF8F00) | Financial docs, premium feel |
| `red` | Crimson (#C00000) | Urgent docs, bold branding |
| `purple` | Royal purple (#7030A0) | Creative, modern, tech branding |

---

## File Naming Conventions

Files should use **realistic client naming conventions**, not generic test names. Choose a naming style that matches the document type and domain:

| Style | Pattern | Example |
|-------|---------|---------|
| Professional | `Firstname_Lastname_CV_2026.pdf` | `Priya_Rajagopal_CV_2026.pdf` |
| Corporate | `DOC-TYPE-YYYY-NNNN.pdf` | `PO-2024-0847.pdf`, `INV-2026-1234.pdf` |
| Casual | `descriptive-name.pdf` | `senior-backend-engineer-jd.pdf` |
| System | `ENTITY_identifier_date.ext` | `candidate_cv_JO-2026-0482.pdf` |

**Rules:**
- Never use `test-1.pdf`, `sample-01.pdf`, or `output.json`
- Match naming to the domain (HR uses name-based, finance uses code-based)
- Include dates, reference numbers, or identifiers where realistic

---

## Multi-File Samples

A single sample can contain multiple related files. For example:

**CV Evaluation sample:**
- `input_data/Priya_Rajagopal_Resume.pdf` (sidebar layout, purple scheme)
- `input_data/NovaCrest_Senior_Backend_Engineer_JD.pdf` (single_column, blue scheme)
- `output_data/evaluation_JO-2026-0482.json`

**Purchase Order sample:**
- `input_data/PO-2024-0847.pdf` (tabular layout, gold scheme)
- `input_data/supplier-spec-sheet.pdf` (single_column, blue scheme)
- `input_data/allergen-declaration.csv`
- `output_data/extracted-fields.json`
- `output_data/compliance-summary.csv`

Each file in a sample should have a **different layout/color combination** for maximum variety.

---

## Visual Diversity Protocol (CRITICAL)

**Every rendered file in a dataset MUST be visually unique — not just in content, but in rendering DNA.** In production, documents come from hundreds of different software systems (Canva, Word, LaTeX, LinkedIn export, ATS systems, handmade HTML-to-PDF). They don't share spacing logic, border treatments, font sizing ratios, or decorative patterns. A dataset where all PDFs "feel" the same — even with different colors and layouts — fails to test parser robustness.

### Core Mechanism: Subagent-Written Renderers

Instead of varying specs on a single renderer, **each subagent writes its own renderer script**. This produces files with genuinely different visual DNA — different spacing algorithms, border treatments, margin proportions, table styling, decorative elements, and text rendering approaches.

**Each subagent receives:**
1. **Reference renderer** (`file_renderer.py`) — "here's one way to make a PDF with fpdf2"
2. **Visual archetype assignment** — a description of the target visual style (see archetypes below)
3. **Render spec** — the content/sections to render (same format as before)
4. **Instruction:** "Write a fresh renderer that produces this content in the assigned visual style. The output must look like it came from a completely different software system than the reference renderer. Change spacing logic, border treatments, font sizing ratios, decorative elements, table styling, margin proportions, etc."

**Each subagent produces:**
1. `renderer_N.py` — custom renderer script
2. Runs it → output file(s)
3. Returns 1-line summary + file paths

### Visual Archetypes

Assign one archetype per subagent. These describe the **software system the document appears to come from**, not just surface-level color/font choices. The subagent must write rendering logic that matches the archetype's DNA.

| Archetype | Visual DNA | Rendering Characteristics |
|-----------|-----------|--------------------------|
| **ATS Export** | Dense, monospace, system-generated feel | Courier font, tight line spacing (1.0), no decorative elements, simple horizontal rules, left-aligned everything, grey headers, machine-like consistency |
| **Canva Modern** | Heavy color blocks, bold geometry | Large colored header banner (full-width rect), generous whitespace (2.0 line spacing), rounded-feel sections (colored background boxes), icon-placeholder markers, asymmetric margins |
| **Word Classic** | Times New Roman, conservative structure | Standard 1-inch margins, 1.15 line spacing, simple black text, minimal color (only in headings), tab-stop aligned dates, traditional bullet points (round dots) |
| **LaTeX Academic** | Computer Modern feel, precise typesetting | Justified text, thin ruled lines, small caps headings, precise mathematical spacing, section numbering (1.1, 1.2), minimal decorative elements, serif throughout |
| **Google Docs Casual** | Clean sans-serif, light and airy | Generous margins, 1.5 line spacing, subtle grey dividers, left-aligned everything, no bold colors, section gaps larger than line gaps, simple bullet dashes |
| **LinkedIn Export** | Branded, structured, card-like | Blue accent color, card-like sections with subtle borders, profile-header pattern (name large, title smaller, location smallest), skills as tags/chips, endorsement counts |
| **Handmade HTML-to-PDF** | Inconsistent, slightly broken | Mixed font sizes that don't quite match, inconsistent margins between sections, some sections indented more than others, occasional orphaned headers, amateur color choices |
| **InDesign Premium** | Magazine-quality, sophisticated | Multi-column with baseline grid, drop caps, pull quotes in accent color, thin hairline rules, small body text (9pt) with generous leading, wide outer margins |
| **Government Form** | Bureaucratic, box-heavy, structured | Bordered boxes for every field group, field labels in small caps above values, reference numbers in headers, sequential section numbering, stamps/seals area, monospace for codes |
| **Startup Minimal** | Ultra-clean, lots of negative space | One accent color only, thin weight fonts, no borders or rules, section breaks via whitespace alone, icons as section markers, asymmetric layout, generous page margins (1.5 inch) |
| **Excel-to-PDF** | Gridlines everywhere, tabular feel | Visible cell borders on everything, alternating row colors, column-aligned numbers, auto-fit column widths, sheet-tab footer, landscape orientation option |
| **Scanned Photocopy** | Degraded, slightly rotated, noisy | Slight grey background (#f5f5f5), text not perfectly aligned to margins, occasional "smudge" (grey rectangles), lower contrast text, slightly larger margins (simulating scan border) |

**Archetype assignment rules:**
- Never assign the same archetype twice in one batch
- For batches larger than 12 files, combine archetypes with modifier instructions (e.g., "LaTeX Academic BUT with color accents" or "Canva Modern BUT dense/compact")
- Each subagent's renderer must differ in **rendering logic**, not just parameter values — different spacing calculations, different border-drawing approaches, different section composition strategies

### What the Subagent Must Change (Not Just Parameters)

The point is NOT "use the reference renderer with different color values." The subagent must write rendering code that **works differently**:

| Rendering Dimension | What to vary | Example differences |
|--------------------|-------------|-------------------|
| **Spacing algorithm** | How vertical space is calculated between elements | Fixed 5mm gaps vs proportional (heading size × 0.4) vs context-dependent (more after tables, less after text) |
| **Border treatments** | How lines/borders/rules are drawn | Thick colored underlines vs thin grey hairlines vs no lines (whitespace only) vs full box borders |
| **Table rendering** | How tabular data is styled | Colored header row + alternating stripes vs minimal (top/bottom rules only) vs full grid vs borderless with bold headers |
| **Font sizing ratios** | Relationship between heading/body/caption sizes | 24/12/9 (dramatic) vs 14/11/9 (conservative) vs 18/10/8 (modern) |
| **Margin proportions** | Page margins and inner padding | Symmetric 1" vs asymmetric (wide left for binding) vs narrow (maximizes content) vs generous (premium feel) |
| **Decorative elements** | Visual accents beyond content | Accent bars, colored boxes, background shapes, watermarks, pull quotes, horizontal rules |
| **Text alignment** | How body text is positioned | Left-aligned vs justified vs centered headers + left body vs ragged-right |
| **Color usage** | How color is applied | Monochrome + one accent vs full-color headers + muted body vs all-grey + colored links vs high-contrast throughout |

### Anti-Patterns (NEVER DO)

- **Spec-only variation on the shared renderer** — changing `color_scheme: "blue"` to `"green"` on the same renderer does NOT produce visual diversity. The spacing, borders, and rendering logic are identical.
- **Copy-paste the reference renderer with minor tweaks** — changing 3 color values and a font name is not a "custom renderer." The subagent must restructure how sections are composed and spaced.
- **All renderers using the same section ordering logic** — the reference renderer renders sections top-to-bottom. Some archetypes should use column-first, sidebar-first, or grid-based approaches.
- **Ignoring the archetype's DNA** — "ATS Export" means dense and mechanical. If the subagent produces something airy and colorful, it failed the assignment regardless of code differences.

### Fallback: Reference Renderer

If a subagent's custom renderer fails (broken PDF, rendering errors) after 2 fix attempts:
1. Fall back to the reference renderer (`file_renderer.py`) with the original render spec
2. Log the failure for post-generation feedback
3. Flag the sample as "reference-rendered" in metadata (lower visual diversity score)

### Visual Diversity for Non-PDF Formats

The same principle — subagent-written rendering code — applies to ALL file types. Each format has its own rendering dimensions that must vary at the code level, not just parameters.

**DOCX:** Different python-docx styling code — paragraph spacing objects, table style definitions, heading format overrides, margin calculations, font registrations. One renderer builds conservative Word docs, another builds modern styled documents.

**XLSX:** Different openpyxl styling — cell border objects, fill patterns, column width algorithms, number format strings, conditional formatting rules, chart styles. One builds clean financial spreadsheets, another builds colorful dashboards.

**CSV:** Different csv module usage — delimiters (comma, semicolon, tab, pipe), quoting strategies, header casing transforms, column ordering logic, encoding choices, BOM presence.

**HTML:** Different CSS generation — grid vs flexbox vs table layout, color palette generation, font stacks, responsive breakpoints, component patterns (cards vs lists vs tables).

---

## Domain-Specific Rendering Guidance

When assigning visual archetypes for domain-specific documents, include these production patterns in the subagent's brief so it knows what real-world variety looks like.

### Invoice / Purchase Order — Production Patterns

Production invoices have massive visual variety. Include this context in the subagent's archetype assignment:

**Layout patterns seen in production:**

| Pattern | Description | Frequency |
|---------|-------------|-----------|
| **Classic tabular** | Letterhead top, addresses below, line item table, totals block | 40% |
| **Modern minimal** | Clean sans-serif, lots of whitespace, accent color bar, compact table | 20% |
| **Dense commercial** | Small fonts, multiple tables (header info, line items, terms), maximizes info per page | 15% |
| **Two-column header** | Company info left, invoice details right, full-width table below | 15% |
| **Branded template** | Heavy color usage, sidebar with company info, styled table | 10% |

**Elements that vary across vendors:**

| Element | Variations |
|---------|-----------|
| **Header block** | Company name + address top-left, logo placeholder top-right. Or centered. Or right-aligned with invoice details left. |
| **Address blocks** | Bill-to / Ship-to side-by-side, or stacked, or Bill-to only. Labels vary: "Bill To", "Invoice To", "Customer", "Sold To" |
| **Invoice metadata** | Invoice #, Date, Due Date, PO Reference, Payment Terms, Currency. Position: top-right block, or below addresses, or in a header table |
| **Line item table** | Columns vary: Item/Description/Qty/Unit Price/Amount (minimal) to Item Code/Description/UOM/Qty/Unit Price/Discount%/Tax/Line Total (complex). Some include sub-items or notes per line. |
| **Subtotals block** | Right-aligned: Subtotal, Discount, Tax (GST/HST/PST breakdown or single), Shipping, Grand Total. Or in a summary table. |
| **Footer** | Payment terms, bank details (wire instructions), late payment penalties, "Thank you for your business" |
| **Multi-page behavior** | Table continues with "Continued on next page" / repeated column headers. Running subtotal per page. Final page has totals. |

**File naming for invoices:**
- `INV-2026-04821.pdf`, `PO-2024-0847-rev2.pdf`
- `Supplier_Name_Invoice_Apr2026.pdf`
- `20260415_CloudTech_Solutions_INV.pdf`

**Key implementation hints for subagent renderers:**
- Use `pdf.set_xy()` for fixed-position header/address blocks (not linear flow)
- Track y-position for line item table; on page break, re-render column headers
- Calculate totals from line items (subtotal, tax, total) — don't just render static text
- Vary the number of line items (3-50) to test small and multi-page invoices
- Include realistic tax handling (Canadian GST/HST, or US sales tax, depending on domain)

### Example: Invoice via Reference Renderer (Gold Standards / Small Batches)

For gold standards or small inline batches, the reference renderer works fine:

```json
{
  "layout": "single_column",
  "color_scheme": "gold",
  "font": "Times",
  "page_footer": true,
  "sections": [
    {"type": "columns", "widths": [0.55, 0.40], "gap": 0.05, "columns": [
      [{"type": "header", "content": "VENDOR NAME", "size": 14}, {"type": "text", "content": "Address...", "size": 9}],
      [{"type": "header", "content": "FACTURE", "size": 18}, {"type": "keyvalue", "pairs": [["Date", "25.03.2026"]]}]
    ]},
    {"type": "columns", "widths": [0.45, 0.45], "gap": 0.10, "columns": [
      [{"type": "subheading", "content": "FACTURER À :"}, {"type": "text", "content": "Customer..."}],
      [{"type": "subheading", "content": "LIVRER À :"}, {"type": "text", "content": "Ship to..."}]
    ]},
    {"type": "table", "headers": ["Réf.", "Description", "Qté", "Prix"], "aligns": ["L","L","R","R"], "col_widths": [0.12,0.48,0.15,0.22], "rows": [...]},
    {"type": "totals", "rows": [{"label": "Total HT :", "value": "7.122,00 EUR"}, {"label": "TVA 20%:", "value": "1.424,40 EUR"}, {"label": "Total TTC :", "value": "8.546,40 EUR"}], "bold_last": true}
  ]
}
```

For batch generation (11+ files), subagents write custom invoice renderers per archetype — one produces "Classic tabular" with dense grid styling, another produces "Modern minimal" with accent bars and whitespace.

---

## Rendering from Plain Text

If the LLM generates plain text instead of a render spec, the renderer auto-parses it:
- ALL-CAPS lines → headings (first one becomes header)
- Pipe-separated lines → contact info
- Lines starting with `- ` or `• ` → bullet lists
- Consecutive `Key: Value` lines → key-value pairs
- Everything else → paragraph text

Use `raw_text` field instead of `sections`:
```json
{
  "raw_text": "PRIYA RAJAGOPAL\nToronto, ON | priya@email.com\n\nPROFESSIONAL EXPERIENCE\n...",
  "layout": "sidebar",
  "color_scheme": "purple"
}
```

---

## CLI Usage

```bash
# Render from a spec file
python scripts/file_renderer.py spec.json --output path/to/file.pdf

# Override layout/color/font
python scripts/file_renderer.py spec.json --output file.pdf --layout sidebar --color-scheme purple --font Times

# Render to other formats
python scripts/file_renderer.py spec.json --output file.txt
python scripts/file_renderer.py spec.json --output file.csv
python scripts/file_renderer.py spec.json --output file.json

# Read spec from stdin
cat spec.json | python scripts/file_renderer.py - --output file.pdf
```
