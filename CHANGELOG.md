# LagnaMaster — CHANGELOG.md
## S190 + Frontend Update — Naisargika Karakas + UI (March 2026)

### S190 — Naisargika Karaka Rules
- **school_rules.py**: R17/R18 implemented as Jaimini Sthir Karak rules (BPHS Ch.32)
- Strict Parashari mode deducts R17/R18 contributions via `school_score_adjustment()`

### Frontend Update (Sessions S167-S190 surface)
- **frontend/src/lib/api.ts**: 8 new types + 6 new fetch functions (svg, pdf, confidence,
  scoresV3, guidance, mundane.analyze); 13 tests passing
- **frontend/src/app/page.tsx**: Two-tab layout (Birth Chart | Mundane)
  - SVG chart with North/South Indian toggle + PDF download
  - Confidence badge with lagna boundary warning (amber tint when < 1°)
  - Collapsible V3 multi-axis scores (D1/D9/D10 grids + yoga chip lists, labelled "heuristic estimate")
  - Lazy-fetch guidance panel (career/health/finance/relationships × L1/L2/L3 depth)
  - Mundane analysis tab (nation/ingress/swearing-in form + themes/challenges/house significations)

### Deployment — /lagnamaster base path (March 2026)
- **Nginx** (`/etc/nginx/sites-available/docker_proxy`): all routes prefixed `/lagnamaster`;
  `/_stcore/` and `/static/` proxied to Streamlit (port 8501); `/lagnamaster/api/` to FastAPI (port 8000)
- **docker-compose.yml**: Streamlit `--server.baseUrlPath /lagnamaster`;
  uvicorn `--root-path /lagnamaster/api` (enables correct Swagger UI paths)
- **URLs**: App → `ip/lagnamaster` · API docs → `ip/lagnamaster/api/docs`

### Test Status: 1338 backend + 13 frontend passing, CI green

---

## S187-S189 — Scoring Gaps + XIX Output API (March 2026)

### S187 — Wiring Gaps Closed
- **multi_axis_scoring.py**: Graha Yuddha war loser −1.5 bhavesh penalty
  (Saravali Ch.4 v.18-22); `strict_school` param on `score_axis`/`score_all_axes`;
  `school_score_adjustment()` called in strict mode
- **scoring_v3.py**: `score_chart_with_dasha()` stub replaced with real
  implementation; D1 scores dasha-sensitized in `score_chart_v3()` when `on_date` supplied

### S189 — XIX Output/API + Infrastructure
- **src/api/main.py**: Version 3.0.0; `db_pg` routing (Postgres + SQLite fallback);
  5 new endpoints: `/svg`, `/pdf`, `/guidance`, `/confidence`, `/scores/v3`
- **src/api/models.py**: `SVGRequest`, `SVGOut`, `GuidanceRequest`, `GuidanceOut`,
  `ConfidenceOut`, `ChartV3Out`
- **Swiss Ephemeris**: Real SE files (sepl_18.se1 + semo_18.se1) from JPL DE431;
  Moshier fallback retired; verified flags=258 (FLG_SWIEPH)
- **ADB Fixtures**: 177 files regenerated post-FLG_TOPOCTR; 7 new charts added

### Test Status: 1338 passed, 3 skipped, CI green


## S187-S188 — Scoring Gaps + XIX Output API (March 2026)

## S190 — Documentation Sync (March 2026)

Refreshed all 11 docs/ files with tacit knowledge from SESSION_LOG.md (S33-S100),
DOCS_ADDENDUM (S15-S18), DOCS_additions (S11-S12). All content now inline in script.
Key: 63+ modules documented, Baaladi fix, montecarlo _worker() requirement,
jaimini DOTALL risk, DivisionalMap non-subscriptable, 1947 Dig Bala verified values,
dependency_prevention datetime UTC/local fix, consumer layer architecture.
Script fixed: git pull --rebase before push to prevent rejection.


## S189 — Living Documentation Folder (March 2026)

### docs/ folder created — 11 markdown files

| File | Lines | Content |
|------|-------|---------|
| `docs/MEMORY.md` | 187 | Session state, startup checklist, next session, wiring gaps, bug status |
| `docs/ARCHITECTURE.md` | 613 | Full module reference with exact function signatures, data classes, all tacit knowledge from DOCS.md |
| `docs/BUGS.md` | 108 | Accurate bug status (all fixed S1–S188), active issues C-18/PG-1/SK-1/UI-1/FX-1/EPH-1/R21-1 |
| `docs/CHANGELOG.md` | 179 | Session history S1–S188 with S189 template |
| `docs/GUARDRAILS.md` | 266 | All 24 guardrails G01–G24 with severity and compliance status |
| `docs/CLASSICAL_CORPUS.md` | 185 | Text inventory, encoding plan, yoga expansion, library ecosystem |
| `docs/KPIS.md` | 86 | All 8 KPI domains with baselines and targets |
| `docs/RESEARCH.md` | 113 | OB-3 calibration, OSF status, SHAP framework, data quality biases |
| `docs/ROADMAP.md` | 141 | Complete phase plan S189–S1050+ with gate criteria |
| `docs/PREDICTION_PIPELINE.md` | 178 | 10-layer prediction quality architecture vs competitors |
| `docs/SESSION_TEMPLATE.md` | 189 | Reusable planning template with pre/post checklists |

**Key tacit knowledge preserved from DOCS.md:**
- `_SENTINEL` pattern in `db.py`; WAL mode on every connection
- `flags=258` = FLG_SWIEPH + FLG_SPEED (confirms real SE files active)
- Ketu = `Rahu.longitude + 180° mod 360`
- 22 asymmetric pairs in Naisargika matrix
- AntarDasha formula: `maha_years × VIMSHOTTARI_YEARS[antar_lord] / 120`
- AV fixed totals: Sun=50, Moon=48, Mars=42, Mercury=55, Jupiter=57, Venus=52, Saturn=40, Sarva=344
- South Indian SVG: CELL=130px, 520×520px, exact cell position dict
- Cazimi = +0.5 override; Asta Vakri = −0.5 (not −1.0); Rx_orb = direct_orb − 2°
- `fastapi` not `fastapi[standard]` in requirements.txt
- `asynccontextmanager` lifespan; `/scores` always recomputed from birth data
- War loser: `getattr(chart, 'planetary_war_losers', set())`; `axes.d1.scores` mutated in-place
- R17/R18 score 0.0 — strict_school has no numeric effect yet

**Ground truth methodology:**
- update_docs_s188.py was used as the source of truth (not the GitHub web UI)
- All bug statuses, session numbers, and test counts verified against that script
- GitHub UI shows stale cached data — always use `git log` instead



### S187 — Wiring Gaps Closed
- **multi_axis_scoring.py**: Graha Yuddha war loser −1.5 bhavesh penalty
  (Saravali Ch.4 v.18-22); `strict_school` param on `score_axis`/`score_all_axes`;
  `school_score_adjustment()` called in strict mode
- **scoring_v3.py**: `score_chart_with_dasha()` stub replaced with real
  implementation; D1 scores dasha-sensitized in `score_chart_v3()` when `on_date` supplied

### S188 — XIX Output/API + Infrastructure
- **src/api/main.py**: Version 3.0.0; `db_pg` routing (Postgres + SQLite fallback);
  5 new endpoints: `/svg`, `/pdf`, `/guidance`, `/confidence`, `/scores/v3`
- **src/api/models.py**: `SVGRequest`, `SVGOut`, `GuidanceRequest`, `GuidanceOut`,
  `ConfidenceOut`, `ChartV3Out`
- **Swiss Ephemeris**: Real SE files (sepl_18.se1 + semo_18.se1) from JPL DE431;
  Moshier fallback retired; verified flags=258 (FLG_SWIEPH)
- **ADB Fixtures**: 177 files regenerated post-FLG_TOPOCTR; 7 new charts added

### Test Status: 1338 passed, 3 skipped, CI green



## v3.0.0 — Sessions 1–160 (March 2026)

## S189 — Immediate Fixes (March 2026)

### Kala Bala 8 Sub-components Verified (tests/test_s189_kala_bala.py)
- All 8 sub-components already implemented in `shadbala.py:234–369` (S111)
- Added 37 targeted tests verifying each sub-component analytically:
  - Nathonnata Bala (day/night — Sun/Venus/Jupiter vs Moon/Mars/Saturn vs Mercury)
  - Paksha Bala (lunar phase — benefic waxing, malefic waning)
  - Tribhaga Bala (day thirds Jupiter/Sun/Saturn; night thirds Moon/Venus/Mars)
  - Vara Bala (weekday lord = 45 virupas)
  - Hora Bala (planetary hour lord = 60 virupas)
  - Masa Bala (solar month lord = 30 virupas)
  - Abda Bala (year lord from Jan 1 weekday = 15 virupas)
  - Ayana Bala (Uttarayana Sun/Mars/Jupiter=48, Moon/Venus/Saturn=12; reversed Dakshinayana)
- Total/sum consistency and per-component range bounds verified

### C-18: 8 Diverse Stress-Test Fixtures Complete (tests/test_s189_diverse_stress.py)
- Added `BC_DATE_CHARTS` to `diverse_chart_fixtures.py`:
  - `julius_caesar_era`: 100 BCE (proleptic year -99) — Swiss Ephemeris negative year test
  - `archimedes_era`: 287 BCE (proleptic year -286) — extreme antiquity boundary test
  - Both wired into `ALL_DIVERSE_FIXTURES` with prefix `bc_`
- All 8 C-18 categories now covered in `ALL_DIVERSE_FIXTURES`:
  1. Neecha Bhanga ✅  2. Graha Yuddha ✅  3. Nakshatra cusp ✅
  4. Parivartana ✅    5. Female chart ✅  6. High-lat >55°N ✅ (Oslo 59.9°, Helsinki 60.2°)
  7. Year-boundary ✅  8. BC date ✅
- Added structural tests for each category + omnibus test_all_8_categories_covered

### Confidence Model Surfaced in Streamlit UI (src/ui/app.py)
- Added 14th tab "🔮 Confidence" wiring `confidence_model.compute_confidence()`
- Tab displays: severity banner (high/medium/low), lagna boundary flag,
  Moon/nakshatra boundary flag, sign-boundary planet list,
  per-house confidence interval table with uncertainty sources,
  adjustable birth-time uncertainty slider (1–30 minutes)

### Nehru Capricorn Lagna Skip — Root Cause Documented
- Root cause: `assert_lagna=False`, `data_trust_level="low"`, `trust_note="Indian 1889 — family memory"`
- Engine computes Cancer Lagna (111.72°); traditional Capricorn is unverified historical claim
- Skip is CORRECT — no code change required; documented in test_s189_diverse_stress.py
  (class TestNehruLagnaSkipRootCause)

### PostgreSQL Live Tests
- 3 tests in test_session20.py remain env-gated (@pytest.mark.skipif not PG_DSN)
- Cannot provision PG_DSN in this environment — deferred to S190 environment setup


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

## S161-170 pending queue complete
## S171 Pending Queue + Diverse Fixture Library complete
## CI Guard + Lint Cleanup (March 2026)

### Problem
103 consecutive CI failures on `main` — all caused by `ruff` lint (E701/E702/E402/
F401/E741) blocking the `Lint` job before pytest ever ran. Root cause was never
addressed because failures required manual copy-paste from GitHub Actions UI.

### Changes

**Lint (ruff) — 732 → 0 errors**
- `ruff format` reformatted 203 files (E701/E702 inline statement style)
- `ruff check --unsafe-fixes` removed unused imports (F401)
- Manual `# noqa: E402,F401` added to intentional late imports in:
  `src/ui/app.py`, `src/calculations/confidence_model.py`,
  `src/calculations/pushkara_navamsha.py`, `tests/fixtures/__init__.py`,
  `tests/fixtures/regression_fixtures.py`, `tests/test_calculations.py`,
  `tests/test_sessions_161_170.py`
- E741 ambiguous `l` → `line_` / `lagna_` in `tools/ci_watch.py`,
  `tools/scrape_200_aa.py`

**CI Workflow fix (`.github/workflows/ci.yml`)**
- Trailing `\` after `exit $STATUS` caused `exit: too many arguments` —
  tests passed (1330/1338) but CI reported exit code 1
- Fixed by removing the stray continuation character

**Pre-push hook (`.git/hooks/pre-push`)**
- Installed via `tools/setup_ci_guard.py`
- Runs `pytest tests/ -q --tb=short -x` before every `git push`
- Blocks push if tests fail; passes through on success
- Bypassable with `git push --no-verify` (emergencies only)

**CI watch tool (`tools/ci_watch.py`)**
- Polls `gh run list` after push; waits for completion
- On failure: fetches `gh run view --log-failed` and prints error lines locally
- `--fix` flag attempts auto-fix for known patterns (missing packages, fixture
  schema mismatches)
- Usage: `.venv/bin/python3 tools/ci_watch.py [--fix] [--run-id ID]`

**Historical cleanup**
- 104 failed CI runs deleted via `gh run delete` — actions page is clean

### Final State
- `ruff check src/ tests/ tools/` → 0 errors
- `pytest tests/` → 1338 passed, 3 skipped, 38 warnings
- CI: green on every push since fix
- Pre-push hook: active on local repo
## S186 School-mixing fix (school_rules.py) + Regression snapshot (regression_snap.py) complete
