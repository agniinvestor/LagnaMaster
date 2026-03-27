# PREDICTION_PIPELINE.md — The 10-Layer Prediction Quality Architecture
> Each layer is a concrete architectural difference from competitors — not a feature claim.
> Source: LagnaMaster_Appendix_S20_S22.docx (Section 20).

---

## Root Cause of Competitor Failure

All major competitors share the same structural failure: **predictions issued into a void with zero accountability.**

```
Competitor cycle:
1. Input:    User enters birth data. No sensitivity check. ±2hr errors undetected.
2. Chart:    Static weights. Lagna context ignored.
3. Output:   LLMs paraphrase planetary templates.
4. Delivery: Report delivered. Fee charged.
5. Learning: NONE. 2030 AstroSage = 2025 AstroSage.
```

**The root cause is epistemological:** competitors are not trying to be right. LagnaMaster is the first platform measuring its own accuracy and improving it systematically.

---

## Layer 1 — Birth Time Sensitivity Certification

Monte Carlo over ±30 minutes → per-chart confidence grade before any calculation proceeds.

| Divisional Chart | Required Accuracy | Grade |
|-----------------|------------------|-------|
| D1 (natal) | ±2 hours | HIGH for 99% |
| D9 (character, marriage) | ±5 minutes | MEDIUM-HIGH |
| D10 (career) | ±6 minutes | MEDIUM |
| D60 (karmic) | ±1–2 minutes | LOW unless hospital-verified |
| KP sublord | ±30 seconds | LOW for almost all |

**Built:** `confidence_model.py` (S188). **API:** `GET /charts/{id}/confidence`.  
**Gap:** Not yet surfaced in Streamlit UI (UI-1 open issue).  
**Competitor gap:** No competitor computes or communicates birth time sensitivity.

---

## Layer 2 — Personality Verification Protocol (20Q)

Before any future prediction is issued, the engine must demonstrate it correctly understands the user's natal personality.

| Confirmation Rate | Action |
|------------------|--------|
| ≥70% | Full confidence — normal bounds |
| 55–69% | Reduced confidence — wider bounds |
| 40–54% | Low confidence — MD-level only |
| <40% | Prediction suspended — verify birth time |

**Key design (G07):** 10% of question slots = adversarial control questions from different house. True signal = house-specific rate MINUS control rate. If net signal < 5% → measuring agreeableness, not planets.

**Built:** Planned at S531–S555.

---

## Layer 3 — Conditional Weight Architecture

```python
W(rule, planet, house, lagna_si, functional_role, dignity, latitude) → float
```

**Practical difference (live as of S162/S194):**  
Saturn conjunct Moon in H7 from Cancer lagna: score −0.8 (Saturn = functional malefic)  
Saturn conjunct Moon in H7 from Capricorn lagna: score −0.16 (Saturn = yogakaraka)

These are NOT the same prediction. AstroSage issues identical H7 assessments for both lagnas.

**Five factors modulating every weight:**
1. Functional role (yogakaraka, functional malefic, badhaka, maraka)
2. Dignity gradient (paramotcha 1.2 → debilitated −1.0 → neecha bhanga −0.4) — not binary
3. House specificity (kendra/trikona/dusthana/upachaya)
4. Aspect orb (continuous function, not binary)
5. Latitude adjustment (experimental, research-flagged)

---

## Layer 4 — Multi-School Reconciliation and Concordance

| Concordance | Action |
|-------------|--------|
| ≥0.90 (all 3 agree) | Narrow confidence interval — high confidence |
| 0.55–0.75 (2 of 3 agree) | Moderate uncertainty — note school dissent |
| <0.35 (all disagree) | **SUPPRESS** — anti-prediction zone |

**Anti-prediction zone is an accuracy strategy, not a limitation.** We suppress 15–25% of potential predictions. Competitors suppress nothing.

**Built:** Concordance in HouseScore planned at S193. School-mixing fix complete (S162).

---

## Layer 5 — Bayesian Posterior Distributions

```python
# Current: float
# Target (S193): HouseScore distribution
HouseScore(mean=2.3, std=1.1, p10=-0.2, p90=4.8, concordance=0.6)
```

**Push threshold (signal/noise ratio):**
```
confidence_mean / confidence_std ≥ 2.0
```

Early lifecycle: std large → few predictions pushed. After 10K events: std shrinks → more pushed.

---

## Layer 6 — Dasha Sequence Temporal Model

Available granularity: MD → AD → PD → SD → PrD cascade with confidence thresholds.

**Built:** `vimshottari_dasa.py` (S6) + `narayana_dasa.py` (S2). Dasha scoring wired to `score_chart_v3()` (S187).  
**Full temporal model:** Planned at S611–S640.

---

## Layer 7 — Dasha Autobiography Protocol

Users input 5–8 confirmed past life events. Engine reverse-maps each to active dasha + transits. Solves the cold-start problem: every new user generates ~5–8 confirmed training events before the first forward prediction.

**Built:** Planned at S556–S580.

---

## Layer 8 — Signal Isolation via user_prior_prob_pre

```
signal_strength = confidence_mean - user_prior_prob_pre
```

**Most scientifically important field in the system.** Distinguishes:
- Engine correctly identified planetary signal → high signal
- Event was going to happen anyway → low signal (base rate only)

**`hindsight_delta`** = `feedback.user_prior_prob − predictions.user_prior_prob_pre` — measures how surprising the event was. Publishable methodology contribution.

**Built:** Planned at S491–S515. `user_prior_prob_pre` MUST be captured before prediction shown (G04).

---

## Layer 9 — Chart Cluster Empirical Social Proof

HDBSCAN chart embeddings → cluster by structural similarity → empirical data from similar charts appended to predictions.

> "67 users with structurally similar charts confirmed a significant career change during Jupiter MD."

**Growth trajectory:**
- 2026 with 1,000 users: clusters thin (5–15 charts) → "Classical rules only"
- 2029 with 100K users: every cluster has hundreds of confirmed events → full social proof

**`MINIMUM_CLUSTER_SIZE = 30`** — hard-coded constant, can only be raised (G16).  
**Built:** Planned at S731–S745.

---

## Layer 10 — Closed-Loop Empirical Weight Update

After prediction window closes, every confirmed/disconfirmed prediction updates Bayesian posterior for every rule that contributed.

**Update magnitude:** proportional to `signal_strength` (Layer 8) and `is_training_eligible` (certainty ≥ 0.7, confidence ≥ 0.6).

**Trigger:** 1,000+ `is_training_eligible=True` events.  
**Built:** Planned at S746–S760.

---

## Competitor Summary

| Competitor | Layers Present | Consequence |
|-----------|---------------|-------------|
| IndAstro | L1 partial, L3 static, L4 Parashari only | Moon-sign predictions. No accountability. |
| AstroTalk | L1 partial, L3 astrologer judgment | Quality depends on individual astrologer. No standardisation. |
| AstroSage | L1 basic, L3 partial | 70M downloads. "AI" = GPT-4 paraphrasing planetary templates. Not ML. Not outcome-calibrated. |
| Lagna360 | L1 (claimed), L3 (opaque) | Zero methodological transparency. Claims unverifiable. |
| Astro.com | L1 best-in-class (Western), L3 standardised | Best calculation engine in the world for Western astrology. Static output. Not a prediction engine — acknowledged honestly. |
