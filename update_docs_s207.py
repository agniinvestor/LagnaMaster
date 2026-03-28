"""update_docs_s207.py — S207 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S207 — 2026-03-28 — Uttara Kalamrita + Jataka Parijata Rule Encoding\n\n"
     "**Tests:** 1618 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/uttara_kalamrita_rules.py`: 17 rules (UK001-UK017) — Arudha Lagna,\n"
     "  special lagnas (Hora, Ghati), Mahapurusha yogas, dasha fructification.\n"
     "- `src/corpus/jataka_parijata_rules.py`: 17 rules (JP001-JP017) — Raja Yoga,\n"
     "  Dhana Yoga, Viparita Raja, Gajakesari, Chara Karakas, Chandra-Mangala.\n"
     "- **Corpus: 135 rules across 6 texts** (R01-R23 + BPHS + Phala + BJ + UK + JP).\n\n"
     "### Next session\nS208 — BirthRecord + Sarwarthachintamani + combined corpus loader\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1610 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1618 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–206 complete",
     "## Actual Current State (Sessions 1–207 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S207",
     "- **Session 207:** Uttara Kalamrita (17) + Jataka Parijata (17); 135 total corpus rules; 1618 tests\n- **Next session:** S208"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S207" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S207")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
