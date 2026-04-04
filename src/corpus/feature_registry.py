"""src/corpus/feature_registry.py — Implemented features + chapter requirements.

This is the enforcement layer for deferred primitives. Before encoding
a chapter, check_chapter_requirements() verifies all required features
are implemented. If not, encoding is blocked.

Usage:
    from src.corpus.feature_registry import check_chapter_requirements
    check_chapter_requirements("Ch.34")  # raises if missing features
"""
from __future__ import annotations

# Features that ARE implemented (add here when a primitive ships)
IMPLEMENTED_FEATURES: frozenset[str] = frozenset({
    # Condition primitives (13)
    "planet_in_house",
    "planet_in_sign",
    "lord_in_house",
    "lord_in_sign",
    "planets_conjunct",
    "planets_conjunct_in_house",
    "planet_aspecting",
    "planet_not_aspecting",
    "planet_not_in_house",
    "planet_dignity",
    "planet_in_sign_type",
    "upagraha_in_house",
    "planet_in_house_from",
    "planet_in_navamsa_sign",
    "dispositor_condition",
    # Schema features
    "modifier_5_effect_schema",
    "primary_domain_taxonomy",
    "inference_skeleton",
    # Derived house (exists but limited to special lagnas)
    "planet_in_derived_house",
})

# Features NOT YET implemented (add trigger + dependency)
PENDING_FEATURES: dict[str, str] = {
    "same_planet_constraint": "Bind variable for conditions that must resolve to same planet (BPHS2303)",
    "shadbala_strength": "6-fold planetary strength computation (BPHS2501)",
    "timing_activation": "Dasha-period probabilistic windows for timing rules",
    "dynamic_karaka": "Stronger-of-two-planets karaka resolution (BPHS1504)",
    "functional_benefic": "Per-lagna benefic/malefic classification (BPHS1503, 1508, 2408, 2623)",
    "planet_in_house_from_aspects": "Aspect mode for planet_in_house_from primitive",
    "navamsa_lagna": "D9 ascendant computation (BPHS2114)",
    "modifier_condition_structured": "Replace modifier condition strings with structured dicts",
    "modifier_execution": "Engine evaluates modifier gates/negates at rule-firing time",
    "prediction_type_classification": "Classify predictions as trait/event/status/health",
    "bhavat_bhavam_execution": "Make derived_house_chains computable, not just metadata",
}

# Chapter → required features (only chapters with non-standard requirements)
CHAPTER_REQUIREMENTS: dict[str, list[str]] = {
    # BPHS Ch.26-31: house-specific effects — no special requirements
    # BPHS Ch.32-33: karakas
    "Ch.32": ["dynamic_karaka"],
    "Ch.33": ["dynamic_karaka"],
    # BPHS Ch.34-42: yogas
    "Ch.34": ["same_planet_constraint"],
    "Ch.35": ["same_planet_constraint"],
    "Ch.36": ["same_planet_constraint"],
    "Ch.37": ["same_planet_constraint"],
    "Ch.38": ["same_planet_constraint"],
    "Ch.39": ["same_planet_constraint"],
    "Ch.40": ["same_planet_constraint"],
    "Ch.41": ["same_planet_constraint"],
    "Ch.42": ["same_planet_constraint"],
    # Laghu Parashari
    "LP": ["functional_benefic"],
}


def check_chapter_requirements(chapter: str) -> list[str]:
    """Check if all required features for a chapter are implemented.

    Returns list of missing features. Empty list = ready to encode.
    Raises ValueError if any are missing (for use as a gate).
    """
    required = CHAPTER_REQUIREMENTS.get(chapter, [])
    missing = [f for f in required if f not in IMPLEMENTED_FEATURES]
    return missing


def enforce_chapter_requirements(chapter: str) -> None:
    """Raise if chapter has unmet feature requirements."""
    missing = check_chapter_requirements(chapter)
    if missing:
        details = [f"  - {f}: {PENDING_FEATURES.get(f, 'no description')}" for f in missing]
        raise ValueError(
            f"Chapter {chapter} blocked — missing required features:\n"
            + "\n".join(details)
            + "\n\nImplement these features before encoding this chapter."
        )
