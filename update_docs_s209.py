"""update_docs_s209.py — S209 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S209 — 2026-03-28 — Corpus Pipeline Integration Tests\n\n"
     "**Tests:** 1638 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `tests/test_s209_corpus_pipeline_integration.py`: 9 integration tests covering\n"
     "  the full pipeline: OSF schema → CV split → corpus load → audit → extractor\n"
     "  → BirthRecord → ADB license check → G22 gate.\n\n"
     "### Next session\nS210 — corpus checkpoint: ROADMAP S201-S210 ✅, CLASSICAL_CORPUS.md update\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1629 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1638 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–208 complete",
     "## Actual Current State (Sessions 1–209 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S209",
     "- **Session 209:** Corpus pipeline integration tests (9 tests); 1638 tests\n- **Next session:** S210"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S209" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S209")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
