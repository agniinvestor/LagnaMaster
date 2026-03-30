"""src/corpus/saravali_special_1.py — Saravali Special Topics (Ch.1-5).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_PLANET_NATURES_DATA = [
    ("sun", "special", "sun_nature", {}, "favorable", "strong", ['character_temperament'], ['sun', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.1", "Sun: King of planets, Sattvic, Agni tattva, Pitta, governs soul/father/bones/heart/eyes/authority"),
    ("moon", "special", "moon_nature", {}, "favorable", "strong", ['mental_health'], ['moon', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.2", "Moon: Queen, Sattvic, Jala tattva, Kapha-Vata, governs mind/mother/blood/emotions/public"),
    ("mars", "special", "mars_nature", {}, "mixed", "strong", ['character_temperament'], ['mars', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.3", "Mars: Commander, Tamasic, Agni tattva, Pitta, governs courage/brothers/land/blood/surgery"),
    ("mercury", "special", "mercury_nature", {}, "favorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.4", "Mercury: Prince, Rajasic, Prithvi tattva, Tridosha, governs speech/commerce/intellect/writing"),
    ("jupiter", "special", "jupiter_nature", {}, "favorable", "strong", ['spirituality'], ['jupiter', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.5", "Jupiter: Minister/Guru, Sattvic, Akasha tattva, Kapha, governs wisdom/children/dharma/wealth"),
    ("venus", "special", "venus_nature", {}, "favorable", "strong", ['marriage'], ['venus', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.6", "Venus: Preceptor of Asuras, Rajasic, Jala tattva, Kapha-Vata, governs love/beauty/vehicles/arts"),
    ("saturn", "special", "saturn_nature", {}, "unfavorable", "strong", ['longevity'], ['saturn', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.7", "Saturn: Servant, Tamasic, Vayu tattva, Vata, governs longevity/discipline/karma/servants/grief"),
    ("rahu", "special", "rahu_nature", {}, "mixed", "strong", ['foreign_travel'], ['rahu', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.8", "Rahu: Shadow planet, Tamasic, foreign obsession, technology, unconventional, outcaste, poison"),
    ("ketu", "special", "ketu_nature", {}, "mixed", "strong", ['spirituality'], ['ketu', 'saravali', 'special', 'planet_natures'], "Ch.1-5 v.9", "Ketu: Shadow planet, Tamasic but spiritual, moksha karaka, past-life, detachment, liberation"),
]

_SIGN_NATURES_DATA = [
    ("general", "special", "aries_nature", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.10", "Aries: Movable/fire/male, ruled by Mars, head of Kalapurusha, pioneering, aggressive"),
    ("general", "special", "taurus_nature", {}, "favorable", "moderate", ['wealth'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.11", "Taurus: Fixed/earth/female, ruled by Venus, face of Kalapurusha, wealth, stability, beauty"),
    ("general", "special", "gemini_nature", {}, "favorable", "moderate", ['intelligence_education'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.12", "Gemini: Dual/air/male, ruled by Mercury, arms of Kalapurusha, communication, duality"),
    ("general", "special", "cancer_nature", {}, "favorable", "moderate", ['mental_health'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.13", "Cancer: Movable/water/female, ruled by Moon, chest of Kalapurusha, nurturing, emotional"),
    ("general", "special", "leo_nature", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.14", "Leo: Fixed/fire/male, ruled by Sun, stomach of Kalapurusha, authority, royalty, power"),
    ("general", "special", "virgo_nature", {}, "favorable", "moderate", ['intelligence_education'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.15", "Virgo: Dual/earth/female, ruled by Mercury, waist of Kalapurusha, analysis, service, health"),
    ("general", "special", "libra_nature", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.16", "Libra: Movable/air/male, ruled by Venus, lower abdomen of Kalapurusha, balance, partnership"),
    ("general", "special", "scorpio_nature", {}, "mixed", "moderate", ['spirituality'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.17", "Scorpio: Fixed/water/female, ruled by Mars, genitals of Kalapurusha, transformation, occult"),
    ("general", "special", "sagittarius_nature", {}, "favorable", "moderate", ['spirituality'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.18", "Sagittarius: Dual/fire/male, ruled by Jupiter, thighs of Kalapurusha, dharma, philosophy"),
    ("general", "special", "capricorn_nature", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.19", "Capricorn: Movable/earth/female, ruled by Saturn, knees of Kalapurusha, ambition, structure"),
    ("general", "special", "aquarius_nature", {}, "mixed", "moderate", ['career_status'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.20", "Aquarius: Fixed/air/male, ruled by Saturn, calves of Kalapurusha, innovation, humanitarianism"),
    ("general", "special", "pisces_nature", {}, "favorable", "moderate", ['spirituality'], ['saravali', 'special', 'sign_natures'], "Ch.1-5 v.21", "Pisces: Dual/water/female, ruled by Jupiter, feet of Kalapurusha, compassion, liberation"),
]

_HOUSE_SIGNIFICATIONS_DATA = [
    ("general", "special", "house_1_sig", {}, "favorable", "moderate", ['physical_appearance', 'character_temperament'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.22", "1st House (Tanu Bhava): body, self, personality, vitality, head, birth circumstances"),
    ("general", "special", "house_2_sig", {}, "favorable", "moderate", ['wealth', 'intelligence_education'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.23", "2nd House (Dhana Bhava): wealth, speech, family, right eye, food, face, early education"),
    ("general", "special", "house_3_sig", {}, "favorable", "moderate", ['character_temperament'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.24", "3rd House (Sahaja Bhava): courage, siblings, short travel, communication, arms, hobbies"),
    ("general", "special", "house_4_sig", {}, "favorable", "moderate", ['property_vehicles', 'mental_health'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.25", "4th House (Sukha Bhava): happiness, mother, property, vehicles, heart, education, peace"),
    ("general", "special", "house_5_sig", {}, "favorable", "moderate", ['intelligence_education', 'progeny'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.26", "5th House (Putra Bhava): children, intellect, past merit, speculation, romance, mantras"),
    ("general", "special", "house_6_sig", {}, "mixed", "moderate", ['enemies_litigation', 'physical_health'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.27", "6th House (Ripu Bhava): enemies, disease, service, debts, competition, maternal uncle"),
    ("general", "special", "house_7_sig", {}, "favorable", "moderate", ['marriage'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.28", "7th House (Kalatra Bhava): spouse, marriage, partnerships, business, foreign travel, death"),
    ("general", "special", "house_8_sig", {}, "mixed", "moderate", ['longevity'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.29", "8th House (Randhra Bhava): longevity, death, transformation, occult, inheritance, chronic disease"),
    ("general", "special", "house_9_sig", {}, "favorable", "moderate", ['spirituality', 'wealth'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.30", "9th House (Dharma Bhava): fortune, father, dharma, guru, pilgrimage, higher education"),
    ("general", "special", "house_10_sig", {}, "favorable", "moderate", ['career_status', 'fame_reputation'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.31", "10th House (Karma Bhava): career, fame, authority, government, profession, public life"),
    ("general", "special", "house_11_sig", {}, "favorable", "moderate", ['wealth'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.32", "11th House (Labha Bhava): gains, aspirations, elder siblings, friends, networks, income"),
    ("general", "special", "house_12_sig", {}, "mixed", "moderate", ['spirituality', 'foreign_travel'], ['saravali', 'special', 'house_significations'], "Ch.1-5 v.33", "12th House (Vyaya Bhava): losses, expenditure, liberation, foreign land, confinement, feet"),
]

_PLANETARY_FRIENDSHIPS_DATA = [
    ("sun", "special", "sun_friends", {}, "favorable", "moderate", ['career_status'], ['sun', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.34", "Sun friends: Moon, Mars, Jupiter; enemies: Venus, Saturn; neutral: Mercury"),
    ("moon", "special", "moon_friends", {}, "favorable", "moderate", ['mental_health'], ['moon', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.35", "Moon friends: Sun, Mercury; enemies: none; neutral: Mars, Jupiter, Venus, Saturn"),
    ("mars", "special", "mars_friends", {}, "favorable", "moderate", ['career_status'], ['mars', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.36", "Mars friends: Sun, Moon, Jupiter; enemies: Mercury; neutral: Venus, Saturn"),
    ("mercury", "special", "mercury_friends", {}, "favorable", "moderate", ['intelligence_education'], ['mercury', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.37", "Mercury friends: Sun, Venus; enemies: Moon; neutral: Mars, Jupiter, Saturn"),
    ("jupiter", "special", "jupiter_friends", {}, "favorable", "moderate", ['spirituality'], ['jupiter', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.38", "Jupiter friends: Sun, Moon, Mars; enemies: Mercury, Venus; neutral: Saturn"),
    ("venus", "special", "venus_friends", {}, "favorable", "moderate", ['marriage'], ['venus', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.39", "Venus friends: Mercury, Saturn; enemies: Sun, Moon; neutral: Mars, Jupiter"),
    ("saturn", "special", "saturn_friends", {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'special', 'planetary_friendships'], "Ch.1-5 v.40", "Saturn friends: Mercury, Venus; enemies: Sun, Moon, Mars; neutral: Jupiter"),
]

_DIGNITY_SYSTEM_DATA = [
    ("general", "special", "exaltation_system", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'dignity_system'], "Ch.1-5 v.41", "Exaltation degrees: Sun 10°Aries, Moon 3°Taurus, Mars 28°Capricorn, Mercury 15°Virgo, Jupiter 5°Cancer, Venus 27°Pisces, Saturn 20°Libra"),
    ("general", "special", "debilitation_system", {}, "unfavorable", "strong", ['career_status'], ['saravali', 'special', 'dignity_system'], "Ch.1-5 v.42", "Debilitation: exactly opposite exaltation signs — Sun Libra, Moon Scorpio, Mars Cancer, Mercury Pisces, Jupiter Capricorn, Venus Virgo, Saturn Aries"),
    ("general", "special", "moolatrikona_system", {}, "favorable", "strong", ['career_status'], ['saravali', 'special', 'dignity_system'], "Ch.1-5 v.43", "Moolatrikona: Sun 0-20°Leo, Moon 3-30°Taurus, Mars 0-12°Aries, Mercury 15-20°Virgo, Jupiter 0-10°Sagittarius, Venus 0-15°Libra, Saturn 0-20°Aquarius"),
    ("general", "special", "own_sign_system", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'dignity_system'], "Ch.1-5 v.44", "Own sign: planet in its ruled sign — full strength expression without exaltation intensity"),
    ("general", "special", "neecha_bhanga", {}, "favorable", "moderate", ['career_status'], ['saravali', 'special', 'dignity_system'], "Ch.1-5 v.45", "Neecha Bhanga Raja Yoga: debilitation cancelled by specific conditions — produces rise after fall"),
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
            rule_id=rid, source="Saravali", chapter="Ch.1-5", school="parashari",
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
        (_PLANET_NATURES_DATA, 2629),
        (_SIGN_NATURES_DATA, 2638),
        (_HOUSE_SIGNIFICATIONS_DATA, 2650),
        (_PLANETARY_FRIENDSHIPS_DATA, 2662),
        (_DIGNITY_SYSTEM_DATA, 2669),
    ]
    result: list[RuleRecord] = []
    for data, s in all_data:
        result.extend(_make_rules(data, s))
    return result


SARAVALI_SPECIAL_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SPECIAL_1_REGISTRY.add(_rule)
