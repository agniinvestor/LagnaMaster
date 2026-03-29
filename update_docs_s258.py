"""update_docs_s258.py — S258 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S258 — 2026-03-29 — Sarvartha Chintamani Exhaustive (150 rules)\n\n"
     "**Tests:** 2141 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `sarvartha_chintamani_exhaustive.py`: 150 rules (SCX001-SCX150) — "
     "Exhaustive encoding of Venkatesha Daivagna's Sarvartha Chintamani (16th century CE): "
     "All 12 lagna results (SCX005-016), house significations (all 12 houses), "
     "3-tier Raja Yoga grading (Maha/Madhyama/Alpa), Dhana Yoga Chakra, "
     "Neecha Bhanga Raja Yoga, Parivartana (66 combos), fame yogas, "
     "longevity (3 pillars, death timing, cause), children, marriage (5-factor), "
     "education, career (by dominant planet), Wealth Trikona (2/6/10 lords), "
     "travel directions, medical (Ayurvedic constitution), dasha timing, "
     "transit (Sade Sati 3 phases, Ashtakavarga), moksha paths, "
     "Shodasavarga grading (Para/Uttama/Madhyama), functional planet system, "
     "Gaja Kesari conditions, Marana Karaka Sthana, Mahabhagya, "
     "Dharmakarmadhipati (SCX118), three-chart synthesis (SCX150), Varshaphala.\n\n"
     "**Corpus total: 2124 rules**\n\n"
     "### Next session\nS259 — Jaimini Sutras Exhaustive (deep encoding)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2121 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2141 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–257 complete",
     "## Actual Current State (Sessions 1–258 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 257:** Jataka Parijata Exhaustive — all 18 chapters (JPX001-150); 150 rules; corpus 1974; 2121 tests\n"
     "- **Next session:** S258",
     "- **Session 257:** Jataka Parijata Exhaustive — all 18 chapters (JPX001-150); 150 rules; corpus 1974; 2121 tests\n"
     "- **Session 258:** Sarvartha Chintamani Exhaustive — all chapters (SCX001-150); 150 rules; corpus 2124; 2141 tests\n"
     "- **Next session:** S259"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S258" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S258")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
