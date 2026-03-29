"""
src/corpus/existing_rules.py — R01-R23 as RuleRecord objects (S203)

Machine-readable encoding of all 23 rules currently implemented in the
scoring engine (src/calculations/multi_axis_scoring.py).

These rules are:
  - implemented=True (all currently active in the engine)
  - confidence ≥ 0.8 (well-established classical citations)
  - school="all" unless school-specific

This module exports a pre-populated CorpusRegistry singleton.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

EXISTING_RULES_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord(
        rule_id="R01",
        source="BPHS",
        chapter="Ch.11",
        school="all",
        category="house_quality",
        description=(
            "Gentle/benefic signs (Cancer, Taurus, Libra, Pisces, Sagittarius) "
            "occupying the house cusp give benefic results for that house."
        ),
        confidence=0.9,
        tags=["gentle_sign", "saumya", "house_sign"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R01",
    ),
    RuleRecord(
        rule_id="R02",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional benefic in the house strengthens house significations. "
            "Yogakaraka planet gives enhanced results (×YKM multiplier)."
        ),
        confidence=0.9,
        tags=["functional_benefic", "in_house"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R02",
    ),
    RuleRecord(
        rule_id="R03",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional benefic aspecting the house (weak condition — half weight). "
            "Aspect brings benefic influence but less than direct occupancy."
        ),
        confidence=0.8,
        tags=["functional_benefic", "aspect", "weak_condition"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R03",
    ),
    RuleRecord(
        rule_id="R04",
        source="BPHS",
        chapter="Ch.47",
        school="all",
        category="dignity",
        description=(
            "Bhavesh (house lord) placed in kendra (1,4,7,10) or trikona (1,5,9) — "
            "but not dusthana — strengthens the house promise. "
            "Source: PVRNR BPHS Ch.47 — bhavesh placement is the primary determinant."
        ),
        confidence=0.95,
        verse="Bhaveshe kendrathrikonasthe bhavam shubhaphalapradam",
        tags=["bhavesh", "kendra", "trikona", "house_lord"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R04",
    ),
    RuleRecord(
        rule_id="R05",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Bhavesh conjoined with a kendra or trikona lord (weak condition — half weight). "
            "Association with angular/trine lords activates positive combinations."
        ),
        confidence=0.8,
        tags=["bhavesh", "association", "kendra_lord", "trikona_lord", "weak_condition"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R05",
    ),
    RuleRecord(
        rule_id="R06",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Bhavesh conjoined with a functional benefic — house lord in good company. "
            "Yogakaraka cotenant gives enhanced results."
        ),
        confidence=0.9,
        tags=["bhavesh", "association", "functional_benefic"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R06",
    ),
    RuleRecord(
        rule_id="R07",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional benefic aspects the bhavesh sign (weak condition — half weight). "
            "Benefic aspect on the house lord improves house delivery."
        ),
        confidence=0.8,
        tags=["bhavesh", "aspect", "functional_benefic", "weak_condition"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R07",
    ),
    RuleRecord(
        rule_id="R08",
        source="Phaladeepika",
        chapter="Ch.6",
        school="all",
        category="kartari",
        description=(
            "Shubha Kartari Yoga: natural benefics flank the house sign on both sides. "
            "The house is 'enclosed' by benefics — protected and enhanced."
        ),
        confidence=0.9,
        verse="Shubhaih parivritam bhavam shubhaphalapradam",
        tags=["kartari", "shubha_kartari", "flanking", "natural_benefic"],
        implemented=True,
        engine_ref="multi_axis_scoring._kartari:shubh",
    ),
    RuleRecord(
        rule_id="R09",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional malefic in the house — afflicts house significations. "
            "Each malefic occupant reduces the house score."
        ),
        confidence=0.9,
        tags=["functional_malefic", "in_house", "affliction"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R09",
    ),
    RuleRecord(
        rule_id="R10",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional malefic aspecting the house (weak condition — half weight). "
            "Malefic aspect reduces but does not destroy house significations."
        ),
        confidence=0.8,
        tags=["functional_malefic", "aspect", "affliction", "weak_condition"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R10",
    ),
    RuleRecord(
        rule_id="R11",
        source="BPHS",
        chapter="Ch.47",
        school="all",
        category="dignity",
        description=(
            "Bhavesh in dusthana (6, 8, 12) — house lord placed in a difficult house. "
            "Strong classical affliction: bhavesh in dusthana harms the house. "
            "Source: PVRNR BPHS Ch.47 — dusthana placement weakens house promise."
        ),
        confidence=0.95,
        tags=["bhavesh", "dusthana", "affliction", "house_lord"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R11",
    ),
    RuleRecord(
        rule_id="R12",
        source="Phaladeepika",
        chapter="Ch.6",
        school="all",
        category="kartari",
        description=(
            "Paapa Kartari Yoga: natural malefics flank the house sign on both sides. "
            "The house is 'enclosed' by malefics — significantly afflicted."
        ),
        confidence=0.9,
        tags=["kartari", "paapa_kartari", "flanking", "natural_malefic"],
        implemented=True,
        engine_ref="multi_axis_scoring._kartari:paap",
    ),
    RuleRecord(
        rule_id="R13",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional malefic conjoined with bhavesh — house lord in bad company. "
            "Direct association of malefic with house lord afflicts house delivery."
        ),
        confidence=0.9,
        tags=["bhavesh", "association", "functional_malefic", "affliction"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R13",
    ),
    RuleRecord(
        rule_id="R14",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description=(
            "Functional malefic aspects the bhavesh sign (weak condition — half weight). "
            "Malefic aspect on house lord reduces house promise."
        ),
        confidence=0.8,
        tags=["bhavesh", "aspect", "functional_malefic", "affliction", "weak_condition"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R14",
    ),
    RuleRecord(
        rule_id="R15",
        source="BPHS",
        chapter="Ch.47",
        school="all",
        category="dignity",
        description=(
            "Bhavesh debilitated — house lord in sign of deep fall or debilitation. "
            "Strongest single affliction in the scoring system. "
            "Source: PVRNR BPHS — bhavesh in neecha destroys house promise."
        ),
        confidence=0.95,
        tags=["bhavesh", "debilitation", "neecha", "dignity"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R15",
    ),
    RuleRecord(
        rule_id="R16",
        source="BPHS",
        chapter="Ch.47",
        school="all",
        category="dignity",
        description=(
            "Bhavesh conjoined with dusthana lord — house lord associates with lord "
            "of a difficult house (6, 8, 12), creating a difficult combination."
        ),
        confidence=0.85,
        tags=["bhavesh", "dusthana_lord", "association", "affliction"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R16",
    ),
    RuleRecord(
        rule_id="R17",
        source="BPHS",
        chapter="Ch.32",
        school="all",
        category="karak",
        description=(
            "Sthira Karak (natural significator) in or aspecting its assigned house "
            "strengthens the house significations. "
            "Source: BPHS Ch.32 Naisargika Karakatva — natural significators for each house."
        ),
        confidence=0.9,
        tags=["karak", "naisargika", "significator", "natural"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R17",
    ),
    RuleRecord(
        rule_id="R18",
        source="BPHS",
        chapter="Ch.32",
        school="all",
        category="karak",
        description=(
            "Sthira Karak in dusthana from its assigned house weakens house delivery. "
            "Natural significator placed 6th, 8th, or 12th from the house it signifies."
        ),
        confidence=0.85,
        tags=["karak", "naisargika", "dusthana", "affliction"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R18",
    ),
    RuleRecord(
        rule_id="R19",
        source="BPHS",
        chapter="Ch.3 v.51-59",
        school="all",
        category="combustion",
        description=(
            "Bhavesh combust (within Sun's combust orb) — house lord loses strength "
            "due to solar proximity. Cazimi (within 1°) is instead strengthened. "
            "Source: BPHS Ch.3 v.51-59; Phaladeepika Ch.2."
        ),
        confidence=0.9,
        verse="Astangato nirbalah",
        tags=["combust", "cazimi", "sun_proximity", "bhavesh"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R19",
    ),
    RuleRecord(
        rule_id="R20",
        source="BPHS",
        chapter="Ch.3",
        school="all",
        category="strength",
        description=(
            "Dig Bala: bhavesh in its house of directional strength "
            "(Sun/Mars: H10; Moon/Venus: H4; Mercury/Jupiter: H1; Saturn: H7). "
            "Source: BPHS Ch.3 — planets gain full directional strength in specific houses."
        ),
        confidence=0.9,
        tags=["dig_bala", "directional_strength", "bhavesh"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R20",
    ),
    RuleRecord(
        rule_id="R21",
        source="BPHS",
        chapter="General",
        school="all",
        category="pushkara",
        description=(
            "Pushkara Navamsha: bhavesh placed in one of the 24 auspicious navamsha "
            "degree zones — confers special benefic results. "
            "Source: BPHS — planets in Pushkara Navamsha are especially powerful."
        ),
        confidence=0.85,
        tags=["pushkara", "navamsha", "auspicious_degree"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R21",
    ),
    RuleRecord(
        rule_id="R22",
        source="Phaladeepika",
        chapter="Ch.2 v.9",
        school="all",
        category="retrograde",
        description=(
            "Retrograde bhavesh: outer planets (Jupiter/Saturn) rx gain inner strength "
            "(+0.25); inner planets (Mercury/Venus/Mars) rx have disrupted significations "
            "(-0.5). Sun/Moon never retrograde. "
            "Source: Phaladeepika Ch.2 v.9; BPHS Ch.3 — vakra planets behave unusually."
        ),
        confidence=0.85,
        tags=["retrograde", "vakra", "bhavesh", "inner_planet", "outer_planet"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R22",
    ),
    RuleRecord(
        rule_id="R23",
        source="BPHS",
        chapter="Ch.66",
        school="all",
        category="ashtakavarga",
        description=(
            "Sarvashtakavarga (SAV) bindus ≥ 5 in the house sign — house has "
            "above-average planetary support across all 8 contributing factors. "
            "Source: BPHS Ch.66 — SAV bindus measure cumulative planetary strength."
        ),
        confidence=0.9,
        tags=["ashtakavarga", "sav", "bindus", "sarva"],
        implemented=True,
        engine_ref="multi_axis_scoring._score_one_house:R23",
    ),
]

for _r in _RULES:
    EXISTING_RULES_REGISTRY.add(_r)
