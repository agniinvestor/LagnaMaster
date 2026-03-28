#!/usr/bin/env python3
"""
tools/start_session.py — LagnaMaster Session Brief Generator

Produces a compressed, accurate, sub-400-token session brief for pasting
into Claude. Eliminates all orientation work from the AI session.

Usage:
    cd ~/LagnaMaster
    .venv/bin/python3 tools/start_session.py

Optional override (to run a specific session instead of next):
    .venv/bin/python3 tools/start_session.py --session S192

Output: paste the printed brief as your FIRST message to Claude.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


# ─────────────────────────────────────────────────────────────────────────────
# Readers
# ─────────────────────────────────────────────────────────────────────────────

def git_sha() -> str:
    r = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, cwd=ROOT
    )
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def git_status_clean() -> bool:
    """Returns True if no tracked files have uncommitted changes.
    Ignores untracked files (update_docs scripts etc.) intentionally."""
    r = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=ROOT
    )
    # Only flag modified/deleted tracked files, not untracked (lines starting with ??)
    tracked_changes = [
        line for line in r.stdout.splitlines()
        if line and not line.startswith("??")
    ]
    return len(tracked_changes) == 0


def run_tests() -> tuple[int, int, int]:
    """Returns (passed, skipped, failed). Runs full suite."""
    # Raise macOS fd limit (default 256 is too low for 1300+ test suite)
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
    except Exception:
        pass  # Non-macOS or already high enough
    print("  Running test suite...", end="", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no", "--no-header"],
        capture_output=True, text=True, cwd=ROOT, env=env
    )
    output = r.stdout + r.stderr
    m = re.search(r"(\d+) passed", output)
    passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) skipped", output)
    skipped = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) failed", output)
    failed = int(m.group(1)) if m else 0
    if passed == 0:
        print(f"\n  pytest rc={r.returncode}, output: {output[:200]!r}")
    else:
        print(f" {passed} passed, {skipped} skipped, {failed} failed")
    return passed, skipped, failed


def run_ruff() -> int:
    """Returns error count."""
    r = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src/", "tests/", "tools/"],
        capture_output=True, text=True, cwd=ROOT
    )
    lines = [line for line in r.stdout.splitlines() if line.strip()]
    return len([line for line in lines if ": E" in line or ": W" in line or ": F" in line])


def read_memory() -> dict:
    """Extract key fields from docs/MEMORY.md."""
    text = (DOCS / "MEMORY.md").read_text()
    result = {}

    # Next session
    m = re.search(r"\*\*Next session:\*\* (S\d+)", text)
    result["next_session"] = m.group(1) if m else None

    # Test baseline from docs (used as sanity check against live run)
    m = re.search(r"\*\*(\d+) passing", text)
    result["docs_test_count"] = int(m.group(1)) if m else 0

    # Engine version
    m = re.search(r"\*\*Engine version:\*\* `([^`]+)`", text)
    result["engine_version"] = m.group(1) if m else "unknown"

    # Open bugs for next session
    bugs = []
    # Extract items from the priority queue table that aren't marked 🔵
    lines = text.splitlines()
    in_queue = False
    for line in lines:
        if "Priority Queue" in line or "Immediate Priority" in line:
            in_queue = True
        if in_queue and line.startswith("| 🟠") or (in_queue and line.startswith("| 🟡")):
            # Extract item description
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                bugs.append(parts[1])
        if in_queue and line.startswith("##") and "Priority" not in line:
            in_queue = False

    result["open_bugs"] = bugs[:5]  # Top 5 only
    return result


def read_roadmap(session_id: str) -> dict:
    """Extract session entry from ROADMAP.md. Handles table rows and section entries."""
    text = (DOCS / "ROADMAP.md").read_text()
    result = {
        "title": None,
        "deliverable": None,
        "guardrails": [],
        "convergence_layer": None,
        "phase": None,
        "boundary": None,
    }

    session_num = int(re.search(r"\d+", session_id).group())

    # Find the phase this session belongs to
    phase_map = [
        (range(191, 216), "Phase 0 — Guardrails & Infrastructure"),
        (range(216, 411), "Phase 1 — Classical Knowledge Foundation"),
        (range(411, 471), "Phase 2 — Engine Rebuild"),
        (range(471, 531), "Phase 3 — Feedback Architecture & Privacy"),
        (range(531, 611), "Phase 4 — Personality Protocol & Onboarding"),
        (range(611, 701), "Phase 5 — Temporal Model"),
        (range(701, 791), "Phase 6 — ML Pipeline & Empirical Discovery"),
        (range(791, 841), "Phase 7 — Product & Revenue"),
        (range(841, 901), "Phase 8 — Multigenerational Pattern Map"),
        (range(901, 951), "Phase 9 — Service Extraction"),
        (range(951, 1051), "Phase 10 — Research Frontiers"),
    ]

    for r, phase_name in phase_map:
        if session_num in r:
            result["phase"] = phase_name
            break

    if session_num < 191:
        result["phase"] = "Immediate / S190 queue"
        result["convergence_layer"] = "Layer I + II — immediate fixes and wiring"

    # Convergence layer by phase
    convergence_map = {
        "Phase 0": "Layer I + II infrastructure",
        "Phase 1": "Layer I — Classical Convergence depth",
        "Phase 2": "Layer I — Engine rebuild with full corpus",
        "Phase 3": "Layer III — Empirical Convergence infrastructure",
        "Phase 4": "Layer II — Structural Convergence person-specific calibration",
        "Phase 5": "Layer II — Temporal Model (delivery cascade)",
        "Phase 6": "Layer III — Empirical Convergence validation",
        "Phase 7": "Product — all three layers operational",
        "Phase 8": "Layer I — Multigenerational extension",
        "Phase 9": "Architecture — service extraction",
        "Phase 10": "Research — scientific output",
    }
    for key, layer in convergence_map.items():
        if result["phase"] and key in result["phase"]:
            result["convergence_layer"] = layer
            break

    # Find table row matching this session
    # Matches: | S191 | ... | or | S191–S200 | ...
    lines = text.splitlines()
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue

        # Check if this row covers our session
        session_cell = cells[0]
        # Handle ranges like S195–S200
        range_match = re.match(r"S(\d+)[\-–]S(\d+)", session_cell)
        exact_match = re.match(r"S(\d+)$", session_cell)

        covers = False
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            covers = start <= session_num <= end
        elif exact_match:
            covers = int(exact_match.group(1)) == session_num

        if covers and len(cells) >= 2:
            result["title"] = session_cell
            result["deliverable"] = cells[1] if len(cells) > 1 else ""
            # Guardrails column (typically 3rd column in Phase 0 table)
            if len(cells) >= 3:
                guardrails_text = cells[2]
                result["guardrails"] = [
                    g.strip() for g in re.findall(r"G\d+", guardrails_text)
                ]
            break

    if not result["deliverable"]:
        result["deliverable"] = f"See docs/ROADMAP.md for {session_id} details"

    return result


def read_active_guardrails(session_id: str) -> list[tuple[str, str]]:
    """Return guardrails with Fix-by matching this session.
    Uses heading-bounded blocks to avoid cross-block contamination."""
    text = (DOCS / "GUARDRAILS.md").read_text()
    session_num = int(re.search(r"\d+", session_id).group())
    active = []

    # Find all ### G\d+ headings and their positions
    heading_positions = [
        (m.group(1), m.start())
        for m in re.finditer(r"### (G\d+)", text)
    ]

    for i, (g_id, pos) in enumerate(heading_positions):
        # Block ends at next heading or end of file
        end = heading_positions[i + 1][1] if i + 1 < len(heading_positions) else len(text)
        block = text[pos:end]

        # Find FIRST Fix-by in this block only
        fix_match = re.search(r"\*\*Fix by:\*\*\s*S(\d+)", block)
        if fix_match and int(fix_match.group(1)) == session_num:
            # Extract title from heading line (strip emoji and severity marker)
            title_match = re.match(
                r"### G\d+\s*[🔴🟠🟡🟢]?\s*(.*?)$", block, re.MULTILINE
            )
            title = title_match.group(1).strip() if title_match else g_id
            active.append((g_id, title[:80]))

    return active


def build_read_list(session_id: str, roadmap: dict) -> list[tuple[str, str]]:
    """
    Build targeted read list based on session deliverable.
    Returns list of (file_spec, reason) tuples.
    File specs use line ranges where possible: 'docs/MEMORY.md:1-30'
    """
    reads = []
    deliverable = (roadmap.get("deliverable") or "").lower()

    # Always: ROADMAP.md entry for this session (already extracted, but Claude needs context)
    reads.append(("docs/ROADMAP.md", "session plan"))
    reads.append(("docs/PREDICTION_PIPELINE.md:1-80", "convergence layer framing"))

    # Conditionally based on deliverable keywords
    keyword_reads = [
        (["architecture", "protocol", "interface", "di container"],
         "docs/ARCHITECTURE.md:1-60", "convergence architecture overview"),
        (["guardrail", "legal", "privacy", "gdpr", "dpdp"],
         "docs/GUARDRAILS.md", "applicable guardrails"),
        (["corpus", "bphs", "rule", "yoga", "text", "encoding"],
         "docs/CLASSICAL_CORPUS.md", "corpus encoding context"),
        (["kpi", "metric", "score", "calibration", "osfb", "brier"],
         "docs/KPIS.md", "metrics baseline"),
        (["research", "osf", "shap", "bayesian", "empirical"],
         "docs/RESEARCH.md", "research methodology"),
        (["roadmap", "phase", "plan"],
         "docs/ROADMAP.md", "phase context"),
    ]

    for keywords, file_spec, reason in keyword_reads:
        if any(k in deliverable for k in keywords):
            if file_spec not in [r[0] for r in reads]:
                reads.append((file_spec, reason))

    # For new module sessions: architecture module inventory
    if any(k in deliverable for k in ["module", "implement", "build", "create", "add"]):
        reads.append(("docs/ARCHITECTURE.md:1-100", "module inventory + convergence layer map"))

    # For sessions touching existing modules: their specific section in ARCHITECTURE.md
    # Map common module names to approximate line ranges
    module_line_hints = {
        "shadbala": "docs/ARCHITECTURE.md:155-175",
        "ephemeris": "docs/ARCHITECTURE.md:78-115",
        "scoring": "docs/ARCHITECTURE.md:180-250",
        "vimshottari": "docs/ARCHITECTURE.md:130-145",
        "varga": "docs/ARCHITECTURE.md:200-215",
        "ashtakavarga": "docs/ARCHITECTURE.md:245-270",
        "dignity": "docs/ARCHITECTURE.md:115-130",
        "nakshatra": "docs/ARCHITECTURE.md:125-135",
        "yogas": "docs/ARCHITECTURE.md:160-180",
        "lpi": "docs/ARCHITECTURE.md:190-210",
    }
    for module_name, line_spec in module_line_hints.items():
        if module_name in deliverable:
            if line_spec not in [r[0] for r in reads]:
                reads.append((line_spec, f"{module_name} module reference"))

    # Deduplicate
    seen = set()
    deduped = []
    for spec, reason in reads:
        if spec not in seen:
            seen.add(spec)
            deduped.append((spec, reason))

    return deduped


def estimate_test_delta(session_id: str, roadmap: dict) -> str:
    """Estimate expected test count increase for session."""
    deliverable = (roadmap.get("deliverable") or "").lower()
    session_num = int(re.search(r"\d+", session_id).group())

    # Known test targets by phase
    if 191 <= session_num <= 215:
        return "+20 to +40 (Phase 0 infrastructure)"
    elif 216 <= session_num <= 410:
        return "+15 to +30 (corpus encoding + rule tests)"
    elif 411 <= session_num <= 470:
        return "+30 to +60 (engine rebuild)"
    elif 471 <= session_num <= 530:
        return "+25 to +50 (feedback schema)"
    elif 531 <= session_num <= 610:
        return "+20 to +40 (protocol tests)"
    elif 611 <= session_num <= 700:
        return "+30 to +60 (temporal model)"
    elif 701 <= session_num <= 790:
        return "+20 to +40 (ML pipeline)"

    # Keyword-based estimate
    if "test" in deliverable or "fixture" in deliverable:
        return "+20 to +50"
    elif "implement" in deliverable or "build" in deliverable:
        return "+15 to +30"
    elif "fix" in deliverable or "patch" in deliverable:
        return "+5 to +15"
    else:
        return "+10 to +25"


# ─────────────────────────────────────────────────────────────────────────────
# Brief formatter
# ─────────────────────────────────────────────────────────────────────────────

def format_brief(
    session_id: str,
    sha: str,
    live_tests: tuple[int, int, int],
    ruff_errors: int,
    memory: dict,
    roadmap: dict,
    active_guardrails: list,
    read_list: list,
    test_delta: str,
) -> str:
    passed, skipped, failed = live_tests
    lines = []

    lines.append("═" * 60)
    lines.append(f"SESSION BRIEF — {session_id}")
    lines.append("═" * 60)
    lines.append("")
    lines.append(f"SHA:   {sha}")
    lines.append(f"PHASE: {roadmap.get('phase', 'unknown')}")
    lines.append(f"LAYER: {roadmap.get('convergence_layer', 'unknown')}")
    lines.append("")
    lines.append("STATE:")
    lines.append(f"  Tests:  {passed} passed, {skipped} skipped, {failed} failed")
    lines.append(f"  Ruff:   {ruff_errors} errors")
    lines.append(f"  Git:    {'clean' if git_status_clean() else 'UNCOMMITTED CHANGES'}")
    lines.append("")
    lines.append("PLAN:")
    lines.append(f"  {roadmap.get('deliverable', 'See ROADMAP.md')}")
    lines.append("")

    if active_guardrails:
        lines.append("GUARDRAILS (active this session):")
        for g_id, title in active_guardrails:
            lines.append(f"  {g_id}: {title}")
        lines.append("")

    if roadmap.get("guardrails"):
        lines.append(f"GUARDRAILS (from roadmap): {', '.join(roadmap['guardrails'])}")
        lines.append("")

    if memory.get("open_bugs"):
        lines.append("OPEN BUGS (relevant):")
        for bug in memory["open_bugs"]:
            lines.append(f"  - {bug}")
        lines.append("")

    lines.append("READ (targeted — load only these):")
    for spec, reason in read_list:
        lines.append(f"  {spec:<45} # {reason}")
    lines.append("")

    # Modules that require India 1947 position verification when touched
    _CALC_SUBSTRATE = {"ephemeris.py", "varga.py", "narayana_dasa.py", "nakshatra.py", "dignity.py"}
    read_specs = [spec for spec, _ in read_list]
    needs_1947 = any(m in " ".join(read_specs) for m in _CALC_SUBSTRATE)

    lines.append("ACCEPTANCE CRITERIA:")
    lines.append(f"  - Full test suite passes: {passed} → {passed}+N  (200+ diverse fixtures)")
    lines.append(f"  - Test delta estimate: {test_delta}")
    lines.append(f"  - Ruff errors: {ruff_errors} → 0")
    lines.append(f"  - Convergence layer: {roadmap.get('convergence_layer', '?')} wired correctly")
    if needs_1947:
        lines.append("  - India 1947 positions: Lagna=7.7286°Tau ±0.05°, Sun=27.989°Can, Moon=3.9835°Can")
    lines.append("")
    lines.append("═" * 60)
    lines.append("INSTRUCTIONS FOR CLAUDE:")
    lines.append("")
    lines.append("1. Read only the files listed in READ above.")
    lines.append("2. Declare session plan (one structured block — no prose).")
    lines.append("3. Write failing tests first.")
    lines.append("4. Write implementation to pass tests.")
    lines.append(f"5. Write update_docs_{session_id.lower()}.py inline (see below).")
    lines.append("6. Output git commands to commit everything atomically.")
    lines.append("")
    lines.append("SCOPE RULE: One session only. When step 6 is complete, stop.")
    lines.append("If implementation cannot complete in one response, reduce scope,")
    lines.append("commit what's done, and note the adjusted scope in the docs script.")
    lines.append("")
    lines.append("DOCS RULE: update_docs_s[N].py is part of this session, not after.")
    lines.append("It must be committed in the same push as the implementation code.")
    lines.append("The pre-push hook validates: pytest + ruff + docs currency together.")
    lines.append("═" * 60)

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate LagnaMaster session brief")
    parser.add_argument("--session", type=str, default=None,
                        help="Session to run (e.g. S192). Defaults to next from MEMORY.md")
    parser.add_argument("--no-test-run", action="store_true",
                        help="Skip live test run (use MEMORY.md baseline). Faster but less accurate.")
    args = parser.parse_args()

    print("LagnaMaster Session Brief Generator")
    print("─" * 40)

    # 1. Git state
    sha = git_sha()
    print(f"  SHA: {sha}")

    # 2. Read MEMORY.md
    memory = read_memory()
    session_id = args.session or memory.get("next_session")
    if not session_id:
        print("ERROR: Could not determine next session from MEMORY.md")
        print("  Add '- **Next session:** S[N]' to MEMORY.md or use --session S[N]")
        sys.exit(1)

    print(f"  Session: {session_id}")

    # 3. Live test run (or use docs baseline)
    if args.no_test_run:
        docs_count = memory.get("docs_test_count", 0)
        live_tests = (docs_count, 3, 0)
        ruff_errors = 0
        print(f"  Tests: {docs_count} (from MEMORY.md — skipping live run)")
    else:
        live_tests = run_tests()
        ruff_errors = run_ruff()
        if live_tests[2] > 0:  # failures
            print(f"\n  ⚠️  WARNING: {live_tests[2]} test failures detected.")
            print("  Resolve test failures before starting a new session.")
            print("  Run: PYTHONPATH=. .venv/bin/pytest tests/ -x --tb=short")
            sys.exit(1)
        if ruff_errors > 0:
            print(f"\n  ⚠️  WARNING: {ruff_errors} ruff errors detected.")
            print("  Run: .venv/bin/ruff check src/ tests/ tools/ --fix")
            sys.exit(1)

    # 4. Read roadmap
    roadmap = read_roadmap(session_id)

    # 5. Active guardrails
    active_guardrails = read_active_guardrails(session_id)

    # 6. Build read list
    read_list = build_read_list(session_id, roadmap)

    # 7. Test delta estimate
    test_delta = estimate_test_delta(session_id, roadmap)

    # 8. Format and print brief
    brief = format_brief(
        session_id=session_id,
        sha=sha,
        live_tests=live_tests,
        ruff_errors=ruff_errors,
        memory=memory,
        roadmap=roadmap,
        active_guardrails=active_guardrails,
        read_list=read_list,
        test_delta=test_delta,
    )

    print("\n" + "─" * 40)
    print("BRIEF (paste this as your first message to Claude):")
    print("─" * 40)
    print(brief)

    # Write to file as well so it can be piped
    brief_file = ROOT / f".session_brief_{session_id.lower()}.txt"
    brief_file.write_text(brief)
    print(f"\n  Also saved to: {brief_file.name}")
    print("  To pipe: pbcopy < .session_brief_s[n].txt  (macOS)")
    print("           xclip -sel clip < .session_brief_s[n].txt  (Linux)")


if __name__ == "__main__":
    main()
