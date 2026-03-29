"""update_docs_s195.py — S195 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
for doc, old, new in [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S195 — 2026-03-28 — Feature Decomposition Infrastructure\n\n"
     "**Tests:** 1517 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/calculations/feature_decomp.py`: `RuleFeature`, `HouseFeatureVector`,\n"
     "  `ChartFeatureVector` dataclasses + `extract_features(chart, school)`.\n"
     "  Four extractors: `gentle_sign` (R01), `bhavesh_dignity` (R04 continuous),\n"
     "  `dig_bala` (R20), `sav_bindus_norm` (R23 continuous).\n"
     "  4 features × 12 houses = 48 features. G22 compliance note in module docstring.\n\n"
     "### Next session\nS196 — kartari_score, combust_score, retrograde_score, bhavesh_house_type\n"),
    (ROOT / "docs/MEMORY.md",
     "- **1503 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1517 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT / "docs/MEMORY.md",
     "## Actual Current State (Sessions 1–194 complete",
     "## Actual Current State (Sessions 1–195 complete"),
    (ROOT / "docs/MEMORY.md",
     "- **Next session:** S195",
     "- **Session 195:** Feature decomp infrastructure — `feature_decomp.py`, 4 extractors, 48 features; 1517 tests\n- **Next session:** S196"),
    (ROOT / "docs/ROADMAP.md",
     "| S195–S200 | Feature decomposition — 23 binary → 150+ continuous features | G22 | 🔴 |",
     "| S195–S200 | Feature decomposition — 23 binary → 150+ continuous features | G22 | 🟡 S195✅ |"),
]:
    text = doc.read_text()
    if old is None:
        if "## S195" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} — S195 appended")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} — patched")
    else:
        print(f"{doc.name} — pattern not found, skipped")
print("update_docs_s195.py done")
