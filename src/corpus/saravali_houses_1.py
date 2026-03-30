"""src/corpus/saravali_houses_1.py — Saravali Sun in 12 Houses (Ch.34).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_SUN_H1_DATA = [
    ("sun", "house_placement", 1, {}, "favorable", "strong", ['physical_appearance', 'character_temperament'], ['sun', 'saravali', 'house_placement', 'house_1'], "Ch.34 v.1", "Sun in 1st: commanding personality, strong constitution, natural authority, leadership qualities"),
    ("sun", "house_placement", 1, {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_1'], "Ch.34 v.2", "Sun in 1st: government favor, administrative ability, recognized by superiors, rises quickly"),
    ("sun", "house_placement", 1, {}, "mixed", "moderate", ['physical_health'], ['sun', 'saravali', 'house_placement', 'house_1'], "Ch.34 v.3", "Sun in 1st: bilious constitution, prone to fevers, strong but overheating, pitta excess"),
    ("sun", "house_placement", 1, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_1'], "Ch.34 v.4", "Sun in 1st: self-earned wealth, independent income, financially confident, generous spending"),
    ("sun", "house_placement", 1, {}, "mixed", "moderate", ['marriage'], ['sun', 'saravali', 'house_placement', 'house_1'], "Ch.34 v.5", "Sun in 1st: ego in relationships, partner feels overshadowed, late marriage possible"),
]

_SUN_H2_DATA = [
    ("sun", "house_placement", 2, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_2'], "Ch.34 v.6", "Sun in 2nd: wealth through authority, government income, precious metals, treasury work"),
    ("sun", "house_placement", 2, {}, "mixed", "moderate", ['intelligence_education'], ['sun', 'saravali', 'house_placement', 'house_2'], "Ch.34 v.7", "Sun in 2nd: authoritative speech, direct communication, harsh but truthful words, commanding voice"),
    ("sun", "house_placement", 2, {}, "unfavorable", "moderate", ['marriage'], ['sun', 'saravali', 'house_placement', 'house_2'], "Ch.34 v.8", "Sun in 2nd: harsh speech strains family, dominating in domestic matters, family tensions"),
    ("sun", "house_placement", 2, {}, "mixed", "moderate", ['physical_health'], ['sun', 'saravali', 'house_placement', 'house_2'], "Ch.34 v.9", "Sun in 2nd: eye problems especially right eye, dental issues, facial skin problems"),
    ("sun", "house_placement", 2, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_2'], "Ch.34 v.10", "Sun in 2nd: respected for knowledge and speech, reputation through communication"),
]

_SUN_H3_DATA = [
    ("sun", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['sun', 'saravali', 'house_placement', 'house_3'], "Ch.34 v.11", "Sun in 3rd: courageous and bold, strong willpower, defeats enemies through might"),
    ("sun", "house_placement", 3, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_3'], "Ch.34 v.12", "Sun in 3rd: famous for valor, respected by siblings, neighborhood leadership"),
    ("sun", "house_placement", 3, {}, "mixed", "moderate", ['enemies_litigation'], ['sun', 'saravali', 'house_placement', 'house_3'], "Ch.34 v.13", "Sun in 3rd: friction with younger siblings, conflicts through pride, aggressive communications"),
    ("sun", "house_placement", 3, {}, "favorable", "moderate", ['intelligence_education'], ['sun', 'saravali', 'house_placement', 'house_3'], "Ch.34 v.14", "Sun in 3rd: skilled in arts and crafts, technical hobbies, hands-on practical intelligence"),
    ("sun", "house_placement", 3, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_3'], "Ch.34 v.15", "Sun in 3rd: income through courage, writing, short journeys, communications industry"),
]

_SUN_H4_DATA = [
    ("sun", "house_placement", 4, {}, "unfavorable", "moderate", ['mental_health'], ['sun', 'saravali', 'house_placement', 'house_4'], "Ch.34 v.16", "Sun in 4th: mental restlessness, dissatisfaction at home, conflicts with mother"),
    ("sun", "house_placement", 4, {}, "unfavorable", "moderate", ['property_vehicles'], ['sun', 'saravali', 'house_placement', 'house_4'], "Ch.34 v.17", "Sun in 4th: difficulties with property, government seizes assets, uncomfortable home"),
    ("sun", "house_placement", 4, {}, "mixed", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_4'], "Ch.34 v.18", "Sun in 4th: career in government service, administrative positions, but domestic unhappiness"),
    ("sun", "house_placement", 4, {}, "mixed", "moderate", ['character_temperament'], ['sun', 'saravali', 'house_placement', 'house_4'], "Ch.34 v.19", "Sun in 4th: proud nature, difficulty settling, frequent relocations, ancestral pride"),
    ("sun", "house_placement", 4, {}, "unfavorable", "moderate", ['longevity'], ['sun', 'saravali', 'house_placement', 'house_4'], "Ch.34 v.20", "Sun in 4th: father faces difficulties, mother health concerns, ancestral property disputes"),
]

_SUN_H5_DATA = [
    ("sun", "house_placement", 5, {}, "favorable", "strong", ['intelligence_education'], ['sun', 'saravali', 'house_placement', 'house_5'], "Ch.34 v.21", "Sun in 5th: brilliant intellect, scholarly achievements, advisory capacity, mantra siddhi"),
    ("sun", "house_placement", 5, {}, "mixed", "moderate", ['progeny'], ['sun', 'saravali', 'house_placement', 'house_5'], "Ch.34 v.22", "Sun in 5th: few children, children face health issues, first child may be distinguished"),
    ("sun", "house_placement", 5, {}, "favorable", "moderate", ['spirituality'], ['sun', 'saravali', 'house_placement', 'house_5'], "Ch.34 v.23", "Sun in 5th: interest in mantras, tantra, past-life merit activates, royal rituals"),
    ("sun", "house_placement", 5, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_5'], "Ch.34 v.24", "Sun in 5th: creative recognition, artistic acclaim, children bring fame"),
    ("sun", "house_placement", 5, {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_5'], "Ch.34 v.25", "Sun in 5th: success in education, counseling, creative arts, speculation"),
]

_SUN_H6_DATA = [
    ("sun", "house_placement", 6, {}, "favorable", "strong", ['enemies_litigation'], ['sun', 'saravali', 'house_placement', 'house_6'], "Ch.34 v.26", "Sun in 6th: destroys enemies completely, victory in competition, legal success"),
    ("sun", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_6'], "Ch.34 v.27", "Sun in 6th: success in medicine, military, law enforcement, competitive fields"),
    ("sun", "house_placement", 6, {}, "mixed", "moderate", ['physical_health'], ['sun', 'saravali', 'house_placement', 'house_6'], "Ch.34 v.28", "Sun in 6th: digestive fire strong but prone to stomach ulcers, acidity, pitta disorders"),
    ("sun", "house_placement", 6, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_6'], "Ch.34 v.29", "Sun in 6th: earns through service, competitive fields, medical or legal income"),
    ("sun", "house_placement", 6, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_6'], "Ch.34 v.30", "Sun in 6th: known for competitive excellence, defeats rivals publicly"),
]

_SUN_H7_DATA = [
    ("sun", "house_placement", 7, {}, "mixed", "moderate", ['marriage'], ['sun', 'saravali', 'house_placement', 'house_7'], "Ch.34 v.31", "Sun in 7th: dominant in marriage, partner from government background, ego clashes"),
    ("sun", "house_placement", 7, {}, "unfavorable", "moderate", ['marriage'], ['sun', 'saravali', 'house_placement', 'house_7'], "Ch.34 v.32", "Sun in 7th: late marriage or dissatisfaction, partner feels overshadowed, separation possible"),
    ("sun", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_7'], "Ch.34 v.33", "Sun in 7th: success through partnerships, business with government connections"),
    ("sun", "house_placement", 7, {}, "mixed", "moderate", ['physical_health'], ['sun', 'saravali', 'house_placement', 'house_7'], "Ch.34 v.34", "Sun in 7th: partner health fluctuations, bilious complaints, travel-related illness"),
    ("sun", "house_placement", 7, {}, "mixed", "moderate", ['foreign_travel'], ['sun', 'saravali', 'house_placement', 'house_7'], "Ch.34 v.35", "Sun in 7th: travels for official duties, foreign government connections"),
]

_SUN_H8_DATA = [
    ("sun", "house_placement", 8, {}, "unfavorable", "moderate", ['longevity'], ['sun', 'saravali', 'house_placement', 'house_8'], "Ch.34 v.36", "Sun in 8th: health challenges, eye problems, fevers, reduced vitality, chronic conditions"),
    ("sun", "house_placement", 8, {}, "unfavorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_8'], "Ch.34 v.37", "Sun in 8th: financial losses through government, fines, penalties, inheritance disputes"),
    ("sun", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['sun', 'saravali', 'house_placement', 'house_8'], "Ch.34 v.38", "Sun in 8th: interest in occult, research into hidden matters, transformation through crisis"),
    ("sun", "house_placement", 8, {}, "unfavorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_8'], "Ch.34 v.39", "Sun in 8th: loss of reputation, scandals possible, hidden life, government penalties"),
    ("sun", "house_placement", 8, {}, "unfavorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_8'], "Ch.34 v.40", "Sun in 8th: career obstacles, conflicts with authority, demotions possible"),
]

_SUN_H9_DATA = [
    ("sun", "house_placement", 9, {}, "favorable", "strong", ['spirituality'], ['sun', 'saravali', 'house_placement', 'house_9'], "Ch.34 v.41", "Sun in 9th: deep devotion to father, dharmic living, pilgrimage, temple worship"),
    ("sun", "house_placement", 9, {}, "favorable", "strong", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_9'], "Ch.34 v.42", "Sun in 9th: rise through merit, government honor, father influential in career"),
    ("sun", "house_placement", 9, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_9'], "Ch.34 v.43", "Sun in 9th: fortune through righteous means, inheritance from father, blessed fortune"),
    ("sun", "house_placement", 9, {}, "favorable", "moderate", ['foreign_travel'], ['sun', 'saravali', 'house_placement', 'house_9'], "Ch.34 v.44", "Sun in 9th: pilgrimage, travel for dharmic purposes, government foreign assignments"),
    ("sun", "house_placement", 9, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_9'], "Ch.34 v.45", "Sun in 9th: honored for dharmic living, respected as moral authority"),
]

_SUN_H10_DATA = [
    ("sun", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_10'], "Ch.34 v.46", "Sun in 10th: attains high positions, government authority, administrative excellence, digbala"),
    ("sun", "house_placement", 10, {}, "favorable", "strong", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_10'], "Ch.34 v.47", "Sun in 10th: widely known and respected, public honors, lasting legacy through work"),
    ("sun", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_10'], "Ch.34 v.48", "Sun in 10th: wealth through career, government salary, professional income, authority-based gains"),
    ("sun", "house_placement", 10, {}, "favorable", "moderate", ['property_vehicles'], ['sun', 'saravali', 'house_placement', 'house_10'], "Ch.34 v.49", "Sun in 10th: government quarters, official vehicles, professional assets"),
    ("sun", "house_placement", 10, {}, "favorable", "moderate", ['character_temperament'], ['sun', 'saravali', 'house_placement', 'house_10'], "Ch.34 v.50", "Sun in 10th: commanding public presence, respected leader, dignified professional bearing"),
]

_SUN_H11_DATA = [
    ("sun", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_11'], "Ch.34 v.51", "Sun in 11th: abundant gains, fulfillment of desires, wealthy friends and networks"),
    ("sun", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_11'], "Ch.34 v.52", "Sun in 11th: recognized in social circles, gains through government connections"),
    ("sun", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'house_placement', 'house_11'], "Ch.34 v.53", "Sun in 11th: elder sibling support, influential contacts, networking success"),
    ("sun", "house_placement", 11, {}, "favorable", "moderate", ['character_temperament'], ['sun', 'saravali', 'house_placement', 'house_11'], "Ch.34 v.54", "Sun in 11th: noble friends, virtuous social circle, dignified community involvement"),
    ("sun", "house_placement", 11, {}, "favorable", "moderate", ['progeny'], ['sun', 'saravali', 'house_placement', 'house_11'], "Ch.34 v.55", "Sun in 11th: gains through children, aspirations fulfilled, social standing through offspring"),
]

_SUN_H12_DATA = [
    ("sun", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['sun', 'saravali', 'house_placement', 'house_12'], "Ch.34 v.56", "Sun in 12th: financial losses, expenditure on government fines, wasteful spending"),
    ("sun", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['sun', 'saravali', 'house_placement', 'house_12'], "Ch.34 v.57", "Sun in 12th: travels abroad for government work, pilgrimage, losses in foreign land"),
    ("sun", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['sun', 'saravali', 'house_placement', 'house_12'], "Ch.34 v.58", "Sun in 12th: spiritual detachment, meditation practice, seclusion, renunciation"),
    ("sun", "house_placement", 12, {}, "unfavorable", "moderate", ['physical_health'], ['sun', 'saravali', 'house_placement', 'house_12'], "Ch.34 v.59", "Sun in 12th: eye weakness, chronic fevers, hospitalization, government confinement possible"),
    ("sun", "house_placement", 12, {}, "unfavorable", "moderate", ['fame_reputation'], ['sun', 'saravali', 'house_placement', 'house_12'], "Ch.34 v.60", "Sun in 12th: hidden life, loss of social standing, anonymous existence"),
]

_SUN_GENERAL_DATA = [
    ("sun", "house_condition", "sun_digbala_10th", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.61", "Sun with directional strength in 10th: maximum career authority, supreme public recognition"),
    ("sun", "house_condition", "sun_in_kendra", {}, "favorable", "moderate", ['career_status', 'fame_reputation'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.62", "Sun in kendra (1/4/7/10): angular strength, government favor, public visibility"),
    ("sun", "house_condition", "sun_in_trikona", {}, "favorable", "strong", ['wealth', 'spirituality'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.63", "Sun in trikona (1/5/9): dharmic fortune, spiritual merit, blessed authority"),
    ("sun", "house_condition", "sun_in_dusthana", {}, "unfavorable", "moderate", ['physical_health', 'career_status'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.64", "Sun in dusthana (6/8/12): health issues, career obstacles, authority diminished"),
    ("sun", "house_condition", "sun_in_upachaya", {}, "favorable", "moderate", ['career_status', 'wealth'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.65", "Sun in upachaya (3/6/10/11): improves over time, growing authority, increasing gains"),
    ("sun", "house_condition", "sun_combustion_effect", {}, "unfavorable", "moderate", ['career_status', 'progeny'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.66", "Sun causing combustion: diminishes co-placed planets karakatvas, overshadows companions"),
    ("sun", "house_condition", "sun_vargottama", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.67", "Sun vargottama in house: amplified authority and recognition in that house matters"),
    ("sun", "house_condition", "sun_aspected_jupiter", {}, "favorable", "strong", ['spirituality', 'career_status'], ['sun', 'saravali', 'house_placement', 'general'], "Ch.34 v.68", "Sun aspected by Jupiter: dharmic authority, blessed career, righteous fame"),
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
            rule_id=rid, source="Saravali", chapter="Ch.34", school="parashari",
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
        (_SUN_H1_DATA, 2133),
        (_SUN_H2_DATA, 2138),
        (_SUN_H3_DATA, 2143),
        (_SUN_H4_DATA, 2148),
        (_SUN_H5_DATA, 2153),
        (_SUN_H6_DATA, 2158),
        (_SUN_H7_DATA, 2163),
        (_SUN_H8_DATA, 2168),
        (_SUN_H9_DATA, 2173),
        (_SUN_H10_DATA, 2178),
        (_SUN_H11_DATA, 2183),
        (_SUN_H12_DATA, 2188),
        (_SUN_GENERAL_DATA, 2193),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_1_REGISTRY.add(_rule)
