"""update_docs_s199.py — S199 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S199 — 2026-03-28 — Feature Contract Tests\n\n"
     "**Tests:** 1545 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `tests/test_s199_feature_contracts.py`: 10 contract tests ensuring\n"
     "  internal consistency of ChartFeatureVector — to_array/to_dict length,\n"
     "  unique names, order consistency, all-float, 12 houses, finite values,\n"
     "  G22 Phase 6 gate (feature_count ≥ 150).\n\n"
     "### Next session\nS200 — final G22 wiring, ChartScoresV3 integration, session log export\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1535 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1545 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–198 complete",
     "## Actual Current State (Sessions 1–199 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S199",
     "- **Session 199:** feature contract tests (10 tests, G22 gate); 1545 tests\n- **Next session:** S200"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S199" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S199")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
