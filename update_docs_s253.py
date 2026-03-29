"""update_docs_s253.py — S253 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S253 — 2026-03-29 — BPHS Bhava Exhaustive (120 rules)\n\n"
     "**Tests:** 2042 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_bhava_exhaustive.py`: 120 rules (BVX001-BVX120) — "
     "Exhaustive encoding of all 12 bhava significations from BPHS Ch.11-22: "
     "Each house primary significations + karakas, all 9 planets in each house, "
     "Marana Karaka Sthana placements, Dig Bala, Bhavat Bhavam principle, "
     "house anatomy/body mapping, longevity classification (Alpayu/Madhyayu/Purnayu), "
     "Maraka analysis, lagna lord in dusthanas, cross-house lord interactions.\n\n"
     "**Corpus total: 1454 rules**\n\n"
     "### Next session\nS254 — BPHS Graha Characteristics Exhaustive (planet natures, elements, karakas)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2028 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2042 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–252 complete",
     "## Actual Current State (Sessions 1–253 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 252:** BPHS Yoga Exhaustive — Ch.35-56, all yoga classes (YEX001-150); 150 rules; corpus 1334; 2028 tests\n"
     "- **Next session:** S253",
     "- **Session 252:** BPHS Yoga Exhaustive — Ch.35-56, all yoga classes (YEX001-150); 150 rules; corpus 1334; 2028 tests\n"
     "- **Session 253:** BPHS Bhava Exhaustive — Ch.11-22, all 12 houses deep (BVX001-120); 120 rules; corpus 1454; 2042 tests\n"
     "- **Next session:** S254"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S253" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S253")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
