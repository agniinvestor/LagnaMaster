"""update_docs_s196.py — S196 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S196 — 2026-03-28 — Feature Extractors: kartari, combust, retrograde, bhavesh_house_type\n\n"
     "**Tests:** 1525 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `feature_decomp.py` +4 extractors: `kartari_score` (R08/R12), `combust_score` (R19),\n"
     "  `retrograde_score` (R22), `bhavesh_house_type` (R04 placement). 8 × 12 = 96 features.\n\n"
     "### Next session\nS197 — benefic_net_score, malefic_net_score, karak_score\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1517 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1525 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–195 complete",
     "## Actual Current State (Sessions 1–196 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S196",
     "- **Session 196:** +4 feature extractors (kartari, combust, retrograde, bhavesh_house_type); 1525 tests\n- **Next session:** S197"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S196" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
