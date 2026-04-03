"""tools/migrate_domains.py — Normalize domains from 15 to 8 primary domains.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migrate_domains.py --report
"""
from __future__ import annotations
import argparse
import importlib
from collections import Counter

from src.corpus.taxonomy import (
    PRIMARY_DOMAINS, PRIMARY_DOMAIN_PRIORITY, DOMAIN_NORMALIZATION,
)

_FAME_TO_WEALTH = {"gains", "nishka", "money", "wealthy", "affluent", "fortunes",
                    "prosperity", "rich", "opulent", "gold", "grains"}
_EDUCATION_TO_CAREER = {"profession", "skill", "expertise", "livelihood", "calling"}
_ENEMIES_TO_CHARACTER = {"cruel", "aggression", "wicked", "sinful", "mean_deeds"}


def normalize_domain(old_domain: str, claim: str = "") -> str:
    if old_domain in PRIMARY_DOMAINS:
        return old_domain
    default = DOMAIN_NORMALIZATION.get(old_domain, "character")
    if old_domain == "fame_reputation":
        cl = claim.lower().replace("_", " ")
        if any(kw in cl for kw in _FAME_TO_WEALTH):
            return "wealth"
        return "career"
    if old_domain == "intelligence_education":
        cl = claim.lower().replace("_", " ")
        if any(kw in cl for kw in _EDUCATION_TO_CAREER):
            return "career"
        return "character"
    if old_domain == "enemies_litigation":
        cl = claim.lower().replace("_", " ")
        if any(kw in cl for kw in _ENEMIES_TO_CHARACTER):
            return "character"
        return "relationships"
    return default


def compute_primary(predictions: list[dict]) -> str:
    if not predictions:
        return "character"
    max_mag = max(p.get("magnitude", 0.0) for p in predictions)
    candidates = [p for p in predictions if p.get("magnitude", 0.0) == max_mag]
    if len(candidates) == 1:
        return candidates[0].get("domain", "character")
    for pd in PRIMARY_DOMAIN_PRIORITY:
        if any(c.get("domain") == pd for c in candidates):
            return pd
    return candidates[0].get("domain", "character")


def _load_all():
    from src.corpus import v2_builder
    _orig = v2_builder.V2ChapterBuilder._validate_add
    v2_builder.V2ChapterBuilder._validate_add = staticmethod(lambda *a, **kw: None)
    results = []
    for ch in ["12","13","14","15","16","17","18","19","20","21","22","23","24a","24b","24c","25"]:
        mod = importlib.import_module(f"src.corpus.bphs_v2_ch{ch}")
        for attr in dir(mod):
            if "REGISTRY" in attr:
                for r in getattr(mod, attr).all():
                    new_preds = []
                    for p in r.predictions:
                        nd = normalize_domain(p.get("domain", ""), p.get("claim", ""))
                        new_preds.append({**p, "domain": nd})
                    primary = compute_primary(new_preds)
                    results.append({
                        "rule_id": r.rule_id, "chapter": ch,
                        "old_domains": list(r.outcome_domains),
                        "new_preds": new_preds, "primary": primary,
                        "tags": sorted({p["domain"] for p in new_preds} - {primary}),
                    })
    v2_builder.V2ChapterBuilder._validate_add = _orig
    return results


def report(rules):
    dist = Counter(r["primary"] for r in rules)
    changes = sum(1 for r in rules if set(r["old_domains"]) != {p["domain"] for p in r["new_preds"]})
    print("=== Primary Domain Distribution ===")
    for d in PRIMARY_DOMAIN_PRIORITY:
        print(f"  {d}: {dist[d]}")
    print(f"\nTotal: {len(rules)} rules, {changes} with domain changes")
    print("\n=== Sample Changes (first 15) ===")
    n = 0
    for r in rules:
        if set(r["old_domains"]) != {p["domain"] for p in r["new_preds"]}:
            print(f"  {r['rule_id']}: {r['old_domains']} → primary={r['primary']}, tags={r['tags']}")
            n += 1
            if n >= 15:
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    rules = _load_all()
    print(f"Loaded {len(rules)} rules\n")
    if args.report:
        report(rules)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
