# LagnaMaster Architecture — Current vs Target

> Generated 2026-04-13 from W0 consolidation session.
> Based on 112-module audit, full data flow trace, and architectural review.

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

## GAP ANALYSIS: CURRENT → TARGET

| #  | Layer | Current | Target | Build phase | Effort |
|----|-------|---------|--------|-------------|--------|
| G1 | 2 | 135+ redundant computations | ChartContext (1×) | Phase C | 2 sessions |
| G2 | 3 | 26 rules hardcoded in Python | All rules in corpus as data | Phase C | 2 sessions |
| G3 | 3 | 2 engines, 2 output types | 1 engine, 1 EvalResult type | Phase C | 2 sessions |
| G4 | 3 | Weights hardcoded in _WEIGHTS | Weight store (versioned data) | Phase C | 1 session |
| G5 | 4 | Rules fire independently | Convergence across D1/D9/D10/dasha/transit | Phase C | 3 sessions |
| G6 | 5 | No timing beyond "dasha period" | Temporal probability P(event\|year) | Phase C/A | 3 sessions |
| G7 | 6 | Output = bag of numbers | Narrative life-phase synthesis | Phase A | 3 sessions |
| G8 | 7 | No 20Q | Chart-person verification | Phase A | 2 sessions |
| G9 | 7 | No life event capture | Outcome anchoring | Phase A | 1 session |
| G10 | 8 | No feedback loop | Event store + calibration engine | Phase A/B | 5 sessions |
| G11 | 8 | No rule evolution | Versioned rules with empirical additions | Phase B | 2 sessions |
| G12 | 8 | No chart archetypes | Cluster discovery from outcomes | Phase B | 3 sessions |
| G13 | - | No user/auth | Multi-user with shared engine | Phase A | 2 sessions |
|    | | | | **Total** | **~31 sessions** |

## BUILD ORDER

```
PHASE C FOUNDATION (G1-G5, ~10 sessions):
  G1: ChartContext
   → G2: Migrate R01-R24 to corpus
   → G3: Unified evaluation engine
   → G4: Weight store schema
   → G5: Convergence layer (multi-signal confirmation)
   → Event store SCHEMA (tables only, no engine yet)

PHASE A PRACTITIONER TOOL (G6-G9 + G13, ~11 sessions):
  G13: User/auth/session
   → G8: 20Q verification
   → G9: Life event capture
   → G6: Temporal probability
   → G7: Narrative synthesis
   → G10: Feedback loop (event store + basic calibration)

PHASE B RESEARCH PLATFORM (G10-G12, ~10 sessions):
  G10: Full calibration engine (Bayesian weight updates)
   → G11: Rule evolution (empirical condition discovery)
   → G12: Chart archetype clustering
   → Prediction language ML
```
