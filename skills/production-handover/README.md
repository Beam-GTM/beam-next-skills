# Production Handover Skill

**Version**: 1.0  
**Created**: 2025-12-29  
**Purpose**: Generate comprehensive production handover documents for vibe-coding → production transitions

---

## 🎯 What This Does

Automatically generates a production handover document by:

1. **Scanning branch changes** - Compares branch vs main to identify all modifications
2. **Checking API status** - Uses `api-planner` skill to verify what APIs are real vs mocked
3. **Analyzing components** - Checks component usage, dependencies, and production readiness
4. **Identifying gaps** - Finds missing tests, error handling, and production concerns
5. **Generating handover doc** - Creates comprehensive document for developers taking over

---

## Quick Start

Say one of these to trigger the skill:
- "generate production handover"
- "create handover document"
- "production handover"
- "handover for developers"
- "scan branch for handover"

---

## What You Get

The skill generates a comprehensive handover document at:
```
beam-next/03-projects/11-handover-cleanup/02-resources/production-handover-{YYYY-MM-DD}.md
```

The document includes:

### 1. Executive Summary
- Overall production readiness assessment
- Key metrics (files changed, lines added)
- Critical blockers

### 2. Branch Changes Summary
- All new files (categorized by type)
- All modified files
- Files deleted
- Feature areas affected

### 3. API Status Analysis
- For each router: what's real vs mocked
- Missing endpoints
- TODO comments and incomplete work
- Schema information

### 4. Component Analysis
- Component usage (used/unused)
- Dependencies (APIs, hooks, stores)
- Production issues (mock data, TODOs, console.logs)

### 5. Testing Status
- Router test coverage
- Component test coverage
- Hook test coverage
- Missing tests identified

### 6. Production Concerns
- Code quality issues (console.logs, TODOs)
- Security concerns
- Performance concerns
- Missing error handling

### 7. Production Readiness Roadmap
- Prioritized action items
- Critical → High → Medium → Low
- Clear next steps

### 8. Questions for Developers
- Architecture questions
- Implementation questions
- Testing questions

---

## How It Works

### Step 1: Branch Analysis
Scans `git diff main...HEAD` to identify:
- New files (components, pages, routers, etc.)
- Modified files
- Deleted files
- Lines changed

### Step 2: API Analysis
For each router found:
- Calls `api-planner` skill to check API status
- Detects mock data, placeholders, TODOs
- Identifies file-based storage (not production-ready)
- Checks for missing endpoints

### Step 3: Component Analysis
For each component:
- Checks if it's used (grep for imports)
- Analyzes dependencies
- Finds production issues (mock data, TODOs, console.logs)

### Step 4: Testing Analysis
Checks for test files:
- Router tests
- Component tests
- Hook tests
- Identifies gaps

### Step 5: Production Concerns
Searches for:
- Console.log statements
- TODO comments
- Mock data
- Missing error handling
- Security issues
- Performance concerns

### Step 6: Generate Document
Creates comprehensive markdown document with all findings organized for easy review.

---

## Example Output

```
# Production Handover: beam-next-new-layout

**Generated**: 2025-12-29
**Branch**: beam-next-new-layout
**Base**: main
**Context**: Vibe-coding → Production hardening

---

## Executive Summary

**Status**: Needs significant work for production
**Production Ready**: ~40% of features
**Needs Work**: 
- Chat system (test implementation)
- Knowledge Base (no backend)
- Missing tests
- Mock data in multiple places

---

## 1. Branch Changes Summary

**Files Changed**: 873
**Lines Added**: 260,000
**Lines Removed**: 11,800

### New Files
- Components: 45 new components
- Pages: 12 new pages
- Routers: 3 new routers (projects, skills, knowledge-base)
- Hooks: 8 new hooks

[... rest of document ...]
```

---

## Integration with Other Skills

### api-planner Skill
This skill uses `api-planner` to check API status. The api-planner:
- Verifies against official API docs
- Detects placeholder patterns
- Reports real vs mock status

### vibe-coding-handoff Skill
For code cleanup (unused components, duplicates), use `vibe-coding-handoff`. This skill focuses on production readiness.

---

## Tips for Using the Handover

1. **Start with Executive Summary** - Get the big picture
2. **Review API Status** - Know what needs to be built
3. **Check Production Concerns** - Address critical issues first
4. **Use the Roadmap** - Prioritize work systematically
5. **Ask Questions** - Use the "Questions for Developers" section

---

## When to Use

Use this skill when:
- ✅ Preparing vibe-coding work for production
- ✅ Handing off to developers
- ✅ Assessing production readiness
- ✅ Planning production work
- ✅ Creating handover documentation

---

**Related Skills**:
- `api-planner` - Check API status
- `vibe-coding-handoff` - Code cleanup and review
