"""src/corpus/saravali_special_2.py — Saravali Special Topics (Ch.6-8).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_LONGEVITY_BASICS_DATA = [
    ("saturn", "special", "saturn_longevity_karaka", {}, "mixed", "strong", ['longevity'], ['saturn', 'saravali', 'special', 'longevity_basics'], "Ch.6-8 v.1", "Saturn as Ayush Karaka: primary significator of longevity, its placement determines lifespan category"),
    ("general", "special", "long_life_100", {}, "favorable", "strong", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.2", "Purnayu (full life 100+ years): strong lagna lord, 8th lord, Saturn all in kendras/trikonas"),
    ("general", "special", "medium_life_70", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.3", "Madhyayu (medium life 60-80): mixed placement of longevity significators, some in dusthanas"),
    ("general", "special", "short_life_40", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.4", "Alpayu (short life 30-40): longevity lords weak, afflicted, in 6/8/12, malefic aspects"),
    ("general", "special", "infant_death", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.5", "Balarishta (infant death 0-8): severe affliction to Moon, lagna, 8th simultaneously by malefics"),
    ("moon", "special", "moon_infant_death", {}, "unfavorable", "strong", ['longevity'], ['moon', 'saravali', 'special', 'longevity_basics'], "Ch.6-8 v.6", "Moon afflicted for Balarishta: Moon hemmed by malefics, in 6/8/12, no benefic aspect — infant mortality risk"),
    ("jupiter", "special", "jupiter_saves_infant", {}, "favorable", "strong", ['longevity'], ['jupiter', 'saravali', 'special', 'longevity_basics'], "Ch.6-8 v.7", "Jupiter aspect cancels Balarishta: Jupiter aspecting Moon or lagna saves infant from early death"),
    ("general", "special", "yogayu_method", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.8", "Yogayu method: lifespan from yoga combinations — specific planet pairs add/subtract years"),
    ("general", "special", "pindayu_method", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.9", "Pindayu method: planetary contributions to lifespan based on house position and sign"),
    ("general", "special", "nisargayu_method", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'longevity_basics'], "Ch.6-8 v.10", "Nisargayu method: natural planetary years — Sun 19, Moon 25, Mars 15, Mercury 12, Jupiter 15, Venus 21, Saturn 20"),
]

_ARISHTA_YOGAS_DATA = [
    ("general", "yoga", "balarishta_1", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.11", "Balarishta: Moon in 6th/8th/12th from lagna with malefic aspect and no benefic influence"),
    ("general", "yoga", "balarishta_2", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.12", "Balarishta: lagna lord debilitated, 8th lord in lagna, both Moon and lagna hemmed by malefics"),
    ("general", "yoga", "balarishta_3", {}, "unfavorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.13", "Balarishta: all malefics in kendras, no benefic in kendra or trikona, weak Moon"),
    ("general", "yoga", "balarishta_cancel_1", {}, "favorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.14", "Balarishta cancelled: Jupiter in kendra from lagna or Moon — protects child from early death"),
    ("general", "yoga", "balarishta_cancel_2", {}, "favorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.15", "Balarishta cancelled: strong benefic in lagna, full Moon in kendra, benefic dasha operating"),
    ("general", "yoga", "arishta_mother", {}, "unfavorable", "moderate", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.16", "Matru Arishta: 4th lord afflicted, Moon in papakartari, malefics in 4th — mother danger"),
    ("general", "yoga", "arishta_father", {}, "unfavorable", "moderate", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.17", "Pitru Arishta: 9th lord afflicted, Sun weak, malefics in 9th — father danger"),
    ("general", "yoga", "arishta_spouse", {}, "unfavorable", "moderate", ['longevity', 'marriage'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.18", "Kalatra Arishta: 7th lord afflicted, Venus weak, malefics in 7th — spouse danger"),
    ("general", "yoga", "longevity_strong_1", {}, "favorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.19", "Strong longevity: lagna lord in kendra with benefic aspect, 8th lord strong, Saturn well-placed"),
    ("general", "yoga", "longevity_strong_2", {}, "favorable", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.20", "Strong longevity: benefics in 1/5/9, malefics in 3/6/11, no severe arishta — long healthy life"),
    ("general", "yoga", "longevity_medium", {}, "mixed", "moderate", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.21", "Medium longevity: mixed indicators, some benefic some malefic influence on 1st/8th lords"),
    ("general", "yoga", "death_timing", {}, "mixed", "strong", ['longevity'], ['saravali', 'yoga', 'arishta_yogas'], "Ch.6-8 v.22", "Death timing: maraka dasha (2nd/7th lord) with transit Saturn over natal Moon or 8th house"),
]

_AYURDAYA_CALC_DATA = [
    ("general", "special", "ayurdaya_sun", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.23", "Sun contribution to lifespan: based on house position, 19 years maximum, reduced by affliction"),
    ("general", "special", "ayurdaya_moon", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.24", "Moon contribution: 25 years maximum, reduced by malefic aspect, waning phase reduces further"),
    ("general", "special", "ayurdaya_mars", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.25", "Mars contribution: 15 years maximum, own/exalted gives full share, debilitated halves"),
    ("general", "special", "ayurdaya_mercury", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.26", "Mercury contribution: 12 years maximum, intellectual activities extend, combust reduces"),
    ("general", "special", "ayurdaya_jupiter", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.27", "Jupiter contribution: 15 years maximum, strong Jupiter gives full share, protects life"),
    ("general", "special", "ayurdaya_venus", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.28", "Venus contribution: 21 years maximum, strong Venus extends, debilitated reduces significantly"),
    ("general", "special", "ayurdaya_saturn", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.29", "Saturn contribution: 20 years maximum, exalted Saturn gives full longevity, debilitated halves"),
    ("general", "special", "ayurdaya_lagna", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.30", "Lagna contribution: house position of lagna lord adds/subtracts years proportionally"),
    ("general", "special", "chakrapani_correction", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.31", "Chakrapani correction: reduction for combustion, planetary war, debilitation — proportional decrease"),
    ("general", "special", "kakshya_hrasa", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'ayurdaya_calc'], "Ch.6-8 v.32", "Kakshya Hrasa: kakshya-based reduction — each malefic transit reduces calculated lifespan by fraction"),
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
            rule_id=rid, source="Saravali", chapter="Ch.6-8", school="parashari",
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
        (_LONGEVITY_BASICS_DATA, 2674),
        (_ARISHTA_YOGAS_DATA, 2684),
        (_AYURDAYA_CALC_DATA, 2696),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_2_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_2_REGISTRY.add(_rule)
