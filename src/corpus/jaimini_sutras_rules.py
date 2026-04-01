"""
src/corpus/jaimini_sutras_rules.py — Jaimini Sutras Rules (S244)

Encodes classical Jaimini astrology principles from Jaimini Sutras
(Maharishi Jaimini) — the alternative system to Parashari with unique
Chara Karakas, Rashi Drishti aspects, Chara/Sthira dashas, and Pada (arudha) system.

Sources:
  Jaimini Sutras (Maharishi Jaimini) — 4 chapters (Adhyayas)
  Jataka Sara Sangraha — commentary on Jaimini
  Kalpalatha — Jaimini commentary

30 rules total: JMS001-JMS030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

JAIMINI_SUTRAS_RULES_REGISTRY = CorpusRegistry()

_JAIMINI_RULES = [
    # --- Chara Karaka System (JMS001-008) ---
    RuleRecord(
        rule_id="JMS001",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Karaka system: The 7 planets (Sun through Saturn, excluding Rahu/Ketu) "
            "are assigned Karaka roles based on their degrees within the sign they occupy. "
            "The planet at the highest degree = Atmakaraka (AK, soul significator). "
            "The planet at the lowest degree = Darakaraka (DK, spouse significator)."
        ),
        confidence=0.95,
        verse="JS Adhyaya 1.1-5",
        tags=["jaimini", "chara_karaka", "atmakaraka", "darakaraka", "degree_based"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS002",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Karaka order: AK (Atmakaraka) = highest degree; "
            "AmK (Amatyakaraka) = 2nd highest = career minister; "
            "BK (Bhratrukaraka) = 3rd = siblings/courage; "
            "MK (Matrukaraka) = 4th = mother; "
            "PK (Puttrakaraka) = 5th = children/intellect; "
            "GK (Gnatikaraka) = 6th = disease/competitors; "
            "DK (Darakaraka) = 7th lowest = spouse/relationships."
        ),
        confidence=0.93,
        verse="JS Adhyaya 1.6-14",
        tags=["jaimini", "chara_karaka", "ak_amk_bk_mk_pk_gk_dk", "7_karakas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS003",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Atmakaraka (AK) significance: The Atmakaraka is the most important planet "
            "in the chart — it represents the soul's desire and the primary life lesson. "
            "The sign AK occupies in Navamsha (D9) = Karakamsha lagna — a secondary lagna "
            "revealing the soul's purpose and spiritual path."
        ),
        confidence=0.92,
        verse="JS Adhyaya 1.15-22",
        tags=["jaimini", "atmakaraka", "karakamsha", "soul_purpose", "navamsha_ak"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS004",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Karakamsha lagna effects: Planets in Karakamsha lagna or aspecting it "
            "reveal spiritual and material destiny. "
            "Sun in Karakamsha = government service, authority. "
            "Moon in Karakamsha = nurturing, public life. "
            "Jupiter in Karakamsha = scholar, spiritual teacher."
        ),
        confidence=0.88,
        verse="JS Adhyaya 1.23-35",
        tags=["jaimini", "karakamsha", "sun_moon_jupiter", "spiritual_destiny"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS005",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Amatyakaraka (AmK) for career: The planet with the 2nd highest degree "
            "is AmK — the minister to the soul. The sign AmK occupies in D10 reveals "
            "the career path. AmK in Kendra/Trikona from Karakamsha = excellent career. "
            "AmK conjunct AK = powerful unity of soul and career."
        ),
        confidence=0.88,
        verse="JS Adhyaya 1.36-44",
        tags=["jaimini", "amatyakaraka", "career", "d10_amk", "kendra_trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS006",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Darakaraka (DK) for marriage: DK = planet at lowest degree = spouse significator. "
            "Sign DK occupies in D9 Navamsha describes spouse's nature. "
            "DK conjunct AK in Navamsha = profound soul-mate connection. "
            "DK in 7th from Navamsha lagna = natural placement for marriage."
        ),
        confidence=0.88,
        verse="JS Adhyaya 1.45-52",
        tags=["jaimini", "darakaraka", "spouse", "d9_dk", "marriage", "soul_mate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS007",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Puttrakaraka (PK) for progeny: PK = 5th planet by degree = children significator. "
            "PK in 5th from Karakamsha = children will follow soul's path. "
            "PK afflicted by Saturn or Rahu = obstacles to progeny. "
            "Jupiter with PK = multiple children, wisdom transmitted to them."
        ),
        confidence=0.86,
        verse="JS Adhyaya 1.53-60",
        tags=["jaimini", "puttrakaraka", "children", "progeny", "5th_karakamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS008",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Gnatikaraka (GK) for health and enemies: GK = 6th planet by degree. "
            "Indicates disease, litigation, competitors. GK in 6th/8th from AK = "
            "persistent health challenges related to that planet's nature. "
            "Strong GK in 3rd/11th from AK = competitive victories."
        ),
        confidence=0.85,
        verse="JS Adhyaya 1.61-68",
        tags=["jaimini", "gnatikaraka", "disease", "enemies", "litigation"],
        implemented=False,
    ),
    # --- Rashi Drishti (Sign Aspects) (JMS009-011) ---
    RuleRecord(
        rule_id="JMS009",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Jaimini Rashi Drishti (sign aspect) rules: "
            "Movable signs (Aries, Cancer, Libra, Capricorn) aspect all fixed signs except adjacent. "
            "Fixed signs (Taurus, Leo, Scorpio, Aquarius) aspect all movable signs except adjacent. "
            "Dual signs (Gemini, Virgo, Sagittarius, Pisces) aspect all other dual signs. "
            "This is in addition to Graha Drishti (planetary aspects)."
        ),
        confidence=0.92,
        verse="JS Adhyaya 1.70-80",
        tags=["jaimini", "rashi_drishti", "sign_aspect", "movable_fixed_dual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS010",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Jaimini aspect application: Planets in a sign aspect (Rashi Drishti) "
            "carry the sign's aspect to the receiving sign and its occupants. "
            "Rashi Drishti is mutual — both signs aspect each other. "
            "Exception: adjacent signs (2-12 relationship) do NOT aspect each other."
        ),
        confidence=0.90,
        verse="JS Adhyaya 1.81-88",
        tags=["jaimini", "rashi_drishti", "mutual_aspect", "adjacent_exception"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS011",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Argala (intervention): A planet in the 2nd, 4th, or 11th house from "
            "any reference point creates Argala (intervention/support) for that reference. "
            "A planet in 3rd, 10th, or 12th from the reference obstructs the Argala. "
            "Argala planets strengthen or modify the significations of the reference."
        ),
        confidence=0.88,
        verse="JS Adhyaya 1.89-98",
        tags=["jaimini", "argala", "intervention", "2nd_4th_11th", "obstruction"],
        implemented=False,
    ),
    # --- Pada (Arudha) System (JMS012-016) ---
    RuleRecord(
        rule_id="JMS012",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Arudha Lagna (AL) calculation: Count the number of signs from the lagna "
            "to its lord; then count the same number of signs from the lord — the resulting "
            "sign is the Arudha Lagna. AL represents the world's perception of the person. "
            "Exception: if AL falls on lagna or 7th from it, move to next/previous sign."
        ),
        confidence=0.92,
        verse="JS Adhyaya 1.100-108",
        tags=["jaimini", "arudha_lagna", "arudha_pada", "perception", "maya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS013",
        source="JaiminiSutras",
        chapter="Adhyaya_1",
        school="jaimini",
        category="jaimini",
        description=(
            "Arudha Padas for all 12 houses: Each house has an Arudha Pada (A1-A12), "
            "calculated the same way as Arudha Lagna but from each house lord. "
            "A7 (Darapada) = public/social persona of marriage. "
            "A10 (Rajyapada) = visible career/status. A11 = visible gains."
        ),
        confidence=0.88,
        verse="JS Adhyaya 1.109-116",
        tags=["jaimini", "arudha_pada", "a1_a12", "darapada", "rajyapada"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS014",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Upapada Lagna (UL): Arudha of the 12th house = Upapada Lagna. "
            "UL indicates the nature of marriage/partnership and the spouse's status. "
            "The sign/lord of UL and planets in/aspecting UL describe the marriage circumstances. "
            "UL in trine to AL = harmonious marriage visible to world."
        ),
        confidence=0.88,
        verse="JS Adhyaya 2.1-8",
        tags=["jaimini", "upapada_lagna", "12th_arudha", "marriage_nature"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS015",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Ghatikalagana (GL): The Arudha of the 11th house = Ghatikalagana, "
            "representing power, authority, and ambition. "
            "Planets aspecting GL by Rashi Drishti = sources of power. "
            "GL in Kendra from Lagna or AL = prominent social power and authority."
        ),
        confidence=0.85,
        verse="JS Adhyaya 2.9-15",
        tags=["jaimini", "ghatikalagana", "power", "authority", "11th_arudha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS016",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Arudha Lagna effects: Many benefics in AL or aspecting it = famous, prosperous. "
            "Malefics in AL = setbacks to public image. "
            "Rahu in AL = illusion, foreign connections, unconventional image. "
            "Saturn in AL = persistent effort, masses, longevity of reputation."
        ),
        confidence=0.87,
        verse="JS Adhyaya 2.16-24",
        tags=["jaimini", "arudha_lagna", "benefics_malefics", "reputation", "rahu_saturn"],
        implemented=False,
    ),
    # --- Chara Dasha (JMS017-021) ---
    RuleRecord(
        rule_id="JMS017",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Dasha structure: Jaimini's primary dasha system is sign-based, "
            "not planet-based. Each sign rules for a variable number of years determined "
            "by the position of the sign's lord. Movable signs: 12 - (degrees of lord in sign). "
            "Fixed signs: lord's degrees. Dual signs: 12 - (degrees), or various methods."
        ),
        confidence=0.87,
        verse="JS Adhyaya 2.25-38",
        tags=["jaimini", "chara_dasha", "sign_dasha", "variable_period"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS018",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Dasha sequence: Starts from the sign of Lagna (or stronger of Lagna/7th). "
            "Proceeds in zodiacal order for odd signs; in reverse order for even signs. "
            "Each sign's Dasha brings results of that sign's house from lagna, its Arudha, "
            "planets in it, and planets aspecting it by Rashi Drishti."
        ),
        confidence=0.85,
        verse="JS Adhyaya 2.39-50",
        tags=["jaimini", "chara_dasha", "sequence", "odd_even_sign", "zodiacal_reverse"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS019",
        source="JaiminiSutras",
        chapter="Adhyaya_2",
        school="jaimini",
        category="jaimini",
        description=(
            "Sthira (fixed) Dasha: Alternative to Chara Dasha using fixed periods. "
            "Sun: 20 yrs; Moon: 1 yr; Mars: 2 yrs; Mercury: 9 yrs; Jupiter: 18 yrs; "
            "Venus: 20 yrs; Saturn: 50 yrs; Rahu: 18 yrs; Ketu: 7 yrs (total 145 yrs). "
            "Used for timing longevity and major life events in Jaimini."
        ),
        confidence=0.83,
        verse="JS Adhyaya 2.51-58",
        tags=["jaimini", "sthira_dasha", "fixed_period", "longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS020",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Dasha sub-periods (Antardashas): Within each sign's Mahadasha, "
            "the Antardashas run through all 12 signs in sequence (or reverse for even signs). "
            "Each Antardasha = Mahadasha duration / 12 × sign factor. "
            "Both Dasha and Antardasha signs active simultaneously for assessment."
        ),
        confidence=0.82,
        verse="JS Adhyaya 3.1-10",
        tags=["jaimini", "chara_dasha", "antardasha", "sub_period", "12_signs"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS021",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Chara Dasha interpretation: During any sign Dasha, assess: "
            "(1) Planets in the Dasha sign; (2) Lord of Dasha sign; "
            "(3) Signs aspecting the Dasha sign via Rashi Drishti; "
            "(4) Arudha Pada of the Dasha sign; (5) AK's relationship to Dasha sign. "
            "Convergence of these factors determines the Dasha's primary theme."
        ),
        confidence=0.85,
        verse="JS Adhyaya 3.11-20",
        tags=["jaimini", "chara_dasha", "interpretation", "5_factors", "arudha"],
        implemented=False,
    ),
    # --- Special Lagnas and Yogas (JMS022-026) ---
    RuleRecord(
        rule_id="JMS022",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Hora Lagna (HL): Rises at 2.5 solar hours after birth (one Hora = 1 hour). "
            "Represents wealth and financial strength. Planets in HL or aspecting HL "
            "by Rashi Drishti = sources of wealth. HL in trine to Lagna = good dhana yoga. "
            "Jupiter on or aspecting HL = abundant wealth."
        ),
        confidence=0.86,
        verse="JS Adhyaya 3.21-28",
        tags=["jaimini", "hora_lagna", "wealth", "financial_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS023",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Navamsha Karakamsha for spirituality: Jupiter or Venus in Karakamsha = "
            "spiritually elevated soul. Ketu in Karakamsha = moksha-seeking nature, "
            "interested in liberation. Saturn in Karakamsha = spiritual discipline through hardship. "
            "AK in Sagittarius/Pisces Navamsha = strongly spiritual chart."
        ),
        confidence=0.87,
        verse="JS Adhyaya 3.29-40",
        tags=["jaimini", "karakamsha", "spirituality", "ketu_moksha", "jupiter_venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS024",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Jaimini Raja Yogas: (1) AK + AmK together in Kendra/Trikona from lagna = "
            "royal status. (2) 5 or more planets aspecting Karakamsha = kingship/prominence. "
            "(3) AmK in Lagna aspected by AK = powerful authority. "
            "(4) AK in 5th from AL = recognition from society."
        ),
        confidence=0.88,
        verse="JS Adhyaya 3.41-52",
        tags=["jaimini", "raja_yoga", "ak_amk", "karakamsha", "prominence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS025",
        source="JaiminiSutras",
        chapter="Adhyaya_3",
        school="jaimini",
        category="jaimini",
        description=(
            "Jaimini Dhana Yogas: (1) HL lord in Kendra/Trikona from HL = wealth. "
            "(2) Multiple benefics aspecting A2 (Arudha of 2nd) = visible wealth. "
            "(3) AK in signs of Jupiter/Venus in Navamsha = comfortable life. "
            "(4) 2nd/11th lords mutual aspect via Rashi Drishti = income sources multiply."
        ),
        confidence=0.86,
        verse="JS Adhyaya 3.53-62",
        tags=["jaimini", "dhana_yoga", "hora_lagna", "a2", "wealth_indicators"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS026",
        source="JaiminiSutras",
        chapter="Adhyaya_4",
        school="jaimini",
        category="jaimini",
        description=(
            "Jaimini longevity determination: Uses the 8th house from lagna AND Hora Lagna. "
            "Lords of lagna and 8th aspecting each other by Rashi Drishti = long life. "
            "Saturn in/aspecting 8th and 8th lord strong = longevity. "
            "Short life indicated when malefics occupy both 8th and Hora Lagna without benefic aspect."
        ),
        confidence=0.84,
        verse="JS Adhyaya 4.1-12",
        tags=["jaimini", "longevity", "8th_house", "hora_lagna", "rashi_drishti"],
        implemented=False,
    ),
    # --- Upagraha (Shadow Planets) (JMS027-030) ---
    RuleRecord(
        rule_id="JMS027",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="upagraha",
        description=(
            "Upagraha (sub-planets) overview: BPHS recognizes 5 upagrahas: "
            "Gulika (son of Saturn), Mandi (malefic sub-planet), Dhuma, Vyatipata, Parivesha. "
            "Gulika = most important; its placement afflicts houses/planets it joins or aspects. "
            "Gulika in Kendra = significant karmic difficulty."
        ),
        confidence=0.85,
        verse="BPHS Ch.24 v.1-8",
        tags=["upagraha", "gulika", "mandi", "dhuma", "shadow_planets", "sub_planets"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS028",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="upagraha",
        description=(
            "Gulika calculation: During daytime, each planetary hour lasts 1/12 of daylight. "
            "Gulika = 8th portion of day (Saturn's day portion). "
            "Gulika's sign position is computed from sunrise; it changes every ~1.5 hours. "
            "Gulika in 5th/7th from lagna = significant challenges in progeny/marriage."
        ),
        confidence=0.84,
        verse="BPHS Ch.24 v.9-18",
        tags=["upagraha", "gulika", "calculation", "planetary_hour", "saturn_portion"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS029",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="upagraha",
        description=(
            "Mandi (Gulika variant): Some texts treat Mandi as a separate point from Gulika. "
            "Mandi = beginning of Saturn's hora; Gulika = midpoint of Saturn's hora. "
            "Mandi afflicts wherever it falls; conjunctions with natal planets bring "
            "Saturnine delays and karmic lessons to those planets' significations."
        ),
        confidence=0.82,
        verse="BPHS Ch.24 v.19-26",
        tags=["upagraha", "mandi", "gulika_variant", "saturn_hora", "karmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JMS030",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="upagraha",
        description=(
            "Dhuma, Vyatipata, Parivesha: Dhuma (smoke) = Sun + 133°20' — malefic point. "
            "Vyatipata = 360° − Dhuma. Parivesha = Vyatipata + 180°. "
            "Indrachapa = 360° − Parivesha. Upaketu = Indrachapa − 16°40'. "
            "These 5 sensitive points are afflictors; their house placement indicates areas of karmic difficulty."
        ),
        confidence=0.80,
        verse="BPHS Ch.24 v.27-38",
        tags=["upagraha", "dhuma", "vyatipata", "parivesha", "sensitive_points"],
        implemented=False,
    ),
]

for rule in _JAIMINI_RULES:
    JAIMINI_SUTRAS_RULES_REGISTRY.add(rule)
