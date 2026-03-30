"""src/corpus/saravali_signs_4.py — S284: Saravali Mercury in 12 Signs (Ch.28).

SAV1431–SAV1560 (130 rules).
Phase: 1B_matrix | Source: Saravali | School: parashari

Mercury in the 12 signs — Saravali Chapter 28.
Mercury governs intellect, speech, commerce, writing, nervous system,
and friendships. For each sign ~10-11 rules cover: intellectual style,
communication, commerce/trade, education, writing ability, nervous
system health, and friendships.

Dignity highlights:
  Exalted:   Virgo (own sign + exaltation)
  Debilitated: Pisces
  Own signs: Gemini, Virgo

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Aries (Ch.28 v.1–v.3)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_ARIES = [
    ("mercury", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aries", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.1",
     "Mercury in Aries: quick and sharp intellect, rapid thinking but "
     "prone to impatience in study and learning"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aries", "sign_placement", "saravali", "speech"],
     "Ch.28 v.1",
     "Mercury in Aries: bold and direct speech, argues forcefully, "
     "may offend through bluntness or aggressive rhetoric"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "aries", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.2",
     "Mercury in Aries: enterprising in trade, takes commercial risks, "
     "gains through bold ventures but losses from hasty decisions"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "weak",
     ["intelligence_education"],
     ["mercury", "aries", "sign_placement", "saravali", "education"],
     "Ch.28 v.2",
     "Mercury in Aries: learns quickly but lacks sustained focus, "
     "prefers action-oriented subjects over theoretical study"),
    ("mercury", "sign_placement", "aries", {},
     "unfavorable", "weak",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "aries", "sign_placement", "saravali", "writing"],
     "Ch.28 v.2",
     "Mercury in Aries: writing style is forceful but lacks refinement, "
     "better at oral expression than written composition"),
    ("mercury", "sign_placement", "aries", {},
     "unfavorable", "weak",
     ["physical_health"],
     ["mercury", "aries", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.3",
     "Mercury in Aries: nervous tension and headaches, restless mind "
     "causes insomnia or stress-related nervous disorders"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "weak",
     ["character_temperament"],
     ["mercury", "aries", "sign_placement", "saravali", "friends"],
     "Ch.28 v.3",
     "Mercury in Aries: attracts friends through wit and confidence, "
     "but quarrels easily and friendships may be short-lived"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "aries", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.3",
     "Mercury in Aries: competitive temperament, sharp tongue, fond of "
     "debates and intellectual contests, combative in discourse"),
    ("mercury", "sign_placement", "aries", {},
     "unfavorable", "weak",
     ["marriage"],
     ["mercury", "aries", "sign_placement", "saravali", "marriage"],
     "Ch.28 v.3",
     "Mercury in Aries: argumentative with spouse, communication issues "
     "in marriage due to impatient and domineering speech"),
    ("mercury", "sign_placement", "aries", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "aries", "sign_placement", "saravali", "career"],
     "Ch.28 v.3",
     "Mercury in Aries: suited to military correspondence, sports "
     "journalism, or competitive fields requiring quick thinking"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Taurus (Ch.28 v.4–v.6)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_TAURUS = [
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "taurus", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.4",
     "Mercury in Taurus: steady and practical intellect, good retention "
     "of learning, preference for useful and applied knowledge"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "taurus", "sign_placement", "saravali", "speech"],
     "Ch.28 v.4",
     "Mercury in Taurus: sweet and measured speech, persuasive in "
     "business negotiations, pleasing voice and articulation"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["mercury", "taurus", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.4",
     "Mercury in Taurus: highly skilled in commerce and banking, gains "
     "through trade in luxury goods, textiles, or agriculture"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "taurus", "sign_placement", "saravali", "education"],
     "Ch.28 v.5",
     "Mercury in Taurus: excels in arts, music theory, and financial "
     "education, patient and thorough learner"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "taurus", "sign_placement", "saravali", "writing"],
     "Ch.28 v.5",
     "Mercury in Taurus: writing on practical matters, skilled at "
     "financial documentation and commercial correspondence"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "weak",
     ["physical_health"],
     ["mercury", "taurus", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.5",
     "Mercury in Taurus: stable nervous constitution, calm mind, "
     "less prone to anxiety than in most other sign placements"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "taurus", "sign_placement", "saravali", "friends"],
     "Ch.28 v.6",
     "Mercury in Taurus: loyal friendships, attracts friends through "
     "reliability and generosity, popular in social circles"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "taurus", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.6",
     "Mercury in Taurus: steady temperament, appreciates beauty and "
     "fine arts, fond of comforts and sensory pleasures"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "moderate",
     ["wealth"],
     ["mercury", "taurus", "sign_placement", "saravali", "wealth"],
     "Ch.28 v.6",
     "Mercury in Taurus: accumulates wealth through intelligent "
     "investments, skilled at managing finances and resources"),
    ("mercury", "sign_placement", "taurus", {},
     "favorable", "weak",
     ["fame_reputation"],
     ["mercury", "taurus", "sign_placement", "saravali", "reputation"],
     "Ch.28 v.6",
     "Mercury in Taurus: well-regarded for trustworthiness and "
     "reliability, known for keeping promises and sound judgment"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Gemini — Own Sign (Ch.28 v.7–v.9)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_GEMINI = [
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "gemini", "sign_placement", "saravali", "intellect", "own_sign"],
     "Ch.28 v.7",
     "Mercury in Gemini (own sign): exceptionally sharp intellect, "
     "versatile mind, proficient in multiple disciplines simultaneously"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "gemini", "sign_placement", "saravali", "speech", "own_sign"],
     "Ch.28 v.7",
     "Mercury in Gemini (own sign): eloquent and witty speaker, "
     "master of rhetoric, skilled in languages and oratory"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["mercury", "gemini", "sign_placement", "saravali", "commerce", "own_sign"],
     "Ch.28 v.7",
     "Mercury in Gemini (own sign): brilliant in trade and commerce, "
     "successful merchant or broker, gains through communication skills"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "gemini", "sign_placement", "saravali", "education", "own_sign"],
     "Ch.28 v.8",
     "Mercury in Gemini (own sign): excels in grammar, logic, mathematics, "
     "and scriptural study, fond of intellectual pursuits"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "gemini", "sign_placement", "saravali", "writing", "own_sign"],
     "Ch.28 v.8",
     "Mercury in Gemini (own sign): gifted writer and poet, skilled in "
     "composing verse, prose, and technical documentation"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["physical_health"],
     ["mercury", "gemini", "sign_placement", "saravali", "nervous", "health", "own_sign"],
     "Ch.28 v.8",
     "Mercury in Gemini (own sign): active but balanced nervous system, "
     "mental agility supported by good nervous health"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mercury", "gemini", "sign_placement", "saravali", "friends", "own_sign"],
     "Ch.28 v.9",
     "Mercury in Gemini (own sign): wide social circle, befriends "
     "scholars and intellectuals, popular and well-connected"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "gemini", "sign_placement", "saravali", "temperament", "own_sign"],
     "Ch.28 v.9",
     "Mercury in Gemini (own sign): curious and adaptable nature, "
     "humorous disposition, fond of travel and variety"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["mercury", "gemini", "sign_placement", "saravali", "fame", "own_sign"],
     "Ch.28 v.9",
     "Mercury in Gemini (own sign): gains fame through intellectual "
     "achievements, recognized as learned and articulate"),
    ("mercury", "sign_placement", "gemini", {},
     "favorable", "strong",
     ["career_status"],
     ["mercury", "gemini", "sign_placement", "saravali", "career", "own_sign"],
     "Ch.28 v.9",
     "Mercury in Gemini (own sign): excels as teacher, writer, "
     "accountant, astrologer, or in any communication profession"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Cancer (Ch.28 v.10–v.12)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_CANCER = [
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "cancer", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.10",
     "Mercury in Cancer: intuitive and imaginative mind, emotional "
     "intelligence strong but analytical objectivity weakened"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "cancer", "sign_placement", "saravali", "speech"],
     "Ch.28 v.10",
     "Mercury in Cancer: speech colored by emotions, persuasive through "
     "sentiment, skilled at storytelling but prone to exaggeration"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "cancer", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.10",
     "Mercury in Cancer: trade connected to food, liquids, or nurturing "
     "products, fluctuating income due to emotional decision-making"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "cancer", "sign_placement", "saravali", "education"],
     "Ch.28 v.11",
     "Mercury in Cancer: learns best through emotional engagement, "
     "excels in history, literature, and psychology"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "cancer", "sign_placement", "saravali", "writing"],
     "Ch.28 v.11",
     "Mercury in Cancer: writing infused with feeling and imagination, "
     "talented in poetry and narrative fiction"),
    ("mercury", "sign_placement", "cancer", {},
     "unfavorable", "weak",
     ["physical_health"],
     ["mercury", "cancer", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.11",
     "Mercury in Cancer: nervous sensitivity, prone to worry and "
     "digestive troubles linked to emotional stress"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "cancer", "sign_placement", "saravali", "friends"],
     "Ch.28 v.12",
     "Mercury in Cancer: emotionally attached to friends, loyal but "
     "easily hurt, friendships based on emotional bonds"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "cancer", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.12",
     "Mercury in Cancer: changeable moods affect judgment, kind-hearted "
     "but impressionable, sentimental disposition"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "weak",
     ["marriage"],
     ["mercury", "cancer", "sign_placement", "saravali", "marriage"],
     "Ch.28 v.12",
     "Mercury in Cancer: emotionally expressive with spouse, "
     "misunderstandings from over-sensitivity in communication"),
    ("mercury", "sign_placement", "cancer", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "cancer", "sign_placement", "saravali", "career"],
     "Ch.28 v.12",
     "Mercury in Cancer: suited to counseling, hospitality, teaching "
     "children, or caretaking professions"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Leo (Ch.28 v.13–v.15)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_LEO = [
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "leo", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.13",
     "Mercury in Leo: proud intellect, thinks in grand terms, good at "
     "strategic planning but may overlook details"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "leo", "sign_placement", "saravali", "speech"],
     "Ch.28 v.13",
     "Mercury in Leo: authoritative and commanding speech, inclined to "
     "boastfulness, skilled at public speaking and leadership address"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "leo", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.13",
     "Mercury in Leo: trade in luxury goods or entertainment, gains "
     "through government connections but overspends on display"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "weak",
     ["intelligence_education"],
     ["mercury", "leo", "sign_placement", "saravali", "education"],
     "Ch.28 v.14",
     "Mercury in Leo: learns for status rather than knowledge, "
     "drawn to political science, management, and drama"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "leo", "sign_placement", "saravali", "writing"],
     "Ch.28 v.14",
     "Mercury in Leo: writes with authority and flair, suited to "
     "political commentary, editorials, or dramatic composition"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "weak",
     ["physical_health"],
     ["mercury", "leo", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.14",
     "Mercury in Leo: stress from pride and ego conflicts affects "
     "nervous system, prone to heart palpitations from anxiety"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "leo", "sign_placement", "saravali", "friends"],
     "Ch.28 v.15",
     "Mercury in Leo: attracts admiring friends, enjoys holding court, "
     "generous with companions but expects deference"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "leo", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.15",
     "Mercury in Leo: dignified bearing, proud and self-assured, "
     "ambitious nature, fond of drama and performance"),
    ("mercury", "sign_placement", "leo", {},
     "mixed", "moderate",
     ["fame_reputation"],
     ["mercury", "leo", "sign_placement", "saravali", "fame"],
     "Ch.28 v.15",
     "Mercury in Leo: known for bold opinions and confident expression, "
     "may gain recognition through political or artistic speech"),
    ("mercury", "sign_placement", "leo", {},
     "unfavorable", "weak",
     ["progeny"],
     ["mercury", "leo", "sign_placement", "saravali", "progeny"],
     "Ch.28 v.15",
     "Mercury in Leo: few children or difficulty relating intellectually "
     "to offspring, proud attitude creates distance with children"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Virgo — Own Sign + Exaltation (Ch.28 v.16–v.18)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_VIRGO = [
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "virgo", "sign_placement", "saravali", "intellect", "own_sign", "exalted"],
     "Ch.28 v.16",
     "Mercury in Virgo (own sign, exalted): superlative intellect, "
     "analytical brilliance, mastery of logic and discrimination"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "virgo", "sign_placement", "saravali", "speech", "own_sign", "exalted"],
     "Ch.28 v.16",
     "Mercury in Virgo (own sign, exalted): precise and articulate speech, "
     "perfect grammar and diction, skilled in refined expression"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["mercury", "virgo", "sign_placement", "saravali", "commerce", "own_sign", "exalted"],
     "Ch.28 v.16",
     "Mercury in Virgo (own sign, exalted): exceptional commercial acumen, "
     "meticulous in accounts, highly successful in trade and business"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["intelligence_education"],
     ["mercury", "virgo", "sign_placement", "saravali", "education", "own_sign", "exalted"],
     "Ch.28 v.17",
     "Mercury in Virgo (own sign, exalted): excels in mathematics, "
     "grammar, astrology, and all sciences requiring precision"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "virgo", "sign_placement", "saravali", "writing", "own_sign", "exalted"],
     "Ch.28 v.17",
     "Mercury in Virgo (own sign, exalted): masterful writer, produces "
     "scholarly works, skilled in technical and scientific composition"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["physical_health"],
     ["mercury", "virgo", "sign_placement", "saravali", "nervous", "health", "exalted"],
     "Ch.28 v.17",
     "Mercury in Virgo (own sign, exalted): robust nervous constitution, "
     "sharp senses, disciplined health habits protect nervous system"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mercury", "virgo", "sign_placement", "saravali", "friends", "own_sign", "exalted"],
     "Ch.28 v.18",
     "Mercury in Virgo (own sign, exalted): attracts learned and virtuous "
     "friends, respected in scholarly circles, wide social network"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mercury", "virgo", "sign_placement", "saravali", "temperament", "own_sign", "exalted"],
     "Ch.28 v.18",
     "Mercury in Virgo (own sign, exalted): discriminating, modest, "
     "virtuous temperament, devoted to truth and precision"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["fame_reputation"],
     ["mercury", "virgo", "sign_placement", "saravali", "fame", "own_sign", "exalted"],
     "Ch.28 v.18",
     "Mercury in Virgo (own sign, exalted): attains lasting fame through "
     "scholarship, writing, or intellectual accomplishments"),
    ("mercury", "sign_placement", "virgo", {},
     "favorable", "strong",
     ["wealth"],
     ["mercury", "virgo", "sign_placement", "saravali", "wealth", "own_sign", "exalted"],
     "Ch.28 v.18",
     "Mercury in Virgo (own sign, exalted): abundant wealth through "
     "intellectual professions, skilled management of resources"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Libra (Ch.28 v.19–v.21)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_LIBRA = [
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "libra", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.19",
     "Mercury in Libra: balanced and fair-minded intellect, good at "
     "weighing arguments, skilled in diplomacy and negotiation"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "libra", "sign_placement", "saravali", "speech"],
     "Ch.28 v.19",
     "Mercury in Libra: refined and harmonious speech, excels in "
     "mediation, tactful expression, and social discourse"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "libra", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.19",
     "Mercury in Libra: skilled in partnership-based commerce, trade in "
     "art, fashion, or beauty products, fair in business dealings"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "libra", "sign_placement", "saravali", "education"],
     "Ch.28 v.20",
     "Mercury in Libra: drawn to law, aesthetics, and comparative "
     "studies, learns through discussion and collaboration"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "libra", "sign_placement", "saravali", "writing"],
     "Ch.28 v.20",
     "Mercury in Libra: elegant writing style, talented in legal "
     "drafting, art criticism, or romantic literature"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "weak",
     ["physical_health"],
     ["mercury", "libra", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.20",
     "Mercury in Libra: generally balanced nervous constitution, "
     "occasional indecisiveness creates mild anxiety"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "strong",
     ["character_temperament"],
     ["mercury", "libra", "sign_placement", "saravali", "friends"],
     "Ch.28 v.21",
     "Mercury in Libra: excellent social skills, many cultured friends, "
     "popular in gatherings, skilled at maintaining relationships"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "libra", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.21",
     "Mercury in Libra: pleasant and charming disposition, lover of "
     "beauty and harmony, avoids conflict and unpleasantness"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["mercury", "libra", "sign_placement", "saravali", "fame"],
     "Ch.28 v.21",
     "Mercury in Libra: respected for fairness and diplomatic skill, "
     "gains reputation as mediator or counselor"),
    ("mercury", "sign_placement", "libra", {},
     "favorable", "moderate",
     ["marriage"],
     ["mercury", "libra", "sign_placement", "saravali", "marriage"],
     "Ch.28 v.21",
     "Mercury in Libra: harmonious communication with spouse, "
     "partnership enhanced by shared intellectual interests"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Scorpio (Ch.28 v.22–v.24)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_SCORPIO = [
    ("mercury", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "scorpio", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.22",
     "Mercury in Scorpio: penetrating and investigative intellect, "
     "skilled at uncovering secrets but prone to suspicious thinking"),
    ("mercury", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["intelligence_education"],
     ["mercury", "scorpio", "sign_placement", "saravali", "speech"],
     "Ch.28 v.22",
     "Mercury in Scorpio: sharp and stinging speech, sarcastic wit, "
     "may wound others through cutting remarks and harsh criticism"),
    ("mercury", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "scorpio", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.22",
     "Mercury in Scorpio: trade in hidden or occult matters, gains "
     "through investigation, insurance, or secret dealings"),
    ("mercury", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "scorpio", "sign_placement", "saravali", "education"],
     "Ch.28 v.23",
     "Mercury in Scorpio: excels in research, occult sciences, "
     "medicine, and detective-like analytical studies"),
    ("mercury", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "scorpio", "sign_placement", "saravali", "writing"],
     "Ch.28 v.23",
     "Mercury in Scorpio: writes with intensity and depth, talented "
     "in mystery, investigative journalism, or occult literature"),
    ("mercury", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mercury", "scorpio", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.23",
     "Mercury in Scorpio: nervous intensity and obsessive thinking, "
     "prone to insomnia, paranoia, and stress-related ailments"),
    ("mercury", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mercury", "scorpio", "sign_placement", "saravali", "friends"],
     "Ch.28 v.24",
     "Mercury in Scorpio: few trusted friends, suspicious of others' "
     "motives, friendships tested by jealousy or secrecy"),
    ("mercury", "sign_placement", "scorpio", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mercury", "scorpio", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.24",
     "Mercury in Scorpio: secretive and brooding temperament, holds "
     "grudges, vindictive when crossed, intense in all pursuits"),
    ("mercury", "sign_placement", "scorpio", {},
     "unfavorable", "weak",
     ["enemies_litigation"],
     ["mercury", "scorpio", "sign_placement", "saravali", "enemies"],
     "Ch.28 v.24",
     "Mercury in Scorpio: creates enemies through sharp tongue, "
     "involved in disputes and litigation from verbal conflicts"),
    ("mercury", "sign_placement", "scorpio", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "scorpio", "sign_placement", "saravali", "career"],
     "Ch.28 v.24",
     "Mercury in Scorpio: suited to research, espionage, detective "
     "work, surgery, or professions requiring deep investigation"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Sagittarius (Ch.28 v.25–v.27)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_SAGITTARIUS = [
    ("mercury", "sign_placement", "sagittarius", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.25",
     "Mercury in Sagittarius: philosophical and expansive intellect, "
     "interested in higher learning but lacks attention to detail"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "speech"],
     "Ch.28 v.25",
     "Mercury in Sagittarius: inspiring and optimistic speech, skilled "
     "at preaching, teaching, and moral instruction"),
    ("mercury", "sign_placement", "sagittarius", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.25",
     "Mercury in Sagittarius: trade connected to education, publishing, "
     "or religion, generous in business but poor at bookkeeping"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["intelligence_education"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "education"],
     "Ch.28 v.26",
     "Mercury in Sagittarius: drawn to philosophy, theology, law, and "
     "foreign languages, learns through broad exploration"),
    ("mercury", "sign_placement", "sagittarius", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "writing"],
     "Ch.28 v.26",
     "Mercury in Sagittarius: writes on philosophical and religious "
     "themes, skilled at translation and comparative literature"),
    ("mercury", "sign_placement", "sagittarius", {},
     "mixed", "weak",
     ["physical_health"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.26",
     "Mercury in Sagittarius: restless nervous energy, prone to "
     "overexertion from multiple simultaneous pursuits"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "friends"],
     "Ch.28 v.27",
     "Mercury in Sagittarius: befriends scholars, priests, and "
     "foreigners, friendships based on shared ideals and learning"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.27",
     "Mercury in Sagittarius: jovial and optimistic temperament, "
     "righteous disposition, loves truth and moral principles"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["fame_reputation"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "fame"],
     "Ch.28 v.27",
     "Mercury in Sagittarius: gains reputation through teaching, "
     "religious discourse, or philosophical publications"),
    ("mercury", "sign_placement", "sagittarius", {},
     "favorable", "moderate",
     ["career_status"],
     ["mercury", "sagittarius", "sign_placement", "saravali", "career"],
     "Ch.28 v.27",
     "Mercury in Sagittarius: excels as teacher, priest, publisher, "
     "translator, or in professions connected to higher learning"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Capricorn (Ch.28 v.28–v.30)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_CAPRICORN = [
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "capricorn", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.28",
     "Mercury in Capricorn: methodical and structured intellect, slow "
     "but thorough thinker, practical and goal-oriented mind"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "capricorn", "sign_placement", "saravali", "speech"],
     "Ch.28 v.28",
     "Mercury in Capricorn: formal and measured speech, speaks with "
     "authority but lacks warmth, blunt and economical with words"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "capricorn", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.28",
     "Mercury in Capricorn: cautious in trade, gains through steady "
     "enterprise, deals in land, minerals, or government contracts"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "capricorn", "sign_placement", "saravali", "education"],
     "Ch.28 v.29",
     "Mercury in Capricorn: disciplined study habits, drawn to "
     "engineering, architecture, administration, and practical sciences"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "capricorn", "sign_placement", "saravali", "writing"],
     "Ch.28 v.29",
     "Mercury in Capricorn: writes on practical and administrative "
     "matters, skilled at official documentation and reports"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "weak",
     ["physical_health"],
     ["mercury", "capricorn", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.29",
     "Mercury in Capricorn: nervous system affected by overwork and "
     "anxiety about status, prone to melancholy and stiffness"),
    ("mercury", "sign_placement", "capricorn", {},
     "unfavorable", "weak",
     ["character_temperament"],
     ["mercury", "capricorn", "sign_placement", "saravali", "friends"],
     "Ch.28 v.30",
     "Mercury in Capricorn: few close friends, reserved in social "
     "settings, prefers professional relationships over personal"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "capricorn", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.30",
     "Mercury in Capricorn: serious and reserved temperament, ambitious "
     "but cautious, values tradition and established methods"),
    ("mercury", "sign_placement", "capricorn", {},
     "unfavorable", "weak",
     ["character_temperament"],
     ["mercury", "capricorn", "sign_placement", "saravali", "worry"],
     "Ch.28 v.30",
     "Mercury in Capricorn: prone to pessimism and excessive worry, "
     "overthinks problems, difficulty enjoying leisure"),
    ("mercury", "sign_placement", "capricorn", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "capricorn", "sign_placement", "saravali", "career"],
     "Ch.28 v.30",
     "Mercury in Capricorn: suited to government service, engineering, "
     "surveying, or administrative and managerial roles"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Aquarius (Ch.28 v.31–v.33)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_AQUARIUS = [
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aquarius", "sign_placement", "saravali", "intellect"],
     "Ch.28 v.31",
     "Mercury in Aquarius: original and unconventional intellect, "
     "innovative thinking but eccentric reasoning at times"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aquarius", "sign_placement", "saravali", "speech"],
     "Ch.28 v.31",
     "Mercury in Aquarius: speaks on humanitarian and progressive themes, "
     "unconventional expression, sometimes misunderstood"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "aquarius", "sign_placement", "saravali", "commerce"],
     "Ch.28 v.31",
     "Mercury in Aquarius: trade in technology, inventions, or social "
     "enterprises, gains through networking and group activities"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aquarius", "sign_placement", "saravali", "education"],
     "Ch.28 v.32",
     "Mercury in Aquarius: drawn to sciences, technology, astrology, "
     "and humanitarian studies, self-taught in many subjects"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "aquarius", "sign_placement", "saravali", "writing"],
     "Ch.28 v.32",
     "Mercury in Aquarius: writes on scientific and social themes, "
     "talented in technical writing and visionary literature"),
    ("mercury", "sign_placement", "aquarius", {},
     "unfavorable", "weak",
     ["physical_health"],
     ["mercury", "aquarius", "sign_placement", "saravali", "nervous", "health"],
     "Ch.28 v.32",
     "Mercury in Aquarius: erratic nervous energy, sudden bouts of "
     "exhaustion, nervous disorders from irregular habits"),
    ("mercury", "sign_placement", "aquarius", {},
     "favorable", "moderate",
     ["character_temperament"],
     ["mercury", "aquarius", "sign_placement", "saravali", "friends"],
     "Ch.28 v.33",
     "Mercury in Aquarius: large network of diverse friends, valued "
     "in group settings, friendships based on shared ideals"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["character_temperament"],
     ["mercury", "aquarius", "sign_placement", "saravali", "temperament"],
     "Ch.28 v.33",
     "Mercury in Aquarius: independent and detached temperament, "
     "values freedom of thought, humanitarian outlook"),
    ("mercury", "sign_placement", "aquarius", {},
     "unfavorable", "weak",
     ["character_temperament"],
     ["mercury", "aquarius", "sign_placement", "saravali", "stubborn"],
     "Ch.28 v.33",
     "Mercury in Aquarius: mentally stubborn despite appearing open, "
     "fixed ideas once formed, difficult to persuade"),
    ("mercury", "sign_placement", "aquarius", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "aquarius", "sign_placement", "saravali", "career"],
     "Ch.28 v.33",
     "Mercury in Aquarius: suited to scientific research, technology, "
     "social reform, astrology, or group leadership roles"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury in Pisces — Debilitated (Ch.28 v.34–v.36)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_PISCES = [
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "strong",
     ["intelligence_education"],
     ["mercury", "pisces", "sign_placement", "saravali", "intellect", "debilitated"],
     "Ch.28 v.34",
     "Mercury in Pisces (debilitated): confused and unfocused intellect, "
     "difficulty with logical analysis, dreamy and impractical thinking"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["intelligence_education"],
     ["mercury", "pisces", "sign_placement", "saravali", "speech", "debilitated"],
     "Ch.28 v.34",
     "Mercury in Pisces (debilitated): vague and rambling speech, "
     "difficulty expressing ideas clearly, prone to exaggeration"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "strong",
     ["career_status", "wealth"],
     ["mercury", "pisces", "sign_placement", "saravali", "commerce", "debilitated"],
     "Ch.28 v.34",
     "Mercury in Pisces (debilitated): poor commercial sense, cheated "
     "in trade, losses through careless accounting and naivety"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["intelligence_education"],
     ["mercury", "pisces", "sign_placement", "saravali", "education", "debilitated"],
     "Ch.28 v.35",
     "Mercury in Pisces (debilitated): struggles with structured "
     "learning, poor at mathematics and logic, but imaginative"),
    ("mercury", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "pisces", "sign_placement", "saravali", "writing", "debilitated"],
     "Ch.28 v.35",
     "Mercury in Pisces (debilitated): writing lacks structure but "
     "rich in imagination, may produce spiritual or mystical works"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["physical_health"],
     ["mercury", "pisces", "sign_placement", "saravali", "nervous", "health", "debilitated"],
     "Ch.28 v.35",
     "Mercury in Pisces (debilitated): weak nervous constitution, "
     "prone to anxiety, phobias, and psychosomatic disorders"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mercury", "pisces", "sign_placement", "saravali", "friends", "debilitated"],
     "Ch.28 v.36",
     "Mercury in Pisces (debilitated): exploited by cunning friends, "
     "too trusting in relationships, deceived through gullibility"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["character_temperament"],
     ["mercury", "pisces", "sign_placement", "saravali", "temperament", "debilitated"],
     "Ch.28 v.36",
     "Mercury in Pisces (debilitated): indecisive and impressionable, "
     "easily influenced, lacks intellectual self-confidence"),
    ("mercury", "sign_placement", "pisces", {},
     "unfavorable", "moderate",
     ["wealth"],
     ["mercury", "pisces", "sign_placement", "saravali", "wealth", "debilitated"],
     "Ch.28 v.36",
     "Mercury in Pisces (debilitated): difficulty accumulating wealth, "
     "money lost through poor judgment and misplaced trust"),
    ("mercury", "sign_placement", "pisces", {},
     "mixed", "moderate",
     ["career_status"],
     ["mercury", "pisces", "sign_placement", "saravali", "career", "debilitated"],
     "Ch.28 v.36",
     "Mercury in Pisces (debilitated): may find success in spiritual "
     "teaching, music, art, or charitable work despite debilitation"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# General / Conditional Rules (SAV1551–SAV1560)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_GENERAL = [
    ("mercury", "sign_placement", "virgo", {"dignity": "exalted"},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mercury", "exalted", "virgo", "saravali", "dignity"],
     "Ch.28 v.37",
     "Mercury exalted in Virgo: produces a brilliant scholar, skilled "
     "writer, and successful merchant — the highest expression of Mercury"),
    ("mercury", "sign_placement", "pisces", {"dignity": "debilitated"},
     "unfavorable", "strong",
     ["intelligence_education", "wealth"],
     ["mercury", "debilitated", "pisces", "saravali", "dignity"],
     "Ch.28 v.37",
     "Mercury debilitated in Pisces: maximum impairment of analytical "
     "ability, commercial failure, and communication difficulties"),
    ("mercury", "sign_placement", "gemini", {"dignity": "own_sign"},
     "favorable", "strong",
     ["intelligence_education", "intelligence_education"],
     ["mercury", "own_sign", "gemini", "saravali", "dignity"],
     "Ch.28 v.38",
     "Mercury in own sign Gemini: full expression of communicative and "
     "intellectual gifts, versatility and eloquence at their peak"),
    ("mercury", "sign_placement", "virgo", {"dignity": "own_sign_exalted"},
     "favorable", "strong",
     ["intelligence_education", "intelligence_education", "career_status"],
     ["mercury", "own_sign", "exalted", "virgo", "saravali", "dignity"],
     "Ch.28 v.38",
     "Mercury in Virgo (own + exalted): double dignity produces supreme "
     "analytical power, unmatched precision in thought and expression"),
    ("mercury", "sign_placement", "sagittarius", {"sign_lord": "jupiter", "relationship": "neutral"},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "sagittarius", "saravali", "neutral_sign", "jupiter"],
     "Ch.28 v.39",
     "Mercury in Jupiter's signs: philosophical bent enhances wisdom "
     "but reduces Mercury's natural precision and analytical sharpness"),
    ("mercury", "sign_placement", "aries", {"sign_lord": "mars", "relationship": "neutral"},
     "mixed", "moderate",
     ["intelligence_education"],
     ["mercury", "aries", "saravali", "neutral_sign", "mars"],
     "Ch.28 v.39",
     "Mercury in Mars' signs: speech becomes forceful and combative, "
     "intellect sharpened for strategy but coarsened in expression"),
    ("mercury", "sign_placement", "cancer", {"sign_lord": "moon", "relationship": "enemy"},
     "unfavorable", "moderate",
     ["intelligence_education"],
     ["mercury", "cancer", "saravali", "enemy_sign", "moon"],
     "Ch.28 v.40",
     "Mercury in Moon's sign Cancer: emotional thinking clouds rational "
     "judgment, intellect subject to tidal moods and changeability"),
    ("mercury", "sign_placement", "leo", {"sign_lord": "sun", "relationship": "friend"},
     "mixed", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "leo", "saravali", "friend_sign", "sun"],
     "Ch.28 v.40",
     "Mercury in Sun's sign Leo: speech gains authority and confidence, "
     "but ego colors intellectual expression and objectivity suffers"),
    ("mercury", "sign_placement", "taurus", {"sign_lord": "venus", "relationship": "friend"},
     "favorable", "moderate",
     ["intelligence_education", "wealth"],
     ["mercury", "taurus", "saravali", "friend_sign", "venus"],
     "Ch.28 v.41",
     "Mercury in Venus' signs: refined and artistic communication, "
     "commercial ability enhanced by aesthetic sense and charm"),
    ("mercury", "sign_placement", "capricorn", {"sign_lord": "saturn", "relationship": "friend"},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "capricorn", "saravali", "friend_sign", "saturn"],
     "Ch.28 v.41",
     "Mercury in Saturn's signs: disciplined and structured thinking, "
     "slow but methodical intellect suited to administrative work"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Builder
# ═══════════════════════════════════════════════════════════════════════════════

_ALL_SIGN_DATA: list[tuple] = [
    ("aries", _MERCURY_ARIES),
    ("taurus", _MERCURY_TAURUS),
    ("gemini", _MERCURY_GEMINI),
    ("cancer", _MERCURY_CANCER),
    ("leo", _MERCURY_LEO),
    ("virgo", _MERCURY_VIRGO),
    ("libra", _MERCURY_LIBRA),
    ("scorpio", _MERCURY_SCORPIO),
    ("sagittarius", _MERCURY_SAGITTARIUS),
    ("capricorn", _MERCURY_CAPRICORN),
    ("aquarius", _MERCURY_AQUARIUS),
    ("pisces", _MERCURY_PISCES),
]


def _make_sign_rules(
    sign_data: list[tuple],
    start_num: int,
    chapter: str,
) -> list[RuleRecord]:
    """Convert raw tuples into RuleRecord instances for sign-placement rules."""
    rules: list[RuleRecord] = []
    num = start_num
    for row in sign_data:
        (planet, ptype, pvalue, extras,
         odir, oint, odoms, extra_tags, vref, desc) = row

        rid = f"SAV{num:04d}"

        primary: dict = {
            "planet": planet,
            "placement_type": ptype,
            "placement_value": pvalue,
        }
        if extras:
            primary.update(extras)

        # Timing: character/appearance rules are unspecified; others dasha-dependent
        if any(d in odoms for d in ("character_temperament", "physical_appearance")):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "mercury", "sign_placement", pvalue] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter=chapter,
            school="parashari",
            category="sign_predictions",
            description=f"[Saravali — Mercury in {pvalue.title()}] {desc}",
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
    """Build all 130 Mercury-in-signs rules (SAV1431–SAV1560)."""
    all_rules: list[RuleRecord] = []
    current_num = 1431

    # 12 signs (120 rules)
    for _sign_name, data in _ALL_SIGN_DATA:
        sign_rules = _make_sign_rules(data, current_num, "Ch.28")
        all_rules.extend(sign_rules)
        current_num += len(data)

    # General / conditional rules (10 rules)
    general_rules = _make_sign_rules(_MERCURY_GENERAL, current_num, "Ch.28")
    all_rules.extend(general_rules)

    return all_rules


SARAVALI_SIGNS_4_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_4_REGISTRY.add(_rule)
