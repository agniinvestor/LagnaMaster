# Cross-Text Schema Governance

> **Status:** Active from S313. All V2 encoding sessions must follow this protocol.
> **Purpose:** Ensure rules from different texts can be automatically matched,
> concordances detected, and divergences captured structurally.

---

## Problem Statement

When BPHS Ch.24 v.55 says "5th lord in 7th → honourable, religious, progenic
happiness" and Saravali Ch.31 v.12 says "5th lord in 7th → delayed marriage,
loss of children", the system must:

1. **DETECT** these are about the same astrological configuration
2. **RECORD** that they agree on some outcomes and disagree on others
3. **QUERY** this later: "show me all rules about 5th lord in 7th, across all texts"

None of this works without a shared key.

---

## 1. Condition Fingerprint (the join key)

Every rule's `primary_condition` can be reduced to a **condition fingerprint** —
a flat string that uniquely identifies the astrological configuration being
described, independent of which text describes it.

### Derivation Algorithm

```
INPUT:  primary_condition dict (from V2ChapterBuilder._build_primary_condition)
OUTPUT: canonical string key

STEP 1: Extract planet
  - If planet starts with "h" and contains "_lord" → normalize to "lord_{N}"
    Example: "h5_lord" → "lord_5"
  - Otherwise use planet as-is, lowercased
    Example: "Jupiter" → "jupiter", "any_benefic" → "any_benefic"
  - If planet is "general" → use "general"

STEP 2: Extract placement type
  - Map to canonical short form:
    "lordship_placement"        → "in_house"
    "house"                     → "in_house"
    "sign_placement"            → "in_sign"
    "conjunction_condition"     → "conjunct"
    "conjunction_in_house"      → "conjunct_in_house"
    "aspect_condition"          → "aspecting"
    "lordship_dignity_condition"→ "dignity"
    "general_condition"         → "general"

STEP 3: Extract placement value
  - Single int    → str(value)           Example: 7 → "7"
  - List of ints  → sorted, joined       Example: [6,8,12] → "6_8_12"
  - String        → as-is, lowercased    Example: "any" → "any"
  - Absent/None   → omit entirely

STEP 4: Compose
  "{planet}.{placement_type}.{placement_value}"

  Dot separator chosen to avoid collision with underscores already
  in planet names (e.g., "any_benefic").
```

### Examples

| Rule | primary_condition | Fingerprint |
|------|------------------|-------------|
| BPHS Ch.24 v.55: 5th lord in 7th | `{planet: "h5_lord", placement_type: "lordship_placement", placement_value: 7}` | `lord_5.in_house.7` |
| Saravali Ch.31 v.12: 5th lord in 7th | (same structure) | `lord_5.in_house.7` |
| BPHS Ch.12 v.1: 1st lord in dusthana | `{planet: "h1_lord", placement_type: "lordship_placement", placement_value: [6,8,12]}` | `lord_1.in_house.6_8_12` |
| BPHS Ch.12 v.2d: benefic in kendra/trikona | `{planet: "any_benefic", placement_type: "house", placement_value: [1,4,5,7,9,10]}` | `any_benefic.in_house.1_4_5_7_9_10` |
| BPHS Ch.25 v.62: Gulika in 1st | `{planet: "general", placement_type: "general_condition"}` | `general.general` |
| Jupiter conjunct Venus | `{planet: "jupiter_venus", placement_type: "conjunction_condition"}` | `jupiter_venus.conjunct` |
| Jupiter in Aries | `{planet: "jupiter", placement_type: "sign_placement", placement_value: "aries"}` | `jupiter.in_sign.aries` |

### Key Property

**Two rules from different texts with the same fingerprint are about the same
astrological configuration.** They MUST be compared for concordance/divergence.

### Implementation

The fingerprint is **derived, not stored**. A function `compute_condition_fingerprint(rule)`
produces it at query time from `primary_condition`. This avoids schema migration
and ensures consistency — the fingerprint is always recomputable.

```python
def compute_condition_fingerprint(rule) -> str:
    """Derive canonical condition fingerprint from primary_condition."""
    pc = rule.primary_condition or {}
    planet = pc.get("planet", "general")
    ptype = pc.get("placement_type", "general_condition")
    pvalue = pc.get("placement_value")

    # Normalize planet: h5_lord → lord_5
    if planet.startswith("h") and "_lord" in planet:
        n = planet.split("_")[0][1:]  # extract number
        planet = f"lord_{n}"
    planet = planet.lower()

    # Normalize placement type
    TYPE_MAP = {
        "lordship_placement": "in_house",
        "house": "in_house",
        "sign_placement": "in_sign",
        "conjunction_condition": "conjunct",
        "conjunction_in_house": "conjunct_in_house",
        "aspect_condition": "aspecting",
        "lordship_dignity_condition": "dignity",
        "general_condition": "general",
    }
    ptype = TYPE_MAP.get(ptype, ptype)

    # Normalize value
    if pvalue is None:
        return f"{planet}.{ptype}"
    elif isinstance(pvalue, list):
        return f"{planet}.{ptype}.{'_'.join(str(v) for v in sorted(pvalue))}"
    else:
        return f"{planet}.{ptype}.{str(pvalue).lower()}"
```

---

## 2. Divergence Taxonomy

When two rules share a fingerprint but make different claims, the disagreement
has a structured TYPE. Free-form `divergence_notes` is insufficient for
machine queries.

### Divergence Types

| Type | Definition | Example |
|------|-----------|---------|
| `DIR` | **Direction conflict** — one text says favorable, other says unfavorable | BPHS: "wealthy" vs Saravali: "poverty" for same placement |
| `INT` | **Intensity difference** — same direction, different strength | Both say favorable, but BPHS says "strong", Saravali says "moderate" |
| `SCO` | **Scope difference** — same prediction, different lagna/dasha applicability | BPHS: universal. Phaladeepika: only for watery signs |
| `CON` | **Condition addition** — one text adds a condition the other doesn't state | Saravali adds "only if aspected by benefic" that BPHS omits |
| `EXC` | **Exception addition** — one text notes an exception the other ignores | BPHS: "except for Aries/Libra ascendant" |
| `ENT` | **Entity difference** — different prediction target | BPHS: about native. Jataka Parijata: about father |
| `DOM` | **Domain difference** — same config, different life area affected | BPHS: affects wealth. Saravali: affects marriage |
| `TIM` | **Timing difference** — different timing assertion | BPHS: early life. Uttara Kalamrita: middle life |
| `SIL` | **Silent** — Text B doesn't mention what Text A claims (absence, not contradiction) | BPHS has this rule; Brihat Jataka doesn't cover this chapter |

### Recording Format

In `divergence_notes`, use structured prefix:

```
"DIR:Saravali — says unfavorable for wealth where BPHS says favorable"
"CON:Phaladeepika — adds condition 'only when aspected by Jupiter'"
"INT:Brihat_Jataka — says moderate intensity where BPHS says strong"
```

Multiple divergences separated by ` | `:

```
"DIR:Saravali — unfavorable | CON:Phaladeepika — adds Jupiter aspect condition"
```

This is **machine-parseable**: split on ` | `, extract type prefix before `:`,
extract source before ` — `.

---

## 3. Cross-Text Encoding Protocol

When encoding a new text at V2 (e.g., Saravali), the encoder follows this
sequence for EVERY rule:

### Step 1: Encode the rule normally
Read the verse, create the rule with V2ChapterBuilder.

### Step 2: Compute fingerprint
Derive the condition fingerprint from the rule's conditions.

### Step 3: Query existing corpus
```python
# Pseudocode — will be a real tool
existing = corpus.find_by_fingerprint("lord_5.in_house.7")
```
This returns all existing rules (from any text) with the same fingerprint.

### Step 4: For each match, classify the relationship

Compare the NEW rule against each EXISTING rule across these dimensions:

| Dimension | Same? | Action |
|-----------|-------|--------|
| outcome_direction | Yes | Record concordance |
| outcome_direction | No | Record `DIR` divergence |
| outcome_intensity | Same | No action needed |
| outcome_intensity | Different | Record `INT` divergence |
| outcome_domains | Overlap | Concordance on overlapping domains |
| outcome_domains | Different | Record `DOM` divergence |
| lagna_scope | Same | Concordance |
| lagna_scope | Different | Record `SCO` divergence |
| entity_target | Same | No action needed |
| entity_target | Different | Record `ENT` divergence |

### Step 5: Update both rules

- **New rule**: set `concordance_texts` and `divergence_notes`
- **Existing rule**: append the new text to its `concordance_texts` or
  add to `divergence_notes`

This is BIDIRECTIONAL — both rules know about each other.

### Step 6: Never guess concordance

If you're not sure whether a match is concordant or divergent,
record it as divergent with type `SIL` and a note. False concordance
is worse than missing concordance.

---

## 4. Known Limitations (validated against 487 V2 rules)

**Validated coverage:**
- 262 unique fingerprints from 487 rules
- Ch.24 (lord-in-house): perfect — every sloka gets a unique matchable fingerprint
- Ch.12-23 (house effects): good — most rules get specific fingerprints

**Limitation 1: `general.general` bucket (93 rules)**
Ch.25 upagraha rules and misc principles all collapse to `general.general`
because they have empty conditions. Fix: add upagraha-specific condition types
to taxonomy (e.g., `{"type": "upagraha_in_house", "upagraha": "gulika", "house": 5}`)
and update the fingerprint function. Deferred until upagraha computation module is built.

**Limitation 2: `lord_X.in_house.any` collisions (30+ rules)**
Rules where house="any" with a secondary condition (dignity, aspect) share the
same fingerprint. The secondary condition differentiates them but isn't captured
in the fingerprint. Fix: append secondary condition type to fingerprint when
primary has `placement_value="any"`. Phase 2 refinement — these rules are
within BPHS and won't collide across texts since the secondary condition
is text-specific.

**Limitation 3: Compound conditions (first-condition-only)**
When a rule has 2+ conditions (lord + dignity, lord + conjunction), the
fingerprint is based on the first condition only. Compound matching requires
a secondary check against the full `conditions` list. Simple fingerprint
matching handles the cross-text join for 80%+ of cases.

- **Automated matching**: The protocol above is MANUAL (encoder does it).
  A `tools/concordance_finder.py` that automates Steps 2-5 is a future
  governance session deliverable (estimated S315-S316).

---

## 5. Enforcement

From S313 onward:

1. **New V2 rules**: `divergence_notes` must use the structured prefix format
   (`DIR:`, `INT:`, `SCO:`, etc.) — free-form notes are rejected by audit.

2. **Cross-text encoding sessions**: Must run fingerprint query before encoding.
   The audit tool will flag rules whose fingerprint matches existing rules but
   have empty `concordance_texts` and empty `divergence_notes`.

3. **Signal_group remains text-specific**: It captures what THIS text claims.
   The condition fingerprint captures what configuration is being described.
   These are different things and both are needed.

---

## 6. Migration Path for Existing Rules

The 461 existing V2 rules (BPHS Ch.12-25) are the ANCHOR text. They don't need
concordance/divergence yet because there's nothing to compare against.

When the first partner text (likely Saravali) is encoded at V2:
1. Every new Saravali rule computes its fingerprint
2. Matches against BPHS fingerprints
3. Records concordance/divergence on BOTH rules
4. The BPHS rules gain concordance data retroactively through this process

No migration of existing rules is needed. The protocol is forward-looking.
