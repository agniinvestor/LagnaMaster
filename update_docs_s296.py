"""update_docs_s296.py — S289-S296 documentation sync (Block C complete)."""
from pathlib import Path
ROOT = Path(__file__).parent

cl = ROOT / "docs/CHANGELOG.md"
ct = cl.read_text()
if "## S289" not in ct:
    cl.write_text(ct.rstrip() + (
        "\n---\n\n## S289–S296 — 2026-03-30 — Saravali Block C Complete: All planets in 12 houses\n\n"
        "**Tests:** 2491 passing, 3 skipped, 0 lint errors\n\n"
        "### What was built\n"
        "Eight planet-in-house modules at exhaustive depth (496 rules total):\n"
        "- `saravali_houses_1.py` (S289): Sun in 12 houses — 68 rules (Ch.34)\n"
        "- `saravali_houses_2.py` (S290): Moon in 12 houses — 60 rules (Ch.35)\n"
        "- `saravali_houses_3.py` (S291): Mars in 12 houses — 57 rules (Ch.36)\n"
        "- `saravali_houses_4.py` (S292): Mercury in 12 houses — 57 rules (Ch.37)\n"
        "- `saravali_houses_5.py` (S293): Jupiter in 12 houses — 60 rules (Ch.38)\n"
        "- `saravali_houses_6.py` (S294): Venus in 12 houses — 56 rules (Ch.39)\n"
        "- `saravali_houses_7.py` (S295): Saturn in 12 houses — 57 rules (Ch.40)\n"
        "- `saravali_houses_8.py` (S296): Rahu+Ketu in 12 houses — 81 rules (Ch.41-42)\n\n"
        "**Block C COMPLETE:** 496 actual rules\n\n"
        "**Corpus:** 6315 rules\n\n### Next session\nS297 — Block D: Special Topics\n"
    ))

mem = ROOT / "docs/MEMORY.md"
mt = mem.read_text()
mt = mt.replace(
    "- **Sessions 285-288:** Saravali Signs Jupiter/Venus/Saturn/Rahu-Ketu — SAV1561-2132; "
    "corpus 5819; 2482 tests — **Block B COMPLETE (1092 actual)**\n- **Next session:** S289",
    "- **Sessions 285-288:** Saravali Signs Jupiter/Venus/Saturn/Rahu-Ketu — SAV1561-2132; "
    "corpus 5819; 2482 tests — **Block B COMPLETE (1092 actual)**\n"
    "- **Sessions 289-296:** Saravali Houses all planets — SAV2133-2628; "
    "corpus 6315; 2491 tests — **Block C COMPLETE (496 actual)**\n- **Next session:** S297", 1)
mt = mt.replace(
    "- **2482 passing, 3 skipped, 0 lint errors, CI green**",
    "- **2491 passing, 3 skipped, 0 lint errors, CI green**", 1)
mem.write_text(mt)

cmap = ROOT / "docs/coverage_maps/saravali.md"
ct2 = cmap.read_text()
for o, n in [
    ("| C1 | Ch.34 | Sun in 12 houses | ~130 | S289 | 🔲 |", "| C1 | Ch.34 | Sun in 12 houses | 68 | S289 | ✅ |"),
    ("| C2 | Ch.35 | Moon in 12 houses | ~130 | S290 | 🔲 |", "| C2 | Ch.35 | Moon in 12 houses | 60 | S290 | ✅ |"),
    ("| C3 | Ch.36 | Mars in 12 houses | ~130 | S291 | 🔲 |", "| C3 | Ch.36 | Mars in 12 houses | 57 | S291 | ✅ |"),
    ("| C4 | Ch.37 | Mercury in 12 houses | ~130 | S292 | 🔲 |", "| C4 | Ch.37 | Mercury in 12 houses | 57 | S292 | ✅ |"),
    ("| C5 | Ch.38 | Jupiter in 12 houses | ~130 | S293 | 🔲 |", "| C5 | Ch.38 | Jupiter in 12 houses | 60 | S293 | ✅ |"),
    ("| C6 | Ch.39 | Venus in 12 houses | ~130 | S294 | 🔲 |", "| C6 | Ch.39 | Venus in 12 houses | 56 | S294 | ✅ |"),
    ("| C7 | Ch.40 | Saturn in 12 houses | ~130 | S295 | 🔲 |", "| C7 | Ch.40 | Saturn in 12 houses | 57 | S295 | ✅ |"),
    ("| C8 | Ch.41–42 | Rahu/Ketu in 12 houses | ~140 | S296 | 🔲 |", "| C8 | Ch.41–42 | Rahu/Ketu in 12 houses | 81 | S296 | ✅ |"),
    ("| **TOTAL C** | | | **~1,050** | **S289–S296** | **0/1050** |", "| **TOTAL C** | | | **496** | **S289–S296** | **496/496 ✅** |"),
    ("| C — Planet-in-House | S289–S296 | ~1,050 | 0/1050 |", "| C — Planet-in-House | S289–S296 | 496 | 496/496 ✅ |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **2132/4100** |", "| **TOTAL** | **S273–S305** | **~4,100** | **2628/4100** |"),
]:
    if o in ct2: ct2 = ct2.replace(o, n, 1)
cmap.write_text(ct2)
print("done")
