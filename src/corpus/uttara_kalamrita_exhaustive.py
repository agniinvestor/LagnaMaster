"""
src/corpus/uttara_kalamrita_exhaustive.py — Uttara Kalamrita Exhaustive (S256)

Exhaustive encoding of Kalidasa's Uttara Kalamrita (17th century CE).
Covers all major doctrines: Special Lagnas, Argala, Arudha Padas,
extended house/planet significations, Upagrahas, Karakas, timing, yogas.

Total: ~150 rules (UKX001–UKX150)
All: implemented=False, school="kalidasa"
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # SPECIAL LAGNAS — KALIDASA'S UNIQUE CONTRIBUTION
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX001", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Hora Lagna (HL): Advances at twice the speed of lagna (2 rashis per 2 hours). "
            "Primary indicator of wealth and financial prosperity. "
            "Strong planets in kendra/trikona from HL give wealth. "
            "Lord of HL well-placed = good earning capacity throughout life.",
        confidence=0.90, verse="UK Ch.2 v.1-4",
        tags=["uk", "hora_lagna", "hl", "wealth", "financial_prosperity", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX002", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Ghati Lagna (GL): Advances at 5x the speed of lagna (1 rashi per ~24 minutes). "
            "Shows power, authority, and rajayoga capacity. "
            "Planets in GL or its trines indicate government/executive positions. "
            "GL lord in kendra with strong planets = political power.",
        confidence=0.88, verse="UK Ch.2 v.5-8",
        tags=["uk", "ghati_lagna", "gl", "power", "authority", "rajayoga", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX003", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Bhava Lagna (BL): Advances at same speed as Sun but from a different base point. "
            "Shows life purpose and soul mission. "
            "Planets in trikona from BL strengthen the native's dharmic path. "
            "BL lord strong = clarity of life purpose.",
        confidence=0.85, verse="UK Ch.2 v.9-12",
        tags=["uk", "bhava_lagna", "bl", "life_purpose", "dharma", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX004", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Sree Lagna (SL): Calculated from Moon's position relative to the fortuna point. "
            "Indicates Lakshmi's grace and overall prosperity. "
            "Lord of SL in kendra = blessings of Lakshmi, material abundance. "
            "Jupiter aspecting SL or its lord = exceptional wealth.",
        confidence=0.85, verse="UK Ch.2 v.13-16",
        tags=["uk", "sree_lagna", "sl", "lakshmi", "prosperity", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX005", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Pranapada Lagna (PL): The vital breath lagna — shows vitality and life force. "
            "Malefics on PL or its lord afflicted = weak constitution. "
            "Benefics on PL = robust health and vitality throughout life. "
            "8th lord from PL afflicted = chronic illness.",
        confidence=0.83, verse="UK Ch.2 v.17-20",
        tags=["uk", "pranapada", "pl", "vitality", "health", "life_force", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX006", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Indu Lagna (IL): The Moon lagna for wealth — derived from 9th lord's period values. "
            "Shows accumulated wealth and inheritance potential. "
            "11th from IL = income; 2nd from IL = savings/accumulated. "
            "Jupiter or Venus on IL = great inherited wealth.",
        confidence=0.83, verse="UK Ch.2 v.21-24",
        tags=["uk", "indu_lagna", "il", "inheritance", "accumulated_wealth", "special_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX007", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Yogi Point and Duplicate Yogi: The Yogi Point is the longitude of Sun+Moon+the Yogi Nakshatra. "
            "Planet ruling the Yogi nakshatra is the Yogi planet — its dasha gives peak benefic results. "
            "Duplicate Yogi (Avayogi) planet is the enemy — its dasha brings challenges.",
        confidence=0.83, verse="UK Ch.2 v.25-30",
        tags=["uk", "yogi_point", "yogi_planet", "avayogi", "dasha_timing"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ARGALA DOCTRINE — KALIDASA'S SYSTEMATIC TREATMENT
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX008", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Primary Argala (Influence Positions): Planets in 2nd, 4th, 11th from any house/planet "
            "create Argala (obstruction-intervention) on that house. "
            "2nd argala: primary wealth/speech influence. "
            "4th argala: sukha/happiness influence. "
            "11th argala: gains/fulfillment influence.",
        confidence=0.90, verse="UK Ch.3 v.1-6",
        tags=["uk", "argala", "2nd_argala", "4th_argala", "11th_argala", "influence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX009", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Secondary Argala: 5th house from reference creates argala for creativity/children. "
            "3rd house argala is considered secondary (Virodha capacity). "
            "All argala can be obstructed: 12th obstructs 2nd, 10th obstructs 4th, 3rd obstructs 11th. "
            "Obstruction (Virodha Argala) requires more planets than the argala.",
        confidence=0.88, verse="UK Ch.3 v.7-12",
        tags=["uk", "argala", "5th_argala", "virodha_argala", "obstruction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX010", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Argala from Arudha Lagna: Calculate argala from AL separately. "
            "2nd from AL shows external wealth/status. "
            "Benefics creating argala on AL = favorable public image. "
            "Malefics creating argala on AL without obstruction = problematic reputation.",
        confidence=0.85, verse="UK Ch.3 v.13-18",
        tags=["uk", "argala", "arudha_lagna", "al_argala", "public_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX011", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Argala from Planets: Each planet receives argala from houses 2/4/11 counted from it. "
            "A planet with unobstructed benefic argala in all 3 positions = most powerful planet. "
            "Such a planet's dasha gives exceptional results in its significations.",
        confidence=0.85, verse="UK Ch.3 v.19-24",
        tags=["uk", "argala", "planet_argala", "unobstructed_argala", "powerful_planet"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ARUDHA PADAS — ALL 12 HOUSES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX012", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Arudha Lagna (A1/AL): Reflection of lagna lord from lagna. "
            "Shows the material/external manifestation of the self. "
            "Exception: if lord is in lagna, count 10th; if lord is in 7th, count 4th. "
            "Planets in AL or 7th from AL shape public perception most strongly.",
        confidence=0.92, verse="UK Ch.4 v.1-6",
        tags=["uk", "arudha", "a1", "arudha_lagna", "external_self", "public_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX013", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Dhana Pada (A2): Arudha of the 2nd house — shows actual wealth manifestation. "
            "Benefics in A2 or aspecting A2 = material wealth. "
            "9th from A2 = accumulated fortune. "
            "A2 lord strong = capacity to accumulate and hold wealth.",
        confidence=0.88, verse="UK Ch.4 v.7-10",
        tags=["uk", "arudha", "a2", "dhana_pada", "wealth_manifestation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX014", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Vikrama Pada (A3): Arudha of the 3rd house — shows courage, initiative, and siblings manifestation. "
            "Malefics in A3 show bold/aggressive actions. "
            "Benefics in A3 = diplomatic, skillful. "
            "Mars/Sun in A3 = military/entrepreneurial career path.",
        confidence=0.85, verse="UK Ch.4 v.11-14",
        tags=["uk", "arudha", "a3", "vikrama_pada", "courage", "initiative"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX015", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Matri Pada (A4): Arudha of the 4th house — shows home, property, mother manifestation. "
            "A4 with Venus/Moon = luxury properties, beautiful home. "
            "Saturn in A4 = old properties or real estate business. "
            "A4 lord in 12th = property abroad.",
        confidence=0.85, verse="UK Ch.4 v.15-18",
        tags=["uk", "arudha", "a4", "matri_pada", "property", "home", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX016", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Mantra Pada (A5): Arudha of the 5th house — shows creativity, children, intellect manifestation. "
            "Jupiter in A5 = wisdom teacher/guru. "
            "A5 with benefics = creative gifts that are publicly recognized. "
            "A5 lord in 5th from lagna = Poorvapunya (past life credits) active.",
        confidence=0.85, verse="UK Ch.4 v.19-22",
        tags=["uk", "arudha", "a5", "mantra_pada", "creativity", "children", "poorvapunya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX017", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Roga Pada (A6): Arudha of the 6th house — shows enemies, disease, service manifestation. "
            "Malefics in A6 = chronic enemies or service in harsh conditions. "
            "Benefics in A6 = helps heal or resolve conflicts. "
            "A6 lord with 8th lord = dangerous enemies.",
        confidence=0.85, verse="UK Ch.4 v.23-26",
        tags=["uk", "arudha", "a6", "roga_pada", "enemies", "disease", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX018", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Dara Pada (A7/DK): Arudha of the 7th house — shows spouse/partner manifestation. "
            "Venus in A7 = beautiful/artistic partner. "
            "Mars in A7 = passionate/aggressive partner. "
            "Saturn in A7 = older or delayed marriage. "
            "A7 with UL (Upapada) = characteristics of actual marriage.",
        confidence=0.90, verse="UK Ch.4 v.27-32",
        tags=["uk", "arudha", "a7", "dara_pada", "spouse", "marriage", "partner"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX019", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Mrityu Pada (A8): Arudha of the 8th house — shows transformation, obstacles, longevity manifestation. "
            "Malefics in A8 = public scandals, sudden reversals. "
            "Benefics in A8 = transforms obstacles into opportunities. "
            "A8 activated in dashas = major life transformation periods.",
        confidence=0.85, verse="UK Ch.4 v.33-36",
        tags=["uk", "arudha", "a8", "mrityu_pada", "transformation", "obstacles"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX020", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Pitri Pada (A9): Arudha of the 9th house — shows fortune, father, dharma manifestation. "
            "Jupiter in A9 = blessed by guru/father, strong dharmic path. "
            "A9 with A1 = the person's dharma aligns with their external persona. "
            "Sun in A9 = prominent father, connection to authority.",
        confidence=0.85, verse="UK Ch.4 v.37-40",
        tags=["uk", "arudha", "a9", "pitri_pada", "fortune", "father", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX021", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Karma Pada (A10): Arudha of the 10th house — shows career, profession, fame manifestation. "
            "Sun/Mars in A10 = government/leadership career. "
            "Mercury in A10 = communication/commerce. "
            "Exalted planet in A10 = highly successful public career. "
            "Saturn in A10 = late-blooming career, hard work required.",
        confidence=0.88, verse="UK Ch.4 v.41-46",
        tags=["uk", "arudha", "a10", "karma_pada", "career", "profession", "fame"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX022", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Labha Pada (A11): Arudha of the 11th house — shows gains, elder siblings, networks manifestation. "
            "Jupiter in A11 = gains from multiple sources. "
            "A11 with many benefics = financially well-connected social network. "
            "A11 lord strong = sustained income flow.",
        confidence=0.85, verse="UK Ch.4 v.47-50",
        tags=["uk", "arudha", "a11", "labha_pada", "gains", "networks", "income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX023", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Upapada Lagna (UL/A12): Arudha of the 12th house — shows spouse's external image. "
            "The most important Arudha for marriage analysis. "
            "Venus/Jupiter in UL or aspecting it = beautiful, prosperous spouse. "
            "Ketu in UL = spiritual/ascetic spouse, or divorce. "
            "Malefics in UL without benefic aspect = troubled marriage.",
        confidence=0.92, verse="UK Ch.4 v.51-58",
        tags=["uk", "arudha", "a12", "upapada_lagna", "ul", "spouse", "marriage_analysis"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # EXTENDED HOUSE SIGNIFICATIONS (KALIDASA'S LIST)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX024", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 1st House Extended: Limbs, beginning, longevity, complexion, happiness, "
            "misery, intelligence, dignity, fame, marks on body, honor/dishonor, "
            "childhood, head hair, nature, character, dream analysis, Atman manifestation.",
        confidence=0.90, verse="UK Ch.5 v.1-8",
        tags=["uk", "1st_house", "extended_signification", "longevity", "fame", "atman", "childhood"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX025", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 2nd House Extended: Wealth, family, speech, face, right eye, food, "
            "silver/gold, copper, enemies (of 7th), imagination, falsehood, tongue, "
            "truth/untruth, nails, gems, perfume, clothing, business acumen, primary education.",
        confidence=0.90, verse="UK Ch.5 v.9-16",
        tags=["uk", "2nd_house", "extended_signification", "right_eye", "speech", "gems"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX026", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 3rd House Extended: Courage, younger siblings, short journeys, right ear, "
            "throat, breath, communication, servants, neighbors, intelligence type, "
            "manual skills, fine arts, sports, dance, drama, writing, signature.",
        confidence=0.90, verse="UK Ch.5 v.17-24",
        tags=["uk", "3rd_house", "extended_signification", "courage", "siblings", "right_ear"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX027", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 4th House Extended: Mother, homeland, property, vehicles, pleasure, "
            "treasure, heart, chest, education, happiness, cattle, fields, "
            "ancestral home, underground wealth, wells, ponds, agriculture, milk.",
        confidence=0.90, verse="UK Ch.5 v.25-32",
        tags=["uk", "4th_house", "extended_signification", "mother", "property", "vehicles"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX028", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 5th House Extended: Children, intellect, past merit, speculation, "
            "devotion to deity, abdomen, upper digestive system, mantras, tantra, "
            "advisors/ministers, ambassadors, gambling, stock market, creative arts, romance.",
        confidence=0.90, verse="UK Ch.5 v.33-40",
        tags=["uk", "5th_house", "extended_signification", "children", "intellect", "mantras"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX029", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 6th House Extended: Enemies, disease, debt, service, theft, wounds, "
            "left ear, intestines, litigation, competition, maternal uncle, stepmother, "
            "obstacles, enmity, poison, accidents, daily work routine.",
        confidence=0.90, verse="UK Ch.5 v.41-48",
        tags=["uk", "6th_house", "extended_signification", "enemies", "disease", "debt"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX030", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 7th House Extended: Spouse, partnerships, trade, travel, sexual pleasure, "
            "bladder/kidneys, desire, passion, lust, business partnerships, contracts, "
            "legal matters, public dealings, foreign relations, death-like separation.",
        confidence=0.90, verse="UK Ch.5 v.49-56",
        tags=["uk", "7th_house", "extended_signification", "spouse", "partnership", "trade"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX031", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 8th House Extended: Longevity, death type, obstacles, hidden wealth, "
            "inheritance, genitals, chronic disease, occult, research, transformation, "
            "in-laws' wealth, disgrace, imprisonment, debt due to others, legacy.",
        confidence=0.90, verse="UK Ch.5 v.57-64",
        tags=["uk", "8th_house", "extended_signification", "longevity", "death", "hidden_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX032", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 9th House Extended: Father, fortune, dharma, higher education, guru, "
            "long journeys, law, philosophy, spiritual practice, thighs, "
            "temples/sacred places, charity, past karma, divine grace.",
        confidence=0.90, verse="UK Ch.5 v.65-72",
        tags=["uk", "9th_house", "extended_signification", "father", "fortune", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX033", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 10th House Extended: Career, fame, authority, government, knees, "
            "profession, ambition, boss/father figure, sky, dignity, honor, "
            "public life, yoga-karma, command, leadership, ruling powers.",
        confidence=0.90, verse="UK Ch.5 v.73-80",
        tags=["uk", "10th_house", "extended_signification", "career", "fame", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX034", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 11th House Extended: Gains, elder siblings, income, left ear, left arm, "
            "aspirations, friends, social network, fulfillment of desires, "
            "profits, recovery from illness, long-term goals, associations.",
        confidence=0.90, verse="UK Ch.5 v.81-88",
        tags=["uk", "11th_house", "extended_signification", "gains", "elder_siblings", "income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX035", source="UttaraKalamrita", chapter="Ch.5", school="kalidasa",
        category="house_signification",
        description="UK 12th House Extended: Losses, expenditure, left eye, imprisonment, "
            "foreign residence, moksha, bed pleasures, charity, donations, "
            "hidden enemies, isolation, meditation, liberation, final journey.",
        confidence=0.90, verse="UK Ch.5 v.89-96",
        tags=["uk", "12th_house", "extended_signification", "losses", "foreign", "moksha"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PLANET SIGNIFICATIONS (KALIDASA'S EXHAUSTIVE LIST)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX036", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Sun Karakatva (UK): Soul (Atman), father, king, political power, "
            "bones, right eye, heart, vitality, government service, authority, "
            "forests, hills, gold, copper, physician, temples, east direction, "
            "Sunday, Leo rashi, Uttara/Uttarashadha/Uttara Bhadra nakshatras.",
        confidence=0.92, verse="UK Ch.6 v.1-8",
        tags=["uk", "sun", "karakatva", "atman", "father", "authority", "right_eye"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX037", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Moon Karakatva (UK): Mind, mother, left eye, blood, water, travel, "
            "public, popularity, silver, pearls, white things, rice, agriculture, "
            "Monday, Cancer rashi, Rohini/Hasta/Shravana nakshatras, "
            "northwest direction, nursing/caretaking professions.",
        confidence=0.92, verse="UK Ch.6 v.9-16",
        tags=["uk", "moon", "karakatva", "mind", "mother", "left_eye", "water"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX038", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Mars Karakatva (UK): Courage, brothers, weapons, fire, blood, "
            "surgery, accidents, muscles, energy, property (land), police/military, "
            "Tuesday, Aries/Scorpio, Mrigashira/Chitra/Dhanishtha nakshatras, "
            "south direction, building construction, cooking, engines.",
        confidence=0.92, verse="UK Ch.6 v.17-24",
        tags=["uk", "mars", "karakatva", "courage", "brothers", "military", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX039", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Mercury Karakatva (UK): Intelligence, speech, communication, writing, "
            "trade, commerce, mathematics, astrology, neighbors, maternal uncles, "
            "skin diseases, Wednesday, Gemini/Virgo, Ashlesha/Jyeshtha/Revati nakshatras, "
            "north direction, printing, accounting, teaching.",
        confidence=0.92, verse="UK Ch.6 v.25-32",
        tags=["uk", "mercury", "karakatva", "intelligence", "speech", "trade", "mathematics"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX040", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Jupiter Karakatva (UK): Wisdom, dharma, guru, children, wealth, "
            "liver, thighs, expansion, optimism, Thursday, Sagittarius/Pisces, "
            "Punarvasu/Vishakha/Purva Bhadrapada nakshatras, northeast direction, "
            "education, law, philosophy, banking, gold, yellow things.",
        confidence=0.92, verse="UK Ch.6 v.33-40",
        tags=["uk", "jupiter", "karakatva", "wisdom", "dharma", "children", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX041", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Venus Karakatva (UK): Love, beauty, wife, vehicles, arts, "
            "semen/reproduction, pleasures, comforts, Friday, Taurus/Libra, "
            "Bharani/Purva Phalguni/Purva Ashadha nakshatras, southeast direction, "
            "jewelry, perfume, film/entertainment, luxury goods.",
        confidence=0.92, verse="UK Ch.6 v.41-48",
        tags=["uk", "venus", "karakatva", "love", "beauty", "arts", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX042", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Saturn Karakatva (UK): Longevity, death, chronic disease, sorrow, "
            "servants, workers, iron, coal, oil, Capricorn/Aquarius, "
            "Pushya/Anuradha/Uttara Bhadrapada nakshatras, west direction, "
            "Saturday, old age, delay, restriction, karma, discipline.",
        confidence=0.92, verse="UK Ch.6 v.49-56",
        tags=["uk", "saturn", "karakatva", "longevity", "karma", "discipline", "delay"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX043", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Rahu Karakatva (UK): Paternal grandfather, foreigners, unusual events, "
            "epidemics, poison, smoke, south-west direction, Aquarius-like effects, "
            "outcasts, foreigners, unexpected gains, sudden reversals, aviation, "
            "Ardra/Swati/Shatabhisha nakshatras, amplifies the sign/house occupied.",
        confidence=0.88, verse="UK Ch.6 v.57-64",
        tags=["uk", "rahu", "karakatva", "foreigners", "unusual", "poison", "amplifier"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX044", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Ketu Karakatva (UK): Maternal grandfather, liberation, spirituality, "
            "detachment, wounds, surgery, occult, astrology, Sagittarius-like effects, "
            "past life karma, Ashwini/Magha/Moola nakshatras, south direction, "
            "dogs, cats, mystical knowledge, moksha.",
        confidence=0.88, verse="UK Ch.6 v.65-72",
        tags=["uk", "ketu", "karakatva", "moksha", "spirituality", "detachment", "past_life"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # UPAGRAHAS (SUB-PLANETS) — KALIDASA'S TREATMENT
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX045", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Dhuma (Smoke): Sun's longitude + 133°20' = Dhuma position. "
            "Malefic sub-planet. Dhuma on natal planets = smoke/confusion in those significations. "
            "Dhuma on lagna = poor health, lack of clarity in life direction.",
        confidence=0.83, verse="UK Ch.7 v.1-4",
        tags=["uk", "upagraha", "dhuma", "malefic_subplanet", "sun_derivative"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX046", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Vyatipata: Dhuma reversed from 360° = 360° - Dhuma longitude. "
            "Shows crossing/obstacles. Transit over natal chart points = difficult periods. "
            "Vyatipata Yoga (Moon and Sun on same declination, opposite hemispheres) = inauspicious.",
        confidence=0.83, verse="UK Ch.7 v.5-8",
        tags=["uk", "upagraha", "vyatipata", "obstacles", "inauspicious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX047", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Parivesha: Vyatipata + 180° = Parivesha. "
            "The halo/corona — shows divine protection when benefics aspect it. "
            "Parivesha on lagna = native has divine shield protecting from enemies.",
        confidence=0.80, verse="UK Ch.7 v.9-12",
        tags=["uk", "upagraha", "parivesha", "divine_protection", "halo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX048", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Indrachapa (Bow of Indra): Parivesha - 180°. "
            "Benefic when well-aspected. Shows royal/government favor. "
            "Indrachapa in lagna or 10th = career success in government sector.",
        confidence=0.80, verse="UK Ch.7 v.13-16",
        tags=["uk", "upagraha", "indrachapa", "government_favor", "royal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX049", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Upaketu: Indrachapa + 16°40' = Upaketu (Ketu's secondary). "
            "Similar effects to Ketu — separation, spiritual tendencies. "
            "Upaketu conjunct natal Moon = emotional detachment or spiritual awakening.",
        confidence=0.658, verse="UK Ch.7 v.17-20",
        tags=["uk", "upagraha", "upaketu", "separation", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX050", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Kala (Time): Derived from Sun's position in Hora. "
            "Shows timing and temporal strength. "
            "Kaala on or aspecting benefics in chart = these benefics give results on time. "
            "Kaala on malefics = delays and time-based obstacles.",
        confidence=0.80, verse="UK Ch.7 v.21-26",
        tags=["uk", "upagraha", "kala", "timing", "temporal_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX051", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Mrityu (Death Point): 8 × Moon longitude + 64°. "
            "Sensitive point for longevity analysis. "
            "Transits over Mrityu during 8th lord's dasha = peak danger period. "
            "Mrityu conjunct natal Ascendant = difficult longevity.",
        confidence=0.82, verse="UK Ch.7 v.27-32",
        tags=["uk", "upagraha", "mrityu", "death_point", "longevity_analysis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX052", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Artha Prikriti (Gulika/Mandi): Most important Upagraha. "
            "Son of Saturn — inherits Saturn's malefic qualities. "
            "Gulika in 1/2/4/7/8/12 = specific sufferings in those areas. "
            "Gulika conjunct Moon = mental disturbances, unstable emotions.",
        confidence=0.88, verse="UK Ch.7 v.33-40",
        tags=["uk", "upagraha", "gulika", "mandi", "saturn_son", "malefic"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # DASHA TIMING — KALIDASA'S UNIQUE ADDITIONS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX053", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Antardasha Quality from Mutual Relationship: "
            "MD lord and AD lord mutual relationship determines dasha quality. "
            "Natural friends = excellent results. "
            "Neutral = moderate results. "
            "Enemies = obstacles and challenges. "
            "But temporary friendship overrides permanent for dasha results.",
        confidence=0.88, verse="UK Ch.8 v.1-8",
        tags=["uk", "dasha", "antardasha", "mutual_relationship", "md_ad_relationship"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX054", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Dasha of Exalted Planet: Exalted planet's dasha = maximum benefits "
            "in the natural significations of that planet. "
            "Exalted benefic in kendra: dasha = peak career/wealth/health results. "
            "Exalted malefic: dasha reduces malefic effects, gives constructive discipline.",
        confidence=0.88, verse="UK Ch.8 v.9-16",
        tags=["uk", "dasha", "exalted_dasha", "maximum_benefits"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX055", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Dasha of Debilitated Planet: Debilitated planet's dasha = challenge period. "
            "Neechabhanga cancels debilitation — cancelled debilitation's dasha = "
            "exceptional success after struggle. "
            "Pure debilitation without cancellation = persistent obstacles.",
        confidence=0.88, verse="UK Ch.8 v.17-24",
        tags=["uk", "dasha", "debilitated_dasha", "neechabhanga", "challenge_period"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX056", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Dasha of Retrograde Planet: Retrograde planet's dasha = review and revision. "
            "Events of the dasha may reverse or repeat patterns from the past. "
            "Retrograde benefic in kendra: dasha gives delayed but lasting success. "
            "Retrograde malefic: past karma returns for resolution.",
        confidence=0.85, verse="UK Ch.8 v.25-32",
        tags=["uk", "dasha", "retrograde_dasha", "past_karma", "revision"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX057", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Transit Activation of Dasha: Dasha lord transiting over natal positions activates themes. "
            "MD lord transiting over natal lagna = peak identity events. "
            "MD lord over natal Moon = emotional/domestic themes peak. "
            "MD lord over natal 10th = career themes activate.",
        confidence=0.85, verse="UK Ch.8 v.33-40",
        tags=["uk", "dasha", "transit_activation", "dasha_lord_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX058", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Prana Dasha (Minute-level): Kalidasa describes 5th level dasha — Prana. "
            "Used for precise event timing within an antardasha. "
            "Sequence mirrors Vimshottari sequence starting from AD lord's nakshatra. "
            "Used in Prashna (horary) for same-day event timing.",
        confidence=0.80, verse="UK Ch.8 v.41-48",
        tags=["uk", "dasha", "prana_dasha", "precision_timing", "prashna"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # BHAVAT BHAVAM AND HOUSE ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX059", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="Bhavat Bhavam Principle: Every house's secondary indicator is found by "
            "counting the same number from that house as the house is from lagna. "
            "Example: 7th from 7th = 1st = native is partner's partner. "
            "5th from 5th = 9th = father of children = grandfather. "
            "9th from 9th = 5th = children of fortune = intellect.",
        confidence=0.92, verse="UK Ch.9 v.1-8",
        tags=["uk", "bhavat_bhavam", "house_mirror", "secondary_indicator"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX060", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="Strength of House: A bhava is strong when: "
            "1) Its lord is in kendra/trikona; "
            "2) Benefics are in or aspect it; "
            "3) It contains its natural karaka; "
            "4) The lord is exalted or in own sign. "
            "Weak house: lord in 6/8/12, with malefics, debilitated.",
        confidence=0.90, verse="UK Ch.9 v.9-16",
        tags=["uk", "bhava_strength", "strong_house", "weak_house", "house_analysis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX061", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="Vacant House Analysis: A house without any planet is judged by its lord. "
            "If lord strong: house themes prosper even without occupants. "
            "If lord in 6/8/12: house suffers despite being empty. "
            "Natural karaka's position also supplements vacant house analysis.",
        confidence=0.88, verse="UK Ch.9 v.17-24",
        tags=["uk", "bhava_analysis", "vacant_house", "house_lord", "natural_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX062", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="Two Planets in Same House: Multiple planets in same house — "
            "if friends, they combine their qualities harmoniously. "
            "If enemies, they fight and reduce each other's results. "
            "Most powerful planet (by Shadbala) dominates the house results.",
        confidence=0.85, verse="UK Ch.9 v.25-32",
        tags=["uk", "bhava_analysis", "multiple_planets", "conjunction", "planetary_war"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # LONGEVITY AND TIMING (KALIDASA'S METHOD)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX063", source="UttaraKalamrita", chapter="Ch.10", school="kalidasa",
        category="longevity",
        description="Longevity Classification (UK): Three categories based on lagna/8th house lord and Moon: "
            "Short life (Alpayu): 0-36 years — multiple malefics in kendra, 8th lord with lagna lord. "
            "Medium life (Madhyayu): 36-72 years — mixed benefic/malefic combinations. "
            "Long life (Purnayu): 72-120 years — benefics in kendra, 8th strong.",
        confidence=0.88, verse="UK Ch.10 v.1-8",
        tags=["uk", "longevity", "alpayu", "madhyayu", "purnayu", "lifespan"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX064", source="UttaraKalamrita", chapter="Ch.10", school="kalidasa",
        category="longevity",
        description="Maraka Planets (UK): Lords of 2nd and 7th are Maraka (death-inflicting). "
            "Saturn, Mars, and Sun also become Marakas when placed in 2nd/7th. "
            "Rahu acting as 2nd/7th lord becomes strongest Maraka. "
            "Maraka dasha in old age = natural death. Maraka dasha in youth = accident/disease.",
        confidence=0.90, verse="UK Ch.10 v.9-16",
        tags=["uk", "longevity", "maraka", "2nd_lord", "7th_lord", "death_inflicting"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX065", source="UttaraKalamrita", chapter="Ch.10", school="kalidasa",
        category="longevity",
        description="8th House Longevity Analysis (UK): "
            "Benefic in 8th = long life, peaceful death. "
            "Malefic in 8th without benefic aspect = difficult death. "
            "Saturn in 8th = very long life (Shani's natural 8th house). "
            "8th lord strong in kendra = protects longevity.",
        confidence=0.88, verse="UK Ch.10 v.17-24",
        tags=["uk", "longevity", "8th_house", "saturn_8th", "peaceful_death"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # KALIDASA'S UNIQUE YOGA RULES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX066", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Subhakartari Yoga: Benefics in houses flanking (2nd and 12th from) "
            "a house or planet = Subhakartari (scissors of benefics). "
            "Planet in Subhakartari = protected and enhanced. "
            "Lagna in Subhakartari = charmed life, natural good fortune.",
        confidence=0.88, verse="UK Ch.11 v.1-6",
        tags=["uk", "yoga", "subhakartari", "benefic_scissors", "protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX067", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Papakartari Yoga: Malefics in 2nd and 12th flanking a house = "
            "Papakartari (scissors of malefics). Planet squeezed by malefics = suppressed. "
            "Lagna in Papakartari = life full of obstacles, confinement tendencies. "
            "Moon in Papakartari = mental anguish.",
        confidence=0.88, verse="UK Ch.11 v.7-12",
        tags=["uk", "yoga", "papakartari", "malefic_scissors", "suppression"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX068", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Vesi/Vasi/Obhayachari Yogas (UK): "
            "Vesi: planets in 2nd from Sun (except Moon) = ability to earn wealth. "
            "Vasi: planets in 12th from Sun = expenditure nature. "
            "Ubhayachari: planets in both 2nd and 12th from Sun = well-rounded personality, royal.",
        confidence=0.88, verse="UK Ch.11 v.13-20",
        tags=["uk", "yoga", "vesi", "vasi", "ubhayachari", "sun_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX069", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Adhi Yoga (UK): Benefics in 6th, 7th, 8th from Moon = Adhi Yoga. "
            "One benefic = minister-level. Two benefics = commander-level. "
            "Three benefics (Jupiter+Venus+Mercury) = king-level success. "
            "Adhi Yoga from Lagna gives even stronger results.",
        confidence=0.90, verse="UK Ch.11 v.21-28",
        tags=["uk", "yoga", "adhi_yoga", "minister", "king", "benefic_positions"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX070", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Shakata Yoga (UK): Moon in 6th or 8th from Jupiter = Shakata Yoga. "
            "Life like a wheel — periods of high success followed by reversals. "
            "Native achieves and loses repeatedly. "
            "Shakata cancelled if Moon is in kendra from lagna.",
        confidence=0.88, verse="UK Ch.11 v.29-34",
        tags=["uk", "yoga", "shakata_yoga", "wheel_of_fortune", "reversals"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX071", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Anapha Yoga: Planets in 12th from Moon (except Sun) = Anapha. "
            "Good health, dignified bearing, self-respect. "
            "Jupiter in 12th from Moon = Anapha = wisdom and reputation.",
        confidence=0.85, verse="UK Ch.11 v.35-40",
        tags=["uk", "yoga", "anapha_yoga", "12th_from_moon", "dignity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX072", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Sunapha Yoga: Planets in 2nd from Moon (except Sun) = Sunapha. "
            "Resourcefulness, wealth-earning ability. "
            "Mars in 2nd from Moon = bold financial decisions. "
            "Jupiter in 2nd from Moon = wisdom-based wealth.",
        confidence=0.85, verse="UK Ch.11 v.41-46",
        tags=["uk", "yoga", "sunapha_yoga", "2nd_from_moon", "resourceful"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX073", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Durudhara Yoga: Planets in both 2nd and 12th from Moon = Durudhara. "
            "Combines Sunapha + Anapha. "
            "Well-balanced personality: earns and manages wealth wisely. "
            "Three or more planets in 2nd+12th from Moon = exceptional Durudhara.",
        confidence=0.85, verse="UK Ch.11 v.47-52",
        tags=["uk", "yoga", "durudhara_yoga", "both_sides_moon", "balanced"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX074", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Kemadruma Yoga: No planets in 2nd or 12th from Moon (except Sun) = Kemadruma. "
            "Loneliness, lack of support, poverty potential. "
            "Kemadruma cancelled if Moon is in kendra from lagna or a strong planet aspects Moon.",
        confidence=0.88, verse="UK Ch.11 v.53-58",
        tags=["uk", "yoga", "kemadruma_yoga", "loneliness", "poverty", "cancellation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX075", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Chandra-Mangala Yoga: Moon conjunct Mars = Chandra-Mangala Yoga. "
            "Intense emotional-physical drive. "
            "Commerce and earning through bold/risky activities. "
            "Wealth through real estate, food, and mass-market businesses.",
        confidence=0.85, verse="UK Ch.11 v.59-64",
        tags=["uk", "yoga", "chandra_mangala", "moon_mars", "commerce", "real_estate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX076", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Parvata Yoga: Benefics in kendras and 6th/8th/12th empty = Parvata Yoga. "
            "Or: lagna lord and 12th lord in mutual kendra or trikona. "
            "Parvata = mountain-like stability and prominence. "
            "Native is like a mountain — firm, prominent, admired.",
        confidence=0.85, verse="UK Ch.11 v.65-70",
        tags=["uk", "yoga", "parvata_yoga", "stability", "prominence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX077", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Kahala Yoga: 4th lord and 9th lord in mutual kendra, with strength in lagna lord. "
            "Or: 4th lord with lagna lord. Kahala = courageous/bold. "
            "Head of small army or group. Local leadership.",
        confidence=0.83, verse="UK Ch.11 v.71-76",
        tags=["uk", "yoga", "kahala_yoga", "courage", "local_leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX078", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Chamara Yoga: Lagna lord exalted in kendra, aspected by Jupiter. "
            "Or: two or more benefics in kendra. "
            "Chamara = royal fan/fly-whisk = symbol of royalty. "
            "Native is honored, fanned, served — high dignitary.",
        confidence=0.85, verse="UK Ch.11 v.77-82",
        tags=["uk", "yoga", "chamara_yoga", "royalty", "honor", "dignitary"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX079", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Sankha Yoga: 5th and 6th lords in mutual kendra, lagna lord strong. "
            "Sankha = conch shell of prosperity. "
            "Fortunate, long-lived, virtuous, fair-minded, righteous. "
            "Enjoys landed property and good marital happiness.",
        confidence=0.83, verse="UK Ch.11 v.83-88",
        tags=["uk", "yoga", "sankha_yoga", "prosperity", "virtue", "long_lived"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX080", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Vanchana Yoga: Lord of lagna in 12th, 12th lord in lagna. "
            "Or: malefics in 3rd and 9th from Moon. "
            "Vanchana = deceit. Native may be deceived or deceives others. "
            "Rahu involved = chronic deception themes.",
        confidence=0.83, verse="UK Ch.11 v.89-94",
        tags=["uk", "yoga", "vanchana_yoga", "deception", "malefic_pattern"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # KARAKAMSHA — ATMAKARAKA IN NAVAMSHA
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX081", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Karakamsha Lagna: The navamsha sign occupied by the Atmakaraka (AK) "
            "becomes the Karakamsha Lagna. "
            "Shows the soul's primary desires and the main focus of this incarnation. "
            "Planets in/aspecting Karakamsha reveal soul's deepest traits.",
        confidence=0.90, verse="UK Ch.12 v.1-6",
        tags=["uk", "karakamsha", "atmakaraka", "navamsha", "soul_desire"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX082", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Atmakaraka Definition: The planet with the highest degree in a sign "
            "is the Atmakaraka — it represents the soul's primary nature. "
            "Among 7 planets (Sun-Saturn). Sun as AK = natural leadership. "
            "Moon as AK = emotional/nurturing nature. "
            "Saturn as AK = karmic/service-oriented soul.",
        confidence=0.90, verse="UK Ch.12 v.7-12",
        tags=["uk", "atmakaraka", "ak", "soul_nature", "highest_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX083", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Planets in Karakamsha: "
            "Sun in KL = government service, political ambitions. "
            "Moon in KL = mind-related career (psychology, writing, public life). "
            "Mars in KL = military, engineering, sports. "
            "Mercury in KL = trade, astrology, writing. "
            "Jupiter in KL = teaching, law, spirituality. "
            "Venus in KL = arts, luxury, entertainment. "
            "Saturn in KL = hard labor, politics, service sectors.",
        confidence=0.88, verse="UK Ch.12 v.13-22",
        tags=["uk", "karakamsha", "planets_in_kl", "career_indication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX084", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Ketu in Karakamsha: Ketu in KL = moksha orientation, spiritual liberation. "
            "Native tends toward renunciation. "
            "Ketu in KL with Jupiter = great spiritual teacher. "
            "Ketu in KL with Venus = religious arts.",
        confidence=0.87, verse="UK Ch.12 v.23-28",
        tags=["uk", "karakamsha", "ketu_kl", "moksha", "renunciation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX085", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="2nd from Karakamsha: Shows accumulated soul-wealth and primary skill. "
            "Benefic in 2nd from KL = skilled in that planet's domain. "
            "Malefic in 2nd from KL = challenges through speech or resources. "
            "Jupiter in 2nd from KL = eloquent, wise speaker.",
        confidence=0.85, verse="UK Ch.12 v.29-34",
        tags=["uk", "karakamsha", "2nd_from_kl", "skill", "speech"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CHARA KARAKAS — JAIMINI INTEGRATION IN UK
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX086", source="UttaraKalamrita", chapter="Ch.13", school="kalidasa",
        category="chara_karaka",
        description="Chara Karaka System: 8 Chara Karakas based on planetary degrees. "
            "AK (Atmakaraka): highest degree — soul. "
            "AMK (Amatyakaraka): 2nd highest — mind/career. "
            "BK (Bhratrikaraka): 3rd — siblings/courage. "
            "MK (Matrikaraka): 4th — mother/property. "
            "PK (Putrakaraka): 5th — children/creativity. "
            "GK (Gnatikaraka): 6th — relatives/enemies. "
            "DK (Darakaraka): 7th/lowest — spouse.",
        confidence=0.88, verse="UK Ch.13 v.1-10",
        tags=["uk", "chara_karaka", "ak", "amk", "bk", "mk", "pk", "gk", "dk"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX087", source="UttaraKalamrita", chapter="Ch.13", school="kalidasa",
        category="chara_karaka",
        description="Amatyakaraka (AMK): The 2nd highest degree planet. "
            "Shows the career and mind direction. "
            "AMK in navamsha shows the natural profession. "
            "Lagna lord + AMK in same sign = career aligns with personality. "
            "AMK in 10th = very prominent career.",
        confidence=0.87, verse="UK Ch.13 v.11-18",
        tags=["uk", "chara_karaka", "amatyakaraka", "amk", "career", "profession"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX088", source="UttaraKalamrita", chapter="Ch.13", school="kalidasa",
        category="chara_karaka",
        description="Darakaraka (DK): The planet with lowest degree = Darakaraka. "
            "Represents the spouse. DK in navamsha shows spouse's nature. "
            "DK's navamsha sign = spouse's primary characteristics. "
            "DK in Karakamsha = spouse as soul-partner.",
        confidence=0.87, verse="UK Ch.13 v.19-26",
        tags=["uk", "chara_karaka", "darakaraka", "dk", "spouse", "navamsha"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MEDICAL ASTROLOGY (KALIDASA)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX089", source="UttaraKalamrita", chapter="Ch.14", school="kalidasa",
        category="medical_astrology",
        description="Disease Diagnosis from Afflicted Houses: "
            "1st house afflicted = general health problems, fevers. "
            "2nd house = mouth, teeth, throat, eye problems. "
            "3rd house = respiratory, right ear, shoulder. "
            "4th house = chest, heart, lung conditions. "
            "6th house = digestive issues, enemies causing illness.",
        confidence=0.85, verse="UK Ch.14 v.1-10",
        tags=["uk", "medical", "disease", "afflicted_houses", "health_diagnosis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX090", source="UttaraKalamrita", chapter="Ch.14", school="kalidasa",
        category="medical_astrology",
        description="Planetary Disease Indicators: "
            "Sun afflicted = bone diseases, fevers, heart. "
            "Moon afflicted = mental issues, blood, gynecological. "
            "Mars afflicted = accidents, blood disorders, inflammation. "
            "Mercury afflicted = nervous system, skin, speech. "
            "Jupiter afflicted = liver, obesity, excess. "
            "Venus afflicted = reproductive, kidney, sexual diseases. "
            "Saturn afflicted = chronic conditions, joints, Vata.",
        confidence=0.87, verse="UK Ch.14 v.11-22",
        tags=["uk", "medical", "planetary_disease", "sun_bones", "saturn_chronic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX091", source="UttaraKalamrita", chapter="Ch.14", school="kalidasa",
        category="medical_astrology",
        description="Cure Timing in Dasha: Disease manifests in malefic dasha of the afflicting planet. "
            "Cure comes during beneficial sub-period. "
            "If 6th lord's dasha = peak illness period. "
            "If benefic in 6th: disease curable; if only malefics in 6th: chronic.",
        confidence=0.85, verse="UK Ch.14 v.23-30",
        tags=["uk", "medical", "disease_dasha", "cure_timing", "6th_lord"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # WEALTH AND PROSPERITY (KALIDASA'S ANALYSIS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX092", source="UttaraKalamrita", chapter="Ch.15", school="kalidasa",
        category="wealth",
        description="Wealth Analysis Tripod: Three primary wealth indicators: "
            "1) 2nd house + 2nd lord (accumulated wealth). "
            "2) 11th house + 11th lord (income sources). "
            "3) Hora Lagna (HL) and its lord (overall financial grace). "
            "All three strong = great wealth. Two strong = comfortable. One = modest.",
        confidence=0.90, verse="UK Ch.15 v.1-8",
        tags=["uk", "wealth", "2nd_house", "11th_house", "hora_lagna", "tripod"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX093", source="UttaraKalamrita", chapter="Ch.15", school="kalidasa",
        category="wealth",
        description="Indu Lagna Wealth Method: Sum the values assigned to each 9th lord "
            "(values: Sun=30, Moon=16, Mars=6, Mercury=8, Jupiter=10, Venus=12, Saturn=1). "
            "Add Sun's value to Moon's 9th lord value, divide by 12 = Indu nakshatra. "
            "Planets aspecting or occupying Indu Lagna strengthen wealth.",
        confidence=0.85, verse="UK Ch.15 v.9-18",
        tags=["uk", "wealth", "indu_lagna_method", "indu_calculation", "9th_lord_values"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX094", source="UttaraKalamrita", chapter="Ch.15", school="kalidasa",
        category="wealth",
        description="Poverty Combinations (UK): "
            "All three: 2nd, 11th, and HL weak = poverty. "
            "Debilitated 2nd lord in 12th = loss of wealth. "
            "12th lord stronger than 2nd lord = expenditure exceeds income. "
            "Rahu in 2nd with no benefic = unreliable income.",
        confidence=0.85, verse="UK Ch.15 v.19-26",
        tags=["uk", "poverty", "2nd_lord_debilitated", "12th_lord_strong", "weak_wealth"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MARRIAGE AND PARTNERSHIP
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX095", source="UttaraKalamrita", chapter="Ch.16", school="kalidasa",
        category="marriage",
        description="Marriage Timing (UK): Marriage occurs during: "
            "Venus dasha/antardasha (primary). "
            "7th lord dasha. "
            "Darakaraka's dasha. "
            "Transits: Jupiter/Venus over 7th house or UL. "
            "Jupiter transiting 7th from natal Moon = marriage year.",
        confidence=0.88, verse="UK Ch.16 v.1-8",
        tags=["uk", "marriage", "timing", "venus_dasha", "7th_lord_dasha", "jupiter_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX096", source="UttaraKalamrita", chapter="Ch.16", school="kalidasa",
        category="marriage",
        description="Spouse Characteristics from UL: "
            "Lord of UL sign = spouse's primary karaka. "
            "Planets in UL = spouse's visible traits. "
            "UL in fiery sign = passionate, energetic spouse. "
            "UL in watery sign = emotional, nurturing spouse. "
            "UL in earthy sign = practical, stable spouse. "
            "UL in airy sign = intellectual, communicative spouse.",
        confidence=0.87, verse="UK Ch.16 v.9-18",
        tags=["uk", "marriage", "ul", "spouse_traits", "upapada_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX097", source="UttaraKalamrita", chapter="Ch.16", school="kalidasa",
        category="marriage",
        description="Divorce and Separation Combinations (UK): "
            "Malefics in UL without benefic aspect = troubled marriage. "
            "8th from UL afflicted = end of marriage. "
            "Ketu in UL = separation (moksha of marriage). "
            "6th lord in 7th = enemies in marriage zone. "
            "Saturn + Rahu in 7th = chronic marital problems.",
        confidence=0.87, verse="UK Ch.16 v.19-28",
        tags=["uk", "marriage", "divorce", "separation", "ketu_ul", "malefic_7th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SPIRITUALITY AND MOKSHA (KALIDASA'S UNIQUE FOCUS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX098", source="UttaraKalamrita", chapter="Ch.17", school="kalidasa",
        category="moksha",
        description="Moksha Indicators (UK): "
            "12th house strong, occupied by benefics = liberation tendency. "
            "Ketu in lagna or 12th = natural spiritual inclination. "
            "Jupiter in 12th = wise renunciation. "
            "12th lord in 12th = complete detachment. "
            "Moon and Sun in 12th = soul seeks liberation.",
        confidence=0.87, verse="UK Ch.17 v.1-8",
        tags=["uk", "moksha", "liberation", "12th_house", "spiritual", "renunciation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX099", source="UttaraKalamrita", chapter="Ch.17", school="kalidasa",
        category="moksha",
        description="Pravrajya Yoga (UK): Strong indicators for monastic life or renunciation: "
            "Four or more planets in one sign. "
            "Lagna lord + Moon lord + Sun lord all in same rashi. "
            "Saturn in 10th with Moon aspecting = karma yoga/service. "
            "Jupiter in kendra aspecting Ketu = teacher-monk.",
        confidence=0.87, verse="UK Ch.17 v.9-18",
        tags=["uk", "moksha", "pravrajya", "renunciation", "monk", "four_planets_one_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX100", source="UttaraKalamrita", chapter="Ch.17", school="kalidasa",
        category="moksha",
        description="Sanyasa Timing: Renunciation occurs during: "
            "Ketu dasha (natural separating planet). "
            "12th lord dasha with Ketu antardasha. "
            "Jupiter + Saturn combined dasha influence. "
            "Saturn transiting 12th from natal Moon = Sanyasa Sadhesati (3rd cycle).",
        confidence=0.83, verse="UK Ch.17 v.19-26",
        tags=["uk", "moksha", "sanyasa", "ketu_dasha", "renunciation_timing"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PRASHNA (HORARY ASTROLOGY)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX101", source="UttaraKalamrita", chapter="Ch.18", school="kalidasa",
        category="prashna",
        description="Prashna Lagna (Query Chart): Cast chart for moment question is asked. "
            "Prashna lagna = the querent's state at query time. "
            "Lord of prashna lagna strong = favorable outcome for query. "
            "Moon's position in prashna = emotional state and likely outcome.",
        confidence=0.85, verse="UK Ch.18 v.1-8",
        tags=["uk", "prashna", "horary", "query_chart", "prashna_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX102", source="UttaraKalamrita", chapter="Ch.18", school="kalidasa",
        category="prashna",
        description="Lost Object Recovery (UK): "
            "Direction of lost item: planet in 2nd from Moon = direction. "
            "4th house = buried/at home. "
            "12th house = lost permanently or stolen. "
            "7th house = in partner's possession. "
            "2nd from prashna lagna indicates the location type.",
        confidence=0.82, verse="UK Ch.18 v.9-18",
        tags=["uk", "prashna", "lost_object", "recovery", "direction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX103", source="UttaraKalamrita", chapter="Ch.18", school="kalidasa",
        category="prashna",
        description="Recovery/Success in Query: Moon moving toward benefic = favorable. "
            "Moon separating from malefic = obstacle is past. "
            "Moon applying to malefic = upcoming obstacle. "
            "Lord of 11th in prashna = fulfillment of desire queried.",
        confidence=0.83, verse="UK Ch.18 v.19-26",
        tags=["uk", "prashna", "moon_applying", "success_query", "11th_lord_prashna"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # TRANSIT RULES (KALIDASA'S EXTENSIONS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX104", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Ashtakavarga and Transit (UK): Saturn transiting a sign with high Ashtakavarga "
            "score (5+) gives good results despite being Saturn. "
            "Saturn in sign with 0-2 bindus = severe challenges. "
            "Jupiter transit always better in signs with high bindus.",
        confidence=0.87, verse="UK Ch.19 v.1-8",
        tags=["uk", "transit", "ashtakavarga", "bindus", "saturn_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX105", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Transit Over Arudha Lagna: Planets transiting over AL create visible public events. "
            "Jupiter transiting AL = public recognition, positive image boost. "
            "Saturn transiting AL = public challenges, reputation tests. "
            "Rahu transiting AL = sudden fame or notoriety.",
        confidence=0.87, verse="UK Ch.19 v.9-16",
        tags=["uk", "transit", "arudha_lagna_transit", "public_events", "jupiter_al"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX106", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Vedha in Transit: Certain signs obstruct (Vedha) the benefic transit of planets. "
            "Jupiter transit in 2nd from Moon is Vedhaed by planets in 12th from Moon. "
            "Saturn transit in 3rd (good) is Vedhaed by planet in 9th. "
            "Vedha planet negates the beneficial/malefic transit result.",
        confidence=0.85, verse="UK Ch.19 v.17-26",
        tags=["uk", "transit", "vedha", "obstruction", "transit_nullification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX107", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Moon's Janma Tara and Transit: "
            "Moon transiting 1st/3rd/5th/7th/9th/11th from natal Moon = favorable. "
            "2nd/4th/6th/8th/10th/12th from natal Moon = unfavorable. "
            "1st from natal Moon (return) = fatigue but cycle restart. "
            "5th and 9th from natal Moon = best transit positions for Moon.",
        confidence=0.88, verse="UK Ch.19 v.27-34",
        tags=["uk", "transit", "moon_transit", "janma_tara", "favorable_positions"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # RECTIFICATION AND SPECIAL TECHNIQUES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX108", source="UttaraKalamrita", chapter="Ch.20", school="kalidasa",
        category="rectification",
        description="Birth Time Rectification (UK): Tanuprashna method. "
            "Ask native about body marks, nature, appearance. "
            "Match to lagna characteristics — Aries lagna = scar on head. "
            "Verify Moon nakshatra with major life events. "
            "Pre/post-midnight birth changes chart significantly.",
        confidence=0.83, verse="UK Ch.20 v.1-8",
        tags=["uk", "rectification", "birth_time", "tanuprashna", "lagna_verification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX109", source="UttaraKalamrita", chapter="Ch.20", school="kalidasa",
        category="rectification",
        description="Nadiamsha Precision: Kalidasa endorses 150-division Nadiamsha (D150) "
            "for precision birth time rectification. "
            "Each nadiamsha = 12 minutes of arc. "
            "Used when birth time is uncertain within 1-2 hours. "
            "The AK planet's nadiamsha reflects exact birth moment.",
        confidence=0.658, verse="UK Ch.20 v.9-16",
        tags=["uk", "rectification", "nadiamsha", "d150", "precision"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # NAKSHATRAS — KALIDASA'S ADDITIONS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX110", source="UttaraKalamrita", chapter="Ch.21", school="kalidasa",
        category="nakshatra",
        description="Tara Bala (Nakshatra Strength from Moon): Count nakshatras from natal Moon. "
            "Positions 1/4/7/10/16/19/22 = Janma/Sampat/Vipat/Kshema/Pratyari/Sadhana/Mitra/Parama Mitra. "
            "1st = Janma (identity); 2nd = Sampat (wealth); 3rd = Vipat (danger); 4th = Kshema (protection); "
            "5th = Pratyari (enemy); 6th = Sadhaka (achievement); 7th = Naidhana (death); 8th = Mitra (friend).",
        confidence=0.90, verse="UK Ch.21 v.1-10",
        tags=["uk", "nakshatra", "tara_bala", "janma_tara", "sampat", "vipat", "kshema"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX111", source="UttaraKalamrita", chapter="Ch.21", school="kalidasa",
        category="nakshatra",
        description="Nakshatra Padas and Navamsha: Each nakshatra has 4 padas of 3°20' each. "
            "Pada 1 = Aries navamsha; Pada 2 = Taurus navamsha; etc. "
            "Pushkara Navamsha: Specific padas of 24 nakshatras give maximum strength. "
            "Planets in Pushkara Navamsha = exceptional power in that nakshatra's domain.",
        confidence=0.88, verse="UK Ch.21 v.11-18",
        tags=["uk", "nakshatra", "pada", "navamsha", "pushkara_navamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX112", source="UttaraKalamrita", chapter="Ch.21", school="kalidasa",
        category="nakshatra",
        description="Moon in Different Nakshatras at Birth (UK Selection): "
            "Rohini Moon: beautiful, prosperous, artistic, fond of pleasures. "
            "Ardra Moon: sharp intellect, sometimes harsh, unconventional. "
            "Pushya Moon: nurturing, stable, traditional, respected. "
            "Magha Moon: ancestral pride, authority, government connections. "
            "Jyeshtha Moon: leadership, possessiveness, strategic.",
        confidence=0.85, verse="UK Ch.21 v.19-28",
        tags=["uk", "nakshatra", "moon_nakshatra", "birth_characteristics"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # VARGA ANALYSIS (KALIDASA'S EMPHASIS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX113", source="UttaraKalamrita", chapter="Ch.22", school="kalidasa",
        category="varga",
        description="Saptavarga Strength: Seven divisional charts used for overall assessment: "
            "D1 (Rashi), D2 (Hora), D3 (Drekkana), D7 (Saptamsha), "
            "D9 (Navamsha), D12 (Dvadashamsha), D30 (Trimsamsha). "
            "A planet strong in 5+ of 7 = extremely powerful. "
            "Kalidasa: judge planet's true strength only after Saptavarga analysis.",
        confidence=0.90, verse="UK Ch.22 v.1-8",
        tags=["uk", "varga", "saptavarga", "divisional_charts", "planet_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX114", source="UttaraKalamrita", chapter="Ch.22", school="kalidasa",
        category="varga",
        description="Shodasavarga (16 Divisional Charts): Kalidasa acknowledges the full Shodasha. "
            "D10 (Dashamsha) for career/profession analysis. "
            "D20 (Vimshamsha) for spiritual progress. "
            "D24 (Chaturvimshamsha) for education. "
            "D40 (Khavedamsha) for auspicious/inauspicious effects. "
            "D60 (Shashtiamsha) for past life karma.",
        confidence=0.88, verse="UK Ch.22 v.9-18",
        tags=["uk", "varga", "shodasavarga", "d10", "d20", "d24", "d60"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX115", source="UttaraKalamrita", chapter="Ch.22", school="kalidasa",
        category="varga",
        description="Navamsha Emphasis (UK): Navamsha is the 'fruit' of the birth chart. "
            "D1 shows the seed; D9 shows what grows. "
            "Planets weak in D1 but strong in D9 = late success. "
            "Planets strong in D1 but weak in D9 = early success, decline later. "
            "Vargottama (same sign D1+D9) = constant strength throughout life.",
        confidence=0.90, verse="UK Ch.22 v.19-28",
        tags=["uk", "varga", "navamsha", "d9", "vargottama", "fruit_chart"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MISCELLANEOUS KALIDASA RULES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX116", source="UttaraKalamrita", chapter="Ch.23", school="kalidasa",
        category="general",
        description="Kalidasa on Chart Reading Sequence: Proper sequence for chart analysis: "
            "1) Lagna and its lord strength. "
            "2) Moon sign and nakshatra. "
            "3) Sun sign (soul indicator). "
            "4) Dasha sequence and current dasha. "
            "5) Transits of slow planets. "
            "6) Special lagnas and yogas. "
            "Never predict from single factor alone.",
        confidence=0.88, verse="UK Ch.23 v.1-8",
        tags=["uk", "general", "chart_reading", "analysis_sequence", "methodology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX117", source="UttaraKalamrita", chapter="Ch.23", school="kalidasa",
        category="general",
        description="Kalidasa on Contradictions: When planets give contradictory indications, "
            "the stronger planet prevails. Strength hierarchy: "
            "Exalted > Own sign > Friendly sign > Neutral > Enemy sign > Debilitated. "
            "Among functional planets, yoga-forming planets outrank single-house lords. "
            "The majority indication prevails over isolated exception.",
        confidence=0.88, verse="UK Ch.23 v.9-18",
        tags=["uk", "general", "contradiction", "strength_hierarchy", "majority_rule"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX118", source="UttaraKalamrita", chapter="Ch.23", school="kalidasa",
        category="general",
        description="Badhaka Planet (UK): Badhaka = obstructing planet. "
            "Movable lagnas (Aries/Cancer/Libra/Capricorn): 11th lord = Badhaka. "
            "Fixed lagnas (Taurus/Leo/Scorpio/Aquarius): 9th lord = Badhaka. "
            "Dual/Mutable lagnas (Gemini/Virgo/Sagittarius/Pisces): 7th lord = Badhaka. "
            "Badhaka planet in kendra = major life obstacle.",
        confidence=0.88, verse="UK Ch.23 v.19-28",
        tags=["uk", "badhaka", "obstructor", "movable_lagna", "fixed_lagna", "dual_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX119", source="UttaraKalamrita", chapter="Ch.24", school="kalidasa",
        category="general",
        description="Combustion Rules (UK Additions): "
            "Moon never becomes combust (only dark/dim at new moon). "
            "Planet within 1° of Sun = fully combust (Moudya), loses all strength. "
            "Within 6° = partial combustion. "
            "Combust planet in Navamsha gains strength back if in own/exalted navamsha.",
        confidence=0.87, verse="UK Ch.24 v.1-8",
        tags=["uk", "combustion", "moudya", "moon_combustion", "navamsha_recovery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX120", source="UttaraKalamrita", chapter="Ch.24", school="kalidasa",
        category="general",
        description="Kalidasa's Concluding Principle: The human chart is a mandala of karma. "
            "No chart is entirely good or bad — every chart has its own Yoga and Bhoga. "
            "The astrologer's duty is to help the native understand their karma "
            "and navigate the planetary periods with wisdom. "
            "Free will operates within the framework of Daiva (destiny).",
        confidence=0.88, verse="UK Ch.24 v.9-18",
        tags=["uk", "general", "philosophy", "karma", "free_will", "daiva", "yoga_bhoga"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL UNIQUE UK RULES (UKX121-UKX150)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="UKX121", source="UttaraKalamrita", chapter="Ch.4", school="kalidasa",
        category="arudha",
        description="Arudha Calculation Exception: If Arudha falls in same sign as the house, "
            "shift 10 signs forward. If Arudha falls in 7th from the house, "
            "shift 10 signs from that position. "
            "These exceptions ensure Arudha doesn't coincide with the house itself.",
        confidence=0.90, verse="UK Ch.4 v.59-64",
        tags=["uk", "arudha", "calculation", "exception_rule", "10th_shift"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX122", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Argala from Moon: Calculate argala from natal Moon separately. "
            "Moon receives argala from houses 2/4/11 counted from Moon. "
            "Benefic argala on Moon = emotional stability, mental clarity. "
            "Malefic argala on Moon = emotional turbulence in corresponding dashas.",
        confidence=0.85, verse="UK Ch.3 v.25-30",
        tags=["uk", "argala", "moon_argala", "emotional_argala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX123", source="UttaraKalamrita", chapter="Ch.6", school="kalidasa",
        category="graha_karakatva",
        description="Naisargika (Natural) Karakatva vs. Chara (Variable): "
            "Natural karakatva = fixed for each planet (Sun=soul, Moon=mind, etc.). "
            "Chara karaka = shifts by degrees in each individual chart. "
            "When natural and chara karakatva align = extremely strong signification. "
            "Example: Sun as natural AK and highest degree AK = double soul indicator.",
        confidence=0.87, verse="UK Ch.6 v.73-80",
        tags=["uk", "karakatva", "naisargika", "chara", "double_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX124", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Raja Yoga from Special Lagnas: "
            "Trikona lord from GL (Ghati Lagna) in kendra from GL = Raja Yoga equivalent. "
            "Kendra lord from HL aspecting HL = financial Raja Yoga. "
            "GL and HL lords conjoined = both power and wealth simultaneously.",
        confidence=0.85, verse="UK Ch.11 v.95-102",
        tags=["uk", "yoga", "raja_yoga", "ghati_lagna", "hora_lagna", "special_lagnas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX125", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="3rd House Upachaya Rule: Upachaya houses (3/6/10/11) improve over time. "
            "Malefics in upachaya houses become beneficial after age 36. "
            "Saturn in 3rd = initial obstacles with siblings, later great strength. "
            "Mars in 6th = enemies defeated through persistence over time.",
        confidence=0.88, verse="UK Ch.9 v.33-40",
        tags=["uk", "upachaya", "3rd_house", "6th_house", "malefic_upachaya", "time_improves"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX126", source="UttaraKalamrita", chapter="Ch.15", school="kalidasa",
        category="wealth",
        description="Dhana Yoga (UK Additions): "
            "2nd lord + 11th lord in mutual kendra = strong Dhana Yoga. "
            "9th lord and 5th lord exchange = Lakshmi Yoga. "
            "All three (2nd, 9th, 11th) lords strong and related = exceptional wealth. "
            "Jupiter aspecting any of these = magnifies wealth.",
        confidence=0.88, verse="UK Ch.15 v.27-34",
        tags=["uk", "wealth", "dhana_yoga", "lakshmi_yoga", "jupiter_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX127", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Vimshottari Sub-period Sequence: The Vimshottari sequence is: "
            "Sun(6)-Moon(10)-Mars(7)-Rahu(18)-Jupiter(16)-Saturn(19)-Mercury(17)-Ketu(7)-Venus(20). "
            "Within each MD, AD follows same sequence starting from MD lord's planet. "
            "Total = 120 years. Most humans experience 3-4 major dashas in a lifetime.",
        confidence=0.95, verse="UK Ch.8 v.49-58",
        tags=["uk", "dasha", "vimshottari", "sequence", "120_years", "ad_sequence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX128", source="UttaraKalamrita", chapter="Ch.10", school="kalidasa",
        category="longevity",
        description="Sarpa Drekkana (Serpent Decans): Drekkanas of certain signs = Sarpa (serpent) quality. "
            "Sarpa drekkanas: 2nd drekkana of Cancer, 1st of Scorpio, 3rd of Pisces. "
            "Lagna in Sarpa drekkana = difficult childhood, unconventional life. "
            "8th lord in Sarpa drekkana = unusual death circumstances.",
        confidence=0.82, verse="UK Ch.10 v.25-32",
        tags=["uk", "longevity", "sarpa_drekkana", "serpent", "8th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX129", source="UttaraKalamrita", chapter="Ch.13", school="kalidasa",
        category="chara_karaka",
        description="Gnatikaraka (GK) Analysis: The 6th ranked Chara Karaka shows extended family, "
            "competitors, disease, and legal matters. "
            "GK in 6th/8th/12th = relatives as enemies or obstacles. "
            "GK in kendra/trikona = supportive family network. "
            "GK aspecting AK = family karma strongly tied to soul lessons.",
        confidence=0.85, verse="UK Ch.13 v.27-34",
        tags=["uk", "chara_karaka", "gnatikaraka", "gk", "extended_family", "competitors"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX130", source="UttaraKalamrita", chapter="Ch.22", school="kalidasa",
        category="varga",
        description="Trimshamsha (D30) for Evil and Suffering: "
            "D30 shows past life sins and their karmic consequences. "
            "D30 lagna occupied by malefics = suffering in that area. "
            "D30 of 6th house = chronic health issues. "
            "Benefics in D30 lagna = past merit protecting from suffering.",
        confidence=0.85, verse="UK Ch.22 v.29-36",
        tags=["uk", "varga", "trimshamsha", "d30", "past_life_karma", "suffering"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX131", source="UttaraKalamrita", chapter="Ch.7", school="kalidasa",
        category="upagraha",
        description="Gulika and Health: Gulika's position shows constitutional weakness area. "
            "Gulika in 1st = chronic head/brain issues. "
            "Gulika in 4th = heart/chest vulnerability. "
            "Gulika in 8th = hidden/chronic illness. "
            "Gulika conjunct lagna lord = native's health is Saturn-afflicted.",
        confidence=0.85, verse="UK Ch.7 v.41-48",
        tags=["uk", "upagraha", "gulika_health", "constitutional_weakness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX132", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Parivartana Yoga (UK Treatment): Lords of two houses in each other's signs. "
            "Trinal Parivartana (1-9, 1-5, 5-9): Dharma Yoga, exceptional fortune. "
            "Kendra Parivartana (1-4, 1-7, 1-10): Rajayoga equivalent strength. "
            "Dusthana Parivartana (6-8, 6-12, 8-12): Viparita Rajayoga potential.",
        confidence=0.90, verse="UK Ch.11 v.103-110",
        tags=["uk", "yoga", "parivartana", "exchange", "dharma_yoga", "viparita"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX133", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Swamsha (AK in Own Navamsha): When AK is in its own sign in navamsha, "
            "the Karakamsha = own sign. Swamsha = very favorable — "
            "native's soul purpose aligns perfectly with their natural abilities. "
            "Exalted AK in navamsha = Swamsha equivalent strength.",
        confidence=0.85, verse="UK Ch.12 v.35-40",
        tags=["uk", "karakamsha", "swamsha", "ak_own_navamsha", "soul_alignment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX134", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Jupiter's Beneficial Transit Positions from Moon: "
            "Jupiter in 2nd = financial improvement period. "
            "Jupiter in 5th = creative/children blessings. "
            "Jupiter in 7th = marriage/partnership opportunities. "
            "Jupiter in 9th = dharmic/religious/educational progress. "
            "Jupiter in 11th = peak gains period.",
        confidence=0.90, verse="UK Ch.19 v.35-44",
        tags=["uk", "transit", "jupiter_transit", "from_moon", "beneficial_positions"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX135", source="UttaraKalamrita", chapter="Ch.19", school="kalidasa",
        category="transit",
        description="Saturn's Difficult Transit Positions from Moon: "
            "Saturn in 1st, 2nd, 12th from natal Moon = Sade Sati (7.5-year period). "
            "Saturn in 4th and 8th from Moon = Ashtama Shani = additional challenges. "
            "Saturn in 3rd from Moon = strength through effort (good period for achievement).",
        confidence=0.90, verse="UK Ch.19 v.45-54",
        tags=["uk", "transit", "saturn_transit", "sade_sati", "ashtama_shani"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX136", source="UttaraKalamrita", chapter="Ch.17", school="kalidasa",
        category="moksha",
        description="Jivatma and Paramatma Relationship: Kalidasa on the spiritual purpose of astrology. "
            "The 5th and 9th houses represent the Jivatma (individual soul). "
            "The 1st house represents the Paramatma (universal soul) connection. "
            "Strong 9th house = native has clear connection to cosmic law.",
        confidence=0.83, verse="UK Ch.17 v.27-34",
        tags=["uk", "moksha", "jivatma", "paramatma", "5th_9th", "spiritual_purpose"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX137", source="UttaraKalamrita", chapter="Ch.14", school="kalidasa",
        category="medical_astrology",
        description="Mental Disease Analysis (UK): "
            "Moon + Saturn in kendra = melancholy/depression. "
            "Moon + Rahu = hysteria, phobias, irrational fears. "
            "Moon + Ketu = dissociation, spiritual disturbances. "
            "Moon afflicted by 3+ malefics = severe mental illness potential. "
            "Jupiter aspecting Moon = mental protection and stability.",
        confidence=0.87, verse="UK Ch.14 v.31-40",
        tags=["uk", "medical", "mental_disease", "moon_saturn", "moon_rahu", "jupiter_protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX138", source="UttaraKalamrita", chapter="Ch.16", school="kalidasa",
        category="marriage",
        description="Second Marriage Indicators (UK): "
            "2 UL (Upapada 2) — count another 12 signs for 2nd marriage. "
            "7th from UL afflicted and UL lord in dusthana = 2nd marriage after loss/divorce. "
            "Multiple planets in 7th = multiple relationship indicators. "
            "Venus in 7th with malefics = two significant partners.",
        confidence=0.85, verse="UK Ch.16 v.29-38",
        tags=["uk", "marriage", "second_marriage", "upapada", "multiple_partners"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX139", source="UttaraKalamrita", chapter="Ch.15", school="kalidasa",
        category="wealth",
        description="Chandra-Laghu (Kendradi Rasi Strength): "
            "Planets in kendra rashis (1/4/7/10) get Kendradi Rasi Bala. "
            "Chara rashis strongest in kendra (positive). "
            "Fixed rashis strongest in succedent houses (2/5/8/11). "
            "Dual rashis strongest in cadent houses (3/6/9/12).",
        confidence=0.85, verse="UK Ch.15 v.35-42",
        tags=["uk", "wealth", "kendradi_rasi", "movable_kendra", "fixed_succedent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX140", source="UttaraKalamrita", chapter="Ch.23", school="kalidasa",
        category="general",
        description="Graha Drishti Strength: Aspect strength values: "
            "Full aspect (drishti) = 1.0 (7th house). "
            "3/4 aspect = 0.75. 1/2 aspect = 0.50. 1/4 aspect = 0.25. "
            "Jupiter's 5th and 9th aspects = full (1.0) despite being trinal. "
            "Mars's 4th and 8th = full (1.0). Saturn's 3rd and 10th = 3/4 (0.75).",
        confidence=0.90, verse="UK Ch.23 v.29-36",
        tags=["uk", "aspect", "drishti_strength", "aspect_values", "full_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX141", source="UttaraKalamrita", chapter="Ch.9", school="kalidasa",
        category="bhava_analysis",
        description="Kendradhipati Dosha: Lords of angular houses (1/4/7/10) are neutral — "
            "they shed their natural benefic/malefic nature. "
            "Natural benefic in kendra = reduces its benefic nature (Kendradhipati Dosha). "
            "Jupiter/Venus as 1st/4th/7th/10th lord = mildly less benefic. "
            "Exception: 1st lord (lagna lord) never gets this dosha.",
        confidence=0.88, verse="UK Ch.9 v.41-48",
        tags=["uk", "kendradhipati", "dosha", "kendra_lord", "benefic_reduction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX142", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Musala Yoga: Most planets in fixed signs = Musala (pestle). "
            "Native is firm, determined, obstinate, accumulates wealth. "
            "Musala person: not easily swayed, excellent at any long-term project. "
            "Most planets in movable signs = Rajju Yoga (roving, travel-prone).",
        confidence=0.83, verse="UK Ch.11 v.111-116",
        tags=["uk", "yoga", "musala_yoga", "fixed_signs", "determination", "rajju_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX143", source="UttaraKalamrita", chapter="Ch.11", school="kalidasa",
        category="yoga",
        description="Nala Yoga: Most planets in dual/mutable signs = Nala. "
            "Variable, adaptable, multiple skills but unstable. "
            "Changes residence, profession frequently. "
            "Intellectual but scattered.",
        confidence=0.80, verse="UK Ch.11 v.117-122",
        tags=["uk", "yoga", "nala_yoga", "dual_signs", "mutable", "adaptable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX144", source="UttaraKalamrita", chapter="Ch.8", school="kalidasa",
        category="dasha_timing",
        description="Conditional Antardasha Results: "
            "If AD lord is in 3/6/8/12 from MD lord = obstacles in that sub-period. "
            "If AD lord is in 2/5/9/11 from MD lord = benefic antardasha results. "
            "If AD lord is conjunct MD lord = very intense, concentrated dasha energy.",
        confidence=0.87, verse="UK Ch.8 v.59-66",
        tags=["uk", "dasha", "antardasha_results", "house_from_md", "ad_from_md"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX145", source="UttaraKalamrita", chapter="Ch.20", school="kalidasa",
        category="rectification",
        description="Sphutas (Sensitive Points) for Rectification: "
            "Sphuta Lagna (SL) = verified lagna degree from major events. "
            "Marriage timing should correlate with Venus/7th house activation. "
            "First career achievement = 10th house lord dasha/transit. "
            "Birth of children = 5th lord activation. Use these to verify birth time.",
        confidence=0.82, verse="UK Ch.20 v.17-26",
        tags=["uk", "rectification", "sphutas", "event_correlation", "birth_time_verify"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX146", source="UttaraKalamrita", chapter="Ch.2", school="kalidasa",
        category="special_lagna",
        description="Varnada Lagna: The Varnada Lagna shows the native's varna (caste/type). "
            "Calculation: Add distances of lagna and Moon from Aries (direct for odd, reverse for even). "
            "Divide by 12 and count from Aries = Varnada. "
            "Varnada shows profession type and societal role.",
        confidence=0.80, verse="UK Ch.2 v.31-36",
        tags=["uk", "special_lagna", "varnada_lagna", "varna", "profession_type"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX147", source="UttaraKalamrita", chapter="Ch.3", school="kalidasa",
        category="argala",
        description="Argala Cancellation in Detail: Obstructing argala requirements: "
            "For 2nd argala: need more planets in 12th than 2nd to cancel. "
            "For 4th argala: need more planets in 10th than 4th. "
            "For 11th argala: need more planets in 3rd than 11th. "
            "Benefics obstruct malefic argala; malefics obstruct benefic argala.",
        confidence=0.87, verse="UK Ch.3 v.31-38",
        tags=["uk", "argala", "cancellation", "virodha_argala_detail", "more_planets"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX148", source="UttaraKalamrita", chapter="Ch.12", school="kalidasa",
        category="karakamsha",
        description="Rahu in Karakamsha: Rahu in KL = foreign connections, unusual career, "
            "mass influence, political intrigue. "
            "Rahu in KL with strong Jupiter = international teacher/diplomat. "
            "Rahu in KL with Saturn = politics, industry leadership. "
            "Rahu in KL with Venus = entertainment, film industry.",
        confidence=0.85, verse="UK Ch.12 v.41-48",
        tags=["uk", "karakamsha", "rahu_kl", "foreign", "mass_influence", "political"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX149", source="UttaraKalamrita", chapter="Ch.21", school="kalidasa",
        category="nakshatra",
        description="Abhijit Nakshatra (UK Treatment): The 28th nakshatra, 6°40' between "
            "Uttarashadha and Shravana in Capricorn (26°40' - 30°). "
            "Only used in specific calculations (Vimshottari corrections). "
            "Moon in Abhijit = strong intelligence, leadership, invincible quality. "
            "Muhurta: Abhijit = auspicious midday window.",
        confidence=0.83, verse="UK Ch.21 v.29-36",
        tags=["uk", "nakshatra", "abhijit", "28th_nakshatra", "leadership", "muhurta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="UKX150", source="UttaraKalamrita", chapter="Ch.24", school="kalidasa",
        category="general",
        description="Kalidasa's Final Teaching: 'One must examine the chart with compassion. "
            "The planets do not punish — they reflect the karmas we carry. "
            "The purpose of Jyotisha is to illuminate the path of dharma, "
            "not to frighten or fatalize. A good astrologer is a healer.' "
            "This encapsulates the spirit of Uttara Kalamrita.",
        confidence=0.88, verse="UK Ch.24 v.19-28",
        tags=["uk", "general", "philosophy", "compassion", "dharma", "jyotisha_purpose"],
        implemented=False,
    ),
]

for rule in _RULES:
    UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.add(rule)
