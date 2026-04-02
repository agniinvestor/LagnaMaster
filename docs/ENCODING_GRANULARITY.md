# Encoding Granularity — Mechanical Definition

> A rule is the smallest unit of prediction that can be independently
> true or false for a given chart.

## What produces a SEPARATE RULE:

1. **A distinct condition** — "lagna lord in dusthana" and "lagna lord conjunct malefic" are two conditions. A chart can satisfy one without the other. Therefore they are two rules.

2. **A distinct outcome for a different entity** — "native is wealthy" and "father is wealthy" are two rules even if they share a condition.

3. **A contrary stated in the text** — "favorable if X" and "unfavorable if not X" are two rules when the text explicitly states both.

4. **A modifier that changes the prediction's direction or magnitude** — "diseases will follow" but "if the planet is benefic or exalted, relief over time" is a separate conditional rule, not just a modifier field. The modifier CHANGES the outcome from unfavorable to mixed/conditional.

5. **A specific timing assertion** — "at age 32" produces a rule with timing_window. If the same verse also says "at age 36 if different condition," that's a second rule.

## What does NOT produce a separate rule:

1. **Synonyms/restatements** — "wealthy" and "affluent" in the same sentence about the same condition = one rule.

2. **Amplifiers that don't change direction** — "if aspected by benefic, even more favorable" is a modifier on the existing rule, not a new rule. The direction stays favorable.

3. **Context or explanation** — "this is because the 9th house rules fortune" goes in commentary.

## Test: BPHS Ch.12 v.1-2

The text says:
- (a) Lagna lord in 6/8/12 → physical felicity diminishes
- (b) Lagna lord in kendra/trikona → felicity
- (c) Lagna lord debilitated/combust/enemy sign → diseases
- (d) Benefic in angle/trine → diseases disappear

Santhanam's notes add:
- (e) Lagna lord conjunct malefic in evil house → dire defect in health AND luck/progress
- (f) If lagna lord is benefic or exalted → relief in course of time
- (g) Benefic in kendra/trikona → powerful remedy for all health ills

Applying the granularity definition:
- (a) and (b) are contrary pairs → 2 rules ✓ (already BPHS1200, BPHS1201)
- (c) is a distinct condition from (a) — debilitation ≠ dusthana placement → 1 rule ✓ (already BPHS1202)
- (d) is a distinct condition → 1 rule ✓ (already BPHS1203)
- (e) is a distinct condition — "conjunct malefic" is independent of "in dusthana" → 1 NEW rule
- (f) CHANGES the direction from unfavorable to conditional/mixed → 1 NEW rule (not just a modifier)
- (g) is a restatement/amplification of (d) → NOT a new rule (goes in commentary of BPHS1203)

**Result: 6 rules from v.1-2 (currently 4, need 2 more)**

## Entity Target — Who Is the Prediction About?

Every rule must answer: **whose fate or behavior is being predicted?**

The `entity_target` field is NOT "who is mentioned in the description." It is
"who would confirm or deny this prediction from their own experience."

### Decision rule

Ask: "If I wanted to verify this prediction, whose life would I examine?"

| The verse says... | Whose life to examine? | entity_target |
|-------------------|----------------------|---------------|
| "Native will be wealthy" | Native | `native` |
| "Wife will not live long" | Spouse | `spouse` |
| "Sons will be hostile to native" | Children | `children` |
| "Father will pass away in childhood" | Father | `father` |
| "Mother will be sickly" | Mother | `mother` |
| "Co-born destroyed" | Siblings | `siblings` |
| "Dual lordship results nullified" | No specific person | `general` |

### Common mistakes

- **"Native will have many sons"** → entity_target = `native`. The prediction is
  about the native's life experience. You would verify by asking the native.

- **"Sons will be inimical to native"** → entity_target = `children`. The prediction
  is about the children's behavior. You would verify by observing the children.

- **"Wife not under his control"** → entity_target = `spouse`. The prediction is
  about the spouse's behavior/disposition.

- **"Paternal happiness"** → entity_target = `native`. This describes the native's
  experience of their father, not a prediction about the father's own life.

- **"Father will die early"** → entity_target = `father`. This IS about the father's
  fate. You would verify by checking whether the father died early.

### When NOT to use 'general'

`general` means "this rule is a structural principle or methodological note, not a
prediction about any specific person." Examples: bhavat bhavam principle, dual
lordship resolution rules, visible/invisible half principle.

`general` is NOT a default for "I'm not sure" or "multiple entities mentioned."
If the verse predicts something about a specific entity, use that entity. If the
verse makes predictions about two different entities, it should be TWO rules
(per granularity principle #2).

## The Mechanical Check

For every rule, scan its `commentary_context` for:
- Conditional keywords: "if", "should", "provided", "in case", "when"
- Exception keywords: "unless", "except", "but if", "however", "relief"
- Separate condition keywords: "conjunct", "together with", "along with"

If these keywords are found AND the rule has no corresponding:
- Entry in `modifiers` for amplifiers
- Entry in `exceptions` for exceptions  
- Sibling rule for distinct conditions

Then flag as: "Commentary contains unencoded condition — review for missing rule or modifier."

This is a BLOCKING check at Step 2B (audit review). Every flagged keyword must be resolved — either a corresponding audit claim exists, or the auditor documents why it is not a separate claim (e.g., "restatement of claim X"). Unresolved flags block encoding.

## Condition vs Modifier vs Exception — Decision Rule

> If the commentary says the condition is **required** for the prediction to hold, it's a **condition**.
> If the commentary says the condition **strengthens, weakens, or contextualizes** an already-valid prediction, it's a **modifier**.
> If the commentary says the condition **completely cancels** the prediction, it's an **exception**.

### Mechanical Test

| Question | If yes | If no |
|----------|--------|-------|
| "Does the prediction fire WITHOUT this factor?" | modifier | condition |
| "Does this factor CANCEL the prediction entirely?" | exception | not an exception |
| "Is this factor REQUIRED by the text (must/necessary/enumerates)?" | condition | use first question |

### Anti-Patterns (DO NOT do these)

- `"house": "any"` — use `planet_in_sign_type` with appropriate `sign_type`
- Required conditions as modifiers — if commentary says "must" / "necessary" / enumerates as (a)(b)(c), these are conditions
- Empty `exceptions` when commentary says "nullified" / "cancelled" — encode the cancellation clause
- `conditions=[]` for upagrahas — use `upagraha_in_house`
- `conditions=[]` for derived houses — use `planet_in_derived_house`

### Derived House Conditions (Ch.29+)

For rules referencing houses counted from Arudha Pada, Upa Pada, Karakamsa, or other derived points:

```python
{"type": "planet_in_derived_house", "derivation": "arudha_pada",
 "base_house": 1, "offset": 7, "planet": "rahu", "mode": "occupies"}
```

- `derivation`: which derived system (arudha_pada, upa_pada, karakamsa, navamsa_lagna, etc.)
- `base_house`: which house's pada (1-12). Required for arudha_pada and upa_pada.
- `offset`: house counted from the derived anchor (1-12)
- `mode`: "occupies" (default) or "aspects"
