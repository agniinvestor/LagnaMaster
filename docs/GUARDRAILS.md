# GUARDRAILS.md — LagnaMaster Master Guardrails
> **Every session from S191 onward must comply with all applicable guardrails BEFORE any code is written.**
> A session shipping in violation of a 🔴 CRITICAL guardrail must be **REVERTED, not patched.**
> Source: LagnaMaster Future State v4 (March 2026).

---

## Severity Key
- 🔴 **CRITICAL** — Non-negotiable blocking requirement. Revert if violated.
- 🟠 **HIGH** — Required before first paid user or public launch.
- 🟡 **MEDIUM** — Required before Series A or significant scale.
- 🟢 **LOW** — Improves quality, not blocking.

---

## Current Compliance Status (Post-S188)

| ID | Priority | Title | Status |
|----|----------|-------|--------|
| G01 | 🔴 | Language: Never use 'prediction' in user-facing UI | 🔴 Not yet implemented |
| G02 | 🔴 | Health content: No illness/death/surgery timing for users | 🔴 Not yet implemented |
| G03 | 🔴 | Privacy: DPDP 2023 + GDPR before first user | 🔴 Not yet implemented |
| G04 | 🔴 | Signal isolation: prior probability captured BEFORE prediction shown | 🔴 Schema not built |
| G05 | 🔴 | Birth time: Never use 'certificate' — use 'Sensitivity Analysis' | 🔴 Not yet implemented |
| G06 | 🔴 | Ayanamsha: KP school requires Krishnamurti — Lahiri produces wrong KP | 🔴 **CURRENTLY VIOLATING** |
| G07 | 🔴 | 20Q: Adversarial control questions mandatory (circular validation risk) | 🔴 Not yet built |
| G08 | 🔴 | Autobiography: Date anchoring interface mandatory (3–6 month misdate avg) | 🔴 Not yet built |
| G09 | 🔴 | Prediction ledger: Research context only — not commercial guarantee | 🔴 Not yet built |
| G10 | 🟠 | Feedback rate: Design for 3–5%, not 15% | 🟠 Not yet addressed |
| G11 | 🟠 | Onboarding: 20Q progressive over 7 days — never a gate | 🟠 Not yet built |
| G12 | 🟠 | Anti-prediction zone: 'Transition period' not 'ambiguous' + return date | 🟠 Not yet built |
| G13 | 🟠 | Revenue: Show locked insight title, not blank wall | 🟠 Not yet built |
| G14 | 🟠 | Adversarial feedback: Credibility scoring before Bayesian pipeline | 🟠 Not yet built |
| G15 | 🟠 | Negativity bias: Differential prompting for positive vs negative events | 🟠 Not yet built |
| G16 | 🟠 | Cluster privacy: Minimum 30 users before social proof display | 🟠 Not yet built |
| G17 | 🟡 | PyJHora license: Algorithm study only — no import in production src/ | 🟡 **Must be first action of S191** |
| G18 | 🟡 | Pre-decision oracle: Brier score context mandatory on all outputs | 🟡 Not yet built |
| G19 | 🟡 | Agency framing: Every output needs 'what you can do' section | 🟡 Not yet built |
| G20 | 🟡 | Twins: Separate analysis track — most valuable natural experiment | 🟡 Not yet built |
| G21 | 🟡 | Localisation: i18n-ready strings from S481 onward — Hindi/Tamil by S860 | 🟡 Not yet built |
| G22 | 🟡 | Pre-registration: No SHAP analysis without OSF filing first | 🟡 0 filings currently |
| G23 | 🟢 | VedAstro MCP: Use during dev sessions for chart verification | 🟢 Not yet installed |
| G24 | 🟢 | VedAstro datasets: Download DOB (15,800) + Marriage (15,000) for ML | 🟢 Not yet downloaded |

---

## Full Guardrail Definitions

### G01 🔴 LANGUAGE: Never use 'prediction' in user-facing UI
Use: `astrological insight`, `timing analysis`, `likelihood assessment`.  
Internal code/DB may use 'prediction' as technical term.  
Applies to: every feature description, push notification, API response field name, marketing material across all jurisdictions.  
**Why:** SEBI (India) regulates investment advice. EU MiFID II may apply to financial outcomes.  
**Fix by:** Before any user-facing feature ships — Q2 2026

---

### G02 🔴 HEALTH CONTENT: No illness, death, or surgery timing for users
Health event timing, illness prediction, surgery timing, mental health events, longevity assessments, death-adjacent content = **NEVER user-facing**.  
Cox survival analysis = internal research only. Biosignal correlations = Research section only.  
**Why:** Indian Medical Council Act; EU MDR 2017/745 (medical device territory); FDA jurisdiction.  
**Fix by:** Before any health-adjacent feature ships

---

### G03 🔴 PRIVACY: DPDP 2023 (India) + GDPR (EU) before first user
Required before any user onboards:
1. Consent ledger (purpose-specific per processing operation)
2. Right-to-erasure pipeline (chart purged; model weights preserved)
3. Data localisation policy (Indian users → Indian data centers)
4. Grievance officer appointed in India
5. Parental consent pathway for under-18
6. Family map requires independent consent per family member
7. DPIA completed for health-adjacent features

**Fix by:** S441 — must precede first user onboarding

---

### G04 🔴 SIGNAL ISOLATION: user_prior_prob_pre MUST be captured BEFORE prediction is shown
**Sequence (non-negotiable):**
1. Show slider: "How likely do you think this event is?" (0–10)
2. Record `user_prior_prob_pre`
3. THEN reveal the astrological assessment

**Any PR removing `user_prior_prob_pre` = REJECT IMMEDIATELY.**  
API layer must enforce this (HTTP 400 if `reveal_prediction` called without `prior_captured_at` set). Schema alone is insufficient.  
**Why:** Hindsight bias permanently corrupts all training data if reversed. Invalidates all signal isolation calculations.  
**Fix by:** S441 — feedback schema ships complete or not at all

---

### G05 🔴 BIRTH TIME: Never use 'certificate' — use 'Sensitivity Analysis'
'Certificate' implies external verification LagnaMaster cannot provide.  
Never suggest uploading hospital records.  
**Correct framing:** "Birth Time Sensitivity Analysis" — how much predictions shift with ±30min variation.  
**Note:** Hospital records log physician's observation time — not the classical birth moment (4 competing definitions: first cry, first breath, cord cutting, full emergence). Document this explicitly.  
**Fix by:** S431 — before birth time sensitivity feature ships

---

### G06 🔴 AYANAMSHA: KP school requires Krishnamurti — Lahiri produces wrong KP results
**Current state: ACTIVELY VIOLATING.** Engine uses Lahiri for all three schools including KP.  
KP predictions with Lahiri are technically incorrect KP. The 249-entry sublord table produces wrong significators.  
**Fix:** Implement ayanamsha selection:
- Lahiri = default (Parashari)
- Krishnamurti = auto-selected when `school='kp'`
- True Chitrapaksha = option
- Store `ayanamsha_used` per chart — changing it makes historical predictions incomparable

**Fix by:** S212 — before any KP predictions issued to users

---

### G07 🔴 20Q VALIDATION: Circular validation requires adversarial control questions
**Problem:** Engine generates 20Q from its own predictions then validates via those same predictions — circular.  
**Rule:** 10% of question slots = control questions from a DIFFERENT house's prediction set.  
**True signal** = `confirmation_rate_house_specific − confirmation_rate_control`  
Questions must: use past-tense verb + time anchor ("In the past 12 months, have you…"). Never signal the desired answer.  
**If net signal < 5%:** Protocol is measuring agreeableness not planets.  
**Fix by:** S481 — before 20Q ships to users

---

### G08 🔴 AUTOBIOGRAPHY: Date anchoring interface mandatory
**Problem:** Autobiographical memory misdates events by 3–6 months on average.  
**Rule:** Show users the active dasha lord for each month they select (memory anchor). Apply date confidence weighting:
- Exact date = 1.0×
- Month + year = 0.7×
- Year only = 0.3×
- Undated events = never used as full-weight training data

**Fix by:** S511 — before autobiography protocol ships

---

### G09 🔴 PREDICTION LEDGER: Research context only — not commercial guarantee
Framing the ledger as a consumer-facing product element creates tort liability.  
All accuracy ledger content must appear in Science/Research section only.  
**Fix by:** Before any accuracy ledger is public-facing

---

### G10 🟠 FEEDBACK RATE: Design for 3–5%, not 15%
The 15% target in v2/v3 has no empirical basis. Industry benchmark for multi-month closure: 3–8% engaged users, 0.5–1% general.  
Shorter initial windows (4–6 weeks) increase closure rate. Push notifications at window close are mandatory.  
**Fix by:** Before product launch — incorporate from S481

---

### G11 🟠 ONBOARDING: 20Q progressive over 7 days — never a gate
- Day 0: full D1 chart + 3 themes immediately
- Days 1–7: 3 questions/day
- Days 14–21: autobiography (1 event/day)
- Never more than 3 questions per session

**Fix by:** S481 onboarding architecture

---

### G12 🟠 ANTI-PREDICTION ZONE: Always give a return date
When concordance < 0.35 suppresses an assessment, say:  
> "[Domain] is in active transition — classical schools disagree on direction, indicating genuine open possibilities. We will give you a [domain] assessment when the picture clarifies in [specific date]."

Never say "too ambiguous to forecast." Always provide a specific return date.  
**Fix by:** S561 — before any user-facing assessment delivery

---

### G13 🟠 REVENUE: Show locked insight title, not blank wall
Free-to-Pro conversion requires showing the title and domain of locked assessments:  
> "A significant career window opens in [LOCKED — upgrade to reveal]"

A blank wall creates no conversion pressure.  
**Fix by:** S691 revenue tier implementation

---

### G14 🟠 ADVERSARIAL FEEDBACK: Credibility scoring before Bayesian pipeline
`credibility < 0.5` users have feedback **down-weighted** (not excluded) in training.  
Detection signals: all predictions confirmed regardless of domain; `occurrence_certainty` always > 0.9; timing always 'in_window'.  
Credibility computed nightly — **never stored as permanent label**.  
**Fix by:** S441 feedback schema — compute before first Bayesian update

---

### G15 🟠 NEGATIVITY BIAS: Differential prompting
Negative events are recalled more accurately — they will systematically over-confirm malefic rules.  
**Rule:**
- Positive predicted events: "Positive outcomes are often absorbed quietly — please reflect on any growth or recognition."
- Negative events: ask intensity (1–5). High intensity = higher training weight.

**Fix by:** S481 feedback interface

---

### G16 🟠 CLUSTER PRIVACY: Minimum 30 users before social proof
Below 30 users in cluster → show "Based on classical rules only — insufficient data from similar charts."  
`MINIMUM_CLUSTER_SIZE = 30` is a **hard-coded constant that can only be raised, never lowered.**  
**Fix by:** S631 HDBSCAN clustering

---

### G17 🟡 PYJHORA LICENSE: Algorithm study only — no import in production src/
PyJHora is AGPL-3.0. Study algorithms; reimplement independently.  
VedAstro (MIT) and jyotishganit (MIT) CAN be imported.  
**Action:** Add ruff rule: no jhora imports permitted in `src/`. Enforce in CI.  
**Fix by:** S191 — **must be first commit of Phase 0**

---

### G18 🟡 PRE-DECISION ORACLE: Brier score context mandatory
Display: "This assessment is based on [N] confirmed events. Our current Brier score is [X] — meaning our [Y]% assessments have been accurate [Z]% of the time."  
Until Brier < 0.15: include "Our assessment accuracy is still improving. Use this as one input among many."  
**Fix by:** S731 — before pre-decision oracle feature ships

---

### G19 🟡 AGENCY FRAMING: Every output needs 'what you can do' section
Classical Jyotish is non-deterministic. Every output includes:  
> "During this period, these themes tend to activate strongly. Here is what heightened awareness and intentional action during this window might look like."

Remedies framed as agami karma action, not magical mitigation.  
**Fix by:** S561 — language layer

---

### G20 🟡 TWINS: Separate analysis track
Twin detection flag in onboarding: "Do you have a twin? Y/N."  
If yes → dedicated twin validation track.  
**Twin feedback NEVER averaged into general Bayesian update pool.**  
Twins with different outcomes for near-identical charts = most valuable natural experiment.  
**Fix by:** S810

---

### G21 🟡 LOCALISATION: i18n-ready strings from S481 onward
All user-facing text uses i18n key lookups from S481. No hardcoded English strings in user-facing code after that.  
Hindi and Tamil by S860. Cultural calibration: probability framing differs by language.  
**Fix by:** S481 — all onboarding strings use i18n keys

---

### G22 🟡 PRE-REGISTRATION: No SHAP analysis without OSF filing first
Every empirical analysis filed on OSF BEFORE execution:
- Exact feature definitions, hypotheses, significance threshold
- Correction method (BH FDR at q<0.05)
- Cross-validation strategy (pre-2010 train, 2010+ test)
- Planned sample size, stopping rule

Analyses without prior registration labeled 'exploratory only' — cannot promote rules to engine.  
**Fix by:** S461 — before S611 SHAP run

---

### G23 🟢 VEDASTRO MCP: Use during development for chart verification
VedAstro MCP Server connects Claude directly to Vedic calculations during development. Use to verify chart calculations, yoga detection, dasha computations in real time. **Not a production dependency.**  
**Fix by:** S191 — install immediately as dev tool

---

### G24 🟢 VEDASTRO DATASETS: Download for ML
- `vedastro-org/15000-Famous-People-Birth-Date-Location` — 15,800 records, Rodden AA, MIT license
- `vedastro-org/15000-Famous-People-Marriage-Divorce-Info` — 15,000 marriage/divorce records

**Fix by:** S191 — download to `data/vedastro/`

---

## G25 🟠 CONVERGENCE COMMUNICATION: Never present Layer I as fully calibrated before Layer III is active

**Rule:** The user interface must distinguish what convergence layer is active when a
prediction is issued. This does not require technical language — but it does require
honest framing.

**Before Phase 6 (Layer III not yet active):**
> "This assessment is based on agreement across multiple classical frameworks
> [what percentage of the time this chart configuration points in the same direction].
> It has not yet been validated against confirmed outcomes from similar charts."

**After Phase 6 (Layer III active, Brier score < 0.20):**
> "This assessment is supported by classical analysis AND has been validated against
> [N] confirmed outcomes from charts with similar configurations."

**Why this is a guardrail and not just a design note:**
The convergence model is architecturally more sophisticated than any competitor.
But presenting high Layer I concordance to users as though it represents empirically
calibrated probability — before Layer III exists — is the same epistemic error as
the competitors we are trying to distinguish from. The pre-decision oracle guardrail
(G18) covers the Brier score context for specific predictions. G25 covers the ongoing
framing of the entire system's confidence basis.

**Anti-pattern to prevent:**
> "Our multi-school convergence model gives this prediction 85% confidence."

This is misleading before Phase 6, because the "confidence" is entirely classical
(Layer I) and partially structural (Layer II), with no empirical calibration (Layer III).
The number 85% implies a validated probability that does not yet exist.

**Correct framing before Phase 6:**
> "Three independent classical frameworks agree on this outcome [with specifics].
> Classical agreement at this level is associated with strong predictive signal —
> we will be able to quantify exactly how strong once our empirical validation is complete."

**Status:** 🟠 Not yet implemented — required before any convergence score is user-facing.
**Fix by:** Before any convergence score is surfaced in the product (Phase 2 at earliest,
but the language must be designed before any score is shown).

