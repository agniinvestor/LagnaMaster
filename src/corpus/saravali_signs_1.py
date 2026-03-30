"""src/corpus/saravali_signs_1.py — S281: Saravali Sun in 12 Signs (Ch.25).

SAV1041–SAV1170 (130 rules).
Phase: 1B_matrix | Source: Saravali | School: parashari

Sun through the twelve signs from Saravali Chapter 25:
  Sun in Aries      — SAV1041–SAV1051 (11 rules)
  Sun in Taurus     — SAV1052–SAV1062 (11 rules)
  Sun in Gemini     — SAV1063–SAV1073 (11 rules)
  Sun in Cancer     — SAV1074–SAV1084 (11 rules)
  Sun in Leo        — SAV1085–SAV1095 (11 rules)
  Sun in Virgo      — SAV1096–SAV1106 (11 rules)
  Sun in Libra      — SAV1107–SAV1117 (11 rules)
  Sun in Scorpio    — SAV1118–SAV1127 (10 rules)
  Sun in Sagittarius— SAV1128–SAV1137 (10 rules)
  Sun in Capricorn  — SAV1138–SAV1147 (10 rules)
  Sun in Aquarius   — SAV1148–SAV1157 (10 rules)
  Sun in Pisces     — SAV1158–SAV1167 (10 rules)
  General Sun-in-sign conditions — SAV1168–SAV1170 (3 rules)

Saravali (by Kalyana Varma, ~800 CE) gives detailed results for the Sun
placed in each of the twelve signs, covering appearance, temperament,
career, wealth, health, relationships, and dignity-modified conditions.

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Aries — Ch.25 (SAV1041–SAV1051)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_ARIES_DATA = [
    # Base rules
    ("sun", "sign_placement", "aries", {},
     "favorable", "strong",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "aries", "exalted"],
     "Ch.25 v.1",
     "Sun in Aries: strong and well-built body, prominent forehead, "
     "commanding presence, natural authority over others"),
    ("sun", "sign_placement", "aries", {},
     "favorable", "strong",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "aries", "valour"],
     "Ch.25 v.2",
     "Sun in Aries: courageous and adventurous spirit, loves travel and "
     "exploration, fearless in undertaking difficult tasks"),
    ("sun", "sign_placement", "aries", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "aries", "authority"],
     "Ch.25 v.3",
     "Sun in Aries: attains positions of leadership and command, respected "
     "by government and superiors, gains through authority"),
    ("sun", "sign_placement", "aries", {},
     "favorable", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "aries", "wealth"],
     "Ch.25 v.4",
     "Sun in Aries: earns wealth through own enterprise and initiative, "
     "financially self-reliant, generous in spending"),
    ("sun", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "aries", "health"],
     "Ch.25 v.5",
     "Sun in Aries: prone to fevers, headaches, and bilious complaints, "
     "strong constitution but overheats easily"),
    ("sun", "sign_placement", "aries", {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "aries", "fame"],
     "Ch.25 v.6",
     "Sun in Aries: renowned for deeds of valor, famous in own circle, "
     "proud and dignified bearing attracts respect"),
    ("sun", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "saravali", "sign_placement", "aries", "relationships"],
     "Ch.25 v.7",
     "Sun in Aries: dominating in relationships, expects obedience from "
     "partner, passionate but impatient in love matters"),
    ("sun", "sign_placement", "aries", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["sun", "saravali", "sign_placement", "aries", "intelligence"],
     "Ch.25 v.8",
     "Sun in Aries: sharp intellect with quick decision-making ability, "
     "inclined to martial arts, sports, or engineering"),
    # Conditional / dignity-modified rules
    ("sun", "sign_condition", "aries_exalted_full", {},
     "favorable", "strong",
     ["fame_reputation", "career_status"],
     ["sun", "saravali", "sign_placement", "aries", "exalted", "dignity"],
     "Ch.25 v.9",
     "Sun exalted in Aries: attains royal status or equivalent high position, "
     "commands vast resources, celebrated and honored widely"),
    ("sun", "sign_condition", "aries_navamsa_strong", {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["sun", "saravali", "sign_placement", "aries", "navamsa", "strong"],
     "Ch.25 v.10",
     "Sun in Aries with strong navamsa placement: wealth from government "
     "or authority figures, lasting reputation, rise to eminence"),
    ("sun", "sign_condition", "aries_aspected_malefic", {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["sun", "saravali", "sign_placement", "aries", "malefic", "aspect"],
     "Ch.25 v.11",
     "Sun in Aries aspected by malefics: valor turns to aggression, "
     "injuries from weapons or fire, quarrels with authorities"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Taurus — Ch.25 (SAV1052–SAV1062)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_TAURUS_DATA = [
    ("sun", "sign_placement", "taurus", {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "taurus", "appearance"],
     "Ch.25 v.12",
     "Sun in Taurus: broad-chested and stout body, attractive face, "
     "slow and deliberate gait, prefers comfort and stability"),
    ("sun", "sign_placement", "taurus", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "taurus", "patience"],
     "Ch.25 v.13",
     "Sun in Taurus: patient and enduring temperament but stubborn when "
     "opposed, attached to material pleasures and luxuries"),
    ("sun", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "taurus", "career"],
     "Ch.25 v.14",
     "Sun in Taurus: earns through agriculture, cattle, textiles, or "
     "luxury goods, success in occupations related to Venus-ruled domains"),
    ("sun", "sign_placement", "taurus", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "taurus", "wealth"],
     "Ch.25 v.15",
     "Sun in Taurus: accumulates wealth gradually through persistent effort, "
     "but expenses on comforts reduce savings"),
    ("sun", "sign_placement", "taurus", {},
     "unfavorable", "weak",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "taurus", "health"],
     "Ch.25 v.16",
     "Sun in Taurus: susceptible to throat ailments, eye troubles, and "
     "diseases of the face, needs moderation in diet"),
    ("sun", "sign_placement", "taurus", {},
     "mixed", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "taurus", "marriage"],
     "Ch.25 v.17",
     "Sun in Taurus: fond of women and sensual pleasures, may have "
     "multiple romantic interests, spouse is attractive but willful"),
    ("sun", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "saravali", "sign_placement", "taurus", "music"],
     "Ch.25 v.18",
     "Sun in Taurus: love for music, singing, and fine arts, possesses "
     "artistic sensibility and appreciation for beauty"),
    ("sun", "sign_placement", "taurus", {},
     "unfavorable", "weak",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "taurus", "reputation"],
     "Ch.25 v.19",
     "Sun in Taurus: tends to be overshadowed by others, lacks the fire "
     "to assert authority, fame comes late if at all"),
    # Conditional
    ("sun", "sign_condition", "taurus_venus_strong", {},
     "favorable", "moderate",
     ["wealth", "marriage"],
     ["sun", "saravali", "sign_placement", "taurus", "venus", "strong"],
     "Ch.25 v.20",
     "Sun in Taurus with strong Venus: enhanced material prosperity, "
     "happy marriage, gains from artistic or creative pursuits"),
    ("sun", "sign_condition", "taurus_enemy_sign", {},
     "unfavorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "taurus", "enemy_sign"],
     "Ch.25 v.21",
     "Sun in Taurus (enemy sign): diminished authority, struggles for "
     "recognition, subordinate position despite talent"),
    ("sun", "sign_condition", "taurus_aspected_benefic", {},
     "favorable", "moderate",
     ["character_temperament", "wealth"],
     ["sun", "saravali", "sign_placement", "taurus", "benefic", "aspect"],
     "Ch.25 v.22",
     "Sun in Taurus aspected by benefics: artistic talents bring recognition, "
     "good character, charitable disposition, financial stability"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Gemini — Ch.25 (SAV1063–SAV1073)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_GEMINI_DATA = [
    ("sun", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "gemini", "appearance"],
     "Ch.25 v.23",
     "Sun in Gemini: well-proportioned body with pleasant features, "
     "quick movements, expressive eyes, youthful appearance"),
    ("sun", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["sun", "saravali", "sign_placement", "gemini", "intellect"],
     "Ch.25 v.24",
     "Sun in Gemini: highly intelligent with aptitude for multiple subjects, "
     "skilled in sciences, astrology, and mathematics"),
    ("sun", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "gemini", "career"],
     "Ch.25 v.25",
     "Sun in Gemini: success in communication-based professions, writing, "
     "teaching, translation, or diplomatic service"),
    ("sun", "sign_placement", "gemini", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "gemini", "wealth"],
     "Ch.25 v.26",
     "Sun in Gemini: wealth comes through intellectual work and trade, "
     "but spending on education and travel reduces accumulation"),
    ("sun", "sign_placement", "gemini", {},
     "mixed", "weak",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "gemini", "health"],
     "Ch.25 v.27",
     "Sun in Gemini: nervous disorders and respiratory complaints, arms "
     "and shoulders vulnerable, mental overwork causes fatigue"),
    ("sun", "sign_placement", "gemini", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "gemini", "dual_nature"],
     "Ch.25 v.28",
     "Sun in Gemini: dual nature with changing interests, versatile but "
     "sometimes lacks persistence, fond of variety and novelty"),
    ("sun", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "gemini", "fame"],
     "Ch.25 v.29",
     "Sun in Gemini: gains fame through oratory, literary works, or "
     "scholarly achievements, known among learned circles"),
    ("sun", "sign_placement", "gemini", {},
     "mixed", "weak",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "gemini", "relationships"],
     "Ch.25 v.30",
     "Sun in Gemini: intellectual compatibility needed in marriage, "
     "may have more than one significant relationship"),
    # Conditional
    ("sun", "sign_condition", "gemini_mercury_conjunct", {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "gemini", "mercury", "conjunct"],
     "Ch.25 v.31",
     "Sun in Gemini with Mercury: Budhaditya yoga in own sign, exceptional "
     "intellect, fame through scholarship or advisory role"),
    ("sun", "sign_condition", "gemini_friend_sign", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "saravali", "sign_placement", "gemini", "friend_sign"],
     "Ch.25 v.32",
     "Sun in Gemini (friend sign): comfortable expression of authority "
     "through knowledge, gains through communication and counsel"),
    ("sun", "sign_condition", "gemini_malefic_aspect", {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["sun", "saravali", "sign_placement", "gemini", "malefic", "aspect"],
     "Ch.25 v.33",
     "Sun in Gemini aspected by malefics: cunning and deceptive speech, "
     "uses intellect for fraud, nervous breakdowns under pressure"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Cancer — Ch.25 (SAV1074–SAV1084)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_CANCER_DATA = [
    ("sun", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "cancer", "appearance"],
     "Ch.25 v.34",
     "Sun in Cancer: round face with soft features, medium stature, "
     "emotional temperament, attachment to home and mother"),
    ("sun", "sign_placement", "cancer", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "cancer", "moody"],
     "Ch.25 v.35",
     "Sun in Cancer: fluctuating moods, easily hurt by criticism, "
     "tends to brood over setbacks, overly sensitive nature"),
    ("sun", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "cancer", "career"],
     "Ch.25 v.36",
     "Sun in Cancer: success in occupations related to water, liquids, "
     "dairy, or public-facing roles, service to women or masses"),
    ("sun", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "cancer", "wealth"],
     "Ch.25 v.37",
     "Sun in Cancer: income fluctuates like tides, earns through public "
     "or domestic affairs, wealth from maternal side possible"),
    ("sun", "sign_placement", "cancer", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "cancer", "health"],
     "Ch.25 v.38",
     "Sun in Cancer: digestive troubles, chest complaints, water-related "
     "diseases, tendency toward obesity and lethargy"),
    ("sun", "sign_placement", "cancer", {},
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["sun", "saravali", "sign_placement", "cancer", "devotion"],
     "Ch.25 v.39",
     "Sun in Cancer: devoted to mother and family traditions, inclined "
     "toward religious observances, charitable and compassionate"),
    ("sun", "sign_placement", "cancer", {},
     "unfavorable", "moderate",
     ["fame_reputation", "career_status"],
     ["sun", "saravali", "sign_placement", "cancer", "authority"],
     "Ch.25 v.40",
     "Sun in Cancer: lacks assertive authority, subordinate to others' "
     "wishes, difficulty in gaining independent recognition"),
    ("sun", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "cancer", "relationships"],
     "Ch.25 v.41",
     "Sun in Cancer: deeply attached to spouse but possessive, domestic "
     "life is central concern, emotional dependency in partnerships"),
    # Conditional
    ("sun", "sign_condition", "cancer_moon_strong", {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "cancer", "moon", "strong"],
     "Ch.25 v.42",
     "Sun in Cancer with strong Moon: gains through public service or "
     "government favor, emotional intelligence brings success"),
    ("sun", "sign_condition", "cancer_waxing_moon", {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "saravali", "sign_placement", "cancer", "waxing", "moon"],
     "Ch.25 v.43",
     "Sun in Cancer with waxing Moon as dispositor: enhanced confidence, "
     "leadership in nurturing professions, popularity with masses"),
    ("sun", "sign_condition", "cancer_malefic_conjunction", {},
     "unfavorable", "moderate",
     ["mental_health", "physical_health"],
     ["sun", "saravali", "sign_placement", "cancer", "malefic", "conjunction"],
     "Ch.25 v.44",
     "Sun in Cancer conjunct malefics: severe emotional disturbances, "
     "chest and stomach ailments, troubled relationship with mother"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Leo — Ch.25 (SAV1085–SAV1095)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_LEO_DATA = [
    ("sun", "sign_placement", "leo", {},
     "favorable", "strong",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "leo", "appearance"],
     "Ch.25 v.45",
     "Sun in Leo: large and imposing body, broad chest, lion-like gait, "
     "majestic appearance, strong bones and constitution"),
    ("sun", "sign_placement", "leo", {},
     "favorable", "strong",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "leo", "leadership"],
     "Ch.25 v.46",
     "Sun in Leo: natural leader with royal bearing, dignified and proud, "
     "commands respect effortlessly, dislikes subordination"),
    ("sun", "sign_placement", "leo", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "leo", "career"],
     "Ch.25 v.47",
     "Sun in Leo: success in government, administration, or positions of "
     "authority, gains patronage of powerful persons, rises to eminence"),
    ("sun", "sign_placement", "leo", {},
     "favorable", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "leo", "wealth"],
     "Ch.25 v.48",
     "Sun in Leo: earns wealth through authority and leadership roles, "
     "generous spending on display and status, royal lifestyle"),
    ("sun", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "leo", "health"],
     "Ch.25 v.49",
     "Sun in Leo: strong vitality but prone to heart-related ailments, "
     "back pain, and fevers from overexertion"),
    ("sun", "sign_placement", "leo", {},
     "favorable", "strong",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "leo", "fame"],
     "Ch.25 v.50",
     "Sun in Leo: widespread fame and recognition, honored by state and "
     "society, name endures beyond own lifetime"),
    ("sun", "sign_placement", "leo", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "saravali", "sign_placement", "leo", "relationships"],
     "Ch.25 v.51",
     "Sun in Leo: domineering in marriage, few children, spouse must be "
     "submissive for harmony, anger flares easily in domestic life"),
    ("sun", "sign_placement", "leo", {},
     "favorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "saravali", "sign_placement", "leo", "enemies"],
     "Ch.25 v.52",
     "Sun in Leo: fierce toward enemies, annihilates opposition, "
     "shows no mercy in combat or competition, loves hunting"),
    # Conditional
    ("sun", "sign_condition", "leo_own_sign", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "leo", "own_sign", "dignity"],
     "Ch.25 v.53",
     "Sun in Leo (own sign): full expression of solar power, kingship or "
     "equivalent authority, lasting legacy and dynastic pride"),
    ("sun", "sign_condition", "leo_jupiter_aspect", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "leo", "jupiter", "aspect"],
     "Ch.25 v.54",
     "Sun in Leo aspected by Jupiter: righteous ruler, dharmic authority, "
     "fame through noble deeds, spiritual leadership"),
    ("sun", "sign_condition", "leo_saturn_aspect", {},
     "unfavorable", "moderate",
     ["career_status", "enemies_litigation"],
     ["sun", "saravali", "sign_placement", "leo", "saturn", "aspect"],
     "Ch.25 v.55",
     "Sun in Leo aspected by Saturn: obstacles to authority, delayed rise, "
     "conflicts with subordinates and labor, chronic health issues"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Virgo — Ch.25 (SAV1096–SAV1106)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_VIRGO_DATA = [
    ("sun", "sign_placement", "virgo", {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "virgo", "appearance"],
     "Ch.25 v.56",
     "Sun in Virgo: slim and well-formed body, feminine features, "
     "soft-spoken manner, meticulous in personal presentation"),
    ("sun", "sign_placement", "virgo", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["sun", "saravali", "sign_placement", "virgo", "intellect"],
     "Ch.25 v.57",
     "Sun in Virgo: sharp analytical mind, skilled in writing and "
     "record-keeping, proficient in languages and literature"),
    ("sun", "sign_placement", "virgo", {},
     "favorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "virgo", "career"],
     "Ch.25 v.58",
     "Sun in Virgo: excels in clerical, administrative, or service "
     "professions, success through detailed and methodical work"),
    ("sun", "sign_placement", "virgo", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "virgo", "wealth"],
     "Ch.25 v.59",
     "Sun in Virgo: earns through service or skilled labor rather than "
     "independent enterprise, moderate but steady income"),
    ("sun", "sign_placement", "virgo", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "virgo", "health"],
     "Ch.25 v.60",
     "Sun in Virgo: prone to intestinal disorders, skin diseases, and "
     "nervous complaints, weak digestive fire"),
    ("sun", "sign_placement", "virgo", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "virgo", "modesty"],
     "Ch.25 v.61",
     "Sun in Virgo: modest and unassuming disposition, critical of self "
     "and others, perfectionist tendencies create anxiety"),
    ("sun", "sign_placement", "virgo", {},
     "mixed", "weak",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "virgo", "reputation"],
     "Ch.25 v.62",
     "Sun in Virgo: known for precision and reliability rather than "
     "charisma, gains respect through competence not authority"),
    ("sun", "sign_placement", "virgo", {},
     "mixed", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "virgo", "relationships"],
     "Ch.25 v.63",
     "Sun in Virgo: critical of spouse, expects perfection in partner, "
     "late marriage possible, compatibility requires intellectual match"),
    # Conditional
    ("sun", "sign_condition", "virgo_mercury_strong", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["sun", "saravali", "sign_placement", "virgo", "mercury", "strong"],
     "Ch.25 v.64",
     "Sun in Virgo with strong Mercury: outstanding analytical abilities, "
     "success in medicine, accounting, or scientific research"),
    ("sun", "sign_condition", "virgo_friend_sign", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "saravali", "sign_placement", "virgo", "friend_sign"],
     "Ch.25 v.65",
     "Sun in Virgo (friend sign): comfortable in service roles, gains "
     "trust of superiors, steady professional advancement"),
    ("sun", "sign_condition", "virgo_kendra_placement", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "virgo", "kendra"],
     "Ch.25 v.66",
     "Sun in Virgo in a kendra: analytical abilities applied to leadership, "
     "recognition for administrative excellence, government service"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Libra — Ch.25 (SAV1107–SAV1117)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_LIBRA_DATA = [
    ("sun", "sign_placement", "libra", {},
     "unfavorable", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "libra", "appearance"],
     "Ch.25 v.67",
     "Sun in Libra: lean and tall body, prominent nose, tendency toward "
     "indecisiveness, seeks approval from others constantly"),
    ("sun", "sign_placement", "libra", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "libra", "weakness"],
     "Ch.25 v.68",
     "Sun in Libra: lacks self-confidence and assertiveness, easily "
     "influenced by others, vacillates in decision-making"),
    ("sun", "sign_placement", "libra", {},
     "unfavorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "libra", "career"],
     "Ch.25 v.69",
     "Sun in Libra: struggles in leadership roles, better suited for "
     "partnerships and collaborative work, trade and commerce"),
    ("sun", "sign_placement", "libra", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "libra", "wealth"],
     "Ch.25 v.70",
     "Sun in Libra: wealth through trade, partnerships, or foreign "
     "connections, but losses through trusting wrong people"),
    ("sun", "sign_placement", "libra", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "libra", "health"],
     "Ch.25 v.71",
     "Sun in Libra: kidney and lower back ailments, headaches, prone to "
     "debility from overindulgence in sensual pleasures"),
    ("sun", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "libra", "marriage"],
     "Ch.25 v.72",
     "Sun in Libra: gives importance to marriage and partnerships, "
     "attractive to opposite sex, seeks harmony in relationships"),
    ("sun", "sign_placement", "libra", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "libra", "reputation"],
     "Ch.25 v.73",
     "Sun in Libra: known for diplomacy and fairness, earns respect "
     "through mediation, but authority is frequently questioned"),
    ("sun", "sign_placement", "libra", {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "saravali", "sign_placement", "libra", "conflict"],
     "Ch.25 v.74",
     "Sun in Libra: prone to humiliation in disputes, defeated by "
     "enemies due to lack of combative spirit, fears confrontation"),
    # Conditional
    ("sun", "sign_condition", "libra_debilitated_full", {},
     "unfavorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "libra", "debilitated", "dignity"],
     "Ch.25 v.75",
     "Sun debilitated in Libra: severe loss of status, humiliation from "
     "authority figures, lack of recognition despite effort"),
    ("sun", "sign_condition", "libra_neecha_bhanga", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "libra", "neecha_bhanga"],
     "Ch.25 v.76",
     "Sun in Libra with neecha-bhanga: cancellation of debility, rises "
     "after initial struggles, success through partnerships"),
    ("sun", "sign_condition", "libra_venus_strong", {},
     "mixed", "moderate",
     ["wealth", "marriage"],
     ["sun", "saravali", "sign_placement", "libra", "venus", "strong"],
     "Ch.25 v.77",
     "Sun in Libra with strong Venus: diplomatic success, gains through "
     "spouse or business partner, artistic or luxurious profession"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Scorpio — Ch.25 (SAV1118–SAV1127)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_SCORPIO_DATA = [
    ("sun", "sign_placement", "scorpio", {},
     "mixed", "strong",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "scorpio", "appearance"],
     "Ch.25 v.78",
     "Sun in Scorpio: sturdy and muscular body, penetrating gaze, "
     "secretive disposition, intense and magnetic personality"),
    ("sun", "sign_placement", "scorpio", {},
     "mixed", "strong",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "scorpio", "intensity"],
     "Ch.25 v.79",
     "Sun in Scorpio: intensely passionate and determined, never forgets "
     "insults, vengeful when wronged, fiercely loyal to allies"),
    ("sun", "sign_placement", "scorpio", {},
     "favorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "scorpio", "career"],
     "Ch.25 v.80",
     "Sun in Scorpio: success in medicine, surgery, research, or "
     "investigation, gains through handling others' resources"),
    ("sun", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "scorpio", "wealth"],
     "Ch.25 v.81",
     "Sun in Scorpio: sudden gains and losses, wealth through inheritance "
     "or joint assets, insurance and hidden resources"),
    ("sun", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "scorpio", "health"],
     "Ch.25 v.82",
     "Sun in Scorpio: susceptible to genital disorders, piles, fistula, "
     "and poisoning, injuries from insects or reptiles"),
    ("sun", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "saravali", "sign_placement", "scorpio", "relationships"],
     "Ch.25 v.83",
     "Sun in Scorpio: possessive and jealous in relationships, suspicious "
     "of spouse, marriage marked by power struggles"),
    ("sun", "sign_placement", "scorpio", {},
     "favorable", "moderate",
     ["enemies_litigation", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "scorpio", "enemies"],
     "Ch.25 v.84",
     "Sun in Scorpio: formidable enemy, destroys opponents through "
     "strategy and persistence, feared in competitive arenas"),
    ("sun", "sign_placement", "scorpio", {},
     "favorable", "moderate",
     ["spirituality", "intelligence_education"],
     ["sun", "saravali", "sign_placement", "scorpio", "occult"],
     "Ch.25 v.85",
     "Sun in Scorpio: drawn to occult sciences, tantric practices, and "
     "hidden knowledge, penetrating insight into mysteries"),
    # Conditional
    ("sun", "sign_condition", "scorpio_mars_strong", {},
     "favorable", "strong",
     ["career_status", "enemies_litigation"],
     ["sun", "saravali", "sign_placement", "scorpio", "mars", "strong"],
     "Ch.25 v.86",
     "Sun in Scorpio with strong Mars: exceptional courage and command, "
     "military or surgical distinction, overcomes all adversaries"),
    ("sun", "sign_condition", "scorpio_malefic_heavy", {},
     "unfavorable", "strong",
     ["physical_health", "longevity"],
     ["sun", "saravali", "sign_placement", "scorpio", "malefic", "heavy"],
     "Ch.25 v.87",
     "Sun in Scorpio heavily afflicted by malefics: danger from poison, "
     "weapons, or hidden enemies, chronic genital ailments"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Sagittarius — Ch.25 (SAV1128–SAV1137)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_SAGITTARIUS_DATA = [
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "sagittarius", "appearance"],
     "Ch.25 v.88",
     "Sun in Sagittarius: tall and well-built body, long face, broad "
     "forehead, dignified carriage, commanding voice"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "strong",
     ["character_temperament", "spirituality"],
     ["sun", "saravali", "sign_placement", "sagittarius", "dharma"],
     "Ch.25 v.89",
     "Sun in Sagittarius: righteous and dharmic nature, devoted to "
     "traditional values, respected for moral integrity"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "sagittarius", "career"],
     "Ch.25 v.90",
     "Sun in Sagittarius: success in law, education, religion, or "
     "philosophy, honored by learned assemblies and institutions"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "sagittarius", "wealth"],
     "Ch.25 v.91",
     "Sun in Sagittarius: wealth through honorable pursuits, patronage "
     "from rulers and institutions, generous and charitable nature"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "weak",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "sagittarius", "health"],
     "Ch.25 v.92",
     "Sun in Sagittarius: generally good health, prone to hip and thigh "
     "ailments, liver complaints from rich diet"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "sagittarius", "fame"],
     "Ch.25 v.93",
     "Sun in Sagittarius: renowned for wisdom and learning, sought for "
     "counsel, fame in religious or academic circles"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "sagittarius", "relationships"],
     "Ch.25 v.94",
     "Sun in Sagittarius: principled in relationships, spouse shares "
     "values and faith, happy domestic life with mutual respect"),
    ("sun", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["sun", "saravali", "sign_placement", "sagittarius", "education"],
     "Ch.25 v.95",
     "Sun in Sagittarius: learned in scriptures and sacred texts, skilled "
     "in teaching and preaching, inclined to higher studies"),
    # Conditional
    ("sun", "sign_condition", "sagittarius_jupiter_strong", {},
     "favorable", "strong",
     ["fame_reputation", "spirituality"],
     ["sun", "saravali", "sign_placement", "sagittarius", "jupiter", "strong"],
     "Ch.25 v.96",
     "Sun in Sagittarius with strong Jupiter: guru-like status, honored "
     "as a spiritual or moral authority, widespread fame"),
    ("sun", "sign_condition", "sagittarius_friend_sign", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "saravali", "sign_placement", "sagittarius", "friend_sign"],
     "Ch.25 v.97",
     "Sun in Sagittarius (friend sign): easy rise through merit, gains "
     "support of teachers and patrons, prosperous career in education"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Capricorn — Ch.25 (SAV1138–SAV1147)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_CAPRICORN_DATA = [
    ("sun", "sign_placement", "capricorn", {},
     "unfavorable", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "capricorn", "appearance"],
     "Ch.25 v.98",
     "Sun in Capricorn: thin and bony body, dry complexion, aged look "
     "even in youth, serious and melancholy disposition"),
    ("sun", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "capricorn", "ambition"],
     "Ch.25 v.99",
     "Sun in Capricorn: highly ambitious but cold and calculating, "
     "disciplined and persistent, sacrifices pleasure for achievement"),
    ("sun", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "capricorn", "career"],
     "Ch.25 v.100",
     "Sun in Capricorn: slow but steady rise in career, success through "
     "perseverance and hardship, serves stern masters"),
    ("sun", "sign_placement", "capricorn", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "capricorn", "wealth"],
     "Ch.25 v.101",
     "Sun in Capricorn: earns through hard labor, miserly tendencies, "
     "wealth comes late in life after prolonged struggle"),
    ("sun", "sign_placement", "capricorn", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "capricorn", "health"],
     "Ch.25 v.102",
     "Sun in Capricorn: rheumatic complaints, joint pains, skin diseases, "
     "wind-related disorders, weak constitution in childhood"),
    ("sun", "sign_placement", "capricorn", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "saravali", "sign_placement", "capricorn", "relationships"],
     "Ch.25 v.103",
     "Sun in Capricorn: difficulty in emotional expression, cold in "
     "relationships, spouse may be older or austere"),
    ("sun", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "capricorn", "reputation"],
     "Ch.25 v.104",
     "Sun in Capricorn: respected for discipline and reliability, earns "
     "grudging respect rather than affection, stern authority"),
    ("sun", "sign_placement", "capricorn", {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "saravali", "sign_placement", "capricorn", "selfish"],
     "Ch.25 v.105",
     "Sun in Capricorn: selfish and ungrateful nature, uses others for "
     "personal advancement, treacherous to benefactors"),
    # Conditional
    ("sun", "sign_condition", "capricorn_saturn_strong", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["sun", "saravali", "sign_placement", "capricorn", "saturn", "strong"],
     "Ch.25 v.106",
     "Sun in Capricorn with strong Saturn: disciplined rise to authority, "
     "gains through mining, construction, or government service"),
    ("sun", "sign_condition", "capricorn_enemy_sign", {},
     "unfavorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "capricorn", "enemy_sign"],
     "Ch.25 v.107",
     "Sun in Capricorn (enemy sign): authority undermined, obstacles from "
     "subordinates and labor, delayed recognition and rewards"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Aquarius — Ch.25 (SAV1148–SAV1157)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_AQUARIUS_DATA = [
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "aquarius", "appearance"],
     "Ch.25 v.108",
     "Sun in Aquarius: tall and lean body, rough or dry complexion, "
     "unconventional appearance, eccentric mannerisms"),
    ("sun", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["sun", "saravali", "sign_placement", "aquarius", "eccentric"],
     "Ch.25 v.109",
     "Sun in Aquarius: independent and unconventional thinker, resists "
     "authority, drawn to reform and humanitarian causes"),
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "aquarius", "career"],
     "Ch.25 v.110",
     "Sun in Aquarius: struggles with conventional employment, prefers "
     "unusual professions, income from technology or social work"),
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "aquarius", "wealth"],
     "Ch.25 v.111",
     "Sun in Aquarius: irregular income, earns through unconventional "
     "means, generous to friends but poor at saving"),
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "aquarius", "health"],
     "Ch.25 v.112",
     "Sun in Aquarius: heart and circulatory problems, calf and ankle "
     "ailments, nervous debility from mental overwork"),
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["fame_reputation"],
     ["sun", "saravali", "sign_placement", "aquarius", "reputation"],
     "Ch.25 v.113",
     "Sun in Aquarius: misunderstood by society, fame among niche groups "
     "only, lacks mainstream recognition despite ability"),
    ("sun", "sign_placement", "aquarius", {},
     "unfavorable", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "aquarius", "relationships"],
     "Ch.25 v.114",
     "Sun in Aquarius: detached in relationships, values friendship over "
     "romance, unconventional approach to marriage"),
    ("sun", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "saravali", "sign_placement", "aquarius", "innovation"],
     "Ch.25 v.115",
     "Sun in Aquarius: innovative and inventive mind, ahead of own time, "
     "intellectual interests in science and technology"),
    # Conditional
    ("sun", "sign_condition", "aquarius_saturn_strong", {},
     "mixed", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "aquarius", "saturn", "strong"],
     "Ch.25 v.116",
     "Sun in Aquarius with strong Saturn: success in large organizations "
     "or social movements, gains through democratic institutions"),
    ("sun", "sign_condition", "aquarius_rahu_conjunction", {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["sun", "saravali", "sign_placement", "aquarius", "rahu", "conjunction"],
     "Ch.25 v.117",
     "Sun in Aquarius with Rahu: extreme rebelliousness, breaks all norms, "
     "mental instability, alienation from family and society"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun in Pisces — Ch.25 (SAV1158–SAV1167)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_PISCES_DATA = [
    ("sun", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["sun", "saravali", "sign_placement", "pisces", "appearance"],
     "Ch.25 v.118",
     "Sun in Pisces: medium-sized body with lustrous eyes, soft and "
     "gentle demeanor, dreamy expression, graceful movements"),
    ("sun", "sign_placement", "pisces", {},
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["sun", "saravali", "sign_placement", "pisces", "compassion"],
     "Ch.25 v.119",
     "Sun in Pisces: compassionate and charitable nature, deeply spiritual, "
     "drawn to selfless service and renunciation"),
    ("sun", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["career_status"],
     ["sun", "saravali", "sign_placement", "pisces", "career"],
     "Ch.25 v.120",
     "Sun in Pisces: success in occupations related to water, shipping, "
     "hospitals, or charitable institutions, service-oriented career"),
    ("sun", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["wealth"],
     ["sun", "saravali", "sign_placement", "pisces", "wealth"],
     "Ch.25 v.121",
     "Sun in Pisces: wealth through overseas connections or foreign trade, "
     "generous disposition reduces personal accumulation"),
    ("sun", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["sun", "saravali", "sign_placement", "pisces", "health"],
     "Ch.25 v.122",
     "Sun in Pisces: foot ailments, lymphatic disorders, tendency toward "
     "substance sensitivity, immune system vulnerabilities"),
    ("sun", "sign_placement", "pisces", {},
     "favorable", "moderate",
     ["fame_reputation", "spirituality"],
     ["sun", "saravali", "sign_placement", "pisces", "fame"],
     "Ch.25 v.123",
     "Sun in Pisces: respected for wisdom and compassion, fame through "
     "spiritual or charitable works, venerated in religious circles"),
    ("sun", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["marriage"],
     ["sun", "saravali", "sign_placement", "pisces", "relationships"],
     "Ch.25 v.124",
     "Sun in Pisces: idealistic in love, seeks spiritual connection with "
     "partner, may sacrifice personal needs for relationship"),
    ("sun", "sign_placement", "pisces", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["sun", "saravali", "sign_placement", "pisces", "intuition"],
     "Ch.25 v.125",
     "Sun in Pisces: intuitive rather than analytical intelligence, gifted "
     "in music, poetry, and imaginative arts"),
    # Conditional
    ("sun", "sign_condition", "pisces_jupiter_strong", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "pisces", "jupiter", "strong"],
     "Ch.25 v.126",
     "Sun in Pisces with strong Jupiter: saintly disposition, widespread "
     "fame for spiritual attainments, blessed by divine grace"),
    ("sun", "sign_condition", "pisces_friend_sign", {},
     "favorable", "moderate",
     ["career_status", "spirituality"],
     ["sun", "saravali", "sign_placement", "pisces", "friend_sign"],
     "Ch.25 v.127",
     "Sun in Pisces (friend sign): harmonious expression of authority "
     "through compassion, success in healing or counseling roles"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# General Sun-in-sign conditions — Ch.25 (SAV1168–SAV1170)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_GENERAL_DATA = [
    ("sun", "sign_condition", "sun_in_own_or_exalted", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "saravali", "sign_placement", "dignity", "own_sign", "exalted"],
     "Ch.25 v.128",
     "Sun in own sign or exaltation: full expression of solar qualities, "
     "leadership, authority, fame, and vitality are enhanced"),
    ("sun", "sign_condition", "sun_in_enemy_or_debilitated", {},
     "unfavorable", "strong",
     ["career_status", "character_temperament"],
     ["sun", "saravali", "sign_placement", "dignity", "enemy_sign", "debilitated"],
     "Ch.25 v.129",
     "Sun in enemy sign or debilitation: weakened authority, lack of "
     "self-confidence, struggles for recognition, health issues"),
    ("sun", "sign_condition", "sun_sign_dispositor_strong", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "saravali", "sign_placement", "dispositor", "strong"],
     "Ch.25 v.130",
     "Sun's sign dispositor strong: mitigates negative sign placement, "
     "support from authority figures, career gains through patronage"),
]


# ── Builder ──────────────────────────────────────────────────────────────────

def _make_sign_rules(
    data: list,
    start_num: int,
) -> list[RuleRecord]:
    """Build RuleRecord objects for Sun sign-placement rules."""
    rules: list[RuleRecord] = []
    num = start_num
    for entry in data:
        (planet, ptype, sign_or_label, _conditions,
         odir, oint, odoms, extra_tags, vref, desc) = entry

        rid = f"SAV{num:04d}"

        if ptype == "sign_placement":
            primary = {
                "planet": planet,
                "placement_type": "sign_placement",
                "placement_value": [sign_or_label],
            }
        else:
            # sign_condition
            primary = {
                "planet": planet,
                "placement_type": "sign_condition",
                "yoga_label": sign_or_label,
            }

        # Character/personality rules are unspecified; others dasha-dependent
        if any(d in odoms for d in ("character_temperament", "physical_appearance")):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "sign_placement", "sun"] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter="Ch.25",
            school="parashari",
            category="sign_predictions",
            description=f"[Saravali — Sun in Signs] {desc}",
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
    all_sign_data = [
        (_SUN_ARIES_DATA, 1041),
        (_SUN_TAURUS_DATA, 1052),
        (_SUN_GEMINI_DATA, 1063),
        (_SUN_CANCER_DATA, 1074),
        (_SUN_LEO_DATA, 1085),
        (_SUN_VIRGO_DATA, 1096),
        (_SUN_LIBRA_DATA, 1107),
        (_SUN_SCORPIO_DATA, 1118),
        (_SUN_SAGITTARIUS_DATA, 1128),
        (_SUN_CAPRICORN_DATA, 1138),
        (_SUN_AQUARIUS_DATA, 1148),
        (_SUN_PISCES_DATA, 1158),
        (_SUN_GENERAL_DATA, 1168),
    ]
    result: list[RuleRecord] = []
    for data, start in all_sign_data:
        result.extend(_make_sign_rules(data, start))
    return result


SARAVALI_SIGNS_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_1_REGISTRY.add(_rule)
