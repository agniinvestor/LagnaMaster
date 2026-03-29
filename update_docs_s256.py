"""update_docs_s256.py — S256 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S256 — 2026-03-29 — Uttara Kalamrita Exhaustive (150 rules)\n\n"
     "**Tests:** 2098 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `uttara_kalamrita_exhaustive.py`: 150 rules (UKX001-UKX150) — "
     "Exhaustive encoding of Kalidasa's Uttara Kalamrita (17th century CE): "
     "All 7 special lagnas (Hora/Ghati/Bhava/Sree/Pranapada/Indu/Yogi), "
     "Argala doctrine (primary/secondary/obstruction), "
     "all 12 Arudha Padas (A1-A12 including UL/Upapada), "
     "extended house significations (all 12 houses), "
     "planet karakatva for all 9 planets, "
     "Upagrahas (Dhuma/Vyatipata/Parivesha/Indrachapa/Gulika/Mrityu), "
     "dasha timing (exalted/debilitated/retrograde dashas), "
     "Karakamsha and Atmakaraka analysis, "
     "Chara Karakas (AK/AMK/BK/DK), "
     "yogas (Subhakartari/Papakartari/Adhi/Kemadruma/Shakata/Parivartana), "
     "medical astrology, wealth/poverty combinations, marriage/divorce indicators, "
     "moksha/Pravrajya yogas, Prashna (horary), transit rules, varga analysis. "
     "All rules: school=kalidasa, source=UttaraKalamrita.\n\n"
     "**Corpus total: 1824 rules**\n\n"
     "### Next session\nS257 — Jataka Parijata Exhaustive (all chapters deep encoding)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2075 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2098 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–255 complete",
     "## Actual Current State (Sessions 1–256 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 255:** Brihat Jataka Exhaustive — all 25 chapters (BJX001-120); 120 rules; corpus 1674; 2075 tests\n"
     "- **Next session:** S256",
     "- **Session 255:** Brihat Jataka Exhaustive — all 25 chapters (BJX001-120); 120 rules; corpus 1674; 2075 tests\n"
     "- **Session 256:** Uttara Kalamrita Exhaustive — all doctrines (UKX001-150); 150 rules; corpus 1824; 2098 tests\n"
     "- **Next session:** S257"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S256" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S256")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
