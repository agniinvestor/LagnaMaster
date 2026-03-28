"""update_docs_s250.py — S250 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S250 — 2026-03-28 — Graha Phala (Planets in Houses) Rules\n\n"
     "**Tests:** 2001 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `graha_phala_rules.py`: 30 rules (GPH001-GPH030) — "
     "Planet-in-house effects from BPHS Ch.23-31 (parashari), "
     "Phala Deepika Ch.3 (mantreswara), Brihat Jataka Ch.2 (varahamihira): "
     "Sun in all houses (Kendra/Trikona/Dusthana), Moon (waxing/waning effects), "
     "Mars (Mangal Dosha 1/4/7, Upachaya 3/6/11), Mercury (intellect/communication), "
     "Jupiter (wisdom/prosperity in all houses), Venus (beauty/happiness), "
     "Saturn (discipline/delay, excellent in Upachaya), Rahu/Ketu in houses, "
     "combust planets (Asta), exalted in dusthana, debilitated in Kendra, Swakshetra.\n\n"
     "**Corpus total: 1076 rules**\n\n"
     "### Next session\nS251 — Remedies and Upayas (classical astrological remedies)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1990 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2001 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–249 complete",
     "## Actual Current State (Sessions 1–250 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 249:** Bhava Phala extended — all 12 house significations/Upachaya/Dusthana/Maraka; 30 rules; corpus 1046; 1990 tests\n"
     "- **Next session:** S250",
     "- **Session 249:** Bhava Phala extended — all 12 house significations/Upachaya/Dusthana/Maraka; 30 rules; corpus 1046; 1990 tests\n"
     "- **Session 250:** Graha Phala — planets in houses (all 7 planets + Rahu/Ketu, Mangal Dosha, combust); 30 rules; corpus 1076; 2001 tests\n"
     "- **Next session:** S251"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S250" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S250")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
