# LagnaMaster — Module Reference

## src/calculations/ — 25 modules

| Module | Function | Phase |
|--------|----------|-------|
| dignity.py | compute_all_dignities(chart) → dict | 1 |
| nakshatra.py | compute_nakshatra(planet, chart) → NakshatraResult | 1 |
| friendship.py | compute_friendship(p1, p2, chart) | 1 |
| house_lord.py | compute_house_map(chart) → HouseMap | 1 |
| chara_karak.py | compute_chara_karakas(chart) | 1 |
| narayana_dasha.py | compute_narayana_dasha(chart, birth_date) | 1 |
| shadbala.py | compute_shadbala(chart) → ShadbalaResult | 1 |
| vimshottari_dasa.py | compute_vimshottari_dasa(chart, birth_date) | 2 |
| ashtakavarga.py | compute_ashtakavarga(chart) → AshtakavargaChart | 1 |
| gochara.py | compute_gochara(chart, transit_date) → GocharaReport | 1 |
| panchanga.py | compute_panchanga(chart) + compute_navamsha_chart(chart) | 1 |
| pushkara_navamsha.py | is_pushkara_navamsha(si, d) + run_monte_carlo(...) | 2 |
| kundali_milan.py | compute_kundali_milan(chart1, chart2) | 2 |
| chara_dasha.py | compute_chara_dasha(chart, birth_date) | 2 |
| kp_significators.py | compute_kp_chart(chart) → KPChart | 2 |
| varshaphala.py | compute_varshaphala(chart, year) | 2 |
| varga.py | compute_varga(chart) → VargaChart | 2 |
| sapta_varga.py | compute_vimshopak(chart) | 2 |
| functional_roles.py | compute_functional_roles(chart) → FunctionalRoles | 4 |
| avastha.py | compute_deeptadi/baladi/lajjitadi(planet, chart) | 4 |
| avastha_v2.py | compute_avasthas_v2(chart) → AvasthaReportV2 | 5 |
| pressure_engine.py | compute_pressure_index(chart, dashas, date) | 4 |
| argala.py | compute_argala(chart) + compute_arudha_lagna(chart) | 4 |
| graha_yuddha.py | compute_graha_yuddha(chart) → list[GrahaYuddha] | 4 |
| multi_lagna.py | compute_chandra/surya/karakamsha_lagna(chart) + compute_all_arudha_padas(chart) | 5 |
| multi_axis_scoring.py | score_all_axes(chart, school) → MultiAxisScores | 5 |
| rule_interaction.py | apply_rule_interactions(fired, scores) → float | 5 |
| lpi.py | compute_lpi(chart, dashas, on_date, school) → LPIResult | 5 |
| divisional_charts.py | compute_divisional_signs(chart) + compute_vimshopaka(chart) + compute_d60(chart) | 5 |
| extended_yogas.py | detect_raja_dhana/viparita/neecha_bhanga_yogas(...) + compute_rasi_drishti/bhavat_bhavam(chart) | 5 |
| narrative.py | generate_narrative(lpi, chart, dashas, date) → NarrativeReport | 5 |
| scoring_v2.py | score_chart_v2(chart) → ChartScoresV2 (ENGINE_VERSION="2.0.0") | 4 |
| scoring_v3.py | score_chart_v3(chart, dashas, date, school) → ChartScoresV3 (ENGINE_VERSION="3.0.0") | 5 |
| scenario.py | apply_scenario(chart, overrides) + compare_scenarios(...) | 5 |

## src/ — Core modules

| Module | Purpose |
|--------|---------|
| ephemeris.py | pyswisseph wrapper, compute_chart() |
| scoring.py | D1 scoring engine v1 (22 rules) |
| db.py | SQLite immutable chart store |
| db_pg.py | PostgreSQL adapter (mirrors db.py API) |
| cache.py | Redis 3-tier caching |
| auth.py | JWT multi-user authentication |
| config.py | School gates (Parashari/KP/Jaimini) |
| worker.py | Celery tasks: compute_chart, monte_carlo, generate_pdf |
| report.py | PDF report generation (reportlab) |
| montecarlo.py | Monte Carlo sensitivity (re-exports pushkara_navamsha) |

## Scoring Schools

Rule weights differ by school (REF_SchoolConfig):

| Rule | Parashari | KP | Jaimini |
|------|-----------|-----|---------|
| R04 Bhavesh in Kendra/Trikon | 2.0 | 1.5 | 1.5 |
| R03 Benefic aspects house | 0.75 | 0.5 | 0.75 |
| R11 Dusthana lord in house | -1.25 | -1.25 | -1.0 |
| R23 SAV bindus ≥5 | +0.5 | +0.25 | +0.5 |
| YK multiplier | 1.5× | 1.5× | 1.25× |

## Life Pressure Index Weights

```
D1  Natal          35%   Core natal promise
CL  Chandra Lagna  15%   Emotional/relational axis
SL  Surya Lagna    10%   Authority/career axis
D9  Navamsha       15%   Inner/dharmic axis
D10 Dashamsha      10%   Career varga axis
Dasha activation   10%   Current timing weight
Gochar transit      5%   Transit influence
```

Active MD lord's natal house: ×1.15 modifier (CALC_DashaModifier).

## Invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. `_SENTINEL` in db.py and auth.py for test isolation
4. nakshatra.py field: `.dasha_lord`
5. DignityLevel enum: DEEP_EXALT/EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL_SIGN/ENEMY_SIGN/DEBIL/DEEP_DEBIL
6. WC rules R03/R05/R07/R14: always ×0.5
7. db_pg.py API exactly mirrors db.py signatures
8. Cache is optional: get() returns None on miss/error
9. Celery JSON only; PDF returned as base64 string
10. JWT tokens typed by "kind" claim
11. Streamlit Cloud entry point: streamlit_app.py
12. CI: docker job has needs: test
13. Helm: secrets in K8s Secret lagnamaster-secrets
14. Next.js: all API calls via /api/* proxy
15. Parashari school always enabled; KP/Jaimini via ENABLE_KP/ENABLE_JAIMINI
16. scoring_v3 ENGINE_VERSION stored in score_runs table for audit trail
17. MonteCarloResult fields: base_scores, mean_scores, std_scores, sensitivity, sample_count
18. Baaladi even-sign: sequence REVERSES (Mrita→Vridha→Yuva→Kumar→Bala from 0°→30°)
