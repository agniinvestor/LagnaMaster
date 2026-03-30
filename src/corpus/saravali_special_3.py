"""src/corpus/saravali_special_3.py — Saravali Special Topics (Ch.9-10).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_RAJA_YOGAS_DATA = [
    ("general", "yoga", "raja_yoga_basic", {}, "favorable", "strong", ['career_status', 'wealth', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.1", "Raja Yoga basic: lord of kendra conjunct/aspecting lord of trikona — kingly status, authority, wealth"),
    ("general", "yoga", "raja_yoga_1_5", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.2", "Raja Yoga 1-5: lagna lord + 5th lord conjunction or mutual aspect — creative authority"),
    ("general", "yoga", "raja_yoga_1_9", {}, "favorable", "strong", ['career_status', 'wealth'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.3", "Raja Yoga 1-9: lagna lord + 9th lord conjunction — dharmic authority, paternal blessing"),
    ("general", "yoga", "raja_yoga_4_5", {}, "favorable", "strong", ['property_vehicles', 'intelligence_education'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.4", "Raja Yoga 4-5: 4th lord + 5th lord — educational eminence, property through intellect"),
    ("general", "yoga", "raja_yoga_4_9", {}, "favorable", "strong", ['property_vehicles', 'spirituality'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.5", "Raja Yoga 4-9: 4th lord + 9th lord — fortunate home, dharmic prosperity, mother blessed"),
    ("general", "yoga", "raja_yoga_5_9", {}, "favorable", "strong", ['spirituality', 'intelligence_education'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.6", "Raja Yoga 5-9: 5th lord + 9th lord — trikona-trikona, supreme dharmic fortune, philosophical king"),
    ("general", "yoga", "raja_yoga_7_9", {}, "favorable", "strong", ['marriage', 'wealth'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.7", "Raja Yoga 7-9: 7th lord + 9th lord — fortune through marriage, spouse brings luck"),
    ("general", "yoga", "raja_yoga_10_9", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.8", "Raja Yoga 10-9: 10th lord + 9th lord — dharma-karma adhipati, supreme professional success"),
    ("general", "yoga", "raja_yoga_10_5", {}, "favorable", "strong", ['career_status', 'intelligence_education'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.9", "Raja Yoga 10-5: 10th lord + 5th lord — creative professional eminence, scholarly authority"),
    ("general", "yoga", "pancha_mahapurusha_general", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.10", "Pancha Mahapurusha: Mars/Mercury/Jupiter/Venus/Saturn in own/exalted in kendra — great personality"),
    ("general", "yoga", "ruchaka_yoga", {}, "favorable", "strong", ['career_status', 'character_temperament'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.11", "Ruchaka Yoga (Mars): martial eminence, commanding, courageous, military/sports authority"),
    ("general", "yoga", "bhadra_yoga", {}, "favorable", "strong", ['intelligence_education', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.12", "Bhadra Yoga (Mercury): intellectual eminence, scholarly, eloquent, commercial success"),
    ("general", "yoga", "hamsa_yoga", {}, "favorable", "strong", ['spirituality', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.13", "Hamsa Yoga (Jupiter): saintly eminence, wisdom, dharmic authority, revered teacher"),
    ("general", "yoga", "malavya_yoga", {}, "favorable", "strong", ['physical_appearance', 'wealth'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.14", "Malavya Yoga (Venus): beauty, luxury, artistic eminence, romantic fulfillment, vehicles"),
    ("general", "yoga", "shasha_yoga", {}, "favorable", "strong", ['career_status', 'longevity'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.15", "Shasha Yoga (Saturn): disciplined eminence, lasting authority, institutional leadership"),
    ("general", "yoga", "raja_yoga_strength", {}, "favorable", "moderate", ['career_status'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.16", "Raja Yoga strength: determined by dignity of involved lords, house placement, and aspects received"),
    ("general", "yoga", "raja_yoga_dasha", {}, "favorable", "strong", ['career_status', 'wealth'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.17", "Raja Yoga fructification: activates during dasha/antardasha of involved lords, not before"),
    ("general", "yoga", "multiple_raja", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saravali', 'yoga', 'raja_yogas'], "Ch.9-10 v.18", "Multiple Raja Yogas: cumulative effect, each additional yoga amplifies authority and fortune"),
]

_AVA_YOGAS_DATA = [
    ("general", "yoga", "daridra_yoga", {}, "unfavorable", "strong", ['wealth'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.19", "Daridra Yoga: 11th lord in 6/8/12, or 11th house afflicted by malefics — poverty, financial ruin"),
    ("general", "yoga", "kemadruma_yoga", {}, "unfavorable", "strong", ['wealth', 'mental_health'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.20", "Kemadruma Yoga: no planet in 2nd/12th from Moon — poverty, mental distress, isolation"),
    ("general", "yoga", "kemadruma_cancel", {}, "favorable", "moderate", ['wealth'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.21", "Kemadruma cancelled: planet in kendra from Moon or lagna, or Moon in kendra — mitigates poverty"),
    ("general", "yoga", "shakata_yoga", {}, "unfavorable", "moderate", ['wealth', 'career_status'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.22", "Shakata Yoga: Jupiter in 6/8/12 from Moon — fluctuating fortune, ups and downs in career"),
    ("general", "yoga", "duryoga", {}, "unfavorable", "moderate", ['wealth'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.23", "Duryoga: 10th lord in 6/8/12 — career difficulties, professional setbacks, service under others"),
    ("general", "yoga", "grahan_yoga", {}, "unfavorable", "strong", ['mental_health'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.24", "Grahan Yoga: Sun/Moon conjunct Rahu/Ketu — eclipse energy, psychological disturbance, obsession"),
    ("general", "yoga", "guru_chandal", {}, "unfavorable", "moderate", ['spirituality', 'intelligence_education'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.25", "Guru Chandal Yoga: Jupiter conjunct Rahu — corrupted wisdom, unorthodox beliefs, false gurus"),
    ("general", "yoga", "vish_yoga", {}, "unfavorable", "moderate", ['mental_health', 'marriage'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.26", "Vish Yoga: Moon conjunct Saturn — emotional restriction, depression, delayed happiness"),
    ("general", "yoga", "chandal_dosha", {}, "unfavorable", "moderate", ['character_temperament'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.27", "Chandal Dosha: Jupiter with Rahu/Ketu — dharmic confusion, unconventional morality"),
    ("general", "yoga", "papa_kartari", {}, "unfavorable", "moderate", ['career_status'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.28", "Papakartari Yoga: house hemmed between two malefics — trapped energy, obstructed significations"),
    ("general", "yoga", "shubha_kartari", {}, "favorable", "moderate", ['career_status'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.29", "Shubhakartari Yoga: house hemmed between two benefics — protected and nourished significations"),
    ("general", "yoga", "sakata_bhanga", {}, "favorable", "moderate", ['wealth'], ['saravali', 'yoga', 'ava_yogas'], "Ch.9-10 v.30", "Shakata Yoga cancelled: Jupiter in kendra from lagna despite 6/8/12 from Moon — fortune restored"),
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
            rule_id=rid, source="Saravali", chapter="Ch.9-10", school="parashari",
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
        (_RAJA_YOGAS_DATA, 2706),
        (_AVA_YOGAS_DATA, 2724),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_3_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_3_REGISTRY.add(_rule)
