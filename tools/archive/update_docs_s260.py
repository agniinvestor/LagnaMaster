"""update_docs_s260.py — S260 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S260 — 2026-03-29 — Lal Kitab Exhaustive (120 rules)\n\n"
     "**Tests:** 2185 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `lal_kitab_rules.py`: 120 rules (LKX001-LKX120) — "
     "Exhaustive encoding of Pt. Roop Chand Joshi's Lal Kitab (1939-1952 editions): "
     "Pakka Ghar (permanent house) for all 9 planets, "
     "Andha (blind) planet system for all planets in enemy houses, "
     "7-type Karmic Debt (Rin) system — Pitru/Matru/Bhai/Stri/Santan/Rajya/Swaya Rin, "
     "planets in all 12 houses with LK-unique interpretations, "
     "complete remedy system (totkas, Chaliha, water/tree/food/animal remedies), "
     "special combinations (Guru-Chandal, Vish Yoga, Raj-Guru Yoga, Mahavir Yoga), "
     "empty house (Khali Ghar) and sleeping planet (Suta Grah) concepts, "
     "Kachcha-Pakka distinction, age-based activation system, "
     "body-house correspondence, directional strength equivalent, "
     "LK number system, color system, philosophy of remedies.\n\n"
     "**Corpus total: 2394 rules**\n\n"
     "### Next session\nS261 — Chandra Kala Nadi Encoding (~120 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2166 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2185 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–259 complete",
     "## Actual Current State (Sessions 1–260 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 259:** Jaimini Sutras Exhaustive — 4 Adhyayas (JMX001-150); 150 rules; corpus 2274; 2166 tests\n"
     "- **Next session:** S260",
     "- **Session 259:** Jaimini Sutras Exhaustive — 4 Adhyayas (JMX001-150); 150 rules; corpus 2274; 2166 tests\n"
     "- **Session 260:** Lal Kitab Exhaustive — 1939-1952 editions (LKX001-120); 120 rules; corpus 2394; 2185 tests\n"
     "- **Next session:** S261"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S260" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S260")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
