---
name: markdown-to-pdf
version: '1.0'
description: "Convert markdown files to professionally styled PDFs. Triggers: 'render pdf', 'markdown to pdf', 'create pdf', 'export pdf', 'generate pdf', 'make pdf'."
category: tools
tags:
  - pdf
  - markdown
  - export
  - documents
requires:
  - markdown2pdf-mcp (npm, global)
updated: '2026-03-03'
visibility: public
---
# Markdown to PDF

Render any markdown file as a clean, professionally styled PDF using Puppeteer. Ideal for legal documents, letters, proposals, and reports.

## Prerequisites

`markdown2pdf-mcp` must be installed globally (provides puppeteer + remarkable):

```bash
npm install -g markdown2pdf-mcp
```

## Workflow

### Step 1: Identify the source file

Ask the user which markdown file to render, or infer from context. Read the file to confirm contents.

### Step 2: Choose styling preset

| Preset | Font | Use case |
|--------|------|----------|
| `legal` | Times New Roman, 11pt, justified | Declarations, contracts, NDAs |
| `business` | Helvetica/Arial, 11pt, left-aligned | Letters, proposals, reports |
| `minimal` | System sans-serif, 10.5pt | Internal docs, notes |

Default to `legal` for anything contractual/formal, `business` otherwise. Ask only if ambiguous.

### Step 3: Render

Run the render script with the source file and preset:

```bash
NODE_PATH=/opt/homebrew/lib/node_modules/markdown2pdf-mcp/node_modules \
  node 00-system/skills/tools/markdown-to-pdf/scripts/render.js \
  --input "<source.md>" \
  --output "<output.pdf>" \
  --preset <legal|business|minimal>
```

### Step 4: Open for review

```bash
open "<output.pdf>"
```

Show the user the file path and size. Ask if they want styling adjustments before sending.

## MCP Integration

`markdown2pdf-mcp` is also configured as an MCP server in `~/.cursor/mcp.json` under key `markdown2pdf`. For simple conversions, the MCP tool `create_pdf_from_markdown` can be used directly once the server is recognized by Cursor.
