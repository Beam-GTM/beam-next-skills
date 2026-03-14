---
name: mid-session-cleanup
version: '1.0'
description: cleanup, check, review, lint, mid-session, sanity check, health check
category: system
updated: '2026-03-02'
visibility: public
---
# Mid-Session Cleanup

Pause mid-session to validate work quality, catch errors, write tests, check consistency, and update plans — then continue working.

## Purpose

The `mid-session-cleanup` skill is a **non-destructive checkpoint** you can run at any point during a session. Unlike `close-session`, it does NOT end the session — it validates the current state of work and continues.

Use it when:
- You've been building for a while and want a sanity check
- You want tests written for new code before moving on
- Plans and implementation may have drifted apart
- You suspect logical errors or inconsistencies
- You're about to context-compact and want clean state first

**Key difference from close-session**: This skill **resumes work** after cleanup. No session reports, no fresh-session instructions, no goodbye.

---

## Execution Sequence

1. **Initialize TodoWrite** with all steps (MANDATORY)
2. Load [workflow.md](references/workflow.md)
3. Execute steps 1–11 sequentially
4. Mark each step complete in TodoWrite as you finish it
5. **Resume work** — return to whatever was in progress

---

## Critical Rules

1. **TodoWrite is MANDATORY**: Initialize at start with all steps
2. **Detect project type**: Development projects get code-specific checks (lint, tests); non-dev projects get document consistency checks
3. **Non-destructive**: Never delete files, break builds, or discard work
4. **Continue after cleanup**: Final step is always "resume working"
5. **Respect context budget**: Keep exploration focused — don't re-read the entire codebase

---

## What It Checks

### For Development Projects
- **Logical errors**: Lint, type-check, and scan recently modified files
- **Test coverage**: Write tests for new/modified code that lacks them
- **Consistency**: Read plan docs, then **verify each item against actual source files** — catch false-positive checkboxes, missed completions, stale architecture descriptions
- **Imports & dependencies**: Unused imports, missing dependencies
- **File hygiene**: Temp files, debug logs, console.logs left in code

### For Non-Development Projects
- **Document consistency**: Read plan files, then verify claims against actual files on disk
- **Cross-reference integrity**: Do linked files/resources exist?
- **Task accuracy**: Are checkboxes in steps.md accurate? Verify by checking what actually exists
- **Content quality**: Spot obvious gaps, TODOs left unresolved

### Always (Both Types)
- **Plan drift detection**: Read plan docs, verify against source files, then **update the original plan in-place** — not just report drift, fix it
- **Learnings capture**: Surface insights, gotchas, and patterns discovered so far — write to `02-memory/core-learnings.md`
- **Resume context update**: Ensure `resume-context.md` / `files_to_load` are current
- **Progress sync**: Update task checkboxes to reflect verified actual state

---

## Workflow Overview

Complete workflow with all steps: See [workflow.md](references/workflow.md)

### Steps (from workflow.md):

1. Identify scope (what changed this session)
2. Detect project type (dev vs non-dev)
3. Check for logical errors
4. Write / update tests (dev projects only)
5. Check plan-implementation consistency
6. Update plans and task checkboxes
7. Capture learnings
8. Update resume context
9. Display cleanup summary
10. Resume work

---

## Integration

### User Triggers

Activated when user says:
- "cleanup", "clean up", "mid-session cleanup"
- "sanity check", "health check", "check my work"
- "review what we've done", "lint everything"
- "write tests for what we built"
- "are we on track?"

### Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `close-session` | Mid-session-cleanup is a subset — it does quality checks but skips session reports, map regeneration, and fresh-session instructions |
| `validate-system` | validate-system checks system integrity; mid-session-cleanup checks *work* integrity |
| `execute-project` | Can be called mid-execution to checkpoint quality |

### NOT an Auto-Trigger

Unlike close-session, this skill is **user-initiated only**. It never fires automatically — the user decides when they want a checkpoint.

---

## Error Handling

**No active project** → Still useful: check for temp files, lint open files, general workspace hygiene

**Lint/test tooling not available** → Skip those steps gracefully, note in summary

**Large number of changes** → Focus on files modified this session only (use git diff to scope)

**Tests fail after writing** → Report failures, don't auto-fix (user decides)

---

## Resources

### references/
- **workflow.md**: Complete step-by-step workflow

---

**Remember**: This skill keeps you moving. Clean up, catch issues early, and keep building.
