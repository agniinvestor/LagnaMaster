"""update_docs_s255.py — S255 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S255 — 2026-03-29 — Brihat Jataka Exhaustive (120 rules)\n\n"
     "**Tests:** 2075 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `brihat_jataka_exhaustive.py`: 120 rules (BJX001-BJX120) — "
     "Exhaustive encoding of all 25 chapters of Varahamihira's Brihat Jataka (6th century CE): "
     "Planet natures/colors/tastes, aspect rules (7th/3rd/10th/4th/8th/5th/9th), "
     "all 12 rashi characteristics, bhava significations in BJ system, "
     "Avastha planetary states (5 states + 9 avasthas), "
     "divisional charts D2/D3/D7/D9/D10/D12/D30, "
     "Pancha Mahapurusha/Raja/Dhana/Nabhasa/Pravrajya yogas, "
     "nakshatra characteristics (Ashwini to Revati + Abhijit), "
     "planets in signs/houses, birth analysis, physical traits, "
     "wealth rules, female horoscopy, Pindayu/Amsayu longevity, "
     "death indicators, dasha phala, transit rules (Sade Sati/Jupiter transit). "
     "All rules: school=varahamihira, source=BrihatJataka.\n\n"
     "**Corpus total: 1674 rules**\n\n"
     "### Next session\nS256 — Uttara Kalamrita Exhaustive (all chapters deep encoding)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2057 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2075 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–254 complete",
     "## Actual Current State (Sessions 1–255 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 254:** BPHS Graha Characteristics — Ch.3-10, all 9 planets complete (GCH001-100); 100 rules; corpus 1554; 2057 tests\n"
     "- **Next session:** S255",
     "- **Session 254:** BPHS Graha Characteristics — Ch.3-10, all 9 planets complete (GCH001-100); 100 rules; corpus 1554; 2057 tests\n"
     "- **Session 255:** Brihat Jataka Exhaustive — all 25 chapters (BJX001-120); 120 rules; corpus 1674; 2075 tests\n"
     "- **Next session:** S256"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S255" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S255")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
