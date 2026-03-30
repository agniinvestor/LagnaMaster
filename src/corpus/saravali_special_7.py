"""src/corpus/saravali_special_7.py — Saravali Special Topics (Ch.54-60).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_DASHA_GENERAL_DATA = [
    ("sun", "special", "sun_dasha", {}, "mixed", "moderate", ['career_status', 'physical_health'], ['sun', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.1", "Sun Mahadasha (6 years): government connections, authority, father events, fevers, eye problems"),
    ("moon", "special", "moon_dasha", {}, "favorable", "moderate", ['mental_health', 'wealth'], ['moon', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.2", "Moon Mahadasha (10 years): public success, emotional events, mother, water-related gains"),
    ("mars", "special", "mars_dasha", {}, "mixed", "moderate", ['career_status', 'enemies_litigation'], ['mars', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.3", "Mars Mahadasha (7 years): courage, property, brothers, surgeries, accidents, legal battles"),
    ("mercury", "special", "mercury_dasha", {}, "favorable", "moderate", ['intelligence_education', 'wealth'], ['mercury', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.4", "Mercury Mahadasha (17 years): learning, commerce, writing, communication, versatile income"),
    ("jupiter", "special", "jupiter_dasha", {}, "favorable", "strong", ['wealth', 'spirituality'], ['jupiter', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.5", "Jupiter Mahadasha (16 years): wisdom, children, fortune, dharma, teaching, institutional growth"),
    ("venus", "special", "venus_dasha", {}, "favorable", "strong", ['marriage', 'wealth'], ['venus', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.6", "Venus Mahadasha (20 years): marriage, luxury, vehicles, arts, romance, material comforts"),
    ("saturn", "special", "saturn_dasha", {}, "mixed", "strong", ['career_status', 'longevity'], ['saturn', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.7", "Saturn Mahadasha (19 years): discipline, delays, chronic issues, eventual mastery, karmic lessons"),
    ("rahu", "special", "rahu_dasha", {}, "mixed", "strong", ['career_status', 'foreign_travel'], ['rahu', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.8", "Rahu Mahadasha (18 years): foreign connections, unconventional success, obsession, technology"),
    ("ketu", "special", "ketu_dasha", {}, "mixed", "moderate", ['spirituality'], ['ketu', 'saravali', 'special', 'dasha_general'], "Ch.54-60 v.9", "Ketu Mahadasha (7 years): spiritual transformation, detachment, past-life resolution, moksha tendency"),
]

_ASHTAKAVARGA_RESULTS_DATA = [
    ("general", "special", "av_high_bindus", {}, "favorable", "strong", ['wealth', 'career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.10", "High Ashtakavarga bindus in house: significations of that house prosper, gains during transit"),
    ("general", "special", "av_low_bindus", {}, "unfavorable", "moderate", ['wealth', 'career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.11", "Low Ashtakavarga bindus: house matters suffer during transit, obstacles and delays"),
    ("general", "special", "av_sarvashtaka_28plus", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.12", "Sarvashtakavarga 28+ bindus in house: strongly beneficial house, transit always positive"),
    ("general", "special", "av_sarvashtaka_below_25", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.13", "Sarvashtakavarga below 25 bindus: weak house, transit brings difficulties"),
    ("general", "special", "av_kakshya_transit", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.14", "Kakshya-level transit: sub-period within transit determined by which planets kakshya is transited"),
    ("general", "special", "av_shodhana", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'ashtakavarga_results'], "Ch.54-60 v.15", "Shodhana reduction: Trikona and Ekadhipatya reduction refines raw bindus for precision"),
]

_TRANSIT_EFFECTS_DATA = [
    ("saturn", "special", "sade_sati", {}, "unfavorable", "strong", ['mental_health', 'career_status'], ['saturn', 'saravali', 'special', 'transit_effects'], "Ch.54-60 v.16", "Sade Sati (Saturn transit over Moon ±1 sign): 7.5 year period of karmic testing, emotional challenge"),
    ("saturn", "special", "sade_sati_peak", {}, "unfavorable", "strong", ['mental_health', 'physical_health'], ['saturn', 'saravali', 'special', 'transit_effects'], "Ch.54-60 v.17", "Sade Sati peak (Saturn on natal Moon): most intense period, depression, loss, transformation"),
    ("saturn", "special", "ashtama_shani", {}, "unfavorable", "moderate", ['physical_health', 'longevity'], ['saturn', 'saravali', 'special', 'transit_effects'], "Ch.54-60 v.18", "Ashtama Shani (Saturn in 8th from Moon): health crisis, longevity concern, hidden enemies"),
    ("jupiter", "special", "jupiter_transit_benefic", {}, "favorable", "strong", ['wealth', 'career_status'], ['jupiter', 'saravali', 'special', 'transit_effects'], "Ch.54-60 v.19", "Jupiter transit through benefic houses: expansion, opportunity, fortune, growth period"),
    ("general", "special", "double_transit", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'transit_effects'], "Ch.54-60 v.20", "Double Transit Theory: Jupiter + Saturn both aspecting a house — event manifests in that area"),
    ("general", "special", "vedha_point", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'transit_effects'], "Ch.54-60 v.21", "Vedha (obstruction): transit benefic obstructed by specific vedha point — benefits blocked"),
    ("general", "special", "retrograde_transit", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'transit_effects'], "Ch.54-60 v.22", "Retrograde transit: planet revisits house — unfinished business, review period, delays"),
    ("general", "special", "transit_over_natal", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'transit_effects'], "Ch.54-60 v.23", "Transit over natal position: planet returns to birth position — new cycle begins, renewal"),
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
            rule_id=rid, source="Saravali", chapter="Ch.54-60", school="parashari",
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
        (_DASHA_GENERAL_DATA, 2832),
        (_ASHTAKAVARGA_RESULTS_DATA, 2841),
        (_TRANSIT_EFFECTS_DATA, 2847),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_7_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_7_REGISTRY.add(_rule)
