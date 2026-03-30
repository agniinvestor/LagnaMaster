"""src/corpus/saravali_special_4.py — Saravali Special Topics (Ch.11-14).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_NABHASA_YOGAS_DATA = [
    ("general", "yoga", "yupa_yoga", {}, "favorable", "moderate", ['spirituality', 'career_status'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.1", "Yupa Yoga (Nabhasa): all planets in 4 consecutive signs starting from kendra — sacrificial merit, religious authority"),
    ("general", "yoga", "ishu_yoga", {}, "favorable", "moderate", ['career_status', 'character_temperament'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.2", "Ishu Yoga: all planets in 4 consecutive signs starting from apoklima — warrior nature, directional focus"),
    ("general", "yoga", "shakti_yoga", {}, "favorable", "moderate", ['career_status', 'wealth'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.3", "Shakti Yoga: all planets in 4 consecutive signs starting from panaphara — powerful accumulation"),
    ("general", "yoga", "danda_yoga", {}, "mixed", "moderate", ['career_status'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.4", "Danda Yoga: all planets in 4 consecutive signs starting from any — disciplined life path"),
    ("general", "yoga", "gada_yoga", {}, "favorable", "moderate", ['wealth', 'career_status'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.5", "Gada Yoga: planets in two kendras alternately — mace-like power, commercial success"),
    ("general", "yoga", "sakata_nabhasa", {}, "mixed", "moderate", ['wealth'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.6", "Sakata Yoga (Nabhasa): planets in 1st and 7th only — fluctuating fortune, chariot wheel pattern"),
    ("general", "yoga", "vihaga_yoga", {}, "favorable", "moderate", ['foreign_travel'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.7", "Vihaga Yoga: planets in 4th and 10th only — bird-like, travels extensively, restless"),
    ("general", "yoga", "sringataka_yoga", {}, "favorable", "moderate", ['wealth', 'marriage'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.8", "Sringataka Yoga: planets in trikonas (1/5/9) only — fortunate triangle, dharmic prosperity"),
    ("general", "yoga", "hala_yoga", {}, "mixed", "moderate", ['wealth', 'career_status'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.9", "Hala Yoga: planets in trikonas from any house — plough pattern, agricultural success"),
    ("general", "yoga", "vajra_yoga", {}, "favorable", "strong", ['career_status', 'character_temperament'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.10", "Vajra Yoga: benefics in 1st and 7th, malefics in 4th and 10th — diamond-strong, invincible"),
    ("general", "yoga", "yava_yoga", {}, "mixed", "moderate", ['wealth'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.11", "Yava Yoga: malefics in 1st and 7th, benefics in 4th and 10th — barley pattern, moderate fortune"),
    ("general", "yoga", "kamala_yoga", {}, "favorable", "strong", ['wealth', 'fame_reputation'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.12", "Kamala Yoga: all planets in kendras — lotus pattern, supreme fortune, multi-dimensional success"),
    ("general", "yoga", "vapi_yoga", {}, "favorable", "moderate", ['wealth', 'property_vehicles'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.13", "Vapi Yoga: all planets in panaparas (2/5/8/11) — well/reservoir pattern, accumulated resources"),
    ("general", "yoga", "kedara_yoga", {}, "favorable", "moderate", ['wealth', 'property_vehicles'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.14", "Kedara Yoga: planets in 7 houses — field pattern, agricultural wealth, land ownership"),
    ("general", "yoga", "sula_yoga", {}, "unfavorable", "moderate", ['physical_health'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.15", "Sula Yoga: planets in 3 houses only — trident pattern, sharp experiences, health crises"),
    ("general", "yoga", "musala_yoga", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.16", "Musala Yoga: all planets in fixed signs — pestle pattern, steady, persistent, unchanging"),
    ("general", "yoga", "nala_yoga", {}, "mixed", "moderate", ['character_temperament'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.17", "Nala Yoga: all planets in dual signs — reed pattern, adaptable, flexible, versatile"),
    ("general", "yoga", "rajju_yoga", {}, "favorable", "moderate", ['foreign_travel'], ['saravali', 'yoga', 'nabhasa_yogas'], "Ch.11-14 v.18", "Rajju Yoga: all planets in movable signs — rope pattern, traveling, active, dynamic"),
]

_SOLAR_LUNAR_YOGAS_DATA = [
    ("sun", "yoga", "vesi_yoga", {}, "favorable", "moderate", ['wealth', 'career_status'], ['sun', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.19", "Vesi Yoga: planet (not Moon) in 2nd from Sun — wealth through authority, supported leadership"),
    ("sun", "yoga", "vasi_yoga", {}, "favorable", "moderate", ['career_status', 'fame_reputation'], ['sun', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.20", "Vasi Yoga: planet (not Moon) in 12th from Sun — fame precedes, authority follows reputation"),
    ("sun", "yoga", "ubhayachari_yoga", {}, "favorable", "strong", ['career_status', 'wealth'], ['sun', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.21", "Ubhayachari Yoga: planets in both 2nd and 12th from Sun — surrounded authority, supreme support"),
    ("moon", "yoga", "sunapha_yoga", {}, "favorable", "moderate", ['wealth', 'intelligence_education'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.22", "Sunapha Yoga: planet (not Sun) in 2nd from Moon — self-made wealth, intellectual resources"),
    ("moon", "yoga", "anapha_yoga", {}, "favorable", "moderate", ['career_status', 'character_temperament'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.23", "Anapha Yoga: planet (not Sun) in 12th from Moon — dignified, well-dressed, virtuous"),
    ("moon", "yoga", "durudhura_yoga", {}, "favorable", "strong", ['wealth', 'career_status'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.24", "Durudhura Yoga: planets in both 2nd and 12th from Moon — surrounded mind, abundant resources"),
    ("moon", "yoga", "kemadruma_definition", {}, "unfavorable", "strong", ['wealth', 'mental_health'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.25", "Kemadruma: no planet in 2nd or 12th from Moon — isolated mind, poverty, mental distress"),
    ("moon", "yoga", "adhi_yoga", {}, "favorable", "strong", ['career_status', 'wealth'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.26", "Adhi Yoga: benefics in 6/7/8 from Moon — ministerial yoga, administrative authority, wealth"),
    ("moon", "yoga", "chandra_mangal_yoga", {}, "favorable", "moderate", ['wealth'], ['moon', 'saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.27", "Chandra-Mangal Yoga: Moon-Mars conjunction — self-made wealth, courage in business, earning through effort"),
    ("general", "yoga", "gajakesari_yoga", {}, "favorable", "strong", ['fame_reputation', 'wealth'], ['saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.28", "Gajakesari Yoga: Jupiter in kendra from Moon — elephant-lion, fame, wealth, wisdom, long life"),
    ("general", "yoga", "amala_yoga", {}, "favorable", "strong", ['fame_reputation', 'character_temperament'], ['saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.29", "Amala Yoga: benefic in 10th from Moon or lagna — spotless reputation, virtuous character"),
    ("general", "yoga", "dhana_yoga_general", {}, "favorable", "strong", ['wealth'], ['saravali', 'yoga', 'solar_lunar_yogas'], "Ch.11-14 v.30", "Dhana Yoga: 2nd/11th lords in kendras/trikonas mutually aspecting — wealth combination"),
]

_CHANDRA_YOGAS_DATA = [
    ("moon", "yoga", "chandra_aries", {}, "mixed", "moderate", ['character_temperament'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.31", "Moon in Aries: courageous mind, impulsive emotions, quick to anger and forgive, adventurous spirit"),
    ("moon", "yoga", "chandra_taurus", {}, "favorable", "strong", ['wealth', 'mental_health'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.32", "Moon exalted in Taurus: peaceful mind, material comfort, beautiful surroundings, emotional stability"),
    ("moon", "yoga", "chandra_cancer", {}, "favorable", "strong", ['mental_health', 'property_vehicles'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.33", "Moon in Cancer (own): supreme emotional intelligence, nurturing nature, domestic happiness"),
    ("moon", "yoga", "chandra_scorpio", {}, "unfavorable", "moderate", ['mental_health'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.34", "Moon debilitated in Scorpio: emotional turmoil, jealousy, suspicion, psychological depth through suffering"),
    ("moon", "yoga", "chandra_full_effect", {}, "favorable", "strong", ['wealth', 'mental_health'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.35", "Full Moon effect: maximum emotional strength, prosperity, creativity, public popularity"),
    ("moon", "yoga", "chandra_dark_effect", {}, "unfavorable", "moderate", ['mental_health', 'wealth'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.36", "Dark Moon effect: diminished emotional strength, vulnerability, financial caution needed"),
    ("moon", "yoga", "chandra_kendra", {}, "favorable", "moderate", ['career_status', 'mental_health'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.37", "Moon in kendra: emotional foundation for success, public connection, leadership through empathy"),
    ("moon", "yoga", "chandra_trikona", {}, "favorable", "moderate", ['wealth', 'spirituality'], ['moon', 'saravali', 'yoga', 'chandra_yogas'], "Ch.11-14 v.38", "Moon in trikona: fortunate emotions, blessed mind, dharmic sensitivity, intuitive prosperity"),
]


def _make_rules(data: list, start_id: int) -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    for i, t in enumerate(data):
        planet, ptype, pval, extra, direction, intensity, domains, tags, vref, desc = t
        pc = {"planet": planet, "placement_type": ptype, "placement_value": [pval] if pval else [], **extra}
        if ptype in ("yoga", "condition", "special"):
            pc["yoga_label"] = pval
        rid = f"SAV{start_id + i}"
        rules.append(RuleRecord(
            rule_id=rid, source="Saravali", chapter="Ch.11-14", school="parashari",
            category="special_topics", description=desc, confidence=0.65,
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
        (_NABHASA_YOGAS_DATA, 2736),
        (_SOLAR_LUNAR_YOGAS_DATA, 2754),
        (_CHANDRA_YOGAS_DATA, 2766),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_4_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_4_REGISTRY.add(_rule)
