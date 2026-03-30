"""update_docs_s266.py — S266 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S266 — 2026-03-30 — Laghu Parashari Sections E, F + LP Complete\n\n"
     "**Tests:** 2295 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Sections E, F completing the Laghu Parashari coverage map — 84 rules "
     "(LPA001-LPA060, LPM001-LPM024):\n\n"
     "- `src/corpus/laghu_parashari_ef.py`: Two registries:\n"
     "  - Section E (Antardasha): 60 rules — key operative combinations of "
     "mahadasha lordship type × antardasha lordship type. Covers trikona, kendra, "
     "yogakaraka, lagna lord, dusthana, maraka, kendradhipati, badhaka, and 8th lord "
     "combinations. Phase 1B_matrix for generic; 1B_conditional for lagna-specific "
     "yogakaraka AD rules (6 lagnas).\n"
     "  - Section F (Maraka): 24 rules — H2 lord and H7 lord per lagna. "
     "Double maraka: Aries=Venus (H2+H7), Libra=Mars (H2+H7). Phase 1B_conditional.\n"
     "- Combined LP coverage: 273 rules across 6 sections (A-F). "
     "Coverage map complete for Laghu Parashari.\n\n"
     "**Corpus:** 2907 rules (2823 + 84)\n\n"
     "### Next session\nS267 — Bhavartha Ratnakara Part 1: Lagna-conditional results "
     "(1B_conditional, lagna_scope fully populated). Highest discrimination signal text.\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 265:** Laghu Parashari Sections B, C, D — LPY001-012 + LPK001-024 + "
     "LPD001-045; corpus 2823; 2270 tests\n"
     "- **Next session:** S266",
     "- **Session 265:** Laghu Parashari Sections B, C, D — LPY001-012 + LPK001-024 + "
     "LPD001-045; corpus 2823; 2270 tests\n"
     "- **Session 266:** Laghu Parashari Sections E, F (complete) — LPA001-060 + "
     "LPM001-024; LP coverage map done; corpus 2907; 2295 tests\n"
     "- **Next session:** S267"),
    (ROOT / "docs/MEMORY.md",
     "- **2270 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2295 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S266" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S266")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections E, F and totals
cmap = ROOT / "docs/coverage_maps/laghu_parashari.md"
cmap_text = cmap.read_text()

# Update status line at top
if "ENCODING NOT STARTED" in cmap_text:
    cmap_text = cmap_text.replace(
        "> **Status: ENCODING NOT STARTED** (target: S264–S266)",
        "> **Status: ✅ COMPLETE** — S264 (A), S265 (B, C, D), S266 (E, F)",
    )

for old_line, new_line in [
    ("| E | Antardasha Combinations | 60 | 🔲 |",
     "| E | Antardasha Combinations | 60 | ✅ S266 |"),
    ("| F | Maraka by Lagna | 24 | 🔲 |",
     "| F | Maraka by Lagna | 24 | ✅ S266 |"),
    ("| **TOTAL** | | **266** | **189/266** |",
     "| **TOTAL** | | **266** | **273/266** ✅ |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:35]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:45]}'")

cmap.write_text(cmap_text)
print("done")
