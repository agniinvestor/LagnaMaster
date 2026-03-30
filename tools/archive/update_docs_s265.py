"""update_docs_s265.py — S265 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S265 — 2026-03-30 — Laghu Parashari Sections B, C, D\n\n"
     "**Tests:** 2270 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Sections B, C, D of the Laghu Parashari coverage map — 81 rules (LPY001-LPY012, "
     "LPK001-LPK024, LPD001-LPD045):\n\n"
     "- `src/corpus/laghu_parashari_bcd.py`: Three registries:\n"
     "  - Section B (Yogakaraka): 12 rules — one per lagna, 6 yogakaraka + 6 no_yogakaraka. "
     "Yogakarakas: Taurus=Saturn, Cancer=Mars, Leo=Mars, Libra=Saturn, Capricorn=Venus, "
     "Aquarius=Venus.\n"
     "  - Section C (Kendradhipati): 24 rules — full KD dosha, maraka+KD overlap, "
     "lagna lord partial cases, trikona-exempt cases. Phase 1B_conditional.\n"
     "  - Section D (Dasha Results): 45 rules — 12 base house-lord dashas + 33 "
     "special category rules (trikona/kendra enhancements, yogakaraka, maraka, badhaka, "
     "upachaya, dignity modifiers, combo lordships). Phase 1B_matrix.\n\n"
     "**Corpus:** 2823 rules (2742 + 81)\n\n"
     "### Next session\nS266 — Laghu Parashari Sections E, F: "
     "Antardasha combinations (~60 rules) + Maraka by lagna (~24 rules)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 264:** Laghu Parashari Functional Nature Table — LPF001-108 (9×12); "
     "Phase 1B conditional; 6 yogakarakas; corpus 2742; 2250 tests\n"
     "- **Next session:** S265",
     "- **Session 264:** Laghu Parashari Functional Nature Table — LPF001-108 (9×12); "
     "Phase 1B conditional; 6 yogakarakas; corpus 2742; 2250 tests\n"
     "- **Session 265:** Laghu Parashari Sections B, C, D — LPY001-012 + LPK001-024 + "
     "LPD001-045; corpus 2823; 2270 tests\n"
     "- **Next session:** S266"),
    (ROOT / "docs/MEMORY.md",
     "- **2250 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2270 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S265" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S265")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections B, C, D
cmap = ROOT / "docs/coverage_maps/laghu_parashari.md"
cmap_text = cmap.read_text()
for old_line, new_line in [
    ("| B | Yogakaraka Designations | 12 | 🔲 |",
     "| B | Yogakaraka Designations | 12 | ✅ S265 |"),
    ("| C | Kendradhipati Dosha | 20 | 🔲 |",
     "| C | Kendradhipati Dosha | 20 | ✅ S265 |"),
    ("| D | Dasha Results by Lordship | 42 | 🔲 |",
     "| D | Dasha Results by Lordship | 42 | ✅ S265 |"),
    ("| **TOTAL** | | **266** | **108/266** |",
     "| **TOTAL** | | **266** | **189/266** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:30]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:40]}'")
cmap.write_text(cmap_text)

print("done")
