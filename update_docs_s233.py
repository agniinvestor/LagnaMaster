"""update_docs_s233.py — S233 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S233 — 2026-03-28 — KP Sublord System Rules\n\n"
     "**Tests:** 1833 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `kp_sublord_rules.py`: 30 rules (KPS001-KPS030) — KP Sublord system from "
     "K.S. Krishnamurti's Reader Vol.1-6. Covers: nakshatra sublord structure (6), "
     "marriage (4), finance (4), career (4), health (4), education/travel/spirituality (4), "
     "horary/prashna (4).\n\n"
     "**Corpus total: 572 rules**\n\n"
     "### Next session\nS234 — BPHS nakshatra-based rules (nakshatras 1-9)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1823 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1833 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–232 complete",
     "## Actual Current State (Sessions 1–233 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 232:** Graha in rashis p4 — Saturn+Rahu+Ketu in 12 rashis; 36 rules; corpus 542; 1823 tests\n"
     "- **Next session:** S233",
     "- **Session 232:** Graha in rashis p4 — Saturn+Rahu+Ketu in 12 rashis; 36 rules; corpus 542; 1823 tests\n"
     "- **Session 233:** KP Sublord system — 30 rules (KPS001-030); corpus 572; 1833 tests\n"
     "- **Next session:** S234"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S233" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S233")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
