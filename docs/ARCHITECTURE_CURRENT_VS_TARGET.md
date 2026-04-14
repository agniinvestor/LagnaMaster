# LagnaMaster Architecture — Golden Source

> **This document is the single authoritative architecture reference.**
> Supersedes: v11 spec (absorbed), ARCHITECTURE.md (legacy), PREDICTION_PIPELINE.md (aspirational).
> Generated 2026-04-13. Based on 112-module audit, full data flow trace, and architectural review.
> Incorporates v11's 20 engineering quality criteria where they strengthen the design.

---

## PURPOSE

A pipeline that turns birth data into **verse-cited predictions** — not numbers, not scores — that a practitioner can read, verify against source texts, and trust. The system improves over time through empirical feedback from every chart analyzed.

**Phase C (now):** Encode classical texts as computable rules. Validate by reading predictions, not by checking rho.
**Phase A (S800+):** Practitioner query interface. 20Q verification. Life event capture.
**Phase B (S1400+):** Empirical calibration. Per-rule accuracy. Chart archetypes. Prediction language ML.

---

## CURRENT STATE

```
USER
  │
  │  "Give me a chart analysis"
  │
  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ INPUT                                                                   │
│   date, time, location                                                  │
│   No user identity. No session. No history.                             │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: ASTRONOMY                                                      │
│                                                                         │
│   ephemeris.py → BirthChart                                             │
│   Swiss Ephemeris (pyswisseph). Lahiri ayanamsha. JPL DE431.            │
│   This layer works correctly. No issues.                                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │  BirthChart passed raw to everything.
                                 │  No shared derived facts object.
                                 │
          ┌──────────────────────┼─────────────────────────┐
          │                      │                         │
          ▼                      ▼                         ▼
┌─────────────────┐   ┌──────────────────┐   ┌────────────────────────┐
│ SCORING ENGINE   │   │ CORPUS ENGINE    │   │ 50+ INDEPENDENT        │
│ (multi_axis_     │   │ (rule_firing +   │   │ MODULE CALLS           │
│  scoring.py)     │   │  inference.py)   │   │ (main.py dispatcher)   │
│                  │   │                  │   │                        │
│ 26 hardcoded     │   │ 654 V2 rules     │   │ yogas_extended         │
│ rules as PYTHON  │   │ from corpus      │   │ yogas_graha            │
│                  │   │                  │   │ nabhasa_yogas          │
│ Recomputes:      │   │ Recomputes:      │   │ vimshottari_dasa       │
│  dignity   ×5    │   │  dignity   ×3    │   │ gochara                │
│  house_map ×5    │   │  house_map ×2    │   │ shadbala               │
│  func_roles ×5   │   │  func_cls  ×1    │   │ ashtakavarga           │
│  ashtakav  ×5    │   │                  │   │ longevity              │
│                  │   │ Output:          │   │ graha_yuddha           │
│ Output:          │   │  FiredRule with  │   │ ... 40 more            │
│  {house: float}  │   │  verse citations │   │                        │
│  No predictions  │   │  predictions     │   │ Each recomputes its    │
│  No verses       │   │  BUT:            │   │ own dignity, house_map │
│  No traceability │   │                  │   │ etc. independently.    │
│                  │   │  ┌────────────┐  │   │                        │
│ Weights:         │   │  │ NEVER READ │  │   │ Output: various types  │
│  _WEIGHTS dict   │   │  │ by scoring │  │   │ dumped into results{}  │
│  hardcoded in    │   │  │ or API     │  │   │                        │
│  Python. Cannot  │   │  └────────────┘  │   │ No structure.          │
│  learn.          │   │                  │   │ No synthesis.          │
└────────┬─────────┘   └──────────────────┘   └───────────┬────────────┘
         │                                                │
         └────────────────────┬───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ OUTPUT                                                                  │
│                                                                         │
│   results = {                                                           │
│     "scoring": {H1: 2.3, H2: -0.5, H3: 1.1, ...},                    │
│     "nabhasa_yogas": [NabhasaYoga(...)],                               │
│     "longevity": 47.2,                                                  │
│     "graha_yuddha": [...],                                              │
│     ... 62 more keys                                                    │
│   }                                                                     │
│                                                                         │
│   Practitioner sees: "H10 = 3.2"                                       │
│                                                                         │
│   What does 3.2 mean?     No answer.                                    │
│   What will happen?       No answer.                                    │
│   When?                   No answer.                                    │
│   Says who?               No answer.                                    │
│   How confident?          No answer.                                    │
│   How does it compare     No answer.                                    │
│     to similar charts?                                                  │
│                                                                         │
│   No feedback mechanism. System produces identical output               │
│   today as it did 100 sessions ago regardless of data.                  │
└─────────────────────────────────────────────────────────────────────────┘


PROBLEMS SUMMARY:
  1. Two rule engines that don't talk           → conflicting answers
  2. 135+ redundant computations per chart      → waste, drift risk
  3. 26 rules hardcoded in Python               → can't learn, can't evolve
  4. Weights hardcoded in Python                → can't calibrate
  5. Output is numbers                          → not predictions
  6. No temporal projection                     → no timing
  7. No cross-signal synthesis                  → no convergence
  8. No narrative                               → no life story
  9. No feedback loop                           → no learning
  10. No user concept                           → no personalization
  11. No 20Q verification                       → can't validate chart
  12. 654 V2 rules fire but output discarded    → encoding is inert
```

---

## TARGET STATE

```
USER
  │
  │  "What about my career? I'm 35, in government, considering a change."
  │
  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ USER LAYER                                                              │
│                                                                         │
│   Authentication. Session. History.                                     │
│   User profile: past charts, 20Q answers, life events, feedback.        │
│   Role: practitioner / researcher / self-inquiry.                       │
│                                                                         │
│   Per-user: charts, feedback, life events.                              │
│   Shared: rules, weights, engine.                                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: ASTRONOMY                                                      │
│                                                                         │
│   ephemeris.py → BirthChart                                             │
│   (unchanged — this works)                                              │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: CHART CONTEXT (computed ONCE, shared by ALL downstream)        │
│                                                                         │
│   build_chart_context(chart) → ChartContext                             │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────┐        │
│   │  house_map         ← 1 call  (currently 70)               │        │
│   │  dignities         ← 1 call  (currently 39)               │        │
│   │  functional_roles  ← 1 call  (currently 8)                │        │
│   │  avasthas          ← 1 call  (currently 5)                │        │
│   │  ashtakavarga      ← 1 call  (currently 13)               │        │
│   │  vargas (D1-D60)   ← 1 call                               │        │
│   │  shadbala          ← 1 call                               │        │
│   │  dashas            ← 1 call                               │        │
│   │  transits (if date)← 1 call                               │        │
│   │  yogas             ← 1 call                               │        │
│   └────────────────────────────────────────────────────────────┘        │
│                                                                         │
│   Every derived fact computed once. Passed to all downstream.           │
│   Modules accept optional ctx= parameter: use if provided,             │
│   compute locally if not. Zero breaking changes.                        │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: UNIFIED RULE EVALUATION                                        │
│                                                                         │
│   ONE engine evaluates ALL rules from ONE corpus.                       │
│   (Former R01-R24 are now corpus rules like everything else.)           │
│                                                                         │
│   evaluate_all_rules(ctx, corpus, weights) → list[EvalResult]           │
│                                                                         │
│   EvalResult:                                                           │
│     rule_id:          "BPHS_CH25_V03"                                   │
│     house:            10                                                │
│     direction:        "favorable"                                       │
│     magnitude:        from weight_store (not hardcoded)                 │
│     verse:            "BPHS Ch.25 v.3"                                  │
│     predictions:      [{domain, text, entity, intensity}]               │
│     conditions_met:   [{primitive, args, result}]   ← traceability     │
│     confidence:       from weight_store + dignity + AV                  │
│                                                                         │
│   Weights read from versioned weight store (not Python dict).           │
│   Engine has no opinions. All intelligence in data.                     │
│   Rule conditions are DATA that can evolve, not code.                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: CONVERGENCE                                                    │
│                                                                         │
│   For each prediction candidate, count independent confirmations:       │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │                                                              │      │
│   │   NATAL PROMISE              ACTIVATION           STATUS    │      │
│   │   ─────────────              ──────────           ──────    │      │
│   │                                                              │      │
│   │   D1:  Jupiter H10L exalted  MD: Jupiter (active)  ✓        │      │
│   │   D9:  Jupiter own sign      AD: Venus (H10 co)   ✓        │      │
│   │   D10: Jupiter strong        Transit Jup: over H10 ✓        │      │
│   │   Yoga: Amala present        Double transit: Jup+Sat ✓      │      │
│   │   AV:  H10 sign 5 bindus     Varshaphala: H10 active ✓     │      │
│   │                                                              │      │
│   │   CONTRA-INDICATORS                                          │      │
│   │   Saturn aspects H10 → obstacle, not denial                  │      │
│   │   Mercury combust → communication challenges                 │      │
│   │                                                              │      │
│   │   CONVERGENCE: 5/5 natal + 5/5 temporal + 2 contrary        │      │
│   │   → PREDICTION STRENGTH: very high with obstacles            │      │
│   │                                                              │      │
│   └──────────────────────────────────────────────────────────────┘      │
│                                                                         │
│   This is NOT summing scores.                                           │
│   This is asking: "how many INDEPENDENT systems confirm this?"          │
│   5 weak signals summing to 3.0 ≠ 3 confirmed signals at 1.0.          │
│   Convergence across independent evidence is qualitatively different.   │
│                                                                         │
│   Output: list[ConvergedPrediction]                                     │
│     prediction, natal_confirmations, temporal_confirmations,            │
│     contra_indicators, convergence_score, peak_window                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 5: TEMPORAL PROBABILITY                                           │
│                                                                         │
│   For each converged prediction, overlay ALL timing systems:            │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │                                                              │      │
│   │   Vimshottari:  Jupiter MD 2028-2044 ████████████████████   │      │
│   │   Antardasha:   Venus AD 2031-2033         ████              │      │
│   │   Pratyantardasha: Mars PAD Q1 2032           █              │      │
│   │   Yogini:       converges 2031-2033        ████              │      │
│   │   Chara:        converges 2030-2034      ████████            │      │
│   │   Transit Jup:  H10 sign Aug 2031-Jul 2032  ████            │      │
│   │   Transit Sat:  aspects H10L 2031-2033     ████              │      │
│   │   Varshaphala:  2031 annual H10 active       ██              │      │
│   │                                                              │      │
│   │   COMBINED P(event|year):                                    │      │
│   │   2028: ░░  2029: ░░  2030: ▓▓  2031: ████  2032: ██████   │      │
│   │   2033: ████  2034: ▓▓  2035: ░░  2036: ░░                  │      │
│   │                                                              │      │
│   │   PEAK: Q1 2032  WINDOW: 2031-2033  CONFIDENCE: 5/7 systems │      │
│   │                                                              │      │
│   └──────────────────────────────────────────────────────────────┘      │
│                                                                         │
│   Each timing system is INDEPENDENT evidence.                           │
│   When 5 of 7 point to same 2-year window = high confidence.            │
│   When they scatter across 10 years = low confidence.                   │
│   System computes this explicitly, not as a vague "Jupiter period."     │
│                                                                         │
│   Output: list[TimedPrediction]                                         │
│     prediction, probability_curve{year: P}, peak_window,               │
│     timing_confidence, contributing_systems[]                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 6: NARRATIVE SYNTHESIS                                            │
│                                                                         │
│   Predictions are not bullet points. A life is a story.                 │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │                                                              │      │
│   │   LIFE PHASES (from dasha sequence + natal promises):        │      │
│   │                                                              │      │
│   │   Saturn MD (2008-2025): BUILDING                            │      │
│   │     Career: restructuring, institutional patience            │      │
│   │     Family: property through difficulty, marriage delayed    │      │
│   │     Health: steady, Saturn-related chronic minor issues      │      │
│   │                                                              │      │
│   │   Jupiter MD (2028-2044): HARVEST                            │      │
│   │     Career: prominence manifests (peak 2031-2033)            │      │
│   │     Family: marriage likely 2031-2033, children follow       │      │
│   │     Spiritual: deepening from mid-40s                        │      │
│   │     Health: generally strong, Jupiter protects                │      │
│   │                                                              │      │
│   │   INTERACTION EFFECTS:                                       │      │
│   │     H10 + H7 same dasha → spouse connected to career         │      │
│   │     H5 after H7 → children after marriage                    │      │
│   │     Saturn aspects throughout → success via institutions     │      │
│   │                                                              │      │
│   │   ABSENCE ANALYSIS:                                          │      │
│   │     H12 dormant throughout → no foreign settlement           │      │
│   │     H8 no activation → no major crisis periods               │      │
│   │     Rahu in H3 → unconventional communication style          │      │
│   │                                                              │      │
│   └──────────────────────────────────────────────────────────────┘      │
│                                                                         │
│   Sequences: what comes before what in the dasha progression            │
│   Interactions: how house promises affect each other                    │
│   Absences: dormant houses are predictions too ("no foreign travel")    │
│   Arcs: overall trajectory from building → harvest → wisdom             │
│                                                                         │
│   Output: NarrativeReport                                               │
│     life_phases[], interaction_effects[], absence_analysis[],           │
│     overall_arc, per_domain_narratives{}                                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 7: VERIFICATION + INTERACTION                                     │
│                                                                         │
│   Before predictions are finalized:                                     │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │ 20Q CHART VERIFICATION                                         │    │
│   │                                                                │    │
│   │ "Chart says eldest sibling. How many older siblings do you     │    │
│   │  have?"  → validates H3/H11 interpretation                    │    │
│   │ "Chart says government career. What sector are you in?"        │    │
│   │  → validates H10 interpretation                               │    │
│   │ "Chart says marriage around 28-30. When did you marry?"        │    │
│   │  → validates H7 timing                                        │    │
│   │                                                                │    │
│   │ If 15/20 answers match → chart-person fit HIGH                 │    │
│   │   → predictions presented with full confidence                 │    │
│   │ If 8/20 answers match → chart-person fit LOW                   │    │
│   │   → birth time may be off, predictions flagged as uncertain    │    │
│   │ If specific domains mismatch (career wrong, family right)      │    │
│   │   → those domain predictions downweighted                     │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│   After predictions are presented:                                      │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │ LIFE EVENT CAPTURE                                             │    │
│   │                                                                │    │
│   │ "Promoted to director in March 2031"                           │    │
│   │  → maps to career prediction + timing window                  │    │
│   │  → confirms BPHS_CH25_V03 + timing accuracy                  │    │
│   │                                                                │    │
│   │ "Divorced in 2029"                                             │    │
│   │  → contradicts H7 marriage prediction for that window         │    │
│   │  → flags BPHS_CH07_V12 for review                            │    │
│   │                                                                │    │
│   │ "This was partially accurate — right domain, wrong timing"     │    │
│   │  → partial confirmation: rule conditions right, timing off    │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│   All events stored with prediction_id + chart_id + timestamp.          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ ① events flow to calibration
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 8: CALIBRATION + LEARNING                                         │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ EVENT STORE (append-only, source of truth)                          │ │
│ │                                                                     │ │
│ │ prediction_outcomes: {prediction_id, chart_id, rule_ids[],          │ │
│ │   predicted_text, predicted_timing, actual_outcome, actual_timing,  │ │
│ │   accuracy, user_feedback, timestamp}                               │ │
│ │                                                                     │ │
│ │ chart_profiles: {chart_id, user_id, birth_data, 20Q_answers{},      │ │
│ │   life_events[], predictions_made[], cluster_id}                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ CALIBRATION ENGINE (batch — hourly/daily, not real-time)            │ │
│ │                                                                     │ │
│ │ 1. PER-RULE ACCURACY                                                │ │
│ │    BPHS_CH25_V03: fired 342×, confirmed 298×, accuracy 87%         │ │
│ │    SCORING_R02: fired 12000×, confirmed 7800×, accuracy 65%        │ │
│ │    → empirical_weight replaces base_weight                         │ │
│ │                                                                     │ │
│ │ 2. PER-CONTEXT ACCURACY                                             │ │
│ │    BPHS_CH25_V03 for night births: 92% (better)                    │ │
│ │    BPHS_CH25_V03 for day births: 78% (worse)                       │ │
│ │    → context_modifier discovered from data                         │ │
│ │                                                                     │ │
│ │ 3. PER-TEXT RELIABILITY                                              │ │
│ │    BPHS career rules: 78% overall                                   │ │
│ │    Saravali career rules: 65% overall                               │ │
│ │    → text_trust_factor per domain                                  │ │
│ │                                                                     │ │
│ │ 4. TIMING CALIBRATION                                                │ │
│ │    Predicted "during Jupiter MD" → happened 2yr after MD start     │ │
│ │    → timing_margin[dasha_level] adjusted                           │ │
│ │                                                                     │ │
│ │ 5. INTENSITY CALIBRATION                                             │ │
│ │    Rule says "strong career" → outcomes show "moderate career"      │ │
│ │    → magnitude_scale[rule_id] adjusted                             │ │
│ │                                                                     │ │
│ │ 6. RULE EVOLUTION                                                    │ │
│ │    BPHS_CH25_V03 v1: "Jupiter H10L exalted → career"              │ │
│ │    Data shows: works 92% WHEN Saturn not aspecting H10             │ │
│ │    BPHS_CH25_V03 v2: adds condition (flagged as empirical)         │ │
│ │    Original verse: PRESERVED. Addition: FLAGGED.                   │ │
│ │                                                                     │ │
│ │ 7. CHART ARCHETYPE DISCOVERY                                         │ │
│ │    Taurus lagna + Moon in Cancer + Jupiter exalted                  │ │
│ │    = recurring pattern → archetype "institutional builder"         │ │
│ │    → predictions for this archetype have known accuracy profile    │ │
│ │                                                                     │ │
│ │ 8. PREDICTION LANGUAGE SCORING                                       │ │
│ │    "government service" predicted → actual "public administration" │ │
│ │    → synonym mapping improves prediction text generation           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ WEIGHT STORE (versioned, shared by all users)                       │ │
│ │                                                                     │ │
│ │ weights_v47 = {                                                     │ │
│ │   "BPHS_CH25_V03": {                                                │ │
│ │      base: 1.0, empirical: 0.87, n: 342, ci: [0.81, 0.93],        │ │
│ │      contexts: {night_birth: 0.92, day_birth: 0.78},               │ │
│ │      timing_margin: +1.2yr                                         │ │
│ │   },                                                                │ │
│ │   "SCORING_R02": {                                                  │ │
│ │      base: 0.30, empirical: 0.22, n: 12000, ci: [0.20, 0.24],     │ │
│ │      contexts: {kendra_house: 0.31, dusthana_house: 0.12}          │ │
│ │   },                                                                │ │
│ │   ...                                                               │ │
│ │ }                                                                   │ │
│ │                                                                     │ │
│ │ Versioned: each calibration run → new version.                      │ │
│ │ Cached: hot path loads at startup, refreshes on new version.        │ │
│ │ Reproducible: any past prediction can be re-derived from            │ │
│ │   chart + weights_vN.                                               │ │
│ └──────────────────────────────────────────┬──────────────────────────┘ │
│                                            │                            │
└────────────────────────────────────────────┼────────────────────────────┘
                                             │
                              ② updated weights feed back
                                 to Layer 3 (rule evaluation)
                                             │
                                             ▼
                                 ┌───────────────────────┐
                                 │ Layer 3 reads updated  │
                                 │ weights on next chart  │
                                 │ computation. System    │
                                 │ improves with every    │
                                 │ feedback event.        │
                                 └───────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ FINAL OUTPUT (what the practitioner actually sees)                       │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │  CAREER (H10)                                           confidence │ │
│ │  ═══════════                                                       │ │
│ │                                                                     │ │
│ │  "Career prominence through government/institutional service.       │ │
│ │   Jupiter as H10 lord is exalted in D1, confirmed in D9 and D10.  │ │
│ │   Amala Yoga supports spotless professional reputation.            │ │
│ │                                                                     │ │
│ │   TIMING: Peak window 2031-2033.                                   │ │
│ │   5 of 7 timing systems converge on this window.                   │ │
│ │   Venus antardasha within Jupiter mahadasha activates H10.         │ │
│ │   Transit Jupiter over natal H10 sign Aug 2031 - Jul 2032.        │ │
│ │                                                                     │ │
│ │   OBSTACLE: Saturn aspects H10 throughout — success comes          │ │
│ │   through patience with institutional resistance, not quick wins.  │ │
│ │                                                                     │ │
│ │   SOURCES: BPHS Ch.25 v.3, Saravali Ch.21 v.8 (both agree).      │ │
│ │   This prediction confirmed in 87% of similar charts (n=342).     │ │
│ │                                                                     │ │
│ │   CONFIDENCE: 82%                                            ████░ │ │
│ │   Chart-person fit: 17/20 questions matched.                       │ │
│ │   Birth time sensitivity: low (prediction stable ±15 min).        │ │
│ │                                                                     │ │
│ │  ──────────────────────────────────────────────────────────────     │ │
│ │  VERIFY: Open BPHS Ch.25 v.3 (p.212 Santhanam Vol 1).             │ │
│ │  "If Jupiter is the lord of the 10th and is exalted..."           │ │
│ │  You can check every claim above against the source text.          │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  This is what "prediction quality" means.                               │
│  Not H10 = 3.2.                                                        │
│  Not rho = 0.45.                                                        │
│  A practitioner can read this, verify it, and trust it.                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ENGINEERING QUALITY CRITERIA (absorbed from v11)

These cross-cutting concerns apply to ALL layers. They are not features — they are properties the system must maintain as it grows. Each has an exit criterion and enforcement mechanism.

### Q1. Derived Facts Tier Ordering (v11 §4)

ChartContext (Layer 2) computes derived facts in a strict dependency order:

```
Tier 1: Positions + Conventions (from Layer 1)
Tier 2: Lordships, House classification (from Tier 1)
Tier 3: Aspects, Conjunction, Combustion, Friendship (from Tiers 1-2)
Tier 4: Dignity, Avasthas (from Tiers 1-3)
Tier 5: Shadbala, Functional roles, Bhava Bala (from Tiers 1-4)
```

**Enforcement:** Within `build_chart_context()`, computation follows this order. No Tier N result may depend on a Tier N+1 result. Module registry maps each module to its tier.

**Exit criterion:** `build_chart_context()` computes in tier order. No circular dependencies.

### Q2. Robustness — Zero Silent Handlers (v11 §2)

Every `except` block either logs with context and re-raises, or handles with a documented sentinel (e.g., `None`, never a plausible default like 66.0 years or 1.0).

**Current:** 8 silent handlers remain (down from 143 in S318).
**Exit criterion:** Zero silent exception handlers in `src/`. Ruff BLE001 clean.

### Q3. Verification Tags (v11 §7)

Every canonical primitive module has `_VERIFICATION = {"level": "bphs_pdf" | "formula_compared" | "unverified", "reference": "BPHS Ch.X v.Y", "session": "SNNN"}`.

**Current:** 9 modules tagged, 104 untagged.
**Enforcement:** A module tagged `unverified` cannot be the canonical source for any concept. The Canonical Source Map (CLAUDE.md) lists only verified sources.
**Exit criterion:** 100% of canonical sources tagged. Zero `unverified` canonical sources.

### Q4. Traceability with Configurable Depth (v11 §9)

Every prediction traces from output to verse citation. Trace depth is configurable:
- **Minimal:** rule_id + verse + direction
- **Standard:** + condition values (planet positions, dignity levels, house placements)
- **Full:** + every intermediate computation (aspect strengths, shadbala components)

**Enforcement:** Every EvalResult includes `conditions_met[]`. Aggregation (Layer 5a) preserves individual results — never discards. Output includes both aggregate and contributing rules.
**Exit criterion:** Any prediction decomposes to individual rule firings in one function call. India 1947 fixture: every prediction traceable to verse.

### Q5. Module Registry (v11 §6, §10)

Every module in `src/calculations/` registered in `src/MODULE_REGISTRY.py` with:
- Layer and tier assignment
- One-sentence purpose
- Canonical source for which concept(s)
- 500-line trigger for review (not a hard limit)

**Enforcement:** CI validates import directions against registry. New modules must be registered before merge.
**Exit criterion:** 100% of `src/calculations/` registered. Zero cross-layer upward imports.

### Q6. Three Version Axes (v11 §19)

Every output includes:
1. **Corpus version** — which rules were used (git commit hash of corpus files)
2. **Schema version** — output format version (bumped on breaking changes)
3. **Weight version** — which calibration weights were applied

**Enforcement:** `ChartScoresV3` (and its successor) includes all three versions. Any past prediction reproducible by specifying versions.
**Exit criterion:** All three version axes tracked in output. Reproduction test: same chart + same versions = identical output.

### Q7. Runtime Invariant Checking (v11 §20)

Lightweight invariant checks run after Layer 2 (ChartContext), before Layer 3 (rule evaluation):
- Every planet in exactly one sign and one house
- Every house has exactly one lord
- Aspect strength non-negative
- Dignity level is a valid enum value
- No contradictory rule conditions

**Current:** `src/invariants.py` exists, called from `ephemeris.py`.
**Enforcement:** Invariant checker runs on every chart. Development: raises. Production: logs and continues.
**Exit criterion:** Zero violations on India 1947 fixture. Checker catches wrong planet count, duplicate lordships, negative aspects.

### Q8. Data Sensitivity (v11 §13)

Birth data (date, time, location) is personally identifiable.
- Stored separately from computed results
- Retention policy functional (not broken like the current `last_accessed` bug)
- No birth data in log output
- CORS restricted, JWT from environment variable

**Exit criterion:** Retention policy works (test-verified). No PII in logs. Auth tokens not hardcoded.

### Q9. Performance (v11 §16)

Single chart computation < 200ms end-to-end (all rules, all layers).
ChartContext eliminates 135+ redundant computations — expected to significantly improve current latency.

**Enforcement:** `tools/benchmark_chart.py` measures per-layer timing. Any layer >50ms triggers investigation.
**Exit criterion:** Benchmark < 200ms. Benchmark runs in CI.

### Q10. Reproducibility (v11 §11)

Same birth data + same config + same corpus version + same weight version = identical output. No randomness. No ambient state.

**Enforcement:** All computation is pure functions. Three version axes (Q6) enable exact reproduction. Snapshot test: India 1947 produces deterministic JSON, tested in CI.
**Exit criterion:** Two runs of same chart produce byte-identical JSON.

### Q11. Observability (v11 §12)

Every canonical primitive logs at DEBUG level: what it computed, from what inputs. Always available — not added during debugging.

**Enforcement:** RuleResult trace (Q4) provides rule-level observability. No silent exceptions (Q2).
**Exit criterion:** Any incorrect output diagnosable from existing logs + rule trace without code changes.

### Q12. Evolvability (v11 §8)

Adding a new text = add rules that import existing primitives. No new computation modules.
Adding a new school = add school-specific modules where that school differs from Parashari.

**Enforcement:** New text checklist: verse audit → encode with existing primitives → tag with source.
New school checklist: identify differing concepts → school-specific modules → register.
**Exit criterion:** New text requires zero computation layer changes. Tested by ≥1 non-BPHS text.

### Q13. Knowledge Preservation (v11 §15)

The corpus is the product. Every rule preserves: source text, chapter, verse, original claim (verse audit), structured conditions, prediction. Losing any makes the rule less valuable.

**Enforcement:** Verse audit files required before encoding (CLAUDE.md Gate 1-2). Builder validates provenance fields (T1-1 through T1-5). Verse audit version-controlled alongside rules.
**Exit criterion:** 100% of rules have complete provenance. Verse audits exist for all encoded chapters.

### Q14. Developer Experience (v11 §10)

Three workflows, each with clear entry/exit:
- **Encoding:** Read CLAUDE.md → 5 gates → ship
- **Bug fixing:** Find canonical source → fix there → tests pass → all consumers fixed
- **Adding a text:** Follow checklist → import existing primitives → encode rules

**Enforcement:** CLAUDE.md protocol, Canonical Source Map, v2_scorecard.py, ruff + pytest hooks.
**Exit criterion:** New session productive within 15 minutes of reading CLAUDE.md. No tribal knowledge required.

---

## GAP ANALYSIS: CURRENT → TARGET

### Structural Gaps

| #  | Layer | Current | Target | Phase |
|----|-------|---------|--------|-------|
| G1 | 2 | 135+ redundant computations | ChartContext with tier ordering (Q1) | C |
| G2 | 3 | 26 rules hardcoded in Python | All rules in corpus as data | C |
| G3 | 3 | 2 engines, 2 output types | 1 engine, 1 EvalResult type with traceability (Q4) | C |
| G4 | 3 | Weights hardcoded in _WEIGHTS | Weight store (versioned data, version axis Q6) | C |
| G5 | 4 | Rules fire independently | Convergence across D1/D9/D10/dasha/transit | C |
| G6 | 5 | No timing beyond "dasha period" | Temporal probability P(event\|year) | C/A |
| G7 | 6 | Output = bag of numbers | Narrative life-phase synthesis | A |
| G8 | 7 | No 20Q | Chart-person verification | A |
| G9 | 7 | No life event capture | Outcome anchoring | A |
| G10 | 8 | No feedback loop | Event store + calibration engine | A/B |
| G11 | 8 | No rule evolution | Versioned rules with empirical additions | B |
| G12 | 8 | No chart archetypes | Cluster discovery from outcomes | B |
| G13 | - | No user/auth | Multi-user with shared engine (Q8 data sensitivity) | A |

### Engineering Quality Gaps (from v11 criteria)

| #  | Criterion | Current | Target | Phase |
|----|-----------|---------|--------|-------|
| Q1 | Tier ordering | No computation order | 5-tier DAG in ChartContext | C (with G1) |
| Q2 | Robustness | 8 silent handlers remain | Zero silent handlers | C |
| Q3 | Verification tags | 9/112 modules tagged | 100% canonical sources tagged | C |
| Q4 | Traceability | No trace from output to verse | Configurable depth (min/std/full) | C (with G3) |
| Q5 | Module registry | Canonical Source Map in CLAUDE.md | MODULE_REGISTRY.py with CI enforcement | C |
| Q6 | Three version axes | No versioning | corpus_version + schema_version + weight_version | C (with G4) |
| Q7 | Runtime invariants | invariants.py exists | Runs on every chart, before rule eval | C |
| Q8 | Data sensitivity | allow_origins=["*"], broken retention | CORS restricted, PII separated, retention works | A (with G13) |
| Q9 | Performance | Unknown (no benchmark) | <200ms per chart, benchmark in CI | C |
| Q10 | Reproducibility | Not tested | Same inputs = byte-identical output, snapshot test | C |
| Q11 | Observability | Ad-hoc logging | DEBUG logging in all canonical primitives | C |
| Q12 | Evolvability | No checklists | New text/school checklists, tested by ≥1 non-BPHS | C |
| Q13 | Knowledge preservation | Verse audits exist for 20 chapters | 100% of encoded chapters have verse audits | Ongoing |
| Q14 | Developer experience | CLAUDE.md protocol exists | 15-minute productive start, no tribal knowledge | C |

---

## BUILD ORDER + DEPENDENCY MAP

Sequenced by dependency, not by effort. Each block must be correct before the next starts.
Items on the same row can be worked in parallel. Arrows (→) mean "blocks".

```
DEPENDENCY GANTT
════════════════

                          PHASE C                           │  PHASE A            │ PHASE B
                          (Foundation)                      │  (Practitioner)     │ (Research)
                                                            │                     │
CRITICAL PATH (serial — each blocks the next):              │                     │
──────────────────────────────────────────────              │                     │
                                                            │                     │
W0 ✅ ─→ G1 ✅ ──→ G2 ✅ ──→ G3 ✅ ──→ G4 ✅ ──→ G5 ✅ ──→ G6 ✅ ┼→ G7 ──→ G10 ───────┼→ G11 ──→ G12
Done     ChartCtx  Rules    Unified   Weight    Convrgn Temp  │  Narrative Feedback │  Rule     Archetypes
         tier ord  to data  engine    store     layer   prob  │  synthesis loop     │  evolution
         D0–D0c resolved: pipeline wired into production.       │                     │
         Entry point: src/pipeline.py:run_pipeline()           │                     │
                                                            │                     │
PARALLEL TRACKS (can proceed alongside critical path):      │                     │
──────────────────────────────────────────────              │                     │
                                                            │                     │
After W0:  Q2 ────────── (fix 8 silent handlers)            │                     │
           Q3 ────────── (verification tags)                │                     │
           Q5 ────────── (MODULE_REGISTRY.py)               │                     │
           Q7 ────────── (runtime invariants)               │                     │
           Q11 ─────────  (DEBUG logging)                   │                     │
           Q12 ─────────  (evolvability checklists)         │                     │
                                                            │                     │
After G1:  Q9 ────────── (benchmark <200ms)                 │                     │
           Q10 ─────────  (reproducibility snapshot)        │                     │
                                                            │                     │
After G4:  Event store SCHEMA ──────────────────────────────┼→ G9 (life events)   │
                                                            │                     │
After G6:  Resume BPHS encoding (Ch.26+) ──────────────────→│                     │
           (encoding produces full predictions: convergence │                     │
            + timing + traceability — verifiable e2e)       │                     │
                                                            │                     │
                                                     G13+Q8 ┼── (user/auth/GDPR) │
                                                         G8 ┼── (20Q)            │
                                                            │                     │


DETAILED VIEW — WHAT EACH ITEM PRODUCES:
════════════════════════════════════════

CRITICAL PATH:

  G1+Q1: ChartContext with 5-tier ordering
  ├─ Produces: build_chart_context() → ChartContext dataclass
  ├─ Contains: house_map, dignities, func_roles, avasthas, ashtakavarga, vargas, shadbala
  ├─ Tier order enforced: positions → lordships → aspects → dignity → shadbala
  ├─ Exit: 135 redundant calls → 1 call. All downstream accepts ctx= parameter.
  └─ Blocks: G2 (rules need ChartContext to evaluate against)

  G2: Migrate R01-R24 to corpus
  ├─ Produces: 26 new V2 rule records in src/corpus/
  ├─ Each with: structured conditions, verse citation, predictions[], weight_key
  ├─ multi_axis_scoring.py evaluate_house_detailed() deleted or becomes thin wrapper
  ├─ Exit: zero hardcoded rules in Python. All rules are data.
  └─ Blocks: G3 (unified engine needs all rules in one format)

  G3+Q4: Unified evaluation engine
  ├─ Produces: evaluate_all_rules(ctx, corpus, weights) → list[EvalResult]
  ├─ EvalResult: rule_id, house, direction, magnitude, verse, predictions[],
  │              conditions_met[] (Q4 traceability), confidence
  ├─ One engine evaluates ALL rules. No parallel paths.
  ├─ Exit: scoring.py, multi_axis_scoring.py, rule_firing.py, inference.py
  │        → single evaluate_all_rules() function
  └─ Blocks: G4 (engine needs weights store to read from)

  G4+Q6: Weight store
  ├─ Produces: weight_store.py with versioned weight table
  ├─ Format: {rule_id: {base_weight, empirical_weight, n, ci, contexts{}}}
  ├─ Three version axes in output: corpus_version, schema_version, weight_version
  ├─ Initial weights: base_weight from encoding, empirical_weight = base (no data yet)
  ├─ Exit: _WEIGHTS dict deleted. Engine reads from store.
  └─ Blocks: G5 (convergence needs weighted rule results)

  G5: Convergence layer
  ├─ Produces: converge(eval_results, ctx) → list[ConvergedPrediction]
  ├─ For each prediction: count independent confirmations across:
  │    natal (D1/D9/D10/D12), temporal (MD/AD/PAD), transit (gochara/double),
  │    yoga (specific combinations)
  ├─ Contra-indicators counted separately (not netted against)
  ├─ Exit: predictions carry convergence_score + confirmation_sources[]
  └─ Blocks: G6 (temporal layer operates on converged predictions)

  G6: Temporal probability
  ├─ Produces: time_project(converged, ctx) → list[TimedPrediction]
  ├─ Overlays: Vimshottari, Chara, Yogini dashas + transits + varshaphala
  ├─ Output: P(event|year) distribution per prediction, peak_window, timing_confidence
  ├─ Exit: predictions have timing, not just "during Jupiter dasha"
  ├─ Blocks: G7 (narrative needs timed predictions to sequence into life phases)
  └─ UNBLOCKS: BPHS encoding resumes here — e2e pipeline produces verifiable
     predictions with convergence + timing + verse traceability

  G7: Narrative synthesis (Phase A)
  ├─ Produces: narrate(timed_predictions) → NarrativeReport
  ├─ Life phases from dasha sequence, interaction effects across houses,
  │  absence analysis (dormant houses), overall arc
  └─ Blocks: G10 (feedback needs predictions to collect feedback against)

  G10: Feedback loop (Phase A/B)
  ├─ Produces: event store + basic calibration engine
  ├─ Warm path: append feedback events. Cold path: batch weight recalculation.
  └─ Blocks: G11, G12 (rule evolution and archetypes need outcome data)

  G11: Rule evolution (Phase B)
  ├─ Produces: versioned rules with empirical condition additions
  └─ Blocks: G12 (archetypes use refined rules)

  G12: Chart archetypes (Phase B)
  └─ Produces: cluster analysis, per-archetype accuracy profiles


PARALLEL TRACKS (independent of critical path):

  Q2:  Fix 8 silent handlers → zero. Independent.
  Q3:  Tag canonical modules with _VERIFICATION. Independent.
  Q5:  MODULE_REGISTRY.py. Independent (strengthens G1-G3 but doesn't block them).
  Q7:  Runtime invariants before rule eval. Depends on G1 (needs ChartContext).
  Q9:  Benchmark. Depends on G1 (measures ChartContext improvement).
  Q10: Reproducibility snapshot. Depends on G3 (needs unified output format).
  Q11: DEBUG logging. Independent.
  Q12: Evolvability checklists. Independent.
  Q13+Q8: User/auth. Independent of core pipeline. Required before G8, G9.
  G8:  20Q. Depends on G13 (needs user sessions).
  G9:  Life events. Depends on G13 + event store schema (from G4).
```

```
PHASE C FOUNDATION:

  Block 1 — Core Pipeline (G1-G4, Q1, Q4, Q6):
    G1+Q1: ChartContext with 5-tier ordering
     → G2: Migrate R01-R24 to corpus as V2 records
     → G3+Q4: Unified evaluation engine with EvalResult traceability
     → G4+Q6: Weight store schema with three version axes
     → Event store SCHEMA (tables only, no engine yet)

  Block 2 — Prediction Quality (G5, G6):
    G5: Convergence layer (multi-signal confirmation across D1/D9/D10/dasha/transit)
    G6: Temporal probability (overlay 7 timing systems → P(event|year))

  Block 3 — Engineering Quality (Q2, Q3, Q5, Q7, Q9, Q10, Q11, Q12):
    Q2: Fix remaining 8 silent handlers
    Q3: Tag all canonical source modules with _VERIFICATION
    Q5: Build MODULE_REGISTRY.py with CI enforcement
    Q7: Wire runtime invariant checker before rule evaluation
    Q9: Create benchmark_chart.py, establish <200ms baseline
    Q10: Snapshot test for India 1947 (deterministic JSON)
    Q11: Add DEBUG logging to all canonical primitives
    Q12: Write new text / new school checklists

PHASE C.5 — PRACTITIONER DEPTH (G8):
  G8: Deepen analysis to practitioner quality (see G8 spec below)
       G8a: Proper varga chart evaluation
       G8b: Domain-specific divisional analysis
       G8c: AD-level narrative depth
       G8d: Current period transit analysis
       G8e: Vimshopak strength integration
       G8f: Claims enrichment

PHASE A PRACTITIONER TOOL:
  G13+Q8: User/auth/session + data sensitivity
   → G8_20Q: 20Q chart-person verification (formerly G8)
   → G9: Life event capture + outcome anchoring
   → G10: Feedback loop (event store → basic calibration)

PHASE B RESEARCH PLATFORM:
  G10: Full calibration engine (Bayesian weight updates)
   → G11: Rule evolution (empirical condition discovery)
   → G12: Chart archetype clustering
   → Prediction language ML
```

---

## UPDATED BUILD ORDER (post G1-G7)

```
PHASE C.5 — Practitioner Depth + Safety:

  G8 (wire 28 unused modules) → G14 (birth time sensitivity) → G15 (safety filter)
  → G13 (user/auth) → Phase A

  G8a: Fix varga evaluation (actual D9/D10 planet positions)    ← BUG FIX
  G8b: Wire yoga modules (yogas_extended, yogas_graha,          ← WIRING
       yogas_pvrnr, nabhasa_yogas) into convergence
  G8c: Wire strength modules (bhava_bala, ishta_kashta,         ← WIRING
       vimshopak, shadbala_patches) into convergence weighting
  G8d: Wire transit modules (gochara, double_transit,           ← WIRING
       av_transit, bhava_and_transit) into temporal projection
  G8e: Wire Jaimini modules (chara_karak, jaimini_full,         ← WIRING
       karakamsha_analysis) as alternative framework channel
  G8f: AD-level narrative depth                                 ← WIRING
  G8g: Domain-specific divisional analysis (D9→marriage, etc.)  ← WIRING
  G8h: Claims enrichment (encoding sessions)                    ← ENCODING

  G14: Wire confidence_model.py into pipeline                   ← WIRING
       Birth time sensitivity warnings in NarrativeReport
       Lagna boundary, nakshatra cusp, dasha uncertainty flags

  G15: Safety filtering in narrative                            ← WIRING
       Suppress/flag health_sensitive claims (129 rules)
       Enforce guardrails G01 (no "prediction"), G02 (no death timing),
       G05 (no "certificate")
```

### Pipeline coverage problem

The pipeline currently uses **12 of 40** computation modules (30%).
28 modules compute useful astrological data that the pipeline ignores:

| Category | Unused modules | Value |
|----------|---------------|-------|
| Yoga detection | yogas_extended, yogas_graha, yogas_pvrnr, nabhasa_yogas, yoga_strength | HIGH — 140+ yoga types, independent confirmation |
| Strength | bhava_bala, dig_bala, ishta_kashta, shadbala_patches, divisional_charts, sapta_varga | HIGH — planet/house viability scores |
| Transit | gochara, double_transit, av_transit, bhava_and_transit, transit_quality_advanced | HIGH — current period analysis |
| Jaimini | chara_karak, jaimini_full, karakamsha_analysis | HIGH — alternative framework |
| Dasha | dasha_activation, ashtottari_dasha | MEDIUM — dasha selection + alternative |
| Special | graha_yuddha, sudarshana, muhurtha_complete, special_lagnas | MEDIUM — edge cases |
| Safety | confidence_model | CRITICAL — birth time sensitivity |
| Multi-lagna | multi_lagna (partially used) | MEDIUM — secondary frames |

All of these EXIST and have tests. But **NONE have been verified against
source texts.** Tests prove the code runs without errors — they do not
prove the code implements what BPHS/Saravali/Jataka Parijata actually say.

### Verification status of the 28 modules

**BPHS-verified (verse audit completed, safe to wire):** 0 of 28.

Only 8 modules in the entire codebase carry `_VERIFICATION = "bphs_pdf"`:
house_lord, dignity, shadbala, ashtakavarga, sputa_drishti, divisional_charts,
varga, argala. These are already in the pipeline via ChartContext.

**The 28 modules proposed for G8 have ZERO verse verification.** The yoga
formulas, Jaimini rules, transit logic, strength calculations — all were
written from secondary references or translator summaries, never compared
line-by-line against the source slokas.

### G8 MANDATORY GATE: Verify before wiring

```
For each module group (G8a through G8e):
  1. READ the relevant BPHS/source chapter verses
  2. COMPARE each function against the verse claims
  3. TAG the module with _VERIFICATION = {"level": "bphs_pdf", ...}
  4. FIX any discrepancies found
  5. ONLY THEN wire into the pipeline

This is the same Gate 1-2 process used for corpus encoding,
applied to computation modules.
```

**Verification order (by risk × impact):**

| Priority | Modules | Source chapters | Why first |
|----------|---------|-----------------|-----------|
| 1 | yogas_extended, yogas_graha | BPHS Ch.35-36, Saravali Ch.15-20 | Yogas are the highest-value convergence signal |
| 2 | nabhasa_yogas | BPHS Ch.35 | 32 specific yogas with precise conditions |
| 3 | bhava_bala, ishta_kashta | BPHS Ch.27-28 | House/planet strength weights everything |
| 4 | gochara, double_transit | BPHS Ch.64-65, transit theory | Transit analysis must be correct for current-period |
| 5 | jaimini_full, chara_karak | Jaimini Sutras | Entirely different framework — high error risk |
| 6 | confidence_model | Not text-based — verify against statistical theory | Birth time sensitivity is mathematical, not textual |
| 7 | Remaining modules | Various | Lower impact on core predictions |

**Estimated effort:** Each module group requires 1 verification session
(read source, compare, tag, fix). Total: ~7 sessions before G8 wiring
is complete.

**What this means for the roadmap:** G8 is NOT "just wiring." It is:
verify → fix → wire → test. The verification step is the bottleneck,
not the wiring.

---

## G8: PRACTITIONER DEPTH — Detailed Specification

> The exam question: "How do you enhance depth of analysis to make the
> model ready for Phase A?  What needs to be done to Phase C to align
> with practitioner approach?"
>
> G1-G7 built the pipeline skeleton.  G8 fills it with practitioner-level
> depth.  Without G8, the system produces structurally correct but
> analytically shallow output that no practitioner would trust.

### The problem

A practitioner reading our current output would immediately flag:

1. **"You only looked at the rashi chart."** — We run D1 scoring rules
   with D9/D10 lagna sign, but planets stay in their D1 signs.  In reality,
   a planet in Aries in D1 might be in Sagittarius in D9.  Lordships change
   completely.  Our "D9 channel" is fake — it's D1 with a different starting
   point, not an actual navamsha analysis.

2. **"Where is the navamsha confirmation?"** — The practitioner's core
   method is: D1 shows the promise, D9 confirms it.  If Jupiter lords H10
   in D1 but is debilitated in D9, the career promise is weakened.  We don't
   check this.

3. **"You give me a 16-year window."** — MD-level timing is useless for
   practical guidance.  A client wants to know "when in the next 2-3 years"
   not "sometime during your Jupiter period."

4. **"What about right now?"** — Every consultation starts with the current
   period.  We have no transit-against-natal analysis for a specific date.

5. **"You have the verses but your predictions are generic."** — Only 46 of
   231 fired corpus rules carry claim text.  The narrative templates are
   blank for 80% of rules.

### G8a: Proper Varga Chart Evaluation

**Current state:** `_evaluate_scoring_rules()` runs D1 scoring rules with
`frame_lagna_si=d9.varga_lagna_sign_index`.  This swaps the ascendant but
planets remain in D1 signs.  It's structurally wrong.

**What exists in codebase:** `ctx.vargas.tables['D9'].planets[name].varga_sign_index`
gives the ACTUAL D9 sign for each planet.  `compute_vimshopaka()` gives 16-varga
dignity.  `compute_vimshopak()` gives 7-varga dignity with per-division breakdown.

**What to build:**
- `build_varga_context(ctx, division='D9') → VargaContext` — builds a lightweight
  context with house_map, lordships, and dignities computed from the ACTUAL varga
  planet positions (not D1 positions with swapped lagna)
- For each house prediction, check: does the house lord's dignity in the relevant
  varga CONFIRM or WEAKEN the D1 promise?
- Vargottama detection: planet in same sign in D1 and D9 = strong confirmation
- Replace the current fake D9/D10 scoring with real varga evaluation

**Exit:** Convergence channel "d9_natal" means actual D9 dignity check, not
D1 rules with D9 lagna.

### G8b: Domain-Specific Divisional Analysis

**Practitioner method:** Each life domain has a specific varga chart:

| Domain | Varga | What to check |
|--------|-------|---------------|
| Marriage/dharma | D9 (Navamsha) | H7 lord dignity, Venus condition, upapada |
| Career | D10 (Dashamsha) | H10 lord dignity, karaka placement, yogas |
| Children | D7 (Saptamsha) | H5 lord dignity, Jupiter condition |
| Property/vehicles | D4 (Chaturthamsha) | H4 lord dignity, Mars/Venus condition |
| Wealth | D2 (Hora) | H2 lord dignity, Jupiter/Venus in hora |
| Siblings | D3 (Drekkana) | H3 lord dignity, Mars condition |
| Parents | D12 (Dwadashamsha) | H9/H4 lords, Sun/Moon dignity |

**What to build:**
- Map each outcome_domain from the corpus to its relevant divisional chart
- For each ConvergedPrediction, check the relevant varga as independent evidence
- Add per-varga confirmation to the convergence layer as named channels
  (e.g., "d9_marriage", "d10_career" instead of generic "d9_natal")

**Exit:** Each domain narrative says "confirmed in D9" or "weakened in D10"
with specific planet-in-sign evidence.

### G8c: AD-Level Narrative Depth

**Current state:** Narrative shows 9 life phases (one per Mahadasha, 6-19 years).
Timing uses year-level peak windows.

**What to build:**
- Within each LifePhase, break into AD sub-periods (9 per MD, each 1-3 years)
- AD lord activates the houses it LORDS — this is the specific timing mechanism
- For each AD, list which houses activate and what claims apply
- `AdSubPeriod` dataclass: lord, start, end, activated_houses, domain_summaries, text
- LifePhase.sub_periods: list[AdSubPeriod]

**Practitioner method:** "During Jupiter MD / Venus AD (2031-2033), Venus activates
H1 and H6 (as their lord), while Jupiter's H8 and H11 lordship sets the backdrop.
Marriage likely in this window because Venus lords the 7th from Moon in D9."

**Exit:** Narrative includes AD-level predictions with 1-3 year precision.

### G8d: Current Period Transit Analysis

**Current state:** Gochara windows in temporal projection use orbital period
approximation.  No analysis of current transits against the natal chart.

**What exists:** `compute_gochara(natal_chart, transit_date) → GocharaReport`
gives exact transit positions with natal house mapping.  `detect_double_transit_yoga()`
checks Jupiter+Saturn aspects for specific domains.

**What to build:**
- `analyze_current_period(ctx, query_date) → CurrentPeriodReport`
- Identifies: current MD, current AD, current PAD
- Computes: Jupiter transit house, Saturn transit house, Rahu transit house
- Checks: double transit activating specific houses
- Detects: Sade Sati (Saturn ±1 sign from natal Moon)
- Maps: which natal promises are CURRENTLY being activated by transit

**Exit:** Pipeline can answer "what is happening right now for this chart?"

### G8e: Vimshopak Strength Integration

**Current state:** Convergence counts channels but doesn't weight by planet
strength.  A planet with Vimshopak score 15/20 is treated the same as one
with 5/20.

**What exists:** `compute_vimshopaka()` (16-varga, scores 0-20) and
`compute_vimshopak()` (7-varga, with per-division dignity breakdown).

**What to build:**
- For each house prediction, multiply convergence by the house lord's
  Vimshopak strength (normalized 0-1)
- A house lorded by a planet with Vimshopak 15/20 gets 0.75× weight
  multiplier on its convergence score
- This differentiates between "5 weak channels confirm" and "3 strong
  channels confirm" — the latter is more reliable

**Exit:** ConvergedPrediction carries a strength-weighted convergence
score alongside the raw channel count.

### G8f: Claims Enrichment

**Current state:** Only 46 of 231 fired corpus rules have populated
`predictions[]`.  The remaining 185 rules fire (conditions met, direction
known) but contribute no claim text to the narrative.

**This is NOT an architecture task — it's an encoding task.** But it's the
single biggest bottleneck for narrative quality.  The NL templates can only
be as rich as the claims data.

**What to do:**
- Run the pipeline on 50 golden charts
- For each rule that fires but has empty predictions[], identify the source
  chapter and verse
- In the next encoding session, populate predictions[] for these rules
- Priority: rules that fire most frequently across the 50 charts

**Exit:** >80% of fired corpus rules have populated predictions[].

### G8 Build Order

```
G8a (fix varga evaluation) → G8b (domain-specific vargas) → G8e (vimshopak)
                                                          ↘
G8c (AD-level depth) ─────────────────────────────────────→ G8d (current transits)
                                                          ↗
G8f (claims enrichment) — parallel, encoding sessions
```

G8a must come first (the current D9/D10 evaluation is structurally wrong).

### Key insight: VERIFY → FIX → WIRE → TEST

Every G8 sub-item follows the same 4-step process:

1. **VERIFY** — read the source text chapters, compare against module logic
2. **FIX** — correct any discrepancies found
3. **WIRE** — connect verified module into pipeline convergence/temporal/narrative
4. **TEST** — run against golden_50 diverse charts, verify no regressions

**Do NOT skip step 1.** Wiring unverified modules into production is building
on assumptions. The 28 modules have tests but zero verse verification.

| Item | Module(s) that already exist | What "wiring" means |
|------|------------------------------|---------------------|
| G8a | `sapta_varga.compute_vimshopak()`, `varga.py` | Fix: use actual varga planet positions instead of D1 with swapped lagna |
| G8b | `yogas_extended`, `yogas_graha`, `yogas_pvrnr`, `nabhasa_yogas` | Add yoga detection results as convergence channel |
| G8c | `bhava_bala`, `ishta_kashta`, `compute_vimshopaka()`, `compute_vimshopak()` | Multiply convergence by planet/house strength scores |
| G8d | `gochara`, `double_transit`, `av_transit`, `bhava_and_transit` | Feed transit analysis into temporal projection for current period |
| G8e | `chara_karak`, `jaimini_full`, `karakamsha_analysis` | Add Jaimini framework as independent convergence channel |
| G8f | `vimshottari_dasa` (AD data exists with dates) | Generate per-AD narrative within each MD life phase |
| G8g | `ctx.vargas` (D2/D3/D4/D7/D9/D10/D12 all computed) | Map domain→varga, check house lord dignity in relevant varga |
| G8h | Corpus `predictions[]` field (schema exists) | Encoding sessions to populate empty claim fields |

---

## G14: BIRTH TIME SENSITIVITY GATE

> `src/calculations/confidence_model.py` already computes everything needed.
> This is a wiring task.

**What exists:**
- `compute_uncertainty_flags(chart)` → lagna_near_sign_boundary, moon_near_nakshatra_cusp, dasha_lord_uncertain, sign_boundary_planets
- `compute_confidence_intervals()` → per-house confidence with birth_time_uncertainty propagation
- `compute_chart_confidence()` → complete confidence report

**What to wire:**
- Call `compute_uncertainty_flags()` in `build_chart_context()` or `run_pipeline()`
- Add `sensitivity_warnings: list[str]` to `NarrativeReport`
- If lagna within 1° of sign boundary → prominent warning: "Birth time sensitivity HIGH — predictions may change with ±5 minute birth time adjustment"
- If Moon near nakshatra cusp → warning: "Dasha sequence may differ with slight birth time change"
- Per-house confidence flags in narrative

**Exit:** Every NarrativeReport carries birth time sensitivity warnings. Unstable predictions are flagged.

---

## G15: SAFETY FILTERING IN NARRATIVE

> 129 corpus rules are `health_sensitive=True` / `safety_tier="restricted"`.
> 6 CRITICAL guardrails (G01, G02, G03, G05, G07, G08) are NOT enforced.

**What exists:**
- `RuleRecord.health_sensitive: bool` — flagged during encoding
- `RuleRecord.safety_tier: str` — "standard" | "restricted" | "research_only"
- `docs/GUARDRAILS.md` — 6 CRITICAL items defined but not implemented

**What to wire:**
- In `narrate()`, filter claims from `health_sensitive` rules:
  - `safety_tier="restricted"` → suppress from narrative text, add to separate `restricted_findings` list
  - `safety_tier="research_only"` → exclude entirely
- Language guardrails in NL templates:
  - G01: Replace "prediction" with "indication" or "tendency" in all output text
  - G02: Health/death timing → "health attention period" not "death likely"
  - G05: Replace "certificate" with "sensitivity analysis"
- Add `NarrativeReport.safety_notes: list[str]` for practitioner-only restricted findings

**Exit:** No user-facing output contains unfiltered health/death claims. Guardrails G01/G02/G05 enforced in all NL templates.

---

## EMPIRICAL VALIDATION — OB-3 vs OB-4

> Measured 2026-04-13. Full dataset: 4,832 AA+A Rodden-rated ADB charts.

### OB-3 (legacy): Spearman ρ of raw house scores vs ADB categories

Uses `score_all_axes().d1.scores` — a single float per house. No convergence, no timing, no traceability.

### OB-4 (pipeline): Spearman ρ of convergence_score vs ADB categories

Uses `converge()` output — independent channel count (scoring + D9 + D10 + BPHS + Saravali + yoga + other_text). Net favorable minus unfavorable.

| House | Domain | OB-3 (OLD) ρ | OB-4 (CONV) ρ | Δ | Improvement |
|-------|--------|-------------|---------------|------|-------------|
| H01 | Vitality | +0.458 | **+0.549** | +0.091 | +20% |
| H03 | Communication | +0.447 | **+0.528** | +0.082 | +18% |
| H05 | Children | +0.475 | **+0.553** | +0.079 | +17% |
| H07 | Relationships | +0.474 | **+0.571** | +0.098 | +21% |
| H09 | Higher learning | +0.425 | **+0.498** | +0.073 | +17% |
| H10 | Career | +0.389 | **+0.447** | +0.057 | +15% |

**Pipeline wins on all 6 houses. 4,832 charts, zero errors. Average Δ = +0.080 (+18%).**

### Why ρ ≈ 0.50 is not publishable

1. **Binary labels are crude.** ADB categories are 1/0; convergence is 1–14 channels. Rank-biserial would be more appropriate, but label quality caps ρ.
2. **ADB categories are noisy proxies.** "Divorced" doesn't mean H7 is weak — it means H7 promise manifested negatively AND the person reported it.
3. **No timing dimension tested.** CONV and TOTAL produce identical ρ because labels have no dates. G6 temporal projection is invisible to this metric.
4. **Direction conflation.** Net convergence (fav − unfav) loses the richness of separate confirmation + contra counts.

### What would reach ρ ≥ 0.70

- Life events with dates (Phase B) — tests timing predictions
- Practitioner blind readings scored against known biographies
- Multi-class labels (strong/moderate/weak) instead of binary
- Per-prediction accuracy rather than per-house correlation

### Tool reference

- `tools/ob3_calibrate.py` — legacy scoring calibration (OB-3)
- `tools/ob4_pipeline_calibrate.py` — pipeline calibration (OB-4)

---

## G1–G6 DEFERRED INVENTORY

> Generated 2026-04-13 after completing G1–G6 critical path.
> Updated same day after exhaustive re-audit.  First version missed
> the most important gaps (CRITICAL tier).  This version is complete.

### CRITICAL — ✅ ALL RESOLVED (2026-04-13)

| # | Status | Item | Resolution |
|---|--------|------|------------|
| D0 | ✅ | Pipeline was dead code | `src/pipeline.py:run_pipeline()` is the production entry point. CLI: `python -m src.pipeline`. Also `score_chart()` and `evaluate_chart()` auto-build ChartContext now. |
| D0a | ✅ | Weight store not in hot path | `scoring_rule_eval.evaluate_rule()` now calls `get_weight_store().school_weights()` instead of importing SCHOOL_WEIGHTS directly. |
| D0b | ✅ | Convergence + temporal disconnected | `TimedPrediction` now carries `temporal_confirmations` + `temporal_systems` + `total_confirmations` property combining natal + temporal counts. |
| D0c | ✅ | ctx= parameter never passed | `score_chart()` and `evaluate_chart()` auto-build ChartContext when ctx=None. All 15+ callers now get ChartContext benefits. |

### HIGH — ✅ ALL RESOLVED (2026-04-13)

| # | Status | Item | Resolution |
|---|--------|------|------------|
| D1 | ✅ | Corpus rules missing verse_ref | `_evaluate_corpus_rules()` now looks up RuleRecord and copies `verse_ref`. 348/348 corpus results have verse. |
| D2 | ✅ | No varga natal channels | Scoring rules now run against D9+D10 lagna. `d9_natal` and `d10_natal` are independent convergence channels. H3 India 1947 = 7-channel convergence. |
| D3 | ✅ | Yoga detection keyword-based | `_classify_channel()` now checks corpus category/tags via cached yoga rule_id set (933 yoga rules identified). |
| D4 | ✅ | conditions_met often empty | `_evaluate_corpus_rules()` extracts from V2 structured conditions OR legacy primary_condition. 348/348 results have conditions_met. |
| D5 | ✅ | Custom logic in 4 scoring rules | R13 mitigation_factor, R19 cazimi/asta_vakri scores, D6 avastha thresholds, WL penalty all moved to ScoringRule.params. Evaluator reads from data. |

### MEDIUM — Improves accuracy / narrows timing

| # | Origin | Item | Why it matters | Suggested fix |
|---|--------|------|----------------|---------------|
| D6 | G6 | Transit overlay (gochara + double transit) not in temporal projection | Dasha-only timing gives broad windows. Transit narrows to 1–2 years. Architecture target shows 7 timing systems, we have 4. | Add `_gochara_windows()` scanning Jupiter/Saturn transit per year. |
| D7 | G6 | Varshaphala (solar return) not overlaid | Annual chart activation is independent evidence. 5th timing system. | Add `_varshaphala_windows()` checking Muntha/Varsha Pati per year. |
| D8 | G6 | Pratyantardasha not overlaid | Narrows timing from years to months within an AD window. | Add PAD scan inside AD matches. |
| D9 | G6 | Peak windows broad for multi-house lords | Venus lords H1+H6 → both activate in all Venus periods. | Split by domain so activation windows differ. Needs G7 domain grouping. |
| D10 | G6 | Temporal projection is year-level only | Architecture shows "Q1 2032" (quarterly precision). We output year integers. | Add month-level precision using AD/PAD start/end dates. |
| D11 | G6 | Probability normalization is crude | `count_of_active_systems / total_systems` per year. Not Bayesian, doesn't weight by system reliability. | Accept for Phase C; proper Bayesian weighting is Phase B (needs calibration data). |
| D12 | G1 | ctx= not wired into ~60 downstream modules | Performance: those modules still recompute dignity/house_map/etc. every call. Not a correctness issue. | Progressively add ctx= to hot-path modules. |
| D13 | G2 | Scoring rules are `ScoringRule` not `RuleRecord` | Two rule types coexist. Unified engine bridges them, but corpus tools (scorecard, auditor) don't see scoring rules. | Create adapter or merge into RuleRecord if schemas converge. |

### LOW — Engineering quality / Phase B prerequisites

| # | Origin | Item | Why it matters | Suggested fix |
|---|--------|------|----------------|---------------|
| D14 | G3 | Old engines (scoring.py, rule_firing.py, inference.py) not deleted | Confusion: two ways to evaluate rules. But all 14k tests and API endpoints depend on them. | Migrate callers to unified engine over multiple sessions. |
| D15 | G4 | SCHOOL_WEIGHTS dict still in scoring_rules.py | Weight store reads from it; not truly "deleted". | Move to JSON/TOML weight file, store reads from file. |
| D16 | G4 | No calibration logic; empirical_weight = base_weight | Phase B / G10 scope. No user feedback data exists yet. | Defer to Phase B. |
| D17 | ✅ | Weight store persistence | Resolved: `save_weight_store()` / `load_weight_store()` with JSON. |
| D18 | — | Q2: 8 silent handlers remain | Robustness. Independent of pipeline. | Parallel track. |
| D19 | — | Q3: Verification tags (9/112 modules) | Provenance. Independent of pipeline. | Parallel track. |
| D20 | — | Q5: MODULE_REGISTRY.py | CI enforcement. Independent of pipeline. | Parallel track. |
| D21 | — | Q9: Benchmark in CI | Performance regression detection. | Parallel track after G1. |
| D22 | — | Q10: Reproducibility snapshot test | Determinism proof. | Parallel track after G3. |
| D23 | — | Q11: DEBUG logging in canonical primitives | Observability. Independent of pipeline. | Parallel track. |
| D24 | — | Q12: Evolvability checklists | Process docs. Independent of pipeline. | Parallel track. |

---

## COMPLETION STATUS (2026-04-14)

### Phase C Foundation — ✅ COMPLETE

- [x] G1: ChartContext (5-tier, ctx= auto-built)
- [x] G2: Rules to data (26 ScoringRule records)
- [x] G3: Unified engine (EvalResult, evaluate_all_rules)
- [x] G4: Weight store (7,467 rules, 3 version axes, JSON persistence)
- [x] G5: Convergence (7 channels, independent counting)
- [x] G6: Temporal projection (7 timing systems, P(year))
- [x] G7: Narrative synthesis (life phases, interactions, absences, arcs, NL templates with claims)
- [x] D0-D5: Pipeline wired into production, data completeness
- [x] D6-D24: All deferred items resolved except D16 (Phase B)

### Phase C.5 Practitioner Depth — NEXT

Each G8 item follows: VERIFY source text → FIX discrepancies → WIRE into pipeline → TEST on golden_50.
28 modules have tests but ZERO verse verification. Verification is the bottleneck.

- [ ] G8a: Fix varga evaluation — VERIFY sapta_varga.py + varga.py against BPHS Ch.6-8, then fix D9/D10 to use actual planet positions
- [ ] G8b: VERIFY yogas_extended, yogas_graha, yogas_pvrnr, nabhasa_yogas against BPHS Ch.35-36 + Saravali Ch.15-20, then wire into convergence
- [ ] G8c: VERIFY bhava_bala, ishta_kashta against BPHS Ch.27-28, then wire into convergence weighting
- [ ] G8d: VERIFY gochara, double_transit, av_transit against BPHS Ch.64-65, then wire into temporal projection
- [ ] G8e: VERIFY chara_karak, jaimini_full against Jaimini Sutras, then wire as alternative channel
- [ ] G8f: AD-level narrative depth (wiring — AD data already verified via vimshottari_dasa)
- [ ] G8g: Domain-specific divisional analysis (D9→marriage, D10→career, D7→children)
- [ ] G8h: Claims enrichment (encoding sessions for empty predictions[])
- [ ] G14: Wire confidence_model.py into pipeline (verify against statistical theory, not text)
- [ ] G15: Safety filtering (enforce guardrails G01/G02/G05, suppress health_sensitive claims)

### Phase A Practitioner Tool — BLOCKED by G15

- [ ] G13+Q8: User/auth/session
- [ ] G8_20Q: 20Q chart-person verification
- [ ] G9: Life event capture
- [ ] G10: Feedback loop + calibration

### Phase B Research Platform — BLOCKED by G10

- [ ] G10: Full calibration engine
- [ ] G11: Rule evolution
- [ ] G12: Chart archetypes
