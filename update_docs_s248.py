"""update_docs_s248.py — S248 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S248 — 2026-03-28 — Lagna Extended Rules\n\n"
     "**Tests:** 1979 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `lagna_extended_rules.py`: 30 rules (LGE001-LGE030) — "
     "All 12 Lagna (Ascendant) characteristics from BPHS Ch.7-18 (parashari), "
     "Phala Deepika Ch.1 (mantreswara), Brihat Jataka Ch.1 (varahamihira): "
     "All 12 lagna personality/body/planet profiles, Yogakaraka by element group "
     "(fire/earth/air/water), Kendra Adhipati Dosha, Trikona Adhipati Shubha, "
     "Chandra Lagna, Surya Lagna, lagna strength indicators, lagna lord in 12 houses, "
     "planets in lagna, physical characteristics, Vargottama Lagna, "
     "8th lord in lagna, multiple planets in lagna.\n\n"
     "**Corpus total: 1016 rules — 1000+ MILESTONE ACHIEVED!**\n\n"
     "### Next session\nS249 — House significations extended (Bhava Phala)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1969 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1979 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–247 complete",
     "## Actual Current State (Sessions 1–248 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 247:** Extended yoga rules — Pancha Mahapurusha/Nabhasa/Viparita/Moon yogas/Kartari; 30 rules; corpus 986; 1969 tests\n"
     "- **Next session:** S248",
     "- **Session 247:** Extended yoga rules — Pancha Mahapurusha/Nabhasa/Viparita/Moon yogas/Kartari; 30 rules; corpus 986; 1969 tests\n"
     "- **Session 248:** Lagna extended — all 12 lagna profiles/Yogakaraka/Kendra Adhipati/Vargottama; 30 rules; corpus 1016; 1979 tests ✅ 1000+ MILESTONE\n"
     "- **Next session:** S249"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S248" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S248")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
