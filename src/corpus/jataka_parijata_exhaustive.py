"""
src/corpus/jataka_parijata_exhaustive.py — Jataka Parijata Exhaustive (S257)

Exhaustive encoding of Vaidyanatha Dikshita's Jataka Parijata (14th century CE).
Covers all 18 chapters: planet/rashi natures, dignities, house significations,
yogas, dashas, longevity, muhurta, and advanced combinations.

Total: ~150 rules (JPX001–JPX150)
All: implemented=False, school="parashari", source="JatakaParijata"
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # CH.1 — PLANET NATURES AND CHARACTERISTICS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX001", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Sun: Male, Sattvic, Kshatriya, Agni (fire) element, lord of Leo, "
            "exalted Aries 10°, debilitated Libra 10°, gold/copper metals, "
            "bitter taste, red/golden color, square shape, mid-age, rules East. "
            "Governs: soul, father, bones, heart, right eye, vitality.",
        confidence=0.92, verse="JP Ch.1 v.1-8",
        tags=["jp", "sun", "graha_nature", "male", "sattvic", "fire", "leo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX002", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Moon: Female, Sattvic-Tamasic mix, Vaishya, Water element, lord of Cancer, "
            "exalted Taurus 3°, debilitated Scorpio 3°, silver/white metal, "
            "salty taste, white/pale color, round shape, youth, rules NW. "
            "Governs: mind, mother, blood, left eye, breasts, water.",
        confidence=0.92, verse="JP Ch.1 v.9-16",
        tags=["jp", "moon", "graha_nature", "female", "water", "cancer"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX003", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Mars: Male, Tamasic, Kshatriya, Fire element, lord of Aries+Scorpio, "
            "exalted Capricorn 28°, debilitated Cancer 28°, copper/iron, "
            "pungent/bitter taste, red color, rules South. "
            "Governs: courage, brothers, land, blood, muscles, surgery.",
        confidence=0.92, verse="JP Ch.1 v.17-24",
        tags=["jp", "mars", "graha_nature", "male", "tamasic", "fire", "aries_scorpio"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX004", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Mercury: Neuter/Mixed, Rajasic, Vaishya, Earth+Air element, "
            "lord of Gemini+Virgo, exalted Virgo 15°, debilitated Pisces 15°. "
            "Green color, mixed taste, rules North. "
            "Governs: intelligence, speech, trade, skin, nerves, youth.",
        confidence=0.92, verse="JP Ch.1 v.25-32",
        tags=["jp", "mercury", "graha_nature", "neuter", "earth_air", "gemini_virgo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX005", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Jupiter: Male, Sattvic, Brahmin, Ether/Space element, "
            "lord of Sagittarius+Pisces, exalted Cancer 5°, debilitated Capricorn 5°. "
            "Yellow/gold color, sweet taste, rules NE. "
            "Governs: wisdom, children, wealth, liver, thighs, fat.",
        confidence=0.92, verse="JP Ch.1 v.33-40",
        tags=["jp", "jupiter", "graha_nature", "male", "sattvic", "brahmin", "ether"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX006", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Venus: Female, Rajasic, Brahmin, Water+Air element, "
            "lord of Taurus+Libra, exalted Pisces 27°, debilitated Virgo 27°. "
            "White/variegated color, sour taste, rules SE. "
            "Governs: love, wife, vehicles, semen, kidney, face.",
        confidence=0.92, verse="JP Ch.1 v.41-48",
        tags=["jp", "venus", "graha_nature", "female", "rajasic", "water_air"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX007", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Saturn: Neuter/Male, Tamasic, Shudra, Air/Vata element, "
            "lord of Capricorn+Aquarius, exalted Libra 20°, debilitated Aries 20°. "
            "Black/dark color, astringent taste, rules West. "
            "Governs: longevity, sorrow, servants, nerves, spleen.",
        confidence=0.92, verse="JP Ch.1 v.49-56",
        tags=["jp", "saturn", "graha_nature", "tamasic", "shudra", "air_vata"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX008", source="JatakaParijata", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Rahu and Ketu: Shadow planets without physical bodies. "
            "Rahu: SW direction, smoky/dark, like Saturn in effect, Aquarius-like. "
            "Ketu: NW direction, like Mars in effect, Scorpio-like. "
            "Both are Tamasic and intensify whatever sign/planet they occupy. "
            "Joint Rahu-Ketu axis = karmic axis of the chart.",
        confidence=0.88, verse="JP Ch.1 v.57-64",
        tags=["jp", "rahu", "ketu", "shadow_planet", "karmic_axis", "tamasic"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.2 — RASHI CHARACTERISTICS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX009", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Aries: Movable, Fiery, Male, Head/Face of Kalapurusha, ruled by Mars. "
            "Productive in east, active at night/rising time. "
            "Quadruped, pitta constitution, short ascension in N hemisphere. "
            "Persons: courageous, impulsive, ambitious, initiating.",
        confidence=0.90, verse="JP Ch.2 v.1-6",
        tags=["jp", "aries", "movable", "fiery", "male", "mars_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX010", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Taurus: Fixed, Earthy, Female, ruled by Venus. "
            "South direction, productive when Sun in south. "
            "Quadruped, Kapha constitution. Long ascension. "
            "Persons: stable, possessive, artistic, sensual, reliable.",
        confidence=0.90, verse="JP Ch.2 v.7-12",
        tags=["jp", "taurus", "fixed", "earthy", "female", "venus_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX011", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Gemini: Dual/Mutable, Airy, Male, ruled by Mercury. "
            "West direction, productive in air. Biped, Vata constitution. "
            "Long ascension. Persons: communicative, adaptable, intellectual, dual-natured.",
        confidence=0.90, verse="JP Ch.2 v.13-18",
        tags=["jp", "gemini", "dual", "airy", "male", "mercury_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX012", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Cancer: Movable, Watery, Female, ruled by Moon. "
            "North direction, productive in water. "
            "Many-footed/crustacean. Kapha constitution. Short ascension. "
            "Persons: nurturing, emotional, family-oriented, intuitive.",
        confidence=0.90, verse="JP Ch.2 v.19-24",
        tags=["jp", "cancer", "movable", "watery", "female", "moon_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX013", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Leo: Fixed, Fiery, Male, ruled by Sun. "
            "East direction, productive in forest/mountains. "
            "Quadruped. Pitta constitution. Long ascension. "
            "Persons: authoritative, proud, generous, leadership-oriented.",
        confidence=0.90, verse="JP Ch.2 v.25-30",
        tags=["jp", "leo", "fixed", "fiery", "male", "sun_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX014", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Virgo: Dual/Mutable, Earthy, Female, ruled by Mercury. "
            "South direction, biped (holds grain and fire). "
            "Vata-Pitta mix. Long ascension. "
            "Persons: analytical, critical, service-oriented, health-conscious.",
        confidence=0.90, verse="JP Ch.2 v.31-36",
        tags=["jp", "virgo", "dual", "earthy", "female", "mercury_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX015", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Libra: Movable, Airy, Male, ruled by Venus. "
            "West direction, biped (marketplace/scales). "
            "Vata constitution. Long ascension. "
            "Persons: balanced, diplomatic, justice-seeking, partnership-oriented.",
        confidence=0.90, verse="JP Ch.2 v.37-42",
        tags=["jp", "libra", "movable", "airy", "male", "venus_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX016", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Scorpio: Fixed, Watery, Female, ruled by Mars. "
            "North direction, many-footed/insect-like. "
            "Kapha-Pitta mix. Short ascension. "
            "Persons: intense, transformative, secretive, investigative, resilient.",
        confidence=0.90, verse="JP Ch.2 v.43-48",
        tags=["jp", "scorpio", "fixed", "watery", "female", "mars_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX017", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Sagittarius: Dual/Mutable, Fiery, Male, ruled by Jupiter. "
            "East direction, biped front/quadruped back (centaur). "
            "Pitta constitution. Long ascension. "
            "Persons: philosophical, adventurous, ethical, freedom-loving.",
        confidence=0.90, verse="JP Ch.2 v.49-54",
        tags=["jp", "sagittarius", "dual", "fiery", "male", "jupiter_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX018", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Capricorn: Movable, Earthy, Female, ruled by Saturn. "
            "South direction, part quadruped/part aquatic. "
            "Vata constitution. Short ascension. "
            "Persons: ambitious, disciplined, practical, status-seeking.",
        confidence=0.90, verse="JP Ch.2 v.55-60",
        tags=["jp", "capricorn", "movable", "earthy", "female", "saturn_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX019", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Aquarius: Fixed, Airy, Male, ruled by Saturn. "
            "West direction, biped (holds pot of water). "
            "Vata constitution. Long ascension. "
            "Persons: humanitarian, progressive, unconventional, intellectual.",
        confidence=0.90, verse="JP Ch.2 v.61-66",
        tags=["jp", "aquarius", "fixed", "airy", "male", "saturn_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX020", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Pisces: Dual/Mutable, Watery, Female, ruled by Jupiter. "
            "North direction, two fish swimming in opposite directions. "
            "Kapha constitution. Short ascension. "
            "Persons: compassionate, intuitive, mystical, adaptable, dissolving.",
        confidence=0.90, verse="JP Ch.2 v.67-72",
        tags=["jp", "pisces", "dual", "watery", "female", "jupiter_ruled"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.3 — DIGNITIES AND PLANETARY STRENGTHS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX021", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="JP Dignities Hierarchy: Exaltation (Uccha) > Own Sign (Swa) > "
            "Great Friend's sign > Friend's sign > Neutral sign > Enemy sign > "
            "Debilitation (Neecha). Planet in Moolatrikona = near own sign strength. "
            "Moolatrikona: Sun (Leo 0-20°), Moon (Taurus 4-20°), Mars (Aries 0-12°), "
            "Mercury (Virgo 15-20°), Jupiter (Sag 0-10°), Venus (Libra 0-15°), Saturn (Aquarius 0-20°).",
        confidence=0.93, verse="JP Ch.3 v.1-10",
        tags=["jp", "dignity", "moolatrikona", "exaltation", "own_sign", "hierarchy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX022", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Neecha Bhanga (JP full rules): Debilitation cancelled when: "
            "1) Lord of debilitation sign in kendra from lagna/Moon. "
            "2) Lord of exaltation sign in kendra from lagna/Moon. "
            "3) Debilitated planet in kendra from lagna. "
            "4) Debilitated planet aspected by its dispositor. "
            "5) Debilitated planet with exalted planet. "
            "6) Exchange between debilitated and exalted planets. "
            "7) Debilitated planet in own navamsha.",
        confidence=0.93, verse="JP Ch.3 v.11-22",
        tags=["jp", "neecha_bhanga", "debilitation_cancellation", "7_conditions"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX023", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Planetary Friendship Classification (JP): "
            "Natural friends: Sun-Moon-Mars-Jupiter. "
            "Sun's enemies: Venus+Saturn. Jupiter's enemies: Mercury+Venus. "
            "Mars's enemies: Mercury. Saturn's friends: Mercury+Venus. "
            "Mercury's neutral: Sun. Venus's neutral: Jupiter+Saturn. "
            "Temporary friendship: planets in signs 2/3/4/10/11/12 from each other.",
        confidence=0.92, verse="JP Ch.3 v.23-34",
        tags=["jp", "friendship", "natural_friends", "enemies", "temporary_friendship"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX024", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Dig Bala (Directional Strength) in JP: "
            "Sun and Mars: maximum in 10th (South). "
            "Moon and Venus: maximum in 4th (North). "
            "Mercury and Jupiter: maximum in 1st (East). "
            "Saturn: maximum in 7th (West). "
            "Opposite house = zero Dig Bala. "
            "Dig Bala is proportional between these extremes.",
        confidence=0.93, verse="JP Ch.3 v.35-44",
        tags=["jp", "dig_bala", "directional_strength", "10th", "4th", "1st", "7th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX025", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Vargottama Definition (JP): A planet occupying the same rashi in both "
            "D1 (natal) and D9 (navamsha) is Vargottama (exalted in its division). "
            "Vargottama planet = permanently strong, reliable throughout dashas. "
            "Even a debilitated Vargottama becomes moderate in effect.",
        confidence=0.93, verse="JP Ch.3 v.45-52",
        tags=["jp", "vargottama", "d1_d9_same", "permanent_strength"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.4 — HOUSE ANALYSIS (BHAVA PHALA)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX026", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="1st House (JP): Lagna = the entire chart's foundation. "
            "JP emphasizes: strong lagna lord = strong native regardless of other factors. "
            "Lagna in movable sign = dynamic, initiating life. "
            "Lagna in fixed sign = stable, accumulating life. "
            "Lagna in dual sign = dual or complex life experiences.",
        confidence=0.90, verse="JP Ch.4 v.1-8",
        tags=["jp", "1st_house", "lagna", "movable", "fixed", "dual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX027", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="2nd House (JP): Dhana Bhava. "
            "Benefics in 2nd = eloquent speech, truthful, wealthy. "
            "Malefics in 2nd (especially Saturn) = harsh speech, delayed wealth. "
            "Moon in 2nd = poetic speech, income from public. "
            "Jupiter in 2nd = Saraswati placement, wisdom and wealth combined.",
        confidence=0.90, verse="JP Ch.4 v.9-16",
        tags=["jp", "2nd_house", "dhana", "speech", "jupiter_2nd", "moon_2nd"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX028", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="5th House (JP): Putra Bhava. "
            "JP unique: 5th house for past merit (Poorvapunya) emphasized strongly. "
            "Jupiter in 5th = Hamsa-like placement for wisdom and children. "
            "5th lord strong + Jupiter strong = children and intellect both blessed. "
            "Mars in 5th = surgical mind or first child delayed.",
        confidence=0.90, verse="JP Ch.4 v.17-26",
        tags=["jp", "5th_house", "putra", "poorvapunya", "jupiter_5th", "mars_5th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX029", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="7th House (JP): Kalatra Bhava — marriage analysis emphasis. "
            "JP: examine 7th lord, Venus, and navamsha 7th simultaneously. "
            "Malefics in 7th without benefic aspect = troubled marriage. "
            "Venus in 7th = beautiful spouse but potential for excess pleasure. "
            "7th lord in 7th = spouse-focused, dependent nature.",
        confidence=0.90, verse="JP Ch.4 v.27-36",
        tags=["jp", "7th_house", "marriage", "venus_7th", "navamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX030", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="9th House (JP): Dharma Bhava — the house of fortune. "
            "JP: 9th house represents both father and guru simultaneously. "
            "Jupiter in 9th = Dharmakarmadhipati Yoga potential. "
            "Sun in 9th = government/authority favor. "
            "9th lord in 5th or 5th lord in 9th = Dharma-Karma exchange = great fortune.",
        confidence=0.90, verse="JP Ch.4 v.37-46",
        tags=["jp", "9th_house", "dharma", "father", "guru", "fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX031", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="10th House (JP): Karma Bhava — career and action. "
            "JP: 10th must be assessed from lagna, Moon, and Sun. "
            "If all three show 10th strong = definitive career success. "
            "Two of three strong = substantial career. "
            "Planet in 10th most powerful by Dig Bala (except Saturn and Moon).",
        confidence=0.90, verse="JP Ch.4 v.47-56",
        tags=["jp", "10th_house", "karma", "career", "triple_10th_assessment"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.5 — PLANETARY RESULTS IN HOUSES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX032", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Sun in Houses (JP): "
            "1st: strong body, arrogant, father problems, eye issues. "
            "4th: mother suffers, property disputes, unhappy home. "
            "5th: intelligent, few children. "
            "7th: wife suffers, traveling spouse. "
            "9th: lucky, father honored, dharmic. "
            "10th: extremely successful career, kingly.",
        confidence=0.88, verse="JP Ch.5 v.1-12",
        tags=["jp", "sun", "graha_bhava", "all_houses", "house_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX033", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Moon in Houses (JP): "
            "1st: beautiful, popular, emotional, mother-focused. "
            "2nd: wealthy through public, good family life. "
            "4th: Dig Bala, happy home, mother blessed. "
            "7th: romantic, many relationships. "
            "8th: inherited wealth, longevity concerns. "
            "10th: public career, mother helps career.",
        confidence=0.88, verse="JP Ch.5 v.13-24",
        tags=["jp", "moon", "graha_bhava", "all_houses", "house_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX034", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Mars in Houses (JP): "
            "1st: energetic, aggressive, accident-prone. "
            "2nd: harsh speech, financial conflicts. "
            "4th: property/mother issues (Mangal Dosha position). "
            "7th: Mangal Dosha — impulsive marriage, partner conflicts. "
            "8th: longevity concerns, hidden enemies. "
            "12th: Mangal Dosha — bedroom issues.",
        confidence=0.88, verse="JP Ch.5 v.25-36",
        tags=["jp", "mars", "graha_bhava", "mangal_dosha", "all_houses"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX035", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Jupiter in Houses (JP): "
            "1st: Dig Bala, wisdom, good health, respected. "
            "4th: happy home, property, nurturing mother. "
            "5th: many children, brilliant intellect. "
            "7th: virtuous spouse, happy marriage. "
            "9th: religious, father blessed, great fortune. "
            "11th: massive gains, wealthy friends.",
        confidence=0.88, verse="JP Ch.5 v.37-48",
        tags=["jp", "jupiter", "graha_bhava", "all_houses", "benefic_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX036", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Venus in Houses (JP): "
            "1st: beautiful, artistic, charming. "
            "4th: Dig Bala, luxurious home, vehicles. "
            "5th: romantic, creative children. "
            "7th: beautiful spouse, pleasure-seeking. "
            "10th: arts-based career, entertainment. "
            "12th: bed comforts, spiritual inclination.",
        confidence=0.88, verse="JP Ch.5 v.49-60",
        tags=["jp", "venus", "graha_bhava", "all_houses", "benefic_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX037", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Saturn in Houses (JP): "
            "1st: lean body, disciplined, isolated childhood. "
            "3rd: brave siblings, self-made. "
            "7th: Dig Bala, delayed/troubled marriage. "
            "10th: slow but steady career, politics. "
            "11th: massive gains after 36 years. "
            "12th: spiritual seeker, foreign residence.",
        confidence=0.88, verse="JP Ch.5 v.61-72",
        tags=["jp", "saturn", "graha_bhava", "all_houses", "delay"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.6 — RAJA YOGA (JP'S MOST FAMOUS CONTRIBUTION)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX038", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Raja Yoga Foundation (JP): Kendra lord + trikona lord relationship. "
            "Any form of association (conjunction/aspect/exchange) between them = Raja Yoga. "
            "Strongest Raja Yoga: 1st lord + 9th lord or 1st lord + 5th lord. "
            "10th lord + 9th lord = Dharmakarmadhipati = peak Raja Yoga.",
        confidence=0.95, verse="JP Ch.6 v.1-8",
        tags=["jp", "yoga", "raja_yoga", "kendra_trikona", "dharmakarmadhipati"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX039", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Multiple Raja Yoga Combinations (JP): "
            "Each lagna produces specific Raja Yogas. "
            "Aries: Mars+Jupiter conjunction. "
            "Taurus: Venus+Saturn. "
            "Gemini: Mercury+Venus. "
            "Cancer: Moon+Jupiter. "
            "Leo: Sun+Jupiter. "
            "JP lists all 12 lagna-specific Raja Yoga planets.",
        confidence=0.90, verse="JP Ch.6 v.9-22",
        tags=["jp", "yoga", "raja_yoga", "lagna_specific", "yoga_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX040", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Yoga Karaka Planet (JP): For certain lagnas, one planet alone creates "
            "Raja Yoga by ruling both kendra and trikona simultaneously. "
            "Capricorn and Aquarius lagnas: Venus = Yoga Karaka. "
            "Cancer and Leo lagnas: Mars = Yoga Karaka. "
            "Taurus and Libra lagnas: Saturn = Yoga Karaka. "
            "These Yoga Karaka planets give Raja Yoga results in their dashas.",
        confidence=0.95, verse="JP Ch.6 v.23-32",
        tags=["jp", "yoga", "yoga_karaka", "single_planet_yoga", "capricorn_aquarius"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX041", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Viparita Raja Yoga (JP Full): Three types: "
            "Harsha Yoga: 6th lord in 6th/8th/12th = victory over enemies, service success. "
            "Sarala Yoga: 8th lord in 6th/8th/12th = long life, hidden gains. "
            "Vimala Yoga: 12th lord in 6th/8th/12th = spiritual freedom, moksha tendency. "
            "JP: all three simultaneously = great liberation and material success.",
        confidence=0.93, verse="JP Ch.6 v.33-44",
        tags=["jp", "yoga", "viparita_raja_yoga", "harsha", "sarala", "vimala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX042", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Pancha Mahapurusha Yoga (JP): "
            "Ruchaka: Mars in Aries/Scorpio/Capricorn in kendra = military/athletic greatness. "
            "Bhadra: Mercury in Gemini/Virgo in kendra = intellectual supremacy. "
            "Hamsa: Jupiter in Cancer/Sagittarius/Pisces in kendra = wisdom/spiritual greatness. "
            "Malavya: Venus in Taurus/Libra/Pisces in kendra = beauty/artistic fame. "
            "Shasha: Saturn in Capricorn/Aquarius/Libra in kendra = administrative power.",
        confidence=0.95, verse="JP Ch.6 v.45-60",
        tags=["jp", "yoga", "mahapurusha", "ruchaka", "bhadra", "hamsa", "malavya", "shasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX043", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Nabhasa Yogas (JP): Shape yogas based on planet distribution. "
            "Rajju: planets only in movable signs = roving, travel-prone life. "
            "Musala: planets only in fixed signs = stability, stubbornness, accumulation. "
            "Nala: planets only in mutable signs = versatility, indecision. "
            "Sreeka: triangle pattern = auspicious, balanced. "
            "Srik: straight line = direct, single-minded.",
        confidence=0.88, verse="JP Ch.6 v.61-76",
        tags=["jp", "yoga", "nabhasa_yoga", "rajju", "musala", "nala", "sreeka"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.7 — DHANA YOGA (WEALTH COMBINATIONS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX044", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Dhana Yoga Combinations (JP): "
            "2nd lord + 11th lord association = primary Dhana Yoga. "
            "5th lord + 9th lord = Lakshmi Yoga (fortune-wealth connection). "
            "2nd lord exalted in 11th = maximum wealth accumulation. "
            "11th lord in 2nd = income converts to savings. "
            "Jupiter in 2nd/5th/9th/11th = natural wealth enhancer.",
        confidence=0.92, verse="JP Ch.7 v.1-12",
        tags=["jp", "yoga", "dhana_yoga", "2nd_11th", "lakshmi_yoga", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX045", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Daridra Yoga (Poverty Combinations JP): "
            "Lagna lord in 6th/8th/12th with malefic = poverty. "
            "12th lord stronger than 2nd lord = chronic expenditure > income. "
            "All three: 2nd, 9th, 11th lords weak/afflicted = severe poverty. "
            "Rahu in 2nd with 2nd lord debilitated = financial chaos.",
        confidence=0.88, verse="JP Ch.7 v.13-22",
        tags=["jp", "yoga", "daridra_yoga", "poverty", "afflicted_2nd", "weak_11th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.8 — LONGEVITY ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX046", source="JatakaParijata", chapter="Ch.8", school="parashari",
        category="longevity",
        description="Longevity Method (JP): Three categories: "
            "Short (Alpayu 0-36): 8th lord with lagna lord, both in dusthana. "
            "Medium (Madhyayu 36-72): Mixed indicators — some benefic, some malefic. "
            "Long (Purnayu 72-120): Benefics in kendra, 8th lord strong. "
            "Assess from lagna, Moon, and Hora Lagna simultaneously.",
        confidence=0.90, verse="JP Ch.8 v.1-10",
        tags=["jp", "longevity", "alpayu", "madhyayu", "purnayu", "8th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX047", source="JatakaParijata", chapter="Ch.8", school="parashari",
        category="longevity",
        description="Maraka Dasha (JP): 2nd and 7th lords = Marakas. "
            "When Maraka dasha falls in old age = natural death. "
            "When Maraka dasha in childhood = severe illness or accident. "
            "Saturn in 7th/2nd = natural Maraka for all charts. "
            "Rahu/Ketu in Maraka houses = sudden/unexpected death timing.",
        confidence=0.90, verse="JP Ch.8 v.11-22",
        tags=["jp", "longevity", "maraka", "maraka_dasha", "2nd_lord", "7th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX048", source="JatakaParijata", chapter="Ch.8", school="parashari",
        category="longevity",
        description="Aristha Yogas (JP) — Early Life Danger: "
            "Moon in 6th/8th/12th with malefic = infant mortality risk. "
            "Saturn-Moon opposition = severe childhood illness. "
            "Malefics in 1st/7th/8th without benefic aspect = weak constitution. "
            "Cancelled by Jupiter aspecting Moon or lagna = saved.",
        confidence=0.88, verse="JP Ch.8 v.23-34",
        tags=["jp", "longevity", "aristha", "infant_mortality", "childhood_illness"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.9 — MARRIAGE AND PROGENY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX049", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="marriage",
        description="Marriage Analysis (JP): Three pillars: "
            "1) 7th house and its lord. "
            "2) Venus (natural karaka). "
            "3) Navamsha 7th house. "
            "All three strong = blessed marriage. "
            "2 strong = good marriage with some challenges. "
            "Only 1 strong = troubled marriage.",
        confidence=0.92, verse="JP Ch.9 v.1-10",
        tags=["jp", "marriage", "three_pillars", "7th_house", "venus", "navamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX050", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="marriage",
        description="Mangal Dosha (JP Definition): Mars in 1st/2nd/4th/7th/8th/12th "
            "from lagna, Moon, or Venus = Mangal Dosha (Kuja Dosha). "
            "JP specifies: Mars in 7th = most severe form. "
            "Cancellation: Mars with benefic, or same dosha in partner's chart, "
            "or Mars in own/exaltation sign. Kuja Dosha after 28 = reduced severity.",
        confidence=0.90, verse="JP Ch.9 v.11-22",
        tags=["jp", "marriage", "mangal_dosha", "kuja_dosha", "mars_positions"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX051", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="marriage",
        description="Children Analysis (JP): "
            "5th house + 5th lord + Jupiter = three pillars for children. "
            "Saturn in 5th = few children or delayed. "
            "Multiple benefics in 5th = many children. "
            "5th lord in dusthana = children suffer. "
            "Ketu in 5th = spiritual children or adopted children.",
        confidence=0.90, verse="JP Ch.9 v.23-34",
        tags=["jp", "children", "5th_house", "jupiter_5th", "ketu_5th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.10 — FOREIGN TRAVEL AND SETTLEMENT
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX052", source="JatakaParijata", chapter="Ch.10", school="parashari",
        category="travel",
        description="Foreign Travel Indicators (JP): "
            "12th lord strong/in kendra = foreign residence likely. "
            "Planets in 3rd/9th/12th = mobility indicators. "
            "Rahu in 1st/9th/12th = foreign connection. "
            "Movable lagna + movable Moon sign = restless, travel-oriented. "
            "Moon in 12th = mind always in foreign/unknown territories.",
        confidence=0.87, verse="JP Ch.10 v.1-10",
        tags=["jp", "travel", "foreign", "12th_lord", "rahu_9th", "movable_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX053", source="JatakaParijata", chapter="Ch.10", school="parashari",
        category="travel",
        description="Foreign Settlement vs. Return (JP): "
            "If 4th house strong: returns to homeland despite travel. "
            "If 4th weak/afflicted + 12th strong: permanent foreign settlement. "
            "Saturn in 4th with malefic aspect = no permanent home. "
            "Moon in 12th + debilitated 4th lord = lives abroad permanently.",
        confidence=0.85, verse="JP Ch.10 v.11-20",
        tags=["jp", "travel", "foreign_settlement", "4th_house", "12th_strong"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.11 — VARGA CHARTS AND DIVISIONAL ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX054", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Navamsha (D9) Importance (JP): "
            "'Navamsha is the crown of divisional charts.' "
            "Weak D1 planet strong in D9 = rewards come after struggle. "
            "Strong D1 weak in D9 = early promise that doesn't mature. "
            "Atmakaraka in navamsha = Karakamsha lagna = soul's purpose chart.",
        confidence=0.93, verse="JP Ch.11 v.1-10",
        tags=["jp", "varga", "navamsha", "d9", "karakamsha", "soul_purpose"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX055", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Dashamsha (D10) for Career (JP): "
            "D10 = one tenth of each sign (3° each). "
            "Assess career from D10 as a complete chart. "
            "10th lord of D10 = profession indicator. "
            "Exalted planet in D10 = peak career achievement in that planet's domain.",
        confidence=0.90, verse="JP Ch.11 v.11-20",
        tags=["jp", "varga", "dashamsha", "d10", "career", "profession"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX056", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Drekkana (D3) for Siblings (JP): "
            "D3 shows sibling relations and co-born details. "
            "3rd lord in D3 = primary sibling indicator. "
            "Mars in 3rd in D3 = brave, energetic siblings. "
            "Saturn in 3rd in D3 = limited or estranged siblings.",
        confidence=0.87, verse="JP Ch.11 v.21-30",
        tags=["jp", "varga", "drekkana", "d3", "siblings", "3rd_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX057", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Saptamsha (D7) for Children (JP): "
            "D7 = each sign divided into 7 parts (4°17' each). "
            "Assess children from D7's 5th house and Jupiter. "
            "5th lord of D7 in dusthana = concerns with children's welfare. "
            "Benefics in 5th of D7 = healthy, fortunate children.",
        confidence=0.87, verse="JP Ch.11 v.31-40",
        tags=["jp", "varga", "saptamsha", "d7", "children", "5th_d7"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.12 — SPECIAL YOGAS (JP UNIQUE)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX058", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Gaja Kesari Yoga (JP Extended): Jupiter in kendra from Moon. "
            "JP adds: must not be combust and must be in non-enemy sign. "
            "If combust or in enemy sign = Gaja Kesari reduced. "
            "Maximum Gaja Kesari: Jupiter exalted in kendra from exalted Moon.",
        confidence=0.92, verse="JP Ch.12 v.1-8",
        tags=["jp", "yoga", "gaja_kesari", "jupiter_moon", "kendra_from_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX059", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Budha-Aditya Yoga (JP): Sun conjunct Mercury. "
            "Mercury within 12° of Sun (not fully combust) = Budha-Aditya. "
            "Intelligence, writing, commerce, government service. "
            "Best when Mercury is Vargottama despite proximity to Sun. "
            "JP: combust Mercury still gives Budha-Aditya but at reduced strength.",
        confidence=0.90, verse="JP Ch.12 v.9-16",
        tags=["jp", "yoga", "budha_aditya", "sun_mercury", "intelligence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX060", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Chandra-Mangala Yoga (JP): Moon conjunct Mars. "
            "Intense, ambitious, wealth through bold action. "
            "Commerce, real estate, food industry. "
            "Controversy: JP warns this can also indicate motherless childhood or marital strife.",
        confidence=0.88, verse="JP Ch.12 v.17-24",
        tags=["jp", "yoga", "chandra_mangala", "moon_mars", "commerce"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX061", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Amala Yoga (JP): Benefic in 10th from lagna or Moon = Amala (spotless). "
            "Native has unblemished reputation. "
            "Jupiter in 10th = spiritual authority. "
            "Venus in 10th = artistic fame. "
            "Mercury in 10th = communication/commerce fame.",
        confidence=0.88, verse="JP Ch.12 v.25-32",
        tags=["jp", "yoga", "amala_yoga", "10th_benefic", "reputation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX062", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Kesari Yoga and Indra Yoga (JP): "
            "Kesari (Lion Yoga): Mars and Jupiter mutually aspecting = courage+wisdom. "
            "Indra Yoga (JP specific): Lords of 5th and 11th exchange signs = "
            "exceptional gains from creativity and intellect. Native becomes like Indra — "
            "honored, wealthy, powerful.",
        confidence=0.85, verse="JP Ch.12 v.33-42",
        tags=["jp", "yoga", "kesari_yoga", "indra_yoga", "5th_11th_exchange"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX063", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Matsya Yoga (Fish Yoga — JP): "
            "Benefics in lagna and 9th; malefics in 5th and 8th; mixed in 4th and 12th. "
            "Fish shape — native is virtuous, religious, and ultimately successful. "
            "Associated with dharmic and prosperous life.",
        confidence=0.82, verse="JP Ch.12 v.43-50",
        tags=["jp", "yoga", "matsya_yoga", "fish_yoga", "dharmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX064", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Kurma Yoga (Tortoise Yoga — JP): "
            "Benefics in 1st/3rd/5th and malefics in 2nd/4th/6th (only in Punarvasu, "
            "Uttara, Vishakha, Pushya, Chitra, Uttarashada constellations). "
            "Longevity, stability, success in later life, wisdom.",
        confidence=0.80, verse="JP Ch.12 v.51-58",
        tags=["jp", "yoga", "kurma_yoga", "tortoise", "longevity", "stability"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.13 — MEDICAL AND PHYSICAL ASTROLOGY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX065", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Body Parts from Houses (JP): "
            "1st: head, brain; 2nd: face, eyes; 3rd: neck, shoulders, arms; "
            "4th: chest, lungs; 5th: heart, stomach; 6th: intestines, lower abdomen; "
            "7th: kidneys, bladder; 8th: genitals, anus; 9th: thighs; "
            "10th: knees; 11th: legs, ankles; 12th: feet, left eye.",
        confidence=0.90, verse="JP Ch.13 v.1-12",
        tags=["jp", "medical", "body_parts", "house_body_map"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX066", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Disease from Planets (JP): "
            "Sun afflicted: fever, bone disease, heart. "
            "Moon afflicted: mental illness, blood, cold/kapha. "
            "Mars afflicted: accidents, surgery, blood disorders. "
            "Mercury afflicted: nervous disorders, skin, speech. "
            "Jupiter afflicted: liver, obesity, jaundice. "
            "Venus afflicted: venereal disease, kidney, reproductive. "
            "Saturn afflicted: chronic diseases, joints, paralysis.",
        confidence=0.90, verse="JP Ch.13 v.13-26",
        tags=["jp", "medical", "disease", "planet_disease", "sun_bone", "saturn_chronic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX067", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Tridosha Theory in JP: Three constitutional types: "
            "Vata (Air): Saturn/Rahu/Mercury influence = thin, nervous, erratic. "
            "Pitta (Fire): Sun/Mars influence = medium build, aggressive, sharp. "
            "Kapha (Water): Moon/Venus/Jupiter influence = heavy, calm, enduring. "
            "Mixed types based on multiple planet dominance.",
        confidence=0.88, verse="JP Ch.13 v.27-38",
        tags=["jp", "medical", "tridosha", "vata", "pitta", "kapha", "constitution"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.14 — FEMALE HOROSCOPY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX068", source="JatakaParijata", chapter="Ch.14", school="parashari",
        category="female_chart",
        description="Female Chart Analysis (JP): For women, additional emphasis on: "
            "Moon (primary indicator of nature), Venus (beauty/sensuality), "
            "8th house (longevity of husband), "
            "7th house from Venus = primary marriage indicator. "
            "Strong Moon + Venus = fortunate, beautiful, happy woman.",
        confidence=0.88, verse="JP Ch.14 v.1-10",
        tags=["jp", "female_chart", "moon_female", "venus_female", "8th_husband"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX069", source="JatakaParijata", chapter="Ch.14", school="parashari",
        category="female_chart",
        description="Widowhood Indicators (JP): "
            "Saturn + Rahu in 7th or 8th = early widowhood risk. "
            "Mars in 7th without benefic = Mangal Dosha for husband's longevity. "
            "8th lord in 7th = husband in danger. "
            "These doshas cancelled by Jupiter's aspect on 7th/8th.",
        confidence=0.85, verse="JP Ch.14 v.11-22",
        tags=["jp", "female_chart", "widowhood", "saturn_rahu_7th", "mars_7th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.15 — TIMING OF EVENTS (DASHA ANALYSIS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX070", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Vimshottari Dasha Results (JP Principles): "
            "Dasha of benefic in kendra = excellent period. "
            "Dasha of planet in own/exalted sign = success in its significations. "
            "Dasha of dusthana lord = challenges in that house's themes. "
            "Dasha of planet with most planets = multiple life themes activated.",
        confidence=0.90, verse="JP Ch.15 v.1-10",
        tags=["jp", "dasha", "vimshottari", "kendra_benefic", "dusthana_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX071", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Antardasha Quality (JP): "
            "AD lord in 2nd/4th/5th/7th/9th/10th/11th from MD lord = positive antardasha. "
            "AD lord in 3rd/6th/8th/12th from MD lord = challenging antardasha. "
            "AD lord same house as MD lord = maximum intensity. "
            "AD lord exalted = exceptionally positive period within MD.",
        confidence=0.88, verse="JP Ch.15 v.11-22",
        tags=["jp", "dasha", "antardasha", "ad_lord_position", "from_md_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX072", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Dasha of Exalted Neecha Planet: "
            "Debilitation cancelled (Neecha Bhanga) planet's dasha = exceptional. "
            "The initial years of such dasha may be difficult; "
            "later years give great success as the cancellation fully manifests. "
            "'The fallen rise highest' — JP principle for Neecha Bhanga dashas.",
        confidence=0.87, verse="JP Ch.15 v.23-32",
        tags=["jp", "dasha", "neecha_bhanga_dasha", "fallen_rises", "exceptional"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.16 — TRANSIT RULES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX073", source="JatakaParijata", chapter="Ch.16", school="parashari",
        category="transit",
        description="Jupiter Transit (JP): Jupiter's beneficial transit positions from natal Moon: "
            "2nd, 5th, 7th, 9th, 11th = favorable periods. "
            "1st/6th/8th/12th = challenging. "
            "Jupiter in 5th from Moon = peak creative and child-related results. "
            "Jupiter in 11th from Moon = peak financial gains.",
        confidence=0.90, verse="JP Ch.16 v.1-10",
        tags=["jp", "transit", "jupiter_transit", "from_moon", "2_5_7_9_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX074", source="JatakaParijata", chapter="Ch.16", school="parashari",
        category="transit",
        description="Saturn Transit and Sade Sati (JP): "
            "Saturn transiting 12th/1st/2nd from natal Moon = 7.5-year Sade Sati. "
            "Most challenging: 1st from Moon (direct transit over natal Moon). "
            "Sade Sati effects: health challenges, career obstacles, relationship tests. "
            "Sade Sati reduces effects if natal Saturn is strong.",
        confidence=0.90, verse="JP Ch.16 v.11-22",
        tags=["jp", "transit", "sade_sati", "saturn_transit", "7_5_years"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX075", source="JatakaParijata", chapter="Ch.16", school="parashari",
        category="transit",
        description="Sun's Monthly Transit: Sun transiting 1st/2nd/3rd/6th/9th/11th from Moon "
            "= favorable month. "
            "Sun transiting 5th/7th/8th/12th from Moon = less favorable. "
            "Used for monthly predictions alongside planetary dashas.",
        confidence=0.85, verse="JP Ch.16 v.23-32",
        tags=["jp", "transit", "sun_transit", "monthly", "favorable_positions"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.17 — MUHURTA AND AUSPICIOUS TIMING
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX076", source="JatakaParijata", chapter="Ch.17", school="parashari",
        category="muhurta",
        description="Marriage Muhurta (JP): Auspicious conditions for marriage ceremony: "
            "Jupiter/Venus strong and not combust. "
            "Lagna free from malefic aspect. "
            "Moon waxing (Shukla Paksha), tithis: 2/3/5/7/10/11/12/13. "
            "Nakshatras: Rohini/Mrigashira/Magha/Uttara/Hasta/Swati/Anuradha/Moola/Uttarashadha/Revati.",
        confidence=0.87, verse="JP Ch.17 v.1-12",
        tags=["jp", "muhurta", "marriage_muhurta", "auspicious", "shukla_paksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX077", source="JatakaParijata", chapter="Ch.17", school="parashari",
        category="muhurta",
        description="Business/Career Muhurta (JP): "
            "Mercury strong and not combust for new ventures. "
            "Moon in 3rd/6th/10th/11th from natal Moon = action time. "
            "Sun in 10th or 11th = authority/income muhurta. "
            "Avoid: Saturday/Tuesday for new beginnings (Mars/Saturn direct action).",
        confidence=0.83, verse="JP Ch.17 v.13-22",
        tags=["jp", "muhurta", "business_muhurta", "mercury_strong", "moon_position"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.18 — SPECIAL COMBINATIONS AND FINAL TEACHINGS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX078", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Vaidyanatha's Chart Reading Method: "
            "Step 1: Identify strongest planet (most dignified, in kendra, most aspects). "
            "Step 2: Identify the most afflicted planet. "
            "Step 3: Trace the dasha sequence to find peak positive and challenging periods. "
            "Step 4: Add transits as confirmation layer. "
            "This systematic approach prevents single-factor errors.",
        confidence=0.88, verse="JP Ch.18 v.1-10",
        tags=["jp", "general", "chart_reading", "methodology", "systematic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX079", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="JP on Contradictory Yogas: When two yogas conflict, "
            "the stronger yoga by planetary strength prevails. "
            "Raja Yoga + Daridra Yoga simultaneously = moderate outcome: "
            "wealth and status come but with setbacks. "
            "Never ignore weak yogas — they still influence timing.",
        confidence=0.88, verse="JP Ch.18 v.11-20",
        tags=["jp", "general", "conflicting_yogas", "stronger_prevails", "moderate_outcome"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX080", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Functional Malefics Rule (JP): For each lagna, lords of 6/8/12 "
            "become functional malefics. Lords of 3 also become mildly malefic. "
            "Their dashas bring challenges. "
            "Even if naturally benefic, Jupiter as 6th lord for Cancer lagna = "
            "creates obstacles in its dasha.",
        confidence=0.90, verse="JP Ch.18 v.21-30",
        tags=["jp", "general", "functional_malefics", "6_8_12_lords", "lagna_dependent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX081", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Functional Benefics (JP): For each lagna, lords of 1/5/9 are "
            "primary functional benefics. Lords of 4/7/10 are moderately beneficial. "
            "11th lord = initially beneficial but leads to excessive gains and karma. "
            "Their dashas bring opportunities matching their house themes.",
        confidence=0.90, verse="JP Ch.18 v.31-40",
        tags=["jp", "general", "functional_benefics", "1_5_9_lords", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX082", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="JP Final Verse (Mangalacharana): 'The effects of planets are never "
            "absolute — they are modified by each other's aspects, by the strength "
            "or weakness of the lagna lord, and by the native's own dharmic actions. "
            "Jyotisha illuminates what is, not what must be.' "
            "Free will always remains active within the karmic framework.",
        confidence=0.88, verse="JP Ch.18 v.41-50",
        tags=["jp", "general", "philosophy", "free_will", "dharma", "final_verse"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL JP RULES (JPX083–JPX150)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="JPX083", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Lagna-Specific Raja Yoga Karakas (JP Full List): "
            "Aries: Jupiter+Sun combo (9th+5th). Taurus: Saturn+Venus (9th+5th=yoga karaka). "
            "Cancer: Jupiter+Mars. Leo: Jupiter+Sun. Virgo: Mercury+Venus. "
            "Libra: Saturn (9th+10th = dual yoga karaka). Scorpio: Sun+Jupiter. "
            "Sagittarius: Sun+Mars. Capricorn: Venus+Mercury. "
            "Aquarius: Venus+Saturn. Pisces: Jupiter+Moon.",
        confidence=0.90, verse="JP Ch.6 v.77-96",
        tags=["jp", "yoga", "lagna_specific_yoga", "yoga_karaka", "all_lagnas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX084", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Combustion and Its Effects (JP): "
            "Mars: combust within 17°. "
            "Mercury: combust within 12° (14° when retrograde). "
            "Jupiter: combust within 11°. "
            "Venus: combust within 10° (8° when retrograde). "
            "Saturn: combust within 15°. "
            "Combust planet loses Shadbala strength proportionally.",
        confidence=0.90, verse="JP Ch.3 v.53-64",
        tags=["jp", "combustion", "combust_degrees", "planet_combustion", "shadbala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX085", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Retrograde Planets (JP): Retrograde = planet near Earth, intensified. "
            "Retrograde benefic in kendra = extremely powerful. "
            "Retrograde planet in exaltation = Raja Yoga equivalent. "
            "Retrograde in debilitation = complicated — stronger malefic effects initially, "
            "but ultimately resolves better than expected.",
        confidence=0.88, verse="JP Ch.3 v.65-74",
        tags=["jp", "retrograde", "vakra", "intensified", "kendra_retrograde"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX086", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="6th House (JP Unique): "
            "JP emphasizes 6th as Upachaya — grows stronger over time. "
            "Mars in 6th = defeats enemies through direct action. "
            "Saturn in 6th = chronic enemies but eventual victory. "
            "Jupiter in 6th = protects from disease (Guru's grace). "
            "6th lord in 12th = enemies send themselves into exile.",
        confidence=0.88, verse="JP Ch.4 v.57-68",
        tags=["jp", "6th_house", "upachaya", "mars_6th", "saturn_6th", "enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX087", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="8th House (JP): Hidden house of transformation. "
            "8th from 8th = 3rd house (longevity of death = brother). "
            "Benefic in 8th = peaceful death, inheritance. "
            "Jupiter in 8th = philosophical acceptance of death, spiritual legacy. "
            "Sun in 8th = government obstacles, father problems.",
        confidence=0.88, verse="JP Ch.4 v.69-80",
        tags=["jp", "8th_house", "transformation", "death", "inheritance", "jupiter_8th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX088", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="12th House (JP): House of release and transcendence. "
            "Ketu in 12th = moksha orientation (Ketu = liberation in home of liberation). "
            "Venus in 12th = bed pleasures, spiritual arts. "
            "Jupiter in 12th = foreign guru, spiritual liberation. "
            "12th lord strong = peaceful retirement, spiritual completion.",
        confidence=0.88, verse="JP Ch.4 v.81-90",
        tags=["jp", "12th_house", "moksha", "ketu_12th", "jupiter_12th", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX089", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Rahu in Houses (JP): "
            "1st: unconventional personality, foreign traits. "
            "2nd: fluctuating wealth, speech with foreign accent. "
            "5th: unusual children, speculative gains. "
            "7th: unusual spouse, foreign partner. "
            "9th: unorthodox philosophy, foreign travels. "
            "10th: success in foreign/unusual career.",
        confidence=0.85, verse="JP Ch.5 v.73-84",
        tags=["jp", "rahu", "graha_bhava", "unconventional", "foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX090", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Ketu in Houses (JP): "
            "1st: spiritual personality, marks/scars on body. "
            "4th: unsettled home life, mother-Ketu themes. "
            "5th: spiritual children, past-life inheritance. "
            "8th: psychic abilities, occult knowledge. "
            "9th: spiritual guru, non-orthodox religion. "
            "12th: Moksha karaka in moksha house — liberation.",
        confidence=0.85, verse="JP Ch.5 v.85-96",
        tags=["jp", "ketu", "graha_bhava", "spiritual", "moksha", "12th_ketu"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX091", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Sakata Yoga Cancellation (JP): "
            "Moon in 6th or 8th from Jupiter = Sakata (wheel) — reversals of fortune. "
            "Cancelled when: Moon is in kendra from lagna, or "
            "Jupiter aspects the Moon, or Moon is exalted/own sign. "
            "JP: partial cancellation if Jupiter in trikona from lagna.",
        confidence=0.87, verse="JP Ch.12 v.59-68",
        tags=["jp", "yoga", "sakata_yoga", "cancellation", "moon_jupiter"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX092", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Pravrajya Yoga Conditions (JP): "
            "Four or more planets in one sign = one possible Pravrajya. "
            "Moon's nakshatra lord = Saturn AND Moon aspected by Saturn = strong Pravrajya. "
            "All planets aspecting lagna = Pravrajya (monastic calling). "
            "Ketu in lagna with Saturn's aspect = definitive renunciation.",
        confidence=0.87, verse="JP Ch.12 v.69-80",
        tags=["jp", "yoga", "pravrajya_yoga", "renunciation", "monk", "saturn_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX093", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Parijata Yoga (JP's Namesake): "
            "Lord of the navamsha occupied by the lagna lord is in kendra or trikona "
            "from lagna = Parijata Yoga (after the celestial flower). "
            "Native is like the divine Parijata tree: rare, precious, highly honored. "
            "Especially strong when this planet is exalted.",
        confidence=0.88, verse="JP Ch.7 v.23-32",
        tags=["jp", "yoga", "parijata_yoga", "namesake", "navamsha_lagna_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX094", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Uttama Yoga (JP): "
            "All planets in own/exalted/friendly signs = Uttama (supreme). "
            "Even 7 of 9 planets in these positions = near-Uttama. "
            "Native achieves supreme excellence in one specific field. "
            "The strongest planet in Uttama position shows the field.",
        confidence=0.85, verse="JP Ch.7 v.33-42",
        tags=["jp", "yoga", "uttama_yoga", "all_strong", "excellence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX095", source="JatakaParijata", chapter="Ch.8", school="parashari",
        category="longevity",
        description="Balarishta (Infant Danger) Cancellation (JP): "
            "Aristha = infant mortality indicators. Cancelled by: "
            "Jupiter in kendra, or strong lagna lord, or waxing Moon in kendra, "
            "or benefic in 8th, or strong 8th lord. "
            "JP: if any strong benefic aspects lagna, aristha is largely cancelled.",
        confidence=0.87, verse="JP Ch.8 v.35-46",
        tags=["jp", "longevity", "balarishta", "cancellation", "jupiter_kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX096", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="marriage",
        description="Timing of Marriage (JP): "
            "7th lord dasha or Venus dasha = primary marriage time. "
            "When Jupiter transits 7th from lagna or natal Moon = marriage year. "
            "When Saturn transits 7th from Venus = delay but eventual marriage. "
            "Second marriage: 2nd UL or 7th lord's 2nd activation.",
        confidence=0.88, verse="JP Ch.9 v.35-46",
        tags=["jp", "marriage", "timing", "7th_lord_dasha", "jupiter_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX097", source="JatakaParijata", chapter="Ch.10", school="parashari",
        category="travel",
        description="9th House Travel (JP): "
            "Strong 9th house = long-distance travel and pilgrimage. "
            "9th lord in movable sign = frequent international travel. "
            "Jupiter in 9th = travel for religious/educational purpose. "
            "Rahu in 9th = travel to foreign, exotic destinations.",
        confidence=0.85, verse="JP Ch.10 v.21-30",
        tags=["jp", "travel", "9th_house", "long_distance", "pilgrimage", "rahu_9th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX098", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Trimsamsha (D30) for Sin and Calamity (JP): "
            "Trimsamsha shows past karma burdens. "
            "Each sign's D30 is ruled by Mars(0-5°)/Saturn(5-12°)/Jupiter(12-20°)/Mercury(20-25°)/Venus(25-30°). "
            "Planet in Mars-ruled Trimsamsha = injuries, conflicts. "
            "Planet in Saturn-ruled = chronic suffering. "
            "In Venus = comfort-related karma.",
        confidence=0.85, verse="JP Ch.11 v.41-52",
        tags=["jp", "varga", "trimsamsha", "d30", "karma_burdens", "past_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX099", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Gulika's Disease Role (JP): "
            "Gulika (Mandi) in a house = hidden poison/disease in that house's area. "
            "Gulika + Moon = mental disturbances. "
            "Gulika + lagna lord = constitutional weakness. "
            "Gulika in 6th/8th = chronic disease karaka. "
            "Benefic aspecting Gulika = reduces medical impact.",
        confidence=0.85, verse="JP Ch.13 v.39-50",
        tags=["jp", "medical", "gulika", "hidden_disease", "mandi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX100", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Pratyantardasha (PD) Analysis (JP): Third-level dasha for precise timing. "
            "PD sequence follows same Vimshottari order from AD lord. "
            "When PD lord + AD lord + MD lord all mutually friendly = triple peak. "
            "When all three are enemies = triple obstacle period.",
        confidence=0.85, verse="JP Ch.15 v.33-44",
        tags=["jp", "dasha", "pratyantardasha", "pd", "triple_alignment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX101", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Kala Sarpa Yoga (JP): All planets hemmed between Rahu and Ketu. "
            "Half Kala Sarpa vs. Full Kala Sarpa. "
            "Effects: intense karma, obstacles, followed by dramatic success. "
            "Cancellation: Planets in lagna or any planet breaking the axis. "
            "JP warns: not always negative — depends on Rahu-Ketu axis quality.",
        confidence=0.87, verse="JP Ch.6 v.97-108",
        tags=["jp", "yoga", "kala_sarpa", "rahu_ketu_axis", "karmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX102", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Chaturashraya Yoga (JP): Planets occupying all four types of signs "
            "(movable, fixed, mutable) = Chaturashraya. "
            "Balanced distribution = well-rounded, adaptable, stable personality. "
            "Extreme imbalance (all in one type) = specialized but limited.",
        confidence=0.80, verse="JP Ch.6 v.109-116",
        tags=["jp", "yoga", "chaturashraya", "all_sign_types", "balanced"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX103", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Shadbala Components (JP): Six-fold strength calculation: "
            "1) Sthana Bala (positional — exalted/own/etc.). "
            "2) Dig Bala (directional). "
            "3) Kala Bala (temporal — day/night, hora). "
            "4) Cheshta Bala (motional — retrograde increases). "
            "5) Naisargika Bala (natural — Sun highest, Saturn lowest). "
            "6) Drik Bala (aspectual — benefic aspects add, malefic deduct).",
        confidence=0.90, verse="JP Ch.3 v.75-90",
        tags=["jp", "shadbala", "6_fold_strength", "sthana", "dig", "kala", "cheshta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX104", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Shrinatha Yoga (JP): Lord of 7th in 10th and Mars in 7th = Shrinatha. "
            "Powerful leadership, especially in military/government. "
            "Or: Venus + Jupiter mutually aspecting = Shrinatha variation. "
            "Great wealth and power through relationships and partnerships.",
        confidence=0.82, verse="JP Ch.6 v.117-124",
        tags=["jp", "yoga", "shrinatha_yoga", "7th_lord_10th", "leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX105", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Vasumati Yoga (JP): Benefics in upachaya houses (3/6/10/11) = Vasumati. "
            "All four upachaya houses with benefics = extremely wealthy and successful. "
            "Even two or three = substantial gains. "
            "Jupiter in 11th alone = Vasumati quality.",
        confidence=0.85, verse="JP Ch.7 v.43-52",
        tags=["jp", "yoga", "vasumati_yoga", "upachaya", "benefic_upachaya", "wealthy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX106", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Ravi Yoga (JP): "
            "Sun conjunct lagna lord = Ravi Yoga — clarity of purpose, leadership. "
            "Sun in own sign (Leo) in kendra = full Ravi Yoga. "
            "Sun + Jupiter in same sign = divine authority combination. "
            "Ravi Yoga in 10th = highest career manifestation.",
        confidence=0.83, verse="JP Ch.12 v.81-90",
        tags=["jp", "yoga", "ravi_yoga", "sun_lagna_lord", "leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX107", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="11th House (JP Unique): Labha Bhava — house of desires fulfilled. "
            "JP: 11th house shows not just gains but social circle quality. "
            "Benefics in 11th = wealthy, well-connected friends. "
            "Saturn in 11th = persistent gains after 36 years. "
            "Jupiter in 11th = gains through wisdom, teaching, and dharmic work.",
        confidence=0.88, verse="JP Ch.4 v.91-100",
        tags=["jp", "11th_house", "labha", "gains", "social_circle", "jupiter_11th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX108", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="3rd House (JP): Parakrama Bhava — courage and initiative. "
            "3rd lord strong = self-made, courageous, entrepreneurial. "
            "Mars in 3rd = warrior, athlete, bold communicator. "
            "Mercury in 3rd = writer, journalist, communicator. "
            "3rd from Moon = mother's siblings, neighborhood influence.",
        confidence=0.88, verse="JP Ch.4 v.101-110",
        tags=["jp", "3rd_house", "parakrama", "courage", "mars_3rd", "mercury_3rd"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX109", source="JatakaParijata", chapter="Ch.16", school="parashari",
        category="transit",
        description="Mars Transit (JP): "
            "Mars transiting 3rd/6th/11th from Moon = energy and action (good). "
            "Mars in 1st/4th/8th/12th from Moon = injuries, obstacles, conflicts. "
            "Mars transiting natal Mars = peak energy, also accident risk. "
            "Used for monthly/weekly event timing.",
        confidence=0.87, verse="JP Ch.16 v.33-44",
        tags=["jp", "transit", "mars_transit", "from_moon", "accident_risk"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX110", source="JatakaParijata", chapter="Ch.16", school="parashari",
        category="transit",
        description="Mercury Transit (JP): "
            "Mercury transiting 2nd/4th/6th/8th/10th/11th from Moon = communication active. "
            "Mercury transiting over natal Mercury = peak intellectual activity. "
            "Mercury retrograde transiting natal positions = review and revision period. "
            "Good for reassessment, not for new contracts.",
        confidence=0.85, verse="JP Ch.16 v.45-54",
        tags=["jp", "transit", "mercury_transit", "retrograde_transit", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX111", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Lakshmi Yoga (JP Full): "
            "Venus + 9th lord in own/exalted sign in kendra/trikona = Lakshmi Yoga. "
            "JP: Additionally, Moon + Jupiter in own/exalted trikona = Lakshmi yoga. "
            "Lakshmi Yoga = persistent, overflowing wealth throughout life. "
            "The strongest of all Dhana Yogas.",
        confidence=0.90, verse="JP Ch.6 v.125-134",
        tags=["jp", "yoga", "lakshmi_yoga", "venus_9th", "persistent_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX112", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Saraswati Yoga (JP): Jupiter + Venus + Mercury in kendra/trikona/2nd = "
            "Saraswati Yoga (goddess of learning). "
            "Native is highly learned, multi-talented, excellent speaker and writer. "
            "All three in mutual kendra = peak Saraswati.",
        confidence=0.88, verse="JP Ch.6 v.135-142",
        tags=["jp", "yoga", "saraswati_yoga", "jupiter_venus_mercury", "learning"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX113", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Eye Disease Analysis (JP): "
            "2nd house = right eye; 12th house = left eye. "
            "Sun afflicted in 2nd = right eye disease. "
            "Moon afflicted in 12th = left eye disease. "
            "Venus + malefic in 2nd/12th = corneal issues. "
            "Jupiter aspecting 2nd/12th = strong eyes, good vision.",
        confidence=0.87, verse="JP Ch.13 v.51-62",
        tags=["jp", "medical", "eyes", "right_eye", "left_eye", "sun_2nd"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX114", source="JatakaParijata", chapter="Ch.13", school="parashari",
        category="medical",
        description="Mental Health (JP): "
            "Moon + Saturn = melancholia, depression. "
            "Moon + Mercury + Rahu = nervous breakdown, anxiety. "
            "Moon + Ketu = spiritual crisis, dissociation. "
            "Moon afflicted in 6th/8th/12th = chronic mental health challenges. "
            "Jupiter aspecting Moon = mental stability and protection.",
        confidence=0.87, verse="JP Ch.13 v.63-74",
        tags=["jp", "medical", "mental_health", "moon_saturn", "depression", "anxiety"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX115", source="JatakaParijata", chapter="Ch.14", school="parashari",
        category="female_chart",
        description="Husband's Longevity from Female Chart (JP): "
            "8th lord (from lagna) in dusthana = husband may predecease. "
            "Mars in 7th with no benefic = Mangal Dosha for husband. "
            "Jupiter aspecting 7th or 8th = husband protected and long-lived. "
            "Strong 7th lord in kendra = faithful, long-lived spouse.",
        confidence=0.85, verse="JP Ch.14 v.23-34",
        tags=["jp", "female_chart", "husband_longevity", "8th_lord", "jupiter_7th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX116", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="First Dasha at Birth: The dasha at birth (based on Moon's nakshatra) "
            "sets the life's initial tone. "
            "Born in benefic dasha = auspicious beginning. "
            "Born in Saturn dasha = difficult childhood but later stability. "
            "Born in Rahu dasha = unusual early life, foreign/unconventional path.",
        confidence=0.87, verse="JP Ch.15 v.45-56",
        tags=["jp", "dasha", "first_dasha", "birth_dasha", "life_tone"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX117", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Planetary Age Strengths (JP): Planets have peak strength at specific ages: "
            "Moon: 0-1 years. Mars: 2-3 years. Mercury: 4-12 years. Venus: 12-32 years. "
            "Jupiter: 16 years. Sun: 21-22 years. Saturn: 36 years (maturation). "
            "Moon's maturation: 24 years. Rahu/Ketu: 42/48 years.",
        confidence=0.87, verse="JP Ch.3 v.91-102",
        tags=["jp", "maturation_age", "planet_age", "peak_strength", "moon_24"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX118", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Brahma Yoga (JP): Jupiter rules 2nd/3rd from Sun, Venus rules 2nd/3rd "
            "from Jupiter, and Mercury rules 2nd/3rd from Venus = Brahma Yoga. "
            "Rare combination. Native gains Brahmic wisdom and teaching ability. "
            "Long life and scholarly achievements.",
        confidence=0.82, verse="JP Ch.6 v.143-152",
        tags=["jp", "yoga", "brahma_yoga", "scholarly", "long_life", "teaching"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX119", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Vishnu Yoga (JP): Saturn in 2nd from Sun, Mercury in 2nd from Moon, "
            "Jupiter in 2nd from Saturn = Vishnu Yoga. "
            "Rare. Sustaining, preserving nature. Protector of dharma. "
            "Native sustains large organizations or families through adversity.",
        confidence=0.80, verse="JP Ch.6 v.153-162",
        tags=["jp", "yoga", "vishnu_yoga", "sustaining", "dharma_protector"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX120", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Shiva Yoga (JP): Mars in 2nd from Saturn, Sun in 2nd from Mars, "
            "Jupiter in 2nd from Sun = Shiva Yoga. "
            "Transformative, powerful, often involves renunciation after worldly peak. "
            "Native achieves great heights then transcends worldly life.",
        confidence=0.80, verse="JP Ch.6 v.163-172",
        tags=["jp", "yoga", "shiva_yoga", "transformation", "renunciation_after_peak"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX121", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Hora Chart (D2) Analysis (JP): "
            "D2 shows wealth in detail. Sun's hora = male wealth, father's wealth. "
            "Moon's hora = female wealth, mother's wealth. "
            "Planet in Sun's hora in D2 = income through authority/government. "
            "Planet in Moon's hora = income through public/business.",
        confidence=0.85, verse="JP Ch.11 v.53-62",
        tags=["jp", "varga", "hora", "d2", "sun_hora", "moon_hora", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX122", source="JatakaParijata", chapter="Ch.17", school="parashari",
        category="muhurta",
        description="Journey Muhurta (JP): "
            "Start journeys when Moon is in 1st/3rd/6th/10th/11th from natal Moon. "
            "Avoid: Moon in 5th/7th/8th/12th for journeys (Chandrashtama). "
            "Best day for eastward journey: Sunday/Monday. "
            "Best day for northward journey: Wednesday/Thursday.",
        confidence=0.82, verse="JP Ch.17 v.23-34",
        tags=["jp", "muhurta", "journey_muhurta", "chandrashtama", "moon_position"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX123", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Lagna Lord in Dusthana (JP Analysis): "
            "1st lord in 6th = service-oriented, health challenges, competitive. "
            "1st lord in 8th = deep researcher, transformative life, longevity varies. "
            "1st lord in 12th = spiritual seeker, foreign residence, losses and gains. "
            "In each case: the dusthana's themes dominate the native's self-expression.",
        confidence=0.88, verse="JP Ch.18 v.51-62",
        tags=["jp", "general", "lagna_lord_dusthana", "6th", "8th", "12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX124", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="9th Lord Analysis (JP): The 9th lord is the fortune-giver. "
            "9th lord in 1st = blessed, fortunate native. "
            "9th lord in kendra = Raja Yoga strength. "
            "9th lord debilitated = reduced fortune until Neecha Bhanga. "
            "9th lord in 9th = maximum fortune, very religious, respected widely.",
        confidence=0.88, verse="JP Ch.18 v.63-74",
        tags=["jp", "general", "9th_lord", "fortune", "raja_yoga", "9th_in_9th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX125", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="10th Lord and Career (JP): "
            "10th lord in 1st = self-made, career centered on self. "
            "10th lord in 5th = creative profession, career from intellect. "
            "10th lord in 9th = dharmic career, teaching/law/religion. "
            "10th lord in 11th = career gives massive income. "
            "10th lord in 10th = consistent, lifelong career strength.",
        confidence=0.88, verse="JP Ch.18 v.75-86",
        tags=["jp", "general", "10th_lord", "career", "profession", "10th_in_different_houses"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX126", source="JatakaParijata", chapter="Ch.7", school="parashari",
        category="yoga",
        description="Dhan Yoga from 5th/9th Exchange (JP): "
            "5th lord in 9th + 9th lord in 5th = Lakshmi-Saraswati Yoga. "
            "Wealth from intellect and fortune. Highly educated and prosperous. "
            "Children and fortune both strong. "
            "JP calls this one of the highest wealth combinations.",
        confidence=0.90, verse="JP Ch.7 v.53-62",
        tags=["jp", "yoga", "dhana", "5th_9th_exchange", "lakshmi_saraswati"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX127", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Dasha of 10th Lord (JP): "
            "10th lord's dasha = peak career period. "
            "If 10th lord is a benefic in kendra = extraordinary career success. "
            "If 10th lord is debilitated: career obstacles but 'fallen Neecha' rises. "
            "10th lord + 9th lord in same dasha = Raja Yoga dasha.",
        confidence=0.88, verse="JP Ch.15 v.57-68",
        tags=["jp", "dasha", "10th_lord_dasha", "career_peak", "raja_yoga_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX128", source="JatakaParijata", chapter="Ch.2", school="parashari",
        category="rashi_nature",
        description="Rashi Aspects (JP): Each rashi aspects the 7th rashi (mutual full aspect). "
            "Additionally, special rashi aspects: "
            "Fixed signs (Taurus/Leo/Scorpio/Aquarius) aspect all other fixed signs (3/4 aspect). "
            "Movable signs (Aries/Cancer/Libra/Capricorn) aspect the next movable (square aspect). "
            "JP uses rashi drishti alongside graha drishti for complete analysis.",
        confidence=0.87, verse="JP Ch.2 v.73-84",
        tags=["jp", "rashi_aspect", "rashi_drishti", "fixed_signs", "movable_signs"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX129", source="JatakaParijata", chapter="Ch.5", school="parashari",
        category="graha_bhava",
        description="Mercury in Houses (JP): "
            "1st: intelligent, communicative, youthful appearance. "
            "3rd: writer/communicator/journalist. "
            "5th: speculative mind, good for business. "
            "7th: intellectual spouse, business partner marriage. "
            "10th: communication-based career. "
            "11th: income through trade/communication.",
        confidence=0.87, verse="JP Ch.5 v.97-108",
        tags=["jp", "mercury", "graha_bhava", "houses", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX130", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Pushkara Navamsha (JP): Specific navamsha padas of high auspiciousness. "
            "24 Pushkara navamsha padas exist across all 27 nakshatras. "
            "Planet in Pushkara = maximum power in its function. "
            "Even an enemy-sign planet in Pushkara navamsha = strong and favorable.",
        confidence=0.85, verse="JP Ch.3 v.103-112",
        tags=["jp", "pushkara_navamsha", "navamsha", "maximum_power", "auspicious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX131", source="JatakaParijata", chapter="Ch.8", school="parashari",
        category="longevity",
        description="Kaksha and Longevity (JP): Kaksha (octant position) used for longevity. "
            "Planets in 1st kaksha = strongest. 8th kaksha = weakest. "
            "Malefics in 1st-2nd kaksha = accelerated death potential. "
            "Benefics in 1st-2nd kaksha = longevity enhancement.",
        confidence=0.80, verse="JP Ch.8 v.47-58",
        tags=["jp", "longevity", "kaksha", "octant", "malefic_kaksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX132", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="children",
        description="Nisheka (Conception) Chart (JP): "
            "Chart of conception = Nisheka chakra. "
            "Counted 273 days before birth. "
            "5th house of Nisheka = children indicator. "
            "Benefics in 5th of Nisheka = healthy child. "
            "Malefics in 5th = difficult birth or health concerns.",
        confidence=0.80, verse="JP Ch.9 v.47-58",
        tags=["jp", "children", "nisheka", "conception", "prenatal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX133", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Durdhura Yoga (JP): Planets in 2nd AND 12th from Moon = Durudhara. "
            "All types of Sunapha + Anapha combined. "
            "Most powerful when 3+ benefics flank Moon from both sides. "
            "JP emphasizes this as the 'naturally wealthy' yoga pattern.",
        confidence=0.85, verse="JP Ch.12 v.91-98",
        tags=["jp", "yoga", "durudhara_yoga", "moon_flanked", "naturally_wealthy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX134", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Dwadashamsha (D12) for Parents (JP): "
            "D12 shows parents in detail. "
            "Odd signs: 1st dwadashamsha = Aries. Even signs: 1st = Taurus. "
            "Sun's D12 placement = father's fortune. "
            "Moon's D12 placement = mother's fortune. "
            "Malefic in 9th of D12 = father faces challenges.",
        confidence=0.85, verse="JP Ch.11 v.63-74",
        tags=["jp", "varga", "dwadashamsha", "d12", "parents", "sun_moon_d12"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX135", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Tithi (Lunar Day) at Birth (JP): "
            "Birth on Purnima (Full Moon) = prominent public figure. "
            "Birth on Amavasya (New Moon) = secretive, introspective, karmic. "
            "Birth on Chaturthi/Ashtami/Dvadashi = mixed blessings. "
            "Birth on Panchami/Dashami = good for wealth and family.",
        confidence=0.83, verse="JP Ch.18 v.87-98",
        tags=["jp", "general", "tithi", "birth_tithi", "purnima", "amavasya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX136", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Vara (Day of Week) at Birth (JP): "
            "Sunday birth: government service, fame, health issues. "
            "Monday birth: emotional, musical, mother-oriented. "
            "Tuesday birth: courage, conflicts, engineering. "
            "Wednesday birth: intellectual, commercial, versatile. "
            "Thursday birth: wisdom, teaching, prosperity. "
            "Friday birth: artistic, pleasurable, relationship-oriented. "
            "Saturday birth: disciplined, isolated, persistent.",
        confidence=0.83, verse="JP Ch.18 v.99-112",
        tags=["jp", "general", "vara", "day_of_week", "birth_day", "sun_moon_mars"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX137", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Kalanidhi Yoga (JP): Jupiter + Mercury conjunct in 2nd/5th, "
            "or Jupiter in 2nd/5th aspected by Mercury/Venus = Kalanidhi. "
            "Exceptional talent in arts and fine learning. "
            "Famous for aesthetic sensibility and cultural refinement.",
        confidence=0.83, verse="JP Ch.6 v.173-182",
        tags=["jp", "yoga", "kalanidhi_yoga", "arts", "jupiter_mercury", "aesthetic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX138", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Veshi/Vosi/Ubhayachari (JP): "
            "Veshi: planets (except Moon) in 2nd from Sun = active in Sun's wake. "
            "Vosi: planets (except Moon) in 12th from Sun = retiring, spiritual. "
            "Ubhayachari: planets on both sides of Sun = well-rounded, royal. "
            "Best: all three trines of Sun occupied = supreme Ubhayachari.",
        confidence=0.85, verse="JP Ch.6 v.183-194",
        tags=["jp", "yoga", "veshi", "vosi", "ubhayachari", "sun_flanked"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX139", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Jupiter Dasha (JP Analysis): Jupiter dasha = expansion, wisdom, wealth. "
            "Best results when Jupiter is in kendra/trikona in own or exalted sign. "
            "For Cancer and Leo lagnas (Jupiter = Yoga Karaka): dasha gives raja-level results. "
            "Jupiter dasha after Saturn dasha = relief and expansion after restriction.",
        confidence=0.88, verse="JP Ch.15 v.69-80",
        tags=["jp", "dasha", "jupiter_dasha", "expansion", "wisdom", "yoga_karaka_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX140", source="JatakaParijata", chapter="Ch.15", school="parashari",
        category="dasha_timing",
        description="Rahu/Ketu Dasha (JP Analysis): "
            "Rahu dasha: results depend on sign occupied and dispositor's strength. "
            "Rahu in strong position = sudden rise, foreign gains. "
            "Ketu dasha: spiritual, separating, introspective. "
            "Both: represent karmic debts from past — either pay or receive.",
        confidence=0.87, verse="JP Ch.15 v.81-92",
        tags=["jp", "dasha", "rahu_dasha", "ketu_dasha", "karmic_debt"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX141", source="JatakaParijata", chapter="Ch.17", school="parashari",
        category="muhurta",
        description="Property/Land Purchase Muhurta (JP): "
            "4th house strong at muhurta time. "
            "Moon waxing, in fixed sign. "
            "Venus/Jupiter in 4th or aspecting 4th. "
            "Avoid: Mars in 4th at muhurta, or malefic in lagna at muhurta.",
        confidence=0.82, verse="JP Ch.17 v.35-44",
        tags=["jp", "muhurta", "property_muhurta", "4th_house", "fixed_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX142", source="JatakaParijata", chapter="Ch.11", school="parashari",
        category="varga",
        description="Shashtiamsha (D60) — Past Life Karma (JP): "
            "D60 = each sign divided into 60 parts (0°30' each). "
            "Governed by 60 deities — each with specific qualities. "
            "Most precise indicator of past life karma and this life's challenges. "
            "Planet in benefic Shashtiamsha = good past karma. "
            "Planet in malefic Shashtiamsha = past life debt active.",
        confidence=0.83, verse="JP Ch.11 v.75-86",
        tags=["jp", "varga", "shashtiamsha", "d60", "past_life", "karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX143", source="JatakaParijata", chapter="Ch.4", school="parashari",
        category="house_quality",
        description="4th House (JP Full): Sukha Bhava. "
            "JP: 4th shows home, mother, vehicles, education, AND heart (emotional center). "
            "Moon + Venus in 4th = luxurious, comfortable home. "
            "4th lord in 9th = fortunate home, property abroad. "
            "Jupiter in 4th = wise mother, educational home environment.",
        confidence=0.88, verse="JP Ch.4 v.111-122",
        tags=["jp", "4th_house", "sukha", "home", "mother", "jupiter_4th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX144", source="JatakaParijata", chapter="Ch.9", school="parashari",
        category="marriage",
        description="Love Marriage vs. Arranged Marriage (JP): "
            "Venus + Mars in same house = love marriage tendency. "
            "5th lord aspecting 7th = love marriage. "
            "Saturn in 7th = arranged/delayed marriage. "
            "Rahu in 7th = unconventional or inter-caste/cross-culture marriage.",
        confidence=0.82, verse="JP Ch.9 v.59-70",
        tags=["jp", "marriage", "love_marriage", "arranged_marriage", "venus_mars", "rahu_7th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX145", source="JatakaParijata", chapter="Ch.12", school="parashari",
        category="yoga",
        description="Pushkala Yoga (JP): Lord of the sign occupied by the Moon "
            "is strong, in kendra with Moon's sign lord, and lagna is full of planets = "
            "Pushkala Yoga. Native is immensely rich, famous, and honored by rulers.",
        confidence=0.83, verse="JP Ch.12 v.99-108",
        tags=["jp", "yoga", "pushkala_yoga", "moon_lord_strong", "immense_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX146", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Sreenatha Yoga (JP): "
            "7th lord exalted in 10th with 10th lord = Sreenatha. "
            "Wealth through partnerships, leadership in business. "
            "Public figure known for partnerships and trade. "
            "Venus as 7th lord exalted = peak form of Sreenatha.",
        confidence=0.82, verse="JP Ch.6 v.195-204",
        tags=["jp", "yoga", "sreenatha_yoga", "7th_lord_10th", "partnership_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX147", source="JatakaParijata", chapter="Ch.3", school="parashari",
        category="dignity",
        description="Planetary War (Graha Yuddha — JP): When two planets within 1° of each other "
            "(excluding Sun and Moon), planetary war occurs. "
            "Winner: planet with higher longitude, or Mars (usually). "
            "Loser's significations suffer. "
            "JP: Jupiter always wins Graha Yuddha when involved.",
        confidence=0.87, verse="JP Ch.3 v.113-122",
        tags=["jp", "graha_yuddha", "planetary_war", "winner_loser", "jupiter_wins"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX148", source="JatakaParijata", chapter="Ch.6", school="parashari",
        category="yoga",
        description="Vallaki Yoga (JP): "
            "Venus in lagna, Moon in 2nd, Jupiter in 3rd, Mercury in 4th, "
            "Sun in 5th, Saturn in 6th, Mars in 7th = Vallaki (lute) yoga. "
            "Extremely rare. Native is a musician or associated with divine arts. "
            "Celebrated for melodious speech and artistic ability.",
        confidence=0.78, verse="JP Ch.6 v.205-214",
        tags=["jp", "yoga", "vallaki_yoga", "music", "arts", "rare"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX149", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Planetary Periods and Life Themes (JP Summary): "
            "Sun period: authority, father, health, government. "
            "Moon period: emotion, home, mother, public. "
            "Mars: action, siblings, property, courage. "
            "Mercury: trade, communication, education. "
            "Jupiter: wisdom, children, wealth, dharma. "
            "Venus: love, arts, vehicle, spouse. "
            "Saturn: discipline, karma, service, restructuring. "
            "Each planet delivers its natal chart promise in its dasha.",
        confidence=0.90, verse="JP Ch.18 v.113-128",
        tags=["jp", "general", "dasha_summary", "planet_themes", "life_areas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPX150", source="JatakaParijata", chapter="Ch.18", school="parashari",
        category="general",
        description="Vaidyanatha's Concluding Principle: "
            "'A learned astrologer should study the strengths and weaknesses of all planets "
            "before pronouncing results. No single planet or house tells the full story. "
            "Jataka Parijata was composed to give complete understanding of "
            "the celestial flower (Parijata) that is the horoscope — beautiful, fragrant, "
            "divine, and ultimately beyond full human comprehension.'",
        confidence=0.88, verse="JP Ch.18 v.129-140",
        tags=["jp", "general", "philosophy", "complete_understanding", "jataka_parijata"],
        implemented=False,
    ),
]

for rule in _RULES:
    JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.add(rule)
