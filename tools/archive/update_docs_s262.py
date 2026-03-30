"""update_docs_s262.py — S262 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S262 — 2026-03-30 — Phaladeepika Exhaustive (120 rules)\n\n"
     "**Tests:** 2227 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `phaladeepika_exhaustive.py`: 120 rules (PHX001-PHX120) — "
     "Exhaustive encoding of Mantreswara's Phaladeepika (14th century CE): "
     "All 9 planet natures with element/dosha/gem/direction/deity, "
     "all 12 rashi characteristics, complete dignity system (exaltation/debilitation/"
     "Moolatrikona/own signs/Neecha Bhanga/Vargottama/combustion/retrograde/Dig Bala), "
     "all 12 house significations, Raja/Dhana/Arishta yogas (Kendra-Trikona/Yoga Karaka/"
     "Pancha Mahapurusha/Gaja Kesari/Budha-Aditya/Viparita Raja/Daridra/Kemadruma/Adhi/"
     "Anapha-Sunapha/Shakata/Lakshmi/Saraswati/Parivartana/Mahabhagya), "
     "longevity/medical/marriage/children/career analysis, "
     "Vimshottari dasha results, Gochara/Sade Sati/Ashtama Shani, "
     "Shodashavarga divisional charts (D2/D3/D7/D9/D10/D12/D30), "
     "Ashtakavarga/Shadbala/Bhava Bala/Ishta-Kashta Phala, "
     "Panchanga/Muhurta nakshatras, three-chart synthesis, karma/free will philosophy, "
     "Jyotisham Vedachakshu (astrology as eye of the Vedas).\n\n"
     "**Corpus total: 2634 rules**\n\n"
     "### Next session\nS263 — BPHS Uncovered Chapters (~120 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2206 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2227 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–261 complete",
     "## Actual Current State (Sessions 1–262 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 261:** Chandra Kala Nadi Exhaustive — Deva Keralam (CKN001-120); 120 rules; corpus 2514; 2206 tests\n"
     "- **Next session:** S262",
     "- **Session 261:** Chandra Kala Nadi Exhaustive — Deva Keralam (CKN001-120); 120 rules; corpus 2514; 2206 tests\n"
     "- **Session 262:** Phaladeepika Exhaustive — Mantreswara 14th century (PHX001-120); 120 rules; corpus 2634; 2227 tests\n"
     "- **Next session:** S263"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S262" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S262")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
