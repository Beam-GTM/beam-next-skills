---
name: create-meeting-presentation-html
description: Generate a self-contained HTML slide presentation for meetings. Load when user says "create presentation", "meeting presentation", "html presentation", "slide deck", "make slides", "presentation for meeting", "create slides for". Saves HTML next to session context when possible — account projects (03-projects/accounts), lead folders (04-workspace/leads), or customer workspace — not only 04-workspace root. User describes use case, context, and goals; AI produces a polished dark-themed HTML deck with arrow-key navigation.
---

# Create Meeting Presentation (HTML)

Generate a self-contained, browser-based HTML slide presentation from a user's meeting brief.

## Output path (resolve before generating HTML)

**Do not default to `04-workspace/` root** if a better anchor exists. Pick the save directory in this order:

1. **User explicitly gives a path** — Use it (create the directory if needed after confirming with the user when non-obvious).

2. **Last interaction / session anchor** — If the user @-referenced files, has open editor paths, or recent messages include a repo path, treat that as the anchor:
   - If the anchor is a **file**, the default save dir is **the directory containing that file**.
   - If the anchor is already a **directory**, save there.

3. **Customer account project** — If the meeting is tied to an account under `03-projects/accounts/{id}-{name}/` (from conversation, open files, or overview/deal docs):
   - Save under **`03-projects/accounts/{id}-{name}/04-outputs/`** (create `04-outputs/` if missing). This matches how account deliverables (decks, reports) are stored.
   - If the user is clearly working only in `03-working/` for this thread and asks to keep everything there, you may save alongside those working files instead — prefer `04-outputs/` for anything you'd send externally.

4. **Lead (pre-account)** — If the company matches a folder under `04-workspace/leads/`, save into **`04-workspace/leads/{company-slug}/`** (same pattern as prospecting and call-analysis). Fuzzy-match company name to existing folder names.

5. **Customer workspace** — If context points at **`04-workspace/customer/{account}/`**, save there.

6. **Fallback** — `04-workspace/` (repo root of workspace) **or** ask once: "No account/lead path found — save under `04-workspace/` or tell me the folder?"

**Always state the chosen path** in the outline step ("Saving to: `…`") so the user can correct it before you write the file.

---

## Workflow

### Step 1: Gather Context

Ask the user (if not already provided):

1. **Meeting purpose** — What's this meeting about? (e.g., project review, sales pitch, sprint retro, alignment call)
2. **Audience** — Who are you presenting to? (e.g., client CEO, internal team, investors)
3. **Key points** — What needs to be covered? List the main topics or talking points
4. **Tone** — Professional / casual / diplomatic / persuasive
5. **Any data or files** — Documents, metrics, timelines, or context files to pull from
6. **Output location** — Only ask if steps above did not yield a path (see **Output path**). Otherwise confirm the resolved directory in one short line.

**Do NOT ask all at once.** If the user already described their use case in detail, extract what you can and only ask for missing critical info.

### Step 2: Plan the Slide Structure

Before writing any HTML, outline the slides:

```
Proposed slides:
1. Title slide — [Title], [Subtitle], [Date]
2. Agenda — [N items with time estimates]
3. [Topic slide] — [Content type: timeline / table / two-col / highlight box]
4. ...
N. [Final slide] — [Closing / discussion / next steps]

Total: ~X slides, ~Y min estimated
```

**Present this outline to the user for approval before generating.**

### Step 3: Generate the HTML

Write a single self-contained `.html` file using the component library below. Key rules:

**Structure:**
- Every slide is a `<div class="slide">` (first slide gets `class="slide title-slide active"`)
- Sequential `data-slide="1"`, `data-slide="2"`, etc.
- Logo bar text uses `{Party A} x {Party B}` or `{Company}` format
- Date and "Confidential" in the meta line on title slide

**Content principles:**
- Keep text concise — slides are for presenting, not reading
- Use tables for structured comparisons
- Use two-col layout for side-by-side concepts
- Use timeline for chronological events
- Use highlight-box for key callouts or important notes
- Use status badges for delivery/progress tracking
- Use big-number for impactful metrics

**Navigation:**
- Arrow keys (left/right) and spacebar
- Touch swipe support for mobile/tablet
- Slide counter in bottom-right

### Step 4: Save and Open

1. `mkdir -p` the target directory if it does not exist (especially `04-outputs/` on account projects).
2. Save the file to the **resolved** location (see **Output path**) with a descriptive name:
   - Pattern: `{context}-presentation-{YYYY-MM-DD}.html`
   - Example: `quarterly-review-presentation-2026-03-01.html`
3. Open in Chrome: `open -a "Google Chrome" "{filepath}"` (macOS)
4. Confirm with user and ask if any slides need adjustment

---

## Component Library

Use these CSS classes and patterns when building slides. All styles are embedded in the HTML — no external dependencies.

### Theme

```
Background: #0a0a0a
Text primary: #fff
Text secondary: #ccc
Text muted: #888 / #666 / #555
Accent: #8b9cf7 (purple-blue)
Success: #4ade80 (green)
Warning: #facc15 (yellow)
Danger: #f87171 (red)
Info: #818cf8 (indigo)
Surface: #111
Surface elevated: #141414 / #141420
Borders: #1a1a1a / #222
```

### Slide Types

**Title Slide:**
```html
<div class="slide title-slide active" data-slide="1">
    <h3 style="margin-bottom: 20px;">{Label / Parties}</h3>
    <h1>{Main Title}</h1>
    <p class="subtitle">{One-line description}</p>
    <p class="meta">{Date} &middot; Confidential</p>
</div>
```

**Agenda Slide:**
```html
<div class="slide" data-slide="2">
    <h2>Agenda</h2>
    <div class="agenda-item">
        <span class="agenda-num">01</span>
        <div class="agenda-content">
            <h4>{Topic}</h4>
            <p>{Brief description}</p>
        </div>
        <span class="agenda-time">{N} min</span>
    </div>
</div>
```

**Content Slide:**
```html
<div class="slide" data-slide="N">
    <h3>{Section Label}</h3>
    <h2>{Slide Title}</h2>
</div>
```

### Content Components

**Table, Two-Col, Highlight Box, Timeline, Status Badges, Big Number, Next Steps List, Divider, Badge** as documented.

### Fixed Elements

```html
<div class="logo-bar">{Label}</div>
<div class="slide-number"><span id="current">1</span> / <span id="total"></span></div>
<div class="nav-hint">&#8592; &#8594; arrow keys to navigate</div>
```

### JavaScript & CSS

Full navigation JS (arrow keys, spacebar, touch swipe) and dark-themed CSS as documented.

---

## Guidelines

- Self-contained: no external dependencies
- 5-10 slides (12 max)
- Less text per slide
- Pull real data from any files provided
- Always show outline first, get approval before generating full HTML

---

## Output

Save with pattern `{context}-presentation-{YYYY-MM-DD}.html` under the directory from **Output path** (account `04-outputs/`, lead folder, customer folder, directory of anchor file, or `04-workspace/` fallback), then open in Chrome.
