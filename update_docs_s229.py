"""update_docs_s229.py — S229 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S229 — 2026-03-28 — BPHS Graha in Rashis Part 1\n\n"
     "**Tests:** 1788 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_rashis_p1.py`: 24 rules — Sun in 12 rashis (SUR001-SUR012) + "
     "Moon in 12 rashis (MOR001-MOR012). Encodes BPHS Ch.17-18 graha-rashi phala. "
     "Exaltation/own/debilitation tags on key placements.\n\n"
     "**Corpus total: 458 rules**\n\n"
     "### Next session\nS230 — BPHS graha in rashis part 2 (Mars + Mercury)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1777 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1788 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–228 complete",
     "## Actual Current State (Sessions 1–229 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Sessions 216–228:** Phase 1 Batch 1 — 299 new BPHS rules encoded (lords-in-houses "
     "144, yogas 75, dignities/aspects/dasha/special-lagnas 80); corpus 135→434 rules; 1777 tests\n"
     "- **Next session:** S229",
     "- **Sessions 216–228:** Phase 1 Batch 1 — 299 new BPHS rules encoded (lords-in-houses "
     "144, yogas 75, dignities/aspects/dasha/special-lagnas 80); corpus 135→434 rules; 1777 tests\n"
     "- **Session 229:** Graha in rashis p1 — Sun+Moon in 12 rashis; 24 rules; corpus 458; 1788 tests\n"
     "- **Next session:** S230"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S229" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S229")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
