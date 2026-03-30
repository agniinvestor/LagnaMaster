"""update_docs_s263.py — S263 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S263 — 2026-03-30 — Phase 1B Schema Definition\n\n"
     "**Tests:** 2227 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Phase 1B gating session — no rules encoded, four protocol documents committed:\n\n"
     "- `docs/PHASE1B_RULE_CONTRACT.md`: 12 mandatory fields per Phase 1B rule, "
     "rejection criteria, confidence formula (mechanical not editorial)\n"
     "- `docs/PHASE1B_OUTCOME_TAXONOMY.md`: 15 fixed outcome domains, "
     "4 directions, 4 intensities, 5 timing qualifiers — not extensible during encoding\n"
     "- `docs/PHASE1B_CONCORDANCE_WORKFLOW.md`: 5-step real-time concordance protocol, "
     "match/divergence/scope-refinement classification, bidirectional update requirement\n"
     "- `docs/coverage_maps/laghu_parashari.md`: Full coverage map for first encoding "
     "target — 6 sections, 266 minimum rules, section-by-section completion tracking\n"
     "- `src/corpus/rule_record.py`: Extended with 14 Phase 1B fields "
     "(primary_condition, modifiers, exceptions, outcome_domains, outcome_direction, "
     "outcome_intensity, outcome_timing, lagna_scope, dasha_scope, verse_ref, "
     "concordance_texts, divergence_notes, phase, system) — all with safe defaults, "
     "Phase 1A rules unaffected\n\n"
     "**Phase 1A relabeled:** S216–S262 (2,634 rules) is the Representative Layer.\n"
     "**Phase 1B target:** ~9,200 structured predictions total.\n\n"
     "### Next session\nS264 — Laghu Parashari Part 1: Functional Nature Table "
     "(9×12 = 108 rules, Section A of coverage map)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S263",
     "- **Next session:** S264"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 262:** Phaladeepika Exhaustive — Mantreswara 14th century (PHX001-120); 120 rules; corpus 2634; 2227 tests\n"
     "- **Next session:** S264",
     "- **Session 262:** Phaladeepika Exhaustive — Mantreswara 14th century (PHX001-120); 120 rules; corpus 2634; 2227 tests\n"
     "- **Session 263:** Phase 1B Schema Definition — Rule Contract + Outcome Taxonomy + Coverage Map + Concordance Workflow; RuleRecord +14 fields; corpus unchanged; 2227 tests\n"
     "- **Next session:** S264"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S263" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S263")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
