---
name: calendar-cleanup
version: '1.0'
description: "Suggest what to do with upcoming meetings. Load when user says calendar
  cleanup, clean up my calendar, which meetings should I decline, review my meetings.
  Uses calendar (Google Calendar or export) and optionally goals/focus to produce
  per-meeting suggestions (decline, shorten, delegate, merge, or keep)."
category: productivity
tags:
- calendar
- meetings
- focus
visibility: public
updated: '2026-02-27'
---
# Calendar Cleanup

Suggest what to do with meetings so your calendar aligns with what matters.

## Purpose

Turn a packed calendar into actionable suggestions: which meetings to decline, shorten, delegate, merge, or keep. Optionally uses goals or "this week's focus" from `02-memory/goals.md` (or `weekly-focus.md`) to prioritize.

**Use when**: You want to trim or reorganize meetings without manually reviewing each one.

**Time**: ~2–4 minutes.

---

## Workflow

### Step 1: Load calendar

- Use **google-calendar** (or calendar export / MCP) to get upcoming events (e.g. next 1–2 weeks). Include title, start/end, attendees, and optional description.
- If no Google Calendar: user can paste a list of meetings or share an export; normalize into a simple list (title, date, duration, attendees).

### Step 2: Optional context

- If `02-memory/goals.md` or a weekly-focus file exists: read short-term goals or "this week's focus" so suggestions can favor alignment (e.g. "aligns with goal X → Keep" or "no clear tie to goals → Consider decline/shorten").

### Step 3: Per-meeting suggestion

For each meeting, suggest one of:

- **Decline** — low value, no clear owner dependency, or duplicate with another meeting.
- **Shorten** — could be 15–30 min instead of 1 hr; suggest a shorter duration.
- **Delegate** — someone else could represent you; name the role or person if obvious.
- **Merge** — combine with another meeting (e.g. two standups → one).
- **Keep** — important, goal-aligned, or required.

Add a one-line rationale per meeting.

### Step 4: Output

- Clear list (table or bullets): meeting title, date/time, duration, suggestion (Decline / Shorten / Delegate / Merge / Keep), rationale.
- Remind user these are suggestions; they make changes in the calendar app.

---

## Prerequisites

- **Calendar**: Google Calendar (google-calendar skill) or user-provided list/export.
- **Goals** (optional): `02-memory/goals.md` or weekly focus for alignment.

---

## Triggers

- "calendar cleanup", "clean up my calendar", "which meetings should I decline", "review my meetings", "meeting audit"

---

## Output

- Per-meeting suggestion with rationale; no automatic calendar changes.
