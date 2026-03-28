"""update_docs_s231.py — S231 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S231 — 2026-03-28 — BPHS Graha in Rashis Part 3\n\n"
     "**Tests:** 1811 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_rashis_p3.py`: 24 rules — Jupiter in 12 rashis (JUR001-JUR012) + "
     "Venus in 12 rashis (VER001-VER012). BPHS Ch.21-22. "
     "Jupiter: own Sagittarius+Pisces, exalt Cancer, neecha Capricorn. "
     "Venus: own Taurus+Libra, exalt Pisces, neecha Virgo.\n\n"
     "**Corpus total: 506 rules**\n\n"
     "### Next session\nS232 — BPHS graha in rashis part 4 (Saturn + Rahu + Ketu)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1799 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1811 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–230 complete",
     "## Actual Current State (Sessions 1–231 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 230:** Graha in rashis p2 — Mars+Mercury in 12 rashis; 24 rules; corpus 482; 1799 tests\n"
     "- **Next session:** S231",
     "- **Session 230:** Graha in rashis p2 — Mars+Mercury in 12 rashis; 24 rules; corpus 482; 1799 tests\n"
     "- **Session 231:** Graha in rashis p3 — Jupiter+Venus in 12 rashis; 24 rules; corpus 506; 1811 tests\n"
     "- **Next session:** S232"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S231" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S231")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
