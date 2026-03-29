"""
update_docs_s194.py — S194 documentation sync

Patches:
  - docs/CHANGELOG.md  — S194 entry
  - docs/MEMORY.md     — test count, session progress, Next session
  - docs/ARCHITECTURE.md — conditional_weights.py module entry

Run:  .venv/bin/python update_docs_s194.py
"""

from pathlib import Path

ROOT = Path(__file__).parent
CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
MEMORY = ROOT / "docs" / "MEMORY.md"
ARCHITECTURE = ROOT / "docs" / "ARCHITECTURE.md"

# ─── CHANGELOG ───────────────────────────────────────────────────────────────

S194_ENTRY = """
---

## S194 — 2026-03-28 — Conditional Weight Functions W(planet, house, lagna, functional_role)

**Commit:** (see git log)
**Tests:** 1503 passing, 3 skipped (require live PG_DSN), 0 lint errors, CI green

### What was built
- `src/calculations/conditional_weights.py`: `WeightContext` dataclass and
  `W(ctx) -> float` function that replaces flat static rule weights with
  context-conditional modifiers:
  - Yogakaraka × YK_MULT (1.5 Parashari/KP, 1.25 Jaimini) — early-return
  - Functional benefic + positive rule × 1.2
  - Functional malefic + negative rule × 1.2 (stronger affliction)
  - Role mismatch × 0.75 (cross-direction mitigation)
  - Kendra/Trikona house + positive rule × 1.1
  - Dusthana house + negative rule × 1.1
  - `g06_compliant` property: KP school requires Krishnamurti ayanamsha (G06)
- `tests/test_s194_conditional_weights.py`: 13 tests covering all modifiers,
  G06 compliance flags, and role-alignment logic.

### What was wired
- `build_context()` convenience constructor for downstream callers.
- Module ready for Phase 2 engine rebuild — not yet wired into live scoring
  to preserve regression stability.

### New invariants
- #38: W(yogakaraka) = base × YK_MULT and returns immediately — no further
  house or role modifiers stack on top of yogakaraka status.
- #39: W(neutral, non-kendra/dusthana) = base_weight exactly (no noise added).

### Guardrail compliance
- G06: WeightContext.g06_compliant flags KP+Lahiri as non-compliant.
  Full fix deferred to S212 (ayanamsha selection).

### Three-Lens Notes
- Tech: Introduces the Layer I weight infrastructure that Phase 2 will wire
  into the full engine. All existing scores are unchanged (not yet wired).
- Astrology: Encodes functional dignity primacy (V.K. Choudhry Systems Approach
  Ch.3) and house-type promise hierarchy (BPHS Ch.11) as computable functions.
- Research: Context-conditional weights are a prerequisite for SHAP analysis
  (Phase 6) — static weights produce uninterpretable attribution.

### Next session
S195 — Feature decomposition: 23 binary rules → 150+ continuous features (G22)
"""

changelog_text = CHANGELOG.read_text()
if "## S194" not in changelog_text:
    CHANGELOG.write_text(changelog_text.rstrip() + "\n" + S194_ENTRY)
    print("CHANGELOG.md — S194 entry appended.")
else:
    print("CHANGELOG.md — S194 already present, skipped.")

# ─── MEMORY.md ───────────────────────────────────────────────────────────────

memory_text = MEMORY.read_text()
patched = memory_text

replacements = [
    (
        "- **1490 passing, 3 skipped, 0 lint errors, CI green**",
        "- **1503 passing, 3 skipped, 0 lint errors, CI green**",
    ),
    (
        "## Actual Current State (Sessions 1–193 complete",
        "## Actual Current State (Sessions 1–194 complete",
    ),
    (
        "- **Next session:** S194",
        "- **Session 194:** Conditional weight functions W(planet, house, lagna, functional_role) — `conditional_weights.py`, G06 g06_compliant flag; 1503 tests\n- **Next session:** S195",
    ),
    # Fix duplicate S193 line from previous session
    (
        "- **Session 193:** HouseScore distribution dataclass — `house_score.py`, `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests\n- **Session 193:** HouseScore distribution dataclass — `house_score.py`, `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests",
        "- **Session 193:** HouseScore distribution dataclass — `house_score.py`, `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests",
    ),
    # Update the Key Metrics table
    (
        "| Tests passing | **1338** (3 skipped) | 8,000+ |",
        "| Tests passing | **1503** (3 skipped) | 8,000+ |",
    ),
]

for old, new in replacements:
    if old in patched:
        patched = patched.replace(old, new, 1)

if patched != memory_text:
    MEMORY.write_text(patched)
    print("MEMORY.md — patched.")
else:
    print("MEMORY.md — no changes (already up to date).")

# ─── ARCHITECTURE.md ─────────────────────────────────────────────────────────

arch_text = ARCHITECTURE.read_text()
arch_patch_old = "  house_score.py               HouseScore distribution dataclass (S193)"
arch_patch_new = (
    "  house_score.py               HouseScore distribution dataclass (S193)\n"
    "  conditional_weights.py       W(WeightContext) → context-conditional rule weights (S194)"
)

# If not already present, inject after house_score line or at end of calculations block
if "conditional_weights.py" not in arch_text:
    if arch_patch_old in arch_text:
        arch_text = arch_text.replace(arch_patch_old, arch_patch_new, 1)
        ARCHITECTURE.write_text(arch_text)
        print("ARCHITECTURE.md — conditional_weights.py entry added.")
    else:
        # Fallback: append a note at the end of file
        note = (
            "\n## S194 — New module\n"
            "- `src/calculations/conditional_weights.py` — `WeightContext` + `W()` "
            "conditional weight function (G06-aware, Phase 2 engine rebuild ready)\n"
        )
        ARCHITECTURE.write_text(arch_text.rstrip() + note)
        print("ARCHITECTURE.md — S194 note appended.")
else:
    print("ARCHITECTURE.md — already up to date.")

# ─── ROADMAP.md: mark S194 complete ──────────────────────────────────────────

ROADMAP = ROOT / "docs" / "ROADMAP.md"
roadmap_text = ROADMAP.read_text()
old_s194 = "| S194 | Conditional weight functions W(planet, house, lagna, functional_role) | G06 | 🔴 |"
new_s194 = "| S194 | Conditional weight functions W(planet, house, lagna, functional_role) | G06 | ✅ |"
if old_s194 in roadmap_text:
    ROADMAP.write_text(roadmap_text.replace(old_s194, new_s194, 1))
    print("ROADMAP.md — S194 marked ✅.")
elif "S194" in roadmap_text and "✅" not in roadmap_text[roadmap_text.find("S194"):roadmap_text.find("S194")+80]:
    print("ROADMAP.md — S194 line format differs, manual update may be needed.")
else:
    print("ROADMAP.md — S194 already marked or not found.")

print("\nupdate_docs_s194.py — done.")
