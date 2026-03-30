"""update_docs_s270.py — S270 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S270 — 2026-03-30 — Bhavartha Ratnakara Part 4: Libra + Scorpio\n\n"
     "**Tests:** 2351 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections G (Libra) + H (Scorpio) — 130 rules (BVR391-BVR520):\n\n"
     "- `src/corpus/bhavartha_ratnakara_4.py`: One registry (BHAVARTHA_RATNAKARA_4_REGISTRY):\n"
     "  - Section G (Libra, 65 rules BVR391-BVR455): Saturn yogakaraka (H4+H5). "
     "Mars double maraka (H2+H7). Jupiter functional malefic (H3+H6). Venus lagna+H8 lord.\n"
     "  - Section H (Scorpio, 65 rules BVR456-BVR520): Moon H9 trikona (functional benefic). "
     "Jupiter H2+H5 (maraka softened by trikona). Mars lagna+H6 lord. No yogakaraka.\n"
     "- Wired into combined_corpus.py (BHAVARTHA_RATNAKARA_4_REGISTRY).\n\n"
     "**Corpus:** 3427 rules (3297 + 130)\n\n"
     "### Next session\nS271 — Bhavartha Ratnakara Part 5: Sagittarius + Capricorn "
     "(~130 rules, BVR521-BVR650)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 269:** Bhavartha Ratnakara Leo + Virgo — BVR261-390; "
     "corpus 3297; 2337 tests\n"
     "- **Next session:** S270",
     "- **Session 269:** Bhavartha Ratnakara Leo + Virgo — BVR261-390; "
     "corpus 3297; 2337 tests\n"
     "- **Session 270:** Bhavartha Ratnakara Libra + Scorpio — BVR391-520; "
     "corpus 3427; 2351 tests\n"
     "- **Next session:** S271"),
    (ROOT / "docs/MEMORY.md",
     "- **2337 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2351 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S270" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S270")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections G, H
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| G | Libra (Tula) | 65 | S270 | 🔲 |",
     "| G | Libra (Tula) | 65 | S270 | ✅ |"),
    ("| H | Scorpio (Vrischika) | 65 | S270 | 🔲 |",
     "| H | Scorpio (Vrischika) | 65 | S270 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **390/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **520/780** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:45]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")

cmap.write_text(cmap_text)
print("done")
