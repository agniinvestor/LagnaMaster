"""src/corpus/saravali_conjunctions_2.py — S274: Saravali two-planet conjunctions.

SAV131–SAV260 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 16-18:
  Sun-Jupiter  (Ch.16-17) — SAV131–SAV173 (43 rules)
  Sun-Venus    (Ch.17)    — SAV174–SAV216 (43 rules)
  Sun-Saturn   (Ch.17-18) — SAV217–SAV260 (44 rules)

Saravali (by Kalyana Varma, ~800 CE) is the most detailed classical text on
planetary conjunctions, giving house-by-house results for every two-planet pair.

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Sun-Jupiter Conjunction — Ch.16-17 (SAV131–SAV173)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_JUPITER_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_jupiter", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "1st_house"],
     "Ch.16 v.36",
     "Sun-Jupiter conjunction in 1st house: commanding personality, respected "
     "leader, blessed with wisdom and authority from early life"),
    ("sun_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "1st_house", "wisdom"],
     "Ch.16 v.37",
     "Sun-Jupiter conjunction in 1st house: virtuous and learned, generous "
     "disposition, inclined toward dharmic pursuits and counseling"),
    ("sun_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["physical_health", "longevity"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "1st_house", "health"],
     "Ch.16 v.38a",
     "Sun-Jupiter conjunction in 1st house: robust constitution protected "
     "by Jupiter's grace, good vitality, resilient physical health"),
    # House 2
    ("sun_jupiter", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "2nd_house"],
     "Ch.16 v.38",
     "Sun-Jupiter conjunction in 2nd house: eloquent speech imbued with wisdom, "
     "wealth through teaching, advisory roles, or scholarly pursuits"),
    ("sun_jupiter", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "2nd_house", "family"],
     "Ch.16 v.39",
     "Sun-Jupiter conjunction in 2nd house: born into respectable family, "
     "truthful speech, gains through family lineage and inheritance"),
    # House 3
    ("sun_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "3rd_house"],
     "Ch.16 v.40",
     "Sun-Jupiter conjunction in 3rd house: courageous with righteous intent, "
     "skilled in communication, respected among siblings and peers"),
    ("sun_jupiter", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "3rd_house", "effort"],
     "Ch.16 v.41",
     "Sun-Jupiter conjunction in 3rd house: success through personal initiative, "
     "but miserly with resources despite possessing ample wealth"),
    # House 4
    ("sun_jupiter", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "4th_house"],
     "Ch.16 v.42",
     "Sun-Jupiter conjunction in 4th house: blessed with property, vehicles, "
     "and domestic comforts, learned in traditional sciences"),
    ("sun_jupiter", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["mental_health", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "4th_house", "peace"],
     "Ch.16 v.43",
     "Sun-Jupiter conjunction in 4th house: inner peace through spiritual "
     "practice, happiness from mother, tranquil domestic environment"),
    # House 5
    ("sun_jupiter", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "5th_house"],
     "Ch.17 v.37",
     "Sun-Jupiter conjunction in 5th house: exceptional wisdom and intellect, "
     "ministerial or advisory position, fame through scholarship"),
    ("sun_jupiter", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "5th_house", "progeny"],
     "Ch.17 v.38",
     "Sun-Jupiter conjunction in 5th house: blessed with worthy children, "
     "success in speculation with wise judgment, creative brilliance"),
    ("sun_jupiter", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "5th_house", "status"],
     "Ch.17 v.38a",
     "Sun-Jupiter conjunction in 5th house: gains through government or "
     "royal patronage, administrative wisdom, respected counselor"),
    # House 6
    ("sun_jupiter", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["enemies_litigation", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "6th_house"],
     "Ch.17 v.39",
     "Sun-Jupiter conjunction in 6th house: overcomes enemies through righteous "
     "conduct, success in competitive endeavors by moral authority"),
    ("sun_jupiter", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "wealth"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "6th_house", "health"],
     "Ch.17 v.40",
     "Sun-Jupiter conjunction in 6th house: liver and bilious disorders, "
     "expenditure on health matters, debts from generous spending"),
    # House 7
    ("sun_jupiter", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "7th_house"],
     "Ch.17 v.41",
     "Sun-Jupiter conjunction in 7th house: righteous but domineering in "
     "partnerships, spouse from respectable family, ego in marriage"),
    ("sun_jupiter", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "7th_house", "trade"],
     "Ch.17 v.42",
     "Sun-Jupiter conjunction in 7th house: successful business partnerships, "
     "gains through foreign connections, ethical commerce"),
    ("sun_jupiter", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "7th_house", "spouse_dharma"],
     "Ch.17 v.42a",
     "Sun-Jupiter conjunction in 7th house: spouse inclined toward religion, "
     "philosophical differences in marriage, moral expectations cause tension"),
    # House 8
    ("sun_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "8th_house"],
     "Ch.17 v.43",
     "Sun-Jupiter conjunction in 8th house: Jupiter's protection grants "
     "longevity despite 8th house placement, interest in occult wisdom"),
    ("sun_jupiter", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "8th_house", "loss"],
     "Ch.17 v.44",
     "Sun-Jupiter conjunction in 8th house: inheritance disputes, loss of "
     "reputation through hidden matters, wealth from unexpected sources"),
    ("sun_jupiter", "conjunction_in_house", 8, {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "8th_house", "research"],
     "Ch.17 v.44a",
     "Sun-Jupiter conjunction in 8th house: deep research ability in "
     "metaphysical subjects, philosophical understanding of mortality"),
    # House 9
    ("sun_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "9th_house"],
     "Ch.17 v.45",
     "Sun-Jupiter conjunction in 9th house: deeply religious and philosophical, "
     "revered as teacher or spiritual guide, father is distinguished"),
    ("sun_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "9th_house", "fortune"],
     "Ch.17 v.46",
     "Sun-Jupiter conjunction in 9th house: extremely fortunate, royal patronage, "
     "wealth through righteous means, pilgrimage and higher learning"),
    ("sun_jupiter", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "9th_house", "preceptor"],
     "Ch.17 v.46a",
     "Sun-Jupiter conjunction in 9th house: becomes a revered preceptor, "
     "passes wisdom to disciples, benefits from guru's blessings"),
    # House 10
    ("sun_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "10th_house"],
     "Ch.17 v.47",
     "Sun-Jupiter conjunction in 10th house: eminent career in governance, law, "
     "or education, widespread fame, commands respect of multitudes"),
    ("sun_jupiter", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "character_temperament"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "10th_house", "virtue"],
     "Ch.17 v.48",
     "Sun-Jupiter conjunction in 10th house: charitable and philanthropic, "
     "earns wealth through ethical professional conduct"),
    ("sun_jupiter", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "10th_house", "judicial"],
     "Ch.17 v.48a",
     "Sun-Jupiter conjunction in 10th house: aptitude for judicial or "
     "religious office, success in law, academia, or temple administration"),
    # House 11
    ("sun_jupiter", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "11th_house"],
     "Ch.17 v.49",
     "Sun-Jupiter conjunction in 11th house: abundant gains from multiple "
     "sources, influential friends, fulfillment of desires"),
    ("sun_jupiter", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "11th_house", "honor"],
     "Ch.17 v.50",
     "Sun-Jupiter conjunction in 11th house: honored by rulers and scholars, "
     "truthful nature attracts loyal supporters and elder siblings"),
    # House 12
    ("sun_jupiter", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "12th_house"],
     "Ch.17 v.51",
     "Sun-Jupiter conjunction in 12th house: spiritual liberation tendencies, "
     "expenditure on religious causes, settles away from birthplace"),
    ("sun_jupiter", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya", "12th_house", "loss"],
     "Ch.17 v.52",
     "Sun-Jupiter conjunction in 12th house: loss of position and wealth, "
     "diminished social status, hidden enemies undermine reputation"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_jupiter", "conjunction_condition", "guru_aditya_yoga_proper", {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "guru_aditya_yoga"],
     "Ch.16 v.44",
     "Guru-Aditya Yoga (Sun-Jupiter conjunction with Jupiter unburnt): exceptional "
     "wisdom, fame through learning, advisory or ministerial position"),
    ("sun_jupiter", "conjunction_condition", "jupiter_combust", {},
     "unfavorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "combust"],
     "Ch.16 v.45",
     "Jupiter combust by Sun (within 11 degrees): diminished wisdom, false guru "
     "tendencies, spiritual pretensions without genuine understanding"),
    ("sun_jupiter", "conjunction_condition", "in_sagittarius", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.16 v.46",
     "Sun-Jupiter conjunction in Sagittarius (Jupiter's own sign): amplified "
     "beneficence, dharmic authority, revered teacher or philosopher"),
    ("sun_jupiter", "conjunction_condition", "in_pisces", {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "own_sign", "pisces"],
     "Ch.16 v.47",
     "Sun-Jupiter conjunction in Pisces (Jupiter's own sign): profound spiritual "
     "insight, compassionate leadership, intuitive wisdom amplified"),
    ("sun_jupiter", "conjunction_condition", "in_leo_sun_own", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "jupiter", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.17 v.53",
     "Sun-Jupiter conjunction in Leo (Sun's own sign): authoritative wisdom, "
     "government or administrative leadership with moral compass"),
    ("sun_jupiter", "conjunction_condition", "in_saturn_sign_capricorn", {},
     "unfavorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "jupiter", "conjunction", "saravali", "saturn_sign", "capricorn"],
     "Ch.17 v.54",
     "Sun-Jupiter conjunction in Capricorn (Saturn's sign): restricted fortune, "
     "delays in achieving authority, wisdom constrained by circumstances"),
    ("sun_jupiter", "conjunction_condition", "in_saturn_sign_aquarius", {},
     "unfavorable", "moderate",
     ["spirituality", "career_status"],
     ["sun", "jupiter", "conjunction", "saravali", "saturn_sign", "aquarius"],
     "Ch.17 v.55",
     "Sun-Jupiter conjunction in Aquarius (Saturn's sign): unconventional beliefs "
     "face resistance, delayed recognition of scholarly merit"),
    ("sun_jupiter", "conjunction_condition", "exalted_jupiter_cancer", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["sun", "jupiter", "conjunction", "saravali", "exaltation", "cancer"],
     "Ch.17 v.56",
     "Sun-Jupiter conjunction in Cancer (Jupiter exalted): supreme beneficence, "
     "wealth and wisdom in abundance, divine grace and protection"),
    ("sun_jupiter", "conjunction_condition", "debilitated_jupiter_capricorn", {},
     "unfavorable", "strong",
     ["spirituality", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "debilitation", "capricorn"],
     "Ch.17 v.57",
     "Sun-Jupiter conjunction in Capricorn (Jupiter debilitated): corrupted "
     "wisdom, materialistic spirituality, misguided counsel to others"),
    ("sun_jupiter", "conjunction_condition", "moon_aspect_emotional_wisdom", {},
     "favorable", "moderate",
     ["mental_health", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "moon_aspect"],
     "Ch.17 v.58",
     "Sun-Jupiter conjunction aspected by Moon: emotional wisdom, empathetic "
     "leadership, intuitive understanding combined with scholarly knowledge"),
    ("sun_jupiter", "conjunction_condition", "mars_aspect_dharmic_warrior", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["sun", "jupiter", "conjunction", "saravali", "mars_aspect"],
     "Ch.17 v.59",
     "Sun-Jupiter conjunction aspected by Mars: dharmic warrior, courage in "
     "pursuit of righteousness, aggressive defense of moral principles"),
    ("sun_jupiter", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     ["sun", "jupiter", "conjunction", "saravali", "kendra"],
     "Ch.17 v.60",
     "Sun-Jupiter conjunction in any kendra (1/4/7/10): Guru-Aditya yoga "
     "gains angular strength, wisdom and authority widely recognized"),
    ("sun_jupiter", "conjunction_condition", "trikona_placement", {},
     "favorable", "strong",
     ["spirituality", "wealth"],
     ["sun", "jupiter", "conjunction", "saravali", "trikona"],
     "Ch.17 v.61",
     "Sun-Jupiter conjunction in any trikona (1/5/9): supreme dharmic merit, "
     "fortune through wisdom, blessings of preceptor and father"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun-Venus Conjunction — Ch.17 (SAV174–SAV216)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_VENUS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_venus", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "1st_house"],
     "Ch.17 v.62",
     "Sun-Venus conjunction in 1st house: attractive appearance with commanding "
     "presence, artistic temperament conflicts with authoritative ego"),
    ("sun_venus", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "1st_house", "romance"],
     "Ch.17 v.63",
     "Sun-Venus conjunction in 1st house: romantic nature but ego dominates "
     "relationships, artistic career hampered by pride"),
    ("sun_venus", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "1st_house", "luxury"],
     "Ch.17 v.63a",
     "Sun-Venus conjunction in 1st house: inclined toward luxury goods and "
     "fine arts, earns through beauty-related professions, charming presence"),
    # House 2
    ("sun_venus", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["wealth", "physical_appearance"],
     ["sun", "venus", "conjunction", "saravali", "2nd_house"],
     "Ch.17 v.64",
     "Sun-Venus conjunction in 2nd house: wealth through artistic pursuits, "
     "sweet and melodious speech, attractive facial features"),
    ("sun_venus", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["sun", "venus", "conjunction", "saravali", "2nd_house", "luxury"],
     "Ch.17 v.65",
     "Sun-Venus conjunction in 2nd house: luxurious lifestyle but excessive "
     "spending on pleasures, family wealth fluctuates with indulgence"),
    # House 3
    ("sun_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "venus", "conjunction", "saravali", "3rd_house"],
     "Ch.17 v.66",
     "Sun-Venus conjunction in 3rd house: talented in performing arts, "
     "courageous in creative expression, harmonious sibling relations"),
    ("sun_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "3rd_house", "media"],
     "Ch.17 v.67",
     "Sun-Venus conjunction in 3rd house: success in media, advertising, or "
     "entertainment industry, gains through short artistic travels"),
    # House 4
    ("sun_venus", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["property_vehicles", "wealth"],
     ["sun", "venus", "conjunction", "saravali", "4th_house"],
     "Ch.17 v.68",
     "Sun-Venus conjunction in 4th house: beautiful home and luxury vehicles, "
     "comforts from mother, aesthetically pleasing domestic life"),
    ("sun_venus", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["mental_health", "marriage"],
     ["sun", "venus", "conjunction", "saravali", "4th_house", "heart"],
     "Ch.17 v.69",
     "Sun-Venus conjunction in 4th house: emotional sensitivity in love "
     "matters, domestic peace disturbed by romantic complications"),
    ("sun_venus", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "4th_house", "education"],
     "Ch.17 v.69a",
     "Sun-Venus conjunction in 4th house: education in fine arts or music, "
     "mother possesses artistic talent, culturally refined upbringing"),
    # House 5
    ("sun_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "5th_house"],
     "Ch.17 v.70",
     "Sun-Venus conjunction in 5th house: creative intelligence, success in "
     "performing arts, dramatic talent brings recognition"),
    ("sun_venus", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["progeny", "marriage"],
     ["sun", "venus", "conjunction", "saravali", "5th_house", "romance"],
     "Ch.17 v.71",
     "Sun-Venus conjunction in 5th house: romantic affairs before marriage, "
     "children may be artistically gifted but relationship with them complex"),
    ("sun_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "5th_house", "speculation"],
     "Ch.17 v.71a",
     "Sun-Venus conjunction in 5th house: gains through entertainment, "
     "speculation in luxury or art markets, creative investments prosper"),
    # House 6
    ("sun_venus", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["marriage", "enemies_litigation"],
     ["sun", "venus", "conjunction", "saravali", "6th_house"],
     "Ch.17 v.72",
     "Sun-Venus conjunction in 6th house: enmity through romantic entanglements, "
     "marriage difficulties, disputes over aesthetic or financial matters"),
    ("sun_venus", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["career_status", "physical_health"],
     ["sun", "venus", "conjunction", "saravali", "6th_house", "service"],
     "Ch.17 v.73",
     "Sun-Venus conjunction in 6th house: service in artistic administration, "
     "urinary or reproductive health concerns, debts from luxury"),
    # House 7
    ("sun_venus", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "7th_house"],
     "Ch.17 v.74",
     "Sun-Venus conjunction in 7th house: ego clashes in marriage, spouse "
     "artistic but relationship suffers from dominance struggles"),
    ("sun_venus", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["sun", "venus", "conjunction", "saravali", "7th_house", "partner"],
     "Ch.17 v.75",
     "Sun-Venus conjunction in 7th house: wealthy spouse but marital discord, "
     "business partnerships strained by aesthetic disagreements"),
    ("sun_venus", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["sun", "venus", "conjunction", "saravali", "7th_house", "combust_marriage"],
     "Ch.17 v.76",
     "Sun-Venus conjunction in 7th house: delayed marriage or multiple "
     "relationships, spouse's health affected, reproductive difficulties"),
    # House 8
    ("sun_venus", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["marriage", "longevity"],
     ["sun", "venus", "conjunction", "saravali", "8th_house"],
     "Ch.17 v.77",
     "Sun-Venus conjunction in 8th house: sudden disruptions in relationships, "
     "hidden affairs, wealth through spouse but with complications"),
    ("sun_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["sun", "venus", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.17 v.78",
     "Sun-Venus conjunction in 8th house: interest in tantric or occult arts, "
     "inheritance from spouse, transformation through relationships"),
    # House 9
    ("sun_venus", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "9th_house"],
     "Ch.17 v.79",
     "Sun-Venus conjunction in 9th house: devotion expressed through art and "
     "beauty, religious practice with aesthetic sensibility"),
    ("sun_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.17 v.80",
     "Sun-Venus conjunction in 9th house: fortunate in artistic career, "
     "gains through father, patronage from cultural institutions"),
    # House 10
    ("sun_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "10th_house"],
     "Ch.17 v.81",
     "Sun-Venus conjunction in 10th house: career in arts, entertainment, or "
     "luxury goods, fame through aesthetic achievements"),
    ("sun_venus", "conjunction_in_house", 10, {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "10th_house", "admin"],
     "Ch.17 v.82",
     "Sun-Venus conjunction in 10th house: administrative talent with artistic "
     "flair, but tension between creative freedom and authority"),
    ("sun_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "10th_house", "luxury_trade"],
     "Ch.17 v.82a",
     "Sun-Venus conjunction in 10th house: wealth through luxury trade, "
     "jewelry, cosmetics, or fashion industry, public appreciation"),
    # House 11
    ("sun_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "11th_house"],
     "Ch.17 v.83",
     "Sun-Venus conjunction in 11th house: gains through arts and entertainment, "
     "influential artistic friends, desires fulfilled through beauty"),
    ("sun_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["marriage", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "11th_house", "social"],
     "Ch.17 v.84",
     "Sun-Venus conjunction in 11th house: benefits from spouse's social "
     "connections, elder siblings in artistic fields, network gains"),
    # House 12
    ("sun_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["marriage", "spirituality"],
     ["sun", "venus", "conjunction", "saravali", "12th_house"],
     "Ch.17 v.85",
     "Sun-Venus conjunction in 12th house: secret love affairs, expenditure "
     "on pleasures, bed comforts but marital dissatisfaction"),
    ("sun_venus", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "physical_health"],
     ["sun", "venus", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.17 v.86",
     "Sun-Venus conjunction in 12th house: financial losses through indulgence, "
     "eye troubles, depleted vitality from excessive pleasures"),
    ("sun_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["foreign_travel", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.17 v.86a",
     "Sun-Venus conjunction in 12th house: artistic career flourishes in "
     "foreign lands, success abroad in entertainment or hospitality"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_venus", "conjunction_condition", "venus_combust", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "combust"],
     "Ch.17 v.87",
     "Venus combust by Sun (within 10 degrees): major relationship and marriage "
     "difficulties, diminished capacity for love and aesthetic appreciation"),
    ("sun_venus", "conjunction_condition", "venus_combust_severe", {},
     "unfavorable", "strong",
     ["marriage", "physical_health"],
     ["sun", "venus", "conjunction", "saravali", "combust", "severe"],
     "Ch.17 v.88",
     "Venus severely combust (within 4 degrees): serious marital dysfunction, "
     "reproductive health issues, inability to sustain partnerships"),
    ("sun_venus", "conjunction_condition", "in_taurus_venus_own", {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.17 v.89",
     "Sun-Venus conjunction in Taurus (Venus's own sign): artistic eminence "
     "despite combustion, material prosperity through creative talent"),
    ("sun_venus", "conjunction_condition", "in_libra_venus_own", {},
     "favorable", "moderate",
     ["marriage", "fame_reputation"],
     ["sun", "venus", "conjunction", "saravali", "own_sign", "libra"],
     "Ch.17 v.90",
     "Sun-Venus conjunction in Libra (Venus's own sign, Sun debilitated): "
     "artistic brilliance despite weakened ego, beauty overcomes authority"),
    ("sun_venus", "conjunction_condition", "in_leo_sun_own", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.17 v.91",
     "Sun-Venus conjunction in Leo (Sun's own sign): ego overshadows aesthetics, "
     "domineering in romantic matters, pride destroys partnerships"),
    ("sun_venus", "conjunction_condition", "exalted_venus_pisces", {},
     "favorable", "strong",
     ["marriage", "spirituality"],
     ["sun", "venus", "conjunction", "saravali", "exaltation", "pisces"],
     "Ch.17 v.92",
     "Sun-Venus conjunction in Pisces (Venus exalted): divine love expressed "
     "through art, spiritual beauty, compassionate and selfless partner"),
    ("sun_venus", "conjunction_condition", "debilitated_venus_virgo", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "debilitation", "virgo"],
     "Ch.17 v.93",
     "Sun-Venus conjunction in Virgo (Venus debilitated): critical and "
     "unromantic, marriage plagued by fault-finding, beauty unappreciated"),
    ("sun_venus", "conjunction_condition", "marriage_timing_delay", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "marriage_timing"],
     "Ch.17 v.94",
     "Sun-Venus conjunction general: marriage timing delayed or disrupted, "
     "quality of marriage heavily affected by combustion degree"),
    ("sun_venus", "conjunction_condition", "jupiter_aspect_grace", {},
     "favorable", "moderate",
     ["marriage", "spirituality"],
     ["sun", "venus", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.17 v.95",
     "Sun-Venus conjunction aspected by Jupiter: divine grace in relationships, "
     "marriage improved by spiritual values, artistic wisdom"),
    ("sun_venus", "conjunction_condition", "saturn_aspect_restriction", {},
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["sun", "venus", "conjunction", "saravali", "saturn_aspect"],
     "Ch.17 v.96",
     "Sun-Venus conjunction aspected by Saturn: severe delays in marriage, "
     "financial hardship affects relationship quality, austere lifestyle"),
    ("sun_venus", "conjunction_condition", "mars_aspect_passion", {},
     "mixed", "strong",
     ["marriage", "character_temperament"],
     ["sun", "venus", "conjunction", "saravali", "mars_aspect"],
     "Ch.17 v.97",
     "Sun-Venus conjunction aspected by Mars: intense passion in relationships, "
     "aggressive romantic pursuit, quarrels with spouse over dominance"),
    ("sun_venus", "conjunction_condition", "kendra_placement", {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["sun", "venus", "conjunction", "saravali", "kendra"],
     "Ch.17 v.98",
     "Sun-Venus conjunction in any kendra (1/4/7/10): angular strength amplifies "
     "both artistic talent and relationship challenges equally"),
    ("sun_venus", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["marriage", "physical_health", "wealth"],
     ["sun", "venus", "conjunction", "saravali", "dusthana"],
     "Ch.17 v.99",
     "Sun-Venus conjunction in any dusthana (6/8/12): worst effects on marriage, "
     "health complications, financial losses through relationships"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun-Saturn Conjunction — Ch.17-18 (SAV217–SAV260)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "strong",
     ["physical_health", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "1st_house"],
     "Ch.17 v.100",
     "Sun-Saturn conjunction in 1st house: lean and sickly body, obstacles "
     "from birth, father-son conflict manifests in self-identity struggles"),
    ("sun_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saturn", "conjunction", "saravali", "1st_house", "delay"],
     "Ch.17 v.101",
     "Sun-Saturn conjunction in 1st house: delayed recognition, authority "
     "comes late in life, early career marked by setbacks and humiliation"),
    ("sun_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "1st_house", "mastery"],
     "Ch.17 v.102",
     "Sun-Saturn conjunction in 1st house: eventual mastery through hardship, "
     "disciplined character forged by adversity, late-blooming success"),
    # House 2
    ("sun_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "2nd_house"],
     "Ch.17 v.103",
     "Sun-Saturn conjunction in 2nd house: harsh speech, financial hardship "
     "in early life, wealth comes slowly through persistent effort"),
    ("sun_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["sun", "saturn", "conjunction", "saravali", "2nd_house", "face"],
     "Ch.17 v.104",
     "Sun-Saturn conjunction in 2nd house: dental problems, facial marks "
     "or scars, eye diseases, family discord over resources"),
    ("sun_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "2nd_house", "savings"],
     "Ch.17 v.104a",
     "Sun-Saturn conjunction in 2nd house: frugal and disciplined with money, "
     "accumulates slowly through persistent savings, austere lifestyle"),
    # House 3
    ("sun_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "3rd_house"],
     "Ch.17 v.105",
     "Sun-Saturn conjunction in 3rd house: courage develops through hardship, "
     "strained relations with siblings, success through persistent effort"),
    ("sun_saturn", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "saturn", "conjunction", "saravali", "3rd_house", "skill"],
     "Ch.17 v.106",
     "Sun-Saturn conjunction in 3rd house: technical or mechanical skills, "
     "excels in craftsmanship, gains through disciplined communication"),
    # House 4
    ("sun_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "property_vehicles"],
     ["sun", "saturn", "conjunction", "saravali", "4th_house"],
     "Ch.17 v.107",
     "Sun-Saturn conjunction in 4th house: devoid of domestic happiness, "
     "loss of ancestral property, troubled relationship with mother"),
    ("sun_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "4th_house", "sorrow"],
     "Ch.17 v.108",
     "Sun-Saturn conjunction in 4th house: deep inner melancholy, heart "
     "disease tendencies, chronic dissatisfaction with life conditions"),
    # House 5
    ("sun_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "strong",
     ["progeny", "intelligence_education"],
     ["sun", "saturn", "conjunction", "saravali", "5th_house"],
     "Ch.18 v.1",
     "Sun-Saturn conjunction in 5th house: delays in progeny, difficult "
     "relationship with children, intelligence suppressed by pessimism"),
    ("sun_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["wealth", "mental_health"],
     ["sun", "saturn", "conjunction", "saravali", "5th_house", "speculation"],
     "Ch.18 v.2",
     "Sun-Saturn conjunction in 5th house: losses through speculation, "
     "poor judgment in investments, creative blockages"),
    ("sun_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["character_temperament", "spirituality"],
     ["sun", "saturn", "conjunction", "saravali", "5th_house", "discipline"],
     "Ch.18 v.2a",
     "Sun-Saturn conjunction in 5th house: disciplined mind develops through "
     "adversity, late intellectual blooming, philosophical maturity"),
    # House 6
    ("sun_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "6th_house"],
     "Ch.18 v.3",
     "Sun-Saturn conjunction in 6th house: eventually conquers enemies through "
     "persistence, success in service but with chronic health issues"),
    ("sun_saturn", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "longevity"],
     ["sun", "saturn", "conjunction", "saravali", "6th_house", "disease"],
     "Ch.18 v.4",
     "Sun-Saturn conjunction in 6th house: chronic bone and joint ailments, "
     "slow-healing diseases, digestive disorders, debts accumulate"),
    # House 7
    ("sun_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "7th_house"],
     "Ch.18 v.5",
     "Sun-Saturn conjunction in 7th house: delayed marriage, older or mature "
     "spouse, partnership marked by duty rather than affection"),
    ("sun_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["sun", "saturn", "conjunction", "saravali", "7th_house", "hardship"],
     "Ch.18 v.6",
     "Sun-Saturn conjunction in 7th house: spouse brings hardship, business "
     "partnerships fraught with obstacles, public disgrace possible"),
    # House 8
    ("sun_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["sun", "saturn", "conjunction", "saravali", "8th_house"],
     "Ch.18 v.7",
     "Sun-Saturn conjunction in 8th house: chronic and debilitating diseases, "
     "reduced longevity, karmic suffering, loss of inheritance"),
    ("sun_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["wealth", "enemies_litigation"],
     ["sun", "saturn", "conjunction", "saravali", "8th_house", "punishment"],
     "Ch.18 v.8",
     "Sun-Saturn conjunction in 8th house: punished by authorities, heavy "
     "fines or imprisonment, financial ruin through sudden reversals"),
    ("sun_saturn", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["sun", "saturn", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.18 v.8a",
     "Sun-Saturn conjunction in 8th house: deep interest in occult sciences "
     "and longevity research, karmic wisdom through near-death experiences"),
    # House 9
    ("sun_saturn", "conjunction_in_house", 9, {},
     "unfavorable", "strong",
     ["spirituality", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "9th_house"],
     "Ch.18 v.9",
     "Sun-Saturn conjunction in 9th house: difficulties with father, "
     "religious doubt, denied blessings of guru and tradition"),
    ("sun_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["career_status", "spirituality"],
     ["sun", "saturn", "conjunction", "saravali", "9th_house", "late_fortune"],
     "Ch.18 v.10",
     "Sun-Saturn conjunction in 9th house: fortune arrives very late in life, "
     "eventual wisdom through suffering, pilgrimage after hardship"),
    # House 10
    ("sun_saturn", "conjunction_in_house", 10, {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "saturn", "conjunction", "saravali", "10th_house"],
     "Ch.18 v.11",
     "Sun-Saturn conjunction in 10th house: career marked by intense struggle "
     "but eventual rise, authority achieved through sustained discipline"),
    ("sun_saturn", "conjunction_in_house", 10, {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "10th_house", "labor"],
     "Ch.18 v.12",
     "Sun-Saturn conjunction in 10th house: success through laborious effort, "
     "may work in mining, oil, iron, or government administration"),
    ("sun_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "saturn", "conjunction", "saravali", "10th_house", "endurance"],
     "Ch.18 v.12a",
     "Sun-Saturn conjunction in 10th house: enduring professional legacy, "
     "builds lasting institutions, respected for perseverance and integrity"),
    # House 11
    ("sun_saturn", "conjunction_in_house", 11, {},
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "11th_house"],
     "Ch.18 v.13",
     "Sun-Saturn conjunction in 11th house: delayed but substantial gains, "
     "income from laborious professions, elder sibling faces hardship"),
    ("sun_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "saturn", "conjunction", "saravali", "11th_house", "perseverance"],
     "Ch.18 v.14",
     "Sun-Saturn conjunction in 11th house: perseverance rewarded with wealth "
     "in later years, respected for endurance and discipline"),
    # House 12
    ("sun_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["wealth", "physical_health"],
     ["sun", "saturn", "conjunction", "saravali", "12th_house"],
     "Ch.18 v.15",
     "Sun-Saturn conjunction in 12th house: heavy expenditure, hospitalization, "
     "exile or separation from homeland, poverty and isolation"),
    ("sun_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["mental_health", "spirituality"],
     ["sun", "saturn", "conjunction", "saravali", "12th_house", "confinement"],
     "Ch.18 v.16",
     "Sun-Saturn conjunction in 12th house: depression and mental anguish, "
     "confinement in institutions, spiritual crisis through suffering"),
    ("sun_saturn", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "12th_house", "renunciation"],
     "Ch.18 v.16a",
     "Sun-Saturn conjunction in 12th house: eventual spiritual renunciation, "
     "service in remote places, karmic debts paid through selfless work"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_saturn", "conjunction_condition", "father_son_conflict_general", {},
     "unfavorable", "strong",
     ["character_temperament", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "father_son_conflict"],
     "Ch.17 v.109",
     "Sun-Saturn conjunction general: inherent father-son conflict, authority "
     "(Sun) vs hardship (Saturn), native struggles with paternal legacy"),
    ("sun_saturn", "conjunction_condition", "karmic_conjunction_general", {},
     "unfavorable", "strong",
     ["career_status", "longevity"],
     ["sun", "saturn", "conjunction", "saravali", "karmic"],
     "Ch.17 v.110",
     "Sun-Saturn conjunction general: intense karmic conjunction bringing "
     "delays, obstacles, and suffering, but eventual mastery through endurance"),
    ("sun_saturn", "conjunction_condition", "saturn_exalted_libra", {},
     "mixed", "strong",
     ["career_status", "wealth"],
     ["sun", "saturn", "conjunction", "saravali", "exaltation", "libra"],
     "Ch.18 v.17",
     "Sun-Saturn conjunction in Libra (Saturn exalted, Sun debilitated): "
     "reversal of fortune — disciplined effort triumphs over weakened ego"),
    ("sun_saturn", "conjunction_condition", "sun_exalted_aries", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "exaltation", "aries"],
     "Ch.18 v.18",
     "Sun-Saturn conjunction in Aries (Sun exalted, Saturn debilitated): "
     "authority despite obstacles, commanding presence overcomes restrictions"),
    ("sun_saturn", "conjunction_condition", "in_capricorn_saturn_own", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["sun", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.18 v.19",
     "Sun-Saturn conjunction in Capricorn (Saturn's own sign): structured "
     "authority, slow but steady rise, discipline rewarded over time"),
    ("sun_saturn", "conjunction_condition", "in_aquarius_saturn_own", {},
     "mixed", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.18 v.20",
     "Sun-Saturn conjunction in Aquarius (Saturn's own sign): unconventional "
     "authority, scientific temperament, serves larger social causes"),
    ("sun_saturn", "conjunction_condition", "in_leo_sun_own", {},
     "unfavorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.18 v.21",
     "Sun-Saturn conjunction in Leo (Sun's own sign): ego battles with "
     "restriction, authority undermined by chronic self-doubt"),
    ("sun_saturn", "conjunction_condition", "jupiter_aspect_karmic_relief", {},
     "favorable", "moderate",
     ["spirituality", "career_status"],
     ["sun", "saturn", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.18 v.22",
     "Sun-Saturn conjunction aspected by Jupiter: karmic relief, suffering "
     "transformed into wisdom, divine grace mitigates hardship"),
    ("sun_saturn", "conjunction_condition", "mars_aspect_intensified", {},
     "unfavorable", "strong",
     ["physical_health", "enemies_litigation"],
     ["sun", "saturn", "conjunction", "saravali", "mars_aspect"],
     "Ch.18 v.23",
     "Sun-Saturn conjunction aspected by Mars: intensified struggle, triple "
     "malefic influence causes accidents, surgeries, legal battles"),
    ("sun_saturn", "conjunction_condition", "moon_aspect_emotional_burden", {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "moon_aspect"],
     "Ch.18 v.24",
     "Sun-Saturn conjunction aspected by Moon: emotional burden of karmic "
     "suffering, depression, strained maternal relationship"),
    ("sun_saturn", "conjunction_condition", "kendra_placement", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["sun", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.18 v.25",
     "Sun-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies both delays and eventual achievements significantly"),
    ("sun_saturn", "conjunction_condition", "trikona_placement", {},
     "mixed", "moderate",
     ["career_status", "spirituality"],
     ["sun", "saturn", "conjunction", "saravali", "trikona"],
     "Ch.18 v.26",
     "Sun-Saturn conjunction in any trikona (1/5/9): dharmic karmic lesson, "
     "suffering leads to spiritual growth and eventual fortune"),
    ("sun_saturn", "conjunction_condition", "dusthana_severe", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "wealth"],
     ["sun", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.18 v.27",
     "Sun-Saturn conjunction in any dusthana (6/8/12): worst karmic effects "
     "manifest — chronic disease, poverty, confinement, shortened life"),
    ("sun_saturn", "conjunction_condition", "upachaya_growth", {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["sun", "saturn", "conjunction", "saravali", "upachaya"],
     "Ch.18 v.28",
     "Sun-Saturn conjunction in upachaya houses (3/6/10/11): malefic energy "
     "channeled constructively with age, competitive success after delays"),
]


# ── Builder ──────────────────────────────────────────────────────────────────

def _make_conjunction_rules(
    pair_label: str,
    planets: list[str],
    data: list,
    start_num: int,
    chapter: str,
) -> list[RuleRecord]:
    """Build RuleRecord objects for a conjunction pair."""
    rules: list[RuleRecord] = []
    num = start_num
    for entry in data:
        (planet_pair, ptype, house_or_label, _conditions,
         odir, oint, odoms, extra_tags, vref, desc) = entry

        rid = f"SAV{num:03d}"

        if ptype == "conjunction_in_house":
            primary = {
                "planet": planet_pair,
                "placement_type": "conjunction_in_house",
                "placement_value": [house_or_label],
                "planets": list(planets),
            }
            timing = "dasha_dependent"
        else:
            primary = {
                "planet": planet_pair,
                "placement_type": "conjunction_condition",
                "yoga_label": house_or_label,
                "planets": list(planets),
            }
            # Character/personality rules are unspecified; conditional ones dasha-dependent
            if any(d in odoms for d in ("character_temperament", "physical_appearance")):
                timing = "unspecified"
            else:
                timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "conjunction", pair_label] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter=chapter,
            school="parashari",
            category="conjunction_predictions",
            description=f"[Saravali — {pair_label}] {desc}",
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
            phase="1B_compound",
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
    sun_jupiter = _make_conjunction_rules(
        "sun_jupiter", ["sun", "jupiter"], _SUN_JUPITER_DATA, 131, "Ch.16-17",
    )
    sun_venus = _make_conjunction_rules(
        "sun_venus", ["sun", "venus"], _SUN_VENUS_DATA, 174, "Ch.17",
    )
    sun_saturn = _make_conjunction_rules(
        "sun_saturn", ["sun", "saturn"], _SUN_SATURN_DATA, 217, "Ch.17-18",
    )
    return sun_jupiter + sun_venus + sun_saturn


SARAVALI_CONJUNCTIONS_2_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_2_REGISTRY.add(_rule)
