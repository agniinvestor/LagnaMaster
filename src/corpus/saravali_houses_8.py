"""src/corpus/saravali_houses_8.py — Saravali Rahu+Ketu in 12 Houses (Ch.41-42).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_RAHU_H1_DATA = [
    ("rahu", "house_placement", 1, {}, "mixed", "moderate", ['character_temperament'], ['rahu', 'saravali', 'house_placement', 'house_1'], "Ch.41 v.1", "Rahu in 1st: unconventional personality, ambitious, foreign appearance, restless nature"),
    ("rahu", "house_placement", 1, {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_1'], "Ch.41 v.2", "Rahu in 1st: success through unconventional means, technology, foreign connections"),
    ("rahu", "house_placement", 1, {}, "unfavorable", "moderate", ['physical_health'], ['rahu', 'saravali', 'house_placement', 'house_1'], "Ch.41 v.3", "Rahu in 1st: mysterious ailments, head problems, nervous disorders"),
    ("rahu", "house_placement", 1, {}, "mixed", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'house_placement', 'house_1'], "Ch.41 v.4", "Rahu in 1st: sudden fame or notoriety, controversial public image"),
]

_RAHU_H2_DATA = [
    ("rahu", "house_placement", 2, {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_2'], "Ch.41 v.5", "Rahu in 2nd: wealth through unconventional means, foreign income, irregular gains"),
    ("rahu", "house_placement", 2, {}, "unfavorable", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'house_placement', 'house_2'], "Ch.41 v.6", "Rahu in 2nd: deceptive speech, lies, harsh or foreign-accented voice"),
    ("rahu", "house_placement", 2, {}, "mixed", "moderate", ['marriage'], ['rahu', 'saravali', 'house_placement', 'house_2'], "Ch.41 v.7", "Rahu in 2nd: unconventional family, foreign relatives, family secrets"),
]

_RAHU_H3_DATA = [
    ("rahu", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['rahu', 'saravali', 'house_placement', 'house_3'], "Ch.41 v.8", "Rahu in 3rd: bold and adventurous, unconventional courage, media skills"),
    ("rahu", "house_placement", 3, {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_3'], "Ch.41 v.9", "Rahu in 3rd: gains through media, technology, communication, or travel"),
    ("rahu", "house_placement", 3, {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_3'], "Ch.41 v.10", "Rahu in 3rd: success in media, technology, foreign communications"),
]

_RAHU_H4_DATA = [
    ("rahu", "house_placement", 4, {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'house_placement', 'house_4'], "Ch.41 v.11", "Rahu in 4th: disturbed domestic peace, haunted property, mother anxiety"),
    ("rahu", "house_placement", 4, {}, "mixed", "moderate", ['property_vehicles'], ['rahu', 'saravali', 'house_placement', 'house_4'], "Ch.41 v.12", "Rahu in 4th: foreign property, unusual home, technology in home"),
    ("rahu", "house_placement", 4, {}, "unfavorable", "moderate", ['marriage'], ['rahu', 'saravali', 'house_placement', 'house_4'], "Ch.41 v.13", "Rahu in 4th: domestic deception, family secrets, cold home atmosphere"),
]

_RAHU_H5_DATA = [
    ("rahu", "house_placement", 5, {}, "mixed", "moderate", ['intelligence_education'], ['rahu', 'saravali', 'house_placement', 'house_5'], "Ch.41 v.14", "Rahu in 5th: unconventional intellect, obsessive thinking, innovative ideas"),
    ("rahu", "house_placement", 5, {}, "unfavorable", "moderate", ['progeny'], ['rahu', 'saravali', 'house_placement', 'house_5'], "Ch.41 v.15", "Rahu in 5th: challenges with children, unusual offspring, adoption possible"),
    ("rahu", "house_placement", 5, {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'house_placement', 'house_5'], "Ch.41 v.16", "Rahu in 5th: occult interests, past-life obsessions, unconventional religion"),
]

_RAHU_H6_DATA = [
    ("rahu", "house_placement", 6, {}, "favorable", "strong", ['enemies_litigation'], ['rahu', 'saravali', 'house_placement', 'house_6'], "Ch.41 v.17", "Rahu in 6th: destroys enemies through cunning, wins unconventional battles"),
    ("rahu", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_6'], "Ch.41 v.18", "Rahu in 6th: success in foreign service, technology, or unconventional medicine"),
    ("rahu", "house_placement", 6, {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_6'], "Ch.41 v.19", "Rahu in 6th: gains through defeating competition, foreign service income"),
]

_RAHU_H7_DATA = [
    ("rahu", "house_placement", 7, {}, "mixed", "moderate", ['marriage'], ['rahu', 'saravali', 'house_placement', 'house_7'], "Ch.41 v.20", "Rahu in 7th: foreign or unconventional spouse, obsessive relationships, multiple partners"),
    ("rahu", "house_placement", 7, {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_7'], "Ch.41 v.21", "Rahu in 7th: success through foreign partnerships, international business"),
    ("rahu", "house_placement", 7, {}, "mixed", "moderate", ['physical_health'], ['rahu', 'saravali', 'house_placement', 'house_7'], "Ch.41 v.22", "Rahu in 7th: reproductive concerns, partner health mystery"),
]

_RAHU_H8_DATA = [
    ("rahu", "house_placement", 8, {}, "unfavorable", "strong", ['longevity'], ['rahu', 'saravali', 'house_placement', 'house_8'], "Ch.41 v.23", "Rahu in 8th: sudden accidents, mysterious health crises, occult dangers"),
    ("rahu", "house_placement", 8, {}, "unfavorable", "moderate", ['mental_health'], ['rahu', 'saravali', 'house_placement', 'house_8'], "Ch.41 v.24", "Rahu in 8th: paranoia, fear of unknown, psychological disturbances"),
    ("rahu", "house_placement", 8, {}, "mixed", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_8'], "Ch.41 v.25", "Rahu in 8th: sudden inheritance, insurance gains, underground income"),
]

_RAHU_H9_DATA = [
    ("rahu", "house_placement", 9, {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'house_placement', 'house_9'], "Ch.41 v.26", "Rahu in 9th: unorthodox religion, foreign guru, unconventional dharma"),
    ("rahu", "house_placement", 9, {}, "unfavorable", "moderate", ['character_temperament'], ['rahu', 'saravali', 'house_placement', 'house_9'], "Ch.41 v.27", "Rahu in 9th: irreligious or hypocritical, father troubled, dharmic confusion"),
    ("rahu", "house_placement", 9, {}, "favorable", "moderate", ['foreign_travel'], ['rahu', 'saravali', 'house_placement', 'house_9'], "Ch.41 v.28", "Rahu in 9th: extensive foreign travel, living abroad, international connections"),
]

_RAHU_H10_DATA = [
    ("rahu", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_10'], "Ch.41 v.29", "Rahu in 10th: powerful career through unconventional means, technology, politics"),
    ("rahu", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'house_placement', 'house_10'], "Ch.41 v.30", "Rahu in 10th: sudden public prominence, controversial fame, media career"),
    ("rahu", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_10'], "Ch.41 v.31", "Rahu in 10th: income through technology, politics, foreign corporations"),
]

_RAHU_H11_DATA = [
    ("rahu", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_11'], "Ch.41 v.32", "Rahu in 11th: abundant gains through technology, foreign networks, unconventional sources"),
    ("rahu", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['rahu', 'saravali', 'house_placement', 'house_11'], "Ch.41 v.33", "Rahu in 11th: powerful connections, gains through influential networks"),
    ("rahu", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['rahu', 'saravali', 'house_placement', 'house_11'], "Ch.41 v.34", "Rahu in 11th: fame through social networks, influential friends"),
]

_RAHU_H12_DATA = [
    ("rahu", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['rahu', 'saravali', 'house_placement', 'house_12'], "Ch.41 v.35", "Rahu in 12th: foreign settlement, exile, spiritual quest abroad"),
    ("rahu", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['rahu', 'saravali', 'house_placement', 'house_12'], "Ch.41 v.36", "Rahu in 12th: hidden expenses, losses through foreign ventures"),
    ("rahu", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['rahu', 'saravali', 'house_placement', 'house_12'], "Ch.41 v.37", "Rahu in 12th: intense spiritual seeking, meditation, isolation"),
]

_KETU_H1_DATA = [
    ("ketu", "house_placement", 1, {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'house_placement', 'house_1'], "Ch.42 v.1", "Ketu in 1st: spiritual and detached personality, past-life marks, unusual appearance"),
    ("ketu", "house_placement", 1, {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'house_placement', 'house_1'], "Ch.42 v.2", "Ketu in 1st: mysterious health issues, skin marks, nervous sensitivity"),
    ("ketu", "house_placement", 1, {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_1'], "Ch.42 v.3", "Ketu in 1st: natural spiritual inclination, past-life awareness"),
]

_KETU_H2_DATA = [
    ("ketu", "house_placement", 2, {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'house_placement', 'house_2'], "Ch.42 v.4", "Ketu in 2nd: financial losses, stammering speech, family dysfunction"),
    ("ketu", "house_placement", 2, {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'house_placement', 'house_2'], "Ch.42 v.5", "Ketu in 2nd: family detachment, cold speech, domestic disinterest"),
    ("ketu", "house_placement", 2, {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'house_placement', 'house_2'], "Ch.42 v.6", "Ketu in 2nd: intuitive knowledge, non-verbal understanding"),
]

_KETU_H3_DATA = [
    ("ketu", "house_placement", 3, {}, "favorable", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_3'], "Ch.42 v.7", "Ketu in 3rd: spiritual courage, past-life valor, detached bravery"),
    ("ketu", "house_placement", 3, {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'house_placement', 'house_3'], "Ch.42 v.8", "Ketu in 3rd: introverted, avoids social media, non-communicative"),
    ("ketu", "house_placement", 3, {}, "favorable", "moderate", ['longevity'], ['ketu', 'saravali', 'house_placement', 'house_3'], "Ch.42 v.9", "Ketu in 3rd: survives through detachment, spiritual protection"),
]

_KETU_H4_DATA = [
    ("ketu", "house_placement", 4, {}, "unfavorable", "moderate", ['property_vehicles'], ['ketu', 'saravali', 'house_placement', 'house_4'], "Ch.42 v.10", "Ketu in 4th: property losses, uncomfortable home, domestic detachment"),
    ("ketu", "house_placement", 4, {}, "unfavorable", "moderate", ['mental_health'], ['ketu', 'saravali', 'house_placement', 'house_4'], "Ch.42 v.11", "Ketu in 4th: emotional void, motherless feeling, inner emptiness"),
    ("ketu", "house_placement", 4, {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_4'], "Ch.42 v.12", "Ketu in 4th: inner liberation, transcends domestic attachment"),
]

_KETU_H5_DATA = [
    ("ketu", "house_placement", 5, {}, "unfavorable", "moderate", ['progeny'], ['ketu', 'saravali', 'house_placement', 'house_5'], "Ch.42 v.13", "Ketu in 5th: challenges with children, unusual offspring, detached parenting"),
    ("ketu", "house_placement", 5, {}, "mixed", "moderate", ['intelligence_education'], ['ketu', 'saravali', 'house_placement', 'house_5'], "Ch.42 v.14", "Ketu in 5th: intuitive brilliance, past-life knowledge, beyond logic"),
    ("ketu", "house_placement", 5, {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_5'], "Ch.42 v.15", "Ketu in 5th: past-life spiritual merit, mantra siddhi without effort"),
]

_KETU_H6_DATA = [
    ("ketu", "house_placement", 6, {}, "favorable", "strong", ['enemies_litigation'], ['ketu', 'saravali', 'house_placement', 'house_6'], "Ch.42 v.16", "Ketu in 6th: enemies dissolve, mysterious victory, diseases overcome spiritually"),
    ("ketu", "house_placement", 6, {}, "favorable", "moderate", ['longevity'], ['ketu', 'saravali', 'house_placement', 'house_6'], "Ch.42 v.17", "Ketu in 6th: protection from diseases, spiritual immunity"),
    ("ketu", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['ketu', 'saravali', 'house_placement', 'house_6'], "Ch.42 v.18", "Ketu in 6th: success through unconventional healing, spiritual service"),
]

_KETU_H7_DATA = [
    ("ketu", "house_placement", 7, {}, "unfavorable", "moderate", ['marriage'], ['ketu', 'saravali', 'house_placement', 'house_7'], "Ch.42 v.19", "Ketu in 7th: detachment from partner, cold marriage, spiritual spouse"),
    ("ketu", "house_placement", 7, {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'house_placement', 'house_7'], "Ch.42 v.20", "Ketu in 7th: unusual partnerships, spiritual collaborations"),
    ("ketu", "house_placement", 7, {}, "unfavorable", "moderate", ['physical_health'], ['ketu', 'saravali', 'house_placement', 'house_7'], "Ch.42 v.21", "Ketu in 7th: reproductive detachment, partner health mystery"),
]

_KETU_H8_DATA = [
    ("ketu", "house_placement", 8, {}, "favorable", "moderate", ['longevity'], ['ketu', 'saravali', 'house_placement', 'house_8'], "Ch.42 v.22", "Ketu in 8th: long life, survives crises, spiritual transformation through near-death"),
    ("ketu", "house_placement", 8, {}, "favorable", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_8'], "Ch.42 v.23", "Ketu in 8th: deep occult mastery, moksha yoga potential, psychic ability"),
    ("ketu", "house_placement", 8, {}, "mixed", "moderate", ['wealth'], ['ketu', 'saravali', 'house_placement', 'house_8'], "Ch.42 v.24", "Ketu in 8th: unexpected inheritance, sudden financial changes"),
]

_KETU_H9_DATA = [
    ("ketu", "house_placement", 9, {}, "favorable", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_9'], "Ch.42 v.25", "Ketu in 9th: past-life dharmic mastery, effortless spiritual knowledge"),
    ("ketu", "house_placement", 9, {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'house_placement', 'house_9'], "Ch.42 v.26", "Ketu in 9th: quietly righteous, beyond organized religion, inner dharma"),
    ("ketu", "house_placement", 9, {}, "mixed", "moderate", ['foreign_travel'], ['ketu', 'saravali', 'house_placement', 'house_9'], "Ch.42 v.27", "Ketu in 9th: spiritual pilgrimage, detached foreign travel"),
]

_KETU_H10_DATA = [
    ("ketu", "house_placement", 10, {}, "mixed", "moderate", ['career_status'], ['ketu', 'saravali', 'house_placement', 'house_10'], "Ch.42 v.28", "Ketu in 10th: unconventional career, detached from ambition, spiritual profession"),
    ("ketu", "house_placement", 10, {}, "unfavorable", "moderate", ['fame_reputation'], ['ketu', 'saravali', 'house_placement', 'house_10'], "Ch.42 v.29", "Ketu in 10th: avoids spotlight, anonymous public service, hidden authority"),
    ("ketu", "house_placement", 10, {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_10'], "Ch.42 v.30", "Ketu in 10th: karma yoga, selfless service, detachment from public recognition"),
]

_KETU_H11_DATA = [
    ("ketu", "house_placement", 11, {}, "mixed", "moderate", ['wealth'], ['ketu', 'saravali', 'house_placement', 'house_11'], "Ch.42 v.31", "Ketu in 11th: irregular gains, unexpected income, detached from desires"),
    ("ketu", "house_placement", 11, {}, "mixed", "moderate", ['character_temperament'], ['ketu', 'saravali', 'house_placement', 'house_11'], "Ch.42 v.32", "Ketu in 11th: detached from social groups, hermit tendency, spiritual friends"),
    ("ketu", "house_placement", 11, {}, "unfavorable", "moderate", ['fame_reputation'], ['ketu', 'saravali', 'house_placement', 'house_11'], "Ch.42 v.33", "Ketu in 11th: avoids social networks, unknown among peers"),
]

_KETU_H12_DATA = [
    ("ketu", "house_placement", 12, {}, "favorable", "strong", ['spirituality'], ['ketu', 'saravali', 'house_placement', 'house_12'], "Ch.42 v.34", "Ketu in 12th: supreme moksha placement, liberation, spiritual enlightenment"),
    ("ketu", "house_placement", 12, {}, "favorable", "moderate", ['foreign_travel'], ['ketu', 'saravali', 'house_placement', 'house_12'], "Ch.42 v.35", "Ketu in 12th: spiritual retreat abroad, ashram life, isolated meditation"),
    ("ketu", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['ketu', 'saravali', 'house_placement', 'house_12'], "Ch.42 v.36", "Ketu in 12th: complete material indifference, financial negligence"),
]

_NODES_GENERAL_DATA = [
    ("rahu", "house_condition", "rahu_in_kendra", {}, "favorable", "moderate", ['career_status', 'wealth'], ['rahu', 'saravali', 'house_placement', 'general'], "Ch.41 v.38", "Rahu in kendra: worldly ambition amplified, unconventional career success"),
    ("rahu", "house_condition", "rahu_in_trikona", {}, "mixed", "moderate", ['spirituality', 'intelligence_education'], ['rahu', 'saravali', 'house_placement', 'general'], "Ch.41 v.39", "Rahu in trikona: unconventional fortune, heterodox wisdom, foreign dharma"),
    ("ketu", "house_condition", "ketu_in_kendra", {}, "mixed", "moderate", ['career_status', 'spirituality'], ['ketu', 'saravali', 'house_placement', 'general'], "Ch.41 v.40", "Ketu in kendra: detached authority, spiritual foundation, unconventional stability"),
    ("ketu", "house_condition", "ketu_in_trikona", {}, "favorable", "moderate", ['spirituality', 'intelligence_education'], ['ketu', 'saravali', 'house_placement', 'general'], "Ch.41 v.41", "Ketu in trikona: past-life merit, intuitive wisdom, effortless dharma"),
    ("rahu", "house_condition", "rahu_ketu_1_7", {}, "mixed", "strong", ['marriage', 'career_status'], ['rahu', 'saravali', 'house_placement', 'general'], "Ch.41 v.42", "Rahu-Ketu in 1-7 axis: self vs partnership tension, karmic relationship lessons"),
    ("rahu", "house_condition", "rahu_ketu_4_10", {}, "mixed", "strong", ['career_status', 'mental_health'], ['rahu', 'saravali', 'house_placement', 'general'], "Ch.41 v.43", "Rahu-Ketu in 4-10 axis: home vs career tension, domestic-professional balance"),
    ("rahu", "house_condition", "rahu_ketu_5_11", {}, "mixed", "moderate", ['progeny', 'wealth'], ['rahu', 'saravali', 'house_placement', 'general'], "Ch.41 v.44", "Rahu-Ketu in 5-11 axis: children vs gains, creative vs social tension"),
    ("nodes", "house_condition", "nodes_with_luminaries", {}, "unfavorable", "strong", ['mental_health', 'physical_health'], ['nodes', 'saravali', 'house_placement', 'general'], "Ch.41 v.45", "Nodes with Sun/Moon: eclipse energy, grahan dosha, psychological impact"),
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
            rule_id=rid, source="Saravali", chapter="Ch.41-42", school="parashari",
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
        (_RAHU_H1_DATA, 2548),
        (_RAHU_H2_DATA, 2552),
        (_RAHU_H3_DATA, 2555),
        (_RAHU_H4_DATA, 2558),
        (_RAHU_H5_DATA, 2561),
        (_RAHU_H6_DATA, 2564),
        (_RAHU_H7_DATA, 2567),
        (_RAHU_H8_DATA, 2570),
        (_RAHU_H9_DATA, 2573),
        (_RAHU_H10_DATA, 2576),
        (_RAHU_H11_DATA, 2579),
        (_RAHU_H12_DATA, 2582),
        (_KETU_H1_DATA, 2585),
        (_KETU_H2_DATA, 2588),
        (_KETU_H3_DATA, 2591),
        (_KETU_H4_DATA, 2594),
        (_KETU_H5_DATA, 2597),
        (_KETU_H6_DATA, 2600),
        (_KETU_H7_DATA, 2603),
        (_KETU_H8_DATA, 2606),
        (_KETU_H9_DATA, 2609),
        (_KETU_H10_DATA, 2612),
        (_KETU_H11_DATA, 2615),
        (_KETU_H12_DATA, 2618),
        (_NODES_GENERAL_DATA, 2621),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_8_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_8_REGISTRY.add(_rule)
