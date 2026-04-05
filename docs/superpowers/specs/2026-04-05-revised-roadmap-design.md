# Revised LagnaMaster Roadmap — Signal Optimization Era

**Date:** 2026-04-05
**Session:** S316 (governance)
**Status:** Approved
**Trigger:** OB-3 rerun showed 23→600 rules gained only +0.016 ρ. Marginal utility of encoding is near zero for signal improvement. Paradigm shift from feature creation → signal optimization.

## The Empirical Evidence

| Rules | Spearman ρ (avg across 6 axes) | Delta |
|-------|-------------------------------|-------|
| 23 (R01-R23, S203) | 0.44 | baseline |
| 600 (V2 corpus, S316) | 0.46 | +0.016 |
| 25,000 (projected, log-saturation) | 0.49-0.51 | +0.03-0.05 |

**Conclusion:** ~90% of available signal captured by 23 well-chosen rules. Remaining rules provide noise smoothing, not signal discovery. All future ρ gains come from weighting, interactions, timing, and better labels.

## Strategic Frame

**Sequence:** Prediction engine (D) → funds → scientific publication (A) → enables → corpus completion (C)

**North star:** Measurable decision lift on career outcomes within 20 sessions.

**Paradigm:** The system is a signal compression + calibration engine over a fixed semantic space. Rules are redundant projections of latent variables. The problem is weighting, interaction, and activation — not breadth.

## Phase 0+1: Measure + Compress + Weight + Interact (S317-S340)

Six concurrent workstreams. NOT sequential.

### A. Evaluation Infrastructure

Build the measurement system that all subsequent optimization targets.

| Metric | What it measures | Target |
|--------|-----------------|--------|
| Spearman ρ | Rank correlation per axis | ≥0.52 on 3+ axes |
| Brier score | Calibration — are 70% predictions right 70% of the time? | Improving trend |
| Decision lift | Top-decile vs bottom-decile outcome rate | ≥1.5× separation |
| Decile separation | Score spread between positive/negative ADB outcomes | Measurable |

**Decision separation testing runs EVERY iteration.** Not after Phase 1. Inside it. Every weight change, every pruning step → re-check: does top 20% separate from bottom 20% on real ADB outcomes?

### B. Feature Compression

- Marginal contribution analysis: for each of ~228 firing rules, compute Δρ when removed
- Cluster correlated rules into latent factors (50-80 independent signals)
- Kill rules with zero or negative marginal contribution
- **NOT variance-based — contribution-based.** Rare-but-high-leverage signals preserved.

### C. Conditional Weight Engine

```
weight = bphs_base × context_multiplier × interaction_factor
```

Context multipliers (BPHS-grounded):
- Yogakaraka: ×1.5 (BPHS Ch.34)
- Functional benefic/malefic: ×1.2 / ×0.8 (per lagna)
- Dignity: exalted ×1.3, own_sign ×1.1, debilitated ×0.6
- House category: kendra/trikona boost, dusthana penalty
- Shadbala: planet-level strength prior
- Ashtakavarga: house-level strength prior

Regularized: all multipliers constrained to [0.3, 3.0]. No single rule dominates.

### D. Interaction Modeling (CRITICAL — DO NOT DEFER)

First-order planet × planet interactions. These are NOT ML discoveries — they're classical yoga definitions.

Priority interactions (from BPHS):
- Saturn × Jupiter = delayed but massive success (Dharma-Karma Adhipati Yoga)
- Venus × Saturn = relationship challenges with eventual stability
- Mars × Jupiter = courage + wisdom (Guru-Mangal Yoga)
- Sun × Saturn = authority conflicts (Pitru-Dosha)
- Moon × Rahu = emotional turbulence (Grahan Yoga)

Implementation: top 20 graha × graha interactions + top 10 lord × house interactions.

```
interaction_score = base_rule_A + base_rule_B + interaction_bonus(A, B)
```

Where `interaction_bonus` comes from BPHS yoga definitions (source-grounded, interpretable, publishable).

**Expected impact:** Interaction modeling can outperform 10,000 additional rules because it captures the non-linear structure that additive scoring misses.

### E. Early Timing Signal

Binary activation: "active period" (current dasha lord rules relevant house) vs "dormant."

```
effective_score = natal_score × activation_factor
activation_factor = 1.0 if dasha_lord_rules_house else 0.5
```

NOT full dasha computation. Just a crude multiplier. Even this changes predictions from "you are X" to "this is relevant now."

### F. ADB Label Enrichment

Binary → tiered continuous proxies:

| ADB Binary | Enriched Proxy |
|-----------|---------------|
| "Notable: Famous: Top 5%" | Fame tier 5 |
| "Notable: Awards: Vocational" | Fame tier 3 |
| "Vocation: Entertainment: Actor" | Career prominence 4 |
| "Personal: Death: Long life" | Longevity score +1 |
| "Family: Divorce" | Relationship stability -1 |

Career strength score = weighted sum of H10-related categories per person.

### Exit Criteria (ALL must be met)

- ρ ≥ 0.52 on 3+ axes
- Top 20% H10 scores are ≥1.5× more likely to be career-positive than bottom 20%
- Brier score improving trend (not necessarily below threshold)
- At least 3 interaction terms with statistically significant contribution

**If separation doesn't emerge by S335:** Stop weight tuning. The problem is representation, not weights. Redesign feature space.

## Phase 2: Decision Engine + First Revenue (S341-S355)

### Lead Product: Career Trajectory

H10 has 1,910 positive ADB labels across 5 categories — largest signal.

**Output format:**
- Career Acceleration Probability: 0-100% with confidence band
- Top 3 contributing factors (interpretable)
- Active/dormant period indicator (from timing signal)
- Recommendation: "strong growth signal" / "consolidation period" / "transition likely"

**Decision simulation on ADB (proxy):**
- Take top-30% H10 scorers → what % are "Notable/Awards/Leadership"?
- Take bottom-30% → what %?
- If ratio < 1.3×: product has no edge. Do not ship.

**User data collection starts immediately with first users:**
- Every prediction → structured outcome tracking
- "Did you switch jobs in the past 12 months?" (binary)
- "When?" (month/year)
- "What was the result?" (better/same/worse)
- NOT "did this resonate?" — that's sentiment, not signal

### Compute All 6 Axes Internally

Career ships first. Relationship, Wealth, Health, Children, Learning computed and logged but not user-facing. This builds the multi-axis dataset for Phase 3+.

## Phase 3: Timing Engine (S356-S375)

### Full Dasha Activation

The S316 hook (`_is_activated`) gets wired to real dasha computation:
- Mahadasha lord → which houses activated
- Antardasha lord → which sub-themes
- Pratyantardasha → event windows (±3 months)

```
temporal_score = natal_score × md_activation × ad_activation
```

### Event Window Predictions

"Career shift most likely between [month] and [month]"

### Metrics

- Timing hit rate: what % of events fall within predicted window?
- Timing MAE: average error in months
- Event detection: did the predicted event type occur?

### Why This Is Phase 3 (Not Later)

Without timing, the product predicts potential, not reality. A user with strong H10 but dormant career dasha gets a misleading "career acceleration" signal. Timing is not an enhancement — it's a filter on all features.

The early timing signal from Phase 0+1 (binary active/dormant) evolves into continuous activation weights here.

## Phase 4: Data Moat + Scale (S376-S410)

### Structured Outcome Capture (Not Just Feedback)

For every user, capture:
- Decision taken (switched jobs? started business? married?)
- Outcome after 6/12 months
- Timestamp of event
- Counterfactual: "what would have happened without this information?"

**This is the moat.** No one else in astrology has structured, timestamped outcome data linked to birth charts.

### Data Wall (Enforced)

| Dataset | Purpose | Used For |
|---------|---------|----------|
| ADB | Scientific benchmark | OB-4 publication, reproducible research |
| User data | Commercial engine | Weight optimization, timing calibration, product improvement |

Never mixed in the same analysis. Never used interchangeably. ADB results must be reproducible by external researchers.

### ML Residual Correction

```
final_weight = bphs_weight × (1 + ml_adjustment)
```

Where ml_adjustment is learned from user data, constrained to [-0.5, +0.5] range. BPHS prior always dominates. ML discovers what classical texts missed, not what they got wrong.

SHAP analysis on user data → identify hidden interactions and weight corrections.

### Expert Validation Layer

Consultant marketplace:
- Consultants review edge cases where model uncertainty is high
- Their assessments become training labels
- Quality-scored: consultants with higher accuracy get more cases

## Phase 5: Publication + Platform (S411-S440)

### OB-4 Publication

- Pre-registered on OSF with enriched ADB labels
- Dual results section: ADB (scientific) + user data (applied)
- Key claim: "Classical astrological principles, when properly weighted and temporally activated, produce measurable decision lift in career outcome prediction"
- Transparent methodology: BPHS priors + empirical calibration + interaction modeling

### Corpus Encoding Resumes

Now maintenance, not growth. Triggered by:
- Prediction fails systematically on a category → encode relevant chapter
- Model uncertainty high for specific configurations → check if unenoded rules cover it
- User feedback flags gap → targeted encoding

NOT: "encode Ch.35 because it's next in the book."

### Platform

- User predictions + outcome tracking = data flywheel
- Consultant validation = quality layer
- Published research = credibility moat
- API for third-party integrations

## KPI System (Final Form)

### Phase 0+1 KPIs

| KPI | Frequency | Owner |
|-----|-----------|-------|
| Spearman ρ per axis | Every session | Engine |
| Decision separation (top/bottom decile) | Every session | Engine |
| Δρ per session | Every session | Process |
| Feature count (trending down) | Weekly | Engine |
| Interaction term significance | Weekly | Engine |

### Phase 2+ KPIs

| KPI | Frequency | Owner |
|-----|-----------|-------|
| Decision lift vs baseline | Every release | Product |
| Brier calibration score | Every release | Engine |
| User prediction accuracy | Monthly | Data |
| Timing MAE (months) | Monthly (Phase 3+) | Engine |
| Structured outcome capture rate | Weekly | Data |
| Δρ per 100 rules added | Per encoding session | Process (should trend → 0) |

### Anti-Metrics (Things That Must NOT Be Rewarded)

- Rules encoded per session
- Corpus coverage percentage
- Rule firing count
- Total feature count (more features ≠ better)

## Incentive Structure

### For Engine Builders
- Rewarded for: Δρ improvement, calibration gains, interaction discoveries
- Penalized for: adding features without marginal contribution proof

### For Encoders (When Encoding Resumes)
- Rewarded for: rules that produce unique variance contribution (Δρ > 0.001)
- Penalized for: redundant rules, zero-impact additions
- Metric: marginal contribution score per rule

### For Data/Product
- Rewarded for: structured outcome capture, user retention, decision lift
- Penalized for: vanity feedback ("did this resonate?"), unstructured data collection

## The 25,000 Rule Question (Settled)

Encoding all 25,000 rules is a Phase 5 corpus preservation activity, not a signal improvement strategy. Projected gain: r ≈ 0.49-0.51 (diminishing returns curve). The same delta is achievable in ~20 sessions via conditional weights + interactions + timing.

Corpus completeness serves Goal C (knowledge preservation) and Goal A (academic credibility — "we encoded the complete BPHS"). It does NOT serve Goal D (prediction accuracy) or Goal B (commercial viability).

## Kill Conditions (Explicit Failure Criteria)

**These are non-negotiable pivot triggers. If ANY is met, stop current work and reassess.**

| Condition | Trigger | Action |
|-----------|---------|--------|
| **No separation** | After 12 sessions of Phase 0+1, top-20% vs bottom-20% ratio < 1.2× on ANY axis | Stop weight tuning. Problem is feature representation, not weights. Redesign scoring from first principles. |
| **r stalls** | ρ unchanged (±0.005) for 8 consecutive sessions despite active optimization | Current approach exhausted. Either labels are ceiling, features are wrong, or interactions are missing. Run falsification battery. |
| **Decision lift zero** | Phase 2 ships and top-30% vs bottom-30% career outcome ratio < 1.3× | Product has no edge. Do not scale. Return to Phase 1 with different axis or different decision framing. |
| **Timing adds nothing** | Phase 3 timing layer produces < 0.01 ρ improvement on any axis | Dasha activation doesn't help with current label quality. Defer timing, accelerate user data collection instead. |
| **User data contradicts ADB** | User outcomes show negative correlation with ADB-optimized predictions | ADB optimization produced notable-person-specific model, not general model. Retrain from user data only. |
| **Overfitting detected** | Train-test ρ gap > 0.05 on any axis | Model is memorizing ADB, not learning signal. Increase regularization, reduce features, simplify interactions. |

## Overfitting Protocol (Mandatory)

Every optimization step must pass these checks:

1. **Holdout set:** 20% of ADB charts (stratified by Rodden rating) permanently reserved. Never used for weight tuning. Only for validation.
2. **5-fold cross-validation:** All ρ improvements reported as mean ± std across folds. If std > 0.03, result is unstable.
3. **Stability check:** Re-run with 10% data removed randomly. If ρ changes by > 0.02, model is fragile.
4. **Interaction audit:** Every interaction term must improve ρ on holdout, not just training. Interaction terms that only help in-sample are removed.

## Interaction Model (Upgraded)

Interactions are NOT pairwise static. They are context-dependent:

```
interaction_score = f(planet_A, planet_B, house, dignity_A, dignity_B, activation_state)
```

Implementation: lookup table indexed by (graha_pair, context_category):

| Pair | Context | Effect | Source |
|------|---------|--------|--------|
| Saturn × Jupiter | Both in kendra, strong dignity | +1.5 (delayed massive success) | BPHS Ch.34 Dharma-Karma Yoga |
| Saturn × Jupiter | One debilitated | +0.3 (delayed moderate) | Reduced yoga |
| Saturn × Jupiter | Both in dusthana | -0.5 (frustrated ambition) | Yoga cancelled |
| Venus × Saturn | H7, strong | +0.8 (stable late marriage) | Phaladeepika |
| Venus × Saturn | H7, weak | -1.0 (relationship destruction) | Contrary |

NOT a flat `interaction_bonus(A, B)`. Context changes the sign and magnitude.

## Timing Model (Upgraded)

Graded activation, not binary:

```
activation = md_weight × ad_weight × dignity_factor
```

Where:
- `md_weight` = 0.2 (irrelevant lord) to 2.0 (direct house lord in strong dignity)
- `ad_weight` = 0.5 (neutral) to 1.5 (reinforcing)
- `dignity_factor` = current transit dignity of dasha lord

Range: 0.1 (deeply dormant) to 4.5 (peak activation). NOT binary 0.5/1.0.

## Decision Simulation Framework (ADB Proxy)

Decision lift is NOT just "top decile is more notable." It must simulate an action:

**Career decision proxy:**
- Split ADB charts by H10 score: top 30% vs bottom 30%
- Within top 30%: what % have "Vocation: Leadership/Politics/Awards"?
- Within bottom 30%: what %?
- **Decision simulation:** "If model recommended career-aggressive action to top-30% and career-conservative to bottom-30%, would outcomes differ?"
- Lift = (top_outcome_rate / bottom_outcome_rate) - 1.0
- Minimum viable lift: 15%

**Counterfactual proxy:**
- For users who are NOT notable (majority): does H10 score correlate with having any career-related ADB category at all?
- If not, model is biased toward extreme outcomes only → useless for normal users

## Early User Exposure (Within 6 Weeks)

Do NOT wait for Phase 2. By session S325 (week 6):
- 20-50 real users with birth data
- Predictions generated by current model (imperfect is fine)
- Structured outcome capture: career changes in past 2 years, relationship status changes, health events
- Purpose: validate that ADB-optimized model has ANY signal on real people
- If signal = 0 on real users: ADB optimization is the wrong objective. Pivot immediately.

## Risk Register (Updated)

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| ADB label ceiling | High | ρ maxes at ~0.52 | Enriched labels + early user data |
| Interaction overfitting | High | False confidence | Mandatory holdout + fold stability + interaction audit |
| Timing complexity explosion | Medium | Phase 3 delays | Graded activation (not binary), start simple |
| User data too sparse | Medium | Data moat delayed | Start collection at week 6, not Phase 4 |
| Notable-person bias | High | Model useless for normal users | Early user exposure by S325, counterfactual proxy |
| Model fragility | Medium | Beautiful in-sample, fails out-of-sample | 5-fold CV, stability checks, 20% permanent holdout |
| Timeline overrun | High | System never ships | Kill conditions force pivots, not extensions |

## Session Allocation (Realistic — 18-24 Months)

| Phase | Sessions | Calendar (at 2 sessions/week) |
|-------|----------|------------------------------|
| Phase 0+1 | S317-S345 (29 sessions) | ~15 weeks |
| Phase 2 | S346-S370 (25 sessions) | ~13 weeks |
| Phase 3 | S371-S400 (30 sessions) | ~15 weeks |
| Phase 4 | S401-S445 (45 sessions) | ~23 weeks |
| Phase 5 | S446-S480 (35 sessions) | ~18 weeks |
| **Total** | **164 sessions** | **~84 weeks (~19 months)** |

**Note:** Timeline is elastic. Kill conditions may compress or expand phases. Phase 4 is longest because data collection is slow and cannot be parallelized.
