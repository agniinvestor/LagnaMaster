"""update_docs_s275.py — S275 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S275 — 2026-03-30 — Saravali Conjunctions Part 3: Moon-Mars, Moon-Mercury, Moon-Jupiter\n\n"
     "**Tests:** 2413 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_3.py`: SARAVALI_CONJUNCTIONS_3_REGISTRY (130 rules SAV261-SAV390)\n"
     "  - Moon-Mars (Ch.17-18, 43 rules): Chandra-Mangal yoga, emotional courage/volatility\n"
     "  - Moon-Mercury (Ch.18, 43 rules): eloquent speech, commercial mind, writing\n"
     "  - Moon-Jupiter (Ch.18-19, 44 rules): Gajakesari variant, wisdom-wealth expansion\n\n"
     "**Corpus:** 4077 rules (3947 + 130)\n\n"
     "### Next session\nS276 — Saravali Conjunctions Part 4: Moon-Venus, Moon-Saturn, Mars-Mercury\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 274:** Saravali Conjunctions 2 (Sun-Jupiter/Venus/Saturn) — SAV131-260; "
     "corpus 3947; 2403 tests\n"
     "- **Next session:** S275",
     "- **Session 274:** Saravali Conjunctions 2 (Sun-Jupiter/Venus/Saturn) — SAV131-260; "
     "corpus 3947; 2403 tests\n"
     "- **Session 275:** Saravali Conjunctions 3 (Moon-Mars/Mercury/Jupiter) — SAV261-390; "
     "corpus 4077; 2413 tests\n"
     "- **Next session:** S276"),
    (ROOT / "docs/MEMORY.md",
     "- **2403 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2413 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S275" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S275")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

cmap = ROOT / "docs/coverage_maps/saravali.md"
cmap_text = cmap.read_text()
for old_line, new_line in [
    ("| A3 | Ch.17–18 | Moon-Mars, Moon-Mercury, Moon-Jupiter conjunctions | ~130 | S275 | 🔲 |",
     "| A3 | Ch.17–18 | Moon-Mars, Moon-Mercury, Moon-Jupiter conjunctions | ~130 | S275 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **260/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **390/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **260/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **390/4100** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
cmap.write_text(cmap_text)
print("done")
