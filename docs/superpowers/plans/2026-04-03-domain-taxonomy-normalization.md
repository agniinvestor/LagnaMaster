# Domain Taxonomy Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize 497 rules from 15 flat domains to 8 primary domains with deterministic selection, prediction-level domain normalization, and computed outcome_domains.

**Architecture:** Add PRIMARY_DOMAINS to taxonomy → update RuleRecord (add primary_domain, make outcome_domains computed) → update builder (replace domains= with primary_domain=, normalize prediction domains) → write migration script with override rules → migrate all 16 chapters → update tools → verify.

**Tech Stack:** Python 3.14, pytest (existing)

**Spec:** `docs/superpowers/specs/2026-04-03-domain-taxonomy-normalization-design.md`

---

### Task 1: Add domain taxonomy constants

**Files:**
- Modify: `src/corpus/taxonomy.py`

- [ ] **Step 1: Add constants**

```python
PRIMARY_DOMAINS = frozenset({
    "wealth", "health", "relationships", "career",
    "progeny", "longevity", "character", "spirituality",
})

PRIMARY_DOMAIN_PRIORITY = [
    "wealth", "health", "relationships", "career",
    "progeny", "longevity", "character", "spirituality",
]

DOMAIN_NORMALIZATION: dict[str, str] = {
    "wealth": "wealth",
    "physical_health": "health",
    "marriage": "relationships",
    "career_status": "career",
    "progeny": "progeny",
    "longevity": "longevity",
    "character_temperament": "character",
    "spirituality": "spirituality",
    "fame_reputation": "career",
    "property_vehicles": "wealth",
    "intelligence_education": "character",
    "enemies_litigation": "relationships",
    "physical_appearance": "character",
    "mental_health": "health",
    "foreign_travel": "career",
}
```

- [ ] **Step 2: Verify**

Run: `PYTHONPATH=. .venv/bin/python -c "from src.corpus.taxonomy import PRIMARY_DOMAINS, DOMAIN_NORMALIZATION; print(f'{len(PRIMARY_DOMAINS)} primary, {len(DOMAIN_NORMALIZATION)} mappings')"`

Expected: `8 primary, 15 mappings`

- [ ] **Step 3: Commit**

```bash
git add src/corpus/taxonomy.py
git commit -m "feat: add PRIMARY_DOMAINS and DOMAIN_NORMALIZATION constants"
```

---

### Task 2: Update RuleRecord

**Files:**
- Modify: `src/corpus/rule_record.py`

- [ ] **Step 1: Add `primary_domain` field to RuleRecord dataclass**

Add after the existing `outcome_domains` field:

```python
primary_domain: str = ""
```

- [ ] **Step 2: Add computed properties**

Add to the RuleRecord class:

```python
@property
def tags(self) -> list[str]:
    """All prediction domains except primary. Derived, not stored."""
    return sorted({p.get("domain", "") for p in self.predictions} - {self.primary_domain})

@property
def computed_outcome_domains(self) -> list[str]:
    """All unique prediction domains. Derived from predictions."""
    return sorted({p.get("domain", "") for p in self.predictions})
```

- [ ] **Step 3: Commit**

```bash
git add src/corpus/rule_record.py
git commit -m "feat: add primary_domain field + computed tags/domains properties"
```

---

### Task 3: Write domain migration script

**Files:**
- Create: `tools/migrate_domains.py`

- [ ] **Step 1: Create the migration script**

```python
"""tools/migrate_domains.py — Normalize domains from 15 to 8 primary domains.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migrate_domains.py --report
"""
from __future__ import annotations
import argparse
import importlib

from src.corpus.taxonomy import (
    PRIMARY_DOMAINS, PRIMARY_DOMAIN_PRIORITY, DOMAIN_NORMALIZATION,
)

# Override rules for ambiguous domains.
# Key patterns in claim text → override domain (instead of default mapping).
_FAME_TO_WEALTH_KEYWORDS = frozenset({
    "gains", "nishka", "money", "wealthy", "affluent", "fortunes",
    "prosperity", "rich", "opulent", "gold", "grains",
})
_FAME_TO_CAREER_KEYWORDS = frozenset({
    "king", "ruler", "royal", "authority", "position", "patronage",
    "honour", "famous", "fame", "renown",
})
_EDUCATION_TO_CAREER_KEYWORDS = frozenset({
    "profession", "skill", "expertise", "livelihood", "calling",
})
_ENEMIES_TO_CHARACTER_KEYWORDS = frozenset({
    "cruel", "aggression", "wicked", "sinful", "mean_deeds",
})


def normalize_prediction_domain(old_domain: str, claim: str = "") -> str:
    """Normalize a prediction domain from 15-set to 8-set."""
    if old_domain in PRIMARY_DOMAINS:
        return old_domain

    default = DOMAIN_NORMALIZATION.get(old_domain, "character")

    # Override rules for ambiguous mappings
    if old_domain == "fame_reputation":
        claim_lower = claim.lower().replace("_", " ")
        if any(kw in claim_lower for kw in _FAME_TO_WEALTH_KEYWORDS):
            return "wealth"
        return "career"  # default for fame

    if old_domain == "intelligence_education":
        claim_lower = claim.lower().replace("_", " ")
        if any(kw in claim_lower for kw in _EDUCATION_TO_CAREER_KEYWORDS):
            return "career"
        return "character"  # default

    if old_domain == "enemies_litigation":
        claim_lower = claim.lower().replace("_", " ")
        if any(kw in claim_lower for kw in _ENEMIES_TO_CHARACTER_KEYWORDS):
            return "character"
        return "relationships"  # default

    return default


def compute_primary_domain(predictions: list[dict]) -> str:
    """Compute primary_domain from normalized predictions."""
    if not predictions:
        return "character"  # fallback

    max_mag = max(p.get("magnitude", 0.0) for p in predictions)
    candidates = [p for p in predictions if p.get("magnitude", 0.0) == max_mag]

    if len(candidates) == 1:
        return candidates[0].get("domain", "character")

    # Tie-breaker: use priority order
    for priority_domain in PRIMARY_DOMAIN_PRIORITY:
        for c in candidates:
            if c.get("domain") == priority_domain:
                return priority_domain

    return candidates[0].get("domain", "character")


def _load_all_rules():
    """Load all rules with their predictions and domains."""
    # Patch builder to allow old-format domains during loading
    from src.corpus import v2_builder
    _orig = v2_builder.V2ChapterBuilder._validate_add
    v2_builder.V2ChapterBuilder._validate_add = staticmethod(
        lambda *a, **kw: None
    )

    results = []
    chapters = [
        "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23", "24a", "24b", "24c", "25",
    ]
    for ch in chapters:
        mod = importlib.import_module(f"src.corpus.bphs_v2_ch{ch}")
        for attr in dir(mod):
            if "REGISTRY" in attr:
                reg = getattr(mod, attr)
                for r in reg.all():
                    # Normalize each prediction's domain
                    new_preds = []
                    for p in r.predictions:
                        old_d = p.get("domain", "")
                        new_d = normalize_prediction_domain(old_d, p.get("claim", ""))
                        new_preds.append({**p, "domain": new_d})

                    primary = compute_primary_domain(new_preds)
                    old_domains = r.outcome_domains

                    results.append({
                        "rule_id": r.rule_id,
                        "chapter": ch,
                        "old_domains": old_domains,
                        "new_predictions": new_preds,
                        "primary_domain": primary,
                        "tags": sorted({p["domain"] for p in new_preds} - {primary}),
                    })

    v2_builder.V2ChapterBuilder._validate_add = _orig
    return results


def report(all_rules):
    """Print normalization report."""
    from collections import Counter
    primary_dist = Counter()
    domain_changes = 0
    primary_mismatches = []

    for entry in all_rules:
        primary_dist[entry["primary_domain"]] += 1

        # Check if any prediction domains changed
        old_set = set(entry["old_domains"])
        new_set = {p["domain"] for p in entry["new_predictions"]}
        if old_set != new_set:
            domain_changes += 1

    print("=== Primary Domain Distribution ===")
    for d in ["wealth", "health", "relationships", "career",
              "progeny", "longevity", "character", "spirituality"]:
        print(f"  {d}: {primary_dist[d]}")
    print(f"\nTotal rules: {len(all_rules)}")
    print(f"Rules with domain changes: {domain_changes}")

    # Show samples of changed rules
    print("\n=== Sample Domain Changes (first 15) ===")
    count = 0
    for entry in all_rules:
        old_set = set(entry["old_domains"])
        new_set = {p["domain"] for p in entry["new_predictions"]}
        if old_set != new_set:
            print(f"  {entry['rule_id']}: {sorted(old_set)} → primary={entry['primary_domain']}, tags={entry['tags']}")
            count += 1
            if count >= 15:
                break


def main():
    parser = argparse.ArgumentParser(description="Domain normalization tool")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    all_rules = _load_all_rules()
    print(f"Loaded {len(all_rules)} rules from 16 chapters\n")

    if args.report:
        report(all_rules)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run report**

Run: `PYTHONPATH=. .venv/bin/python tools/migrate_domains.py --report`

Review distribution and sample changes.

- [ ] **Step 3: Commit**

```bash
git add tools/migrate_domains.py
git commit -m "feat: domain migration script with override rules and report mode"
```

---

### Task 4: Update V2ChapterBuilder

**Files:**
- Modify: `src/corpus/v2_builder.py`

- [ ] **Step 1: Replace `domains` parameter with `primary_domain` in `add()` method**

Find the `add()` method signature. Replace the `domains` parameter with `primary_domain: str`. Update the method body to:
- Accept `primary_domain` instead of `domains`
- Normalize all prediction domains using `DOMAIN_NORMALIZATION`
- Validate `primary_domain` is in `PRIMARY_DOMAINS`
- Validate `primary_domain` matches at least one prediction's normalized domain
- Set `outcome_domains` from normalized prediction domains (for backward compat until removal)

- [ ] **Step 2: Update domain validation**

Replace existing domain validation with:

```python
from src.corpus.taxonomy import PRIMARY_DOMAINS, DOMAIN_NORMALIZATION

if primary_domain not in PRIMARY_DOMAINS:
    errors.append(f"primary_domain='{primary_domain}' not in PRIMARY_DOMAINS")

# Normalize prediction domains
for p in predictions:
    old_d = p.get("domain", "")
    if old_d not in PRIMARY_DOMAINS:
        normalized = DOMAIN_NORMALIZATION.get(old_d)
        if normalized:
            p["domain"] = normalized
        else:
            errors.append(f"prediction domain '{old_d}' not normalizable")

# Primary must match a prediction
pred_domains = {p.get("domain", "") for p in predictions}
if primary_domain not in pred_domains:
    errors.append(f"primary_domain='{primary_domain}' not in prediction domains {pred_domains}")
```

- [ ] **Step 3: Commit**

```bash
git add src/corpus/v2_builder.py
git commit -m "feat: builder accepts primary_domain, normalizes prediction domains"
```

---

### Task 5: Migrate all 16 chapter files

**Files:**
- Modify: All 16 `src/corpus/bphs_v2_ch*.py` files

- [ ] **Step 1: For each chapter file, transform every `b.add()` call**

Replace:
```python
domains=["wealth", "marriage"],
```
with:
```python
primary_domain="wealth",
```

And normalize prediction domain values:
```python
"domain": "marriage"  →  "domain": "relationships"
"domain": "physical_health"  →  "domain": "health"
"domain": "career_status"  →  "domain": "career"
"domain": "character_temperament"  →  "domain": "character"
"domain": "fame_reputation"  →  "domain": "career"  (or "wealth" per override)
"domain": "property_vehicles"  →  "domain": "wealth"
"domain": "intelligence_education"  →  "domain": "character"  (or "career" per override)
"domain": "enemies_litigation"  →  "domain": "relationships"  (or "character" per override)
"domain": "physical_appearance"  →  "domain": "character"
"domain": "mental_health"  →  "domain": "health"
"domain": "foreign_travel"  →  "domain": "career"
```

Use the migration script's `--report` output to determine correct `primary_domain` for each rule (highest-magnitude prediction's normalized domain).

- [ ] **Step 2: Verify each chapter builds**

```bash
PYTHONPATH=. .venv/bin/python -c "
for ch in ['12','13','14','15','16','17','18','19','20','21','22','23','24a','24b','24c','25']:
    mod = __import__(f'src.corpus.bphs_v2_ch{ch}', fromlist=['x'])
    for attr in dir(mod):
        if 'REGISTRY' in attr:
            reg = getattr(mod, attr)
            print(f'Ch.{ch}: {reg.count()} rules OK')
"
```

- [ ] **Step 3: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`

- [ ] **Step 4: Verify no old domain names remain in predictions**

```bash
PYTHONPATH=. .venv/bin/python -c "
import importlib
from src.corpus.taxonomy import PRIMARY_DOMAINS
bad = 0
for ch in ['12','13','14','15','16','17','18','19','20','21','22','23','24a','24b','24c','25']:
    mod = importlib.import_module(f'src.corpus.bphs_v2_ch{ch}')
    for attr in dir(mod):
        if 'REGISTRY' in attr:
            for r in getattr(mod, attr).all():
                for p in r.predictions:
                    if p.get('domain', '') not in PRIMARY_DOMAINS:
                        print(f'  BAD: {r.rule_id} prediction domain={p[\"domain\"]}')
                        bad += 1
print(f'Non-primary prediction domains: {bad}')
"
```

Expected: `Non-primary prediction domains: 0`

- [ ] **Step 5: Commit**

```bash
git add src/corpus/bphs_v2_ch*.py
git commit -m "feat: normalize all 497 rules to 8 primary domains

Primary domain distribution: [from report]
All prediction domains normalized from 15→8
outcome_domains now derived from predictions"
```

---

### Task 6: Update scorecard and tools

**Files:**
- Modify: `tools/v2_scorecard.py`
- Modify: `tools/condition_modifier_audit.py` (if domain references exist)

- [ ] **Step 1: Update scorecard domain references**

Search for references to old domain names (e.g., `"marriage"`, `"physical_health"`, `"career_status"`) in the scorecard and update to use `PRIMARY_DOMAINS` or the new names.

- [ ] **Step 2: Update VALID_OUTCOME_DOMAINS in taxonomy**

Replace the existing `VALID_OUTCOME_DOMAINS` set with `PRIMARY_DOMAINS` (or update it to match the 8-domain set).

- [ ] **Step 3: Commit**

```bash
git add tools/v2_scorecard.py tools/condition_modifier_audit.py src/corpus/taxonomy.py
git commit -m "fix: update tools for 8-domain taxonomy"
```

---

### Task 7: Post-migration verification

- [ ] **Step 1: Full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 14,497+ passed

- [ ] **Step 2: Scorecard**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep "Ship-ready"`
Expected: `Ship-ready: 16/16 chapters`

- [ ] **Step 3: Domain distribution**

Run: `PYTHONPATH=. .venv/bin/python tools/migrate_domains.py --report 2>&1 | head -15`

Print final distribution for verification.

- [ ] **Step 4: Push**

```bash
git push
```
