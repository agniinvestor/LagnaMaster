"""update_docs_s259.py — S259 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S259 — 2026-03-29 — Jaimini Sutras Exhaustive (150 rules)\n\n"
     "**Tests:** 2166 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `jaimini_sutras_exhaustive.py`: 150 rules (JMX001-JMX150) — "
     "Exhaustive encoding of Maharishi Jaimini's Jaimini Sutras (4 Adhyayas): "
     "Complete Chara Karaka system (AK/AMK/BK/PK/MK/GK/DK, 8-karaka system), "
     "Rashi Drishti complete table (movable/fixed/dual sign aspects, exception rule), "
     "Arudha/Pada system (AL, UL/Upapada, A2-A12, Darapada, Rajyapada), "
     "Chara Dasha (odd-sign forward, even-sign backward, year calculation), "
     "Sthira/Shoola Dasha (longevity analysis, Brahma/Rudra/Maheshvara), "
     "Karakamsha Lagna (all 12 houses from KL, all 9 planets in KL), "
     "Ishta Devata, Palana Devata, Atma Devata (spiritual planets), "
     "Jaimini Raja Yoga (AK-AMK, Karakamsha yogas, Chamara, Bandha, Daridra), "
     "Moksha Yoga and Kevalya/Kaivalya Yoga, Pravrajya (renunciation), "
     "Argala and Virodha-Argala, special lagnas (Hora/Ghati/Varnada), "
     "advanced timing (Narayana Dasha, Mandooka Dasha, 3-point verification), "
     "final synthesis (karma vs free will, Sampoorna Jyotisha teaching).\n\n"
     "**Corpus total: 2274 rules**\n\n"
     "### Next session\nS260 — Lal Kitab Encoding (~120 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2141 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2166 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–258 complete",
     "## Actual Current State (Sessions 1–259 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 258:** Sarvartha Chintamani Exhaustive — all chapters (SCX001-150); 150 rules; corpus 2124; 2141 tests\n"
     "- **Next session:** S259",
     "- **Session 258:** Sarvartha Chintamani Exhaustive — all chapters (SCX001-150); 150 rules; corpus 2124; 2141 tests\n"
     "- **Session 259:** Jaimini Sutras Exhaustive — 4 Adhyayas (JMX001-150); 150 rules; corpus 2274; 2166 tests\n"
     "- **Next session:** S260"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S259" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S259")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
