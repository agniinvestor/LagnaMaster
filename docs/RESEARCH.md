# RESEARCH.md — Research Methodology & Validation
> **Update when research milestones are hit, calibration runs, or OSF registrations filed.**

---

## OSF Pre-Registration Status

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
