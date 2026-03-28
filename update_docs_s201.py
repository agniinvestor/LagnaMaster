"""update_docs_s201.py — S201 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S201 — 2026-03-28 — OSF Pre-Registration Schema (G22)\n\n"
     "**Tests:** 1558 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/research/osf_registration.py`: `HypothesisSpec`, `CVStrategy`, `OSFRegistration`\n"
     "  dataclasses + `to_dict()` / `to_json()` serialization.\n"
     "- `docs/research/osf_draft_ob3.json`: Draft OB-3 filing — primary H1 (concordance\n"
     "  predicts above single-school baseline), 3 secondary hypotheses, BH-FDR q<0.05,\n"
     "  time-split CV (pre-2010 train / 2010+ test), minimum_sample=1000.\n\n"
     "### Next session\nS202 — RuleRecord + CorpusRegistry infrastructure\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1550 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1558 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–200 complete",
     "## Actual Current State (Sessions 1–201 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S201",
     "- **Session 201:** OSF schema (HypothesisSpec, CVStrategy, OSFRegistration) + OB-3 draft; 1558 tests\n- **Next session:** S202"),
    (ROOT/"docs/RESEARCH.md",
     "| OB-3 XGBoost analysis | 🔴 **NOT YET FILED** |",
     "| OB-3 XGBoost analysis | 🟡 **Draft in docs/research/osf_draft_ob3.json** |"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S201" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S201")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
