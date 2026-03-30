"""update_docs_s238.py — S238 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S238 — 2026-03-28 — Brihat Jataka Extended Rules\n\n"
     "**Tests:** 1877 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `brihat_jataka_ext.py`: 30 rules (BJE001-BJE030) — "
     "Varahamihira's Brihat Jataka (6th cent CE): planetary natures for all 9 grahas (9 rules), "
     "hora/drekkana/navamsha systems (3 rules), aspects (3 rules), "
     "raja/dhana yogas (3 rules), life events (5 rules), dasha timing (3 rules).\n\n"
     "**Corpus total: 716 rules**\n\n"
     "### Next session\nS239 — Phala Deepika extended rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1869 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1877 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–237 complete",
     "## Actual Current State (Sessions 1–238 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 237:** Varga rules — D9/D10/D4/D7/D12+others; 30 rules; corpus 686; 1869 tests\n"
     "- **Next session:** S238",
     "- **Session 237:** Varga rules — D9/D10/D4/D7/D12+others; 30 rules; corpus 686; 1869 tests\n"
     "- **Session 238:** Brihat Jataka extended — planetary natures+aspects+yogas+timing; 30 rules; corpus 716; 1877 tests\n"
     "- **Next session:** S239"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S238" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S238")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
