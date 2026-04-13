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
W0 ✅ ─→ G1+Q1 ──→ G2 ──→ G3+Q4 ──→ G4+Q6 ──→ G5 ──→ G6 ─┼→ G7 ──→ G10 ───────┼→ G11 ──→ G12
Done     ChartCtx  Rules   Unified   Weight    Convrgn Temp │  Narrative Feedback │  Rule     Archetypes
         tier ord  to data engine    store     layer   prob │  synthesis loop     │  evolution
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
After G3:  Resume BPHS encoding (Ch.26+) ──────────────────→│                     │
           (encoding now produces verifiable predictions)   │                     │
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
  └─ Blocks: G7 (narrative needs timed predictions to sequence into life phases)

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

PHASE A PRACTITIONER TOOL:
  G13+Q8: User/auth/session + data sensitivity
   → G8: 20Q chart-person verification
   → G9: Life event capture + outcome anchoring
   → G7: Narrative life-phase synthesis
   → G10: Feedback loop (event store → basic calibration)

PHASE B RESEARCH PLATFORM:
  G10: Full calibration engine (Bayesian weight updates)
   → G11: Rule evolution (empirical condition discovery)
   → G12: Chart archetype clustering
   → Prediction language ML
```
