#!/usr/bin/env python3
"""
tools/start_session.py — LagnaMaster Session Packet Generator (v2)

Emits a self-contained ~350-token packet. Claude receives signatures,
test skeleton, and exact git command. Zero in-session file reads needed.

Usage:
    cd ~/LagnaMaster
    .venv/bin/python3 tools/start_session.py
    .venv/bin/python3 tools/start_session.py --session S193
    .venv/bin/python3 tools/start_session.py --no-test-run
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

_MODULE_MAP = {
    "shadbala": "src/calculations/shadbala.py",
    "kala_bala": "src/calculations/shadbala.py",
    "ephemeris": "src/ephemeris.py",
    "birth_chart": "src/ephemeris.py",
    "scoring": "src/calculations/scoring_v3.py",
    "score_chart": "src/calculations/scoring_v3.py",
    "multi_axis": "src/calculations/multi_axis_scoring.py",
    "house_score": "src/calculations/scoring_v3.py",
    "lpi": "src/calculations/lpi.py",
    "varga": "src/calculations/varga.py",
    "dignity": "src/calculations/dignity.py",
    "nakshatra": "src/calculations/nakshatra.py",
    "narayana": "src/calculations/narayana_dasa.py",
    "vimshottari": "src/calculations/vimshottari_dasa.py",
    "confidence": "src/calculations/confidence_model.py",
    "confidence_tab": "src/ui/confidence_tab.py",
    "ashtakavarga": "src/calculations/ashtakavarga.py",
    "promise": "src/calculations/promise_engine.py",
    "yogas": "src/calculations/yogas.py",
    "jaimini": "src/calculations/jaimini_full.py",
    "kp": "src/calculations/kp_full.py",
    "weight": "src/calculations/multi_axis_scoring.py",
    "protocol": "src/interfaces/__init__.py",
    "interface": "src/interfaces/__init__.py",
    "feedback": "src/privacy/consent_engine.py",
    "consent": "src/privacy/consent_engine.py",
    "db": "src/db.py",
    "api": "src/api/main.py",
    "streamlit": "src/ui/app.py",
    "ui": "src/ui/app.py",
}


def git_sha():
    r = subprocess.run(["git","rev-parse","--short","HEAD"], capture_output=True, text=True, cwd=ROOT)
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def git_status_clean():
    r = subprocess.run(["git","status","--porcelain"], capture_output=True, text=True, cwd=ROOT)
    tracked = [ln for ln in r.stdout.splitlines() if ln and not ln.startswith("??")]
    return len(tracked) == 0


def run_tests():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
    except Exception:
        pass
    print("  Running test suite...", end="", flush=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    r = subprocess.run(
        [str(ROOT / ".venv/bin/pytest"), "tests/", "-q", "--tb=no", "--no-header"],
        capture_output=True, text=True, cwd=ROOT, env=env,
    )
    output = r.stdout + r.stderr
    if r.returncode == 1 and not re.search(r"\d+ passed", output):
        print(f"\n  pytest rc=1, output: {output[:200]!r}")
    m = re.search(r"(\d+) passed", output)
    passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) skipped", output)
    skipped = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) failed", output)
    failed = int(m.group(1)) if m else 0
    print(f" {passed} passed, {skipped} skipped, {failed} failed")
    return passed, skipped, failed


def run_ruff():
    r = subprocess.run(
        [str(ROOT / ".venv/bin/ruff"), "check", "src/", "tests/", "tools/"],
        capture_output=True, text=True, cwd=ROOT,
    )
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    return len([ln for ln in lines if ": E" in ln or ": W" in ln or ": F" in ln])


def read_memory():
    text = (DOCS / "MEMORY.md").read_text()
    m = re.search(r"\*\*Next session:\*\* (S\d+)", text)
    next_session = m.group(1) if m else None
    m = re.search(r"\*\*(\d+) passing", text)
    docs_test_count = int(m.group(1)) if m else 0
    return {"next_session": next_session, "docs_test_count": docs_test_count}


def read_roadmap(session_id):
    text = (DOCS / "ROADMAP.md").read_text()
    session_num = int(re.search(r"\d+", session_id).group())
    result = {"title": session_id, "deliverable": None, "guardrails": [],
              "phase": None, "convergence_layer": None}
    phase_map = [
        (range(191,216), "Phase 0 — Guardrails & Infrastructure", "Layer I + II infrastructure"),
        (range(216,411), "Phase 1 — Classical Knowledge Foundation", "Layer I — Classical Convergence depth"),
        (range(411,471), "Phase 2 — Engine Rebuild", "Layer I — Engine rebuild"),
        (range(471,531), "Phase 3 — Feedback Architecture", "Layer III — Empirical Convergence infrastructure"),
        (range(531,611), "Phase 4 — Personality Protocol", "Layer II — person-specific calibration"),
        (range(611,701), "Phase 5 — Temporal Model", "Layer II — Temporal Model"),
        (range(701,791), "Phase 6 — ML Pipeline", "Layer III — Empirical Convergence validation"),
        (range(791,841), "Phase 7 — Product & Revenue", "Product — all layers operational"),
    ]
    for rng, phase, layer in phase_map:
        if session_num in rng:
            result["phase"] = phase
            result["convergence_layer"] = layer
            break
    if session_num < 191:
        result["phase"] = "Immediate"
        result["convergence_layer"] = "Layer I + II — immediate fixes"
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue
        sc = cells[0]
        rm = re.match(r"S(\d+)[\-\u2013]S(\d+)", sc)
        em = re.match(r"S(\d+)$", sc)
        covers = False
        if rm:
            covers = int(rm.group(1)) <= session_num <= int(rm.group(2))
        elif em:
            covers = int(em.group(1)) == session_num
        if covers and len(cells) >= 2:
            result["deliverable"] = cells[1]
            if len(cells) >= 3:
                result["guardrails"] = re.findall(r"G\d+", cells[2])
            break
    return result


def read_active_guardrails(session_id):
    text = (DOCS / "GUARDRAILS.md").read_text()
    session_num = int(re.search(r"\d+", session_id).group())
    active = []
    heading_positions = [(m.group(1), m.start()) for m in re.finditer(r"### (G\d+)", text)]
    for i, (g_id, pos) in enumerate(heading_positions):
        end = heading_positions[i+1][1] if i+1 < len(heading_positions) else len(text)
        block = text[pos:end]
        fix_match = re.search(r"\*\*Fix by:\*\*\s*S(\d+)", block)
        if fix_match and int(fix_match.group(1)) == session_num:
            tm = re.match(r"### G\d+\s*[\U0001F534\U0001F7E0\U0001F7E1\U0001F7E2]?\s*(.*?)$", block, re.MULTILINE)
            title = tm.group(1).strip() if tm else g_id
            active.append((g_id, title[:70]))
    return active


def _topic_slug(deliverable):
    words = re.findall(r"[a-z0-9]+", (deliverable or "").lower())
    stop = {"the","a","an","and","or","with","for","to","of","in","is","replaces","install","download","add"}
    meaningful = [w for w in words if w not in stop and len(w) > 2][:2]
    return "_".join(meaningful) if meaningful else "impl"


def extract_signatures(deliverable, guardrails):
    if not deliverable:
        return []
    keywords = re.findall(r"[a-z0-9_]+", deliverable.lower())
    seen_files = set()
    file_candidates = []
    for kw in keywords:
        if kw in _MODULE_MAP:
            fp = _MODULE_MAP[kw]
            if fp not in seen_files:
                seen_files.add(fp)
                file_candidates.append(fp)
    guardrail_files = {"G04": "src/calculations/scoring_v3.py", "G06": "src/calculations/shadbala.py",
                       "G18": "src/calculations/confidence_model.py"}
    for g in guardrails:
        fp = guardrail_files.get(g)
        if fp and fp not in seen_files:
            seen_files.add(fp)
            file_candidates.append(fp)
    signatures = []
    for rel_path in file_candidates[:3]:
        full = ROOT / rel_path
        if not full.exists():
            signatures.append(f"  {rel_path}  [not yet created]")
            continue
        text = full.read_text()
        short = Path(rel_path).name
        sigs = []
        for line in text.splitlines():
            stripped = line.strip()
            if re.match(r"^(def |class |@dataclass)", stripped):
                nm = re.match(r"^(?:def |class )([A-Za-z][^(:]+)", stripped)
                if nm and not nm.group(1).startswith("_"):
                    sigs.append(f"  {short}:  {stripped[:88]}")
        signatures.extend(sigs[:4])
        if len(signatures) >= 8:
            break
    return signatures[:8]


def generate_test_skeleton(session_id, deliverable):
    d = (deliverable or "").lower()
    skeletons = []
    keyword_tests = [
        ("dataclass",    ["test_dataclass_fields()", "test_dataclass_serializes_to_json()"]),
        ("distribution", ["test_distribution_has_mean_std_p10_p90()", "test_distribution_range_valid()"]),
        ("weight",       ["test_weight_returns_float()", "test_weight_lagna_conditional()"]),
        ("vedastro",     ["test_vedastro_importable()", "test_vedastro_chart_matches_ephemeris()"]),
        ("ruff",         ["test_ruff_no_jhora_rule_active()", "test_jhora_import_blocked()"]),
        ("jhora",        ["test_jhora_not_importable_from_src()"]),
        ("protocol",     ["test_protocol_defines_required_methods()", "test_concrete_class_satisfies_protocol()"]),
        ("interface",    ["test_interface_is_runtime_checkable()"]),
        ("shadbala",     ["test_shadbala_all_7_planets()", "test_shadbala_total_positive()"]),
        ("kala_bala",    ["test_kala_bala_8_components()", "test_kala_bala_vara_friday()"]),
        ("confidence",   ["test_confidence_returns_grade()", "test_lagna_stability_flag()"]),
        ("postgres",     ["test_pg_connection_with_dsn()", "test_pg_insert_and_retrieve()"]),
        ("corpus",       ["test_corpus_rule_has_required_fields()", "test_corpus_rule_count_increases()"]),
        ("score",        ["test_score_returns_house_dict()", "test_score_india_1947_h2_negative()"]),
    ]
    for keyword, tests in keyword_tests:
        if keyword in d:
            skeletons.extend(tests)
    skeletons.append("test_existing_suite_unaffected()")
    seen = set()
    unique = []
    for t in skeletons:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:6]


def predict_output_files(session_id, deliverable):
    sn = session_id.lower()
    d = (deliverable or "").lower()
    slug = _topic_slug(d)
    new_files = [f"tests/test_{sn}_{slug}.py", f"update_docs_{sn}.py"]
    modified = ["docs/MEMORY.md", "docs/CHANGELOG.md"]
    if any(k in d for k in ["dataclass","house_score","distribution"]):
        new_files.insert(0, "src/calculations/house_score.py")
        modified.insert(0, "src/calculations/scoring_v3.py")
    elif any(k in d for k in ["protocol","interface"]):
        new_files.insert(0, "src/interfaces/classical_engine.py")
        modified.insert(0, "src/interfaces/__init__.py")
    elif "weight" in d:
        new_files.insert(0, "src/calculations/weight_manager.py")
        modified.insert(0, "src/calculations/multi_axis_scoring.py")
    elif "ruff" in d or "jhora" in d:
        modified.insert(0, ".ruff.toml")
    elif "vedastro" in d:
        new_files.insert(0, "data/vedastro/  (dataset)")
    elif any(k in d for k in ["corpus","bphs","rule"]):
        new_files.insert(0, "src/calculations/corpus_rules.py")
    return new_files, modified


def estimate_test_delta(session_id, roadmap):
    session_num = int(re.search(r"\d+", session_id).group())
    if 191 <= session_num <= 215:
        return "+15 to +30"
    elif 216 <= session_num <= 410:
        return "+10 to +25"
    elif 411 <= session_num <= 530:
        return "+20 to +50"
    return "+10 to +25"


def format_packet(session_id, sha, live_tests, ruff_errors, roadmap, active_guardrails,
                  signatures, test_skeleton, new_files, modified_files, test_delta):
    passed, skipped, failed = live_tests
    sn = session_id.lower()
    slug = _topic_slug(roadmap.get("deliverable",""))
    lines = []

    lines.append("══════ " + session_id + " PACKET " + "═" * max(0, 50 - len(session_id)))
    lines.append(f"SHA: {sha}  |  {passed} passed, {failed} failed  |  ruff: {ruff_errors} errors")
    lines.append(f"Git: {'clean ✅' if git_status_clean() else 'UNCOMMITTED CHANGES ⚠️'}")
    lines.append("")
    lines.append(f"DELIVERABLE: {roadmap.get('deliverable', 'See ROADMAP.md')}")
    lines.append(f"LAYER:       {roadmap.get('convergence_layer', 'unknown')}")

    all_g = list(active_guardrails)
    active_ids = {g for g, _ in all_g}
    for g in roadmap.get("guardrails", []):
        if g not in active_ids:
            all_g.append((g, ""))
    if all_g:
        g_str = ", ".join(f"{g} ({t[:25]})" if t else g for g, t in all_g)
        lines.append(f"GUARDRAILS:  {g_str}")
    lines.append("")

    if signatures:
        lines.append("RELEVANT SIGNATURES:")
        lines.extend(signatures)
        lines.append("")

    if test_skeleton:
        lines.append(f"TEST SKELETON  →  tests/test_{sn}_{slug}.py:")
        for t in test_skeleton:
            lines.append(f"  {t}")
        lines.append("")

    lines.append("FILES TO CREATE:")
    for f in new_files:
        lines.append(f"  {f}")
    lines.append("FILES TO MODIFY:")
    for f in modified_files:
        lines.append(f"  {f}")
    lines.append("")

    _CALC = {"ephemeris.py","varga.py","narayana_dasa.py","nakshatra.py","dignity.py"}
    needs_1947 = any(m in " ".join(new_files+modified_files) for m in _CALC)
    lines.append(f"ACCEPTANCE: {passed} → {passed}+N tests  |  ruff: 0  |  delta: {test_delta}")
    if needs_1947:
        lines.append("  + India 1947: Lagna=7.7286°Tau ±0.05°, Sun=27.989°Can, Moon=3.9835°Can")
    lines.append("")

    tracked = [f for f in new_files + ["docs/ARCHITECTURE.md","docs/MEMORY.md","docs/CHANGELOG.md"]
               if not f.startswith("data/") and "dataset" not in f]
    lines.append("COMMIT WHEN DONE:")
    if len(" ".join(tracked)) > 70:
        lines.append("  git add \\")
        for p in tracked[:-1]:
            lines.append(f"    {p} \\")
        lines.append(f"    {tracked[-1]}")
    else:
        lines.append(f"  git add {chr(32).join(tracked)}")
    lines.append(f"  git commit -m \"feat({session_id}): [description]\"")
    lines.append("  git push")
    lines.append("")
    lines.append("─── EXECUTION ORDER " + "─" * 40)
    lines.append("1. Read src/ files listed in RELEVANT SIGNATURES before writing anything.")
    lines.append("2. Declare plan — structured block, <10 lines, no prose")
    lines.append("3. Write tests/test_s[N]_*.py — ALL FAILING")
    lines.append("4. Write implementation until all tests pass")
    lines.append("5. Write update_docs_s[N].py")
    lines.append("6. git add / commit / push  (pre-push hook is the gate)")
    lines.append("")
    lines.append("SCOPE: Exactly the ROADMAP deliverable. Nothing added silently.")
    lines.append("BLOCKING: Reduce scope, commit what passes, record blocker in docs. Stop.")
    lines.append("AUTONOMY: Own every technical decision. Tests pass + ruff clean = ships.")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=str, default=None)
    parser.add_argument("--no-test-run", action="store_true")
    args = parser.parse_args()

    print("LagnaMaster Session Packet Generator v2")
    print("─" * 40)

    sha = git_sha()
    print(f"  SHA: {sha}")

    memory = read_memory()
    session_id = args.session or memory.get("next_session")
    if not session_id:
        print("ERROR: no next session in MEMORY.md. Use --session S[N]")
        sys.exit(1)
    print(f"  Session: {session_id}")

    if args.no_test_run:
        docs_count = memory.get("docs_test_count", 0)
        live_tests = (docs_count, 3, 0)
        ruff_errors = 0
        print(f"  Tests: {docs_count} (MEMORY.md baseline)")
    else:
        live_tests = run_tests()
        ruff_errors = run_ruff()
        if live_tests[2] > 0:
            print(f"\n  ⚠️  {live_tests[2]} failures — fix before starting session")
            sys.exit(1)
        if ruff_errors > 0:
            print(f"\n  ⚠️  {ruff_errors} ruff errors — run ruff --fix")
            sys.exit(1)

    roadmap    = read_roadmap(session_id)
    guardrails = read_active_guardrails(session_id)
    signatures = extract_signatures(roadmap.get("deliverable",""), roadmap.get("guardrails",[]))
    skeleton   = generate_test_skeleton(session_id, roadmap.get("deliverable",""))
    new_files, modified = predict_output_files(session_id, roadmap.get("deliverable",""))
    delta      = estimate_test_delta(session_id, roadmap)

    packet = format_packet(
        session_id=session_id, sha=sha, live_tests=live_tests,
        ruff_errors=ruff_errors, roadmap=roadmap,
        active_guardrails=guardrails, signatures=signatures,
        test_skeleton=skeleton, new_files=new_files,
        modified_files=modified, test_delta=delta,
    )

    print("\n" + "─"*40)
    print("PACKET (paste as first message to Claude Code):")
    print("─"*40)
    print(packet)

    brief_file = ROOT / f".session_brief_{session_id.lower()}.txt"
    brief_file.write_text(packet)
    print(f"\n  Saved: {brief_file.name}")
    print(f"  Copy:  pbcopy < {brief_file.name}")


if __name__ == "__main__":
    main()
