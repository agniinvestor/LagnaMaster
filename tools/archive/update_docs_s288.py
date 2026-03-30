"""update_docs_s288.py — S285-S288 documentation sync (batch)."""
from pathlib import Path
ROOT = Path(__file__).parent

cl = ROOT / "docs/CHANGELOG.md"
cl_text = cl.read_text()
entry = (
    "\n---\n\n## S285–S288 — 2026-03-30 — Saravali Block B Complete: All planets in 12 signs\n\n"
    "**Tests:** 2482 passing, 3 skipped, 0 lint errors\n\n"
    "### What was built\n"
    "Four planet-in-sign modules at EXHAUSTIVE depth (572 rules total):\n"
    "- `saravali_signs_5.py` (S285): Jupiter in 12 signs — SAV1561-1702 (142 rules, Ch.29)\n"
    "- `saravali_signs_6.py` (S286): Venus in 12 signs — SAV1703-1861 (159 rules, Ch.30)\n"
    "- `saravali_signs_7.py` (S287): Saturn in 12 signs — SAV1862-2002 (141 rules, Ch.31)\n"
    "- `saravali_signs_8.py` (S288): Rahu+Ketu in 12 signs — SAV2003-2132 (130 rules, Ch.32-33)\n\n"
    "Rule counts are now driven by text depth, not session targets.\n\n"
    "**Block B COMPLETE:** 1,092 actual rules (was estimated ~1,050)\n\n"
    "**Corpus:** 5819 rules\n\n### Next session\nS289 — Block C: Sun in 12 houses\n"
)
if "## S285" not in cl_text:
    cl.write_text(cl_text.rstrip() + entry)

mem = ROOT / "docs/MEMORY.md"
mt = mem.read_text()
mt = mt.replace(
    "- **Sessions 281-284:** Saravali Signs Sun/Moon/Mars/Mercury — SAV1041-1560; "
    "corpus 5247; 2477 tests\n- **Next session:** S285",
    "- **Sessions 281-284:** Saravali Signs Sun/Moon/Mars/Mercury — SAV1041-1560; "
    "corpus 5247; 2477 tests\n"
    "- **Sessions 285-288:** Saravali Signs Jupiter/Venus/Saturn/Rahu-Ketu — SAV1561-2132; "
    "corpus 5819; 2482 tests — **Block B COMPLETE (1092 actual)**\n- **Next session:** S289", 1)
mt = mt.replace(
    "- **2477 passing, 3 skipped, 0 lint errors, CI green**",
    "- **2482 passing, 3 skipped, 0 lint errors, CI green**", 1)
mem.write_text(mt)

cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| B5 | Ch.29 | Jupiter in 12 signs | ~130 | S285 | 🔲 |",
     "| B5 | Ch.29 | Jupiter in 12 signs | 142 | S285 | ✅ |"),
    ("| B6 | Ch.30 | Venus in 12 signs | ~130 | S286 | 🔲 |",
     "| B6 | Ch.30 | Venus in 12 signs | 159 | S286 | ✅ |"),
    ("| B7 | Ch.31 | Saturn in 12 signs | ~130 | S287 | 🔲 |",
     "| B7 | Ch.31 | Saturn in 12 signs | 141 | S287 | ✅ |"),
    ("| B8 | Ch.32–33 | Rahu/Ketu in 12 signs | ~140 | S288 | 🔲 |",
     "| B8 | Ch.32–33 | Rahu/Ketu in 12 signs | 130 | S288 | ✅ |"),
    ("| **TOTAL B** | | | **~1,050** | **S281–S288** | **520/1050** |",
     "| **TOTAL B** | | | **1,092** | **S281–S288** | **1092/1092 ✅** |"),
    ("| B — Planet-in-Sign | S281–S288 | ~1,050 | 520/1050 |",
     "| B — Planet-in-Sign | S281–S288 | 1,092 | 1092/1092 ✅ |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **1560/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **2132/4100** |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
