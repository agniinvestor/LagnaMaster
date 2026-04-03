"""tools/migrate_modifiers.py — Classify and migrate modifiers to new 5-effect schema.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --report
"""
from __future__ import annotations
import argparse
import importlib


def _patch_builder_for_migration():
    """Monkey-patch V2Builder._validate_add to skip T1-18 modifier validation.

    Corpus files encoded before T1-18 was introduced use the old modifier
    schema (no 'target'/'scope' fields, 'conditionalizes'/'moderate' instead
    of 'gates'/'medium').  Importing those modules raises ValueError.  This
    patch lets the migration script load them so it can classify and report
    the old modifiers.  Normal builds are unaffected.
    """
    from src.corpus import v2_builder  # noqa: PLC0415

    @staticmethod  # type: ignore[misc]
    def _validate_add_migration_noop(conditions, direction, intensity,
                                     domains, predictions, *,
                                     description="", entity_target="native",
                                     commentary_context="", modifiers=None):
        """No-op validator for migration — skips all T1-* checks so that
        corpus files using the old modifier schema (pre-T1-18) can be imported
        for classification without raising ValueError."""

    v2_builder.V2ChapterBuilder._validate_add = _validate_add_migration_noop


# Patch BEFORE any corpus imports so that module-level b.add() calls succeed.
_patch_builder_for_migration()

_DEFAULT_MAP = {
    "conditionalizes": ("gates", "rule"),
    "amplifies": ("amplifies", "prediction"),
    "negates": ("negates", "prediction"),
}

_MANUAL_OVERRIDES: dict[tuple[str, int], tuple[str, str]] = {
    # Gates → Qualifies (adds interpretation/secondary outcome, not a requirement)
    ("BPHS2428", 0): ("qualifies", "prediction"),   # childhood→good health temporal interpretation
    ("BPHS2440", 0): ("qualifies", "prediction"),   # despite fortunes, feels miserable
    ("BPHS2444", 0): ("qualifies", "prediction"),   # ancestral property risk + asceticism
    ("BPHS2469", 0): ("qualifies", "prediction"),   # Venus/Taurus lagna-specific nuance
    ("BPHS2484", 0): ("qualifies", "prediction"),   # Ramadayalu contradicts — commentary interpretation
    ("BPHS2488", 0): ("qualifies", "prediction"),   # marriage pecuniary gains despite unhappiness
    ("BPHS2499", 0): ("qualifies", "prediction"),   # not health but long life — mixed interpretation
    ("BPHS2523", 0): ("qualifies", "prediction"),   # intelligence despite career paralysis
    ("BPHS2628", 0): ("qualifies", "prediction"),   # females + bad character but progenic happiness
    ("BPHS2629", 0): ("qualifies", "prediction"),   # misfortunes but progenic happiness
    # Amplifies → Attenuates (weakens rather than strengthens)
    ("BPHS1832", 0): ("attenuates", "prediction"),  # Venus bereft of strength weakens
    ("BPHS2306", 0): ("attenuates", "prediction"),  # not aspected by benefic = lack of protection
    ("BPHS2415", 0): ("attenuates", "prediction"),  # no benefic aspect/conjunction
    # Negates → Attenuates (reduces magnitude, doesn't fully cancel)
    ("BPHS2501", 0): ("attenuates", "prediction"),  # weak shadbala → medium longevity (not denial)
    # Amplifies → Qualifies (changes nature/interpretation, not magnitude)
    ("BPHS2468", 0): ("qualifies", "prediction"),   # adoption + digestive defects (adds outcomes)
    ("BPHS2497", 0): ("qualifies", "prediction"),   # 'shishu' = timing qualification (childhood)
    ("BPHS2553", 0): ("qualifies", "prediction"),   # obstacles then adopt (temporal interpretation)
}

_STRENGTH_MAP = {"weak": "weak", "moderate": "medium", "strong": "strong", "none": None}

_CHAPTERS = [
    "12", "13", "14", "15", "16", "17", "18", "19",
    "20", "21", "22", "23", "24a", "24b", "24c", "25",
]


def _load_all_modifiers():
    results = []
    for ch in _CHAPTERS:
        mod = importlib.import_module(f"src.corpus.bphs_v2_ch{ch}")
        for attr in dir(mod):
            if "REGISTRY" in attr:
                reg = getattr(mod, attr)
                for r in reg.all():
                    for i, m in enumerate(r.modifiers or []):
                        results.append({
                            "rule_id": r.rule_id,
                            "chapter": ch,
                            "modifier_index": i,
                            "old": m,
                        })
    return results


def classify(rule_id: str, idx: int, old_mod: dict) -> dict | None:
    key = (rule_id, idx)
    if key in _MANUAL_OVERRIDES:
        new_effect, new_target = _MANUAL_OVERRIDES[key]
    else:
        old_effect = old_mod.get("effect", "")
        new_effect, new_target = _DEFAULT_MAP.get(old_effect, ("qualifies", "prediction"))

    old_strength = old_mod.get("strength", "moderate")
    new_strength = _STRENGTH_MAP.get(old_strength)
    if new_strength is None:
        return None

    return {
        "condition": old_mod.get("condition", ""),
        "effect": new_effect,
        "target": new_target,
        "strength": new_strength,
        "scope": "local",
    }


def report(all_mods):
    by_effect = {"gates": [], "amplifies": [], "attenuates": [], "negates": [], "qualifies": [], "REMOVED": []}
    for entry in all_mods:
        new = classify(entry["rule_id"], entry["modifier_index"], entry["old"])
        if new is None:
            by_effect["REMOVED"].append(entry)
        else:
            by_effect[new["effect"]].append((entry, new))

    for effect, items in by_effect.items():
        print(f"\n=== {effect} ({len(items)}) ===")
        if effect == "REMOVED":
            for entry in items:
                print(f"  {entry['rule_id']}[{entry['modifier_index']}]: {entry['old']['condition']}")
        else:
            for entry, new in items:
                old_eff = entry["old"]["effect"]
                mapped = "conditionalizes->gates" if old_eff == "conditionalizes" and effect == "gates" else ""
                changed = f" <- WAS {old_eff}" if old_eff != effect and not mapped else ""
                print(f"  {entry['rule_id']}[{entry['modifier_index']}]: {new['condition'][:70]}{changed}")

    total = sum(len(v) for v in by_effect.values())
    print(f"\nTotal: {total} modifiers classified")
    for eff in ["gates", "amplifies", "attenuates", "negates", "qualifies", "REMOVED"]:
        print(f"  {eff}: {len(by_effect[eff])}")


def main():
    parser = argparse.ArgumentParser(description="Modifier migration tool")
    parser.add_argument("--report", action="store_true", help="Print classification report")
    args = parser.parse_args()

    all_mods = _load_all_modifiers()
    print(f"Loaded {len(all_mods)} modifiers from {len(_CHAPTERS)} chapters")

    if args.report:
        report(all_mods)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
