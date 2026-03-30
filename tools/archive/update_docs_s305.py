"""update_docs_s305.py — S297-S305 documentation sync (Block D + Saravali complete)."""
from pathlib import Path
ROOT = Path(__file__).parent

cl = ROOT / "docs/CHANGELOG.md"
ct = cl.read_text()
if "## S297" not in ct:
    cl.write_text(ct.rstrip() + (
        "\n---\n\n## S297–S305 — 2026-03-30 — Saravali Block D Complete: Special Topics (SARAVALI COMPLETE)\n\n"
        "**Tests:** 2501 passing, 3 skipped, 0 lint errors\n\n"
        "### What was built\n"
        "Nine special topic modules (270 rules total):\n"
        "- D1 (S297): Planet natures, signs, houses — 45 rules (Ch.1-5)\n"
        "- D2 (S298): Longevity, Arishta, Ayurdaya — 32 rules (Ch.6-8)\n"
        "- D3 (S299): Raja Yogas, Ava Yogas — 30 rules (Ch.9-10)\n"
        "- D4 (S300): Nabhasa/Solar/Lunar/Chandra Yogas — 38 rules (Ch.11-14)\n"
        "- D5 (S301): Bhava effects detailed — 30 rules (Ch.43-48)\n"
        "- D6 (S302): Female horoscopy, Marriage, Progeny — 28 rules (Ch.49-53)\n"
        "- D7 (S303): Dasha results, AV, Transits — 23 rules (Ch.54-60)\n"
        "- D8 (S304): Death, Lost horoscopy, Drekkana — 20 rules (Ch.61-65)\n"
        "- D9 (S305): Nimitta, Planetary war, Summary — 24 rules (Ch.66-68)\n\n"
        "**SARAVALI COMPLETE:** 2,898 total rules across all 68 chapters\n"
        "  - Block A (Conjunctions): 1,040 rules\n"
        "  - Block B (Planet-in-Sign): 1,092 rules\n"
        "  - Block C (Planet-in-House): 496 rules\n"
        "  - Block D (Special Topics): 270 rules\n\n"
        "**Corpus:** 6,585 rules\n\n### Next session\nS306 — Chamatkara Chintamani\n"
    ))

mem = ROOT / "docs/MEMORY.md"
mt = mem.read_text()
mt = mt.replace(
    "- **Sessions 289-296:** Saravali Houses all planets — SAV2133-2628; "
    "corpus 6315; 2491 tests — **Block C COMPLETE (496 actual)**\n- **Next session:** S297",
    "- **Sessions 289-296:** Saravali Houses all planets — SAV2133-2628; "
    "corpus 6315; 2491 tests — **Block C COMPLETE (496 actual)**\n"
    "- **Sessions 297-305:** Saravali Special Topics — SAV2629-2898; "
    "corpus 6585; 2501 tests — **SARAVALI COMPLETE (2898 rules, all 68 chapters)**\n- **Next session:** S306", 1)
mt = mt.replace(
    "- **2491 passing, 3 skipped, 0 lint errors, CI green**",
    "- **2501 passing, 3 skipped, 0 lint errors, CI green**", 1)
mem.write_text(mt)

cmap = ROOT / "docs/coverage_maps/saravali.md"
ct2 = cmap.read_text()
for o, n in [
    ("| D1 | Ch.1–5 | Planet natures, signs, houses, basics | ~100 | S297 | 🔲 |", "| D1 | Ch.1–5 | Planet natures, signs, houses, basics | 45 | S297 | ✅ |"),
    ("| D2 | Ch.6–8 | Longevity, Arishta (infant death), Ayurdaya | ~130 | S298 | 🔲 |", "| D2 | Ch.6–8 | Longevity, Arishta, Ayurdaya | 32 | S298 | ✅ |"),
    ("| D3 | Ch.9–10 | Raja Yogas, Ava Yogas | ~130 | S299 | 🔲 |", "| D3 | Ch.9–10 | Raja Yogas, Ava Yogas | 30 | S299 | ✅ |"),
    ("| D4 | Ch.11–14 | Nabhasa Yogas, Solar/Lunar Yogas, Chandra Yogas | ~130 | S300 | 🔲 |", "| D4 | Ch.11–14 | Nabhasa/Solar/Lunar/Chandra Yogas | 38 | S300 | ✅ |"),
    ("| D5 | Ch.43–48 | Effects of Bhavas (detailed house results) | ~130 | S301 | 🔲 |", "| D5 | Ch.43–48 | Bhava effects detailed | 30 | S301 | ✅ |"),
    ("| D6 | Ch.49–53 | Female horoscopy, Marriage, Progeny | ~120 | S302 | 🔲 |", "| D6 | Ch.49–53 | Female horoscopy, Marriage, Progeny | 28 | S302 | ✅ |"),
    ("| D7 | Ch.54–60 | Dasha results, Ashtakavarga, Transits | ~130 | S303 | 🔲 |", "| D7 | Ch.54–60 | Dasha results, AV, Transits | 23 | S303 | ✅ |"),
    ("| D8 | Ch.61–65 | Death circumstances, Lost horoscopy, Drekkana | ~100 | S304 | 🔲 |", "| D8 | Ch.61–65 | Death, Lost horoscopy, Drekkana | 20 | S304 | ✅ |"),
    ("| D9 | Ch.66–68 | Misc: Nimitta (omens), Planetary war, Summary | ~90 | S305 | 🔲 |", "| D9 | Ch.66–68 | Nimitta, Planetary war, Summary | 24 | S305 | ✅ |"),
    ("| **TOTAL D** | | | **~960** | **S297–S305** | **0/960** |", "| **TOTAL D** | | | **270** | **S297–S305** | **270/270 ✅** |"),
    ("| D — Special Topics | S297–S305 | ~960 | 0/960 |", "| D — Special Topics | S297–S305 | 270 | 270/270 ✅ |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **2628/4100** |", "| **TOTAL** | **S273–S305** | **2,898** | **2898/2898 ✅** |"),
]:
    if o in ct2: ct2 = ct2.replace(o, n, 1)
cmap.write_text(ct2)
print("done")
