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

This is a WARNING (not blocking) because not every "if" in commentary is an unencoded condition. But it surfaces the pattern for human review.
