"""update_docs_s251.py — S251 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S251 — 2026-03-28 — BPHS Graha-Bhava Complete (Exhaustive Planet-in-House)\n\n"
     "**Tests:** 2012 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_graha_bhava_complete.py`: 108 rules (GBC001-GBC108) — "
     "Exhaustive one-rule-per-planet-per-house encoding from BPHS Ch.23-31: "
     "Sun in all 12 houses (GBC001-012), Moon (GBC013-024), Mars (GBC025-036), "
     "Mercury (GBC037-048), Jupiter (GBC049-060), Venus (GBC061-072), "
     "Saturn (GBC073-084), Rahu (GBC085-096), Ketu (GBC097-108). "
     "Each rule captures primary BPHS effects, house quality (Kendra/Trikona/Dusthana/Upachaya), "
     "health significations, relationship indicators, and career themes. "
     "New exhaustive approach: no arbitrary caps — full chapter coverage.\n\n"
     "**Corpus total: 1184 rules**\n\n"
     "### Next session\nS252 — BPHS Yoga Exhaustive (all 500+ yoga combinations from Ch.35-45)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2001 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2012 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–250 complete",
     "## Actual Current State (Sessions 1–251 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 250:** Graha Phala — planets in houses (all 7 planets + Rahu/Ketu, Mangal Dosha, combust); 30 rules; corpus 1076; 2001 tests\n"
     "- **Next session:** S251",
     "- **Session 250:** Graha Phala — planets in houses (all 7 planets + Rahu/Ketu, Mangal Dosha, combust); 30 rules; corpus 1076; 2001 tests\n"
     "- **Session 251:** BPHS Graha-Bhava Complete — exhaustive 9×12 planet-house matrix (GBC001-108); 108 rules; corpus 1184; 2012 tests\n"
     "- **Next session:** S252"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S251" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S251")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
