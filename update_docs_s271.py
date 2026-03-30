"""update_docs_s271.py — S271 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S271 — 2026-03-30 — Bhavartha Ratnakara Part 5: Sagittarius + Capricorn\n\n"
     "**Tests:** 2365 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections I (Sagittarius) + J (Capricorn) — 130 rules (BVR521-BVR650):\n\n"
     "- `src/corpus/bhavartha_ratnakara_5.py`: One registry (BHAVARTHA_RATNAKARA_5_REGISTRY):\n"
     "  - Section I (Sagittarius, 65 rules BVR521-BVR585): Sun H9 trikona (functional benefic). "
     "Mars H5+H12 (trikona dominates). Venus H6+H11 (functional malefic). No yogakaraka.\n"
     "  - Section J (Capricorn, 65 rules BVR586-BVR650): Venus yogakaraka (H5+H10). "
     "Jupiter H3+H12 (functional malefic despite natural benefic). Saturn lagna+H2 lord.\n"
     "- Wired into combined_corpus.py.\n\n"
     "**Corpus:** 3557 rules (3427 + 130)\n\n"
     "### Next session\nS272 — Bhavartha Ratnakara Part 6: Aquarius + Pisces "
     "(~130 rules, BVR651-BVR780, completing all 12 lagnas)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 270:** Bhavartha Ratnakara Libra + Scorpio — BVR391-520; "
     "corpus 3427; 2351 tests\n"
     "- **Next session:** S271",
     "- **Session 270:** Bhavartha Ratnakara Libra + Scorpio — BVR391-520; "
     "corpus 3427; 2351 tests\n"
     "- **Session 271:** Bhavartha Ratnakara Sagittarius + Capricorn — BVR521-650; "
     "corpus 3557; 2365 tests\n"
     "- **Next session:** S272"),
    (ROOT / "docs/MEMORY.md",
     "- **2351 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2365 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S271" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S271")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections I, J
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| I | Sagittarius (Dhanus) | 65 | S271 | 🔲 |",
     "| I | Sagittarius (Dhanus) | 65 | S271 | ✅ |"),
    ("| J | Capricorn (Makara) | 65 | S271 | 🔲 |",
     "| J | Capricorn (Makara) | 65 | S271 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **520/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **650/780** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:45]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")

cmap.write_text(cmap_text)
print("done")
