#!/usr/bin/env python3
"""
tools/install_hooks.py — Install LagnaMaster git hooks

Sets up:
  .git/hooks/pre-push   — unified quality gate (tests + ruff + docs currency)

Run once after cloning or after tools/pre_push_hook.sh is updated:
    .venv/bin/python3 tools/install_hooks.py
"""
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = ROOT / ".git" / "hooks"
TOOLS_DIR = ROOT / "tools"


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
    # Make executable
    current = dst.stat().st_mode
    dst.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"  ✅  Installed: {dst}")
    print(f"      Source:    {src}")
    print()
    print("The pre-push hook will now run automatically on every git push:")
    print("  1. Full test suite (pytest)")
    print("  2. Ruff lint (0 errors required)")
    print("  3. Docs currency (MEMORY.md test count must match live count)")
    print()
    print("To bypass in an emergency (do not use routinely):")
    print("  git push --no-verify")


if __name__ == "__main__":
    install()
