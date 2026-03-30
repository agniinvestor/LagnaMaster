# PHASE1B_RULE_CONTRACT.md — Phase 1B Rule Contract
> **This document gates all Phase 1B encoding. No Phase 1B session begins without it.**
> Committed in S263. Not modifiable during encoding sessions — only in designated
> schema review sessions.

---

## What This Contract Is

Every Phase 1B rule must satisfy this contract before it is committed. A rule that
fails the contract is **rejected** — not committed, not counted, not included in
any corpus total. There are no exceptions and no partial compliance.

Phase 1A rules (S216–S262) are automatically tagged `phase: "1A_representative"` and
are exempt from this contract. They serve as the coverage index layer.

---

## Mandatory Fields

These 12 fields must be populated on every Phase 1B rule. "Populated" means a
non-empty, non-default value that carries actual information.

### 1. `primary_condition` (dict — not empty)

The structured trigger for this rule. Must be machine-parseable.

**Format:**
```python
{
    "planet": "Jupiter",          # one of: Sun Moon Mars Mercury Jupiter Venus Saturn Rahu Ketu
    "placement_type": "house",    # house | sign | nakshatra | divisional
    "placement_value": 7          # integer 1-12 for house, sign name for sign, etc.
}
```

**Valid examples:**
```python
{"planet": "Saturn", "placement_type": "house", "placement_value": 7}
{"planet": "Jupiter", "placement_type": "sign", "placement_value": "cancer"}
{"planet": "Moon", "placement_type": "nakshatra", "placement_value": "rohini"}
```

**Rejected:**
```python
{}                              # empty — not a valid condition
{"planet": "Saturn"}           # incomplete — placement missing
{"description": "Saturn in 7"} # prose — not structured
```

For compound rules (yogas, conjunctions), `primary_condition` is the dominant planet
or the condition that triggers the combination. Additional planets go in `modifiers`.

---

### 2. `modifiers` (list — may be empty list `[]` if no modifiers exist)

Conditions that change the degree or direction of the outcome. Each modifier:

```python
{
    "condition": "aspected_by_saturn",   # string describing the modifier
    "effect": "negates",                 # amplifies | negates | conditionalizes
    "strength": "strong"                 # strong | moderate | weak
}
```

`[]` is valid when the rule has no stated modifiers.
Prose modifiers buried in `description` without a corresponding structured entry
in `modifiers` are a contract violation.

---

### 3. `exceptions` (list — may be empty `[]`)

Conditions that fully cancel this rule (not just weaken it). String list.

```python
["if_lagna_lord_in_6_8_12", "if_jupiter_combust"]
```

`[]` is valid when the source text states no exceptions.

---

### 4. `outcome_domains` (list — at least one entry from taxonomy)

From `PHASE1B_OUTCOME_TAXONOMY.md`. No free-form values. Every value must appear
in the 15-domain taxonomy exactly as spelled.

```python
["marriage", "wealth"]        # valid
["spouse quality"]            # REJECTED — free-form
["marital_happiness"]         # REJECTED — not in taxonomy
```

---

### 5. `outcome_direction` (str — one of four values)

`"favorable"` | `"unfavorable"` | `"neutral"` | `"mixed"`

Empty string `""` is **rejected**. Every Phase 1B rule must state its direction.

---

### 6. `outcome_intensity` (str — one of four values)

`"strong"` | `"moderate"` | `"weak"` | `"conditional"`

`"conditional"` means the intensity depends on another factor stated in `modifiers`.
Empty string `""` is **rejected**.

---

### 7. `lagna_scope` (list — empty `[]` means universal)

Empty list = this rule applies to all lagnas.
Non-empty list = applies ONLY to the listed lagnas.

```python
[]                              # universal — valid
["scorpio", "cancer"]           # lagna-conditional — valid
["Scorpio"]                     # REJECTED — must be lowercase
```

All lagna names must be lowercase: aries, taurus, gemini, cancer, leo, virgo,
libra, scorpio, sagittarius, capricorn, aquarius, pisces.

If a rule appears in the source text as applying to a specific lagna but you
encode it as universal, that is a fidelity violation.

---

### 8. `dasha_scope` (list — empty `[]` means universal)

Empty list = applies regardless of active dasha.
Non-empty list = applies only during listed dasha lord planets.

```python
[]                              # universal
["saturn", "rahu"]             # only active in Saturn or Rahu dasha
```

---

### 9. `verse_ref` (str — chapter AND verse required)

Phase 1B requires verse-level attribution, not chapter-only.

```python
"Ch.14 v.23"      # valid
"Ch.14"           # REJECTED — chapter only
"v.23"            # REJECTED — verse without chapter
""                # REJECTED — empty
```

**Known limitation:** Verse citations are best-effort from training knowledge,
not from primary philological verification. They are navigation aids for human
verification, not independently verified citations. The corpus documentation
states this explicitly.

---

### 10. `concordance_texts` (list — populated at encoding time)

Must be checked **before** encoding. The workflow is in `PHASE1B_CONCORDANCE_WORKFLOW.md`.

Empty list `[]` is valid — it means this is a unique-source prediction (found
only in this text). But you must have run the concordance check before leaving
it empty. "I didn't check" is a contract violation.

```python
["BPHS", "Saravali"]     # corroborated — valid
[]                        # unique source, checked — valid
```

---

### 11. `phase` (str — must be one of three values)

`"1B_matrix"` | `"1B_conditional"` | `"1B_compound"`

- `1B_matrix`: systematic placement rule (planet-in-house, planet-in-sign,
  planet-in-nakshatra, functional nature table). These are the 9×12 grid rules.
- `1B_conditional`: rule that applies only to specific lagnas or dashas.
  `lagna_scope` or `dasha_scope` will be non-empty.
- `1B_compound`: rule requiring 2+ planetary conditions simultaneously (yogas,
  conjunctions, exception-override rules).

Default `"1A_representative"` is **rejected** for Phase 1B rules.

---

### 12. `system` (str — one of three values)

`"natal"` | `"horary"` | `"varshaphala"`

- `natal`: standard birth chart interpretation (default, most rules)
- `horary`: Prasna Marga rules — apply to query charts only, different causal logic
- `varshaphala`: Tajika Neelakanthi rules — apply to annual charts only

**Critical:** Rules with `system: "horary"` or `system: "varshaphala"` must NOT
be used in natal chart analysis. These systems have different house signification
logic and different strength criteria. Mixing them contaminates natal analysis.

---

## Contract Compliance Check (Verification Sessions)

After a text is fully encoded, a verification session audits:
1. **Coverage map completeness:** all sections at minimum rule count
2. **Contract compliance spot check:** 10% of rules sampled, all 12 fields checked
3. **Taxonomy consistency:** no free-form `outcome_domains` values
4. **verse_ref completeness:** all rules have chapter + verse
5. **Concordance completeness:** all rules have had concordance check run

A text is not marked complete until the verification session passes.

---

## Confidence Calibration (Phase 1B — mechanical, not editorial)

Phase 1B confidence is calculated from structure, not from the encoder's judgment:

```
base = 0.6                                      # single-text claim
concordance_bonus = 0.08 × len(concordance_texts)  # +0.08 per corroborating text
divergence_penalty = 0.05 × len(divergence_texts)  # -0.05 per disagreeing text
verse_bonus = 0.05 if verse_ref else 0.0           # verse-level citation bonus
```

`confidence = min(1.0, base + concordance_bonus + verse_bonus - divergence_penalty)`

This formula replaces the editorial judgment used in Phase 1A. A rule corroborated
by 3 texts from different schools automatically reaches confidence ≥ 0.84.

---

## What Is NOT A Contract Violation

- `divergence_notes = ""` — valid if no divergence found
- `modifiers = []` — valid if source text states no modifiers
- `exceptions = []` — valid if source text states no exceptions
- `lagna_scope = []` — valid for universal rules
- `outcome_timing = "unspecified"` — valid when timing is not stated in source

---

## Quick Reference — Contract at a Glance

| Field | Empty Allowed? | Controlled Vocabulary? |
|-------|---------------|----------------------|
| `primary_condition` | NO | Structured dict |
| `modifiers` | YES (`[]`) | `amplifies\|negates\|conditionalizes` |
| `exceptions` | YES (`[]`) | Free string |
| `outcome_domains` | NO | 15-domain taxonomy |
| `outcome_direction` | NO | 4 values |
| `outcome_intensity` | NO | 4 values |
| `outcome_timing` | YES (`"unspecified"`) | 5 values |
| `lagna_scope` | YES (`[]` = universal) | 12 lagna names, lowercase |
| `dasha_scope` | YES (`[]` = universal) | 9 planet names, lowercase |
| `verse_ref` | NO | `"Ch.N v.M"` format |
| `concordance_texts` | YES (`[]` = unique source) | Source text names |
| `phase` | NO | 3 values |
| `system` | NO | 3 values |


---

## S305 Extensions — Additional Fields

These fields were added to RuleRecord in S305 to prevent future rework.
All have backward-compatible defaults. Machine-derived at build time where possible.

| Field | Type | Default | Populated By |
|-------|------|---------|-------------|
| `prediction_type` | str | "event" | Machine: description keyword scan for trait/event words |
| `gender_scope` | str | "universal" | Machine: description scan for gendered language |
| `certainty_level` | str | "definite" | Machine: description scan for vague words (may/might) |
| `strength_condition` | str | "any" | Machine: description scan for exalted/debilitated/combust |
| `house_system` | str | "sign_based" | Manual: set during encoding per text's house system |
| `ayanamsha_sensitive` | bool | False | Auto: True when placement_type == "sign_placement" |
| `school_specific` | dict | {} | Manual: non-Parashari fields (Jaimini/KP/Lal Kitab/Nadi/Muhurtha) |
| `remedy` | list[str] | [] | Manual: remedial measures from verse |
| `evaluation_method` | str | "placement_check" | Auto: mapped from placement_type |
| `last_modified_session` | str | "" | Auto: stamped by builder function |

### New Valid Values

- `outcome_timing`: added `"natal_permanent"` for traits (personality, appearance)
- `system`: added `"transit"` and `"muhurtha"`
- `phase`: added `"1A_deprecated"` for Phase 1A rules replaced by Phase 1B

### Modifier Extraction (Machine-Enforced)

The `modifier_extractor.py` module parses conditional language from descriptions:

| Pattern | Extracted Modifier |
|---------|-------------------|
| "aspected by Saturn" | `{condition: "aspected_by_saturn", effect: "modifies", strength: "strong"}` |
| "if exalted" | `{condition: "if_exalted", effect: "amplifies", strength: "strong"}` |
| "combust" | `{condition: "if_combust", effect: "negates", strength: "moderate"}` |
| "unless retrograde" | Added to `exceptions` list |
| "neecha bhanga" | Added to `exceptions` list |

Applied automatically at build time in `combined_corpus.py`.
Pre-push dashboard shows modifier population percentage.
