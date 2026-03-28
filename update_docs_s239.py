"""update_docs_s239.py — S239 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S239 — 2026-03-28 — Phala Deepika Extended Rules\n\n"
     "**Tests:** 1886 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `phala_deepika_ext.py`: 30 rules (PDE001-PDE030) — "
     "Mantreswara's Phala Deepika (13th cent CE): planets in 1st/7th/10th/4th houses (12), "
     "Pancha Mahapurusha yoga details (5), special yogas (5), "
     "health/disease (4), yoga cancellation/timing/Graha Yuddha (4).\n\n"
     "**Corpus total: 746 rules**\n\n"
     "### Next session\nS240 — Uttara Kalamrita extended rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1877 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1886 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–238 complete",
     "## Actual Current State (Sessions 1–239 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 238:** Brihat Jataka extended — planetary natures+aspects+yogas+timing; 30 rules; corpus 716; 1877 tests\n"
     "- **Next session:** S239",
     "- **Session 238:** Brihat Jataka extended — planetary natures+aspects+yogas+timing; 30 rules; corpus 716; 1877 tests\n"
     "- **Session 239:** Phala Deepika extended — planets in houses+yogas+health; 30 rules; corpus 746; 1886 tests\n"
     "- **Next session:** S240"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S239" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S239")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
