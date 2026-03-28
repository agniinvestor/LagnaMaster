"""update_docs_s242.py — S242 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S242 — 2026-03-28 — Classical Transit (Gochara) Rules\n\n"
     "**Tests:** 1934 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `transit_rules.py`: 30 rules (TRN001-TRN030) — "
     "Classical Gochara (transit) rules from BPHS Ch.90 (parashari) and "
     "Sarvartha Chintamani Ch.10 (sarvartha): fundamental transit-from-Moon principle, "
     "Vedha obstruction, Ashtakavarga bindus, per-planet transit results (Sun/Moon/Mars/"
     "Mercury/Jupiter/Venus/Saturn/Rahu/Ketu), Sade Sati (7.5 years), Ashtama Shani, "
     "double transit (Jupiter+Saturn), triple trigger, retrograde three-pass, Tajika.\n\n"
     "**Corpus total: 836 rules**\n\n"
     "### Next session\nS243 — Ashtakavarga rules / Jaimini Sutras\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1904 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1934 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–241 complete",
     "## Actual Current State (Sessions 1–242 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 241:** Jataka Parijata extended — lagnas+yogas+all 9 Maha Dasha results; 30 rules; corpus 806; 1904 tests ✅ 800+ MILESTONE\n"
     "- **Next session:** S242",
     "- **Session 241:** Jataka Parijata extended — lagnas+yogas+all 9 Maha Dasha results; 30 rules; corpus 806; 1904 tests ✅ 800+ MILESTONE\n"
     "- **Session 242:** Classical transit rules — Gochara/Vedha/Ashtakavarga/Sade Sati/double transit; 30 rules; corpus 836; 1934 tests\n"
     "- **Next session:** S243"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S242" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S242")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
