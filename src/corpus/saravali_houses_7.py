"""src/corpus/saravali_houses_7.py — Saravali Saturn in 12 Houses (Ch.40).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_SATURN_H1_DATA = [
    ("saturn", "house_placement", 1, {}, "mixed", "moderate", ['physical_appearance'], ['saturn', 'saravali', 'house_placement', 'house_1'], "Ch.40 v.1", "Saturn in 1st: lean body, aged appearance, serious demeanor, slow movements"),
    ("saturn", "house_placement", 1, {}, "mixed", "moderate", ['character_temperament'], ['saturn', 'saravali', 'house_placement', 'house_1'], "Ch.40 v.2", "Saturn in 1st: disciplined and hardworking, but pessimistic, melancholic tendency"),
    ("saturn", "house_placement", 1, {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_1'], "Ch.40 v.3", "Saturn in 1st: chronic ailments, bone problems, slow metabolism, delayed recovery"),
    ("saturn", "house_placement", 1, {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_1'], "Ch.40 v.4", "Saturn in 1st: late bloomer, success through sustained effort, gradual rise"),
    ("saturn", "house_placement", 1, {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'house_placement', 'house_1'], "Ch.40 v.5", "Saturn in 1st: delayed marriage, cold personality in relationships"),
]

_SATURN_H2_DATA = [
    ("saturn", "house_placement", 2, {}, "unfavorable", "moderate", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_2'], "Ch.40 v.6", "Saturn in 2nd: financial restrictions, delayed accumulation, poverty in early life"),
    ("saturn", "house_placement", 2, {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'house_placement', 'house_2'], "Ch.40 v.7", "Saturn in 2nd: stammering speech, harsh words, but deep practical knowledge"),
    ("saturn", "house_placement", 2, {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'house_placement', 'house_2'], "Ch.40 v.8", "Saturn in 2nd: family tensions, cold family atmosphere, food restrictions"),
    ("saturn", "house_placement", 2, {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_2'], "Ch.40 v.9", "Saturn in 2nd: dental problems, eye issues, facial skin problems"),
]

_SATURN_H3_DATA = [
    ("saturn", "house_placement", 3, {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'house_placement', 'house_3'], "Ch.40 v.10", "Saturn in 3rd: patient courage, endurance, determined will, structured effort"),
    ("saturn", "house_placement", 3, {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_3'], "Ch.40 v.11", "Saturn in 3rd: success through writing, research, structured communication"),
    ("saturn", "house_placement", 3, {}, "mixed", "moderate", ['enemies_litigation'], ['saturn', 'saravali', 'house_placement', 'house_3'], "Ch.40 v.12", "Saturn in 3rd: strained sibling relations, neighbors cause problems, isolation"),
    ("saturn", "house_placement", 3, {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'house_placement', 'house_3'], "Ch.40 v.13", "Saturn in 3rd: longevity improved, survives difficult circumstances"),
]

_SATURN_H4_DATA = [
    ("saturn", "house_placement", 4, {}, "unfavorable", "moderate", ['mental_health'], ['saturn', 'saravali', 'house_placement', 'house_4'], "Ch.40 v.14", "Saturn in 4th: domestic unhappiness, cold home, mother suffers, emotional restriction"),
    ("saturn", "house_placement", 4, {}, "unfavorable", "moderate", ['property_vehicles'], ['saturn', 'saravali', 'house_placement', 'house_4'], "Ch.40 v.15", "Saturn in 4th: old or dilapidated home, vehicle breakdowns, property disputes"),
    ("saturn", "house_placement", 4, {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_4'], "Ch.40 v.16", "Saturn in 4th: success in mining, construction, underground work, late stability"),
    ("saturn", "house_placement", 4, {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'house_placement', 'house_4'], "Ch.40 v.17", "Saturn in 4th: cold domestic life, partner unhappy, domestic isolation"),
]

_SATURN_H5_DATA = [
    ("saturn", "house_placement", 5, {}, "unfavorable", "moderate", ['progeny'], ['saturn', 'saravali', 'house_placement', 'house_5'], "Ch.40 v.18", "Saturn in 5th: delayed or denied children, adoption possible, strict parenting"),
    ("saturn", "house_placement", 5, {}, "unfavorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'house_placement', 'house_5'], "Ch.40 v.19", "Saturn in 5th: slow learner but deep, practical over theoretical, traditional education"),
    ("saturn", "house_placement", 5, {}, "mixed", "moderate", ['spirituality'], ['saturn', 'saravali', 'house_placement', 'house_5'], "Ch.40 v.20", "Saturn in 5th: structured spiritual practice, disciplined devotion, karmic merit"),
    ("saturn", "house_placement", 5, {}, "unfavorable", "moderate", ['mental_health'], ['saturn', 'saravali', 'house_placement', 'house_5'], "Ch.40 v.21", "Saturn in 5th: creative blocks, joylessness, depression tendency"),
]

_SATURN_H6_DATA = [
    ("saturn", "house_placement", 6, {}, "favorable", "moderate", ['enemies_litigation'], ['saturn', 'saravali', 'house_placement', 'house_6'], "Ch.40 v.22", "Saturn in 6th: defeats enemies through persistence, legal stamina, outlasts rivals"),
    ("saturn", "house_placement", 6, {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_6'], "Ch.40 v.23", "Saturn in 6th: success in service, healthcare, law enforcement, manual labor"),
    ("saturn", "house_placement", 6, {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_6'], "Ch.40 v.24", "Saturn in 6th: chronic ailments overcome slowly, joint problems, but endurance"),
    ("saturn", "house_placement", 6, {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'house_placement', 'house_6'], "Ch.40 v.25", "Saturn in 6th: survives diseases, strong immune response over time"),
]

_SATURN_H7_DATA = [
    ("saturn", "house_placement", 7, {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'house_placement', 'house_7'], "Ch.40 v.26", "Saturn in 7th: delayed marriage, older spouse, cold partnership, separation risk"),
    ("saturn", "house_placement", 7, {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_7'], "Ch.40 v.27", "Saturn in 7th: business partnerships with older people, structured collaborations"),
    ("saturn", "house_placement", 7, {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_7'], "Ch.40 v.28", "Saturn in 7th: reproductive issues, partner health problems"),
    ("saturn", "house_placement", 7, {}, "mixed", "moderate", ['foreign_travel'], ['saturn', 'saravali', 'house_placement', 'house_7'], "Ch.40 v.29", "Saturn in 7th: foreign connections through business, practical partnerships abroad"),
]

_SATURN_H8_DATA = [
    ("saturn", "house_placement", 8, {}, "mixed", "moderate", ['longevity'], ['saturn', 'saravali', 'house_placement', 'house_8'], "Ch.40 v.30", "Saturn in 8th: long life but with chronic ailments, endurance through suffering"),
    ("saturn", "house_placement", 8, {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_8'], "Ch.40 v.31", "Saturn in 8th: chronic diseases, joint degeneration, slow-acting poisons"),
    ("saturn", "house_placement", 8, {}, "mixed", "moderate", ['spirituality'], ['saturn', 'saravali', 'house_placement', 'house_8'], "Ch.40 v.32", "Saturn in 8th: deep karmic understanding, transformation through suffering"),
    ("saturn", "house_placement", 8, {}, "unfavorable", "moderate", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_8'], "Ch.40 v.33", "Saturn in 8th: inheritance disputes, hidden financial losses, debts"),
]

_SATURN_H9_DATA = [
    ("saturn", "house_placement", 9, {}, "mixed", "moderate", ['spirituality'], ['saturn', 'saravali', 'house_placement', 'house_9'], "Ch.40 v.34", "Saturn in 9th: disciplined religious practice, traditional dharma, structured devotion"),
    ("saturn", "house_placement", 9, {}, "unfavorable", "moderate", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_9'], "Ch.40 v.35", "Saturn in 9th: delayed fortune, father faces hardship, restricted prosperity"),
    ("saturn", "house_placement", 9, {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_9'], "Ch.40 v.36", "Saturn in 9th: success in traditional institutions, law, government, religious authority"),
    ("saturn", "house_placement", 9, {}, "unfavorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'house_placement', 'house_9'], "Ch.40 v.37", "Saturn in 9th: dogmatic, rigid beliefs, conflicts with father or guru"),
]

_SATURN_H10_DATA = [
    ("saturn", "house_placement", 10, {}, "favorable", "strong", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_10'], "Ch.40 v.38", "Saturn in 10th: success through discipline, administrative authority, government positions, digbala"),
    ("saturn", "house_placement", 10, {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'house_placement', 'house_10'], "Ch.40 v.39", "Saturn in 10th: respected for competence, lasting professional reputation"),
    ("saturn", "house_placement", 10, {}, "favorable", "moderate", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_10'], "Ch.40 v.40", "Saturn in 10th: wealth through career persistence, government income, institutional leadership"),
    ("saturn", "house_placement", 10, {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'house_placement', 'house_10'], "Ch.40 v.41", "Saturn in 10th: career prioritized over marriage, workaholic tendencies"),
]

_SATURN_H11_DATA = [
    ("saturn", "house_placement", 11, {}, "favorable", "strong", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_11'], "Ch.40 v.42", "Saturn in 11th: steady gains, long-term investments pay off, wealthy older friends"),
    ("saturn", "house_placement", 11, {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'house_placement', 'house_11'], "Ch.40 v.43", "Saturn in 11th: professional networks, institutional connections, elder support"),
    ("saturn", "house_placement", 11, {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'house_placement', 'house_11'], "Ch.40 v.44", "Saturn in 11th: respected in community, gains through discipline and persistence"),
    ("saturn", "house_placement", 11, {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'house_placement', 'house_11'], "Ch.40 v.45", "Saturn in 11th: aspirations fulfilled in old age, late-life satisfaction"),
]

_SATURN_H12_DATA = [
    ("saturn", "house_placement", 12, {}, "unfavorable", "moderate", ['wealth'], ['saturn', 'saravali', 'house_placement', 'house_12'], "Ch.40 v.46", "Saturn in 12th: financial losses, expenses on chronic illness, debts"),
    ("saturn", "house_placement", 12, {}, "mixed", "moderate", ['foreign_travel'], ['saturn', 'saravali', 'house_placement', 'house_12'], "Ch.40 v.47", "Saturn in 12th: foreign exile, work abroad in difficult conditions, isolation overseas"),
    ("saturn", "house_placement", 12, {}, "mixed", "moderate", ['spirituality'], ['saturn', 'saravali', 'house_placement', 'house_12'], "Ch.40 v.48", "Saturn in 12th: moksha through suffering, solitary spiritual practice, renunciation"),
    ("saturn", "house_placement", 12, {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'house_placement', 'house_12'], "Ch.40 v.49", "Saturn in 12th: hospitalization, chronic conditions, feet problems, hidden ailments"),
]

_SATURN_GENERAL_DATA = [
    ("saturn", "house_condition", "saturn_digbala_7th", {}, "favorable", "strong", ['career_status', 'marriage'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.50", "Saturn digbala in 7th: structured partnerships — note: this is classically debated"),
    ("saturn", "house_condition", "saturn_shasha", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.51", "Saturn in kendra own/exalted: Shasha Yoga, disciplined eminence, lasting authority"),
    ("saturn", "house_condition", "saturn_in_kendra", {}, "favorable", "moderate", ['career_status', 'longevity'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.52", "Saturn in kendra: foundational discipline, slow but steady rise"),
    ("saturn", "house_condition", "saturn_in_upachaya", {}, "favorable", "moderate", ['career_status', 'wealth'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.53", "Saturn in upachaya (3/6/10/11): improves with time, growing discipline rewarded"),
    ("saturn", "house_condition", "saturn_in_dusthana", {}, "unfavorable", "moderate", ['physical_health', 'wealth'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.54", "Saturn in dusthana: chronic health, financial restriction, karmic suffering"),
    ("saturn", "house_condition", "saturn_aspected_jupiter", {}, "favorable", "moderate", ['spirituality', 'career_status'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.55", "Saturn aspected by Jupiter: dharmic discipline, blessed hardship"),
    ("saturn", "house_condition", "saturn_aspected_mars", {}, "unfavorable", "moderate", ['physical_health', 'enemies_litigation'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.56", "Saturn aspected by Mars: accidents, chronic inflammation, legal battles"),
    ("saturn", "house_condition", "saturn_vargottama", {}, "favorable", "strong", ['career_status', 'longevity'], ['saturn', 'saravali', 'house_placement', 'general'], "Ch.40 v.57", "Saturn vargottama: amplified discipline, enduring authority and longevity"),
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
            rule_id=rid, source="Saravali", chapter="Ch.40", school="parashari",
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
        (_SATURN_H1_DATA, 2491),
        (_SATURN_H2_DATA, 2496),
        (_SATURN_H3_DATA, 2500),
        (_SATURN_H4_DATA, 2504),
        (_SATURN_H5_DATA, 2508),
        (_SATURN_H6_DATA, 2512),
        (_SATURN_H7_DATA, 2516),
        (_SATURN_H8_DATA, 2520),
        (_SATURN_H9_DATA, 2524),
        (_SATURN_H10_DATA, 2528),
        (_SATURN_H11_DATA, 2532),
        (_SATURN_H12_DATA, 2536),
        (_SATURN_GENERAL_DATA, 2540),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_house_rules(data, s))
    return result


SARAVALI_HOUSES_7_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_HOUSES_7_REGISTRY.add(_rule)
