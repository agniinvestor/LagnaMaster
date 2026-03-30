"""update_docs_s276.py — S276 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S276 — 2026-03-30 — Saravali Conjunctions Part 4: Moon-Venus, Moon-Saturn, Mars-Mercury\n\n"
     "**Tests:** 2420 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_4.py`: SARAVALI_CONJUNCTIONS_4_REGISTRY (130 rules SAV391-SAV520)\n"
     "  - Moon-Venus: romantic/artistic luxury; Moon-Saturn: Vish yoga, melancholy; Mars-Mercury: technical skills\n\n"
     "**Corpus:** 4207 rules\n\n### Next session\nS277\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 275:** Saravali Conjunctions 3 (Moon-Mars/Mercury/Jupiter) — SAV261-390; "
     "corpus 4077; 2413 tests\n- **Next session:** S276",
     "- **Session 275:** Saravali Conjunctions 3 (Moon-Mars/Mercury/Jupiter) — SAV261-390; "
     "corpus 4077; 2413 tests\n"
     "- **Session 276:** Saravali Conjunctions 4 (Moon-Venus/Saturn, Mars-Mercury) — SAV391-520; "
     "corpus 4207; 2420 tests\n- **Next session:** S277"),
    (ROOT / "docs/MEMORY.md",
     "- **2413 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2420 passing, 3 skipped, 0 lint errors, CI green**"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S276" not in text:
            doc.write_text(text.rstrip() + new)
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| A4 | Ch.18–19 | Moon-Venus, Moon-Saturn, Mars-Mercury conjunctions | ~130 | S276 | 🔲 |",
     "| A4 | Ch.18–19 | Moon-Venus, Moon-Saturn, Mars-Mercury conjunctions | ~130 | S276 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **390/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **520/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **390/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **520/4100** |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
