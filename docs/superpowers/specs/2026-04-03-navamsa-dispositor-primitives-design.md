# Design Spec: Navamsa + Dispositor Condition Primitives

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Approved
**Scope:** 2 new condition primitives, 5 rule migrations (1 meta-rule stays as modifier)

## Problem

6 rules have conditions encoded as modifiers requiring navamsa position or dispositor state. 5 are migratable; 1 (BPHS2642) is a global meta-rule that stays as modifier.

## Primitives

### 1. `planet_in_navamsa_sign` — planet's D9 position

```json
{
  "type": "planet_in_navamsa_sign",
  "planet": "Venus",
  "sign": ["Aries", "Scorpio"]
}
```

Fires when the planet's navamsa sign matches. Navamsa computation: divide 30° sign into 9 parts (3°20' each). The navamsa sign sequence starts from the sign itself for movable signs, from the 9th sign for fixed, from the 5th for dual.

Actually — simpler: navamsa sign index = `floor(planet_degree_in_sign / (30/9))` gives the navamsa pada (0-8), then map to sign based on starting sign of the nakshatra cycle. Standard formula:

```python
navamsa_index = int(planet.degree_in_sign / (30/9))  # 0-8
# Starting sign: Aries for fire signs, Cancer for earth, Libra for air, Capricorn for water
FIRE = [0, 4, 8]    # Aries, Leo, Sagittarius
EARTH = [1, 5, 9]   # Taurus, Virgo, Capricorn  
AIR = [2, 6, 10]    # Gemini, Libra, Aquarius
WATER = [3, 7, 11]  # Cancer, Scorpio, Pisces
if planet.sign_index in FIRE: start = 0        # Aries
elif planet.sign_index in EARTH: start = 3     # Cancer
elif planet.sign_index in AIR: start = 6       # Libra
elif planet.sign_index in WATER: start = 9     # Capricorn
navamsa_sign_index = (start + navamsa_index) % 12
```

### 2. `dispositor_condition` — state of a planet's sign-lord

```json
{
  "type": "dispositor_condition",
  "planet": "Rahu",
  "dispositor_state": "in_house",
  "house": 8
}
```

Resolves: "the lord of the sign Rahu occupies" and checks if that lord is in house 8.

Supported `dispositor_state` values:
- `"in_house"` — dispositor is in specified house
- `"dignity"` — dispositor has specified dignity (exalted/debilitated/strong/weak)

```json
{"type": "dispositor_condition", "planet": "Venus", "dispositor_state": "dignity", "dignity": "exalted"}
```

## Blocked Rules → Migration

| Rule | Current modifier | New condition |
|------|-----------------|---------------|
| BPHS1221 | `in_own_rasi_or_navamsa` | `planet_in_navamsa_sign` with own signs |
| BPHS1837 | `venus_in_mars_navamsa_or_conjunct_mars` | `planet_in_navamsa_sign(Venus, [Aries, Scorpio])` |
| BPHS2114 | `navamsa_ascendant_with_malefic` | Complex — navamsa ascendant requires full D9 computation. DEFER. |
| BPHS1841 | `dispositor_of_venus_in_exaltation` | `dispositor_condition(Venus, dignity, exalted)` |
| BPHS2021 | `rahus_dispositor_in_8th` | `dispositor_condition(Rahu, in_house, 8)` |
| BPHS2642 | `dispositor_well_placed...` | Stays as modifier (meta-rule) |

**BPHS2114 deferred:** "Navamsa ascendant with malefic" requires computing the D9 lagna, which is a separate chart computation beyond planet positions. Keep as modifier.

**Net: 4 rules migrated, 2 stay as modifiers.**

## Files Changed

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add `planet_in_navamsa_sign`, `dispositor_condition` |
| `src/corpus/v2_builder.py` | Add validation for both |
| `src/calculations/rule_firing.py` | Add engine evaluation for both |
| `tests/test_rule_firing.py` | Add tests |
| `src/corpus/bphs_v2_ch12.py` | Migrate BPHS1221 |
| `src/corpus/bphs_v2_ch18.py` | Migrate BPHS1837 |
| `src/corpus/bphs_v2_ch18.py` | Migrate BPHS1841 |
| `src/corpus/bphs_v2_ch20.py` | Migrate BPHS2021 |
