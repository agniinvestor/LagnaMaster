"""update_docs_s230.py — S230 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S230 — 2026-03-28 — BPHS Graha in Rashis Part 2\n\n"
     "**Tests:** 1799 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_rashis_p2.py`: 24 rules — Mars in 12 rashis (MAR001-MAR012) + "
     "Mercury in 12 rashis (BUR001-BUR012). BPHS Ch.19-20. "
     "Mars own-sign Aries+Scorpio, exaltation Capricorn, debilitation Cancer. "
     "Mercury own-sign+exaltation Virgo, moolatrikona Gemini, debilitation Sagittarius.\n\n"
     "**Corpus total: 482 rules**\n\n"
     "### Next session\nS231 — BPHS graha in rashis part 3 (Jupiter + Venus)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1788 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1799 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–229 complete",
     "## Actual Current State (Sessions 1–230 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 229:** Graha in rashis p1 — Sun+Moon in 12 rashis; 24 rules; corpus 458; 1788 tests\n"
     "- **Next session:** S230",
     "- **Session 229:** Graha in rashis p1 — Sun+Moon in 12 rashis; 24 rules; corpus 458; 1788 tests\n"
     "- **Session 230:** Graha in rashis p2 — Mars+Mercury in 12 rashis; 24 rules; corpus 482; 1799 tests\n"
     "- **Next session:** S231"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S230" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S230")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
