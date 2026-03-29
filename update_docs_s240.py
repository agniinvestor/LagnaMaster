"""update_docs_s240.py — S240 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S240 — 2026-03-28 — Uttara Kalamrita Extended Rules\n\n"
     "**Tests:** 1895 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `uttara_kalamrita_ext.py`: 30 rules (UKE001-UKE030) — "
     "Kalidasa's Uttara Kalamrita (17th cent CE): all 12 house extended significations (12), "
     "all 9 planetary gemstones/directions/deities (9), bhavat bhavam, kartari yogas, "
     "combustion degrees, retrograde strength, temporal malefic/benefic classification (9).\n\n"
     "**Corpus total: 776 rules**\n\n"
     "### Next session\nS241 — Jataka Parijata extended rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1886 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1895 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–239 complete",
     "## Actual Current State (Sessions 1–240 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 239:** Phala Deepika extended — planets in houses+yogas+health; 30 rules; corpus 746; 1886 tests\n"
     "- **Next session:** S240",
     "- **Session 239:** Phala Deepika extended — planets in houses+yogas+health; 30 rules; corpus 746; 1886 tests\n"
     "- **Session 240:** Uttara Kalamrita extended — house+planet significations+principles; 30 rules; corpus 776; 1895 tests\n"
     "- **Next session:** S241"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S240" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S240")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
