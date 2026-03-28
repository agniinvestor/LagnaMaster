"""update_docs_s198.py — S198 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S198 — 2026-03-28 — Feature Extractors: pushkara_nav, war_loser\n\n"
     "**Tests:** 1535 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `feature_decomp.py` +2 extractors: `pushkara_nav` (R21 Pushkara Navamsha),\n"
     "  `war_loser` (Graha Yuddha Saravali Ch.4). 13 × 12 = 156 features.\n"
     "- **Crosses 150-feature threshold** — feature space ready for Phase 6 (G22).\n\n"
     "### Next session\nS199 — contract tests: feature_count ≥ 150, array/dict consistency\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1530 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1535 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–197 complete",
     "## Actual Current State (Sessions 1–198 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S198",
     "- **Session 198:** +2 extractors (pushkara_nav, war_loser); 156 features (≥150 ✅); 1535 tests\n- **Next session:** S199"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S198" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S198")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
