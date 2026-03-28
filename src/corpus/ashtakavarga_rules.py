"""
src/corpus/ashtakavarga_rules.py — Ashtakavarga Rules (S243)

Encodes the Ashtakavarga system — the classical quantitative method for
assessing planetary strengths, transit quality, and life period analysis.

Sources:
  BPHS Ch.66-76 — Ashtakavarga Adhyaya (Parashara)
  Brihat Jataka Ch.19 — Ashtakavarga (Varahamihira)
  Sarvartha Chintamani Ch.10 — Transit + Ashtakavarga integration

30 rules total: AST001-AST030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

ASHTAKAVARGA_RULES_REGISTRY = CorpusRegistry()

_ASHTAKAVARGA_RULES = [
    # --- Fundamental Structure (AST001-005) ---
    RuleRecord(
        rule_id="AST001",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga fundamental: Each of the 7 visible planets (Sun through Saturn) "
            "and the Lagna contribute beneficial points (bindus) to each of the 12 houses. "
            "Total points for each house from all 8 contributors = Sarvashtakavarga score."
        ),
        confidence=0.95,
        verse="BPHS Ch.66 v.1-5",
        tags=["ashtakavarga", "fundamental", "8_contributors", "bindus", "sarvashtakavarga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST002",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Prasthara Ashtakavarga: Each planet has its own table showing which "
            "positions of other planets and lagna give it a benefic point (1) or "
            "no point (0). Maximum 8 points per sign in any planet's Prasthara table. "
            "Sun's Prasthara: 8 contributors × 12 signs = 96 cells."
        ),
        confidence=0.93,
        verse="BPHS Ch.66 v.6-12",
        tags=["ashtakavarga", "prasthara", "individual_table", "8_max_per_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST003",
        source="BPHS",
        chapter="Ch.67",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Sarvashtakavarga: Sum of all 7 planets' Prasthara tables gives the "
            "Sarvashtakavarga — total bindus for each sign. Maximum 56 per sign "
            "(7 planets × 8 max). Signs with 25+ bindus are generally strong; "
            "signs with 30+ are very strong for transit and natal purposes."
        ),
        confidence=0.92,
        verse="BPHS Ch.67 v.1-8",
        tags=["ashtakavarga", "sarvashtakavarga", "56_max", "25_plus_strong", "30_plus_very_strong"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST004",
        source="BPHS",
        chapter="Ch.68",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Trikona Shodhana (triangular reduction): From each planet's Prasthara "
            "table, subtract the minimum of the three trine signs (1-5-9, 2-6-10, 3-7-11, "
            "4-8-12) from all three. This removes common factors and reveals differential strength. "
            "Applied to all 8 Prasthara tables before Ekadhipatya Shodhana."
        ),
        confidence=0.90,
        verse="BPHS Ch.68 v.1-10",
        tags=["ashtakavarga", "trikona_shodhana", "reduction", "trine_minimum", "differential"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST005",
        source="BPHS",
        chapter="Ch.68",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ekadhipatya Shodhana (same-lord reduction): For signs ruled by the same planet "
            "(Mercury rules Gemini+Virgo; Venus rules Taurus+Libra; Saturn rules "
            "Capricorn+Aquarius), if both signs have points, subtract the lesser from the "
            "greater and assign 0 to the lesser. Applied after Trikona Shodhana."
        ),
        confidence=0.89,
        verse="BPHS Ch.68 v.11-18",
        tags=["ashtakavarga", "ekadhipatya_shodhana", "same_ruler", "mercury_venus_saturn"],
        implemented=False,
    ),
    # --- Sun Ashtakavarga (AST006) ---
    RuleRecord(
        rule_id="AST006",
        source="BPHS",
        chapter="Ch.69",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Sun's Ashtakavarga (Bhinnashtakavarga): Sun gives bindus from: "
            "Sun in 1,2,4,7,8,9,10,11; Moon in 3,6,10,11; Mars in 1,2,4,7,8,9,10,11; "
            "Mercury in 3,5,6,9,10,11,12; Jupiter in 5,6,9,11; "
            "Venus in 6,7,12; Saturn in 1,2,4,7,8,9,10,11; Lagna in 3,4,6,10,11,12."
        ),
        confidence=0.88,
        verse="BPHS Ch.69 v.1-8",
        tags=["ashtakavarga", "sun_bav", "sun_bindus", "bhinnashtakavarga"],
        implemented=False,
    ),
    # --- Moon Ashtakavarga (AST007) ---
    RuleRecord(
        rule_id="AST007",
        source="BPHS",
        chapter="Ch.70",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Moon's Ashtakavarga: Moon gives bindus from: "
            "Sun in 3,6,7,8,10,11; Moon in 1,3,6,7,10,11; Mars in 2,3,5,6,9,10,11; "
            "Mercury in 1,3,4,5,7,8,10,11; Jupiter in 1,4,7,8,10,11,12; "
            "Venus in 3,4,5,7,9,10,11; Saturn in 3,5,6,11; Lagna in 3,6,10,11."
        ),
        confidence=0.88,
        verse="BPHS Ch.70 v.1-8",
        tags=["ashtakavarga", "moon_bav", "moon_bindus", "bhinnashtakavarga"],
        implemented=False,
    ),
    # --- Mars, Mercury, Jupiter, Venus, Saturn BAV (AST008-012) ---
    RuleRecord(
        rule_id="AST008",
        source="BPHS",
        chapter="Ch.71",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Mars Ashtakavarga: Mars gives bindus from positions of all 8 contributors. "
            "Key benefic positions: 3, 5, 6, 10, 11 from Mars natal are generally good "
            "for transit. Mars BAV score of 5+ in a sign indicates good Mars transit results. "
            "Malefic positions: 1, 2, 4, 7, 8, 12."
        ),
        confidence=0.87,
        verse="BPHS Ch.71 v.1-8",
        tags=["ashtakavarga", "mars_bav", "mars_bindus", "5_plus_good"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST009",
        source="BPHS",
        chapter="Ch.72",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Mercury Ashtakavarga: Mercury gives bindus based on relative positions. "
            "Mercury BAV benefic positions: 1, 3, 5, 6, 9, 10, 11, 12 from natal Mercury. "
            "Mercury BAV 5+ bindus in transit sign = good communication, business, intellect. "
            "Mercury is the only planet that includes itself in its own BAV calculation."
        ),
        confidence=0.87,
        verse="BPHS Ch.72 v.1-8",
        tags=["ashtakavarga", "mercury_bav", "mercury_bindus", "self_included"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST010",
        source="BPHS",
        chapter="Ch.73",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Jupiter Ashtakavarga: Jupiter BAV benefic positions: 1, 2, 3, 4, 7, 8, 10, 11. "
            "Jupiter BAV 6+ bindus in transit sign = excellent wisdom, prosperity, and grace. "
            "Jupiter BAV total (all 12 signs) reveals dharmic strength of the chart. "
            "High Jupiter BAV total (45+) = blessed chart."
        ),
        confidence=0.88,
        verse="BPHS Ch.73 v.1-8",
        tags=["ashtakavarga", "jupiter_bav", "jupiter_bindus", "dharmic_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST011",
        source="BPHS",
        chapter="Ch.74",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Venus Ashtakavarga: Venus BAV benefic positions: 1, 2, 3, 4, 5, 8, 9, 10, 11. "
            "Venus BAV 6+ bindus in transit sign = pleasure, luxury, relationship happiness. "
            "Venus BAV total reveals overall happiness, wealth, and relationship potential. "
            "High Venus BAV (50+) = great comforts and pleasures in life."
        ),
        confidence=0.87,
        verse="BPHS Ch.74 v.1-8",
        tags=["ashtakavarga", "venus_bav", "venus_bindus", "relationship_happiness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST012",
        source="BPHS",
        chapter="Ch.75",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Saturn Ashtakavarga: Saturn BAV benefic positions: 3, 5, 6, 11. "
            "Saturn BAV 4+ bindus in transit sign = favorable Saturn transit. "
            "Saturn BAV 0-2 = very difficult Saturn transit; 3 = neutral; 4+ = good. "
            "Saturn BAV is key for Sade Sati assessment — low bindus worsen Sade Sati."
        ),
        confidence=0.90,
        verse="BPHS Ch.75 v.1-8",
        tags=["ashtakavarga", "saturn_bav", "saturn_bindus", "3_5_6_11_good", "sade_sati"],
        implemented=False,
    ),
    # --- Kakshya (Sub-lord) System (AST013-014) ---
    RuleRecord(
        rule_id="AST013",
        source="BPHS",
        chapter="Ch.76",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Kakshya divisions: Each sign (30°) is divided into 8 kakshyas of 3°45' each. "
            "Ruled in order by Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna. "
            "A transiting planet in a kakshya whose ruler contributed a bindu = good result; "
            "in kakshya of a non-contributing planet = poor result from that transit."
        ),
        confidence=0.87,
        verse="BPHS Ch.76 v.1-12",
        tags=["ashtakavarga", "kakshya", "3_45_minutes", "sub_divisions", "transit_timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST014",
        source="BPHS",
        chapter="Ch.76",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Kakshya transit timing: By identifying which kakshya a transiting planet "
            "occupies and whether that kakshya lord contributed a bindu, one can pinpoint "
            "the exact period within a month/year when a transit is most beneficial. "
            "Transit peak = planet in kakshya of a contributor with high BAV bindus."
        ),
        confidence=0.85,
        verse="BPHS Ch.76 v.13-20",
        tags=["ashtakavarga", "kakshya", "transit_timing", "peak_period", "contributor"],
        implemented=False,
    ),
    # --- Pinda (Score) Analysis (AST015-017) ---
    RuleRecord(
        rule_id="AST015",
        source="BPHS",
        chapter="Ch.67",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Pinda Saham (sum score): Total of all bindus in a planet's Bhinnashtakavarga "
            "table after Trikona + Ekadhipatya Shodhana. Pinda Saham indicates overall "
            "planetary strength. Sun Pinda 5+ = strong; below 4 = weak. "
            "Used to assess which planets are strongest in the chart."
        ),
        confidence=0.86,
        verse="BPHS Ch.67 v.9-15",
        tags=["ashtakavarga", "pinda_saham", "total_score", "planetary_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST016",
        source="Brihat_Jataka",
        chapter="Ch.19",
        school="varahamihira",
        category="ashtakavarga",
        description=(
            "Yoga Saham (yoga score): When multiple planets have high bindus in the same "
            "sign, it creates a Yoga Saham — concentrated life energy. Varahamihira states: "
            "3+ planets each with 5+ bindus in the same sign = powerful destiny cluster "
            "for matters of that sign's house from lagna."
        ),
        confidence=0.84,
        verse="BJ Ch.19 v.5-9",
        tags=["ashtakavarga", "yoga_saham", "destiny_cluster", "3_planets_5_bindus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST017",
        source="BPHS",
        chapter="Ch.67",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Rashi Pinda (sign totals): From the Sarvashtakavarga, the total bindus "
            "in each sign reveal the overall auspiciousness of that sign for life events. "
            "Rashi with highest bindu count = most productive sign for activity. "
            "Transit Jupiter or Dasha lord to high-bindu signs = peak results."
        ),
        confidence=0.87,
        verse="BPHS Ch.67 v.16-22",
        tags=["ashtakavarga", "rashi_pinda", "sign_total", "auspicious_signs"],
        implemented=False,
    ),
    # --- Transit Assessment with BAV (AST018-022) ---
    RuleRecord(
        rule_id="AST018",
        source="Sarvartha_Chintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="ashtakavarga",
        description=(
            "Jupiter transit with Ashtakavarga: Jupiter transiting a sign with 5+ bindus "
            "in Jupiter's BAV = highly auspicious year for education, prosperity, children. "
            "Jupiter transiting 5th from Moon with 6+ bindus = childbirth indication. "
            "Jupiter transiting 11th with 5+ bindus = major financial gains."
        ),
        confidence=0.89,
        verse="SC Ch.10 v.8-14",
        tags=["ashtakavarga", "jupiter_transit_bav", "5_bindus", "prosperity", "education"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST019",
        source="Sarvartha_Chintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="ashtakavarga",
        description=(
            "Saturn transit with Ashtakavarga: Saturn in Sade Sati position (12th/1st/2nd "
            "from Moon) with only 1-2 bindus = very severe difficulties. "
            "Saturn in 7.5-year positions with 4+ bindus in Saturn BAV = mitigated Sade Sati. "
            "Remedies strongly recommended when Saturn BAV < 3 during Sade Sati."
        ),
        confidence=0.88,
        verse="SC Ch.10 v.15-21",
        tags=["ashtakavarga", "saturn_transit_bav", "sade_sati", "mitigation", "low_bindus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST020",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga transit rule: 8 bindus in transit sign = excellent, virtually "
            "no obstacles. 7 = very good. 6 = good. 5 = moderate good. "
            "4 = average. 3 = slight difficulties. 2 = difficult. 1 = very difficult. "
            "0 = complete blockage; remedies essential."
        ),
        confidence=0.92,
        verse="BPHS Ch.66 v.13-20",
        tags=["ashtakavarga", "bindu_scale", "8_excellent", "0_blockage", "transit_quality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST021",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga annual assessment: At the start of each year (Solar return or "
            "Varshapravesh), assess where Jupiter and Saturn are transiting. "
            "If both are in signs with high BAV bindus for the natal chart, the year is "
            "excellent. If both are in low-bindu signs, the year is challenging overall."
        ),
        confidence=0.85,
        verse="BPHS Ch.66 v.21-26",
        tags=["ashtakavarga", "annual_assessment", "jupiter_saturn", "varshapravesh"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST022",
        source="Sarvartha_Chintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="ashtakavarga",
        description=(
            "Ashtakavarga for Dasha timing: The Dasha lord's transit through signs "
            "with high bindus in its own BAV produces the promised results of that Dasha. "
            "Low-bindu transits of the Dasha lord = delays and obstacles despite good Dasha. "
            "Highest-bindu sign of Dasha lord BAV = peak of Dasha results."
        ),
        confidence=0.86,
        verse="SC Ch.10 v.22-28",
        tags=["ashtakavarga", "dasha_timing", "dasha_lord_transit", "peak_dasha"],
        implemented=False,
    ),
    # --- Longevity and Life Span (AST023-025) ---
    RuleRecord(
        rule_id="AST023",
        source="BPHS",
        chapter="Ch.76",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Longevity from Sarvashtakavarga: Total bindus in all 12 signs / 7 = "
            "approximate life-span indicator (Prastara method). "
            "Total 337 bindus (theoretical max for 7 planets) in practice ranges 250-360. "
            "Sarvashtakavarga total below 220 = shorter life; above 300 = longer life."
        ),
        confidence=0.80,
        verse="BPHS Ch.76 v.21-28",
        tags=["ashtakavarga", "longevity", "life_span", "sarvashtakavarga_total"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST024",
        source="BPHS",
        chapter="Ch.76",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Lagna Ashtakavarga for health: The bindus in the Lagna sign of "
            "Sarvashtakavarga and the Lagna lord's BAV score indicate constitution strength. "
            "Lagna with 25+ total Sarva bindus = robust constitution. "
            "Lagna with fewer than 20 = delicate health; more attention to 6th house."
        ),
        confidence=0.82,
        verse="BPHS Ch.76 v.29-34",
        tags=["ashtakavarga", "lagna_health", "constitution", "sarva_bindus_25"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST025",
        source="Brihat_Jataka",
        chapter="Ch.19",
        school="varahamihira",
        category="ashtakavarga",
        description=(
            "Varahamihira on Ashtakavarga and periods of action: Signs with the most "
            "bindus in the Sarvashtakavarga become the most active signs in a person's life. "
            "The Dasha of the lord of the highest-bindu sign = most productive life period. "
            "Antardasha of lord of lowest-bindu sign = most difficult sub-period."
        ),
        confidence=0.83,
        verse="BJ Ch.19 v.10-16",
        tags=["ashtakavarga", "active_signs", "productive_dasha", "varahamihira"],
        implemented=False,
    ),
    # --- Practical Applications (AST026-030) ---
    RuleRecord(
        rule_id="AST026",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga for Muhurta (electional astrology): Choose dates when transiting "
            "planets occupy signs with high bindus in their respective BAVs. "
            "For marriage: Venus in high-bindu sign. Business: Mercury. "
            "Surgery or competition: Mars in favorable BAV position."
        ),
        confidence=0.84,
        verse="BPHS Ch.66 v.27-32",
        tags=["ashtakavarga", "muhurta", "electional", "venus_business_mars"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST027",
        source="Sarvartha_Chintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="ashtakavarga",
        description=(
            "Ashtakavarga and financial planning: The 2nd and 11th house BAV scores "
            "indicate wealth accumulation potential. "
            "2nd house Sarva bindus 30+ = strong wealth house. "
            "Saturn or Jupiter transiting 11th house with 5+ bindus = major income event."
        ),
        confidence=0.85,
        verse="SC Ch.10 v.29-35",
        tags=["ashtakavarga", "financial", "2nd_11th_house", "wealth_accumulation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST028",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga and career: The 10th house BAV score in Sarvashtakavarga "
            "and the 10th lord's BAV indicate career strength. "
            "10th house Sarva bindus 28+ = strong career potential. "
            "Planets transiting 10th with 5+ bindus in their BAV = career milestone period."
        ),
        confidence=0.86,
        verse="BPHS Ch.66 v.33-38",
        tags=["ashtakavarga", "career", "10th_house", "career_milestone"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST029",
        source="BPHS",
        chapter="Ch.66",
        school="parashari",
        category="ashtakavarga",
        description=(
            "Ashtakavarga and foreign travel: The 12th house BAV total and Saturn/Rahu "
            "transit through 12th with low bindus = forced foreign travel or exile. "
            "Jupiter transiting 12th with 5+ bindus = voluntary beneficial foreign journey. "
            "12th house Sarva bindus 25+ = good fortune in foreign lands."
        ),
        confidence=0.83,
        verse="BPHS Ch.66 v.39-44",
        tags=["ashtakavarga", "foreign_travel", "12th_house", "exile", "jupiter_12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="AST030",
        source="Sarvartha_Chintamani",
        chapter="Ch.10",
        school="sarvartha",
        category="ashtakavarga",
        description=(
            "Ashtakavarga chart comparison: When comparing two charts for compatibility, "
            "sum the bindus each person's chart has in the other's key signs (Moon, Venus, 7th). "
            "Combined bindu score 20+ in these signs = natural harmony and mutual support. "
            "Low combined bindus = friction and misunderstanding in the relationship."
        ),
        confidence=0.82,
        verse="SC Ch.10 v.36-42",
        tags=["ashtakavarga", "compatibility", "chart_comparison", "synastry", "combined_bindus"],
        implemented=False,
    ),
]

for rule in _ASHTAKAVARGA_RULES:
    ASHTAKAVARGA_RULES_REGISTRY.add(rule)
