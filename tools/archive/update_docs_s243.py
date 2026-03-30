"""update_docs_s243.py — S243 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S243 — 2026-03-28 — Ashtakavarga Rules\n\n"
     "**Tests:** 1925 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `ashtakavarga_rules.py`: 30 rules (AST001-AST030) — "
     "Classical Ashtakavarga system from BPHS Ch.66-76 (parashari), "
     "Brihat Jataka Ch.19 (varahamihira), Sarvartha Chintamani Ch.10 (sarvartha): "
     "Prasthara BAV structure, Sarvashtakavarga, Trikona + Ekadhipatya Shodhana, "
     "all 7 planet BAVs (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn), "
     "Kakshya timing divisions, Pinda/Yoga/Rashi Saham, transit assessment by "
     "bindus (0-8 scale), longevity, career/wealth/travel/compatibility applications.\n\n"
     "**Corpus total: 866 rules**\n\n"
     "### Next session\nS244 — Jaimini Sutras / Upagraha rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1914 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1925 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–242 complete",
     "## Actual Current State (Sessions 1–243 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 242:** Classical transit rules — Gochara/Vedha/Ashtakavarga/Sade Sati/double transit; 30 rules; corpus 836; 1914 tests\n"
     "- **Next session:** S243",
     "- **Session 242:** Classical transit rules — Gochara/Vedha/Ashtakavarga/Sade Sati/double transit; 30 rules; corpus 836; 1914 tests\n"
     "- **Session 243:** Ashtakavarga rules — BAV structure/Shodhana/Kakshya/planet BAVs/transit assessment; 30 rules; corpus 866; 1925 tests\n"
     "- **Next session:** S244"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S243" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S243")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
