# PREDICTION_PIPELINE.md — The 10-Layer Prediction Quality Architecture
> Each layer is a concrete architectural difference from competitors — not a feature claim.
> Source: LagnaMaster_Appendix_S20_S22.docx (Section 20).

---

## The Three Convergence Layers

> The GPT formula `Event = Promise × Dasha × Transit × Strength` is a first-year
> textbook simplification. LagnaMaster's actual model has three distinct convergence
> layers that interact. Understanding which layer a module belongs to governs how
> sessions should build, test, and interpret it.

---

### Layer I — Classical Convergence

**What it is:** Agreement across independent classical frameworks pointing at the same outcome.
A prediction gains confidence when Parashari scoring, KP significators, Jaimini karakamsha,
multi-axis LPI, and varga analysis all agree. The anti-prediction zone (concordance < 0.35)
is not a product limitation — it is the correct classical behavior: when three independent
schools genuinely disagree, the truthful answer is "uncertain."

**Modules that contribute (already built):**
`multi_axis_scoring.py` (23 rules × 5 axes), `rule_interaction.py` (30 pairs),
`varga_agreement.py` (★★/★/○ system), `lpi.py` (7-layer weighted score),
`kp_full.py` (sublord school), `jaimini_full.py` (Jaimini school),
`scoring_v3.py` (multi-school concordance output), `school concordance` field in HouseScore.

**Critical principle:** Classical convergence sets the prior. It does not determine
whether the prior is activation-ready. That is Layer II's job.

---

### Layer II — Structural Convergence

**What it is:** Whether the classical promise is activation-ready at this point in time
for this specific person. Three independent structural checks must align:

- **Promise** — D1 score + multi-varga agreement + multi-school concordance confirm
  the theme exists in the natal chart
- **Capacity** — The active dasha lord's natal placement, functional role, argala, and
  AV strength determine whether the dasha can actually deliver the promise
- **Delivery** — Transit trigger, dasha-transit timing alignment, and pratyantar timing
  determine whether the window is open

**Modules that contribute (built):**
`promise_engine.py` (3-level Promise/Capacity/Delivery), `yoga_fructification.py`
(PVRNR p147-148 three conditions), `stronger_of_two.py` (PVRNR p194),
`dasha_scoring.py` (dasha-sensitized scoring), `narayana_argala.py` (argala capacity),
`av_transit.py` (AV transit delivery), `confidence_model.py` (birth time sensitivity),
`vimshottari_dasa.py` + `narayana_dasa.py` (timing cascade).

**Critical principle:** A yoga that exists in Layer I (classically strong) but fails
Layer II (dasha lord weak, no transit trigger, capacity missing) cannot manifest.
The failure is not permanent — the next dasha may activate it.

---

### Layer III — Empirical Convergence

**What it is:** Agreement between the classical model's posterior distributions and
confirmed outcomes from structurally similar charts. This layer is **not yet built**
(Phase 3–6). When operational, it will answer: "Do charts like this, with this
combination of classical convergence signals, actually produce outcomes like this
at a statistically validated rate above base rates?"

**Modules that will contribute (planned):**
Feedback schema with `user_prior_prob_pre` (S491–S515), Bayesian weight update pipeline
(S746–S760), HDBSCAN chart clustering with social proof (S731–S745),
XGBoost + SHAP feature importance analysis (S701–S730).

**Critical principle:** Empirical convergence does not replace classical convergence —
it calibrates it. A classically high-convergence prediction that consistently fails
empirical validation is a Category C finding: a 2,000-year-old rule worth challenging
with intellectual honesty, not abandoning without replication.

---

### Convergence Interaction: The Full Formula

```
Confidence(prediction) =
    f(
        classical_concordance(Parashari, KP, Jaimini, varga),   # Layer I
        structural_activation(promise, capacity, delivery),      # Layer II
        empirical_calibration(posterior, cluster_evidence)       # Layer III [Phase 3+]
    )

Push threshold: signal_to_noise ≥ 2.0
Anti-prediction zone: classical_concordance < 0.35 → SUPPRESS regardless of Layer II
```

**The anti-prediction zone fires on Layer I alone.** Even perfect structural activation
cannot override genuine multi-school classical disagreement. This is intentional: it
would be epistemically dishonest to issue a confident prediction when the classical
tradition itself is divided.

---

### How the 10 Build Layers Map to Convergence Layers

| Build Layer | Convergence Layer |
|-------------|------------------|
| L1: Birth time sensitivity | Layer II — precision of promise |
| L2: 20Q personality verification | Layer II — person-specific calibration of Layer I signals |
| L3: Conditional weight functions | Layer I — depth of classical weight model |
| L4: Multi-school concordance | Layer I — core concordance signal |
| L5: Bayesian posterior distributions | Layer I → III bridge — posteriors updated by Layer III |
| L6: Dasha temporal model | Layer II — capacity and delivery cascade |
| L7: Dasha autobiography | Layer III seed — cold-start training events |
| L8: Signal isolation via prior prob | Layer III — empirical signal above base rate |
| L9: Chart cluster social proof | Layer III — outcome evidence from similar charts |
| L10: Closed-loop weight update | Layer III — recalibration of Layer I weights |

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
