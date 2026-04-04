# Legacy Migration Audit System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tool that validates V2 encoding covers all V1 legacy signal before excluding legacy rules from the execution corpus.

**Architecture:** Three layers — (1) `migration_tags.py` for claim extraction from prose/structured rules using keyword→tag mapping, (2) `migration_audit.py` CLI tool that loads V1+V2 rules, extracts claims, matches using two-tier buckets, outputs per-chapter report, (3) `migration_registry.py` for persistent per-chapter audit state that gates legacy exclusion in `combined_corpus.py`.

**Tech Stack:** Python 3.14, pytest, argparse, JSON output. No external NLP dependencies — deterministic keyword matching only.

**Spec:** `docs/superpowers/specs/2026-04-04-legacy-migration-audit-design.md`

---

## File Structure

| File | Responsibility |
|------|---------------|
| `src/corpus/migration_tags.py` | Mechanism vocabulary, domain keywords, claim extraction from text |
| `src/corpus/migration_registry.py` | Per-chapter audit state (unaudited→audited→verified) |
| `tools/migration_audit.py` | CLI tool: load rules, extract, match, report |
| `src/corpus/combined_corpus.py` | Gated exclusion using registry status |
| `tools/v2_scorecard.py` | Section P: migration audit status display |
| `tests/test_migration_tags.py` | Unit tests for extraction |
| `tests/test_migration_audit.py` | Integration tests for matching + reporting |

---

### Task 1: Mechanism Vocabulary + Claim Extraction (`migration_tags.py`)

**Files:**
- Create: `src/corpus/migration_tags.py`
- Test: `tests/test_migration_tags.py`

- [ ] **Step 1: Write failing tests for domain extraction from prose**

```python
# tests/test_migration_tags.py
"""Tests for migration claim extraction."""
from __future__ import annotations


def test_extract_domains_from_wealth_text():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("native will be wealthy and famous")
    domains = {c["domain_direction"] for c in claims}
    assert "wealth_favorable" in domains


def test_extract_domains_from_health_text():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("native suffers from stomach disorders")
    domains = {c["domain_direction"] for c in claims}
    assert "health_unfavorable" in domains


def test_extract_mechanism_authority():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("loss of wealth through the king")
    assert any("authority" in c.get("mechanisms", []) for c in claims)


def test_extract_multiple_mechanisms():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("wealth through king and father")
    mechs = set()
    for c in claims:
        mechs.update(c.get("mechanisms", []))
    assert "authority" in mechs
    assert "family_paternal" in mechs


def test_extract_mixed_direction():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("wealthy but through questionable means")
    domains = {c["domain_direction"] for c in claims}
    assert "wealth_favorable" in domains or "wealth_mixed" in domains


def test_unmapped_text_low_confidence():
    from src.corpus.migration_tags import extract_claims
    claims = extract_claims("life becomes difficult in many ways")
    assert all(c.get("confidence", 1.0) < 0.5 for c in claims) or len(claims) == 0


def test_extract_v2_prediction():
    from src.corpus.migration_tags import extract_v2_bucket
    pred = {"domain": "wealth", "direction": "favorable",
            "claim": "wealthy_through_virtuous_means"}
    bucket = extract_v2_bucket(pred)
    assert bucket["domain_direction"] == "wealth_favorable"
    assert "virtue" in bucket["mechanisms"]


def test_mechanism_tags_frozen():
    """Mechanism tags should not be modified at runtime."""
    from src.corpus.migration_tags import MECHANISM_TAGS
    assert isinstance(MECHANISM_TAGS, dict)
    assert "authority" in MECHANISM_TAGS
    assert len(MECHANISM_TAGS) == 18
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_migration_tags.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `migration_tags.py`**

```python
# src/corpus/migration_tags.py
"""Mechanism vocabulary and claim extraction for migration audit.

Extracts two-tier claim buckets from both V1 prose descriptions and
V2 structured predictions using deterministic keyword matching.
No NLP dependencies — pure keyword→tag mapping.

Governance: MECHANISM_TAGS is a controlled vocabulary. No new tags
without explicit approval. Tag additions must be committed with
justification in the commit message.
"""
from __future__ import annotations

# ── Tier 2: Mechanism Tags (v0.1 — 18 tags) ────────────────────────────
MECHANISM_TAGS: dict[str, list[str]] = {
    "authority":        ["king", "government", "state", "ruler", "royal"],
    "family_paternal":  ["father", "paternal", "pitru"],
    "family_maternal":  ["mother", "maternal", "matru"],
    "siblings":         ["brother", "sister", "co-born", "sibling", "coborn"],
    "spouse":           ["wife", "husband", "spouse", "marriage", "marital"],
    "disputes":         ["litigation", "conflict", "quarrel", "dispute", "enemy", "enemies"],
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

# ── Semantic keywords for domain + direction extraction ─────────────────
# Maps keyword → (domain, direction)
_DOMAIN_KEYWORDS: dict[str, tuple[str, str]] = {
    # Wealth
    "wealthy": ("wealth", "favorable"), "rich": ("wealth", "favorable"),
    "gains": ("wealth", "favorable"), "affluent": ("wealth", "favorable"),
    "prosperous": ("wealth", "favorable"), "income": ("wealth", "favorable"),
    "poor": ("wealth", "unfavorable"), "poverty": ("wealth", "unfavorable"),
    "loss": ("wealth", "unfavorable"), "expenses": ("wealth", "unfavorable"),
    "destitute": ("wealth", "unfavorable"), "penury": ("wealth", "unfavorable"),
    # Health
    "disease": ("health", "unfavorable"), "sickly": ("health", "unfavorable"),
    "disorders": ("health", "unfavorable"), "ailment": ("health", "unfavorable"),
    "healthy": ("health", "favorable"),
    # Character
    "happy": ("character", "favorable"), "happiness": ("character", "favorable"),
    "adventurous": ("character", "favorable"), "intelligent": ("character", "favorable"),
    "miserable": ("character", "unfavorable"), "wicked": ("character", "unfavorable"),
    # Career
    "fame": ("career", "favorable"), "famous": ("career", "favorable"),
    "king": ("career", "favorable"), "authority": ("career", "favorable"),
    "ruler": ("career", "favorable"), "poet": ("career", "favorable"),
    "speaker": ("career", "favorable"),
    # Relationships
    "wife": ("relationships", "favorable"), "husband": ("relationships", "favorable"),
    "marriage": ("relationships", "favorable"), "marital": ("relationships", "favorable"),
    "amity": ("relationships", "favorable"),
    "enmity": ("relationships", "unfavorable"), "divorce": ("relationships", "unfavorable"),
    # Progeny
    "sons": ("progeny", "favorable"), "children": ("progeny", "favorable"),
    "progeny": ("progeny", "favorable"), "barren": ("progeny", "unfavorable"),
    # Longevity
    "death": ("longevity", "unfavorable"), "die": ("longevity", "unfavorable"),
    "longevity": ("longevity", "favorable"), "danger": ("longevity", "unfavorable"),
    # Spirituality
    "spiritual": ("spirituality", "favorable"), "moksha": ("spirituality", "favorable"),
    "renunciation": ("spirituality", "favorable"),
}

# Negation words that flip direction
_NEGATION_WORDS = {"not", "no", "without", "devoid", "bereft", "loss", "lack",
                   "diminished", "reduced", "denied"}


def _infer_mechanisms(text: str) -> list[str]:
    """Extract mechanism tags from text using keyword matching."""
    words = text.lower().split()
    # Also check bigrams for compound terms like "co-born"
    text_lower = text.lower()
    found: list[str] = []
    for tag, keywords in MECHANISM_TAGS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(tag)
    return found


def _infer_domains(text: str) -> list[tuple[str, str]]:
    """Extract (domain, direction) pairs from text."""
    words = text.lower().replace(",", " ").replace(".", " ").split()
    found: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    # Check for negation context (simple window-based)
    has_negation = bool(_NEGATION_WORDS & set(words))

    for word in words:
        if word in _DOMAIN_KEYWORDS:
            domain, direction = _DOMAIN_KEYWORDS[word]
            # Flip direction if negation detected near domain keyword
            if has_negation and direction == "favorable":
                direction = "unfavorable"
            elif has_negation and direction == "unfavorable":
                direction = "favorable"
            pair = (domain, direction)
            if pair not in seen:
                found.append(pair)
                seen.add(pair)
    return found


def _extraction_confidence(text: str, domains: list[tuple[str, str]],
                           mechanisms: list[str]) -> float:
    """Confidence score for claim extraction quality."""
    words = text.lower().split()
    total = max(len(words), 1)

    mechanism_hits = sum(1 for w in words
                        if any(w in syns for syns in MECHANISM_TAGS.values()))
    semantic_hits = sum(1 for w in words if w in _DOMAIN_KEYWORDS)
    signal_hits = mechanism_hits + semantic_hits
    signal_density = signal_hits / total

    if signal_density >= 0.15:
        return min(0.95, 0.6 + signal_density * 2)
    elif signal_density >= 0.05:
        return 0.5 + signal_density * 2
    elif domains:
        return 0.4
    else:
        return 0.2


def extract_claims(text: str) -> list[dict]:
    """Extract claim buckets from prose text (V1 rules).

    Returns list of claim dicts, each with:
        domain_direction: str  (e.g., "wealth_favorable")
        mechanisms: list[str]  (e.g., ["authority", "taxation"])
        confidence: float      (0.0 - 1.0)
        source_text: str       (original text)
    """
    domains = _infer_domains(text)
    mechanisms = _infer_mechanisms(text)
    confidence = _extraction_confidence(text, domains, mechanisms)

    if not domains:
        # UNMAPPED — no domain confidently extracted
        return [{"domain_direction": "", "mechanisms": mechanisms,
                 "confidence": confidence, "source_text": text}]

    claims: list[dict] = []
    for domain, direction in domains:
        claims.append({
            "domain_direction": f"{domain}_{direction}",
            "mechanisms": mechanisms,
            "confidence": confidence,
            "source_text": text,
        })
    return claims


def extract_v2_bucket(prediction: dict) -> dict:
    """Extract bucket from a V2 prediction dict.

    Uses same keyword mapping as V1 to ensure symmetric comparison.
    """
    domain = prediction.get("domain", "")
    direction = prediction.get("direction", "")
    claim_text = prediction.get("claim", "")

    mechanisms = _infer_mechanisms(claim_text)

    return {
        "domain_direction": f"{domain}_{direction}" if domain else "",
        "mechanisms": mechanisms,
        "confidence": 0.95,  # V2 has structured domain/direction — high confidence
        "source_text": claim_text,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_migration_tags.py -v`
Expected: ALL PASS

- [ ] **Step 5: Lint check**

Run: `.venv/bin/ruff check src/corpus/migration_tags.py tests/test_migration_tags.py`
Expected: All checks passed

- [ ] **Step 6: Commit**

```bash
git add src/corpus/migration_tags.py tests/test_migration_tags.py
git commit -m "feat: migration claim extraction — keyword→tag mapping for V1/V2 comparison"
```

---

### Task 2: Matching Engine + Migration Audit Tool (`migration_audit.py`)

**Files:**
- Create: `tools/migration_audit.py`
- Test: `tests/test_migration_audit.py`

- [ ] **Step 1: Write failing tests for matching logic**

```python
# tests/test_migration_audit.py
"""Tests for migration audit matching and reporting."""
from __future__ import annotations


def test_match_full_domain_and_mechanism():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable", "mechanisms": ["authority"], "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": ["authority", "virtue"]}]
    assert match_v1_to_v2(v1, v2s) == "FULL"


def test_match_partial_mechanism_missing():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable", "mechanisms": ["authority", "taxation"], "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "PARTIAL"


def test_match_gap_critical_no_domain():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "health_unfavorable", "mechanisms": ["digestive"], "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "GAP_CRITICAL"


def test_match_unmapped_low_confidence():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "", "mechanisms": [], "confidence": 0.2}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": []}]
    assert match_v1_to_v2(v1, v2s) == "UNMAPPED"


def test_match_full_no_mechanisms():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable", "mechanisms": [], "confidence": 0.8}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "FULL"


def test_audit_chapter_returns_report():
    from tools.migration_audit import audit_chapter
    report = audit_chapter("BPHS", "Ch.29")
    assert report["chapter"] == "Ch.29"
    assert "matching" in report
    assert report["v1_rules"] >= 0
    assert report["v2_rules"] >= 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_migration_audit.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `migration_audit.py`**

```python
#!/usr/bin/env python3
"""tools/migration_audit.py — Legacy V1→V2 migration audit tool.

Compares V1 legacy rules against V2 structured rules for a given chapter.
Extracts claims from both using two-tier bucketing (domain+direction +
mechanism tags), then matches to find FULL/PARTIAL/GAP/UNMAPPED.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29 --json
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --all
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from src.corpus.migration_tags import extract_claims, extract_v2_bucket


def _load_rules(source: str, chapter: str):
    """Load all rules for a source+chapter from combined corpus."""
    from src.corpus.combined_corpus import build_corpus
    corpus = build_corpus()
    v1, v2 = [], []
    for r in corpus.all():
        if r.source != source or r.chapter != chapter:
            continue
        if r.last_modified_session >= "S310":
            v2.append(r)
        else:
            v1.append(r)
    return v1, v2


def match_v1_to_v2(v1_bucket: dict, v2_buckets: list[dict]) -> str:
    """Match a single V1 claim bucket against all V2 claim buckets.

    Uses subset matching: V1 mechanisms must be a subset of V2 mechanisms
    for a FULL match.
    """
    v1_domain_dir = v1_bucket.get("domain_direction", "")
    v1_mechs = set(v1_bucket.get("mechanisms", []))
    confidence = v1_bucket.get("confidence", 1.0)

    # Step 0: Unmapped check
    if confidence < 0.3 and not v1_domain_dir:
        return "UNMAPPED"

    # Step 1: Domain+Direction match
    if not v1_domain_dir:
        return "UNMAPPED"

    domain_matches = [b for b in v2_buckets if b["domain_direction"] == v1_domain_dir]
    if not domain_matches:
        return "GAP_CRITICAL"

    # Step 2: Mechanism match (subset-based)
    if not v1_mechs:
        return "FULL"

    v2_mechs_union: set[str] = set()
    for b in domain_matches:
        v2_mechs_union.update(b.get("mechanisms", []))

    if v1_mechs <= v2_mechs_union:
        return "FULL"
    elif v1_mechs & v2_mechs_union:
        return "PARTIAL"
    else:
        return "PARTIAL"


def audit_chapter(source: str, chapter: str) -> dict:
    """Run migration audit for a single chapter. Returns report dict."""
    v1_rules, v2_rules = _load_rules(source, chapter)

    # Extract V1 claims
    v1_claims: list[dict] = []
    for r in v1_rules:
        claims = extract_claims(r.description)
        for c in claims:
            c["v1_rule_id"] = r.rule_id
            v1_claims.append(c)

    # Extract V2 claims
    v2_buckets: list[dict] = []
    for r in v2_rules:
        for pred in r.predictions:
            bucket = extract_v2_bucket(pred)
            bucket["v2_rule_id"] = r.rule_id
            v2_buckets.append(bucket)

    # Match
    results = {"FULL": 0, "PARTIAL": 0, "GAP_CRITICAL": 0, "UNMAPPED": 0}
    gaps: list[dict] = []
    partials: list[dict] = []
    unmapped: list[dict] = []
    low_confidence: list[dict] = []

    for v1c in v1_claims:
        result = match_v1_to_v2(v1c, v2_buckets)
        results[result] = results.get(result, 0) + 1

        if result == "GAP_CRITICAL":
            gaps.append({
                "type": "GAP_CRITICAL",
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_claim": v1c["domain_direction"],
                "v1_mechanisms": v1c.get("mechanisms", []),
                "v1_text": v1c.get("source_text", "")[:200],
            })
        elif result == "PARTIAL":
            v1_mechs = set(v1c.get("mechanisms", []))
            v2_mechs_union: set[str] = set()
            for b in v2_buckets:
                if b["domain_direction"] == v1c["domain_direction"]:
                    v2_mechs_union.update(b.get("mechanisms", []))
            missing = v1_mechs - v2_mechs_union
            partials.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_bucket": v1c["domain_direction"],
                "v1_mechanisms": list(v1_mechs),
                "v2_mechanisms": list(v2_mechs_union),
                "missing_mechanisms": list(missing),
                "annotation": None,
            })
        elif result == "UNMAPPED":
            unmapped.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_text": v1c.get("source_text", "")[:200],
                "confidence": v1c.get("confidence", 0),
            })

        if v1c.get("confidence", 1.0) < 0.5 and result != "UNMAPPED":
            low_confidence.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_text": v1c.get("source_text", "")[:200],
                "extracted_bucket": v1c["domain_direction"],
                "confidence": v1c.get("confidence", 0),
            })

    total_claims = sum(results.values())
    coverage = (results["FULL"] / total_claims) if total_claims > 0 else 0.0
    avg_confidence = (
        sum(c.get("confidence", 0) for c in v1_claims) / len(v1_claims)
        if v1_claims else 0.0
    )

    # Confidence tier
    if avg_confidence >= 0.8:
        conf_tier = "HIGH"
    elif avg_confidence >= 0.5:
        conf_tier = "MEDIUM"
    else:
        conf_tier = "LOW"

    return {
        "chapter": chapter,
        "source": source,
        "audit_date": str(date.today()),
        "v1_rules": len(v1_rules),
        "v2_rules": len(v2_rules),
        "v1_claims_extracted": len(v1_claims),
        "v2_claims_extracted": len(v2_buckets),
        "matching": {
            "full": results["FULL"],
            "partial": results["PARTIAL"],
            "gap_critical": results["GAP_CRITICAL"],
            "unmapped": results["UNMAPPED"],
        },
        "confidence": round(avg_confidence, 2),
        "confidence_tier": conf_tier,
        "gaps": gaps,
        "partials": partials,
        "unmapped": unmapped,
        "low_confidence": low_confidence,
    }


def format_report(report: dict) -> str:
    """Format audit report as CLI text."""
    ch = report["chapter"]
    lines = [
        f"Migration Audit — BPHS {ch}",
        "=" * 40,
        f"V1 rules: {report['v1_rules']} → {report['v1_claims_extracted']} claims extracted",
        f"V2 rules: {report['v2_rules']} → {report['v2_claims_extracted']} claims extracted",
        f"Confidence: {report['confidence']:.0%} ({report['confidence_tier']})",
        "",
    ]

    m = report["matching"]
    total = sum(m.values())
    for key in ("full", "partial", "gap_critical", "unmapped"):
        count = m[key]
        pct = f"{count / total * 100:.0f}%" if total > 0 else "0%"
        label = key.upper().replace("_", " ")
        marker = ""
        if key == "gap_critical" and count > 0:
            marker = "  ← domain missing"
        elif key == "partial" and count > 0:
            marker = "  ← mechanism loss"
        elif key == "unmapped" and count > 0:
            marker = "  ← manual review"
        lines.append(f"  {label:20s}: {count:4d} ({pct:>4s}){marker}")

    # Status
    has_gaps = m["gap_critical"] > 0
    unannotated = sum(1 for p in report["partials"] if not p.get("annotation"))
    if has_gaps or unannotated > 0:
        reasons = []
        if has_gaps:
            reasons.append(f"{m['gap_critical']} gaps")
        if unannotated:
            reasons.append(f"{unannotated} unannotated partials")
        lines.append(f"\nStatus: NOT VERIFIED ({', '.join(reasons)})")
    else:
        lines.append("\nStatus: VERIFIED ✅")

    if report["gaps"]:
        lines.append("\nGAPS (must fix):")
        for g in report["gaps"]:
            lines.append(f"  {g['v1_rule_id']}: {g['v1_claim']} → no V2 match")
            if g.get("v1_text"):
                lines.append(f"    text: {g['v1_text'][:100]}")

    if report["partials"]:
        lines.append("\nPARTIALS (must annotate):")
        for p in report["partials"]:
            missing = ", ".join(p.get("missing_mechanisms", []))
            lines.append(f"  {p['v1_rule_id']}: {p['v1_bucket']} missing [{missing}]")

    if report["unmapped"]:
        lines.append("\nUNMAPPED (manual review):")
        for u in report["unmapped"]:
            lines.append(f"  {u['v1_rule_id']}: \"{u['v1_text'][:80]}\" (conf={u['confidence']:.2f})")

    if report["low_confidence"]:
        lines.append("\nLOW CONFIDENCE (review):")
        for lc in report["low_confidence"]:
            lines.append(f"  {lc['v1_rule_id']}: \"{lc['v1_text'][:80]}\" → {lc['extracted_bucket']} (conf={lc['confidence']:.2f})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Legacy V1→V2 Migration Audit")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chapter", help="Chapter number (e.g., 29)")
    group.add_argument("--all", action="store_true", help="Audit all V2-upgraded chapters")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--source", default="BPHS", help="Source text (default: BPHS)")

    args = parser.parse_args()

    if args.chapter:
        chapters = [f"Ch.{args.chapter}"]
    else:
        # All V2-upgraded chapters
        chapters = [f"Ch.{n}" for n in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29]]

    for ch in chapters:
        report = audit_chapter(args.source, ch)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_report(report))
            print()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_migration_audit.py -v`
Expected: ALL PASS

- [ ] **Step 5: Run the tool on Ch.29 as smoke test**

Run: `PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29`
Expected: CLI report showing V1 claims matched against V2

- [ ] **Step 6: Lint check**

Run: `.venv/bin/ruff check tools/migration_audit.py tests/test_migration_audit.py`
Expected: All checks passed

- [ ] **Step 7: Commit**

```bash
git add tools/migration_audit.py tests/test_migration_audit.py
git commit -m "feat: migration audit tool — V1→V2 claim matching with two-tier buckets"
```

---

### Task 3: Migration Registry (`migration_registry.py`)

**Files:**
- Create: `src/corpus/migration_registry.py`
- Test: `tests/test_migration_registry.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_migration_registry.py
"""Tests for migration registry."""
from __future__ import annotations


def test_registry_initial_state():
    from src.corpus.migration_registry import get_status
    # Unaudited chapters return default
    status = get_status("BPHS", "Ch.99")
    assert status["status"] == "unaudited"


def test_registry_verified_chapter():
    from src.corpus.migration_registry import is_verified
    # No chapters verified yet (unless explicitly added)
    assert not is_verified("BPHS", "Ch.99")


def test_registry_has_expected_structure():
    from src.corpus.migration_registry import MIGRATION_REGISTRY
    assert isinstance(MIGRATION_REGISTRY, dict)
    # All entries must have required fields
    for key, entry in MIGRATION_REGISTRY.items():
        assert "status" in entry
        assert entry["status"] in ("unaudited", "audited", "verified")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_migration_registry.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `migration_registry.py`**

```python
"""src/corpus/migration_registry.py — Per-chapter V1→V2 migration audit state.

Source of truth for which chapters have been migration-audited.
Only chapters with status="verified" can have their legacy rules
excluded from the execution corpus.

Status transitions:
    unaudited → audited (tool has been run, gaps may exist)
    audited → verified (gaps=0, all partials annotated, confidence>=0.7)
    verified → legacy exclusion activates in combined_corpus.py

To verify a chapter:
    1. Run: tools/migration_audit.py --chapter N
    2. Fix all GAP_CRITICAL items
    3. Annotate all PARTIAL items
    4. Add entry here with status="verified"
"""
from __future__ import annotations

# Per-chapter audit state. Key = (source, chapter).
# Add entries as chapters are audited and verified.
# Initially empty — chapters are "unaudited" by default.
MIGRATION_REGISTRY: dict[tuple[str, str], dict] = {
    # Example (uncomment when Ch.29 is verified):
    # ("BPHS", "Ch.29"): {
    #     "status": "verified",
    #     "coverage": 1.0,
    #     "full_count": 38,
    #     "partial_count": 5,
    #     "gap_critical_count": 0,
    #     "unmapped_count": 0,
    #     "confidence": 0.92,
    #     "verified_at": "2026-04-04",
    #     "verified_session": "S314",
    #     "partial_annotations": [],
    #     "notes": "",
    # },
}

_DEFAULT_STATUS: dict = {
    "status": "unaudited",
    "coverage": 0.0,
    "full_count": 0,
    "partial_count": 0,
    "gap_critical_count": 0,
    "unmapped_count": 0,
    "confidence": 0.0,
    "verified_at": "",
    "verified_session": "",
    "partial_annotations": [],
    "notes": "",
}


def get_status(source: str, chapter: str) -> dict:
    """Get migration audit status for a chapter."""
    return MIGRATION_REGISTRY.get((source, chapter), dict(_DEFAULT_STATUS))


def is_verified(source: str, chapter: str) -> bool:
    """Check if a chapter's migration has been verified."""
    entry = MIGRATION_REGISTRY.get((source, chapter))
    return entry is not None and entry.get("status") == "verified"
```

- [ ] **Step 4: Run tests**

Run: `.venv/bin/pytest tests/test_migration_registry.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add src/corpus/migration_registry.py tests/test_migration_registry.py
git commit -m "feat: migration registry — per-chapter audit state for legacy exclusion gating"
```

---

### Task 4: Gated Exclusion in `combined_corpus.py`

**Files:**
- Modify: `src/corpus/combined_corpus.py`

- [ ] **Step 1: Write failing test**

```python
# Add to tests/test_migration_registry.py

def test_combined_corpus_excludes_only_verified():
    """Legacy rules should only be excluded for verified chapters."""
    from src.corpus.combined_corpus import build_corpus
    corpus = build_corpus()
    all_rules = list(corpus.all())

    # Ch.29 is NOT verified yet → legacy should still be present
    ch29_legacy = [r for r in all_rules
                   if r.source == "BPHS" and r.chapter == "Ch.29"
                   and r.last_modified_session < "S310"]
    # Should have legacy rules since registry is empty
    assert len(ch29_legacy) > 0, "Legacy rules should exist for unverified chapters"
```

- [ ] **Step 2: Run test to verify it passes** (currently no exclusion = legacy present)

Run: `.venv/bin/pytest tests/test_migration_registry.py::test_combined_corpus_excludes_only_verified -v`
Expected: PASS (legacy is present since no chapters are verified yet)

- [ ] **Step 3: Add gated exclusion to `combined_corpus.py`**

Add this to `build_corpus()` function, after the `_V2_UPGRADED_CHAPTERS` definition and before the rule-loading loop. Read the file first to find the exact insertion point.

```python
    # ── Legacy exclusion for migration-verified chapters ─────────────────
    # Only excludes legacy for chapters that have been explicitly verified
    # through the migration audit process (migration_registry.py).
    from src.corpus.migration_registry import is_verified as _migration_verified

    def _is_superseded(rule) -> bool:
        """Return True if this legacy rule is superseded by verified V2 encoding."""
        if rule.last_modified_session >= "S310":
            return False  # V2 rules are never superseded
        return _migration_verified(rule.source, rule.chapter)
```

Then update the rule-loading loop:

```python
    _excluded_count = 0
    for source_reg in sources:
        for rule in source_reg.all():
            if _is_superseded(rule):
                _excluded_count += 1
                continue
            registry.add(rule)
```

- [ ] **Step 4: Run full test suite**

Run: `.venv/bin/pytest tests/ -x --tb=short -q`
Expected: 14510+ passed (no exclusion happens since registry is empty)

- [ ] **Step 5: Commit**

```bash
git add src/corpus/combined_corpus.py tests/test_migration_registry.py
git commit -m "feat: gated legacy exclusion — only excludes for migration-verified chapters"
```

---

### Task 5: Scorecard Section P

**Files:**
- Modify: `tools/v2_scorecard.py`

- [ ] **Step 1: Add Section P to scorecard format function**

In `format_scorecard()`, after Section O (legacy debt) and before red flags, add:

```python
    # P. Migration Audit Status
    from src.corpus.migration_registry import MIGRATION_REGISTRY, get_status
    _v2_chapters = [
        ("BPHS", f"Ch.{n}") for n in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29]
    ]
    if _v2_chapters:
        lines.append("P. MIGRATION AUDIT STATUS")
        verified_count = 0
        for source, ch in _v2_chapters:
            st = get_status(source, ch)
            status = st["status"]
            if status == "verified":
                verified_count += 1
                lines.append(f"    {ch:8s}: VERIFIED ✅ ({st['verified_at']}, "
                             f"{st['confidence']:.0%}, {st['partial_count']} annotated partials)")
            elif status == "audited":
                lines.append(f"    {ch:8s}: AUDITED  ⚠️ ({st['gap_critical_count']} gaps, "
                             f"{st['partial_count']} partials)")
            else:
                lines.append(f"    {ch:8s}: UNAUDITED ❌")
        lines.append(f"  Verified: {verified_count}/{len(_v2_chapters)} chapters")
        lines.append("")
```

- [ ] **Step 2: Run scorecard to verify Section P appears**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep -A20 "MIGRATION AUDIT"`
Expected: Section P showing all chapters as UNAUDITED

- [ ] **Step 3: Lint check**

Run: `.venv/bin/ruff check tools/v2_scorecard.py`
Expected: All checks passed

- [ ] **Step 4: Run full test suite**

Run: `.venv/bin/pytest tests/ -x --tb=short -q`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add tools/v2_scorecard.py
git commit -m "feat(scorecard): add Section P — migration audit status per chapter"
```

---

### Task 6: Smoke Test on Ch.29 + Push

- [ ] **Step 1: Run migration audit on Ch.29**

Run: `PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29`

Review the output. Note:
- How many V1 claims were extracted
- How many matched FULL
- Any GAP_CRITICAL items (need encoding)
- Any UNMAPPED items (need review)

- [ ] **Step 2: Run full scorecard**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | tail -30`

Verify Section P shows Ch.29 as UNAUDITED (correct — we haven't verified it yet).

- [ ] **Step 3: Run full test suite + ruff**

Run: `.venv/bin/ruff check src/ tests/ tools/ && .venv/bin/pytest tests/ -x --tb=short -q`
Expected: All clean, 14510+ passed

- [ ] **Step 4: Push**

Run: `git push`
Expected: Pre-push hook passes, all commits pushed.
