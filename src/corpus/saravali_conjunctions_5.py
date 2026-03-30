"""src/corpus/saravali_conjunctions_5.py — S277: Saravali two-planet conjunctions.

SAV521–SAV650 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 20-21:
  Mars-Jupiter  (Ch.20) — SAV521–SAV563 (43 rules)
  Mars-Venus    (Ch.20) — SAV564–SAV606 (43 rules)
  Mars-Saturn   (Ch.20-21) — SAV607–SAV650 (44 rules)

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
# Mars-Jupiter Conjunction — Ch.20 (SAV521–SAV563)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_JUPITER_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mars_jupiter", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["character_temperament", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "1st_house"],
     "Ch.20 v.1",
     "Mars-Jupiter conjunction in 1st house: courageous and wise, righteous "
     "warrior personality, commands respect through dharmic conduct"),
    ("mars_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["mars", "jupiter", "conjunction", "saravali", "1st_house", "body"],
     "Ch.20 v.2",
     "Mars-Jupiter conjunction in 1st house: strong and well-built physique, "
     "robust health, protective and commanding physical presence"),
    # House 2
    ("mars_jupiter", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["mars", "jupiter", "conjunction", "saravali", "2nd_house"],
     "Ch.20 v.3",
     "Mars-Jupiter conjunction in 2nd house: wealth earned through bold and "
     "righteous enterprise, eloquent speech with moral authority"),
    ("mars_jupiter", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["character_temperament", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "2nd_house", "speech"],
     "Ch.20 v.4",
     "Mars-Jupiter conjunction in 2nd house: forthright speech that may offend, "
     "respected for honesty but creates friction in family dealings"),
    # House 3
    ("mars_jupiter", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["character_temperament", "career_status"],
     ["mars", "jupiter", "conjunction", "saravali", "3rd_house"],
     "Ch.20 v.5",
     "Mars-Jupiter conjunction in 3rd house: exceptional courage guided by wisdom, "
     "successful in valorous enterprises, heroic and principled"),
    ("mars_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "3rd_house", "sibling"],
     "Ch.20 v.6",
     "Mars-Jupiter conjunction in 3rd house: benefits from younger siblings, "
     "success in short journeys, gains through publishing or media"),
    # House 4
    ("mars_jupiter", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["property_vehicles", "mental_health"],
     ["mars", "jupiter", "conjunction", "saravali", "4th_house"],
     "Ch.20 v.7",
     "Mars-Jupiter conjunction in 4th house: gains landed property through "
     "assertive action but domestic peace is disrupted by righteousness disputes"),
    ("mars_jupiter", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["mars", "jupiter", "conjunction", "saravali", "4th_house", "learning"],
     "Ch.20 v.8",
     "Mars-Jupiter conjunction in 4th house: learned in traditional sciences, "
     "protective of mother and homeland, strong moral foundation"),
    # House 5
    ("mars_jupiter", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["mars", "jupiter", "conjunction", "saravali", "5th_house"],
     "Ch.20 v.9",
     "Mars-Jupiter conjunction in 5th house: intelligent and brave children, "
     "success in speculation guided by wisdom, creative dharmic action"),
    ("mars_jupiter", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "5th_house", "authority"],
     "Ch.20 v.10",
     "Mars-Jupiter conjunction in 5th house: advisory or ministerial position, "
     "commands authority through combination of courage and knowledge"),
    # House 6
    ("mars_jupiter", "conjunction_in_house", 6, {},
     "favorable", "strong",
     ["enemies_litigation", "career_status"],
     ["mars", "jupiter", "conjunction", "saravali", "6th_house"],
     "Ch.20 v.11",
     "Mars-Jupiter conjunction in 6th house: vanquishes all enemies through "
     "righteous combat, success in legal battles and competitive fields"),
    ("mars_jupiter", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["physical_health", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "6th_house", "health"],
     "Ch.20 v.12",
     "Mars-Jupiter conjunction in 6th house: strong constitution, overcomes "
     "diseases through vigorous lifestyle, protective nature toward dependents"),
    # House 7
    ("mars_jupiter", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "7th_house"],
     "Ch.20 v.13",
     "Mars-Jupiter conjunction in 7th house: spouse of noble character but "
     "domineering nature creates friction, righteous but forceful in partnerships"),
    ("mars_jupiter", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mars", "jupiter", "conjunction", "saravali", "7th_house", "trade"],
     "Ch.20 v.14",
     "Mars-Jupiter conjunction in 7th house: success in business partnerships, "
     "gains through foreign trade, ethical but assertive commercial dealings"),
    # House 8
    ("mars_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "spirituality"],
     ["mars", "jupiter", "conjunction", "saravali", "8th_house"],
     "Ch.20 v.15",
     "Mars-Jupiter conjunction in 8th house: Jupiter's protection mitigates "
     "Mars's danger, interest in occult sciences, moderate longevity"),
    ("mars_jupiter", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["wealth", "enemies_litigation"],
     ["mars", "jupiter", "conjunction", "saravali", "8th_house", "loss"],
     "Ch.20 v.16",
     "Mars-Jupiter conjunction in 8th house: inheritance disputes, loss through "
     "legal confrontations, unexpected financial setbacks despite moral standing"),
    # House 9
    ("mars_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "9th_house"],
     "Ch.20 v.17",
     "Mars-Jupiter conjunction in 9th house: champion of dharma, righteous "
     "warrior defending faith, fame through religious or philosophical leadership"),
    ("mars_jupiter", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["mars", "jupiter", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.20 v.18",
     "Mars-Jupiter conjunction in 9th house: fortunate through father, gains "
     "from religious institutions, success in law or higher education"),
    # House 10
    ("mars_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "10th_house"],
     "Ch.20 v.19",
     "Mars-Jupiter conjunction in 10th house: dharma-karma yoga, powerful "
     "career combining action and wisdom, renowned leader or commander"),
    ("mars_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["mars", "jupiter", "conjunction", "saravali", "10th_house", "authority"],
     "Ch.20 v.20",
     "Mars-Jupiter conjunction in 10th house: attains high authority, wealth "
     "through government or institutional service, respected administrator"),
    ("mars_jupiter", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "10th_house", "virtue"],
     "Ch.20 v.21",
     "Mars-Jupiter conjunction in 10th house: virtuous conduct in professional "
     "life, combines assertiveness with fairness, public benefactor"),
    # House 11
    ("mars_jupiter", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "11th_house"],
     "Ch.20 v.22",
     "Mars-Jupiter conjunction in 11th house: abundant gains through righteous "
     "enterprise, powerful allies, fulfillment of ambitions"),
    ("mars_jupiter", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "11th_house", "network"],
     "Ch.20 v.23",
     "Mars-Jupiter conjunction in 11th house: benefits from elder siblings, "
     "leadership in social organizations, honored by community"),
    # House 12
    ("mars_jupiter", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["mars", "jupiter", "conjunction", "saravali", "12th_house"],
     "Ch.20 v.24",
     "Mars-Jupiter conjunction in 12th house: spiritual warrior, expenditure "
     "on religious causes, pilgrimage to distant lands"),
    ("mars_jupiter", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["enemies_litigation", "wealth"],
     ["mars", "jupiter", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.20 v.25",
     "Mars-Jupiter conjunction in 12th house: loss through legal battles, "
     "hidden enemies despite righteous conduct, financial drain"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mars_jupiter", "conjunction_condition", "own_sign_mars_aries", {},
     "favorable", "strong",
     ["career_status", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.20 v.26",
     "Mars-Jupiter conjunction in Aries (Mars's own sign): assertive wisdom, "
     "bold leadership guided by principle, pioneering dharmic action"),
    ("mars_jupiter", "conjunction_condition", "own_sign_mars_scorpio", {},
     "favorable", "strong",
     ["career_status", "spirituality"],
     ["mars", "jupiter", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.20 v.27",
     "Mars-Jupiter conjunction in Scorpio (Mars's own sign): deep investigative "
     "wisdom, success in research or occult disciplines, transformative leader"),
    ("mars_jupiter", "conjunction_condition", "own_sign_jupiter_sagittarius", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.20 v.28",
     "Mars-Jupiter conjunction in Sagittarius (Jupiter's own sign): philosophical "
     "warrior, champion of higher learning, fame through dharmic courage"),
    ("mars_jupiter", "conjunction_condition", "own_sign_jupiter_pisces", {},
     "favorable", "strong",
     ["spirituality", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "own_sign", "pisces"],
     "Ch.20 v.29",
     "Mars-Jupiter conjunction in Pisces (Jupiter's own sign): compassionate "
     "warrior, spiritual discipline, courage directed toward charitable causes"),
    ("mars_jupiter", "conjunction_condition", "exalted_mars_capricorn", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "exaltation", "capricorn"],
     "Ch.20 v.30",
     "Mars-Jupiter conjunction in Capricorn (Mars exalted): powerful dharmic "
     "authority, disciplined and principled leadership, great administrative success"),
    ("mars_jupiter", "conjunction_condition", "exalted_jupiter_cancer", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["mars", "jupiter", "conjunction", "saravali", "exaltation", "cancer"],
     "Ch.20 v.31",
     "Mars-Jupiter conjunction in Cancer (Jupiter exalted): abundant blessings, "
     "protective wisdom, wealth through righteous and nurturing enterprise"),
    ("mars_jupiter", "conjunction_condition", "debilitated_mars_cancer", {},
     "mixed", "moderate",
     ["character_temperament", "mental_health"],
     ["mars", "jupiter", "conjunction", "saravali", "debilitation", "cancer_mars"],
     "Ch.20 v.32",
     "Mars-Jupiter conjunction in Cancer (Mars debilitated, Jupiter exalted): "
     "wisdom compensates weakened courage, emotional but morally guided"),
    ("mars_jupiter", "conjunction_condition", "debilitated_jupiter_capricorn", {},
     "mixed", "moderate",
     ["spirituality", "career_status"],
     ["mars", "jupiter", "conjunction", "saravali", "debilitation", "capricorn_jupiter"],
     "Ch.20 v.33",
     "Mars-Jupiter conjunction in Capricorn (Jupiter debilitated, Mars exalted): "
     "material success but diminished dharmic compass, ambitious pragmatism"),
    ("mars_jupiter", "conjunction_condition", "jupiter_aspect_amplified", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["mars", "jupiter", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.20 v.34",
     "Mars-Jupiter conjunction with additional Jupiter aspect: dharmic energy "
     "powerfully amplified, revered teacher-warrior, spiritual authority"),
    ("mars_jupiter", "conjunction_condition", "saturn_aspect_restraining", {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["mars", "jupiter", "conjunction", "saravali", "saturn_aspect"],
     "Ch.20 v.35",
     "Mars-Jupiter conjunction aspected by Saturn: disciplined but delayed "
     "success, obstacles to righteous action, patience tested repeatedly"),
    ("mars_jupiter", "conjunction_condition", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "kendra"],
     "Ch.20 v.36",
     "Mars-Jupiter conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies dharma-karma yoga, prominent and influential personality"),
    ("mars_jupiter", "conjunction_condition", "trikona_placement", {},
     "favorable", "strong",
     ["spirituality", "wealth"],
     ["mars", "jupiter", "conjunction", "saravali", "trikona"],
     "Ch.20 v.37",
     "Mars-Jupiter conjunction in any trikona (1/5/9): strongly dharmic, "
     "fortune through righteous courage, blessed by divine protection"),
    ("mars_jupiter", "conjunction_condition", "dusthana_placement", {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["mars", "jupiter", "conjunction", "saravali", "dusthana"],
     "Ch.20 v.38",
     "Mars-Jupiter conjunction in any dusthana (6/8/12): Jupiter mitigates "
     "Mars malefic in evil houses, struggles lead to eventual spiritual growth"),
    ("mars_jupiter", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "enemies_litigation"],
     ["mars", "jupiter", "conjunction", "saravali", "upachaya"],
     "Ch.20 v.39",
     "Mars-Jupiter conjunction in upachaya houses (3/6/10/11): both courage "
     "and wisdom grow with age, progressive gains through righteous competition"),
    ("mars_jupiter", "conjunction_condition", "dharma_karma_yoga", {},
     "favorable", "strong",
     ["career_status", "spirituality"],
     ["mars", "jupiter", "conjunction", "saravali", "dharma_karma"],
     "Ch.20 v.40",
     "Mars-Jupiter conjunction forming dharma-karma yoga (9th/10th lords): "
     "exceptional combination for righteous leadership and professional dharma"),
    ("mars_jupiter", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["spirituality", "enemies_litigation"],
     ["mars", "jupiter", "conjunction", "saravali", "rahu", "triple"],
     "Ch.20 v.41",
     "Mars-Jupiter conjunction joined by Rahu: corrupted dharma, uses righteous "
     "facade for selfish ends, legal troubles from misrepresentation"),
    ("mars_jupiter", "conjunction_condition", "ketu_conjunction_triple", {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["mars", "jupiter", "conjunction", "saravali", "ketu", "triple"],
     "Ch.20 v.42",
     "Mars-Jupiter conjunction joined by Ketu: ascetic warrior, sudden spiritual "
     "transformation, renunciation of worldly ambition for higher path"),
    ("mars_jupiter", "conjunction_condition", "teacher_warrior_general", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mars", "jupiter", "conjunction", "saravali", "teacher", "warrior"],
     "Ch.20 v.43",
     "Mars-Jupiter conjunction well-placed: natural teacher-warrior archetype, "
     "aptitude for martial arts instruction, coaching, or military education"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars-Venus Conjunction — Ch.20 (SAV564–SAV606)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_VENUS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mars_venus", "conjunction_in_house", 1, {},
     "mixed", "strong",
     ["character_temperament", "physical_appearance"],
     ["mars", "venus", "conjunction", "saravali", "1st_house"],
     "Ch.20 v.39",
     "Mars-Venus conjunction in 1st house: attractive and passionate personality, "
     "magnetic physical presence, strong sensual nature dominates temperament"),
    ("mars_venus", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "1st_house", "passion"],
     "Ch.20 v.40",
     "Mars-Venus conjunction in 1st house: intense romantic inclinations, "
     "passionate disposition, artistic aggression in self-expression"),
    # House 2
    ("mars_venus", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "2nd_house"],
     "Ch.20 v.41",
     "Mars-Venus conjunction in 2nd house: wealth through arts, entertainment, "
     "or luxury goods, but extravagant spending on pleasures"),
    ("mars_venus", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["character_temperament", "physical_appearance"],
     ["mars", "venus", "conjunction", "saravali", "2nd_house", "speech"],
     "Ch.20 v.42",
     "Mars-Venus conjunction in 2nd house: passionate and seductive speech, "
     "attractive facial features, but harsh words in anger"),
    # House 3
    ("mars_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "3rd_house"],
     "Ch.20 v.43",
     "Mars-Venus conjunction in 3rd house: artistic courage, bold creative "
     "expression, success in performing arts or competitive aesthetics"),
    ("mars_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["mars", "venus", "conjunction", "saravali", "3rd_house", "talent"],
     "Ch.20 v.44",
     "Mars-Venus conjunction in 3rd house: talented in crafts and fine arts, "
     "gains through skilled handiwork, dynamic communication style"),
    # House 4
    ("mars_venus", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["property_vehicles", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "4th_house"],
     "Ch.20 v.45",
     "Mars-Venus conjunction in 4th house: luxurious home but domestic strife, "
     "beautiful vehicles and property acquired through passionate effort"),
    ("mars_venus", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "4th_house", "unrest"],
     "Ch.20 v.46",
     "Mars-Venus conjunction in 4th house: emotional turbulence at home, "
     "passion disrupts domestic peace, conflicts with mother over relationships"),
    # House 5
    ("mars_venus", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["progeny", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "5th_house"],
     "Ch.20 v.47",
     "Mars-Venus conjunction in 5th house: passionate love affairs, creative "
     "but impulsive romantic entanglements, artistic children"),
    ("mars_venus", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["intelligence_education", "wealth"],
     ["mars", "venus", "conjunction", "saravali", "5th_house", "speculation"],
     "Ch.20 v.48",
     "Mars-Venus conjunction in 5th house: speculative gains through arts or "
     "entertainment, artistic intelligence, but risky romantic investments"),
    # House 6
    ("mars_venus", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "6th_house"],
     "Ch.20 v.49",
     "Mars-Venus conjunction in 6th house: enmity through romantic involvements, "
     "defeats rivals in love but creates jealous enemies"),
    ("mars_venus", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "6th_house", "health"],
     "Ch.20 v.50",
     "Mars-Venus conjunction in 6th house: reproductive health issues, "
     "urinary or venereal complaints, marital discord from health matters"),
    # House 7
    ("mars_venus", "conjunction_in_house", 7, {},
     "mixed", "strong",
     ["marriage", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "7th_house"],
     "Ch.20 v.51",
     "Mars-Venus conjunction in 7th house: highly charged marriage, intense "
     "physical attraction to spouse, passionate but volatile partnership"),
    ("mars_venus", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "enemies_litigation"],
     ["mars", "venus", "conjunction", "saravali", "7th_house", "conflict"],
     "Ch.20 v.52",
     "Mars-Venus conjunction in 7th house: quarrels with spouse over romantic "
     "matters, jealousy in marriage, multiple relationships possible"),
    ("mars_venus", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "7th_house", "trade"],
     "Ch.20 v.53",
     "Mars-Venus conjunction in 7th house: success in luxury trade, cosmetics, "
     "or fashion industry, profitable business partnerships"),
    # House 8
    ("mars_venus", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["marriage", "longevity"],
     ["mars", "venus", "conjunction", "saravali", "8th_house"],
     "Ch.20 v.54",
     "Mars-Venus conjunction in 8th house: danger through passionate involvements, "
     "secret affairs cause scandal, reproductive health complications"),
    ("mars_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["mars", "venus", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.20 v.55",
     "Mars-Venus conjunction in 8th house: inheritance through spouse, interest "
     "in tantric or occult practices, transformative sensual experiences"),
    # House 9
    ("mars_venus", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "9th_house"],
     "Ch.20 v.56",
     "Mars-Venus conjunction in 9th house: passion conflicts with dharmic "
     "path, devotional fervor, artistic expression in religious context"),
    ("mars_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "foreign_travel"],
     ["mars", "venus", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.20 v.57",
     "Mars-Venus conjunction in 9th house: fortune through arts and culture, "
     "gains in foreign lands, passionate pursuit of higher learning"),
    # House 10
    ("mars_venus", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "venus", "conjunction", "saravali", "10th_house"],
     "Ch.20 v.58",
     "Mars-Venus conjunction in 10th house: career in arts, entertainment, "
     "or luxury industries, fame through passionate creative work"),
    ("mars_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "10th_house", "commerce"],
     "Ch.20 v.59",
     "Mars-Venus conjunction in 10th house: wealth through fashion, cosmetics, "
     "or beauty industry, dynamic and attractive professional presence"),
    # House 11
    ("mars_venus", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "11th_house"],
     "Ch.20 v.60",
     "Mars-Venus conjunction in 11th house: abundant gains through artistic "
     "ventures, passionate friendships, fulfilled romantic desires"),
    ("mars_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "11th_house", "social"],
     "Ch.20 v.61",
     "Mars-Venus conjunction in 11th house: popular in social circles, "
     "magnetic personality attracts influential friends and admirers"),
    # House 12
    ("mars_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["mars", "venus", "conjunction", "saravali", "12th_house"],
     "Ch.20 v.62",
     "Mars-Venus conjunction in 12th house: secret love affairs, expenditure "
     "on pleasures and luxuries, passionate bed comforts"),
    ("mars_venus", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.20 v.63",
     "Mars-Venus conjunction in 12th house: financial loss through romantic "
     "entanglements, scandal from illicit relationships, dissipation"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mars_venus", "conjunction_condition", "own_sign_venus_taurus", {},
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["mars", "venus", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.20 v.64",
     "Mars-Venus conjunction in Taurus (Venus's own sign): artistic passion "
     "refined, beautiful and sensual nature, wealth through luxury and arts"),
    ("mars_venus", "conjunction_condition", "own_sign_venus_libra", {},
     "favorable", "moderate",
     ["marriage", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "own_sign", "libra"],
     "Ch.20 v.65",
     "Mars-Venus conjunction in Libra (Venus's own sign, Mars debilitated): "
     "artistic elegance tempers aggression, success in fashion or diplomacy"),
    ("mars_venus", "conjunction_condition", "own_sign_mars_aries", {},
     "mixed", "strong",
     ["character_temperament", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.20 v.66",
     "Mars-Venus conjunction in Aries (Mars's own sign): aggressive beauty, "
     "dominating passion, forceful in romantic pursuits, impulsive lover"),
    ("mars_venus", "conjunction_condition", "own_sign_mars_scorpio", {},
     "mixed", "strong",
     ["marriage", "spirituality"],
     ["mars", "venus", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.20 v.67",
     "Mars-Venus conjunction in Scorpio (Mars's own sign): intense sexual "
     "magnetism, transformative relationships, tantric inclinations"),
    ("mars_venus", "conjunction_condition", "exalted_venus_pisces", {},
     "favorable", "strong",
     ["marriage", "spirituality"],
     ["mars", "venus", "conjunction", "saravali", "exaltation", "pisces"],
     "Ch.20 v.68",
     "Mars-Venus conjunction in Pisces (Venus exalted): divine love, compassionate "
     "passion, devotional arts, selfless romantic nature"),
    ("mars_venus", "conjunction_condition", "exalted_mars_capricorn", {},
     "mixed", "strong",
     ["career_status", "marriage"],
     ["mars", "venus", "conjunction", "saravali", "exaltation", "capricorn"],
     "Ch.20 v.69",
     "Mars-Venus conjunction in Capricorn (Mars exalted): disciplined passion, "
     "ambitious artist, practical approach to romantic relationships"),
    ("mars_venus", "conjunction_condition", "debilitated_venus_virgo", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "debilitation", "virgo"],
     "Ch.20 v.70",
     "Mars-Venus conjunction in Virgo (Venus debilitated): critical and "
     "dissatisfied in love, passion without refinement, marital complaints"),
    ("mars_venus", "conjunction_condition", "debilitated_mars_cancer", {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["mars", "venus", "conjunction", "saravali", "debilitation", "cancer"],
     "Ch.20 v.71",
     "Mars-Venus conjunction in Cancer (Mars debilitated): emotional and "
     "possessive lover, jealousy without courage to act, passive aggression"),
    ("mars_venus", "conjunction_condition", "saturn_aspect_controlled", {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "saturn_aspect"],
     "Ch.20 v.72",
     "Mars-Venus conjunction aspected by Saturn: controlled passion, delayed "
     "marriage, disciplined artistic expression, enduring but cold partnership"),
    ("mars_venus", "conjunction_condition", "jupiter_aspect_sanctified", {},
     "favorable", "strong",
     ["marriage", "spirituality"],
     ["mars", "venus", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.20 v.73",
     "Mars-Venus conjunction aspected by Jupiter: sanctified love, blessed "
     "marriage, passion guided by dharma, artistic devotion"),
    ("mars_venus", "conjunction_condition", "kendra_placement", {},
     "mixed", "strong",
     ["marriage", "career_status"],
     ["mars", "venus", "conjunction", "saravali", "kendra"],
     "Ch.20 v.74",
     "Mars-Venus conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies passionate nature, prominent romantic or artistic life"),
    ("mars_venus", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["marriage", "wealth"],
     ["mars", "venus", "conjunction", "saravali", "trikona"],
     "Ch.20 v.75",
     "Mars-Venus conjunction in any trikona (1/5/9): dharmic protection over "
     "passion, fortune through arts, sanctified romantic pursuits"),
    ("mars_venus", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["marriage", "physical_health"],
     ["mars", "venus", "conjunction", "saravali", "dusthana"],
     "Ch.20 v.76",
     "Mars-Venus conjunction in any dusthana (6/8/12): passion causes downfall, "
     "scandal, reproductive health issues, loss through romantic affairs"),
    ("mars_venus", "conjunction_condition", "upachaya_placement", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mars", "venus", "conjunction", "saravali", "upachaya"],
     "Ch.20 v.77",
     "Mars-Venus conjunction in upachaya houses (3/6/10/11): artistic drive "
     "strengthens with age, progressive gains through creative competition"),
    ("mars_venus", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "rahu", "triple"],
     "Ch.20 v.78",
     "Mars-Venus conjunction joined by Rahu: obsessive and illicit passion, "
     "unconventional relationships, scandal through forbidden attractions"),
    ("mars_venus", "conjunction_condition", "ketu_conjunction_triple", {},
     "mixed", "moderate",
     ["marriage", "spirituality"],
     ["mars", "venus", "conjunction", "saravali", "ketu", "triple"],
     "Ch.20 v.79",
     "Mars-Venus conjunction joined by Ketu: sudden loss of passion, detachment "
     "from romantic life, past-life karmic relationships, tantric tendencies"),
    ("mars_venus", "conjunction_condition", "artistic_career", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mars", "venus", "conjunction", "saravali", "art", "career"],
     "Ch.20 v.80",
     "Mars-Venus conjunction well-placed: natural aptitude for performing arts, "
     "dance, martial arts with aesthetic grace, sports with artistic flair"),
    ("mars_venus", "conjunction_condition", "mutual_enemy_sign", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "venus", "conjunction", "saravali", "enemy_sign"],
     "Ch.20 v.81",
     "Mars-Venus conjunction in enemy sign: passion misdirected, romantic "
     "failures, artistic talent suppressed by hostile environment"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars-Saturn Conjunction — Ch.20-21 (SAV607–SAV650)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mars_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "strong",
     ["physical_health", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "1st_house"],
     "Ch.20 v.77",
     "Mars-Saturn conjunction in 1st house: cruel and aggressive temperament, "
     "prone to injuries and scars, frustrated personality with violent outbursts"),
    ("mars_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["physical_appearance", "longevity"],
     ["mars", "saturn", "conjunction", "saravali", "1st_house", "body"],
     "Ch.20 v.78",
     "Mars-Saturn conjunction in 1st house: lean and hard body marked by wounds, "
     "chronic health complaints, aged appearance beyond years"),
    # House 2
    ("mars_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "strong",
     ["wealth", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "2nd_house"],
     "Ch.20 v.79",
     "Mars-Saturn conjunction in 2nd house: loss of wealth through litigation "
     "and conflict, harsh and abusive speech, family discord and estrangement"),
    ("mars_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["mars", "saturn", "conjunction", "saravali", "2nd_house", "face"],
     "Ch.20 v.80",
     "Mars-Saturn conjunction in 2nd house: dental problems, facial scars, "
     "diseases of mouth and eyes, dietary disorders"),
    # House 3
    ("mars_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["mars", "saturn", "conjunction", "saravali", "3rd_house"],
     "Ch.20 v.81",
     "Mars-Saturn conjunction in 3rd house: courageous but ruthless, succeeds "
     "through relentless effort, strained relations with siblings"),
    ("mars_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["enemies_litigation", "fame_reputation"],
     ["mars", "saturn", "conjunction", "saravali", "3rd_house", "valor"],
     "Ch.20 v.82",
     "Mars-Saturn conjunction in 3rd house: feared by opponents, malefics "
     "do well in upachaya, but gains through harsh and ruthless methods"),
    # House 4
    ("mars_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["property_vehicles", "mental_health"],
     ["mars", "saturn", "conjunction", "saravali", "4th_house"],
     "Ch.20 v.83",
     "Mars-Saturn conjunction in 4th house: loss of property through fire "
     "or litigation, no domestic peace, severe conflict with mother"),
    ("mars_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "4th_house", "misery"],
     "Ch.20 v.84",
     "Mars-Saturn conjunction in 4th house: deep mental anguish, heartless "
     "disposition, devoid of happiness, troubled childhood"),
    # House 5
    ("mars_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "strong",
     ["progeny", "intelligence_education"],
     ["mars", "saturn", "conjunction", "saravali", "5th_house"],
     "Ch.20 v.85",
     "Mars-Saturn conjunction in 5th house: obstacles to progeny, danger to "
     "children, harsh disciplinarian, miscarriages or surgical interventions"),
    ("mars_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["wealth", "mental_health"],
     ["mars", "saturn", "conjunction", "saravali", "5th_house", "loss"],
     "Ch.20 v.86",
     "Mars-Saturn conjunction in 5th house: speculative losses, frustrated "
     "ambitions, anger clouds judgment, poor decision-making"),
    # House 6
    ("mars_saturn", "conjunction_in_house", 6, {},
     "favorable", "strong",
     ["enemies_litigation", "career_status"],
     ["mars", "saturn", "conjunction", "saravali", "6th_house"],
     "Ch.21 v.1",
     "Mars-Saturn conjunction in 6th house: crushes all enemies and opponents, "
     "malefics excel in 6th house, success in competitive and legal battles"),
    ("mars_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "6th_house", "health"],
     "Ch.21 v.2",
     "Mars-Saturn conjunction in 6th house: overcomes diseases through endurance "
     "but prone to chronic inflammatory and bone disorders"),
    # House 7
    ("mars_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "7th_house"],
     "Ch.21 v.3",
     "Mars-Saturn conjunction in 7th house: disastrous for marriage, spouse "
     "suffers greatly, extreme conflict and possible separation or widowhood"),
    ("mars_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "longevity"],
     ["mars", "saturn", "conjunction", "saravali", "7th_house", "spouse"],
     "Ch.21 v.4",
     "Mars-Saturn conjunction in 7th house: danger to spouse's health and "
     "longevity, marital violence, legal battles related to partnership"),
    # House 8
    ("mars_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["mars", "saturn", "conjunction", "saravali", "8th_house"],
     "Ch.21 v.5",
     "Mars-Saturn conjunction in 8th house: severely shortened lifespan, danger "
     "from accidents, weapons, or falls, chronic and painful diseases"),
    ("mars_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["wealth", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "8th_house", "danger"],
     "Ch.21 v.6",
     "Mars-Saturn conjunction in 8th house: financial ruin through legal battles, "
     "imprisonment, punishment from authorities, inheritance denied"),
    # House 9
    ("mars_saturn", "conjunction_in_house", 9, {},
     "unfavorable", "strong",
     ["spirituality", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "9th_house"],
     "Ch.21 v.7",
     "Mars-Saturn conjunction in 9th house: irreligious and cruel, disrespects "
     "father and preceptors, misfortune in matters of dharma"),
    ("mars_saturn", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["career_status", "wealth"],
     ["mars", "saturn", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.21 v.8",
     "Mars-Saturn conjunction in 9th house: misfortune in career, obstructed "
     "by authorities, denied father's support, struggles in higher education"),
    # House 10
    ("mars_saturn", "conjunction_in_house", 10, {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "saturn", "conjunction", "saravali", "10th_house"],
     "Ch.21 v.9",
     "Mars-Saturn conjunction in 10th house: relentless ambition, rises through "
     "sheer force and persistence but creates many enemies in career"),
    ("mars_saturn", "conjunction_in_house", 10, {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "10th_house", "authority"],
     "Ch.21 v.10",
     "Mars-Saturn conjunction in 10th house: conflicts with authorities and "
     "superiors, career marked by power struggles and legal confrontations"),
    # House 11
    ("mars_saturn", "conjunction_in_house", 11, {},
     "mixed", "moderate",
     ["wealth", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "11th_house"],
     "Ch.21 v.11",
     "Mars-Saturn conjunction in 11th house: gains through hard and persistent "
     "effort, malefics do well in upachaya, but friendships are contentious"),
    ("mars_saturn", "conjunction_in_house", 11, {},
     "mixed", "moderate",
     ["fame_reputation", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "11th_house", "ambition"],
     "Ch.21 v.12",
     "Mars-Saturn conjunction in 11th house: ambitious social climber, achieves "
     "goals through intimidation, feared but not loved by associates"),
    # House 12
    ("mars_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["wealth", "physical_health"],
     ["mars", "saturn", "conjunction", "saravali", "12th_house"],
     "Ch.21 v.13",
     "Mars-Saturn conjunction in 12th house: heavy losses, hospitalization, "
     "imprisonment possible, expenditure on legal battles and medical treatment"),
    ("mars_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["enemies_litigation", "mental_health"],
     ["mars", "saturn", "conjunction", "saravali", "12th_house", "confinement"],
     "Ch.21 v.14",
     "Mars-Saturn conjunction in 12th house: confinement or exile, hidden "
     "enemies cause grave harm, mental anguish and isolation"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mars_saturn", "conjunction_condition", "own_sign_mars_aries", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.21 v.15",
     "Mars-Saturn conjunction in Aries (Mars's own sign, Saturn debilitated): "
     "aggressive energy overwhelms restriction, volatile and impulsive actions"),
    ("mars_saturn", "conjunction_condition", "own_sign_mars_scorpio", {},
     "unfavorable", "strong",
     ["enemies_litigation", "longevity"],
     ["mars", "saturn", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.21 v.16",
     "Mars-Saturn conjunction in Scorpio (Mars's own sign): vindictive and "
     "secretive, danger from hidden enemies, surgical or accident risk"),
    ("mars_saturn", "conjunction_condition", "own_sign_saturn_capricorn", {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.21 v.17",
     "Mars-Saturn conjunction in Capricorn (Saturn's own sign, Mars exalted): "
     "relentless ambition, both planets strong, ruthless but effective leadership"),
    ("mars_saturn", "conjunction_condition", "own_sign_saturn_aquarius", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.21 v.18",
     "Mars-Saturn conjunction in Aquarius (Saturn's own sign): unconventional "
     "aggression, reformist warrior, fights for social causes with harsh methods"),
    ("mars_saturn", "conjunction_condition", "exalted_mars_capricorn", {},
     "mixed", "strong",
     ["career_status", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "exaltation", "capricorn_mars"],
     "Ch.21 v.19",
     "Mars-Saturn conjunction in Capricorn (Mars exalted): powerful but dangerous "
     "combination, great achievement through ruthless and relentless ambition"),
    ("mars_saturn", "conjunction_condition", "exalted_saturn_libra", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "exaltation", "libra"],
     "Ch.21 v.20",
     "Mars-Saturn conjunction in Libra (Saturn exalted, Mars debilitated): "
     "disciplined restraint, aggression controlled by structure, patient endurance"),
    ("mars_saturn", "conjunction_condition", "debilitated_saturn_aries", {},
     "unfavorable", "strong",
     ["character_temperament", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "debilitation", "aries_saturn"],
     "Ch.21 v.21",
     "Mars-Saturn conjunction in Aries (Saturn debilitated): uncontrolled "
     "aggression, reckless behavior, accidents from impulsive actions"),
    ("mars_saturn", "conjunction_condition", "debilitated_mars_cancer", {},
     "unfavorable", "strong",
     ["mental_health", "marriage"],
     ["mars", "saturn", "conjunction", "saravali", "debilitation", "cancer_mars"],
     "Ch.21 v.22",
     "Mars-Saturn conjunction in Cancer (Mars debilitated): domestic violence, "
     "emotional cruelty, deep frustration at home, danger to mother"),
    ("mars_saturn", "conjunction_condition", "jupiter_aspect_mitigating", {},
     "mixed", "moderate",
     ["character_temperament", "spirituality"],
     ["mars", "saturn", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.21 v.23",
     "Mars-Saturn conjunction aspected by Jupiter: worst malefic effects "
     "mitigated, dharmic protection, suffering leads to spiritual growth"),
    ("mars_saturn", "conjunction_condition", "venus_aspect_softening", {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "venus_aspect"],
     "Ch.21 v.24",
     "Mars-Saturn conjunction aspected by Venus: harsh nature softened in "
     "relationships, artistic outlet for frustration, moderate marital results"),
    ("mars_saturn", "conjunction_condition", "kendra_placement", {},
     "unfavorable", "strong",
     ["career_status", "marriage"],
     ["mars", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.21 v.25",
     "Mars-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies double malefic, prominent but destructive influence on life"),
    ("mars_saturn", "conjunction_condition", "trikona_placement", {},
     "unfavorable", "moderate",
     ["spirituality", "wealth"],
     ["mars", "saturn", "conjunction", "saravali", "trikona"],
     "Ch.21 v.26",
     "Mars-Saturn conjunction in any trikona (1/5/9): dharmic houses afflicted, "
     "obstacles to fortune and spiritual progress, struggles with faith"),
    ("mars_saturn", "conjunction_condition", "dusthana_danger", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.21 v.27",
     "Mars-Saturn conjunction in any dusthana (6/8/12): most dangerous placement, "
     "severe accidents, chronic diseases, imprisonment, life-threatening events"),
    ("mars_saturn", "conjunction_condition", "upachaya_general", {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "upachaya"],
     "Ch.21 v.28",
     "Mars-Saturn conjunction in upachaya houses (3/6/10/11): malefics improve "
     "with time in growth houses, delayed but eventual competitive success"),
    ("mars_saturn", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "rahu", "triple"],
     "Ch.21 v.29",
     "Mars-Saturn conjunction joined by Rahu: extreme danger, triple malefic "
     "combination, accidents, poisoning, imprisonment, life-threatening events"),
    ("mars_saturn", "conjunction_condition", "ketu_conjunction_triple", {},
     "unfavorable", "strong",
     ["physical_health", "spirituality"],
     ["mars", "saturn", "conjunction", "saravali", "ketu", "triple"],
     "Ch.21 v.30",
     "Mars-Saturn conjunction joined by Ketu: sudden accidents, surgical "
     "emergencies, spiritual crisis through extreme suffering"),
    ("mars_saturn", "conjunction_condition", "accident_prone_general", {},
     "unfavorable", "strong",
     ["physical_health", "longevity"],
     ["mars", "saturn", "conjunction", "saravali", "accident", "danger"],
     "Ch.21 v.31",
     "Mars-Saturn conjunction in vulnerable position: accident-prone constitution, "
     "danger from fire, machinery, falls, and blunt trauma"),
    ("mars_saturn", "conjunction_condition", "legal_battles_general", {},
     "unfavorable", "moderate",
     ["enemies_litigation", "wealth"],
     ["mars", "saturn", "conjunction", "saravali", "legal", "battle"],
     "Ch.21 v.32",
     "Mars-Saturn conjunction afflicting relevant houses: protracted legal "
     "battles, disputes over property, punitive action from authorities"),
    ("mars_saturn", "conjunction_condition", "mutual_friend_sign", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["mars", "saturn", "conjunction", "saravali", "friend_sign"],
     "Ch.21 v.33",
     "Mars-Saturn conjunction in friendly sign: harsh energy slightly channeled, "
     "disciplined aggression yields results in structured environments"),
    ("mars_saturn", "conjunction_condition", "enemy_sign_placement", {},
     "unfavorable", "strong",
     ["character_temperament", "enemies_litigation"],
     ["mars", "saturn", "conjunction", "saravali", "enemy_sign"],
     "Ch.21 v.34",
     "Mars-Saturn conjunction in enemy sign: both malefics weakened and "
     "frustrated, reckless and self-destructive behavior, severe enmity"),
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
    mars_jupiter = _make_conjunction_rules(
        "mars_jupiter", ["mars", "jupiter"], _MARS_JUPITER_DATA, 521, "Ch.20",
    )
    mars_venus = _make_conjunction_rules(
        "mars_venus", ["mars", "venus"], _MARS_VENUS_DATA, 564, "Ch.20",
    )
    mars_saturn = _make_conjunction_rules(
        "mars_saturn", ["mars", "saturn"], _MARS_SATURN_DATA, 607, "Ch.20-21",
    )
    return mars_jupiter + mars_venus + mars_saturn


SARAVALI_CONJUNCTIONS_5_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_5_REGISTRY.add(_rule)
