"""update_docs_s211.py — S211 documentation sync"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S211 — 2026-03-28 — ML Infrastructure Schema (pgvector + TimescaleDB + MLflow + Family)\n\n"
     "**Tests:** 1651 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/db_vector.py`: pgvector schema — `chart_embeddings` table for 156-dim feature\n"
     "  vectors, IVFFlat cosine index, `feature_schema_versions`.\n"
     "- `src/db_timescale.py`: TimescaleDB schema — `dasha_periods`, `outcome_confirmations`\n"
     "  (G04: user_prior_prob_pre field), `transit_activations` hypertables.\n"
     "- `src/ml/mlflow_config.py`: MLflow experiment registry — OB-3 / OB-3-SHAP /\n"
     "  EXPLORATORY configs with G22 guardrail notes.\n"
     "- `src/db_family.py`: `FamilyRelation` enum + family_groups / family_members /\n"
     "  family_relations / family_patterns schema (G03/G16 compliance notes).\n\n"
     "### Next session\nS212 — Ayanamsha selection + KP school fix (G06 compliance)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1638 passing, 3 skipped, 0 lint errors, CI green (S210 checkpoint)**",
     "- **1651 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–210 complete",
     "## Actual Current State (Sessions 1–211 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S211",
     "- **Session 211:** pgvector + TimescaleDB + MLflow + family schema; 1651 tests\n- **Next session:** S212"),
    (ROOT/"docs/ROADMAP.md",
     "| S211 | Redis + pgvector + TimescaleDB + MLflow + family schema | — | 🔴 |",
     "| S211 | Redis + pgvector + TimescaleDB + MLflow + family schema | — | ✅ |"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S211" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S211")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
