"""update_docs_s241.py — S241 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S241 — 2026-03-28 — Jataka Parijata Extended Rules\n\n"
     "**Tests:** 1904 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `jataka_parijata_ext.py`: 30 rules (JPE001-JPE030) — "
     "Vaidyanatha Dikshita's Jataka Parijata (14th cent CE): all 12 lagna analyses (10 rules, "
     "grouping last 3), Parivartana yoga classifications, Neecha Bhanga Raja Yoga, "
     "Vesi/Vasi/Obhayachari/Chandra Mangala/Shakata/Kemadruma yogas, "
     "all 9 Vimshottari Mahadasha results.\n\n"
     "**Corpus total: 806 rules — 800+ MILESTONE ACHIEVED!**\n\n"
     "### Next session\nS242 — Sarvartha Chintamani / transit rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1895 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1904 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–240 complete",
     "## Actual Current State (Sessions 1–241 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 240:** Uttara Kalamrita extended — house+planet significations+principles; 30 rules; corpus 776; 1895 tests\n"
     "- **Next session:** S241",
     "- **Session 240:** Uttara Kalamrita extended — house+planet significations+principles; 30 rules; corpus 776; 1895 tests\n"
     "- **Session 241:** Jataka Parijata extended — lagnas+yogas+all 9 Maha Dasha results; 30 rules; corpus 806; 1904 tests ✅ 800+ MILESTONE\n"
     "- **Next session:** S242"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S241" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S241")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
