"""tools/tag_bb_chains.py — Auto-tag derived_house_chains on V2 rules.

This is LEGITIMATE automation because BB chains are DETERMINISTIC from the
house number — they don't require reading source text. The 12x12 matrix
in bb_reference.py computes them.

Usage:
    PYTHONPATH=. .venv/bin/python tools/tag_bb_chains.py --dry-run
    PYTHONPATH=. .venv/bin/python tools/tag_bb_chains.py --apply
"""
from __future__ import annotations

import argparse
import sys


def get_house_from_rule(rule) -> int | None:
    """Extract the primary house number from a rule's conditions."""
    pc = rule.primary_condition
    conditions = pc.get("conditions", [])
    for cond in conditions:
        ct = cond.get("type", "")
        if ct in ("planet_in_house", "lord_in_house"):
            hv = cond.get("house", None)
            if isinstance(hv, int) and 1 <= hv <= 12:
                return hv
    return None


def compute_chains_for_rule(rule) -> list[dict]:
    """Compute BB chains for a rule based on its house."""
    from src.corpus.bb_reference import get_primary_bb_chains

    house = get_house_from_rule(rule)
    if house is None:
        return []

    return get_primary_bb_chains(house, max_chains=3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show what would be tagged")
    parser.add_argument("--apply", action="store_true", help="Write to source files")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply")
        sys.exit(1)

    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    v2_rules = [r for r in corpus.all() if r.last_modified_session == "S311"]

    tagged = 0
    skipped = 0
    already = 0

    for r in v2_rules:
        if r.derived_house_chains:
            already += 1
            continue

        chains = compute_chains_for_rule(r)
        if not chains:
            skipped += 1
            continue

        tagged += 1
        if args.dry_run:
            print(f"{r.rule_id} ({r.chapter}): + {len(chains)} chains")
            for c in chains:
                print(f"  {c['derivative']} of H{c['base_house']} ({c['label']})")

    print(f"\nSummary: {tagged} to tag, {already} already have chains, {skipped} skipped (no house)")

    if args.apply:
        print("\nTo apply: modify each bphs_v2_ch*.py file to add derived_house_chains=[...]")
        print("This requires editing the source files — use the encoding session to do this.")


if __name__ == "__main__":
    main()
