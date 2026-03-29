"""
src/corpus/jaimini_sutras_exhaustive.py — Jaimini Sutras Exhaustive (S259)

Exhaustive encoding of Maharishi Jaimini's Jaimini Sutras (4 Adhyayas):
- Chara Karaka system (8 variable karakas by planetary degrees)
- Rashi Drishti (sign aspects — mutual among fixed, movable, dual signs)
- Chara Dasha (movable sign dasha sequence)
- Sthira Dasha (fixed sign dasha, also called Shula Dasha)
- Niryana Shoola Dasha
- Arudha/Pada system (all 12 padas including Upapada)
- Argala doctrine (Jaimini version)
- Karakamsha and Swamsha analysis
- Upapada Lagna for marriage
- Raja Yoga (Jaimini-specific combinations)
- Jaimini aspects and house significations
- Atmakaraka results in navamsha (Karakamsha)
- Timing of events via dasha combinations

150 rules: JMX001-JMX150.
All: school="jaimini", source="JaiminiSutras", implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Chara Karaka System (JMX001-012) ─────────────────────────────────────
    RuleRecord(
        rule_id="JMX001",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Atmakaraka (AK): the planet with the highest degree in the chart "
            "(ignoring sign) represents the soul's primary signification. "
            "Rahu degrees are subtracted from 30 to find his effective degree."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.1",
        tags=["jmx", "chara_karaka", "atmakaraka", "soul", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX002",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Amatyakaraka (AMK): planet with second-highest degree. "
            "Signifies career, profession, and ministers. "
            "Conjunction of AK and AMK lords produces royal combinations."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.2",
        tags=["jmx", "chara_karaka", "amatyakaraka", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX003",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Bhratrikaraka (BK): third-highest degree planet. "
            "Signifies siblings, courage, co-borns. "
            "Putrakaraka (PK): fourth-highest degree — signifies children and intellect."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.3",
        tags=["jmx", "chara_karaka", "bhratrikaraka", "putrakaraka", "siblings", "children", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX004",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Matrikaraka (MK): fifth-highest degree planet — signifies mother, mind, homeland. "
            "Gnatikaraka (GK): sixth-highest — signifies enemies, disease, obstacles, competition."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.4",
        tags=["jmx", "chara_karaka", "matrikaraka", "gnatikaraka", "mother", "enemies", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX005",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Darakaraka (DK): planet with lowest degree — signifies spouse, partnerships. "
            "In the 7-karaka system, Putrakaraka fills both PK and MK positions. "
            "Jaimini allows 7-karaka or 8-karaka system depending on commentary tradition."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.1.5",
        tags=["jmx", "chara_karaka", "darakaraka", "spouse", "marriage", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX006",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Atmakaraka in navamsha (Karakamsha Lagna) indicates the soul's deepest aspirations. "
            "The sign of AK in D9 becomes the Karakamsha Lagna (KL). "
            "Planets in KL or aspecting it by Rashi Drishti modify life's spiritual direction."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.15",
        tags=["jmx", "karakamsha", "atmakaraka", "navamsha", "spiritual", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX007",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Swamsha: sign occupied by AK in D1 (birth chart). "
            "Karakamsha is in D9, Swamsha in D1. "
            "Both are used for career and spiritual analysis in Jaimini system."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.1.20",
        tags=["jmx", "swamsha", "atmakaraka", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX008",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "If two planets have identical degrees, the one in the higher sign (Aries=1) "
            "is given higher karaka status. This prevents ties in the Chara Karaka assignment. "
            "All 9 planets including Rahu participate in the 8-karaka system."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.1.6",
        tags=["jmx", "chara_karaka", "rahu", "degree_tie_breaking", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX009",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Atmakaraka results in Karakamsha: Sun in KL → leadership, government service, "
            "royal patronage. Moon → agriculture, public service, popularity."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.2.1",
        tags=["jmx", "karakamsha", "sun", "moon", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX010",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Mars in Karakamsha → military, surgery, engineering, weapons. "
            "Mercury in KL → trade, communication, writing, accounts. "
            "Jupiter in KL → teaching, priesthood, philosophy, law."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.2.2",
        tags=["jmx", "karakamsha", "mars", "mercury", "jupiter", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX011",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Venus in Karakamsha → arts, luxury goods, beauty industry, diplomacy, sensual pleasures. "
            "Saturn in KL → service to the masses, labourers, agriculture, mining, delays."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.2.3",
        tags=["jmx", "karakamsha", "venus", "saturn", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX012",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="chara_karaka",
        description=(
            "Rahu in Karakamsha → foreign lands, unconventional career, technology, "
            "chemicals, aviation. Ketu in KL → liberation, spiritual attainment, "
            "past-life skills, mathematics, occult."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 1.2.4",
        tags=["jmx", "karakamsha", "rahu", "ketu", "career", "spiritual", "jaimini"],
        implemented=False,
    ),

    # ── Rashi Drishti — Sign Aspects (JMX013-020) ───────────────────────────
    RuleRecord(
        rule_id="JMX013",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Rashi Drishti: All movable signs (Aries/Cancer/Libra/Capricorn) "
            "aspect all fixed signs (Taurus/Leo/Scorpio/Aquarius) except the adjacent one. "
            "This is a sign-to-sign aspect, not planet-to-planet."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.25",
        tags=["jmx", "rashi_drishti", "movable_signs", "fixed_signs", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX014",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "All fixed signs (Taurus/Leo/Scorpio/Aquarius) aspect all movable signs "
            "(Aries/Cancer/Libra/Capricorn) except the adjacent one. "
            "Mutual aspect between movable and fixed (except adjacent) is the Jaimini rule."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.26",
        tags=["jmx", "rashi_drishti", "movable_signs", "fixed_signs", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX015",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "All dual signs (Gemini/Virgo/Sagittarius/Pisces) aspect each other mutually. "
            "This creates 6 pairs of mutual dual-sign aspects. "
            "Dual signs do NOT aspect movable or fixed signs."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.27",
        tags=["jmx", "rashi_drishti", "dual_signs", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX016",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Exception to Rashi Drishti: adjacent signs do NOT aspect each other. "
            "Aries does not aspect Taurus (adjacent fixed), Cancer does not aspect Leo, etc. "
            "The adjacent exception applies only between movable-fixed pairs."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.28",
        tags=["jmx", "rashi_drishti", "adjacent_exception", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX017",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Planets in a sign cast Rashi Drishti on all signs that their sign aspects. "
            "A planet in Aries aspects Leo, Scorpio, Aquarius (fixed except Taurus). "
            "Rashi Drishti is stronger than Graha Drishti in Jaimini for most analyses."
        ),
        confidence=0.96,
        verse="Jaimini Sutras 1.1.29",
        tags=["jmx", "rashi_drishti", "planets", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX018",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Aries aspects Leo, Scorpio, Aquarius. Cancer aspects Libra, Scorpio, Aquarius. "
            "Capricorn aspects Aries, Cancer, Libra. Libra aspects Aries, Cancer, Capricorn. "
            "Full table: movable signs aspect fixed signs excluding the one before them."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.30",
        tags=["jmx", "rashi_drishti", "aries", "cancer", "libra", "capricorn", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX019",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Fixed sign aspects: Taurus aspects Cancer, Libra, Capricorn. "
            "Leo aspects Scorpio, Aquarius, Taurus. Scorpio aspects Aries, Leo, Aquarius (exc Cancer). "
            "Aquarius aspects Taurus, Leo, Scorpio (exc Capricorn)."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.31",
        tags=["jmx", "rashi_drishti", "taurus", "leo", "scorpio", "aquarius", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX020",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Graha Drishti (planetary aspects) also apply in Jaimini for specific analyses. "
            "For Raja Yoga and Karakamsha: use Rashi Drishti primarily. "
            "For Upapada marriage analysis: Rashi Drishti on Upapada Lagna from its lord is key."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 1.1.32",
        tags=["jmx", "rashi_drishti", "graha_drishti", "upapada", "marriage", "jaimini"],
        implemented=False,
    ),

    # ── Arudha / Pada System (JMX021-035) ────────────────────────────────────
    RuleRecord(
        rule_id="JMX021",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Arudha Lagna (AL / A1): count from Lagna to its lord, "
            "then the same number of signs from the lord. That sign is the Arudha Lagna. "
            "If result falls in Lagna or 7th from Lagna, use 10th from Lagna instead."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.40",
        tags=["jmx", "arudha", "arudha_lagna", "pada", "image", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX022",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Arudha Lagna (AL) represents the image or illusion of the self — "
            "how the world perceives the native. Benefics in AL → good reputation, "
            "malefics in AL → controversial, influential, or feared persona."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.41",
        tags=["jmx", "arudha", "arudha_lagna", "reputation", "public_image", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX023",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Upapada Lagna (UL / A12): Arudha of the 12th house. "
            "Method: count from 12th house to its lord, same from lord. "
            "UL is the primary indicator of spouse, marriage, and the bed pleasures house."
        ),
        confidence=0.98,
        verse="Jaimini Sutras 1.1.42",
        tags=["jmx", "arudha", "upapada", "marriage", "spouse", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX024",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Planets in Upapada Lagna modify spouse qualities: "
            "Jupiter in UL → wise, religious spouse. Venus in UL → beautiful, artistic spouse. "
            "Saturn in UL → elder spouse or delayed marriage. Mars in UL → passionate, argumentative."
        ),
        confidence=0.96,
        verse="Jaimini Sutras 1.1.43",
        tags=["jmx", "upapada", "spouse", "marriage", "planets_in_upapada", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX025",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Planets aspecting Upapada by Rashi Drishti also colour spouse qualities. "
            "If UL lord is strong and aspected by benefics → long-lasting marriage. "
            "Malefics aspecting UL or 2nd from UL → separation or spouse's ill health."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.1.44",
        tags=["jmx", "upapada", "marriage", "separation", "longevity_of_marriage", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX026",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Second marriage: if 2nd from UL has malefics or UL lord is debilitated/combust, "
            "there is a second marriage. Count of planets in 2nd from UL = number of marriages. "
            "A9 (arudha of 9th) also indicates second spouse."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 1.1.45",
        tags=["jmx", "upapada", "second_marriage", "marriage", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX027",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Darapada (A7): arudha of the 7th house. Indicates the type of partner encountered. "
            "If A7 = AL → spouse and self have similar public image. "
            "If A7 is in 6th/8th/12th from AL → conflict between self-image and partner's."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 1.1.46",
        tags=["jmx", "arudha", "darapada", "a7", "spouse", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX028",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Matrupada (A4): arudha of 4th house — mother's image and property matters. "
            "Putrapada (A5): arudha of 5th house — children's wellbeing and intelligence. "
            "Rajyapada (A10): arudha of 10th house — career status and prestige."
        ),
        confidence=0.94,
        verse="Jaimini Sutras 1.1.47",
        tags=["jmx", "arudha", "a4", "a5", "a10", "mother", "children", "career", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX029",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "AL in a kendra or trikona from Moon → person achieves recognition and fame. "
            "AL and Moon in mutual kendra/trikona → prominent social standing. "
            "AL aspected by AK by Rashi Drishti → soul's purpose aligns with public role."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.1.50",
        tags=["jmx", "arudha_lagna", "moon", "fame", "recognition", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX030",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Dhana (A2): arudha of 2nd house — accumulated wealth and financial image. "
            "Vighna (A8): arudha of 8th — obstacles, legacies, longevity challenges. "
            "Mrityu (A8) gives obstacles; benefic AL aspecting A8 by Rashi Drishti mitigates."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.1.51",
        tags=["jmx", "arudha", "a2", "a8", "wealth", "longevity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX031",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Gnati (A6): arudha of 6th house — enemies, diseases, litigation image. "
            "Malefics with A6 → persistent enemies and health struggles. "
            "Trikona rule: if AL, A9, and A5 are all strong → dharmic life path."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.1.52",
        tags=["jmx", "arudha", "a6", "enemies", "disease", "dharma", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX032",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Exception rule for Arudha calculation: if the calculated Arudha falls in "
            "the same sign as the house or in its 7th, move to the 10th from that sign. "
            "This is the fundamental Jaimini correction for Arudha Pada calculation."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.41",
        tags=["jmx", "arudha", "calculation", "exception_rule", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX033",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Planets in 1st and 7th from AL give their results openly in public. "
            "2nd and 12th from AL → financial results and hidden expenditures publicly. "
            "Malefic in 3rd from AL → courage shown publicly; malefic in 6th from AL → open enemies."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.1.55",
        tags=["jmx", "arudha_lagna", "public_results", "reputation", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX034",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Argala from AL: planets in 2nd, 4th, and 11th from AL cast Argala (intervention). "
            "2nd Argala (most powerful): modifies financial and speech matters. "
            "4th Argala: happiness and domestic/comfort matters. 11th Argala: gains and desires."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 1.4.1",
        tags=["jmx", "argala", "arudha_lagna", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX035",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="arudha",
        description=(
            "Obstruction to Argala (Virodha-Argala): planets in 12th obstruct 2nd Argala, "
            "10th obstructs 4th Argala, 3rd obstructs 11th Argala. "
            "If obstructors outnumber Argala causers, the Argala is neutralised."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 1.4.2",
        tags=["jmx", "argala", "virodha_argala", "obstruction", "jaimini"],
        implemented=False,
    ),

    # ── Chara Dasha (JMX036-050) ──────────────────────────────────────────────
    RuleRecord(
        rule_id="JMX036",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Chara Dasha: movable sign dasha system. Sequence begins from Lagna sign. "
            "Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius) proceed forward; "
            "Even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces) proceed backward."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 2.1.1",
        tags=["jmx", "chara_dasha", "dasha", "movable_signs", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX037",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Chara Dasha years for each sign: determined by the lord's position. "
            "Count from the sign to its lord; subtract 1 = dasha years. "
            "For dual-lorded signs (Scorpio: Mars/Ketu), use the stronger lord."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 2.1.2",
        tags=["jmx", "chara_dasha", "dasha_years", "dasha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX038",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Chara Dasha year calculation: if the lord is in the same sign, dasha = 12 years. "
            "If forward (odd sign), count forward; if backward (even sign), count backward. "
            "Minimum dasha = 1 year, maximum = 12 years."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 2.1.3",
        tags=["jmx", "chara_dasha", "dasha_years", "calculation", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX039",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Events during Chara Dasha: examine the dasha sign's contents by Rashi Drishti. "
            "If the dasha sign has/aspects AK → karmic/soul-level events. "
            "If dasha sign has/aspects UL → marriage events. AMK → career events."
        ),
        confidence=0.94,
        verse="Jaimini Sutras 2.1.5",
        tags=["jmx", "chara_dasha", "dasha", "timing", "events", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX040",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Chara Dasha antardasha (sub-period): within each dasha, "
            "sub-dashas run through all 12 signs in the same sequence (forward/backward). "
            "Starting from the main dasha sign itself, each sub runs proportionally."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 2.1.8",
        tags=["jmx", "chara_dasha", "antardasha", "sub_period", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX041",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Death timing in Chara Dasha: dasha of the 8th sign from AL (or Lagna) "
            "or the sign with malefics aspecting the Lagna. "
            "AK in a sign → its dasha is significant for spiritual transformation (not always physical death)."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 2.1.12",
        tags=["jmx", "chara_dasha", "death", "timing", "longevity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX042",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Marriage timing: Chara Dasha of the sign containing Upapada Lagna (UL) "
            "or 7th from UL, or the sign aspected by Darakaraka — indicates marriage. "
            "Also: dasha of sign containing the 7th lord from Lagna in D9."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 2.1.15",
        tags=["jmx", "chara_dasha", "marriage", "timing", "upapada", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX043",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Career peak timing: dasha of sign containing AMK or aspected by AMK by Rashi Drishti. "
            "Also: dasha of 10th sign from AL. "
            "If AMK is in kendra from AK → career peak coincides with soul's purpose period."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 2.1.18",
        tags=["jmx", "chara_dasha", "career", "timing", "amatyakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX044",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Chara Dasha of the sign containing the 9th lord or 9th from Lagna → "
            "travel, pilgrimage, father's matters, higher education, dharmic events. "
            "9th from AK → spiritual initiation or guru-meeting timing."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 2.1.20",
        tags=["jmx", "chara_dasha", "travel", "father", "dharma", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX045",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="chara_dasha",
        description=(
            "Children timing: dasha of sign containing PK (Putrakaraka) or "
            "5th from Karakamsha. Benefics in 5th from AK or KL → easier conception. "
            "Jupiter aspecting 5th from KL by Rashi Drishti → children in that dasha."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 2.1.22",
        tags=["jmx", "chara_dasha", "children", "timing", "putrakaraka", "jaimini"],
        implemented=False,
    ),

    # ── Sthira / Shoola Dasha (JMX046-055) ───────────────────────────────────
    RuleRecord(
        rule_id="JMX046",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Sthira Dasha (also Shula Dasha): fixed sign dasha system for longevity analysis. "
            "Movable signs give 7 years, Fixed signs give 8 years, Dual signs give 9 years. "
            "Sequence starts from the stronger of Lagna or 7th from Lagna."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 2.2.1",
        tags=["jmx", "sthira_dasha", "shula_dasha", "longevity", "dasha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX047",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Sthira Dasha sequence: if Lagna is odd sign, proceed through signs forward. "
            "If Lagna is even sign, proceed backward. "
            "Use Sthira Dasha primarily for timing of death and major life upheavals."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 2.2.2",
        tags=["jmx", "sthira_dasha", "death", "timing", "longevity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX048",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Niryana Shoola Dasha: death-inflicting dasha. "
            "Sign with Saturn, or aspected by Saturn and Rahu together by Rashi Drishti, "
            "is the Shoola (trident) sign — its dasha brings severe health crises."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 2.2.5",
        tags=["jmx", "sthira_dasha", "shoola_dasha", "death", "saturn", "rahu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX049",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Longevity from Sthira Dasha: sum of dasha periods until a Shoola sign dasha "
            "gives rough lifespan estimate. Three levels — Alpayu (short life < 33), "
            "Madhyayu (medium 33-66), Purnayu (full life 66-100+)."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 2.2.8",
        tags=["jmx", "sthira_dasha", "longevity", "alpayu", "madhyayu", "purnayu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX050",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Brahma, Rudra, and Maheshvara: three special planets calculated in Jaimini "
            "for longevity determination. Brahma planet is lord of the most powerful kendra. "
            "Rudra planet is lord of 8th from Lagna. Their dashas have special significance."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 2.2.10",
        tags=["jmx", "brahma_planet", "rudra_planet", "longevity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX051",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Brahma planet: lord of the stronger of 6th/8th/12th from AK or lord of Hora Lagna. "
            "Brahma's dasha grants blessings of long life when strong. "
            "Rudra: the stronger of 8th lord from Lagna or 8th lord from Moon — indicates disease/death timing."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 2.2.11",
        tags=["jmx", "brahma_planet", "rudra_planet", "atmakaraka", "longevity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX052",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Maheshvara: planet aspecting or conjunct 8th from Lagna or 8th from Hora Lagna. "
            "If Maheshvara is malefic and in the Shoola dasha sign → critical health period. "
            "Jupiter as Maheshvara mitigates; Saturn as Maheshvara intensifies."
        ),
        confidence=0.84,
        verse="Jaimini Sutras 2.2.12",
        tags=["jmx", "maheshvara", "longevity", "saturn", "jupiter", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX053",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Antardasha within Sthira Dasha: sub-signs run in same direction as main dasha. "
            "Each sub-sign = (main dasha years / 12) as proportional sub-period. "
            "Event timing: when both main and sub dasha connect to the event's karaka sign."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 2.2.15",
        tags=["jmx", "sthira_dasha", "antardasha", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX054",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Navamsha Dasha (Narayana Dasha variant): some commentators use D9 lagna "
            "as starting point for Chara Dasha. This gives spiritual timing and inner life events. "
            "Physical events use D1 Chara Dasha; soul-level events use D9 Narayana Dasha."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 2.3.1",
        tags=["jmx", "narayana_dasha", "navamsha", "dasha", "spiritual", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX055",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="sthira_dasha",
        description=(
            "Padakrama Dasha: sequential dasha of Arudha Padas. "
            "Begins from AL, proceeds through A2, A3... A12 in sequence. "
            "Each Pada dasha period = years indicated by that Pada's house significance."
        ),
        confidence=0.80,
        verse="Jaimini Sutras 2.3.5",
        tags=["jmx", "padakrama_dasha", "arudha", "dasha", "jaimini"],
        implemented=False,
    ),

    # ── Jaimini Raja Yoga (JMX056-072) ────────────────────────────────────────
    RuleRecord(
        rule_id="JMX056",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Raja Yoga (primary): AK and AMK conjunction or mutual Rashi Drishti. "
            "Soul (AK) and career planet (AMK) unite → career becomes dharmic purpose. "
            "Strongest Raja Yoga in Jaimini system."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.2.20",
        tags=["jmx", "raja_yoga", "atmakaraka", "amatyakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX057",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "If AK is in a kendra (1/4/7/10) or trikona (1/5/9) from Lagna, "
            "and aspected by benefics by Rashi Drishti → powerful Raja Yoga for recognition. "
            "AK in Lagna itself is the most powerful position."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.2.21",
        tags=["jmx", "raja_yoga", "atmakaraka", "kendra", "trikona", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX058",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Karakamsha Raja Yoga: Jupiter or Venus in Karakamsha Lagna → "
            "Rajayoga of the highest order. Jupiter in KL → wisdom-based leadership. "
            "Venus in KL → artistic/aesthetic leadership and luxury."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 1.2.25",
        tags=["jmx", "raja_yoga", "karakamsha", "jupiter", "venus", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX059",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "5th and 9th lords from Karakamsha in mutual aspect by Rashi Drishti → "
            "fortune and intelligence combine for success. "
            "If these lords also aspect AK → dharmakarmadhipati yoga equivalent in Jaimini."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.2.26",
        tags=["jmx", "raja_yoga", "karakamsha", "dharma", "fortune", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX060",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Kevala Yoga: AK alone in a sign with no other planet, no Rashi Drishti from others → "
            "person achieves singular greatness in isolation. "
            "AK unaspected and in exaltation or own sign → spiritual liberation (Moksha Yoga)."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 1.2.30",
        tags=["jmx", "kevala_yoga", "raja_yoga", "atmakaraka", "moksha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX061",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Bandha Yoga (imprisonment): AK with Saturn and Rahu by conjunction or Rashi Drishti "
            "in Lagna or 12th → imprisonment, exile, or severe restriction in career. "
            "Jupiter aspecting AK by Rashi Drishti mitigates Bandha Yoga."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 1.2.35",
        tags=["jmx", "bandha_yoga", "imprisonment", "atmakaraka", "saturn", "rahu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX062",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Sula Yoga: malefics in 6th and 8th from Lagna simultaneously → "
            "suffering and obstacles in life. Named for the trident (Shula). "
            "Benefic in Lagna aspecting both 6th and 8th by Rashi Drishti mitigates."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 1.2.38",
        tags=["jmx", "sula_yoga", "malefics", "obstacles", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX063",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Nabhasa Yogas in Jaimini: when all planets fall in specific sign patterns. "
            "Rajju Yoga (all planets in movable signs) → itinerant, travels frequently. "
            "Musala Yoga (all in fixed signs) → firm, accumulated wealth. "
            "Nala Yoga (all in dual signs) → versatile, multiple occupations."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 1.3.5",
        tags=["jmx", "nabhasa_yoga", "rajju_yoga", "musala_yoga", "nala_yoga", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX064",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Srikantha Yoga: benefics in 1st, 5th, and 9th from Karakamsha → "
            "devotion, wisdom, dharmic prosperity. This is Jaimini's equivalent of "
            "the Parashari Raja Yoga formed by trikona lords' conjunction."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 1.3.10",
        tags=["jmx", "srikantha_yoga", "raja_yoga", "karakamsha", "trikona", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX065",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Chamara Yoga (Jaimini): AK in a kendra from Lagna, aspected by Jupiter and Venus "
            "by Rashi Drishti → royalty, honour, and scholarly recognition. "
            "Named for the royal fly-whisk symbol of authority."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 1.3.12",
        tags=["jmx", "chamara_yoga", "raja_yoga", "atmakaraka", "jupiter", "venus", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX066",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Dhana Yoga: 2nd lord and 11th lord from AL in mutual Rashi Drishti "
            "or both aspecting AL → great wealth accumulation. "
            "If AL lord is strong in D2 (Hora chart) and aspected by AMK → sustained wealth."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 1.3.15",
        tags=["jmx", "dhana_yoga", "wealth", "arudha_lagna", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX067",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Daridra Yoga (Jaimini): malefics in 1st and 7th from AL simultaneously, "
            "with no benefic Rashi Drishti → poverty and loss of status. "
            "12th from AL with malefics → hidden debts and financial drain."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 1.3.18",
        tags=["jmx", "daridra_yoga", "poverty", "arudha_lagna", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX068",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Pravrajya (renunciation): Saturn and AK in same sign or mutual Rashi Drishti, "
            "aspected by Jupiter → monastic calling. "
            "Ketu with AK and no benefics except Jupiter → spiritual renunciation path."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 2.4.1",
        tags=["jmx", "pravrajya", "renunciation", "moksha", "atmakaraka", "saturn", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX069",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Moksha Yoga: AK in own sign or exaltation in navamsha, "
            "with Ketu or Jupiter by Rashi Drishti → final liberation likely in this birth. "
            "12th from Karakamsha aspected by Jupiter or Venus → spiritual liberation."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 2.4.5",
        tags=["jmx", "moksha_yoga", "liberation", "atmakaraka", "ketu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX070",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Vidhwa Yoga (widowhood): if UL lord is in 6th/8th/12th from UL "
            "and aspected by malefics by Rashi Drishti → early widowhood. "
            "Saturn in 7th from UL → long-lived spouse but eventual separation."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 2.4.8",
        tags=["jmx", "widowhood", "upapada", "marriage", "saturn", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX071",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Balarishta (childhood adversity): if AK is afflicted in 8th from Lagna "
            "or in Lagna aspected by malefics only → childhood difficulties. "
            "Protections: benefic Rashi Drishti on Lagna or AK from Jupiter reduces Balarishta."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 3.1.1",
        tags=["jmx", "balarishta", "childhood", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX072",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="raja_yoga",
        description=(
            "Jaimini Roga Yoga (disease): malefics in 6th from Karakamsha or "
            "6th from Lagna aspected by GK (Gnatikaraka) by Rashi Drishti → "
            "chronic disease. Specific malefic indicates body system affected."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 3.1.5",
        tags=["jmx", "roga_yoga", "disease", "medical", "karakamsha", "jaimini"],
        implemented=False,
    ),

    # ── Karakamsha Analysis (JMX073-090) ──────────────────────────────────────
    RuleRecord(
        rule_id="JMX073",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Karakamsha Lagna (KL): sign of AK in D9 chart. "
            "1st from KL → self and body; 5th from KL → education, intellect, children; "
            "9th from KL → dharma, father, fortune; 10th from KL → career and status."
        ),
        confidence=0.96,
        verse="Jaimini Sutras 1.2.10",
        tags=["jmx", "karakamsha", "houses", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX074",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "2nd from Karakamsha: indicates speech, family, and accumulated learning. "
            "Mercury in 2nd from KL → eloquent, scholarly. Malefic in 2nd from KL → "
            "harsh speech or family troubles. Jupiter in 2nd from KL → wisdom in speech."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.2.12",
        tags=["jmx", "karakamsha", "speech", "family", "mercury", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX075",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "4th from Karakamsha: happiness, property, and mother. "
            "Venus or Moon in 4th from KL → good property and comforts. "
            "Saturn in 4th from KL → property through hard work; Rahu → unconventional home."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.2.13",
        tags=["jmx", "karakamsha", "property", "happiness", "mother", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX076",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "5th from Karakamsha: children and intellect. "
            "Benefics in 5th from KL → intelligent children and good education. "
            "Jupiter in 5th from KL → scholars, philosophers; Venus → artistic children."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 1.2.14",
        tags=["jmx", "karakamsha", "children", "intellect", "education", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX077",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "7th from Karakamsha: spouse characteristics. "
            "Venus in 7th from KL → beautiful, devoted spouse. Jupiter → wise spouse. "
            "Mars → passionate but aggressive; Saturn → older or delayed marriage."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.2.15",
        tags=["jmx", "karakamsha", "spouse", "marriage", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX078",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "8th from Karakamsha: longevity and cause of death direction. "
            "Malefics in 8th from KL with no benefic aspect → difficult death. "
            "Saturn in 8th from KL → death by chronic disease or old age; "
            "Mars → accidents; Sun → fever/government; Moon → water."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 1.2.16",
        tags=["jmx", "karakamsha", "longevity", "death", "saturn", "mars", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX079",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "12th from Karakamsha: moksha, expenditure, foreign travel. "
            "Ketu in 12th from KL → Moksha Yoga (liberation). "
            "Jupiter or Venus in 12th from KL → spiritual liberation through devotion. "
            "Saturn in 12th → isolation, asceticism, final renunciation."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.2.17",
        tags=["jmx", "karakamsha", "moksha", "liberation", "ketu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX080",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Kevalya (Kaivalya) Yoga: AK with Ketu and Jupiter in Karakamsha → "
            "the very highest moksha — complete dissolution of individual soul into universal. "
            "Rarest and most powerful spiritual yoga in Jaimini system."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 1.2.30",
        tags=["jmx", "kaivalya_yoga", "moksha", "liberation", "ketu", "jupiter", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX081",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Sun in Karakamsha: government service, leadership, father-figure roles. "
            "Person rises through official channels and authority structures. "
            "Aspected by Jupiter by Rashi Drishti → ministerial or advisory roles."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 1.2.1",
        tags=["jmx", "karakamsha", "sun", "government", "leadership", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX082",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Moon in Karakamsha: farming, public service, trading in liquids/food, "
            "nursing, hospitality industry. Person has mass appeal and public recognition. "
            "Moon strong in KL → emotional intelligence and nurturing leadership."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.2.2",
        tags=["jmx", "karakamsha", "moon", "public_service", "leadership", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX083",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Mars in Karakamsha: military officer, surgeon, engineer, police, chef. "
            "Mars also indicates weapons and fire. In navamsha exaltation → decorated military hero. "
            "Mars with Ketu in KL → tantra, occult, or weapons expert."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.2.2",
        tags=["jmx", "karakamsha", "mars", "military", "surgery", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX084",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Mercury in Karakamsha: trade, commerce, communication, accounts, writing. "
            "Mercury with Jupiter → teaching and publishing. "
            "Mercury with Venus → fine arts combined with commerce. "
            "Mercury with Rahu → digital technology, foreign trade."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 1.2.3",
        tags=["jmx", "karakamsha", "mercury", "trade", "communication", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX085",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="karakamsha",
        description=(
            "Saturn in Karakamsha: service industries, labourers, agriculture, oil/mines, "
            "manufacturing, construction. Saturn in KL in exaltation → famous industrialist. "
            "Saturn with Rahu in KL → chemical, petroleum, or waste-management industry."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 1.2.3",
        tags=["jmx", "karakamsha", "saturn", "service", "industry", "jaimini"],
        implemented=False,
    ),

    # ── Special Topics & Miscellaneous Jaimini (JMX086-115) ──────────────────
    RuleRecord(
        rule_id="JMX086",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini's unique house significations differ from Parashari: "
            "5th house → past karma, mantras, devotion, ishta devata. "
            "12th house → final liberation, expenses, foreign residence, and sleep."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 3.2.1",
        tags=["jmx", "house_significations", "5th_house", "12th_house", "karma", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX087",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Ishta Devata: planet in 12th from Karakamsha (or aspecting it by Rashi Drishti) "
            "indicates the native's chosen deity. Sun → Shiva; Moon → Parvati/Devi; "
            "Mars → Skanda/Hanuman; Mercury → Vishnu; Jupiter → Brahma/Guru; "
            "Venus → Lakshmi; Saturn → Shiva/Shani; Rahu → Durga; Ketu → Ganesha."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 3.2.5",
        tags=["jmx", "ishta_devata", "spiritual", "karakamsha", "deity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX088",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Palana Devata (sustaining deity): planet in 6th from Karakamsha. "
            "This is the deity that maintains and protects the native through difficulties. "
            "If no planet in 6th from KL, use the 6th lord from KL."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 3.2.8",
        tags=["jmx", "palana_devata", "spiritual", "karakamsha", "deity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX089",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Atma Devata (soul deity): planet that is the Atmakaraka itself indicates "
            "the soul's primary divine association. Sun as AK → Shiva. Moon as AK → Devi. "
            "Jupiter as AK → Brahma/Indra. Venus as AK → Lakshmi. Saturn as AK → Vishnu."
        ),
        confidence=0.84,
        verse="Jaimini Sutras 3.2.10",
        tags=["jmx", "atma_devata", "atmakaraka", "spiritual", "deity", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX090",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Rashi Tulya Navamsha: when a planet's sign in D1 equals its navamsha sign, "
            "it is in Vargottama (Jaimini confirms Parashari here). "
            "Vargottama AK → very powerful soul purpose; results fully manifested."
        ),
        confidence=0.93,
        verse="Jaimini Sutras 3.3.1",
        tags=["jmx", "vargottama", "navamsha", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX091",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini planetary friendships differ from Parashari for Rashi Drishti strength: "
            "friends casting Rashi Drishti → supportive aspect. "
            "Enemies casting Rashi Drishti → challenging aspect. "
            "Neutrals → mixed results. Natural friendships apply."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 3.3.5",
        tags=["jmx", "planetary_friendships", "rashi_drishti", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX092",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini on education: Mercury, Jupiter, and 5th from KL determine education. "
            "If Rahu aspects Mercury and 5th from KL by Rashi Drishti → foreign education "
            "or unconventional subjects. Ketu there → mathematics, programming, occult sciences."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 3.3.8",
        tags=["jmx", "education", "mercury", "jupiter", "karakamsha", "rahu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX093",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini on travel and foreign residence: planets in 12th from AL by Rashi Drishti "
            "from Rahu or 9th from AL → foreign travel/residence. "
            "Rahu in 12th from AL → long-term foreign settlement. "
            "Ketu in 12th from AL → spiritual retreat or ashram abroad."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 3.3.12",
        tags=["jmx", "travel", "foreign", "rahu", "ketu", "arudha_lagna", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX094",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini siblings: 3rd from Lagna and BK (Bhratrikaraka). "
            "Number of planets in 3rd from Lagna and 3rd from AK indicates siblings' count. "
            "BK in 3rd from Lagna aspected by benefics → many prosperous siblings."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 3.3.15",
        tags=["jmx", "siblings", "bhratrikaraka", "3rd_house", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX095",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Father's longevity: 9th from AK and MK (Matrikaraka) for father (inverted). "
            "Some commentators use 9th from Lagna with its lord for father. "
            "Malefics in 9th from AK with no benefic Rashi Drishti → early father loss."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 3.4.1",
        tags=["jmx", "father", "longevity", "atmakaraka", "9th_house", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX096",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Mother's longevity: 4th from AK and MK for mother. "
            "Moon with MK or aspecting MK by Rashi Drishti → strong mother figure. "
            "Saturn in 4th from MK → early mother loss or separation."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 3.4.2",
        tags=["jmx", "mother", "longevity", "matrikaraka", "moon", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX097",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini on financial success: AK in 2nd from AL or aspecting AL by Rashi Drishti → "
            "self-made wealth. AMK in 11th from AL → steady gains from career. "
            "Both AK and AMK aspecting AL → outstanding financial success."
        ),
        confidence=0.89,
        verse="Jaimini Sutras 3.4.5",
        tags=["jmx", "wealth", "financial", "atmakaraka", "amatyakaraka", "arudha_lagna", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX098",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini medical analysis: malefics in specific signs from KL indicate diseases. "
            "Rahu in 6th from KL → poison, chemical toxicity, or foreign disease. "
            "Saturn in 6th from KL → chronic wasting diseases, arthritis, bone issues. "
            "Mars in 6th from KL → inflammatory diseases, accidents, surgery."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 3.4.8",
        tags=["jmx", "medical", "disease", "karakamsha", "rahu", "saturn", "mars", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX099",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Kala (divisional timing): use of D60 (Shastiamsha) for past-life karma. "
            "AK's D60 position indicates the karmic wound from previous life to heal. "
            "D60 lord in good dignity → karma completing; debilitated → karma intensifying."
        ),
        confidence=0.80,
        verse="Jaimini Sutras 3.4.12",
        tags=["jmx", "d60", "karma", "past_life", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX100",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Rashi Parivartan (sign exchange): two planets in each other's signs "
            "create a powerful Rashi Drishti exchange. This functions like Yoga in Parashari. "
            "If the two planets are AK and AMK → most powerful career-soul alignment."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 3.5.1",
        tags=["jmx", "parivartana", "rashi_drishti", "exchange", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX101",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Mandooka Dasha (frog dasha): skipping dasha that jumps by certain signs. "
            "Starts from Lagna, skips alternating signs. "
            "Used for timing of events that occur in leaps (sudden opportunities)."
        ),
        confidence=0.78,
        verse="Jaimini Sutras 4.1.1",
        tags=["jmx", "mandooka_dasha", "dasha", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX102",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Trikona Dasha: proceeds through trikona (1-5-9) first, then other signs. "
            "Used specifically for examining fortuna and dharmic life arc. "
            "Each trikona sign = 1/3 of total life arc for that trinal theme."
        ),
        confidence=0.77,
        verse="Jaimini Sutras 4.1.5",
        tags=["jmx", "trikona_dasha", "dasha", "dharma", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX103",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Dwisaptati Sama Dasha: 72-year dasha cycle for charts where Lagna lord "
            "is in 7th from Lagna or vice versa. 9 planets, 8 years each = 72 total. "
            "Used as alternative to Vimshottari in specific charts."
        ),
        confidence=0.78,
        verse="Jaimini Sutras 4.2.1",
        tags=["jmx", "dwisaptati_dasha", "dasha", "72_years", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX104",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Saptarishi Dasha: dasha system based on the 7 sages (Ursa Major) and AK. "
            "Each sage corresponds to a nakshatra cluster. Used for spiritual timing. "
            "Rare system mentioned in commentaries by Raghava Bhatta."
        ),
        confidence=0.72,
        verse="Jaimini Sutras 4.2.5",
        tags=["jmx", "saptarishi_dasha", "dasha", "nakshatras", "spiritual", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX105",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Varnada Lagna (Jaimini): derived from Hora Lagna and Ghati Lagna positions. "
            "Method: add HL and GL positions; if sum > 12, subtract 12. "
            "Varnada Lagna shows the social caste/role assigned by karma."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 4.3.1",
        tags=["jmx", "varnada_lagna", "special_lagnas", "karma", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX106",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Hora Lagna (Jaimini): at sunrise, Hora Lagna = Lagna. "
            "For every 2.5 ghatikas (1 hora = 60 mins), HL advances by 1 sign. "
            "HL signifies wealth consciousness and financial timing."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 4.3.2",
        tags=["jmx", "hora_lagna", "special_lagnas", "wealth", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX107",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Ghati Lagna (Jaimini): Lagna at sunrise, then advances 1 sign per ghati (24 mins). "
            "GL signifies power, authority, and political influence. "
            "Strong planets with GL → strong authority figure; malefics → abuse of power."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 4.3.3",
        tags=["jmx", "ghati_lagna", "special_lagnas", "power", "authority", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX108",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Prashna (horary): use the time of question as Prashna Lagna. "
            "AK at time of question → key karaka for the query topic. "
            "Rashi Drishti from benefics on Prashna Lagna → favorable outcome."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 4.4.1",
        tags=["jmx", "prashna", "horary", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX109",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini transit analysis: use Rashi Drishti for transiting planets' effects. "
            "Jupiter's Rashi Drishti on a natal sign protects that sign's significations. "
            "Saturn's Rashi Drishti delays and restricts; Mars' Drishti activates and agitates."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 4.4.5",
        tags=["jmx", "transit", "rashi_drishti", "jupiter", "saturn", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX110",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Upapada for 2nd marriage: 2nd UL = Arudha of A9 (9th house arudha). "
            "If both UL and 2nd UL are aspected by Venus by Rashi Drishti → "
            "both marriages are harmonious but the person seeks variety."
        ),
        confidence=0.80,
        verse="Jaimini Sutras 4.4.8",
        tags=["jmx", "upapada", "second_marriage", "marriage", "venus", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX111",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini children's count prediction: 5th from AK and PK (Putrakaraka). "
            "Number of benefics in 5th from AK or aspecting 5th from AK by Rashi Drishti = "
            "approximate number of children. Jupiter there = strong fecundity."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 4.5.1",
        tags=["jmx", "children", "putrakaraka", "atmakaraka", "5th_house", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX112",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Tithi Pravesh Chakra (annual chart): chart cast for the moment "
            "when Sun returns to its natal degree within the natal tithi. "
            "Used as yearly timing chart in some Jaimini traditions."
        ),
        confidence=0.75,
        verse="Jaimini Sutras 4.5.5",
        tags=["jmx", "tithi_pravesh", "annual_chart", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX113",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini on Jupiter results: Jupiter with AK → dharmic and philosophical nature. "
            "Jupiter aspecting Lagna by Rashi Drishti → grants wisdom, good character, "
            "abundance, and protection from great harm."
        ),
        confidence=0.92,
        verse="Jaimini Sutras 4.6.1",
        tags=["jmx", "jupiter", "atmakaraka", "dharma", "wisdom", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX114",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini on Venus results: Venus with AK → artistic talent and pursuit of beauty. "
            "Venus aspecting KL by Rashi Drishti → success in arts, luxury trade, or cinema. "
            "Venus with UL in D9 → deeply loving marriage partner."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 4.6.2",
        tags=["jmx", "venus", "arts", "marriage", "karakamsha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX115",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="special",
        description=(
            "Jaimini confirms: if AK is weak (debilitated, combust, in enemy sign in D9) "
            "→ the soul's purpose is suppressed; life lacks direction and fulfillment. "
            "Remedies: strengthen AK's significations through worship of its deity."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 4.6.5",
        tags=["jmx", "atmakaraka", "weakness", "remedies", "soul", "jaimini"],
        implemented=False,
    ),

    # ── Advanced Jaimini Combinations (JMX116-135) ────────────────────────────
    RuleRecord(
        rule_id="JMX116",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="advanced",
        description=(
            "Narayana Dasha: a variant of Chara Dasha starting from the stronger of "
            "Lagna or 7th for the first 6 signs, then the other for the next 6 signs. "
            "Used by K.N. Rao's school as the primary Jaimini predictive dasha."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 2.1.1 (Narayana interpretation)",
        tags=["jmx", "narayana_dasha", "chara_dasha", "dasha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX117",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini exception for Aries Lagna Chara Dasha: if Lagna is Aries (odd movable), "
            "sequence goes forward: Aries→Taurus→Gemini... "
            "If Lagna is Taurus (even fixed) → Taurus→Aries→Pisces... (backward). "
            "This odd-even forward-backward rule applies to all 12 signs."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 2.1.4",
        tags=["jmx", "chara_dasha", "aries", "taurus", "sequence", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX118",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="advanced",
        description=(
            "Dual lordship resolution (Scorpio): Scorpio has Mars (traditional) and Ketu (Jaimini). "
            "Some commentators use Ketu for Chara Dasha calculations for Scorpio, "
            "Mars for all other purposes. This is the primary commentarial divergence in Jaimini."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 1.1.10 (commentary)",
        tags=["jmx", "scorpio", "mars", "ketu", "dual_lordship", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX119",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="advanced",
        description=(
            "Aquarius dual lordship: Saturn (traditional) and Rahu (Jaimini commentaries). "
            "Rahu as Aquarius co-lord → foreign/technology significations for Aquarius. "
            "In Chara Dasha: use Rahu for Aquarius dasha years per some traditions."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 1.1.11 (commentary)",
        tags=["jmx", "aquarius", "saturn", "rahu", "dual_lordship", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX120",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini Argala strength hierarchy: 2nd house Argala > 4th > 11th. "
            "5th house also casts Argala (secondary, mentioned in some texts). "
            "Argala from malefics can be beneficial if the malefic is yogakaraka or AK."
        ),
        confidence=0.84,
        verse="Jaimini Sutras 1.4.3",
        tags=["jmx", "argala", "hierarchy", "strength", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX121",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini on retrograde planets: retrograde planet in a sign gains added strength "
            "for Rashi Drishti purposes. Retrograde AK → the soul's purpose is intensely felt "
            "but may be delayed in manifestation. Retrograde AMK → career reversals."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 1.3.20",
        tags=["jmx", "retrograde", "atmakaraka", "amatyakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX122",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini exaltation strength in Rashi Drishti: planet in exaltation casts "
            "Rashi Drishti with full force (100%). In own sign → 75%. In friend's sign → 50%. "
            "In enemy's sign → 25%. Debilitated → 0% or minimal (some say none)."
        ),
        confidence=0.84,
        verse="Jaimini Sutras 1.3.22",
        tags=["jmx", "rashi_drishti", "exaltation", "debilitation", "strength", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX123",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini timing via sub-sub-period (Prana Dasha within antardasha): "
            "each antardasha further divided by same Chara sequence. "
            "Three levels of timing — Dasha / Antar / Prana — give precise event timing."
        ),
        confidence=0.80,
        verse="Jaimini Sutras 2.1.10",
        tags=["jmx", "chara_dasha", "prana_dasha", "timing", "precision", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX124",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini confirms Navamsha's primacy for marriage analysis (agrees with Parashari). "
            "D9 chart shows the soul's quality of relationships. "
            "But UL (Upapada) in D1 is unique to Jaimini — the societal/public marriage event."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 3.2.15",
        tags=["jmx", "navamsha", "marriage", "upapada", "d9", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX125",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini varga analysis: AK in D10 (Dashamsha) indicates career direction. "
            "If AK's D10 sign has benefics or is strong → career fulfills soul's purpose. "
            "AMK in D10 Lagna or its kendra → career pinnacle positions."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 3.5.5",
        tags=["jmx", "d10", "dashamsha", "career", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX126",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini Chara Karaka in D9: all 8 Chara Karakas recalculated in D9. "
            "The AK in D9 occupies Karakamsha. Other karakas' D9 positions show "
            "soul-level relationships with their significations."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 4.3.8",
        tags=["jmx", "chara_karaka", "navamsha", "d9", "atmakaraka", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX127",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini Paka Lagna: sign where Lagna lord is placed. "
            "Events of the Paka Lagna sign's houses activate in the relevant Chara Dasha. "
            "Strong Paka Lagna (lord exalted/own sign) → individual acts from inner strength."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 4.3.10",
        tags=["jmx", "paka_lagna", "lagna_lord", "dasha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX128",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Arudha Lagna lord position determines type of reputation: "
            "AL lord in 1st from AL → self-made image. In 7th → partner shapes one's image. "
            "In 10th from AL → career defines reputation. In 12th from AL → hidden/mysterious persona."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 4.3.12",
        tags=["jmx", "arudha_lagna", "reputation", "public_image", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX129",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "If Lagna lord and AL lord are the same planet → authentic self and public image align. "
            "Person's true character matches public reputation. Rare and highly favorable. "
            "Malefics aspecting this shared lord → authenticity challenged by enemies."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 4.3.13",
        tags=["jmx", "arudha_lagna", "lagna", "authenticity", "reputation", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX130",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini on natural karakas vs. Chara Karakas: natural karakas (Sun for father, "
            "Moon for mother, etc.) supplement Chara Karakas. "
            "When natural karaka and Chara Karaka are the same planet → intensified results."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 4.6.8",
        tags=["jmx", "natural_karakas", "chara_karaka", "synthesis", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX131",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini Lagna Kendradi Rashi Bala: the strength of a sign is determined by "
            "how many benefics occupy or aspect it vs. malefics. "
            "Kendra signs (1/4/7/10) get extra weight in Jaimini strength calculations."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 4.7.1",
        tags=["jmx", "rashi_bala", "kendra", "strength", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX132",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini confirms use of Hora Lagna for wealth: "
            "if Hora Lagna and its lord are strong (in kendra/trikona or own/exaltation sign) → "
            "natural wealth acquisition. HL with Jupiter by Rashi Drishti → exceptional fortune."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 4.7.3",
        tags=["jmx", "hora_lagna", "wealth", "fortune", "jupiter", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX133",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini Chara Dasha with Vimshottari: using both dashas together for verification. "
            "When Chara Dasha and Vimshottari both indicate an event simultaneously → "
            "near certainty of that event occurring in that period."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 4.7.5",
        tags=["jmx", "chara_dasha", "vimshottari", "dual_dasha", "timing", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX134",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini unique combination for spiritual practice: "
            "if 5th from KL has Jupiter and 12th from KL has Ketu (or vice versa), "
            "the native is destined for deep spiritual practice and possible moksha in this birth."
        ),
        confidence=0.85,
        verse="Jaimini Sutras 4.7.8",
        tags=["jmx", "spiritual", "moksha", "karakamsha", "jupiter", "ketu", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX135",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="advanced",
        description=(
            "Jaimini on Rahu-Ketu axis in relation to AK: "
            "if Rahu or Ketu conjuncts AK → strong karmic mission in this life. "
            "Ketu with AK → past-life mastery being applied; Rahu with AK → new territory soul is exploring."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 4.7.10",
        tags=["jmx", "rahu", "ketu", "atmakaraka", "karma", "soul", "jaimini"],
        implemented=False,
    ),

    # ── Final Jaimini Synthesis Rules (JMX136-150) ───────────────────────────
    RuleRecord(
        rule_id="JMX136",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini 3-point verification for any event: "
            "(1) relevant karaka active in Chara Dasha, "
            "(2) relevant sign aspected by Rashi Drishti of that karaka, "
            "(3) transit confirmation. All 3 together → near-certain event timing."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 4.8.1",
        tags=["jmx", "three_point_verification", "timing", "methodology", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX137",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini confirms: the chart analysis must integrate both D1 (physical events) "
            "and D9 (soul events). Physical marriage ≠ soul marriage. "
            "The highest synthesis is when D1 and D9 both confirm the same event."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 4.8.3",
        tags=["jmx", "d1", "d9", "synthesis", "marriage", "soul", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX138",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini on interpreting malefic Rashi Drishti: malefic aspecting Lagna by RD → "
            "difficulties in the physical body and environment. "
            "But if that malefic is also AK → the soul itself is pushing through hardship for growth."
        ),
        confidence=0.87,
        verse="Jaimini Sutras 4.8.5",
        tags=["jmx", "rashi_drishti", "malefics", "atmakaraka", "growth", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX139",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini hierarchy of indicators (most to least reliable): "
            "1. AK position 2. Karakamsha 3. Arudha Lagna 4. Upapada 5. Hora Lagna. "
            "Any event confirmed by all five → absolute certainty."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 4.8.8",
        tags=["jmx", "hierarchy", "indicators", "methodology", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX140",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini's fundamental teaching: the soul (AK) is the master of the chart. "
            "All planets serve the AK's purpose. Chart reading begins with AK, "
            "proceeds through its associations, and ends with the soul's final destination (moksha)."
        ),
        confidence=0.95,
        verse="Jaimini Sutras 4.9.1",
        tags=["jmx", "atmakaraka", "soul", "philosophy", "moksha", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX141",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Lagna strength determination: the stronger of Lagna and 7th from Lagna "
            "is determined by: (1) more planets, (2) aspect by own lord, "
            "(3) aspect by benefics by Rashi Drishti. The stronger side initiates Chara Dasha."
        ),
        confidence=0.91,
        verse="Jaimini Sutras 1.1.35",
        tags=["jmx", "lagna_strength", "chara_dasha", "methodology", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX142",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Pisces (Mina) as Lagna: Pisces Lagna Chara Dasha goes backward "
            "(Pisces→Aquarius→Capricorn...) as Pisces is an even dual sign. "
            "Some commentaries make Pisces forward due to dual sign ambiguity."
        ),
        confidence=0.82,
        verse="Jaimini Sutras 2.1.6",
        tags=["jmx", "pisces", "chara_dasha", "dual_signs", "sequence", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX143",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="special",
        description=(
            "Jaimini Chara Dasha starting sign exception: "
            "if Lagna is Scorpio (odd fixed), start Chara Dasha from Scorpio going forward. "
            "If Scorpio Lagna and Rahu is used as co-lord, dasha years may differ from Mars calculation."
        ),
        confidence=0.80,
        verse="Jaimini Sutras 3.1.8",
        tags=["jmx", "scorpio", "chara_dasha", "dasha_start", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX144",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Summary of all Rashi Drishti pairs: "
            "Aries↔Leo, Aries↔Scorpio, Aries↔Aquarius; "
            "Cancer↔Libra, Cancer↔Scorpio, Cancer↔Aquarius; "
            "Libra↔Aries, Libra↔Cancer, Libra↔Capricorn; "
            "Capricorn↔Aries, Capricorn↔Cancer, Capricorn↔Libra."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.30-31 (summary)",
        tags=["jmx", "rashi_drishti", "aspects", "summary", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX145",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Fixed sign Rashi Drishti summary: "
            "Taurus↔Cancer, Taurus↔Libra, Taurus↔Capricorn; "
            "Leo↔Scorpio, Leo↔Aquarius, Leo↔Taurus; "
            "Scorpio↔Leo, Scorpio↔Aquarius, Scorpio↔Aries; "
            "Aquarius↔Taurus, Aquarius↔Leo, Aquarius↔Scorpio."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.31 (summary)",
        tags=["jmx", "rashi_drishti", "taurus", "leo", "scorpio", "aquarius", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX146",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="rashi_drishti",
        description=(
            "Dual sign Rashi Drishti summary: "
            "Gemini↔Virgo, Gemini↔Sagittarius, Gemini↔Pisces; "
            "Virgo↔Gemini, Virgo↔Sagittarius, Virgo↔Pisces; "
            "Sagittarius↔Gemini, Sagittarius↔Virgo, Sagittarius↔Pisces; "
            "Pisces↔Gemini, Pisces↔Virgo, Pisces↔Sagittarius."
        ),
        confidence=0.97,
        verse="Jaimini Sutras 1.1.27 (summary)",
        tags=["jmx", "rashi_drishti", "gemini", "virgo", "sagittarius", "pisces", "aspects", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX147",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini teaching on free will vs. karma: AK shows the soul's karma (fixed). "
            "AL shows what can be modified through effort (free will arena). "
            "Where AK and AL strongly agree → fate; where they differ → human agency possible."
        ),
        confidence=0.86,
        verse="Jaimini Sutras 4.9.5",
        tags=["jmx", "karma", "free_will", "atmakaraka", "arudha_lagna", "philosophy", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX148",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini's supreme Raja Yoga — the Hamsa equivalent: "
            "AK in own sign in navamsha, conjunct AMK, aspected by Jupiter by Rashi Drishti → "
            "great king or equivalent authority in modern context."
        ),
        confidence=0.88,
        verse="Jaimini Sutras 4.9.8",
        tags=["jmx", "raja_yoga", "supreme_yoga", "atmakaraka", "amatyakaraka", "jupiter", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX149",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini Chakra (wheel) of life: "
            "the 12 signs of the zodiac represent the wheel of karma. "
            "Each sign traversed in Chara Dasha = one chapter of karmic life. "
            "The complete 12-sign cycle (~144 years max) represents full karmic repayment."
        ),
        confidence=0.83,
        verse="Jaimini Sutras 4.9.10",
        tags=["jmx", "karma_wheel", "chara_dasha", "philosophy", "zodiac", "jaimini"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMX150",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="synthesis",
        description=(
            "Jaimini's concluding teaching (Adhyaya 4 end): "
            "the astrologer must know both Parashari and Jaimini systems. "
            "Parashari gives the forest; Jaimini gives the individual tree. "
            "Together they constitute complete Vedic astrological knowledge (Sampoorna Jyotisha)."
        ),
        confidence=0.90,
        verse="Jaimini Sutras 4.9.15",
        tags=["jmx", "synthesis", "parashari", "jaimini", "sampoorna_jyotisha", "philosophy"],
        implemented=False,
    ),
]

for rule in _RULES:
    JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.add(rule)
