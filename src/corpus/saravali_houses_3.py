"""src/corpus/saravali_houses_3.py — Saravali Mars in 12 Houses (Ch.36).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_MARS_H1_DATA = [
    ("mars", "house_placement", 1, {}, "favorable", "strong", ['character_temperament'], ['mars', 'saravali', 'house_placement', 'house_1'], "Ch.36 v.1", "Mars in 1st: courageous and aggressive personality, athletic build, leadership through action"),
    ("mars", "house_placement", 1, {}, "mixed", "moderate", ['physical_health'], ['mars', 'saravali', 'house_placement', 'house_1'], "Ch.36 v.2", "Mars in 1st: prone to injuries, cuts, burns, fevers, strong but accident-prone"),
    ("mars", "house_placement", 1, {}, "unfavorable", "moderate", ['marriage'], ['mars', 'saravali', 'house_placement', 'house_1'], "Ch.36 v.3", "Mars in 1st: manglik dosha, aggressive in relationships, dominating partner"),
    ("mars", "house_placement", 1, {}, "favorable", "moderate", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_1'], "Ch.36 v.4", "Mars in 1st: success in military, police, sports, engineering, surgery"),
    ("mars", "house_placement", 1, {}, "mixed", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_1'], "Ch.36 v.5", "Mars in 1st: earns through own effort, impulsive spending, financial ups and downs"),
]

_MARS_H2_DATA = [
    ("mars", "house_placement", 2, {}, "mixed", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_2'], "Ch.36 v.6", "Mars in 2nd: wealth through property, engineering, or military, but financial aggression"),
    ("mars", "house_placement", 2, {}, "unfavorable", "moderate", ['intelligence_education'], ['mars', 'saravali', 'house_placement', 'house_2'], "Ch.36 v.7", "Mars in 2nd: abusive language, argumentative speech, causes family quarrels"),
    ("mars", "house_placement", 2, {}, "unfavorable", "moderate", ['marriage'], ['mars', 'saravali', 'house_placement', 'house_2'], "Ch.36 v.8", "Mars in 2nd: family disputes, harsh words hurt relationships"),
    ("mars", "house_placement", 2, {}, "mixed", "moderate", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_2'], "Ch.36 v.9", "Mars in 2nd: income through engineering, metals, or property"),
]

_MARS_H3_DATA = [
    ("mars", "house_placement", 3, {}, "favorable", "strong", ['character_temperament'], ['mars', 'saravali', 'house_placement', 'house_3'], "Ch.36 v.10", "Mars in 3rd: extremely courageous, adventurous, physically active, sports champion"),
    ("mars", "house_placement", 3, {}, "favorable", "moderate", ['enemies_litigation'], ['mars', 'saravali', 'house_placement', 'house_3'], "Ch.36 v.11", "Mars in 3rd: defeats enemies decisively, brave siblings, dominance"),
    ("mars", "house_placement", 3, {}, "favorable", "moderate", ['fame_reputation'], ['mars', 'saravali', 'house_placement', 'house_3'], "Ch.36 v.12", "Mars in 3rd: famous for valor, military honors, recognized courage"),
    ("mars", "house_placement", 3, {}, "favorable", "moderate", ['property_vehicles'], ['mars', 'saravali', 'house_placement', 'house_3'], "Ch.36 v.13", "Mars in 3rd: vehicles, land through courage, real estate success"),
]

_MARS_H4_DATA = [
    ("mars", "house_placement", 4, {}, "unfavorable", "moderate", ['property_vehicles'], ['mars', 'saravali', 'house_placement', 'house_4'], "Ch.36 v.14", "Mars in 4th: property disputes, fire damage to home, vehicle accidents"),
    ("mars", "house_placement", 4, {}, "unfavorable", "moderate", ['mental_health'], ['mars', 'saravali', 'house_placement', 'house_4'], "Ch.36 v.15", "Mars in 4th: domestic unrest, aggressive home environment, conflict with mother"),
    ("mars", "house_placement", 4, {}, "mixed", "moderate", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_4'], "Ch.36 v.16", "Mars in 4th: success in construction, real estate, mining, but domestic sacrifice"),
    ("mars", "house_placement", 4, {}, "unfavorable", "moderate", ['marriage'], ['mars', 'saravali', 'house_placement', 'house_4'], "Ch.36 v.17", "Mars in 4th: manglik dosha, domestic violence risk, aggressive home atmosphere"),
]

_MARS_H5_DATA = [
    ("mars", "house_placement", 5, {}, "mixed", "moderate", ['intelligence_education'], ['mars', 'saravali', 'house_placement', 'house_5'], "Ch.36 v.18", "Mars in 5th: sharp analytical mind, engineering talent, impulsive decisions"),
    ("mars", "house_placement", 5, {}, "unfavorable", "moderate", ['progeny'], ['mars', 'saravali', 'house_placement', 'house_5'], "Ch.36 v.19", "Mars in 5th: challenges with children, abortions possible, aggressive parenting"),
    ("mars", "house_placement", 5, {}, "mixed", "moderate", ['spirituality'], ['mars', 'saravali', 'house_placement', 'house_5'], "Ch.36 v.20", "Mars in 5th: interest in tantric practices, mantra siddhi, occult sciences"),
    ("mars", "house_placement", 5, {}, "favorable", "moderate", ['enemies_litigation'], ['mars', 'saravali', 'house_placement', 'house_5'], "Ch.36 v.21", "Mars in 5th: defeats enemies through strategy, competitive spirit"),
]

_MARS_H6_DATA = [
    ("mars", "house_placement", 6, {}, "favorable", "strong", ['enemies_litigation'], ['mars', 'saravali', 'house_placement', 'house_6'], "Ch.36 v.22", "Mars in 6th: destroys enemies completely, victory in competition, legal triumph"),
    ("mars", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_6'], "Ch.36 v.23", "Mars in 6th: success in military, police, surgery, law enforcement"),
    ("mars", "house_placement", 6, {}, "favorable", "moderate", ['physical_health'], ['mars', 'saravali', 'house_placement', 'house_6'], "Ch.36 v.24", "Mars in 6th: overcomes diseases, strong immunity, surgical recovery"),
    ("mars", "house_placement", 6, {}, "mixed", "moderate", ['marriage'], ['mars', 'saravali', 'house_placement', 'house_6'], "Ch.36 v.25", "Mars in 6th: conflicts in relationships, litigation in partnerships"),
]

_MARS_H7_DATA = [
    ("mars", "house_placement", 7, {}, "unfavorable", "strong", ['marriage'], ['mars', 'saravali', 'house_placement', 'house_7'], "Ch.36 v.26", "Mars in 7th: manglik dosha, aggressive spouse, marital conflict, possible separation"),
    ("mars", "house_placement", 7, {}, "mixed", "moderate", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_7'], "Ch.36 v.27", "Mars in 7th: success through competitive partnerships, engineering or metals business"),
    ("mars", "house_placement", 7, {}, "unfavorable", "moderate", ['longevity'], ['mars', 'saravali', 'house_placement', 'house_7'], "Ch.36 v.28", "Mars in 7th: partner health concerns, accidents through partnerships"),
    ("mars", "house_placement", 7, {}, "mixed", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_7'], "Ch.36 v.29", "Mars in 7th: financial disputes with partner, joint ventures conflict-prone"),
]

_MARS_H8_DATA = [
    ("mars", "house_placement", 8, {}, "unfavorable", "moderate", ['longevity'], ['mars', 'saravali', 'house_placement', 'house_8'], "Ch.36 v.30", "Mars in 8th: accidents, surgeries, chronic inflammation, blood disorders"),
    ("mars", "house_placement", 8, {}, "mixed", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_8'], "Ch.36 v.31", "Mars in 8th: sudden gains and losses, inheritance through conflict, insurance"),
    ("mars", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['mars', 'saravali', 'house_placement', 'house_8'], "Ch.36 v.32", "Mars in 8th: tantric practices, transformation through crisis, occult research"),
    ("mars", "house_placement", 8, {}, "unfavorable", "moderate", ['fame_reputation'], ['mars', 'saravali', 'house_placement', 'house_8'], "Ch.36 v.33", "Mars in 8th: scandalous events, accidents publicized, reputation through crisis"),
]

_MARS_H9_DATA = [
    ("mars", "house_placement", 9, {}, "mixed", "moderate", ['spirituality'], ['mars', 'saravali', 'house_placement', 'house_9'], "Ch.36 v.34", "Mars in 9th: aggressive dharma, fights for beliefs, conflicts with father"),
    ("mars", "house_placement", 9, {}, "unfavorable", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_9'], "Ch.36 v.35", "Mars in 9th: fortune through struggle, father-son conflict, religious disputes"),
    ("mars", "house_placement", 9, {}, "mixed", "moderate", ['foreign_travel'], ['mars', 'saravali', 'house_placement', 'house_9'], "Ch.36 v.36", "Mars in 9th: travel for military or sports, conflicts abroad"),
    ("mars", "house_placement", 9, {}, "unfavorable", "moderate", ['character_temperament'], ['mars', 'saravali', 'house_placement', 'house_9'], "Ch.36 v.37", "Mars in 9th: conflicts with guru, challenges dharmic authority"),
]

_MARS_H10_DATA = [
    ("mars", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['mars', 'saravali', 'house_placement', 'house_10'], "Ch.36 v.38", "Mars in 10th: success in military, engineering, surgery, sports, police, digbala"),
    ("mars", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['mars', 'saravali', 'house_placement', 'house_10'], "Ch.36 v.39", "Mars in 10th: famous for professional achievements, competitive excellence"),
    ("mars", "house_placement", 10, {}, "mixed", "moderate", ['character_temperament'], ['mars', 'saravali', 'house_placement', 'house_10'], "Ch.36 v.40", "Mars in 10th: authoritative but aggressive, commands through strength"),
    ("mars", "house_placement", 10, {}, "favorable", "moderate", ['property_vehicles'], ['mars', 'saravali', 'house_placement', 'house_10'], "Ch.36 v.41", "Mars in 10th: land through government, military quarters, engineering projects"),
]

_MARS_H11_DATA = [
    ("mars", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_11'], "Ch.36 v.42", "Mars in 11th: abundant gains through courage, property deals, engineering profits"),
    ("mars", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['mars', 'saravali', 'house_placement', 'house_11'], "Ch.36 v.43", "Mars in 11th: famous friends, gains through military or sports connections"),
    ("mars", "house_placement", 11, {}, "favorable", "moderate", ['enemies_litigation'], ['mars', 'saravali', 'house_placement', 'house_11'], "Ch.36 v.44", "Mars in 11th: elder sibling support, networks of powerful people"),
    ("mars", "house_placement", 11, {}, "favorable", "moderate", ['character_temperament'], ['mars', 'saravali', 'house_placement', 'house_11'], "Ch.36 v.45", "Mars in 11th: powerful friends, martial allies, competitive networks"),
]

_MARS_H12_DATA = [
    ("mars", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['mars', 'saravali', 'house_placement', 'house_12'], "Ch.36 v.46", "Mars in 12th: financial losses through aggression, legal penalties, fines"),
    ("mars", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['mars', 'saravali', 'house_placement', 'house_12'], "Ch.36 v.47", "Mars in 12th: settlement abroad through military or engineering, exile possible"),
    ("mars", "house_placement", 12, {}, "unfavorable", "moderate", ['physical_health'], ['mars', 'saravali', 'house_placement', 'house_12'], "Ch.36 v.48", "Mars in 12th: hospitalization from injuries, hidden enemies cause physical harm"),
    ("mars", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['mars', 'saravali', 'house_placement', 'house_12'], "Ch.36 v.49", "Mars in 12th: tantric practice, energy work, kundalini through physical discipline"),
]

_MARS_GENERAL_DATA = [
    ("mars", "house_condition", "mars_digbala_10th", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.50", "Mars digbala in 10th: supreme professional courage, military/engineering fame"),
    ("mars", "house_condition", "mars_manglik", {}, "unfavorable", "strong", ['marriage'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.51", "Mars in 1/4/7/8/12: Manglik dosha, marital difficulties, partner compatibility crucial"),
    ("mars", "house_condition", "mars_ruchaka", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.52", "Mars in kendra own/exalted: Ruchaka Yoga, martial eminence, commanding authority"),
    ("mars", "house_condition", "mars_in_kendra", {}, "favorable", "moderate", ['career_status', 'character_temperament'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.53", "Mars in kendra: angular courage, professional strength, action-oriented leadership"),
    ("mars", "house_condition", "mars_in_dusthana", {}, "mixed", "moderate", ['enemies_litigation', 'physical_health'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.54", "Mars in dusthana: destroys enemies in 6th, but health/accident risk in 8th/12th"),
    ("mars", "house_condition", "mars_aspected_jupiter", {}, "favorable", "moderate", ['career_status', 'spirituality'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.55", "Mars aspected by Jupiter: righteous courage, dharmic warrior, blessed action"),
    ("mars", "house_condition", "mars_aspected_saturn", {}, "unfavorable", "moderate", ['physical_health', 'enemies_litigation'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.56", "Mars aspected by Saturn: accidents, chronic inflammation, legal battles, obstruction"),
    ("mars", "house_condition", "mars_combustion", {}, "unfavorable", "moderate", ['character_temperament', 'physical_health'], ['mars', 'saravali', 'house_placement', 'general'], "Ch.36 v.57", "Mars combust: suppressed courage, internalized aggression, hidden anger"),
]


def _make_house_rules(data: list, start_id: int) -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    for i, t in enumerate(data):
        planet, ptype, pval, extra, direction, intensity, domains, tags, vref, desc = t
        pc = {"planet": planet, "placement_type": ptype, **extra}
        if ptype == "house_placement":
            pc["placement_value"] = [pval]
            pc["house"] = pval
        elif ptype == "house_condition":
            pc["placement_value"] = []
            pc["yoga_label"] = pval
        rid = f"SAV{start_id + i}"
        rules.append(RuleRecord(
            rule_id=rid, source="Saravali", chapter="Ch.36", school="parashari",
            category="house_predictions", description=desc, confidence=0.65,
            verse="Saravali " + vref, tags=tags, implemented=False, engine_ref="",
            primary_condition=pc, modifiers=[], exceptions=[],
            outcome_domains=domains, outcome_direction=direction,
            outcome_intensity=intensity, outcome_timing="dasha_dependent",
            lagna_scope=[], dasha_scope=[], verse_ref=vref,
            concordance_texts=[], divergence_notes="",
            phase="1B_matrix", system="natal",
        ))
    return rules


def _build_all_rules() -> list[RuleRecord]:
    all_data = [
        (_MARS_H1_DATA, 2261),
        (_MARS_H2_DATA, 2266),
        (_MARS_H3_DATA, 2270),
        (_MARS_H4_DATA, 2274),
        (_MARS_H5_DATA, 2278),
        (_MARS_H6_DATA, 2282),
        (_MARS_H7_DATA, 2286),
        (_MARS_H8_DATA, 2290),
        (_MARS_H9_DATA, 2294),
        (_MARS_H10_DATA, 2298),
        (_MARS_H11_DATA, 2302),
        (_MARS_H12_DATA, 2306),
        (_MARS_GENERAL_DATA, 2310),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_3_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_3_REGISTRY.add(_rule)
