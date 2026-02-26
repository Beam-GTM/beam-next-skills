---
name: production-handover
description: "Generate comprehensive production handover document by scanning branch changes, checking API status, analyzing component usage, and identifying production readiness gaps. Designed for vibe-coding → production transitions."
version: "1.0"
created: "2025-12-29"
triggers:
  - "generate production handover"
  - "create handover document"
  - "production handover"
  - "handover for developers"
  - "scan branch for handover"
  - "prepare production handover"
---

# Production Handover Skill

**Purpose**: Automatically generate a comprehensive production handover document by analyzing branch changes, checking API status, reviewing component usage, and identifying what needs work to make vibe-coding work production-ready.

**Context**: This skill is designed for transitions from vibe-coding (designer/rapid prototyping) to production-ready code. It helps developers understand what exists, what's missing, and what needs to be built/tested.

---

## 🎯 What This Does

1. **Scans branch vs main** - Identifies all changed files and features
2. **Checks API status** - Uses `api-planner` skill to verify what APIs exist vs what's mocked
3. **Analyzes components** - Checks component usage, dependencies, and patterns
4. **Identifies gaps** - Finds missing tests, error handling, production concerns
5. **Generates handover doc** - Creates comprehensive document for developers

---

## 🏗️ Workflow

### Step 1: SCAN - Branch Analysis

**Command**: `git diff --name-only main...HEAD`

**What to capture**:
- All new files (by type: components, pages, routers, utils)
- All modified files
- Files deleted
- Lines added/removed per file
- Feature areas affected

**Categorize by**:
- `src/components/` - UI components
- `src/pages/` - Pages/routes
- `src/server/api/routers/` - API endpoints
- `src/hooks/` - Custom hooks
- `src/utils/` - Utilities
- `src/stores/` - State management

**Output structure**:
```markdown
## Branch Changes Summary

**Branch**: {branch_name}
**Base**: main
**Files Changed**: {count}
**Lines Added**: {count}
**Lines Removed**: {count}

### New Files
- Components: {list}
- Pages: {list}
- Routers: {list}
- Hooks: {list}
- Utils: {list}

### Modified Files
- {list with brief description of changes}

### Deleted Files
- {list}
```

---

### Step 2: API ANALYSIS - Check What Exists

**Use the `api-planner` skill** to check each router/feature:

**For each router found** (`src/server/api/routers/*.ts`):

1. **Identify the feature** (e.g., "projects", "skills", "knowledge-base")
2. **Call api-planner**:
   ```
   "Check APIs for {feature} - verify what exists vs what's mocked"
   ```
3. **Extract from api-planner output**:
   - Which endpoints exist (real backend)
   - Which endpoints are mocked/placeholder
   - Which endpoints are missing
   - Schema information
   - TODO comments indicating incomplete work

**Check patterns**:
- `grep -r "TODO" src/server/api/routers/` - Find incomplete implementations
- `grep -r "MOCK\|mock" src/server/api/routers/` - Find mock data
- `grep -r "\.data/" src/server/api/routers/` - Find file-based storage (not production)
- `grep -r "throw new Error" src/server/api/routers/` - Find unimplemented endpoints

**Output structure**:
```markdown
## API Status Analysis

### {Feature} Router (`{router_file}`)

**Status**: {Real API | Mock/Placeholder | Missing}

**Endpoints**:
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/list` | GET | ✅ Real | Calls backend API |
| `/create` | POST | ⚠️ Mock | Returns hardcoded data |
| `/update` | PUT | ❌ Missing | TODO comment found |

**Issues Found**:
- [ ] Mock data in {endpoint}
- [ ] File-based storage (`.data/` directory)
- [ ] TODO comments: {list}
- [ ] Missing error handling
- [ ] No validation schemas

**Production Readiness**: {Ready | Needs Work | Not Started}
```

---

### Step 3: COMPONENT ANALYSIS - Usage & Dependencies

**For each component** (`src/components/**/*.tsx`):

1. **Check if it's used**:
   ```bash
   grep -r "import.*ComponentName" src/
   grep -r "<ComponentName" src/
   ```

2. **Check dependencies**:
   - What APIs it calls
   - What hooks it uses
   - What stores it accesses
   - What props it expects

3. **Check for patterns**:
   - Mock data hardcoded in component
   - TODO comments
   - Console.log statements
   - Missing error boundaries
   - Missing loading states

**Output structure**:
```markdown
## Component Analysis

### {ComponentName} (`{file_path}`)

**Status**: {Used | Unused | Partially Used}
**Used In**: {list of files that import it}

**Dependencies**:
- APIs: {list}
- Hooks: {list}
- Stores: {list}

**Issues**:
- [ ] Mock data hardcoded
- [ ] TODO comments: {list}
- [ ] Console.log statements
- [ ] Missing error handling
- [ ] Missing loading states
- [ ] No TypeScript types for props

**Production Readiness**: {Ready | Needs Work}
```

---

### Step 4: TESTING ANALYSIS - Coverage Gaps

**Check for tests**:
```bash
# Find test files
find __tests__ -name "*{feature}*" -o -name "*{component}*"

# Check if routers have tests
ls __tests__/server/api/routers/

# Check if components have tests
ls __tests__/components/
```

**Output structure**:
```markdown
## Testing Status

### Routers
| Router | Tests | Status |
|--------|-------|--------|
| projectsRouter | ❌ None | Missing |
| skillsRouter | ❌ None | Missing |

### Components
| Component | Tests | Status |
|-----------|-------|--------|
| ProjectsContainer | ✅ Yes | Has tests |
| CreateProjectModal | ❌ None | Missing |

### Hooks
| Hook | Tests | Status |
|------|-------|--------|
| useProjects | ✅ Yes | Has tests |
```

---

### Step 5: PRODUCTION CONCERNS - Find Issues

**Search for common production issues**:

```bash
# Console logs
grep -r "console\." src/ --include="*.ts" --include="*.tsx"

# TODO comments
grep -r "TODO\|FIXME\|XXX" src/ --include="*.ts" --include="*.tsx"

# Mock data
grep -r "MOCK\|mock.*=" src/ --include="*.ts" --include="*.tsx" | grep -v "mockRouter\|mockClient\|__tests__"

# Error handling (missing try/catch)
# Check router files for missing error handling

# Hardcoded values
grep -r "localhost\|127.0.0.1\|hardcoded" src/ --include="*.ts" --include="*.tsx"

# Missing validation
# Check if router endpoints have Zod schemas
```

**Output structure**:
```markdown
## Production Concerns

### Code Quality Issues
- [ ] Console.log statements: {count} found
  - {list of files}
- [ ] TODO comments: {count} found
  - {list with context}
- [ ] Mock data: {count} instances
  - {list of locations}
- [ ] Missing error handling: {list}
- [ ] Hardcoded values: {list}

### Security Concerns
- [ ] File upload validation missing
- [ ] Input sanitization needed
- [ ] Authentication checks missing
- [ ] Rate limiting not implemented

### Performance Concerns
- [ ] Large bundle size components
- [ ] Missing pagination
- [ ] No lazy loading
- [ ] Missing memoization
```

---

### Step 6: GENERATE HANDOVER DOCUMENT

**Create comprehensive handover document**:

**Location**: `beam-next/03-projects/11-handover-cleanup/02-resources/production-handover-{YYYY-MM-DD}.md`

**Document structure**:

```markdown
# Production Handover: {Branch Name}

**Generated**: {date}
**Branch**: {branch_name}
**Base**: main
**Context**: Vibe-coding → Production hardening

---

## Executive Summary

**Status**: {Overall assessment}
**Production Ready**: {X}% of features
**Needs Work**: {List of critical items}

---

## 1. Branch Changes Summary
{From Step 1}

## 2. API Status Analysis
{From Step 2}

## 3. Component Analysis
{From Step 3}

## 4. Testing Status
{From Step 4}

## 5. Production Concerns
{From Step 5}

## 6. Production Readiness Roadmap

### Critical (Blocking Production)
- [ ] {Item 1}
- [ ] {Item 2}

### High Priority
- [ ] {Item 1}
- [ ] {Item 2}

### Medium Priority
- [ ] {Item 1}

### Low Priority
- [ ] {Item 1}

## 7. Questions for Developers

### Architecture Questions
- {Question about design decisions}

### Implementation Questions
- {Question about specific code}

### Testing Questions
- {Question about test strategy}

## 8. File Reference

### Key Files to Review
- {List of important files with brief descriptions}

### API Endpoints
- {List of endpoints with status}

### Components
- {List of components with status}

---

**Next Steps**: Review this document, prioritize work, and begin production hardening.
```

---

## Example Interaction

```
User: "generate production handover"

AI: 
I'll scan the branch, check APIs, analyze components, and generate a comprehensive handover document.

[Step 1: Scanning branch...]
Found 873 files changed, 260k lines added

[Step 2: Checking APIs...]
Checking projects router... ⚠️ Mock data found
Checking skills router... ✅ Real API
Checking knowledge-base router... ❌ Missing

[Step 3: Analyzing components...]
Found 45 new components
12 components have mock data
8 components missing error handling

[Step 4: Checking tests...]
No router tests found
Some component tests exist

[Step 5: Finding production concerns...]
Found 23 console.log statements
15 TODO comments
8 instances of mock data

[Generating handover document...]
✅ Created: beam-next/03-projects/11-handover-cleanup/02-resources/production-handover-2025-12-29.md

The handover document includes:
- Complete branch analysis
- API status for all features
- Component usage and issues
- Testing gaps
- Production concerns
- Actionable roadmap

Review the document and let me know if you need clarification on any section.
```

---

## Integration with Other Skills

### Use `api-planner` Skill

When checking APIs, call the api-planner skill:
```
"Check APIs for {feature} - I need to know what's real vs mocked for production handover"
```

The api-planner will:
- Check official API docs
- Scan router files
- Detect placeholder patterns
- Report real vs mock status

### Use `vibe-coding-handoff` Skill

For code quality analysis, you can reference the vibe-coding-handoff skill's findings, but this skill focuses on production readiness rather than code cleanup.

---

## Output Files

**Primary Output**:
- `beam-next/03-projects/11-handover-cleanup/02-resources/production-handover-{YYYY-MM-DD}.md`

**Optional Supporting Files** (if needed):
- `beam-next/03-projects/11-handover-cleanup/02-resources/api-analysis-{YYYY-MM-DD}.json` - Raw API data
- `beam-next/03-projects/11-handover-cleanup/02-resources/component-analysis-{YYYY-MM-DD}.json` - Raw component data

---

## Tips for Developers

When reviewing the handover document:

1. **Start with API Status** - Know what needs to be built
2. **Review Production Concerns** - Address critical issues first
3. **Check Component Dependencies** - Understand the architecture
4. **Plan Testing Strategy** - Based on testing gaps
5. **Use the Roadmap** - Prioritize work systematically

---

**Version**: 1.0  
**Last Updated**: 2025-12-29
