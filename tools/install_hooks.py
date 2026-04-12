#!/usr/bin/env python3
"""
tools/install_hooks.py — Install LagnaMaster git hooks

Sets up:
  .git/hooks/pre-push    — unified quality gate (tests + ruff + docs currency)
  .git/hooks/commit-msg  — commit message format validation

Run once after cloning or after hook scripts are updated:
    .venv/bin/python3 tools/install_hooks.py
"""
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = ROOT / ".git" / "hooks"
TOOLS_DIR = ROOT / "tools"


def _make_executable(path: Path):
    current = path.stat().st_mode
    path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install():
    if not HOOKS_DIR.exists():
        print("ERROR: .git/hooks not found — are you in the repo root?")
        sys.exit(1)

    # pre-push
    src = TOOLS_DIR / "pre_push_hook.sh"
    dst = HOOKS_DIR / "pre-push"

    if not src.exists():
        print(f"ERROR: {src} not found")
        sys.exit(1)

    shutil.copy2(src, dst)
    _make_executable(dst)
    print(f"  Installed: {dst}")
    print(f"      Source:    {src}")

    # commit-msg hook — validates commit message format
    commit_msg_dst = HOOKS_DIR / "commit-msg"
    commit_msg_script = f"""#!/bin/sh
# LagnaMaster commit-msg hook — validates commit format
# Installed by tools/install_hooks.py
.venv/bin/python tools/validate_commits.py "$1"
"""
    commit_msg_dst.write_text(commit_msg_script)
    _make_executable(commit_msg_dst)
    print(f"  Installed: {commit_msg_dst}")
    print()
    print("Hooks installed:")
    print("  pre-push:   full test suite + ruff + docs currency")
    print("  commit-msg: commit message format validation")
    print()
    print("To bypass in an emergency (do not use routinely):")
    print("  git commit --no-verify / git push --no-verify")


if __name__ == "__main__":
    install()
