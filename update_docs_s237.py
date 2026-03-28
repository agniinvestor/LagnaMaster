"""update_docs_s237.py — S237 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S237 — 2026-03-28 — BPHS Varga (Divisional Chart) Rules\n\n"
     "**Tests:** 1869 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_varga_rules.py`: 30 rules (VAR001-VAR030) — "
     "D9 Navamsha (10 rules): vargottama, karakamsha, timing, pushkara; "
     "D10 Dashamsha (8 rules): lagna, Sun/Saturn, career timing; "
     "Other vargas D4/D7/D12/D16/D20/D24/D30/D60/D5 (12 rules): specific "
     "house significations + panchamsha/saptavargaja bala.\n\n"
     "**Corpus total: 686 rules**\n\n"
     "### Next session\nS238 — Brihat Jataka: planetary natures and results\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1860 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1869 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–236 complete",
     "## Actual Current State (Sessions 1–237 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 236:** Bhava karakas — naisargika+Jaimini chara+special; 30 rules; corpus 656; 1860 tests\n"
     "- **Next session:** S237",
     "- **Session 236:** Bhava karakas — naisargika+Jaimini chara+special; 30 rules; corpus 656; 1860 tests\n"
     "- **Session 237:** Varga rules — D9/D10/D4/D7/D12+others; 30 rules; corpus 686; 1869 tests\n"
     "- **Next session:** S238"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S237" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S237")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
