"""update_docs_s210.py — S210 documentation sync (corpus checkpoint)"""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S210 — 2026-03-28 — Corpus Checkpoint (S201–S210 complete)\n\n"
     "**Tests:** 1638 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `CLASSICAL_CORPUS.md` updated: 135-rule corpus status, OSF filing status,\n"
     "  pipeline infrastructure summary.\n"
     "- `ROADMAP.md`: S201–S210 marked ✅.\n\n"
     "### Phase 0 corpus pipeline summary (S201–S210)\n"
     "| Session | Built |\n"
     "|---------|-------|\n"
     "| S201 | OSF pre-registration schema + OB-3 draft filing |\n"
     "| S202 | RuleRecord + CorpusRegistry infrastructure |\n"
     "| S203 | ADB license compliance + R01-R23 encoded |\n"
     "| S204 | TextExtractor Protocol + TimeBasedSplit CV |\n"
     "| S205 | CorpusAudit + 31 BPHS rules |\n"
     "| S206 | Phaladeepika (21) + Brihat Jataka (26) rules; 101 total |\n"
     "| S207 | Uttara Kalamrita (17) + Jataka Parijata (17); 135 total |\n"
     "| S208 | BirthRecord + COMBINED_CORPUS singleton |\n"
     "| S209 | Pipeline integration tests |\n"
     "| S210 | Corpus checkpoint + docs |\n\n"
     "### Next session\nS211 — Redis + pgvector + TimescaleDB + MLflow + family schema\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1638 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1638 passing, 3 skipped, 0 lint errors, CI green (S210 checkpoint)**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–209 complete",
     "## Actual Current State (Sessions 1–210 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Next session:** S210",
     "- **Session 210:** Corpus checkpoint; ROADMAP S201-S210 ✅; 135 rules across 6 texts\n- **Next session:** S211"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S210" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S210")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
