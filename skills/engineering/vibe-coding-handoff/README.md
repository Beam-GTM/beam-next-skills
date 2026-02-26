# Vibe Coding Handoff Skill

A skill for reviewing and cleaning up vibe-coding changes before handoff to ensure code quality and maintainability.

## Quick Start

Say one of these to trigger the skill:
- "handoff review"
- "review changes"
- "cleanup code"
- "vibe coding handoff"

## What It Does

1. **Scans** your branch for new/modified files
2. **Analyzes** for unused components, duplicates, and issues
3. **Compares** new vs existing components
4. **Reports** findings with prioritized action items
5. **Cleans** (with approval) - removes unused code, extracts utilities

## Example Session

```
You: handoff review

AI: Running handoff analysis...

📊 SCAN: 12 new files, 8 modified
🔍 ISSUES: 3 found

1. [High] Duplicate: formatSkillName in 2 files
2. [Medium] Similar: FileTree ≈ KnowledgeBaseTree
3. [Low] Inline: 823-line file could be split

💡 Say "apply fix 1" or "apply all fixes"
```

## Files

- `SKILL.md` - Main skill definition and workflows
- `README.md` - This file

## Related Skills

- `project-sync` - Sync implementation status
- `linear-vibe-code-mapper` - Link code to tickets

