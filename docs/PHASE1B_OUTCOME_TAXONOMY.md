# PHASE1B_OUTCOME_TAXONOMY.md — Phase 1B Outcome Taxonomy
> **Fixed vocabulary. Not extensible during encoding sessions.**
> Any outcome that cannot be mapped here requires a schema review session,
> not a mid-encoding workaround.

---

## Purpose

The outcome taxonomy ensures every Phase 1B rule's outcome is expressed in
machine-readable, analytically consistent terms. Two rules about marriage from
different texts must use the same `outcome_domains` value so they can be queried
and compared. Free-form prose in `outcome_domains` breaks this.

---

## 15 Primary Domains

These are the only valid values for `outcome_domains`. Use exact spelling, lowercase.

| Domain | Covers | Example predictions |
|--------|--------|---------------------|
| `longevity` | Length of life, life span | "grants long life", "short life", "medium life span" |
| `physical_health` | Bodily condition, disease, physical vitality | "gives disease of the stomach", "strong constitution", "prone to fevers" |
| `mental_health` | Psychological state, mind quality, emotional stability | "causes mental anxiety", "clear and calm mind", "prone to depression" |
| `wealth` | Material resources, financial prosperity, income | "gives wealth", "poverty", "sudden financial gain", "loss of money" |
| `career_status` | Profession, occupation, social standing, authority | "career in government", "success in business", "leadership role" |
| `marriage` | Spouse quality, marriage timing, marital happiness, divorce | "delays marriage", "learned spouse", "multiple marriages", "marital discord" |
| `progeny` | Children: count, quality, gender, relationship | "many sons", "daughter first", "loss of children", "devoted children" |
| `spirituality` | Religious inclination, liberation, devotion, dharmic behavior | "deeply religious", "attains liberation", "indifferent to religion" |
| `intelligence_education` | Mental acuity, learning, scholarly achievement | "highly intelligent", "mastery of scriptures", "poor education" |
| `character_temperament` | Personality, moral character, behavioral tendencies | "truthful and just", "cruel nature", "generous disposition" |
| `physical_appearance` | Body, complexion, physique, features | "tall and handsome", "dark complexion", "muscular build" |
| `foreign_travel` | Travel abroad, residence away from birthplace, exile | "lives in foreign lands", "frequent travel", "exile from homeland" |
| `enemies_litigation` | Enemies, legal disputes, opposition, debts | "victory over enemies", "legal troubles", "freedom from debt" |
| `property_vehicles` | Land, houses, conveyances, fixed assets | "owns property", "loss of land", "fine vehicles" |
| `fame_reputation` | Honor, recognition, public standing, renown | "famous and respected", "loss of reputation", "widespread fame" |

---

## Using Multiple Domains

A rule can have multiple `outcome_domains` entries. Use all that apply.

**Example:**
> "Jupiter in 7th gives a learned and wealthy spouse and a happy marriage."

```python
outcome_domains = ["marriage", "wealth"]  # spouse quality → marriage; wealthy spouse → wealth
```

**Over-tagging is worse than under-tagging.** If a domain is only tangentially
implied, do not include it. Err toward fewer, more precise domains.

---

## 4 Outcome Directions

| Value | When to use |
|-------|-------------|
| `"favorable"` | Unambiguously positive outcome stated in source |
| `"unfavorable"` | Unambiguously negative outcome stated in source |
| `"neutral"` | No significant positive or negative outcome; descriptive only |
| `"mixed"` | Source states both positive and negative aspects for same rule |

**When in doubt between favorable/mixed:** If the source text qualifies a positive
outcome with a significant negative modifier, use `"mixed"`. If the positive is
the main statement and the negative is incidental, use `"favorable"` and record
the negative in `modifiers`.

---

## 4 Outcome Intensities

| Value | When to use |
|-------|-------------|
| `"strong"` | Source uses emphatic language: "certainly", "definitely", "greatly", "much" |
| `"moderate"` | Qualified positive/negative: "somewhat", "generally", "tends to" |
| `"weak"` | Minor effect stated: "slight tendency", "small influence" |
| `"conditional"` | Intensity explicitly depends on another factor stated in `modifiers` |

**When the source does not specify intensity:** Default to `"moderate"`. Do not
use `"strong"` without explicit emphasis in the source.

---

## 5 Timing Qualifiers

| Value | When to use |
|-------|-------------|
| `"early_life"` | Source states the effect manifests before age 30 |
| `"middle_life"` | Source states the effect manifests between ages 30–60 |
| `"late_life"` | Source states the effect manifests after age 60 |
| `"dasha_dependent"` | Source states effect only during a specific dasha; also set `dasha_scope` |
| `"unspecified"` | Source does not specify timing (most rules fall here) |

Default: `"unspecified"`. Only deviate when the source explicitly states timing.

---

## Mapping Guide — Common Prose to Taxonomy

| Source text says | `outcome_domains` | `outcome_direction` | `outcome_intensity` |
|-----------------|-------------------|---------------------|---------------------|
| "gives wealth and prosperity" | `["wealth"]` | `"favorable"` | `"moderate"` |
| "causes great wealth" | `["wealth"]` | `"favorable"` | `"strong"` |
| "poverty and misery" | `["wealth"]` | `"unfavorable"` | `"strong"` |
| "delays marriage" | `["marriage"]` | `"unfavorable"` | `"moderate"` |
| "learned and beautiful spouse" | `["marriage"]` | `"favorable"` | `"moderate"` |
| "many sons" | `["progeny"]` | `"favorable"` | `"moderate"` |
| "loss of children" | `["progeny"]` | `"unfavorable"` | `"strong"` |
| "intelligent and knowledgeable" | `["intelligence_education"]` | `"favorable"` | `"moderate"` |
| "disease of the lungs" | `["physical_health"]` | `"unfavorable"` | `"moderate"` |
| "long-lived and healthy" | `["longevity", "physical_health"]` | `"favorable"` | `"moderate"` |
| "famous and respected in society" | `["fame_reputation"]` | `"favorable"` | `"moderate"` |
| "cruel and deceitful nature" | `["character_temperament"]` | `"unfavorable"` | `"moderate"` |
| "spiritual and devoted" | `["spirituality"]` | `"favorable"` | `"moderate"` |
| "government job and authority" | `["career_status"]` | `"favorable"` | `"moderate"` |
| "lives abroad" | `["foreign_travel"]` | `"neutral"` | `"moderate"` |
| "victory over enemies" | `["enemies_litigation"]` | `"favorable"` | `"moderate"` |
| "owns houses and lands" | `["property_vehicles"]` | `"favorable"` | `"moderate"` |
| "good health but mental worries" | `["physical_health", "mental_health"]` | `"mixed"` | `"moderate"` |

---

## What Requires a Schema Review (Not Encoding)

If you encounter a prediction that genuinely cannot be mapped to any of the 15 domains:
1. Do NOT invent a new domain value mid-encoding
2. Do NOT use `"other"` as a domain (it is not in the taxonomy)
3. Record the unmappable prediction in the session notes
4. After the session, evaluate whether the taxonomy requires a new domain
5. A schema review adds the domain to this file and updates `rule_record.py`

In practice, all Vedic astrological predictions map to one of these 15 domains.
The taxonomy was designed to be exhaustive for Jyotish content.
