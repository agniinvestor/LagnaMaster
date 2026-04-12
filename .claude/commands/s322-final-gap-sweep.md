# S322: Final Gap Sweep — Zero L2, Zero Stale Labels, All Chapters Ship-Ready

## Session type
**Encoding** — read commentary, add modifiers/relationships, clean stale labels. No new primitives, no infrastructure.

## Pre-flight
```bash
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep -E 'BLOCKED|L2'
```

## Success criteria
1. Zero L2 rules across all 17 V2 chapters
2. Ch.19 and Ch.30 both show SHIP (L3+ ratio >= 90%)
3. Zero `NON-COMPUTABLE` labels in commentary_context across entire corpus
4. Zero stale "not yet implemented" comments in V2 files
5. All tests pass, ruff clean

---

## Part A: Fix 21 L2 rules (conditional_language_no_modifier)

All 21 rules are L2 because their `commentary_context` contains conditional language ("if", "unless", "except", "however", "but if", "provided", "only when") but the rule has no `modifiers`, `exceptions`, `rule_relationship`, or `lagna_scope` to handle it.

**The fix for EACH rule is one of:**
1. Add a `modifiers` list capturing the conditional stated in commentary
2. Add an `exceptions` list if the conditional is a cancellation condition
3. Add a `rule_relationship` if the conditional creates an alternative/contrary rule
4. If the conditional language is translator commentary (not a verse condition), reword the commentary to remove the conditional keyword — but ONLY if the verse itself has no conditional

**Read the commentary_context of each rule to decide which fix applies. Do NOT blindly add empty modifiers.**

### Ch.14 (3 rules — currently SHIP, don't break it)

**BPHS1402** (`bphs_v2_ch14.py`, v.5-6): "3rd lord and Mars together with malefic or in debilitation: destruction of coborn"
- Commentary mentions exception for Capricorn/Scorpio/Aries. This exception is already in the `exceptions` field — check. If present, the grader should see it. The issue may be the `commentary_context` using "if" about something else. Read the rule, identify the conditional keyword in commentary, and either add the right modifier or reword commentary.

**BPHS1425** (`bphs_v2_ch14.py`, v.4): "3rd lord in odd sign: male coborn tendency"
- Commentary says "If the 3rd house is occupied by a male planet as well as in a male sign, the contribution is strong." This "if" is explaining amplification. Add: `modifiers=[{"condition": "male_planet_in_3rd_and_odd_sign", "effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local"}]`

**BPHS1427** (`bphs_v2_ch14.py`, v.4): "Both male and female planets in 3rd: coborn of both sexes"
- Commentary likely has a similar "if" conditional. Read and add the right modifier.

### Ch.17 (1 rule — currently SHIP)

**BPHS1708** (`bphs_v2_ch17.py`, v.9-12): Jupiter — freedom from diseases
- Commentary mentions "while Jupiter afflicts the male's liver" — the "while" conditional. Jupiter is unique in the disease table because it says "freedom from diseases" not a disease. The conditional in commentary is a note about exceptions. Add `commentary_context` rewording OR a modifier for the exception.

### Ch.18 (1 rule — currently SHIP)

**BPHS1843** (`bphs_v2_ch18.py`, v.7-8): Jupiter in 7th
- Read the rule. Identify the conditional keyword. Fix accordingly.

### Ch.19 (4 rules — BLOCKED at 89%, needs these fixed to reach 90%)

**BPHS1908** (`bphs_v2_ch19.py`, v.5-6): Lords of 5th, 8th, ascendant in own navamsa — long life
**BPHS1911** (`bphs_v2_ch19.py`, v.9): 8th lord debilitated, malefic in 8th
**BPHS1916** (`bphs_v2_ch19.py`, v.14): Ascendant lord exalted, Moon 11th, Jupiter 8th
**BPHS1917** (`bphs_v2_ch19.py`, v.15): Ascendant lord exceedingly strong

Ch.19 has 18 rules total. 4 are L2. To get L3+ >= 90%, need at most 1 L2 (1/18 = 5.5% → 94.4% L3+). So fixing 3 of 4 would suffice, but fix all 4.

### Ch.20 (1 rule — currently SHIP)

**BPHS2021** (`bphs_v2_ch20.py`, v.30): Rahu in 5th (9th from 9th) + 9th lord
- Read, fix conditional.

### Ch.24a (1 rule — currently SHIP)

**BPHS2415** (`bphs_v2_ch24a.py`, v.12): Lagna lord in 12th devoid of benefic aspects
- Read, fix conditional.

### Ch.29 (1 rule — currently SHIP)

**BPHS2923** (`bphs_v2_ch29.py`, v.26): Benefic or malefic exalted in 7th from Lagna Pada
- Read, fix conditional.

### Ch.30 (9 rules — BLOCKED at 85%, needs these fixed to reach 90%)

**BPHS3000** (v.1-6), **BPHS3007** (v.7-12), **BPHS3008** (v.7-12), **BPHS3011** (v.13-15), **BPHS3020** (v.25-28), **BPHS3025** (v.29-30), **BPHS3029** (v.32), **BPHS3032** (v.33-36), **BPHS3035** (v.38)

Ch.30 has 46 rules. 9 are L2. Need at most 4 L2 (4/46 = 8.7% → 91.3% L3+). So fixing 5 of 9 would suffice, but fix all 9.

For each Ch.30 rule:
1. Read the rule's `commentary_context`
2. Find the conditional keyword
3. Decide: is it a verse condition (add modifier) or translator note (reword commentary)?
4. Apply fix

---

## Part B: Remove stale NON-COMPUTABLE labels (4 items)

### B1: `src/corpus/bphs_v2_ch30.py`
Lines 191, 208, 213, 228: "NON-COMPUTABLE: requires derived_house_sign/lord_of_derived_house"
- Both `derived_house_sign` and `lord_of_derived_house` ARE in IMPLEMENTED_FEATURES (taxonomy.py)
- Check if `rule_firing.py` actually handles them. If yes → remove NON-COMPUTABLE text. If no → leave it but note "primitive registered, handler pending in rule_firing.py"
- For commentary_context strings (lines 208, 228): replace "NON-COMPUTABLE: requires X" with "Uses X primitive (S316)."
- For code comments (lines 191, 213): update to reflect current status

### B2: `src/corpus/bphs_v2_ch29.py`
Line 625: "These require a derived_house_relationship primitive not yet implemented."
- The primitive is `derived_points_relationship` and IS implemented
- Change to: "# Uses derived_points_relationship primitive (implemented S316)."

### B3: `src/corpus/migration_registry.py`
Line 146: "All NON-COMPUTABLE (need argala_condition primitive)"
- argala_condition IS implemented since S316
- Change to: "Encoded from PDF in S315. 17 rules from 8 predictive slokas. argala_condition implemented S316. Slokas 1-10 are computational (Argala formation)."

---

## Execution order

1. **Part B first** (stale labels) — quick, low risk, 15 min
2. **Part A, ship-critical chapters first** — Ch.19 (4 rules) then Ch.30 (9 rules)
3. **Part A, remaining** — Ch.14, Ch.17, Ch.18, Ch.20, Ch.24a, Ch.29

After each chapter group, run:
```bash
.venv/bin/pytest tests/ -q --tb=short -x 2>&1 | tail -5
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```

## Commits (3)
1. `fix(S322): remove 4 stale NON-COMPUTABLE labels from Ch.29/30/migration`
2. `fix(S322): resolve 13 L2 rules in Ch.19 + Ch.30 — both chapters now ship-ready`
3. `fix(S322): resolve 8 remaining L2 rules across Ch.14/17/18/20/24a/29`

## Final validation
```bash
.venv/bin/pytest tests/ -q --tb=short -x
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep -E 'BLOCKED|L2|SHIP'
# Every chapter should show SHIP ✅, every L2 count should be 0
```

## Report format
```
L2 RULES BEFORE: 21
L2 RULES AFTER: [count]
STALE LABELS REMOVED: [count]
CHAPTERS UNBLOCKED: Ch.19 (was 89% → now [X]%), Ch.30 (was 85% → now [X]%)
SHIP-READY: [count]/17 chapters
```

## Non-negotiable
1. Read each rule's `commentary_context` BEFORE deciding on a fix
2. Do NOT add empty/meaningless modifiers just to silence the grader — the modifier must reflect a real verse condition
3. If the conditional language is genuinely translator commentary (not a verse condition), reword the commentary to remove the triggering keyword — but preserve the information
4. Do NOT change rule descriptions or predictions — only metadata fields (modifiers, exceptions, rule_relationship, commentary_context)
5. If rewording commentary, keep the Santhanam attribution and factual content — only restructure to avoid false-positive conditional keyword detection
