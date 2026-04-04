# Legacy Migration Audit System — Design Spec

**Date:** 2026-04-04
**Session:** S314
**Status:** Approved
**Scope:** Tool + registry + gated exclusion for V1→V2 migration verification

## Problem

15 BPHS chapters (Ch.12-25, Ch.29) have both V2 rules (537) and legacy V1 rules (553). Legacy rules are Phase 1A — unstructured prose, no computable conditions, no predictions. They inflate corpus counts and create ambiguity. But they may contain claims that V2 encoding missed.

**Goal:** Prove V2 covers all V1 signal before excluding legacy. Extract signal, not structure.

## Non-Goals

- No auto-migration of V1→V2 (principle: right over easy)
- No modification of V1 rules (remain as-is for reference)
- No NLP beyond keyword matching (deterministic only)
- No domain reclassification (uses existing 8 domains)

## Architecture (3 Layers)

### Layer 1 — Audit Tool (`tools/migration_audit.py`)

**Input:** Chapter identifier (e.g., `--chapter 29`)

**Process:**
1. Load all V1 rules for `(source="BPHS", chapter="Ch.N")`
2. Load all V2 rules for the same chapter
3. Load verse audit from `data/verse_audits/chN_audit.json`
4. Extract claims from V1 prose using keyword→tag mapping
5. Extract claims from V2 structured predictions
6. Match V1 claims against V2 claims using two-tier buckets
7. Classify each V1 claim as FULL / PARTIAL / GAP_CRITICAL / GAP_PARTIAL_DOMAIN
8. Compute confidence score for extraction quality
9. Output report

**Output schema (JSON):**

```json
{
  "chapter": "Ch.29",
  "source": "BPHS",
  "audit_date": "2026-04-04",
  "v1_rules": 30,
  "v2_rules": 40,
  "v1_claims_extracted": 45,
  "v2_claims_extracted": 62,
  "matching": {
    "full": 38,
    "partial": 5,
    "gap_critical": 1,
    "gap_partial_domain": 1
  },
  "confidence": 0.92,
  "confidence_tier": "HIGH",
  "low_confidence_claims": [
    {
      "v1_rule_id": "BPHS_V1_XXXX",
      "v1_text": "life becomes difficult",
      "extracted_bucket": "health_unfavorable",
      "confidence": 0.4,
      "reason": "abstract prose, no keyword match"
    }
  ],
  "gaps": [
    {
      "type": "GAP_CRITICAL",
      "v1_rule_id": "BPHS_V1_YYYY",
      "v1_claim": "wealth_favorable + virtue",
      "nearest_v2": null,
      "action_required": "encode missing claim"
    }
  ],
  "partials": [
    {
      "v1_rule_id": "BPHS_V1_ZZZZ",
      "v1_bucket": "wealth_favorable + authority",
      "v2_bucket": "wealth_favorable",
      "missing_mechanism": "authority",
      "annotation": null
    }
  ]
}
```

**CLI output:**

```
Migration Audit — BPHS Ch.29
═══════════════════════════════
V1 rules: 30 → 45 claims extracted
V2 rules: 40 → 62 claims extracted
Confidence: 92% (HIGH)

FULL MATCH:          38 (84%)
PARTIAL:              5 (11%)  ← mechanism loss
GAP_CRITICAL:         1 ( 2%)  ← domain missing
GAP_PARTIAL_DOMAIN:   1 ( 2%)  ← partial domain coverage

Status: NOT VERIFIED (2 gaps, 5 unannotated partials)

GAPS (must fix):
  BPHS_V1_YYYY: wealth_favorable+virtue → no V2 match

PARTIALS (must annotate):
  BPHS_V1_ZZZZ: wealth_favorable+authority → V2 has wealth_favorable only

LOW CONFIDENCE (review):
  BPHS_V1_XXXX: "life becomes difficult" → health_unfavorable (conf=0.4)
```

### Layer 2 — Migration Registry (`src/corpus/migration_registry.py`)

**Purpose:** Persistent per-chapter audit state. Source of truth for exclusion decisions.

**Structure:**

```python
MIGRATION_REGISTRY: dict[tuple[str, str], dict] = {
    ("BPHS", "Ch.29"): {
        "status": "verified",       # unaudited | audited | verified
        "coverage": 1.0,
        "full_count": 38,
        "partial_count": 5,
        "gap_critical_count": 0,
        "gap_partial_count": 0,
        "confidence": 0.92,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [
            {
                "v1_rule_id": "BPHS_V1_ZZZZ",
                "reason": "V1 said 'through king', V2 says 'through authority' — acceptable abstraction",
            }
        ],
        "notes": "All V1 claims mapped or intentionally dropped with annotation",
    },
}
```

**Status transitions:**

```
unaudited → audited (tool has been run, gaps exist)
audited → verified (gaps=0, all partials annotated)
verified → exclusion activates
```

**Verification gate (must ALL be true):**
- `gap_critical_count == 0`
- `gap_partial_count == 0`
- All partials have non-empty annotations
- `confidence >= 0.7`

### Layer 3 — Gated Exclusion (`combined_corpus.py`)

**Logic:**

```python
from src.corpus.migration_registry import MIGRATION_REGISTRY

def _is_superseded(rule) -> bool:
    if rule.last_modified_session >= "S310":
        return False  # V2 rules never excluded
    key = (rule.source, rule.chapter)
    entry = MIGRATION_REGISTRY.get(key)
    if entry and entry["status"] == "verified":
        return True  # legacy excluded only after verified migration
    return False
```

**Scorecard Section P:**

```
P. MIGRATION AUDIT STATUS
  Ch.12  : VERIFIED ✅ (2026-04-04, 100%, 3 annotated partials)
  Ch.13  : AUDITED  ⚠️ (2 gaps remaining)
  Ch.14  : UNAUDITED ❌
  ...
  Verified: 5/15 chapters
  Legacy excluded: 187/553 rules
```

## Two-Tier Claim Bucketing

### Tier 1 — Domain + Direction (coarse filter, 24 buckets)

8 domains × 3 directions:

```
wealth_favorable, wealth_unfavorable, wealth_mixed
health_favorable, health_unfavorable, health_mixed
relationships_favorable, relationships_unfavorable, relationships_mixed
career_favorable, career_unfavorable, career_mixed
progeny_favorable, progeny_unfavorable, progeny_mixed
longevity_favorable, longevity_unfavorable, longevity_mixed
character_favorable, character_unfavorable, character_mixed
spirituality_favorable, spirituality_unfavorable, spirituality_mixed
```

### Tier 2 — Mechanism Tags (controlled vocabulary)

**v0.1 — 18 tags:**

```python
MECHANISM_TAGS: dict[str, list[str]] = {
    "authority":        ["king", "government", "state", "ruler", "royal"],
    "family_paternal":  ["father", "paternal", "pitru"],
    "family_maternal":  ["mother", "maternal", "matru"],
    "siblings":         ["brother", "sister", "co-born", "sibling"],
    "spouse":           ["wife", "husband", "spouse", "marriage", "marital"],
    "disputes":         ["litigation", "conflict", "quarrel", "dispute", "enemy"],
    "taxation":         ["tax", "revenue", "levy", "dues"],
    "virtue":           ["righteous", "virtuous", "dharma", "fair", "noble"],
    "deception":        ["fraud", "deception", "cheat", "questionable", "unfair"],
    "public":           ["public", "people", "masses", "popular"],
    "self_effort":      ["self", "own", "personal", "industry"],
    "digestive":        ["stomach", "digestion", "bowel", "gastric"],
    "fire_accident":    ["fire", "burn", "fever", "inflammation"],
    "reputation":       ["fame", "reputation", "honor", "respect", "status"],
    "poverty":          ["poor", "poverty", "destitute", "penury"],
    "progeny_count":    ["sons", "daughters", "children", "progeny", "issue"],
    "longevity_risk":   ["death", "die", "longevity", "lifespan", "danger"],
    "spiritual":        ["spiritual", "moksha", "liberation", "renunciation"],
}
```

**Governance rule:** No new tags without explicit approval. Tag additions must be committed with justification.

### V2 Claim Extraction (Fix 1 — must not assume mechanism is explicit)

V2 rules have structured `predictions` but mechanism is embedded in the `claim` string, not a separate field. V2 extraction uses the **same keyword mapping** as V1:

```python
def extract_v2_bucket(prediction: dict) -> dict:
    """Extract bucket from a V2 prediction dict."""
    domain = prediction["domain"]
    direction = prediction["direction"]
    claim_text = prediction.get("claim", "")

    # Infer mechanism from claim string using same keyword mapping as V1
    mechanisms = infer_mechanisms_from_text(claim_text)

    return {
        "domain_direction": f"{domain}_{direction}",
        "mechanisms": mechanisms,  # list[str], may be empty
    }
```

This ensures V1 and V2 are compared on the same extraction basis — no asymmetric advantage to V2's structure.

### Confidence Scoring (Fix 4 — includes semantic keywords)

```python
# Semantic keywords that indicate domain even without mechanism detail
SEMANTIC_KEYWORDS: dict[str, str] = {
    "wealthy": "wealth", "rich": "wealth", "poor": "wealth",
    "gains": "wealth", "loss": "wealth", "expenses": "wealth",
    "happy": "character", "miserable": "character", "adventurous": "character",
    "disease": "health", "sickly": "health", "healthy": "health",
    "fame": "career", "king": "career", "authority": "career",
    "wife": "relationships", "husband": "relationships", "marriage": "relationships",
    "sons": "progeny", "children": "progeny", "progeny": "progeny",
    "death": "longevity", "longevity": "longevity", "danger": "longevity",
    "spiritual": "spirituality", "moksha": "spirituality",
}

def extraction_confidence(text: str, extracted_domains: list[str],
                          extracted_mechanisms: list[str]) -> float:
    """How confident are we in the extraction from this text?"""
    words = text.lower().split()
    total = max(len(words), 1)

    # Count signal words (mechanism keywords + semantic keywords)
    mechanism_hits = sum(1 for w in words
                        if any(w in syns for syns in MECHANISM_TAGS.values()))
    semantic_hits = sum(1 for w in words if w in SEMANTIC_KEYWORDS)
    signal_hits = mechanism_hits + semantic_hits
    signal_density = signal_hits / total

    if signal_density >= 0.15:
        return min(0.95, 0.6 + signal_density * 2)
    elif signal_density >= 0.05:
        return 0.5 + signal_density * 2
    elif extracted_domains:
        return 0.4  # got a domain but weak signal
    else:
        return 0.2  # effectively unmapped
```

**Tiers:**
- HIGH (>= 0.8): confident extraction
- MEDIUM (0.5-0.8): review recommended
- LOW (< 0.5): manual inspection required
- UNMAPPED (< 0.3 AND no domain extracted): no confident extraction possible — must review manually

The UNMAPPED category prevents false classifications. Rather than guessing `health_unfavorable` for "life becomes difficult," the system says "I don't know" and flags for human review.

### Claim Bucket Structure (Fix 2 — multi-mechanism support)

Each claim bucket supports **multiple mechanisms** (a single V1 claim can reference more than one source/channel):

```python
{
    "domain_direction": "wealth_favorable",  # Tier 1
    "mechanisms": ["authority", "taxation"],  # Tier 2 — list, not single value
    "source_rule_id": "BPHS_V1_XXXX",
    "source_text": "gains through king and taxes",
    "confidence": 0.85,
}
```

V1 example: "wealth through king and father" → `mechanisms: ["authority", "family_paternal"]`

### Gap Classification

| Type | Meaning | Action |
|------|---------|--------|
| FULL | Domain matches AND V1 mechanisms are a subset of V2 mechanisms | None |
| PARTIAL | Domain matches, but V1 has mechanisms not in V2 | Must annotate reason |
| GAP_CRITICAL | Domain NOT in any V2 rule | Must encode or justify |
| GAP_PARTIAL_DOMAIN | Domain exists but claim is split differently | Must review |
| UNMAPPED | Extraction confidence < 0.3 and no domain | Manual review required |

### Matching Algorithm (Fix 3 — subset-based, prevents overmatching)

```python
def match_v1_to_v2(v1_bucket: dict, v2_buckets: list[dict]) -> str:
    """Match a V1 claim bucket against all V2 claim buckets.

    Uses subset matching: V1 mechanisms must be a subset of V2 mechanisms
    for a FULL match. This prevents false FULLs where V2 has extra
    mechanisms that V1 didn't claim.
    """
    v1_domain_dir = v1_bucket["domain_direction"]
    v1_mechs = set(v1_bucket.get("mechanisms", []))

    # Step 0: Unmapped check
    if v1_bucket.get("confidence", 1.0) < 0.3 and not v1_domain_dir:
        return "UNMAPPED"

    # Step 1: Domain+Direction match
    domain_matches = [b for b in v2_buckets if b["domain_direction"] == v1_domain_dir]
    if not domain_matches:
        return "GAP_CRITICAL"

    # Step 2: Mechanism match (subset-based)
    if not v1_mechs:
        # V1 has no mechanism — domain match is sufficient
        return "FULL"

    # Collect all V2 mechanisms across matching domain rules
    v2_mechs_union = set()
    for b in domain_matches:
        v2_mechs_union.update(b.get("mechanisms", []))

    if v1_mechs <= v2_mechs_union:
        # All V1 mechanisms are covered by V2
        return "FULL"
    elif v1_mechs & v2_mechs_union:
        # Some overlap but not full coverage
        return "PARTIAL"
    else:
        # Domain matches but zero mechanism overlap
        return "PARTIAL"
```

## Execution Pipeline

```
1. Encode chapter V2 (encoding session)
2. Run: tools/migration_audit.py --chapter N
3. Review output:
   - GAP_CRITICAL → encode missing claims
   - GAP_PARTIAL_DOMAIN → review split
   - PARTIAL → annotate or encode
   - LOW_CONFIDENCE → manual inspection
4. Re-run audit until gaps = 0
5. Annotate all partials with reasons
6. Update migration_registry.py: status = "verified"
7. combined_corpus.py automatically excludes legacy
8. Scorecard Section P shows verification status
```

## Files to Create/Modify

| File | Action |
|------|--------|
| `tools/migration_audit.py` | CREATE — audit tool |
| `src/corpus/migration_registry.py` | CREATE — per-chapter audit state |
| `src/corpus/migration_tags.py` | CREATE — mechanism vocabulary + extraction |
| `src/corpus/combined_corpus.py` | MODIFY — gated exclusion using registry |
| `tools/v2_scorecard.py` | MODIFY — add Section P |

## Success Criteria

1. Tool runs on any V2-upgraded chapter and produces actionable report
2. Ch.29 passes as first test case (0 gaps after fixing)
3. Registry tracks per-chapter state persistently
4. Exclusion only activates for verified chapters
5. Scorecard surfaces migration status without manual checking
6. Mechanism vocabulary is locked — no drift
