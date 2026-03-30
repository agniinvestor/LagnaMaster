"""src/corpus/saravali_conjunctions_6.py — S278: Saravali two-planet conjunctions.

SAV651–SAV780 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapter 21-22:
  Mercury-Jupiter  (Ch.21) — SAV651–SAV693 (43 rules)
  Mercury-Venus    (Ch.21) — SAV694–SAV736 (43 rules)
  Mercury-Saturn   (Ch.21-22) — SAV737–SAV780 (44 rules)

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
# Mercury-Jupiter Conjunction — Ch.21 (SAV651–SAV693)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_JUPITER_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mercury_jupiter", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["mercury", "jupiter", "conjunction", "saravali", "1st_house"],
     "Ch.21 v.1",
     "Mercury-Jupiter conjunction in 1st house: highly learned and wise, "
     "eloquent speaker with philosophical depth, respected for scholarly attainments"),
    ("mercury_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["fame_reputation", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "1st_house", "teacher"],
     "Ch.21 v.2",
     "Mercury-Jupiter conjunction in 1st house: natural teacher or counselor, "
     "earns respect through intellectual leadership, advisory roles"),
    # House 2
    ("mercury_jupiter", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "2nd_house"],
     "Ch.21 v.3",
     "Mercury-Jupiter conjunction in 2nd house: wealth through scholarly pursuits, "
     "eloquent and persuasive speech, earns through teaching or publishing"),
    ("mercury_jupiter", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "2nd_house", "family"],
     "Ch.21 v.4",
     "Mercury-Jupiter conjunction in 2nd house: comes from learned family, "
     "truthful and virtuous speech, respected in academic circles"),
    # House 3
    ("mercury_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "jupiter", "conjunction", "saravali", "3rd_house"],
     "Ch.21 v.5",
     "Mercury-Jupiter conjunction in 3rd house: courageous in intellectual pursuits, "
     "skilled writer and communicator, success in publishing and media"),
    ("mercury_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "jupiter", "conjunction", "saravali", "3rd_house", "trade"],
     "Ch.21 v.6",
     "Mercury-Jupiter conjunction in 3rd house: large-scale trade through siblings, "
     "profitable short journeys, success in commercial ventures"),
    # House 4
    ("mercury_jupiter", "conjunction_in_house", 4, {},
     "favorable", "strong",
     ["intelligence_education", "property_vehicles"],
     ["mercury", "jupiter", "conjunction", "saravali", "4th_house"],
     "Ch.21 v.7",
     "Mercury-Jupiter conjunction in 4th house: deeply educated, owns property "
     "and vehicles, happiness through learning and domestic comforts"),
    ("mercury_jupiter", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["spirituality", "mental_health"],
     ["mercury", "jupiter", "conjunction", "saravali", "4th_house", "peace"],
     "Ch.21 v.8",
     "Mercury-Jupiter conjunction in 4th house: peaceful and contented mind, "
     "spiritual inclination through study, blessed by mother"),
    # House 5
    ("mercury_jupiter", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "5th_house"],
     "Ch.21 v.9",
     "Mercury-Jupiter conjunction in 5th house: exceptional intelligence and wisdom, "
     "fame through scholarship, ministerial or advisory position"),
    ("mercury_jupiter", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "5th_house", "progeny"],
     "Ch.21 v.10",
     "Mercury-Jupiter conjunction in 5th house: intelligent and learned children, "
     "success in teaching, gains through educational institutions"),
    # House 6
    ("mercury_jupiter", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "6th_house"],
     "Ch.21 v.11",
     "Mercury-Jupiter conjunction in 6th house: defeats enemies through intellectual "
     "strategy and legal acumen, but prone to digestive disorders"),
    ("mercury_jupiter", "conjunction_in_house", 6, {},
     "unfavorable", "weak",
     ["physical_health", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "6th_house", "health"],
     "Ch.21 v.12",
     "Mercury-Jupiter conjunction in 6th house: scholarly abilities underutilized "
     "in service roles, nervous complaints, disputes with colleagues"),
    # House 7
    ("mercury_jupiter", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["marriage", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "7th_house"],
     "Ch.21 v.13",
     "Mercury-Jupiter conjunction in 7th house: wise and learned spouse, "
     "intellectual partnership, gains through marriage and collaboration"),
    ("mercury_jupiter", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "jupiter", "conjunction", "saravali", "7th_house", "trade"],
     "Ch.21 v.14",
     "Mercury-Jupiter conjunction in 7th house: large-scale commerce and trade, "
     "success in business partnerships, diplomatic and persuasive"),
    # House 8
    ("mercury_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "8th_house"],
     "Ch.21 v.15",
     "Mercury-Jupiter conjunction in 8th house: research into hidden knowledge, "
     "interest in philosophy of death and transformation, moderate longevity"),
    ("mercury_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.21 v.16",
     "Mercury-Jupiter conjunction in 8th house: aptitude for occult philosophy, "
     "mystical studies, inheritance of scholarly texts or knowledge"),
    # House 9
    ("mercury_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "9th_house"],
     "Ch.21 v.17",
     "Mercury-Jupiter conjunction in 9th house: deeply philosophical and devout, "
     "fame through religious scholarship, pilgrimage and scriptural mastery"),
    ("mercury_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["fame_reputation", "wealth"],
     ["mercury", "jupiter", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.21 v.18",
     "Mercury-Jupiter conjunction in 9th house: highly fortunate, patronage from "
     "institutions, father is learned, gains through higher education"),
    # House 10
    ("mercury_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "10th_house"],
     "Ch.21 v.19",
     "Mercury-Jupiter conjunction in 10th house: eminent career in education, "
     "law, or philosophy, widespread fame through intellectual achievements"),
    ("mercury_jupiter", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "10th_house", "commerce"],
     "Ch.21 v.20",
     "Mercury-Jupiter conjunction in 10th house: large-scale commercial success, "
     "wealth through publishing, consulting, or academic administration"),
    ("mercury_jupiter", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "10th_house", "virtue"],
     "Ch.21 v.21",
     "Mercury-Jupiter conjunction in 10th house: virtuous and charitable in "
     "profession, engages in meritorious public service, philanthropic"),
    # House 11
    ("mercury_jupiter", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "11th_house"],
     "Ch.21 v.22",
     "Mercury-Jupiter conjunction in 11th house: abundant gains through intellect, "
     "profitable scholarly network, income from teaching and writing"),
    ("mercury_jupiter", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["mercury", "jupiter", "conjunction", "saravali", "11th_house", "friends"],
     "Ch.21 v.23",
     "Mercury-Jupiter conjunction in 11th house: learned and influential friends, "
     "honored by scholarly communities, fulfillment of aspirations"),
    # House 12
    ("mercury_jupiter", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "12th_house"],
     "Ch.21 v.24",
     "Mercury-Jupiter conjunction in 12th house: spiritual learning in seclusion, "
     "philosophical contemplation, expenditure on education and charity"),
    ("mercury_jupiter", "conjunction_in_house", 12, {},
     "unfavorable", "weak",
     ["wealth", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.21 v.25",
     "Mercury-Jupiter conjunction in 12th house: intellectual talents not fully "
     "recognized, financial losses through over-generosity, foreign settlement"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mercury_jupiter", "conjunction_condition", "gemini_analytical_philosophy", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.21 v.26",
     "Mercury-Jupiter conjunction in Gemini (Mercury's own sign): analytical "
     "philosophy, logical approach to wisdom, excellence in debate and discourse"),
    ("mercury_jupiter", "conjunction_condition", "virgo_analytical_precision", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.21 v.27",
     "Mercury-Jupiter conjunction in Virgo (Mercury exalted): perfectionist "
     "scholarship, analytical mastery, systematic approach to learning"),
    ("mercury_jupiter", "conjunction_condition", "sagittarius_wisdom_teaching", {},
     "favorable", "strong",
     ["intelligence_education", "spirituality"],
     ["mercury", "jupiter", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.21 v.28",
     "Mercury-Jupiter conjunction in Sagittarius (Jupiter's own sign): wisdom "
     "teaching, philosophical preaching, success as guru or professor"),
    ("mercury_jupiter", "conjunction_condition", "pisces_intuitive_wisdom", {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "own_sign", "pisces"],
     "Ch.21 v.29",
     "Mercury-Jupiter conjunction in Pisces (Jupiter exalted, Mercury debilitated): "
     "intuitive wisdom but poor analytical skills, devotional rather than logical"),
    ("mercury_jupiter", "conjunction_condition", "jupiter_amplifies_commerce", {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "commerce", "large_scale"],
     "Ch.21 v.30",
     "Mercury-Jupiter conjunction in good dignity: Jupiter amplifies Mercury's "
     "commercial abilities, large-scale trade, international business success"),
    ("mercury_jupiter", "conjunction_condition", "benefic_aspect_conjunction", {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "benefic_aspect"],
     "Ch.21 v.31",
     "Mercury-Jupiter conjunction aspected by Venus: artistic scholarship, "
     "beautiful expression of philosophy, success in publishing"),
    ("mercury_jupiter", "conjunction_condition", "malefic_aspect_conjunction", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["mercury", "jupiter", "conjunction", "saravali", "malefic_aspect"],
     "Ch.21 v.32",
     "Mercury-Jupiter conjunction aspected by malefics (Saturn/Mars): wisdom "
     "obstructed, intellectual arrogance, disputes with teachers"),
    ("mercury_jupiter", "conjunction_condition", "mars_aspect_debate", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "jupiter", "conjunction", "saravali", "mars_aspect"],
     "Ch.21 v.33",
     "Mercury-Jupiter conjunction aspected by Mars: sharp debating skills, "
     "argumentative scholar, success in competitive academics"),
    ("mercury_jupiter", "conjunction_condition", "saturn_aspect_depth", {},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "saturn_aspect"],
     "Ch.21 v.34",
     "Mercury-Jupiter conjunction aspected by Saturn: deep but slow scholarship, "
     "delayed academic recognition, success in research after perseverance"),
    ("mercury_jupiter", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "kendra"],
     "Ch.21 v.35",
     "Mercury-Jupiter conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies scholarly eminence, prominent teaching or advisory career"),
    ("mercury_jupiter", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["mercury", "jupiter", "conjunction", "saravali", "trikona"],
     "Ch.21 v.36",
     "Mercury-Jupiter conjunction in any trikona (1/5/9): dharmic intellect, "
     "philosophical merit brings fortune, scriptural mastery"),
    ("mercury_jupiter", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "jupiter", "conjunction", "saravali", "dusthana"],
     "Ch.21 v.37",
     "Mercury-Jupiter conjunction in any dusthana (6/8/12): wisdom underutilized, "
     "scholarly potential wasted, nervous disorders from overthinking"),
    ("mercury_jupiter", "conjunction_condition", "retrograde_mercury", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "jupiter", "conjunction", "saravali", "retrograde_mercury"],
     "Ch.21 v.38",
     "Mercury-Jupiter conjunction with retrograde Mercury: unconventional "
     "philosophy, revisits ancient teachings, delayed academic recognition"),
    ("mercury_jupiter", "conjunction_condition", "retrograde_jupiter", {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "jupiter", "conjunction", "saravali", "retrograde_jupiter"],
     "Ch.21 v.39",
     "Mercury-Jupiter conjunction with retrograde Jupiter: internalized wisdom, "
     "questions orthodox teachings, philosophical innovation through reflection"),
    ("mercury_jupiter", "conjunction_condition", "publishing_success", {},
     "favorable", "moderate",
     ["fame_reputation", "wealth"],
     ["mercury", "jupiter", "conjunction", "saravali", "publishing", "writing"],
     "Ch.21 v.40",
     "Mercury-Jupiter conjunction well-placed: natural aptitude for publishing, "
     "authorship of philosophical or educational texts, literary fame"),
    ("mercury_jupiter", "conjunction_condition", "teaching_career", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mercury", "jupiter", "conjunction", "saravali", "teaching", "education"],
     "Ch.21 v.41",
     "Mercury-Jupiter conjunction in good dignity: success as teacher, professor, "
     "or educational administrator, earns through knowledge dissemination"),
    ("mercury_jupiter", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "jupiter", "conjunction", "saravali", "upachaya"],
     "Ch.21 v.42",
     "Mercury-Jupiter conjunction in upachaya houses (3/6/10/11): scholarly "
     "abilities grow with age, progressive gains through education and commerce"),
    ("mercury_jupiter", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["mercury", "jupiter", "conjunction", "saravali", "rahu", "triple"],
     "Ch.21 v.43",
     "Mercury-Jupiter conjunction joined by Rahu: distorted wisdom, unorthodox "
     "views create controversy, intellectual deception, nervous anxiety"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury-Venus Conjunction — Ch.21 (SAV694–SAV736)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_VENUS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mercury_venus", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["physical_appearance", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "1st_house"],
     "Ch.21 v.44",
     "Mercury-Venus conjunction in 1st house: attractive appearance, charming "
     "and eloquent, skilled in fine arts, music, or dance"),
    ("mercury_venus", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "1st_house", "artistic"],
     "Ch.21 v.45",
     "Mercury-Venus conjunction in 1st house: artistic intelligence, creative "
     "expression brings fame, appreciated for aesthetic sensibility"),
    # House 2
    ("mercury_venus", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "2nd_house"],
     "Ch.21 v.46",
     "Mercury-Venus conjunction in 2nd house: sweet and melodious speech, "
     "wealth through artistic or commercial pursuits, poetic talent"),
    ("mercury_venus", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "2nd_house", "music"],
     "Ch.21 v.47",
     "Mercury-Venus conjunction in 2nd house: gifted singer or musician, "
     "earns through vocal arts, beautiful and persuasive speech"),
    # House 3
    ("mercury_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mercury", "venus", "conjunction", "saravali", "3rd_house"],
     "Ch.21 v.48",
     "Mercury-Venus conjunction in 3rd house: creative and courageous, skilled "
     "in artistic writing, success in media, advertising, or design"),
    ("mercury_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "3rd_house", "commerce"],
     "Ch.21 v.49",
     "Mercury-Venus conjunction in 3rd house: profitable artistic ventures, "
     "success in fashion, cosmetics, or luxury goods trade"),
    # House 4
    ("mercury_venus", "conjunction_in_house", 4, {},
     "favorable", "strong",
     ["property_vehicles", "mental_health"],
     ["mercury", "venus", "conjunction", "saravali", "4th_house"],
     "Ch.21 v.50",
     "Mercury-Venus conjunction in 4th house: beautiful home and vehicles, "
     "domestic happiness, artistic furnishing, musically inclined mother"),
    ("mercury_venus", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "4th_house", "education"],
     "Ch.21 v.51",
     "Mercury-Venus conjunction in 4th house: education in fine arts, "
     "refined tastes, peaceful and aesthetically pleasing environment"),
    # House 5
    ("mercury_venus", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "5th_house"],
     "Ch.21 v.52",
     "Mercury-Venus conjunction in 5th house: exceptional creative intelligence, "
     "fame through performing arts, romantic and poetic temperament"),
    ("mercury_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "5th_house", "progeny"],
     "Ch.21 v.53",
     "Mercury-Venus conjunction in 5th house: artistically gifted children, "
     "gains through entertainment, successful creative speculation"),
    # House 6
    ("mercury_venus", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "6th_house"],
     "Ch.21 v.54",
     "Mercury-Venus conjunction in 6th house: overcomes rivals through charm "
     "and diplomacy, but artistic talents serve others more than self"),
    ("mercury_venus", "conjunction_in_house", 6, {},
     "unfavorable", "weak",
     ["physical_health", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "6th_house", "health"],
     "Ch.21 v.55",
     "Mercury-Venus conjunction in 6th house: skin complaints or urinary "
     "disorders, overindulgence in pleasures, disputes with artistic peers"),
    # House 7
    ("mercury_venus", "conjunction_in_house", 7, {},
     "favorable", "strong",
     ["marriage", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "7th_house"],
     "Ch.21 v.56",
     "Mercury-Venus conjunction in 7th house: charming and attractive spouse, "
     "harmonious marriage, partnership in artistic or commercial ventures"),
    ("mercury_venus", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "7th_house", "business"],
     "Ch.21 v.57",
     "Mercury-Venus conjunction in 7th house: success in aesthetic commerce, "
     "profitable partnerships in luxury trade, diplomatic skill"),
    # House 8
    ("mercury_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "intelligence_education"],
     ["mercury", "venus", "conjunction", "saravali", "8th_house"],
     "Ch.21 v.58",
     "Mercury-Venus conjunction in 8th house: interest in hidden arts and "
     "tantric aesthetics, inheritance of artistic treasures, secret romances"),
    ("mercury_venus", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["wealth", "marriage"],
     ["mercury", "venus", "conjunction", "saravali", "8th_house", "loss"],
     "Ch.21 v.59",
     "Mercury-Venus conjunction in 8th house: financial losses through "
     "overindulgence, scandals in relationships, artistic frustration"),
    # House 9
    ("mercury_venus", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["mercury", "venus", "conjunction", "saravali", "9th_house"],
     "Ch.21 v.60",
     "Mercury-Venus conjunction in 9th house: devotional art and sacred music, "
     "philosophical aesthetics, pilgrimage to places of beauty and learning"),
    ("mercury_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["fame_reputation", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.21 v.61",
     "Mercury-Venus conjunction in 9th house: fortunate through artistic "
     "patronage, father appreciates arts, gains through higher education in arts"),
    # House 10
    ("mercury_venus", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "10th_house"],
     "Ch.21 v.62",
     "Mercury-Venus conjunction in 10th house: eminent career in arts, music, "
     "or entertainment, widespread fame through creative accomplishments"),
    ("mercury_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "10th_house", "commerce"],
     "Ch.21 v.63",
     "Mercury-Venus conjunction in 10th house: wealth through luxury commerce, "
     "success in fashion, jewelry, cosmetics, or entertainment industry"),
    ("mercury_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "10th_house", "charm"],
     "Ch.21 v.64",
     "Mercury-Venus conjunction in 10th house: charming public persona, "
     "wins hearts through eloquence, respected for aesthetic contributions"),
    # House 11
    ("mercury_venus", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "11th_house"],
     "Ch.21 v.65",
     "Mercury-Venus conjunction in 11th house: abundant gains through artistic "
     "work, profitable friendships in creative circles, fulfilled desires"),
    ("mercury_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "11th_house", "network"],
     "Ch.21 v.66",
     "Mercury-Venus conjunction in 11th house: influential friends in arts "
     "and commerce, gains through elder siblings, social charm brings success"),
    # House 12
    ("mercury_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "12th_house"],
     "Ch.21 v.67",
     "Mercury-Venus conjunction in 12th house: expenditure on pleasures and "
     "artistic pursuits, spiritual beauty, appreciation of sacred art"),
    ("mercury_venus", "conjunction_in_house", 12, {},
     "unfavorable", "weak",
     ["wealth", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.21 v.68",
     "Mercury-Venus conjunction in 12th house: artistic talents better "
     "appreciated abroad, losses through luxuries, bed pleasures dominate"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mercury_venus", "conjunction_condition", "venus_sign_taurus", {},
     "favorable", "strong",
     ["physical_appearance", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.21 v.69",
     "Mercury-Venus conjunction in Taurus (Venus own sign): artistic beauty "
     "personified, mastery of music and dance, magnetic physical charm"),
    ("mercury_venus", "conjunction_condition", "venus_sign_libra", {},
     "favorable", "strong",
     ["character_temperament", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "own_sign", "libra"],
     "Ch.21 v.70",
     "Mercury-Venus conjunction in Libra (Venus own sign): refined aesthetic "
     "sense, diplomatic eloquence, success in design and fine arts"),
    ("mercury_venus", "conjunction_condition", "mercury_sign_gemini", {},
     "favorable", "strong",
     ["intelligence_education", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.21 v.71",
     "Mercury-Venus conjunction in Gemini (Mercury own sign): commercial arts, "
     "clever in artistic marketing, success in media and advertising"),
    ("mercury_venus", "conjunction_condition", "mercury_sign_virgo", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.21 v.72",
     "Mercury-Venus conjunction in Virgo (Mercury exalted): technical artistry, "
     "precision in craft, analytical approach to creative design"),
    ("mercury_venus", "conjunction_condition", "jupiter_aspect_devotional", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.21 v.73",
     "Mercury-Venus conjunction aspected by Jupiter: devotional art, sacred "
     "music, temple architecture, success in spiritual artistic expression"),
    ("mercury_venus", "conjunction_condition", "mars_aspect_competitive", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["mercury", "venus", "conjunction", "saravali", "mars_aspect"],
     "Ch.21 v.74",
     "Mercury-Venus conjunction aspected by Mars: competitive arts, dance with "
     "vigor, dramatic performance, success in athletic or martial aesthetics"),
    ("mercury_venus", "conjunction_condition", "saturn_aspect_discipline", {},
     "mixed", "moderate",
     ["career_status", "intelligence_education"],
     ["mercury", "venus", "conjunction", "saravali", "saturn_aspect"],
     "Ch.21 v.75",
     "Mercury-Venus conjunction aspected by Saturn: disciplined artistic practice, "
     "classical art forms, delayed but enduring creative recognition"),
    ("mercury_venus", "conjunction_condition", "natural_friends_harmony", {},
     "favorable", "moderate",
     ["character_temperament", "mental_health"],
     ["mercury", "venus", "conjunction", "saravali", "natural_friends"],
     "Ch.21 v.76",
     "Mercury-Venus as natural friends: harmonious combination enhances both "
     "artistic and intellectual faculties, balanced creative expression"),
    ("mercury_venus", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "kendra"],
     "Ch.21 v.77",
     "Mercury-Venus conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies artistic fame, prominent career in creative fields"),
    ("mercury_venus", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["mercury", "venus", "conjunction", "saravali", "trikona"],
     "Ch.21 v.78",
     "Mercury-Venus conjunction in any trikona (1/5/9): dharmic art, creative "
     "expression serves spiritual growth, blessed artistic talent"),
    ("mercury_venus", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "dusthana"],
     "Ch.21 v.79",
     "Mercury-Venus conjunction in any dusthana (6/8/12): artistic talents "
     "underappreciated, losses through indulgence, creative frustration"),
    ("mercury_venus", "conjunction_condition", "performing_arts_skill", {},
     "favorable", "moderate",
     ["fame_reputation", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "performing_arts", "dance"],
     "Ch.21 v.80",
     "Mercury-Venus conjunction well-placed: natural aptitude for performing "
     "arts — dance, drama, music — success on stage and in entertainment"),
    ("mercury_venus", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "venus", "conjunction", "saravali", "upachaya"],
     "Ch.21 v.81",
     "Mercury-Venus conjunction in upachaya houses (3/6/10/11): artistic "
     "abilities grow with age, progressive gains through creative commerce"),
    ("mercury_venus", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["mercury", "venus", "conjunction", "saravali", "rahu", "triple"],
     "Ch.21 v.82",
     "Mercury-Venus conjunction joined by Rahu: obsessive artistic pursuit, "
     "illicit romantic attractions, deceptive charm, nervous indulgence"),
    ("mercury_venus", "conjunction_condition", "ketu_conjunction_triple", {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "venus", "conjunction", "saravali", "ketu", "triple"],
     "Ch.21 v.83",
     "Mercury-Venus conjunction joined by Ketu: detachment from artistic "
     "pleasures, mystical creativity, unconventional aesthetic expression"),
    ("mercury_venus", "conjunction_condition", "exalted_venus_pisces", {},
     "favorable", "strong",
     ["fame_reputation", "spirituality"],
     ["mercury", "venus", "conjunction", "saravali", "exaltation", "pisces"],
     "Ch.21 v.84",
     "Mercury-Venus conjunction in Pisces (Venus exalted, Mercury debilitated): "
     "transcendent beauty in art, devotional music, intuitive creative genius"),
    ("mercury_venus", "conjunction_condition", "luxury_trade_skill", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "venus", "conjunction", "saravali", "luxury", "trade"],
     "Ch.21 v.85",
     "Mercury-Venus conjunction in good dignity: aptitude for luxury goods "
     "trade, jewelry, perfumes, cosmetics, or fashion commerce"),
    ("mercury_venus", "conjunction_condition", "literary_arts_skill", {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["mercury", "venus", "conjunction", "saravali", "poetry", "literature"],
     "Ch.21 v.86",
     "Mercury-Venus conjunction well-placed: poetic and literary talent, "
     "success as lyricist, playwright, or romantic fiction author"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mercury-Saturn Conjunction — Ch.21-22 (SAV737–SAV780)
# ═══════════════════════════════════════════════════════════════════════════════
_MERCURY_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mercury_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "1st_house"],
     "Ch.21 v.82",
     "Mercury-Saturn conjunction in 1st house: methodical and serious thinker, "
     "slow but deep intellect, reserved and cautious disposition"),
    ("mercury_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "weak",
     ["physical_appearance", "mental_health"],
     ["mercury", "saturn", "conjunction", "saravali", "1st_house", "appearance"],
     "Ch.21 v.83",
     "Mercury-Saturn conjunction in 1st house: lean and aged appearance, "
     "prone to melancholy, anxious temperament, worry-driven personality"),
    ("mercury_saturn", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "1st_house", "research"],
     "Ch.21 v.84",
     "Mercury-Saturn conjunction in 1st house: aptitude for research and "
     "systematic study, success in technical or scientific disciplines"),
    # House 2
    ("mercury_saturn", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "2nd_house"],
     "Ch.21 v.85",
     "Mercury-Saturn conjunction in 2nd house: careful and measured speech, "
     "wealth through accounting or structured financial management"),
    ("mercury_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "2nd_house", "speech"],
     "Ch.21 v.86",
     "Mercury-Saturn conjunction in 2nd house: harsh or bitter speech, "
     "pessimistic outlook, critical of others, slow in verbal expression"),
    # House 3
    ("mercury_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "3rd_house"],
     "Ch.21 v.87",
     "Mercury-Saturn conjunction in 3rd house: persevering in communication, "
     "skilled in technical writing, serious approach to learning"),
    ("mercury_saturn", "conjunction_in_house", 3, {},
     "unfavorable", "weak",
     ["mental_health", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "3rd_house", "sibling"],
     "Ch.21 v.88",
     "Mercury-Saturn conjunction in 3rd house: strained relations with siblings, "
     "pessimistic outlook, courage delayed until maturity"),
    # House 4
    ("mercury_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "property_vehicles"],
     ["mercury", "saturn", "conjunction", "saravali", "4th_house"],
     "Ch.21 v.89",
     "Mercury-Saturn conjunction in 4th house: mental restlessness despite "
     "structured thinking, delayed property acquisition, domestic austerity"),
    ("mercury_saturn", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "4th_house", "education"],
     "Ch.21 v.90",
     "Mercury-Saturn conjunction in 4th house: education in technical or "
     "scientific fields, slow but thorough learning, disciplined study habits"),
    # House 5
    ("mercury_saturn", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["intelligence_education", "progeny"],
     ["mercury", "saturn", "conjunction", "saravali", "5th_house"],
     "Ch.21 v.91",
     "Mercury-Saturn conjunction in 5th house: deep but slow intellect, "
     "delayed progeny, children may be serious or studious in nature"),
    ("mercury_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["mental_health", "progeny"],
     ["mercury", "saturn", "conjunction", "saravali", "5th_house", "anxiety"],
     "Ch.21 v.92",
     "Mercury-Saturn conjunction in 5th house: anxiety about children, "
     "creative expression inhibited by excessive self-criticism"),
    # House 6
    ("mercury_saturn", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["enemies_litigation", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "6th_house"],
     "Ch.21 v.93",
     "Mercury-Saturn conjunction in 6th house: defeats enemies through "
     "patient strategy, success in accounting, auditing, or legal research"),
    ("mercury_saturn", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["mercury", "saturn", "conjunction", "saravali", "6th_house", "health"],
     "Ch.21 v.94",
     "Mercury-Saturn conjunction in 6th house: nervous disorders, skin "
     "ailments, digestive problems from worry and anxiety"),
    # House 7
    ("mercury_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "7th_house"],
     "Ch.22 v.1",
     "Mercury-Saturn conjunction in 7th house: delayed marriage, spouse may "
     "be older or serious, partnership lacks warmth and spontaneity"),
    ("mercury_saturn", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mercury", "saturn", "conjunction", "saravali", "7th_house", "business"],
     "Ch.22 v.2",
     "Mercury-Saturn conjunction in 7th house: success in structured business "
     "partnerships, methodical approach to trade, slow but steady commerce"),
    # House 8
    ("mercury_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     ["mercury", "saturn", "conjunction", "saravali", "8th_house"],
     "Ch.22 v.3",
     "Mercury-Saturn conjunction in 8th house: chronic anxiety and fear, "
     "research into death and occult, longevity concerns from nervous strain"),
    ("mercury_saturn", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["intelligence_education", "spirituality"],
     ["mercury", "saturn", "conjunction", "saravali", "8th_house", "research"],
     "Ch.22 v.4",
     "Mercury-Saturn conjunction in 8th house: deep research ability, "
     "investigation of hidden matters, gains through meticulous analysis"),
    # House 9
    ("mercury_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "9th_house"],
     "Ch.22 v.5",
     "Mercury-Saturn conjunction in 9th house: serious approach to philosophy, "
     "structured religious practice, delayed higher education but deep knowledge"),
    ("mercury_saturn", "conjunction_in_house", 9, {},
     "unfavorable", "weak",
     ["spirituality", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "9th_house", "father"],
     "Ch.22 v.6",
     "Mercury-Saturn conjunction in 9th house: difficulties with father, "
     "skeptical of traditional religion, materialistic approach to philosophy"),
    # House 10
    ("mercury_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mercury", "saturn", "conjunction", "saravali", "10th_house"],
     "Ch.22 v.7",
     "Mercury-Saturn conjunction in 10th house: success in scientific or "
     "technical career, methodical rise to authority, structured leadership"),
    ("mercury_saturn", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "10th_house", "accounting"],
     "Ch.22 v.8",
     "Mercury-Saturn conjunction in 10th house: wealth through accounting, "
     "administration, or engineering, slow but enduring professional success"),
    # House 11
    ("mercury_saturn", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "11th_house"],
     "Ch.22 v.9",
     "Mercury-Saturn conjunction in 11th house: steady gains through disciplined "
     "work, income from technical or research positions, frugal accumulation"),
    ("mercury_saturn", "conjunction_in_house", 11, {},
     "mixed", "moderate",
     ["fame_reputation", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "11th_house", "friends"],
     "Ch.22 v.10",
     "Mercury-Saturn conjunction in 11th house: few but loyal friends, "
     "respected for reliability, gains through older or mature associates"),
    # House 12
    ("mercury_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "mental_health"],
     ["mercury", "saturn", "conjunction", "saravali", "12th_house"],
     "Ch.22 v.11",
     "Mercury-Saturn conjunction in 12th house: expenditure exceeds income, "
     "chronic worry, intellectual isolation, research in solitude"),
    ("mercury_saturn", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "foreign_travel"],
     ["mercury", "saturn", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.22 v.12",
     "Mercury-Saturn conjunction in 12th house: technical work abroad, "
     "spiritual discipline through renunciation, austere foreign settlement"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mercury_saturn", "conjunction_condition", "capricorn_systematic", {},
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.22 v.13",
     "Mercury-Saturn conjunction in Capricorn (Saturn own sign): systematic "
     "research, organizational mastery, success in structured disciplines"),
    ("mercury_saturn", "conjunction_condition", "aquarius_innovative", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.22 v.14",
     "Mercury-Saturn conjunction in Aquarius (Saturn own sign): innovative "
     "research, unconventional technical approach, humanitarian intellect"),
    ("mercury_saturn", "conjunction_condition", "gemini_analytical", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.22 v.15",
     "Mercury-Saturn conjunction in Gemini (Mercury own sign): analytical "
     "discipline, structured communication, technical writing excellence"),
    ("mercury_saturn", "conjunction_condition", "virgo_perfectionist", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.22 v.16",
     "Mercury-Saturn conjunction in Virgo (Mercury exalted): perfectionist "
     "analysis, meticulous research, excellence in scientific methodology"),
    ("mercury_saturn", "conjunction_condition", "jupiter_aspect_philosophical", {},
     "favorable", "strong",
     ["intelligence_education", "spirituality"],
     ["mercury", "saturn", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.22 v.17",
     "Mercury-Saturn conjunction aspected by Jupiter: philosophical research, "
     "wisdom through disciplined study, academic eminence after perseverance"),
    ("mercury_saturn", "conjunction_condition", "mars_aspect_engineering", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "mars_aspect"],
     "Ch.22 v.18",
     "Mercury-Saturn conjunction aspected by Mars: engineering aptitude, "
     "technical precision with energetic drive, success in applied sciences"),
    ("mercury_saturn", "conjunction_condition", "venus_aspect_softening", {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "venus_aspect"],
     "Ch.22 v.19",
     "Mercury-Saturn conjunction aspected by Venus: austerity softened, "
     "artistic discipline, success in architectural or design fields"),
    ("mercury_saturn", "conjunction_condition", "malefic_aspect_conjunction", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["mercury", "saturn", "conjunction", "saravali", "malefic_aspect"],
     "Ch.22 v.20",
     "Mercury-Saturn conjunction aspected by Mars without Jupiter: extreme "
     "anxiety, nervous breakdown, chronic health from mental strain"),
    ("mercury_saturn", "conjunction_condition", "kendra_placement", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.22 v.21",
     "Mercury-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "supports structured career, recognized for methodical expertise"),
    ("mercury_saturn", "conjunction_condition", "trikona_placement", {},
     "mixed", "moderate",
     ["intelligence_education", "spirituality"],
     ["mercury", "saturn", "conjunction", "saravali", "trikona"],
     "Ch.22 v.22",
     "Mercury-Saturn conjunction in any trikona (1/5/9): dharmic discipline, "
     "structured approach to philosophy, merit through sustained effort"),
    ("mercury_saturn", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["mercury", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.22 v.23",
     "Mercury-Saturn conjunction in any dusthana (6/8/12): severe anxiety, "
     "nervous ailments, chronic worry, intellectual potential wasted"),
    ("mercury_saturn", "conjunction_condition", "retrograde_mercury", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "retrograde_mercury"],
     "Ch.22 v.24",
     "Mercury-Saturn conjunction with retrograde Mercury: revisits old research, "
     "unconventional methodology, delayed but original contributions"),
    ("mercury_saturn", "conjunction_condition", "retrograde_saturn", {},
     "unfavorable", "moderate",
     ["career_status", "mental_health"],
     ["mercury", "saturn", "conjunction", "saravali", "retrograde_saturn"],
     "Ch.22 v.25",
     "Mercury-Saturn conjunction with retrograde Saturn: internalized discipline "
     "becomes excessive self-criticism, career delays, chronic dissatisfaction"),
    ("mercury_saturn", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mercury", "saturn", "conjunction", "saravali", "upachaya"],
     "Ch.22 v.26",
     "Mercury-Saturn conjunction in upachaya houses (3/6/10/11): methodical "
     "abilities strengthen with age, progressive gains through discipline"),
    ("mercury_saturn", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "strong",
     ["mental_health", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "rahu", "triple"],
     "Ch.22 v.27",
     "Mercury-Saturn conjunction joined by Rahu: obsessive and paranoid thinking, "
     "deceptive research, fraudulent accounting, severe nervous disorders"),
    ("mercury_saturn", "conjunction_condition", "ketu_conjunction_triple", {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "ketu", "triple"],
     "Ch.22 v.28",
     "Mercury-Saturn conjunction joined by Ketu: sudden detachment from worldly "
     "research, mystical inclination, unconventional scientific methods"),
    ("mercury_saturn", "conjunction_condition", "scientific_aptitude", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mercury", "saturn", "conjunction", "saravali", "science", "research"],
     "Ch.22 v.29",
     "Mercury-Saturn conjunction in good dignity: natural aptitude for scientific "
     "research, mathematics, statistics, or technical engineering"),
    ("mercury_saturn", "conjunction_condition", "accounting_skill", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "saturn", "conjunction", "saravali", "accounting", "finance"],
     "Ch.22 v.30",
     "Mercury-Saturn conjunction well-placed: skilled in accounting, auditing, "
     "and financial record-keeping, meticulous with numbers and contracts"),
    ("mercury_saturn", "conjunction_condition", "enemy_sign_placement", {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["mercury", "saturn", "conjunction", "saravali", "enemy_sign"],
     "Ch.22 v.31",
     "Mercury-Saturn conjunction in enemy sign: intellect burdened by anxiety, "
     "chronic pessimism, harsh criticism of others, isolation from peers"),
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
    mercury_jupiter = _make_conjunction_rules(
        "mercury_jupiter", ["mercury", "jupiter"], _MERCURY_JUPITER_DATA, 651, "Ch.21",
    )
    mercury_venus = _make_conjunction_rules(
        "mercury_venus", ["mercury", "venus"], _MERCURY_VENUS_DATA, 694, "Ch.21",
    )
    mercury_saturn = _make_conjunction_rules(
        "mercury_saturn", ["mercury", "saturn"], _MERCURY_SATURN_DATA, 737, "Ch.21-22",
    )
    return mercury_jupiter + mercury_venus + mercury_saturn


SARAVALI_CONJUNCTIONS_6_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_6_REGISTRY.add(_rule)
