# MEMORY.md — LagnaMaster Session State
> **⚠️ MANDATORY: Update this file at the END of every session without fail.**
> Ground truth = git commits + update_docs_s*.py scripts, NOT the GitHub UI (known caching issue).

---

## ⚠️ Git Caching Warning

The GitHub web interface shows stale data (Sessions 1–10, 222 tests). This is a known caching issue.
**Always verify via `git log --oneline -5 && git status` — never trust the GitHub UI.**

The `update_docs_s188.py` in the repo root is the canonical documentation-sync artifact.
When in doubt, read that file to reconstruct state.

---

## Actual Current State (Sessions 1–228 complete — March 2026)

### Repository
- **Repo:** `github.com/agniinvestor/LagnaMaster`
- **Engine version:** `v3.0.0`
- **Python:** `3.14`
- **Ephemeris:** pyswisseph **JPL DE431** real files (`sepl_18.se1` + `semo_18.se1`) — Moshier fallback **retired**
- **Historical charts (pre-1800):** use `seplm_18.se1` + `semom_18.se1`

### Test Status
- **1777 passing, 3 skipped, 0 lint errors, CI green**
- The 3 skipped tests require a live `PG_DSN` (PostgreSQL). They pass when a Postgres instance is wired.
- 200+ ADB fixture charts covering all 12 Lagnas

### Session Progress
- **Sessions 1–10:** Pilot build — 12 calculation modules, 222 tests, Docker, Streamlit UI
- **Sessions 11–160:** Classical depth — all major calculation modules, 1000+ tests
- **Sessions 161–162:** Wiring fixes — Topocentric Moon, functional dignity in R02/R09
- **Sessions 163–186:** Scoring depth, school-mixing fix, regression snapshot
- **Sessions 187–188:** Final wiring gaps + XIX output API + Postgres routing + Swiss Ephemeris upgrade
- **Sessions 189–191:** Phase 0 bootstrap — Kala Bala verification, C-18 stress fixtures, VedAstro install, Protocol stubs, ruff G17 rule
- **Session 192:** Protocol adapters — ScoringEngineAdapter, VimshottariDasaAdapter, NullFeedbackService, NullMLService
- **Session 193:** HouseScore distribution dataclass — `house_score.py`, `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests
- **Session 194:** Conditional weight functions W(planet, house, lagna, functional_role) — `conditional_weights.py`, G06 g06_compliant flag; 1503 tests
- **Session 195:** Feature decomp infrastructure — `feature_decomp.py`, 4 extractors, 48 features; 1517 tests
- **Session 196:** +4 feature extractors (kartari, combust, retrograde, bhavesh_house_type); 1525 tests
- **Session 197:** +3 feature extractors (benefic_net_score, malefic_net_score, karak_score); 1530 tests
- **Session 198:** +2 extractors (pushkara_nav, war_loser); 156 features (≥150 ✅); 1535 tests
- **Session 199:** feature contract tests (10 tests, G22 gate); 1545 tests
- **Session 200:** ChartScoresV3 feature_vector field; ROADMAP S195–S200 ✅; 1550 tests
- **Session 201:** OSF schema (HypothesisSpec, CVStrategy, OSFRegistration) + OB-3 draft; 1558 tests
- **Session 202:** RuleRecord + CorpusRegistry corpus infrastructure; 1570 tests
- **Session 203:** ADB license + R01-R23 corpus encoding (EXISTING_RULES_REGISTRY); 1582 tests
- **Session 204:** TextExtractor Protocol + TimeBasedSplit CV splitter; 1592 tests
- **Session 205:** CorpusAudit + 31 BPHS extended rules (B001-B031); 1602 tests
- **Session 206:** Phaladeepika (21) + Brihat Jataka (26) rules; 101 total corpus rules; 1610 tests
- **Session 207:** Uttara Kalamrita (17) + Jataka Parijata (17); 135 total corpus rules; 1618 tests
- **Session 208:** BirthRecord + COMBINED_CORPUS (135+ rules, 6 texts); 1629 tests
- **Session 209:** Corpus pipeline integration tests (9 tests); 1638 tests
- **Session 210:** Corpus checkpoint; ROADMAP S201-S210 ✅; 135 rules across 6 texts
- **Session 211:** pgvector + TimescaleDB + MLflow + family schema; 1651 tests
- **Session 212:** KP ayanamsha enforcement (G06 🟡); compute_kp_chart(); 1660 tests
- **Sessions 213–215:** Protocol verification + CI observability + Phase 0 checkpoint; src/ci/ package; 1722 tests
- **Sessions 216–228:** Phase 1 Batch 1 — 299 new BPHS rules encoded (lords-in-houses 144, yogas 75, dignities/aspects/dasha/special-lagnas 80); corpus 135→434 rules; 1777 tests
- **Next session:** S229

---

## Session Startup Checklist (Run BEFORE Every Session)

```bash
# Step 1: Verify actual state — ignore GitHub UI
cd ~/LagnaMaster && git log --oneline -5 && git status

# Step 2: Lint check (must be 0)
.venv/bin/ruff check src/ tests/ tools/ 2>&1 | grep -c 'error'

# Step 3: Test count (must match or exceed 1338)
PYTHONPATH=. .venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3

# Step 4: Read docs/MEMORY.md — check "Next Session"
# Step 5: Read docs/CHANGELOG.md — last 30 lines
# Step 6: Read session entry in docs/ROADMAP.md
# Step 7: Check docs/GUARDRAILS.md for applicable guardrails
# Step 8: If running empirical analysis → verify OSF timestamp first (G22)
```

---

## Next Session: S189

### Immediate Priority Queue

| Priority | Item | Effort |
|----------|------|--------|
| 🟠 HIGH | C-18: 8 diverse stress-test fixtures (Neecha Bhanga, Graha Yuddha, nakshatra cusp, Parivartana, female, high-lat >55°N, year-boundary, BC date) | 1 day |
| 🟠 HIGH | Verify Shadbala Kala Bala all 8 sub-components complete | 2 hr |
| 🟠 HIGH | PostgreSQL live test (PG_DSN, run the 3 skipped tests) | 2 hr |
| 🟡 MED | Confidence model surfaced in Streamlit UI | 2 hr |
| 🟡 MED | Nehru Capricorn Lagna skip — investigate root cause | 1 hr |
| 🟡 MED | BC date charts: `seplm_18.se1` + `semom_18.se1` in `ephe/` | 30 min |
| 🔵 FUTURE | OB-3: Empirical calibration ML pipeline (500+ charts) | weeks |
| 🔵 FUTURE | Mundane astrology consumer pipeline | 3–4 days |

---

## All Wiring Gaps — Status (as of S188)

All critical wiring gaps are **CLOSED**. No outstanding gaps.

| Gap | Closed In | How Fixed |
|-----|-----------|-----------|
| Topocentric Moon (`FLG_TOPOCTR`) | S161 | `swe.set_topo()` + `SEFLG_TOPOCTR` in `ephemeris.py` |
| Functional dignity in R02/R09 | S162 | `compute_functional_classifications(lagna_si)` replacing natural classification |
| Dasha scoring wired to `score_chart_v3` | S187 | Real implementation replacing stub; mutates `axes.d1.scores` when `on_date` supplied |
| War loser penalty in `_score_one_house` | S187 | `getattr(chart, 'planetary_war_losers', set())`; −1.5 penalty (Saravali Ch.4 v.18-22) |
| `strict_school` param on `score_axis`/`score_all_axes` | S187 | Wire live; `school_score_adjustment()` called in strict mode |
| XIX SVG/PDF/guidance/confidence API | S188 | 5 new endpoints in `src/api/main.py` |
| Postgres routing (`db_pg` replaces `db`) | S188 | `db_pg` with automatic SQLite fallback when `PG_DSN` unset |
| Swiss Ephemeris real files | S188 | `sepl_18.se1` + `semo_18.se1` from `github.com/aloistr/swisseph` |

---

## Bug Status (all resolved as of S188)

| ID | Status |
|----|--------|
| P-1 (midnight falsy) | ✅ FIXED S1-S2: `if hour is None` in `ephemeris.py` |
| P-4 (ayanamsha silent fail) | ✅ FIXED S1-S2: raises `ValueError` immediately |
| N-1 (Taurus=4yr) | ✅ FIXED S1-S2: corrected to 7yr in `narayana_dasa.py` |
| S-2 (J14=3851) | ✅ FIXED S8: `min(60, mean_motion/|speed|×60)` |
| E-1 | ✅ NOT PRESENT in Python — `swe.julday` handles it; regression test added |
| A-2 | ✅ NOT PRESENT in Python — `speed < 0` used directly; regression test added |

---

## Active Scoring Invariants (live as of S188)

| # | Invariant | Source |
|---|-----------|--------|
| 35 | War loser bhavesh = −1.5 penalty to house score (permanent) | Saravali Ch.4 v.18-22 |
| 36 | `strict_school=True` deducts Jaimini contributions in Parashari mode | Architecture decision |

Note: R17/R18 currently score 0.0 — so Invariant #36 has no numeric effect yet.

---

## Regression Standard

The regression suite is the **200+ ADB diverse fixture charts** (all 12 Lagnas,
Sections A–H of diverse_chart_fixtures.py). The pre-push hook runs the full
1338+ test suite. This is the quality gate for every session.

**India 1947 position verification** is NOT the standard regression gate.
It is only relevant in sessions where `ephemeris.py`, `varga.py`,
`narayana_dasa.py`, `nakshatra.py`, or `dignity.py` appear in the READ LIST
(i.e., sessions that touch the calculation substrate). The `start_session.py`
brief will call this out explicitly when relevant.

When India 1947 position verification IS needed:
```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,           # midnight IST — tests P-1 fix
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5, "ayanamsha": "lahiri",
}
# Lagna: 7.7286° Taurus (tolerance ±0.05°)
# Sun:   27.989° Cancer
# Moon:  3.9835° Cancer → Pushya nakshatra (index 7) → Saturn birth dasha (19yr)
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer
```

---

## Key Metrics (Post-S188)

| Metric | Current | 2030 Target |
|--------|---------|------------|
| Tests passing | **1503** (3 skipped) | 8,000+ |
| Lint errors | **0** | 0 |
| Classical rules | 23 (R01–R23) | 3,000+ |
| Ephemeris | **DE431 real files** | DE431 maintained |
| ADB fixtures | **200+** (all 12 Lagnas) | 5,000+ |
| API endpoints | **10** (5 new in S188) | — |
| Brier score | Pre-baseline | ≤0.10 |
| Signal isolation | Pre-baseline | +0.22 |

---

## Session End Protocol (MANDATORY)

```bash
# 1. Full test suite
PYTHONPATH=. .venv/bin/pytest tests/ -q 2>&1 | tail -5

# 2. Lint
.venv/bin/ruff check src/ tests/ tools/

# 3. Commit
git add -A && git commit -m "feat(S[N]): [description]"
git push

# 4. Run documentation sync:
#    .venv/bin/python3 update_docs_s[N].py
#    git add docs/ MEMORY.md PLAN.md CHANGELOG.md README.md
#    git commit -m "docs(S[N]): sync documentation"

# 5. Update docs/MEMORY.md — change "Next Session", update metrics
# 6. Append to docs/CHANGELOG.md — use SESSION_TEMPLATE.md format
# 7. Mark fixed bugs in docs/BUGS.md
# 8. Update docs/KPIS.md if any metric moved
```
