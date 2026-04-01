"""src/corpus/condition_fingerprint.py — Canonical condition fingerprint.

Derives a flat string key from a rule's primary_condition that uniquely
identifies the astrological configuration, independent of which text
describes it. Two rules from different texts with the same fingerprint
are about the SAME configuration and must be compared.

See docs/CROSS_TEXT_GOVERNANCE.md for the full protocol.

Usage:
    from src.corpus.condition_fingerprint import compute_fingerprint
    fp = compute_fingerprint(rule)
    # "lord_5.in_house.7"
"""
from __future__ import annotations


_TYPE_MAP = {
    "lordship_placement": "in_house",
    "house": "in_house",
    "sign_placement": "in_sign",
    "conjunction_condition": "conjunct",
    "conjunction_in_house": "conjunct_in_house",
    "aspect_condition": "aspecting",
    "lordship_dignity_condition": "dignity",
    "general_condition": "general",
}


def compute_fingerprint(rule) -> str:
    """Derive canonical condition fingerprint from rule.primary_condition.

    Returns a dot-separated string: "{planet}.{placement_type}.{value}"
    The dot separator avoids collision with underscores in planet names.

    Examples:
        lord_5.in_house.7
        jupiter.in_house.7
        any_benefic.in_house.1_4_5_7_9_10
        jupiter_venus.conjunct
        general.general
    """
    pc = rule.primary_condition if hasattr(rule, "primary_condition") else {}
    if not pc:
        return "general.general"

    planet = pc.get("planet", "general")
    ptype = pc.get("placement_type", "general_condition")
    pvalue = pc.get("placement_value")

    # Normalize planet: h5_lord → lord_5
    if isinstance(planet, str) and planet.startswith("h") and "_lord" in planet:
        parts = planet.split("_")
        n = parts[0][1:]  # extract number after 'h'
        planet = f"lord_{n}"
    if isinstance(planet, str):
        planet = planet.lower()

    # Normalize placement type
    ptype = _TYPE_MAP.get(ptype, ptype)

    # Normalize value
    if pvalue is None:
        return f"{planet}.{ptype}"
    elif isinstance(pvalue, list):
        sorted_vals = sorted(pvalue, key=lambda x: (isinstance(x, str), x))
        return f"{planet}.{ptype}.{'_'.join(str(v) for v in sorted_vals)}"
    else:
        return f"{planet}.{ptype}.{str(pvalue).lower()}"


def fingerprint_prefix(fp: str) -> str:
    """Extract the configuration prefix (planet + placement type) from a fingerprint.

    This groups rules about the same planet/lord in the same placement type,
    regardless of specific house/sign. Useful for broader queries.

    Example: "lord_5.in_house.7" → "lord_5.in_house"
    """
    parts = fp.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else fp
