# LagnaMaster — MEMORY.md
## Engine State (Sessions 1–160, March 2026)

### Core Stack
- Python 3.12 · pyswisseph · FastAPI + Celery + Redis · PostgreSQL · Next.js 14 · K8s Helm
- Engine version: v3.0.0 · 1000+ tests · CI green

### Critical Invariants — NEVER violate these

1.  hour=0 is valid (midnight) — NEVER treat as falsy
2.  Ketu = Rahu + 180° mod 360
3.  Nakshatra index: `int(lon*3/40)` — NEVER `int(lon/13.333)`
4.  MT check runs BEFORE exaltation in dignity.py
5.  display_score(raw) = 10×tanh(raw/8) — never clamp to [-10,+10]
6.  Sarva.bindus = sarva.raw_bindus (NOT double-reduced)
7.  strength() uses self.bindus (same array the test checks)
8.  AV planet tables: raw_bindus=pre-Shodhana, bindus=post-Shodhana
9.  Graha Yuddha winner = higher northward latitude (Saravali Ch.4)
10. War loser = effectively debilitated FOR ENTIRE LIFE (Saravali Ch.4 v.18-22)
11. compute_special_lagnas birth_dt defaults to datetime.now()
12. Rahu/Ketu is_retrograde = True always in Jyotish
13. qualifies_for_ashtottari() MUST be called before ashtottari dasha
14. panchanga.py supersedes panchang.py — never call old module
15. Functional dignity (by Lagna) must be used for R02/R09, not natural
16. Badhakesh: Movable=H11 lord, Fixed=H9 lord, Dual=H7 lord
17. Topocentric Moon: swe.set_topo() + SEFLG_TOPOCTR required for precision
18. Varshaphala is Tajika school — different aspects (0/60/90/120/180° only)
19. Muntha = (natal_lagna_sign + years_elapsed) % 12
20. Yoga strength is gradient 0.0-1.0, not binary present/absent
21. NBRY must surface in yoga list with +1.5 scoring bonus (Uttarakalamrita Ch.4)
22. Rashi Drishti: 20 lines in jaimini_rashi_drishti.py unblock ALL Jaimini
23. School declaration: use calc_config.CalcConfig — never mix schools silently
24. KP system: node_mode='true', ayanamsha='krishnamurti', separate pipeline
25. scoring_v3.py is a HEURISTIC — output must be labeled as estimate, not verdict

### What scoring_v3.py CANNOT claim
- It cannot claim to reproduce classical Jyotish judgments (I-A: no classical text
  assigns numeric weights)
- It cannot claim to be authoritative when Lagna is within 1° of a sign boundary
  (ayanamsha-sensitive)
- All output = "heuristic estimate" not "classical verdict"

### Module Inventory (src/calculations/)

| Module | Session | Primary Responsibility |
|--------|---------|----------------------|
| dignity.py | 109 | MT ranges, Paramotcha, NB all 6, Vargottama |
| nakshatra.py | 113 | float fix, Abhijit nakshatra |
| shadbala.py | 111 | Dig Bala arc, Kala Bala 8 sub, Drik Bala, Naisargika, Saptavargaja |
| ashtakavarga.py | 112 | Trikona+Ekadhipatya Shodhana, Kakshya, sarva consistency |
| scoring_patches.py | 110 | ASPECT_STRENGTH 3/4, display_score tanh, Kemadruma, Raj Yoga |
| planetary_state.py | 115-117 | Parivartana, Graha Yuddha+latitude, Mandi/Gulika |
| bhava_and_transit.py | 118 | Bhava Chalita, Vedha, 3-lagna transit, Ashtama Shani |
| pratyantar_dasha.py | 120 | 3rd Vimshottari PD = ad×pd/120 |
| bhava_bala.py | 125 | Bhava Bala per house |
| special_lagnas.py | 130 | Hora/Ghati/Bhava/Varnada/Sree/Indu/Pranapada/Upapada |
| config_additions.py | 124 | 36 ayanamshas, node mode, AstronomicalConfig |
| yogas_additions.py | 119 | PM Yoga D9, Sunapha/Anapha/Vesi/Vasi |
| sputa_drishti.py | 128 | Degree-based aspect orbs |
| chara_karaka_config.py | 129 | 7/8 karaka, Karakamsha, Swamsha |
| jaimini_rashi_drishti.py | 135 | Rashi Drishti + Argala |
| functional_dignity.py | 137 | Functional benefics, Badhakesh, Yogakaraka |
| planet_avasthas.py | 138 | Bala/Jagradadi/Deeptadi Avasthas |
| transit_quality_advanced.py | 142-143 | Tarabala, Chandrabala, 64th navamsha |
| upagrahas_derived.py | 146 | Dhuma, Vyatipata, Parivesha, Indrachapa, Upaketu |
| shadbala_patches.py | 147 | BPHS thresholds, 5-fold friendship, NBRY |
| varshaphala.py | 149 | Solar return, Muntha, Varshesha, Tajika aspects |
| karakamsha_analysis.py | 150 | Karakamsha, Ishta Devata, Upapada |
| yoga_strength.py | 140/145 | Yoga gradient 0-1.0, Amala/Vasumati/Chamara/Sannyasa |
| dasha_activation.py | 154 | Yoga timeline, conditional dasha, triple concordance |
| dasha_scoring.py | 139 | Dasha-sensitized scoring |
| muhurtha_complete.py | 148 | Tarabala+Chandrabala+Panchaka+Abhijit+purpose |
| kp_sublord.py | 155 | KP 249 sub-lord table, significators |
| calc_config.py | 156 | School/authority declaration |
| sudarshana.py | 159 | Sudarshana Chakra + Dasha Pravesh |
| confidence_model.py | 158 | Birth time uncertainty, confidence intervals |
| shodashavarga_bala.py | 147/G-3 | 16-varga Shodashavarga Bala |

### Known Remaining Wiring Gaps (MUST FIX)

1. **Topocentric Moon** — ephemeris.py Moon calc needs swe.set_topo() + SEFLG_TOPOCTR
2. **Functional dignity in scoring** — R02/R09 still use natural classification
3. **Dasha scoring not wired** — dasha_scoring.py built but score_chart() has no query_date
4. **War loser not downstream** — compute_dignity() doesn't check planetary_war_losers

### Test Coverage (Sessions 1-160)

- test_phase0.py: 73 tests — dignity, nakshatra, AV core
- test_ashtakavarga.py: ~40 tests — Shodhana, Kakshya, strength()
- test_varshaphala.py: 25 tests — all green
- test_comprehensive_build.py: 76 tests — Sessions 135-160
- test_pending_build.py: ~45 tests — Sessions 139-160
- test_phase9.py + all others: ~750 tests
- TOTAL: 1000+ passing, CI green


## Sessions 161-170 (Pending Queue Complete)
S161 Topocentric Moon patched in ephemeris.py (swe.set_topo)
S162 Functional dignity _is_functional_benefic/_is_functional_malefic in scoring_v3.py
S163 score_chart_with_dasha() wrapper wired
S164 get_dignity_with_war_override() in dignity.py
S165/166 tests/fixtures/regression_fixtures.py — 5 reference charts + diff_scores()
S167 north_indian_chart.py — North Indian diamond SVG + South Indian grid
S168 pdf_export.py — 2-page HTML/PDF export with weasyprint fallback
S169 kp_cuspal.py — cuspal sub-lord analysis, event promise, fructification
S170 drekkana_variants.py — Parasara/Jagannatha/Somanatha D3 + vargas.py wire

## S171+ Pending Queue Completion
- diverse_chart_fixtures.py: 70+ synthetic fixtures covering all 12 Lagnas, Graha Yuddha, Parivartana, Neecha Bhanga, Kemadruma, Sannyasa, nakshatra boundaries, transits, Tarabala, Vedha, functional dignity
- test_diverse_charts.py: parametric tests using diverse fixtures; 34-module smoke test
- TOPOCENTRIC_MOON_ENABLED = True (was False)
- weasyprint in requirements.txt
- ACTIVE_DREKKANA_METHOD = "parasara" declared in vargas.py
- baseline_india_1947.json stub created for regression testing
