---
name: git
version: '1.0'
description: 'Git operations for Nexus. Load when user mentions: git, sync upstream,
  fetch upstream, fetch origin, push origin, pull, commit, git status, git add, git
  log, git branch, git stash, git reset, git revert, undo commit, update from template,
  setup git, ssh key, clone repo, git config.'
author: Abdul Rafay
category: general
updated: '2026-02-25'
visibility: public
---
# Git

**Version**: 3.0

Git operations for Nexus repositories.

---

## First Time Setup

**Never used git before? Start here.** This walks you through everything from zero to a working repo.

> **Already set up?** Run the diagnostic to check:
> ```bash
> python3 00-system/skills/git/scripts/check_git_setup.py
> ```
> If all checks pass, skip to [Which Operation Do I Need?](#which-operation-do-i-need)

---

### Step 0: Install Git

**Check if git is installed:**
```bash
git --version
```

**If not installed:**

| Platform | Command |
|----------|---------|
| macOS | `xcode-select --install` |
| Ubuntu/Debian | `sudo apt update && sudo apt install git` |
| Fedora/RHEL | `sudo dnf install git` |
| Windows | Download from https://git-scm.com/download/win |

---

### Step 1: Configure Your Identity

Git needs to know who you are. This is attached to every commit you make.

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.name@beam.ai"
```

**Verify:**
```bash
git config --global user.name
git config --global user.email
```

---

### Step 2: Set Up SSH Key

SSH keys let you securely connect to GitHub without typing your password every time.

**Check if you already have a key:**
```bash
ls ~/.ssh/id_ed25519.pub
```

If the file exists, skip to **Add key to GitHub** below.

**Generate a new SSH key:**
```bash
ssh-keygen -t ed25519 -C "your.name@beam.ai"
```
- Press Enter for default file location
- Enter a passphrase (recommended) or press Enter for none

**Copy your public key:**

| Platform | Command |
|----------|---------|
| macOS | `pbcopy < ~/.ssh/id_ed25519.pub` |
| Linux | `cat ~/.ssh/id_ed25519.pub` (then copy the output) |
| Windows | `clip < ~/.ssh/id_ed25519.pub` |

**Add key to GitHub:**
1. Go to https://github.com/settings/keys
2. Click **New SSH key**
3. Title: `Beam Work Laptop` (or whatever describes your machine)
4. Paste the key
5. Click **Add SSH key**

**Test the connection:**
```bash
ssh -T git@github.com
```

You should see: `Hi {username}! You've successfully authenticated...`

> **Something not working?** See [references/first-time-setup.md](references/first-time-setup.md) for troubleshooting.

---

### Step 3: Clone Your Repo

```bash
git clone git@github.com:Beam-AI-Solutions/{repo-name}.git
cd {repo-name}
```

Replace `{repo-name}` with your actual repository name (e.g., `nexus-client-acme`).

---

### Step 4: Configure Upstream

Upstream connects your repo to the Nexus template so you can receive system updates.

```bash
git remote add upstream git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git
```

**Verify remotes are set up:**
```bash
git remote -v
```

You should see:
```
origin    git@github.com:Beam-AI-Solutions/{repo-name}.git (fetch)
origin    git@github.com:Beam-AI-Solutions/{repo-name}.git (push)
upstream  git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git (fetch)
upstream  git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git (push)
```

---

### Step 5: Verify Everything Works

```bash
git status              # Should show clean working tree
git fetch upstream      # Should succeed without errors
```

**You're all set!** Continue to the daily operations below.

---

## Which Operation Do I Need?

| I want to... | Operation |
|--------------|-----------|
| Set up git for the first time | [First Time Setup](#first-time-setup) |
| Save my work locally | [Add](#1-git-add-stage) → [Commit](#2-git-commit) |
| Share my work with team | [Push](#4-git-push-origin) |
| Get my team's latest work | [Pull](#3-git-pull-origin) |
| Get system updates from template | [Sync Upstream](#9-sync-from-upstream) |
| See what I've changed | [Status](#common-operations) / [Diff](#6-git-diff) |
| Undo a mistake | [Recovery](#recovery-undo-mistakes) |

---

## Configuration

**Upstream**: `git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git`

**To change upstream URL**:
```bash
git remote set-url upstream {new-url}
```

**To add upstream** (if not configured):
```bash
git remote add upstream git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git
```

**Protected folders** (never sync from upstream):
| Folder | Why Protected |
|--------|---------------|
| `01-memory/` | Your goals, learnings, config |
| `02-projects/` | Your active projects |
| `03-skills/` | Your custom skills |
| `04-workspace/` | Your client workspaces |
| `05-archived/` | Your archived items |
| `.env` | Your API keys |

Only `00-system/` is safe to sync from upstream.

---

## Common Operations

These 5 operations cover 90% of daily use.

### 1. Git Add (Stage)

Stage files for commit.

```bash
git add {file}           # Stage specific file
git add .                # Stage all changes
```

**Interactive** (show user options):
```
Unstaged files:
1. 00-system/skills/git/
2. 01-memory/goals.md

Which files to stage? (e.g., "1" or "1,2" or "all")
```

---

### 2. Git Commit

Commit staged changes.

**Step 1**: Show what's staged
```bash
git diff --cached --stat
```

**Step 2**: Ask user for commit message
```
Staged changes:
  - 00-system/skills/git/SKILL.md (+50/-20)

Commit message conventions:
  [Dev] ...       - Development/feature work
  [Fix] ...       - Bug fixes
  [System] ...    - System framework changes
  [Memory] ...    - Memory/config changes
  [Project] ...   - Project changes
  [Skill] ...     - Skill changes
  [Workspace] ... - Workspace changes

What commit message would you like to use?
```

**Step 3**: Wait for user response, then commit
```bash
git commit -m "{user's message}"
```

**IMPORTANT**: Always ask user for commit message. Never commit without user confirmation.

---

### 3. Git Pull Origin

Get latest changes from your team's repo and merge.

```bash
git pull origin {branch}
```

**When to use**: You want your teammates' latest work merged into yours.

---

### 4. Git Push Origin

Share your commits with your team.

**Step 1**: Check status
```bash
git status
```

**Step 2**: Show what will be pushed
```bash
git log origin/{branch}..HEAD --oneline
```

**Step 3**: Ask user to confirm
```
Ready to push to origin/{branch}:
  - c07ff65 [Dev] Git skill v2.0
  - abc1234 Previous commit

Push these commits? (yes/no)
```

**Step 4**: If confirmed, push
```bash
git push origin {branch}
```

**IMPORTANT**: Always show what will be pushed and ask for confirmation.

---

### 5. Git Status

See current state.

```bash
git status
```

Shows: current branch, staged changes, unstaged changes, untracked files.

---

## Advanced Operations

### 6. Git Diff

Show changes in detail.

```bash
git diff                      # Unstaged changes
git diff --cached             # Staged changes
git diff HEAD..upstream/main  # Compare with upstream
git diff HEAD..origin/main    # Compare with origin
```

---

### 7. Git Log

Show commit history.

```bash
git log --oneline -20         # Short format
git log --oneline --graph -20 # With branch graph
```

---

### 8. Git Fetch (without merge)

Download changes without merging. Use when you want to review before merging.

**Fetch vs Pull**:
| Command | Downloads | Merges | Use when |
|---------|-----------|--------|----------|
| `fetch` | Yes | No | Want to review changes first |
| `pull` | Yes | Yes | Ready to merge immediately |

```bash
git fetch origin              # Fetch from your repo
git fetch upstream            # Fetch from template

# After fetch, review:
git diff HEAD..origin/main    # See what changed
git merge origin/main         # Then merge if ready
```

---

### 9. Sync from Upstream

Safely get system updates from the template repo.

**What git_sync.py does**:
1. Checks if upstream is configured
2. Fetches from upstream
3. Categorizes changes (safe/protected/careful)
4. Returns JSON for AI to present options

**Workflow**:

```bash
python3 00-system/skills/git/scripts/git_sync.py --check-only
```

Present to user:
```
SAFE to sync (00-system/):
  - 00-system/skills/new-skill/

PROTECTED (will NOT sync):
  - 01-memory/...

Options:
A) Sync 00-system/ only
B) Show diff first
C) Abort
```

**Apply sync**:
```bash
git checkout upstream/main -- 00-system/
git add 00-system/
git commit -m "[System] Sync from upstream"
git push origin {branch}   # If user confirms
```

---

### 10. Git Branch

```bash
git branch -a                    # List all branches
git checkout -b {name}           # Create and switch
git checkout {name}              # Switch to existing
git branch -d {name}             # Delete branch
```

---

### 11. Git Stash

Temporarily save uncommitted work.

```bash
git stash push -m "{desc}"       # Save
git stash list                   # List saved
git stash pop                    # Restore and remove
git stash apply stash@{N}        # Restore specific
git stash drop stash@{N}         # Delete specific
```

---

### 12. Conflict Resolution

**CRITICAL**: Never auto-resolve. Show user both versions, let them decide.

See [references/conflict-resolution.md](references/conflict-resolution.md)

**Quick flow**:
1. `git diff --name-only --diff-filter=U` - List conflicts
2. Show BOTH versions to user
3. User chooses: Keep yours (A), Keep theirs (B), Manual edit (C)
4. `git add {file}` - Mark resolved
5. `git commit` - Complete merge

---

## Recovery (Undo Mistakes)

### "I accidentally staged files"

```bash
git reset {file}              # Unstage specific file
git reset                     # Unstage all
```

---

### "I accidentally committed"

**Undo commit, keep changes staged**:
```bash
git reset --soft HEAD~1
```

**Undo commit, keep changes unstaged**:
```bash
git reset HEAD~1
```

**Undo commit, discard changes** (DESTRUCTIVE):
```bash
git reset --hard HEAD~1
```

---

### "I accidentally pushed"

**Create a new commit that reverses the changes** (safe, preserves history):
```bash
git revert HEAD               # Revert last commit
git revert {commit-hash}      # Revert specific commit
git push origin {branch}      # Push the revert
```

---

### "I accidentally merged"

**If NOT pushed yet**:
```bash
git reset --hard HEAD~1       # Go back before merge
```

**If already pushed** (create revert commit):
```bash
git revert -m 1 HEAD          # Revert merge commit
git push origin {branch}
```

---

### "I want to discard all local changes"

**Discard unstaged changes**:
```bash
git checkout -- {file}        # Specific file
git checkout -- .             # All files
```

**Discard EVERYTHING and match remote** (DESTRUCTIVE):
```bash
git fetch origin
git reset --hard origin/{branch}
```

---

## Quick Reference

**Common (90% of use)**:
| Task | Command |
|------|---------|
| Stage | `git add {files}` |
| Commit | `git commit -m "msg"` |
| Pull | `git pull origin {branch}` |
| Push | `git push origin {branch}` |
| Status | `git status` |

**Advanced**:
| Task | Command |
|------|---------|
| Diff | `git diff` |
| Log | `git log --oneline -20` |
| Fetch | `git fetch origin` |
| Stash | `git stash push -m "msg"` |
| Branch | `git branch -a` |

**Recovery**:
| Problem | Solution |
|---------|----------|
| Unstage | `git reset {file}` |
| Undo commit (keep changes) | `git reset --soft HEAD~1` |
| Undo pushed commit | `git revert HEAD && git push` |
| Discard local changes | `git checkout -- .` |

---

## Safety Rules

1. **NEVER** force push to main/master
2. **NEVER** auto-resolve conflicts
3. **NEVER** sync protected folders from upstream
4. **NEVER** commit without asking user for commit message
5. **ALWAYS** show user what will change before applying
6. **ALWAYS** let user decide on conflicts
7. **ALWAYS** confirm before destructive operations (reset --hard)
8. **ALWAYS** ask user before any action that modifies git history
