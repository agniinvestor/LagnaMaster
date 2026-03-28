"""update_docs_s246.py — S246 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S246 — 2026-03-28 — Dasha Systems Rules\n\n"
     "**Tests:** 1958 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `dasha_systems_rules.py`: 30 rules (DSY001-DSY030) — "
     "Classical Dasha systems from BPHS Ch.46-64 (parashari), "
     "Uttara Kalamrita Ch.4 (kalidasa), Sarvartha Chintamani Ch.8 (sarvartha), "
     "Jaimini Sutras (jaimini): Vimshottari extended (birth balance/Antardasha/results), "
     "Ashtottari (108yr), Yogini (36yr), Kalachakra (100yr), Shodashottari (116yr), "
     "Dwisaptati (72yr), conditional dasha selection, Narayana/Padakrama Jaimini dashas, "
     "Sookshma/Prana micro-dashas, transit confirmation, Maraka, yogakaraka dasha, "
     "Sun/Jupiter/Saturn/Rahu/Ketu Mahadasha results.\n\n"
     "**Corpus total: 956 rules**\n\n"
     "### Next session\nS247 — Yoga extended (Pancha Mahapurusha, Dhana, Raja yogas expansion)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1947 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1958 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–245 complete",
     "## Actual Current State (Sessions 1–246 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 245:** Shadbala rules — 6-fold strength/Sthana/Dig/Kala/Chesta/Naisargika/Drik; 30 rules; corpus 926; 1947 tests\n"
     "- **Next session:** S246",
     "- **Session 245:** Shadbala rules — 6-fold strength/Sthana/Dig/Kala/Chesta/Naisargika/Drik; 30 rules; corpus 926; 1947 tests\n"
     "- **Session 246:** Dasha systems — Vimshottari/Ashtottari/Yogini/Kalachakra/Maraka/planet results; 30 rules; corpus 956; 1958 tests\n"
     "- **Next session:** S247"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S246" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S246")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
