# First Time Setup - Troubleshooting Reference

Detailed troubleshooting for SSH, git config, and first-time clone issues.

---

## SSH Key Troubleshooting

### "Permission denied (publickey)"

**Cause:** GitHub doesn't recognize your SSH key.

**Fix checklist:**
1. Confirm key exists: `ls ~/.ssh/id_ed25519.pub`
2. Confirm key is added to GitHub: https://github.com/settings/keys
3. Confirm SSH agent is running and key is loaded:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```
4. Test again: `ssh -T git@github.com`

---

### "Host key verification failed"

**Cause:** Your machine hasn't verified GitHub's server identity yet.

**Fix:**
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

---

### Using a Non-Default Key Name

If your key isn't named `id_ed25519`, tell SSH which key to use.

**Create or edit `~/.ssh/config`:**
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/your_key_name
  AddKeysToAgent yes
```

---

### Multiple SSH Keys (Personal + Work)

If you have both a personal and work GitHub account:

**`~/.ssh/config`:**
```
# Work GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_beam

# Personal GitHub
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal
```

Clone personal repos with: `git clone git@github-personal:user/repo.git`

---

## Platform-Specific Notes

### macOS

**SSH agent + Keychain (persist key across restarts):**

Add to `~/.ssh/config`:
```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

Then:
```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

---

### Linux

**Auto-start SSH agent (add to `~/.bashrc` or `~/.zshrc`):**
```bash
if [ -z "$SSH_AUTH_SOCK" ]; then
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
fi
```

---

### Windows

**Using Git Bash:**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**Using Windows OpenSSH (PowerShell as admin):**
```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

---

## Git Config Issues

### "Author identity unknown"

**Cause:** `user.name` and `user.email` not configured.

**Fix:**
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.name@beam.ai"
```

---

### Wrong Email on Commits

**Check current config:**
```bash
git config --global user.email
```

**Fix for future commits:**
```bash
git config --global user.email "correct.email@beam.ai"
```

**Per-repo override** (if you use different emails for different repos):
```bash
cd /path/to/repo
git config user.email "different.email@example.com"
```

---

## Clone Issues

### "Repository not found" or 403

**Causes:**
- You don't have access to the repo → ask admin to add you
- Using HTTPS instead of SSH → use `git@github.com:...` not `https://github.com/...`
- Wrong org/repo name → double-check the URL

---

### "Could not resolve hostname"

**Cause:** DNS or network issue.

**Fix:**
1. Check internet: `ping github.com`
2. If on VPN, try disconnecting and retrying
3. Try HTTPS as fallback: `git clone https://github.com/Beam-AI-Solutions/{repo}.git`

---

## Upstream Remote Issues

### "fatal: remote upstream already exists"

**Fix:** Remove and re-add:
```bash
git remote remove upstream
git remote add upstream git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git
```

---

### "fatal: 'upstream' does not appear to be a git repository"

**Fix:** Check the URL is correct:
```bash
git remote -v
git remote set-url upstream git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git
```

---

## Quick Diagnostic

Run this to check your full setup:
```bash
python3 00-system/skills/git/scripts/check_git_setup.py
```

The script checks git installation, config, SSH key, GitHub connection, and remote configuration, then tells you exactly what needs fixing.
