"""update_docs_s279.py — S279 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S279 — 2026-03-30 — Saravali Conjunctions Part 7: Jupiter-Venus, Jupiter-Saturn, Venus-Saturn\n\n"
     "**Tests:** 2441 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "- `src/corpus/saravali_conjunctions_7.py`: SARAVALI_CONJUNCTIONS_7_REGISTRY (130 rules SAV781-SAV910)\n"
     "  - Jupiter-Venus: supreme beneficence; Jupiter-Saturn: dharma vs karma; Venus-Saturn: artistic discipline\n\n"
     "**Corpus:** 4597 rules\n\n### Next session\nS280 — Three+ planet conjunctions (Block A complete)\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 278:** Saravali Conjunctions 6 (Mercury-Jupiter/Venus/Saturn) — SAV651-780; "
     "corpus 4467; 2434 tests\n- **Next session:** S279",
     "- **Session 278:** Saravali Conjunctions 6 (Mercury-Jupiter/Venus/Saturn) — SAV651-780; "
     "corpus 4467; 2434 tests\n"
     "- **Session 279:** Saravali Conjunctions 7 (Jupiter-Venus/Saturn, Venus-Saturn) — SAV781-910; "
     "corpus 4597; 2441 tests\n- **Next session:** S280"),
    (ROOT / "docs/MEMORY.md",
     "- **2434 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2441 passing, 3 skipped, 0 lint errors, CI green**"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S279" not in text: doc.write_text(text.rstrip() + new)
    elif old in text: doc.write_text(text.replace(old, new, 1))
cmap = ROOT / "docs/coverage_maps/saravali.md"
ct = cmap.read_text()
for o, n in [
    ("| A7 | Ch.21–22 | Jupiter-Venus, Jupiter-Saturn, Venus-Saturn | ~130 | S279 | 🔲 |",
     "| A7 | Ch.21–22 | Jupiter-Venus, Jupiter-Saturn, Venus-Saturn | ~130 | S279 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **780/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **910/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **780/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **910/4100** |"),
]:
    if o in ct: ct = ct.replace(o, n, 1)
cmap.write_text(ct)
print("done")
