"""update_docs_s205.py — S205 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S205 — 2026-03-28 — CorpusAudit + 31 BPHS Extended Rules\n\n"
     "**Tests:** 1602 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/corpus_audit.py`: `CorpusAudit` — run()/text_report() for completeness\n"
     "  checking (total, implemented, unimplemented, by school/category/source).\n"
     "- `src/corpus/bphs_extended.py`: 31 new BPHS rule encodings (B001-B031) covering\n"
     "  lagna-lord placement, 9th/10th yoga, vargottama, exaltation/debilitation,\n"
     "  aspects (Jupiter/Saturn/Mars), yogakaraka, argala, transits, upachaya.\n"
     "  All `implemented=False` — Phase 1 (S216-S250) encoding targets.\n\n"
     "### Next session\nS206 — Phaladeepika rules + Brihat Jataka rules (30 rules each)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1592 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1602 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–204 complete",
     "## Actual Current State (Sessions 1–205 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S205",
     "- **Session 205:** CorpusAudit + 31 BPHS extended rules (B001-B031); 1602 tests\n- **Next session:** S206"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S205" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S205")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
