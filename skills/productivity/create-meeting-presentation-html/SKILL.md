---
name: create-meeting-presentation-html
version: '1.0'
description: Generate a self-contained HTML slide presentation for meetings. Load
  when user says "create presentation", "meeting presentation", "html presentation",
  "slide deck", "make slides", "presentation for meeting", "create slides for". User
  describes their use case, context, and goals — AI generates a polished dark-themed
  HTML deck with arrow-key navigation.
author: Hassaan Ahmed
category: general
tags:
- create
- meeting
updated: '2026-02-16'
visibility: public
---
# Create Meeting Presentation (HTML)

Generate a self-contained, browser-based HTML slide presentation from a user's meeting brief.

## Workflow

### Step 1: Gather Context

Ask the user (if not already provided):

1. **Meeting purpose** — What's this meeting about? (e.g., project review, sales pitch, sprint retro, alignment call)
2. **Audience** — Who are you presenting to? (e.g., client CEO, internal team, investors)
3. **Key points** — What needs to be covered? List the main topics or talking points
4. **Tone** — Professional / casual / diplomatic / persuasive
5. **Any data or files** — Documents, metrics, timelines, or context files to pull from
6. **Output location** — Where to save the HTML file (default: `04-workspace/`)

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

1. Save the file to the agreed location with a descriptive name:
   - Pattern: `{context}-presentation-{YYYY-MM-DD}.html`
   - Example: `quarterly-review-presentation-2026-03-01.html`
2. Open in Chrome: `open -a "Google Chrome" "{filepath}"`
3. Confirm with user and ask if any slides need adjustment

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
    <!-- Repeat for each agenda item -->
</div>
```

**Content Slide (generic):**
```html
<div class="slide" data-slide="N">
    <h3>{Section Label}</h3>
    <h2>{Slide Title}</h2>
    <!-- Content components below -->
</div>
```

### Content Components

**Table:**
```html
<table>
    <thead>
        <tr><th>Column 1</th><th>Column 2</th><th>Column 3</th></tr>
    </thead>
    <tbody>
        <tr><td>Data</td><td>Data</td><td>Data</td></tr>
    </tbody>
</table>
```

**Two-Column Layout:**
```html
<div class="two-col">
    <div class="col">
        <h4>{Left Title}</h4>
        <ul><li>{Item}</li></ul>
    </div>
    <div class="col">
        <h4>{Right Title}</h4>
        <ul><li>{Item}</li></ul>
    </div>
</div>
```

**Two-Column with Colored Borders (for contrast cards):**
```html
<div class="two-col">
    <div class="col" style="border: 2px solid #1a3a1a;">
        <h4 style="color: #4ade80;">{Positive Label}</h4>
        <p style="font-size: 22px; color: #fff;">{Title}</p>
        <p style="color: #888; font-size: 15px;">{Description}</p>
    </div>
    <div class="col" style="border: 2px solid #1a1a3a;">
        <h4 style="color: #818cf8;">{Neutral Label}</h4>
        <p style="font-size: 22px; color: #fff;">{Title}</p>
        <p style="color: #888; font-size: 15px;">{Description}</p>
    </div>
</div>
```

**Highlight Box (callout):**
```html
<div class="highlight-box">
    <p><strong>{Key point}</strong> {supporting text}</p>
</div>
```

**Timeline:**
```html
<div class="timeline">
    <div class="timeline-item">
        <div class="date">{Date or period}</div>
        <div class="event"><strong>{Phase}:</strong> {Description}</div>
    </div>
    <!-- Repeat -->
</div>
```

**Status Badges:**
```html
<span class="status done">Delivered</span>
<span class="status partial">In Progress</span>
<span class="status deferred">Deferred</span>
<span class="status not-started">Not Started</span>
```

**Big Number (metrics):**
```html
<div>
    <div class="big-number">{Value}</div>
    <div class="big-number-label">{Label}</div>
</div>
```

**Strikethrough Amount (before/after comparison):**
```html
<div style="display: flex; gap: 40px; align-items: center;">
    <div>
        <div class="amount-strike" style="font-size: 40px;">{Old Value}</div>
        <div style="color: #555; font-size: 14px;">{Old Label}</div>
    </div>
    <div style="font-size: 40px; color: #444;">&rarr;</div>
    <div>
        <div class="big-number" style="font-size: 40px; color: #4ade80;">{New Value}</div>
        <div style="color: #555; font-size: 14px;">{New Label}</div>
    </div>
</div>
```

**Next Steps List:**
```html
<ul class="next-steps-list">
    <li>
        <span class="step-icon">1</span>
        <div><strong>{Action}</strong> &mdash; {Details}</div>
    </li>
    <!-- Repeat -->
</ul>
```

**Divider:**
```html
<div class="divider"></div>
```

**Badge (inline label):**
```html
<span class="badge">{Label}</span>
```

### Fixed Elements (always included)

```html
<div class="logo-bar">{Label}</div>
<div class="slide-number"><span id="current">1</span> / <span id="total"></span></div>
<div class="nav-hint">&#8592; &#8594; arrow keys to navigate</div>
```

### JavaScript (always included)

```html
<script>
    const slides = document.querySelectorAll('.slide');
    let current = 0;
    document.getElementById('total').textContent = slides.length;
    function showSlide(n) {
        slides[current].classList.remove('active');
        current = (n + slides.length) % slides.length;
        slides[current].classList.add('active');
        document.getElementById('current').textContent = current + 1;
    }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); showSlide(current + 1); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); showSlide(current - 1); }
    });
    let touchStartX = 0;
    document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
    document.addEventListener('touchend', (e) => {
        const diff = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 50) { diff > 0 ? showSlide(current + 1) : showSlide(current - 1); }
    });
</script>
```

---

## Style Reference (full CSS)

The complete CSS block to include in every generated presentation:

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0a0a; color: #e0e0e0;
    overflow: hidden; height: 100vh; width: 100vw;
}
.slide {
    display: none; flex-direction: column; justify-content: center;
    padding: 60px 100px; height: 100vh; width: 100vw;
    animation: fadeIn 0.4s ease;
}
.slide.active { display: flex; }
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.slide-number {
    position: fixed; bottom: 30px; right: 40px;
    font-size: 14px; color: #555; font-variant-numeric: tabular-nums;
}
.logo-bar {
    position: fixed; top: 30px; left: 40px;
    font-size: 13px; color: #444; letter-spacing: 1px; text-transform: uppercase;
}
h1 { font-size: 48px; font-weight: 700; line-height: 1.2; margin-bottom: 20px; color: #fff; }
h2 { font-size: 36px; font-weight: 600; margin-bottom: 30px; color: #fff; }
h3 { font-size: 20px; font-weight: 600; color: #8b9cf7; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
.subtitle { font-size: 22px; color: #888; margin-bottom: 40px; line-height: 1.5; }
.agenda-item { display: flex; align-items: flex-start; gap: 20px; padding: 20px 0; border-bottom: 1px solid #1a1a1a; }
.agenda-item:last-child { border-bottom: none; }
.agenda-num { font-size: 32px; font-weight: 700; color: #8b9cf7; min-width: 50px; }
.agenda-content h4 { font-size: 22px; font-weight: 600; color: #fff; margin-bottom: 4px; }
.agenda-content p { font-size: 16px; color: #777; }
.agenda-time { font-size: 14px; color: #555; margin-left: auto; white-space: nowrap; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; }
th { text-align: left; padding: 14px 20px; background: #141414; color: #8b9cf7; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid #222; }
td { padding: 16px 20px; border-bottom: 1px solid #1a1a1a; font-size: 16px; color: #ccc; }
tr:hover td { background: #111; }
.status { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }
.status.done { background: #0f2d1a; color: #4ade80; }
.status.partial { background: #2d2a0f; color: #facc15; }
.status.deferred { background: #1a1a2e; color: #818cf8; }
.status.not-started { background: #2d0f0f; color: #f87171; }
.highlight-box { background: #141420; border-left: 4px solid #8b9cf7; padding: 24px 30px; border-radius: 0 12px 12px 0; margin: 20px 0; }
.highlight-box p { font-size: 18px; line-height: 1.6; color: #bbb; }
.highlight-box strong { color: #fff; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 20px; }
.col { background: #111; border-radius: 12px; padding: 30px; }
.col h4 { font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #fff; }
.col ul { list-style: none; padding: 0; }
.col li { padding: 8px 0; font-size: 16px; color: #aaa; border-bottom: 1px solid #1a1a1a; }
.col li:last-child { border-bottom: none; }
.big-number { font-size: 52px; font-weight: 700; color: #8b9cf7; }
.big-number-label { font-size: 16px; color: #666; margin-top: 4px; }
.proposal-option { background: #111; border: 2px solid #1a1a1a; border-radius: 12px; padding: 30px; margin: 15px 0; }
.proposal-option.recommended { border-color: #8b9cf7; background: #111118; }
.proposal-option h4 { font-size: 20px; color: #fff; margin-bottom: 8px; }
.proposal-option p { font-size: 16px; color: #999; line-height: 1.5; }
.badge { display: inline-block; background: #8b9cf7; color: #0a0a0a; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 4px; margin-left: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.timeline { position: relative; padding-left: 30px; margin-top: 10px; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: #222; }
.timeline-item { position: relative; padding: 16px 0; }
.timeline-item::before { content: ''; position: absolute; left: -27px; top: 22px; width: 12px; height: 12px; border-radius: 50%; background: #8b9cf7; border: 2px solid #0a0a0a; }
.timeline-item .date { font-size: 13px; color: #555; margin-bottom: 4px; }
.timeline-item .event { font-size: 17px; color: #ccc; }
.nav-hint { position: fixed; bottom: 30px; left: 40px; font-size: 13px; color: #333; }
.amount-strike { text-decoration: line-through; color: #555; }
.amount-new { color: #4ade80; font-weight: 700; }
.divider { height: 1px; background: #222; margin: 30px 0; }
.next-steps-list { list-style: none; padding: 0; margin-top: 10px; }
.next-steps-list li { display: flex; align-items: flex-start; gap: 14px; padding: 14px 0; font-size: 18px; color: #ccc; border-bottom: 1px solid #1a1a1a; }
.next-steps-list li:last-child { border-bottom: none; }
.step-icon { width: 28px; height: 28px; background: #141420; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; margin-top: 2px; }
.title-slide { justify-content: center; align-items: center; text-align: center; }
.title-slide h1 { font-size: 56px; margin-bottom: 10px; }
.title-slide .subtitle { font-size: 20px; max-width: 500px; }
.meta { font-size: 14px; color: #444; margin-top: 30px; }
```

---

## Guidelines

- **Self-contained**: No external CSS, JS, fonts, or images. Everything inline.
- **Responsive-ish**: Works in fullscreen browser. Touch support for tablets.
- **Slide count**: Aim for 5-10 slides. More than 12 is too many for a meeting.
- **Text density**: Less is more. If a slide has more than ~6 lines of text, split it.
- **Data first**: If the user provides files, contracts, metrics — pull real data into slides.
- **Confirm before generating**: Always show the slide outline and get approval before writing the full HTML.

---

## Output

```json
{
  "file_path": "path/to/presentation.html",
  "slide_count": N,
  "estimated_duration": "X min",
  "opened_in": "Chrome"
}
```
