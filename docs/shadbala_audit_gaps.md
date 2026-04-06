# Shadbala Audit — BPHS Ch.27 vs shadbala.py

**Audited:** S317 (2026-04-06)
**Source:** BPHS Santhanam Vol 1, Ch.27 v.1-38 (pp.263-288)
**Code:** `src/calculations/shadbala.py`

## Verified Correct

| Component | BPHS Ref | Code | Status |
|-----------|----------|------|--------|
| Naisargika Bala values | v.14 (p.276): 60/7 × rank | `NAISARGIKA_BALA` | ✅ exact match |
| Naisargika Bala order | Sun>Moon>Venus>Jupiter>Mercury>Mars>Saturn | Same | ✅ |
| Dig Bala peak houses | v.12-15 (p.267) | `DIG_BALA_PEAK_HOUSE` | ✅ |
| Dig Bala formula | diff_from_deduction_house / 3 | `compute_dig_bala()` | ✅ algebraically equiv |
| Kendradi Bala | v.5 (p.266): kendra=60, panapara=30, apoklima=15 | `KENDRADI_VIRUPAS` | ✅ |
| Nathonnata day/night groups | Sun/Jupiter/Venus=day; Moon/Mars/Saturn=night; Mercury=both | Lines 256-258 | ✅ |
| Shadbala thresholds | v.32-33 (p.287): Sun=390, Moon=360, Mars=300, Merc=420, Jup=390, Ven=330, Sat=300 | `is_strong` thresholds | ✅ |
| Drik Bala | v.19 (p.284) — fixed in S317 to use BPHS Ch.26 speculum | `compute_drik_bala()` | ✅ |

## Gaps Found

### GAP 1: Saptavargaja Bala — wrong values + wrong methodology

**BPHS v.2-4 (p.265):** Uses 7-level compound (Panchadha) relationship:

| Level | BPHS Virupas | Code Virupas | Delta |
|-------|-------------|-------------|-------|
| Moolatrikona | **45** | 30.0 | -15 |
| Own sign (Swakshetra) | **30** | 22.5 | -7.5 |
| Adhi Mitra (extreme friend) | **20** | — (missing level) | — |
| Mitra (friend) | **15** | 15.0 | ✅ |
| Sama (neutral) | **10** | 7.5 | -2.5 |
| Shatru (enemy) | **4** | 3.75 | -0.25 |
| Adhi Shatru (extreme enemy) | **2** | 1.875 | -0.125 |

**Methodology gap:** BPHS requires computing the compound (Panchadha Maitri) relationship between the planet and the sign lord for EACH of the 7 vargas individually. This is chart-dependent. The code uses simple dignity levels which conflate exaltation with friendship.

**To fix:** Requires calling `panchadha_relation()` per varga position. The `panchadha_maitri.py` module already exists and is verified correct.

**Impact:** Saptavargaja is one of the largest Sthana Bala components (0-315 virupas across 7 vargas). Wrong values here affect the entire Shadbala total.

### GAP 2: Ojhayugma Bala — missing Navamsa check

**BPHS v.4 (p.265):** "These are applicable to such Navamsas also."

Should check BOTH Rasi AND Navamsa independently:
- Male planet in odd Rasi: +15 virupas
- Male planet in odd Navamsa: +15 virupas
- Maximum: 30 virupas

**Code:** Gives 30 for Rasi match only, 0 for non-match. No Navamsa check.

**To fix:** Compute planet's Navamsa sign, check odd/even independently. Add 15 per match.

### GAP 3: Chesta Bala — wrong formula

**BPHS v.24-25 (p.285):** For Mars to Saturn:
```
Chesta Kendra = Apogee - (mean_longitude + true_longitude) / 2
If > 180°, deduct from 360°.
Chesta Bala = Chesta Kendra / 3
```

**For Sun (v.18, p.284):** Sun's Chesta Bala = Sun's Ayana Bala.
**For Moon (v.18, p.284):** Moon's Chesta Bala = Moon's Paksha Bala.

**Also (v.21-23, p.284-285):** 8 types of planetary motion with assigned strengths:
- Vakra (retrograde): 60
- Anuvakra (retrograde in prev sign): 30
- Vikala (stationary): 15
- Manda (slow): 30
- Mandatara (slower): 15
- Sama (somewhat increasing): 7.5
- Chara (fast): 45
- Atichara (accelerated into next sign): 30

**Code:** Uses `speed / mean_speed` ratio scaled to 0-60. This is a different formula entirely. The BPHS formula requires mean longitude and apogee (Seeghrocha), not speed.

**To fix:** Need mean longitudes (from ephemeris) and planetary apogees. The 8-motion classification is an alternative/complementary system.

### GAP 4: Nathonnata Bala — binary instead of continuous

**BPHS v.8-9 (p.268):** Uses Natha ghatis (time units from midnight/noon):
```
Natha Bala = |Natha ghatis - 30| / 30 × 60 virupas
```
This gives a continuous 0-60 range based on exact birth time.

**Code:** Binary: 60 if born in correct period (day/night), 0 otherwise.

**To fix:** Convert birth time to ghatis, apply the continuous formula.

### GAP 5: Abda/Masa Bala — simplified lord computation

**BPHS v.13 (p.270):** Uses Ahargana (abbreviated days from creation) to compute:
- Abda lord: Ahargana / 360 → weekday of year start → year lord (15 virupas)
- Masa lord: Ahargana / 30 → month start weekday → month lord (30 virupas)

**Code:** Uses weekday of January 1st (Abda) and Sun's sign lord (Masa). Different computations.

**To fix:** Implement Ahargana computation (speculum on pp.271-274 provides tables). Or use modern ephemeris for year/month start dates.

### GAP 6: Ayana Bala — simplified to binary

**BPHS v.15-17 (pp.277-283):** Uses planetary declination (Kranti) with a full speculum table (pp.278-283):
```
Ayana Bala = (23°27' ± Kranti) / (46°54') × 60
```
With sign-specific adjustments for each planet.

**Code:** Binary: 48 or 12 based on Uttarayana/Dakshinayana.

**To fix:** Compute declination from longitude, apply the speculum formula.

### GAP 7: Drik Bala formula nuance

**BPHS v.19 (p.284):** "Reduce one fourth of the Drishti Pinda if a planet has malefic aspects on it and add a fourth if it is aspected by a benefic. Super add the entire aspect of Mercury and Jupiter."

The S317 fix uses continuous BPHS drishti (correct for aspect STRENGTH), but the benefic/malefic adjustment formula differs from the text. BPHS adds/subtracts 1/4 of aspect strength, with a special full-add for Mercury and Jupiter aspects.

**Current code:** Adds full benefic aspect, subtracts full malefic aspect, scaled by 30.

**To fix:** Adjust to 1/4 for general benefic/malefic, full for Mercury/Jupiter.

### GAP 8: Bhava Bala (house strength)

**BPHS v.26-29 (p.286):** Defines Bhava Bala (house-level strength) separate from planetary Shadbala. Sign-specific deduction houses, benefic/malefic adjustments, lord's strength addition.

**Code:** `bhava_bala.py` exists but not audited against these verses.

**To audit:** Separate session — Bhava Bala is house-level, Shadbala is planet-level.

### GAP 9: Per-component minimums

**BPHS v.34-36 (p.288):** Three planet groups with per-component minimums:

| Component | Group A (Jup/Merc/Sun) | Group B (Moon/Ven) | Group C (Mars/Sat) |
|-----------|----------------------|-------------------|-------------------|
| Sthana Bala | 165 | 133 | 96 |
| Dig Bala | 35 | 50 | 30 |
| Kala Bala | 50 | 30 | 40 |
| Chesta Bala | 112 | 100 | 67 |
| Ayana Bala | 30 | 40 | 20 |

**Code:** Only checks total threshold via `is_strong`. No per-component minimums.

**To fix:** Add per-component checks. Low priority — total threshold is the primary check.

## Priority Order for Fixes

1. **Saptavargaja values + Panchadha** (GAP 1) — largest impact on Sthana Bala, infrastructure exists
2. **Chesta Bala formula** (GAP 3) — requires mean longitude computation
3. **Ayana Bala** (GAP 6) — requires declination computation
4. **Nathonnata continuous** (GAP 4) — straightforward time conversion
5. **Ojhayugma Navamsa** (GAP 2) — needs Navamsa sign computation
6. **Drik Bala 1/4 adjustment** (GAP 7) — refinement of current implementation
7. **Abda/Masa Ahargana** (GAP 5) — Ahargana tables available in text
8. **Per-component minimums** (GAP 9) — low priority
9. **Bhava Bala audit** (GAP 8) — separate scope
