#!/usr/bin/env python3
"""
Git Setup Diagnostic
Checks if git is properly configured for Nexus collaboration.
Returns JSON with status per check and recommendations.
"""

import json
import subprocess
import os
import sys
from pathlib import Path


def run(cmd, timeout=10):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)


def check_git_installed():
    ok, output = run("git --version")
    if ok:
        version = output.replace("git version ", "")
        return {"status": "pass", "detail": version}
    return {"status": "fail", "detail": "Git is not installed", "fix": "Install git: macOS: xcode-select --install | Linux: sudo apt install git | Windows: https://git-scm.com/download/win"}


def check_git_config():
    ok_name, name = run("git config --global user.name")
    ok_email, email = run("git config --global user.email")

    if ok_name and name and ok_email and email:
        return {"status": "pass", "detail": f"{name} <{email}>"}

    missing = []
    if not (ok_name and name):
        missing.append("user.name")
    if not (ok_email and email):
        missing.append("user.email")

    return {
        "status": "fail",
        "detail": f"Missing: {', '.join(missing)}",
        "fix": 'git config --global user.name "Your Name" && git config --global user.email "you@beam.ai"'
    }


def check_ssh_key():
    ssh_dir = Path.home() / ".ssh"
    key_types = ["id_ed25519", "id_rsa", "id_ecdsa"]

    for key_type in key_types:
        pub_key = ssh_dir / f"{key_type}.pub"
        if pub_key.exists():
            return {"status": "pass", "detail": f"Found {pub_key.name}"}

    return {
        "status": "fail",
        "detail": "No SSH key found",
        "fix": 'ssh-keygen -t ed25519 -C "you@beam.ai" then add to https://github.com/settings/keys'
    }


def check_github_connection():
    ok, output = run("ssh -T git@github.com 2>&1", timeout=15)
    # ssh -T returns exit code 1 even on success, check output
    combined = output.lower()
    if "successfully authenticated" in combined or "you've successfully" in combined:
        return {"status": "pass", "detail": "GitHub SSH connection works"}
    if "permission denied" in combined:
        return {
            "status": "fail",
            "detail": "Permission denied - SSH key not recognized by GitHub",
            "fix": "Add your SSH key to GitHub: https://github.com/settings/keys"
        }
    if "could not resolve" in combined or "network" in combined:
        return {
            "status": "fail",
            "detail": "Cannot reach GitHub - network issue",
            "fix": "Check internet connection and try again"
        }
    # Some environments return non-zero but still authenticate
    if "hi " in combined:
        return {"status": "pass", "detail": "GitHub SSH connection works"}
    return {
        "status": "warn",
        "detail": f"Unexpected response: {output[:100]}",
        "fix": "See references/first-time-setup.md for SSH troubleshooting"
    }


def check_remotes():
    ok, output = run("git remote -v")
    if not ok:
        return {
            "status": "fail",
            "detail": "Not in a git repository",
            "fix": "Clone your repo first: git clone git@github.com:Beam-AI-Solutions/{repo-name}.git"
        }

    has_origin = "origin" in output
    has_upstream = "upstream" in output

    if has_origin and has_upstream:
        return {"status": "pass", "detail": "Both origin and upstream configured"}
    if has_origin and not has_upstream:
        return {
            "status": "warn",
            "detail": "Origin configured but upstream missing",
            "fix": "git remote add upstream git@github.com:Beam-AI-Solutions/Nexus-Master-Suite.git"
        }
    if not has_origin:
        return {
            "status": "fail",
            "detail": "No origin remote configured",
            "fix": "Clone your repo first or add origin: git remote add origin git@github.com:Beam-AI-Solutions/{repo-name}.git"
        }

    return {"status": "fail", "detail": "No remotes configured"}


def main():
    checks = {
        "git_installed": check_git_installed(),
        "git_config": check_git_config(),
        "ssh_key": check_ssh_key(),
        "github_connection": check_github_connection(),
        "remotes": check_remotes(),
    }

    all_pass = all(c["status"] == "pass" for c in checks.values())
    has_fail = any(c["status"] == "fail" for c in checks.values())

    if all_pass:
        summary = "All checks passed - git is fully configured!"
    elif has_fail:
        failed = [k for k, v in checks.items() if v["status"] == "fail"]
        summary = f"Setup incomplete - fix: {', '.join(failed)}"
    else:
        summary = "Mostly configured - see warnings"

    result = {
        "summary": summary,
        "ready": all_pass,
        "checks": checks,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
