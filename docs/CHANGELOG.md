# CHANGELOG.md — LagnaMaster Session History
> **Append a new entry at the END of every session without fail.**
> Format: `## S[N] — [Date] — [Title]`
> Ground truth: `update_docs_s*.py` scripts, not the GitHub UI (known caching issue).

---

## How to Write a Session Entry

```markdown
## S[N] — [YYYY-MM-DD] — [Session Title]

**Commit:** [SHA]
**Tests:** [N passing / N skipped / 0 lint errors]

### What was built
- `[module].py`: [description]

### What was wired
- [Connection made between modules]

### Bugs fixed
- [Bug ID]: [fix description]

### New invariants
- #[N]: [description] — [classical source]

### Three-Lens Notes
- Tech: [architectural impact]
- Astrology: [rules added, corpus progress]
- Research: [scientific integrity impact]

### Next session
S[N+1] — [Title]
```

---

## Session History

### S1–S5 — Pilot Build

- **S1**: `ephemeris.py` — pyswisseph wrapper, BirthChart dataclass. P-1 (midnight fix: `if hour is None`), P-4 (bad ayanamsha → ValueError), N-1 (Narayana Dasa Taurus=7yr) all fixed. 14 tests.
- **S2**: `src/calculations/` — 7 Jyotish modules (dignity, nakshatra, friendship, house_lord, chara_karak, narayana_dasa, shadbala). 36 tests.
- **S3**: `scoring.py` (22-rule engine) + `api/main.py` (5 endpoints) + `db.py` (SQLite, `_SENTINEL` pattern, WAL mode). 20 tests.
- **S4**: `ui/app.py` — Streamlit 3-tab UI. 6 tests.
- **S5**: Docker Compose + Dockerfile + Makefile + integration tests. 17 tests.
- **Total S1–S5**: 93/93 tests passing.

### S6–S10 — Accuracy Completion

- **S6**: `vimshottari_dasa.py` + `chart_visual.py` (South Indian SVG 520×520px, CELL=130px) + 4-tab UI. 20 tests.
- **S7**: `yogas.py` (13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special) + enriched planet table + Yogas tab in UI. 14 tests.
- **S8**: `ashtakavarga.py` (Parashari 8-source bindu tables, fixed totals Sun=50/Moon=48/Mars=42/Mercury=55/Jupiter=57/Venus=52/Saturn=40/Sarva=344). E-1/A-2 regression guards. S-2 fixed (Chesta Bala formula: `min(60, mean_motion/|speed|×60)`). 26 tests.
- **S9**: `gochara.py` (transit analysis, Sade Sati, AV bindus) + Shadbala UI surface + Transits tab. 29 tests.
- **S10**: `panchanga.py` (5-limb almanac: Tithi/Vara/Nakshatra/Yoga/Karana + D9) + Navamsha SVG (`navamsha_svg()`). 40 tests.
- **Total S1–S10**: 222/222 tests passing (pilot complete).

### S11–S108 — Extended Classical Depth

*Sessions adding additional calculation modules, scoring refinements, ADB import pipeline, additional yoga types, Streamlit UI extensions, and accuracy fixes. Test count grew from 222 → ~990.*

Key milestones:
- ADB XML importer (`tools/adb_xml_importer.py`) — batch fixture import
- Extended yogas, additional Shadbala sub-components
- Streamlit 7-tab UI completion (all tabs: Chart/Scores/Yogas/AV/Dasha/Transits/Rules)
- Docker → K8s planning, Next.js consumer UI scaffolding
- `packages.txt` (`gcc g++ python3-dev`) confirmed for Streamlit Cloud pyswisseph compilation

### S109–S160 — Classical Audit Phase

*Systematic audit against BPHS, Phaladeepika, Saravali, Brihat Jataka, Jaimini Sutras. Heuristic scoring engine noted as non-classical methodology. Phase 0 correctness fixes applied.*

Key milestones:
- Multi-axis scoring (`multi_axis_scoring.py`) — D1/D9/D10/CL/SL axis architecture
- Scoring V3 scaffolding (`scoring_v3.py`) — dasha-sensitized score infrastructure
- School-mixing fix (Jaimini/Parashari strict separation via `calc_config.py`)
- All 12 Lagnas covered in ADB fixture set
- Regression snapshot infrastructure (J-2)

---

## S161 — Topocentric Moon (FLG_TOPOCTR)

**Status:** ✅ Complete  
**What was wired:**
- `ephemeris.py`: `swe.set_topo(lat, lon, 0)` called before Moon calculation
- `SEFLG_TOPOCTR` flag added for Moon only
- Corrects Moon parallax up to 1° — critical for nakshatra boundary cases
- 177 ADB fixture files regenerated post-correction

---

## S162 — Functional Dignity in R02/R09

**Status:** ✅ Complete  
**What was wired:**
- `multi_axis_scoring.py` R02/R09: replaced natural (Naisargika) classification with `compute_functional_classifications(lagna_si)`
- Saturn yogakaraka from Capricorn lagna now scores differently to Saturn functional malefic from Cancer lagna
- Approximately 8% of charts affected

---

## S163–S186 — Scoring Depth + School Fixes + Regression Snapshot

*Additional scoring invariants, school-mixing architecture fixes, regression snapshot infrastructure (J-2), ADB fixture expansion. Tests grew from ~990 → ~1300.*

---

## S187 — Scoring Wiring Gaps Closed

**Tests:** ~1310+ passing  
**Commit message:** `feat(S187): wire scoring gaps — war loser penalty, dasha scoring, strict_school`

### multi_axis_scoring.py
- **War loser penalty**: `_score_one_house` now checks `bh_war_loser`:
  ```python
  bh_war_loser = bhavesh in getattr(chart, 'planetary_war_losers', set())
  # If True → -1.5 penalty to house score (permanent, not just at time of war)
  # Classical source: Saravali Ch.4 v.18-22
  ```
- **strict_school**: `score_axis()` and `score_all_axes()` accept `strict_school: bool = False`. When `True`, `school_score_adjustment()` deducts forbidden-school rule contributions. *Note: R17/R18 currently score 0.0 so no numeric change yet.*

### scoring_v3.py
- `score_chart_with_dasha()` stub replaced with real implementation accepting `base_scores` param
- `score_chart_v3()` now calls it after `score_all_axes()`, mutating `axes.d1.scores` when `on_date` supplied
- D1 scores are now dasha-sensitized when a query date is provided

### New Invariants
- **#35**: War loser bhavesh = −1.5 to house score (Saravali Ch.4 v.18-22) — **live**
- **#36**: `strict_school=True` deducts Jaimini contributions in Parashari mode — **live**

---

## S188 — XIX Output/API + Postgres Routing + Swiss Ephemeris

**Tests:** 1338 passing, 3 skipped (require live PG_DSN), 0 lint errors, CI green  
**Commit message:** `docs(S188): sync all documentation — S187 wiring gaps, S188 XIX API, SE upgrade`

### src/api/main.py
- Version bumped to `3.0.0`
- `src.db` → `src.db_pg` (Postgres routing — auto-falls back to SQLite if `PG_DSN` not set)
- 5 new endpoints added:

| Endpoint | Module | Description |
|----------|--------|-------------|
| `POST /charts/{id}/svg` | `north_indian_chart.py` | North/South Indian SVG |
| `POST /charts/{id}/pdf` | `pdf_export.py` | 2-page PDF (weasyprint / HTML fallback) |
| `POST /charts/{id}/guidance` | `guidance_api.py` | Consumer L1/L2/L3 guidance |
| `GET /charts/{id}/confidence` | `confidence_model.py` | Lagna/nakshatra boundary warnings |
| `GET /charts/{id}/scores/v3` | `scoring_v3.py` | Dasha-sensitized multi-axis scores |

### src/api/models.py
Added: `SVGRequest`, `SVGOut`, `GuidanceRequest`, `GuidanceOut`, `ConfidenceOut`, `ChartV3Out`

### Swiss Ephemeris Upgrade
- Real SE files downloaded from `github.com/aloistr/swisseph`:
  - `sepl_18.se1` (473K — planets) + `semo_18.se1` (1.2M — Moon)
- pyswisseph now uses JPL DE431 — Moshier fallback **retired**
- Verified: `swe.calc_ut()` returns `flags=258` (FLG_SWIEPH=2 + FLG_SPEED=256), confirming real files active
- Historical charts (pre-1800): requires `seplm_18.se1` + `semom_18.se1`

### ADB Fixtures
- 177 existing fixture files regenerated post-FLG_TOPOCTR Moon correction
- 7 new fixtures added: Ambedkar, Bush, Kennedy, Rockefeller, Roosevelt FDR, Tata JRD, Wells HG
- All 12 Lagnas now covered across 200+ real birth charts

---

## S189 — [DATE TBD] — [FILL IN AFTER COMPLETION]

**Commit:** [FILL IN]  
**Tests:** [FILL IN]

### What was built / fixed
[FILL IN]

### Next session
S190 — [FILL IN]

---

## S193 — 2026-03-28 — HouseScore Distribution Dataclass

**Commit:** (see git log)
**Tests:** 1490 passing, 3 skipped (require live PG_DSN), 0 lint errors, CI green

### What was built
- `src/calculations/house_score.py`: `HouseScore` dataclass with fields
  `house`, `score`, `mean`, `std`, `p10`, `p90` plus `to_dict()` for JSON
  serialisation.  `compute_house_scores(chart, school)` wraps D1 scoring and
  confidence-interval propagation to produce `dict[int, HouseScore]`.
- `tests/test_s193_housescore_distribution.py`: 6 tests covering dataclass
  fields, JSON serialisation, distribution ordering (p10 ≤ mean ≤ p90),
  full dict shape, and India 1947 H2-negative regression.

### What was wired
- `ChartScoresV3` gains a `house_distributions: dict` field (backward-compat)
  populated by `compute_house_scores()` inside `score_chart_v3()`.

### New invariants
- #37: `HouseScore.p10 <= HouseScore.mean <= HouseScore.p90` — always enforced
  by construction (normal-distribution percentile derivation from 95 % CI).

### Three-Lens Notes
- Tech: House scores are now typed objects — consumers can extract uncertainty
  bands without re-running the confidence model.
- Astrology: Distribution width reflects birth-time uncertainty (±5 min) and
  Lagna/Moon nakshatra boundary proximity.
- Research: p10/p90 bands enable ensemble-style prediction intervals.

### Next session
S194 — [TBD]

---

## S194 — 2026-03-28 — Conditional Weight Functions W(planet, house, lagna, functional_role)

**Commit:** (see git log)
**Tests:** 1503 passing, 3 skipped (require live PG_DSN), 0 lint errors, CI green

### What was built
- `src/calculations/conditional_weights.py`: `WeightContext` dataclass and
  `W(ctx) -> float` function that replaces flat static rule weights with
  context-conditional modifiers:
  - Yogakaraka × YK_MULT (1.5 Parashari/KP, 1.25 Jaimini) — early-return
  - Functional benefic + positive rule × 1.2
  - Functional malefic + negative rule × 1.2 (stronger affliction)
  - Role mismatch × 0.75 (cross-direction mitigation)
  - Kendra/Trikona house + positive rule × 1.1
  - Dusthana house + negative rule × 1.1
  - `g06_compliant` property: KP school requires Krishnamurti ayanamsha (G06)
- `tests/test_s194_conditional_weights.py`: 13 tests covering all modifiers,
  G06 compliance flags, and role-alignment logic.

### What was wired
- `build_context()` convenience constructor for downstream callers.
- Module ready for Phase 2 engine rebuild — not yet wired into live scoring
  to preserve regression stability.

### New invariants
- #38: W(yogakaraka) = base × YK_MULT and returns immediately — no further
  house or role modifiers stack on top of yogakaraka status.
- #39: W(neutral, non-kendra/dusthana) = base_weight exactly (no noise added).

### Guardrail compliance
- G06: WeightContext.g06_compliant flags KP+Lahiri as non-compliant.
  Full fix deferred to S212 (ayanamsha selection).

### Three-Lens Notes
- Tech: Introduces the Layer I weight infrastructure that Phase 2 will wire
  into the full engine. All existing scores are unchanged (not yet wired).
- Astrology: Encodes functional dignity primacy (V.K. Choudhry Systems Approach
  Ch.3) and house-type promise hierarchy (BPHS Ch.11) as computable functions.
- Research: Context-conditional weights are a prerequisite for SHAP analysis
  (Phase 6) — static weights produce uninterpretable attribution.

### Next session
S195 — Feature decomposition: 23 binary rules → 150+ continuous features (G22)
---

## S195 — 2026-03-28 — Feature Decomposition Infrastructure

**Tests:** 1517 passing, 3 skipped, 0 lint errors

### What was built
- `src/calculations/feature_decomp.py`: `RuleFeature`, `HouseFeatureVector`,
  `ChartFeatureVector` dataclasses + `extract_features(chart, school)`.
  Four extractors: `gentle_sign` (R01), `bhavesh_dignity` (R04 continuous),
  `dig_bala` (R20), `sav_bindus_norm` (R23 continuous).
  4 features × 12 houses = 48 features. G22 compliance note in module docstring.

### Next session
S196 — kartari_score, combust_score, retrograde_score, bhavesh_house_type
---

## S196 — 2026-03-28 — Feature Extractors: kartari, combust, retrograde, bhavesh_house_type

**Tests:** 1525 passing, 3 skipped, 0 lint errors

### What was built
- `feature_decomp.py` +4 extractors: `kartari_score` (R08/R12), `combust_score` (R19),
  `retrograde_score` (R22), `bhavesh_house_type` (R04 placement). 8 × 12 = 96 features.

### Next session
S197 — benefic_net_score, malefic_net_score, karak_score
---

## S197 — 2026-03-28 — Feature Extractors: benefic_net_score, malefic_net_score, karak_score

**Tests:** 1530 passing, 3 skipped, 0 lint errors

### What was built
- `feature_decomp.py` +3 extractors: `benefic_net_score` (R02-R07), `malefic_net_score` (R09-R14),
  `karak_score` (R17/R18 Sthira Karak). 11 × 12 = 132 features.
- Wired `compute_functional_roles` into `extract_features()` for is_fb/is_fm.

### Next session
S198 — pushkara_nav + war_loser extractors → 13 × 12 = 156 features
---

## S198 — 2026-03-28 — Feature Extractors: pushkara_nav, war_loser

**Tests:** 1535 passing, 3 skipped, 0 lint errors

### What was built
- `feature_decomp.py` +2 extractors: `pushkara_nav` (R21 Pushkara Navamsha),
  `war_loser` (Graha Yuddha Saravali Ch.4). 13 × 12 = 156 features.
- **Crosses 150-feature threshold** — feature space ready for Phase 6 (G22).

### Next session
S199 — contract tests: feature_count ≥ 150, array/dict consistency
---

## S199 — 2026-03-28 — Feature Contract Tests

**Tests:** 1545 passing, 3 skipped, 0 lint errors

### What was built
- `tests/test_s199_feature_contracts.py`: 10 contract tests ensuring
  internal consistency of ChartFeatureVector — to_array/to_dict length,
  unique names, order consistency, all-float, 12 houses, finite values,
  G22 Phase 6 gate (feature_count ≥ 150).

### Next session
S200 — final G22 wiring, ChartScoresV3 integration, session log export
---

## S200 — 2026-03-28 — G22 Integration + ChartScoresV3 Feature Vector

**Tests:** 1550 passing, 3 skipped, 0 lint errors

### What was built
- `scoring_v3.py`: Added `feature_vector: ChartFeatureVector` field to `ChartScoresV3`.
  `score_chart_v3()` now calls `extract_features(chart, school)` and populates it.
- `ROADMAP.md`: S193–S200 marked ✅. Feature decomposition phase complete.
- **Phase 0 feature decomposition milestone:** 13 × 12 = 156 continuous features,
  all G22 compliant. Phase 6 (ML Pipeline) feature space requirement satisfied.

### Phase summary (S195–S200)
| Session | Added | Running total |
|---------|-------|---------------|
| S195 | gentle_sign, bhavesh_dignity, dig_bala, sav_bindus_norm | 48 |
| S196 | kartari_score, combust_score, retrograde_score, bhavesh_house_type | 96 |
| S197 | benefic_net_score, malefic_net_score, karak_score | 132 |
| S198 | pushkara_nav, war_loser | **156** |
| S199 | Contract tests (G22 gate) | — |
| S200 | ChartScoresV3 wiring, ROADMAP ✅ | — |

### Next session
S201 — OSF pre-registration + ADB license + corpus extractor pipeline
---

## S201 — 2026-03-28 — OSF Pre-Registration Schema (G22)

**Tests:** 1558 passing, 3 skipped, 0 lint errors

### What was built
- `src/research/osf_registration.py`: `HypothesisSpec`, `CVStrategy`, `OSFRegistration`
  dataclasses + `to_dict()` / `to_json()` serialization.
- `docs/research/osf_draft_ob3.json`: Draft OB-3 filing — primary H1 (concordance
  predicts above single-school baseline), 3 secondary hypotheses, BH-FDR q<0.05,
  time-split CV (pre-2010 train / 2010+ test), minimum_sample=1000.

### Next session
S202 — RuleRecord + CorpusRegistry infrastructure
---

## S202 — 2026-03-28 — Corpus Infrastructure: RuleRecord + CorpusRegistry

**Tests:** 1570 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/rule_record.py`: `RuleRecord` dataclass — rule_id, source, chapter,
  school, category, description, confidence (0–1), verse, tags, implemented, engine_ref.
- `src/corpus/registry.py`: `CorpusRegistry` — add/get/filter/count/summary;
  raises ValueError on duplicate rule_id.

### Next session
S203 — ADB license compliance module + data source tracking
---

## S203 — 2026-03-28 — ADB License Compliance + R01-R23 Corpus Encoding

**Tests:** 1582 passing, 3 skipped, 0 lint errors

### What was built
- `src/research/data_license.py`: `DataSourceLicense` dataclass, `KNOWN_SOURCES`
  (ADB non-commercial, PUBLIC_DOMAIN, BPHS_TEXT, SELF_REPORTED),
  `check_source_license(source_id, commercial)` — raises PermissionError for ADB+commercial.
- `src/corpus/existing_rules.py`: All 23 engine rules (R01-R23) encoded as
  `RuleRecord` objects in `EXISTING_RULES_REGISTRY`. All marked `implemented=True`,
  confidence ≥ 0.8, full classical source citations.

### Next session
S204 — corpus extractor base class + BPHS text extractor
---

## S204 — 2026-03-28 — TextExtractor Protocol + TimeBasedSplit CV

**Tests:** 1592 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/extractor_base.py`: `TextExtractor` Protocol + `BaseExtractor` base class.
  `load_into(registry)` convenience method — skips duplicate rule IDs.
- `src/research/cv_splitter.py`: `TimeBasedSplit` — `is_train/is_test/split()`,
  validates no look-ahead, parameters match OB-3 OSF draft (train≤2009, test≥2010).

### Next session
S205 — corpus audit script + BPHS new rule encoding (30 rules)
---

## S205 — 2026-03-28 — CorpusAudit + 31 BPHS Extended Rules

**Tests:** 1602 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/corpus_audit.py`: `CorpusAudit` — run()/text_report() for completeness
  checking (total, implemented, unimplemented, by school/category/source).
- `src/corpus/bphs_extended.py`: 31 new BPHS rule encodings (B001-B031) covering
  lagna-lord placement, 9th/10th yoga, vargottama, exaltation/debilitation,
  aspects (Jupiter/Saturn/Mars), yogakaraka, argala, transits, upachaya.
  All `implemented=False` — Phase 1 (S216-S250) encoding targets.

### Next session
S206 — Phaladeepika rules + Brihat Jataka rules (30 rules each)
---

## S206 — 2026-03-28 — Phaladeepika + Brihat Jataka Rule Encoding

**Tests:** 1610 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/phaladeepika_rules.py`: 21 rules (PH001-PH021) — planetary states,
  Kartari, house judgment, Graha Yuddha, dasha activation, Dig Bala, Paksha Bala.
- `src/corpus/brihat_jataka_rules.py`: 26 rules (BJ001-BJ026) — exaltation degrees,
  natural benefic/malefic, house significations (H1-H12), aspects, Moon yogas.
- **Corpus milestone:** 23 + 31 + 21 + 26 = **101 rules** — exceeds 100.

### Next session
S207 — Uttara Kalamrita + Jataka Parijata rules (30 rules)
---

## S207 — 2026-03-28 — Uttara Kalamrita + Jataka Parijata Rule Encoding

**Tests:** 1618 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/uttara_kalamrita_rules.py`: 17 rules (UK001-UK017) — Arudha Lagna,
  special lagnas (Hora, Ghati), Mahapurusha yogas, dasha fructification.
- `src/corpus/jataka_parijata_rules.py`: 17 rules (JP001-JP017) — Raja Yoga,
  Dhana Yoga, Viparita Raja, Gajakesari, Chara Karakas, Chandra-Mangala.
- **Corpus: 135 rules across 6 texts** (R01-R23 + BPHS + Phala + BJ + UK + JP).

### Next session
S208 — BirthRecord + Sarwarthachintamani + combined corpus loader
---

## S208 — 2026-03-28 — BirthRecord + CombinedCorpus

**Tests:** 1629 passing, 3 skipped, 0 lint errors

### What was built
- `src/corpus/birth_record.py`: `BirthRecord` ML data schema — record_id,
  birth date/time, lat/lon, data_source, Rodden rating, confirmed_events.
- `src/corpus/combined_corpus.py`: `COMBINED_CORPUS` singleton — loads all 6
  text registries (135+ rules) into one searchable CorpusRegistry.
  `build_corpus()` for fresh rebuild.

### Next session
S209 — corpus pipeline integration tests
