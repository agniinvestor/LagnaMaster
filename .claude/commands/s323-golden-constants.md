# S323: Governance — Canonical Astrological Constants (Golden Source)

## Session type
**Governance** — create single canonical source for all astrological constants, then refactor all consumers to import from it. No encoding.

## Problem

Astrological reference data (sign lords, benefics/malefics, house classifications, aspects, dignities, karaka tables) is independently defined in 11-28+ files each. S317/S318 found and fixed data bugs, but fixed them by patching individual copies rather than consolidating. Two bugs survived because only one copy was fixed while others remained wrong (BUG-051 gentle signs, diagnostic_scorer special aspects). This will happen again until the architecture prevents it.

Additionally, 5 modules in `src/calculations/` are dead code (0 production importers). One of them (`diagnostic_scorer.py`) had bugs "fixed" in S322 that never affected production because the file is never called. Dead code must be removed before consolidating constants — no point migrating constants out of files that should be deleted.

## Pre-flight
```bash
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```

---

## Step 0: Delete dead modules (BEFORE constants work)

These 5 files have 0 production importers. Delete them entirely. ~1,301 lines removed.

### Dead modules to delete:

1. **`src/calculations/config_additions.py`** (141 lines) — ayanamsha map expansion, replaced by `calc_config.py`. Zero importers.

2. **`src/calculations/feature_expansion.py`** (171 lines) — unfinished Phase 2 feature expansion. Zero importers.

3. **`src/calculations/diagnostic_scorer.py`** (355 lines) — diagnostic scoring module. Only importer is `feature_expansion.py` (also dead). Dead island. Contains wrong special aspects that were "fixed" in S322 but never affected production.

4. **`src/calculations/scoring_v2.py`** (409 lines) — superseded scoring version. Only importer is `tests/test_phase4.py`.

5. **`src/calculations/avastha.py`** (225 lines) — old avastha module, superseded by `avasthas.py` (BPHS Ch.45 aligned, 28 importers). Only importer is `tests/test_phase4.py`.

### For each deletion:
1. Delete the file
2. Run `grep -rn 'from src.calculations.MODULE import\|import src.calculations.MODULE' src/ tests/ tools/ --include='*.py'` to find any importers
3. If importers exist in **test files only** (`tests/test_phase4.py`): update the test to either import from the canonical replacement or delete the test if it's testing dead functionality
4. If importers exist in **production code**: STOP — the file is not dead. Investigate before deleting.
5. Run `.venv/bin/pytest tests/ -q --tb=short -x` after each deletion

### Commit:
```
refactor(S323): delete 5 dead modules — config_additions, feature_expansion, diagnostic_scorer, scoring_v2, avastha

1,301 lines of dead code removed. diagnostic_scorer had 0 production
callers (only importer was feature_expansion, also dead). scoring_v2
and avastha.py superseded by scoring.py and avasthas.py respectively.
test_phase4.py updated to import from canonical modules.
```

---

## Deliverable: `src/data/constants.py`

Create a single file that is the ONLY place astrological constants are defined. Every other file imports from it. Each constant cites its BPHS source.

**IMPORTANT:** Step 0 (dead code deletion) MUST complete before Step 1. Do not migrate constants from deleted files. The following files will no longer exist after Step 0 and should be IGNORED during refactoring:
- `src/calculations/config_additions.py`
- `src/calculations/feature_expansion.py`
- `src/calculations/diagnostic_scorer.py`
- `src/calculations/scoring_v2.py`
- `src/calculations/avastha.py`

### Step 1: Create the file

Create `src/data/constants.py` with ALL of the following. For each constant, cite the BPHS chapter and verse. Use the values from the known-correct canonical sources identified below.

```python
"""src/data/constants.py — Canonical astrological constants.

GOLDEN SOURCE: Every astrological constant in LagnaMaster is defined here
and ONLY here. All other modules import from this file.

Each constant cites its BPHS source. If a constant comes from a different
text, that text is cited instead. If values differ between texts, BPHS is
authoritative unless noted.

Verified against: R. Santhanam, BPHS Vol 1, Ranjan Publications.
"""
```

#### Constants to include:

**A. Planet classifications**
```python
# BPHS Ch.3 v.11 (p.27-28)
# Moon and Mercury are CONDITIONALLY benefic/malefic:
#   Moon: malefic when waning (Krishna Paksha), benefic when waxing
#   Mercury: malefic when conjunct malefics
# For static lookups (no chart context), classify both as benefic.
NATURAL_BENEFICS: frozenset[str] = frozenset({"Jupiter", "Venus", "Mercury", "Moon"})
NATURAL_MALEFICS: frozenset[str] = frozenset({"Sun", "Mars", "Saturn", "Rahu", "Ketu"})

# All 9 grahas in standard order
PLANETS: tuple[str, ...] = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
SEVEN_PLANETS: tuple[str, ...] = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
```

**B. Sign lords** — canonical source: `functional_dignity.py` lines 23-36
```python
# BPHS Ch.3 v.49-51 — Planetary Rulership
# sign_index (0=Aries) → ruling planet
SIGN_LORDS: dict[int, str] = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}
```

**C. Sign classifications**
```python
# BPHS — even-numbered signs (0-indexed) are feminine/gentle
# Taurus(1), Cancer(3), Virgo(5), Scorpio(7), Capricorn(9), Pisces(11)
GENTLE_SIGNS: frozenset[int] = frozenset({1, 3, 5, 7, 9, 11})
CRUEL_SIGNS: frozenset[int] = frozenset({0, 2, 4, 6, 8, 10})

SIGN_NAMES: tuple[str, ...] = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
```

**D. House classifications**
```python
# BPHS Ch.11 — Bhava Characteristics
KENDRA_HOUSES: frozenset[int] = frozenset({1, 4, 7, 10})
TRIKONA_HOUSES: frozenset[int] = frozenset({1, 5, 9})
DUSTHANA_HOUSES: frozenset[int] = frozenset({6, 8, 12})
UPACHAYA_HOUSES: frozenset[int] = frozenset({3, 6, 10, 11})
MARAKA_HOUSES: frozenset[int] = frozenset({2, 7})
PANAPHARA_HOUSES: frozenset[int] = frozenset({2, 5, 8, 11})
APOKLIMA_HOUSES: frozenset[int] = frozenset({3, 6, 9, 12})
```

**E. Special aspects** — canonical source: `sputa_drishti.py` lines 51-55
```python
# BPHS Ch.26 v.9-12 — Graha Drishti (special planetary aspects)
# Offset from aspecting planet's house position. All planets also have
# 7th aspect (offset=6) which is universal, not listed here.
SPECIAL_ASPECTS: dict[str, frozenset[int]] = {
    "Mars": frozenset({4, 8}),      # 4th and 8th house aspects
    "Jupiter": frozenset({5, 9}),   # 5th and 9th house aspects
    "Saturn": frozenset({3, 10}),   # 3rd and 10th house aspects
}
```

**F. Dig Bala** — canonical source: `dig_bala.py` lines 27-35
```python
# BPHS Ch.27 — Directional Strength (peak houses)
DIG_BALA_PEAK: dict[str, int] = {
    "Sun": 10, "Moon": 4, "Mars": 10, "Mercury": 1,
    "Jupiter": 1, "Venus": 4, "Saturn": 7,
}
```

**G. Sthira Karaka** — canonical source: `scoring.py` lines 42-55
```python
# BPHS Ch.32 v.34 — Naisargika (Fixed) Significators per house
STHIRA_KARAKA: dict[int, tuple[str, ...]] = {
    1: ("Sun",),
    2: ("Jupiter",),
    3: ("Mars",),
    4: ("Moon", "Venus"),       # BUG-052 fix: Venus = vehicles/comforts
    5: ("Jupiter",),
    6: ("Mars", "Saturn"),
    7: ("Venus",),
    8: ("Saturn",),
    9: ("Jupiter", "Sun"),      # BUG-053 fix: Sun = father karaka
    10: ("Sun", "Mercury", "Saturn"),  # BUG-054 fix: removed Jupiter
    11: ("Jupiter",),
    12: ("Saturn",),
}
```

**H. Exaltation/Debilitation signs** — canonical source: `dignity.py` lines 64-81
```python
# BPHS Ch.3 v.49-51 — Exaltation signs (0-indexed)
EXALTATION_SIGN: dict[str, int] = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6,
}
DEBILITATION_SIGN: dict[str, int] = {
    "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
    "Jupiter": 9, "Venus": 5, "Saturn": 0,
}
# Exaltation degrees — BPHS Ch.3 v.49-51
EXALTATION_DEGREE: dict[str, float] = {
    "Sun": 10.0, "Moon": 3.0, "Mars": 28.0, "Mercury": 15.0,
    "Jupiter": 5.0, "Venus": 27.0, "Saturn": 20.0,
}
```

**I. Moolatrikona ranges** — canonical source: `dignity.py` MOOLTRIKONA_RANGES
Import and re-export rather than duplicating — `dignity.py` has the degree-bounded ranges.

**J. Nakshatra names** — canonical source: `nakshatra.py`
```python
# 27 Nakshatras in order (Ashwini=0 to Revati=26)
# Duplicated in 7+ files (vimshottari_dasa, kp_sublord, kp, panchanga, etc.)
NAKSHATRA_NAMES: tuple[str, ...] = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
)
```

**K. Vimshottari Dasha data** — canonical source: `vimshottari_dasa.py`
```python
# BPHS Ch.46 — Vimshottari Dasha years and sequence
# Duplicated in 6+ files (kp_sublord, kp, pratyantar_dasha, special_lagnas, upaya)
VIMSHOTTARI_YEARS: dict[str, int] = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Mercury": 17, "Jupiter": 16,
    "Venus": 20, "Saturn": 19, "Rahu": 18, "Ketu": 7,
}  # Total: 120 years

# Dasha sequence (starting from Ketu) — duplicated in 4+ files
VIMSHOTTARI_SEQUENCE: tuple[str, ...] = (
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
)
```

**L. Own signs** — canonical source: `dignity.py`
```python
# BPHS Ch.3 v.49-51 — each planet's own signs (sign indices)
# Duplicated in diagnostic_scorer.py and others
OWN_SIGNS: dict[str, tuple[int, ...]] = {
    "Sun": (4,), "Moon": (3,), "Mars": (0, 7), "Mercury": (2, 5),
    "Jupiter": (8, 11), "Venus": (1, 6), "Saturn": (9, 10),
}
```

**M. Combustion orbs** — source: BPHS Ch.3 (Santhanam notes p.28)
```python
# Degrees from Sun at which a planet becomes combust
# Currently only in corpus documentation — needs hardcoded canonical source
COMBUSTION_ORBS: dict[str, float] = {
    "Moon": 12.0, "Mars": 17.0, "Mercury": 14.0, "Mercury_retro": 12.0,
    "Jupiter": 11.0, "Venus": 10.0, "Venus_retro": 8.0, "Saturn": 15.0,
}
```

**N. Naisargika Bala** — canonical source: `shadbala.py`
```python
# BPHS Ch.27 — Natural strength (Shashtiamsha units)
NAISARGIKA_BALA: dict[str, float] = {
    "Sun": 60.0, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
    "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57,
}
```

**O. Weekday and Hora lords**
```python
# Standard weekday sequence (Sunday=0)
WEEKDAY_LORDS: tuple[str, ...] = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

# Hora sequence (planetary hours)
HORA_SEQUENCE: tuple[str, ...] = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
```

**P. Zodiac elements and qualities**
```python
# Fire/Earth/Air/Water by sign index
FIRE_SIGNS: frozenset[int] = frozenset({0, 4, 8})      # Aries, Leo, Sagittarius
EARTH_SIGNS: frozenset[int] = frozenset({1, 5, 9})     # Taurus, Virgo, Capricorn
AIR_SIGNS: frozenset[int] = frozenset({2, 6, 10})      # Gemini, Libra, Aquarius
WATER_SIGNS: frozenset[int] = frozenset({3, 7, 11})    # Cancer, Scorpio, Pisces

# Cardinal/Fixed/Mutable (Chara/Sthira/Dwiswabhava)
CARDINAL_SIGNS: frozenset[int] = frozenset({0, 3, 6, 9})   # Aries, Cancer, Libra, Capricorn
FIXED_SIGNS: frozenset[int] = frozenset({1, 4, 7, 10})     # Taurus, Leo, Scorpio, Aquarius
MUTABLE_SIGNS: frozenset[int] = frozenset({2, 5, 8, 11})   # Gemini, Virgo, Sagittarius, Pisces
```

**Q. Naisargika friendship** — canonical source: `panchadha_maitri.py`
Import and re-export.

### Step 2: Verify the file

After creating `src/data/constants.py`:
```bash
.venv/bin/python -c "from src.data.constants import *; print('OK')"
.venv/bin/ruff check src/data/constants.py
```

Also verify that `src/data/__init__.py` exists (create if needed).

### Step 3: Refactor consumers — ONE CATEGORY AT A TIME

For each constant category (A through H), do the following:

1. **Grep for BOTH definitions AND usages** of this constant across ALL of `src/`, `tools/`, and `tests/`:
   - Definitions: `grep -rn 'VARIABLE_NAME.*=.*{' src/ tools/ tests/` (the assignment)
   - Usages: `grep -rn 'VARIABLE_NAME' src/ tools/ tests/` (everything that references it)
   - Cross-file imports: `grep -rn 'from.*import.*VARIABLE_NAME' src/ tools/ tests/` (anything importing it from the OLD location)
2. **Replace** the local definition with an import: `from src.data.constants import X`
3. **DELETE** the local constant definition
4. **Fix all downstream importers** — if any other file was doing `from src.scoring import STHIR_KARAK`, change it to `from src.data.constants import STHIRA_KARAKA`. This is the critical step that prevents breakage.
5. **Run tests** after each category — do NOT batch multiple categories without testing
6. **Commit** after each category passes

**Order of refactoring** (by risk — lowest first, highest duplication last):
1. GENTLE_SIGNS / CRUEL_SIGNS (2 files)
2. SPECIAL_ASPECTS (4 files)
3. DIG_BALA_PEAK (4 files)
4. STHIRA_KARAKA (4 files)
5. EXALTATION / DEBILITATION / OWN_SIGNS (6 files)
6. COMBUSTION_ORBS + NAISARGIKA_BALA + WEEKDAY/HORA (3-5 files)
7. VIMSHOTTARI_YEARS + VIMSHOTTARI_SEQUENCE (6+ files)
8. NAKSHATRA_NAMES (7 files)
9. NATURAL_BENEFICS / NATURAL_MALEFICS (15+ files)
10. SIGN_NAMES (10+ files)
11. PLANETS / SEVEN_PLANETS (18+ files)
12. SIGN_LORDS (11 files)
13. HOUSE_CLASSIFICATIONS — KENDRA/TRIKONA/DUSTHANA/UPACHAYA (28+ files)
14. ZODIAC ELEMENTS + QUALITIES — FIRE/EARTH/AIR/WATER, CARDINAL/FIXED/MUTABLE (unknown count — grep first)

**For each file that DEFINES a constant locally:**
- Add import at top: `from src.data.constants import X`
- **DELETE the local constant definition entirely** — do not comment it out, do not leave it as `# removed`
- Update all references in the file to use the canonical name (e.g., `_NAT_BENEFIC` → `NATURAL_BENEFICS`). Use find-and-replace across the whole file.
- If the local used a different type (set vs frozenset vs tuple), the frozenset from constants.py should work in all contexts (membership testing, iteration). If a specific function needs a list/tuple, wrap at call site.
- **If removing the constant leaves a file with no remaining logic** (just imports and re-exports), consider whether the file itself should be deleted. Files that existed only to define constants that now live in constants.py are dead weight. But if the file has functions or classes that use the constants, keep the file — just with the import replacing the local definition.
- **Rename all internal references** — if a file used `_NAT_BENEFIC` in 12 places, all 12 must change to `NATURAL_BENEFICS`. Do not leave aliases like `_NAT_BENEFIC = NATURAL_BENEFICS` — that recreates the duplication problem.
- After each file is refactored, run `ruff check` on it. Fix any unused import or undefined name errors immediately.

**For each file that IMPORTS a constant from a non-canonical source:**
- If file A does `from src.calculations.functional_dignity import _SIGN_LORDS`, change it to `from src.data.constants import SIGN_LORDS`
- If file A does `from src.scoring import STHIR_KARAK`, change it to `from src.data.constants import STHIRA_KARAKA`
- **Every import path for a migrated constant must point to `src.data.constants`** — no file should import astrological constants from any other module. This is what makes constants.py the single canonical layer.

**For tools/ and tests/ files:**
- Same rules apply. If `tools/v2_scorecard.py` or `tests/test_rule_firing.py` define or import constants, they must also be updated to use `src.data.constants`.
- Test files that define expected values (e.g., `assert SIGN_LORDS[0] == "Mars"`) should import from constants.py too — they're verifying the canonical source, not maintaining a parallel copy.

### Step 4: Add import guard

After all refactoring, add to `.pre-commit-config.yaml` or a ruff rule:
- Grep for patterns like `_BENEFIC.*=.*{` or `SIGN_LORD.*=.*{` in `src/` files (excluding `src/data/constants.py`)
- If found, warn: "Astrological constant defined outside src/data/constants.py"

This can also be a simple grep-based hook in `tools/validate_constants.py`.

---

## Commits (one per category + the initial file)

1. `feat(S323): create src/data/constants.py — canonical astrological constants`
2. `refactor(S323): consolidate GENTLE_SIGNS + SPECIAL_ASPECTS to constants.py`
3. `refactor(S323): consolidate NATURAL_BENEFICS/MALEFICS to constants.py (15+ files)`
4. `refactor(S323): consolidate SIGN_LORDS to constants.py (11 files)`
5. `refactor(S323): consolidate HOUSE_CLASSIFICATIONS to constants.py (28+ files)`
6. `refactor(S323): consolidate DIG_BALA + STHIRA_KARAKA + EXALT/DEBIL to constants.py`
7. `feat(S323): add validate_constants.py — prevent future duplication`

## Validation after EACH commit
```bash
.venv/bin/pytest tests/ -q --tb=short -x
.venv/bin/ruff check src/ tests/
```

## Final validation
```bash
# Verify no local definitions remain — each grep MUST return 0 results
for pattern in '_BENEFIC.*=.*{' 'SIGN_LORD.*=.*{' '_GENTLE.*=.*{' 'SPECIAL_ASPECT.*=.*{' \
    'KENDRA.*=.*{' 'TRIKONA.*=.*{' 'DUSTHANA.*=.*{' 'DIG_BALA.*=.*{' 'STHIR.*KARAK.*=.*{' \
    'EXALT.*SIGN.*=.*{' 'DEBIL.*SIGN.*=.*{' 'OWN_SIGN.*=.*{' \
    'VIMSHOTTARI.*YEAR.*=.*{' 'NAKSHATRA_NAME.*=.*(' '_PLANETS_7.*=.*[' \
    '"Sun".*"Moon".*"Mars".*"Mercury".*='; do
  hits=$(grep -rn "$pattern" src/ --include='*.py' | grep -v 'constants.py' | grep -v '__pycache__' | wc -l)
  if [ "$hits" -gt 0 ]; then
    echo "FAIL: $pattern found in $hits files outside constants.py"
    grep -rn "$pattern" src/ --include='*.py' | grep -v 'constants.py' | grep -v '__pycache__'
  fi
done
```

## Report format
```
STEP 0 — DEAD CODE DELETION:
  Dead modules deleted: [count] / 5
  Lines removed: [count] / ~1,301
  Tests updated: [count]

STEP 1-3 — CONSTANTS CONSOLIDATION:
  CONSTANTS FILE: src/data/constants.py ([X] constants defined)
  FILES REFACTORED: [count]
  LOCAL DEFINITIONS DELETED: [count]
  LINES OF CODE REMOVED: [net count — deletions minus new imports]
  DUPLICATIONS REMAINING: [count] (must be 0)

STEP 4 — GUARD:
  GUARD TOOL: tools/validate_constants.py (present/absent)

TOTAL SESSION:
  Net lines removed: [dead code + constant dedup combined]
  Files deleted: [list]
```

## Non-negotiable
1. Do NOT change any constant VALUES — only move definitions to constants.py
2. If you find a value that looks wrong, DO NOT FIX IT in this session — note it and move on. This session is about consolidation, not correction.
3. Test after EVERY category refactor — do not batch
4. If a test fails after removing a local definition, investigate: the import may have a name mismatch or type mismatch. Fix the import, do not revert to local definition.
5. Keep `dignity.py`, `panchadha_maitri.py`, `vimshottari_dasa.py` as the detailed implementations — constants.py re-exports their key constants, not duplicates them.
6. Some files may use conditional benefic/malefic logic (checking Moon waning, Mercury conjunction). Those files should import `NATURAL_BENEFICS` for the static set but keep their conditional logic. Do NOT remove conditional logic.
7. **DELETE, don't alias.** Do NOT leave `_NAT_BENEFIC = NATURAL_BENEFICS` — that's a local alias which recreates the duplication problem. Every reference in the file must use the canonical name directly.
8. **The goal is net code reduction.** After this session, `wc -l` across all refactored files should show fewer total lines than before. If it doesn't, you're adding complexity, not removing it.
9. **Dead files get deleted.** If removing constants from a file leaves only imports and no logic, delete the file entirely and update any importers of that file to import from constants.py instead.
