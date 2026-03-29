"""update_docs_s213.py — S213-S215 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S213–S215 — 2026-03-28 — Protocol Verification + CI Observability + Phase 0 Checkpoint\n\n"
     "**Tests:** 1722 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/ci/protocol_compliance.py`: `check_all_protocols()` — runtime isinstance checks\n"
     "  for all four Protocol adapters (ClassicalEngine, DashaEngine, FeedbackService, MLService).\n"
     "- `src/ci/health_check.py`: `CIHealthReport` dataclass + `run_health_check()` — structured\n"
     "  CI observability with corpus count, G06/G17 guardrail status, Phase 0 module presence.\n"
     "- `src/ci/phase0_checkpoint.py`: `Phase0Checkpoint` + `run_phase0_audit()` — comprehensive\n"
     "  audit of all 25 Phase 0 sessions (S191–S215); serves as Phase 0 gate.\n\n"
     "### Phase 0 gate status\n"
     "All 25 Phase 0 sessions (S191–S215) verified complete. `run_phase0_audit()` returns\n"
     "25/25 sessions complete. CI health check passes. Phase 1 (S216) can begin.\n\n"
     "### Next session\nS216 — BPHS all 97 chapters AI-assisted encoding (Phase 1 start)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1660 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1722 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–212 complete",
     "## Actual Current State (Sessions 1–215 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 212:** KP ayanamsha enforcement (G06 🟡); compute_kp_chart(); 1660 tests\n- **Next session:** S213",
     "- **Session 212:** KP ayanamsha enforcement (G06 🟡); compute_kp_chart(); 1660 tests\n"
     "- **Sessions 213–215:** Protocol verification + CI observability + Phase 0 checkpoint; "
     "src/ci/ package; 1722 tests\n- **Next session:** S216"),
    (ROOT/"docs/ROADMAP.md",
     "| S213–S215 | Protocol verification + CI observability + Phase 0 checkpoint | All Phase 0 | 🔴 |",
     "| S213–S215 | Protocol verification + CI observability + Phase 0 checkpoint | All Phase 0 | ✅ |"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S213" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S213")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
