"""src/corpus/taxonomy.py — Controlled vocabularies for all enumerated fields.

Single source of truth. Every enumerated field in RuleRecord is validated
against these sets. No free-form values allowed in enumerated fields.

Used by V2ChapterBuilder.add() and corpus_audit.py for validation.
"""
from __future__ import annotations

VALID_OUTCOME_DOMAINS = frozenset({
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
})

VALID_OUTCOME_DIRECTIONS = frozenset({
    "favorable", "unfavorable", "neutral", "mixed",
})

VALID_OUTCOME_INTENSITIES = frozenset({
    "strong", "moderate", "weak", "conditional",
})

VALID_SCHOOLS = frozenset({
    "parashari", "kp", "jaimini", "nadi", "lal_kitab", "tajika", "all",
})

VALID_SYSTEMS = frozenset({
    "natal", "horary", "varshaphala", "muhurtha", "transit",
})

VALID_PHASES = frozenset({
    "1A_representative", "1A_deprecated",
    "1B_matrix", "1B_conditional", "1B_compound",
})

VALID_ENTITY_TARGETS = frozenset({
    "native", "father", "mother", "spouse", "children", "siblings", "general",
})

VALID_TIMING_TYPES = frozenset({
    "age", "age_range", "after_event", "dasha_period", "unspecified",
})

VALID_PREDICTION_TYPES = frozenset({
    "event", "trait", "capacity",
})

VALID_GENDER_SCOPES = frozenset({
    "universal", "male", "female",
})

VALID_CERTAINTY_LEVELS = frozenset({
    "definite", "probable", "possible",
})

VALID_EVALUATION_METHODS = frozenset({
    "placement_check", "yoga_detection", "lordship_check",
    "dasha_activation", "transit_check",
})

VALID_SAFETY_TIERS = frozenset({
    "standard", "restricted", "research_only",
})

VALID_RELATIONSHIP_TYPES = frozenset({
    "alternative", "addition", "override", "contrary_mirror", "mitigation",
})

VALID_CONDITION_PRIMITIVES = frozenset({
    "planet_in_house", "planet_in_sign", "planets_conjunct_in_house",
    "planets_conjunct", "lord_in_house", "lord_in_sign",
    "planet_aspecting", "planet_not_aspecting", "planet_dignity",
    # New primitives (S313 governance)
    "planet_in_sign_type",
    "planet_in_derived_house",
    "upagraha_in_house",
    "planet_in_house_from",
})

VALID_SIGN_TYPES = frozenset({
    "movable", "fixed", "dual",
    "fire", "earth", "air", "water",
    "odd", "even",
})

VALID_DERIVATIONS = frozenset({
    "arudha_pada", "upa_pada", "karakamsa",
    "navamsa_lagna", "hora_lagna", "ghati_lagna",
    "varnada_lagna", "sri_lagna", "indu_lagna", "pranapada_lagna",
})

VALID_UPAGRAHAS = frozenset({
    "dhuma", "vyatipata", "paridhi", "chapa", "dhwaja",
    "gulika", "pranapada", "mandi",
})

VALID_CONDITION_MODES = frozenset({
    "occupies", "aspects",
})
