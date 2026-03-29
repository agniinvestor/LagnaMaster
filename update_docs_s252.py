"""update_docs_s252.py — S252 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S252 — 2026-03-28 — BPHS Yoga Exhaustive (150 rules)\n\n"
     "**Tests:** 2028 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `bphs_yoga_exhaustive.py`: 150 rules (YEX001-YEX150) — "
     "Exhaustive encoding of BPHS Ch.35-56 yoga catalog: "
     "Pancha Mahapurusha (5), Nabhasa yogas — Ashraya/Dala/Sankhya (15+), "
     "Raja Yogas from kendra-trikona lords (11), Dhana Yogas (10), "
     "Neechabhanga Raja Yoga (8 cancellation conditions), "
     "Viparita Raja Yoga — Harsha/Sarala/Vimala (3), "
     "Parivartana yogas (12), Lunar yogas — Sunapha/Anapha/Durudhara/Kemadruma/Gaja-Kesari (10+), "
     "Solar yogas — Veshi/Voshi/Ubhayachari/Budha-Aditya (4), "
     "Named yogas — Saraswati/Lakshmi/Parijata/Mahabhagya/Adhi/Amala/Vasumati (15+), "
     "Sanyasa/Moksha/Pravrajya/Bandhana/Kala Sarpa (8), "
     "Dosha yogas — Mangal/Pitru/Matru/Putra/Vivaha (6), "
     "Graha Bala yogas — all 7 planets (8), Nabhasa patterns (10+).\n\n"
     "**Corpus total: 1334 rules**\n\n"
     "### Next session\nS253 — BPHS Bhava Exhaustive (all 12 houses, deep significations)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2012 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2028 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–251 complete",
     "## Actual Current State (Sessions 1–252 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 251:** BPHS Graha-Bhava Complete — exhaustive 9×12 planet-house matrix (GBC001-108); 108 rules; corpus 1184; 2012 tests\n"
     "- **Next session:** S252",
     "- **Session 251:** BPHS Graha-Bhava Complete — exhaustive 9×12 planet-house matrix (GBC001-108); 108 rules; corpus 1184; 2012 tests\n"
     "- **Session 252:** BPHS Yoga Exhaustive — Ch.35-56, all yoga classes (YEX001-150); 150 rules; corpus 1334; 2028 tests\n"
     "- **Next session:** S253"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S252" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S252")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
