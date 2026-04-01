"""
src/corpus/shadbala_rules.py — Shadbala Rules (S245)

Encodes the Shadbala system — the classical six-fold planetary strength
calculation from BPHS Ch.27-38. Shadbala provides a quantitative measure
of each planet's total strength in the natal chart.

Sources:
  BPHS Ch.27-38 — Shadbala Adhyaya (Parashara)
  Brihat Jataka Ch.1 — Planetary Nature and Strength (Varahamihira)
  Sarvartha Chintamani Ch.2 — Planet Strengths

30 rules total: SDB001-SDB030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

SHADBALA_RULES_REGISTRY = CorpusRegistry()

_SHADBALA_RULES = [
    # --- Overview and Structure (SDB001-003) ---
    RuleRecord(
        rule_id="SDB001",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="shadbala",
        description=(
            "Shadbala overview: Six sources of planetary strength: "
            "(1) Sthana Bala (positional strength), (2) Dig Bala (directional strength), "
            "(3) Kala Bala (temporal strength), (4) Chesta Bala (motional strength), "
            "(5) Naisargika Bala (natural strength), (6) Drik Bala (aspectual strength). "
            "Total Shadbala in Rupas determines planetary power to give results."
        ),
        confidence=0.95,
        verse="BPHS Ch.27 v.1-8",
        tags=["shadbala", "6_strengths", "sthana_dig_kala_chesta_naisargika_drik", "rupas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB002",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="shadbala",
        description=(
            "Shadbala minimum thresholds (Ishta Shadbala): Minimum required Shadbala "
            "for a planet to fully give its results: "
            "Sun 390 Shashtiamsas; Moon 360; Mars 300; Mercury 420; "
            "Jupiter 390; Venus 330; Saturn 300. "
            "Below minimum = planet is weak and cannot fully manifest its significations."
        ),
        confidence=0.93,
        verse="BPHS Ch.27 v.9-18",
        tags=["shadbala", "minimum_threshold", "ishta_shadbala", "rupas_requirement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB003",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="shadbala",
        description=(
            "Bhava Bala: House strength calculated from Shadbala of house lord + "
            "planets in the house + aspects received. "
            "Bhava with strong lord and occupied/aspected by benefics = strong house. "
            "Bhava Bala used to determine which houses deliver results most clearly."
        ),
        confidence=0.90,
        verse="BPHS Ch.27 v.19-28",
        tags=["shadbala", "bhava_bala", "house_strength", "lord_strength"],
        implemented=False,
    ),
    # --- Sthana Bala (Positional Strength) (SDB004-008) ---
    RuleRecord(
        rule_id="SDB004",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="shadbala",
        description=(
            "Uchcha Bala (exaltation strength): Maximum 60 Shashtiamsas when planet is at "
            "exact exaltation degree; minimum 0 at exact debilitation degree. "
            "Intermediate values: 60 × (distance from debilitation / 180). "
            "Sun: max at 10° Aries; Moon: max at 3° Taurus; Mars: max at 28° Capricorn."
        ),
        confidence=0.93,
        verse="BPHS Ch.28 v.1-10",
        tags=["shadbala", "sthana_bala", "uchcha_bala", "exaltation_strength", "60_max"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB005",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="shadbala",
        description=(
            "Sapta-Vargaja Bala (divisional dignity strength): Based on planet's dignity "
            "in 7 vargas (D1, D2, D3, D7, D9, D12, D30). "
            "Moolatrikona = 45; Own sign = 30; Great friend's sign = 22.5; "
            "Friend's sign = 15; Neutral = 7.5; Enemy = 3.75; Great enemy = 1.875."
        ),
        confidence=0.90,
        verse="BPHS Ch.28 v.11-22",
        tags=["shadbala", "sthana_bala", "sapta_vargaja", "divisional_dignity", "7_vargas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB006",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="shadbala",
        description=(
            "Ojayugma Bala (odd/even sign strength): "
            "Sun, Mars, Jupiter, Saturn = stronger in odd signs (Aries, Gemini, Leo...); "
            "Moon, Venus = stronger in even signs (Taurus, Cancer, Virgo...). "
            "Mercury = equally strong in both. Strength = 15 Shashtiamsas in favorable signs."
        ),
        confidence=0.88,
        verse="BPHS Ch.28 v.23-28",
        tags=["shadbala", "sthana_bala", "ojayugma", "odd_even_sign", "15_shasht"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB007",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="shadbala",
        description=(
            "Kendradi Bala (quadrant strength): "
            "Planet in Kendra (1, 4, 7, 10) = 60 Shashtiamsas; "
            "in Panapara (2, 5, 8, 11) = 30; in Apoklima (3, 6, 9, 12) = 15. "
            "Planets in Kendra have maximum positional power to influence the chart."
        ),
        confidence=0.90,
        verse="BPHS Ch.28 v.29-34",
        tags=["shadbala", "sthana_bala", "kendradi_bala", "kendra_60", "apoklima_15"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB008",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="shadbala",
        description=(
            "Drekkana Bala: Male planets (Sun, Jupiter, Mars) = strong in 1st Drekkana (0-10°). "
            "Neutral planets (Mercury, Saturn) = strong in 2nd Drekkana (10-20°). "
            "Female planets (Moon, Venus) = strong in 3rd Drekkana (20-30°). "
            "Strength = 15 Shashtiamsas in appropriate Drekkana."
        ),
        confidence=0.87,
        verse="BPHS Ch.28 v.35-40",
        tags=["shadbala", "sthana_bala", "drekkana_bala", "gender_drekkana"],
        implemented=False,
    ),
    # --- Dig Bala (Directional Strength) (SDB009) ---
    RuleRecord(
        rule_id="SDB009",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="shadbala",
        description=(
            "Dig Bala (directional strength): Maximum 60 Shashtiamsas when planet is in "
            "its strongest direction/house. "
            "Jupiter, Mercury: strongest in Lagna (1st house, East). "
            "Sun, Mars: strongest in 10th house (South). "
            "Moon, Venus: strongest in 4th (North). Saturn: strongest in 7th (West). "
            "0 at opposite direction; proportional in between."
        ),
        confidence=0.92,
        verse="BPHS Ch.29 v.1-10",
        tags=["shadbala", "dig_bala", "directional_strength", "1st_10th_4th_7th"],
        implemented=False,
    ),
    # --- Kala Bala (Temporal Strength) (SDB010-015) ---
    RuleRecord(
        rule_id="SDB010",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="shadbala",
        description=(
            "Nathonnatha Bala (day/night strength): "
            "Day births: Sun, Jupiter, Venus are stronger (60 Shashtiamsas). "
            "Night births: Moon, Mars, Saturn are stronger. "
            "Mercury is equally strong day and night. "
            "Strength = 60 for the appropriate time; 0 for inappropriate; "
            "intermediate based on sun's distance from horizon."
        ),
        confidence=0.90,
        verse="BPHS Ch.30 v.1-8",
        tags=["shadbala", "kala_bala", "nathonnatha", "day_night_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB011",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="shadbala",
        description=(
            "Paksha Bala (lunar phase strength): "
            "Benefics (Moon, Mercury, Jupiter, Venus) = stronger in Shukla Paksha (waxing Moon). "
            "Malefics (Sun, Mars, Saturn) = stronger in Krishna Paksha (waning Moon). "
            "Maximum 60 Shashtiamsas at Full Moon for benefics; "
            "maximum at New Moon for malefics; proportional otherwise."
        ),
        confidence=0.90,
        verse="BPHS Ch.30 v.9-16",
        tags=["shadbala", "kala_bala", "paksha_bala", "shukla_krishna_paksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB012",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="shadbala",
        description=(
            "Tribhaga Bala (tri-section temporal strength): "
            "Day is divided into 3 parts; night into 3 parts. "
            "1st part of day: Mercury strong. 2nd part: Sun strong. 3rd part: Saturn strong. "
            "1st part of night: Moon strong. 2nd part: Venus strong. 3rd part: Mars strong. "
            "Jupiter is always strong. Strength = 60 in strong time; 0 otherwise."
        ),
        confidence=0.87,
        verse="BPHS Ch.30 v.17-24",
        tags=["shadbala", "kala_bala", "tribhaga_bala", "day_night_thirds"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB013",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="shadbala",
        description=(
            "Varsha/Masa/Vara/Hora Bala (year/month/day/hour lords): "
            "The lord of the current year, month, weekday, and hora receives +15 each. "
            "Planet that is Varsha lord (Solar year lord) = +15 Shashtiamsas. "
            "Vara lord (weekday lord) = +45 extra strength for that planet."
        ),
        confidence=0.85,
        verse="BPHS Ch.30 v.25-36",
        tags=["shadbala", "kala_bala", "vara_bala", "hora_bala", "temporal_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB014",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="shadbala",
        description=(
            "Ayana Bala (solstice strength): "
            "Sun, Mars, Jupiter, Venus: stronger in Uttarayana (Sun moving north, Jan-Jun). "
            "Moon, Saturn: stronger in Dakshinayana (Sun moving south, Jul-Dec). "
            "Mercury: always strong. Maximum 60 Shashtiamsas; varies by Sun's declination."
        ),
        confidence=0.87,
        verse="BPHS Ch.31 v.1-10",
        tags=["shadbala", "kala_bala", "ayana_bala", "uttarayana_dakshinayana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB015",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="shadbala",
        description=(
            "Yuddha Bala (war strength): When two planets are within 1° of each other "
            "(Graha Yuddha / planetary war), the planet with higher latitude wins. "
            "Winner gains +strength; loser loses strength. "
            "Exception: Sun and Moon are never in war with each other."
        ),
        confidence=0.85,
        verse="BPHS Ch.31 v.11-18",
        tags=["shadbala", "kala_bala", "yuddha_bala", "graha_yuddha", "planetary_war"],
        implemented=False,
    ),
    # --- Chesta Bala (Motional Strength) (SDB016-018) ---
    RuleRecord(
        rule_id="SDB016",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="shadbala",
        description=(
            "Chesta Bala overview (motional strength): "
            "Sun and Moon: Chesta Bala = Ayana Bala (not separate). "
            "Other planets: strength based on motion type. "
            "Vakra (retrograde) = 60; Anuvakra (just turning retrograde) = 30; "
            "Vikala (stationary) = 15; Sama (average speed) = 7.5; "
            "Mandatara (slower than average) = 45; Manda (slower) = 30; "
            "Sighra (fast) = 45."
        ),
        confidence=0.88,
        verse="BPHS Ch.32 v.1-12",
        tags=["shadbala", "chesta_bala", "motional_strength", "retrograde_60"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB017",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="shadbala",
        description=(
            "Retrograde planet strength: Retrograde (Vakra) planets receive maximum "
            "Chesta Bala (60 Shashtiamsas). A retrograde planet is doubly powerful — "
            "it intensifies its significations and creates karmic importance. "
            "Retrograde planet in exaltation = one of the highest possible strengths."
        ),
        confidence=0.90,
        verse="BPHS Ch.32 v.13-18",
        tags=["shadbala", "chesta_bala", "retrograde", "vakra", "maximum_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB018",
        source="Brihat Jataka",
        chapter="Ch.1",
        school="varahamihira",
        category="shadbala",
        description=(
            "Varahamihira on planet speed: A planet moving faster than its mean motion "
            "delivers results quickly in its Dasha period. "
            "A planet moving slower = delays results but gives them more persistently. "
            "Retrograde planet = revisiting karma; direct = fresh karma being created."
        ),
        confidence=0.85,
        verse="BJ Ch.1 v.8-14",
        tags=["shadbala", "chesta_bala", "planet_speed", "dasha_timing", "varahamihira"],
        implemented=False,
    ),
    # --- Naisargika Bala (Natural Strength) (SDB019) ---
    RuleRecord(
        rule_id="SDB019",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="shadbala",
        description=(
            "Naisargika Bala (natural/inherent strength): Fixed strength values "
            "regardless of chart position: "
            "Sun = 60; Moon = 51.43; Venus = 42.85; Jupiter = 34.28; "
            "Mercury = 25.71; Mars = 17.14; Saturn = 8.57 Shashtiamsas. "
            "Sun is inherently strongest; Saturn inherently weakest."
        ),
        confidence=0.93,
        verse="BPHS Ch.33 v.1-6",
        tags=["shadbala", "naisargika_bala", "natural_strength", "fixed_values", "sun_60_saturn_8"],
        implemented=False,
    ),
    # --- Drik Bala (Aspectual Strength) (SDB020-021) ---
    RuleRecord(
        rule_id="SDB020",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="shadbala",
        description=(
            "Drik Bala (aspectual strength): Strength gained/lost from aspects received. "
            "Full aspect from benefic (Jupiter, Mercury, Venus, waxing Moon) = +60. "
            "Full aspect from malefic (Sun, Mars, Saturn, waning Moon, Rahu/Ketu) = -60. "
            "Partial aspects: proportional to aspect strength percentage."
        ),
        confidence=0.88,
        verse="BPHS Ch.34 v.1-10",
        tags=["shadbala", "drik_bala", "aspectual_strength", "benefic_malefic_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB021",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="shadbala",
        description=(
            "Drik Bala calculation: Full aspect = 60 × (aspect percentage / 100). "
            "Jupiter's 5th/9th aspect = 50% strength; Mars/Saturn special aspects = 75%; "
            "Full 7th aspect = 100%. Drik Bala can be negative if malefic aspects dominate. "
            "Planet with strongly negative Drik Bala = afflicted despite other strengths."
        ),
        confidence=0.86,
        verse="BPHS Ch.34 v.11-20",
        tags=["shadbala", "drik_bala", "aspect_percentage", "negative_drik"],
        implemented=False,
    ),
    # --- Ishta/Kashta Phala (SDB022-023) ---
    RuleRecord(
        rule_id="SDB022",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="shadbala",
        description=(
            "Ishta Phala (desired results): Derived from Uchcha Bala × Chesta Bala / 60. "
            "Indicates how much good result a planet will produce. "
            "High Ishta Phala + high Shadbala = planet fully delivers positive significations. "
            "Used to rank planets by their ability to give auspicious results."
        ),
        confidence=0.87,
        verse="BPHS Ch.35 v.1-8",
        tags=["shadbala", "ishta_phala", "desired_results", "uchcha_chesta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB023",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="shadbala",
        description=(
            "Kashta Phala (undesired results): Derived from Neecha Bala × Chesta Bala / 60. "
            "Neecha Bala = (60 - Uchcha Bala). Indicates negative/difficult results. "
            "High Kashta Phala = planet gives suffering in its significations. "
            "Ratio Ishta:Kashta reveals overall planetary benevolence."
        ),
        confidence=0.86,
        verse="BPHS Ch.35 v.9-16",
        tags=["shadbala", "kashta_phala", "undesired_results", "neecha_bala"],
        implemented=False,
    ),
    # --- Vimshopaka Bala (SDB024-025) ---
    RuleRecord(
        rule_id="SDB024",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="shadbala",
        description=(
            "Vimshopaka Bala (20-point system): Alternative strength calculation based on "
            "dignity in D1, D2, D3, D9, D12 (5-Varga system) or extended Varga sets. "
            "Maximum 20 points. Planet in Swakshetra/Moolatrikona in all 5 vargas = 20/20. "
            "Vimshopaka 15+ = very strong; 10-15 = moderate; below 10 = weak."
        ),
        confidence=0.88,
        verse="BPHS Ch.36 v.1-12",
        tags=["shadbala", "vimshopaka_bala", "20_point", "5_varga", "dignity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB025",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="shadbala",
        description=(
            "Extended Vimshopaka (7 and 10-Varga systems): "
            "7-Varga: D1, D2, D3, D7, D9, D12, D30 — each weighted differently. "
            "10-Varga: adds D16, D24, D60 to 7-varga set. "
            "D60 carries most weight in 10-Varga (4.5 pts). "
            "A planet strong in D60 has accumulated merit from past lives."
        ),
        confidence=0.85,
        verse="BPHS Ch.36 v.13-24",
        tags=["shadbala", "vimshopaka_bala", "7_varga", "10_varga", "d60_past_life"],
        implemented=False,
    ),
    # --- Applications and Interpretation (SDB026-030) ---
    RuleRecord(
        rule_id="SDB026",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="shadbala",
        description=(
            "Shadbala for Dasha predictions: During a planet's Mahadasha, it delivers "
            "results proportional to its Shadbala strength. "
            "Planet with 500+ Shashtiamsas = full results in Mahadasha. "
            "Planet with only 200 = weak Dasha, results delayed or incomplete. "
            "Dasha of strongest Shadbala planet = best life period."
        ),
        confidence=0.88,
        verse="BPHS Ch.37 v.1-10",
        tags=["shadbala", "dasha_prediction", "500_full", "200_weak", "best_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB027",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="shadbala",
        description=(
            "Bala Ratios for chart analysis: "
            "Dominant planet (Atma Karaka by Shadbala) = the planet with highest total. "
            "If Lagna lord is also strongest in Shadbala = excellent life force. "
            "If Sun is strongest = leadership and authority. "
            "If Moon is strongest = emotional intelligence, public favor."
        ),
        confidence=0.86,
        verse="BPHS Ch.37 v.11-20",
        tags=["shadbala", "dominant_planet", "lagna_lord_strongest", "sun_moon_dominant"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB028",
        source="SarvarthaChintamani",
        chapter="Ch.2",
        school="sarvartha",
        category="shadbala",
        description=(
            "Sarvartha Chintamani on strength hierarchy: A planet strong in Shadbala "
            "but in enemy's sign still gives good results due to overall strength. "
            "A planet in exaltation but with low Kala/Chesta Bala = inconsistent results. "
            "Total Shadbala is the deciding factor when individual components conflict."
        ),
        confidence=0.84,
        verse="SC Ch.2 v.1-8",
        tags=["shadbala", "strength_hierarchy", "total_deciding", "exaltation_vs_kala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB029",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="shadbala",
        description=(
            "Shadbala for yogas: A yoga operates through its most Shadbala-strong component. "
            "Raj yoga with weak participants = yoga present but results diluted. "
            "Raj yoga where all yogakarakas have 400+ Shashtiamsas = fully activated yoga. "
            "Shadbala strength of yoga planets amplifies or dampens yoga results."
        ),
        confidence=0.87,
        verse="BPHS Ch.38 v.1-10",
        tags=["shadbala", "yoga_activation", "raja_yoga_strength", "400_activated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SDB030",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="shadbala",
        description=(
            "Relative Shadbala (Bal Ratio): Ratio of a planet's Shadbala to the "
            "minimum required (Ishta Shadbala threshold). "
            "Ratio 1.0+ = planet meets minimum standard. "
            "Ratio 1.5+ = strong planet. Ratio 2.0+ = exceptionally strong. "
            "Ratio below 0.5 = very weak planet, needs astrological remedies."
        ),
        confidence=0.87,
        verse="BPHS Ch.38 v.11-20",
        tags=["shadbala", "bal_ratio", "relative_strength", "1_5_strong", "remedies"],
        implemented=False,
    ),
]

for rule in _SHADBALA_RULES:
    SHADBALA_RULES_REGISTRY.add(rule)
