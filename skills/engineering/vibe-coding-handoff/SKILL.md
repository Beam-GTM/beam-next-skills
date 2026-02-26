---
name: vibe-coding-handoff
description: "Review and clean up vibe-coding changes before handoff. Identifies unused components, simplification opportunities, duplicate code, and generates a comprehensive handoff report."
version: "1.0"
created: "2025-12-25"
triggers:
  - "handoff review"
  - "review changes"
  - "cleanup code"
  - "vibe coding handoff"
  - "code review for handoff"
  - "simplify components"
  - "comprehensive review"
  - "comprehensive branch review"
  - "update comprehensive review"
---

# Vibe Coding Handoff Skill

**Purpose**: Review vibe-coding changes to identify simplification opportunities, unused components, duplicate code, and generate a handoff-ready codebase.

---

## 🎯 What This Does

Analyzes code changes to prepare for handoff:
- **Scan**: Detect new/modified files in the branch
- **Analyze**: Find unused components, duplicate code, and simplification opportunities
- **Compare**: Check new vs existing components
- **Report**: Generate comprehensive handoff documentation
- **Clean**: Remove unused code and consolidate duplicates

---

## 🏗️ Workflow Steps

### Step 1: SCAN - Identify Changes

```
User: "handoff review" or "review changes for handoff"
    ↓
[Scan Phase]
    → Compare branch to main/develop
    → List all new files
    → List all modified files
    → Categorize by type (components, pages, utilities, etc.)
```

**What to scan:**
- `git diff --name-only main...HEAD` - Get changed files
- Group by directory/type
- Count lines added/removed

---

### Step 2: ANALYZE - Find Issues

```
[Analysis Phase]
    → Check for unused exports
    → Find duplicate functions
    → Identify similar components
    → Check for dead imports
    → Find inline code that should be extracted
```

**Analysis Categories:**

#### 2.1 Unused Components
```typescript
// Check: Is this component imported anywhere?
// Tool: grep for component name in all files
grep -r "import.*ComponentName" src/
grep -r "<ComponentName" src/
```

#### 2.2 Duplicate Code
```typescript
// Check: Same function in multiple files
// Example: formatSkillName in SkillsContainer + SkillDropdown
// Action: Extract to shared utility
```

#### 2.3 Similar Components (Enhanced)
```typescript
// Check: Two components with overlapping functionality
// Example: FileTree vs KnowledgeBaseTree
// Action: Merge or document reason for separation

// Post-Extraction Pattern Detection:
// After component extraction, re-scan extracted components for patterns
// - Group by type/pattern (FilterBar, Modal, Table, Drawer, etc.)
// - Compare props, JSX structure, hooks used
// - Flag components with >70% similarity
// Example: ToolOptimizerFilterBar + DatasetModalFilters + FeedbackCollectionFilterBar
//          → All filter bars, ~80% similar → Consolidation opportunity

// Context-Aware Decision Framework:
// ✅ Consolidate if: Same functionality, different data sources
// ⚠️ Consider if: Similar functionality, different UX requirements  
// ❌ Don't consolidate if: Different business logic or user flows
```

#### 2.4 Dead Imports
```typescript
// Check: Imports that aren't used
// Tool: ESLint unused-imports rule
```

#### 2.5 Inline Code to Extract
```typescript
// Check: Large inline functions or components
// Example: 800-line file with inline tab components
// Action: Extract to separate files
```

#### 2.6 Mock Data & API Architecture
```typescript
// Check for scattered mock data generators in components
// Patterns to detect:
const generateMockTaskNodes = () => { ... }
const mockTaskNodes = [...]
const getMockTaskCount = () => { ... }

// Check for data source inconsistencies:
// - Component filters real API data but displays mock data
// - Missing API endpoints that should exist

// Detection:
grep -rn "generateMock\|mock.*Nodes\|getMock" src/ --include="*.tsx" --include="*.ts"
grep -rn "const.*mock.*=" src/ --include="*.tsx" --include="*.ts" | grep -v "mockRouter\|mockClient"

// Recommendation: Move to src/server/mocks/{feature}Router.ts
// Impact: Centralized mock API, easier to replace with real API
```

---

### Step 3: COMPARE - New vs Existing

```
[Comparison Phase]
    → List all NEW components created
    → List EXISTING components reused
    → Identify components that could replace new ones
    → Find shared components that could be created
```

**Comparison Table Template:**

| New Component | Similar Existing | Action |
|---------------|------------------|--------|
| FileTree | KnowledgeBaseTree | Merge → use existing |
| SkillDropdown | - | Keep (unique purpose) |
| formatSkillName | - | Extract to shared utility |

---

### Step 4: REPORT - Generate Documentation

```
[Report Phase]
    → Create dated folder: {YYYY-MM-DD}-branch-review/
    → Generate comprehensive-review-{YYYY-MM-DD}.md
    → Generate improvements-and-concerns-{YYYY-MM-DD}.md
    → Generate slack-update-{YYYY-MM-DD}.md (for #project-beam-next)
    → List all findings with priorities
    → Provide action items
    → Include code snippets for fixes
```
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
run_terminal_cmd

**Output Structure**: 
- Create folder: `{project}/02-resources/{YYYY-MM-DD}-branch-review/`
- Generate three files with dates in filenames:
  1. `comprehensive-review-{YYYY-MM-DD}.md` - Full branch review with metrics, features, layouts, routers, components
  2. `improvements-and-concerns-{YYYY-MM-DD}.md` - Actionable improvements organized by priority (Critical, High, Medium, Low)
  3. `slack-update-{YYYY-MM-DD}.md` - Formatted Slack message for #project-beam-next channel

**Folder Naming**: Use format `YYYY-MM-DD-branch-review` (e.g., `2025-12-27-branch-review`)
**File Naming**: Include date in all filenames (e.g., `comprehensive-review-2025-12-27.md`)

**Iterative Review Recommendation:**
After major refactoring (component extraction, consolidation), recommend re-running review:
- Component extraction may reveal new duplication patterns
- Consolidation may expose additional optimization opportunities
- Each refactoring phase can reveal cascading improvements
- Say "handoff review" again after fixes to catch new patterns

---

### Step 5: CLEAN - Apply Fixes (Optional)

```
[Cleanup Phase - User Approval Required]
    → Delete unused components
    → Extract duplicate utilities
    → Merge similar components
    → Update imports
```

---

## 📋 Handoff Report Template

**Output Structure**: 
- Create dated folder: `{project}/02-resources/{YYYY-MM-DD}-branch-review/`
- Generate three files in that folder with dates in filenames:
  1. `comprehensive-review-{YYYY-MM-DD}.md` - Full branch review
  2. `improvements-and-concerns-{YYYY-MM-DD}.md` - Actionable improvements and concerns
  3. `slack-update-{YYYY-MM-DD}.md` - Formatted Slack message for #project-beam-next

### Comprehensive Review Template

```markdown
# Comprehensive Branch Review: {branch-name} vs main

**Generated**: YYYY-MM-DD
**Branch**: `{branch-name}`
**Reviewer**: AI Assistant (vibe-coding-handoff skill)

---

## 📊 Summary

| Metric | Count |
|--------|-------|
| Files Added | X |
| Files Modified | X |
| Components Created | X |
| Utilities Created | X |
| Issues Found | X |
| Actions Required | X |

---

## ✅ New Components

| Component | Lines | Purpose | Status |
|-----------|-------|---------|--------|
| ComponentA | 150 | Description | ✅ Keep |
| ComponentB | 80 | Description | ⚠️ Review |

---

## 🔍 Issues Found

### Critical (Must Fix)
1. **Unused Component**: `OldComponent.tsx`
   - Not imported anywhere
   - Action: Delete

### High Priority
1. **Duplicate Code**: `formatName` function
   - Found in: File1.tsx, File2.tsx
   - Action: Extract to shared utility

### Medium Priority
1. **Similar Components**: `FileTree` vs `KnowledgeBaseTree`
   - Recommendation: Merge into one

### Low Priority
1. **Inline extraction**: Large inline functions
   - Recommendation: Consider extracting

---

## 🛠️ Action Items

- [ ] Delete unused components
- [ ] Extract duplicates to utilities
- [ ] Merge similar components
- [ ] Update documentation

---

## 📁 Files Reference

### New Files
- `src/components/new/Component.tsx`
- `src/pages/new/page.tsx`

### Modified Files
- `src/existing/file.tsx`

### Deleted Files (Recommended)
- `src/unused/component.tsx`
```

### Improvements and Concerns Template

```markdown
# Improvements and Concerns

**Generated**: YYYY-MM-DD
**Branch**: `{branch-name}`

---

## 🔴 Critical Issues (Must Fix Before Production)

### 1. [Issue Title]

**Issue**: [Description]

**Impact**: [Impact description]

**Files Affected**:
- `path/to/file.ts`

**Recommendation**:
- [Action item 1]
- [Action item 2]

---

## 🟡 High Priority Improvements

### 1. [Improvement Title]

[Description]

---

## 🟢 Medium Priority Improvements

### 1. [Improvement Title]

[Description]

---

## 🔍 Mock Data & API Architecture

### Scattered Mock Data
⚠️ **Found in {N} components:**
- `path/to/file.tsx`: `generateMockTaskNodes()`
- `path/to/file2.tsx`: `mockTaskNodes`

**Recommendation:**
- Move to `src/server/mocks/{feature}Router.ts`
- Impact: Centralized mock API, easier to replace with real API
- Priority: Medium

### Data Source Inconsistencies
⚠️ **Filter/Display Mismatch:**
- Component filters real API data but displays mock data
- Location: `path/to/file.tsx`
- Impact: Filters may not work correctly
- Priority: High

---

## 🔄 Post-Extraction Patterns

### Component Families Detected
After component extraction, found similar patterns:

**Filter Bar Family** (3 components, ~80% similar):
- `ToolOptimizerFilterBar` (248 lines)
- `DatasetModalFilters` (235 lines)
- `FeedbackCollectionFilterBar` (239 lines)

**Recommendation:**
- Consolidate into `LearningFilterBar` component
- Estimated reduction: ~400-500 lines
- Context check: ✅ Same functionality, different data sources → Safe to consolidate
- Priority: High

**Table Family** (2 components):
- `CategoryTasksTable` (optimization mode)
- `CategoryTasksTable` (feedback mode)

**Recommendation:**
- ⚠️ Different contexts (optimization vs feedback)
- Consider shared base component with context-specific props
- Priority: Medium

---

## 🔵 Low Priority / Nice to Have

### 1. [Improvement Title]

[Description]

---

## 📋 Action Items Summary

### Immediate (Before Production)
- [ ] [Action item]

### Short Term (Next Sprint)
- [ ] [Action item]

### Medium Term (Next Month)
- [ ] [Action item]

---

## 🎯 Priority Matrix

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| [Issue] | High | Medium | 🔴 Critical |

---
```

---

## 🔧 Analysis Scripts

### Check for Unused Exports

```bash
# Find component files
find src/components -name "*.tsx" -type f | while read file; do
  component=$(basename "$file" .tsx)
  # Check if imported anywhere else
  count=$(grep -r "import.*$component" src/ --include="*.tsx" | grep -v "$file" | wc -l)
  if [ "$count" -eq 0 ]; then
    echo "UNUSED: $file"
  fi
done
```

### Find Duplicate Functions

```bash
# Look for common function patterns
grep -rn "export const format" src/ --include="*.tsx" --include="*.ts"
grep -rn "export function format" src/ --include="*.tsx" --include="*.ts"
```

### Check Similar Components

```bash
# Find components with similar names
find src/components -name "*Tree*.tsx" -type f
find src/components -name "*Modal*.tsx" -type f
find src/components -name "*Dropdown*.tsx" -type f

# After extraction, group by pattern (FilterBar, Modal, Table, Drawer, etc.)
find src/components -name "*FilterBar*.tsx" -o -name "*Filter*.tsx"
find src/components -name "*Table*.tsx"
find src/components -name "*Drawer*.tsx"
```

### Check Mock Data Patterns

```bash
# Find mock data generators
grep -rn "generateMock\|mock.*Nodes\|getMock" src/ --include="*.tsx" --include="*.ts"
grep -rn "const.*mock.*=" src/ --include="*.tsx" --include="*.ts" | grep -v "mockRouter\|mockClient"
```

### Get Changed Files

```bash
# Compare to main branch
git diff --name-only main...HEAD
git diff --stat main...HEAD
```

---

## 🚀 Usage Examples

### Example 1: Full Handoff Review

```
User: "handoff review for skills feature"

AI: Running handoff analysis...

📊 SCAN RESULTS
- 12 new files
- 8 modified files
- 3 deleted files

🔍 ANALYSIS FINDINGS

✅ Components OK (5):
  - SkillsContainer.tsx (353 lines) - Well structured
  - CreateSkillModal.tsx (150 lines) - Proper separation
  - SkillDropdown.tsx (370 lines) - Unique purpose

⚠️ Issues Found (3):

1. DUPLICATE CODE [High]
   formatSkillName in SkillsContainer + SkillDropdown
   → Extract to src/utils/formatters.ts

2. SIMILAR COMPONENTS [Medium]
   FileTree (119 lines) vs KnowledgeBaseTree (405 lines)
   → Merge: Use KnowledgeBaseTree everywhere

3. INLINE CODE [Low]
   Skill detail page has 823 lines with inline tabs
   → Consider extracting to tabs/

📋 Generated: 2025-12-25-branch-review/comprehensive-review-2025-12-25.md
📋 Generated: 2025-12-25-branch-review/improvements-and-concerns-2025-12-25.md

💡 Say "apply fix 1" to extract formatSkillName
   Or "apply all fixes" to run everything
```

---

### Example 2: Check Specific File

```
User: "check if FileTree is used"

AI: Searching for FileTree usage...

📊 FileTree Usage Analysis

Imports found: 3
  - CodingAgentContainer.tsx (line 15)
  - BeamNextContainer.tsx (line 22)
  - EditTab.tsx (line 8)

Similar component exists: KnowledgeBaseTree
  - Location: src/components/shared/KnowledgeBaseTree/
  - Lines: 405 (vs FileTree: 119)
  - Features: Agent grouping, file sources, context menus

💡 Recommendation: Replace FileTree with KnowledgeBaseTree
   (May need adapter for different data structure)
```

---

### Example 3: Apply Specific Fix

```
User: "apply fix 1 - extract formatSkillName"

AI: Extracting formatSkillName utility...

✅ Created: src/utils/formatters.ts
✅ Updated: SkillsContainer.tsx (removed local function, added import)
✅ Updated: SkillDropdown.tsx (removed local function, added import)
✅ Updated: skill detail page (added import)

📊 Results:
- Lines removed: 28 (duplicates)
- New utility file: 15 lines
- Net reduction: 13 lines
- DRY principle: ✅ Applied

🔄 Run "handoff review" to verify changes
```

---

## ⚙️ Configuration

Create `handoff-config.yaml` in project working directory:

```yaml
scan:
  base_branch: "main"
  include_paths:
    - "src/components"
    - "src/pages"
    - "src/server"
    - "src/utils"
  exclude_paths:
    - "node_modules"
    - ".next"
    - "dist"
  file_types:
    - "*.tsx"
    - "*.ts"

analysis:
  check_unused_exports: true
  check_duplicate_functions: true
  check_similar_components: true
  check_dead_imports: true
  check_inline_extraction: true
  inline_threshold_lines: 200

compare:
  component_dirs:
    - "src/components/shared"
    - "src/components/sections"
    - "src/components/ui"

report:
  output_dir: "02-resources"
  folder_template: "{date}-branch-review"
  files:
    - name: "comprehensive-review-{date}.md"
      template: "comprehensive-review"
    - name: "improvements-and-concerns-{date}.md"
      template: "improvements-and-concerns"
  include_code_snippets: true
  include_git_diff: true

cleanup:
  require_approval: true
  create_backup: true
  run_lint_after: true
```

---

## 📈 Success Criteria

**Good Handoff:**
- ✅ All unused code removed
- ✅ No duplicate functions
- ✅ Similar components merged or documented
- ✅ Inline code extracted where appropriate
- ✅ Handoff report generated
- ✅ All new components documented

**Excellent Handoff:**
- ✅ Everything above, plus:
- ✅ Unit tests for new utilities
- ✅ Updated README/docs
- ✅ Clean git history
- ✅ No linter warnings
- ✅ Peer review completed

---

## 🔗 Integration

### With Git Workflow
- Run before PR merge
- Include report in PR description
- Tag issues for follow-up

### With CI/CD
- Add as pre-merge check
- Fail if critical issues found
- Generate report as artifact

### With Documentation
- Update component docs
- Add to changelog
- Link to Linear tickets

---

## 📚 Related Skills

- `project-sync` - Sync implementation status
- `linear-vibe-code-mapper` - Link code to tickets
- `create-skill` - Create new skills

---

**Version**: 1.0
**Created**: 2025-12-25
**Status**: ✅ Ready to use


