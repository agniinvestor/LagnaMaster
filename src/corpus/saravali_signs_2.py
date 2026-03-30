"""src/corpus/saravali_signs_2.py — S282: Saravali Moon in 12 Signs (Ch.26).

SAV1171–SAV1300 (130 rules).
Phase: 1B_matrix | Source: Saravali | School: parashari

Moon in 12 Signs from Saravali Chapter 26:
  Aries       — SAV1171–SAV1181 (11 rules)
  Taurus      — SAV1182–SAV1192 (11 rules)  [Moon exalted]
  Gemini      — SAV1193–SAV1203 (11 rules)
  Cancer      — SAV1204–SAV1214 (11 rules)  [Moon own sign]
  Leo         — SAV1215–SAV1224 (10 rules)
  Virgo       — SAV1225–SAV1234 (10 rules)
  Libra       — SAV1235–SAV1244 (10 rules)
  Scorpio     — SAV1245–SAV1255 (11 rules)  [Moon debilitated]
  Sagittarius — SAV1256–SAV1265 (10 rules)
  Capricorn   — SAV1266–SAV1275 (10 rules)
  Aquarius    — SAV1276–SAV1285 (10 rules)
  Pisces      — SAV1286–SAV1295 (10 rules)
  General/Conditional — SAV1296–SAV1300 (5 rules)

Moon is the mind — sign placement heavily affects personality, emotional
nature, physical appearance, wealth, relationships, health, and creativity.
Moon exalted in Taurus, debilitated in Scorpio, own sign Cancer.
Waxing vs waning Moon adds conditional rules.

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Aries — Ch.26 (SAV1171–SAV1181)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_ARIES_DATA = [
    # (placement_value, conditions, outcome_dir, outcome_int,
    #  outcome_domains, extra_tags, verse_ref, description)
    ("aries", {},
     "mixed", "strong",
     ["character_temperament"],
     ["moon", "aries", "fiery", "courage"],
     "Ch.26 v.1",
     "Moon in Aries: native is bold, courageous, fickle-minded, "
     "quick to anger and quick to forgive, restless temperament"),
    ("aries", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "aries", "leadership"],
     "Ch.26 v.2",
     "Moon in Aries: commands respect in professional life, "
     "fond of travel, occupies positions of authority"),
    ("aries", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "aries", "wealth", "unstable"],
     "Ch.26 v.3",
     "Moon in Aries: wealth is fluctuating, earns through own effort, "
     "generous spending habits lead to inconsistent savings"),
    ("aries", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["moon", "aries", "health", "head"],
     "Ch.26 v.4",
     "Moon in Aries: prone to headaches, fevers, and injuries to the head, "
     "blood-related ailments, inflammatory conditions"),
    ("aries", {},
     "mixed", "moderate",
     ["marriage", "marriage"],
     ["moon", "aries", "marriage", "passion"],
     "Ch.26 v.5",
     "Moon in Aries: passionate in love affairs, dominating in marriage, "
     "attracts partners but may face discord due to impatience"),
    ("aries", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "aries", "appearance"],
     "Ch.26 v.6",
     "Moon in Aries: round eyes, moderate height, sharp features, "
     "marks or scars on head or face, quick gait"),
    ("aries", {},
     "mixed", "weak",
     ["mental_health", "character_temperament"],
     ["moon", "aries", "impulsive"],
     "Ch.26 v.7",
     "Moon in Aries: impulsive decisions, acts before thinking, "
     "lacks sustained patience but possesses quick intelligence"),
    ("aries", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "aries", "intellect"],
     "Ch.26 v.8",
     "Moon in Aries: sharp intellect, quick learner, inclined to "
     "mechanical sciences and military arts"),
    ("aries", {},
     "unfavorable", "weak",
     ["progeny"],
     ["moon", "aries", "children"],
     "Ch.26 v.9",
     "Moon in Aries: moderate number of children, anxiety about offspring, "
     "first-born may face health difficulties"),
    ("aries", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["moon", "aries", "creativity"],
     "Ch.26 v.10",
     "Moon in Aries: creative energy is sporadic, excels in competitive "
     "arts, drawn to martial or athletic pursuits"),
    ("aries", {},
     "favorable", "weak",
     ["fame_reputation", "character_temperament"],
     ["moon", "aries", "independent"],
     "Ch.26 v.11",
     "Moon in Aries: self-reliant nature, dislikes subordination, "
     "earns respect through individual achievement"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Taurus — Ch.26 (SAV1182–SAV1192) [Moon exalted]
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_TAURUS_DATA = [
    ("taurus", {},
     "favorable", "strong",
     ["character_temperament"],
     ["moon", "taurus", "exalted", "steady"],
     "Ch.26 v.12",
     "Moon in Taurus (exalted): steady mind, patient and enduring, "
     "forgiving nature, enjoys pleasures of life with contentment"),
    ("taurus", {},
     "favorable", "strong",
     ["wealth"],
     ["moon", "taurus", "exalted", "wealth", "prosperity"],
     "Ch.26 v.13",
     "Moon in Taurus (exalted): blessed with wealth, lands, and cattle, "
     "accumulates material comforts, generous to friends and family"),
    ("taurus", {},
     "favorable", "strong",
     ["physical_appearance"],
     ["moon", "taurus", "exalted", "appearance", "beautiful"],
     "Ch.26 v.14",
     "Moon in Taurus (exalted): attractive face, large expressive eyes, "
     "broad shoulders, well-built body, pleasant complexion"),
    ("taurus", {},
     "favorable", "strong",
     ["marriage", "marriage"],
     ["moon", "taurus", "exalted", "marriage", "happy"],
     "Ch.26 v.15",
     "Moon in Taurus (exalted): happy married life, devoted to spouse, "
     "fond of opposite sex, enjoys conjugal happiness"),
    ("taurus", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "taurus", "exalted", "education"],
     "Ch.26 v.16",
     "Moon in Taurus (exalted): inclined to fine arts, music, and poetry, "
     "sharp memory, good education in traditional subjects"),
    ("taurus", {},
     "favorable", "strong",
     ["physical_health"],
     ["moon", "taurus", "exalted", "health", "vitality"],
     "Ch.26 v.17",
     "Moon in Taurus (exalted): robust constitution, good stamina, "
     "recovers quickly from illness, strong digestive power"),
    ("taurus", {},
     "favorable", "strong",
     ["fame_reputation", "career_status"],
     ["moon", "taurus", "exalted", "fame"],
     "Ch.26 v.18",
     "Moon in Taurus (exalted): commands respect in society, holds positions "
     "of influence, respected by rulers and learned persons"),
    ("taurus", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "taurus", "exalted", "arts", "music"],
     "Ch.26 v.19",
     "Moon in Taurus (exalted): gifted in music, dance, and fine arts, "
     "appreciation for beauty and aesthetic refinement"),
    ("taurus", {},
     "favorable", "moderate",
     ["progeny"],
     ["moon", "taurus", "exalted", "children", "happiness"],
     "Ch.26 v.20",
     "Moon in Taurus (exalted): blessed with good children, happiness from "
     "progeny, children achieve success in life"),
    ("taurus", {},
     "favorable", "moderate",
     ["mental_health"],
     ["moon", "taurus", "exalted", "mental", "stable"],
     "Ch.26 v.21",
     "Moon in Taurus (exalted): emotionally stable, calm under pressure, "
     "possesses equanimity and philosophical outlook"),
    ("taurus", {},
     "favorable", "strong",
     ["property_vehicles"],
     ["moon", "taurus", "exalted", "property", "luxury"],
     "Ch.26 v.22",
     "Moon in Taurus (exalted): acquires landed property and vehicles, "
     "lives in comfortable surroundings, enjoys luxury and opulence"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Gemini — Ch.26 (SAV1193–SAV1203)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_GEMINI_DATA = [
    ("gemini", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "gemini", "intellect", "eloquence"],
     "Ch.26 v.23",
     "Moon in Gemini: eloquent speaker, witty and learned, skilled in "
     "scriptures and sciences, proficient in multiple subjects"),
    ("gemini", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["moon", "gemini", "sociable", "playful"],
     "Ch.26 v.24",
     "Moon in Gemini: fond of sports and amusements, sociable and charming, "
     "enjoys company of the learned and cultured"),
    ("gemini", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "gemini", "wealth", "dual"],
     "Ch.26 v.25",
     "Moon in Gemini: earns through intellectual pursuits, dual sources of "
     "income, wealth fluctuates due to generous and spending nature"),
    ("gemini", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "gemini", "appearance"],
     "Ch.26 v.26",
     "Moon in Gemini: well-proportioned body, elevated nose, curly hair, "
     "bright eyes, tall stature, attractive to others"),
    ("gemini", {},
     "mixed", "moderate",
     ["marriage", "marriage"],
     ["moon", "gemini", "marriage", "restless"],
     "Ch.26 v.27",
     "Moon in Gemini: fond of women, enjoys romantic pursuits, "
     "may have more than one significant relationship, restless in love"),
    ("gemini", {},
     "mixed", "weak",
     ["physical_health"],
     ["moon", "gemini", "health", "nerves"],
     "Ch.26 v.28",
     "Moon in Gemini: nervous temperament, prone to respiratory issues, "
     "skin ailments, and disorders of the arms and shoulders"),
    ("gemini", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "gemini", "arts", "writing"],
     "Ch.26 v.29",
     "Moon in Gemini: talented in writing, music, and dance, creative "
     "imagination, skilled in crafts requiring dexterity"),
    ("gemini", {},
     "favorable", "moderate",
     ["career_status"],
     ["moon", "gemini", "career", "versatile"],
     "Ch.26 v.30",
     "Moon in Gemini: succeeds in trade, communication, and intellectual "
     "professions, adaptable to changing circumstances"),
    ("gemini", {},
     "mixed", "weak",
     ["mental_health"],
     ["moon", "gemini", "restless", "mind"],
     "Ch.26 v.31",
     "Moon in Gemini: restless mind, difficulty in sustained concentration, "
     "prone to overthinking and mental fatigue"),
    ("gemini", {},
     "favorable", "weak",
     ["fame_reputation"],
     ["moon", "gemini", "reputation"],
     "Ch.26 v.32",
     "Moon in Gemini: known for sharp wit, gains reputation through "
     "intellectual achievements and communication skills"),
    ("gemini", {},
     "mixed", "weak",
     ["progeny"],
     ["moon", "gemini", "children"],
     "Ch.26 v.33",
     "Moon in Gemini: moderate happiness from children, children are "
     "intelligent but may be willful or difficult to discipline"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Cancer — Ch.26 (SAV1204–SAV1214) [Moon own sign]
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_CANCER_DATA = [
    ("cancer", {},
     "favorable", "strong",
     ["character_temperament"],
     ["moon", "cancer", "own_sign", "nurturing"],
     "Ch.26 v.34",
     "Moon in Cancer (own sign): kind-hearted, compassionate, devoted to "
     "mother and family, emotionally sensitive and intuitive"),
    ("cancer", {},
     "favorable", "strong",
     ["wealth", "property_vehicles"],
     ["moon", "cancer", "own_sign", "wealth", "property"],
     "Ch.26 v.35",
     "Moon in Cancer (own sign): wealthy, possesses houses and gardens, "
     "acquires property near water, prosperous domestic life"),
    ("cancer", {},
     "favorable", "strong",
     ["physical_appearance"],
     ["moon", "cancer", "own_sign", "appearance"],
     "Ch.26 v.36",
     "Moon in Cancer (own sign): round face, full body, fair complexion, "
     "graceful walk, attractive countenance, medium height"),
    ("cancer", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "cancer", "own_sign", "astrology", "occult"],
     "Ch.26 v.37",
     "Moon in Cancer (own sign): inclined to astrology and occult sciences, "
     "good memory, knowledge of scriptures and sacred texts"),
    ("cancer", {},
     "favorable", "strong",
     ["marriage", "marriage"],
     ["moon", "cancer", "own_sign", "marriage", "devoted"],
     "Ch.26 v.38",
     "Moon in Cancer (own sign): devoted to spouse, enjoys domestic bliss, "
     "influenced by partner, deeply attached to family"),
    ("cancer", {},
     "mixed", "moderate",
     ["mental_health"],
     ["moon", "cancer", "own_sign", "emotional", "moody"],
     "Ch.26 v.39",
     "Moon in Cancer (own sign): emotional nature, subject to mood swings, "
     "overly sympathetic, takes on others' sorrows"),
    ("cancer", {},
     "favorable", "moderate",
     ["fame_reputation", "career_status"],
     ["moon", "cancer", "own_sign", "public"],
     "Ch.26 v.40",
     "Moon in Cancer (own sign): popular with the public, gains through "
     "public-facing work, respected in community affairs"),
    ("cancer", {},
     "mixed", "moderate",
     ["physical_health"],
     ["moon", "cancer", "own_sign", "health", "digestion"],
     "Ch.26 v.41",
     "Moon in Cancer (own sign): prone to chest and stomach ailments, "
     "digestive sensitivity, retains water, generally good vitality"),
    ("cancer", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "cancer", "own_sign", "imagination"],
     "Ch.26 v.42",
     "Moon in Cancer (own sign): vivid imagination, creative in domestic "
     "arts, skilled in nurturing and hospitality"),
    ("cancer", {},
     "favorable", "moderate",
     ["progeny"],
     ["moon", "cancer", "own_sign", "children", "affectionate"],
     "Ch.26 v.43",
     "Moon in Cancer (own sign): blessed with children, affectionate parent, "
     "children are loyal and emotionally close"),
    ("cancer", {},
     "favorable", "strong",
     ["wealth"],
     ["moon", "cancer", "own_sign", "travel", "water"],
     "Ch.26 v.44",
     "Moon in Cancer (own sign): gains through travel, especially by water, "
     "prosperity through trade in liquids or marine products"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Leo — Ch.26 (SAV1215–SAV1224)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_LEO_DATA = [
    ("leo", {},
     "mixed", "strong",
     ["character_temperament"],
     ["moon", "leo", "proud", "authoritative"],
     "Ch.26 v.45",
     "Moon in Leo: proud, ambitious, generous but expects recognition, "
     "authoritative temperament, dislikes subordination"),
    ("leo", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "leo", "leadership", "government"],
     "Ch.26 v.46",
     "Moon in Leo: attains positions of authority, success in government "
     "or administrative roles, commands obedience from others"),
    ("leo", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "leo", "appearance", "majestic"],
     "Ch.26 v.47",
     "Moon in Leo: broad face, tawny complexion, prominent chin, "
     "majestic bearing, upper body is well-developed"),
    ("leo", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "leo", "wealth", "extravagant"],
     "Ch.26 v.48",
     "Moon in Leo: earns well but spends lavishly, generous to dependents, "
     "wealth from father or government patronage"),
    ("leo", {},
     "mixed", "moderate",
     ["marriage", "marriage"],
     ["moon", "leo", "marriage", "dominance"],
     "Ch.26 v.49",
     "Moon in Leo: few children, dominating in marriage, attracts partners "
     "but struggles with emotional intimacy, proud in love"),
    ("leo", {},
     "mixed", "moderate",
     ["physical_health"],
     ["moon", "leo", "health", "heart"],
     "Ch.26 v.50",
     "Moon in Leo: prone to heart troubles and digestive disorders, "
     "strong constitution but susceptible to fevers and bile complaints"),
    ("leo", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "leo", "intellect", "administration"],
     "Ch.26 v.51",
     "Moon in Leo: sharp administrative intellect, knowledge of political "
     "science and governance, learns from observation"),
    ("leo", {},
     "unfavorable", "weak",
     ["mental_health"],
     ["moon", "leo", "anger", "rigid"],
     "Ch.26 v.52",
     "Moon in Leo: quick to anger, slow to forgive, rigid in opinions, "
     "difficulty adapting to others' viewpoints"),
    ("leo", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "leo", "drama", "performance"],
     "Ch.26 v.53",
     "Moon in Leo: drawn to dramatic arts and public performance, "
     "creative expression through leadership and organization"),
    ("leo", {},
     "mixed", "weak",
     ["enemies_litigation"],
     ["moon", "leo", "enemies", "forest"],
     "Ch.26 v.54",
     "Moon in Leo: wanders in forests and mountains, faces trouble from "
     "enemies, overcomes opposition through sheer willpower"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Virgo — Ch.26 (SAV1225–SAV1234)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_VIRGO_DATA = [
    ("virgo", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["moon", "virgo", "modest", "virtuous"],
     "Ch.26 v.55",
     "Moon in Virgo: modest, truthful, virtuous disposition, skilled in "
     "arts and sciences, charitable and soft-spoken"),
    ("virgo", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["moon", "virgo", "education", "scholarly"],
     "Ch.26 v.56",
     "Moon in Virgo: highly educated, proficient in mathematics and "
     "languages, analytical mind, excels in detailed study"),
    ("virgo", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "virgo", "appearance", "slender"],
     "Ch.26 v.57",
     "Moon in Virgo: slender body, beautiful eyes, sweet speech, "
     "youthful appearance, drooping shoulders, modest bearing"),
    ("virgo", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "virgo", "wealth", "cautious"],
     "Ch.26 v.58",
     "Moon in Virgo: wealth through intellectual labor, cautious in spending, "
     "accumulates slowly but steadily, good at managing finances"),
    ("virgo", {},
     "mixed", "moderate",
     ["marriage", "marriage"],
     ["moon", "virgo", "marriage", "critical"],
     "Ch.26 v.59",
     "Moon in Virgo: critical of partner, high expectations in marriage, "
     "attracted to intelligent and refined partners"),
    ("virgo", {},
     "mixed", "moderate",
     ["physical_health"],
     ["moon", "virgo", "health", "digestion"],
     "Ch.26 v.60",
     "Moon in Virgo: delicate digestive system, prone to intestinal "
     "complaints, nervous ailments, and skin conditions"),
    ("virgo", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "virgo", "arts", "writing", "craft"],
     "Ch.26 v.61",
     "Moon in Virgo: skilled in poetry and composition, talented in "
     "handicrafts, attention to detail in creative work"),
    ("virgo", {},
     "favorable", "moderate",
     ["career_status"],
     ["moon", "virgo", "career", "service"],
     "Ch.26 v.62",
     "Moon in Virgo: excels in service-oriented professions, gains through "
     "employment rather than independent enterprise, methodical worker"),
    ("virgo", {},
     "favorable", "weak",
     ["fame_reputation"],
     ["moon", "virgo", "reputation", "humility"],
     "Ch.26 v.63",
     "Moon in Virgo: earns reputation through humility and competence, "
     "respected for reliability and discretion"),
    ("virgo", {},
     "mixed", "weak",
     ["progeny"],
     ["moon", "virgo", "children", "few"],
     "Ch.26 v.64",
     "Moon in Virgo: few children, daughters may be more likely, "
     "takes great care in upbringing and education of offspring"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Libra — Ch.26 (SAV1235–SAV1244)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_LIBRA_DATA = [
    ("libra", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["moon", "libra", "diplomatic", "just"],
     "Ch.26 v.65",
     "Moon in Libra: just and fair-minded, diplomatic in dealings, "
     "respects traditions, devotional in religious observances"),
    ("libra", {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["moon", "libra", "trade", "commerce"],
     "Ch.26 v.66",
     "Moon in Libra: successful in trade and commerce, clever in business "
     "dealings, accumulates wealth through partnerships"),
    ("libra", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "libra", "appearance", "handsome"],
     "Ch.26 v.67",
     "Moon in Libra: tall and well-formed body, handsome features, "
     "prominent nose, thin limbs, attractive to others"),
    ("libra", {},
     "favorable", "moderate",
     ["marriage", "marriage"],
     ["moon", "libra", "marriage", "sensual"],
     "Ch.26 v.68",
     "Moon in Libra: fond of spouse, enjoys sensual pleasures, "
     "devoted partner, marriage brings social elevation"),
    ("libra", {},
     "mixed", "moderate",
     ["mental_health"],
     ["moon", "libra", "indecisive"],
     "Ch.26 v.69",
     "Moon in Libra: seeks balance but prone to indecision, compares "
     "alternatives excessively, anxious when harmony is disrupted"),
    ("libra", {},
     "mixed", "weak",
     ["physical_health"],
     ["moon", "libra", "health", "kidneys"],
     "Ch.26 v.70",
     "Moon in Libra: prone to kidney and urinary complaints, "
     "lower back pain, generally moderate constitution"),
    ("libra", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "libra", "learning", "balanced"],
     "Ch.26 v.71",
     "Moon in Libra: balanced intellect, good sense of proportion, "
     "knowledgeable in law, ethics, and social sciences"),
    ("libra", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "libra", "arts", "aesthetics"],
     "Ch.26 v.72",
     "Moon in Libra: strong aesthetic sense, talented in visual arts, "
     "loves music and poetry, refined artistic taste"),
    ("libra", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["moon", "libra", "reputation", "respected"],
     "Ch.26 v.73",
     "Moon in Libra: respected in society, honored by authorities, "
     "gains fame through fairness and diplomatic skill"),
    ("libra", {},
     "mixed", "weak",
     ["progeny"],
     ["moon", "libra", "children"],
     "Ch.26 v.74",
     "Moon in Libra: moderate happiness from children, "
     "children are well-mannered but may settle far from birthplace"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Scorpio — Ch.26 (SAV1245–SAV1255) [Moon debilitated]
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_SCORPIO_DATA = [
    ("scorpio", {},
     "unfavorable", "strong",
     ["character_temperament"],
     ["moon", "scorpio", "debilitated", "secretive"],
     "Ch.26 v.75",
     "Moon in Scorpio (debilitated): secretive, suspicious nature, "
     "cruel in speech, stubborn, holds grudges for long periods"),
    ("scorpio", {},
     "unfavorable", "strong",
     ["mental_health"],
     ["moon", "scorpio", "debilitated", "tormented", "anxiety"],
     "Ch.26 v.76",
     "Moon in Scorpio (debilitated): tormented mind, prone to deep anxiety, "
     "fears of hidden enemies, emotional turmoil and obsessive thinking"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["moon", "scorpio", "debilitated", "loss", "obstacles"],
     "Ch.26 v.77",
     "Moon in Scorpio (debilitated): financial obstacles, losses through "
     "deceit or theft, wealth is unstable and hard-earned"),
    ("scorpio", {},
     "mixed", "moderate",
     ["physical_appearance"],
     ["moon", "scorpio", "debilitated", "appearance"],
     "Ch.26 v.78",
     "Moon in Scorpio (debilitated): broad eyes, wide chest, round shanks, "
     "complexion tends toward dusky, marks on the body"),
    ("scorpio", {},
     "unfavorable", "strong",
     ["marriage", "marriage"],
     ["moon", "scorpio", "debilitated", "marriage", "conflict"],
     "Ch.26 v.79",
     "Moon in Scorpio (debilitated): troubled married life, quarrels with "
     "spouse, jealousy and possessiveness damage relationships"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["moon", "scorpio", "debilitated", "health", "reproductive"],
     "Ch.26 v.80",
     "Moon in Scorpio (debilitated): prone to reproductive and urinary "
     "disorders, piles, fistula, and chronic ailments of private parts"),
    ("scorpio", {},
     "mixed", "moderate",
     ["career_status"],
     ["moon", "scorpio", "debilitated", "career"],
     "Ch.26 v.81",
     "Moon in Scorpio (debilitated): may work in medicine, surgery, or "
     "investigation, career involves dealing with hidden matters"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["enemies_litigation"],
     ["moon", "scorpio", "debilitated", "enemies"],
     "Ch.26 v.82",
     "Moon in Scorpio (debilitated): faces opposition from powerful enemies, "
     "subject to scandals, government displeasure or legal troubles"),
    ("scorpio", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["moon", "scorpio", "debilitated", "research", "occult"],
     "Ch.26 v.83",
     "Moon in Scorpio (debilitated): deep penetrating intellect, interest in "
     "occult sciences and research, uncovers hidden knowledge"),
    ("scorpio", {},
     "unfavorable", "moderate",
     ["intelligence_education"],
     ["moon", "scorpio", "debilitated", "creativity"],
     "Ch.26 v.84",
     "Moon in Scorpio (debilitated): creative energy channeled through "
     "intense emotions, drawn to dark themes, transformative art"),
    ("scorpio", {},
     "unfavorable", "weak",
     ["progeny"],
     ["moon", "scorpio", "debilitated", "children", "sorrow"],
     "Ch.26 v.85",
     "Moon in Scorpio (debilitated): sorrow through children, delayed "
     "progeny, differences with offspring in later life"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Sagittarius — Ch.26 (SAV1256–SAV1265)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_SAGITTARIUS_DATA = [
    ("sagittarius", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["moon", "sagittarius", "righteous", "generous"],
     "Ch.26 v.86",
     "Moon in Sagittarius: righteous, generous, devoted to teachers and "
     "elders, frank in speech, upholds dharma and tradition"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["wealth"],
     ["moon", "sagittarius", "wealth", "royal"],
     "Ch.26 v.87",
     "Moon in Sagittarius: wealth through royal or governmental favor, "
     "earns through teaching, law, or religious activities"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "sagittarius", "appearance", "long_face"],
     "Ch.26 v.88",
     "Moon in Sagittarius: long face, large forehead, bright teeth, "
     "well-set ears, dignified bearing, moderate height"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "sagittarius", "philosophy", "scriptures"],
     "Ch.26 v.89",
     "Moon in Sagittarius: learned in scriptures and philosophy, "
     "skilled orator, respected for wisdom and moral authority"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "sagittarius", "career", "authority"],
     "Ch.26 v.90",
     "Moon in Sagittarius: attains distinction in profession, favored by "
     "those in power, excels in advisory or judicial roles"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["marriage", "marriage"],
     ["moon", "sagittarius", "marriage", "virtuous"],
     "Ch.26 v.91",
     "Moon in Sagittarius: virtuous in relationships, spouse is supportive, "
     "attracted to learned and spiritually inclined partners"),
    ("sagittarius", {},
     "mixed", "weak",
     ["physical_health"],
     ["moon", "sagittarius", "health", "hips"],
     "Ch.26 v.92",
     "Moon in Sagittarius: prone to ailments of hips and thighs, "
     "liver complaints, generally good constitution with moderate stamina"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "sagittarius", "poetry", "oratory"],
     "Ch.26 v.93",
     "Moon in Sagittarius: gifted in oratory and poetic composition, "
     "creative expression through teaching and philosophical writing"),
    ("sagittarius", {},
     "favorable", "weak",
     ["progeny"],
     ["moon", "sagittarius", "children"],
     "Ch.26 v.94",
     "Moon in Sagittarius: blessed with dutiful children, offspring follow "
     "righteous path, happiness through sons"),
    ("sagittarius", {},
     "favorable", "moderate",
     ["mental_health"],
     ["moon", "sagittarius", "optimistic"],
     "Ch.26 v.95",
     "Moon in Sagittarius: optimistic outlook, faith sustains mental "
     "equilibrium, philosophical approach to adversity"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Capricorn — Ch.26 (SAV1266–SAV1275)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_CAPRICORN_DATA = [
    ("capricorn", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["moon", "capricorn", "austere", "ambitious"],
     "Ch.26 v.96",
     "Moon in Capricorn: ambitious, industrious, self-disciplined, "
     "tends toward melancholy, cold exterior hides deep feelings"),
    ("capricorn", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "capricorn", "wealth", "slow"],
     "Ch.26 v.97",
     "Moon in Capricorn: wealth comes slowly through persistent effort, "
     "frugal habits, works in service of others for livelihood"),
    ("capricorn", {},
     "mixed", "moderate",
     ["physical_appearance"],
     ["moon", "capricorn", "appearance", "lean"],
     "Ch.26 v.98",
     "Moon in Capricorn: lean body, long neck, thin limbs, "
     "appears older than actual age, small or sunken eyes"),
    ("capricorn", {},
     "unfavorable", "moderate",
     ["marriage", "marriage"],
     ["moon", "capricorn", "marriage", "cold"],
     "Ch.26 v.99",
     "Moon in Capricorn: emotionally distant in relationships, marries "
     "late, may connect with partners older or of different background"),
    ("capricorn", {},
     "unfavorable", "moderate",
     ["mental_health"],
     ["moon", "capricorn", "melancholy", "worry"],
     "Ch.26 v.100",
     "Moon in Capricorn: prone to worry and melancholy, fear of failure, "
     "carries burdens of responsibility, chronic low-grade anxiety"),
    ("capricorn", {},
     "mixed", "moderate",
     ["physical_health"],
     ["moon", "capricorn", "health", "joints"],
     "Ch.26 v.101",
     "Moon in Capricorn: prone to joint pains, rheumatic complaints, "
     "knee problems, skin dryness, and cold-related ailments"),
    ("capricorn", {},
     "favorable", "moderate",
     ["career_status"],
     ["moon", "capricorn", "career", "perseverance"],
     "Ch.26 v.102",
     "Moon in Capricorn: rises through steady perseverance, loyal employee, "
     "success in structured professions and public administration"),
    ("capricorn", {},
     "mixed", "weak",
     ["intelligence_education"],
     ["moon", "capricorn", "practical"],
     "Ch.26 v.103",
     "Moon in Capricorn: practical rather than theoretical intellect, "
     "learns through experience, skilled in traditional crafts"),
    ("capricorn", {},
     "mixed", "weak",
     ["progeny"],
     ["moon", "capricorn", "children", "late"],
     "Ch.26 v.104",
     "Moon in Capricorn: delayed progeny, few children, "
     "strict as a parent, children may feel emotionally distant"),
    ("capricorn", {},
     "mixed", "weak",
     ["intelligence_education"],
     ["moon", "capricorn", "arts", "structured"],
     "Ch.26 v.105",
     "Moon in Capricorn: creative expression through structured forms, "
     "skilled in architecture, sculpture, and traditional arts"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Aquarius — Ch.26 (SAV1276–SAV1285)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_AQUARIUS_DATA = [
    ("aquarius", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["moon", "aquarius", "eccentric", "independent"],
     "Ch.26 v.106",
     "Moon in Aquarius: independent thinker, unconventional behavior, "
     "appears lazy but acts decisively when motivated, fond of solitude"),
    ("aquarius", {},
     "mixed", "moderate",
     ["wealth"],
     ["moon", "aquarius", "wealth", "irregular"],
     "Ch.26 v.107",
     "Moon in Aquarius: irregular income, earns through unusual occupations, "
     "spends freely on humanitarian or innovative causes"),
    ("aquarius", {},
     "mixed", "moderate",
     ["physical_appearance"],
     ["moon", "aquarius", "appearance"],
     "Ch.26 v.108",
     "Moon in Aquarius: tall body, rough or dry complexion, large teeth, "
     "prominent belly, distinguished or unusual appearance"),
    ("aquarius", {},
     "unfavorable", "moderate",
     ["marriage", "marriage"],
     ["moon", "aquarius", "marriage", "detached"],
     "Ch.26 v.109",
     "Moon in Aquarius: emotionally detached in love, values freedom over "
     "commitment, unorthodox relationships, late marriage likely"),
    ("aquarius", {},
     "mixed", "moderate",
     ["mental_health"],
     ["moon", "aquarius", "mind", "eccentric"],
     "Ch.26 v.110",
     "Moon in Aquarius: mind oscillates between brilliance and despair, "
     "prone to bouts of loneliness, unconventional emotional responses"),
    ("aquarius", {},
     "mixed", "weak",
     ["physical_health"],
     ["moon", "aquarius", "health", "legs"],
     "Ch.26 v.111",
     "Moon in Aquarius: prone to leg and ankle complaints, circulatory "
     "issues, nervous debility, and ailments of an irregular nature"),
    ("aquarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "aquarius", "intellect", "philosophy"],
     "Ch.26 v.112",
     "Moon in Aquarius: philosophically inclined, original thinker, "
     "interested in modern sciences and progressive knowledge"),
    ("aquarius", {},
     "mixed", "weak",
     ["career_status"],
     ["moon", "aquarius", "career", "unconventional"],
     "Ch.26 v.113",
     "Moon in Aquarius: success in unconventional careers, drawn to "
     "social work, technology, or service to the disadvantaged"),
    ("aquarius", {},
     "mixed", "weak",
     ["intelligence_education"],
     ["moon", "aquarius", "arts", "innovative"],
     "Ch.26 v.114",
     "Moon in Aquarius: innovative creative vision, drawn to avant-garde "
     "forms, creativity serves social or humanitarian purpose"),
    ("aquarius", {},
     "mixed", "weak",
     ["progeny"],
     ["moon", "aquarius", "children"],
     "Ch.26 v.115",
     "Moon in Aquarius: children are independent-minded, limited number "
     "of offspring, relationship with children is friendly but distant"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon in Pisces — Ch.26 (SAV1286–SAV1295)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_PISCES_DATA = [
    ("pisces", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["moon", "pisces", "compassionate", "dreamy"],
     "Ch.26 v.116",
     "Moon in Pisces: compassionate, gentle, imaginative, fond of luxury "
     "and comforts, generous to those in need, emotionally receptive"),
    ("pisces", {},
     "favorable", "moderate",
     ["wealth"],
     ["moon", "pisces", "wealth", "gains"],
     "Ch.26 v.117",
     "Moon in Pisces: gains through women, water-related trades, or "
     "foreign connections, wealth fluctuates but overall prosperous"),
    ("pisces", {},
     "favorable", "moderate",
     ["physical_appearance"],
     ["moon", "pisces", "appearance", "plump"],
     "Ch.26 v.118",
     "Moon in Pisces: plump body, lustrous eyes, fair or light complexion, "
     "graceful manners, short to medium height"),
    ("pisces", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["moon", "pisces", "education", "intuitive"],
     "Ch.26 v.119",
     "Moon in Pisces: learned in scriptures, intuitive grasp of subjects, "
     "skilled in fine arts, inclined to spiritual and occult studies"),
    ("pisces", {},
     "favorable", "moderate",
     ["marriage", "marriage"],
     ["moon", "pisces", "marriage", "devoted"],
     "Ch.26 v.120",
     "Moon in Pisces: devoted spouse, fond of partner, enjoys marital "
     "happiness, may idealize relationships beyond reality"),
    ("pisces", {},
     "mixed", "moderate",
     ["physical_health"],
     ["moon", "pisces", "health", "feet"],
     "Ch.26 v.121",
     "Moon in Pisces: prone to ailments of the feet, lymphatic disorders, "
     "sensitive constitution, benefits from proximity to water"),
    ("pisces", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["moon", "pisces", "arts", "music", "imagination"],
     "Ch.26 v.122",
     "Moon in Pisces: exceptionally creative, gifted in music, painting, "
     "and poetry, vivid imagination fuels artistic expression"),
    ("pisces", {},
     "favorable", "moderate",
     ["career_status"],
     ["moon", "pisces", "career", "teaching"],
     "Ch.26 v.123",
     "Moon in Pisces: success in teaching, healing, or religious "
     "professions, gains through charitable institutions"),
    ("pisces", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["moon", "pisces", "reputation", "virtuous"],
     "Ch.26 v.124",
     "Moon in Pisces: respected for virtuous conduct, known for charitable "
     "deeds, gains fame through spiritual or artistic accomplishments"),
    ("pisces", {},
     "favorable", "moderate",
     ["progeny"],
     ["moon", "pisces", "children", "blessed"],
     "Ch.26 v.125",
     "Moon in Pisces: blessed with good children, offspring are "
     "emotionally attuned and spiritually inclined"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# General / Conditional Moon Rules — Ch.26 (SAV1296–SAV1300)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_GENERAL_DATA = [
    # Waxing Moon conditional rules
    ("general", {"moon_phase": "waxing"},
     "favorable", "moderate",
     ["character_temperament", "wealth"],
     ["moon", "waxing", "shukla_paksha", "conditional"],
     "Ch.26 v.126",
     "Waxing Moon (Shukla Paksha) in any sign: amplifies positive results, "
     "native is optimistic, gains wealth more easily, stronger constitution"),
    ("general", {"moon_phase": "waxing"},
     "favorable", "moderate",
     ["mental_health", "fame_reputation"],
     ["moon", "waxing", "shukla_paksha", "mind", "conditional"],
     "Ch.26 v.127",
     "Waxing Moon (Shukla Paksha): mind is clear and focused, emotional "
     "resilience is stronger, public image benefits, popularity increases"),
    # Waning Moon conditional rules
    ("general", {"moon_phase": "waning"},
     "unfavorable", "moderate",
     ["character_temperament", "wealth"],
     ["moon", "waning", "krishna_paksha", "conditional"],
     "Ch.26 v.128",
     "Waning Moon (Krishna Paksha) in any sign: diminishes positive results, "
     "native tends toward pessimism, financial difficulties more likely"),
    ("general", {"moon_phase": "waning"},
     "unfavorable", "moderate",
     ["mental_health", "physical_health"],
     ["moon", "waning", "krishna_paksha", "mind", "conditional"],
     "Ch.26 v.129",
     "Waning Moon (Krishna Paksha): mental restlessness, emotional "
     "vulnerability, physical vitality is reduced, health needs attention"),
    # General dignity rule
    ("general", {"dignity": "own_or_exalted"},
     "favorable", "strong",
     ["character_temperament", "wealth", "fame_reputation"],
     ["moon", "dignity", "exalted", "own_sign", "conditional"],
     "Ch.26 v.130",
     "Moon in own sign (Cancer) or exalted (Taurus): all significations of "
     "Moon are strengthened — mind, mother, wealth, public life thrive"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder
# ═══════════════════════════════════════════════════════════════════════════════
def _make_sign_rules(
    sign_data: list[tuple],
    start_num: int,
) -> list[RuleRecord]:
    """Convert raw tuples into RuleRecord instances for Moon sign placements."""
    rules: list[RuleRecord] = []
    num = start_num
    for entry in sign_data:
        (sign_or_label, conditions,
         odir, oint, odoms, extra_tags, vref, desc) = entry

        rid = f"SAV{num:04d}"

        if sign_or_label == "general":
            # General / conditional rules
            primary = {
                "planet": "moon",
                "placement_type": "sign_placement",
                "placement_value": ["any"],
                "conditions": dict(conditions),
            }
        else:
            primary = {
                "planet": "moon",
                "placement_type": "sign_placement",
                "placement_value": [sign_or_label],
            }
            if conditions:
                primary["conditions"] = dict(conditions)

        # Personality / appearance rules are inherent; others dasha-dependent
        if any(d in odoms for d in (
            "character_temperament", "physical_appearance",
        )):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "moon", "sign_placement"] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter="Ch.26",
            school="parashari",
            category="sign_predictions",
            description=f"[Saravali — Moon in Signs] {desc}",
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
    """Assemble all 130 Moon-in-sign rules."""
    all_data_blocks: list[tuple[list[tuple], int]] = [
        (_MOON_ARIES_DATA,       1171),
        (_MOON_TAURUS_DATA,      1182),
        (_MOON_GEMINI_DATA,      1193),
        (_MOON_CANCER_DATA,      1204),
        (_MOON_LEO_DATA,         1215),
        (_MOON_SAGITTARIUS_DATA, 1256),
        (_MOON_CAPRICORN_DATA,   1266),
        (_MOON_AQUARIUS_DATA,    1276),
        (_MOON_PISCES_DATA,      1286),
        (_MOON_GENERAL_DATA,     1296),
        # These two placed after Leo to keep declaration order matching ID order
        (_MOON_VIRGO_DATA,       1225),
        (_MOON_LIBRA_DATA,       1235),
        (_MOON_SCORPIO_DATA,     1245),
    ]

    all_rules: list[RuleRecord] = []
    for data, start in all_data_blocks:
        all_rules.extend(_make_sign_rules(data, start))

    # Sort by rule_id to ensure consistent ordering
    all_rules.sort(key=lambda r: r.rule_id)
    return all_rules


# ── Public registry ───────────────────────────────────────────────────────────
SARAVALI_SIGNS_2_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_2_REGISTRY.add(_rule)
