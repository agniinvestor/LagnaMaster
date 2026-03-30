"""src/corpus/saravali_houses_4.py — Saravali Mercury in 12 Houses (Ch.37).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_MERCURY_H1_DATA = [
    ("mercury", "house_placement", 1, {}, "favorable", "strong", ['intelligence_education', 'character_temperament'], ['mercury', 'saravali', 'house_placement', 'house_1'], "Ch.37 v.1", "Mercury in 1st: brilliant and witty, youthful appearance, eloquent communicator, digbala"),
    ("mercury", "house_placement", 1, {}, "favorable", "moderate", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_1'], "Ch.37 v.2", "Mercury in 1st: success through intellect, versatile professional, multiple skills"),
    ("mercury", "house_placement", 1, {}, "favorable", "moderate", ['physical_appearance'], ['mercury', 'saravali', 'house_placement', 'house_1'], "Ch.37 v.3", "Mercury in 1st: youthful and attractive, expressive face, lively eyes"),
    ("mercury", "house_placement", 1, {}, "favorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_1'], "Ch.37 v.4", "Mercury in 1st: multiple income sources, commercial instinct, business-minded"),
    ("mercury", "house_placement", 1, {}, "mixed", "moderate", ['physical_health'], ['mercury', 'saravali', 'house_placement', 'house_1'], "Ch.37 v.5", "Mercury in 1st: nervous energy, skin sensitivity, restless constitution"),
]

_MERCURY_H2_DATA = [
    ("mercury", "house_placement", 2, {}, "favorable", "strong", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_2'], "Ch.37 v.6", "Mercury in 2nd: wealth through commerce, writing, teaching, intellectual pursuits"),
    ("mercury", "house_placement", 2, {}, "favorable", "strong", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_2'], "Ch.37 v.7", "Mercury in 2nd: persuasive speech, multilingual, skilled in debate, eloquent"),
    ("mercury", "house_placement", 2, {}, "favorable", "moderate", ['marriage'], ['mercury', 'saravali', 'house_placement', 'house_2'], "Ch.37 v.8", "Mercury in 2nd: communicative family, intellectual household, educated relatives"),
    ("mercury", "house_placement", 2, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_2'], "Ch.37 v.9", "Mercury in 2nd: famous for eloquence, respected speaker, persuasive voice"),
]

_MERCURY_H3_DATA = [
    ("mercury", "house_placement", 3, {}, "favorable", "strong", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_3'], "Ch.37 v.10", "Mercury in 3rd: excellent writer, media success, skilled communicator"),
    ("mercury", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['mercury', 'saravali', 'house_placement', 'house_3'], "Ch.37 v.11", "Mercury in 3rd: adaptable, travels for business, active social life"),
    ("mercury", "house_placement", 3, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_3'], "Ch.37 v.12", "Mercury in 3rd: known for communication skills, published works"),
    ("mercury", "house_placement", 3, {}, "favorable", "moderate", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_3'], "Ch.37 v.13", "Mercury in 3rd: success in writing, journalism, media, publishing"),
]

_MERCURY_H4_DATA = [
    ("mercury", "house_placement", 4, {}, "favorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_4'], "Ch.37 v.14", "Mercury in 4th: educated household, intellectual home, study at home"),
    ("mercury", "house_placement", 4, {}, "favorable", "moderate", ['property_vehicles'], ['mercury', 'saravali', 'house_placement', 'house_4'], "Ch.37 v.15", "Mercury in 4th: multiple vehicles, well-designed home, tech improvements"),
    ("mercury", "house_placement", 4, {}, "mixed", "moderate", ['mental_health'], ['mercury', 'saravali', 'house_placement', 'house_4'], "Ch.37 v.16", "Mercury in 4th: overthinking, mental restlessness, analytical anxiety"),
    ("mercury", "house_placement", 4, {}, "favorable", "moderate", ['marriage'], ['mercury', 'saravali', 'house_placement', 'house_4'], "Ch.37 v.17", "Mercury in 4th: communicative family, spouse values education"),
]

_MERCURY_H5_DATA = [
    ("mercury", "house_placement", 5, {}, "favorable", "strong", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_5'], "Ch.37 v.18", "Mercury in 5th: exceptional intellect, scholarly achievements, mathematical ability"),
    ("mercury", "house_placement", 5, {}, "favorable", "moderate", ['progeny'], ['mercury', 'saravali', 'house_placement', 'house_5'], "Ch.37 v.19", "Mercury in 5th: intelligent children, good education for offspring"),
    ("mercury", "house_placement", 5, {}, "favorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_5'], "Ch.37 v.20", "Mercury in 5th: gains through speculation, creative writing, intellectual property"),
    ("mercury", "house_placement", 5, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_5'], "Ch.37 v.21", "Mercury in 5th: creative recognition, published works, academic honors"),
]

_MERCURY_H6_DATA = [
    ("mercury", "house_placement", 6, {}, "favorable", "moderate", ['enemies_litigation'], ['mercury', 'saravali', 'house_placement', 'house_6'], "Ch.37 v.22", "Mercury in 6th: defeats enemies through intellect, legal acumen"),
    ("mercury", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_6'], "Ch.37 v.23", "Mercury in 6th: success in medicine, accounting, law, analysis"),
    ("mercury", "house_placement", 6, {}, "mixed", "moderate", ['physical_health'], ['mercury', 'saravali', 'house_placement', 'house_6'], "Ch.37 v.24", "Mercury in 6th: nervous disorders, skin issues, digestive sensitivity"),
    ("mercury", "house_placement", 6, {}, "unfavorable", "moderate", ['physical_health'], ['mercury', 'saravali', 'house_placement', 'house_6'], "Ch.37 v.25", "Mercury in 6th: nervous system disorders, skin diseases, stress illness"),
]

_MERCURY_H7_DATA = [
    ("mercury", "house_placement", 7, {}, "favorable", "moderate", ['marriage'], ['mercury', 'saravali', 'house_placement', 'house_7'], "Ch.37 v.26", "Mercury in 7th: intellectual spouse, partnership based on shared interests"),
    ("mercury", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_7'], "Ch.37 v.27", "Mercury in 7th: success through partnerships, business acumen"),
    ("mercury", "house_placement", 7, {}, "mixed", "moderate", ['marriage'], ['mercury', 'saravali', 'house_placement', 'house_7'], "Ch.37 v.28", "Mercury in 7th: multiple relationships possible, youthful partner"),
    ("mercury", "house_placement", 7, {}, "favorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_7'], "Ch.37 v.29", "Mercury in 7th: wealth through trade partnerships, commercial collaborations"),
]

_MERCURY_H8_DATA = [
    ("mercury", "house_placement", 8, {}, "mixed", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_8'], "Ch.37 v.30", "Mercury in 8th: research ability, occult knowledge, forensic expertise"),
    ("mercury", "house_placement", 8, {}, "unfavorable", "moderate", ['physical_health'], ['mercury', 'saravali', 'house_placement', 'house_8'], "Ch.37 v.31", "Mercury in 8th: nervous disorders, skin diseases, mysterious ailments"),
    ("mercury", "house_placement", 8, {}, "mixed", "moderate", ['longevity'], ['mercury', 'saravali', 'house_placement', 'house_8'], "Ch.37 v.32", "Mercury in 8th: medium longevity, analytical about health"),
    ("mercury", "house_placement", 8, {}, "unfavorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_8'], "Ch.37 v.33", "Mercury in 8th: commercial losses, fraud risk, financial secrets"),
]

_MERCURY_H9_DATA = [
    ("mercury", "house_placement", 9, {}, "favorable", "strong", ['spirituality', 'intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_9'], "Ch.37 v.34", "Mercury in 9th: scholarly dharma, philosophical writing, spiritual teaching"),
    ("mercury", "house_placement", 9, {}, "favorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_9'], "Ch.37 v.35", "Mercury in 9th: fortune through writing, publishing, teaching, foreign trade"),
    ("mercury", "house_placement", 9, {}, "favorable", "moderate", ['foreign_travel'], ['mercury', 'saravali', 'house_placement', 'house_9'], "Ch.37 v.36", "Mercury in 9th: intellectual foreign connections, study abroad"),
    ("mercury", "house_placement", 9, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_9'], "Ch.37 v.37", "Mercury in 9th: scholarly fame, published philosophical works"),
]

_MERCURY_H10_DATA = [
    ("mercury", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_10'], "Ch.37 v.38", "Mercury in 10th: success in business, administration, writing, media, technology"),
    ("mercury", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_10'], "Ch.37 v.39", "Mercury in 10th: known for professional intellect, business achievements"),
    ("mercury", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_10'], "Ch.37 v.40", "Mercury in 10th: wealth through career intellect, multiple income sources"),
    ("mercury", "house_placement", 10, {}, "favorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_10'], "Ch.37 v.41", "Mercury in 10th: expertise in management, administrative intelligence"),
]

_MERCURY_H11_DATA = [
    ("mercury", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_11'], "Ch.37 v.42", "Mercury in 11th: abundant gains through commerce, intellectual networks"),
    ("mercury", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['mercury', 'saravali', 'house_placement', 'house_11'], "Ch.37 v.43", "Mercury in 11th: popular in intellectual circles, communication gains"),
    ("mercury", "house_placement", 11, {}, "favorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_11'], "Ch.37 v.44", "Mercury in 11th: scholarly friends, diverse social circle"),
    ("mercury", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['mercury', 'saravali', 'house_placement', 'house_11'], "Ch.37 v.45", "Mercury in 11th: commercial networking, multiple business ventures"),
]

_MERCURY_H12_DATA = [
    ("mercury", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['mercury', 'saravali', 'house_placement', 'house_12'], "Ch.37 v.46", "Mercury in 12th: foreign education, intellectual work abroad, writing in seclusion"),
    ("mercury", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['mercury', 'saravali', 'house_placement', 'house_12'], "Ch.37 v.47", "Mercury in 12th: losses through poor communication, cheated in trade"),
    ("mercury", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['mercury', 'saravali', 'house_placement', 'house_12'], "Ch.37 v.48", "Mercury in 12th: meditation on mantras, analytical spirituality"),
    ("mercury", "house_placement", 12, {}, "unfavorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'house_placement', 'house_12'], "Ch.37 v.49", "Mercury in 12th: confused thinking, communication misunderstandings"),
]

_MERCURY_GENERAL_DATA = [
    ("mercury", "house_condition", "mercury_digbala_1st", {}, "favorable", "strong", ['intelligence_education', 'physical_appearance'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.50", "Mercury digbala in 1st: supreme intellect, youthful appearance, witty personality"),
    ("mercury", "house_condition", "mercury_bhadra", {}, "favorable", "strong", ['intelligence_education', 'fame_reputation'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.51", "Mercury in kendra own/exalted: Bhadra Yoga, intellectual eminence, scholarly fame"),
    ("mercury", "house_condition", "mercury_in_kendra", {}, "favorable", "moderate", ['intelligence_education', 'career_status'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.52", "Mercury in kendra: intellectual foundation, communication strength, commercial acumen"),
    ("mercury", "house_condition", "mercury_in_dusthana", {}, "unfavorable", "moderate", ['intelligence_education', 'physical_health'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.53", "Mercury in dusthana: confused thinking, nervous disorders, communication failures"),
    ("mercury", "house_condition", "mercury_combust", {}, "unfavorable", "moderate", ['intelligence_education', 'career_status'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.54", "Mercury combust: intellect overshadowed, speech impaired, commercial losses"),
    ("mercury", "house_condition", "mercury_retrograde", {}, "mixed", "moderate", ['intelligence_education', 'career_status'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.55", "Mercury retrograde: revisiting old ideas, communication delays, past-life intellectual karma"),
    ("mercury", "house_condition", "mercury_with_benefic", {}, "favorable", "moderate", ['intelligence_education', 'career_status'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.56", "Mercury with benefics: amplified intellectual beneficence, blessed communication"),
    ("mercury", "house_condition", "mercury_with_malefic", {}, "unfavorable", "moderate", ['intelligence_education', 'character_temperament'], ['mercury', 'saravali', 'house_placement', 'general'], "Ch.37 v.57", "Mercury with malefics: corrupted intellect, deceptive speech, misused intelligence"),
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
            rule_id=rid, source="Saravali", chapter="Ch.37", school="parashari",
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
        (_MERCURY_H1_DATA, 2318),
        (_MERCURY_H2_DATA, 2323),
        (_MERCURY_H3_DATA, 2327),
        (_MERCURY_H4_DATA, 2331),
        (_MERCURY_H5_DATA, 2335),
        (_MERCURY_H6_DATA, 2339),
        (_MERCURY_H7_DATA, 2343),
        (_MERCURY_H8_DATA, 2347),
        (_MERCURY_H9_DATA, 2351),
        (_MERCURY_H10_DATA, 2355),
        (_MERCURY_H11_DATA, 2359),
        (_MERCURY_H12_DATA, 2363),
        (_MERCURY_GENERAL_DATA, 2367),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_4_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_4_REGISTRY.add(_rule)
