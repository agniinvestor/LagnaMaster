"""src/corpus/saravali_special_5.py — Saravali Special Topics (Ch.43-48).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_BHAVA_EFFECTS_1_6_DATA = [
    ("general", "special", "bhava_1_strong", {}, "favorable", "strong", ['physical_appearance', 'longevity'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.1", "Strong 1st house: robust health, attractive personality, long life, self-confidence"),
    ("general", "special", "bhava_1_weak", {}, "unfavorable", "moderate", ['physical_health', 'character_temperament'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.2", "Weak 1st house: sickly constitution, lack of confidence, poor self-image"),
    ("general", "special", "bhava_2_strong", {}, "favorable", "strong", ['wealth', 'intelligence_education'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.3", "Strong 2nd house: great wealth, eloquent speech, happy family, good food"),
    ("general", "special", "bhava_2_weak", {}, "unfavorable", "moderate", ['wealth'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.4", "Weak 2nd house: poverty, speech defects, family discord, poor nutrition"),
    ("general", "special", "bhava_3_strong", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.5", "Strong 3rd house: courageous, creative siblings, communication skills, short travel success"),
    ("general", "special", "bhava_3_weak", {}, "unfavorable", "moderate", ['character_temperament'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.6", "Weak 3rd house: cowardice, sibling enmity, communication failures, travel problems"),
    ("general", "special", "bhava_4_strong", {}, "favorable", "strong", ['property_vehicles', 'mental_health'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.7", "Strong 4th house: beautiful home, vehicles, domestic happiness, emotional peace, mother blessed"),
    ("general", "special", "bhava_4_weak", {}, "unfavorable", "moderate", ['mental_health', 'property_vehicles'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.8", "Weak 4th house: homeless feeling, vehicle problems, domestic unhappiness, mother suffers"),
    ("general", "special", "bhava_5_strong", {}, "favorable", "strong", ['intelligence_education', 'progeny'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.9", "Strong 5th house: brilliant mind, blessed children, creative genius, past-life merit"),
    ("general", "special", "bhava_5_weak", {}, "unfavorable", "moderate", ['progeny', 'intelligence_education'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.10", "Weak 5th house: childlessness or difficult children, poor intellect, no spiritual merit"),
    ("general", "special", "bhava_6_strong", {}, "favorable", "moderate", ['enemies_litigation'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.11", "Strong 6th house: victory over enemies, good health through service, competitive success"),
    ("general", "special", "bhava_6_weak", {}, "unfavorable", "moderate", ['physical_health', 'enemies_litigation'], ['saravali', 'special', 'bhava_effects_1_6'], "Ch.43-48 v.12", "Weak 6th house: defeated by enemies, chronic disease, debts overwhelm, servant problems"),
]

_BHAVA_EFFECTS_7_12_DATA = [
    ("general", "special", "bhava_7_strong", {}, "favorable", "strong", ['marriage'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.13", "Strong 7th house: happy marriage, beautiful spouse, successful partnerships, business success"),
    ("general", "special", "bhava_7_weak", {}, "unfavorable", "moderate", ['marriage'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.14", "Weak 7th house: marital unhappiness, no partner, failed partnerships, business losses"),
    ("general", "special", "bhava_8_strong", {}, "favorable", "moderate", ['longevity'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.15", "Strong 8th house: long life, inheritance, occult knowledge, transformation capacity"),
    ("general", "special", "bhava_8_weak", {}, "unfavorable", "strong", ['longevity', 'physical_health'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.16", "Weak 8th house: short life, chronic disease, no inheritance, sudden crises"),
    ("general", "special", "bhava_9_strong", {}, "favorable", "strong", ['wealth', 'spirituality'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.17", "Strong 9th house: great fortune, dharmic father, guru blessings, pilgrimage, higher education"),
    ("general", "special", "bhava_9_weak", {}, "unfavorable", "moderate", ['wealth', 'spirituality'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.18", "Weak 9th house: unfortunate, father troubled, no guru guidance, irreligious, poor fortune"),
    ("general", "special", "bhava_10_strong", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.19", "Strong 10th house: high career achievement, public honor, professional eminence, lasting legacy"),
    ("general", "special", "bhava_10_weak", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.20", "Weak 10th house: career failure, no public recognition, menial work, professional obscurity"),
    ("general", "special", "bhava_11_strong", {}, "favorable", "strong", ['wealth'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.21", "Strong 11th house: abundant gains, fulfilled desires, wealthy friends, aspirations achieved"),
    ("general", "special", "bhava_11_weak", {}, "unfavorable", "moderate", ['wealth'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.22", "Weak 11th house: unfulfilled desires, no gains, poor friends, aspirations blocked"),
    ("general", "special", "bhava_12_strong", {}, "favorable", "moderate", ['spirituality'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.23", "Strong 12th house: spiritual liberation, peaceful exit, comfortable foreign stay, good sleep"),
    ("general", "special", "bhava_12_weak", {}, "unfavorable", "moderate", ['wealth', 'physical_health'], ['saravali', 'special', 'bhava_effects_7_12'], "Ch.43-48 v.24", "Weak 12th house: heavy expenditure, hospitalization, imprisonment, exile, disturbed sleep"),
]

_BHAVA_LORDS_DATA = [
    ("general", "special", "bhava_lord_own", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.25", "Bhava lord in own house: significations flourish, full expression of house matters"),
    ("general", "special", "bhava_lord_exalted", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.26", "Bhava lord exalted: extraordinary results of that house, beyond normal expectations"),
    ("general", "special", "bhava_lord_debilitated", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.27", "Bhava lord debilitated: house matters suffer severely, needs remedial measures"),
    ("general", "special", "bhava_lord_6_8_12", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.28", "Bhava lord in 6/8/12 from own house: significations obstructed, delayed, or destroyed"),
    ("general", "special", "bhava_lord_kendra", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.29", "Bhava lord in kendra from own house: supported significations, angular strength"),
    ("general", "special", "bhava_lord_trikona", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'bhava_lords'], "Ch.43-48 v.30", "Bhava lord in trikona from own house: fortunate expression, dharmic support"),
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
            rule_id=rid, source="Saravali", chapter="Ch.43-48", school="parashari",
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
        (_BHAVA_EFFECTS_1_6_DATA, 2774),
        (_BHAVA_EFFECTS_7_12_DATA, 2786),
        (_BHAVA_LORDS_DATA, 2798),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_5_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_5_REGISTRY.add(_rule)
