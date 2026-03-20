# LagnaMaster — Module Reference

## src/calculations/ — 49 modules across 7 phases

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
