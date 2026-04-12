# S318 Final Sweep: Close All Remaining Code Bugs

## Context

S318 deep audit found 104 bugs. 78 are fixed. 26 remain. Of those, 6 are corpus data bugs (BUG-089–094) that require BPHS PDF encoding sessions — they cannot be fixed here. That leaves **20 code bugs** that CAN be fixed now. This session fixes all 20.

The full audit is in `docs/s318_deep_audit.md`. The "VERIFIED WRONG" table (lines 1089–1125) is the primary reference for each fix — it lists what the code has, what BPHS says, and the exact verse reference.

## Already Fixed: 78 of 104

BUG-001–013, 014–017, 024, 025, 028–037, 039, 040, 043–058, 064–074, 075–078, 079–088, 095–099, 101–104.

## What Remains: 20 code bugs + 6 deferred corpus bugs

| Workstream | Bugs | Files | Independent? |
|-----------|------|-------|-------------|
| A: Shadbala BPHS corrections | BUG-041, 042 | shadbala.py | Yes |
| B: Divisional chart formulas | BUG-022, 023, 026, 027 | divisional_charts.py | Yes |
| C: Kundali Milan data tables | BUG-059, 060, 061, 062 | kundali_milan.py | Yes |
| D: Computation fixes | BUG-018, 019, 020, 021 | dominance_engine.py, multi_lagna.py, orb_strength.py, kp_sublord.py | Yes |
| E: Aspect strength + Moolatrikona | BUG-038, 063 | scoring_patches.py, rule_firing.py | Yes |
| F: Security hardening | SEC-01, SEC-02, SEC-03 | auth.py, api/main.py | Yes |
| G: Corpus data (DEFERRED) | BUG-089–094 | corpus/*.json | N/A — encoding session |

Workstreams A–F are independent and can run in parallel.

---

## Step 0: Session Startup (MANDATORY)

Read these files — do NOT skip:
1. `lessons_learned.md`
2. `core_principles.md`
3. `tools/INDEX.md`

Verify baseline:
```
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```
Expected: ~14530 passed, 0 lint errors.

---

## Step 1: Dispatch Parallel Agents for Workstreams A–F

Use the `superpowers:dispatching-parallel-agents` skill pattern. Spawn 6 agents using the Agent tool. Each agent works in an isolated worktree (`isolation: "worktree"`) so they don't conflict.

### Agent A: Shadbala BPHS Corrections (BUG-041, 042)

```
prompt: |
  You are fixing Shadbala bugs in src/calculations/shadbala.py. This is a governance/fix 
  session — no new features. Read docs/s318_deep_audit.md lines 1089-1125 for the 
  "VERIFIED WRONG" table with exact BPHS references.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14

  BUG-041: Five Shadbala sub-component bugs (all in shadbala.py):

  1. Tribhaga Bala (BPHS Ch.27 v.12 p.269):
     - Day is divided into 3 equal parts from SUNRISE (not midnight). 
       Currently uses midnight-based hours. Fix: accept sunrise_jd parameter or 
       compute approximate sunrise. If sunrise not available, use 6:00 AM local as 
       reasonable approximation.
     - Day sequence WRONG: code has Mercury 1st third → change nothing else. 
       BUT verify: BPHS says Jupiter always gets 20 virupas (day and night). 
       Currently Jupiter only gets 20 in 1st third of day.
       Fix: Jupiter should get tribhaga_bala = 20.0 unconditionally.
     - Night sequence: code has Moon/Venus/Mars. BPHS says Venus/Moon/Mars.
       Fix: swap Moon and Venus in the night dict.

  2. Drekkana Bala (BPHS Ch.27 v.6 p.266):
     - Female planets in 2nd drekkana should get 15 virupas (code gives 15 for 3rd).
     - Neutral planets in 3rd drekkana should get 15 virupas (code gives 0 always).
     Fix: correct the drekkana → gender → virupa mapping.

  3. Hora Bala (BPHS Ch.27 v.13 p.272):
     - Should start from SUNRISE, not midnight.
     Fix: same sunrise approach as Tribhaga. Odd hora from sunrise = Sun's hora, 
     even = Moon's hora.

  4. Chesta Bala (BPHS Ch.27 v.21-25 p.284):
     - Should use 8-state motion classification:
       Vakra(retrograde)=60, Anuvakra(entering retro)=30, Vikala(stationary)=15, 
       Manda(slow direct)=30, Mandatara(very slow)=15, Sama(mean speed)=7.5, 
       Chara(fast direct)=45, Atichara(very fast)=30
     - Current code uses simple elongation/3 which is wrong.
     - Read the current implementation first. If it already has motion states, just 
       verify the virupa values. If it uses elongation, replace with the 8-state model.
     - For determining motion state: compare planet's daily motion to its mean daily 
       motion. If daily_motion < 0 → Vakra. If |daily_motion| < 0.1 → Vikala. 
       If 0 < daily_motion < mean/2 → Mandatara. If mean/2 < daily < mean → Manda. 
       If daily ≈ mean → Sama. If daily > mean*1.5 → Atichara. Else → Chara.
     - Mean daily motions: Sun≈1.0°, Moon≈13.2°, Mars≈0.524°, Mercury≈1.383°, 
       Jupiter≈0.083°, Venus≈1.2°, Saturn≈0.034°
     NOTE: Sun and Moon do not have Chesta Bala per BPHS. They use Ayana Bala instead.
     If the code already handles this correctly, leave it.

  BUG-042: Yuddha Bala (BPHS Ch.27 v.20 p.284):
     - Planetary War (Yuddha/Graha Yuddha) completely missing from shadbala.
     - When two planets are within 1° of each other in longitude, the planet with 
       higher latitude wins the war.
     - Winner gets the loser's Chesta Bala added to their own.
     - Loser gets their Chesta Bala subtracted.
     - Only applies to Mars, Mercury, Jupiter, Venus, Saturn (not Sun/Moon).
     - Implementation: after computing Chesta Bala for all planets, check all pairs 
       for proximity < 1°. For each war pair, transfer Chesta Bala from loser to winner.
     - Add a `yuddha_bala` field to the ShadBala dataclass if not present.

  IMPORTANT: Read shadbala.py FIRST to understand the current structure before making 
  changes. The file is ~500 lines. Understand how ShadBala dataclass, compute_shadbala(), 
  and sub-component functions work before modifying.

  After fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit each bug separately:
  fix(S318): BUG-041 — shadbala Tribhaga/Drekkana/Hora/Chesta per BPHS Ch.27
  fix(S318): BUG-042 — add Yuddha Bala (planetary war) to shadbala
```

### Agent B: Divisional Chart Formulas (BUG-022, 023, 026, 027)

```
prompt: |
  You are fixing divisional chart formula bugs in src/calculations/divisional_charts.py.
  Read docs/s318_deep_audit.md lines 1089-1125 for the "VERIFIED WRONG" table.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14

  IMPORTANT: Also read src/calculations/varga.py — it is the CANONICAL source for 
  divisional chart formulas (verified against BPHS). Where divisional_charts.py disagrees 
  with varga.py, align with varga.py. Where both are wrong per BPHS, fix both.

  BUG-022: D60 even-sign formula
  - divisional_charts.py uses (5 + div) % 12 (Virgo start)
  - varga.py uses (5 + k) % 12 (also Virgo start)  
  - BPHS text is ambiguous per audit. Since both agree on Virgo(5), this may 
    actually be ALREADY ALIGNED. Read both implementations carefully and verify 
    they produce identical results for test cases. If they match → mark as resolved.
    If they differ → align divisional_charts.py to varga.py.

  BUG-023: D7 zero-falsy bug
  - Read the current _d7() in divisional_charts.py. If it uses proper if/else 
    instead of and/or idiom, it's already fixed. Verify and move on.

  BUG-026: D16 Shodasamsa formula (BPHS Ch.6 v.16 p.74)
  - BPHS: Movable signs → from Aries, Fixed → from Leo, Mutable → from Sagittarius
  - Audit says code used si%4 (wrong). Check current code — it may already be fixed 
    to use si%3 (modality). If already correct, mark resolved.

  BUG-027: Other divisional formulas verified wrong:
  - D3 Drekkana: should be trikona (1st/5th/9th from sign = si + k*4), 
    NOT element-based grouping. Check current _d3().
  - D4 Chaturthamsa: should be kendras from sign (si + k*3).
    Check current _d4().
  - D10 Dasamsa even signs: should be from 9th sign (si + 9 + k) % 12.
    Check current _d10().
  - D20 Vimsamsa: Movable→Aries, Fixed→Sagittarius, Mutable→Leo.
    Check current _d20().
  - D24 Chaturvimsamsa even signs: even→Cancer(3).
    Audit says code has even→Sagittarius(8). Check current _d24().
  - D45 Akshavedamsa: Movable→Aries, Fixed→Leo, Mutable→Sagittarius.
    Check current _d45().

  FOR EACH formula: 
  1. Read both divisional_charts.py and varga.py implementations
  2. Compare against BPHS reference in audit
  3. Write a small test to verify the formula for known inputs
  4. If wrong, fix to match BPHS
  5. Run tests after each fix

  Also verify: does varga.py have the same formulas? If yes, ensure they match.
  The goal is BOTH files produce identical results for all divisional charts.

  After fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): BUG-022,023,026,027 — divisional chart formulas per BPHS Ch.6
```

### Agent C: Kundali Milan Data Tables (BUG-059, 060, 061, 062)

```
prompt: |
  You are fixing data table errors in src/calculations/kundali_milan.py — the marriage 
  compatibility (Ashtakoot) module. Read docs/s318_deep_audit.md for the "DD11: 
  kundali_milan.py" section and "VERIFIED WRONG" table (lines 1115-1124).

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14

  BUG-059: Yoni animals swapped for Mrigashira and Ardra
  - Mrigashira should be "serpent" (code has "dog" per BUG-058 fix comment)
  - Ardra should be "dog" (code has "cat" per BUG-058 fix comment)
  Read the current _YONI list. The BUG-058 fix may have already been applied but with 
  wrong values. Standard Muhurta reference:
    Ashwini=horse, Bharani=elephant, Krittika=goat, Rohini=serpent, 
    Mrigashira=serpent, Ardra=dog, Punarvasu=cat, Pushya=goat,
    Ashlesha=cat, Magha=rat, P.Phalguni=rat, U.Phalguni=cow,
    Hasta=buffalo, Chitra=tiger, Swati=buffalo, Vishakha=tiger,
    Anuradha=deer, Jyeshtha=deer, Moola=dog, P.Ashadha=monkey,
    U.Ashadha=mongoose, Shravana=monkey, Dhanishtha=lion,
    Shatabhisha=horse, P.Bhadrapada=lion, U.Bhadrapada=cow,
    Revati=elephant
  Update the _YONI list to match this standard reference.

  BUG-060: Gana error for Rohini
  - Audit says this is DISPUTED — Muhurta Chintamani says Deva (current code), 
    some South Indian sources say Manava.
  - Since the code already has Deva and the primary reference supports it, 
    ADD A COMMENT noting the dispute but keep Deva. Mark as resolved.

  BUG-061: Graha Maitri — 6 friendship pairs wrong
  Per BPHS Ch.3 v.55 p.40:
  - Moon-Jupiter: should be Neutral (code has Friend)
  - Moon-Venus: should be Neutral (code has Friend) 
  - Mercury-Moon: should be Enemy (code has Neutral)
  - Mercury-Saturn: should be Neutral (code has Friend)
  - Venus-Moon: should be Enemy (code has Neutral)
  - Saturn-Mars: should be Enemy (code has Neutral)
  
  Find the friendship matrix in kundali_milan.py (likely a dict or list). 
  Fix ONLY these 6 pairs. Do NOT touch other pairs that are already correct.

  BUG-062: Tara Kuta — Janma Tara scored wrong
  - Tara group 1 (Janma) should be inauspicious = 0 points
  - Code has _TS = {1: 0, ...} — wait, that looks correct already (1→0)?
  - Read the code carefully. The dict maps tara_group → points. Check if 
    group 1 (Janma) maps to 0. If it does, this may be already fixed.
  - Standard Tara scoring: groups 1(Janma), 3(Vipat), 5(Pratyari), 7(Vadha) = 
    inauspicious (0 points). Groups 2, 4, 6, 8, 9 = auspicious (3 points).
  - Verify the entire _TS dict against this standard.

  After fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): BUG-059,060,061,062 — kundali milan Yoni/Gana/Maitri/Tara corrections
```

### Agent D: Computation Fixes (BUG-018, 019, 020, 021)

```
prompt: |
  You are fixing 4 computation bugs across 4 files. Read docs/s318_deep_audit.md for 
  details (search for each BUG number and the C16-C18 critical bug descriptions).

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  India 1947 fixture: compute_chart(year=1947, month=8, day=15, hour=0.0, 
    lat=28.6139, lon=77.2090, tz_offset=5.5)

  BUG-018: Jupiter aspect off-by-one in dominance_engine.py
  File: src/calculations/dominance_engine.py
  - Line ~89: `(jup_h + 4) % 12 + 1` is wrong for 1-indexed house numbers
  - Correct: `(jup_h - 1 + 4) % 12 + 1` (convert to 0-indexed, add offset, back to 1-indexed)
  - Same pattern for all special aspects in this file — check Mars and Saturn too.
  - Read the file to understand the house indexing convention used.

  BUG-019: Arudha Pada off-by-one in multi_lagna.py
  File: src/calculations/multi_lagna.py
  - Line ~238: `final = (raw + 9) % 12` — should add 10, not 9
  - BPHS exception rule: when counted distance = 1 or 7 (same/7th house), 
    add 10 signs instead of using the standard rule.
  - Read the function to understand the full Arudha Pada calculation.
  - Verify: `(raw + 10) % 12` or `(raw - 1 + 10) % 12` depending on indexing.

  BUG-020: orb_strength.py aspect_strength() fundamentally wrong
  File: src/calculations/orb_strength.py
  - Current code measures proximity to nearest 30° multiple (any sign boundary).
  - CORRECT approach: measure proximity to ACTUAL ASPECT ANGLES.
  - Standard aspects: conjunction(0°), opposition(180°), trine(120°), 
    square(90°), sextile(60°)
  - Special aspects: Mars 4th/8th (90°/210°→equivalently: look at actual house offsets)
  
  The fix should:
  1. Define actual aspect angles: [0, 60, 90, 120, 180] for general aspects
  2. For each pair of planets, compute the angular separation
  3. Find the nearest actual aspect angle
  4. Strength = 1.0 - (distance_from_nearest_aspect / orb_limit)
  5. If distance > orb_limit, strength = 0.0
  
  Read the file first to understand the current API and callers. Maintain the same 
  function signature so callers don't break.

  BUG-021: kp_sublord.py weekday mapping wrong
  File: src/calculations/kp_sublord.py
  - Line ~287: `day_lords = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]`
  - Python weekday(): Monday=0, Tuesday=1, ..., Sunday=6
  - Standard weekday lords: Monday=Moon, Tuesday=Mars, ..., Sunday=Sun
  - So the list should be: ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
  - Fix: reorder the list to match Python's weekday() convention.

  After ALL fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit each separately:
  fix(S318): BUG-018 — Jupiter aspect off-by-one in dominance_engine
  fix(S318): BUG-019 — Arudha Pada exception adds 10 signs not 9
  fix(S318): BUG-020 — orb_strength uses actual aspect angles
  fix(S318): BUG-021 — kp_sublord weekday mapping matches Python convention
```

### Agent E: Aspect Strength + Moolatrikona (BUG-038, 063)

```
prompt: |
  You are fixing 2 bugs in LagnaMaster. Read docs/s318_deep_audit.md "VERIFIED WRONG" 
  table for details.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14

  BUG-038: ASPECT_STRENGTH values uniform instead of graded
  File: src/calculations/scoring_patches.py
  - Current: all special aspects = 0.75
  - BPHS Ch.26 v.2-5 p.254 defines GRADED aspect strengths:
    * Full aspect (7th house): 1.0 (all planets)
    * Mars special: 4th house = 3/4 (0.75), 8th house = 1/4 (0.25) — wait, 
      actually this needs BPHS verification. Let me state what the audit found:
    * The audit says "Graded: 1/4, 1/2, 3/4 + special bonuses" vs "Uniform 0.75"
    * Standard BPHS aspect strengths (in virupas/60):
      - 3rd/10th house: 1/4 aspect (15 virupas)
      - 5th/9th house: 1/2 aspect (30 virupas)  
      - 4th/8th house: 3/4 aspect (45 virupas)
      - 7th house: full aspect (60 virupas)
    * Special aspects ADD to these base values:
      - Mars 4th + 8th: already 3/4, Mars's special makes it full (1.0)
      - Jupiter 5th + 9th: already 1/2, Jupiter's special makes it full (1.0)
      - Saturn 3rd + 10th: already 1/4, Saturn's special makes it full (1.0)
  
  Read the file to understand the ASPECT_STRENGTH dict structure. Update it to use 
  graded values:
  - Mars 4th house: 1.0 (special full), Mars 8th house: 1.0 (special full)
  - Jupiter 5th house: 1.0 (special full), Jupiter 9th house: 1.0 (special full)
  - Saturn 3rd house: 1.0 (special full), Saturn 10th house: 1.0 (special full)
  
  BUT also add the BASE aspect strengths for ALL planets:
  - All planets 3rd/10th: 0.25
  - All planets 5th/9th: 0.50
  - All planets 4th/8th: 0.75
  - All planets 7th: 1.0
  
  Check how ASPECT_STRENGTH is consumed (grep for it). If callers expect only 
  special-planet entries, you may need to change the dict structure. Read consumers first.

  BUG-063: Moolatrikona uses sign-only check instead of degree-bounded
  File: src/calculations/rule_firing.py
  - Current: checks only if planet is in its Moolatrikona SIGN
  - BPHS Ch.3 v.51-54 p.39 defines DEGREE RANGES:
    * Sun: Leo 0°-20°
    * Moon: Taurus 3°-30° (some say 4°-20°, use 3°-30° per Santhanam)
    * Mars: Aries 0°-12°
    * Mercury: Virgo 15°-20°
    * Jupiter: Sagittarius 0°-10°
    * Venus: Libra 0°-15°
    * Saturn: Aquarius 0°-20°
  - Read the current moolatrikona check in rule_firing.py.
  - Also read src/calculations/dignity.py which has MOOLTRIKONA_RANGES — 
    this is the canonical source (verified correct per audit line 1069).
  - Fix: import MOOLTRIKONA_RANGES from dignity.py and use it in rule_firing.py 
    for degree-bounded checks.
  - The check should be: planet's sign matches MT sign AND planet's degree within 
    the MT degree range.

  After fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit each separately:
  fix(S318): BUG-038 — graded aspect strengths per BPHS Ch.26
  fix(S318): BUG-063 — moolatrikona degree-bounded check per BPHS Ch.3
```

### Agent F: Security Hardening (SEC-01, SEC-02, SEC-03)

```
prompt: |
  You are fixing 3 security issues in LagnaMaster. Read docs/s318_deep_audit.md for the 
  Security section.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14

  SEC-01: JWT secret hardcoded fallback (HIGH)
  File: src/api/auth.py (or similar — grep for "JWT" or "SECRET" in src/)
  - Find the hardcoded JWT secret fallback
  - Replace with: os.environ.get("JWT_SECRET") with NO fallback — if the env var 
    is missing, raise a clear error at startup
  - Add: if not JWT_SECRET: raise RuntimeError("JWT_SECRET environment variable required")
  - This ensures the app cannot start with a hardcoded secret in production

  SEC-02: CORS allow_origins=["*"] (MEDIUM)
  File: src/api/main.py
  - Find the CORS middleware configuration
  - Change allow_origins from ["*"] to os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
  - This defaults to localhost for development but requires explicit configuration 
    for production

  SEC-03: Version string stale (LOW)
  File: src/api/main.py
  - Find version="0.1.0" or similar
  - Update to version="3.0.0" to match the actual engine version in CLAUDE.md

  After fixes: .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): SEC-01,02,03 — JWT secret, CORS origins, version string
```

---

## Step 2: Reconcile Agent Results

After all 6 agents complete:

1. **Check each agent's worktree** for a branch with commits.
2. **Merge order** (least conflict risk first):
   - Agent F (security — isolated files)
   - Agent C (kundali_milan — isolated file)
   - Agent E (scoring_patches + rule_firing — low overlap)
   - Agent D (4 independent files)
   - Agent B (divisional_charts — isolated file)
   - Agent A (shadbala — isolated file, but largest change)

3. **Cherry-pick** each worktree branch's commits onto main:
   ```
   git cherry-pick <commit-sha>
   ```

4. **If merge conflicts:** resolve manually, keeping the bug-fix agent's version for the file it was fixing.

5. **Run full verification after all merges:**
   ```
   .venv/bin/pytest tests/ -q --tb=short -x
   .venv/bin/ruff check src/ tests/
   ```

---

## Step 3: Post-Merge Regression Tests

After merging, write targeted regression tests for the highest-risk fixes:

1. **Shadbala Chesta Bala** — verify 8-state classification produces virupas in [0, 60]
2. **Divisional charts** — cross-validate divisional_charts.py vs varga.py for all 16 vargas using India 1947 fixture
3. **Kundali Milan** — verify Mrigashira yoni = serpent, Ardra = dog, and 6 friendship corrections
4. **orb_strength** — verify 0 strength returned for non-aspect angles (e.g., 45°)
5. **Moolatrikona** — verify Sun at Leo 25° is NOT moolatrikona (only 0-20°)

Create `tests/test_s318_final_regressions.py` with these tests.

---

## Step 4: Run /rework-check

Invoke the `/rework-check` skill to detect if any rework happened during the session.

---

## Step 5: Invoke superpowers:verification-before-completion

Before claiming done, invoke `superpowers:verification-before-completion`. This ensures:
- All tests actually pass (fresh run, not cached)
- Lint is clean
- No regressions from baseline

---

## Step 6: Update Documentation

Update these files:
- `docs/MEMORY.md` — test count, S318 Final Sweep entry, update "78 fixed" to final count
- `docs/CHANGELOG.md` — S318 Final Sweep entry with three-lens analysis
- `docs/SESSION_LOG.md` — S318 Final Sweep summary line

---

## Step 7: Completion Report

| Item | Value |
|------|-------|
| Bugs fixed this session | list each BUG-NNN and SEC-NN |
| Total S318 bugs fixed | should be 98 of 104 (or 101 if SEC counted) |
| Bugs remaining | should be 6 — the deferred corpus bugs |
| Tests before vs after | pass/fail/skip counts |
| Regressions | any (should be 0) |
| Shadbala components fixed | Tribhaga, Drekkana, Hora, Chesta, Yuddha |
| Divisional formulas verified | list which D-charts were fixed vs already correct |
| Deferred to encoding | BUG-089–094 with reason |

---

## Corpus Data Bugs — DEFERRED (BUG-089–094)

These require BPHS PDF verification and the full encoding protocol. Do NOT attempt here.

| Bug | What | Why Deferred |
|-----|------|-------------|
| BUG-089 | 10 factual errors in V2 corpus | Verse-by-verse BPHS verification needed |
| BUG-090 | ~40 rules: aspect vs occupation confusion | Re-read BPHS text for each rule |
| BUG-091 | OR-vs-AND logic in 3 rules | BPHS text determines correct logic |
| BUG-092 | Relative→absolute house positions | Verse context needed |
| BUG-093 | 9 of 11 marriage timing rules incomplete | Missing conditions to encode |
| BUG-094 | Ch.19 missing 9 of 15 slokas | Full encoding session (BPHS Vol 1 pp.169-172) |

Use `/encode-chapter 19` in a future encoding session for BUG-094.

---

## Key Files

- Audit: `docs/s318_deep_audit.md` (lines 1089–1125 = "VERIFIED WRONG" table)
- BPHS Vol 1: `BPHS-Santhanam-Vol-1.pdf`
- BPHS Vol 2: `BPHS-Santhanam-Vol-2.pdf`
- Tools index: `tools/INDEX.md`
- Canonical varga formulas: `src/calculations/varga.py`
- Canonical dignity data: `src/calculations/dignity.py`

## Session Type

**Governance/fix session** — no new corpus rules, no new features. Fix BPHS-verified formula bugs, correct data tables, harden security.

## Baseline

- Tests: ~14530 passed, 210 skipped, 360 xfailed
- Ruff: 0 errors
- Total fixed so far: 78 of 104

## Non-Negotiable Rules

1. Read the source file BEFORE modifying it. Understand existing code.
2. grep for callers BEFORE changing any function signature.
3. Run tests AFTER each fix, not just at the end.
4. Do NOT touch scoring weights in multi_axis_scoring.py (breaks regression snapshots).
5. Do NOT modify corpus JSON files (that's encoding session work).
6. When BPHS reference exists in the audit, use it. Don't guess.
7. If a bug listed here turns out to be already fixed, verify and move on — don't re-fix.
