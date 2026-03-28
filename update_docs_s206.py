"""update_docs_s206.py — S206 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S206 — 2026-03-28 — Phaladeepika + Brihat Jataka Rule Encoding\n\n"
     "**Tests:** 1610 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/phaladeepika_rules.py`: 21 rules (PH001-PH021) — planetary states,\n"
     "  Kartari, house judgment, Graha Yuddha, dasha activation, Dig Bala, Paksha Bala.\n"
     "- `src/corpus/brihat_jataka_rules.py`: 26 rules (BJ001-BJ026) — exaltation degrees,\n"
     "  natural benefic/malefic, house significations (H1-H12), aspects, Moon yogas.\n"
     "- **Corpus milestone:** 23 + 31 + 21 + 26 = **101 rules** — exceeds 100.\n\n"
     "### Next session\nS207 — Uttara Kalamrita + Jataka Parijata rules (30 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1602 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1610 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–205 complete",
     "## Actual Current State (Sessions 1–206 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S206",
     "- **Session 206:** Phaladeepika (21) + Brihat Jataka (26) rules; 101 total corpus rules; 1610 tests\n- **Next session:** S207"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S206" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S206")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
