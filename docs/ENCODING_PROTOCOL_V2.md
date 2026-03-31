# Encoding Protocol V2 — Corpus Standard Upgrade

> **Effective S309 onward. All new encoding AND all re-encoding must follow these protocols.**
> Violations found by `corpus_audit.py` must be fixed before commit.

---

## 6 Mandatory Protocols

### Protocol Z: Verse Audit Before Encoding (PREREQUISITE)

Before encoding ANY chapter, create a verse audit file at
`data/verse_audits/chN_audit.json` by reading the PDF. The audit lists
every claim per verse using the granularity definition from
`docs/ENCODING_GRANULARITY.md`. The builder REFUSES to build a chapter
without this file.

Process: SOURCE (PDF) → AUDIT (JSON) → ENCODE (Python) → VERIFY (scorecard)
Never: SOURCE → ENCODE → CHECK

**Validation:** `V2ChapterBuilder.build()` checks for audit file existence. Missing = ValueError.

---

### Protocol A: One-Claim-One-Rule

Every specific claim in the source text produces its own rule. A verse stating
"father dies at age 16 if X" AND "father dies at age 18 if Y" produces **2 rules**.

**What is a "claim"?**
- A specific prediction about a specific entity with a specific outcome
- A timing assertion (age, dasha, event)
- A contrary-situation mirror (when text explicitly states opposite)

**What is NOT a separate claim:**
- Synonyms/restatements of the same prediction
- Context or explanation (goes in `commentary_context`)

**Validation:** `corpus_audit.py` flags rules where `len(predictions) > 3` as potential summarization.

---

### Protocol B: Contrary Mirror Generation

When the text states "In a contrary situation, opposite results will come to pass"
or equivalent, encode BOTH rules:
1. The stated favorable/unfavorable rule
2. The contrary mirror with inverted `outcome_direction`

The mirror rule gets:
```python
rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS0800"]}
```

**Validation:** Audit checks that every rule tagged `contrary_mirror` has a matching parent.

---

### Protocol C: Entity Target Mandatory

Every rule must declare WHO the prediction is about. The encoder must actively
verify — do not accept the default `"native"` without checking.

**House-based defaults (verify, don't blindly apply):**
- H9 rules: often `"father"` (but fortune rules may be `"native"`)
- H7 rules with marriage: often `"spouse"` (but partnership rules may be `"native"`)
- H5 rules with progeny: often `"children"`
- H4 rules with mother: often `"mother"`
- H3 rules with siblings: often `"siblings"`

**Keyword check:** Scan the verse for: father, mother, spouse, wife, husband,
children, sons, daughters, brother, sister, progeny, co-born.

---

### Protocol D: Commentary Inclusion

For every sloka in the Santhanam (or equivalent) translation:
1. Read the verse translation
2. Read the notes/commentary below the verse
3. If the notes contain:
   - Timing specifics → `timing_window`
   - Edge cases → `exceptions` or `commentary_context`
   - Cross-references → `cross_chapter_refs`
   - Alternative conditions → separate rule or `commentary_context`
   - Bhavat bhavam reasoning → `derived_house_chain`

The verse alone is insufficient. The commentary is where practical specificity lives.

---

### Protocol E: Computable Conditions Only

New encoding must use ONLY the 8 computable primitives in the `conditions` list
within `primary_condition`. No new yoga_label strings.

**The 8 primitives:**
| Primitive | Meaning | Example |
|-----------|---------|---------|
| `planet_in_house` | Planet X is in house N | Jupiter in 7th |
| `planet_in_sign` | Planet X is in sign S | Jupiter in Cancer |
| `planets_conjunct_in_house` | Planets X,Y in house N | Sun+Jupiter in 5th |
| `planets_conjunct` | Planets X,Y in same house | Mars+Saturn together |
| `lord_in_house` | Lord of house M in house N | 9th lord in 10th |
| `lord_in_sign` | Lord of house M in sign S | 9th lord in Pisces |
| `planet_aspecting` | Planet X aspects house N | Jupiter aspects 7th |
| `planet_dignity` | Planet X in dignity state D | Jupiter exalted |

**Compound conditions** = list of primitives AND'd together:
```python
primary_condition={
    "planet": "h9_lord",
    "placement_type": "lordship_dignity_condition",
    "conditions": [
        {"type": "lord_in_house", "lord_of": 9, "house": "any"},
        {"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"},
    ],
}
```

If a condition can't be expressed as primitives, the schema needs a new primitive —
not a new yoga_label string.

---

### Protocol F: Timing Extraction

For every verse, explicitly check: does the text state WHEN this manifests?

**Timing types:**
| Type | Example | `timing_window` |
|------|---------|-----------------|
| Specific age | "at age 32" | `{"type": "age", "value": 32, "precision": "exact"}` |
| Age range | "in 16th/18th year" | `{"type": "age_range", "value": [16, 18], "precision": "approximate"}` |
| After event | "after marriage" | `{"type": "after_event", "value": "marriage", "precision": "approximate"}` |
| Dasha period | "in Jupiter dasha" | `{"type": "dasha_period", "value": "jupiter", "precision": "approximate"}` |
| Life stage | "early life" | `{"type": "age_range", "value": [0, 30], "precision": "approximate"}` |
| Not stated | — | `{"type": "unspecified"}` or `{}` |

`"unspecified"` is acceptable ONLY when the text genuinely doesn't mention timing.

---

## `predictions` Field Contract

Each prediction in the `predictions` list is a dict with:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `entity` | str | Yes | native/father/mother/spouse/children/siblings |
| `claim` | str | Yes | Specific prediction claim (snake_case) |
| `domain` | str | Yes | From 15-domain taxonomy |
| `direction` | str | Yes | favorable/unfavorable/neutral/mixed |
| `magnitude` | float | No | 0.0-1.0 strength of this specific claim |

**Example for "Jupiter in 7th — learned, noble, virtuous spouse":**
```python
predictions=[
    {"entity": "spouse", "claim": "learned_and_noble", "domain": "marriage",
     "direction": "favorable", "magnitude": 0.8},
    {"entity": "native", "claim": "wisdom_through_marriage", "domain": "intelligence_education",
     "direction": "favorable", "magnitude": 0.6},
    {"entity": "native", "claim": "hamsa_yoga_in_kendra", "domain": "fame_reputation",
     "direction": "favorable", "magnitude": 0.7},
]
```

---

## `signal_group` Convention

Format: `{planet}_{house}_{primary_domain}` or `{lord}_in_{house}_{domain}`

**Examples:**
- `jupiter_h7_marriage` — all rules about Jupiter in 7th house affecting marriage
- `h9_lord_in_h10_career` — 9th lord in 10th house career rules
- `saturn_mars_h7_marriage` — Saturn+Mars conjunction in 7th affecting marriage

Rules in the same signal_group are NOT independent votes. The engine uses the
most specific sub-rule that fires, not the sum of all.

---

## Controlled Vocabularies

### entity_target
`native` `father` `mother` `spouse` `children` `siblings` `general`

### timing_window.type
`age` `age_range` `after_event` `dasha_period` `unspecified`

### timing_window.precision
`exact` `approximate` `unspecified`

### rule_relationship.type
`alternative` `addition` `override` `contrary_mirror`

### primary_condition.conditions[].type (8 primitives)
`planet_in_house` `planet_in_sign` `planets_conjunct_in_house`
`planets_conjunct` `lord_in_house` `lord_in_sign`
`planet_aspecting` `planet_dignity`
