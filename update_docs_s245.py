"""update_docs_s245.py — S245 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S245 — 2026-03-28 — Shadbala Rules\n\n"
     "**Tests:** 1947 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `shadbala_rules.py`: 30 rules (SDB001-SDB030) — "
     "Classical Shadbala 6-fold strength system from BPHS Ch.27-38 (parashari), "
     "Brihat Jataka Ch.1 (varahamihira), Sarvartha Chintamani Ch.2 (sarvartha): "
     "Sthana Bala (Uchcha/Sapta-Vargaja/Ojayugma/Kendradi/Drekkana), "
     "Dig Bala (directional), Kala Bala (Paksha/Tribhaga/Vara/Ayana/Yuddha), "
     "Chesta Bala (retrograde=60), Naisargika Bala (fixed values), "
     "Drik Bala (aspectual), Ishta/Kashta Phala, Vimshopaka (5/7/10-Varga), "
     "minimum thresholds, Dasha applications.\n\n"
     "**Corpus total: 926 rules**\n\n"
     "### Next session\nS246 — Dasha systems (Vimshotari, Ashtottari, Yogini)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1936 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1947 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–244 complete",
     "## Actual Current State (Sessions 1–245 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 244:** Jaimini Sutras + Upagrahas — Chara Karakas/Rashi Drishti/Arudha/Chara Dasha/Gulika; 30 rules; corpus 896; 1936 tests\n"
     "- **Next session:** S245",
     "- **Session 244:** Jaimini Sutras + Upagrahas — Chara Karakas/Rashi Drishti/Arudha/Chara Dasha/Gulika; 30 rules; corpus 896; 1936 tests\n"
     "- **Session 245:** Shadbala rules — 6-fold strength/Sthana/Dig/Kala/Chesta/Naisargika/Drik; 30 rules; corpus 926; 1947 tests\n"
     "- **Next session:** S246"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S245" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S245")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
