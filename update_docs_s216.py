"""update_docs_s216.py — S216-S228 Phase 1 batch documentation sync."""
from pathlib import Path
ROOT = Path(__file__).parent
patches = [
    (ROOT/"docs/CHANGELOG.md", None,
     "\n---\n\n## S216–S228 — 2026-03-28 — Phase 1 Classical Knowledge Foundation (Batch 1)\n\n"
     "**Tests:** 1777 passing, 3 skipped, 0 lint errors\n\n"
     "### What was built\n"
     "**Lord-in-Houses (144 rules, S216-S221):** Complete 12×12 matrix of house lord "
     "positions encoded from BPHS Ch.24-35:\n"
     "- `bphs_lords_h1_h2.py`: H1L001-H1L012 + H2L001-H2L012 (lagna + 2nd lord)\n"
     "- `bphs_lords_h3_h4.py`: H3L/H4L series (3rd + 4th lord)\n"
     "- `bphs_lords_h5_h6.py`: H5L/H6L series (5th + 6th lord) — includes viparita yoga\n"
     "- `bphs_lords_h7_h8.py`: H7L/H8L series (7th + 8th lord)\n"
     "- `bphs_lords_h9_h10.py`: H9L/H10L series (9th + 10th lord) — dharma karma adhipati\n"
     "- `bphs_lords_h11_h12.py`: H11L/H12L series (11th + 12th lord)\n\n"
     "**Yoga encoding (S222-S224):**\n"
     "- `bphs_yogas_basic.py`: 25 rules — Pancha Mahapurusha, Gajakesari, Neecha Bhanga, "
     "Viparita, Parivartana, sun/moon-based yogas\n"
     "- `bphs_raja_yoga.py`: 25 rules — kendra-trikona combinations, yogakaraka rules "
     "per lagna, cancellation rules\n"
     "- `bphs_dhana_yoga.py`: 25 rules — wealth yogas, daridra, vasumati, parivartana dhana\n\n"
     "**Supporting rules (S225-S228):**\n"
     "- `bphs_dignities_ext.py`: 20 rules — exaltation, moolatrikona, own sign, vargottama, "
     "digbala, combustion, graha yuddha\n"
     "- `bphs_aspects.py`: 20 rules — special aspects (Jupiter/Saturn/Mars), mangal dosha, "
     "argala\n"
     "- `bphs_dasha_results.py`: 20 rules — all 9 planet dasha themes, lordship modification\n"
     "- `bphs_special_lagnas.py`: 20 rules — Chandra/Surya/Arudha/Upapada/Hora/Ghati lagnas\n\n"
     "**Total corpus: 434 rules** (from 135 at end of Phase 0)\n\n"
     "### Next session\nS229 — Continue Phase 1: BPHS graha in rashis + KP sublord rules\n"),
    (ROOT/"docs/MEMORY.md",
     "- **1722 passing, 3 skipped, 0 lint errors, CI green**",
     "- **1777 passing, 3 skipped, 0 lint errors, CI green**"),
    (ROOT/"docs/MEMORY.md",
     "## Actual Current State (Sessions 1–215 complete",
     "## Actual Current State (Sessions 1–228 complete"),
    (ROOT/"docs/MEMORY.md",
     "- **Sessions 213–215:** Protocol verification + CI observability + Phase 0 checkpoint; "
     "src/ci/ package; 1722 tests\n- **Next session:** S216",
     "- **Sessions 213–215:** Protocol verification + CI observability + Phase 0 checkpoint; "
     "src/ci/ package; 1722 tests\n"
     "- **Sessions 216–228:** Phase 1 Batch 1 — 299 new BPHS rules encoded (lords-in-houses "
     "144, yogas 75, dignities/aspects/dasha/special-lagnas 80); corpus 135→434 rules; 1777 tests\n"
     "- **Next session:** S229"),
]
for doc, old, new in patches:
    text = doc.read_text()
    if old is None:
        if "## S216" not in text:
            doc.write_text(text.rstrip() + new); print(f"{doc.name} appended")
        else:
            print(f"{doc.name} already has S216")
    elif old in text:
        doc.write_text(text.replace(old, new, 1)); print(f"{doc.name} patched")
    else:
        print(f"{doc.name} pattern not found")
print("done")
