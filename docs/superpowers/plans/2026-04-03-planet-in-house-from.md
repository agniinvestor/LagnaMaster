# `planet_in_house_from` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `planet_in_house_from` condition primitive that evaluates "planet A in Nth house from planet B" and migrate 9 existing workarounds to use it.

**Architecture:** New condition type added to taxonomy → validated by builder → evaluated by rule_firing engine. Occupancy mode only. Module-level `_MALEFICS`/`_BENEFICS` constants added to rule_firing for candidate resolution. Migration converts modifier-based workarounds to structured conditions.

**Tech Stack:** Python 3.14, pytest, pyswisseph (existing)

**Spec:** `docs/superpowers/specs/2026-04-03-planet-in-house-from-design.md`

---

### Task 1: Add primitive to taxonomy

**Files:**
- Modify: `src/corpus/taxonomy.py:71-79`

- [ ] **Step 1: Add `planet_in_house_from` to VALID_CONDITION_PRIMITIVES**

```python
VALID_CONDITION_PRIMITIVES = frozenset({
    "planet_in_house", "planet_in_sign", "planets_conjunct_in_house",
    "planets_conjunct", "lord_in_house", "lord_in_sign",
    "planet_aspecting", "planet_not_aspecting", "planet_dignity",
    # New primitives (S313 governance)
    "planet_in_sign_type",
    "planet_in_derived_house",
    "upagraha_in_house",
    "planet_in_house_from",
})
```

- [ ] **Step 2: Verify import works**

Run: `.venv/bin/python -c "from src.corpus.taxonomy import VALID_CONDITION_PRIMITIVES; assert 'planet_in_house_from' in VALID_CONDITION_PRIMITIVES; print('OK')"`

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add src/corpus/taxonomy.py
git commit -m "feat: add planet_in_house_from to condition primitives taxonomy"
```

---

### Task 2: Add builder validation

**Files:**
- Modify: `src/corpus/v2_builder.py:459-478` (after upagraha_in_house block)
- Modify: `src/corpus/v2_builder.py:704-706` (primary condition mapping)

- [ ] **Step 1: Add validation block in `_validate_add()` after the `upagraha_in_house` elif block (after line 478)**

```python
            elif ctype == "planet_in_house_from":
                planet = cond.get("planet", "")
                if not planet:
                    errors.append(
                        f"T1-1: conditions[{i}] planet_in_house_from missing 'planet'"
                    )
                ref = cond.get("reference", "")
                if not ref:
                    errors.append(
                        f"T1-1: conditions[{i}] planet_in_house_from missing 'reference'"
                    )
                elif ref in ("any_malefic", "any_benefic"):
                    errors.append(
                        f"T1-1: conditions[{i}] planet_in_house_from 'reference' must "
                        f"resolve to single planet, not '{ref}'"
                    )
                offset = cond.get("offset")
                if not isinstance(offset, int) or not (1 <= offset <= 12):
                    errors.append(
                        f"T1-1: conditions[{i}].offset={offset} must be int 1-12"
                    )
                mode = cond.get("mode", "")
                if mode != "occupies":
                    errors.append(
                        f"T1-1: conditions[{i}].mode='{mode}' must be 'occupies' "
                        f"(only supported mode)"
                    )
```

- [ ] **Step 2: Add primary condition mapping in `_build_primary_condition()` — add before the `else` block at line 707**

Change the existing line 704:

```python
        elif ct in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
```

to:

```python
        elif ct in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house", "planet_in_house_from"):
```

This ensures the primary_condition dict gets `planet` and `placement_type` populated for backward compat.

- [ ] **Step 3: Test validation accepts valid condition**

Run: `.venv/bin/python -c "
from src.corpus.v2_builder import V2ChapterBuilder
b = V2ChapterBuilder(chapter='Test', category='test', id_start=9900, session='TEST', sloka_count=1, entity_target='native')
b.add(
    conditions=[{'type': 'planet_in_house_from', 'planet': 'Saturn', 'reference': 'Rahu', 'offset': 8, 'mode': 'occupies'}],
    signal_group='test_relative', direction='unfavorable', intensity='moderate', domains=['physical_health'],
    predictions=[{'entity': 'native', 'claim': 'test', 'domain': 'physical_health', 'direction': 'unfavorable', 'magnitude': 0.5}],
    verse_ref='Test v.1', description='Test rule', commentary_context='Test context'
)
print('Validation passed')
"`

Expected: `Validation passed`

- [ ] **Step 4: Test validation rejects invalid conditions**

Run: `.venv/bin/python -c "
from src.corpus.v2_builder import V2ChapterBuilder
b = V2ChapterBuilder(chapter='Test', category='test', id_start=9900, session='TEST', sloka_count=1, entity_target='native')
try:
    b.add(
        conditions=[{'type': 'planet_in_house_from', 'planet': 'Saturn', 'reference': 'any_malefic', 'offset': 8, 'mode': 'occupies'}],
        signal_group='test_bad', direction='unfavorable', intensity='moderate', domains=['physical_health'],
        predictions=[{'entity': 'native', 'claim': 'test', 'domain': 'physical_health', 'direction': 'unfavorable', 'magnitude': 0.5}],
        verse_ref='Test v.1', description='Test', commentary_context='Test'
    )
    print('ERROR: should have raised')
except ValueError as e:
    print(f'Correctly rejected: {e}')
"`

Expected: `Correctly rejected: ...reference...single planet...`

- [ ] **Step 5: Commit**

```bash
git add src/corpus/v2_builder.py
git commit -m "feat: builder validation for planet_in_house_from primitive"
```

---

### Task 3: Add engine evaluation

**Files:**
- Modify: `src/calculations/rule_firing.py:377` (before `else: unknown condition` block)

- [ ] **Step 1: Add module-level constants at top of rule_firing.py (after imports, before functions)**

```python
_MALEFICS = ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
_BENEFICS = ("Jupiter", "Venus", "Mercury", "Moon")
```

- [ ] **Step 2: Add evaluation block before the `else` at line 377**

```python
        elif ctype == "planet_in_house_from":
            planet_spec = cond.get("planet", "")
            ref_spec = cond.get("reference", "")
            offset = cond.get("offset", 0)

            # Resolve reference → must be exactly 1 planet
            resolved_ref = []
            if ref_spec.startswith("lord_of_"):
                h = int(ref_spec.split("_")[-1])
                p = _lord_of_house(chart, h)
                if p:
                    resolved_ref = [p]
            else:
                p = ref_spec.strip().title()
                if _find_planet(chart, p):
                    resolved_ref = [p]

            if len(resolved_ref) != 1:
                return False, 0

            ref_planet = resolved_ref[0]
            ref_house = _planet_house(chart, ref_planet)
            target_house = (ref_house + offset - 1) % 12 + 1

            # Resolve planet → may be multiple (any_malefic, etc.)
            if planet_spec == "any_malefic":
                candidates = list(_MALEFICS)
            elif planet_spec == "any_benefic":
                candidates = list(_BENEFICS)
            elif planet_spec.startswith("lord_of_"):
                lh = int(planet_spec.split("_")[-1])
                lord = _lord_of_house(chart, lh)
                candidates = [lord] if lord else []
            else:
                candidates = [planet_spec.strip().title()]

            valid_candidates = [c for c in candidates if _find_planet(chart, c)]
            if not valid_candidates:
                return False, 0

            hit = any(
                _planet_house(chart, c) == target_house
                for c in valid_candidates
            )
            if not hit:
                return False, 0
            matched_house = matched_house or target_house
```

- [ ] **Step 3: Commit**

```bash
git add src/calculations/rule_firing.py
git commit -m "feat: engine evaluation for planet_in_house_from primitive"
```

---

### Task 4: Write tests

**Files:**
- Modify: `tests/test_rule_firing.py`

- [ ] **Step 1: Add 8 test functions at end of test file**

```python
# ═══ planet_in_house_from tests ══════════════════════════════════════════════

def test_planet_in_house_from_basic():
    """Basic occupancy: planet in Nth house from reference."""
    from src.calculations.rule_firing import _check_compound_conditions
    chart = _get_india_1947_chart()
    # Get actual houses for Saturn and Rahu in India 1947
    from src.calculations.rule_firing import _planet_house
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    # Compute what offset would make Saturn land in its actual house from Rahu
    offset = (saturn_house - rahu_house) % 12 + 1
    # This should fire
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires, f"Saturn should be in {offset}th from Rahu"
    assert house == saturn_house


def test_planet_in_house_from_no_match():
    """Planet NOT in computed house → does not fire."""
    from src.calculations.rule_firing import _check_compound_conditions
    chart = _get_india_1947_chart()
    from src.calculations.rule_firing import _planet_house
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    wrong_offset = (saturn_house - rahu_house + 3) % 12 + 1  # deliberately wrong
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": wrong_offset, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires


def test_planet_in_house_from_any_malefic():
    """any_malefic: fires if ANY malefic in target house."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947_chart()
    jupiter_house = _planet_house(chart, "Jupiter")
    # 5th from Jupiter
    target = (jupiter_house + 5 - 1) % 12 + 1
    # Check if any malefic is there
    malefic_houses = [_planet_house(chart, m) for m in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")]
    expected = target in malefic_houses
    conds = [{"type": "planet_in_house_from", "planet": "any_malefic",
              "reference": "Jupiter", "offset": 5, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires == expected


def test_planet_in_house_from_lord_of_n():
    """lord_of_N as reference: resolves correctly."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house, _lord_of_house
    chart = _get_india_1947_chart()
    lord5 = _lord_of_house(chart, 5)
    lord5_house = _planet_house(chart, lord5)
    moon_house = _planet_house(chart, "Moon")
    offset = (moon_house - lord5_house) % 12 + 1
    conds = [{"type": "planet_in_house_from", "planet": "Moon",
              "reference": "lord_of_5", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires
    assert house == moon_house


def test_planet_in_house_from_offset_1_same_house():
    """offset=1 means same house as reference (conjunction-like)."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947_chart()
    # Find two planets in the same house
    houses = {}
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        h = _planet_house(chart, p)
        if h in houses:
            # Found a pair
            conds = [{"type": "planet_in_house_from", "planet": p,
                      "reference": houses[h], "offset": 1, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires, f"{p} and {houses[h]} should be in same house (offset=1)"
            return
        houses[h] = p
    # If no conjunction exists in this chart, test offset=1 fires when planet IS in ref's house
    # Use Sun as both reference and planet conceptually
    sun_house = _planet_house(chart, "Sun")
    conds = [{"type": "planet_in_house_from", "planet": "Sun",
              "reference": "Sun", "offset": 1, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires


def test_planet_in_house_from_missing_reference():
    """Missing reference planet → (False, 0)."""
    from src.calculations.rule_firing import _check_compound_conditions
    chart = _get_india_1947_chart()
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Pluto", "offset": 8, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert not fires
    assert house == 0


def test_planet_in_house_from_offset_12_wraparound():
    """offset=12: 12th from reference wraps correctly."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947_chart()
    sun_house = _planet_house(chart, "Sun")
    # 12th from Sun = house before Sun
    target = (sun_house + 12 - 1) % 12 + 1
    # target should equal (sun_house + 11) % 12 + 1 = sun_house - 1 (with wrap)
    assert target == ((sun_house - 2) % 12 + 1)
    # Find if any planet is there
    for p in ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        if _planet_house(chart, p) == target:
            conds = [{"type": "planet_in_house_from", "planet": p,
                      "reference": "Sun", "offset": 12, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires
            return
    # No planet there — test that it correctly returns False
    conds = [{"type": "planet_in_house_from", "planet": "Jupiter",
              "reference": "Sun", "offset": 12, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    jupiter_house = _planet_house(chart, "Jupiter")
    assert fires == (jupiter_house == target)


def test_planet_in_house_from_all_candidates_miss():
    """any_benefic but none in target house → False."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947_chart()
    # Pick an offset from Saturn that likely has no benefic
    saturn_house = _planet_house(chart, "Saturn")
    benefic_houses = {_planet_house(chart, b) for b in ("Jupiter", "Venus", "Mercury", "Moon")}
    # Find an offset where no benefic lives
    for off in range(1, 13):
        target = (saturn_house + off - 1) % 12 + 1
        if target not in benefic_houses:
            conds = [{"type": "planet_in_house_from", "planet": "any_benefic",
                      "reference": "Saturn", "offset": off, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert not fires, f"No benefic should be in {off}th from Saturn (house {target})"
            return
```

- [ ] **Step 2: Verify helper function `_get_india_1947_chart` exists in test file**

Check: `grep -n "_get_india_1947_chart\|_india_1947\|compute_chart.*1947" tests/test_rule_firing.py | head -5`

If the fixture is named differently, update the test function calls to match. The India 1947 fixture is `compute_chart(year=1947, month=8, day=15, hour=0.0, lat=28.6139, lon=77.2090, tz_offset=5.5)`.

- [ ] **Step 3: Run tests**

Run: `.venv/bin/pytest tests/test_rule_firing.py -v -k "planet_in_house_from" --tb=short`

Expected: 8 passed

- [ ] **Step 4: Run full suite to check no regressions**

Run: `.venv/bin/pytest tests/ -q --tb=short`

Expected: 14,488+ passed (8 new), 0 failed

- [ ] **Step 5: Commit**

```bash
git add tests/test_rule_firing.py
git commit -m "test: 8 test cases for planet_in_house_from primitive"
```

---

### Task 5: Migrate Ch.16 workarounds (4 rules)

**Files:**
- Modify: `src/corpus/bphs_v2_ch16.py`

- [ ] **Step 1: Migrate BPHS1614 (v.20) — Venus in 9th from Jupiter**

Find the modifiers list for BPHS1614 and replace the `venus_in_9th_from_jupiter` modifier with a structured condition. Add to the conditions list:

```python
{"type": "planet_in_house_from", "planet": "Venus", "reference": "Jupiter", "offset": 9, "mode": "occupies"},
```

Remove the corresponding modifier entry. Keep `ascendant_lord_with_venus` modifier if present (it's a separate condition).

- [ ] **Step 2: Migrate BPHS1616 (v.22) — malefic in 5th from Jupiter**

Find the modifiers list for BPHS1616 and replace `malefic_in_5th_from_jupiter` modifier with a structured condition. Add to conditions:

```python
{"type": "planet_in_house_from", "planet": "any_malefic", "reference": "Jupiter", "offset": 5, "mode": "occupies"},
```

Remove the modifier entry.

- [ ] **Step 3: Migrate BPHS1629 (v.24-32) — Jupiter 5th from Saturn OR vice versa**

This is an OR case. Split into two rules with `rule_relationship: alternative`. The existing rule becomes the Jupiter-from-Saturn variant. Add a new rule for Saturn-from-Jupiter:

For the existing BPHS1629 rule, replace modifier `jupiter_5th_from_saturn_or_vice_versa` with a condition:

```python
{"type": "planet_in_house_from", "planet": "Jupiter", "reference": "Saturn", "offset": 5, "mode": "occupies"},
```

Add `rule_relationship={"type": "alternative", "related_rules": ["BPHS16XX"]}` (use the next available ID).

Add a new `b.add(...)` immediately after with:
- Same predictions, verse_ref, domains, signal_group (append `_alt`)
- Condition: `planet_in_house_from(Saturn, Jupiter, 5, occupies)` + the existing `planet_in_house(any_malefic, 5)` condition
- `rule_relationship={"type": "alternative", "related_rules": ["BPHS1629"]}`

- [ ] **Step 4: Migrate BPHS1630 (v.24-32) — Saturn 5th from Jupiter**

Replace modifier `saturn_5th_from_jupiter` with condition:

```python
{"type": "planet_in_house_from", "planet": "Saturn", "reference": "Jupiter", "offset": 5, "mode": "occupies"},
```

Remove the modifier entry.

- [ ] **Step 5: Verify Ch.16 builds and tests pass**

Run: `PYTHONPATH=. .venv/bin/python -c "from src.corpus.bphs_v2_ch16 import BPHS_V2_CH16_REGISTRY; print(f'OK: {BPHS_V2_CH16_REGISTRY.count()} rules')"`

Run: `.venv/bin/pytest tests/ -q --tb=short -x`

Expected: All pass, no regressions

- [ ] **Step 6: Commit**

```bash
git add src/corpus/bphs_v2_ch16.py
git commit -m "fix: Ch.16 — migrate 4 planet-relative workarounds to planet_in_house_from"
```

---

### Task 6: Migrate Ch.17 workarounds (2 rules)

**Files:**
- Modify: `src/corpus/bphs_v2_ch17.py`

- [ ] **Step 1: Migrate BPHS1713 (v.20-22) — Moon in 12th from Sun (currently unencoded)**

This condition exists only in commentary. Add to the conditions list of the rule for v.20-22 (BPHS1713, signal_group `sun_h6_h8_water_danger_5_9`):

```python
{"type": "planet_in_house_from", "planet": "Moon", "reference": "Sun", "offset": 12, "mode": "occupies"},
```

Update commentary to remove "not encoded" language.

- [ ] **Step 2: Migrate BPHS1719 (v.20) — Saturn in 8th from Rahu**

Replace modifier `saturn_in_8th_from_rahu` with condition:

```python
{"type": "planet_in_house_from", "planet": "Saturn", "reference": "Rahu", "offset": 8, "mode": "occupies"},
```

Remove the modifier entry.

- [ ] **Step 3: Verify Ch.17 builds and tests pass**

Run: `PYTHONPATH=. .venv/bin/python -c "from src.corpus.bphs_v2_ch17 import BPHS_V2_CH17_REGISTRY; print(f'OK: {BPHS_V2_CH17_REGISTRY.count()} rules')"`

Run: `.venv/bin/pytest tests/ -q --tb=short -x`

- [ ] **Step 4: Commit**

```bash
git add src/corpus/bphs_v2_ch17.py
git commit -m "fix: Ch.17 — migrate 2 planet-relative workarounds to planet_in_house_from"
```

---

### Task 7: Migrate Ch.18 workarounds (3 rules)

**Files:**
- Modify: `src/corpus/bphs_v2_ch18.py`

- [ ] **Step 1: Migrate BPHS1818 (v.27) — Venus 7th from Moon + Saturn 7th from Venus**

Replace the two modifiers `venus_in_7th_from_moon` and `saturn_in_7th_from_venus` with two structured conditions:

```python
{"type": "planet_in_house_from", "planet": "Venus", "reference": "Moon", "offset": 7, "mode": "occupies"},
{"type": "planet_in_house_from", "planet": "Saturn", "reference": "Venus", "offset": 7, "mode": "occupies"},
```

Remove both modifier entries. Remove the approximate `planets_conjunct(Venus, Saturn)` condition that was a proxy.

- [ ] **Step 2: Migrate BPHS1834 (v.40-41) — Moon 7th from Venus + Mercury 7th from Moon**

Replace the two modifiers `moon_in_7th_from_venus` and `mercury_in_7th_from_moon` with two structured conditions:

```python
{"type": "planet_in_house_from", "planet": "Moon", "reference": "Venus", "offset": 7, "mode": "occupies"},
{"type": "planet_in_house_from", "planet": "Mercury", "reference": "Moon", "offset": 7, "mode": "occupies"},
```

Remove both modifier entries.

- [ ] **Step 3: Verify Ch.18 builds and tests pass**

Run: `PYTHONPATH=. .venv/bin/python -c "from src.corpus.bphs_v2_ch18 import BPHS_V2_CH18_REGISTRY; print(f'OK: {BPHS_V2_CH18_REGISTRY.count()} rules')"`

Run: `.venv/bin/pytest tests/ -q --tb=short -x`

- [ ] **Step 4: Commit**

```bash
git add src/corpus/bphs_v2_ch18.py
git commit -m "fix: Ch.18 — migrate 3 planet-relative workarounds to planet_in_house_from"
```

---

### Task 8: Post-migration verification

**Files:** none (verification only)

- [ ] **Step 1: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`

Expected: 14,488+ passed, 0 failed

- [ ] **Step 2: Run condition modifier audit**

Run: `PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py 2>&1 | grep -i "relative\|from_jupiter\|from_rahu\|from_moon\|from_venus\|from_saturn\|from_sun"`

Expected: Zero or near-zero results (all workarounds migrated)

- [ ] **Step 3: Run scorecard — verify no regression**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep "Ship-ready"`

Expected: `Ship-ready: 8/16 chapters` (no regression)

- [ ] **Step 4: Check for L2 regressions**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep "L2"`

Expected: `L2=0` for all shipped chapters

- [ ] **Step 5: Run condition modifier audit for Ch.16-18 specifically**

Run: `PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py 2>&1 | grep -E "Ch.1[678]"`

Expected: Significant reduction in medium flags (planet-relative ones eliminated)
