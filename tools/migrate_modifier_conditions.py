#!/usr/bin/env python3
"""tools/migrate_modifier_conditions.py — Migrate modifier condition strings to structured dicts."""
from __future__ import annotations
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus.combined_corpus import build_corpus


def try_parse(condition_str: str) -> list[dict] | None:
    """Attempt to parse a modifier condition string into structured form.
    Returns None if ambiguous."""
    s = condition_str.strip().lower()

    m = re.match(r"lord_of_(\d+)_in_(?:house_)?(\d+)", s)
    if m:
        return [{"type": "lord_in_house", "lord_of": int(m.group(1)), "house": int(m.group(2))}]

    m = re.match(r"(\w+)_in_house_(\d+)", s)
    if m:
        return [{"type": "planet_in_house", "planet": m.group(1), "house": int(m.group(2))}]

    m = re.match(r"(\w+)_(?:is_)?exalted", s)
    if m:
        return [{"type": "planet_dignity", "planet": m.group(1), "dignity": "exalted"}]

    m = re.match(r"(\w+)_(?:is_)?debilitated", s)
    if m:
        return [{"type": "planet_dignity", "planet": m.group(1), "dignity": "debilitated"}]

    m = re.match(r"(\w+)_conjunct_(\w+)", s)
    if m:
        return [{"type": "planets_conjunct", "planets": [m.group(1), m.group(2)]}]

    return None


def main():
    corpus = build_corpus()
    rules = [r for r in corpus.all() if r.phase.startswith("1B")]
    total_mods = 0
    parsed = 0
    unparsed = 0
    unparsed_examples = []

    for rule in rules:
        for mod in (rule.modifiers or []):
            cond = mod.get("condition", "")
            if not cond or isinstance(cond, list):
                continue
            total_mods += 1
            result = try_parse(cond)
            if result:
                parsed += 1
            else:
                unparsed += 1
                if len(unparsed_examples) < 20:
                    unparsed_examples.append({"rule": rule.rule_id, "condition": cond})

    print(f"Total string modifier conditions: {total_mods}")
    print(f"Parseable (auto-convert): {parsed} ({100*parsed/max(total_mods,1):.0f}%)")
    print(f"Ambiguous (keep as string): {unparsed} ({100*unparsed/max(total_mods,1):.0f}%)")
    if unparsed_examples:
        print(f"\nFirst {len(unparsed_examples)} unparseable:")
        for ex in unparsed_examples:
            print(f"  {ex['rule']}: {ex['condition']}")


if __name__ == "__main__":
    main()
