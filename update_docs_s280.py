"""update_docs_s280.py — S280 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S280 — 2026-03-30 — Saravali Conjunctions Part 8: Three+ planet conjunctions\n\n"
     "**Tests:** 2449 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_8.py`: SARAVALI_CONJUNCTIONS_8_REGISTRY (130 rules SAV911-SAV1040)\n"
     "  - 80 three-planet conjunction rules (15 groups × 5 rules + 5 general)\n"
     "  - 30 four+ planet stellium rules\n"
     "  - 20 special conditions (graha yuddha, combustion, retrograde, sandhi, gandanta, nodes)\n\n"
     "**Block A COMPLETE:** 1,040/1,040 conjunction rules (SAV001-SAV1040)\n\n"
     "**Corpus:** 4727 rules\n\n### Next session\nS281 — Block B: Sun in 12 signs\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 279:** Saravali Conjunctions 7 (Jupiter-Venus/Saturn, Venus-Saturn) — SAV781-910; "
     "corpus 4597; 2441 tests\n- **Next session:** S280",
     "- **Session 279:** Saravali Conjunctions 7 (Jupiter-Venus/Saturn, Venus-Saturn) — SAV781-910; "
     "corpus 4597; 2441 tests\n"
     "- **Session 280:** Saravali Conjunctions 8 (3+ planet) — SAV911-1040; "
     "corpus 4727; 2449 tests — **Block A COMPLETE (1040/1040)**\n- **Next session:** S281"),
    (ROOT / "docs/MEMORY.md",
     "- **2441 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2449 passing, 3 skipped, 0 lint errors, CI green**"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S280" not in text: doc.write_text(text.rstrip() + new)
    elif old in text: doc.write_text(text.replace(old, new, 1))
cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| A8 | Ch.23–24 | Three+ planet conjunctions, special combinations | ~130 | S280 | 🔲 |",
     "| A8 | Ch.23–24 | Three+ planet conjunctions, special combinations | ~130 | S280 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **910/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **1040/1040 ✅** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **910/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **1040/4100** |"),
    ("| A — Conjunctions | S273–S280 | ~1,040 | 0/1040 |",
     "| A — Conjunctions | S273–S280 | ~1,040 | 1040/1040 ✅ |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
