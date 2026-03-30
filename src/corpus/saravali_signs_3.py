"""src/corpus/saravali_signs_3.py — S283: Saravali Mars in 12 signs (Ch.27).

SAV1301–SAV1430 (130 rules).
Phase: 1B_matrix | Source: Saravali | School: parashari

Mars in 12 signs from Saravali Chapter 27:
  Mars in Aries       — SAV1301–SAV1311 (11 rules)
  Mars in Taurus      — SAV1312–SAV1321 (10 rules)
  Mars in Gemini      — SAV1322–SAV1331 (10 rules)
  Mars in Cancer      — SAV1332–SAV1342 (11 rules)
  Mars in Leo         — SAV1343–SAV1352 (10 rules)
  Mars in Virgo       — SAV1353–SAV1362 (10 rules)
  Mars in Libra       — SAV1363–SAV1372 (10 rules)
  Mars in Scorpio     — SAV1373–SAV1383 (11 rules)
  Mars in Sagittarius — SAV1384–SAV1393 (10 rules)
  Mars in Capricorn   — SAV1394–SAV1404 (11 rules)
  Mars in Aquarius    — SAV1405–SAV1414 (10 rules)
  Mars in Pisces      — SAV1415–SAV1424 (10 rules)
  General/conditional — SAV1425–SAV1430 (6 rules)

Mars signifies: courage, aggression, energy, brothers, surgery, military,
engineering, property, accidents, blood-related health, enemies.
Mars exalted in Capricorn, debilitated in Cancer, own signs Aries & Scorpio.

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Aries (own sign) — Ch.27 (SAV1301–SAV1311)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_ARIES_DATA = [
    # (placement_value, extra_qualifiers, outcome_direction, outcome_intensity,
    #  outcome_domains, extra_tags, verse_ref, description)
    ("aries", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mars", "aries", "own_sign", "courage"],
     "Ch.27 v.1",
     "Mars in Aries (own sign): exceptionally courageous and bold, "
     "natural leader with commanding presence, fearless in adversity"),
    ("aries", {},
     "favorable", "strong",
     ["career_status"],
     ["mars", "aries", "own_sign", "military", "career"],
     "Ch.27 v.1",
     "Mars in Aries (own sign): excels in military, police, or defence careers, "
     "attains authority and rank through valorous deeds"),
    ("aries", {},
     "favorable", "moderate",
     ["wealth", "property_vehicles"],
     ["mars", "aries", "own_sign", "property"],
     "Ch.27 v.2",
     "Mars in Aries (own sign): acquires landed property and vehicles, "
     "gains wealth through own enterprise and daring ventures"),
    ("aries", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["mars", "aries", "own_sign", "fame"],
     "Ch.27 v.2",
     "Mars in Aries (own sign): renowned for bravery and martial prowess, "
     "respected by rulers and people in authority"),
    ("aries", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "aries", "own_sign", "health", "accidents"],
     "Ch.27 v.3",
     "Mars in Aries (own sign): prone to head injuries, scars on face or head, "
     "fevers and inflammatory conditions affecting upper body"),
    ("aries", {},
     "mixed", "moderate",
     ["enemies_litigation"],
     ["mars", "aries", "own_sign", "enemies"],
     "Ch.27 v.3",
     "Mars in Aries (own sign): conquers enemies through force but creates "
     "new adversaries through aggressive conduct"),
    ("aries", {},
     "favorable", "moderate",
     ["progeny"],
     ["mars", "aries", "own_sign", "brothers"],
     "Ch.27 v.4",
     "Mars in Aries (own sign): supported by brothers, harmonious relations "
     "with siblings who may also be courageous and independent"),
    ("aries", {},
     "unfavorable", "weak",
     ["marriage"],
     ["mars", "aries", "own_sign", "marriage", "temperament"],
     "Ch.27 v.4",
     "Mars in Aries (own sign): domineering in marriage, spouse may suffer "
     "from native's aggressive and controlling temperament"),
    ("aries", {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mars", "aries", "own_sign", "initiative"],
     "Ch.27 v.5",
     "Mars in Aries (own sign): quick decision-maker, pioneering spirit, "
     "excels in competitive examinations and strategic planning"),
    ("aries", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "aries", "own_sign", "anger"],
     "Ch.27 v.5",
     "Mars in Aries (own sign): wrathful and impatient, prone to sudden "
     "outbursts of anger, quarrelsome disposition"),
    ("aries", {},
     "favorable", "moderate",
     ["career_status"],
     ["mars", "aries", "own_sign", "engineering", "surgery"],
     "Ch.27 v.6",
     "Mars in Aries (own sign): aptitude for surgery, engineering, or work "
     "involving fire, metals, and sharp instruments"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Taurus — Ch.27 (SAV1312–SAV1321)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_TAURUS_DATA = [
    ("taurus", {},
     "mixed", "moderate",
     ["wealth"],
     ["mars", "taurus", "wealth"],
     "Ch.27 v.7",
     "Mars in Taurus: accumulates wealth through persistent effort but "
     "expenditure on luxuries and indulgences dissipates gains"),
    ("taurus", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "taurus", "sensuality"],
     "Ch.27 v.7",
     "Mars in Taurus: attracted to sensual pleasures, fond of fine food "
     "and physical comforts, stubborn and possessive nature"),
    ("taurus", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "taurus", "marriage", "discord"],
     "Ch.27 v.8",
     "Mars in Taurus: discord in marital life, quarrels over finances "
     "and possessions, jealous and controlling toward spouse"),
    ("taurus", {},
     "mixed", "moderate",
     ["career_status"],
     ["mars", "taurus", "career", "agriculture"],
     "Ch.27 v.8",
     "Mars in Taurus: gains through agriculture, real estate, or food-related "
     "industries, but faces obstacles from superiors"),
    ("taurus", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "taurus", "health", "throat"],
     "Ch.27 v.9",
     "Mars in Taurus: susceptible to throat infections, dental problems, "
     "and afflictions of the face and neck region"),
    ("taurus", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mars", "taurus", "brothers"],
     "Ch.27 v.9",
     "Mars in Taurus: strained relations with siblings, disputes over "
     "shared property or inheritance matters"),
    ("taurus", {},
     "favorable", "moderate",
     ["property_vehicles"],
     ["mars", "taurus", "property", "land"],
     "Ch.27 v.10",
     "Mars in Taurus: acquires landed property and agricultural assets, "
     "benefits from real estate investments"),
    ("taurus", {},
     "unfavorable", "moderate",
     ["enemies_litigation"],
     ["mars", "taurus", "enemies", "litigation"],
     "Ch.27 v.10",
     "Mars in Taurus: faces litigation related to property, disputes with "
     "neighbours or relatives over boundary and land matters"),
    ("taurus", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mars", "taurus", "courage", "determination"],
     "Ch.27 v.11",
     "Mars in Taurus: determined and persevering but inflexible, "
     "courage expressed through endurance rather than aggression"),
    ("taurus", {},
     "unfavorable", "weak",
     ["fame_reputation"],
     ["mars", "taurus", "reputation"],
     "Ch.27 v.11",
     "Mars in Taurus: reputation suffers through association with persons "
     "of questionable character, scandal through romantic liaisons"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Gemini — Ch.27 (SAV1322–SAV1331)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_GEMINI_DATA = [
    ("gemini", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mars", "gemini", "intellect", "wit"],
     "Ch.27 v.12",
     "Mars in Gemini: sharp intellect and quick wit, skilled in debate "
     "and argumentation, excels in competitive academics"),
    ("gemini", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mars", "gemini", "restless", "temperament"],
     "Ch.27 v.12",
     "Mars in Gemini: restless and easily bored, pursues many interests "
     "simultaneously without completing tasks, mentally agitated"),
    ("gemini", {},
     "favorable", "moderate",
     ["career_status"],
     ["mars", "gemini", "career", "communication"],
     "Ch.27 v.13",
     "Mars in Gemini: success in journalism, law, engineering drafting, "
     "or technical writing, careers combining intellect with action"),
    ("gemini", {},
     "unfavorable", "moderate",
     ["progeny"],
     ["mars", "gemini", "brothers", "quarrels"],
     "Ch.27 v.13",
     "Mars in Gemini: quarrelsome relations with brothers and cousins, "
     "verbal disputes and misunderstandings with siblings"),
    ("gemini", {},
     "unfavorable", "weak",
     ["marriage"],
     ["mars", "gemini", "marriage", "arguments"],
     "Ch.27 v.14",
     "Mars in Gemini: marital discord through harsh speech and criticism, "
     "tendency to argue with spouse over trivial matters"),
    ("gemini", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "gemini", "health", "arms", "nervous"],
     "Ch.27 v.14",
     "Mars in Gemini: prone to injuries of arms, hands, and shoulders, "
     "nervous disorders and respiratory ailments"),
    ("gemini", {},
     "mixed", "moderate",
     ["wealth"],
     ["mars", "gemini", "wealth", "earnings"],
     "Ch.27 v.15",
     "Mars in Gemini: earns through multiple sources and side ventures "
     "but income fluctuates, inconsistent financial stability"),
    ("gemini", {},
     "favorable", "weak",
     ["enemies_litigation"],
     ["mars", "gemini", "enemies", "strategy"],
     "Ch.27 v.15",
     "Mars in Gemini: overcomes enemies through cunning and strategic "
     "communication rather than direct confrontation"),
    ("gemini", {},
     "unfavorable", "weak",
     ["property_vehicles"],
     ["mars", "gemini", "property"],
     "Ch.27 v.16",
     "Mars in Gemini: difficulty in acquiring permanent property, "
     "frequent changes of residence, unsettled domestic base"),
    ("gemini", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["mars", "gemini", "fame", "versatility"],
     "Ch.27 v.16",
     "Mars in Gemini: known for versatility and cleverness, "
     "reputation as skilled communicator but also as unreliable"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Cancer (debilitated) — Ch.27 (SAV1332–SAV1342)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_CANCER_DATA = [
    ("cancer", {},
     "unfavorable", "strong",
     ["character_temperament"],
     ["mars", "cancer", "debilitated", "courage"],
     "Ch.27 v.17",
     "Mars in Cancer (debilitated): diminished courage and willpower, "
     "lacks assertiveness, vacillates in decisions under pressure"),
    ("cancer", {},
     "unfavorable", "strong",
     ["physical_health"],
     ["mars", "cancer", "debilitated", "health", "blood"],
     "Ch.27 v.17",
     "Mars in Cancer (debilitated): blood-related disorders, stomach "
     "ailments, acidity, ulcers, and chest complaints"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["property_vehicles"],
     ["mars", "cancer", "debilitated", "property"],
     "Ch.27 v.18",
     "Mars in Cancer (debilitated): loss of ancestral property, "
     "difficulties in acquiring land or permanent residence"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["career_status"],
     ["mars", "cancer", "debilitated", "career"],
     "Ch.27 v.18",
     "Mars in Cancer (debilitated): unstable career, frequent job changes, "
     "difficulties with authority figures, denied promotions"),
    ("cancer", {},
     "unfavorable", "strong",
     ["mental_health"],
     ["mars", "cancer", "debilitated", "mental", "anxiety"],
     "Ch.27 v.19",
     "Mars in Cancer (debilitated): emotionally volatile, prone to anxiety "
     "and depression, anger mixed with sentimentality"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["progeny"],
     ["mars", "cancer", "debilitated", "brothers"],
     "Ch.27 v.19",
     "Mars in Cancer (debilitated): separation from brothers, lack of "
     "support from siblings, possible enmity with younger brothers"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["enemies_litigation"],
     ["mars", "cancer", "debilitated", "enemies"],
     "Ch.27 v.20",
     "Mars in Cancer (debilitated): defeated by enemies, prone to "
     "litigation losses, harassed by opponents and rivals"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "cancer", "debilitated", "marriage"],
     "Ch.27 v.20",
     "Mars in Cancer (debilitated): unhappy married life, emotional "
     "turbulence in partnerships, quarrels over domestic matters"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["mars", "cancer", "debilitated", "wealth", "loss"],
     "Ch.27 v.21",
     "Mars in Cancer (debilitated): financial instability, loss through "
     "bad investments, expenditure exceeds income"),
    ("cancer", {},
     "unfavorable", "weak",
     ["fame_reputation"],
     ["mars", "cancer", "debilitated", "reputation"],
     "Ch.27 v.21",
     "Mars in Cancer (debilitated): lacks public recognition, efforts go "
     "unappreciated, reputation marred by indecisiveness"),
    ("cancer", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "cancer", "debilitated", "accidents", "water"],
     "Ch.27 v.22",
     "Mars in Cancer (debilitated): danger from water, accidents near "
     "liquids, burns from hot fluids, surgical interventions on chest"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Leo — Ch.27 (SAV1343–SAV1352)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_LEO_DATA = [
    ("leo", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mars", "leo", "courage", "leadership"],
     "Ch.27 v.23",
     "Mars in Leo: commanding personality, lion-hearted courage, "
     "natural authority and regal bearing in conduct"),
    ("leo", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mars", "leo", "career", "government"],
     "Ch.27 v.23",
     "Mars in Leo: rises to positions of authority in government or "
     "military, gains favor from rulers and powerful persons"),
    ("leo", {},
     "favorable", "moderate",
     ["wealth", "property_vehicles"],
     ["mars", "leo", "wealth", "forest"],
     "Ch.27 v.24",
     "Mars in Leo: wealth from mountainous or forest regions, gains "
     "through government contracts and authoritative positions"),
    ("leo", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "leo", "health", "heart", "fever"],
     "Ch.27 v.24",
     "Mars in Leo: prone to heart-related ailments, high fevers, "
     "spinal problems, and inflammatory conditions"),
    ("leo", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "leo", "marriage", "dominance"],
     "Ch.27 v.25",
     "Mars in Leo: dominating in marriage, expects subservience from spouse, "
     "ego clashes lead to marital discord"),
    ("leo", {},
     "favorable", "moderate",
     ["enemies_litigation"],
     ["mars", "leo", "enemies", "victory"],
     "Ch.27 v.25",
     "Mars in Leo: vanquishes enemies decisively, successful in litigation, "
     "intimidates opponents through sheer force of personality"),
    ("leo", {},
     "mixed", "moderate",
     ["progeny"],
     ["mars", "leo", "brothers"],
     "Ch.27 v.26",
     "Mars in Leo: fewer brothers but those present are capable and strong, "
     "may have rivalry with siblings over leadership"),
    ("leo", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "leo", "anger", "pride"],
     "Ch.27 v.26",
     "Mars in Leo: excessive pride and arrogance, quick temper that "
     "alienates subordinates and well-wishers"),
    ("leo", {},
     "favorable", "moderate",
     ["career_status"],
     ["mars", "leo", "military", "adventure"],
     "Ch.27 v.27",
     "Mars in Leo: excels in adventurous pursuits, hunting, sports, "
     "military expeditions, and competitive endeavors"),
    ("leo", {},
     "favorable", "weak",
     ["intelligence_education"],
     ["mars", "leo", "knowledge", "strategy"],
     "Ch.27 v.27",
     "Mars in Leo: strategic thinker, skilled in political maneuvering, "
     "knowledge of warfare and administration"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Virgo — Ch.27 (SAV1353–SAV1362)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_VIRGO_DATA = [
    ("virgo", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mars", "virgo", "analytical", "critical"],
     "Ch.27 v.28",
     "Mars in Virgo: analytical and detail-oriented but overly critical, "
     "perfectionist tendencies cause friction with others"),
    ("virgo", {},
     "favorable", "moderate",
     ["career_status"],
     ["mars", "virgo", "career", "technical"],
     "Ch.27 v.28",
     "Mars in Virgo: success in technical and scientific careers, "
     "engineering, medicine, pharmacy, and precision work"),
    ("virgo", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "virgo", "courage", "timidity"],
     "Ch.27 v.29",
     "Mars in Virgo: courage diminished by excessive analysis, "
     "hesitates before acting, lacks boldness in confrontation"),
    ("virgo", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "virgo", "health", "digestive", "intestinal"],
     "Ch.27 v.29",
     "Mars in Virgo: digestive disorders, intestinal inflammations, "
     "hernia, and ailments of the lower abdomen"),
    ("virgo", {},
     "unfavorable", "weak",
     ["marriage"],
     ["mars", "virgo", "marriage", "criticism"],
     "Ch.27 v.30",
     "Mars in Virgo: critical of spouse, finds fault in domestic matters, "
     "marital tension through nagging and perfectionism"),
    ("virgo", {},
     "mixed", "moderate",
     ["wealth"],
     ["mars", "virgo", "wealth", "service"],
     "Ch.27 v.30",
     "Mars in Virgo: earns through service and skilled labour, moderate "
     "wealth but prudent management preserves resources"),
    ("virgo", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mars", "virgo", "brothers", "distance"],
     "Ch.27 v.31",
     "Mars in Virgo: limited support from brothers, siblings may live "
     "at a distance or have strained relations"),
    ("virgo", {},
     "favorable", "moderate",
     ["enemies_litigation"],
     ["mars", "virgo", "enemies", "method"],
     "Ch.27 v.31",
     "Mars in Virgo: defeats enemies through methodical planning and "
     "legal documentation rather than direct confrontation"),
    ("virgo", {},
     "unfavorable", "weak",
     ["property_vehicles"],
     ["mars", "virgo", "property"],
     "Ch.27 v.32",
     "Mars in Virgo: delayed acquisition of property, gains smaller "
     "assets rather than large estates"),
    ("virgo", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["mars", "virgo", "fame", "skill"],
     "Ch.27 v.32",
     "Mars in Virgo: recognized for technical skills and craftsmanship, "
     "reputation as meticulous worker rather than bold leader"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Libra — Ch.27 (SAV1363–SAV1372)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_LIBRA_DATA = [
    ("libra", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mars", "libra", "diplomacy", "aggression"],
     "Ch.27 v.33",
     "Mars in Libra: attempts to balance aggression with diplomacy, "
     "alternates between assertiveness and yielding, inner conflict"),
    ("libra", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "libra", "marriage", "passion"],
     "Ch.27 v.33",
     "Mars in Libra: excessive passion in relationships leads to "
     "complications, multiple attachments, jealousy in marriage"),
    ("libra", {},
     "mixed", "moderate",
     ["career_status"],
     ["mars", "libra", "career", "trade", "business"],
     "Ch.27 v.34",
     "Mars in Libra: success in trade, commerce, and business partnerships, "
     "but disagreements with business partners cause setbacks"),
    ("libra", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "libra", "courage", "indecision"],
     "Ch.27 v.34",
     "Mars in Libra: courage undermined by desire for approval, "
     "postpones decisive action seeking consensus"),
    ("libra", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "libra", "health", "kidney", "urinary"],
     "Ch.27 v.35",
     "Mars in Libra: kidney and urinary tract inflammations, "
     "lower back pain, reproductive system disorders"),
    ("libra", {},
     "mixed", "moderate",
     ["wealth"],
     ["mars", "libra", "wealth", "luxury"],
     "Ch.27 v.35",
     "Mars in Libra: earns well but spends lavishly on luxuries, "
     "fine clothing, and social entertainments"),
    ("libra", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mars", "libra", "brothers"],
     "Ch.27 v.36",
     "Mars in Libra: indifferent relations with siblings, lack of "
     "strong bonding, brothers may not be supportive"),
    ("libra", {},
     "mixed", "moderate",
     ["enemies_litigation"],
     ["mars", "libra", "enemies", "legal"],
     "Ch.27 v.36",
     "Mars in Libra: involvement in legal disputes, mixed results in "
     "litigation, enemies in business partnerships"),
    ("libra", {},
     "favorable", "weak",
     ["fame_reputation"],
     ["mars", "libra", "fame", "social"],
     "Ch.27 v.37",
     "Mars in Libra: gains social recognition through charm and networking, "
     "known in artistic or commercial circles"),
    ("libra", {},
     "unfavorable", "weak",
     ["property_vehicles"],
     ["mars", "libra", "property", "disputes"],
     "Ch.27 v.37",
     "Mars in Libra: property disputes with partners or spouse, "
     "joint ownership leads to conflicts and legal tangles"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Scorpio (own sign) — Ch.27 (SAV1373–SAV1383)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_SCORPIO_DATA = [
    ("scorpio", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mars", "scorpio", "own_sign", "courage", "intensity"],
     "Ch.27 v.38",
     "Mars in Scorpio (own sign): intense courage and determination, "
     "penetrating intellect, fearless in pursuing objectives"),
    ("scorpio", {},
     "favorable", "strong",
     ["career_status"],
     ["mars", "scorpio", "own_sign", "career", "investigation"],
     "Ch.27 v.38",
     "Mars in Scorpio (own sign): excels in investigation, research, surgery, "
     "military intelligence, and covert operations"),
    ("scorpio", {},
     "favorable", "moderate",
     ["enemies_litigation"],
     ["mars", "scorpio", "own_sign", "enemies", "destruction"],
     "Ch.27 v.39",
     "Mars in Scorpio (own sign): destroys enemies completely, "
     "relentless in pursuing adversaries, decisive in conflicts"),
    ("scorpio", {},
     "unfavorable", "strong",
     ["physical_health"],
     ["mars", "scorpio", "own_sign", "health", "surgery", "blood"],
     "Ch.27 v.39",
     "Mars in Scorpio (own sign): prone to surgical operations, "
     "blood disorders, piles, fistula, and reproductive ailments"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "scorpio", "own_sign", "vindictive", "secretive"],
     "Ch.27 v.40",
     "Mars in Scorpio (own sign): vindictive and secretive nature, "
     "holds grudges, capable of calculated retribution"),
    ("scorpio", {},
     "favorable", "moderate",
     ["wealth"],
     ["mars", "scorpio", "own_sign", "wealth", "inheritance"],
     "Ch.27 v.40",
     "Mars in Scorpio (own sign): gains through inheritance, insurance, "
     "or partner's resources, wealth from hidden sources"),
    ("scorpio", {},
     "favorable", "moderate",
     ["property_vehicles"],
     ["mars", "scorpio", "own_sign", "property"],
     "Ch.27 v.41",
     "Mars in Scorpio (own sign): acquires property through determined effort, "
     "benefits from underground resources, mines, or excavation"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "scorpio", "own_sign", "marriage", "intensity"],
     "Ch.27 v.41",
     "Mars in Scorpio (own sign): intense and possessive in marriage, "
     "jealousy and suspicion strain marital harmony"),
    ("scorpio", {},
     "mixed", "moderate",
     ["progeny"],
     ["mars", "scorpio", "own_sign", "brothers"],
     "Ch.27 v.42",
     "Mars in Scorpio (own sign): complex relations with brothers, "
     "deep loyalty but power struggles within sibling hierarchy"),
    ("scorpio", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["mars", "scorpio", "own_sign", "fame", "power"],
     "Ch.27 v.42",
     "Mars in Scorpio (own sign): gains fame through transformative actions, "
     "known for power, influence, and uncompromising stance"),
    ("scorpio", {},
     "favorable", "moderate",
     ["career_status"],
     ["mars", "scorpio", "own_sign", "surgery", "chemistry"],
     "Ch.27 v.43",
     "Mars in Scorpio (own sign): aptitude for surgery, chemistry, "
     "metallurgy, and work involving transformation of materials"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Sagittarius — Ch.27 (SAV1384–SAV1393)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_SAGITTARIUS_DATA = [
    ("sagittarius", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mars", "sagittarius", "righteous", "courage"],
     "Ch.27 v.44",
     "Mars in Sagittarius: righteous courage, fights for just causes, "
     "principled warrior who follows dharmic conduct"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mars", "sagittarius", "career", "law", "military"],
     "Ch.27 v.44",
     "Mars in Sagittarius: success in law enforcement, military command, "
     "judicial roles, or religious leadership positions"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["spirituality"],
     ["mars", "sagittarius", "dharma", "teaching"],
     "Ch.27 v.45",
     "Mars in Sagittarius: active in religious or philosophical pursuits, "
     "may teach martial or physical disciplines"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["wealth", "property_vehicles"],
     ["mars", "sagittarius", "wealth", "father"],
     "Ch.27 v.45",
     "Mars in Sagittarius: inherits paternal wealth, gains through "
     "long-distance ventures, trade with foreign lands"),
    ("sagittarius", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "sagittarius", "health", "thighs", "liver"],
     "Ch.27 v.46",
     "Mars in Sagittarius: ailments of thighs and hips, liver "
     "inflammations, injuries during travel or sports"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["progeny"],
     ["mars", "sagittarius", "brothers", "support"],
     "Ch.27 v.46",
     "Mars in Sagittarius: supportive brothers, harmonious sibling "
     "relations, brothers may be in military or law"),
    ("sagittarius", {},
     "mixed", "moderate",
     ["marriage"],
     ["mars", "sagittarius", "marriage", "independence"],
     "Ch.27 v.47",
     "Mars in Sagittarius: values independence in marriage, spouse "
     "must share philosophical outlook, friction over beliefs"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["enemies_litigation"],
     ["mars", "sagittarius", "enemies", "dharma"],
     "Ch.27 v.47",
     "Mars in Sagittarius: overcomes enemies through righteous action, "
     "success in legal matters through ethical conduct"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mars", "sagittarius", "knowledge", "philosophy"],
     "Ch.27 v.48",
     "Mars in Sagittarius: inclined toward higher learning, philosophy, "
     "and strategic studies, good grasp of scriptures"),
    ("sagittarius", {},
     "favorable", "weak",
     ["fame_reputation"],
     ["mars", "sagittarius", "fame", "honour"],
     "Ch.27 v.48",
     "Mars in Sagittarius: honoured for valour and righteousness, "
     "respected in religious and academic institutions"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Capricorn (exalted) — Ch.27 (SAV1394–SAV1404)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_CAPRICORN_DATA = [
    ("capricorn", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mars", "capricorn", "exalted", "courage", "discipline"],
     "Ch.27 v.49",
     "Mars in Capricorn (exalted): supreme courage combined with discipline, "
     "strategic and methodical warrior, achieves through perseverance"),
    ("capricorn", {},
     "favorable", "strong",
     ["career_status"],
     ["mars", "capricorn", "exalted", "career", "authority"],
     "Ch.27 v.49",
     "Mars in Capricorn (exalted): attains high position of authority, "
     "excels in military command, administration, and engineering"),
    ("capricorn", {},
     "favorable", "strong",
     ["wealth", "property_vehicles"],
     ["mars", "capricorn", "exalted", "wealth", "property"],
     "Ch.27 v.50",
     "Mars in Capricorn (exalted): acquires substantial wealth and "
     "extensive landed property, vehicles, and material assets"),
    ("capricorn", {},
     "favorable", "strong",
     ["fame_reputation"],
     ["mars", "capricorn", "exalted", "fame", "honour"],
     "Ch.27 v.50",
     "Mars in Capricorn (exalted): widely renowned and honoured, "
     "gains fame through leadership and decisive achievements"),
    ("capricorn", {},
     "favorable", "moderate",
     ["enemies_litigation"],
     ["mars", "capricorn", "exalted", "enemies", "victory"],
     "Ch.27 v.51",
     "Mars in Capricorn (exalted): thoroughly vanquishes enemies, "
     "opponents dare not challenge, success in all disputes"),
    ("capricorn", {},
     "favorable", "moderate",
     ["progeny"],
     ["mars", "capricorn", "exalted", "brothers"],
     "Ch.27 v.51",
     "Mars in Capricorn (exalted): well-supported by brothers, siblings "
     "prosper and maintain harmonious relations"),
    ("capricorn", {},
     "mixed", "moderate",
     ["marriage"],
     ["mars", "capricorn", "exalted", "marriage"],
     "Ch.27 v.52",
     "Mars in Capricorn (exalted): spouse is capable and industrious, "
     "but native's career focus may cause emotional distance"),
    ("capricorn", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "capricorn", "exalted", "health", "bones", "joints"],
     "Ch.27 v.52",
     "Mars in Capricorn (exalted): prone to bone fractures, joint injuries, "
     "knee problems, and ailments of the skeletal system"),
    ("capricorn", {},
     "favorable", "strong",
     ["career_status"],
     ["mars", "capricorn", "exalted", "military", "engineering"],
     "Ch.27 v.53",
     "Mars in Capricorn (exalted): exceptional aptitude for military strategy, "
     "civil engineering, architecture, and construction"),
    ("capricorn", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mars", "capricorn", "exalted", "ambition", "determination"],
     "Ch.27 v.53",
     "Mars in Capricorn (exalted): highly ambitious and goal-oriented, "
     "patient in pursuit, does not rest until objective is achieved"),
    ("capricorn", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mars", "capricorn", "exalted", "practical", "knowledge"],
     "Ch.27 v.54",
     "Mars in Capricorn (exalted): practical intelligence, excels in "
     "applied sciences, technical education, and hands-on skills"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Aquarius — Ch.27 (SAV1405–SAV1414)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_AQUARIUS_DATA = [
    ("aquarius", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mars", "aquarius", "unconventional", "courage"],
     "Ch.27 v.55",
     "Mars in Aquarius: unconventional approach to challenges, courage "
     "expressed through social causes and humanitarian action"),
    ("aquarius", {},
     "mixed", "moderate",
     ["career_status"],
     ["mars", "aquarius", "career", "technology", "reform"],
     "Ch.27 v.55",
     "Mars in Aquarius: success in technology, electronics, social reform, "
     "or unconventional career paths, works for collective causes"),
    ("aquarius", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["mars", "aquarius", "wealth", "irregular"],
     "Ch.27 v.56",
     "Mars in Aquarius: irregular income, financial ups and downs, "
     "earns through unusual means but struggles to save"),
    ("aquarius", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "aquarius", "health", "circulation", "legs"],
     "Ch.27 v.56",
     "Mars in Aquarius: circulatory disorders, varicose veins, "
     "injuries to legs and ankles, nervous system ailments"),
    ("aquarius", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["mars", "aquarius", "marriage", "detachment"],
     "Ch.27 v.57",
     "Mars in Aquarius: emotional detachment in marriage, prioritizes "
     "social circles over spouse, unconventional relationship views"),
    ("aquarius", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mars", "aquarius", "brothers", "distance"],
     "Ch.27 v.57",
     "Mars in Aquarius: brothers may live at a distance, relationship "
     "with siblings is friendly but lacks deep bonding"),
    ("aquarius", {},
     "mixed", "moderate",
     ["enemies_litigation"],
     ["mars", "aquarius", "enemies", "groups"],
     "Ch.27 v.58",
     "Mars in Aquarius: enemies from social groups or organizations, "
     "conflicts with community members, mixed litigation results"),
    ("aquarius", {},
     "unfavorable", "weak",
     ["property_vehicles"],
     ["mars", "aquarius", "property"],
     "Ch.27 v.58",
     "Mars in Aquarius: difficulty acquiring property through conventional "
     "means, may gain unusual or non-traditional assets"),
    ("aquarius", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["mars", "aquarius", "fame", "reform"],
     "Ch.27 v.59",
     "Mars in Aquarius: gains recognition in progressive or reform movements, "
     "known for unorthodox views and social activism"),
    ("aquarius", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "aquarius", "anger", "rebellion"],
     "Ch.27 v.59",
     "Mars in Aquarius: rebellious and defiant of authority, anger "
     "directed at systemic injustice, clashes with establishment"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars in Pisces — Ch.27 (SAV1415–SAV1424)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_PISCES_DATA = [
    ("pisces", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mars", "pisces", "courage", "passive"],
     "Ch.27 v.60",
     "Mars in Pisces: courage diluted by compassion and hesitation, "
     "lacks aggressive drive, prefers passive resistance"),
    ("pisces", {},
     "mixed", "moderate",
     ["career_status"],
     ["mars", "pisces", "career", "medicine", "healing"],
     "Ch.27 v.60",
     "Mars in Pisces: aptitude for healing arts, hospital work, "
     "marine careers, or charitable institutions"),
    ("pisces", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mars", "pisces", "health", "feet", "blood"],
     "Ch.27 v.61",
     "Mars in Pisces: ailments of the feet, blood impurities, "
     "susceptibility to infections and waterborne diseases"),
    ("pisces", {},
     "unfavorable", "moderate",
     ["enemies_litigation"],
     ["mars", "pisces", "enemies", "hidden"],
     "Ch.27 v.61",
     "Mars in Pisces: harassed by hidden enemies and secret opponents, "
     "losses through deceit and treachery of trusted persons"),
    ("pisces", {},
     "mixed", "moderate",
     ["wealth"],
     ["mars", "pisces", "wealth", "charity"],
     "Ch.27 v.62",
     "Mars in Pisces: earns adequately but spends generously on charity "
     "and compassionate causes, wealth dissipated through giving"),
    ("pisces", {},
     "mixed", "moderate",
     ["spirituality"],
     ["mars", "pisces", "spiritual", "pilgrimage"],
     "Ch.27 v.62",
     "Mars in Pisces: inclined toward spiritual pursuits, undertakes "
     "pilgrimages, energy directed toward devotional activities"),
    ("pisces", {},
     "unfavorable", "weak",
     ["marriage"],
     ["mars", "pisces", "marriage", "sacrifice"],
     "Ch.27 v.63",
     "Mars in Pisces: self-sacrificing in marriage but feels unappreciated, "
     "spouse may be demanding or sickly"),
    ("pisces", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mars", "pisces", "brothers"],
     "Ch.27 v.63",
     "Mars in Pisces: limited support from brothers, siblings may be "
     "in distant lands or involved in spiritual pursuits"),
    ("pisces", {},
     "unfavorable", "weak",
     ["property_vehicles"],
     ["mars", "pisces", "property", "loss"],
     "Ch.27 v.64",
     "Mars in Pisces: difficulty retaining property, losses through "
     "water damage, flooding, or mismanagement of assets"),
    ("pisces", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["mars", "pisces", "fame", "compassion"],
     "Ch.27 v.64",
     "Mars in Pisces: known for compassion and charitable works, "
     "reputation in spiritual or healing communities"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# General / Conditional rules — Ch.27 (SAV1425–SAV1430)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_GENERAL_DATA = [
    # These use special placement_value or conditions
    ("general_dignity", {"dignity": "exalted_or_own"},
     "favorable", "strong",
     ["career_status", "fame_reputation", "character_temperament"],
     ["mars", "dignity", "exalted", "own_sign", "general"],
     "Ch.27 v.65",
     "Mars in own sign or exalted: native is brave, wealthy, leader of men, "
     "conqueror of enemies, blessed with brothers and landed property"),
    ("general_dignity", {"dignity": "debilitated_or_enemy"},
     "unfavorable", "strong",
     ["character_temperament", "physical_health", "wealth"],
     ["mars", "dignity", "debilitated", "enemy_sign", "general"],
     "Ch.27 v.66",
     "Mars debilitated or in enemy sign: cowardly, sickly, poor, troubled by "
     "enemies, devoid of brothers, prone to accidents and blood disorders"),
    ("general_aspect", {"condition": "benefic_aspect"},
     "favorable", "moderate",
     ["character_temperament", "career_status"],
     ["mars", "benefic_aspect", "modification", "general"],
     "Ch.27 v.67",
     "Mars receiving benefic aspect: negative traits of Mars placement are "
     "mitigated, courage channeled constructively, career gains enhanced"),
    ("general_aspect", {"condition": "malefic_aspect"},
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     ["mars", "malefic_aspect", "modification", "general"],
     "Ch.27 v.67",
     "Mars receiving malefic aspect: aggressive tendencies amplified, "
     "increased accident-proneness, more enemies and litigation"),
    ("general_house_lord", {"condition": "mars_as_yogakaraka"},
     "favorable", "strong",
     ["career_status", "wealth", "fame_reputation"],
     ["mars", "yogakaraka", "cancer_lagna", "leo_lagna", "general"],
     "Ch.27 v.68",
     "Mars as yogakaraka (Cancer/Leo lagna) in good sign placement: "
     "extraordinary results in career, wealth, and social standing"),
    ("general_combustion", {"condition": "combust"},
     "unfavorable", "moderate",
     ["character_temperament", "progeny", "physical_health"],
     ["mars", "combust", "sun", "general"],
     "Ch.27 v.68",
     "Mars combust (close to Sun): courage diminished, health problems "
     "related to heat and blood, difficulties with brothers"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder
# ═══════════════════════════════════════════════════════════════════════════════

def _make_sign_rules(
    data: list[tuple],
    start_num: int,
) -> list[RuleRecord]:
    """Convert raw tuples into RuleRecord objects for Mars sign placements."""
    rules: list[RuleRecord] = []
    num = start_num
    for row in data:
        (sign_or_label, extra_quals, odir, oint,
         odoms, extra_tags, vref, desc) = row

        rid = f"SAV{num:04d}"

        # Build primary_condition
        if sign_or_label in (
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
        ):
            primary = {
                "planet": "mars",
                "placement_type": "sign_placement",
                "placement_value": sign_or_label,
            }
            if extra_quals:
                primary.update(extra_quals)
            timing = "unspecified"
        else:
            # General / conditional rules
            primary = {
                "planet": "mars",
                "placement_type": "general_condition",
                "condition_label": sign_or_label,
            }
            primary.update(extra_quals)
            timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "sign_placement", "mars"] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter="Ch.27",
            school="parashari",
            category="sign_predictions",
            description=f"[Saravali — Mars in signs] {desc}",
            confidence=0.65,
            tags=tags,
            implemented=False,
            primary_condition=primary,
            outcome_domains=odoms,
            outcome_direction=odir,
            outcome_intensity=oint,
            outcome_timing=timing,
            lagna_scope=[],
            verse_ref=vref,
            phase="1B_matrix",
            system="natal",
            prediction_type="event",
            gender_scope="universal",
            certainty_level="definite",
            strength_condition="any",
            house_system="sign_based",
            ayanamsha_sensitive=False,
            evaluation_method="placement_check",
            last_modified_session="S305",
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    """Assemble all 130 Mars-in-signs rules."""
    all_data = [
        (_MARS_ARIES_DATA, 1301),        # SAV1301–SAV1311  (11)
        (_MARS_TAURUS_DATA, 1312),        # SAV1312–SAV1321  (10)
        (_MARS_GEMINI_DATA, 1322),        # SAV1322–SAV1331  (10)
        (_MARS_CANCER_DATA, 1332),        # SAV1332–SAV1342  (11)
        (_MARS_LEO_DATA, 1343),           # SAV1343–SAV1352  (10)
        (_MARS_VIRGO_DATA, 1353),         # SAV1353–SAV1362  (10)
        (_MARS_LIBRA_DATA, 1363),         # SAV1363–SAV1372  (10)
        (_MARS_SCORPIO_DATA, 1373),       # SAV1373–SAV1383  (11)
        (_MARS_SAGITTARIUS_DATA, 1384),   # SAV1384–SAV1393  (10)
        (_MARS_CAPRICORN_DATA, 1394),     # SAV1394–SAV1404  (11)
        (_MARS_AQUARIUS_DATA, 1405),      # SAV1405–SAV1414  (10)
        (_MARS_PISCES_DATA, 1415),        # SAV1415–SAV1424  (10)
        (_MARS_GENERAL_DATA, 1425),       # SAV1425–SAV1430  (6)
    ]
    rules: list[RuleRecord] = []
    for data, start in all_data:
        rules.extend(_make_sign_rules(data, start))
    return rules


SARAVALI_SIGNS_3_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_3_REGISTRY.add(_rule)
