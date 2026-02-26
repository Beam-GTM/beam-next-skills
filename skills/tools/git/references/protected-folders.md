# Protected Folders

> **Version**: 1.0
> **Purpose**: Folders that should be protected during upstream sync

---

## Protection Levels

### Level 1: NEVER Overwrite (User Data)

These folders contain user-specific data that should NEVER be overwritten from upstream:

| Folder | Reason |
|--------|--------|
| `01-memory/` | User goals, learnings, session reports |
| `02-projects/` | User's active projects (except README.md) |
| `03-skills/` | User's custom skills |
| `04-workspace/` | User's workspace and client data |
| `05-archived/` | User's archived projects |
| `.env` | User's API keys and secrets |

### Level 2: Merge Carefully (Configuration)

These files may have user modifications that should be preserved:

| File | Reason |
|------|--------|
| `01-memory/user-config.yaml` | User preferences |
| `CLAUDE.md` | May have user customizations |

### Level 3: Safe to Sync (System)

These folders can be safely updated from upstream:

| Folder | Reason |
|--------|--------|
| `00-system/` | System framework, skills, documentation |

---

## Sync Strategy

### Recommended Approach

1. **Fetch upstream** without merging
2. **Review changes** in `00-system/`
3. **Cherry-pick or merge** only system updates
4. **Never force-push** to protected folders

### Safe Sync Command

```bash
# Fetch upstream changes
git fetch upstream

# See what changed in system folder only
git diff HEAD..upstream/main -- 00-system/

# Merge only 00-system changes
git checkout upstream/main -- 00-system/
git add 00-system/
git commit -m "Sync 00-system from upstream"
```

---

## Warning Signs

Stop and review if sync would modify:
- Any file in `01-memory/` through `05-archived/`
- `.env` or other credential files
- `03-skills/` (user custom skills)
