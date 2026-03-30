"""src/corpus/saravali_special_8.py — Saravali Special Topics (Ch.61-65).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_DEATH_CIRCUMSTANCES_DATA = [
    ("general", "special", "death_fire", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.1", "Death by fire: Mars in 8th, Sun afflicting 8th lord, fire signs prominent in 8th/3rd"),
    ("general", "special", "death_water", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.2", "Death by drowning: Moon in 8th afflicted, water signs in 8th, Saturn-Moon in watery navamsa"),
    ("general", "special", "death_weapon", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.3", "Death by weapon: Mars-Saturn in 8th, Aries/Scorpio in 8th, Mars aspect on 8th lord"),
    ("general", "special", "death_disease", {}, "unfavorable", "moderate", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.4", "Death by disease: 6th lord in 8th, chronic planet in 8th, no benefic aspect on 8th"),
    ("general", "special", "death_fall", {}, "unfavorable", "moderate", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.5", "Death by fall: Saturn in 8th, Rahu in 8th in airy sign, afflicted 8th in movable sign"),
    ("general", "special", "death_peaceful", {}, "favorable", "moderate", ['longevity', 'spirituality'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.6", "Peaceful death: benefics in 8th, Jupiter aspecting 8th, strong 8th lord in benefic sign"),
    ("general", "special", "death_direction", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.7", "Death direction: determined by strongest planet in 8th house sign — fire=East, earth=South, air=West, water=North"),
    ("general", "special", "death_place", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.8", "Death place: movable sign on 8th = foreign land, fixed = own home, dual = while traveling"),
    ("general", "special", "maraka_dasha", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.9", "Maraka Dasha: 2nd/7th lord dasha at advanced age, with transit Saturn over 8th — death timing"),
    ("general", "special", "maraka_planet", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'death_circumstances'], "Ch.61-65 v.10", "Maraka planet identification: 2nd lord is primary maraka, 7th lord secondary, connected malefics support"),
]

_LOST_HOROSCOPY_DATA = [
    ("general", "special", "nashta_jataka_lagna", {}, "mixed", "moderate", ['character_temperament'], ['saravali', 'special', 'lost_horoscopy'], "Ch.61-65 v.11", "Nashta Jataka lagna recovery: from prasna chart rising sign at moment of query about lost chart"),
    ("general", "special", "nashta_moon", {}, "mixed", "moderate", ['mental_health'], ['saravali', 'special', 'lost_horoscopy'], "Ch.61-65 v.12", "Lost horoscopy Moon: derived from questioners mental state, day of week, nakshatra at query time"),
    ("general", "special", "nashta_planets", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'lost_horoscopy'], "Ch.61-65 v.13", "Lost chart planetary positions: reconstructed from life events, physical features, known dashas"),
    ("general", "special", "nashta_verification", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'lost_horoscopy'], "Ch.61-65 v.14", "Verification method: reconstructed chart tested against known life events — matches confirm accuracy"),
]

_DREKKANA_EFFECTS_DATA = [
    ("general", "special", "drekkana_1st", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.15", "1st Drekkana (0-10°): personality strongly shaped by sign lord, robust physical expression"),
    ("general", "special", "drekkana_2nd", {}, "mixed", "moderate", ['character_temperament'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.16", "2nd Drekkana (10-20°): 5th sign lord influence, creative and intellectual coloring"),
    ("general", "special", "drekkana_3rd", {}, "mixed", "moderate", ['character_temperament'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.17", "3rd Drekkana (20-30°): 9th sign lord influence, dharmic and philosophical coloring"),
    ("general", "special", "drekkana_8th", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.18", "8th house Drekkana: determines manner of death — serpent/human/divine form indicates death type"),
    ("general", "special", "drekkana_22nd", {}, "unfavorable", "moderate", ['longevity'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.19", "22nd Drekkana (Khara): 22nd drekkana from lagna — always malefic, indicates vulnerable body part"),
    ("general", "special", "drekkana_lagna", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'special', 'drekkana_effects'], "Ch.61-65 v.20", "Lagna Drekkana: first third of rising sign — strongest personal influence on appearance and nature"),
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
            rule_id=rid, source="Saravali", chapter="Ch.61-65", school="parashari",
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
        (_DEATH_CIRCUMSTANCES_DATA, 2855),
        (_LOST_HOROSCOPY_DATA, 2865),
        (_DREKKANA_EFFECTS_DATA, 2869),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_8_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_8_REGISTRY.add(_rule)
