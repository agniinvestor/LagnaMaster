"""src/corpus/saravali_houses_6.py — Saravali Venus in 12 Houses (Ch.39).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_VENUS_H1_DATA = [
    ("venus", "house_placement", 1, {}, "favorable", "strong", ['physical_appearance'], ['venus', 'saravali', 'house_placement', 'house_1'], "Ch.39 v.1", "Venus in 1st: strikingly beautiful, attractive personality, magnetic charm, graceful bearing"),
    ("venus", "house_placement", 1, {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_1'], "Ch.39 v.2", "Venus in 1st: romantic and loving nature, attracts partners easily, sensual personality"),
    ("venus", "house_placement", 1, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_1'], "Ch.39 v.3", "Venus in 1st: luxury through personal charm, income from beauty-related work"),
    ("venus", "house_placement", 1, {}, "favorable", "moderate", ['character_temperament'], ['venus', 'saravali', 'house_placement', 'house_1'], "Ch.39 v.4", "Venus in 1st: artistic nature, refined tastes, diplomatic, pleasure-loving"),
]

_VENUS_H2_DATA = [
    ("venus", "house_placement", 2, {}, "favorable", "strong", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_2'], "Ch.39 v.5", "Venus in 2nd: great wealth, luxury goods, precious gems, fine speech, beautiful family"),
    ("venus", "house_placement", 2, {}, "favorable", "moderate", ['intelligence_education'], ['venus', 'saravali', 'house_placement', 'house_2'], "Ch.39 v.6", "Venus in 2nd: sweet melodious speech, poetic ability, knowledge of arts"),
    ("venus", "house_placement", 2, {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_2'], "Ch.39 v.7", "Venus in 2nd: beautiful family, loving household, artistic home environment"),
    ("venus", "house_placement", 2, {}, "favorable", "moderate", ['physical_appearance'], ['venus', 'saravali', 'house_placement', 'house_2'], "Ch.39 v.8", "Venus in 2nd: attractive face, beautiful eyes, charming smile"),
]

_VENUS_H3_DATA = [
    ("venus", "house_placement", 3, {}, "favorable", "moderate", ['intelligence_education'], ['venus', 'saravali', 'house_placement', 'house_3'], "Ch.39 v.9", "Venus in 3rd: artistic communication, creative writing, media talent"),
    ("venus", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['venus', 'saravali', 'house_placement', 'house_3'], "Ch.39 v.10", "Venus in 3rd: social and charming, artistic hobbies, pleasure in travel"),
    ("venus", "house_placement", 3, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_3'], "Ch.39 v.11", "Venus in 3rd: income through arts, media, advertising, creative commerce"),
    ("venus", "house_placement", 3, {}, "mixed", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_3'], "Ch.39 v.12", "Venus in 3rd: flirtatious nature, multiple romantic interests, restless in love"),
]

_VENUS_H4_DATA = [
    ("venus", "house_placement", 4, {}, "favorable", "strong", ['property_vehicles'], ['venus', 'saravali', 'house_placement', 'house_4'], "Ch.39 v.13", "Venus in 4th: beautiful and luxurious home, comfort, elegant vehicles, domestic pleasure"),
    ("venus", "house_placement", 4, {}, "favorable", "moderate", ['mental_health'], ['venus', 'saravali', 'house_placement', 'house_4'], "Ch.39 v.14", "Venus in 4th: emotional contentment, aesthetic home environment, inner peace"),
    ("venus", "house_placement", 4, {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_4'], "Ch.39 v.15", "Venus in 4th: devoted spouse, beautiful domestic life, romantic home"),
    ("venus", "house_placement", 4, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_4'], "Ch.39 v.16", "Venus in 4th: wealth through property, interior design, hospitality"),
]

_VENUS_H5_DATA = [
    ("venus", "house_placement", 5, {}, "favorable", "strong", ['intelligence_education'], ['venus', 'saravali', 'house_placement', 'house_5'], "Ch.39 v.17", "Venus in 5th: exceptional artistic talent, creative genius, romantic intelligence"),
    ("venus", "house_placement", 5, {}, "favorable", "moderate", ['progeny'], ['venus', 'saravali', 'house_placement', 'house_5'], "Ch.39 v.18", "Venus in 5th: beautiful and artistic children, loving parent, creative family"),
    ("venus", "house_placement", 5, {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_5'], "Ch.39 v.19", "Venus in 5th: romantic love affairs, passionate courtship, poetic romance"),
    ("venus", "house_placement", 5, {}, "favorable", "moderate", ['fame_reputation'], ['venus', 'saravali', 'house_placement', 'house_5'], "Ch.39 v.20", "Venus in 5th: creative fame, artistic recognition, cultural celebrity"),
]

_VENUS_H6_DATA = [
    ("venus", "house_placement", 6, {}, "unfavorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_6'], "Ch.39 v.21", "Venus in 6th: romantic difficulties, conflicts in love, partner health issues"),
    ("venus", "house_placement", 6, {}, "mixed", "moderate", ['career_status'], ['venus', 'saravali', 'house_placement', 'house_6'], "Ch.39 v.22", "Venus in 6th: success in healthcare beauty, cosmetics, fashion service"),
    ("venus", "house_placement", 6, {}, "unfavorable", "moderate", ['physical_health'], ['venus', 'saravali', 'house_placement', 'house_6'], "Ch.39 v.23", "Venus in 6th: reproductive issues, urinary complaints, skin conditions"),
    ("venus", "house_placement", 6, {}, "mixed", "moderate", ['enemies_litigation'], ['venus', 'saravali', 'house_placement', 'house_6'], "Ch.39 v.24", "Venus in 6th: enemies through romantic entanglements, female rivals"),
]

_VENUS_H7_DATA = [
    ("venus", "house_placement", 7, {}, "favorable", "strong", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_7'], "Ch.39 v.25", "Venus in 7th: beautiful and loving spouse, happy marriage, romantic fulfillment"),
    ("venus", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['venus', 'saravali', 'house_placement', 'house_7'], "Ch.39 v.26", "Venus in 7th: success through partnerships, beauty business, diplomatic career"),
    ("venus", "house_placement", 7, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_7'], "Ch.39 v.27", "Venus in 7th: wealth through marriage, partner brings fortune"),
    ("venus", "house_placement", 7, {}, "favorable", "moderate", ['fame_reputation'], ['venus', 'saravali', 'house_placement', 'house_7'], "Ch.39 v.28", "Venus in 7th: popular couple, social recognition through partnership"),
]

_VENUS_H8_DATA = [
    ("venus", "house_placement", 8, {}, "mixed", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_8'], "Ch.39 v.29", "Venus in 8th: intense and transformative love, partner resources, sexual depth"),
    ("venus", "house_placement", 8, {}, "unfavorable", "moderate", ['longevity'], ['venus', 'saravali', 'house_placement', 'house_8'], "Ch.39 v.30", "Venus in 8th: reproductive health concerns, urinary issues, partner health worries"),
    ("venus", "house_placement", 8, {}, "mixed", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_8'], "Ch.39 v.31", "Venus in 8th: inheritance, partner wealth, insurance, occult arts income"),
    ("venus", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['venus', 'saravali', 'house_placement', 'house_8'], "Ch.39 v.32", "Venus in 8th: tantric practices, transformation through love, kundalini"),
]

_VENUS_H9_DATA = [
    ("venus", "house_placement", 9, {}, "favorable", "strong", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_9'], "Ch.39 v.33", "Venus in 9th: spouse from good family, dharmic marriage, fortunate partnership"),
    ("venus", "house_placement", 9, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_9'], "Ch.39 v.34", "Venus in 9th: fortune through arts, luxury trade, cultural institutions"),
    ("venus", "house_placement", 9, {}, "favorable", "moderate", ['foreign_travel'], ['venus', 'saravali', 'house_placement', 'house_9'], "Ch.39 v.35", "Venus in 9th: pleasure travel, artistic connections abroad, cultural exchange"),
    ("venus", "house_placement", 9, {}, "favorable", "moderate", ['spirituality'], ['venus', 'saravali', 'house_placement', 'house_9'], "Ch.39 v.36", "Venus in 9th: devotional beauty, bhakti path, aesthetic spirituality"),
]

_VENUS_H10_DATA = [
    ("venus", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['venus', 'saravali', 'house_placement', 'house_10'], "Ch.39 v.37", "Venus in 10th: success in arts, entertainment, fashion, diplomacy, luxury industries"),
    ("venus", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['venus', 'saravali', 'house_placement', 'house_10'], "Ch.39 v.38", "Venus in 10th: famous for beauty or artistic achievement, glamorous career"),
    ("venus", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_10'], "Ch.39 v.39", "Venus in 10th: wealth through creative profession, luxury brand leadership"),
    ("venus", "house_placement", 10, {}, "favorable", "moderate", ['character_temperament'], ['venus', 'saravali', 'house_placement', 'house_10'], "Ch.39 v.40", "Venus in 10th: diplomatic professional manner, charming public presence"),
]

_VENUS_H11_DATA = [
    ("venus", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_11'], "Ch.39 v.41", "Venus in 11th: abundant gains through arts, luxury, partnerships, female friends"),
    ("venus", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['venus', 'saravali', 'house_placement', 'house_11'], "Ch.39 v.42", "Venus in 11th: popular and well-liked, social success, glamorous circle"),
    ("venus", "house_placement", 11, {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_11'], "Ch.39 v.43", "Venus in 11th: romantic friendships, love through social networks"),
    ("venus", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['venus', 'saravali', 'house_placement', 'house_11'], "Ch.39 v.44", "Venus in 11th: artistic networking, gains through beauty industry connections"),
]

_VENUS_H12_DATA = [
    ("venus", "house_placement", 12, {}, "mixed", "moderate", ['marriage'], ['venus', 'saravali', 'house_placement', 'house_12'], "Ch.39 v.45", "Venus in 12th: secret love affairs, bed pleasures, foreign romantic connections"),
    ("venus", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['venus', 'saravali', 'house_placement', 'house_12'], "Ch.39 v.46", "Venus in 12th: pleasure in foreign lands, artistic work abroad, luxury overseas"),
    ("venus", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['venus', 'saravali', 'house_placement', 'house_12'], "Ch.39 v.47", "Venus in 12th: extravagant spending, losses through luxury, financial drain"),
    ("venus", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['venus', 'saravali', 'house_placement', 'house_12'], "Ch.39 v.48", "Venus in 12th: devotional surrender, beauty in solitude, artistic meditation"),
]

_VENUS_GENERAL_DATA = [
    ("venus", "house_condition", "venus_digbala_4th", {}, "favorable", "strong", ['property_vehicles', 'marriage'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.49", "Venus digbala in 4th: supreme domestic luxury, beautiful home, marital bliss"),
    ("venus", "house_condition", "venus_malavya", {}, "favorable", "strong", ['physical_appearance', 'wealth'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.50", "Venus in kendra own/exalted: Malavya Yoga, beauty, luxury, artistic eminence"),
    ("venus", "house_condition", "venus_in_kendra", {}, "favorable", "moderate", ['marriage', 'wealth'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.51", "Venus in kendra: romantic foundation, partnership strength, material comfort"),
    ("venus", "house_condition", "venus_in_trikona", {}, "favorable", "strong", ['marriage', 'wealth'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.52", "Venus in trikona: blessed love, fortunate romance, artistic fortune"),
    ("venus", "house_condition", "venus_in_dusthana", {}, "unfavorable", "moderate", ['marriage', 'physical_health'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.53", "Venus in dusthana: romantic difficulties, health issues, love struggles"),
    ("venus", "house_condition", "venus_aspected_jupiter", {}, "favorable", "strong", ['marriage', 'wealth'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.54", "Venus aspected by Jupiter: blessed love life, prosperous partnerships"),
    ("venus", "house_condition", "venus_aspected_saturn", {}, "mixed", "moderate", ['marriage', 'longevity'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.55", "Venus aspected by Saturn: delayed but lasting love, patient beauty"),
    ("venus", "house_condition", "venus_combust", {}, "unfavorable", "moderate", ['marriage', 'physical_appearance'], ['venus', 'saravali', 'house_placement', 'general'], "Ch.39 v.56", "Venus combust: diminished beauty and love fortune, partner suppressed"),
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
            rule_id=rid, source="Saravali", chapter="Ch.39", school="parashari",
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
        (_VENUS_H1_DATA, 2435),
        (_VENUS_H2_DATA, 2439),
        (_VENUS_H3_DATA, 2443),
        (_VENUS_H4_DATA, 2447),
        (_VENUS_H5_DATA, 2451),
        (_VENUS_H6_DATA, 2455),
        (_VENUS_H7_DATA, 2459),
        (_VENUS_H8_DATA, 2463),
        (_VENUS_H9_DATA, 2467),
        (_VENUS_H10_DATA, 2471),
        (_VENUS_H11_DATA, 2475),
        (_VENUS_H12_DATA, 2479),
        (_VENUS_GENERAL_DATA, 2483),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_6_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_6_REGISTRY.add(_rule)
