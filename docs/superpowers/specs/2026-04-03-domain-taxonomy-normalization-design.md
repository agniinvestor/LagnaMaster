# Design Spec: Domain Taxonomy Normalization

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Approved
**Scope:** Add `primary_domain` field, normalize prediction-level domains, deprecate `outcome_domains`

## Problem

497 rules use 15 flat domains with 74 unique combinations in `outcome_domains`. Same prediction types get inconsistent domain tags ("famous" sometimes `fame_reputation`, sometimes bundled with `wealth`). This blocks meaningful aggregation and scoring. The root cause: `outcome_domains` conflates scoring axes with retrieval categories.

## Decision

Introduce `primary_domain` (exactly one per rule, from a curated 8-domain set) as the scoring axis. Prediction-level `domain` fields (already present) remain the ground truth. `outcome_domains` becomes derived (computed from prediction domains), not stored. Tags are computed on demand as `unique(prediction.domain) - {primary_domain}`.

## Primary Domain Set (8 domains)

```python
PRIMARY_DOMAINS = frozenset({
    "wealth",
    "health",
    "relationships",
    "career",
    "progeny",
    "longevity",
    "character",
    "spirituality",
})
```

### Mapping from current 15 domains → primary

| Current domain | Primary domain | Notes |
|---|---|---|
| wealth | wealth | Direct |
| physical_health | health | Direct |
| marriage | relationships | Generalized |
| career_status | career | Shortened |
| progeny | progeny | Direct |
| longevity | longevity | Direct |
| character_temperament | character | Shortened |
| spirituality | spirituality | Direct |
| fame_reputation | career (default) or wealth | Case-by-case: king/royal → career, money/gains → wealth |
| property_vehicles | wealth | Sub-type of wealth |
| intelligence_education | character (default) or career | Learning → character, professional skill → career |
| enemies_litigation | relationships (default) or character | Interpersonal → relationships, behavioral → character |
| physical_appearance | character | Trait prediction |
| mental_health | health | Health sub-type |
| foreign_travel | career or relationships | Context-dependent, rare (3 rules) |

### Selection Rule for primary_domain

Deterministic — no subjective judgment:

```
primary_domain = domain of the prediction with highest magnitude
```

**Tie-breaker** (when multiple predictions share highest magnitude):
```
Priority order: wealth > health > relationships > career > progeny > longevity > character > spirituality
```

### primary_domain must match a prediction

```
primary_domain ∈ {p["domain"] for p in predictions}
```

This means prediction-level domains must ALSO use the 8-domain primary set. The current 15-domain vocabulary in predictions needs normalization to the 8-domain set during migration.

## Schema Change

### RuleRecord

```python
# Add:
primary_domain: str = ""  # one of PRIMARY_DOMAINS

# Remove (or deprecate):
# outcome_domains is no longer stored — computed from predictions on demand
```

### Computed properties (not stored)

```python
@property
def tags(self) -> list[str]:
    """All prediction domains except primary."""
    return sorted({p["domain"] for p in self.predictions} - {self.primary_domain})

@property  
def outcome_domains(self) -> list[str]:
    """All unique prediction domains. Backward compat."""
    return sorted({p["domain"] for p in self.predictions})
```

### Builder changes

The builder currently accepts `domains=["wealth", "marriage"]` as a parameter. Change to `primary_domain="wealth"` (single string). The builder derives outcome_domains from predictions internally.

### Prediction-level domain normalization

All 15 current prediction domains map to the 8 primary domains:
```python
_DOMAIN_NORMALIZATION = {
    "wealth": "wealth",
    "physical_health": "health",
    "marriage": "relationships",
    "career_status": "career",
    "progeny": "progeny",
    "longevity": "longevity",
    "character_temperament": "character",
    "spirituality": "spirituality",
    "fame_reputation": "career",      # default; some → wealth
    "property_vehicles": "wealth",
    "intelligence_education": "character",  # default; some → career
    "enemies_litigation": "relationships",  # default; some → character
    "physical_appearance": "character",
    "mental_health": "health",
    "foreign_travel": "career",
}
```

## Builder Validation

```python
# primary_domain must be in PRIMARY_DOMAINS
if primary_domain not in PRIMARY_DOMAINS:
    error

# primary_domain must match at least one prediction's domain
pred_domains = {p["domain"] for p in predictions}
if primary_domain not in pred_domains:
    error

# All prediction domains must be in PRIMARY_DOMAINS
for p in predictions:
    if p["domain"] not in PRIMARY_DOMAINS:
        error
```

## Migration Process

1. Add `PRIMARY_DOMAINS` and `_DOMAIN_NORMALIZATION` to `taxonomy.py`
2. Update `RuleRecord` — add `primary_domain`, make `outcome_domains` a computed property
3. Update `V2ChapterBuilder` — replace `domains=` parameter with `primary_domain=`, normalize prediction domains during `add()`
4. Write migration script that:
   - Normalizes all prediction-level domains (15 → 8)
   - Computes `primary_domain` for each rule (highest magnitude prediction's domain, with tie-breaker)
   - Removes explicit `outcome_domains` from builder calls
5. Update all 16 chapter files
6. Update scorecard and audit tools to use new domain fields
7. Verify: tests, scorecard, no regression

## Files Changed

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add `PRIMARY_DOMAINS`, `_DOMAIN_NORMALIZATION` |
| `src/corpus/rule_record.py` | Add `primary_domain`, make `outcome_domains` computed |
| `src/corpus/v2_builder.py` | Replace `domains=` with `primary_domain=`, normalize prediction domains |
| `tools/v2_scorecard.py` | Update domain references |
| `tools/condition_modifier_audit.py` | Update domain references if applicable |
| `src/corpus/bphs_v2_ch*.py` (16 files) | Replace `domains=[...]` with `primary_domain="..."`, normalize prediction domains |

## Post-Migration Verification

1. Full test suite
2. Scorecard — 16/16 SHIP maintained
3. No old domain names in prediction fields
4. Every rule has exactly one `primary_domain`
5. `primary_domain` matches a prediction domain in every rule

## Future Extensions (NOT now)

- Prediction type classification (trait/event/status/health) — separate concern, Track 7+
- Hierarchical domain model — not needed; primary + derived tags is sufficient
- Domain weighting for aggregation — Track 5 (inference architecture)
