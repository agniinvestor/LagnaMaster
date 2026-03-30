"""update_docs_s204.py — S204 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S204 — 2026-03-28 — TextExtractor Protocol + TimeBasedSplit CV\n\n"
     "**Tests:** 1592 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/extractor_base.py`: `TextExtractor` Protocol + `BaseExtractor` base class.\n"
     "  `load_into(registry)` convenience method — skips duplicate rule IDs.\n"
     "- `src/research/cv_splitter.py`: `TimeBasedSplit` — `is_train/is_test/split()`,\n"
     "  validates no look-ahead, parameters match OB-3 OSF draft (train≤2009, test≥2010).\n\n"
     "### Next session\nS205 — corpus audit script + BPHS new rule encoding (30 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1582 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1592 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–203 complete",
     "## Actual Current State (Sessions 1–204 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S204",
     "- **Session 204:** TextExtractor Protocol + TimeBasedSplit CV splitter; 1592 tests\n- **Next session:** S205"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S204" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S204")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
