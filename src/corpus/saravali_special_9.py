"""src/corpus/saravali_special_9.py — Saravali Special Topics (Ch.66-68).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_NIMITTA_OMENS_DATA = [
    ("general", "special", "nimitta_definition", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.1", "Nimitta (omens): signs observed at moment of chart reading — auspicious or inauspicious indicators"),
    ("general", "special", "nimitta_birds", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.2", "Bird omens: specific birds seen during consultation indicate favorable or unfavorable outcomes"),
    ("general", "special", "nimitta_sounds", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.3", "Sound omens: pleasant sounds = favorable, harsh sounds = unfavorable for the query subject"),
    ("general", "special", "nimitta_direction", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.4", "Direction omens: questioner approaching from specific direction indicates affected life area"),
    ("general", "special", "nimitta_body_signs", {}, "mixed", "moderate", ['physical_health'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.5", "Body signs: twitching, itching at specific body parts during reading — predictive indicators"),
    ("general", "special", "nimitta_time", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'nimitta_omens'], "Ch.66-68 v.6", "Time omens: auspicious/inauspicious hours for consultation, day of week significance"),
]

_GRAHA_YUDDHA_DATA = [
    ("general", "special", "graha_yuddha_def", {}, "mixed", "strong", ['career_status'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.7", "Graha Yuddha (planetary war): two planets within 1° — winner has higher latitude, loser debilitated"),
    ("general", "special", "yuddha_winner", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.8", "Planetary war winner: planet with higher northward latitude — gains strength of both karakatvas"),
    ("general", "special", "yuddha_loser", {}, "unfavorable", "strong", ['career_status'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.9", "Planetary war loser: effectively debilitated for entire life — karakatvas severely diminished"),
    ("general", "special", "yuddha_mars_mercury", {}, "mixed", "strong", ['intelligence_education', 'enemies_litigation'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.10", "Mars-Mercury war: intellect vs aggression, communication conflicts, engineering vs commerce"),
    ("general", "special", "yuddha_jupiter_venus", {}, "mixed", "strong", ['spirituality', 'marriage'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.11", "Jupiter-Venus war: wisdom vs beauty, dharma vs pleasure, teacher vs artist"),
    ("general", "special", "yuddha_mars_saturn", {}, "unfavorable", "strong", ['physical_health', 'career_status'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.12", "Mars-Saturn war: most dangerous, accidents, chronic conditions, extreme frustration"),
    ("general", "special", "yuddha_mercury_venus", {}, "mixed", "moderate", ['intelligence_education', 'marriage'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.13", "Mercury-Venus war: intellect vs aesthetics, commerce vs arts, communication vs beauty"),
    ("general", "special", "yuddha_jupiter_saturn", {}, "mixed", "strong", ['career_status', 'spirituality'], ['saravali', 'special', 'graha_yuddha'], "Ch.66-68 v.14", "Jupiter-Saturn war: expansion vs restriction, wisdom vs discipline, hope vs reality"),
]

_SUMMARY_PRINCIPLES_DATA = [
    ("general", "special", "bhava_karaka", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.15", "Bhava Karaka principle: each house has a natural significator whose strength supports house matters"),
    ("general", "special", "karaka_bhava_nashaya", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.16", "Karaka Bhava Nashaya: significator IN its own signified house — paradoxically weakens that house"),
    ("general", "special", "aspect_strength", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.17", "Aspect strength hierarchy: conjunction > opposition > trine > square — decreasing influence"),
    ("general", "special", "dignity_hierarchy", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.18", "Dignity strength: exalted > moolatrikona > own > friend > neutral > enemy > debilitated"),
    ("general", "special", "retrograde_strength", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.19", "Retrograde planets: considered strong in some texts — Saravali considers them as having special focus"),
    ("general", "special", "combustion_rule", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.20", "Combustion distances: Mars 17°, Mercury 14°(12° retrograde), Jupiter 11°, Venus 10°(8° retro), Saturn 15°"),
    ("general", "special", "avastha_system", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.21", "Planetary Avasthas: Bala(infant), Kumara(youth), Yuva(adult), Vruddha(old), Mrita(dead) — age-based strength"),
    ("general", "special", "varga_bala", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.22", "Varga Bala: planet in same sign across multiple divisional charts — amplified strength"),
    ("general", "special", "shadbala_minimum", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.23", "Shadbala minimum: each planet needs minimum rupas for strength — Sun 6.5, Moon 6.0, Mars 5.0, Mercury 7.0, Jupiter 6.5, Venus 5.5, Saturn 5.0"),
    ("general", "special", "prediction_priority", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'summary_principles'], "Ch.66-68 v.24", "Prediction priority: Dasha > Transit > Yoga > House lord > Aspect — hierarchical interpretation"),
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
            rule_id=rid, source="Saravali", chapter="Ch.66-68", school="parashari",
            category="special_topics", description=desc, confidence=0.65,
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
        (_NIMITTA_OMENS_DATA, 2875),
        (_GRAHA_YUDDHA_DATA, 2881),
        (_SUMMARY_PRINCIPLES_DATA, 2889),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_9_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_9_REGISTRY.add(_rule)
