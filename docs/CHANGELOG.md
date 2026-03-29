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
---

## S209 — 2026-03-28 — Corpus Pipeline Integration Tests

**Tests:** 1638 passing, 3 skipped, 0 lint errors

### What was built
- `tests/test_s209_corpus_pipeline_integration.py`: 9 integration tests covering
  the full pipeline: OSF schema → CV split → corpus load → audit → extractor
  → BirthRecord → ADB license check → G22 gate.

### Next session
S210 — corpus checkpoint: ROADMAP S201-S210 ✅, CLASSICAL_CORPUS.md update
---

## S210 — 2026-03-28 — Corpus Checkpoint (S201–S210 complete)

**Tests:** 1638 passing, 3 skipped, 0 lint errors

### What was built
- `CLASSICAL_CORPUS.md` updated: 135-rule corpus status, OSF filing status,
  pipeline infrastructure summary.
- `ROADMAP.md`: S201–S210 marked ✅.

### Phase 0 corpus pipeline summary (S201–S210)
| Session | Built |
|---------|-------|
| S201 | OSF pre-registration schema + OB-3 draft filing |
| S202 | RuleRecord + CorpusRegistry infrastructure |
| S203 | ADB license compliance + R01-R23 encoded |
| S204 | TextExtractor Protocol + TimeBasedSplit CV |
| S205 | CorpusAudit + 31 BPHS rules |
| S206 | Phaladeepika (21) + Brihat Jataka (26) rules; 101 total |
| S207 | Uttara Kalamrita (17) + Jataka Parijata (17); 135 total |
| S208 | BirthRecord + COMBINED_CORPUS singleton |
| S209 | Pipeline integration tests |
| S210 | Corpus checkpoint + docs |

### Next session
S211 — Redis + pgvector + TimescaleDB + MLflow + family schema
---

## S211 — 2026-03-28 — ML Infrastructure Schema (pgvector + TimescaleDB + MLflow + Family)

**Tests:** 1651 passing, 3 skipped, 0 lint errors

### What was built
- `src/db_vector.py`: pgvector schema — `chart_embeddings` table for 156-dim feature
  vectors, IVFFlat cosine index, `feature_schema_versions`.
- `src/db_timescale.py`: TimescaleDB schema — `dasha_periods`, `outcome_confirmations`
  (G04: user_prior_prob_pre field), `transit_activations` hypertables.
- `src/ml/mlflow_config.py`: MLflow experiment registry — OB-3 / OB-3-SHAP /
  EXPLORATORY configs with G22 guardrail notes.
- `src/db_family.py`: `FamilyRelation` enum + family_groups / family_members /
  family_relations / family_patterns schema (G03/G16 compliance notes).

### Next session
S212 — Ayanamsha selection + KP school fix (G06 compliance)
---

## S212 — 2026-03-28 — Ayanamsha Selection + KP G06 Compliance

**Tests:** 1660 passing, 3 skipped, 0 lint errors

### What was built
- `src/calculations/kp_ayanamsha.py`: `KP_AYANAMSHA` constant, `get_kp_ayanamsha()`,
  `validate_kp_chart()` (returns g06_compliant bool + warning), `compute_kp_chart()`
  wrapper that defaults to krishnamurti ayanamsha.
- `GUARDRAILS.md`: G06 updated to 🟡 — enforcement mechanism in place;
  existing charts not retroactively fixed (would require data migration).

### G06 status
New KP analysis using `compute_kp_chart()` is compliant. Existing charts stored with Lahiri ayanamsha must be flagged separately (Phase 1 data migration).

### Next session
S213 — Protocol verification + CI observability
---

## S213–S215 — 2026-03-28 — Protocol Verification + CI Observability + Phase 0 Checkpoint

**Tests:** 1722 passing, 3 skipped, 0 lint errors

### What was built
- `src/ci/protocol_compliance.py`: `check_all_protocols()` — runtime isinstance checks
  for all four Protocol adapters (ClassicalEngine, DashaEngine, FeedbackService, MLService).
- `src/ci/health_check.py`: `CIHealthReport` dataclass + `run_health_check()` — structured
  CI observability with corpus count, G06/G17 guardrail status, Phase 0 module presence.
- `src/ci/phase0_checkpoint.py`: `Phase0Checkpoint` + `run_phase0_audit()` — comprehensive
  audit of all 25 Phase 0 sessions (S191–S215); serves as Phase 0 gate.

### Phase 0 gate status
All 25 Phase 0 sessions (S191–S215) verified complete. `run_phase0_audit()` returns
25/25 sessions complete. CI health check passes. Phase 1 (S216) can begin.

### Next session
S216 — BPHS all 97 chapters AI-assisted encoding (Phase 1 start)
---

## S216–S228 — 2026-03-28 — Phase 1 Classical Knowledge Foundation (Batch 1)

**Tests:** 1777 passing, 3 skipped, 0 lint errors

### What was built
**Lord-in-Houses (144 rules, S216-S221):** Complete 12×12 matrix of house lord positions encoded from BPHS Ch.24-35:
- `bphs_lords_h1_h2.py`: H1L001-H1L012 + H2L001-H2L012 (lagna + 2nd lord)
- `bphs_lords_h3_h4.py`: H3L/H4L series (3rd + 4th lord)
- `bphs_lords_h5_h6.py`: H5L/H6L series (5th + 6th lord) — includes viparita yoga
- `bphs_lords_h7_h8.py`: H7L/H8L series (7th + 8th lord)
- `bphs_lords_h9_h10.py`: H9L/H10L series (9th + 10th lord) — dharma karma adhipati
- `bphs_lords_h11_h12.py`: H11L/H12L series (11th + 12th lord)

**Yoga encoding (S222-S224):**
- `bphs_yogas_basic.py`: 25 rules — Pancha Mahapurusha, Gajakesari, Neecha Bhanga, Viparita, Parivartana, sun/moon-based yogas
- `bphs_raja_yoga.py`: 25 rules — kendra-trikona combinations, yogakaraka rules per lagna, cancellation rules
- `bphs_dhana_yoga.py`: 25 rules — wealth yogas, daridra, vasumati, parivartana dhana

**Supporting rules (S225-S228):**
- `bphs_dignities_ext.py`: 20 rules — exaltation, moolatrikona, own sign, vargottama, digbala, combustion, graha yuddha
- `bphs_aspects.py`: 20 rules — special aspects (Jupiter/Saturn/Mars), mangal dosha, argala
- `bphs_dasha_results.py`: 20 rules — all 9 planet dasha themes, lordship modification
- `bphs_special_lagnas.py`: 20 rules — Chandra/Surya/Arudha/Upapada/Hora/Ghati lagnas

**Total corpus: 434 rules** (from 135 at end of Phase 0)

### Next session
S229 — Continue Phase 1: BPHS graha in rashis + KP sublord rules
---

## S229 — 2026-03-28 — BPHS Graha in Rashis Part 1

**Tests:** 1788 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_rashis_p1.py`: 24 rules — Sun in 12 rashis (SUR001-SUR012) + Moon in 12 rashis (MOR001-MOR012). Encodes BPHS Ch.17-18 graha-rashi phala. Exaltation/own/debilitation tags on key placements.

**Corpus total: 458 rules**

### Next session
S230 — BPHS graha in rashis part 2 (Mars + Mercury)
---

## S230 — 2026-03-28 — BPHS Graha in Rashis Part 2

**Tests:** 1799 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_rashis_p2.py`: 24 rules — Mars in 12 rashis (MAR001-MAR012) + Mercury in 12 rashis (BUR001-BUR012). BPHS Ch.19-20. Mars own-sign Aries+Scorpio, exaltation Capricorn, debilitation Cancer. Mercury own-sign+exaltation Virgo, moolatrikona Gemini, debilitation Sagittarius.

**Corpus total: 482 rules**

### Next session
S231 — BPHS graha in rashis part 3 (Jupiter + Venus)
---

## S231 — 2026-03-28 — BPHS Graha in Rashis Part 3

**Tests:** 1811 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_rashis_p3.py`: 24 rules — Jupiter in 12 rashis (JUR001-JUR012) + Venus in 12 rashis (VER001-VER012). BPHS Ch.21-22. Jupiter: own Sagittarius+Pisces, exalt Cancer, neecha Capricorn. Venus: own Taurus+Libra, exalt Pisces, neecha Virgo.

**Corpus total: 506 rules**

### Next session
S232 — BPHS graha in rashis part 4 (Saturn + Rahu + Ketu)
---

## S232 — 2026-03-28 — BPHS Graha in Rashis Part 4

**Tests:** 1823 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_rashis_p4.py`: 36 rules — Saturn in 12 rashis (SAR001-SAR012) + Rahu in 12 rashis (RHR001-RHR012) + Ketu in 12 rashis (KTR001-KTR012). BPHS Ch.23, Ch.45-46. Saturn: own Capricorn+Aquarius, exalt Libra, neecha Aries. Rahu/Ketu: exaltation/debilitation per traditional commentary.

**Corpus total: 542 rules** (108 graha-in-rashi rules complete for all 9 grahas)

### Next session
S233 — KP sublord rules + nakshatra lords
---

## S233 — 2026-03-28 — KP Sublord System Rules

**Tests:** 1833 passing, 3 skipped, 0 lint errors

### What was built
- `kp_sublord_rules.py`: 30 rules (KPS001-KPS030) — KP Sublord system from K.S. Krishnamurti's Reader Vol.1-6. Covers: nakshatra sublord structure (6), marriage (4), finance (4), career (4), health (4), education/travel/spirituality (4), horary/prashna (4).

**Corpus total: 572 rules**

### Next session
S234 — BPHS nakshatra-based rules (nakshatras 1-9)
---

## S234 — 2026-03-28 — BPHS Nakshatra Rules Part 1

**Tests:** 1843 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_nakshatra_rules_p1.py`: 28 rules (NAK001-NAK028) — Nakshatras 1-14 (Ashwini through Chitra): nature, deity, symbol, keywords (14 rules) + Moon in nakshatras 1-14 (14 rules). BPHS Ch.3-4.

**Corpus total: 600 rules**

### Next session
S235 — BPHS nakshatra rules part 2 (nakshatras 15-27)
---

## S235 — 2026-03-28 — BPHS Nakshatra Rules Part 2

**Tests:** 1851 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_nakshatra_rules_p2.py`: 26 rules (NAK029-NAK054) — Nakshatras 15-27 (Swati through Revati): characteristics (13 rules) + Moon in nakshatras 15-27 (13 rules). BPHS Ch.5. Completes full 27-nakshatra catalog (54 characteristic rules + 54 Moon rules).

**Corpus total: 626 rules**

### Next session
S236 — BPHS Bhava Karakas (house significators)
---

## S236 — 2026-03-28 — BPHS Bhava Karakas

**Tests:** 1860 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_bhava_karakas.py`: 30 rules (BHK001-BHK030) — Naisargika karakas for all 12 houses (12 rules), Jaimini Chara Karakas AK/AmK/BK/MK/PK/GK/DK (8 rules), special karaka rules including Karaka-Bhava-Nashta, gender-based spouse karakas, dasha activation (10 rules).

**Corpus total: 656 rules**

### Next session
S237 — Varga chart rules (D9 Navamsha + D10 Dashamsha)
---

## S237 — 2026-03-28 — BPHS Varga (Divisional Chart) Rules

**Tests:** 1869 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_varga_rules.py`: 30 rules (VAR001-VAR030) — D9 Navamsha (10 rules): vargottama, karakamsha, timing, pushkara; D10 Dashamsha (8 rules): lagna, Sun/Saturn, career timing; Other vargas D4/D7/D12/D16/D20/D24/D30/D60/D5 (12 rules): specific house significations + panchamsha/saptavargaja bala.

**Corpus total: 686 rules**

### Next session
S238 — Brihat Jataka: planetary natures and results
---

## S238 — 2026-03-28 — Brihat Jataka Extended Rules

**Tests:** 1877 passing, 3 skipped, 0 lint errors

### What was built
- `brihat_jataka_ext.py`: 30 rules (BJE001-BJE030) — Varahamihira's Brihat Jataka (6th cent CE): planetary natures for all 9 grahas (9 rules), hora/drekkana/navamsha systems (3 rules), aspects (3 rules), raja/dhana yogas (3 rules), life events (5 rules), dasha timing (3 rules).

**Corpus total: 716 rules**

### Next session
S239 — Phala Deepika extended rules
---

## S239 — 2026-03-28 — Phala Deepika Extended Rules

**Tests:** 1886 passing, 3 skipped, 0 lint errors

### What was built
- `phala_deepika_ext.py`: 30 rules (PDE001-PDE030) — Mantreswara's Phala Deepika (13th cent CE): planets in 1st/7th/10th/4th houses (12), Pancha Mahapurusha yoga details (5), special yogas (5), health/disease (4), yoga cancellation/timing/Graha Yuddha (4).

**Corpus total: 746 rules**

### Next session
S240 — Uttara Kalamrita extended rules
---

## S240 — 2026-03-28 — Uttara Kalamrita Extended Rules

**Tests:** 1895 passing, 3 skipped, 0 lint errors

### What was built
- `uttara_kalamrita_ext.py`: 30 rules (UKE001-UKE030) — Kalidasa's Uttara Kalamrita (17th cent CE): all 12 house extended significations (12), all 9 planetary gemstones/directions/deities (9), bhavat bhavam, kartari yogas, combustion degrees, retrograde strength, temporal malefic/benefic classification (9).

**Corpus total: 776 rules**

### Next session
S241 — Jataka Parijata extended rules
---

## S241 — 2026-03-28 — Jataka Parijata Extended Rules

**Tests:** 1904 passing, 3 skipped, 0 lint errors

### What was built
- `jataka_parijata_ext.py`: 30 rules (JPE001-JPE030) — Vaidyanatha Dikshita's Jataka Parijata (14th cent CE): all 12 lagna analyses (10 rules, grouping last 3), Parivartana yoga classifications, Neecha Bhanga Raja Yoga, Vesi/Vasi/Obhayachari/Chandra Mangala/Shakata/Kemadruma yogas, all 9 Vimshottari Mahadasha results.

**Corpus total: 806 rules — 800+ MILESTONE ACHIEVED!**

### Next session
S242 — Sarvartha Chintamani / transit rules
---

## S242 — 2026-03-28 — Classical Transit (Gochara) Rules

**Tests:** 1914 passing, 3 skipped, 0 lint errors

### What was built
- `transit_rules.py`: 30 rules (TRN001-TRN030) — Classical Gochara (transit) rules from BPHS Ch.90 (parashari) and Sarvartha Chintamani Ch.10 (sarvartha): fundamental transit-from-Moon principle, Vedha obstruction, Ashtakavarga bindus, per-planet transit results (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu), Sade Sati (7.5 years), Ashtama Shani, double transit (Jupiter+Saturn), triple trigger, retrograde three-pass, Tajika.

**Corpus total: 836 rules**

### Next session
S243 — Ashtakavarga rules / Jaimini Sutras
---

## S243 — 2026-03-28 — Ashtakavarga Rules

**Tests:** 1925 passing, 3 skipped, 0 lint errors

### What was built
- `ashtakavarga_rules.py`: 30 rules (AST001-AST030) — Classical Ashtakavarga system from BPHS Ch.66-76 (parashari), Brihat Jataka Ch.19 (varahamihira), Sarvartha Chintamani Ch.10 (sarvartha): Prasthara BAV structure, Sarvashtakavarga, Trikona + Ekadhipatya Shodhana, all 7 planet BAVs (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn), Kakshya timing divisions, Pinda/Yoga/Rashi Saham, transit assessment by bindus (0-8 scale), longevity, career/wealth/travel/compatibility applications.

**Corpus total: 866 rules**

### Next session
S244 — Jaimini Sutras / Upagraha rules
---

## S244 — 2026-03-28 — Jaimini Sutras + Upagraha Rules

**Tests:** 1936 passing, 3 skipped, 0 lint errors

### What was built
- `jaimini_sutras_rules.py`: 30 rules (JMS001-JMS030) — Jaimini Sutras (Maharishi Jaimini) + BPHS Ch.24: Chara Karaka system (AK/AmK/BK/MK/PK/GK/DK by degree), Karakamsha lagna, Rashi Drishti sign aspects, Argala intervention, Arudha/Pada system (AL/UL/GL/HL), Chara Dasha structure and interpretation, Sthira Dasha periods, Jaimini yogas (Raja/Dhana), longevity assessment, Upagrahas (Gulika/Mandi/Dhuma/Vyatipata).

**Corpus total: 896 rules**

### Next session
S245 — Shadbala rules
---

## S245 — 2026-03-28 — Shadbala Rules

**Tests:** 1947 passing, 3 skipped, 0 lint errors

### What was built
- `shadbala_rules.py`: 30 rules (SDB001-SDB030) — Classical Shadbala 6-fold strength system from BPHS Ch.27-38 (parashari), Brihat Jataka Ch.1 (varahamihira), Sarvartha Chintamani Ch.2 (sarvartha): Sthana Bala (Uchcha/Sapta-Vargaja/Ojayugma/Kendradi/Drekkana), Dig Bala (directional), Kala Bala (Paksha/Tribhaga/Vara/Ayana/Yuddha), Chesta Bala (retrograde=60), Naisargika Bala (fixed values), Drik Bala (aspectual), Ishta/Kashta Phala, Vimshopaka (5/7/10-Varga), minimum thresholds, Dasha applications.

**Corpus total: 926 rules**

### Next session
S246 — Dasha systems (Vimshotari, Ashtottari, Yogini)
---

## S246 — 2026-03-28 — Dasha Systems Rules

**Tests:** 1958 passing, 3 skipped, 0 lint errors

### What was built
- `dasha_systems_rules.py`: 30 rules (DSY001-DSY030) — Classical Dasha systems from BPHS Ch.46-64 (parashari), Uttara Kalamrita Ch.4 (kalidasa), Sarvartha Chintamani Ch.8 (sarvartha), Jaimini Sutras (jaimini): Vimshottari extended (birth balance/Antardasha/results), Ashtottari (108yr), Yogini (36yr), Kalachakra (100yr), Shodashottari (116yr), Dwisaptati (72yr), conditional dasha selection, Narayana/Padakrama Jaimini dashas, Sookshma/Prana micro-dashas, transit confirmation, Maraka, yogakaraka dasha, Sun/Jupiter/Saturn/Rahu/Ketu Mahadasha results.

**Corpus total: 956 rules**

### Next session
S247 — Yoga extended (Pancha Mahapurusha, Dhana, Raja yogas expansion)
---

## S247 — 2026-03-28 — Extended Yoga Rules

**Tests:** 1969 passing, 3 skipped, 0 lint errors

### What was built
- `yoga_extended_rules.py`: 30 rules (YGE001-YGE030) — Extended yoga rules from BPHS Ch.35-45 (parashari), Phala Deepika Ch.6 (mantreswara), Brihat Jataka Ch.12 (varahamihira): All 5 Pancha Mahapurusha yogas (Ruchaka/Bhadra/Hamsa/Malavya/Shasha), Nabhasa yogas (Rajju/Musala/Nala/Mala/Sarpa/Shula/Yava/Kamala), Viparita Raja Yoga, Mahabhagya, Parijata, Kesari, Amala, Lakshmi, Saraswati, Kahala, Chandra-Mangala Dhana yogas, Pravrajya/Moksha/Sanyasa/Bandhana spiritual yogas, Anapha/Sunapha/Durudhara Moon yogas, Kartari Yoga.

**Corpus total: 986 rules**

### Next session
S248 — Lagna (Ascendant) extended rules
---

## S248 — 2026-03-28 — Lagna Extended Rules

**Tests:** 1979 passing, 3 skipped, 0 lint errors

### What was built
- `lagna_extended_rules.py`: 30 rules (LGE001-LGE030) — All 12 Lagna (Ascendant) characteristics from BPHS Ch.7-18 (parashari), Phala Deepika Ch.1 (mantreswara), Brihat Jataka Ch.1 (varahamihira): All 12 lagna personality/body/planet profiles, Yogakaraka by element group (fire/earth/air/water), Kendra Adhipati Dosha, Trikona Adhipati Shubha, Chandra Lagna, Surya Lagna, lagna strength indicators, lagna lord in 12 houses, planets in lagna, physical characteristics, Vargottama Lagna, 8th lord in lagna, multiple planets in lagna.

**Corpus total: 1016 rules — 1000+ MILESTONE ACHIEVED!**

### Next session
S249 — House significations extended (Bhava Phala)
---

## S249 — 2026-03-28 — Bhava Phala (House Results) Extended Rules

**Tests:** 1990 passing, 3 skipped, 0 lint errors

### What was built
- `bhava_phala_rules.py`: 30 rules (BPH001-BPH030) — Extended house results from BPHS Ch.11-22 (parashari), Uttara Kalamrita Ch.4 (kalidasa), Phala Deepika Ch.7 (mantreswara): All 12 bhava extended significations, Bhavat Bhavam principle, Upachaya houses (3/6/10/11), Dusthana houses (6/8/12), Trikona houses (1/5/9), Maraka principle (2nd/7th lords), house occupation effects, Parivartana between house lords, empty/vacant house rules, Bhava Chalita, health-body part correlations, specific house combinations.

**Corpus total: 1046 rules**

### Next session
S250 — Planets in houses extended (Graha Phala)
---

## S250 — 2026-03-28 — Graha Phala (Planets in Houses) Rules

**Tests:** 2001 passing, 3 skipped, 0 lint errors

### What was built
- `graha_phala_rules.py`: 30 rules (GPH001-GPH030) — Planet-in-house effects from BPHS Ch.23-31 (parashari), Phala Deepika Ch.3 (mantreswara), Brihat Jataka Ch.2 (varahamihira): Sun in all houses (Kendra/Trikona/Dusthana), Moon (waxing/waning effects), Mars (Mangal Dosha 1/4/7, Upachaya 3/6/11), Mercury (intellect/communication), Jupiter (wisdom/prosperity in all houses), Venus (beauty/happiness), Saturn (discipline/delay, excellent in Upachaya), Rahu/Ketu in houses, combust planets (Asta), exalted in dusthana, debilitated in Kendra, Swakshetra.

**Corpus total: 1076 rules**

### Next session
S251 — Remedies and Upayas (classical astrological remedies)
---

## S251 — 2026-03-28 — BPHS Graha-Bhava Complete (Exhaustive Planet-in-House)

**Tests:** 2012 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_bhava_complete.py`: 108 rules (GBC001-GBC108) — Exhaustive one-rule-per-planet-per-house encoding from BPHS Ch.23-31: Sun in all 12 houses (GBC001-012), Moon (GBC013-024), Mars (GBC025-036), Mercury (GBC037-048), Jupiter (GBC049-060), Venus (GBC061-072), Saturn (GBC073-084), Rahu (GBC085-096), Ketu (GBC097-108). Each rule captures primary BPHS effects, house quality (Kendra/Trikona/Dusthana/Upachaya), health significations, relationship indicators, and career themes. New exhaustive approach: no arbitrary caps — full chapter coverage.

**Corpus total: 1184 rules**

### Next session
S252 — BPHS Yoga Exhaustive (all 500+ yoga combinations from Ch.35-45)
---

## S252 — 2026-03-28 — BPHS Yoga Exhaustive (150 rules)

**Tests:** 2028 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_yoga_exhaustive.py`: 150 rules (YEX001-YEX150) — Exhaustive encoding of BPHS Ch.35-56 yoga catalog: Pancha Mahapurusha (5), Nabhasa yogas — Ashraya/Dala/Sankhya (15+), Raja Yogas from kendra-trikona lords (11), Dhana Yogas (10), Neechabhanga Raja Yoga (8 cancellation conditions), Viparita Raja Yoga — Harsha/Sarala/Vimala (3), Parivartana yogas (12), Lunar yogas — Sunapha/Anapha/Durudhara/Kemadruma/Gaja-Kesari (10+), Solar yogas — Veshi/Voshi/Ubhayachari/Budha-Aditya (4), Named yogas — Saraswati/Lakshmi/Parijata/Mahabhagya/Adhi/Amala/Vasumati (15+), Sanyasa/Moksha/Pravrajya/Bandhana/Kala Sarpa (8), Dosha yogas — Mangal/Pitru/Matru/Putra/Vivaha (6), Graha Bala yogas — all 7 planets (8), Nabhasa patterns (10+).

**Corpus total: 1334 rules**

### Next session
S253 — BPHS Bhava Exhaustive (all 12 houses, deep significations)
---

## S253 — 2026-03-29 — BPHS Bhava Exhaustive (120 rules)

**Tests:** 2042 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_bhava_exhaustive.py`: 120 rules (BVX001-BVX120) — Exhaustive encoding of all 12 bhava significations from BPHS Ch.11-22: Each house primary significations + karakas, all 9 planets in each house, Marana Karaka Sthana placements, Dig Bala, Bhavat Bhavam principle, house anatomy/body mapping, longevity classification (Alpayu/Madhyayu/Purnayu), Maraka analysis, lagna lord in dusthanas, cross-house lord interactions.

**Corpus total: 1454 rules**

### Next session
S254 — BPHS Graha Characteristics Exhaustive (planet natures, elements, karakas)
---

## S254 — 2026-03-29 — BPHS Graha Characteristics (100 rules)

**Tests:** 2057 passing, 3 skipped, 0 lint errors

### What was built
- `bphs_graha_characteristics.py`: 100 rules (GCH001-GCH100) — Exhaustive encoding of all 9 planet natures/attributes from BPHS Ch.3-10: Nature/element/dosha/body for all 7 planets + Rahu/Ketu, full karakatva (significator roles), exaltation/debilitation/own signs, special aspects (Mars 4/8, Jupiter 5/9, Saturn 3/10), combustion degrees, Graha Yuddha (planetary war), rising types (Sheershodaya/Prishtodaya/Ubhayodaya), Vimshottari dasha periods + nakshatra sequence, Rashi modality/elements/gender, Nakshatra trikonas + ganas, temporal friendship rules, Saptavarga/Vargottama, retrograde/stationary states, medical astrology (8 planets), gems/metals/mantras for all 9 planets, planetary cabinet, objects, tastes, deities, maturation ages, seasonal/hourly strengths.

**Corpus total: 1554 rules**

### Next session
S255 — Brihat Jataka Exhaustive (all 25 chapters deep encoding)
---

## S255 — 2026-03-29 — Brihat Jataka Exhaustive (120 rules)

**Tests:** 2075 passing, 3 skipped, 0 lint errors

### What was built
- `brihat_jataka_exhaustive.py`: 120 rules (BJX001-BJX120) — Exhaustive encoding of all 25 chapters of Varahamihira's Brihat Jataka (6th century CE): Planet natures/colors/tastes, aspect rules (7th/3rd/10th/4th/8th/5th/9th), all 12 rashi characteristics, bhava significations in BJ system, Avastha planetary states (5 states + 9 avasthas), divisional charts D2/D3/D7/D9/D10/D12/D30, Pancha Mahapurusha/Raja/Dhana/Nabhasa/Pravrajya yogas, nakshatra characteristics (Ashwini to Revati + Abhijit), planets in signs/houses, birth analysis, physical traits, wealth rules, female horoscopy, Pindayu/Amsayu longevity, death indicators, dasha phala, transit rules (Sade Sati/Jupiter transit). All rules: school=varahamihira, source=BrihatJataka.

**Corpus total: 1674 rules**

### Next session
S256 — Uttara Kalamrita Exhaustive (all chapters deep encoding)
---

## S256 — 2026-03-29 — Uttara Kalamrita Exhaustive (150 rules)

**Tests:** 2098 passing, 3 skipped, 0 lint errors

### What was built
- `uttara_kalamrita_exhaustive.py`: 150 rules (UKX001-UKX150) — Exhaustive encoding of Kalidasa's Uttara Kalamrita (17th century CE): All 7 special lagnas (Hora/Ghati/Bhava/Sree/Pranapada/Indu/Yogi), Argala doctrine (primary/secondary/obstruction), all 12 Arudha Padas (A1-A12 including UL/Upapada), extended house significations (all 12 houses), planet karakatva for all 9 planets, Upagrahas (Dhuma/Vyatipata/Parivesha/Indrachapa/Gulika/Mrityu), dasha timing (exalted/debilitated/retrograde dashas), Karakamsha and Atmakaraka analysis, Chara Karakas (AK/AMK/BK/DK), yogas (Subhakartari/Papakartari/Adhi/Kemadruma/Shakata/Parivartana), medical astrology, wealth/poverty combinations, marriage/divorce indicators, moksha/Pravrajya yogas, Prashna (horary), transit rules, varga analysis. All rules: school=kalidasa, source=UttaraKalamrita.

**Corpus total: 1824 rules**

### Next session
S257 — Jataka Parijata Exhaustive (all chapters deep encoding)
