"""update_docs_s234.py — S234 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S234 — 2026-03-28 — BPHS Nakshatra Rules Part 1\n\n"
     "**Tests:** 1843 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_nakshatra_rules_p1.py`: 28 rules (NAK001-NAK028) — "
     "Nakshatras 1-14 (Ashwini through Chitra): nature, deity, symbol, keywords (14 rules) + "
     "Moon in nakshatras 1-14 (14 rules). BPHS Ch.3-4.\n\n"
     "**Corpus total: 600 rules**\n\n"
     "### Next session\nS235 — BPHS nakshatra rules part 2 (nakshatras 15-27)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1833 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1843 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–233 complete",
     "## Actual Current State (Sessions 1–234 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 233:** KP Sublord system — 30 rules (KPS001-030); corpus 572; 1833 tests\n"
     "- **Next session:** S234",
     "- **Session 233:** KP Sublord system — 30 rules (KPS001-030); corpus 572; 1833 tests\n"
     "- **Session 234:** Nakshatra rules p1 — nakshatras 1-14 + Moon; 28 rules; corpus 600; 1843 tests\n"
     "- **Next session:** S235"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S234" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S234")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
