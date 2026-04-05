# Diagnostic Scoring Equation — Phase 2 Core

**Date:** 2026-04-05
**Session:** S316 (governance)
**Status:** Draft — requires review before implementation
**Scope:** Define the formal scoring function for one domain (H10/Career), grounded in BPHS, with computable formulas.

## Problem

Two scoring systems exist. Neither implements how practitioners evaluate charts:
- System A (23-rule): additive `Σ(weight × rule)` with workbook-invented weights
- System B (600-rule): flat `Σ(favorable - unfavorable) × confidence`

Practitioners evaluate hierarchically: structure → capacity → reinforcement → friction → activation. The scoring equation must formalize this.

## The Equation (Revised — Numerically Stable)

```
BASE = CAPACITY × (1 + α·REINFORCEMENT - β·FRICTION)
CAREER_SCORE = STRUCTURE_WEIGHT × sigmoid(k × BASE) × ACTIVATION
```

Where:
- `STRUCTURE_WEIGHT ∈ [0, 1]` — soft gate via sigmoid (NOT binary)
- `CAPACITY ∈ [0, 1]` — structured sub-components (NOT flat sum)
- `REINFORCEMENT ∈ [0, 1]` — dominant yoga + small secondary
- `FRICTION ∈ [0, 1]` — variance of major components (systematic, not heuristic)
- `ACTIVATION ∈ [0, 1.5]` — graded timing (NOT binary)
- `α = 0.5` — reinforcement scaling
- `β = 0.5` — friction scaling
- `k = 4.0` — sigmoid steepness (tunable)
- Output range: [0, 1] after sigmoid compression

**Why sigmoid:** Raw multiplication of noisy components causes collapse (one weak layer wipes everything) and explosion (reinforcement stacking inflates tails). Sigmoid stabilizes output while preserving ranking.

**Why soft gate:** Practitioners don't hard-cutoff. Weak structure = constrained outcome, not zero. `STRUCTURE_WEIGHT = sigmoid(a × (STRUCTURE_RAW - 0.3))` gives smooth transition around threshold.

## Layer 1: STRUCTURE (Gate)

**Question:** Does the 10th house lord have minimum viability?

**BPHS grounding:** Ch.21 v.1-2 — "If the 10th lord is endowed with strength and is placed in a good house, the native will have good career results. If devoid of strength, obstructions in work."

**Formula:**

```
lord_dignity = dignity_score(lord_of_10, chart)
    # exalted → 1.0, moolatrikona → 0.85, own_sign → 0.75
    # neutral → 0.4, debilitated → 0.1
    # Source: BPHS Ch.3 v.18-22 (dignity hierarchy)

lord_placement = placement_score(lord_of_10, chart)
    # kendra (1,4,7,10) → 0.9, trikona (5,9) → 0.85
    # upachaya (3,6,10,11) → 0.6, neutral (2) → 0.5
    # dusthana (6,8,12) → 0.2
    # Source: BPHS Ch.47 (bhavesh placement effects)

lord_impairment = impairment_score(lord_of_10, chart)
    # combust → -0.3, retrograde_outer → +0.1, retrograde_inner → -0.2
    # planetary_war_loser → -0.4
    # Source: BPHS Ch.3 v.51-59 (combustion), Saravali Ch.4 v.18-22 (war)

STRUCTURE_RAW = 0.5 × lord_dignity + 0.3 × lord_placement + 0.2 × (1 + lord_impairment)
```

Weights (0.5/0.3/0.2): dignity is PRIMARY indicator per BPHS Ch.21 v.1 ("endowed with strength" = dignity first). Placement second. Impairment modifies.

**Soft gate (sigmoid):**
```
STRUCTURE_WEIGHT = sigmoid(8 × (STRUCTURE_RAW - 0.3))
```

Steepness=8 gives: STRUCTURE_RAW=0.1 → weight≈0.08, STRUCTURE_RAW=0.3 → weight=0.5, STRUCTURE_RAW=0.5 → weight≈0.92. Weak structures are suppressed, not zeroed. This matches practitioner behavior: weak charts CAN produce results, just constrained.

**Source mapping to R01-R23:**
- R04 (bhavesh in kendra/trikona) → lord_placement
- R11 (bhavesh in dusthana) → lord_placement
- R15 (bhavesh debilitated) → lord_dignity
- R19 (bhavesh combust) → lord_impairment
- R20 (dig bala) → lord_dignity bonus
- R22 (retrograde) → lord_impairment

## Layer 2: CAPACITY (Weighted Score)

**Question:** How much career support/affliction does this chart have?

**BPHS grounding:** Ch.21 v.3-20 — specific combinations of planets in/aspecting H10 and their effects on career.

**Formula:**

```
house_support = benefic_score(house=10, chart)
    # Each functional benefic in H10: +0.15
    # Each functional benefic aspecting H10: +0.08 (weak condition per BPHS)
    # Yogakaraka in H10: +0.25 (BPHS Ch.34 — highest functional status)
    # Source: R02, R03

house_affliction = malefic_score(house=10, chart)
    # Each functional malefic in H10: -0.15
    # Each functional malefic aspecting H10: -0.08
    # Source: R09, R10

lord_company = association_score(lord_of_10, chart)
    # Benefic conjunct lord: +0.12 per benefic
    # Malefic conjunct lord: -0.12 per malefic
    # Dusthana lord conjunct: -0.10
    # Source: R06, R07, R13, R14, R16

kartari = kartari_score(house=10, chart)
    # Shubha kartari (benefics flanking): +0.10
    # Paapa kartari (malefics flanking): -0.10
    # Source: R08, R12

karaka = karaka_score(house=10, chart)
    # Sun (career karaka) in H10 or aspecting: +0.10
    # Sun in dusthana from H10: -0.08
    # Saturn (profession karaka) similarly
    # Source: R17, R18

ashtakavarga = sav_score(house=10, chart)
    # SAV bindus ≥ 5: +0.10
    # SAV bindus ≤ 3: -0.10
    # Source: R23, BPHS Ch.66

house_sign = sign_quality(house=10, chart)
    # Gentle/benefic sign: +0.05
    # Source: R01

CAPACITY is structured into 3 independently normalized sub-components:

LORD_STRENGTH ∈ [0, 1]:
    = 0.6 × lord_dignity + 0.25 × lord_placement_quality + 0.15 × (1 + lord_impairment)
    # Lord's own condition: dignity dominates (BPHS Ch.21 v.1)

HOUSE_CONDITION ∈ [0, 1]:
    = 0.5 + house_support + house_affliction + kartari + house_sign
    # Net support/affliction on the house itself
    # Clamped to [0, 1]

KARAKA_SUPPORT ∈ [0, 1]:
    = 0.5 + karaka + ashtakavarga
    # Natural significator + planetary support
    # Clamped to [0, 1]

CAPACITY = w1 × LORD_STRENGTH + w2 × HOUSE_CONDITION + w3 × KARAKA_SUPPORT
    where w1=0.45, w2=0.35, w3=0.20
```

**Why structured:** Lord strength, house condition, and karaka support are fundamentally different signals. Summing them flat mixes primary drivers with secondary modifiers. Weighted combination preserves the classical hierarchy: lord is most important (BPHS Ch.21 v.1), house condition second (Ch.21 v.3-7), karaka third (Ch.32).

**Why these weights (0.45/0.35/0.20):** Reflects BPHS ordering. Lord is assessed first and given most importance. House condition is the environment. Karaka is supplementary. These are the calibration targets — the ordering is classical, the magnitudes need empirical validation.

## Layer 3: REINFORCEMENT (Yoga Patterns)

**Question:** Do special combinations amplify the career signal?

**BPHS grounding:** Ch.34-42 (yoga definitions). Ch.21 v.8-20 (specific career combinations).

**Formula:**

```
primary_yoga = max score among active yogas relevant to H10:
    # Dharma-Karma Adhipati Yoga (9th+10th lords connected): 0.4
    # Raja Yoga (kendra lord + trikona lord): 0.3
    # Source: BPHS Ch.34-36

secondary_yogas = sum of minor yoga scores (capped at 0.3):
    # Pushkara Navamsha (lord in auspicious degree): 0.1
    # Bhavesh with kendra/trikona lord: 0.1
    # Source: R05, R21

REINFORCEMENT = min(1.0, primary_yoga + 0.5 × secondary_yogas)
```

**Why max-dominant:** Yoga patterns are not independent — a chart with 5 Raja Yogas isn't 5× better than one with 1. The dominant yoga sets the ceiling; secondary yogas add small increments. `max(primary) + 0.5 × sum(secondary)` prevents artificial stacking while still rewarding multiple patterns.

**Why multiplicative in the equation:** Reinforcement multiplies CAPACITY through `(1 + α·R)`. A yoga in a chart with zero capacity produces nothing. This is explicit in BPHS Ch.34 — yogas "bestow results" only when the chart has structural promise.

## Layer 4: FRICTION (Contradictions)

**Question:** Do conflicting signals reduce the career outcome?

**BPHS grounding:** Ch.21 v.14-16 (specific contradictions mentioned).

**Formula:**

```
FRICTION = variance([LORD_STRENGTH, HOUSE_CONDITION, KARAKA_SUPPORT])

Specifically:
    mean_component = (LORD_STRENGTH + HOUSE_CONDITION + KARAKA_SUPPORT) / 3
    FRICTION = sqrt( ((LORD_STRENGTH - mean)² + (HOUSE_CONDITION - mean)² + (KARAKA_SUPPORT - mean)²) / 3 )
```

Normalized to [0, 1] by dividing by theoretical max variance (0.471 when one component is 0 and others are 1).

```
FRICTION = min(1.0, raw_variance / 0.471)
```

**Why variance, not heuristic list:** Friction is disagreement between major components. A chart where lord is strong (0.9) but house is afflicted (0.2) and karaka is neutral (0.5) has high friction — the signals conflict. This is systematic: it captures ALL contradictions, not just pre-enumerated ones.

**Why separate from capacity:** Capacity is the weighted mean of components. Friction is the spread. Same mean capacity (0.5) with low friction (components all ~0.5) is a stable, predictable outcome. Same mean with high friction (components at 0.9, 0.1, 0.5) is an unstable, volatile outcome. Practitioners explicitly distinguish "mixed chart" from "average chart."

## Layer 5: ACTIVATION (Timing Gate)

**Question:** Is the career domain activated right now?

**BPHS grounding:** Vimshottari Dasha system — BPHS Ch.46.

**Formula (v1 — crude):**

```
md_lord = current_mahadasha_lord(chart, date)
ad_lord = current_antardasha_lord(chart, date)

md_relevance:
    md_lord == lord_of_10 → 1.0 (direct activation)
    md_lord is karaka of H10 → 0.7 (karaka activation)
    md_lord aspects H10 → 0.5 (aspectual activation)
    else → 0.2 (dormant — reduced, not zero)

ad_modifier:
    ad_lord reinforces md → 1.3 (aligned sub-period)
    ad_lord neutral → 1.0
    ad_lord contradicts → 0.7

ACTIVATION = clamp(md_relevance × ad_modifier, 0.1, 1.5)
```

Range [0.1, 1.5]: dormant periods suppress but don't zero out; peak periods can amplify beyond base.

**Without activation:** Set ACTIVATION=1.0 for natal promise assessment. With activation, score becomes event potential for a specific time period.

## Complete Equation

```
CAREER_SCORE = STRUCTURE_GATE × CAPACITY × (1 + 0.5 × REINFORCEMENT) × (1 - 0.5 × FRICTION) × ACTIVATION
```

Range: [0, 1] where:
- 0 = no career potential (structure gate failed or dormant timing)
- 0.25 = weak career indication
- 0.5 = average/neutral
- 0.75 = strong career indication
- 1.0 = exceptional (all layers aligned)

## Grounding Audit

Every term traces to a classical source:

| Component | Variables | Classical Source |
|-----------|-----------|-----------------|
| lord_dignity | 5-level scale | BPHS Ch.3 v.18-22 |
| lord_placement | kendra/trikona/dusthana | BPHS Ch.47 |
| lord_impairment | combust/retrograde/war | BPHS Ch.3 v.51-59, Saravali Ch.4 |
| house_support | benefics in/aspecting | BPHS Ch.11, Ch.21 v.3-7 |
| house_affliction | malefics in/aspecting | BPHS Ch.11, Ch.21 v.14-16 |
| lord_company | planets conjunct lord | BPHS Ch.21 v.8-13 |
| kartari | flanking planets | Phaladeepika Ch.6 |
| karaka | natural significator | BPHS Ch.32 |
| ashtakavarga | SAV bindus | BPHS Ch.66 |
| yoga patterns | specific combinations | BPHS Ch.34-42 |
| friction | contradictions | BPHS Ch.21 v.14-16 |
| activation | dasha lord | BPHS Ch.46 |

## What's NOT Grounded (Honest)

| Parameter | Value | Source | Honest assessment |
|-----------|-------|--------|-------------------|
| Structure weights (0.5/0.3/0.2) | Dignity > Placement > Impairment | Implied by BPHS Ch.21 ordering | Reasonable inference, not explicit in text |
| α (reinforcement scaling) | 0.5 | Engineered | No classical basis. Caps yoga amplification at 50%. |
| β (friction scaling) | 0.5 | Engineered | No classical basis. Caps contradiction reduction at 50%. |
| Gate threshold (0.3) | Debilitated + dusthana + impaired = gate | Practitioner consensus | Not a specific verse. General principle. |
| Individual effect magnitudes (+0.15, -0.08, etc.) | See capacity layer | Engineered from relative classical importance | Ordered correctly by BPHS (benefic in > benefic aspecting) but exact numbers are not from text. |

These parameters are the calibration targets. BPHS defines the STRUCTURE (what matters, in what order). The MAGNITUDES need empirical calibration — which is what Phase 6 ML was designed to do.

## Mapping to Existing Infrastructure

| Equation Component | Existing Code | Status |
|-------------------|--------------|--------|
| dignity_score | `_planet_dignity_state()` in rule_firing.py | Exists (5-level) |
| lord_placement | `_planet_house()` in rule_firing.py | Exists |
| combust/retrograde | `compute_all_dignities()` in dignity.py | Exists |
| functional_benefic | `compute_functional_classifications()` | Exists (S316) |
| planet_aspecting | `_planet_aspects_house()` in rule_firing.py | Exists |
| kartari | `_kartari()` in multi_axis_scoring.py | Exists |
| karaka | sthira karaka assignments in existing_rules.py | Exists |
| ashtakavarga | `compute_all_ashtakavarga()` | Exists |
| yoga detection | V2 rules Ch.34-42 conditions | Primitives exist (S316), chapters not encoded |
| dasha | Vimshottari computation | Exists |

**Every computational building block already exists.** The equation is the assembly instructions.

## Implementation Plan

1. Create `src/calculations/diagnostic_scorer.py` — implements the 5-layer equation
2. Use existing computational functions (no new computation needed)
3. Test on India 1947 fixture first (sanity check)
4. Run H10 separation test on 4,832 ADB charts
5. Compare against System A (23-rule additive) and System B (V2 flat)
6. If separation improves → the hierarchical model captures signal that additive missed
7. If separation doesn't improve → either the parameters are wrong or the classical structure doesn't map to ADB outcomes

## Validation: 3-Way Comparison Test

The equation is a HYPOTHESIS about how astrology works mathematically. It must be tested against alternatives.

**Test protocol:**

Score all 4,832 ADB charts on H10 using three models. For each, compute top-30% vs bottom-30% career outcome separation.

| Model | Equation | What it tests |
|-------|----------|---------------|
| Model A (baseline) | `Σ(workbook_weight × rule_fires)` — current 23-rule additive | Does the existing system produce separation? |
| Model B (hierarchical) | The equation above — structure × sigmoid(capacity × modifier) × activation | Does hierarchical scoring improve separation? |
| Model C (simplified) | `STRUCTURE_WEIGHT × CAPACITY` only — no reinforcement, no friction | Is the basic hierarchy enough, or do yoga/friction layers add signal? |

**Success criteria:**
- Model B separation > Model A separation → hierarchy adds signal
- Model B separation > Model C separation → reinforcement/friction layers add signal
- If Model A > Model B → hierarchical model is worse than additive (equation is wrong)
- If Model C ≈ Model B → reinforcement/friction are noise (simplify)

**Implementation:**
- `src/calculations/diagnostic_scorer.py` — Model B
- `tools/ob3_calibrate.py` — already has Model A
- Model C = diagnostic_scorer with reinforcement=0, friction=0

**Run with ACTIVATION=1.0 for all charts** (natal promise only, no timing). Timing tested separately after natal equation is validated.

## What This Does NOT Solve

- Weight magnitudes are still engineered (calibration is Phase 6)
- Yoga detection is limited (Ch.34-42 not yet encoded)
- Timing is crude (binary v1)
- Only H10 — other domains need their own equations (similar structure, different karakas/lords)
- ADB label quality is still the ceiling
