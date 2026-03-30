"""update_docs_s284.py — S281-S284 documentation sync (batch)."""
from pathlib import Path
ROOT = Path(__file__).parent

# Batch update for S281-S284
cl = ROOT / "docs/CHANGELOG.md"
cl_text = cl.read_text()
entry = (
    "\n---\n\n## S281–S284 — 2026-03-30 — Saravali Block B (Part 1): Sun/Moon/Mars/Mercury in 12 signs\n\n"
    "**Tests:** 2477 passing, 3 skipped, 0 lint errors\n\n"
    "### What was built\n"
    "Four planet-in-sign modules (520 rules total):\n"
    "- `saravali_signs_1.py` (S281): Sun in 12 signs — SAV1041-1170 (Ch.25)\n"
    "- `saravali_signs_2.py` (S282): Moon in 12 signs — SAV1171-1300 (Ch.26)\n"
    "- `saravali_signs_3.py` (S283): Mars in 12 signs — SAV1301-1430 (Ch.27)\n"
    "- `saravali_signs_4.py` (S284): Mercury in 12 signs — SAV1431-1560 (Ch.28)\n\n"
    "**Corpus:** 5247 rules\n\n### Next session\nS285 — Jupiter in 12 signs\n"
)
if "## S281" not in cl_text:
    cl.write_text(cl_text.rstrip() + entry)

mem = ROOT / "docs/MEMORY.md"
mem_text = mem.read_text()
mem_text = mem_text.replace(
    "- **Session 280:** Saravali Conjunctions 8 (3+ planet) — SAV911-1040; "
    "corpus 4727; 2449 tests — **Block A COMPLETE (1040/1040)**\n- **Next session:** S281",
    "- **Session 280:** Saravali Conjunctions 8 (3+ planet) — SAV911-1040; "
    "corpus 4727; 2449 tests — **Block A COMPLETE (1040/1040)**\n"
    "- **Sessions 281-284:** Saravali Signs Sun/Moon/Mars/Mercury — SAV1041-1560; "
    "corpus 5247; 2477 tests\n- **Next session:** S285",
    1)
mem_text = mem_text.replace(
    "- **2449 passing, 3 skipped, 0 lint errors, CI green**",
    "- **2477 passing, 3 skipped, 0 lint errors, CI green**",
    1)
mem.write_text(mem_text)

cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| B1 | Ch.25 | Sun in 12 signs | ~130 | S281 | 🔲 |",
     "| B1 | Ch.25 | Sun in 12 signs | ~130 | S281 | ✅ |"),
    ("| B2 | Ch.26 | Moon in 12 signs | ~130 | S282 | 🔲 |",
     "| B2 | Ch.26 | Moon in 12 signs | ~130 | S282 | ✅ |"),
    ("| B3 | Ch.27 | Mars in 12 signs | ~130 | S283 | 🔲 |",
     "| B3 | Ch.27 | Mars in 12 signs | ~130 | S283 | ✅ |"),
    ("| B4 | Ch.28 | Mercury in 12 signs | ~130 | S284 | 🔲 |",
     "| B4 | Ch.28 | Mercury in 12 signs | ~130 | S284 | ✅ |"),
    ("| **TOTAL B** | | | **~1,050** | **S281–S288** | **0/1050** |",
     "| **TOTAL B** | | | **~1,050** | **S281–S288** | **520/1050** |"),
    ("| B — Planet-in-Sign | S281–S288 | ~1,050 | 0/1050 |",
     "| B — Planet-in-Sign | S281–S288 | ~1,050 | 520/1050 |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **1040/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **1560/4100** |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
