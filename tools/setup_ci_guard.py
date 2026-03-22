#!/usr/bin/env python3
"""
tools/setup_ci_guard.py — LagnaMaster CI Guard Setup
Installs two things:
  1. .git/hooks/pre-push   — runs pytest before every push (blocks broken pushes)
  2. tools/ci_watch.py     — polls GitHub Actions after push, prints failures locally

Run once:
    cd ~/LagnaMaster && .venv/bin/python3 tools/setup_ci_guard.py
"""
from pathlib import Path
import os, stat, sys

ROOT = Path(__file__).resolve().parent.parent

# ─── 1. Pre-push hook ────────────────────────────────────────────────────────
HOOK = ROOT / ".git/hooks/pre-push"

HOOK_SCRIPT = '''\
#!/usr/bin/env bash
# LagnaMaster pre-push hook — blocks push if tests fail
# Installed by tools/setup_ci_guard.py

set -e
cd "$(git rev-parse --show-toplevel)"

PYTHON=".venv/bin/python3"
if [ ! -f "$PYTHON" ]; then
    echo "⚠️  .venv not found — skipping pre-push tests"
    exit 0
fi

echo "🔍 Running tests before push..."
ulimit -n 4096
PYTHONPATH=. "$PYTHON" -m pytest tests/ -q --tb=short -x 2>&1 | tail -20

STATUS=${PIPESTATUS[0]}
if [ $STATUS -ne 0 ]; then
    echo ""
    echo "❌ Tests failed — push blocked."
    echo "   Fix the failures above, then push again."
    echo "   To skip (NOT recommended): git push --no-verify"
    exit 1
fi

echo "✅ All tests passed — pushing."
exit 0
'''

HOOK.write_text(HOOK_SCRIPT)
HOOK.chmod(HOOK.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
print(f"  OK  .git/hooks/pre-push installed")

# ─── 2. ci_watch.py ──────────────────────────────────────────────────────────
CI_WATCH = ROOT / "tools/ci_watch.py"

CI_WATCH_SCRIPT = '''\
#!/usr/bin/env python3
"""
tools/ci_watch.py — Watch GitHub Actions CI and print failures locally.

Usage:
    cd ~/LagnaMaster

    # Watch the latest run (auto-detects current branch):
    .venv/bin/python3 tools/ci_watch.py

    # Watch and attempt auto-fix for known error patterns:
    .venv/bin/python3 tools/ci_watch.py --fix

    # Watch a specific run ID:
    .venv/bin/python3 tools/ci_watch.py --run-id 12345678
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Known auto-fixable error patterns ────────────────────────────────────────
# Each entry: (regex_to_match_in_log, fix_command_or_callable, description)
AUTO_FIXES = [
    # Missing 'hour' field in fixture
    (
        r"AssertionError: (\w+\.json): missing hour",
        None,  # handled by custom logic below
        "Missing 'hour' field in ADB fixture",
    ),
    # Import error — missing module
    (
        r"ModuleNotFoundError: No module named '([^']+)'",
        lambda m: f".venv/bin/pip install {m.group(1).split('.')[0]} --break-system-packages",
        "Missing Python package",
    ),
    # KeyError in fixture dict
    (
        r"KeyError: '([^']+)'.*fixtures/adb_charts/(\w+\.json)",
        None,
        "Fixture schema mismatch — needs regeneration",
    ),
]


def run(cmd: str) -> tuple[str, int]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr, result.returncode


def gh(*args) -> tuple[str, int]:
    return run(f"gh {' '.join(args)}")


def get_latest_run_id(branch: str) -> str | None:
    out, _ = gh("run", "list", "--branch", branch, "--limit", "1", "--json", "databaseId,status,conclusion")
    try:
        runs = json.loads(out)
        if runs:
            return str(runs[0]["databaseId"])
    except Exception:
        pass
    return None


def get_run_status(run_id: str) -> tuple[str, str]:
    out, _ = gh("run", "view", run_id, "--json", "status,conclusion")
    try:
        d = json.loads(out)
        return d.get("status", ""), d.get("conclusion", "")
    except Exception:
        return "", ""


def get_failed_log(run_id: str) -> str:
    out, _ = gh("run", "view", run_id, "--log-failed")
    return out


def current_branch() -> str:
    out, _ = run("git branch --show-current")
    return out.strip()


def watch(run_id: str | None, auto_fix: bool):
    branch = current_branch()
    print(f"Branch: {branch}")

    if not run_id:
        print("Waiting for CI run to appear...", end="", flush=True)
        for _ in range(30):
            run_id = get_latest_run_id(branch)
            if run_id:
                break
            print(".", end="", flush=True)
            time.sleep(5)
        print()

    if not run_id:
        print("❌ Could not find a CI run. Check https://github.com/agniinvestor/LagnaMaster/actions")
        sys.exit(1)

    print(f"Run ID: {run_id}")
    print(f"URL:    https://github.com/agniinvestor/LagnaMaster/actions/runs/{run_id}")
    print()

    # Poll until complete
    dots = 0
    while True:
        status, conclusion = get_run_status(run_id)
        if status in ("completed", "cancelled"):
            break
        msg = f"\\r⏳ Status: {status:<15}"
        print(msg, end="", flush=True)
        dots += 1
        time.sleep(10)

    print()

    if conclusion == "success":
        print("✅ CI passed.")
        return

    if conclusion in ("failure", "timed_out", "cancelled"):
        print(f"❌ CI {conclusion}. Fetching failure log...")
        print()
        log = get_failed_log(run_id)
        if not log.strip():
            print("No log output returned. Check the URL above.")
            return

        # Extract the most useful lines (errors + assertions)
        useful = []
        lines = log.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if any(k in stripped for k in [
                "FAILED", "ERROR", "Error", "assert", "AssertionError",
                "KeyError", "ImportError", "ModuleNotFoundError",
                "AttributeError", "TypeError", "raise ", "short test summary"
            ]):
                # Include a few lines of context
                start = max(0, i - 1)
                end = min(len(lines), i + 4)
                useful.extend(lines[start:end])
                useful.append("---")

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for l in useful:
            if l not in seen:
                seen.add(l)
                deduped.append(l)

        print("─" * 70)
        print("\\n".join(deduped[:120]))  # cap at 120 lines
        print("─" * 70)
        print()

        if auto_fix:
            attempt_auto_fix(log)


def attempt_auto_fix(log: str):
    print("🔧 Scanning for known auto-fixable patterns...")
    fixed_any = False

    for pattern, fix, description in AUTO_FIXES:
        m = re.search(pattern, log)
        if not m:
            continue

        print(f"  Found: {description}")

        if callable(fix):
            cmd = fix(m)
            print(f"  Running: {cmd}")
            out, code = run(f"cd {ROOT} && {cmd}")
            if code == 0:
                print(f"  ✅ Applied: {description}")
                fixed_any = True
            else:
                print(f"  ⚠️  Failed: {out[:200]}")

        elif fix is None:
            # Pattern-specific custom logic
            if "missing hour" in description:
                print("  Running: tools/adb_xml_importer.py --overwrite to regenerate fixtures")
                out, code = run(
                    f"cd {ROOT} && .venv/bin/python3 tools/adb_xml_importer.py "
                    f"adb_sample/c_sample.xml --overwrite 2>&1 | tail -10"
                )
                print(f"  {out[:300]}")
                if code == 0:
                    fixed_any = True

            elif "schema mismatch" in description:
                print("  This needs manual investigation — fixture schema changed.")

    if fixed_any:
        print()
        print("Fixes applied. Now:")
        print("  ulimit -n 4096 && PYTHONPATH=. .venv/bin/pytest tests/ -q --tb=short 2>&1 | tail -5")
        print("  git add -A && git commit -m 'fix: CI auto-fix' && git push")
    else:
        print("  No auto-fixable patterns found. Review the log above manually.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch GitHub Actions CI")
    parser.add_argument("--run-id", help="Specific run ID to watch")
    parser.add_argument("--fix", action="store_true", help="Attempt auto-fix on failure")
    args = parser.parse_args()
    watch(args.run_id, args.fix)
'''

CI_WATCH.write_text(CI_WATCH_SCRIPT)
CI_WATCH.chmod(CI_WATCH.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
print(f"  OK  tools/ci_watch.py installed")

# ─── 3. Improve GitHub Actions workflow ──────────────────────────────────────
# Find the workflow file
workflows = list((ROOT / ".github/workflows").glob("*.yml")) + \
            list((ROOT / ".github/workflows").glob("*.yaml"))

if workflows:
    wf = workflows[0]
    text = wf.read_text()

    # Add --tb=short and structured summary if not already present
    if "::error::" not in text:
        old = "pytest tests/"
        new = (
            "pytest tests/ -q --tb=short 2>&1 | tee /tmp/pytest_out.txt; "
            "STATUS=${PIPESTATUS[0]}; "
            "if [ $STATUS -ne 0 ]; then "
            "grep -E 'FAILED|ERROR|AssertionError' /tmp/pytest_out.txt | "
            "while IFS= read -r line; do echo \"::error::$line\"; done; fi; "
            "exit $STATUS"
        )
        if old in text:
            text = text.replace(old, new)
            wf.write_text(text)
            print(f"  OK  {wf.name} — added ::error:: annotations")
        else:
            print(f"  SKIP {wf.name} — pytest invocation not found in expected form")
    else:
        print(f"  SKIP {wf.name} — already has error annotations")
else:
    print("  SKIP — no .github/workflows/*.yml found")

print()
print("Setup complete. Workflow going forward:")
print()
print("  BEFORE PUSH (automatic):")
print("    git push  →  pre-push hook runs pytest locally")
print("               →  if tests fail: push is blocked, fix and retry")
print("               →  if tests pass: push proceeds")
print()
print("  AFTER PUSH (if CI fails anyway):")
print("    .venv/bin/python3 tools/ci_watch.py          # watch + print failures")
print("    .venv/bin/python3 tools/ci_watch.py --fix    # watch + attempt auto-fix")
print()
print("  SKIP hook for emergencies (use sparingly):")
print("    git push --no-verify")
print()
print("Commit with:")
print("  git add .git/hooks/pre-push tools/ci_watch.py .github/workflows/")
print("  git commit -m 'chore: pre-push test guard + ci_watch auto-fix tool'")
print("  git push")
