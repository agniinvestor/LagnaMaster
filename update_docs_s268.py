"""update_docs_s268.py — S268 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S268 — 2026-03-30 — Bhavartha Ratnakara Part 2: Gemini + Cancer\n\n"
     "**Tests:** 2323 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections C (Gemini) + D (Cancer) — 130 rules (BVR131-BVR260):\n\n"
     "- `src/corpus/bhavartha_ratnakara_2.py`: One registry (BHAVARTHA_RATNAKARA_2_REGISTRY):\n"
     "  - Section C (Gemini, 65 rules BVR131-BVR195): Sun (7), Moon (6), Mars (7), "
     "Mercury (6), Jupiter (6), Venus (6), Saturn (6), yogas (10) + extra placements (11). "
     "lagna_scope=['gemini'] on all rules.\n"
     "  - Section D (Cancer, 65 rules BVR196-BVR260): Sun (5), Moon (6), Mars (6), "
     "Mercury (5), Jupiter (5), Venus (6), Saturn (6), yogas (14) + extra placements (12). "
     "lagna_scope=['cancer'] on all rules. Yogakaraka Mars highlighted.\n"
     "- All 7 classical planets covered for both lagnas.\n"
     "- phase=1B_conditional, source=BhavarthaRatnakara, school=parashari on every rule.\n\n"
     "**Corpus:** 3167 rules (3037 + 130)\n\n"
     "### Next session\nS269 — Bhavartha Ratnakara Part 3: Leo + Virgo "
     "(~130 rules, BVR261-BVR390)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 267:** Bhavartha Ratnakara Aries + Taurus — BVR001-130; "
     "corpus 3037; 2309 tests\n"
     "- **Next session:** S268",
     "- **Session 267:** Bhavartha Ratnakara Aries + Taurus — BVR001-130; "
     "corpus 3037; 2309 tests\n"
     "- **Session 268:** Bhavartha Ratnakara Gemini + Cancer — BVR131-260; "
     "corpus 3167; 2323 tests\n"
     "- **Next session:** S269"),
    (ROOT / "docs/MEMORY.md",
     "- **2309 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2323 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S268" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S268")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections C, D
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| C | Gemini (Mithuna) | 65 | S268 | 🔲 |",
     "| C | Gemini (Mithuna) | 65 | S268 | ✅ |"),
    ("| D | Cancer (Karka) | 65 | S268 | 🔲 |",
     "| D | Cancer (Karka) | 65 | S268 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **130/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **260/780** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:45]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")

cmap.write_text(cmap_text)
print("done")
