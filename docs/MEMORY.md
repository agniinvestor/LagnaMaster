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

## Actual Current State (Sessions 1–189 complete — March 2026)

### Repository
- **Repo:** `github.com/agniinvestor/LagnaMaster`
- **Engine version:** `v3.0.0`
- **Python:** `3.14`
- **Ephemeris:** pyswisseph **JPL DE431** real files (`sepl_18.se1` + `semo_18.se1`) — Moshier fallback **retired**
- **Historical charts (pre-1800):** use `seplm_18.se1` + `semom_18.se1`

### Test Status
- **1338 passing, 3 skipped, 0 lint errors, CI green**
- The 3 skipped tests require a live `PG_DSN` (PostgreSQL). They pass when a Postgres instance is wired.
- 200+ ADB fixture charts covering all 12 Lagnas

### Session Progress
- **Sessions 1–10:** Pilot build — 12 calculation modules, 222 tests, Docker, Streamlit UI
- **Sessions 11–160:** Classical depth — all major calculation modules, 1000+ tests
- **Sessions 161–162:** Wiring fixes — Topocentric Moon, functional dignity in R02/R09
- **Sessions 163–186:** Scoring depth, school-mixing fix, regression snapshot
- **Sessions 187–188:** Final wiring gaps + XIX output API + Postgres routing + Swiss Ephemeris upgrade
- **Session 189:** ADB XML importer, diverse fixtures (B-H), CI guard, mundane endpoint, semom_18.se1
- **Next session:** S190

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

**Before any session that builds or modifies a calculation module, also read:**
`docs/PREDICTION_PIPELINE.md` — specifically "The Three Convergence Layers" section.
Ask: which convergence layer does this module belong to, and what consumes its output?
A module not wired to its convergence layer's downstream consumer produces no
improvement to prediction quality regardless of how correct it is in isolation.

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

## India 1947 Reference Chart (Frozen Regression Fixture)

```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,           # midnight IST — tests P-1 fix
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}
# Lagna: 7.7286° Taurus (tolerance ±0.05°)
# Sun:   27.989° Cancer
# Moon:  3.9835° Cancer → Pushya nakshatra (index 7) → Saturn birth dasha (19yr)
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer
# Narayana Dasha: Taurus (7yr) → Aries (6yr) → Pisces (3yr)...
```

---

## Key Metrics (Post-S188)

| Metric | Current | 2030 Target |
|--------|---------|------------|
| Tests passing | **1338** (3 skipped) | 8,000+ |
| Lint errors | **0** | 0 |
| Classical rules | 23 (R01–R23) | 3,000+ |
| Ephemeris | **DE431 real files** | DE431 maintained |
| ADB fixtures | **200+** (all 12 Lagnas) | 5,000+ |
| API endpoints | **10** (5 new in S188) | — |
| Brier score | Pre-baseline | ≤0.10 |
| Signal isolation | Pre-baseline | +0.22 |

---

## Session End Protocol (AUTOMATED)

```bash
# NEW AUTOMATED LOOP — replaces the manual checklist below
.venv/bin/python3 tools/start_session.py   # run BEFORE opening Claude
# [paste brief to Claude — Claude writes tests + impl + update_docs_s[N].py]
.venv/bin/python3 update_docs_s[N].py      # run AFTER Claude session
git push                                    # pre-push hook: tests + ruff + docs
```

The pre-push hook is the single quality gate. If it passes, the session is done.

---

**Manual equivalent (if automation unavailable):**


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
