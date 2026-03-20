# LagnaMaster — Module Reference

## src/calculations/ — 41 modules

### Core Calculation Modules (Phase 1–3)
| Module | Key function | Purpose |
|--------|-------------|---------|
| dignity.py | compute_all_dignities(chart) | DignityLevel per planet |
| nakshatra.py | compute_all_nakshatras(chart) | 27-nakshatra system |
| friendship.py | compute_all_friendships(chart) | Naisargika + Tatkalik |
| house_lord.py | compute_house_map(chart) | Bhavesh per house |
| chara_karak.py | compute_chara_karakas(chart) | AK/AmK/BK/MK/PK/GK/DK |
| narayana_dasha.py | compute_narayana_dasha(chart, date) | Sign-based dasha |
| shadbala.py | compute_shadbala(chart) | 6-fold planetary strength |
| vimshottari_dasa.py | compute_vimshottari_dasa(chart, date) | 120-year dasha |
| ashtakavarga.py | compute_ashtakavarga(chart) | SAV bindus |
| gochara.py | compute_gochara(chart, date) | Transit analysis |
| panchanga.py | compute_panchanga(chart) | 5 elements + D9 |

### Feature Modules (Phase 2)
| Module | Key function | Purpose |
|--------|-------------|---------|
| pushkara_navamsha.py | is_pushkara_navamsha(si, d) | Pushkara zones + Monte Carlo |
| kundali_milan.py | compute_kundali_milan(c1, c2) | 36-point compatibility |
| chara_dasha.py | compute_chara_dasha(chart, date) | Jaimini sign dasha |
| kp_significators.py | compute_kp_chart(chart) | KP significator tables |
| varshaphala.py | compute_varshaphala(chart, year) | Annual Tajika chart |
| varga.py | compute_varga(chart) | 8 divisional charts |
| sapta_varga.py | compute_vimshopak(chart) | Vimshopaka Bala (7 vargas) |

### Pressure Engine (Phase 4)
| Module | Key function | Purpose |
|--------|-------------|---------|
| functional_roles.py | compute_functional_roles(chart) | Per-lagna maleficence |
| avastha.py | compute_deeptadi/baladi/lajjitadi | Phase 4 avasthas |
| pressure_engine.py | compute_pressure_index(chart, dashas, date) | LPI v1 |
| argala.py | compute_argala(chart) | Argala/Virodhargala |
| graha_yuddha.py | compute_graha_yuddha(chart) | Planetary war |
| scoring_v2.py | score_chart_v2(chart) | ENGINE_VERSION="2.0.0" |

### Workbook Parity (Phase 5)
| Module | Key function | Purpose |
|--------|-------------|---------|
| multi_lagna.py | compute_chandra/surya/karakamsha_lagna + all 12 arudha padas | Multi-axis frames |
| multi_axis_scoring.py | score_all_axes(chart, school) | 5-axis × 23 rules |
| rule_interaction.py | apply_rule_interactions(fired, scores) | 30 rule-pair modifiers |
| lpi.py | compute_lpi(chart, dashas, date, school) | Full 7-layer LPI |
| divisional_charts.py | compute_divisional_signs + vimshopaka + d60 | 16 vargas + D60 |
| extended_yogas.py | detect_raja/viparita/neecha + rasi_drishti + bhavat_bhavam | Core yoga corpus |
| avastha_v2.py | compute_avasthas_v2(chart) | Corrected Baaladi + Sayanadi |
| narrative.py | generate_narrative(lpi, chart, dashas, date) | Plain-English report |
| scoring_v3.py | score_chart_v3(chart, dashas, date, school) | ENGINE_VERSION="3.0.0" |
| scenario.py | apply_scenario + compare_scenarios | Counterfactual explorer |

### Classical Depth (Phase 6)
| Module | Key function | Purpose |
|--------|-------------|---------|
| ishta_kashta.py | compute_ishta_kashta(chart) | Ishta/Kashta Phala BPHS Ch.27 |
| longevity.py | longevity_range(chart) + detect_balarishta | Pindayu/Nisargayu/Amsayu |
| yogini_dasha.py | compute_yogini_dasha(chart, date) | 8-lord 36-year cycle |
| kp_full.py | kp_sub_lord_chain + kp_cusps + kp_ruling_planets + kp_event_promise | Full KP engine |
| yogas_extended.py | detect_all_extended_yogas(chart, dashas, date) | 200+ Nabhasa/Chandra/Surya/Dhana yogas |
| special_lagnas.py | compute_special_lagnas(chart) | Hora/Ghati/Sree/Indu/Pranapada |
| jaimini_full.py | detect_jaimini_yogas + karakamsha_scores + jaimini_longevity | Full Jaimini corpus |
| empirica.py | record_event + compute_accuracy | Empirical event log |

---

## Scoring Schools (REF_SchoolConfig)

| Rule | Parashari | KP | Jaimini |
|------|-----------|-----|---------|
| R04 Bhavesh in Kendra/Trikon | 2.0 | 1.5 | 1.5 |
| R03 Benefic aspects house (WC) | 0.75 | 0.5 | 0.75 |
| R11 Dusthana lord in house | −1.25 | −1.25 | −1.0 |
| R17 Sthir Karak in Kendra/Trikon | 0.5 | 0.5 | 0.75 |
| R23 SAV bindus ≥5 | +0.5 | +0.25 | +0.5 |
| YK multiplier | 1.5× | 1.5× | 1.25× |

## Life Pressure Index Weights

| Layer | Weight | Source sheet |
|-------|--------|-------------|
| D1 Natal | 35% | SCORE_AllHouses |
| Chandra Lagna | 15% | SCORE_H*_Chandra |
| Surya Lagna | 10% | SCORE_H*_Surya |
| D9 Navamsha | 15% | CALC_CompositeVargaScore |
| D10 Dashamsha | 10% | CALC_CompositeVargaScore |
| Dasha activation | 10% | CALC_PredictiveTimeline |
| Gochar transit | 5% | CALC_PredictiveTimeline |

Active MD lord's natal house: ×1.15 (CALC_DashaModifier)

## Invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. `_SENTINEL` in db.py and auth.py for test isolation
4. DignityLevel enum: DEEP_EXALT/EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL_SIGN/ENEMY_SIGN/DEBIL/DEEP_DEBIL
5. WC rules R03/R05/R07/R14: always ×0.5
6. db_pg.py API exactly mirrors db.py signatures
7. Streamlit Cloud entry: streamlit_app.py
8. Helm: secrets in K8s Secret lagnamaster-secrets
9. Parashari always enabled; KP/Jaimini via ENABLE_KP/ENABLE_JAIMINI
10. MonteCarloResult fields: base_scores, mean_scores, std_scores, sensitivity, sample_count
11. Baaladi even-sign: sequence REVERSES (Mrita→Vridha→Yuva→Kumar→Bala)
12. Yogini Dasha: nakshatra index = floor(moon_lon × 27 / 360) — computed directly
13. KP sub-lord: spans proportional to Vimshottari years within each nakshatra
14. Empirica event types: Career/Marriage/Divorce/Health_Crisis/Finance/Travel/Loss/Education/Other
15. ENGINE_VERSION="3.0.0" stored on every score_run for audit trail
