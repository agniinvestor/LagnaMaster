"""update_docs_s203.py — S203 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S203 — 2026-03-28 — ADB License Compliance + R01-R23 Corpus Encoding\n\n"
     "**Tests:** 1582 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/research/data_license.py`: `DataSourceLicense` dataclass, `KNOWN_SOURCES`\n"
     "  (ADB non-commercial, PUBLIC_DOMAIN, BPHS_TEXT, SELF_REPORTED),\n"
     "  `check_source_license(source_id, commercial)` — raises PermissionError for ADB+commercial.\n"
     "- `src/corpus/existing_rules.py`: All 23 engine rules (R01-R23) encoded as\n"
     "  `RuleRecord` objects in `EXISTING_RULES_REGISTRY`. All marked `implemented=True`,\n"
     "  confidence ≥ 0.8, full classical source citations.\n\n"
     "### Next session\nS204 — corpus extractor base class + BPHS text extractor\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1570 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1582 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–202 complete",
     "## Actual Current State (Sessions 1–203 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S203",
     "- **Session 203:** ADB license + R01-R23 corpus encoding (EXISTING_RULES_REGISTRY); 1582 tests\n- **Next session:** S204"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S203" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S203")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
