# Mid-Session Cleanup Workflow

Complete step-by-step workflow for validating work quality, catching errors, writing tests, checking consistency, and updating plans mid-session.

---

## Table of Contents

- [Step 1: Initialize TodoList](#step-1-initialize-todolist)
- [Step 2: Identify Scope](#step-2-identify-scope)
- [Step 3: Detect Project Type](#step-3-detect-project-type)
- [Step 4: Check for Logical Errors](#step-4-check-for-logical-errors)
- [Step 5: Write / Update Tests](#step-5-write--update-tests)
- [Step 6: Check Plan-Implementation Consistency](#step-6-check-plan-implementation-consistency)
- [Step 7: Update Plans and Task Checkboxes](#step-7-update-plans-and-task-checkboxes)
- [Step 8: Capture Learnings](#step-8-capture-learnings)
- [Step 9: Update Resume Context](#step-9-update-resume-context)
- [Step 10: Display Cleanup Summary](#step-10-display-cleanup-summary)
- [Step 11: Resume Work](#step-11-resume-work)

---

## Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Identify scope (what changed)
- [ ] Detect project type
- [ ] Check for logical errors
- [ ] Write / update tests
- [ ] Check plan-implementation consistency
- [ ] Update plans and checkboxes
- [ ] Capture learnings
- [ ] Update resume context
- [ ] Display cleanup summary
- [ ] Resume work
```

**Mark tasks complete as you finish each step throughout this workflow.**

---

## Step 2: Identify Scope

Determine what has changed during this session so far.

### 2a. Check Git Status

```bash
git status --short
git diff --name-only
git diff --cached --name-only
```

Collect:
- **Modified files** (tracked, staged and unstaged)
- **New files** (untracked)
- **Deleted files**

### 2b. Identify Active Project

- Check `03-projects/` for projects with `status: IN_PROGRESS`
- If working in a specific app directory (e.g. `04-apps/`), note the app context
- Record the project ID and name for later steps

### 2c. Build Change Summary

```
Changed files this session:
- [N] modified files
- [N] new files
- [N] deleted files

Active project: [name] or "No active project"
Working directory: [path]
```

Store this for use in subsequent steps.

---

## Step 3: Detect Project Type

Determine whether this is a development project or a non-dev project.

### Detection Signals

**Development project** (any of these):
- Working directory contains `package.json`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `go.mod`, or similar
- Modified files include `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`, `.go`, `.java`, `.swift`, etc.
- A test framework config exists (`vitest.config.*`, `jest.config.*`, `pytest.ini`, `.mocharc.*`, etc.)
- Project plan references code, APIs, architecture

**Non-development project**:
- Changes are primarily `.md`, `.yaml`, `.json` (documentation/config)
- Project is research, strategy, content, or planning focused
- No code files in the change set

### Record Decision

```
Project type: DEVELOPMENT | NON-DEV
Language/framework: [e.g. TypeScript/React/Electron, Python/FastAPI]
Test framework: [e.g. Vitest, Jest, Pytest, none detected]
```

---

## Step 4: Check for Logical Errors

### For Development Projects

#### 4a. Run Linter on Modified Files

Use the ReadLints tool on each modified source file:
- Only check files modified this session (from Step 2)
- Skip `node_modules/`, `dist/`, `build/`, `.cache/`, vendored files
- Collect all errors and warnings

#### 4b. Review Code for Common Issues

For each modified source file, scan for:
- **Unused imports** — imported but never referenced
- **Debug artifacts** — `console.log`, `debugger`, `print()` statements left in
- **TODO/FIXME comments** — note but don't auto-resolve
- **Incomplete error handling** — empty catch blocks, unhandled promise rejections
- **Type mismatches** (TypeScript) — function signatures vs usage
- **Dead code** — unreachable returns, commented-out blocks

#### 4c. Cross-File Consistency

For related modified files, check:
- **Interface/type changes** propagated to all consumers
- **API contract changes** reflected in both caller and callee
- **Shared state** — if a store/context changed, are all consumers updated?
- **Import paths** — no broken imports after file moves/renames

#### 4d. Categorize Findings

```
Errors (must fix):
- [file:line] Description

Warnings (should fix):
- [file:line] Description

Info (optional):
- [file:line] Description
```

**Fix errors immediately.** Warnings are reported in the summary for user decision.

### For Non-Development Projects

#### 4a. Document Quality Check

For each modified `.md` file:
- Check for broken internal links (`[text](path)` where path doesn't exist)
- Check for incomplete sections (headers with no content)
- Check for unresolved placeholders (`[TODO]`, `[TBD]`, `XXX`)
- Verify YAML frontmatter is valid (if present)

#### 4b. Cross-Reference Check

- If documents reference other files, verify those files exist
- If documents reference project IDs, verify those projects exist
- Check for stale references to deleted/moved content

---

## Step 5: Write / Update Tests

**SKIP this step entirely for non-development projects.**

### 5a. Identify Untested Code

For each modified/new source file:
1. Check if a corresponding test file exists:
   - `foo.ts` → `foo.test.ts` or `foo.spec.ts` or `__tests__/foo.test.ts`
   - `foo.py` → `test_foo.py` or `foo_test.py` or `tests/test_foo.py`
2. If test file exists, check if new functions/exports have test coverage
3. Build a list of untested code

### 5b. Prioritize What to Test

Focus on:
- **New public functions/exports** — highest priority
- **Modified function signatures** — ensure existing tests still match
- **Business logic** — core algorithms, data transformations
- **Edge cases in modified code** — null/undefined handling, boundary conditions

Skip:
- Simple getters/setters
- Pure UI components (unless complex logic)
- Generated code
- Type definitions

### 5c. Write Tests

For each untested function/module:

1. Read the source file to understand behavior
2. Create or update the test file
3. Write tests covering:
   - Happy path (expected inputs → expected outputs)
   - Edge cases (empty, null, boundary values)
   - Error cases (invalid inputs, failure modes)
4. Follow existing test patterns in the project (naming, structure, assertions)

### 5d. Run Tests

```bash
# Detect and run the appropriate test command
# TypeScript/Vitest: npx vitest run --reporter=verbose [file]
# TypeScript/Jest: npx jest [file]
# Python/Pytest: python -m pytest [file] -v
```

- Run only the new/modified test files (not the full suite)
- Record pass/fail results
- **If tests fail**: Report failures but do NOT auto-fix source code — the test may have caught a real bug

### 5e. Report

```
Tests written:
- [file] N new tests (pass/fail status)

Tests updated:
- [file] N tests modified (pass/fail status)

Test failures (may indicate real bugs):
- [file:test_name] Expected X, got Y
```

---

## Step 6: Check Plan-Implementation Consistency

**CRITICAL**: This step must verify claims against actual files — READ the source of truth before marking anything as done or drifted.

### 6a. Locate Plan Documents

Look for plan files in these locations (priority order):
1. `{project-dir}/docs/plan.md`
2. `{project-dir}/planning/steps.md` or `tasks.md`
3. `{project-dir}/docs/*.md` (any planning docs)
4. `03-projects/{project}/planning/steps.md`
5. `03-projects/{project}/02-resources/` (plan resources)

### 6b. Read the Plan, Then Verify Against Implementation

For each plan document found, **read it fully**, then for each task/item:

**Task-level verification** (read actual files to confirm):
- For each task marked `[x]`: Read the file/code it refers to — does the implementation actually exist and work? If not → flag as false positive
- For each task marked `[ ]`: Check git diff and modified files — was this actually completed this session? If yes → flag as missed checkbox
- For tasks referencing specific files (e.g. "create auth-service.ts"): Glob/Read to verify the file exists and has the expected content

**Architecture/design verification** (dev projects — read actual source):
- Plan says "use library X" → Check `package.json`/`requirements.txt`/imports — is it actually used?
- Plan describes API shape/types → Read the actual type definitions and interfaces — do they match?
- Plan mentions files/modules → Glob to check which exist and which don't

**Scope verification**:
- Compare modified files from Step 2 against plan items — any work done that isn't in the plan?
- Any plan items that were skipped or deprioritized during execution?

### 6c. Build Drift Report

```
Plan-Implementation Drift:
- [OK] Aligned: N items verified against source
- [DRIFT] N items diverged (details below)
- [FALSE POSITIVE] N items marked done but not actually complete
- [MISSING] N planned items not yet started
- [UNPLANNED] N items done but not in plan

Details:
- [DRIFT] plan.md line X: Plan says "..." but [file] shows "..."
- [FALSE POSITIVE] plan.md: "create X" marked [x] but file doesn't exist
- [MISSING] steps.md task: "..." — not started
- [UNPLANNED] Added [file/feature] not in original plan
```

### 6d. Stale Docs Detection (lightweight)

If working in a project that has a `docs/` directory, run a quick scan for completed docs still sitting in root:

```bash
python3 00-system/skills/system/project-cleanup/scripts/docs_cleanup.py \
  --docs-path {project-dir}/docs --json
```

If the scan finds done files:
- **Do NOT archive them during mid-session cleanup** (keep cleanup fast)
- **Add a note to the cleanup summary** (Step 10):
  ```
  Docs Hygiene:
  - [N] docs in root look done — run `project-cleanup --docs-cleanup` to archive them
  ```
- This is detection only. Archival is handled by the `project-cleanup` skill's docs-cleanup mode.

---

## Step 7: Update Plans and Task Checkboxes

Based on **verified** findings from Step 6, update the plan documents.

### 7a. Update Task Checkboxes

For tasks confirmed complete (verified by reading source files):
- Update `- [ ]` to `- [x]` in the relevant task/plan file
- Use Edit tool with exact string replacement

For tasks marked complete but verified as NOT actually done:
- Ask user before unchecking: "Task X is marked done but [file] doesn't exist / implementation is incomplete. Uncheck it?"

### 7b. Update Plan Documents In-Place

**CRITICAL**: Update the **original plan file itself** — don't just report drift, fix the document.

**IF drift was detected**:
- Update the specific lines in the plan that no longer match reality
- Add a brief inline note where the change happened (e.g. `*(updated: switched to library Y)*`)
- If the change is significant, add a "Plan Updates" section at the bottom noting what changed and why
- Do NOT silently rewrite the whole plan — make changes traceable

**IF unplanned work was done**:
- Add those items to the plan in the appropriate section (not just at the bottom)
- Mark with `*(added during implementation)*` so it's clear what was planned vs. discovered

**IF plan has stale/outdated sections**:
- Update them to match current state (architecture diagrams, file lists, API shapes)
- Keep the plan as a living document that reflects reality

### 7c. Recalculate Progress

After checkbox updates:
- Count total tasks and completed tasks
- Calculate percentage
- Update any progress fields in `overview.md` or plan headers

```
Progress update:
- Before cleanup: X/Y tasks (Z%)
- After cleanup: A/Y tasks (B%)
- Delta: +N tasks marked complete, M false positives corrected
```

---

## Step 8: Capture Learnings

Surface insights, gotchas, and patterns from the session so far and persist them to `02-memory/core-learnings.md`.

### 8a. Identify Learnings

Review the session's work and look for:

**Insights** — non-obvious discoveries worth remembering:
- "Library X doesn't support Y despite docs suggesting it does"
- "This API returns dates in format Z, not what we assumed"
- "Pattern X works better than pattern Y for this use case"

**Gotchas / What to Avoid**:
- Bugs that took time to diagnose (save the diagnosis for next time)
- Footguns in APIs, libraries, or tooling
- Configuration traps ("setting X breaks Y")

**What Works Well**:
- Approaches that proved effective
- Tool/library choices that paid off
- Workflow patterns worth repeating

**Best Practices** (emerged during work):
- Code patterns that should be standardized
- Architecture decisions that generalize beyond this project

### 8b. Ask User

If learnings were identified, present them for confirmation:

```
I noticed a few things worth capturing as learnings:

1. [Insight/gotcha/pattern description]
2. [Insight/gotcha/pattern description]

Want me to add these to core-learnings? (yes / edit / skip)
```

- **"yes"** → Write all to `02-memory/core-learnings.md`
- **"edit"** → Let user modify, then write
- **"skip"** → Move on without writing
- **No learnings found** → Skip silently, no need to ask

### 8c. Write to core-learnings.md

Read `02-memory/core-learnings.md`, then append each learning under the appropriate section:

- Insights → `## Insights` section
- Gotchas → `## What to Avoid` section
- Effective approaches → `## What Works Well` section
- Patterns → `## Best Practices` section

**Format** (matches existing entries):
```markdown
### [Learning Title] (YYYY-MM-DD)
**Observed**: [Context of when/how this was discovered]

**Key principle**: [The takeaway in one sentence]

**Applied to**: [Project or area this applies to]
```

Update `**Last Updated**` at the bottom of the file.

---

## Step 9: Update Resume Context

Ensure the project can be resumed cleanly after a context compact or new session.

### 9a. Locate Resume Context

Check for:
- `{project-dir}/planning/resume-context.md`
- `{project-dir}/02-resources/resume-context.md`
- `03-projects/{project}/planning/resume-context.md`

### 9b. Update Fields

If resume-context.md exists, update:
- `continue_at`: Point to current work location (file:line or "Phase X, Task Y")
- `files_to_load`: Add any new critical files created this session
- `blockers`: Update with any discovered blockers
- `last_updated`: Current timestamp

If resume-context.md doesn't exist but should (active project with code):
- Suggest creating one, but don't auto-create

### 9c. Session Notes

If `03-working/session-notes.md` or equivalent exists:
- Append any new decisions or discoveries from this session
- Note any gotchas found during cleanup

---

## Step 10: Display Cleanup Summary

Show a concise summary of everything found and fixed:

```
-------------------------------------------------------
Mid-Session Cleanup Complete
-------------------------------------------------------

Scope: [N] files checked ([N] modified, [N] new)
Project: [name] ([DEV/NON-DEV])

Errors Fixed:
- [N] lint errors resolved
- [N] logical issues corrected

Tests:
- [N] new tests written ([pass]/[fail])
- [N] existing tests verified

Plan Consistency:
- [OK] [N] items aligned
- [DRIFT] [N] items updated
- [N] checkboxes corrected

Learnings: [N] captured to core-learnings.md | None this round

Resume Context: [Updated / Created / Already current / N/A]

Remaining Warnings:
- [warning 1]
- [warning 2]

Ready to continue! What's next?
-------------------------------------------------------
```

**Keep it concise** — max ~15 lines for the summary. Details were handled in each step.

---

## Step 11: Resume Work

**CRITICAL**: This skill does NOT end the session.

After displaying the summary:
1. Mark all TodoWrite steps as complete
2. Return control to the user
3. Continue with whatever was in progress before cleanup was triggered

```
Cleanup complete — picking up where we left off.
```

**Do NOT**:
- Create a session report (that's close-session's job)
- Instruct user to start fresh session
- Regenerate full workspace maps (that's close-session's job)
- Display a goodbye message

**DO**:
- Stay in the current execution context
- Remember what was being worked on before cleanup
- Be ready for the next instruction

---

**END OF WORKFLOW**
