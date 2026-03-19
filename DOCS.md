# LagnaMaster — Technical Documentation

> Last updated: 2026-03-20 | Sessions 1–32 | 717/717 tests

## New in Phase 4 (Sessions 28–32)

### `src/calculations/functional_roles.py` (Session 28)

Per-lagna functional role matrix — the most critical under-modeled layer.

```python
roles = compute_functional_roles(chart)
roles.yogakarakas          # planets ruling kendra+trikona simultaneously
roles.badhaka_house        # 11 (moveable) / 9 (fixed) / 7 (dual) lagna
roles.badhaka_lord         # lord of badhaka house
roles.maraka_lords         # H2 + H7 lords
roles.dusthana_lords       # H6 + H8 + H12 lords
roles.functional_benefics  # lagna-specific, not universal
roles.functional_malefics  # lagna-specific
roles.is_yogakaraka(p)     # True if planet is yogakaraka for this lagna
roles.is_functional_malefic(p)
```

**Key insight**: Venus rules H1+H6 for Sagittarius lagna — making it both lagna lord (protective) and H6 lord (challenging). This dual-role is computed correctly by the functional matrix.

### `src/calculations/avastha.py` (Session 29)

Three classical planetary state systems:

```python
report = compute_all_avasthas(chart)
report.deeptadi["Jupiter"]    # "Deepta"/"Swastha"/"Mudita"/"Shanta"/"Dukha"/"Kshobhita"
report.baladi["Saturn"]       # "Bala"/"Kumara"/"Yuva"/"Vriddha"/"Mrita"
report.lajjitadi.state        # "Lajjita"/"Kshobhita"/"Kshudhita"/"Trushita"/"Garvita"/"Mudita"
report.lajjitadi.pressure_score  # 0.0–1.0
report.effective_multipliers  # deeptadi × baladi per planet
```

**Lajjita** (5th lord ashamed) = highest pressure state. Occurs when 5th lord is in dusthana with malefics or combust. Strong correlation with psychological burden, creative grief, anxiety.

### `src/calculations/pressure_engine.py` (Session 30)

**The Life Pressure Index** — the central missing capability.

```
PressureIndex = (structural_vulnerability/10 × dasha_activation × transit_load / resilience) × 10
```

Four components:
1. `structural_vulnerability(chart)` → float [0..10] — natal baseline from Moon condition, Saturn-Moon, badhaka, dusthana interlocking, Lajjitadi
2. `dasha_activation_weight(chart, dashas, date)` → float [0..2] — amplifies when MD/AD lords are functional malefics, badhaka lords, or marakas
3. `transit_load(chart, date)` → float [0..2] — Sade Sati, Saturn/Rahu over lagna, malefic clusters
4. `resilience_factor(chart, dashas, date)` → float [0.5..2.0] — Jupiter strength, yogakaraka dasha, Jupiter transit over Moon kendra

```python
# Single date
point = compute_pressure_index(chart, dashas, date(2026,6,15))
print(f"{point.pressure_index:.1f} — {point.label}")
print(f"Drivers: {point.key_drivers}")

# Timeline
timeline = compute_pressure_timeline(chart, dashas,
    from_date=date(2024,1,1), to_date=date(2028,12,31), step_months=3)
crisis_periods = [p for p in timeline if p.is_elevated]
```

Labels: Tranquil (<2.5) / Mild (<4.0) / Moderate (<5.5) / Elevated (<7.0) / High (<8.5) / Critical (≥8.5)

### `src/calculations/argala.py` (Session 31)

Jaimini Argala + Arudha Lagna:

```python
# Argala on Lagna
argala = compute_argala(chart, reference_house=1)
argala.net_argala_score    # positive = net support, negative = obstruction
argala.entries             # list of ArgalaEntry per argala house
for e in argala.entries:
    print(f"H{e.house_from_reference} argala: {e.net_effect} ({e.nature})")

# Arudha Lagna
al = compute_arudha_lagna(chart)
al.arudha_lagna_sign       # social mirror sign
al.al_condition            # "Strong"/"Afflicted"/"Mixed"/"Neutral"
al.pressure_note           # explanation
```

### `src/calculations/scoring_v2.py` + `graha_yuddha.py` (Session 32)

```python
# Graha Yuddha
wars = compute_graha_yuddha(chart)
for w in wars:
    print(f"{w.winner} defeats {w.loser} in {w.sign} (sep={w.separation_degrees:.3f}°)")

# Scoring Engine v2
from src.calculations.scoring_v2 import score_chart_v2, ENGINE_VERSION
scores = score_chart_v2(chart)
print(scores.engine_version)   # "2.0.0" — store alongside each score run
print(scores.summary())
for h, hs in scores.houses.items():
    print(f"H{h}: {hs.final_score:+.2f} | func_malefic_bhavesh={hs.functional_malefic_bhavesh}")
```

v2 differences from v1: functional (lagna-specific) benefic/malefic classification; Graha Yuddha penalty (losers give 50% benefic score); ENGINE_VERSION field on every output; declarative rule results with traceable scoring.

## Test Suite — 717 total

```
S1–S10  pilot          222
S11–S19 features       225
S20–S27 production     210
S28–S32 pressure       36   (test_phase4.py)
                       ────
                        717
Note: functional_roles(9) + avastha(6) + pressure_engine(9) + argala(5) + graha_yuddha+scoring_v2(7) = 36
```

## Remaining gaps (honest assessment)

| Gap | Priority | Notes |
|-----|----------|-------|
| Vimsopaka Bala | High | Divisional chart strength across 16 vargas |
| Full Kala Sarpa Yoga | High | All planets between Rahu/Ketu axis |
| Compound temporal activation (multiplicative) | High | pressure_engine is additive; true multiplicative model needs all three layers formally combined |
| Audit log | Medium | user_id + engine_version per score_run |
| Sandhi sensitivity | Medium | Planets in last/first 1° of sign penalized |
| Grantha Bhanga (war cancellation) | Medium | If war loser is in own/exalt sign, cancels war |
