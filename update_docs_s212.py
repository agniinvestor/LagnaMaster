"""update_docs_s212.py — S212 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S212 — 2026-03-28 — Ayanamsha Selection + KP G06 Compliance\n\n"
     "**Tests:** 1660 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/calculations/kp_ayanamsha.py`: `KP_AYANAMSHA` constant, `get_kp_ayanamsha()`,\n"
     "  `validate_kp_chart()` (returns g06_compliant bool + warning), `compute_kp_chart()`\n"
     "  wrapper that defaults to krishnamurti ayanamsha.\n"
     "- `GUARDRAILS.md`: G06 updated to 🟡 — enforcement mechanism in place;\n"
     "  existing charts not retroactively fixed (would require data migration).\n\n"
     "### G06 status\n"
     "New KP analysis using `compute_kp_chart()` is compliant. Existing charts "
     "stored with Lahiri ayanamsha must be flagged separately (Phase 1 data migration).\n\n"
     "### Next session\nS213 — Protocol verification + CI observability\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1651 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1660 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–211 complete",
     "## Actual Current State (Sessions 1–212 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S212",
     "- **Session 212:** KP ayanamsha enforcement (G06 🟡); compute_kp_chart(); 1660 tests\n- **Next session:** S213"),
    (ROOT/"docs/ROADMAP.md",
     "| S212 | Ayanamsha selection + KP school fix (G06 compliance) | G06 | 🔴 |",
     "| S212 | Ayanamsha selection + KP school fix (G06 compliance) | G06 | ✅ |"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S212" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S212")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
