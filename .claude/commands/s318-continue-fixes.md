# S318 Phase -1: Continue Bug Fixes

## Context

S318 deep audit found 104 deduplicated bugs across 660 files (178,072 lines). The full audit is in `docs/s318_deep_audit.md`. The canonical architecture is in `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`.

## What's Already Fixed (35 of 104 bugs, across 4 commits)

### Commit 1 (2d9887f0): BUG-001,002,003,006,007,008,024,025,050
- Mars aspects {3,9}→{3,7} in multi_axis_scoring.py, feature_decomp.py (BUG-001)
- Mars {3,7,9}→{3,7}, Jupiter {4,6,9}→{4,8}, Saturn {2,6,9}→{2,9} in scoring_v2.py (BUG-002,003)
- Sunapha/Anapha swap fixed in yogas_extended.py (BUG-006)
- Vesi/Vasi swap fixed in yogas_extended.py (BUG-007)
- Rajju/Musala/Nala: sign_index%3 not house number in yogas_extended.py (BUG-008)
- Shadbala Tribhaga day Jupiter→Mercury, night Moon/Venus→Venus/Moon, Jupiter always 20 in shadbala.py (BUG-024,025)
- Cancer yogakaraka Venus→Mars via canonical KNOWN_YOGAKARAKAS import in scoring.py (BUG-050)

### Commit 2 (7518c15b): BUG-009,010,013,035,036,040,056,057,058,066
- Tara Janma group 1 auspicious→inauspicious in kundali_milan.py (BUG-057)
- Yoni Mrigashira→serpent, Ardra→dog in kundali_milan.py (BUG-058)
- Bhakut 5/9 penalty removed in kundali_milan.py (BUG-013)
- 6 friendship errors per BPHS Ch.3 v.55 in kundali_milan.py (BUG-056)
- Baladi even-sign reversal per BPHS Ch.45 v.3 in avastha.py (BUG-009)
- Vriddha 0.50→0.125, Mrita 0.10→0.0 in avastha.py (BUG-010)
- planet_not_in_house: check ALL houses in list in rule_firing.py (BUG-035)
- planet_not_aspecting: check ALL houses in list in rule_firing.py (BUG-036)
- av_transit: getattr→planet_av.get in av_transit.py (BUG-040)
- data_minimisation: last_accessed→created_at in data_minimisation.py (BUG-066)

### Commit 3 (93d61e14): BUG-004,005,016,017,028,029,030,031,032,033,034,039
- 9 divisional chart formulas in divisional_charts.py (D3,D4,D7,D10,D16,D20,D24,D45) (BUG-016,017,029-034)
- scoring_v2 bh_cotenants sign_index comparison (BUG-005)
- Shadbala Drekkana Bala female→2nd, neutral→3rd in shadbala.py (BUG-028)
- varshaphala hardcoded 1947 removed (BUG-039)

### Commit 4 (64751c97): BUG-011,012,015,037
- MT degree ranges from BPHS Ch.3 v.51-54 in rule_firing.py (BUG-037)
- dasha_scoring compute actual running MD lord (BUG-012)
- D60 even-sign offset aligned with varga.py (BUG-015)
- Lajjitadi scope noted as any-planet per BPHS Ch.45 (BUG-011)

## What Remains (69 of 104 bugs)

### IMMEDIATE PRIORITY: Dignity Wiring (BUG-081 — the single highest-impact fix)

`score_chart()` in `src/scoring.py` calls `compute_all_dignities()` but only uses the result for R19 (combustion). Exalted Jupiter scores identically to debilitated Jupiter. Add R24 after R22 in the house scoring loop (~10 lines):

```python
# After the R22 block (approximately line 570 in scoring.py):
r24_score = 0.0
if bhavesh in dignities:
    from src.calculations.dignity import DIGNITY_SCORE
    r24_score = DIGNITY_SCORE.get(dignities[bhavesh].dignity, 0.0)
rules.append(RuleResult(
    rule="R24", description=f"Bhavesh {bhavesh} dignity modifier",
    score=r24_score, triggered=r24_score != 0.0,
))
```

Also add `"R24": 1.00` to the W dict. Test: India 1947 house scores should change (dignity now contributes). Update snapshot values with pytest.approx.

### CATEGORY 2: Missing Features (7 bugs)

| Bug | File | What to Do |
|-----|------|-----------|
| BUG-043 | shadbala.py | Yuddha Bala missing — add planetary war detection (planets within 1 degree, brighter wins) |
| BUG-044 | shadbala.py | Ojhayugma: Mercury/Saturn flat 15 → check rasi+navamsa independently |
| BUG-045 | varshaphala.py | Sahams not implemented — document as known gap, not fixable in a bug fix session |
| BUG-046 | varshaphala.py | Mudda Dasha not implemented — same, document |
| BUG-047 | varshaphala.py | Pancha Vargeeya Bala not implemented — same, document |
| BUG-048 | rule_firing.py:1316-1321 | _is_activated is no-op (both branches return True) — needs timing context to fix properly; document |
| BUG-049 | scoring.py | R21 hardcoded to 0 — needs Pushkara Navamsha logic; document |

For BUG-045 through BUG-049: these are missing features, not wrong formulas. Add KNOWN_GAP comments citing the bug ID. Don't build new features in a fix session.

### CATEGORY 3: Remaining Data Table Errors (5 bugs remaining)

| Bug | File | Fix |
|-----|------|-----|
| BUG-051 | scoring.py:91,94 | Gentle signs: 3 different sets, none match BPHS. Canonical set (0-indexed signs of benefic lords): {1,2,3,5,6,8,11} |
| BUG-052-054 | scoring.py vs multi_axis_scoring.py | Sthir Karak H4/H9/H10 disagree — needs BPHS Ch.32 verification |
| BUG-055 | functional_dignity.py | H1 lord always classified as yogakaraka — add exclusion |
| BUG-064 | scoring.py vs multi_axis_scoring.py | Dig Bala peak houses Mars=[10,3] vs Mars=10 — use canonical (Mars=10 only) |
| BUG-065 | ashtakavarga.py:274 | SAV computed from post-Shodhana BAVs — change to raw_bindus |

### CATEGORY 4: Silent Failures (9 specific bugs + 143 handlers)

The 9 specific bugs (BUG-066 through BUG-074) — BUG-066 is already fixed. Remaining:
| Bug | File | Fix |
|-----|------|-----|
| BUG-067 | app.py | 21 silent except: pass → add st.error() or logger.exception() |
| BUG-068 | pressure_engine.py | 5 handlers returning 1.0 → log + return None |
| BUG-069 | dominance_engine.py | 4 handlers setting jup_strong=True → log + raise |
| BUG-070 | longevity.py | Returns 66.0 on error → log + raise |
| BUG-071 | planet_effectiveness.py:51 | Wrong shadbala API signature → fix call |
| BUG-072 | api/main.py:123-135 | save_chart dict vs JSON string → json.dumps() |
| BUG-073 | api/main_v2.py:217-224 | ChartSummary wrong fields → fix model construction |
| BUG-074 | app.py:75 | monte_carlo_sensitivity → compute_sensitivity |

For the 143 silent handlers broadly: configure ruff BLE001 strictly. Fix the worst offenders (longevity returning 66.0, dominance_engine setting jup_strong=True). The UI handlers (st.error) are acceptable.

### CATEGORY 5: Dead/Unreachable Code (6 bugs)

| Bug | What to Do |
|-----|-----------|
| BUG-075 | Delete 15 orphaned modules (planet_avasthas.py, sayanadi_full.py, friendship.py, yogas_additions.py, etc.) |
| BUG-076 | Delete remaining ~124 dead files (22,692 lines) — use import graph from s318 audit |
| BUG-077 | 12 dead expressions — delete the no-op lines |
| BUG-078 | 13 dead functions — delete |
| BUG-079 | 3 broken imports (src.calculations.vargas, src.reports.pdf_report, src.calculations.score_to_language) — fix or remove |
| BUG-080 | setup_ci_guard.py module-level side effects — add `if __name__ == "__main__"` guard |

### CATEGORY 6: Architecture Flaws (8 bugs)

| Bug | What to Do |
|-----|-----------|
| BUG-081 | Dignity not wired → R24 (see IMMEDIATE PRIORITY above) |
| BUG-082 | Two parallel scoring engines → fix score_all_axes() data bugs (already done in commits 1-4), add RuleResult traceability, deprecate with warning |
| BUG-083 | Scoring uses divisional_charts.py → change imports to varga.py |
| BUG-084 | CalcConfig name collision → rename one of them |
| BUG-085 | Weight discrepancies R10/R13/R20 → align to one set of weights |
| BUG-086 | functional_dignity vs functional_roles disagree → use KNOWN_FUNCTIONAL_MALEFICS (bphs_pdf verified) as canonical |
| BUG-087 | 5 avastha modules with 3 value sets → redirect pressure_engine to avasthas.py, delete dead modules |
| BUG-088 | v2_builder mirror() bypasses validation → call _validate_add() in mirror() |

### CATEGORY 7: Corpus Data Errors (8 bugs)

| Bug | What to Do |
|-----|-----------|
| BUG-089 | 10 factual errors in V2 corpus — fix each condition per BPHS PDF (verse refs in s318 audit) |
| BUG-090 | ~40 rules: aspect vs occupation confusion — re-encode per BPHS text |
| BUG-091 | OR-vs-AND logic errors — fix in 3 rules (BPHS1501, BPHS1611, BPHS1600) |
| BUG-092 | Relative→absolute house positions — fix in affected rules |
| BUG-093 | 9 of 11 marriage timing rules incomplete — add missing conditions |
| BUG-094 | Ch.19 missing 9 of 15 slokas — encode from BPHS Vol 1 pp.169-172 |
| BUG-095 | Ch.24a v.3 fabricated claim — delete "no siblings lost" |
| BUG-096 | saravali_signs_5.py header says 130, has 142 — fix header |

### CATEGORY 8: Test Gaps (8 bugs)

| Bug | What to Do |
|-----|-----------|
| BUG-097 | avasthas.py has 0 test coverage → write tests citing BPHS Ch.45 |
| BUG-098 | 107 exact float assertions → pytest.approx |
| BUG-099 | test_panchanga_legacy.py empty stub → delete |
| BUG-100 | 2 tests with try/except pass → fix or delete |
| BUG-101 | test_kundali_milan.py test_h3 fake test → fix or delete |
| BUG-102 | Dignity effect on scoring never tested → write test after R24 wiring |
| BUG-103 | List-valued conditions never tested → write test for rule_firing |
| BUG-104 | D9 cross-validation no-op → fix try/except in test_varga.py |

## Execution Protocol

1. Read `docs/s318_deep_audit.md` for full bug details (the DEDUPLICATED MASTER BUG LIST section has all 104 with exact file:line references)
2. Read `lessons_learned.md` and `core_principles.md`
3. Fix bugs in priority order: BUG-081 (dignity wiring) first, then remaining categories
4. After each fix: `.venv/bin/pytest tests/ -q --tb=short -x`
5. After each batch: `.venv/bin/ruff check src/ tests/`
6. Commit format: `fix(S318): BUG-NNN description — BPHS Ch.N v.M`
7. If a fix causes >5 unrelated test failures, stop and investigate
8. For missing features (BUG-043 through BUG-049): add KNOWN_GAP comments, don't build new features
9. For corpus fixes (BUG-089 through BUG-096): these are encoding session work, not formula fixes. Note them but defer to encoding sessions unless trivial.

## Key Files

- Audit: `docs/s318_deep_audit.md`
- Architecture: `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`
- Execution plan: `docs/superpowers/specs/2026-04-07-v11-execution-plan.md`
- BPHS Vol 1: `BPHS-Santhanam-Vol-1.pdf`
- BPHS Vol 2: `BPHS-Santhanam-Vol-2.pdf`

## Session Type

This is a **governance/fix session** (not encoding). No new corpus rules. No new features. Fix existing bugs, wire existing computations, delete dead code.
