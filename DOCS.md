# LagnaMaster — Module Reference

## src/calculations/ — 84 modules across 19 phases

### Phase 1 — Pilot (Sessions 1–10)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| dignity.py | compute_all_dignities(chart) | REF_Dignity |
| nakshatra.py | compute_all_nakshatras(chart) | REF_Nakshatra |
| friendship.py | compute_all_friendships(chart) | REF_NaisargikaFriendship |
| house_lord.py | compute_house_map(chart) | CALC_BhaveshMap |
| chara_karak.py | compute_chara_karakas(chart) | CALC_CharaKarak |
| narayana_dasha.py | compute_narayana_dasha(chart, date) | CALC_NarayanaDasa |
| shadbala.py | compute_shadbala(chart) | CALC_Shadbala |
| vimshottari_dasa.py | compute_vimshottari_dasa(chart, date) | REF_DashaSequence |
| ashtakavarga.py | compute_ashtakavarga(chart) | CALC_Ashtakavarga |
| gochara.py | compute_gochara(chart, date) | CALC_Gochar |
| panchanga.py | compute_panchanga(chart) + compute_navamsha_chart | CALC_D9_Navamsha |

### Phase 2 — Features (Sessions 11–19)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| pushkara_navamsha.py | is_pushkara_navamsha(si, d) + run_monte_carlo | REF_PushkaraNavamsha |
| kundali_milan.py | compute_kundali_milan(chart1, chart2) | CALC_Compatibility |
| chara_dasha.py | compute_chara_dasha(chart, date) | CALC_NarayanaDasa* |
| kp_significators.py | compute_kp_chart(chart) | CALC_KPSubLord |
| varshaphala.py | compute_varshaphala(chart, year) | REF_DivisionalRules |
| varga.py | compute_varga(chart) | REF_DivisionalRules |
| sapta_varga.py | compute_vimshopak(chart) | CALC_VimshopakaBala |

### Phase 4 — Pressure Engine (Sessions 28–32)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| functional_roles.py | compute_functional_roles(chart) | CALC_BhaveshMap |
| avastha.py | compute_deeptadi/baladi/lajjitadi | REF_AvasthaRules |
| pressure_engine.py | compute_pressure_index(chart, dashas, date) | CALC_PredictiveTimeline |
| argala.py | compute_argala(chart) + compute_arudha_lagna | CALC_Argala |
| graha_yuddha.py | compute_graha_yuddha(chart) | CALC_GrahaYuddha |
| scoring_v2.py | score_chart_v2(chart) | SCORE_AllHouses |

### Phase 5 — Workbook Parity (Sessions 33–40)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| multi_lagna.py | compute_chandra/surya/karakamsha_lagna + arudha padas | CALC_ChandraLagna/SuryaLagna |
| multi_axis_scoring.py | score_all_axes(chart, school) | SCORE_H*_D1/Chandra/Surya/D9/D10 |
| rule_interaction.py | apply_rule_interactions(fired, scores) | CALC_RuleInteractionEngine |
| lpi.py | compute_lpi(chart, dashas, date, school) | OUTPUT_LifePressureIndex |
| divisional_charts.py | compute_divisional_signs + vimshopaka + d60 | CALC_DivisionalMap |
| extended_yogas.py | detect_raja/viparita/neecha + rasi_drishti + bhavat_bhavam | YOGA_DhanaRaja/Viparita |
| avastha_v2.py | compute_avasthas_v2(chart) | CALC_Avasthas |
| narrative.py | generate_narrative(lpi, chart, dashas, date) | OUTPUT_NarrativeReport |
| scoring_v3.py | score_chart_v3(chart, dashas, date, school) | SCORE_AllHouses |
| scenario.py | apply_scenario + compare_scenarios | INPUT_Chart_Scenario |

### Phase 6 — Classical Depth (Sessions 41–48)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| ishta_kashta.py | compute_ishta_kashta(chart) | REF_ShadbalaData |
| longevity.py | longevity_range(chart) + detect_balarishta | BPHS Ch.44 |
| yogini_dasha.py | compute_yogini_dasha(chart, date) | REF_DashaSequence |
| kp_full.py | kp_sub_lord_chain + kp_cusps + kp_event_promise | REF_KPSubLordTable |
| yogas_extended.py | detect_all_extended_yogas(chart, dashas, date) | YOGA_Mahapurush/Graha |
| special_lagnas.py | compute_special_lagnas(chart) | BPHS Ch.14 |
| jaimini_full.py | detect_jaimini_yogas + karakamsha_scores + jaimini_longevity | CALC_Karakamsha |
| empirica.py | record_event + compute_accuracy | REF_EmpiricaSchema |
| empirica_router.py | REST endpoints for empirical validation | REF_EmpiricaSchema |

### Phase 7 — Workbook Completeness (Sessions 49–56)
| Module | Key function | Source sheet |
|--------|-------------|-------------|
| sayanadi_full.py | compute_all_sayanadi(chart, yuddha_losers) | REF_AvasthaRules §2 |
| panchadha_maitri.py | compute_panchadha_matrix(chart) | CALC_PanchadhaMaitri |
| lagnesh_strength.py | compute_lagnesh_strength(chart) | CALC_LagneshStrength |
| dig_bala.py | compute_dig_bala(chart) | CALC_DigBala |
| yogas_graha.py | detect_graha_yogas(chart, dashas, date) | YOGA_Graha |
| narayana_argala.py | compute_argala_on_sign(si, chart) + narayana_dasha_argala_modifier | NOTES_NarayanaDasaCompliance ND-6 |
| config_toggles.py | CalcConfig + resolve_ayanamsha + r22_modifier | REF_Config §1 |
| varga_agreement.py | compute_varga_agreement(chart, school) | CALC_CompositeVargaScore col I |

---

## Scoring Schools (REF_SchoolConfig)

| Rule | Parashari | KP | Jaimini |
|------|-----------|-----|---------|
| R04 Bhavesh in Kendra/Trikon | 2.0 | 1.5 | 1.5 |
| R03 Benefic aspects (WC) | 0.75 | 0.5 | 0.75 |
| R11 Dusthana lord in house | −1.25 | −1.25 | −1.0 |
| R15 Bhavesh in Dukshthan | −2.0 | −1.75 | −2.0 |
| R17 Sthir Karak in Kendra | +0.5 | +0.5 | +0.75 |
| R23 SAV bindus ≥5 | +0.5 | +0.25 | +0.5 |
| YK multiplier | 1.5× | 1.5× | 1.25× |

## LPI Layer Weights

| Layer | Weight | Source |
|-------|--------|--------|
| D1 Natal | 35% | SCORE_AllHouses |
| Chandra Lagna | 15% | SCORE_H*_Chandra |
| Surya Lagna | 10% | SCORE_H*_Surya |
| D9 Navamsha | 15% | CALC_CompositeVargaScore |
| D10 Dashamsha | 10% | CALC_CompositeVargaScore |
| Dasha activation | 10% | CALC_PredictiveTimeline |
| Gochar transit | 5% | CALC_Gochar |

Active MD lord's natal house: ×1.15 (CALC_DashaModifier)
Narayana Dasha Argala modifier: −0.5 to +0.5 (PVRNR Ch.5, ND-6)

## Ayanamsha Reference

| Name | pyswisseph ID | Use case |
|------|--------------|---------|
| lahiri | 1 | Standard Vedic/BPHS (default) |
| raman | 3 | B.V. Raman tradition |
| krishnamurti | 5 | KP system |
| fagan_bradley | 0 | Western sidereal |

## Sayanadi 12 States (REF_AvasthaRules §2)

| # | State | Trigger | Modifier |
|---|-------|---------|---------|
| 1 | Sayana (sleeping) | Odd sign, 0°–10° | 0.60 |
| 2 | Upavesh (stirring) | Odd sign, 10°–20° | 0.75 |
| 3 | Netrapani (introspective) | Odd sign, 20°–30° | 0.85 |
| 4 | Kautuka (playful) | Even sign, 0°–10° | 0.85 |
| 5 | Nishcheshta (powerless) | Even sign, 10°–20° | 0.60 |
| 6 | Kshuditha (hungry) | Enemy sign | 0.75 |
| 7 | Trashita (thirsty) | Watery sign + malefic 7th | 0.75 |
| 8 | Deena (afraid) | Graha Yuddha loser | 0.50 |
| 9 | Mudita (joyful) | Friendly sign + benefic aspect | 1.25 |
| 10 | Sthira (content) | Own or exaltation sign | 1.25 |
| 11 | Kopa (angry) | Combust (within Sun's orb) | 0.50 |
| 12 | Prakrita (natural) | All other | 1.00 |

## Dig Bala Peak Houses (CALC_DigBala)

| Planet | Peak House | Opposite |
|--------|-----------|---------|
| Sun | H10 (Karma) | H4 |
| Moon | H4 (Sukha) | H10 |
| Mars | H10 (Karma) | H4 |
| Mercury | H1 (Lagna) | H7 |
| Jupiter | H1 (Lagna) | H7 |
| Venus | H4 (Sukha) | H10 |
| Saturn | H7 (Kalatra) | H1 |

Score formula: `1 − circular_distance(current, peak) / 6`

## Lagnesh Modifier Table (CALC_LagneshStrength)

| Condition | Modifier |
|-----------|---------|
| Kendra/Trikona + Exaltation | +0.75 |
| Kendra/Trikona | +0.50 |
| Kendra/Trikona + Debilitation | +0.25 |
| Neutral + Exaltation | +0.25 |
| Neutral | 0.00 |
| Neutral + Debilitation | −0.25 |
| Dukshthan + Exaltation | −0.25 |
| Dukshthan | −0.50 |
| Dukshthan + Debilitation | −0.75 |

## System Invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. DignityLevel enum: DEEP_EXALT/EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL_SIGN/ENEMY_SIGN/DEBIL/DEEP_DEBIL
4. WC rules R03/R05/R07/R14: always ×0.5
5. Streamlit Cloud entry: streamlit_app.py
6. MonteCarloResult fields: base_scores, mean_scores, std_scores, sensitivity, sample_count
7. Baaladi even-sign: sequence REVERSES (Mrita→Vridha→Yuva→Kumar→Bala from 0°→30°)
8. Sayanadi priority: Kopa > Deena > Sthira > Mudita > Kshuditha > Trashita > decanate > Prakrita
9. Yogini Dasha: nak_idx = floor(moon_lon × 27 / 360), start = nak_idx % 8
10. KP sub-lord spans: proportional to Vimshottari years within each nakshatra
11. Empirica event types: Career/Marriage/Divorce/Health_Crisis/Finance/Travel/Loss/Education/Other
12. ENGINE_VERSION = "3.0.0" on every score_run
13. Lagnesh modifier: −0.75 to +0.75 applied uniformly to all 12 house scores
14. Dig Bala: continuous 0.0–1.0; peak=1.0, opposite=0.0
15. Panchadha Maitri: Naisargika Friend × Tatkalik Friend = Adhi Mitra (+1.0)
16. Narayana Dasha Argala: net modifier −0.5 to +0.5 per PVRNR Ch.5
17. Varga agreement ★★ = High confidence, ★ = Moderate, ○ = Low
18. Tatkalik Friend houses from P1: {2,3,4,10,11,12}; Enemy: {1,5,6,7,8,9}
19. Ayanamsha IDs: Lahiri=1, Raman=3, Krishnamurti=5, Fagan-Bradley=0
20. Deena state: planet in yuddha_losers set passed from graha_yuddha.py

### Phase 8 — PVRNR Textbook Tier 1 (Sessions 57–63)
| Module | Key function | PVRNR source |
|--------|-------------|-------------|
| orb_strength.py | conjunction_strength(lon1, lon2) + association_strength(p1, p2, chart) | p147, p149 |
| yoga_fructification.py | yoga_fructification_score(planets, chart) + compute_amsa_level(planet, chart) | p147-148 |
| stronger_of_two.py | stronger_planet(p1, p2, chart) + stronger_sign(si1, si2, chart) | p194 |
| av_transit.py | compute_transit_av_score(chart, date) + planet_transit_quality(planet, si, chart) | p154, p165 |
| arudha_perception.py | compute_al_perception(chart, house) + compute_full_perception_model(chart) | Ch.9 p97-104 |
| yogas_pvrnr.py | detect_pvrnr_yogas(chart, dashas, date) | Ch.11 p125-130 |
| planet_effectiveness.py | compute_planet_effectiveness(planet, chart) + compute_all_effectiveness(chart) | Ch.15 p201 |

## Orb Strength Reference (PVRNR p147, p149)

| Orb | Strength | PVRNR verdict |
|-----|---------|--------------|
| 0° | 1.00 | Maximum — full results |
| 3° | 0.75 | Strong |
| 6° | 0.50 | PVRNR threshold ("within 6° or so") |
| 8° | 0.33 | Weak (Rajiv Gandhi example, p149) |
| 15°+ | 0.00 | No effective conjunction |

## Yoga Fructification Conditions (PVRNR p147)

Three conditions all required for full delivery:
1. Free from functional malefic conjunction/aspect
2. Conjunction/aspect within 6° (PVRNR explicit threshold)
3. Not combust, not debilitated, not in inimical sign

Verdict mapping: ≥0.75=Full, ≥0.50=Partial, ≥0.25=Weak, <0.25=Minimal.

## Planet Effectiveness Weights (Phase 8)

| Component | Weight | Source |
|-----------|--------|--------|
| Shadbala | 20% | BPHS Ch.27 |
| Avastha (Baaladi × Sayanadi) | 20% | BPHS Ch.45-47 |
| AV BAV rekhas in natal sign | 15% | BPHS Ch.66-76 |
| Dig Bala (directional strength) | 15% | BPHS Ch.27 |
| Amsa level (Dasa Varga count) | 15% | BPHS Ch.6 |
| Combustion penalty | 7.5% | BPHS Ch.3 |
| Graha Yuddha outcome | 7.5% | BPHS Ch.3 |

## Updated Invariants (Phase 8 additions)

21. Orb formula: `strength = max(0, 1 − orb_degrees / 15)` — 0.5 at 6°, 0.33 at 8°
22. Yoga fructification: all three PVRNR conditions must pass for Full verdict
23. Stronger-of-two hierarchy: cotenants > dignity > exalted cotenants > rasi aspects > degree
24. AV transit: BAV ≥5 rekhas = favorable, ≤3 = unfavorable (per-planet in transit sign)
25. AL perception: strong house + weak AL = Hidden Success; weak house + strong AL = Apparent Success
26. Planet effectiveness: summary-only synthesis — does NOT replace specific-purpose strength measures
27. Amsa level uses minimum across yoga planets (weakest link determines yoga strength)

### Phase 9 — Synthesis & Judgment Layer (Sessions 64–70)
| Module | Key function | Gap addressed |
|--------|-------------|--------------|
| dominance_engine.py | compute_dominance_factors(chart, dashas, date) + dominant_theme() | GAP 1 |
| promise_engine.py | compute_full_promise(chart, dashas, date) + compute_house_promise(chart, h) | GAP 2 |
| domain_weighting.py | compute_domain_lpi(chart, dashas, date, domain) + get_domain_weights(domain) | GAP 3 |
| planet_chains.py | compute_stelliums(chart) + compute_all_dispositor_chains(chart) + compute_mutual_receptions(chart) | GAP 4 |
| house_modulation.py | house_type_modifier(house, chart, age) + apply_house_modulation(scores, chart, age) | GAP 5+6 |
| confidence_model.py | compute_confidence(chart, sensitivity_report) → ConfidenceReport | GAP 8 |
| chart_exceptions.py | detect_chart_exceptions(chart) → ChartExceptionReport | GAP 9 |

## Domain Axis Weights Reference (PVRNR p181)

| Domain | D1 | Chandra | Surya | D9 | D10 | Dasha | Gochar | Primary H |
|--------|----|---------|-------|----|-----|-------|--------|-----------|
| career | 20% | 5% | 10% | 10% | 35% | 15% | 5% | 10 |
| marriage | 20% | 10% | 5% | 35% | 5% | 15% | 10% | 7 |
| mind_psychology | 20% | 40% | 10% | 10% | 5% | 10% | 5% | 4 |
| wealth | 35% | 10% | 10% | 10% | 10% | 15% | 10% | 2 |
| health_longevity | 45% | 15% | 10% | 10% | 5% | 10% | 5% | 8 |
| spirituality | 15% | 10% | 5% | 45% | 5% | 15% | 5% | 9 |
| children | 25% | 10% | 10% | 20% | 5% | 20% | 10% | 5 |
| default | 35% | 15% | 10% | 15% | 10% | 10% | 5% | — |

## Promise Levels

| Level | Score threshold | Ceiling | Meaning |
|-------|----------------|---------|---------|
| Strong | ≥ 3.0 | 9.0 | Clear natal promise — dasha will deliver |
| Moderate | ≥ 1.5 | 7.0 | Good promise — partial results likely |
| Weak | ≥ 0.5 | 5.0 | Marginal promise — results limited |
| Absent | ≥ −0.5 | 3.0 | No positive promise — dasha cannot create |
| Negated | < −0.5 | 1.0 | Active affliction — results unlikely |

## Confidence Model Weights

| Component | Weight | Description |
|-----------|--------|-------------|
| Varga agreement | 30% | ★★=1.0, ★=0.65, ○=0.30 |
| Conflict score | 25% | Benefic+malefic both active = 0.40 |
| Sensitivity | 20% | Monte Carlo stable=0.85, unstable=0.40 |
| Boundary proximity | 15% | \|score\|/2.0 — near zero = uncertain |
| Role clarity | 10% | Lord has clear functional role |

## Chart Exception Severities

| Exception | Severity | Triggers |
|-----------|----------|---------|
| Severely Challenged Chart | Critical | Average D1 score < −2.5 |
| Lagnesh in 8th + debilitated | Critical | Lagnesh debil in H8 |
| Empty Kendras | High | No planets in H1/4/7/10 |
| Lagnesh in 8th | High | Lagnesh in H8 (not debil) |
| Dusthana Lords Strong | High | ≥2 of H6/H8/H12 lords in kendra/trikona |
| Moon Severely Afflicted | High | ≥2 malefics conjunct OR malefic+dusthana |
| Multiple Combust Benefics | High | ≥2 natural benefics combust |
| Hemisphere Imbalance | Moderate | All planets in visible or invisible half |
| Exceptionally Strong Chart | Advisory | Average D1 score > +2.5 |

## Updated Invariants (Phase 9 additions)

28. Dominance engine: encodes named BPHS rules only — not gestalt synthesis
29. Promise: "dasha cannot produce what's absent" — ceiling applies even with activation
30. Domain weights all sum to exactly 1.0 (verified in tests)
31. Stellium = 3+ planets in same sign; Cancer stellium 1947 = ≥5 planets
32. Dispositor chain terminates at planet in own sign (max depth 9, cycle-safe)
33. Upachaya age modifier: 35y = 0.80×, 60y = 1.00× (full maturation)
34. Confidence: requires_expert_review when label="Uncertain" OR flags ≥ 3

---

## Consumer Product Layer (Phases 10–14)

### Architecture

All consumer traffic passes through a four-stage pipeline before reaching the user.
Engine modules are never called directly from consumer-facing endpoints.

```
guidance_api.py
  └─ score_to_language.py     Map engine scores to 5-tier signal system
  └─ explainability_tiers.py  Gate L1/L2/L3 content by depth parameter
  └─ fatalism_filter.py       Rewrite deterministic/catastrophising language
  └─ disclaimer_engine.py     Append scope disclaimers + dependency nudges
```

### Guidance pipeline modules (Phase 10)

| Module | Key function | Purpose |
|--------|-------------|---------|
| score_to_language.py | score_to_signal(score) → SignalLevel | 5-tier score mapping |
| fatalism_filter.py | filter_output(text) → str | Rewrite deterministic language |
| explainability_tiers.py | explain(engine_result, depth) → GuidanceContent | L1/L2/L3 gating |
| guidance_api.py | get_guidance(chart_id, domain, depth, on_date) → GuidanceResponse | Single consumer contract |
| disclaimer_engine.py | append_disclaimer(response, domain, session_count) → GuidanceResponse | Scope limiting |

### Privacy modules (Phase 11)

| Module | Key function | Regulation |
|--------|-------------|-----------|
| consent_engine.py | grant_consent() + right_to_erasure() | GDPR Art.7, Art.17 |
| family_consent.py | add_family_member() + revoke_consent() | GDPR + DPDP |
| data_minimisation.py | audit_stored_fields() + apply_retention_policy() | GDPR Art.5 |

### Score-to-signal reference

| Score | Signal bars | Timing label | Guidance tone |
|-------|------------|-------------|--------------|
| ≥ +3.0 | ●●●●● | Clear passage | Affirming, action-oriented |
| +1.5 to +3 | ●●●●○ | Favourable | Supportive, encouraging |
| +0.5 to +1.5 | ●●●○○ | Mixed — lean in | Balanced, preparation-focused |
| −0.5 to +0.5 | ●●○○○ | Neutral | Neither/nor, reflective |
| −1.5 to −0.5 | ●○○○○ | Navigate carefully | Patient, strategic |
| ≤ −1.5 | ○○○○○ | Significant resistance | Foundation-building, not forcing |

### Fatalism filter word-level rules

Blocked patterns (trigger rewrite): "will fail", "doomed", "impossible", "never
recover", "ruined", "financial ruin", "health crisis", "death", "destroyed",
"no hope", "certain to", "guaranteed to fail".

Rewrite rules:
- Outcome certainty → outcome tendency ("will struggle" → "may face resistance")
- Permanence → period-bound ("never" → "in this period")
- Catastrophe → challenge ("crisis" → "significant challenge")
- Fatalism → agency ("doomed to" → "may benefit from careful preparation for")

### Consumer design constraints (invariants 35–42)

35. Raw LPI and house scores permanently gated behind L3 explicit opt-in
36. L3 opt-in resets each session — no persistent L3 mode for consumers
37. Signal system is 5-bar (0–5), never percentages or star ratings
38. All guidance uses possibility language, never deterministic claims
39. Feedback loop is human-supervised only — no automated parameter changes
40. Right-to-erasure cascade is total: outputs + birth data + event log → tombstone
41. Family chart cross-analysis requires active consent from every individual
42. Session frequency caps: ≥3/day or ≥15/week triggers dependency nudge

### Risk register

| Risk | Severity | Mitigation |
|------|---------|-----------|
| User fatalism from negative scores | High | Score-to-language layer; scores never shown at L1/L2 |
| Dependency / compulsive checking | High | Session frequency monitor; no streak mechanics |
| Medical/financial advice claims | Critical | Disclaimer engine; explicit product scope statement |
| GDPR non-compliance | Critical | Consent engine + right-to-erasure (S76) |
| Child exposure | High | Age gate at chart creation (under-18 blocked) |
| Family profiling without consent | High | Per-person consent gate (S77) |
| Feedback loop manipulation | Medium | Human-supervised queue; no auto-retrain |
| Cultural insensitivity | Medium | Possibility framing; no deterministic cultural claims |
| Expert review bypass | Medium | Confidence model flags routed to practitioner handoff |
| Birth time sensitivity harm | Low | Confidence indicators; sensitivity alerts in L2 |

---

## Complete Module Reference (all 90 sessions)

### src/guidance/ — Consumer Pipeline (Phase 10, 14)

| Module | Primary function | Consumer role |
|--------|-----------------|--------------|
| score_to_language.py | score_to_signal(score) → SignalLevel | Maps scores to 5-bar system |
| fatalism_filter.py | filter_output(text) → str | Rewrites 26 deterministic patterns |
| explainability_tiers.py | explain(domain, score, depth) → GuidanceContent | L1/L2/L3 gating |
| guidance_api.py | get_guidance(chart, domain, depth) → GuidanceResponse | Single consumer contract |
| disclaimer_engine.py | get_disclaimer(domain) + append_disclaimer() | Scope limits + dependency nudge |
| educational_layer.py | get_educational_content(domain) → list | "Learn" mode explanations |
| reflection_prompts.py | get_reflection_prompt(domain, label) → str | Socratic question conversion |
| practitioner_handoff.py | build_chart_summary(chart) + should_recommend_practitioner() | Safe handoff to experts |

### src/privacy/ — Privacy & Legal (Phase 11)

| Module | Primary function | Regulation |
|--------|-----------------|-----------|
| consent_engine.py | grant_consent() + right_to_erasure() | GDPR Art.7 + Art.17 |
| family_consent.py | add_family_member() + can_run_compatibility() | GDPR + DPDP |
| data_minimisation.py | minimise_birth_time() + apply_retention_policy() | GDPR Art.5 |

### src/feedback/ — Feedback Governance (Phase 13)

| Module | Primary function | Safety role |
|--------|-----------------|------------|
| feedback_loop.py | record_feedback() + get_quality_metrics() | Human-supervised queue |
| harm_escalation.py | check_usage_pattern() → EscalationSignal | Gentle prompt only |
| dependency_prevention.py | log_session() + check_dependency_status() | Usage frequency monitor |

### src/api/ — API Layer

| Module | Routes | Notes |
|--------|--------|-------|
| main.py | /charts, /scores | Original v1 |
| main_v2.py | all v2 routes | Includes all routers |
| auth_router.py | /auth/register, /auth/login | JWT |
| school_router.py | /user/school | Parashari/KP/Jaimini toggle |
| empirica_router.py | /empirica/events, /empirica/accuracy | Event log + accuracy |
| mobile_router.py | /mobile/guidance, /mobile/alerts/schedule | L1 only, user-scheduled |

---

## Final System Invariants (all 42)

**Engine (Phases 1–9):**
1–20: see Phase 7 docs
21–27: see Phase 8 docs (orb formula, fructification, stronger-of-two)
28–34: see Phase 9 docs (dominance, promise, domain weights, stellium)

**Consumer Pipeline (Phases 10–14):**
35. Raw LPI and house scores gated behind L3 explicit opt-in
36. L3 opt-in resets each session — no persistent L3 mode
37. Signal system is 5-bar (0–5) — never percentages or star ratings
38. All guidance uses possibility language — never deterministic claims
39. Feedback loop is human-supervised only — no automated parameter changes
40. Right-to-erasure cascade: outputs + birth data + event log → tombstone
41. Family chart cross-analysis requires active consent from every individual
42. Dependency nudge: ≥ 3 sessions/day or ≥ 15/week

**Privacy:**
43. Birth time stored to minute precision only (seconds stripped)
44. IP addresses hashed (SHA-256, first 16 chars) on ingress
45. Location stored to city level only (no street, no postcode)
46. Raw birth data deleted after 90 days of user inactivity
47. Event log anonymised after 1 year (user_id → hash)
48. Age gate: under-18 blocked from chart creation

**Safety:**
49. Fatalism filter applied to ALL text before any API response
50. Harm escalation: gentle prompt only — no automatic intervention
51. No crisis resources surfaced unless explicitly requested by user
52. Practitioner referral available when confidence = "Uncertain" or critical exceptions > 0
53. No streak mechanics, no badges, no unsolicited push notifications
54. Dependency nudge text contains no shaming or alarming language

### Phase 15–18 — Muhurta, Prashna, Dashas, Upaya, Mundane (Sessions 91–100)
| Module | Key function | Source |
|--------|-------------|--------|
| panchanga.py | compute_panchanga(sun_lon, moon_lon, dt) + compute_hora() + compute_choghadiya() | BPHS almanac |
| muhurta.py | score_muhurta(task, panchanga, birth_nak, birth_moon_si, lagna_si) → MuhurtaScore | PVRNR Table 79 |
| prashna.py | analyze_prashna(chart, query_type, query_dt) → PrashnaAnalysis | BPHS Prashna |
| kalachakra_dasha.py | compute_kalachakra_dasha(chart, birth_date) + current_kalachakra_period() | BPHS Ch.36 |
| shoola_dasha.py | compute_shoola_dasha(chart, date) + compute_sudasa(chart, date) | BPHS ayur |
| tara_dasha.py | compute_tara_dasha(chart, birth_date) → list[TaraDashaPeriod] | BPHS nakshatra |
| upaya.py | get_upaya(planet, affliction) + get_chart_upayas(chart) → list[UpayadRecommendation] | PVRNR Ch.34 |
| mundane.py | analyze_mundane_chart(chart, type, desc, date, location) + compress_vimshottari() | PVRNR Ch.35 |
| contextual.py | compute_contextual_flags(chart, lat, birth_year) → ContextualFlags | PVRNR DKP |
| ashtottari_dasha.py | compute_ashtottari_dasha(chart, date) + qualifies_for_ashtottari(chart) | BPHS Ch.47 |

## Panchanga Reference

| Limb | Formula | Range |
|------|---------|-------|
| Tithi | (moon_lon − sun_lon) / 12° | 1–30 |
| Vara | weekday (Jyotish: Sun=0…Sat=6) | 0–6 |
| Nakshatra | moon_lon × 27/360 | 0–26 |
| Yoga | (sun_lon + moon_lon) × 27/360 | 0–26 |
| Karana | half-tithi (mod 11) | 0–10 |

Special yogas: Amrita Siddhi (14 Vara×Nakshatra pairs) and Sarvaartha Siddhi (40+ pairs).
Hora: planetary hour from sunrise, 24 per day. Choghadiya: 8 day + 8 night periods.

## Muhurta Task Rules (PVRNR Table 79)

| Task | Key house | Good Varas | Rule |
|------|-----------|-----------|------|
| marriage | H7 | Mon/Wed/Thu/Fri | H8 empty; benefics in H7 acceptable |
| business_launch | H10 | Mon/Wed/Thu/Fri | H8 empty; H10 strong; lagnesh strong |
| house_construction | H4 | Mon/Wed/Thu/Fri | H8 empty; H4 strong |
| surgery | H8 | Sun/Tue | Avoid nakshatra of affected body part |
| travel | H3 | Mon/Wed/Thu/Fri | H3 strong; avoid Gandanta |

## Dasha Inventory (all systems)

| Dasha | File | Cycle | Basis |
|-------|------|-------|-------|
| Vimshottari | vimshottari_dasa.py | 120yr | Moon nakshatra |
| Narayana | narayana_dasha.py | 108yr | Lagna sign |
| Yogini | yogini_dasha.py | 36yr | Moon nakshatra |
| Chara | chara_dasha.py | variable | Jaimini sign |
| Kalachakra | kalachakra_dasha.py | 100yr | Moon navamsha pada |
| Ashtottari | ashtottari_dasha.py | 108yr | Moon nakshatra (8 planets) |
| Shoola | shoola_dasha.py | variable | Lagna trine |
| Sudasa | shoola_dasha.py | variable | Lagna/8th sign |
| Tara | tara_dasha.py | 120yr | Moon nakshatra (9 categories) |
| Drig | drig_dasha.py | variable | Sign aspects received |
| Lagna Kendradi | lagna_kendradi_dasha.py | variable | Kendra/Panapara/Apoklima from Lagna |

## Upaya Gemstone Table (PVRNR Table 77)

| Planet | Gemstone | Metal | Finger | Day |
|--------|---------|-------|--------|-----|
| Sun | Ruby | Gold | Ring | Sunday |
| Moon | White Pearl | Gold | Little | Monday |
| Mars | Red Coral | Copper | Ring | Tuesday |
| Mercury | Emerald | Silver | Little | Wednesday |
| Jupiter | Yellow Sapphire | Gold | Index | Thursday |
| Venus | Diamond | Silver | Middle | Friday |
| Saturn | Blue Sapphire | Iron | Middle | Saturday |
| Rahu | Hessonite | Silver | Middle | Saturday |
| Ketu | Cat's Eye | Silver | Ring | Tuesday |

## Mundane House Significations (PVRNR p461)

| House | Mundane signification |
|-------|----------------------|
| H1 | General state of affairs, public health, cabinet |
| H2 | State revenue, wealth, imports, commerce |
| H3 | Telecommunications, transportation, media |
| H4 | Education, real estate, agriculture |
| H5 | Children, crime, mentality of leaders |
| H6 | State loans, debt, diseases, armed forces |
| H7 | Women's health, war, foreign relations |
| H8 | Death rate, state treasury, sudden events |
| H9 | Religion, judiciary, foreign affairs |
| H10 | Government, ruling party, leadership |
| H11 | Parliament, gains, alliances |
| H12 | Expenditure, foreign enemies, hospitals |

## Updated System Invariants (Phase 15–18 additions)

55. Muhurta score 0-7: Excellent≥5, Good≥4, Acceptable≥3, Avoid<3
56. Tarabala good groups: {1,3,5,7} (Janma/Sampat/Kshema/Mitra)
57. Chandrabala good positions: {1,3,6,7,10,11} from birth Moon sign
58. Kalachakra: BPHS Ch.36 canonical version; Savya=odd-pada, Apasavya=even-pada
59. Ashtottari: only applies when Rahu NOT in H1 or H7
60. Tara good categories: Sampat/Kshema/Sadhana/Mitra/Ati-Mitra
61. Upaya disclaimer present on every recommendation — non-negotiable
62. Mundane SAV threshold: ≥30 rekhas = strong house (D-10 example PVRNR p167)
63. panchanga.py supersedes panchang.py; test_panchanga_legacy.py is empty stub
64. Bandhu Yoga in jaimini_full.py uses self-contained AK lookup (no global ak_planet)

---

### Phase 19 — Advanced Dashas, Yogas & Plugin Architecture (Sessions 101–108)

| Module | Key function | Source |
|--------|-------------|--------|
| drig_dasha.py | compute_drig_dasha(chart, birth_date) → list[DrigDashaPeriod] | PVRNR preface p8; BPHS Ch.41-43 |
| lagna_kendradi_dasha.py | compute_lagna_kendradi_dasha(chart, birth_date) → list[LagnaKendradiPeriod] | PVRNR preface p8 |
| double_transit.py | compute_double_transit(chart, transit_date, domain) → DoubleTransitResult | K.N. Rao double transit theory |
| upapada_lagna.py | compute_upapada(chart) → UpapadaAnalysis | PVRNR Ch.9 p97-104 |
| kala_sarpa.py | compute_kala_sarpa(chart) → KalaSarpaResult | Modern convention (not BPHS) |
| nabhasa_yogas.py | detect_nabhasa_yogas(chart) → list[NabhasaYoga] | BPHS Ch.35 — 32 types |
| pitr_dosha.py | compute_pitr_dosha(chart) → PitrDoshaResult | Modern convention (not BPHS) |
| rule_plugin.py | register_yoga() + register_scorer() + apply_all_plugins(chart) | Plugin architecture |

## Drig Dasha Reference (PVRNR preface p8)

One of the "two rasi dasas that don't use navamsha." Period lengths are determined by
the number of rasi aspects received by each sign. Sequence starts from Lagna (if Lagna
stronger than Moon) or Moon sign (if Moon stronger). Odd signs go forward, even signs
go backward through the zodiac.

| Sign type | Direction |
|-----------|----------|
| Odd Lagna | Forward through zodiac |
| Even Lagna | Reverse through zodiac |

## Lagna Kendradi Dasha Reference

Signs grouped from Lagna by house type, processed in order:
- **Group 1 — Kendra**: signs at H1, H4, H7, H10 from Lagna
- **Group 2 — Panapara**: signs at H2, H5, H8, H11 from Lagna
- **Group 3 — Apoklima**: signs at H3, H6, H9, H12 from Lagna

Period length per sign = (planet count in sign) + 1 (minimum 1yr, maximum 12yr).

## Double Transit Reference (K.N. Rao)

| Domain | Key house | Confirmation threshold |
|--------|----------|----------------------|
| marriage | H7 lord, D9 Lagna, natal Moon | Both Jupiter + Saturn favorable |
| career | H10 lord | Both Jupiter + Saturn favorable |
| general | Dasha lord natal position | Both favorable |

Double confirmed = both transit aspects favorable.
Partial = one favorable, one challenging.
Not activated = neither.

## Nabhasa Yoga Groups (BPHS Ch.35)

| Group | Count | Basis |
|-------|-------|-------|
| Āśraya | 3 | Sign type (movable/fixed/dual) all planets occupy |
| Dala | 2 | House type (kendra/trikona) all planets occupy |
| Ākriti | 20 | Geometric distribution pattern across signs |
| Sankhya | 7 | Total number of occupied signs (1–7) |

Only the strongest yoga in each group manifests (BPHS rule).

## Modern Convention Disclaimer

`kala_sarpa.py` and `pitr_dosha.py` are labelled "modern practitioner convention"
because they do not appear in classical texts (BPHS, Parashara). Both modules carry
a `classical_disclaimer` field in their result dataclass. This is non-negotiable.

## Plugin Architecture Reference

```python
# Register a custom yoga
@register_yoga("Name", source="Regional tradition", score_if_present=1.5)
def my_yoga(chart) -> bool: ...

# Register a custom scorer
@register_scorer("Name", source="Custom", applies_to_houses=[1, 7])
def my_scorer(chart, house) -> float: ...

# Run all plugins
results = apply_all_plugins(chart)
# results.yoga_results   → list[PluginYogaResult]
# results.score_results  → list[PluginScoreResult]
# results.total_modifier → float (sum of all score modifiers)
```

All plugin results carry `plugin_note = "Custom/extended rule — not core classical engine"`.

## Updated System Invariants (Phase 19 additions)

65. Drig Dasha: sequence starts Lagna if Lagna>Moon, else Moon sign; odd=forward, even=reverse
66. Lagna Kendradi: Kendra group first, then Panapara, then Apoklima; period = planets+1
67. Double Transit: Both Jupiter+Saturn must aspect for "Double confirmation" signal
68. Upapada: if computed UL falls in H1 or H7 from AL, shift 10 signs (PVRNR exception)
69. Kala Sarpa: classical_disclaimer field is mandatory — yoga not in BPHS
70. Nabhasa: only strongest yoga per group manifests; all 32 types from BPHS Ch.35
71. Pitr Dosha: classical_disclaimer field mandatory; severity = Strong/Moderate/Mild/Not present
72. Plugin yogas: all results carry plugin_note; never override core engine outputs
