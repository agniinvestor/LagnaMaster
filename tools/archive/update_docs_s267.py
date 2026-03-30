"""update_docs_s267.py — S267 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S267 — 2026-03-30 — Bhavartha Ratnakara Part 1: Aries + Taurus\n\n"
     "**Tests:** 2309 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections A (Aries) + B (Taurus) — 130 rules (BVR001-BVR130):\n\n"
     "- `src/corpus/bhavartha_ratnakara_1.py`: One registry (BHAVARTHA_RATNAKARA_1_REGISTRY):\n"
     "  - Section A (Aries, 65 rules BVR001-BVR065): Sun (8), Moon (6), Mars (9), "
     "Mercury (6), Jupiter (7), Venus (8), Saturn (6), yogas (11). "
     "Lagna-conditional with lagna_scope=['aries'] on all rules.\n"
     "  - Section B (Taurus, 65 rules BVR066-BVR130): Sun (5), Moon (4), Mars (6), "
     "Mercury (8), Jupiter (6), Venus (7), Saturn (9), yogas (10). "
     "Lagna-conditional with lagna_scope=['taurus'] on all rules.\n"
     "- All 7 classical planets covered for both lagnas.\n"
     "- phase=1B_conditional, source=BhavarthaRatnakara, school=parashari on every rule.\n\n"
     "**Corpus:** 3037 rules (2907 + 130)\n\n"
     "### Next session\nS268 — Bhavartha Ratnakara Part 2: Gemini + Cancer "
     "(~130 rules, BVR131-BVR260)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 266:** Laghu Parashari Sections E, F (complete) — LPA001-060 + "
     "LPM001-024; LP coverage map done; corpus 2907; 2295 tests\n"
     "- **Next session:** S267",
     "- **Session 266:** Laghu Parashari Sections E, F (complete) — LPA001-060 + "
     "LPM001-024; LP coverage map done; corpus 2907; 2295 tests\n"
     "- **Session 267:** Bhavartha Ratnakara Aries + Taurus — BVR001-130; "
     "corpus 3037; 2309 tests\n"
     "- **Next session:** S268"),
    (ROOT / "docs/MEMORY.md",
     "- **2295 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2309 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S267" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S267")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections A, B
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| A | Aries (Mesha) | 65 | S267 | 🔲 |",
     "| A | Aries (Mesha) | 65 | S267 | ✅ |"),
    ("| B | Taurus (Vrishabha) | 65 | S267 | 🔲 |",
     "| B | Taurus (Vrishabha) | 65 | S267 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **0/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **130/780** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:40]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:50]}'")

cmap.write_text(cmap_text)
print("done")
