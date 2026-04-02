"""tools/condition_modifier_audit.py — Audit V2 rules for condition/modifier misclassification.

Scans all bphs_v2_ch*.py files. For each rule, checks if any modifier
should actually be a condition (based on commentary evidence) and if any
exceptions are missing (based on "nullified"/"cancelled" keywords).

Usage:
    .venv/bin/python -m tools.condition_modifier_audit [--json]
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path

# Ensure the project root is on sys.path so 'src' is importable when run
# as a script directly (python tools/condition_modifier_audit.py).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def classify_modifier(*, modifier: dict, commentary: str) -> dict:
    """Classify a single modifier as correctly placed or misclassified.

    Returns dict with 'type', 'confidence', 'evidence'.
    """
    cond_text = modifier.get("condition", "").lower()
    comm_lower = commentary.lower()

    # High confidence: "must", "required", "necessary" in modifier condition text
    _REQUIRED_KW = ("must", "required", "necessary")
    for kw in _REQUIRED_KW:
        if kw in cond_text:
            return {
                "type": "modifier_should_be_condition",
                "confidence": "high",
                "evidence": f"Modifier condition contains '{kw}'",
            }

    # High confidence: commentary has enumeration pattern (a), (b), (c)
    enum_pattern = re.search(r'\(a\).*\(b\)', comm_lower)
    if enum_pattern:
        # Check if this modifier's condition text appears near an enumeration item
        cond_words = set(cond_text.replace("_", " ").split())
        if len(cond_words & set(comm_lower.split())) >= 3:
            return {
                "type": "modifier_should_be_condition",
                "confidence": "high",
                "evidence": "Commentary enumerates conditions with (a)(b)(c) pattern",
            }

    # High confidence: commentary says "3 conditions" or "N conditions"
    if re.search(r'\d+\s+conditions?\s', comm_lower):
        return {
            "type": "modifier_should_be_condition",
            "confidence": "high",
            "evidence": "Commentary explicitly counts conditions",
        }

    # Medium confidence: modifier describes a placement/conjunction
    # Note: "aspected" alone is excluded when the condition also contains
    # qualitative adverbs ("more_favorable", "favorable", "stronger") which
    # indicate the modifier is a genuine amplifier, not a misplaced condition.
    _AMPLIFIER_SIGNALS = ("more_favorable", "favorable", "stronger", "weaker",
                           "more_results", "less_results", "enhanced", "reduced")
    is_amplifier = any(sig in cond_text for sig in _AMPLIFIER_SIGNALS)

    _PLACEMENT_KW = ("lord", "in_house", "in_h", "conjunct", "in_sign",
                      "in_movable", "in_fixed", "in_dual", "in_")
    if not is_amplifier and any(kw in cond_text for kw in _PLACEMENT_KW):
        return {
            "type": "modifier_should_be_condition",
            "confidence": "medium",
            "evidence": "Modifier condition describes a placement or conjunction",
        }

    # Also flag "aspected" when not paired with amplifier signals
    if not is_amplifier and "aspected" in cond_text:
        return {
            "type": "modifier_should_be_condition",
            "confidence": "medium",
            "evidence": "Modifier condition describes a placement or conjunction",
        }

    # Low confidence: ambiguous
    return {
        "type": "modifier_possibly_misclassified",
        "confidence": "low",
        "evidence": "Ambiguous — could be required or amplifying",
    }


def scan_commentary_for_missing_exceptions(*, commentary: str, exceptions: list) -> list[dict]:
    """Check if commentary mentions cancellation but exceptions list is empty."""
    if exceptions:
        return []

    flags = []
    _CANCEL_KW = ("nullified", "cancelled", "canceled", "exception",
                   "does not apply", "gets negated")
    comm_lower = commentary.lower()
    for kw in _CANCEL_KW:
        if kw in comm_lower:
            flags.append({
                "type": "missing_exception",
                "confidence": "medium",
                "evidence": f"Commentary contains '{kw}' but exceptions list is empty",
            })
            break  # one flag per rule for this check
    return flags


def audit_registry(registry, chapter_name: str) -> list[dict]:
    """Audit all rules in a registry. Returns list of flag dicts."""
    results = []
    for rule in registry.all():
        rule_flags = []

        # Check each modifier
        for i, mod in enumerate(rule.modifiers or []):
            classification = classify_modifier(
                modifier=mod,
                commentary=rule.commentary_context or "",
            )
            if classification["confidence"] != "low" or classification["type"] == "modifier_should_be_condition":
                rule_flags.append({
                    **classification,
                    "modifier_index": i,
                    "current_value": mod,
                })

        # Check for missing exceptions
        exception_flags = scan_commentary_for_missing_exceptions(
            commentary=rule.commentary_context or "",
            exceptions=rule.exceptions or [],
        )
        rule_flags.extend(exception_flags)

        if rule_flags:
            results.append({
                "rule_id": rule.rule_id,
                "chapter": chapter_name,
                "verse_ref": rule.verse_ref,
                "flags": rule_flags,
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Audit V2 rules for condition/modifier issues")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Find all V2 chapter modules
    corpus_dir = Path("src/corpus")
    chapters = sorted(corpus_dir.glob("bphs_v2_ch*.py"))

    all_results = []
    for ch_path in chapters:
        module_name = f"src.corpus.{ch_path.stem}"
        mod = importlib.import_module(module_name)
        # Find the registry (named BPHS_V2_CH*_REGISTRY)
        reg_name = [n for n in dir(mod) if n.endswith("_REGISTRY") and n.startswith("BPHS")]
        if not reg_name:
            continue
        registry = getattr(mod, reg_name[0])
        results = audit_registry(registry, ch_path.stem)
        all_results.extend(results)

    if args.json:
        print(json.dumps(all_results, indent=2))
    else:
        high = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "high")
        medium = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "medium")
        low = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "low")
        print(f"Audit complete: {len(all_results)} rules flagged")
        print(f"  High confidence:   {high}")
        print(f"  Medium confidence: {medium}")
        print(f"  Low confidence:    {low}")
        for r in all_results:
            for f in r["flags"]:
                if f["confidence"] in ("high", "medium"):
                    print(f"  {r['rule_id']} ({r['verse_ref']}): [{f['confidence']}] {f['evidence']}")

    sys.exit(1 if high > 0 else 0)


if __name__ == "__main__":
    main()
