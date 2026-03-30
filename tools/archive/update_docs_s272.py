"""update_docs_s272.py — S272 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S272 — 2026-03-30 — Bhavartha Ratnakara Part 6: Aquarius + Pisces\n\n"
     "**Tests:** 2379 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections K (Aquarius) + L (Pisces) — 130 rules (BVR651-BVR780):\n\n"
     "- `src/corpus/bhavartha_ratnakara_6.py`: One registry (BHAVARTHA_RATNAKARA_6_REGISTRY):\n"
     "  - Section K (Aquarius, 65 rules BVR651-BVR715): Venus yogakaraka (H4+H9). "
     "Moon H6 (functional malefic). Jupiter H2+H11 (maraka + upachaya).\n"
     "  - Section L (Pisces, 65 rules BVR716-BVR780): Mars H9 trikona (functional benefic). "
     "Moon H5 trikona (functional benefic). Mercury H4+H7 (KD dosha). No yogakaraka.\n"
     "- Wired into combined_corpus.py.\n"
     "- **Bhavartha Ratnakara COMPLETE**: all 12 lagnas encoded, 780/780 rules.\n\n"
     "**Corpus:** 3687 rules (3557 + 130)\n\n"
     "### Next session\nS273 — Saravali sutra-level re-encode (conjunctions)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 271:** Bhavartha Ratnakara Sagittarius + Capricorn — BVR521-650; "
     "corpus 3557; 2365 tests\n"
     "- **Next session:** S272",
     "- **Session 271:** Bhavartha Ratnakara Sagittarius + Capricorn — BVR521-650; "
     "corpus 3557; 2365 tests\n"
     "- **Session 272:** Bhavartha Ratnakara Aquarius + Pisces — BVR651-780; "
     "corpus 3687; 2379 tests — **BVR COMPLETE (780/780)**\n"
     "- **Next session:** S273"),
    (ROOT / "docs/MEMORY.md",
     "- **2365 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2379 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S272" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S272")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections K, L + mark complete
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| K | Aquarius (Kumbha) | 65 | S272 | 🔲 |",
     "| K | Aquarius (Kumbha) | 65 | S272 | ✅ |"),
    ("| L | Pisces (Meena) | 65 | S272 | 🔲 |",
     "| L | Pisces (Meena) | 65 | S272 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **650/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **780/780 ✅** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:45]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")

cmap.write_text(cmap_text)
print("done")
