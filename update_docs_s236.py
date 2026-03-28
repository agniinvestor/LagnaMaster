"""update_docs_s236.py — S236 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S236 — 2026-03-28 — BPHS Bhava Karakas\n\n"
     "**Tests:** 1860 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_bhava_karakas.py`: 30 rules (BHK001-BHK030) — "
     "Naisargika karakas for all 12 houses (12 rules), Jaimini Chara Karakas "
     "AK/AmK/BK/MK/PK/GK/DK (8 rules), special karaka rules including "
     "Karaka-Bhava-Nashta, gender-based spouse karakas, dasha activation (10 rules).\n\n"
     "**Corpus total: 656 rules**\n\n"
     "### Next session\nS237 — Varga chart rules (D9 Navamsha + D10 Dashamsha)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1851 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1860 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–235 complete",
     "## Actual Current State (Sessions 1–236 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 235:** Nakshatra rules p2 — nakshatras 15-27 + Moon; 26 rules; corpus 626; 1851 tests\n"
     "- **Next session:** S236",
     "- **Session 235:** Nakshatra rules p2 — nakshatras 15-27 + Moon; 26 rules; corpus 626; 1851 tests\n"
     "- **Session 236:** Bhava karakas — naisargika+Jaimini chara+special; 30 rules; corpus 656; 1860 tests\n"
     "- **Next session:** S237"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S236" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S236")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
