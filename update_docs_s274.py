"""update_docs_s274.py — S274 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S274 — 2026-03-30 — Saravali Conjunctions Part 2: Sun-Jupiter, Sun-Venus, Sun-Saturn\n\n"
     "**Tests:** 2403 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_2.py`: SARAVALI_CONJUNCTIONS_2_REGISTRY (130 rules SAV131-SAV260)\n"
     "  - Sun-Jupiter (Ch.16-17, 43 rules): Guru-Aditya yoga, combust Jupiter\n"
     "  - Sun-Venus (Ch.17, 43 rules): combust Venus marriage effects, artistic tension\n"
     "  - Sun-Saturn (Ch.17-18, 44 rules): karmic conjunction, father-son conflict, delays\n\n"
     "**Corpus:** 3947 rules (3817 + 130)\n\n"
     "### Next session\nS275 — Saravali Conjunctions Part 3: Moon-Mars, Moon-Mercury, Moon-Jupiter\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 273:** Saravali Conjunctions 1 (Sun-Moon/Mars/Mercury) — SAV001-130; "
     "corpus 3817; 2393 tests\n"
     "- **Next session:** S274",
     "- **Session 273:** Saravali Conjunctions 1 (Sun-Moon/Mars/Mercury) — SAV001-130; "
     "corpus 3817; 2393 tests\n"
     "- **Session 274:** Saravali Conjunctions 2 (Sun-Jupiter/Venus/Saturn) — SAV131-260; "
     "corpus 3947; 2403 tests\n"
     "- **Next session:** S275"),
    (ROOT / "docs/MEMORY.md",
     "- **2393 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2403 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S274" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S274")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

cmap = ROOT / "docs/coverage_maps/saravali.md"
cmap_text = cmap.read_text()
for old_line, new_line in [
    ("| A2 | Ch.16–17 | Sun-Jupiter, Sun-Venus, Sun-Saturn conjunctions | ~130 | S274 | 🔲 |",
     "| A2 | Ch.16–17 | Sun-Jupiter, Sun-Venus, Sun-Saturn conjunctions | ~130 | S274 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **130/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **260/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **130/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **260/4100** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
cmap.write_text(cmap_text)
print("done")
