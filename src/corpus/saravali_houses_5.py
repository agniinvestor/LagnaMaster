"""src/corpus/saravali_houses_5.py — Saravali Jupiter in 12 Houses (Ch.38).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_JUPITER_H1_DATA = [
    ("jupiter", "house_placement", 1, {}, "favorable", "strong", ['character_temperament', 'physical_appearance'], ['jupiter', 'saravali', 'house_placement', 'house_1'], "Ch.38 v.1", "Jupiter in 1st: noble and dignified personality, well-built body, wise and generous nature"),
    ("jupiter", "house_placement", 1, {}, "favorable", "strong", ['intelligence_education'], ['jupiter', 'saravali', 'house_placement', 'house_1'], "Ch.38 v.2", "Jupiter in 1st: natural wisdom, philosophical mind, learned and respected"),
    ("jupiter", "house_placement", 1, {}, "favorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_1'], "Ch.38 v.3", "Jupiter in 1st: self-earned wealth through wisdom, fortunate and prosperous"),
    ("jupiter", "house_placement", 1, {}, "favorable", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_1'], "Ch.38 v.4", "Jupiter in 1st: respected and honored, known for virtue and learning"),
    ("jupiter", "house_placement", 1, {}, "favorable", "moderate", ['longevity'], ['jupiter', 'saravali', 'house_placement', 'house_1'], "Ch.38 v.5", "Jupiter in 1st: good health, long life, protected from major calamities"),
]

_JUPITER_H2_DATA = [
    ("jupiter", "house_placement", 2, {}, "favorable", "strong", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_2'], "Ch.38 v.6", "Jupiter in 2nd: great wealth, eloquent speech, family prosperity, treasury expertise"),
    ("jupiter", "house_placement", 2, {}, "favorable", "moderate", ['intelligence_education'], ['jupiter', 'saravali', 'house_placement', 'house_2'], "Ch.38 v.7", "Jupiter in 2nd: learned and wise speech, knowledge of scriptures, teaching ability"),
    ("jupiter", "house_placement", 2, {}, "favorable", "moderate", ['marriage'], ['jupiter', 'saravali', 'house_placement', 'house_2'], "Ch.38 v.8", "Jupiter in 2nd: harmonious family, devoted spouse, supportive relatives"),
    ("jupiter", "house_placement", 2, {}, "favorable", "moderate", ['physical_appearance'], ['jupiter', 'saravali', 'house_placement', 'house_2'], "Ch.38 v.9", "Jupiter in 2nd: attractive face, bright eyes, pleasant voice"),
]

_JUPITER_H3_DATA = [
    ("jupiter", "house_placement", 3, {}, "mixed", "moderate", ['character_temperament'], ['jupiter', 'saravali', 'house_placement', 'house_3'], "Ch.38 v.10", "Jupiter in 3rd: courageous but miserly, strained sibling relations, short-distance travel"),
    ("jupiter", "house_placement", 3, {}, "mixed", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_3'], "Ch.38 v.11", "Jupiter in 3rd: moderate income, gains through communication and travel"),
    ("jupiter", "house_placement", 3, {}, "mixed", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_3'], "Ch.38 v.12", "Jupiter in 3rd: local reputation, known in neighborhood, community involvement"),
    ("jupiter", "house_placement", 3, {}, "mixed", "moderate", ['enemies_litigation'], ['jupiter', 'saravali', 'house_placement', 'house_3'], "Ch.38 v.13", "Jupiter in 3rd: conflicts with siblings, neighbors, communication disputes"),
]

_JUPITER_H4_DATA = [
    ("jupiter", "house_placement", 4, {}, "favorable", "strong", ['property_vehicles'], ['jupiter', 'saravali', 'house_placement', 'house_4'], "Ch.38 v.14", "Jupiter in 4th: owns beautiful properties, luxury vehicles, comfortable home, digbala"),
    ("jupiter", "house_placement", 4, {}, "favorable", "strong", ['mental_health'], ['jupiter', 'saravali', 'house_placement', 'house_4'], "Ch.38 v.15", "Jupiter in 4th: deep inner peace, contentment, emotional stability, happy mother"),
    ("jupiter", "house_placement", 4, {}, "favorable", "moderate", ['intelligence_education'], ['jupiter', 'saravali', 'house_placement', 'house_4'], "Ch.38 v.16", "Jupiter in 4th: educated household, academic environment, learned atmosphere"),
    ("jupiter", "house_placement", 4, {}, "favorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_4'], "Ch.38 v.17", "Jupiter in 4th: wealth through land, agriculture, education, or real estate"),
    ("jupiter", "house_placement", 4, {}, "favorable", "moderate", ['marriage'], ['jupiter', 'saravali', 'house_placement', 'house_4'], "Ch.38 v.18", "Jupiter in 4th: harmonious domestic life, devoted spouse, happy family"),
]

_JUPITER_H5_DATA = [
    ("jupiter", "house_placement", 5, {}, "favorable", "strong", ['intelligence_education'], ['jupiter', 'saravali', 'house_placement', 'house_5'], "Ch.38 v.19", "Jupiter in 5th: supreme wisdom, scholarly brilliance, philosophical mastery, guru-like"),
    ("jupiter", "house_placement", 5, {}, "favorable", "strong", ['progeny'], ['jupiter', 'saravali', 'house_placement', 'house_5'], "Ch.38 v.20", "Jupiter in 5th: blessed with virtuous children, excellent offspring, joyful parenting"),
    ("jupiter", "house_placement", 5, {}, "favorable", "moderate", ['spirituality'], ['jupiter', 'saravali', 'house_placement', 'house_5'], "Ch.38 v.21", "Jupiter in 5th: past-life merit, mantra siddhi, devotional practice bears fruit"),
    ("jupiter", "house_placement", 5, {}, "favorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_5'], "Ch.38 v.22", "Jupiter in 5th: gains through speculation, creative ventures, intellectual property"),
    ("jupiter", "house_placement", 5, {}, "favorable", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_5'], "Ch.38 v.23", "Jupiter in 5th: acclaimed for wisdom, creative recognition, scholarly honors"),
]

_JUPITER_H6_DATA = [
    ("jupiter", "house_placement", 6, {}, "mixed", "moderate", ['enemies_litigation'], ['jupiter', 'saravali', 'house_placement', 'house_6'], "Ch.38 v.24", "Jupiter in 6th: enemies subdued through wisdom, legal skill, diplomatic victory"),
    ("jupiter", "house_placement", 6, {}, "mixed", "moderate", ['physical_health'], ['jupiter', 'saravali', 'house_placement', 'house_6'], "Ch.38 v.25", "Jupiter in 6th: liver complaints, obesity tendency, overindulgence in food"),
    ("jupiter", "house_placement", 6, {}, "mixed", "moderate", ['career_status'], ['jupiter', 'saravali', 'house_placement', 'house_6'], "Ch.38 v.26", "Jupiter in 6th: service-oriented career, healthcare, legal aid, charitable work"),
    ("jupiter", "house_placement", 6, {}, "unfavorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_6'], "Ch.38 v.27", "Jupiter in 6th: financial disputes, debts, losses through over-generosity"),
]

_JUPITER_H7_DATA = [
    ("jupiter", "house_placement", 7, {}, "favorable", "strong", ['marriage'], ['jupiter', 'saravali', 'house_placement', 'house_7'], "Ch.38 v.28", "Jupiter in 7th: wise and virtuous spouse, happy marriage, partnership brings fortune"),
    ("jupiter", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['jupiter', 'saravali', 'house_placement', 'house_7'], "Ch.38 v.29", "Jupiter in 7th: success through partnerships, advisory roles, diplomatic career"),
    ("jupiter", "house_placement", 7, {}, "favorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_7'], "Ch.38 v.30", "Jupiter in 7th: wealth through marriage, business partnerships, trade"),
    ("jupiter", "house_placement", 7, {}, "favorable", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_7'], "Ch.38 v.31", "Jupiter in 7th: popular and well-liked, known through partnerships"),
]

_JUPITER_H8_DATA = [
    ("jupiter", "house_placement", 8, {}, "unfavorable", "moderate", ['longevity'], ['jupiter', 'saravali', 'house_placement', 'house_8'], "Ch.38 v.32", "Jupiter in 8th: health fluctuations, liver issues, but generally long life"),
    ("jupiter", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['jupiter', 'saravali', 'house_placement', 'house_8'], "Ch.38 v.33", "Jupiter in 8th: deep occult knowledge, transformation through wisdom, research"),
    ("jupiter", "house_placement", 8, {}, "mixed", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_8'], "Ch.38 v.34", "Jupiter in 8th: inheritance, sudden gains, insurance benefits, but financial secrecy"),
    ("jupiter", "house_placement", 8, {}, "unfavorable", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_8'], "Ch.38 v.35", "Jupiter in 8th: hidden talents, unrecognized wisdom, private life preferred"),
]

_JUPITER_H9_DATA = [
    ("jupiter", "house_placement", 9, {}, "favorable", "strong", ['spirituality'], ['jupiter', 'saravali', 'house_placement', 'house_9'], "Ch.38 v.36", "Jupiter in 9th: supreme dharmic fortune, deeply religious, blessed by gurus, pilgrimage"),
    ("jupiter", "house_placement", 9, {}, "favorable", "strong", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_9'], "Ch.38 v.37", "Jupiter in 9th: abundant fortune, father wealthy and wise, blessed prosperity"),
    ("jupiter", "house_placement", 9, {}, "favorable", "strong", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_9'], "Ch.38 v.38", "Jupiter in 9th: renowned for virtue and wisdom, honored by institutions"),
    ("jupiter", "house_placement", 9, {}, "favorable", "moderate", ['foreign_travel'], ['jupiter', 'saravali', 'house_placement', 'house_9'], "Ch.38 v.39", "Jupiter in 9th: pilgrimage, foreign education, dharmic travel, international honor"),
    ("jupiter", "house_placement", 9, {}, "favorable", "moderate", ['career_status'], ['jupiter', 'saravali', 'house_placement', 'house_9'], "Ch.38 v.40", "Jupiter in 9th: success in education, law, religion, or philosophical work"),
]

_JUPITER_H10_DATA = [
    ("jupiter", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['jupiter', 'saravali', 'house_placement', 'house_10'], "Ch.38 v.41", "Jupiter in 10th: attains high positions, respected leader, professional eminence"),
    ("jupiter", "house_placement", 10, {}, "favorable", "strong", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_10'], "Ch.38 v.42", "Jupiter in 10th: widely renowned, public honors, lasting professional legacy"),
    ("jupiter", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_10'], "Ch.38 v.43", "Jupiter in 10th: wealth through career, institutional leadership, advisory income"),
    ("jupiter", "house_placement", 10, {}, "favorable", "moderate", ['character_temperament'], ['jupiter', 'saravali', 'house_placement', 'house_10'], "Ch.38 v.44", "Jupiter in 10th: righteous professional conduct, ethical leadership, dharmic career"),
]

_JUPITER_H11_DATA = [
    ("jupiter", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_11'], "Ch.38 v.45", "Jupiter in 11th: abundant gains, fulfilled desires, prosperous networks"),
    ("jupiter", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'house_11'], "Ch.38 v.46", "Jupiter in 11th: influential social circle, gains through learned connections"),
    ("jupiter", "house_placement", 11, {}, "favorable", "moderate", ['progeny'], ['jupiter', 'saravali', 'house_placement', 'house_11'], "Ch.38 v.47", "Jupiter in 11th: elder children prosper, gains through offspring"),
    ("jupiter", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['jupiter', 'saravali', 'house_placement', 'house_11'], "Ch.38 v.48", "Jupiter in 11th: professional networking success, institutional connections"),
]

_JUPITER_H12_DATA = [
    ("jupiter", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['jupiter', 'saravali', 'house_placement', 'house_12'], "Ch.38 v.49", "Jupiter in 12th: spiritual liberation tendency, moksha yoga, detachment from material"),
    ("jupiter", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['jupiter', 'saravali', 'house_placement', 'house_12'], "Ch.38 v.50", "Jupiter in 12th: generous to a fault, expenditure on charity, financial losses"),
    ("jupiter", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['jupiter', 'saravali', 'house_placement', 'house_12'], "Ch.38 v.51", "Jupiter in 12th: foreign settlement, pilgrimage, spiritual retreat abroad"),
    ("jupiter", "house_placement", 12, {}, "unfavorable", "moderate", ['progeny'], ['jupiter', 'saravali', 'house_placement', 'house_12'], "Ch.38 v.52", "Jupiter in 12th: few children, children settle abroad, distant from offspring"),
]

_JUPITER_GENERAL_DATA = [
    ("jupiter", "house_condition", "jupiter_digbala_1st", {}, "favorable", "strong", ['character_temperament', 'intelligence_education'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.53", "Jupiter digbala in 1st: supreme wisdom, noble personality"),
    ("jupiter", "house_condition", "jupiter_hamsa", {}, "favorable", "strong", ['spirituality', 'fame_reputation'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.54", "Jupiter in kendra own/exalted: Hamsa Yoga, saintly eminence"),
    ("jupiter", "house_condition", "jupiter_in_kendra", {}, "favorable", "strong", ['wealth', 'career_status'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.55", "Jupiter in kendra: foundation of fortune, professional wisdom"),
    ("jupiter", "house_condition", "jupiter_in_trikona", {}, "favorable", "strong", ['wealth', 'spirituality'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.56", "Jupiter in trikona: dharmic fortune, blessed wisdom"),
    ("jupiter", "house_condition", "jupiter_in_dusthana", {}, "mixed", "moderate", ['physical_health', 'wealth'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.57", "Jupiter in dusthana: wisdom tested, health from overindulgence"),
    ("jupiter", "house_condition", "jupiter_aspected_moon", {}, "favorable", "strong", ['wealth', 'mental_health'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.58", "Jupiter aspected by Moon: Gajakesari, emotional wisdom, prosperity"),
    ("jupiter", "house_condition", "jupiter_aspected_saturn", {}, "mixed", "moderate", ['career_status', 'spirituality'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.59", "Jupiter aspected by Saturn: structured wisdom, delayed recognition"),
    ("jupiter", "house_condition", "jupiter_vargottama", {}, "favorable", "strong", ['wealth', 'spirituality'], ['jupiter', 'saravali', 'house_placement', 'general'], "Ch.38 v.60", "Jupiter vargottama: amplified beneficence across all domains"),
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
            rule_id=rid, source="Saravali", chapter="Ch.38", school="parashari",
            category="house_predictions", description=desc, confidence=0.65,
            verse="Saravali " + vref, tags=tags, implemented=False, engine_ref="",
            primary_condition=pc, modifiers=[], exceptions=[],
            outcome_domains=domains, outcome_direction=direction,
            outcome_intensity=intensity, outcome_timing="dasha_dependent",
            lagna_scope=[], dasha_scope=[], verse_ref=vref,
            concordance_texts=[], divergence_notes="",
            phase="1B_matrix", system="natal",
            prediction_type="event",
            gender_scope="universal",
            certainty_level="definite",
            strength_condition="any",
            house_system="sign_based",
            ayanamsha_sensitive=False,
            evaluation_method="placement_check",
            last_modified_session="S305",
        ))
    return rules


def _build_all_rules() -> list[RuleRecord]:
    all_data = [
        (_JUPITER_H1_DATA, 2375),
        (_JUPITER_H2_DATA, 2380),
        (_JUPITER_H3_DATA, 2384),
        (_JUPITER_H4_DATA, 2388),
        (_JUPITER_H5_DATA, 2393),
        (_JUPITER_H6_DATA, 2398),
        (_JUPITER_H7_DATA, 2402),
        (_JUPITER_H8_DATA, 2406),
        (_JUPITER_H9_DATA, 2410),
        (_JUPITER_H10_DATA, 2415),
        (_JUPITER_H11_DATA, 2419),
        (_JUPITER_H12_DATA, 2423),
        (_JUPITER_GENERAL_DATA, 2427),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_5_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_5_REGISTRY.add(_rule)
