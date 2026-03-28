# RESEARCH.md — Research Methodology & Validation
> **Update when research milestones are hit, calibration runs, or OSF registrations filed.**

---

## OSF Pre-Registration Status
### Primary Research Hypothesis (must be the OSF filing at S461)

The primary scientific question is NOT "does rule R04 predict career outcomes?"
That question tests a tiny fragment of a 5,000-year tradition and produces findings
that can be dismissed as testing an unrepresentative sample.

**The primary hypothesis is:**
> Multi-factor classical convergence — specifically, the simultaneous agreement of
> Parashari house scoring, KP sublord analysis, and Jaimini karakamsha, combined with
> Layer II structural activation (dasha capacity × transit delivery) — predicts
> life outcome domains at a statistically validated rate **above any single school's
> baseline**, as measured by Brier score improvement and signal isolation above user
> prior probability.

**Why this is the right hypothesis:**
1. It is novel — no published study has tested whether cross-school concordance
   is itself a predictive signal, independent of any single school's accuracy
2. It is directly testable — the concordance score is a computed number; outcomes
   are binary confirmed/disconfirmed events; the signal isolation formula cleanly
   separates planetary signal from base rate
3. It is defensible if negative — a null result (concordance not predictive above
   individual schools) is a genuine scientific contribution that constrains future
   astrology research
4. It is the question that justifies the architecture — if multi-factor convergence
   is NOT more predictive than single-school analysis, the entire convergence model
   needs rethinking before Phase 7 product launch

**Secondary hypotheses (also pre-registered, tested after primary):**
- Category A: Individual rules that survive BH FDR correction at q<0.05
- Category C: Classical rules with significant negative predictive validity
  (fire when outcome doesn't occur more than expected by chance)
- Interaction hypothesis: Does Layer I × Layer II interaction predict better than
  either layer alone? (Tests whether structural activation adds information above
  classical concordance)

**OSF filing must specify:**
- Primary hypothesis stated above
- Convergence score computation (exact formula as implemented)
- Signal isolation formula (`confidence_mean − user_prior_prob_pre`)
- BH FDR correction at q<0.05 for all secondary hypotheses
- Time-split cross-validation: pre-2010 train, 2010+ test
- Minimum sample: 1,000 training-eligible confirmed events
- Stopping rule: no analysis before minimum sample reached, regardless of schedule

---



| Registration | Status | Covers |
|-------------|--------|--------|
| OB-3 XGBoost analysis | 🔴 **NOT YET FILED** | Feature V1, hypotheses, BH FDR at q<0.05, time-split CV |
| Full corpus SHAP analysis | 🔴 **NOT YET FILED** | Feature V2, yoga hypotheses, 1,500+ rules |

**Rule:** Every empirical analysis must be filed on OSF BEFORE execution. Analyses without prior registration labeled 'exploratory only' and cannot promote rules to the engine.

---

## OB-3 Calibration (Current Baseline)

**File:** `calibration_ob3.json`  
**Method:** Mann-Whitney U test of house scores against ADB outcomes

| Result | Value | Interpretation |
|--------|-------|----------------|
| Global rho | **0.40** | ✅ Real signal — global discrimination works |
| Axis-specific r (average) | **~0.02** | 🔴 Conditional weights needed (S194 target) |

**Root cause of axis-specific failure:** Static weights treat Saturn yogakaraka identically to Saturn functional malefic. S194 conditional weight functions (`weight_manager.py`) address this.

---

## Data Quality Issues

### ADB (Astro-Databank) Bias
- Only "notable" people — skewed to men, wealthy, English-speaking
- Survivorship bias: notable people tend to live longer
- Most from pre-1900 — cohort bias
- **Current license:** 200+ fixture charts; full 55,000+ requires license request: `adbdata@astro.com`
- **Mitigation:** Within-stratum pairwise ranking. Control for birth year, gender, nationality in all regressions.

### Autobiographical Memory Bias
- Events misdated by average **3–6 months** even for significant events within 5 years
- Negative events dated as more recent (telescoping effect)
- **Mitigation:** Date anchoring UI (show active dasha lord per month selected), confidence weights (exact=1.0, month+year=0.7, year-only=0.3)

### Negativity Bias in Feedback
- Negative events recalled more accurately and dated more precisely
- Will systematically over-confirm malefic rules (Saturn, Mars, Rahu)
- **Mitigation:** Differential prompting; intensity rating for negative events (high intensity = stronger weight)

---

## SHAP Analysis Framework (Phase 6, S701–S730)

### Three Result Categories

| Category | Definition | Action |
|----------|-----------|--------|
| **A: Confirmed** | Pre-specified + FDR-passed | Promote to engine with higher weight |
| **B: New Discovery** | FDR-passed but not pre-specified | File OSF amendment, replicate before using |
| **C: Challenged** | Pre-specified + FDR-FAILED | Flag in corpus, DO NOT remove without replication |

**Category C is scientifically most important:** potentially 2,000-year-old confirmation biases. Document with intellectual honesty.

### Cross-Validation Strategy
- **Primary:** Time-split (pre-2010 train, 2010+ test) — prevents temporal data leakage
- **Secondary:** Leave-one-group-out by profession category (controls for notability bias in ADB)
- BH FDR correction at q<0.05 — mandatory, no exceptions

---

## Signal Isolation Architecture
### Convergence State Must Be Recorded at Prediction Time

The feedback schema (Phase 3) must capture not just the user's prior probability and
the outcome — it must also capture the **convergence state at the time of prediction**.
This is the schema addition that makes Phase 6 Bayesian updates scientifically valid:

```sql
-- Required additions to predictions table (Phase 3 schema):
ALTER TABLE predictions ADD COLUMN layer1_concordance_score FLOAT;    -- e.g., 0.82
ALTER TABLE predictions ADD COLUMN layer1_varga_agreement   TEXT;      -- "★★", "★", "○"
ALTER TABLE predictions ADD COLUMN layer2_promise_strength  TEXT;      -- "Strong", "Moderate", "Weak", "Negated"
ALTER TABLE predictions ADD COLUMN layer2_capacity_met      BOOLEAN;   -- dasha lord check passed
ALTER TABLE predictions ADD COLUMN layer2_delivery_met      BOOLEAN;   -- transit gate passed
ALTER TABLE predictions ADD COLUMN convergence_tier         TEXT;      -- "Full", "L1+L2", "L1_only"

-- "Full" = all three layers active (not available until Phase 6)
-- "L1+L2" = classical + structural convergence (available from Phase 2)
-- "L1_only" = classical concordance only (current state)
```

Without `convergence_tier` recorded at prediction time, the Bayesian update pipeline
in Phase 6 will average together:
- Confirmed predictions that succeeded because all layers agreed (signal)
- Confirmed predictions that succeeded despite low concordance (possibly noise)

These produce opposite training signals and must not be averaged.



```
user_prior_prob_pre (captured BEFORE prediction shown)
        ↓
signal_strength = confidence_mean - user_prior_prob_pre
```

If engine says 70% and user expected 65% → signal = +5pp (weak — possibly just base rate)  
If engine says 70% and user expected 20% → signal = +50pp (strong planetary signal)

**hindsight_delta** (novel — no competitor tracks this):
```sql
hindsight_delta = feedback.user_prior_prob - predictions.user_prior_prob_pre
```
High hindsight_delta + confirmed event = strongest training signal (event was surprising).  
This field alone is worth a methodology paper in the Journal of Judgment and Decision Making.

---

## Bayesian Weight Update

**Trigger:** 1,000+ `is_training_eligible=True` feedback events  
**Update magnitude proportional to:** `signal_strength` × credibility weight  
**`is_training_eligible`:** `occurrence_certainty ≥ 0.7` AND `report_confidence ≥ 0.6`

**Push threshold (signal/noise ratio):**
```
signal_to_noise = confidence_mean / confidence_std ≥ 2.0
```
Early lifecycle: std large → few predictions pushed.  
After 10K events: std shrinks → more predictions pushed.

---

## The Scientific Moat

| Moat | Why irreplicable |
|------|-----------------|
| OSF pre-registration timestamp | AstroSage cannot pre-register a study that didn't exist before. The timestamp is a permanent scientific credibility asset. |
| `user_prior_prob_pre` field | No existing astrology platform captures what the user believed BEFORE seeing the prediction. Hindsight delta is publishable methodology. |
| Confirmed events database at T+2 years | At 500K+ events, empirically calibrated rule weights are non-replicable. |
| Category A/C SHAP findings | Published, pre-registered analysis showing which classical rules are confirmed (A) and which are 2,000-year-old confirmation biases (C). |
