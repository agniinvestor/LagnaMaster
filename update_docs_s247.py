"""update_docs_s247.py — S247 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S247 — 2026-03-28 — Extended Yoga Rules\n\n"
     "**Tests:** 1969 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `yoga_extended_rules.py`: 30 rules (YGE001-YGE030) — "
     "Extended yoga rules from BPHS Ch.35-45 (parashari), "
     "Phala Deepika Ch.6 (mantreswara), Brihat Jataka Ch.12 (varahamihira): "
     "All 5 Pancha Mahapurusha yogas (Ruchaka/Bhadra/Hamsa/Malavya/Shasha), "
     "Nabhasa yogas (Rajju/Musala/Nala/Mala/Sarpa/Shula/Yava/Kamala), "
     "Viparita Raja Yoga, Mahabhagya, Parijata, Kesari, Amala, "
     "Lakshmi, Saraswati, Kahala, Chandra-Mangala Dhana yogas, "
     "Pravrajya/Moksha/Sanyasa/Bandhana spiritual yogas, "
     "Anapha/Sunapha/Durudhara Moon yogas, Kartari Yoga.\n\n"
     "**Corpus total: 986 rules**\n\n"
     "### Next session\nS248 — Lagna (Ascendant) extended rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1958 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1969 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–246 complete",
     "## Actual Current State (Sessions 1–247 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 246:** Dasha systems — Vimshottari/Ashtottari/Yogini/Kalachakra/Maraka/planet results; 30 rules; corpus 956; 1958 tests\n"
     "- **Next session:** S247",
     "- **Session 246:** Dasha systems — Vimshottari/Ashtottari/Yogini/Kalachakra/Maraka/planet results; 30 rules; corpus 956; 1958 tests\n"
     "- **Session 247:** Extended yoga rules — Pancha Mahapurusha/Nabhasa/Viparita/Moon yogas/Kartari; 30 rules; corpus 986; 1969 tests\n"
     "- **Next session:** S248"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S247" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S247")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
