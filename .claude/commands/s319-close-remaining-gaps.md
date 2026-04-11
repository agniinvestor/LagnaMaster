# S319 Close Remaining Gaps

Close the 8 remaining encoding gaps from S319 Phase 3. Each gap has a different character — encode what the verse says, document what the engine can't express, and don't fabricate closures.

## Session type
**Encoding** — read PDF, encode rules, commit. No new primitives, no infrastructure.

## Pre-flight
```bash
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```

---

## Gap 1 — Ch.17 Rahu disease (CAN ENCODE)

**File:** `src/corpus/bphs_v2_ch17.py`
**PDF:** p.154-155, v.9-12 table on p.155
**Verse says:** Rahu → "Danger from the so called low-caste men"

The S319 agent excluded Rahu saying "they do not own any house." This is wrong — the verse table on p.155 explicitly lists Rahu by name between Saturn and Ketu.

**Action:** Read p.155. Encode one rule following the existing Moon/Mars/Mercury/Jupiter/Venus/Saturn pattern in the file. Use `planet_in_house` with `planet: "Rahu"`, house `[6, 8]`. Note in `commentary_context` that Rahu's "disease" is social danger rather than physical ailment. Use `primary_domain="health"` to match the other rules in the block — the verse groups all 9 grahas under "DISEASES IN GENERAL."

## Gap 2 — Ch.17 Ketu disease (CAN ENCODE)

**File:** `src/corpus/bphs_v2_ch17.py`
**PDF:** p.155, same table
**Verse says:** Ketu → "Diseases of the navel"

Same exclusion error as Rahu. Straightforward health prediction.

**Action:** Encode one rule with `planet: "Ketu"`, house `[6, 8]`, `primary_domain="health"`. Disease of the navel is unambiguous.

After encoding both: run tests, ruff, commit:
`feat(S319): encode Ch.17 Rahu/Ketu disease rules — v.9-12 table completion`

---

## Gap 3 — Ch.14 Saturn/Rahu as male planets (INVESTIGATE THEN DECIDE)

**File:** `src/corpus/bphs_v2_ch14.py`
**PDF:** p.139, notes on gender of planets

The S319 agent encoded Sun, Mars, Jupiter as male planets in 3rd → brothers (BPHS1424). The notes on p.139 say: "Saturn and Rahu be treated as males while Mercury and Ketu are females." The agent noted this in commentary but didn't encode standalone rules.

**Action:**
1. Read p.139 carefully. Does the verse itself classify Saturn/Rahu as male, or only Santhanam's notes?
2. If the **verse** says it → encode two rules (Saturn in 3rd → brothers, Rahu in 3rd → brothers) following BPHS1424's pattern
3. If only **Santhanam's notes** say it → encode with `confidence` reduced by 0.05 and note in `commentary_context` that this is translator classification, not verse text (Principle #8, L013)
4. Either way, the claims exist in the source material. Encode them.

Commit: `feat(S319): encode Ch.14 Saturn/Rahu male planet variants for co-born gender`

---

## Gap 4 — Ch.12 v.5-7 possible 4th gap (INVESTIGATE — MAY NOT EXIST)

**File:** `src/corpus/bphs_v2_ch12.py`
**PDF:** p.128, v.5-7

The S318 audit said "4 gaps" but named only 3: "v.3 ascendant branch, v.5-7 Mercury/Venus paths." All 3 are now encoded. The 4th may be the "along with the Moon" conjunction variant from Santhanam's notes on p.128: "If Mercury, Jupiter or Venus be in the ascendant along with the Moon."

**Action:**
1. Read p.128. Read the existing v.5-7c rule (around line 439) which has Moon conjunction as a modifier
2. Ask: Is "benefic in ascendant WITH Moon" a distinct condition from "benefic in kendra"? The verse says "in the ascendant along with the Moon, OR be in angle from the ascendant" — these are two alternative paths
3. If the Moon-conjunction path is genuinely distinct and only captured as a modifier, promote it to a standalone rule
4. If the existing modifier adequately captures it, document why and close this gap as "covered by modifier on BPHS1210"

Do NOT fabricate a rule to hit a count. If the existing encoding covers the verse, say so.

---

## Gaps 5-8 — Ch.13 v.5 aspect paths (CANNOT ENCODE — DOCUMENT)

**File:** `src/corpus/bphs_v2_ch13.py`
**PDF:** p.133, v.5

The verse says "aspected by or conjunct by Jupiter and Venus." The conjunction paths are encoded (BPHS1307 Jupiter, BPHS1309 Venus). The aspect paths cannot be encoded because `planet_aspecting` requires a numeric house target — it can't express "Jupiter aspecting wherever lord_of_2 happens to be."

**These are genuine engine limitations, not encoding laziness.**

**Action:**
1. Verify the existing code comment (around line 307) accurately describes the limitation
2. Do NOT encode a workaround rule that fakes the aspect (e.g. using aspect to house 2 — that's wrong, the verse says aspect to the lord's position, not the house)
3. Add a one-line comment if not already present: `# ENGINE GAP: 4 aspect-path rules deferred — needs planet_aspecting to resolve lord positions`
4. Do NOT add these to any "accepted simplification" or "governance backlog" doc. They stay as code comments until a governance session adds the primitive.

No commit needed unless the comment was missing.

---

## After all gaps processed

1. Run `.venv/bin/pytest tests/ -q --tb=short -x` — all must pass
2. Run `.venv/bin/ruff check src/ tests/`
3. Report:

```
ORIGINAL GAPS: 8
ENCODED: [count] (list rule IDs)
CLOSED AS COVERED: [count] (explain why existing encoding suffices)
DEFERRED — ENGINE LIMITATION: 4 (Ch.13 aspect paths — needs new primitive)
REMAINING: [count] (should be 0 outside of engine limitations)
```

## Non-negotiable

1. Read the PDF verse BEFORE deciding whether to encode or skip
2. Do NOT weaken the existing or_group validation to make rules pass
3. Do NOT add new condition primitives — that's a governance session
4. When the verse says something and you want to skip it, you need a reason from the verse, not from your convenience
