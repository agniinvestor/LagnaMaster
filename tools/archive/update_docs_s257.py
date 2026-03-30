"""update_docs_s257.py — S257 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S257 — 2026-03-29 — Jataka Parijata Exhaustive (150 rules)\n\n"
     "**Tests:** 2121 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `jataka_parijata_exhaustive.py`: 150 rules (JPX001-JPX150) — "
     "Exhaustive encoding of Vaidyanatha Dikshita's Jataka Parijata (14th century CE): "
     "All 9 planet natures (element/dosha/taste/color/direction), all 12 rashi characteristics, "
     "complete dignity system (exaltation/Moolatrikona/Vargottama/combustion/retrograde), "
     "Dig Bala for all 7 planets, Shadbala 6-component system, "
     "house analysis (all 12 houses with planet placements), "
     "Raja Yoga (kendra-trikona, Yoga Karaka, lagna-specific), "
     "Pancha Mahapurusha, Viparita Raja Yoga (Harsha/Sarala/Vimala), "
     "Nabhasa Yogas, Dhana/Daridra Yogas, Lakshmi/Saraswati Yogas, "
     "Parijata Yoga (namesake), Brahma/Vishnu/Shiva Yogas, "
     "longevity (Alpayu/Madhyayu/Purnayu, Maraka, Balarishta), "
     "marriage (three pillars, Mangal Dosha, timing), children, travel, "
     "female charts, medical (Tridosha, disease), dasha timing, transits, "
     "varga charts (D2/D3/D7/D9/D10/D12/D30/D60), muhurta.\n\n"
     "**Corpus total: 1974 rules**\n\n"
     "### Next session\nS258 — Sarvartha Chintamani Exhaustive (all chapters deep encoding)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2098 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2121 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–256 complete",
     "## Actual Current State (Sessions 1–257 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 256:** Uttara Kalamrita Exhaustive — all doctrines (UKX001-150); 150 rules; corpus 1824; 2098 tests\n"
     "- **Next session:** S257",
     "- **Session 256:** Uttara Kalamrita Exhaustive — all doctrines (UKX001-150); 150 rules; corpus 1824; 2098 tests\n"
     "- **Session 257:** Jataka Parijata Exhaustive — all 18 chapters (JPX001-150); 150 rules; corpus 1974; 2121 tests\n"
     "- **Next session:** S258"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S257" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S257")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
