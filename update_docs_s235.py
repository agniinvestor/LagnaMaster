"""update_docs_s235.py — S235 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S235 — 2026-03-28 — BPHS Nakshatra Rules Part 2\n\n"
     "**Tests:** 1851 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_nakshatra_rules_p2.py`: 26 rules (NAK029-NAK054) — "
     "Nakshatras 15-27 (Swati through Revati): characteristics (13 rules) + "
     "Moon in nakshatras 15-27 (13 rules). BPHS Ch.5. "
     "Completes full 27-nakshatra catalog (54 characteristic rules + 54 Moon rules).\n\n"
     "**Corpus total: 626 rules**\n\n"
     "### Next session\nS236 — BPHS Bhava Karakas (house significators)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1843 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1851 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–234 complete",
     "## Actual Current State (Sessions 1–235 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 234:** Nakshatra rules p1 — nakshatras 1-14 + Moon; 28 rules; corpus 600; 1843 tests\n"
     "- **Next session:** S235",
     "- **Session 234:** Nakshatra rules p1 — nakshatras 1-14 + Moon; 28 rules; corpus 600; 1843 tests\n"
     "- **Session 235:** Nakshatra rules p2 — nakshatras 15-27 + Moon; 26 rules; corpus 626; 1851 tests\n"
     "- **Next session:** S236"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S235" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S235")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
