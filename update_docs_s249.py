"""update_docs_s249.py — S249 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S249 — 2026-03-28 — Bhava Phala (House Results) Extended Rules\n\n"
     "**Tests:** 1990 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bhava_phala_rules.py`: 30 rules (BPH001-BPH030) — "
     "Extended house results from BPHS Ch.11-22 (parashari), "
     "Uttara Kalamrita Ch.4 (kalidasa), Phala Deepika Ch.7 (mantreswara): "
     "All 12 bhava extended significations, Bhavat Bhavam principle, "
     "Upachaya houses (3/6/10/11), Dusthana houses (6/8/12), Trikona houses (1/5/9), "
     "Maraka principle (2nd/7th lords), house occupation effects, "
     "Parivartana between house lords, empty/vacant house rules, "
     "Bhava Chalita, health-body part correlations, specific house combinations.\n\n"
     "**Corpus total: 1046 rules**\n\n"
     "### Next session\nS250 — Planets in houses extended (Graha Phala)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1979 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1990 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–248 complete",
     "## Actual Current State (Sessions 1–249 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 248:** Lagna extended — all 12 lagna profiles/Yogakaraka/Kendra Adhipati/Vargottama; 30 rules; corpus 1016; 1979 tests ✅ 1000+ MILESTONE\n"
     "- **Next session:** S249",
     "- **Session 248:** Lagna extended — all 12 lagna profiles/Yogakaraka/Kendra Adhipati/Vargottama; 30 rules; corpus 1016; 1979 tests ✅ 1000+ MILESTONE\n"
     "- **Session 249:** Bhava Phala extended — all 12 house significations/Upachaya/Dusthana/Maraka; 30 rules; corpus 1046; 1990 tests\n"
     "- **Next session:** S250"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S249" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S249")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
