"""update_docs_s254.py — S254 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S254 — 2026-03-29 — BPHS Graha Characteristics (100 rules)\n\n"
     "**Tests:** 2057 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_characteristics.py`: 100 rules (GCH001-GCH100) — "
     "Exhaustive encoding of all 9 planet natures/attributes from BPHS Ch.3-10: "
     "Nature/element/dosha/body for all 7 planets + Rahu/Ketu, "
     "full karakatva (significator roles), exaltation/debilitation/own signs, "
     "special aspects (Mars 4/8, Jupiter 5/9, Saturn 3/10), combustion degrees, "
     "Graha Yuddha (planetary war), rising types (Sheershodaya/Prishtodaya/Ubhayodaya), "
     "Vimshottari dasha periods + nakshatra sequence, Rashi modality/elements/gender, "
     "Nakshatra trikonas + ganas, temporal friendship rules, Saptavarga/Vargottama, "
     "retrograde/stationary states, medical astrology (8 planets), "
     "gems/metals/mantras for all 9 planets, planetary cabinet, objects, tastes, deities, "
     "maturation ages, seasonal/hourly strengths.\n\n"
     "**Corpus total: 1554 rules**\n\n"
     "### Next session\nS255 — Brihat Jataka Exhaustive (all 25 chapters deep encoding)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2042 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2057 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–253 complete",
     "## Actual Current State (Sessions 1–254 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 253:** BPHS Bhava Exhaustive — Ch.11-22, all 12 houses deep (BVX001-120); 120 rules; corpus 1454; 2042 tests\n"
     "- **Next session:** S254",
     "- **Session 253:** BPHS Bhava Exhaustive — Ch.11-22, all 12 houses deep (BVX001-120); 120 rules; corpus 1454; 2042 tests\n"
     "- **Session 254:** BPHS Graha Characteristics — Ch.3-10, all 9 planets complete (GCH001-100); 100 rules; corpus 1554; 2057 tests\n"
     "- **Next session:** S255"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S254" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S254")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
