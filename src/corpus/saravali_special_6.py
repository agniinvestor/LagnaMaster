"""src/corpus/saravali_special_6.py — Saravali Special Topics (Ch.49-53).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_STRI_JATAKA_DATA = [
    ("venus", "special", "venus_female_chart", {}, "favorable", "strong", ['marriage', 'physical_appearance'], ['venus', 'saravali', 'special', 'stri_jataka'], "Ch.49-53 v.1", "Venus strong in female chart: beautiful, attractive, devoted wife, romantic fulfillment"),
    ("mars", "special", "mars_female_chart", {}, "mixed", "moderate", ['marriage'], ['mars', 'saravali', 'special', 'stri_jataka'], "Ch.49-53 v.2", "Mars strong in female chart: independent woman, manglik effects, passionate but dominating"),
    ("moon", "special", "moon_female_chart", {}, "favorable", "strong", ['marriage', 'progeny'], ['moon', 'saravali', 'special', 'stri_jataka'], "Ch.49-53 v.3", "Moon strong in female chart: fertile, nurturing mother, emotionally rich married life"),
    ("saturn", "special", "saturn_female_chart", {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'special', 'stri_jataka'], "Ch.49-53 v.4", "Saturn afflicting 7th in female chart: delayed marriage, older husband, cold relationship"),
    ("general", "special", "7th_lord_female", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.5", "7th lord strong in female chart: good husband, happy marriage, supportive partner"),
    ("general", "special", "8th_house_female", {}, "mixed", "moderate", ['marriage', 'longevity'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.6", "8th house in female chart: mangalya (marital auspiciousness), husband longevity, conjugal happiness"),
    ("general", "special", "venus_mars_female", {}, "mixed", "moderate", ['marriage', 'character_temperament'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.7", "Venus-Mars conjunction female chart: passionate nature, intense romantic life, multiple attractions"),
    ("general", "special", "moon_saturn_female", {}, "unfavorable", "moderate", ['marriage', 'mental_health'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.8", "Moon-Saturn in female chart: emotional restriction, depression, delayed marriage, cold husband"),
    ("jupiter", "special", "jupiter_7th_female", {}, "favorable", "strong", ['marriage'], ['jupiter', 'saravali', 'special', 'stri_jataka'], "Ch.49-53 v.9", "Jupiter in/aspecting 7th female chart: virtuous husband, dharmic marriage, children blessed"),
    ("general", "special", "widow_yoga", {}, "unfavorable", "strong", ['marriage', 'longevity'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.10", "Widow yoga: 8th lord afflicted, malefics in 8th, no benefic aspect on 8th — husband longevity concern"),
    ("general", "special", "remarriage_yoga", {}, "mixed", "moderate", ['marriage'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.11", "Remarriage yoga: dual signs on 7th cusp, 7th lord in dual sign, Venus in dual — second marriage likely"),
    ("general", "special", "barren_yoga", {}, "unfavorable", "strong", ['progeny'], ['saravali', 'special', 'stri_jataka'], "Ch.49-53 v.12", "Barren yoga: 5th lord afflicted, malefics in 5th, no benefic influence — childlessness"),
]

_MARRIAGE_TIMING_DATA = [
    ("venus", "special", "venus_dasha_marriage", {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'special', 'marriage_timing'], "Ch.49-53 v.13", "Marriage in Venus dasha: Venus as natural karaka, its dasha period most likely for marriage"),
    ("general", "special", "7th_lord_dasha", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'marriage_timing'], "Ch.49-53 v.14", "Marriage in 7th lord dasha: activated house of partnership, transit support confirms"),
    ("jupiter", "special", "jupiter_transit_7th", {}, "favorable", "moderate", ['marriage'], ['jupiter', 'saravali', 'special', 'marriage_timing'], "Ch.49-53 v.15", "Jupiter transit over 7th or 7th lord: expansion of partnership area, marriage facilitated"),
    ("saturn", "special", "saturn_transit_7th", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'special', 'marriage_timing'], "Ch.49-53 v.16", "Saturn transit over 7th: delay or mature partnership, serious commitment, older partner"),
    ("general", "special", "vivaha_muhurta", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'marriage_timing'], "Ch.49-53 v.17", "Marriage Muhurta: auspicious lunar day, nakshatra, and ascendant ensure lasting bond"),
    ("general", "special", "manglik_matching", {}, "mixed", "moderate", ['marriage'], ['saravali', 'special', 'marriage_timing'], "Ch.49-53 v.18", "Manglik matching: Mars dosha checked in both charts, cancelled if both manglik"),
    ("general", "special", "guna_matching", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'marriage_timing'], "Ch.49-53 v.19", "Guna Milan (36 points): compatibility scoring across 8 dimensions, minimum 18 for acceptance"),
    ("general", "special", "nadi_dosha", {}, "unfavorable", "strong", ['marriage', 'progeny'], ['saravali', 'special', 'marriage_timing'], "Ch.49-53 v.20", "Nadi Dosha: same nadi in both charts — genetic incompatibility, progeny concerns, health issues"),
]

_PROGENY_DATA = [
    ("jupiter", "special", "jupiter_5th_children", {}, "favorable", "strong", ['progeny'], ['jupiter', 'saravali', 'special', 'progeny'], "Ch.49-53 v.21", "Jupiter in/aspecting 5th: blessed with children, virtuous offspring, many children possible"),
    ("general", "special", "5th_lord_strong", {}, "favorable", "moderate", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.22", "5th lord strong: children prosper, good education, obedient offspring, family continues"),
    ("general", "special", "5th_lord_weak", {}, "unfavorable", "moderate", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.23", "5th lord weak: delayed children, sickly offspring, educational difficulties, disobedient children"),
    ("saturn", "special", "saturn_5th_children", {}, "unfavorable", "moderate", ['progeny'], ['saturn', 'saravali', 'special', 'progeny'], "Ch.49-53 v.24", "Saturn in/afflicting 5th: delayed childbirth, few children, adoption considered, strict parenting"),
    ("general", "special", "putra_dosha", {}, "unfavorable", "strong", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.25", "Putra Dosha: 5th lord in 6/8/12, malefics in 5th, no benefic aspect — childlessness concern"),
    ("general", "special", "santhana_yoga", {}, "favorable", "strong", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.26", "Santhana Yoga: 5th lord with Jupiter, benefics in 5th — blessed with many worthy children"),
    ("general", "special", "first_child_gender", {}, "mixed", "moderate", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.27", "First child gender: odd signs on 5th cusp and odd navamsa — male child; even signs — female"),
    ("general", "special", "child_timing", {}, "favorable", "moderate", ['progeny'], ['saravali', 'special', 'progeny'], "Ch.49-53 v.28", "Child timing: Jupiter transit over 5th or 5th lord, 5th lord dasha, benefic antardasha"),
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
            rule_id=rid, source="Saravali", chapter="Ch.49-53", school="parashari",
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
        (_STRI_JATAKA_DATA, 2804),
        (_MARRIAGE_TIMING_DATA, 2816),
        (_PROGENY_DATA, 2824),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_6_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_6_REGISTRY.add(_rule)
