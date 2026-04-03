# BUGS.md — LagnaMaster Known Bugs & Status
> **Update this file whenever a bug is fixed or a new one is found.**
> Ground truth: `update_docs_s188.py` + `PLAN.md` from repository.

---

## ⚠️ Important: Excel vs Python Bug Distinction

Some bugs existed in the Excel v5 workbook but were **never present in the Python code** — they were caught before translation. Do not mark Python code as "having" these bugs.

---

## All Known Excel v5 Bugs — Status in Python Codebase

| ID | Severity | Excel Bug | Python Status |
|----|----------|-----------|---------------|
| **P-1** | CRITICAL | Midnight birth: `B6=0` treated as falsy in VBA/Python | ✅ **FIXED** (S1-S2): `if hour is None` check in `ephemeris.py`. Regression test in `test_calculations.py`. |
| **P-4** | CRITICAL | `natal_changes()`: variable `bd` undefined — ayanamsha fallback silent-fails | ✅ **FIXED** (S1-S2): Unknown ayanamsha raises `ValueError` immediately in `ephemeris.py`. Never silently defaults. |
| **N-1** | CRITICAL | Narayana Dasha REF table: Taurus = 4yr (should be 7yr) | ✅ **FIXED** (S1-S2): Period table in `narayana_dasa.py` corrected to 7yr. India 1947 regression validates full cycle. |
| **S-2** | HIGH | `CALC_Shadbala` J14 = 3851 (hardcoded anomalous value in Chesta Bala) | ✅ **FIXED** (S8): Replaced with `min(60, mean_motion/\|speed\|×60)` in `shadbala.py`. |
| **E-1** | CRITICAL | B19 JD formula omits Gregorian correction — 13-day error in Meeus fallback | ✅ **NOT PRESENT** in Python code: `swe.julday` handles Gregorian/Julian calendar correctly. Regression test added. |
| **A-2** | HIGH | `CALC_CombustionCheck` H6 references wrong row after RetrogradeFix rewrite | ✅ **NOT PRESENT** in Python code: Python uses `speed < 0` directly. Regression test added. |

---

## Active Known Issues (Python codebase, S188 state)

### C-18 🟠 HIGH — Stress-Test Edge Cases Not Cross-Validated

**Issue:** 8 classical edge-case categories need real-computation cross-validation, not mock-based testing.

**Status per category (post-360-chart pipeline):**

| # | Category | In 360 ADB? | In diverse_chart_fixtures? | Cross-validated? | Gap |
|---|----------|-------------|---------------------------|-----------------|-----|
| 1 | Neecha Bhanga | Can't verify (no dignity in verdicts) | Yes (3 synthetic) | **No** | Need real ADB charts with NB + Phase 2 dignity diff |
| 2 | Graha Yuddha | 187 conjunctions (proxy only) | Yes (3 synthetic) | **No** | Conjunction ≠ Graha Yuddha (needs latitude check) |
| 3 | Nakshatra cusp | 100 charts | Yes (9 synthetic) | **Positions only** | Need Phase 2 nakshatra cross-validation |
| 4 | Parivartana | Can't verify (no house lords in verdicts) | Yes (3 synthetic) | **No** | Need real ADB charts + Phase 2 house lord diff |
| 5 | Female chart | 50 charts | No | **Positions only** | Need gender-dependent rule testing |
| 6 | High-latitude (>55°) | 45 charts | Yes (2 synthetic) | **Positions only** | Bhava Chalita divergence not tested |
| 7 | Year-boundary | 8 charts | No | **Positions only** | JD edge case covered by position agreement |
| 8 | BC/pre-1800 | 24 charts | No | **Positions only** | Needs `seplm_18.se1` + `semom_18.se1` verification |

**Root problem:** `diverse_chart_fixtures.py` has synthetic position dicts for categories 1-4 but no real birth records. `test_diverse_charts.py` tests them via mock — never through `compute_chart()`. The 360-chart pipeline uses real computation but only covers positions (Phase 1).

**To close C-18:** Extend diff_engine to Phase 2 (dignity, house lords, yogas), then verify the 360 ADB charts actually trigger these conditions. For categories not naturally present in ADB data, find real birth charts that exhibit them (BV Raman Notable Horoscopes is a source).

**Effort:** Blocked on Phase 2 diff engine extension  
**Session:** S189 (opened), updated S312+

---

### PG-1 🟠 HIGH — PostgreSQL Tests Skipped
**Issue:** 3 tests in test suite require a live PostgreSQL instance (`PG_DSN` env var). They are currently skipped.  
**Fix:** Spin up Postgres, set `PG_DSN`, run `pytest tests/ -q` to confirm all 3 pass.  
**Effort:** 2 hours  
**Session:** S189

---

### SK-1 🟡 MEDIUM — Shadbala Kala Bala Sub-Components Unverified
**Issue:** Kala Bala has 8 sub-components per BPHS. Not confirmed whether all 8 are implemented vs partial.  
**Impact:** Shadbala total may be off by the missing components.  
**Fix:** Cross-check `shadbala.py` against PyJHora algorithm reference. Verify all 8: Nathonnata, Paksha, Tribhaga, Abda, Masa, Vara, Hora, Ayana.  
**Effort:** 2 hours  
**Session:** S189

---

### UI-1 🟡 MEDIUM — Confidence Model Not Surfaced in Streamlit UI
**Issue:** `GET /charts/{id}/confidence` endpoint exists and works (S188). The `ConfidenceOut` model is defined. But the Streamlit UI has no tab or section displaying birth time sensitivity / lagna boundary warnings to the analyst.  
**Effort:** 2 hours  
**Session:** S189

---

### FX-1 🟡 MEDIUM — Nehru Capricorn Lagna Skip
**Issue:** One ADB fixture (Nehru, Capricorn Lagna) is skipped in `test_calculations.py` with no documented root cause.  
**Fix:** Investigate — likely a sign-specific bug in one calculation module for Capricorn Lagna.  
**Effort:** 1 hour  
**Session:** S189

---

### EPH-1 🟡 MEDIUM — BC Date Charts Need Extended Ephemeris Files
**Issue:** For birth charts before 1800 AD, the standard `sepl_18.se1` / `semo_18.se1` files are insufficient. The extended files `seplm_18.se1` + `semom_18.se1` are needed.  
**Fix:** Download extended files from `github.com/aloistr/swisseph` to `ephe/`.  
**Effort:** 30 minutes  
**Session:** S189

---

### R21-1 🟡 MEDIUM — R21 Pushkara Navamsha Stub
**Issue:** Rule R21 (Pushkara Navamsha) is a stub returning `score=0.0` for all charts. It silently contributes nothing to house scores.  
**Classical reference:** PVRNR BPHS — Pushkara Navamsha planets are exceptionally strengthened.  
**Fix:** Implement the 14 Pushkara Navamsha positions (specific navamsha padas) and the additional Pushkara Bhaga degrees. Assign a `+0.5` modifier when bhavesh occupies a Pushkara position.  
**Effort:** 2-3 hours  
**Session:** S190+

---

## Recently Fixed (Archive)

| Session | ID | Fix |
|---------|----|----|
| S1-S2 | P-1 | Midnight fix: `if hour is None` in `ephemeris.py` |
| S1-S2 | P-4 | Bad ayanamsha → `ValueError` immediately, never silently defaults |
| S1-S2 | N-1 | Narayana Dasa Taurus=7yr corrected in `narayana_dasa.py` |
| S8 | S-2 | Shadbala Chesta Bala: `min(60, mean_motion/\|speed\|×60)` |
| S8 | E-1 | Confirmed NOT PRESENT in Python — `swe.julday` handles it; regression test added |
| S8 | A-2 | Confirmed NOT PRESENT in Python — `speed < 0` used directly; regression test added |
| S161 | Topocentric Moon | `swe.set_topo()` + `SEFLG_TOPOCTR` for Moon in `ephemeris.py` — DONE ✅ |
| S162 | Functional dignity in R02/R09 | `compute_functional_classifications(lagna_si)` wired in — DONE ✅ |
| S187 | War loser penalty | `_score_one_house` checks `planetary_war_losers`; −1.5 if bhavesh is loser — DONE ✅ |
| S187 | Dasha scoring | `score_chart_with_dasha()` stub replaced with real implementation — DONE ✅ |
| S187 | strict_school param | `score_axis()` / `score_all_axes()` accept `strict_school=True` — DONE ✅ |
| S188 | XIX API endpoints | 5 new endpoints (SVG/PDF/guidance/confidence/v3) — DONE ✅ |
| S188 | Postgres routing | `db_pg` with SQLite fallback wired in `main.py` — DONE ✅ |
| S188 | Swiss Ephemeris files | Real `sepl_18.se1` + `semo_18.se1` installed; Moshier retired — DONE ✅ |
