"""update_docs_s269.py — S269 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S269 — 2026-03-30 — Bhavartha Ratnakara Part 3: Leo + Virgo\n\n"
     "**Tests:** 2337 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Bhavartha Ratnakara Sections E (Leo) + F (Virgo) — 130 rules (BVR261-BVR390):\n\n"
     "- `src/corpus/bhavartha_ratnakara_3.py`: One registry (BHAVARTHA_RATNAKARA_3_REGISTRY):\n"
     "  - Section E (Leo, 65 rules BVR261-BVR325): Mars yogakaraka (H4+H9) highlighted. "
     "Sun as lagna lord, Saturn as double malefic (H6+H7). All 7 planets + yogas covered.\n"
     "  - Section F (Virgo, 65 rules BVR326-BVR390): Mercury owns H1+H10 (lagna + career). "
     "Jupiter full KD dosha. Venus as H9 trikona + H2 maraka lord. Saturn H5 trikona.\n"
     "- lagna_scope=['leo'] and lagna_scope=['virgo'] on all respective rules.\n\n"
     "**Corpus:** 3297 rules (3167 + 130)\n\n"
     "### Next session\nS270 — Bhavartha Ratnakara Part 4: Libra + Scorpio "
     "(~130 rules, BVR391-BVR520)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 268:** Bhavartha Ratnakara Gemini + Cancer — BVR131-260; "
     "corpus 3167; 2323 tests\n"
     "- **Next session:** S269",
     "- **Session 268:** Bhavartha Ratnakara Gemini + Cancer — BVR131-260; "
     "corpus 3167; 2323 tests\n"
     "- **Session 269:** Bhavartha Ratnakara Leo + Virgo — BVR261-390; "
     "corpus 3297; 2337 tests\n"
     "- **Next session:** S270"),
    (ROOT / "docs/MEMORY.md",
     "- **2323 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2337 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S269" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S269")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Sections E, F
cmap = ROOT / "docs/coverage_maps/bhavartha_ratnakara.md"
cmap_text = cmap.read_text()

for old_line, new_line in [
    ("| E | Leo (Simha) | 65 | S269 | 🔲 |",
     "| E | Leo (Simha) | 65 | S269 | ✅ |"),
    ("| F | Virgo (Kanya) | 65 | S269 | 🔲 |",
     "| F | Virgo (Kanya) | 65 | S269 | ✅ |"),
    ("| **TOTAL** | | **780** | **S267–S272** | **260/780** |",
     "| **TOTAL** | | **780** | **S267–S272** | **390/780** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated '{old_line[:45]}...'")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")

cmap.write_text(cmap_text)
print("done")
