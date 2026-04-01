"""
src/corpus/phala_deepika_ext.py — Phala Deepika Extended Rules (S239)

Encodes Mantreswara's Phala Deepika (13th century CE) extended rules
on planetary results in houses, special yogas, and unique interpretations.

Sources:
  Phala Deepika (Mantreswara) — Chapters 5, 6, 8, 13, 14, 20
  Gopesh Kumar Ojha translation
  Surya Prakash commentary

30 rules total: PDE001-PDE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

PHALA_DEEPIKA_EXT_REGISTRY = CorpusRegistry()

_PHALA_DEEPIKA_EXT = [
    # --- Planets in Houses (Phala Deepika approach) (PDE001-012) ---
    RuleRecord(
        rule_id="PDE001",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Sun in 1st house: Strong constitution, leadership quality, proud nature. "
            "Phala Deepika adds: Sun in lagna gives eye problems (bilious constitution), "
            "tendency to baldness, and strong individuality. Father is influential."
        ),
        confidence=0.87,
        verse="PD Ch.5 v.1-3",
        tags=["sun_in_house", "1st_house", "leadership", "eye_problems", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE002",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Moon in 1st house: Attractive, imaginative, emotional, fond of travel. "
            "Phala Deepika: Moon in lagna gives beautiful eyes, corpulent body, "
            "love of pleasures, devoted to mother. Strong mental faculties."
        ),
        confidence=0.87,
        verse="PD Ch.5 v.4-6",
        tags=["moon_in_house", "1st_house", "attractive", "emotional", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE003",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Mars in 1st house: Athletic, courageous, impulsive, prone to accidents. "
            "Phala Deepika specifically: Mars in lagna causes wounds/scars on head or face. "
            "Courageous but impetuous; may have difficult relationship with brother."
        ),
        confidence=0.87,
        verse="PD Ch.5 v.7-9",
        tags=["mars_in_house", "1st_house", "athletic", "wounds", "impulsive", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE004",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Mercury in 1st house: Intelligent, communicative, scholarly, youthful appearance. "
            "Phala Deepika: Mercury in lagna gives wit and humor, mathematical ability, "
            "skill in arts, and business acumen. Tends toward slender physique."
        ),
        confidence=0.86,
        verse="PD Ch.5 v.10-12",
        tags=["mercury_in_house", "1st_house", "intelligent", "scholarly", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE005",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Jupiter in 1st house: Wise, generous, stout physique, philosophical nature. "
            "Phala Deepika: Jupiter in lagna gives an affable personality, respect from scholars, "
            "and a large body. Good for spiritual study and counseling professions."
        ),
        confidence=0.87,
        verse="PD Ch.5 v.13-15",
        tags=["jupiter_in_house", "1st_house", "wise", "generous", "philosophical", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE006",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Venus in 1st house: Beautiful, charming, passionate, fond of luxury. "
            "Phala Deepika: Venus in lagna gives bright eyes, elegant appearance, "
            "fondness for fine arts. Sensually active; popular with opposite sex."
        ),
        confidence=0.87,
        verse="PD Ch.5 v.16-18",
        tags=["venus_in_house", "1st_house", "beautiful", "charming", "luxury", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE007",
        source="Phaladeepika",
        chapter="Ch.5",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Saturn in 1st house: Lean physique, melancholic temperament, endurance, hardship early life. "
            "Phala Deepika: Saturn in lagna causes delayed success, difficulties in early years, "
            "tendency to solitude. Achieves through discipline and perseverance."
        ),
        confidence=0.86,
        verse="PD Ch.5 v.19-21",
        tags=["saturn_in_house", "1st_house", "lean", "melancholic", "endurance", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE008",
        source="Phaladeepika",
        chapter="Ch.6",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Sun in 7th house: Delayed marriage or difficulty in marital happiness. "
            "Phala Deepika: Sun in 7th gives domineering spouse, eye trouble, wandering nature. "
            "Government service or public career influences marriage timing."
        ),
        confidence=0.85,
        verse="PD Ch.6 v.1-3",
        tags=["sun_in_house", "7th_house", "delayed_marriage", "domineering_spouse", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE009",
        source="Phaladeepika",
        chapter="Ch.6",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Venus in 7th house: Beautiful spouse, multiple relationships possible. "
            "Phala Deepika: Venus in 7th gives a charming, artistic partner. "
            "May lead to over-indulgence in sensual pleasures; generally positive for marriage."
        ),
        confidence=0.86,
        verse="PD Ch.6 v.4-6",
        tags=["venus_in_house", "7th_house", "beautiful_spouse", "sensual", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE010",
        source="Phaladeepika",
        chapter="Ch.6",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Saturn in 7th house: Late marriage, cold or serious spouse, karmic relationship. "
            "Phala Deepika: Saturn in 7th delays marriage; spouse may be older or serious. "
            "Stability through commitment once marriage happens."
        ),
        confidence=0.85,
        verse="PD Ch.6 v.7-9",
        tags=["saturn_in_house", "7th_house", "late_marriage", "serious_spouse", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE011",
        source="Phaladeepika",
        chapter="Ch.6",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Jupiter in 10th house: Virtuous, respected, successful in profession, religious inclination. "
            "Phala Deepika: Jupiter in 10th gives fame, authority, religious work. "
            "Career in education, law, or spiritual service strongly favored."
        ),
        confidence=0.88,
        verse="PD Ch.6 v.10-12",
        tags=["jupiter_in_house", "10th_house", "respected", "religious", "career", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE012",
        source="Phaladeepika",
        chapter="Ch.6",
        school="mantreswara",
        category="graha_in_bhava",
        description=(
            "Moon in 4th house: Domestic happiness, devoted to mother, abundant home life. "
            "Phala Deepika: Moon in 4th (its kendra + exaltation zone in Cancer/Taurus) "
            "gives exceptional domestic peace and maternal blessings."
        ),
        confidence=0.88,
        verse="PD Ch.6 v.13-15",
        tags=["moon_in_house", "4th_house", "domestic_happiness", "mother", "mantreswara"],
        implemented=False,
    ),
    # --- Phala Deepika Special Yogas (PDE013-022) ---
    RuleRecord(
        rule_id="PDE013",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Pancha Mahapurusha Yoga details: "
            "Only when the ruling planet is exalted or own-sign AND in kendra. "
            "In addition, Ruchaka (Mars) gives warrior nature, fearlessness, "
            "red complexion, mark on body from weapon."
        ),
        confidence=0.88,
        verse="PD Ch.8 v.1-5",
        tags=["yoga", "pancha_mahapurusha", "ruchaka", "mars", "warrior", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE014",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Bhadra Yoga (Mercury exalt/own in kendra): Phala Deepika specifies "
            "lotus-marked hands, eloquent speech, sharp intellect, long-lived, "
            "earning through intellect and writing. Distinguished appearance."
        ),
        confidence=0.87,
        verse="PD Ch.8 v.6-8",
        tags=["yoga", "bhadra_yoga", "mercury", "eloquence", "intellect", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE015",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Hamsa Yoga (Jupiter exalt/own in kendra): Phala Deepika specifies "
            "handsome, virtuous, honored by kings, fair complexion, beautiful nose, "
            "loves music and water, well-versed in shastras."
        ),
        confidence=0.88,
        verse="PD Ch.8 v.9-11",
        tags=["yoga", "hamsa_yoga", "jupiter", "virtuous", "honored", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE016",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Malavya Yoga (Venus exalt/own in kendra): Phala Deepika specifies "
            "beautiful form, charming eyes, sweet fragrance, learned in arts, "
            "wealthy, long-lived, successful in creative pursuits."
        ),
        confidence=0.87,
        verse="PD Ch.8 v.12-14",
        tags=["yoga", "malavya_yoga", "venus", "beautiful", "wealthy", "arts", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE017",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Shasha Yoga (Saturn exalt/own in kendra): Phala Deepika specifies "
            "commanding, fond of forests and mountains, leader of servile class, "
            "skilled in labor management, strong lower body."
        ),
        confidence=0.86,
        verse="PD Ch.8 v.15-17",
        tags=["yoga", "shasha_yoga", "saturn", "commanding", "laborer", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE018",
        source="Phaladeepika",
        chapter="Ch.8",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Gajakesari Yoga refinement: Jupiter must be in kendra "
            "from BOTH Moon AND lagna for full effect. If only from Moon, partial results. "
            "The yoga gives oratorical ability, fame, strong memory, and longevity."
        ),
        confidence=0.87,
        verse="PD Ch.8 v.18-20",
        tags=["yoga", "gajakesari", "jupiter_moon_kendra", "refined_condition", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE019",
        source="Phaladeepika",
        chapter="Ch.13",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Adhi Yoga: When benefics (Jupiter, Venus, Mercury) "
            "are in 6th, 7th, and 8th from Moon in various combinations. "
            "All three: minister or king. Two: commander or wealthy. One: person of means."
        ),
        confidence=0.86,
        verse="PD Ch.13 v.1-5",
        tags=["yoga", "adhi_yoga", "6_7_8_from_moon", "benefics", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE020",
        source="Phaladeepika",
        chapter="Ch.13",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Kahala Yoga: 4th lord and its lord in mutual kendra, "
            "with lagna lord strong. Gives authoritative, bold nature, "
            "success as head of army or large organization."
        ),
        confidence=0.83,
        verse="PD Ch.13 v.6-8",
        tags=["yoga", "kahala_yoga", "4th_lord_kendra", "authority", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE021",
        source="Phaladeepika",
        chapter="Ch.13",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Chamara Yoga: Lagna lord exalted in kendra, aspected "
            "by Jupiter, or two or more benefics in kendra. "
            "Native becomes an eminent person, respected like royalty, long-lived."
        ),
        confidence=0.84,
        verse="PD Ch.13 v.9-11",
        tags=["yoga", "chamara_yoga", "lagna_lord_exalted", "benefics_kendra", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE022",
        source="Phaladeepika",
        chapter="Ch.13",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Musala Yoga: All planets in fixed signs (Taurus, Leo, Scorpio, Aquarius). "
            "Native is wealthy, steady in purpose, famous among people of his class, "
            "respected for firmness and consistency."
        ),
        confidence=0.83,
        verse="PD Ch.13 v.12-14",
        tags=["yoga", "musala_yoga", "fixed_signs", "wealthy", "steady", "mantreswara"],
        implemented=False,
    ),
    # --- Phala Deepika on Health and Disease (PDE023-026) ---
    RuleRecord(
        rule_id="PDE023",
        source="Phaladeepika",
        chapter="Ch.14",
        school="mantreswara",
        category="health",
        description=(
            "Phala Deepika medical astrology: Sun affliction → heart/eye disorders. "
            "Moon affliction → mental/blood disorders. Mars affliction → bile, blood, "
            "surgery risk. Mercury → skin/nervous disorders. Jupiter → liver/fat disorders."
        ),
        confidence=0.85,
        verse="PD Ch.14 v.1-5",
        tags=["health", "planetary_disease", "medical_astrology", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE024",
        source="Phaladeepika",
        chapter="Ch.14",
        school="mantreswara",
        category="health",
        description=(
            "Phala Deepika health continued: Venus affliction → venereal/reproductive disorders. "
            "Saturn affliction → chronic disease, joint/bone problems. "
            "Rahu → mysterious illness, poison. Ketu → spiritual/karmic illness."
        ),
        confidence=0.84,
        verse="PD Ch.14 v.6-10",
        tags=["health", "venus_disease", "saturn_chronic", "rahu_ketu_illness", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE025",
        source="Phaladeepika",
        chapter="Ch.14",
        school="mantreswara",
        category="health",
        description=(
            "6th house lord and disease: The sign occupied by 6th lord indicates "
            "the body part prone to disease. 6th lord in fire signs = fevers; "
            "water signs = water-related illness; earth = chronic conditions; air = vata disorders."
        ),
        confidence=0.84,
        verse="PD Ch.14 v.11-13",
        tags=["health", "6th_lord", "body_part", "element_disease", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE026",
        source="Phaladeepika",
        chapter="Ch.14",
        school="mantreswara",
        category="health",
        description=(
            "Phala Deepika on accidents: Mars-Saturn-Rahu combination in any house "
            "indicates risk of accidents, surgery, or violent events in their "
            "respective dasha periods, especially when Mars transits the natal position."
        ),
        confidence=0.83,
        verse="PD Ch.14 v.14-16",
        tags=["health", "accidents", "mars_saturn_rahu", "dasha_trigger", "mantreswara"],
        implemented=False,
    ),
    # --- Phala Deepika Miscellaneous Principles (PDE027-030) ---
    RuleRecord(
        rule_id="PDE027",
        source="Phaladeepika",
        chapter="Ch.20",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Rajayoga cancellation: If a rajayoga-forming planet "
            "is in the 6th, 8th, or 12th house, or is conjunct with the lord "
            "of those houses, the yoga is cancelled or severely weakened."
        ),
        confidence=0.88,
        verse="PD Ch.20 v.1-4",
        tags=["yoga_cancellation", "rajayoga", "6_8_12", "yoga_bhanga", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE028",
        source="Phaladeepika",
        chapter="Ch.20",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika: Benefits from yoga are experienced during the dasha "
            "of the yoga-forming planets. If the dasha has already passed before "
            "the yoga's effects can manifest, the yoga's fruits may not fully appear."
        ),
        confidence=0.85,
        verse="PD Ch.20 v.5-7",
        tags=["yoga_timing", "dasha_yoga", "yoga_fruits", "timing_principle", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE029",
        source="Phaladeepika",
        chapter="Ch.20",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Sarpa Yoga: All planets between Rahu and Ketu (hemmed in). "
            "Native faces struggles, bondage to past karma, difficulties with freedom. "
            "Can also indicate extreme focus/achievement in one direction."
        ),
        confidence=0.82,
        verse="PD Ch.20 v.8-10",
        tags=["yoga", "sarpa_yoga", "rahu_ketu_hemmed", "karma", "bondage", "mantreswara"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="PDE030",
        source="Phaladeepika",
        chapter="Ch.20",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika on Planetary War (Graha Yuddha): "
            "When two planets are within 1° of each other, the planet with "
            "lesser latitude loses the war. Winner gains full strength; loser "
            "loses significations in the chart."
        ),
        confidence=0.86,
        verse="PD Ch.20 v.11-14",
        tags=["graha_yuddha", "planetary_war", "1_degree", "winner_loser", "mantreswara"],
        implemented=False,
    ),
]

for _r in _PHALA_DEEPIKA_EXT:
    PHALA_DEEPIKA_EXT_REGISTRY.add(_r)
