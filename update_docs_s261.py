"""update_docs_s261.py — S261 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S261 — 2026-03-29 — Chandra Kala Nadi Exhaustive (120 rules)\n\n"
     "**Tests:** 2206 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `chandra_kala_nadi_rules.py`: 120 rules (CKN001-CKN120) — "
     "Exhaustive encoding of Chandra Kala Nadi (Deva Keralam), Tamil Nadi text: "
     "All 27 nakshatra Moon results in 1st house with unique CKN interpretations, "
     "9 Tara system (Janma/Sampat/Vipat/Kshema/Pratyak/Sadhana/Naidhana/Mitra/Parama Mitra), "
     "complete transit (Gochara) analysis by nakshatra, "
     "Vimshottari Dasha results modified by natal Moon nakshatra for all 9 planets, "
     "nakshatra-level yoga combinations (Nakshatra Sandhi, Raja Yoga, Parivartana), "
     "Gandanta nakshatra analysis (3 junction points), "
     "Nakshatra Pada (quarter) analysis, Pushkara Navamsha, "
     "medical analysis by nakshatra, Chandravela muhurta system, "
     "Abhijit nakshatra, Yogi/Avayogi, Nakshatra Shadbala, "
     "philosophy of Nadi astrology (27 nakshatras = cosmic alphabet).\n\n"
     "**Corpus total: 2514 rules**\n\n"
     "### Next session\nS262 — Phaladeepika Exhaustive (~120 rules)\n"),
    (ROOT/"docs/MEMORY.md",
     "- **2185 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2206 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–260 complete",
     "## Actual Current State (Sessions 1–261 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Session 260:** Lal Kitab Exhaustive — 1939-1952 editions (LKX001-120); 120 rules; corpus 2394; 2185 tests\n"
     "- **Next session:** S261",
     "- **Session 260:** Lal Kitab Exhaustive — 1939-1952 editions (LKX001-120); 120 rules; corpus 2394; 2185 tests\n"
     "- **Session 261:** Chandra Kala Nadi Exhaustive — Deva Keralam (CKN001-120); 120 rules; corpus 2514; 2206 tests\n"
     "- **Next session:** S262"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S261" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S261")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
