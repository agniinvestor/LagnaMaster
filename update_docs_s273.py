"""update_docs_s273.py — S273 documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent

patches = [
    (ROOT / "docs/CHANGELOG.md", None,
     "\n---\n\n## S273 — 2026-03-30 — Saravali Conjunctions Part 1: Sun-Moon, Sun-Mars, Sun-Mercury\n\n"
     "**Tests:** 2393 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "Saravali sutra-level re-encode begins. Coverage map created for all 68 chapters.\n"
     "First conjunction batch — 130 rules (SAV001-SAV130):\n\n"
     "- `src/corpus/saravali_conjunctions_1.py`: SARAVALI_CONJUNCTIONS_1_REGISTRY\n"
     "  - Sun-Moon conjunction (Ch.15, 43 rules): house placements + waxing/waning/sign modifiers\n"
     "  - Sun-Mars conjunction (Ch.16, 43 rules): fiery/martial outcomes per house + dignity conditions\n"
     "  - Sun-Mercury conjunction (Ch.16-17, 44 rules): Budhaditya yoga, combust vs cazimi\n"
     "- phase=1B_compound, lagna_scope=[] (universal), source=Saravali\n"
     "- Coverage map: docs/coverage_maps/saravali.md — 4 blocks, ~4,100 rules planned\n"
     "- Wired into combined_corpus.py.\n\n"
     "**Corpus:** 3817 rules (3687 + 130)\n\n"
     "### Next session\nS274 — Saravali Conjunctions Part 2: Sun-Jupiter, Sun-Venus, Sun-Saturn\n"),
    (ROOT / "docs/MEMORY.md",
     "- **Session 272:** Bhavartha Ratnakara Aquarius + Pisces — BVR651-780; "
     "corpus 3687; 2379 tests — **BVR COMPLETE (780/780)**\n"
     "- **Next session:** S273",
     "- **Session 272:** Bhavartha Ratnakara Aquarius + Pisces — BVR651-780; "
     "corpus 3687; 2379 tests — **BVR COMPLETE (780/780)**\n"
     "- **Session 273:** Saravali Conjunctions 1 (Sun-Moon/Mars/Mercury) — SAV001-130; "
     "corpus 3817; 2393 tests\n"
     "- **Next session:** S274"),
    (ROOT / "docs/MEMORY.md",
     "- **2379 passing, 3 skipped, 0 lint errors, CI green**",
     "- **2393 passing, 3 skipped, 0 lint errors, CI green**"),
]

for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S273" not in text:
            doc.write_text(text.rstrip() + new)
            print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S273")
    elif old in text:
        doc.write_text(text.replace(old, new, 1))
        print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found — check manually")

# Update coverage map Section A1
cmap = ROOT / "docs/coverage_maps/saravali.md"
cmap_text = cmap.read_text()
for old_line, new_line in [
    ("| A1 | Ch.15–16 | Sun-Moon, Sun-Mars, Sun-Mercury conjunctions | ~130 | S273 | 🔲 |",
     "| A1 | Ch.15–16 | Sun-Moon, Sun-Mars, Sun-Mercury conjunctions | ~130 | S273 | ✅ |"),
    ("| **TOTAL A** | | | **~1,040** | **S273–S280** | **0/1040** |",
     "| **TOTAL A** | | | **~1,040** | **S273–S280** | **130/1040** |"),
    ("| **TOTAL** | **S273–S305** | **~4,100** | **0/4100** |",
     "| **TOTAL** | **S273–S305** | **~4,100** | **130/4100** |"),
]:
    if old_line in cmap_text:
        cmap_text = cmap_text.replace(old_line, new_line, 1)
        print(f"Coverage map: updated")
    else:
        print(f"Coverage map: pattern not found — '{old_line[:55]}'")
cmap.write_text(cmap_text)
print("done")
