"""update_docs_s244.py — S244 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S244 — 2026-03-28 — Jaimini Sutras + Upagraha Rules\n\n"
     "**Tests:** 1936 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `jaimini_sutras_rules.py`: 30 rules (JMS001-JMS030) — "
     "Jaimini Sutras (Maharishi Jaimini) + BPHS Ch.24: "
     "Chara Karaka system (AK/AmK/BK/MK/PK/GK/DK by degree), Karakamsha lagna, "
     "Rashi Drishti sign aspects, Argala intervention, Arudha/Pada system (AL/UL/GL/HL), "
     "Chara Dasha structure and interpretation, Sthira Dasha periods, Jaimini yogas "
     "(Raja/Dhana), longevity assessment, Upagrahas (Gulika/Mandi/Dhuma/Vyatipata).\n\n"
     "**Corpus total: 896 rules**\n\n"
     "### Next session\nS245 — Shadbala rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1925 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1936 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–243 complete",
     "## Actual Current State (Sessions 1–244 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 243:** Ashtakavarga rules — BAV structure/Shodhana/Kakshya/planet BAVs/transit assessment; 30 rules; corpus 866; 1925 tests\n"
     "- **Next session:** S244",
     "- **Session 243:** Ashtakavarga rules — BAV structure/Shodhana/Kakshya/planet BAVs/transit assessment; 30 rules; corpus 866; 1925 tests\n"
     "- **Session 244:** Jaimini Sutras + Upagrahas — Chara Karakas/Rashi Drishti/Arudha/Chara Dasha/Gulika; 30 rules; corpus 896; 1936 tests\n"
     "- **Next session:** S245"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S244" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S244")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
