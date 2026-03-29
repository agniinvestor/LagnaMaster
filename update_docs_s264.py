"""update_docs_s264.py — S264 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    # CHANGELOG — append S264 entry
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S264 — 2026-03-30 — Laghu Parashari Functional Nature Table\n\n"
     "**Tests:** 2250 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Section A of the Laghu Parashari coverage map — 108 rules (LPF001–LPF108):\n\n"
     "- `src/corpus/laghu_parashari_functional.py`: Functional nature classification "
     "for 9 planets × 12 lagnas. Data-driven via `_TABLE` dict. All Phase 1B fields "
     "populated: `primary_condition`, `lagna_scope`, `outcome_direction`, "
     "`outcome_intensity`, `outcome_domains`, `verse_ref`, `phase='1B_conditional'`, "
     "`system='natal'`, `outcome_timing='dasha_dependent'`.\n"
     "- 6 yogakaraka rules tagged: Taurus=Saturn (LPF016), Cancer=Mars (LPF030), "
     "Leo=Mars (LPF039), Libra=Saturn (LPF061), Capricorn=Venus (LPF087), "
     "Aquarius=Venus (LPF096).\n"
     "- `src/corpus/combined_corpus.py`: Added `LAGHU_PARASHARI_FUNCTIONAL_REGISTRY`.\n"
     "- `tests/test_s264_laghu_parashari_functional.py`: 23 tests — count, IDs, "
     "all 12 lagnas × 9 rules, yogakaraka count, spot-checks on 6 specific rules, "
     "combined corpus count ≥ 2742.\n\n"
     "**Corpus:** 2742 rules (2634 Phase 1A + 108 Phase 1B)\n\n"
     "### Next session\nS265 — Laghu Parashari Sections B, C, D: "
     "Yogakaraka (~12), Kendradhipati (~20), Dasha Results by lordship (~42)\n"),

    # MEMORY.md — update test count
    (ROOT / "docs/MEMORY.md",
     "- **2227 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2250 passing, 3 skipped, 0 lint errors, CI green**"),

    # MEMORY.md — add S264 session line and update Next session
    (ROOT / "docs/MEMORY.md",
     "- **Session 263:** Phase 1B Schema Definition — Rule Contract + Outcome Taxonomy"
     " + Coverage Map + Concordance Workflow; RuleRecord +14 fields; corpus unchanged; 2227 tests\n"
     "- **Next session:** S264",
     "- **Session 263:** Phase 1B Schema Definition — Rule Contract + Outcome Taxonomy"
     " + Coverage Map + Concordance Workflow; RuleRecord +14 fields; corpus unchanged; 2227 tests\n"
     "- **Session 264:** Laghu Parashari Functional Nature Table — LPF001-108 (9×12); "
     "Phase 1B conditional; 6 yogakarakas; corpus 2742; 2250 tests\n"
     "- **Next session:** S265"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S264" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S264")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Section A status
cmap = ROOT / "docs/coverage_maps/laghu_parashari.md"
cmap_text = cmap.read_text()
if "Section A" in cmap_text and "pending" in cmap_text:
    cmap_text = cmap_text.replace(
        "| A | Functional Nature Table  | 9×12 = 108 | S264      | pending  |",
        "| A | Functional Nature Table  | 9×12 = 108 | S264      | complete |",
    )
    cmap.write_text(cmap_text)
    print(f"{cmap.name} Section A marked complete")
else:
    print(f"{cmap.name} — Section A status not updated (check manually)")

print("done")
