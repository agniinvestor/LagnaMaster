"""update_docs_s202.py — S202 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S202 — 2026-03-28 — Corpus Infrastructure: RuleRecord + CorpusRegistry\n\n"
     "**Tests:** 1570 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/rule_record.py`: `RuleRecord` dataclass — rule_id, source, chapter,\n"
     "  school, category, description, confidence (0–1), verse, tags, implemented, engine_ref.\n"
     "- `src/corpus/registry.py`: `CorpusRegistry` — add/get/filter/count/summary;\n"
     "  raises ValueError on duplicate rule_id.\n\n"
     "### Next session\nS203 — ADB license compliance module + data source tracking\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1558 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1570 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–201 complete",
     "## Actual Current State (Sessions 1–202 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S202",
     "- **Session 202:** RuleRecord + CorpusRegistry corpus infrastructure; 1570 tests\n- **Next session:** S203"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S202" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S202")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
