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
