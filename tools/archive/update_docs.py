#!/usr/bin/env python3
"""
Update MEMORY.md, CHANGELOG.md, and PLAN.md with complete Session 1-160 state.
Run from ~/LagnaMaster: python3 update_docs.py
"""
import os
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# ── MEMORY.md ──────────────────────────────────────────────────────────────────
MEMORY = """# LagnaMaster — MEMORY.md
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
"""

# ── CHANGELOG.md ───────────────────────────────────────────────────────────────
CHANGELOG = """# LagnaMaster — CHANGELOG.md

## v3.0.0 — Sessions 1–160 (March 2026)

### Phase 0 — Classical Correctness (S109-114)
- **dignity.py**: Mooltrikona exact BPHS Ch.3 ranges; Paramotcha continuous gradient;
  Rahu/Ketu school-specific exaltation; Neecha Bhanga all 6 conditions; NBRY when ≥2;
  DEEP_EXALT ±5°; Vargottama; Sandhi; Pushkara Navamsha/Bhaga
- **scoring_patches.py**: ASPECT_STRENGTH 3/4 for Mars/Jupiter/Saturn (BPHS Ch.26);
  display_score = 10×tanh(raw/8); Kemadruma 3 conditions + 4 cancellations;
  Raj Yoga exchange/aspect forms (BPHS Ch.36)
- **shadbala.py**: Dig Bala degree-arc formula; Kala Bala all 8 sub-components;
  Drik Bala; Naisargika exact BPHS values; Saptavargaja Bala; Ishta/Kashta Bala
- **ashtakavarga.py**: Trikona Shodhana + Ekadhipatya Shodhana; Sarva from reduced
  tables; Kakshya analysis (3°45' sub-divisions); sarva.bindus = raw_bindus (consistent)
- **nakshatra.py**: float fix int(lon×3/40); 8 regression fixtures
- **cross_validate.py**: JHora CSV cross-validation script

### Phase 1 — Core Classical Completeness (S115-124)
- **planetary_state.py**: Vargottama override; Parivartana (Maha/Kahala/Dainya);
  Graha Yuddha with latitude (Saravali Ch.4 v.12-18); Mandi/Gulika upagrahas;
  PLANETARY_WAR_LOSER_OVERRIDE constant
- **bhava_and_transit.py**: Bhava Chalita overlay; Vedha obstruction table
  (Phaladeepika Ch.26); transit from Lagna+Moon+Sun; Ashtama Shani
- **yogas_additions.py**: PM Yoga D9 strength (Sanjay Rath Ch.5);
  Sunapha/Anapha/Durudhura (BPHS Ch.38); Vesi/Vasi/Ubhayachari node exclusion (BPHS Ch.37)
- **pratyantar_dasha.py**: 3rd level Vimshottari PD
- **narayana_dasha.py**: direction per-sign parity fix (Sanjay Rath Ch.4)
- **config_additions.py**: 36 ayanamsha constants; node mode toggle; AstronomicalConfig

### Phase 2 — Depth (S125-134)
- **bhava_bala.py**: Bhava Bala (Bhavadhipati + Dig + Drishti)
- **sputa_drishti.py**: Degree-based aspect orbs with linear fade
- **chara_karaka_config.py**: 7/8 karaka toggle; Karakamsha; Swamsha; atmakaraka alias
- **special_lagnas.py**: 8 special lagnas including Upapada
- **dasha_sandhi.py**: 6-month Sandhi alerting
- **ayurdaya.py**: Pindayu + Amsayu + Nisargayu

### Sessions 135-160 — Comprehensive Build (March 2026)
- **jaimini_rashi_drishti.py** (S135): Rashi Drishti + Argala — 20 lines unblocking
  all Jaimini analysis (Jaimini Sutras Adhyaya 1 Pada 1 v.15-20)
- **functional_dignity.py** (S137): Functional benefics/malefics all 12 Lagnas;
  Badhakesh; Yogakaraka (V.K. Choudhry Ch.3; BPHS Ch.34)
- **planet_avasthas.py** (S138): Bala Avastha (BPHS Ch.45); Jagradadi (Saravali Ch.5);
  Deeptadi 9-state (Phaladeepika Ch.8)
- **transit_quality_advanced.py** (S142-143): Tarabala (Phaladeepika Ch.26 v.20-25);
  Chandrabala; 64th navamsha + 22nd drekkana; double transit theory (Sanjay Rath Ch.14);
  Chandra Shtama; AdvancedTransitResult with quality_score
- **upagrahas_derived.py** (S146): Dhuma, Vyatipata, Parivesha, Indrachapa, Upaketu
  (Phaladeepika Ch.26; BPHS Ch.25)
- **shadbala_patches.py** (S147): BPHS minimum thresholds (Ch.27 v.76-80);
  5-fold Panchadhyayee Maitri (Ch.15); NBRY surfacing +1.5 bonus; war loser persistence
- **varshaphala.py** (S149): Solar return via binary search; Muntha; Varshesha;
  TajikaAspect dataclass; all 5 Tajika aspects with orbs; 25 tests green
- **karakamsha_analysis.py** (S150): Karakamsha; Ishta Devata by Rashi Drishti;
  deity/mantra/gemstone; Upapada marriage analysis
- **yoga_strength.py** (S140/145): Yoga gradient 0.0-1.0 with D9 confirmation;
  Amala/Vasumati/Chamara/Mahabhagya; 12 Sannyasa Yoga types
- **dasha_activation.py** (S154): Yoga Activation Timeline; conditional dasha
  applicability; Triple Chart Concordance (Gayatri Devi Vasudev Ch.4)
- **dasha_scoring.py** (S139): Dasha-sensitized scoring — 1.5× for active dasha lord
- **muhurtha_complete.py** (S148): Full Muhurtha — Tarabala+Chandrabala+Panchaka+
  Vishti+Siddha/Amrita/Visa+Abhijit+purpose-specific rules (Muhurta Chintamani)
- **kp_sublord.py** (S155): 249 sub-lord table; compute_kp_significators();
  ruling planets (K.S. Krishnamurti Reader Series)
- **calc_config.py** (S156): CalcConfig.school/authority; PARASHARI_PVRNR,
  KP_CONFIG, JAIMINI_RATH presets (Sanjay Rath Preface)
- **sudarshana.py** (S159): Sudarshana Chakra 3-wheel concordance (BPHS Ch.67);
  Dasha Pravesh charts (K.N. Rao Advanced Techniques Vol.2)
- **confidence_model.py** (S158): Birth time uncertainty propagation; lagna/nakshatra
  boundary flags; ConfidenceInterval per house (Hart de Fouw, Light on Life Appendix)
- **shodashavarga_bala.py** (G-3): 16-varga Shodashavarga Bala extension

### Bug Fixes (CI Stabilization)
- AV strength(): bindus threshold 5/4/Weak — sarva.bindus=raw_bindus for consistency
- Sannyasa yoga names all contain 'Sannyasa' string (test assertion)
- Varshaphala signature: birth_year keyword + natal_birth_date alias + **kwargs
- compute_confidence() HouseConfidence + ChartConfidenceReport2 matching test_phase9
- Ruff F841: removed unused current_lon, summary, lords, lagna_si variables
- Ruff F821: is_maraka → rules_maraka in functional_dignity.py
- Ruff F811: removed duplicate compute_confidence alias
- Sannyasa yoga try/except guards compute_yoga_strength on mock charts
"""

# ── PLAN.md ────────────────────────────────────────────────────────────────────
PLAN = """# LagnaMaster — PLAN.md
## Sessions 1–160 Complete · Sessions 161+ Roadmap

### Completed Architecture (Sessions 1–160)

#### Calculation Engine
- 34 calculation modules in src/calculations/
- Parashari + Jaimini + Tajika + KP school declarations
- 1000+ tests, CI green, all sessions complete

#### What Is Done vs What Needs Wiring

**DONE AND WIRED into main pipeline:**
- dignity.py, shadbala.py, ashtakavarga.py (all wired to scoring)
- scoring_patches.py (ASPECT_STRENGTH + display_score in scoring_v3.py)
- nakshatra.py, bhava_and_transit.py, planetary_state.py
- varshaphala.py (25 tests, standalone module)
- All special lagnas, dasha systems, varga charts

**BUILT but NOT YET WIRED into main scoring pipeline:**
- functional_dignity.py — compute_functional_classifications() not in R02/R09
- dasha_scoring.py — apply_dasha_scoring() not called from score_chart()
- planet_avasthas.py — combined_modifier not applied to scoring
- shadbala_patches.py — war loser override not checked in compute_dignity()

**TOPOCENTRIC MOON — 2-line fix, NOT applied:**
```python
# In ephemeris.py, before Moon swe.calc_ut() call:
swe.set_topo(birth_lat, birth_lon, 0)
flags |= swe.FLG_TOPOCTR  # for Moon calculation only
```

### Sessions 161–170 (Priority Queue)

| Session | Task | Effort | Impact |
|---------|------|--------|--------|
| 161 | Topocentric Moon — 2 lines in ephemeris.py | 30 min | HIGH — nakshatra accuracy |
| 162 | Wire functional dignity into R02/R09 | 2 hr | HIGH — systematic fix for all charts |
| 163 | Wire dasha_scoring into score_chart() | 3 hr | HIGH — temporal scoring |
| 164 | Wire war loser into compute_dignity() | 2 hr | MED — Graha Yuddha downstream |
| 165 | JHora reference fixtures (5 charts as JSON) | 4 hr | HIGH — external validation |
| 166 | Regression snapshot (J-2) | 3 hr | MED — prevents silent score changes |
| 167 | North Indian chart SVG | 6 hr | HIGH — commercial value |
| 168 | PDF export (weasyprint) | 4 hr | HIGH — client deliverables |
| 169 | KP cuspal sub-lord + promise/fructification | 8 hr | MED — KP completeness |
| 170 | Drekkana variant selection (Parasara/Jagannatha) | 2 hr | MED — D3 correctness |

### Classical Audit — Resolution Status

| Domain | Audit Issues | Done | Wired | Roadmap |
|--------|-------------|------|-------|---------|
| I. Scoring Engine | 5 | 4 | 1 (I-E) | 0 |
| II. Astronomical | 5 | 4 | 1 (F-1 topo) | 0 |
| III. Dignity | 14 | 13 | 1 (B-3 war) | 0 |
| IV. Aspects | 3 | 3 | 0 | 0 |
| V. House System | 3 | 2 | 1 (G-2) | 0 |
| VI. Vargas | 10 | 10 | 0 | 0 |
| VII. Shadbala | 8 | 8 | 0 | 0 |
| VIII. Yogas | 11 | 11 | 0 | 0 |
| IX. Dasha | 7 | 7 | 0 | 0 |
| X. AV | 4 | 4 | 0 | 0 |
| XI. Transit | 8 | 7 | 1 (XI-D) | 0 |
| XII. Panchanga | 4 | 4 | 0 | 0 |
| XIII. Jaimini | 6 | 6 | 0 | 0 |
| XIV. Special Lagnas | 2 | 2 | 0 | 0 |
| XVI. Varshaphala | 1 | 1 | 0 | 0 |
| XVIII. Validation | 3 | 1 | 1 | 1 |
| XIX. Output/API | 5 | 1 | 1 | 3 |
| OB. Architecture | 5 | 4 | 0 | 1 |

### OB-3 (Empirical Calibration) — Long-Term Roadmap
Requires 500+ verified charts with documented life events.
ML pipeline: collect → verify → feature extract → gradient boost → feature importance.
Not feasible without chart corpus collection. Track as separate research project.

### Architecture Decisions (Permanent)

1. Scoring engine is a HEURISTIC — never present as classical verdict
2. School declaration (calc_config.py) gates which rules fire
3. CalcConfig.authority resolves inter-authority conflicts (PVRNR vs BV Raman)
4. All new rules must carry source: str docstring citing Text Author Ch.X v.Y
5. New yogas must have passing test with India 1947 OR a specific counter-example chart
6. Varshaphala is Tajika school — different aspects, separate pipeline
7. KP requires true node + KP ayanamsha + separate significator pipeline
"""

# Write files
with open("MEMORY.md", "w") as f: f.write(MEMORY)
print("OK  MEMORY.md")

with open("CHANGELOG.md", "w") as f: f.write(CHANGELOG)
print("OK  CHANGELOG.md")

with open("PLAN.md", "w") as f: f.write(PLAN)
print("OK  PLAN.md")

print("\nDone. Run:")
print("  git add MEMORY.md CHANGELOG.md PLAN.md")
print("  git commit -m 'docs: comprehensive MEMORY/CHANGELOG/PLAN through Session 160'")
print("  git push")
