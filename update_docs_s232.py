"""update_docs_s232.py — S232 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S232 — 2026-03-28 — BPHS Graha in Rashis Part 4\n\n"
     "**Tests:** 1823 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_rashis_p4.py`: 36 rules — Saturn in 12 rashis (SAR001-SAR012) + "
     "Rahu in 12 rashis (RHR001-RHR012) + Ketu in 12 rashis (KTR001-KTR012). "
     "BPHS Ch.23, Ch.45-46. "
     "Saturn: own Capricorn+Aquarius, exalt Libra, neecha Aries. "
     "Rahu/Ketu: exaltation/debilitation per traditional commentary.\n\n"
     "**Corpus total: 542 rules** (108 graha-in-rashi rules complete for all 9 grahas)\n\n"
     "### Next session\nS233 — KP sublord rules + nakshatra lords\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1811 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1823 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–231 complete",
     "## Actual Current State (Sessions 1–232 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 231:** Graha in rashis p3 — Jupiter+Venus in 12 rashis; 24 rules; corpus 506; 1811 tests\n"
     "- **Next session:** S232",
     "- **Session 231:** Graha in rashis p3 — Jupiter+Venus in 12 rashis; 24 rules; corpus 506; 1811 tests\n"
     "- **Session 232:** Graha in rashis p4 — Saturn+Rahu+Ketu in 12 rashis; 36 rules; corpus 542; 1823 tests\n"
     "- **Next session:** S233"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S232" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S232")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
