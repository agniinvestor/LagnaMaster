# Rule Contract V2 — Single Source of Truth

All other documents (ARCHITECTURE.md, ROADMAP.md, MEMORY.md) reference this file.
Do not define rule fields elsewhere. If a field is not listed here, it does not exist.

## Field Reference

### Phase 1A Base Fields (7 mandatory)

| Field | Type | Default | Required |
|-------|------|---------|----------|
| `rule_id` | str | — | Yes |
| `source` | str | — | Yes |
| `chapter` | str | — | Yes |
| `school` | str | — | Yes |
| `category` | str | — | Yes |
| `description` | str | — | Yes |
| `confidence` | float | — | Yes, [0.0, 1.0] |
| `verse` | str | `""` | No |
| `keyword_tags` | list[str] | `[]` | No |
| `implemented` | bool | `False` | No |
| `engine_ref` | str | `""` | No |

### Phase 1B Structural Fields (V2-MANDATORY)

These fields MUST be populated for any V2 rule. Empty = contract violation.

| Field | Type | Default | V2-Mandatory | Constraint |
|-------|------|---------|-------------|------------|
| `primary_condition` | dict | `{}` | Yes | Structured: {conditions: [{type, ...}]} |
| `outcome_domains` | list[str] | `[]` | Yes | >= 1 from 15-domain taxonomy |
| `outcome_direction` | str | `""` | Yes | favorable\|unfavorable\|neutral\|mixed |
| `outcome_intensity` | str | `""` | Yes | strong\|moderate\|weak\|conditional |
| `outcome_timing` | str | `"unspecified"` | No | unspecified\|natal_permanent\|early_life\|middle_life\|late_life\|dasha_dependent |
| `verse_ref` | str | `""` | Yes | "Ch.N v.M" or "Ch.N v.M-K" format |
| `phase` | str | `"1A_representative"` | Yes | 1B_matrix\|1B_conditional\|1B_compound |
| `system` | str | `"natal"` | Yes | natal\|horary\|varshaphala\|muhurtha\|transit |
| `entity_target` | str | `"native"` | Yes | native\|father\|mother\|spouse\|children\|siblings\|general |
| `modifiers` | list[dict] | `[]` | No | May be empty if verse has no modifiers |
| `exceptions` | list[str] | `[]` | No | May be empty |
| `lagna_scope` | list[str] | `[]` | No | Empty = universal |
| `dasha_scope` | list[str] | `[]` | No | Empty = universal |
| `concordance_texts` | list[str] | `[]` | No | Empty valid if checked; list corroborating sources |
| `divergence_notes` | str | `""` | No | Empty if no divergence |

### S305 Extensions

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `prediction_type` | str | `"event"` | event\|trait\|capacity |
| `gender_scope` | str | `"universal"` | universal\|male\|female |
| `certainty_level` | str | `"definite"` | definite\|probable\|possible |
| `strength_condition` | str | `"any"` | any\|strong\|weak\|exalted\|debilitated\|own_sign\|combust\|moolatrikona |
| `house_system` | str | `"sign_based"` | sign_based\|bhava_chalita\|kp |
| `ayanamsha_sensitive` | bool | `False` | |
| `school_specific` | dict | `{}` | Non-Parashari extensions |
| `remedy` | list[str] | `[]` | |
| `evaluation_method` | str | `"placement_check"` | placement_check\|yoga_detection\|lordship_check\|dasha_activation\|transit_check |
| `last_modified_session` | str | `""` | |

### S309 Corpus Standard (Predictions + Context)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `predictions` | list[dict] | `[]` | Each: {entity, claim, domain, direction, magnitude} |
| `entity_target` | str | `"native"` | See Entity Decision below |
| `signal_group` | str | `""` | Groups rules from same chart signal |
| `commentary_context` | str | `""` | Translator notes; never empty for V2 |
| `cross_chapter_refs` | list[str] | `[]` | Links to related chapters |
| `timing_window` | dict | `{}` | {type, value?, precision?} |
| `functional_modulation` | dict | `{}` | How prediction changes by lagna functional role |
| `derived_house_chains` | list[dict] | `[]` | Bhavat bhavam: {base_house, derivative, effective_house, entity, domain} |
| `convergence_signals` | list[str] | `[]` | Independent confirming conditions |
| `rule_relationship` | dict | `{}` | {type, related_rules}; type: alternative\|addition\|override\|contrary_mirror\|mitigation |

### S311 Governance Framework

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `translator` | str | `""` | e.g., "santhanam" |
| `schema_version` | int | `2` | Must be 2 for V2 rules |
| `health_sensitive` | bool | `False` | Longevity/death predictions |
| `safety_tier` | str | `"standard"` | standard\|restricted\|research_only |
| `falsifiable` | bool | `True` | Can user confirm/deny? |
| `requires_entity_consent` | bool | `False` | Needs family member consent |
| `deprecated_reason` | str | `""` | |
| `encoding_session_context` | str | `""` | |

### Maker-Checker Protocol

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `review_status` | str | `"unreviewed"` | unreviewed\|pending\|reviewed\|disputed |
| `review_session` | str | `""` | |
| `review_notes` | str | `""` | |

---

## Granularity Definition

A **claim** is the smallest unit of prediction independently true/false for a chart.

**Produces a separate rule:**
1. Distinct condition (lagna lord in dusthana vs lagna lord conjunct malefic)
2. Different entity target (native wealthy vs father wealthy)
3. Explicit contrary stated in text ("favorable if X" AND "unfavorable if not X")
4. Modifier that CHANGES direction or magnitude (outcome flips)
5. Specific timing assertion ("at age 32" and "at age 36" = two rules)

**Does NOT produce a separate rule:**
1. Synonyms / restatements (wealthy = affluent)
2. Amplifiers that don't change direction
3. Context / explanation (goes in `commentary_context`)

## Entity Target Decision

Whose life would you examine to verify the prediction?

| Text says... | entity_target |
|---|---|
| "Native will be wealthy" | `native` |
| "Wife will not live long" | `spouse` |
| "Father will pass away" | `father` |
| "Sons will be inimical" | `children` |
| General societal effect | `general` |

## Confidence Formula (mechanical, not editorial)

```
base = 0.60
+ 0.08 x len(concordance_texts)
+ 0.05 if verse_ref populated
- 0.05 x count(divergence_sources)
capped at [0.10, 1.0]
```

## Validation Chain

1. `v2_builder.py` — enforces at build time (entity mismatch, missing fields)
2. `v2_scorecard.py` — scores at encoding time (direction, intensity, predictions structure)
3. `validate_rules.py` — checks at commit time (format, ranges, cross-field consistency)
4. `pre_push_hook.sh` — runs at push time (full test suite + ruff + docs currency)

If this document and `rule_record.py` disagree, **rule_record.py is canonical** — update this document.
