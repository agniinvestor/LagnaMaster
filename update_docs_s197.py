"""update_docs_s197.py — S197 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S197 — 2026-03-28 — Feature Extractors: benefic_net_score, malefic_net_score, karak_score\n\n"
     "**Tests:** 1530 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `feature_decomp.py` +3 extractors: `benefic_net_score` (R02-R07), `malefic_net_score` (R09-R14),\n"
     "  `karak_score` (R17/R18 Sthira Karak). 11 × 12 = 132 features.\n"
     "- Wired `compute_functional_roles` into `extract_features()` for is_fb/is_fm.\n\n"
     "### Next session\nS198 — pushkara_nav + war_loser extractors → 13 × 12 = 156 features\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1525 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1530 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–196 complete",
     "## Actual Current State (Sessions 1–197 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S197",
     "- **Session 197:** +3 feature extractors (benefic_net_score, malefic_net_score, karak_score); 1530 tests\n- **Next session:** S198"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S197" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S197")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
