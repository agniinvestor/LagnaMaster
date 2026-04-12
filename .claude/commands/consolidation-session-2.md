# Engine Consolidation Phase 2 — Resolve Remaining Duplications

## Session type
**Governance** — no encoding, no new features. Pure refactoring with test-driven verification.

## Why this exists

S326 consolidation session (W0-1 through W0-4) eliminated 722 lines across 24 files, but several duplication clusters remain unresolved. These fall into three categories: (A) a D9 formula disagreement that needs correctness investigation, (B) functions with different signatures that need careful API unification, and (C) lower-priority constant/type duplications.

## Ground rules (same as W0)

- **Every change must be test-verified.** Run full test suite after each consolidation.
- **Do NOT change behavior** unless two implementations disagree — then pick the CORRECT one per BPHS and document the choice.
- **One cluster at a time.** Complete, test, commit.
- **Commit message format:** `refactor(W0-N): consolidate <what> — <canonical source> is now single implementation`

## Pre-flight

```bash
.venv/bin/pytest tests/ -q --tb=short
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/ob3_calibrate.py --report 2>&1 | grep 'ρ=' > /tmp/baseline_ob3_w0b.txt
```

Save all baselines before any changes.

---

## Phase A: D9 Navamsha Formula Investigation (MUST DO FIRST)

panchanga.py `_d9_sign_index` disagrees with varga.py `_d9_sign_index` for 180 out of 360 degrees. Both claim to implement the Parasara navamsha formula.

### A1. Determine which formula is correct

```python
# panchanga.py formula:
def _d9_sign_index(lon):
    sign = int(lon / 30) % 12
    deg_in_sign = lon % 30
    pada = int(deg_in_sign / (30 / 9))
    is_odd = sign % 2 == 0  # 0-indexed: Aries=0 (even) = odd sign in BPHS
    return (sign * 9 + pada) % 12 if is_odd else (sign * 9 + pada + 9) % 12

# varga.py formula (also in nakshatra.py):
_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}  # Fire->Ar, Earth->Cp, Air->Li, Water->Cn
def _d9_sign_index(longitude):
    si = int(longitude / 30) % 12
    pada = int((longitude % 30) * 9 / 30)
    return (_D9_START[si % 4] + pada) % 12
```

**Verification method:**
1. Read BPHS Ch.6 v.5-6 (Navamsha division rules). The standard rule is:
   - Fire signs (Ar/Le/Sg): navamsha starts from Aries
   - Earth signs (Ta/Vi/Cp): navamsha starts from Capricorn
   - Air signs (Ge/Li/Aq): navamsha starts from Libra
   - Water signs (Cn/Sc/Pi): navamsha starts from Cancer
2. Test against known navamsha positions (e.g., Sun at 10 degrees Aries = 4th navamsha of Aries = Cancer navamsha)
3. Cross-validate against PyJHora or VedAstro if available in fixtures

### A2. Fix the incorrect formula

If panchanga.py is wrong (likely — the `_D9_START` approach matches standard textbooks), fix it to use varga.py's formula. This is a **behavioral change** — document it and check what `compute_navamsha_chart()` returns differ.

### A3. Make panchanga.py import from varga.py

After fixing, replace panchanga's local `_d9_sign_index` with:
```python
from src.calculations.varga import _d9_sign_index
```

Run tests. Expect some navamsha-related tests to break if panchanga was wrong. Fix test expectations.

---

## Phase B: Function-Level Duplications (Different Signatures)

### B1. Longevity: longevity.py vs ayurdaya.py

Both compute Pindayu/Nisargayu/Amsayu. `main.py` calls BOTH.

**Investigation:**
1. Read both files. Map their public APIs.
2. Check `main.py` — does it call both? What does it use from each?
3. If ayurdaya.py is a superset of longevity.py, make longevity.py delegate to it.
4. If they compute different longevity systems, they're not duplicates — just update main.py to avoid calling both if outputs overlap.

### B2. Vimshopaka: divisional_charts.py vs sapta_varga.py

`compute_vimshopaka()` vs `compute_vimshopak()` (note spelling difference).

**Investigation:**
1. Compare return types and APIs
2. Check callers: `scoring_v3` uses `divisional_charts`; `app.py` uses `sapta_varga`
3. If logic is identical, pick one and make the other delegate
4. If return types differ, create a common interface or keep both with a note

### B3. Nabhasa yogas: nabhasa_yogas.py vs yogas_extended.py

Both detect nabhasa yogas. `main.py` calls both.

**Investigation:**
1. Check if `yogas_extended.py` internally calls `nabhasa_yogas.py`
2. If yes, remove the direct call from main.py (it's double-counting)
3. If they're independent implementations, pick one as canonical

### B4. Chara karakas: chara_karak.py vs chara_karaka_config.py

Unify `compute_chara_karakas` to one source.

**Investigation:**
1. Compare function signatures and return types
2. Check all callers
3. Make one delegate to the other

### B5. Karakamsha: multi_lagna.py vs chara_karaka_config.py

`compute_karakamsha` exists in both with different signatures:
- `multi_lagna.py`: takes just `chart`
- `chara_karaka_config.py`: takes `chart` + `chara_result`

**Investigation:**
1. Does multi_lagna internally compute chara karakas? If so, make it call chara_karaka_config
2. Unify to the more complete version

### B6. Planetary war: graha_yuddha.py vs planetary_state.py

`planetary_state.detect_graha_yuddha()` may be uncalled.

**Investigation:**
1. `grep -rn 'detect_graha_yuddha\|compute_graha_yuddha' src/ tests/` — check callers
2. If planetary_state version is uncalled, delete it
3. If both are called, compare implementations (one has latitude checks, one doesn't)

### B7. Tarabala + Chandrabala: transit_quality_advanced.py vs muhurtha_complete.py

**Investigation:**
1. Check if muhurtha_complete imports from transit_quality_advanced
2. If not, make it import — transit_quality_advanced is the more used module

### B8. _EXALT_LON / _DEBIL_LON: ishta_kashta.py vs longevity.py

Both have identical absolute-longitude exaltation/debilitation tables.

**Fix:** Move to a shared location (either constants.py or dignity.py) and import from both files. These are different from the sign-index tables (EXALT_SIGN) — they store precise zodiac longitudes for Uchcha Bala calculation.

---

## Phase C: Remaining Constant Duplications

### C1. rule_firing.py: _EXALT_SIGN, _DEBIL_SIGN, _OWN_SIGNS with Rahu/Ketu

These extend the canonical dignity.py tables with Rahu/Ketu entries.

**Fix:** Either:
- Add Rahu/Ketu to dignity.py's canonical tables (dignity.py already has them in `_NAISARGIKA`)
- Or import base from dignity.py and extend locally: `_EXALT_SIGN = {**EXALT_SIGN, "Rahu": 1, "Ketu": 7}`

### C2. _SPECIAL_ASPECTS in rule_firing.py

Now that `_planet_aspects_house` delegates to `multi_axis_scoring._aspects`, the local `_SPECIAL_ASPECTS` dict in rule_firing.py is unused.

**Fix:** Delete `_SPECIAL_ASPECTS` from rule_firing.py if nothing else references it.

### C3. nakshatra.py NAKSHATRA_NAMES

nakshatra.py still defines its own `NAKSHATRA_NAMES` list (27 entries). constants.py has the canonical `NAKSHATRA_NAMES` tuple.

**Fix:** Replace with `from src.data.constants import NAKSHATRA_NAMES`. Check callers — some may depend on it being a list vs tuple.

### C4. _D9_START in nakshatra.py

After Phase A resolves the D9 formula, nakshatra.py's local `_D9_START` dict is unused (since `_d9_sign_index` is now imported from varga.py).

**Fix:** Delete `_D9_START` from nakshatra.py.

---

## Phase D: Result Type Consolidation (if time permits)

### D1. HouseScore name collision

`scoring.py:HouseScore` (rule-based, has rules list) vs `house_score.py:HouseScore` (distribution, has mean/std/p10/p90). Different purposes, same name.

**Fix:** Rename `house_score.py:HouseScore` to `HouseScoreDistribution`. Update all callers.

### D2. Yoga result types

6 types: `YogaResult`, `NabhasaYoga`, `GrahaYogaResult`, `PluginYogaResult`, `RajYogaResult`, `NamedYogaResult`.

**Investigation:** Check if these are structurally similar enough to unify with a base class. Only do this if 3+ types share the same fields.

---

## Post-flight

```bash
.venv/bin/pytest tests/ -q --tb=short
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/ob3_calibrate.py --report 2>&1 | grep 'ρ='
# Compare to /tmp/baseline_ob3_w0b.txt
```

## Priority order if context runs out

1. Phase A (D9 formula) — correctness issue, not just duplication
2. Phase B1-B3 (longevity, vimshopaka, nabhasa) — main.py calling BOTH
3. Phase B6 (planetary war) — likely dead code to delete
4. Phase C1-C4 (remaining constants) — quick wins
5. Phase B4-B5, B7-B8 — lower impact
6. Phase D — nice-to-have

## Completion checklist

Before claiming done:
1. How many of the remaining clusters were resolved? (count)
2. Is the D9 formula now correct and unified? (show test output)
3. Does main.py still call both longevity AND ayurdaya? (show grep)
4. Did OB-3 rho regress? (show before/after)
5. How many tests broke and were fixed?
6. Total lines removed (git diff --stat)
