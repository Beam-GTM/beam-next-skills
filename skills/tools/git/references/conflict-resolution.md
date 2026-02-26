# Conflict Resolution Guide

> **Version**: 1.0
> **Purpose**: How to present and resolve merge conflicts in Nexus

---

## AI Behavior: Never Auto-Resolve

**CRITICAL**: AI must NEVER automatically resolve conflicts. Always:
1. Show the conflict to the user
2. Explain what each side represents
3. Ask user to choose
4. Apply user's decision

---

## Presenting Conflicts to User

### Step 1: List Conflicted Files

```bash
git diff --name-only --diff-filter=U
```

Display to user:
```
Conflicts found in:
1. 00-system/skills/some-skill/SKILL.md
2. CLAUDE.md

Which file would you like to resolve first?
```

### Step 2: Show Conflict Details

For each conflicted file, show:

```markdown
**File**: 00-system/skills/some-skill/SKILL.md

**YOUR version** (local):
[Show the content between <<<<<<< HEAD and =======]

**UPSTREAM version** (from template):
[Show the content between ======= and >>>>>>> upstream/main]

Which version do you want to keep?
- A) Keep YOUR version
- B) Keep UPSTREAM version
- C) Keep BOTH (I'll merge manually)
- D) Show me the full file to edit
```

### Step 3: Apply User's Choice

| User Choice | Action |
|-------------|--------|
| A (yours) | `git checkout --ours <file>` |
| B (theirs) | `git checkout --theirs <file>` |
| C (both) | Open file for manual edit |
| D (full file) | Show full file, let user edit |

---

## Quick Reference for User

| Task | Command |
|------|---------|
| See conflicted files | `git diff --name-only --diff-filter=U` |
| Keep my version | `git checkout --ours <file>` |
| Keep upstream version | `git checkout --theirs <file>` |
| Abort merge | `git merge --abort` |
| Mark as resolved | `git add <file>` |
| Continue merge | `git commit` |

---

## Conflict Markers Explained

When showing user a conflict:
```
<<<<<<< HEAD
(Your local changes - what you have now)
=======
(Upstream changes - from the template repo)
>>>>>>> upstream/main
```

Always explain which is which so user can make informed decision.
