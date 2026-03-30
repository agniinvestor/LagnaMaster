"""src/corpus/saravali_houses_2.py — Saravali Moon in 12 Houses (Ch.35).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_MOON_H1_DATA = [
    ("moon", "house_placement", 1, {}, "favorable", "strong", ['physical_appearance', 'character_temperament'], ['moon', 'saravali', 'house_placement', 'house_1'], "Ch.35 v.1", "Moon in 1st: attractive personality, popular, emotionally expressive, charming demeanor"),
    ("moon", "house_placement", 1, {}, "favorable", "moderate", ['mental_health'], ['moon', 'saravali', 'house_placement', 'house_1'], "Ch.35 v.2", "Moon in 1st: peaceful mind when strong, imaginative, receptive to others feelings"),
    ("moon", "house_placement", 1, {}, "mixed", "moderate", ['physical_health'], ['moon', 'saravali', 'house_placement', 'house_1'], "Ch.35 v.3", "Moon in 1st: watery constitution, prone to colds, phlegmatic, needs hydration"),
    ("moon", "house_placement", 1, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_1'], "Ch.35 v.4", "Moon in 1st: income through public dealings, fluctuating but generous resources"),
    ("moon", "house_placement", 1, {}, "mixed", "moderate", ['foreign_travel'], ['moon', 'saravali', 'house_placement', 'house_1'], "Ch.35 v.5", "Moon in 1st: travels frequently, restless disposition, changes residence often"),
]

_MOON_H2_DATA = [
    ("moon", "house_placement", 2, {}, "favorable", "strong", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_2'], "Ch.35 v.6", "Moon in 2nd: wealth through public dealings, food industry, liquids, emotional intelligence"),
    ("moon", "house_placement", 2, {}, "favorable", "moderate", ['intelligence_education'], ['moon', 'saravali', 'house_placement', 'house_2'], "Ch.35 v.7", "Moon in 2nd: sweet and persuasive speech, poetic ability, melodious voice"),
    ("moon", "house_placement", 2, {}, "favorable", "moderate", ['marriage'], ['moon', 'saravali', 'house_placement', 'house_2'], "Ch.35 v.8", "Moon in 2nd: beautiful family life, close to mother, nurturing family atmosphere"),
    ("moon", "house_placement", 2, {}, "favorable", "moderate", ['physical_appearance'], ['moon', 'saravali', 'house_placement', 'house_2'], "Ch.35 v.9", "Moon in 2nd: beautiful face, attractive eyes, soft and pleasing features"),
    ("moon", "house_placement", 2, {}, "favorable", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_2'], "Ch.35 v.10", "Moon in 2nd: success in food, beverages, dairy, or beauty industries"),
]

_MOON_H3_DATA = [
    ("moon", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['moon', 'saravali', 'house_placement', 'house_3'], "Ch.35 v.11", "Moon in 3rd: courageous in gentle way, mental strength, creative pursuits"),
    ("moon", "house_placement", 3, {}, "mixed", "moderate", ['enemies_litigation'], ['moon', 'saravali', 'house_placement', 'house_3'], "Ch.35 v.12", "Moon in 3rd: emotional conflicts with siblings, moody communications"),
    ("moon", "house_placement", 3, {}, "favorable", "moderate", ['intelligence_education'], ['moon', 'saravali', 'house_placement', 'house_3'], "Ch.35 v.13", "Moon in 3rd: creative writing, artistic communication, media skills"),
    ("moon", "house_placement", 3, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_3'], "Ch.35 v.14", "Moon in 3rd: income through writing, short trips, communication-based commerce"),
]

_MOON_H4_DATA = [
    ("moon", "house_placement", 4, {}, "favorable", "strong", ['property_vehicles'], ['moon', 'saravali', 'house_placement', 'house_4'], "Ch.35 v.15", "Moon in 4th: beautiful home, domestic happiness, vehicles, land near water, digbala"),
    ("moon", "house_placement", 4, {}, "favorable", "strong", ['mental_health'], ['moon', 'saravali', 'house_placement', 'house_4'], "Ch.35 v.16", "Moon in 4th: peace of mind, emotional contentment, strong mother relationship"),
    ("moon", "house_placement", 4, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_4'], "Ch.35 v.17", "Moon in 4th: wealth through real estate, agriculture, or water-related industries"),
    ("moon", "house_placement", 4, {}, "favorable", "moderate", ['progeny'], ['moon', 'saravali', 'house_placement', 'house_4'], "Ch.35 v.18", "Moon in 4th: emotional bond with children, nurturing parenting, family traditions"),
    ("moon", "house_placement", 4, {}, "favorable", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_4'], "Ch.35 v.19", "Moon in 4th: success in hospitality, real estate, agriculture, dairy farming"),
]

_MOON_H5_DATA = [
    ("moon", "house_placement", 5, {}, "favorable", "strong", ['intelligence_education'], ['moon', 'saravali', 'house_placement', 'house_5'], "Ch.35 v.20", "Moon in 5th: creative brilliance, artistic talent, imaginative mind, intuitive learning"),
    ("moon", "house_placement", 5, {}, "favorable", "moderate", ['progeny'], ['moon', 'saravali', 'house_placement', 'house_5'], "Ch.35 v.21", "Moon in 5th: blessed with children especially daughters, emotional bond with offspring"),
    ("moon", "house_placement", 5, {}, "favorable", "moderate", ['spirituality'], ['moon', 'saravali', 'house_placement', 'house_5'], "Ch.35 v.22", "Moon in 5th: devotional nature, past-life merit, mantras and prayers effective"),
    ("moon", "house_placement", 5, {}, "favorable", "moderate", ['fame_reputation'], ['moon', 'saravali', 'house_placement', 'house_5'], "Ch.35 v.23", "Moon in 5th: popular and well-liked, creative reputation, emotional charisma"),
    ("moon", "house_placement", 5, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_5'], "Ch.35 v.24", "Moon in 5th: gains through speculation, creative income, entertainment"),
]

_MOON_H6_DATA = [
    ("moon", "house_placement", 6, {}, "unfavorable", "moderate", ['physical_health'], ['moon', 'saravali', 'house_placement', 'house_6'], "Ch.35 v.25", "Moon in 6th: stomach disorders, water-related ailments, emotional eating"),
    ("moon", "house_placement", 6, {}, "unfavorable", "moderate", ['enemies_litigation'], ['moon', 'saravali', 'house_placement', 'house_6'], "Ch.35 v.26", "Moon in 6th: enemies through emotional conflicts, maternal side disputes"),
    ("moon", "house_placement", 6, {}, "mixed", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_6'], "Ch.35 v.27", "Moon in 6th: service-oriented career, nursing, hospitality, healthcare, catering"),
    ("moon", "house_placement", 6, {}, "mixed", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_6'], "Ch.35 v.28", "Moon in 6th: frequent job changes, service in public sector, emotional workplace issues"),
]

_MOON_H7_DATA = [
    ("moon", "house_placement", 7, {}, "favorable", "moderate", ['marriage'], ['moon', 'saravali', 'house_placement', 'house_7'], "Ch.35 v.29", "Moon in 7th: attractive and emotional spouse, romantic marriage, good family"),
    ("moon", "house_placement", 7, {}, "mixed", "moderate", ['marriage'], ['moon', 'saravali', 'house_placement', 'house_7'], "Ch.35 v.30", "Moon in 7th: multiple relationships possible, emotional dependency on partner"),
    ("moon", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_7'], "Ch.35 v.31", "Moon in 7th: success through public dealings, partnerships, trade in liquids"),
    ("moon", "house_placement", 7, {}, "favorable", "moderate", ['physical_appearance'], ['moon', 'saravali', 'house_placement', 'house_7'], "Ch.35 v.32", "Moon in 7th: attractive partner, good-looking couple, social popularity"),
]

_MOON_H8_DATA = [
    ("moon", "house_placement", 8, {}, "unfavorable", "moderate", ['longevity'], ['moon', 'saravali', 'house_placement', 'house_8'], "Ch.35 v.33", "Moon in 8th: health fluctuations, emotional crises, mother health concerns"),
    ("moon", "house_placement", 8, {}, "unfavorable", "moderate", ['mental_health'], ['moon', 'saravali', 'house_placement', 'house_8'], "Ch.35 v.34", "Moon in 8th: anxiety, depression tendency, fear of unknown, disturbed sleep"),
    ("moon", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['moon', 'saravali', 'house_placement', 'house_8'], "Ch.35 v.35", "Moon in 8th: occult sensitivity, psychic ability, transformation through crisis"),
    ("moon", "house_placement", 8, {}, "unfavorable", "moderate", ['physical_health'], ['moon', 'saravali', 'house_placement', 'house_8'], "Ch.35 v.36", "Moon in 8th: chronic ailments, water-related diseases, emotional health crises"),
]

_MOON_H9_DATA = [
    ("moon", "house_placement", 9, {}, "favorable", "strong", ['spirituality'], ['moon', 'saravali', 'house_placement', 'house_9'], "Ch.35 v.37", "Moon in 9th: devotional nature, pilgrimage, blessed by mother, dharmic living"),
    ("moon", "house_placement", 9, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_9'], "Ch.35 v.38", "Moon in 9th: fortune through travel, water-related gains, maternal inheritance"),
    ("moon", "house_placement", 9, {}, "favorable", "moderate", ['fame_reputation'], ['moon', 'saravali', 'house_placement', 'house_9'], "Ch.35 v.39", "Moon in 9th: popular and well-liked, public recognition, charitable reputation"),
    ("moon", "house_placement", 9, {}, "favorable", "moderate", ['character_temperament'], ['moon', 'saravali', 'house_placement', 'house_9'], "Ch.35 v.40", "Moon in 9th: virtuous and charitable nature, generous, spiritually inclined"),
]

_MOON_H10_DATA = [
    ("moon", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_10'], "Ch.35 v.41", "Moon in 10th: public career, fame through service, popularity, leadership through empathy"),
    ("moon", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['moon', 'saravali', 'house_placement', 'house_10'], "Ch.35 v.42", "Moon in 10th: widely known public figure, emotional connection with masses"),
    ("moon", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_10'], "Ch.35 v.43", "Moon in 10th: income through public dealings, government service, emotional intelligence at work"),
    ("moon", "house_placement", 10, {}, "favorable", "moderate", ['property_vehicles'], ['moon', 'saravali', 'house_placement', 'house_10'], "Ch.35 v.44", "Moon in 10th: government service, public vehicles, comfortable official residence"),
]

_MOON_H11_DATA = [
    ("moon", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_11'], "Ch.35 v.45", "Moon in 11th: abundant gains, fulfillment of desires, wealthy female friends"),
    ("moon", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['moon', 'saravali', 'house_placement', 'house_11'], "Ch.35 v.46", "Moon in 11th: popular in social circles, gains through women, networking"),
    ("moon", "house_placement", 11, {}, "favorable", "moderate", ['progeny'], ['moon', 'saravali', 'house_placement', 'house_11'], "Ch.35 v.47", "Moon in 11th: children bring gains, elder sibling support, community involvement"),
    ("moon", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['moon', 'saravali', 'house_placement', 'house_11'], "Ch.35 v.48", "Moon in 11th: success through social connections, public networks, community leadership"),
]

_MOON_H12_DATA = [
    ("moon", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['moon', 'saravali', 'house_placement', 'house_12'], "Ch.35 v.49", "Moon in 12th: financial losses, expenditure on pleasures, hidden expenses"),
    ("moon", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['moon', 'saravali', 'house_placement', 'house_12'], "Ch.35 v.50", "Moon in 12th: travels abroad, settlement in foreign land, expenses through travel"),
    ("moon", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['moon', 'saravali', 'house_placement', 'house_12'], "Ch.35 v.51", "Moon in 12th: meditation ability, spiritual sensitivity, isolation tendencies"),
    ("moon", "house_placement", 12, {}, "unfavorable", "moderate", ['mental_health'], ['moon', 'saravali', 'house_placement', 'house_12'], "Ch.35 v.52", "Moon in 12th: insomnia, vivid dreams, emotional isolation, psychic sensitivity"),
]

_MOON_GENERAL_DATA = [
    ("moon", "house_condition", "moon_digbala_4th", {}, "favorable", "strong", ['mental_health', 'property_vehicles'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.53", "Moon digbala in 4th: supreme domestic happiness, emotional peace, beautiful home"),
    ("moon", "house_condition", "moon_waxing_house", {}, "favorable", "moderate", ['wealth', 'mental_health'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.54", "Waxing Moon: amplified beneficence, positive emotions, growing prosperity"),
    ("moon", "house_condition", "moon_waning_house", {}, "unfavorable", "moderate", ['mental_health', 'wealth'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.55", "Waning Moon: diminished emotional strength, declining resources, anxiety"),
    ("moon", "house_condition", "moon_full", {}, "favorable", "strong", ['wealth', 'mental_health'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.56", "Full Moon: maximum emotional strength, prosperity, creative power"),
    ("moon", "house_condition", "moon_new", {}, "unfavorable", "moderate", ['mental_health', 'wealth'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.57", "New Moon: diminished strength, emotional depletion, vulnerability"),
    ("moon", "house_condition", "moon_in_kendra", {}, "favorable", "moderate", ['mental_health', 'career_status'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.58", "Moon in kendra: emotional stability, public presence, domestic foundation"),
    ("moon", "house_condition", "moon_in_dusthana", {}, "unfavorable", "moderate", ['mental_health', 'physical_health'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.59", "Moon in dusthana: emotional disturbance, health fluctuation, anxiety"),
    ("moon", "house_condition", "moon_aspected_jupiter", {}, "favorable", "strong", ['wealth', 'mental_health'], ['moon', 'saravali', 'house_placement', 'general'], "Ch.35 v.60", "Moon aspected by Jupiter: Gajakesari elements, emotional wisdom, prosperity"),
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
            rule_id=rid, source="Saravali", chapter="Ch.35", school="parashari",
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
        (_MOON_H1_DATA, 2201),
        (_MOON_H2_DATA, 2206),
        (_MOON_H3_DATA, 2211),
        (_MOON_H4_DATA, 2215),
        (_MOON_H5_DATA, 2220),
        (_MOON_H6_DATA, 2225),
        (_MOON_H7_DATA, 2229),
        (_MOON_H8_DATA, 2233),
        (_MOON_H9_DATA, 2237),
        (_MOON_H10_DATA, 2241),
        (_MOON_H11_DATA, 2245),
        (_MOON_H12_DATA, 2249),
        (_MOON_GENERAL_DATA, 2253),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_2_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_2_REGISTRY.add(_rule)
