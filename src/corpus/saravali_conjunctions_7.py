"""src/corpus/saravali_conjunctions_7.py — S279: Saravali two-planet conjunctions.

SAV781–SAV910 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 21-23:
  Jupiter-Venus  (Ch.21-22) — SAV781–SAV823 (43 rules)
  Jupiter-Saturn (Ch.22)    — SAV824–SAV866 (43 rules)
  Venus-Saturn   (Ch.22-23) — SAV867–SAV910 (44 rules)

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
# Jupiter-Venus Conjunction — Ch.21-22 (SAV781–SAV823)
# ═══════════════════════════════════════════════════════════════════════════════
_JUPITER_VENUS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("jupiter_venus", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "1st_house"],
     "Ch.21 v.1",
     "Jupiter-Venus conjunction in 1st house: handsome appearance, virtuous "
     "character, blessed with wisdom and material comforts"),
    ("jupiter_venus", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["fame_reputation", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "1st_house", "learned"],
     "Ch.21 v.2",
     "Jupiter-Venus conjunction in 1st house: learned and eloquent, "
     "respected in society, commands admiration for grace and wisdom"),
    # House 2
    ("jupiter_venus", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "2nd_house"],
     "Ch.21 v.3",
     "Jupiter-Venus conjunction in 2nd house: accumulates great wealth, "
     "sweet and persuasive speech, enjoys luxury and fine food"),
    ("jupiter_venus", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "2nd_house", "family"],
     "Ch.21 v.4",
     "Jupiter-Venus conjunction in 2nd house: distinguished family, "
     "poetic talent, earns through teaching, arts, or advisory roles"),
    # House 3
    ("jupiter_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "3rd_house"],
     "Ch.21 v.5",
     "Jupiter-Venus conjunction in 3rd house: generous and courageous, "
     "benefits from siblings, gains through artistic short journeys"),
    ("jupiter_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["jupiter", "venus", "conjunction", "saravali", "3rd_house", "skill"],
     "Ch.21 v.6",
     "Jupiter-Venus conjunction in 3rd house: skilled in fine arts and "
     "communication, success in media, publishing, or creative commerce"),
    ("jupiter_venus", "conjunction_in_house", 3, {},
     "favorable", "weak",
     ["fame_reputation", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "3rd_house", "charm"],
     "Ch.21 v.7",
     "Jupiter-Venus conjunction in 3rd house: charming personality wins "
     "allies, persuasive and graceful in negotiations, admired by peers"),
    # House 4
    ("jupiter_venus", "conjunction_in_house", 4, {},
     "favorable", "strong",
     ["property_vehicles", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "4th_house"],
     "Ch.21 v.7",
     "Jupiter-Venus conjunction in 4th house: blessed with fine vehicles, "
     "beautiful home, landed property, and domestic happiness"),
    ("jupiter_venus", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["mental_health", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "4th_house", "peace"],
     "Ch.21 v.8",
     "Jupiter-Venus conjunction in 4th house: contented mind, enjoys "
     "maternal blessings, harmonious family life, inner peace"),
    # House 5
    ("jupiter_venus", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "5th_house"],
     "Ch.21 v.9",
     "Jupiter-Venus conjunction in 5th house: blessed with talented children, "
     "creative brilliance, success in speculation and arts"),
    ("jupiter_venus", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "5th_house", "fortune"],
     "Ch.21 v.10",
     "Jupiter-Venus conjunction in 5th house: great fortune through "
     "purva-punya, ministerial position, fame through wisdom and artistry"),
    ("jupiter_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["marriage", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "5th_house", "romance"],
     "Ch.21 v.11",
     "Jupiter-Venus conjunction in 5th house: romantic and devoted in love, "
     "happy courtship, refined taste in pleasures and entertainment"),
    # House 6
    ("jupiter_venus", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "6th_house"],
     "Ch.21 v.11",
     "Jupiter-Venus conjunction in 6th house: overcomes enemies through "
     "diplomacy, but benefics weakened in dusthana reduce prosperity"),
    ("jupiter_venus", "conjunction_in_house", 6, {},
     "unfavorable", "weak",
     ["physical_health", "marriage"],
     ["jupiter", "venus", "conjunction", "saravali", "6th_house", "health"],
     "Ch.21 v.12",
     "Jupiter-Venus conjunction in 6th house: diabetes or sugar-related "
     "ailments, indulgence causes health issues, marital discord"),
    # House 7
    ("jupiter_venus", "conjunction_in_house", 7, {},
     "favorable", "strong",
     ["marriage", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "7th_house"],
     "Ch.21 v.13",
     "Jupiter-Venus conjunction in 7th house: beautiful and virtuous spouse, "
     "happy marriage, gains wealth through partnerships"),
    ("jupiter_venus", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "7th_house", "social"],
     "Ch.21 v.14",
     "Jupiter-Venus conjunction in 7th house: socially prominent, diplomatic "
     "nature, admired for charm and ethical conduct in dealings"),
    ("jupiter_venus", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "7th_house", "trade"],
     "Ch.21 v.15",
     "Jupiter-Venus conjunction in 7th house: success in business partnerships, "
     "gains through trade in luxury goods, prosperous foreign dealings"),
    # House 8
    ("jupiter_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "8th_house"],
     "Ch.21 v.15",
     "Jupiter-Venus conjunction in 8th house: long life due to double "
     "benefic protection, but wealth through inheritance or spouse only"),
    ("jupiter_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.21 v.16",
     "Jupiter-Venus conjunction in 8th house: interest in tantric or "
     "mystical arts, hidden wisdom, spiritual transformation through crisis"),
    # House 9
    ("jupiter_venus", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "9th_house"],
     "Ch.22 v.1",
     "Jupiter-Venus conjunction in 9th house: deeply religious and "
     "prosperous, blessed by preceptor, fortune through dharmic pursuits"),
    ("jupiter_venus", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["fame_reputation", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "9th_house", "guru"],
     "Ch.22 v.2",
     "Jupiter-Venus conjunction in 9th house: revered as teacher or guide, "
     "philosophical beauty, fame through wisdom and artistic expression"),
    ("jupiter_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["jupiter", "venus", "conjunction", "saravali", "9th_house", "father"],
     "Ch.22 v.3",
     "Jupiter-Venus conjunction in 9th house: benefits from wealthy and "
     "cultured father, long-distance travel brings fortune and grace"),
    # House 10
    ("jupiter_venus", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "10th_house"],
     "Ch.22 v.3",
     "Jupiter-Venus conjunction in 10th house: eminent career in arts, "
     "education, or finance, widespread fame, royal or government favor"),
    ("jupiter_venus", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["jupiter", "venus", "conjunction", "saravali", "10th_house", "luxury"],
     "Ch.22 v.4",
     "Jupiter-Venus conjunction in 10th house: wealth through profession, "
     "luxurious lifestyle, commands vehicles, servants, and comforts"),
    ("jupiter_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "10th_house", "virtue"],
     "Ch.22 v.5",
     "Jupiter-Venus conjunction in 10th house: virtuous conduct in public "
     "life, earns recognition for ethical leadership and generous patronage"),
    # House 11
    ("jupiter_venus", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "11th_house"],
     "Ch.22 v.5",
     "Jupiter-Venus conjunction in 11th house: abundant gains from multiple "
     "sources, influential friends, fulfillment of all desires"),
    ("jupiter_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["character_temperament", "marriage"],
     ["jupiter", "venus", "conjunction", "saravali", "11th_house", "social"],
     "Ch.22 v.6",
     "Jupiter-Venus conjunction in 11th house: virtuous and generous, "
     "happy marriage, gains through spouse and elder siblings"),
    # House 12
    ("jupiter_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "12th_house"],
     "Ch.22 v.7",
     "Jupiter-Venus conjunction in 12th house: charitable and spiritual, "
     "expenditure on noble causes, but material wealth diminished"),
    ("jupiter_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["foreign_travel", "marriage"],
     ["jupiter", "venus", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.22 v.8",
     "Jupiter-Venus conjunction in 12th house: gains in foreign lands, "
     "bed pleasures, but separation from homeland and family"),
    ("jupiter_venus", "conjunction_in_house", 12, {},
     "favorable", "weak",
     ["spirituality", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "12th_house", "moksha"],
     "Ch.22 v.9",
     "Jupiter-Venus conjunction in 12th house: inclined toward liberation, "
     "renounces worldly pleasures for spiritual growth, visits holy places"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("jupiter_venus", "conjunction_condition", "jupiter_sign_sagittarius", {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.22 v.10",
     "Jupiter-Venus conjunction in Sagittarius (Jupiter's own sign): wisdom "
     "dominates, philosophical depth with artistic expression, dharmic life"),
    ("jupiter_venus", "conjunction_condition", "jupiter_sign_pisces", {},
     "favorable", "strong",
     ["spirituality", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "own_sign", "pisces", "exaltation"],
     "Ch.22 v.11",
     "Jupiter-Venus conjunction in Pisces (Jupiter own + Venus exalted): "
     "supreme beneficence, exceptional fortune, wisdom and luxury combined"),
    ("jupiter_venus", "conjunction_condition", "venus_sign_taurus", {},
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["jupiter", "venus", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.22 v.12",
     "Jupiter-Venus conjunction in Taurus (Venus's own sign): luxury "
     "dominates, beautiful appearance, great material prosperity"),
    ("jupiter_venus", "conjunction_condition", "venus_sign_libra", {},
     "favorable", "strong",
     ["marriage", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "own_sign", "libra"],
     "Ch.22 v.13",
     "Jupiter-Venus conjunction in Libra (Venus's own sign): harmonious "
     "relationships, artistic fame, luxury dominates with social grace"),
    ("jupiter_venus", "conjunction_condition", "debilitated_jupiter_capricorn", {},
     "unfavorable", "moderate",
     ["spirituality", "career_status"],
     ["jupiter", "venus", "conjunction", "saravali", "debilitation", "capricorn"],
     "Ch.22 v.14",
     "Jupiter-Venus conjunction in Capricorn (Jupiter debilitated): wisdom "
     "suppressed by materialism, spiritual hypocrisy, hollow luxury"),
    ("jupiter_venus", "conjunction_condition", "debilitated_venus_virgo", {},
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["jupiter", "venus", "conjunction", "saravali", "debilitation", "virgo"],
     "Ch.22 v.15",
     "Jupiter-Venus conjunction in Virgo (Venus debilitated): over-critical "
     "nature in relationships, beauty marred by perfectionism, delayed wealth"),
    ("jupiter_venus", "conjunction_condition", "saturn_aspect_discipline", {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["jupiter", "venus", "conjunction", "saravali", "saturn_aspect"],
     "Ch.22 v.16",
     "Jupiter-Venus conjunction aspected by Saturn: disciplined luxury, "
     "wealth acquired slowly but retained, restrained indulgence"),
    ("jupiter_venus", "conjunction_condition", "mars_aspect_protection", {},
     "favorable", "moderate",
     ["wealth", "enemies_litigation"],
     ["jupiter", "venus", "conjunction", "saravali", "mars_aspect"],
     "Ch.22 v.17",
     "Jupiter-Venus conjunction aspected by Mars: protective wealth, "
     "courage to defend fortune, energized beneficence"),
    ("jupiter_venus", "conjunction_condition", "mercury_aspect_commerce", {},
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["jupiter", "venus", "conjunction", "saravali", "mercury_aspect"],
     "Ch.22 v.18",
     "Jupiter-Venus conjunction aspected by Mercury: commercial wisdom, "
     "artistic intelligence, success in luxury trade and education"),
    ("jupiter_venus", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "kendra"],
     "Ch.22 v.19",
     "Jupiter-Venus conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies double benefic power, wealth and fame prominent"),
    ("jupiter_venus", "conjunction_condition", "trikona_placement", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["jupiter", "venus", "conjunction", "saravali", "trikona"],
     "Ch.22 v.20",
     "Jupiter-Venus conjunction in any trikona (1/5/9): supreme dharmic "
     "combination, fortune through wisdom and artistic merit"),
    ("jupiter_venus", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["wealth", "marriage"],
     ["jupiter", "venus", "conjunction", "saravali", "dusthana"],
     "Ch.22 v.21",
     "Jupiter-Venus conjunction in any dusthana (6/8/12): benefics weakened, "
     "wealth and relationship blessings diminished, wasted potential"),
    ("jupiter_venus", "conjunction_condition", "artistic_wisdom", {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["jupiter", "venus", "conjunction", "saravali", "art", "wisdom"],
     "Ch.22 v.22",
     "Jupiter-Venus conjunction well-placed: natural aptitude for combining "
     "philosophy and art, success as teacher of aesthetic disciplines"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Jupiter-Saturn Conjunction — Ch.22 (SAV824–SAV866)
# ═══════════════════════════════════════════════════════════════════════════════
_JUPITER_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("jupiter_saturn", "conjunction_in_house", 1, {},
     "mixed", "strong",
     ["character_temperament", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "1st_house"],
     "Ch.22 v.23",
     "Jupiter-Saturn conjunction in 1st house: serious and mature demeanor, "
     "assumes responsibility early, structured approach to life"),
    ("jupiter_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "1st_house", "austere"],
     "Ch.22 v.24",
     "Jupiter-Saturn conjunction in 1st house: lean or thin body, austere "
     "appearance, philosophical but pessimistic outlook"),
    # House 2
    ("jupiter_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "2nd_house"],
     "Ch.22 v.25",
     "Jupiter-Saturn conjunction in 2nd house: delayed but lasting wealth, "
     "measured speech, accumulates through patience and frugality"),
    ("jupiter_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "2nd_house", "family"],
     "Ch.22 v.26",
     "Jupiter-Saturn conjunction in 2nd house: traditional family values, "
     "knowledge of ancient sciences, respected for serious scholarship"),
    # House 3
    ("jupiter_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "3rd_house"],
     "Ch.22 v.27",
     "Jupiter-Saturn conjunction in 3rd house: courageous but cautious, "
     "gains through persistent effort, strained relations with siblings"),
    ("jupiter_saturn", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "3rd_house", "skill"],
     "Ch.22 v.28",
     "Jupiter-Saturn conjunction in 3rd house: skilled in structured "
     "communication, success in technical writing or law"),
    ("jupiter_saturn", "conjunction_in_house", 3, {},
     "mixed", "weak",
     ["character_temperament", "enemies_litigation"],
     ["jupiter", "saturn", "conjunction", "saravali", "3rd_house", "sibling"],
     "Ch.22 v.29",
     "Jupiter-Saturn conjunction in 3rd house: differences with younger "
     "siblings, solitary in endeavors, self-reliant but isolated efforts"),
    # House 4
    ("jupiter_saturn", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["property_vehicles", "mental_health"],
     ["jupiter", "saturn", "conjunction", "saravali", "4th_house"],
     "Ch.22 v.29",
     "Jupiter-Saturn conjunction in 4th house: acquires property after "
     "delay, old or ancestral buildings, limited domestic happiness"),
    ("jupiter_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "4th_house", "mind"],
     "Ch.22 v.30",
     "Jupiter-Saturn conjunction in 4th house: heavy mind, burdened by "
     "responsibilities, lacks carefree enjoyment, melancholic tendency"),
    # House 5
    ("jupiter_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["progeny", "intelligence_education"],
     ["jupiter", "saturn", "conjunction", "saravali", "5th_house"],
     "Ch.22 v.31",
     "Jupiter-Saturn conjunction in 5th house: delayed progeny, children "
     "are serious and disciplined, structured intellectual approach"),
    ("jupiter_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["wealth", "intelligence_education"],
     ["jupiter", "saturn", "conjunction", "saravali", "5th_house", "fortune"],
     "Ch.22 v.32",
     "Jupiter-Saturn conjunction in 5th house: fortune through perseverance, "
     "speculative gains only after careful planning, conservative approach"),
    # House 6
    ("jupiter_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["jupiter", "saturn", "conjunction", "saravali", "6th_house"],
     "Ch.22 v.33",
     "Jupiter-Saturn conjunction in 6th house: defeats enemies through "
     "patience and legal means, chronic but manageable health conditions"),
    ("jupiter_saturn", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["career_status", "enemies_litigation"],
     ["jupiter", "saturn", "conjunction", "saravali", "6th_house", "service"],
     "Ch.22 v.34",
     "Jupiter-Saturn conjunction in 6th house: excels in service-oriented "
     "career, structured approach to overcoming obstacles, judicial skill"),
    ("jupiter_saturn", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "6th_house", "health"],
     "Ch.22 v.35",
     "Jupiter-Saturn conjunction in 6th house: liver or joint ailments, "
     "weight-related health issues, stress from excessive responsibility"),
    # House 7
    ("jupiter_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "7th_house"],
     "Ch.22 v.35",
     "Jupiter-Saturn conjunction in 7th house: delayed marriage, spouse "
     "is mature and serious, partnerships built on duty rather than passion"),
    ("jupiter_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "7th_house", "spouse"],
     "Ch.22 v.36",
     "Jupiter-Saturn conjunction in 7th house: elder or older spouse, "
     "loyalty and commitment in marriage but lacks romantic expression"),
    # House 8
    ("jupiter_saturn", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "8th_house"],
     "Ch.22 v.37",
     "Jupiter-Saturn conjunction in 8th house: long life with chronic "
     "ailments, inheritance after struggle, slow transformation"),
    ("jupiter_saturn", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["jupiter", "saturn", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.22 v.38",
     "Jupiter-Saturn conjunction in 8th house: deep interest in occult "
     "sciences, structured research into hidden knowledge, karmic wisdom"),
    # House 9
    ("jupiter_saturn", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["spirituality", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "9th_house"],
     "Ch.22 v.39",
     "Jupiter-Saturn conjunction in 9th house: structured wisdom, disciplined "
     "spiritual practice, respect for tradition and religious authority"),
    ("jupiter_saturn", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "9th_house", "dharma"],
     "Ch.22 v.40",
     "Jupiter-Saturn conjunction in 9th house: fortune through dharmic "
     "career, delayed but lasting prosperity, benefits from father"),
    ("jupiter_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "9th_house", "father"],
     "Ch.22 v.41",
     "Jupiter-Saturn conjunction in 9th house: serious father figure, "
     "strict religious upbringing, faith tested through hardship"),
    # House 10
    ("jupiter_saturn", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "10th_house"],
     "Ch.22 v.41",
     "Jupiter-Saturn conjunction in 10th house: powerful career in law, "
     "governance, or institutional leadership, enduring professional fame"),
    ("jupiter_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "10th_house", "authority"],
     "Ch.22 v.42",
     "Jupiter-Saturn conjunction in 10th house: accumulates wealth through "
     "authority, respected for integrity in public service"),
    ("jupiter_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "10th_house", "legacy"],
     "Ch.22 v.43",
     "Jupiter-Saturn conjunction in 10th house: builds lasting legacy, "
     "known for principled governance, combines vision with execution"),
    # House 11
    ("jupiter_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "11th_house"],
     "Ch.22 v.43",
     "Jupiter-Saturn conjunction in 11th house: steady gains through "
     "long-term investments, influential network of associates"),
    ("jupiter_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "11th_house", "social"],
     "Ch.22 v.44",
     "Jupiter-Saturn conjunction in 11th house: respected among peers, "
     "elder sibling is wise and supportive, organizational leadership"),
    ("jupiter_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "11th_house", "gains"],
     "Ch.22 v.45",
     "Jupiter-Saturn conjunction in 11th house: gains through government "
     "or institutional channels, profits from long-term structured ventures"),
    # House 12
    ("jupiter_saturn", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "12th_house"],
     "Ch.22 v.45",
     "Jupiter-Saturn conjunction in 12th house: renunciation tendencies, "
     "expenditure on spiritual pursuits, detachment from worldly gain"),
    ("jupiter_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "physical_health"],
     ["jupiter", "saturn", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.22 v.46",
     "Jupiter-Saturn conjunction in 12th house: financial losses through "
     "misplaced trust, hospitalization, isolation from family"),
    ("jupiter_saturn", "conjunction_in_house", 12, {},
     "mixed", "weak",
     ["foreign_travel", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.22 v.47",
     "Jupiter-Saturn conjunction in 12th house: settlement in foreign land, "
     "career abroad in structured institutions, distant from birthplace"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("jupiter_saturn", "conjunction_condition", "jupiter_sign_sagittarius", {},
     "favorable", "strong",
     ["spirituality", "career_status"],
     ["jupiter", "saturn", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.22 v.48",
     "Jupiter-Saturn conjunction in Sagittarius (Jupiter's own sign): Jupiter "
     "dominates, dharmic authority, wisdom structures society"),
    ("jupiter_saturn", "conjunction_condition", "jupiter_sign_pisces", {},
     "favorable", "moderate",
     ["spirituality", "intelligence_education"],
     ["jupiter", "saturn", "conjunction", "saravali", "own_sign", "pisces"],
     "Ch.22 v.49",
     "Jupiter-Saturn conjunction in Pisces (Jupiter's own sign): intuitive "
     "wisdom, spiritual discipline, compassionate authority"),
    ("jupiter_saturn", "conjunction_condition", "saturn_sign_capricorn", {},
     "mixed", "strong",
     ["career_status", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.22 v.50",
     "Jupiter-Saturn conjunction in Capricorn (Saturn own + Jupiter debilitated): "
     "Saturn dominates, material ambition overrides spiritual growth"),
    ("jupiter_saturn", "conjunction_condition", "saturn_sign_aquarius", {},
     "mixed", "moderate",
     ["career_status", "intelligence_education"],
     ["jupiter", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.22 v.51",
     "Jupiter-Saturn conjunction in Aquarius (Saturn's own sign): Saturn "
     "dominates, humanitarian ideals, structured social reform"),
    ("jupiter_saturn", "conjunction_condition", "saturn_exalted_libra", {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "exaltation", "libra"],
     "Ch.22 v.52",
     "Jupiter-Saturn conjunction in Libra (Saturn exalted): disciplined "
     "justice, balanced authority, societal impact through fair governance"),
    ("jupiter_saturn", "conjunction_condition", "mars_aspect_transformation", {},
     "unfavorable", "strong",
     ["career_status", "enemies_litigation"],
     ["jupiter", "saturn", "conjunction", "saravali", "mars_aspect"],
     "Ch.22 v.53",
     "Jupiter-Saturn conjunction aspected by Mars: forced transformation, "
     "violent upheaval in career, conflicts with authority structures"),
    ("jupiter_saturn", "conjunction_condition", "moon_aspect_emotional", {},
     "mixed", "moderate",
     ["mental_health", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "moon_aspect"],
     "Ch.22 v.54",
     "Jupiter-Saturn conjunction aspected by Moon: emotional depth added "
     "to structural wisdom, public sensitivity, fluctuating fortune"),
    ("jupiter_saturn", "conjunction_condition", "venus_aspect_softening", {},
     "favorable", "moderate",
     ["marriage", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "venus_aspect"],
     "Ch.22 v.55",
     "Jupiter-Saturn conjunction aspected by Venus: austere combination "
     "softened by grace, delayed but beautiful relationships, refined taste"),
    ("jupiter_saturn", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.22 v.56",
     "Jupiter-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "gives societal impact, institutional authority, lasting legacy"),
    ("jupiter_saturn", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "trikona"],
     "Ch.22 v.57",
     "Jupiter-Saturn conjunction in any trikona (1/5/9): dharmic discipline, "
     "structured spiritual growth, karmic merit yields delayed fortune"),
    ("jupiter_saturn", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["physical_health", "wealth"],
     ["jupiter", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.22 v.58",
     "Jupiter-Saturn conjunction in any dusthana (6/8/12): heavy karmic "
     "burden, chronic ailments, financial struggles, spiritual tests"),
    ("jupiter_saturn", "conjunction_condition", "generational_impact", {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["jupiter", "saturn", "conjunction", "saravali", "generational", "societal"],
     "Ch.22 v.59",
     "Jupiter-Saturn conjunction as generational marker: born during major "
     "societal shift, carries collective karma, public destiny"),
    ("jupiter_saturn", "conjunction_condition", "retrograde_saturn", {},
     "unfavorable", "moderate",
     ["career_status", "character_temperament"],
     ["jupiter", "saturn", "conjunction", "saravali", "retrograde", "saturn"],
     "Ch.22 v.60",
     "Jupiter-Saturn conjunction with retrograde Saturn: intensified karmic "
     "lessons, revisits past-life duties, delayed structural achievements"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Venus-Saturn Conjunction — Ch.22-23 (SAV867–SAV910)
# ═══════════════════════════════════════════════════════════════════════════════
_VENUS_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("venus_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["physical_appearance", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "1st_house"],
     "Ch.22 v.61",
     "Venus-Saturn conjunction in 1st house: attractive but austere "
     "appearance, reserved demeanor, artistic temperament with discipline"),
    ("venus_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "1st_house", "reserved"],
     "Ch.22 v.62",
     "Venus-Saturn conjunction in 1st house: delayed romantic fulfillment, "
     "serious approach to relationships, marries later in life"),
    # House 2
    ("venus_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "2nd_house"],
     "Ch.22 v.63",
     "Venus-Saturn conjunction in 2nd house: patient accumulation of wealth, "
     "careful speech, frugal despite appreciation for beauty"),
    ("venus_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "2nd_house", "family"],
     "Ch.22 v.64",
     "Venus-Saturn conjunction in 2nd house: traditional family values, "
     "skilled in crafts requiring patience, earns through disciplined art"),
    ("venus_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "weak",
     ["physical_appearance", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "2nd_house", "face"],
     "Ch.22 v.65",
     "Venus-Saturn conjunction in 2nd house: plain facial features, "
     "restrained expression, beauty appreciated only with maturity"),
    # House 3
    ("venus_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["venus", "saturn", "conjunction", "saravali", "3rd_house"],
     "Ch.22 v.65",
     "Venus-Saturn conjunction in 3rd house: persistent effort in creative "
     "pursuits, strained sibling relations, success through discipline"),
    ("venus_saturn", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["venus", "saturn", "conjunction", "saravali", "3rd_house", "craft"],
     "Ch.22 v.66",
     "Venus-Saturn conjunction in 3rd house: mastery of detailed crafts, "
     "skilled artisan, success in architecture or precision arts"),
    # House 4
    ("venus_saturn", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["property_vehicles", "mental_health"],
     ["venus", "saturn", "conjunction", "saravali", "4th_house"],
     "Ch.23 v.1",
     "Venus-Saturn conjunction in 4th house: acquires property slowly, "
     "aesthetically pleasing but modest home, lacks domestic warmth"),
    ("venus_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "marriage"],
     ["venus", "saturn", "conjunction", "saravali", "4th_house", "heart"],
     "Ch.23 v.2",
     "Venus-Saturn conjunction in 4th house: emotional restraint, difficulty "
     "expressing affection, feels lonely despite material comforts"),
    # House 5
    ("venus_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["progeny", "intelligence_education"],
     ["venus", "saturn", "conjunction", "saravali", "5th_house"],
     "Ch.23 v.3",
     "Venus-Saturn conjunction in 5th house: delayed children, artistic "
     "intellect, structured creative expression, conservative investments"),
    ("venus_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "5th_house", "romance"],
     "Ch.23 v.4",
     "Venus-Saturn conjunction in 5th house: cautious in romance, love "
     "comes late but is enduring, mature approach to courtship"),
    ("venus_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["venus", "saturn", "conjunction", "saravali", "5th_house", "creative"],
     "Ch.23 v.5",
     "Venus-Saturn conjunction in 5th house: creative talents require long "
     "cultivation, success in classical arts after years of practice"),
    # House 6
    ("venus_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["venus", "saturn", "conjunction", "saravali", "6th_house"],
     "Ch.23 v.5",
     "Venus-Saturn conjunction in 6th house: overcomes enemies through "
     "patience, chronic skin or urinary conditions, service-oriented work"),
    ("venus_saturn", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["venus", "saturn", "conjunction", "saravali", "6th_house", "health"],
     "Ch.23 v.6",
     "Venus-Saturn conjunction in 6th house: marital discord due to health "
     "issues, reproductive ailments, beauty marred by chronic illness"),
    # House 7
    ("venus_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "7th_house"],
     "Ch.23 v.7",
     "Venus-Saturn conjunction in 7th house: late marriage, spouse is "
     "older or mature, relationship built on duty and commitment"),
    ("venus_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["venus", "saturn", "conjunction", "saravali", "7th_house", "spouse"],
     "Ch.23 v.8",
     "Venus-Saturn conjunction in 7th house: partner from lower status or "
     "older age, wealth through spouse comes slowly but steadily"),
    ("venus_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["career_status", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "7th_house", "business"],
     "Ch.23 v.9",
     "Venus-Saturn conjunction in 7th house: business partnerships require "
     "patience, success in beauty or luxury industries with older partners"),
    # House 8
    ("venus_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["longevity", "marriage"],
     ["venus", "saturn", "conjunction", "saravali", "8th_house"],
     "Ch.23 v.9",
     "Venus-Saturn conjunction in 8th house: marital difficulties, loss of "
     "partner's wealth, chronic reproductive or urinary ailments"),
    ("venus_saturn", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["venus", "saturn", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.23 v.10",
     "Venus-Saturn conjunction in 8th house: interest in tantric arts, "
     "hidden wealth through patient effort, transformation through loss"),
    # House 9
    ("venus_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "9th_house"],
     "Ch.23 v.11",
     "Venus-Saturn conjunction in 9th house: disciplined devotion, "
     "aesthetic approach to spirituality, structured religious practice"),
    ("venus_saturn", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.23 v.12",
     "Venus-Saturn conjunction in 9th house: delayed fortune that endures, "
     "reputation for artistic or cultural contributions"),
    ("venus_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "marriage"],
     ["venus", "saturn", "conjunction", "saravali", "9th_house", "father"],
     "Ch.23 v.13",
     "Venus-Saturn conjunction in 9th house: father is disciplined or "
     "austere, pilgrimage to sacred places, devotion mixed with duty"),
    # House 10
    ("venus_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "10th_house"],
     "Ch.23 v.13",
     "Venus-Saturn conjunction in 10th house: career in arts, fashion, or "
     "structured aesthetics, slow but steady professional rise"),
    ("venus_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["venus", "saturn", "conjunction", "saravali", "10th_house", "craft"],
     "Ch.23 v.14",
     "Venus-Saturn conjunction in 10th house: wealth through disciplined "
     "craftsmanship, architecture, or luxury industries"),
    ("venus_saturn", "conjunction_in_house", 10, {},
     "favorable", "weak",
     ["fame_reputation", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "10th_house", "public"],
     "Ch.23 v.15",
     "Venus-Saturn conjunction in 10th house: public image of restrained "
     "elegance, recognized for enduring artistic contributions"),
    # House 11
    ("venus_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "11th_house"],
     "Ch.23 v.15",
     "Venus-Saturn conjunction in 11th house: steady gains through patient "
     "effort, fulfillment of desires after long wait, loyal friends"),
    ("venus_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "11th_house", "elder"],
     "Ch.23 v.16",
     "Venus-Saturn conjunction in 11th house: benefits from elder siblings "
     "or older associates, respected for refined and disciplined nature"),
    # House 12
    ("venus_saturn", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["venus", "saturn", "conjunction", "saravali", "12th_house"],
     "Ch.23 v.17",
     "Venus-Saturn conjunction in 12th house: expenditure on comforts, "
     "bed pleasures with restraint, spiritual beauty in solitude"),
    ("venus_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["venus", "saturn", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.23 v.18",
     "Venus-Saturn conjunction in 12th house: separation from spouse, "
     "loss through indulgence, eye troubles, hospitalization"),
    ("venus_saturn", "conjunction_in_house", 12, {},
     "mixed", "weak",
     ["foreign_travel", "spirituality"],
     ["venus", "saturn", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.23 v.19",
     "Venus-Saturn conjunction in 12th house: settlement abroad, finds "
     "beauty in foreign cultures, artistic pursuits in distant lands"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("venus_saturn", "conjunction_condition", "venus_sign_taurus", {},
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["venus", "saturn", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.23 v.20",
     "Venus-Saturn conjunction in Taurus (Venus's own sign): refined "
     "discipline, beauty with substance, steady accumulation of luxury"),
    ("venus_saturn", "conjunction_condition", "venus_sign_libra", {},
     "favorable", "strong",
     ["marriage", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "own_sign", "libra", "exaltation"],
     "Ch.23 v.21",
     "Venus-Saturn conjunction in Libra (both strong — Venus own, Saturn "
     "exalted): balanced artistic mastery, harmonious discipline, peak results"),
    ("venus_saturn", "conjunction_condition", "saturn_sign_capricorn", {},
     "mixed", "strong",
     ["career_status", "wealth"],
     ["venus", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.23 v.22",
     "Venus-Saturn conjunction in Capricorn (Saturn's own sign): austere "
     "beauty, discipline dominates luxury, career over romance"),
    ("venus_saturn", "conjunction_condition", "saturn_sign_aquarius", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.23 v.23",
     "Venus-Saturn conjunction in Aquarius (Saturn's own sign): austere "
     "beauty, humanitarian aesthetics, unconventional artistic expression"),
    ("venus_saturn", "conjunction_condition", "debilitated_venus_virgo", {},
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["venus", "saturn", "conjunction", "saravali", "debilitation", "virgo"],
     "Ch.23 v.24",
     "Venus-Saturn conjunction in Virgo (Venus debilitated): over-critical "
     "in love, beauty suppressed by perfectionism, delayed prosperity"),
    ("venus_saturn", "conjunction_condition", "debilitated_saturn_aries", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "debilitation", "aries"],
     "Ch.23 v.25",
     "Venus-Saturn conjunction in Aries (Saturn debilitated): impulsive "
     "restrictions, frustrated desire, discipline breaks down under pressure"),
    ("venus_saturn", "conjunction_condition", "jupiter_aspect_blessing", {},
     "favorable", "moderate",
     ["marriage", "wealth"],
     ["venus", "saturn", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.23 v.26",
     "Venus-Saturn conjunction aspected by Jupiter: blessed patience, "
     "divine grace eases delays, eventual happiness in marriage and wealth"),
    ("venus_saturn", "conjunction_condition", "mars_aspect_frustration", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "mars_aspect"],
     "Ch.23 v.27",
     "Venus-Saturn conjunction aspected by Mars: frustrated desire, "
     "passionate conflicts in relationships, anger from denied pleasures"),
    ("venus_saturn", "conjunction_condition", "mercury_aspect_skill", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["venus", "saturn", "conjunction", "saravali", "mercury_aspect"],
     "Ch.23 v.28",
     "Venus-Saturn conjunction aspected by Mercury: skilled in detailed "
     "artistic work, commercial success in luxury crafts, analytical beauty"),
    ("venus_saturn", "conjunction_condition", "kendra_placement", {},
     "mixed", "moderate",
     ["career_status", "marriage"],
     ["venus", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.23 v.29",
     "Venus-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "gives prominence to artistic discipline, public recognition"),
    ("venus_saturn", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["wealth", "spirituality"],
     ["venus", "saturn", "conjunction", "saravali", "trikona"],
     "Ch.23 v.30",
     "Venus-Saturn conjunction in any trikona (1/5/9): dharmic beauty, "
     "artistic merit brings fortune, disciplined devotion rewarded"),
    ("venus_saturn", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["venus", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.23 v.31",
     "Venus-Saturn conjunction in any dusthana (6/8/12): chronic ailments "
     "of reproductive system, marital misery, beauty fades through hardship"),
    ("venus_saturn", "conjunction_condition", "late_marriage_indicator", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["venus", "saturn", "conjunction", "saravali", "late_marriage"],
     "Ch.23 v.32",
     "Venus-Saturn conjunction as late marriage indicator: general principle — "
     "marriage delayed beyond normal age, partner older or mature"),
    ("venus_saturn", "conjunction_condition", "artistic_mastery", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["venus", "saturn", "conjunction", "saravali", "art", "mastery"],
     "Ch.23 v.33",
     "Venus-Saturn conjunction well-placed: mastery in arts requiring "
     "patience — sculpture, architecture, classical music, fine crafts"),
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
        ))
        num += 1
    return rules


def _build_all_rules() -> list[RuleRecord]:
    jupiter_venus = _make_conjunction_rules(
        "jupiter_venus", ["jupiter", "venus"], _JUPITER_VENUS_DATA, 781, "Ch.21-22",
    )
    jupiter_saturn = _make_conjunction_rules(
        "jupiter_saturn", ["jupiter", "saturn"], _JUPITER_SATURN_DATA, 824, "Ch.22",
    )
    venus_saturn = _make_conjunction_rules(
        "venus_saturn", ["venus", "saturn"], _VENUS_SATURN_DATA, 867, "Ch.22-23",
    )
    return jupiter_venus + jupiter_saturn + venus_saturn


SARAVALI_CONJUNCTIONS_7_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_7_REGISTRY.add(_rule)
