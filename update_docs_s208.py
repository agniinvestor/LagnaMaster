"""update_docs_s208.py — S208 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S208 — 2026-03-28 — BirthRecord + CombinedCorpus\n\n"
     "**Tests:** 1629 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/birth_record.py`: `BirthRecord` ML data schema — record_id,\n"
     "  birth date/time, lat/lon, data_source, Rodden rating, confirmed_events.\n"
     "- `src/corpus/combined_corpus.py`: `COMBINED_CORPUS` singleton — loads all 6\n"
     "  text registries (135+ rules) into one searchable CorpusRegistry.\n"
     "  `build_corpus()` for fresh rebuild.\n\n"
     "### Next session\nS209 — corpus pipeline integration tests\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1618 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1629 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–207 complete",
     "## Actual Current State (Sessions 1–208 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S208",
     "- **Session 208:** BirthRecord + COMBINED_CORPUS (135+ rules, 6 texts); 1629 tests\n- **Next session:** S209"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S208" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S208")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
