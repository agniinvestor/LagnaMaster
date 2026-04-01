"""tools/rework_detector.py — Pre-commit rework and lesson detection.

Analyzes staged changes for patterns that indicate rework, missing controls,
or lessons that should be recorded. Returns non-zero if action needed.

Called by pre-push hook. Output is advisory (warnings), not blocking,
but surfaces patterns that the session-end protocol should address.

Signals detected:
  1. NAMING_GAP    — same string replaced across 3+ files (convention missing)
  2. TEST_CHASING  — test assertion values changed to match new code (fragile test)
  3. REWORK_COMMIT — commit message contains "fix", "fixup", "amend" after encoding commit
  4. MEMORY_STALE  — code pushed but MEMORY.md metrics unchanged
  5. SOURCE_DRIFT  — source text name not in CANONICAL_SOURCES

Usage:
    PYTHONPATH=. .venv/bin/python tools/rework_detector.py
    PYTHONPATH=. .venv/bin/python tools/rework_detector.py --strict  # exit 1 on any finding
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys


def _run(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def check_naming_gap() -> list[str]:
    """Detect if the same string replacement was made across 3+ files."""
    findings = []
    diff = _run("git diff --cached --unified=0 2>/dev/null || git diff HEAD~1 --unified=0 2>/dev/null")
    if not diff:
        return findings

    # Track removed/added line pairs per file
    removals: dict[str, int] = {}  # removed string → count of files
    for line in diff.split("\n"):
        if line.startswith("-") and not line.startswith("---"):
            # Normalize whitespace and extract the core change
            clean = line[1:].strip()
            if len(clean) > 10:  # ignore trivial changes
                removals[clean] = removals.get(clean, 0) + 1

    for text, count in removals.items():
        if count >= 3:
            findings.append(
                f"NAMING_GAP: '{text[:60]}...' removed from {count} files — "
                f"was this a convention that should have been enforced by a control?"
            )
    return findings


def check_test_chasing() -> list[str]:
    """Detect test assertions changed to match new data (not new invariants)."""
    findings = []
    diff = _run("git diff --cached -- 'tests/' 2>/dev/null || git diff HEAD~1 -- 'tests/' 2>/dev/null")
    if not diff:
        return findings

    # Look for patterns: -assert X == "old_value" / +assert X == "new_value"
    old_asserts = []
    new_asserts = []
    for line in diff.split("\n"):
        if line.startswith("-") and "assert" in line and "==" in line:
            old_asserts.append(line)
        elif line.startswith("+") and "assert" in line and "==" in line:
            new_asserts.append(line)

    if old_asserts and new_asserts and len(old_asserts) == len(new_asserts):
        # Assertions were CHANGED, not added — potential test chasing
        for old, new in zip(old_asserts, new_asserts):
            findings.append(
                f"TEST_CHASING: assertion changed (not added) — is this test asserting "
                f"an invariant or just tracking current values?\n"
                f"  was: {old.strip()}\n"
                f"  now: {new.strip()}"
            )
    return findings


def check_rework_commits() -> list[str]:
    """Detect fix/fixup commits following encoding commits."""
    findings = []
    log = _run("git log --oneline -5 2>/dev/null")
    if not log:
        return findings

    lines = log.strip().split("\n")
    rework_words = ("fix:", "fixup:", "amend:", "fix(", "hotfix:")
    encoding_words = ("feat(S", "feat(s")

    for i, line in enumerate(lines):
        msg = line.split(" ", 1)[1] if " " in line else ""
        is_fix = any(msg.lower().startswith(w) for w in rework_words)
        if is_fix and i + 1 < len(lines):
            prev_msg = lines[i + 1].split(" ", 1)[1] if " " in lines[i + 1] else ""
            is_encoding = any(prev_msg.lower().startswith(w) for w in encoding_words)
            if is_encoding:
                findings.append(
                    f"REWORK_COMMIT: '{msg[:60]}' follows encoding commit '{prev_msg[:60]}' — "
                    f"should this have been caught before the encoding commit shipped?"
                )
    return findings


def check_source_drift() -> list[str]:
    """Detect non-canonical source text names in staged corpus files."""
    findings = []
    try:
        from src.corpus.source_texts import VALID_SOURCE_NAMES
    except ImportError:
        return findings

    diff = _run(
        "git diff --cached -- 'src/corpus/' 2>/dev/null || "
        "git diff HEAD~1 -- 'src/corpus/' 2>/dev/null"
    )
    if not diff:
        return findings

    # Look for source="..." patterns in added lines
    for line in diff.split("\n"):
        if line.startswith("+") and "source=" in line:
            match = re.search(r'source=["\']([^"\']+)["\']', line)
            if match:
                name = match.group(1)
                if name not in VALID_SOURCE_NAMES:
                    findings.append(
                        f"SOURCE_DRIFT: source='{name}' not in CANONICAL_SOURCES — "
                        f"valid names: {sorted(VALID_SOURCE_NAMES)}"
                    )
    return findings


def check_memory_stale() -> list[str]:
    """Detect if code was pushed but MEMORY.md metrics are stale."""
    findings = []
    diff_files = _run(
        "git diff --cached --name-only 2>/dev/null || "
        "git diff HEAD~1 --name-only 2>/dev/null"
    )
    if not diff_files:
        return findings

    has_corpus_changes = any(
        f.startswith("src/corpus/") for f in diff_files.split("\n")
    )
    has_memory_change = any(
        "MEMORY" in f for f in diff_files.split("\n")
    )

    if has_corpus_changes and not has_memory_change:
        findings.append(
            "MEMORY_STALE: corpus files changed but MEMORY.md not updated in this commit — "
            "metrics may be stale for next session"
        )
    return findings


def main():
    parser = argparse.ArgumentParser(description="Rework & lesson detector")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any finding (blocks push)")
    args = parser.parse_args()

    all_findings: list[str] = []
    all_findings.extend(check_source_drift())
    all_findings.extend(check_rework_commits())
    all_findings.extend(check_test_chasing())
    all_findings.extend(check_naming_gap())
    all_findings.extend(check_memory_stale())

    if not all_findings:
        print("  No rework signals detected")
        return 0

    print(f"  {len(all_findings)} rework signal(s) detected:")
    for f in all_findings:
        print(f"    ⚡ {f}")
    print()
    print("  Action: check if a lesson or control is needed before session ends.")

    if args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
