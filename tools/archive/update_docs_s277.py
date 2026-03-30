"""update_docs_s277.py — S277 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S277 — 2026-03-30 — Saravali Conjunctions Part 5: Mars-Jupiter, Mars-Venus, Mars-Saturn\n\n"
     "**Tests:** 2427 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_5.py`: SARAVALI_CONJUNCTIONS_5_REGISTRY (130 rules SAV521-SAV650)\n"
     "  - Mars-Jupiter: dharma-karma warrior; Mars-Venus: passionate intensity; Mars-Saturn: most malefic pair\n\n"
     "**Corpus:** 4337 rules\n\n### Next session\nS278\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 276:** Saravali Conjunctions 4 (Moon-Venus/Saturn, Mars-Mercury) — SAV391-520; "
     "corpus 4207; 2420 tests\n- **Next session:** S277",
     "- **Session 276:** Saravali Conjunctions 4 (Moon-Venus/Saturn, Mars-Mercury) — SAV391-520; "
     "corpus 4207; 2420 tests\n"
     "- **Session 277:** Saravali Conjunctions 5 (Mars-Jupiter/Venus/Saturn) — SAV521-650; "
     "corpus 4337; 2427 tests\n- **Next session:** S278"),
    (ROOT / "docs/MEMORY.md",
     "- **2420 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2427 passing, 3 skipped, 0 lint errors, CI green**"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S277" not in text:
            doc.write_text(text.rstrip() + new)
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| A5 | Ch.19–20 | Mars-Jupiter, Mars-Venus, Mars-Saturn conjunctions | ~130 | S277 | 🔲 |",
     "| A5 | Ch.19–20 | Mars-Jupiter, Mars-Venus, Mars-Saturn conjunctions | ~130 | S277 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **520/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **650/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **520/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **650/4100** |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
