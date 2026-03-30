"""
src/corpus/dasha_systems_rules.py — Dasha Systems Rules (S246)

Encodes classical planetary period (Dasha) systems beyond the basic
Vimshottari covered in earlier sessions. Covers Ashtottari, Yogini,
Kalachakra, Shodashottari, and timing principles.

Sources:
  BPHS Ch.46-66 — Dasha Adhyaya (multiple dasha systems)
  Uttara Kalamrita — Dasha interpretation
  Sarvartha Chintamani Ch.8 — Dasha timing

30 rules total: DSY001-DSY030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

DASHA_SYSTEMS_RULES_REGISTRY = CorpusRegistry()

_DASHA_RULES = [
    # --- Vimshottari Dasha Extended (DSY001-006) ---
    RuleRecord(
        rule_id="DSY001",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari Dasha — the primary Parashari dasha: 120-year cycle based on "
            "natal Moon's nakshatra. 9 planets × their periods: "
            "Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17. "
            "Starting dasha determined by Moon's exact position in its nakshatra at birth."
        ),
        confidence=0.97,
        verse="BPHS Ch.46 v.1-12",
        tags=["dasha", "vimshottari", "120_years", "moon_nakshatra", "primary_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY002",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari balance at birth: The dasha period already elapsed at birth = "
            "(Moon's degrees traversed in nakshatra / total nakshatra degrees) × dasha period. "
            "Remaining balance = dasha period − elapsed. "
            "Remaining balance determines first dasha at birth; subsequent dashas follow in full."
        ),
        confidence=0.95,
        verse="BPHS Ch.46 v.13-20",
        tags=["dasha", "vimshottari", "birth_balance", "elapsed_degrees", "remaining_period"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY003",
        source="BPHS",
        chapter="Ch.47",
        school="parashari",
        category="dasha",
        description=(
            "Antardasha (sub-period) sequence: Within each Mahadasha, the 9 sub-periods "
            "begin with the Mahadasha lord itself, then proceed in Vimshottari order. "
            "Sub-period duration = (Maha × Antar) / 120 years. "
            "Pratyantardasha = sub-sub-period using same proportional formula."
        ),
        confidence=0.93,
        verse="BPHS Ch.47 v.1-10",
        tags=["dasha", "vimshottari", "antardasha", "sub_period", "mahadasha_lord_first"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY004",
        source="BPHS",
        chapter="Ch.48",
        school="parashari",
        category="dasha",
        description=(
            "Vimshottari result principles: Mahadasha lord delivers results based on: "
            "(1) its natal house position; (2) houses it rules; (3) planets in those houses; "
            "(4) aspects it receives; (5) its Shadbala strength. "
            "Antardasha lord modifies the Mahadasha theme — harmonious if lords are friends."
        ),
        confidence=0.90,
        verse="BPHS Ch.48 v.1-12",
        tags=["dasha", "vimshottari", "result_principles", "5_factors", "friend_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY005",
        source="Uttara_Kalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="dasha",
        description=(
            "Dasha-Anter compatibility: When Dasha and Antardasha lords are: "
            "Natural friends = very favorable period. Natural neutrals = mixed results. "
            "Natural enemies = difficult period with conflicts in the themes they signify. "
            "Temporary friendship (based on natal chart) can override natural enmity."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.5-14",
        tags=["dasha", "vimshottari", "dasha_anter_compatibility", "natural_friends_enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY006",
        source="Sarvartha_Chintamani",
        chapter="Ch.8",
        school="sarvartha",
        category="dasha",
        description=(
            "Dasha lord in houses — general principles: "
            "Dasha lord in 1/5/9 from lagna = excellent period (Trikona). "
            "Dasha lord in 4/7/10 = productive but demanding (Kendra). "
            "Dasha lord in 3/6/11 = gains through effort/competition. "
            "Dasha lord in 2/8/12 = financial, health, or loss themes."
        ),
        confidence=0.87,
        verse="SC Ch.8 v.1-10",
        tags=["dasha", "dasha_lord_house", "trikona_kendra", "house_themes"],
        implemented=False,
    ),
    # --- Ashtottari Dasha (DSY007-010) ---
    RuleRecord(
        rule_id="DSY007",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="dasha",
        description=(
            "Ashtottari Dasha: 108-year cycle used when Rahu is in a Kendra or Trikona "
            "from the Hora Lagna in a daytime birth (or specific other conditions). "
            "8 planets (excluding Jupiter in some versions): "
            "Sun 6, Moon 15, Mars 8, Mercury 17, Saturn 10, Jupiter 19, Rahu 12, Venus 21."
        ),
        confidence=0.85,
        verse="BPHS Ch.49 v.1-12",
        tags=["dasha", "ashtottari", "108_years", "rahu_kendra", "8_planets"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY008",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="dasha",
        description=(
            "Ashtottari applicability conditions: Used when Rahu is in 1st, 2nd, 4th, 5th, "
            "7th, 9th, 10th, or 11th house from the Lagna (Kendra or Trikona + 2nd/11th). "
            "Also applicable for night births when Rahu is in certain positions. "
            "When both Vimshottari and Ashtottari apply, Vimshottari takes precedence."
        ),
        confidence=0.82,
        verse="BPHS Ch.49 v.13-22",
        tags=["dasha", "ashtottari", "applicability", "rahu_position", "night_birth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY009",
        source="BPHS",
        chapter="Ch.49",
        school="parashari",
        category="dasha",
        description=(
            "Ashtottari sequence and interpretation: Starts from natal Moon's nakshatra "
            "lord (same as Vimshottari). Proceeds in the order: Sun, Moon, Mars, Mercury, "
            "Saturn, Jupiter, Rahu, Venus. Results interpreted similarly to Vimshottari "
            "but Rahu's 12-year period is notably shorter (18 in Vimshottari)."
        ),
        confidence=0.82,
        verse="BPHS Ch.49 v.23-32",
        tags=["dasha", "ashtottari", "sequence", "rahu_12_years"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY010",
        source="BPHS",
        chapter="Ch.50",
        school="parashari",
        category="dasha",
        description=(
            "Yogini Dasha: 36-year cycle using 8 Yoginis (divine feminine energy forms). "
            "Mangala (Moon) 1yr, Pingala (Sun) 2yr, Dhanya (Jupiter) 3yr, Bhramari (Mars) 4yr, "
            "Bhadrika (Mercury) 5yr, Ulka (Saturn) 6yr, Siddha (Venus) 7yr, Sankata (Rahu) 8yr. "
            "Starts from nakshatra lord of natal Moon, computed by nakshatra mod 8."
        ),
        confidence=0.83,
        verse="BPHS Ch.50 v.1-15",
        tags=["dasha", "yogini_dasha", "36_years", "8_yoginis", "feminine_energy"],
        implemented=False,
    ),
    # --- Kalachakra Dasha (DSY011-013) ---
    RuleRecord(
        rule_id="DSY011",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Kalachakra Dasha: Sign-based dasha in two groups — "
            "Savya (forward) signs: Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius. "
            "Apasavya (reverse) signs: Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces. "
            "Dasha sequence proceeds zodiacally for Savya, reverse for Apasavya signs."
        ),
        confidence=0.82,
        verse="BPHS Ch.51 v.1-12",
        tags=["dasha", "kalachakra", "savya_apasavya", "sign_based", "forward_reverse"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY012",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Kalachakra periods: Each nakshatra quarter (pada) corresponds to a rashi. "
            "The periods are based on the Navamsha sign of the natal Moon's pada. "
            "Each sign has a fixed Kalachakra period: Aries 7, Taurus 16, Gemini 9, "
            "Cancer 21, Leo 5, Virgo 9 (and so on for all 12 signs, total 100 years)."
        ),
        confidence=0.80,
        verse="BPHS Ch.51 v.13-24",
        tags=["dasha", "kalachakra", "navamsha_pada", "100_years", "fixed_periods"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY013",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Kalachakra deha and jeeva signs: In Kalachakra, alternate signs in the dasha "
            "sequence are 'deha' (body) and 'jeeva' (life force) signs. "
            "Malefic planets in Deha sign during its dasha = health challenges. "
            "Malefics in Jeeva sign = threats to life energy. "
            "Benefics in both = vitality and protection."
        ),
        confidence=0.659,
        verse="BPHS Ch.51 v.25-36",
        tags=["dasha", "kalachakra", "deha_jeeva", "health", "life_force"],
        implemented=False,
    ),
    # --- Other Dasha Systems (DSY014-017) ---
    RuleRecord(
        rule_id="DSY014",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Shodashottari Dasha: 116-year cycle; used when lagna is in Hora of Moon "
            "at night birth. 8 planets × periods: Sun 11, Moon 11, Mars 12, Mercury 13, "
            "Jupiter 14, Saturn 15, Rahu 16, Venus 16. "
            "Sequence begins from the planet ruling the nakshatra pada of natal Moon."
        ),
        confidence=0.80,
        verse="BPHS Ch.52 v.1-12",
        tags=["dasha", "shodashottari", "116_years", "night_birth", "hora_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY015",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Dwisaptati-sama Dasha: 72-year cycle; applicable when lagna lord is in 7th "
            "or 7th lord is in lagna. 9 planets × 8 years each = 72 years. "
            "Sequence from lagna lord's nakshatra. Used alongside Vimshottari for "
            "charts with strong mutual lagna-7th house connection (marriage-focused charts)."
        ),
        confidence=0.659,
        verse="BPHS Ch.53 v.1-10",
        tags=["dasha", "dwisaptati", "72_years", "7th_lord_lagna", "8_years_each"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY016",
        source="BPHS",
        chapter="Ch.54",
        school="parashari",
        category="dasha",
        description=(
            "Shatabdika Dasha: 100-year cycle; used for longevity analysis. "
            "Based on lagna degree position in the navamsha. "
            "Sign periods in Shatabdika: same as Kalachakra periods. "
            "Primarily used to pinpoint dangerous periods in longevity assessment."
        ),
        confidence=0.657,
        verse="BPHS Ch.54 v.1-8",
        tags=["dasha", "shatabdika", "100_years", "longevity", "navamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY017",
        source="BPHS",
        chapter="Ch.55",
        school="parashari",
        category="dasha",
        description=(
            "Chaturashiti-sama Dasha: 84-year cycle (9 planets × ~9.33 yrs each). "
            "Applicable when the 10th lord is in 10th house. "
            "Career-focused dasha; used to time professional achievements. "
            "Strong 10th house = this dasha very relevant for timing career peaks."
        ),
        confidence=0.657,
        verse="BPHS Ch.55 v.1-8",
        tags=["dasha", "chaturashiti", "84_years", "10th_lord_10th", "career"],
        implemented=False,
    ),
    # --- Conditional and Uncommon Dashas (DSY018-020) ---
    RuleRecord(
        rule_id="DSY018",
        source="BPHS",
        chapter="Ch.56",
        school="parashari",
        category="dasha",
        description=(
            "Conditional dasha selection principle: BPHS states that multiple dasha "
            "systems may apply to a chart. The rule: "
            "(1) Vimshottari is universal default. "
            "(2) Special dashas apply only when the stated condition is met. "
            "(3) When special dasha applies, use both Vimshottari AND the special dasha. "
            "(4) Agreement of both dashas = greater certainty of prediction."
        ),
        confidence=0.85,
        verse="BPHS Ch.56 v.1-10",
        tags=["dasha", "conditional_dasha", "vimshottari_default", "agreement_principle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY019",
        source="Jaimini_Sutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="dasha",
        description=(
            "Jaimini Narayana Dasha: Sign-based dasha starting from the stronger of "
            "lagna or 7th house. Each sign rules for years equal to the number of signs "
            "from the sign to its lord (in the appropriate direction for Savya/Apasavya). "
            "Narayana Dasha reveals which sign's themes dominate each life period."
        ),
        confidence=0.83,
        verse="JS Adhyaya 2.60-75",
        tags=["dasha", "narayana_dasha", "jaimini", "sign_based", "savya_apasavya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY020",
        source="Jaimini_Sutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="dasha",
        description=(
            "Padakrama Dasha: Jaimini dasha based on Arudha Padas (A1-A12). "
            "Runs through each Arudha sign; results reflect the perceived/public manifestation "
            "of that house's themes during that period. "
            "Useful for timing public events, reputation changes, marriage (A7), career (A10)."
        ),
        confidence=0.80,
        verse="JS Adhyaya 3.65-78",
        tags=["dasha", "padakrama_dasha", "jaimini", "arudha_pada", "public_events"],
        implemented=False,
    ),
    # --- Dasha Timing and Precision (DSY021-025) ---
    RuleRecord(
        rule_id="DSY021",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="dasha",
        description=(
            "Sookshma (micro) Dasha: Sub-divisions below Pratyantardasha. "
            "Sookshma (4th level) and Prana (5th level) Dasha provide day-by-day precision. "
            "Sookshma = Pratyantardasha × planet ratio / 120. "
            "Prana = Sookshma × planet ratio / 120. Used for timing specific events within days."
        ),
        confidence=0.82,
        verse="BPHS Ch.57 v.1-12",
        tags=["dasha", "sookshma_dasha", "prana_dasha", "micro_period", "day_precision"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY022",
        source="Sarvartha_Chintamani",
        chapter="Ch.8",
        school="sarvartha",
        category="dasha",
        description=(
            "Transit confirmation of Dasha results: Major events occur when: "
            "(1) Dasha promise exists + (2) Transit confirms. "
            "Specifically: Jupiter and Saturn transiting key houses (7th for marriage, "
            "10th for career) while the Dasha lord's period promises the event = event occurs. "
            "Without transit confirmation, Dasha promise may not manifest."
        ),
        confidence=0.88,
        verse="SC Ch.8 v.11-20",
        tags=["dasha", "transit_confirmation", "dasha_transit", "jupiter_saturn", "event_timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY023",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="dasha",
        description=(
            "First Dasha results (birth dasha): The Mahadasha running at birth sets "
            "the initial life theme. A benefic Dasha at birth (Jupiter/Venus) = "
            "fortunate beginning, supportive family. A malefic Dasha (Saturn/Rahu) at birth = "
            "challenging early childhood but potential for strength later."
        ),
        confidence=0.85,
        verse="BPHS Ch.58 v.1-8",
        tags=["dasha", "birth_dasha", "first_dasha", "early_childhood", "life_theme"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY024",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="dasha",
        description=(
            "Dasha of yogakaraka: During the Dasha of a yogakaraka planet "
            "(planet owning both Kendra and Trikona, esp. for fixed signs), "
            "the native rises to prominence. Yogakaraka Dasha = period of sustained growth, "
            "recognition, and fulfillment of major life ambitions."
        ),
        confidence=0.88,
        verse="BPHS Ch.58 v.9-18",
        tags=["dasha", "yogakaraka_dasha", "prominence", "kendra_trikona_lord", "rise"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY025",
        source="BPHS",
        chapter="Ch.59",
        school="parashari",
        category="dasha",
        description=(
            "Maraka (death-inflicting) Dasha: Lords of 2nd and 7th houses are Marakas. "
            "During Maraka Dasha, especially if near longevity threshold, health crises occur. "
            "Maraka Antardasha within Maraka Mahadasha = highest risk period. "
            "Saturn and Rahu in 7th/2nd amplify Maraka effects in their Dashas."
        ),
        confidence=0.87,
        verse="BPHS Ch.59 v.1-12",
        tags=["dasha", "maraka", "2nd_7th_lord", "longevity", "health_crisis"],
        implemented=False,
    ),
    # --- Dasha Results for Specific Planets (DSY026-030) ---
    RuleRecord(
        rule_id="DSY026",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="dasha",
        description=(
            "Sun Mahadasha (6 years): Government service, authority, father's matters, "
            "health issues (eyes, heart, bones). Sun well-placed = rise in status/career. "
            "Sun in 6/8/12 = health challenges, separation from father, loss of authority. "
            "Sun Dasha good for: leadership, government contacts, father relationship."
        ),
        confidence=0.87,
        verse="BPHS Ch.60 v.1-8",
        tags=["dasha", "sun_dasha", "6_years", "government", "father", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY027",
        source="BPHS",
        chapter="Ch.61",
        school="parashari",
        category="dasha",
        description=(
            "Jupiter Mahadasha (16 years): Wisdom, prosperity, children, spiritual growth, "
            "guru blessings, long-distance travel. Jupiter well-placed = golden period. "
            "Jupiter in 6/8/12 = legal issues, health, expenditure, but still expansive. "
            "Jupiter Dasha good for: education, wealth, marriage for children, spiritual progress."
        ),
        confidence=0.88,
        verse="BPHS Ch.61 v.1-8",
        tags=["dasha", "jupiter_dasha", "16_years", "prosperity", "wisdom", "golden_period"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY028",
        source="BPHS",
        chapter="Ch.62",
        school="parashari",
        category="dasha",
        description=(
            "Saturn Mahadasha (19 years): Discipline, hard work, delays, chronic issues, "
            "masses, agriculture, real estate. Saturn well-placed = slow but steady accumulation. "
            "Saturn in 1/8/12 = health challenges, isolation, heavy responsibilities. "
            "Saturn Dasha good for: persistent effort, service fields, old-age support structures."
        ),
        confidence=0.87,
        verse="BPHS Ch.62 v.1-8",
        tags=["dasha", "saturn_dasha", "19_years", "discipline", "delays", "accumulation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY029",
        source="BPHS",
        chapter="Ch.63",
        school="parashari",
        category="dasha",
        description=(
            "Rahu Mahadasha (18 years): Foreign connections, innovation, unconventional paths, "
            "sudden changes, illusion. Rahu well-placed = material success, fame. "
            "Rahu conjunct benefics = exceptional worldly achievement. "
            "Rahu Dasha delivers results of the house it occupies and its dispositor."
        ),
        confidence=0.86,
        verse="BPHS Ch.63 v.1-8",
        tags=["dasha", "rahu_dasha", "18_years", "foreign", "sudden_changes", "dispositor"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DSY030",
        source="BPHS",
        chapter="Ch.64",
        school="parashari",
        category="dasha",
        description=(
            "Ketu Mahadasha (7 years): Spirituality, renunciation, moksha, mysticism, "
            "sudden disconnections, past-life karma. Ketu well-placed = spiritual insights. "
            "Ketu Dasha often brings: separation from the material, health mysteries, "
            "interest in esoteric subjects. Ketu delivers results of its sign lord."
        ),
        confidence=0.86,
        verse="BPHS Ch.64 v.1-8",
        tags=["dasha", "ketu_dasha", "7_years", "spirituality", "moksha", "past_karma"],
        implemented=False,
    ),
]

for rule in _DASHA_RULES:
    DASHA_SYSTEMS_RULES_REGISTRY.add(rule)
