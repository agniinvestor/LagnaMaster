#!/usr/bin/env python3
"""Rework detection for LagnaMaster sessions.

Scans recent git history for rework indicators:
  - Commit messages containing fix/amend/correct/revert/redo/rework/repair
  - Multiple commits touching the same file (iteration/rework)

Exit code 0 = no rework detected
Exit code 1 = rework detected (hooks can gate on this)

Usage:
    python tools/rework_counter.py              # last 20 commits
    python tools/rework_counter.py --commits 50 # last 50 commits
    python tools/rework_counter.py --since HEAD~10  # since a specific ref
"""

import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict


# --- Configuration ---

REWORK_KEYWORDS = re.compile(
    r"\b(fix|fixup|fix[_-]up|amend|correct|revert|redo|rework|repair|oops|typo|missed|forgot)\b",
    re.IGNORECASE,
)

# Minimum file touch count to flag as iteration rework
FILE_TOUCH_THRESHOLD = 2

LESSONS_TEMPLATE = """
## L0NN: [Title] (Session)

**What:** [Specific failure — what happened, what was the rework?]
**Cost:** [Sessions/hours/commits wasted. Be specific.]
**Control:** [What code/hook/gate should be built to prevent recurrence?]
**Would catch?** [Yes/No + explain why the control catches this pattern]
""".strip()


def run_git(*args: str) -> str:
    """Run a git command, return stdout. Raises on failure."""
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def get_commits(n: int, since: str | None = None) -> list[dict]:
    """Return list of {hash, subject, body, files} for recent commits.

    Uses two-pass approach to avoid ambiguity between body text and filenames.
    """
    # Pass 1: Get commit metadata (hash, subject only -- body is unreliable
    # with multiline, so we get subject which is sufficient for keyword detection)
    if since:
        log_range = f"{since}..HEAD"
        raw = run_git("log", log_range, "--format=%H%x00%s")
    else:
        raw = run_git("log", f"-{n}", "--format=%H%x00%s")

    if not raw:
        return []

    commits = []
    for line in raw.strip().split("\n"):
        line = line.strip()
        if not line or "\x00" not in line:
            continue
        parts = line.split("\x00", 1)
        commit_hash = parts[0]
        subject = parts[1] if len(parts) > 1 else ""
        commits.append({
            "hash": commit_hash[:8],
            "subject": subject,
            "files": [],
        })

    # Pass 2: Get files for each commit
    for c in commits:
        try:
            files_raw = run_git(
                "diff-tree", "--no-commit-id", "--name-only", "-r", c["hash"],
            )
            c["files"] = [f for f in files_raw.split("\n") if f.strip()]
        except RuntimeError:
            c["files"] = []

    return commits


def detect_keyword_rework(commits: list[dict]) -> list[dict]:
    """Find commits whose subject matches rework keywords."""
    flagged = []
    for c in commits:
        matches = REWORK_KEYWORDS.findall(c["subject"])
        if matches:
            flagged.append({
                **c,
                "keywords": [m.lower() for m in matches],
            })
    return flagged


def detect_file_iteration(commits: list[dict]) -> dict[str, list[str]]:
    """Find files touched by multiple commits (iteration rework).

    Returns {filepath: [commit_hash, ...]} for files above threshold.
    """
    file_commits: dict[str, list[str]] = defaultdict(list)
    for c in commits:
        for f in c["files"]:
            file_commits[f].append(c["hash"])

    return {
        f: hashes
        for f, hashes in file_commits.items()
        if len(hashes) >= FILE_TOUCH_THRESHOLD
    }


def print_report(
    total: int,
    keyword_rework: list[dict],
    file_iteration: dict[str, list[str]],
) -> None:
    """Print structured rework report."""
    rework_count = len(keyword_rework)
    iterated_files = len(file_iteration)
    rework_pct = (rework_count / total * 100) if total > 0 else 0

    print("=" * 60)
    print("REWORK DETECTION REPORT")
    print("=" * 60)
    print()
    print(f"  Total commits scanned:     {total}")
    print(f"  Rework commits (keyword):  {rework_count}")
    print(f"  Rework percentage:         {rework_pct:.1f}%")
    print(f"  Files with iteration:      {iterated_files}")
    print()

    if keyword_rework:
        print("-" * 60)
        print("KEYWORD REWORK COMMITS")
        print("-" * 60)
        for c in keyword_rework:
            kw = ", ".join(sorted(set(c["keywords"])))
            print(f"  {c['hash']}  [{kw}]  {c['subject']}")
            if c["files"]:
                for f in c["files"][:5]:
                    print(f"             -> {f}")
                if len(c["files"]) > 5:
                    print(f"             -> ... and {len(c['files']) - 5} more")
        print()

    if file_iteration:
        print("-" * 60)
        print("FILES TOUCHED BY MULTIPLE COMMITS (iteration)")
        print("-" * 60)
        # Sort by touch count descending
        for f, hashes in sorted(
            file_iteration.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"  {len(hashes)}x  {f}  ({', '.join(hashes)})")
        print()

    # Categorize the rework patterns
    keyword_counter: Counter = Counter()
    for c in keyword_rework:
        for kw in c["keywords"]:
            keyword_counter[kw] += 1

    if keyword_counter:
        print("-" * 60)
        print("REWORK PATTERN SUMMARY")
        print("-" * 60)
        for kw, count in keyword_counter.most_common():
            print(f"  {kw}: {count} occurrence(s)")
        print()

    # Always print the action required section if rework detected
    if keyword_rework or file_iteration:
        print("=" * 60)
        print("ACTION REQUIRED: Add a lessons_learned entry")
        print("=" * 60)
        print()
        print("Every rework incident must produce a lesson. Use this template:")
        print()
        print(LESSONS_TEMPLATE)
        print()
        print("Add it to: docs/lessons_learned.md or the project memory file.")
        print("Pattern: What specific mistake caused the rework?")
        print("Control: What code enforcement prevents recurrence?")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect rework in recent git history")
    parser.add_argument(
        "--commits", "-n",
        type=int,
        default=20,
        help="Number of recent commits to scan (default: 20)",
    )
    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Git ref to scan from (e.g., HEAD~10, abc1234). Overrides --commits.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress report output, only set exit code",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of text report",
    )
    args = parser.parse_args()

    try:
        commits = get_commits(args.commits, args.since)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if not commits:
        if not args.quiet:
            print("No commits found in the specified range.")
        return 0

    keyword_rework = detect_keyword_rework(commits)
    file_iteration = detect_file_iteration(commits)

    has_rework = bool(keyword_rework) or bool(file_iteration)

    if args.json:
        import json
        report = {
            "total_commits": len(commits),
            "rework_commits": len(keyword_rework),
            "rework_percentage": round(len(keyword_rework) / len(commits) * 100, 1),
            "iterated_files": len(file_iteration),
            "keyword_rework": [
                {"hash": c["hash"], "subject": c["subject"], "keywords": c["keywords"]}
                for c in keyword_rework
            ],
            "file_iteration": {f: hashes for f, hashes in file_iteration.items()},
            "has_rework": has_rework,
        }
        print(json.dumps(report, indent=2))
    elif not args.quiet:
        print_report(len(commits), keyword_rework, file_iteration)

    return 1 if has_rework else 0


if __name__ == "__main__":
    sys.exit(main())
