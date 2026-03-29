# PHASE1B_CONCORDANCE_WORKFLOW.md — Real-Time Concordance Protocol
> **Follow this workflow for every Phase 1B rule before encoding it.**
> Concordance is not retroactive. It is built rule by rule during encoding.

---

## Why Real-Time

Concordance added after the fact is editorial — it reflects what the encoder
remembers about other texts. Real-time concordance reflects what the corpus
actually contains. The difference is reliability.

The corpus self-calibrates through concordance. A rule where 3 texts from
different schools and centuries independently state the same prediction has
mechanically earned high confidence. This only works if concordance is checked
before encoding, not after.

---

## The Workflow (5 Steps Per Rule)

### Step 1 — Identify the Prediction

Read the source text verse. Extract:
- The planet involved
- The placement (house / sign / nakshatra)
- The condition (dignity, aspect, conjunction if any)
- The stated outcome

**Write the `primary_condition` dict before doing anything else.**

---

### Step 2 — Query the Existing Corpus

Before writing the rule, check: does the corpus already contain a rule with the
same `primary_condition`?

The query is: "Find all rules where `primary_condition.planet` = X AND
`primary_condition.placement_type` = Y AND `primary_condition.placement_value` = Z."

In practice during encoding sessions: scan the corpus source files for the
same planet + placement combination.

---

### Step 3 — Classify the Match

**No match found:**
→ This is a primary source rule. Proceed to encoding. `concordance_texts = []`.
Leave a mental note: the next text you encode should check back to this rule.

**Match found — same prediction:**
The matched rule and this rule state materially the same outcome for the same
configuration. "Materially same" means: same `outcome_direction` and same
`outcome_domains`, even if intensity differs.

→ This is concordance. Go to Step 4a.

**Match found — different prediction:**
The matched rule and this rule state different or opposing outcomes for the same
configuration. Example: BPHS says Saturn in 7th gives a delayed but stable
marriage; Chamatkara Chintamani says Saturn in 7th destroys the marriage.

→ This is divergence. Go to Step 4b.

**Match found — different scope:**
The matched rule applies universally; this rule applies only to specific lagnas.
Or vice versa. This is not divergence — it is scope refinement.

→ Treat as a new rule (not concordance, not divergence). Set `lagna_scope`
to make the scope difference explicit. Note in `divergence_notes` that the
matched rule has a different scope.

---

### Step 4a — Record Concordance

1. Add the existing rule's source to your new rule's `concordance_texts`
2. Update the existing rule's file to add your new text to its `concordance_texts`
   (this is the two-way update — both rules point to each other)
3. Recalculate confidence for both rules using the formula in PHASE1B_RULE_CONTRACT.md

**Example:**
You are encoding Saravali Ch.14 v.8: "Jupiter in 7th gives a noble and virtuous spouse."
You find BPHS_GBC_007 already in the corpus: `{planet: Jupiter, placement_type: house, placement_value: 7}`, direction=favorable, domains=[marriage].

Your Saravali rule:
```python
concordance_texts = ["BPHS"]
```

Update BPHS_GBC_007:
```python
concordance_texts = ["Saravali"]  # add Saravali
```

If BPHS_GBC_007 already has concordance from a third text:
```python
concordance_texts = ["Saravali", "Phaladeepika"]  # add to existing list
```

---

### Step 4b — Record Divergence

Divergence is more valuable than concordance analytically. It tells you where
schools genuinely disagree — which is exactly what the corpus needs to surface.

1. Encode your new rule normally
2. Populate `divergence_notes` with:
   - The rule_id of the conflicting rule
   - What it says vs. what you're encoding
   - The school of each
3. Update the existing rule's `divergence_notes` to reference your new rule
4. Do NOT try to resolve the divergence. Record it faithfully.

**Example:**
You are encoding Chamatkara Chintamani Ch.6 v.3: "Saturn in 7th destroys marriage."
You find BPHS_GBC_XXX: `{planet: Saturn, placement_type: house, placement_value: 7}`, direction=mixed (delays but stable marriage eventually).

Your CCC rule:
```python
divergence_notes = "BPHS (BPHS_GBC_XXX) states Saturn in 7th gives delayed but ultimately stable marriage. CCC states it destroys marriage. School difference: BPHS is generic Parashari; CCC may reflect a specific lagna context."
```

Update BPHS_GBC_XXX:
```python
divergence_notes = "CCC (CCC_XXX) states Saturn in 7th destroys marriage. BPHS states delayed but stable. Divergence recorded."
```

---

### Step 5 — Encode the Rule

Now write the rule with `concordance_texts` already populated. Do not leave
concordance as a TODO. It is populated in this step or it is a contract violation.

---

## What Counts as "Same Prediction"

**Same prediction (concordance):**
- Same planet, same house/sign/nakshatra
- Same outcome domain(s)
- Same outcome direction (both favorable OR both unfavorable)
- Intensity may differ (one text says "strong", another says "moderate") — still concordance

**Different prediction (divergence):**
- Same planet, same house/sign/nakshatra
- Opposite outcome direction (one says favorable, other says unfavorable)
- Or: completely different outcome domain (one says marriage, other says wealth)

**Scope refinement (not concordance or divergence):**
- Same configuration but different lagna scope
- One rule universal, other rule only for specific lagnas
- Encode as separate rules with different `lagna_scope`; note scope difference

---

## Confidence Impact Summary

| Scenario | `concordance_texts` | Confidence |
|----------|--------------------|-----------|
| Unique source, no matches | `[]` | 0.65 (base + verse bonus) |
| Corroborated by 1 other text | `["BPHS"]` | 0.73 |
| Corroborated by 2 texts | `["BPHS", "Saravali"]` | 0.81 |
| Corroborated by 3+ texts | `["BPHS", "Saravali", "BJX"]` | 0.89+ |
| Has divergence from 1 text | (with 1 concordance) | 0.68 |

Rules in the 0.89+ range are the high-confidence anchors — these are the SHAP
model's most reliable classical features.

---

## Common Mistakes to Avoid

**Mistake 1: "I'll add concordance later."**
There is no "later." Concordance added post-encoding is editorial, not systematic.
The workflow is Step 2 → Step 3 → Step 4 → Step 5 in that order, for every rule.

**Mistake 2: Treating scope refinement as divergence.**
If BPHS says "Jupiter in 7th gives good spouse" universally and Bhavartha Ratnakara
says "For Scorpio lagna, Jupiter in 7th gives especially learned spouse" — these
are NOT divergent. The BR rule is a scope refinement. Encode it with
`lagna_scope: ["scorpio"]` and note that the BPHS rule covers the universal case.

**Mistake 3: Over-claiming concordance.**
Two rules are concordant only if they make the same specific prediction. "Jupiter
in 7th is favorable for marriage" and "Jupiter in 7th gives wealth" are NOT
concordant — different domains. Do not add one text to the other's `concordance_texts`
unless the domain AND direction match.

**Mistake 4: Not updating the existing rule.**
Concordance is bidirectional. Both rules must reference each other. If only your
new rule references the existing one, the existing rule's confidence score will
not reflect the new corroboration.
