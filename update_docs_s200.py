"""update_docs_s200.py — S200 documentation sync (Phase 0 feature decomp complete)"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S200 — 2026-03-28 — G22 Integration + ChartScoresV3 Feature Vector\n\n"
     "**Tests:** 1550 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `scoring_v3.py`: Added `feature_vector: ChartFeatureVector` field to `ChartScoresV3`.\n"
     "  `score_chart_v3()` now calls `extract_features(chart, school)` and populates it.\n"
     "- `ROADMAP.md`: S193–S200 marked ✅. Feature decomposition phase complete.\n"
     "- **Phase 0 feature decomposition milestone:** 13 × 12 = 156 continuous features,\n"
     "  all G22 compliant. Phase 6 (ML Pipeline) feature space requirement satisfied.\n\n"
     "### Phase summary (S195–S200)\n"
     "| Session | Added | Running total |\n"
     "|---------|-------|---------------|\n"
     "| S195 | gentle_sign, bhavesh_dignity, dig_bala, sav_bindus_norm | 48 |\n"
     "| S196 | kartari_score, combust_score, retrograde_score, bhavesh_house_type | 96 |\n"
     "| S197 | benefic_net_score, malefic_net_score, karak_score | 132 |\n"
     "| S198 | pushkara_nav, war_loser | **156** |\n"
     "| S199 | Contract tests (G22 gate) | — |\n"
     "| S200 | ChartScoresV3 wiring, ROADMAP ✅ | — |\n\n"
     "### Next session\nS201 — OSF pre-registration + ADB license + corpus extractor pipeline\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1545 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1550 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–199 complete",
     "## Actual Current State (Sessions 1–200 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S200",
     "- **Session 200:** ChartScoresV3 feature_vector field; ROADMAP S195–S200 ✅; 1550 tests\n- **Next session:** S201"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S200" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S200")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
