"""src/corpus/saravali_conjunctions_4.py — S276: Saravali two-planet conjunctions.

SAV391–SAV520 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 19-20:
  Moon-Venus    (Ch.19) — SAV391–SAV433 (43 rules)
  Moon-Saturn   (Ch.19) — SAV434–SAV476 (43 rules)
  Mars-Mercury  (Ch.19-20) — SAV477–SAV520 (44 rules)

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
# Moon-Venus Conjunction — Ch.19 (SAV391–SAV433)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_VENUS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("moon_venus", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["physical_appearance", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "1st_house"],
     "Ch.19 v.1",
     "Moon-Venus conjunction in 1st house: beautiful and attractive appearance, "
     "charming personality, graceful demeanor admired by all"),
    ("moon_venus", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "1st_house", "luxury"],
     "Ch.19 v.2",
     "Moon-Venus conjunction in 1st house: luxurious lifestyle, fond of fine "
     "clothes and ornaments, enjoys comforts and sensual pleasures"),
    ("moon_venus", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "1st_house", "romantic"],
     "Ch.19 v.3",
     "Moon-Venus conjunction in 1st house: romantic and affectionate nature, "
     "attracts love easily, fond of music and artistic pursuits"),
    # House 2
    ("moon_venus", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["moon", "venus", "conjunction", "saravali", "2nd_house"],
     "Ch.19 v.4",
     "Moon-Venus conjunction in 2nd house: handsome face, sweet and melodious "
     "speech, accumulates wealth through artistic or aesthetic work"),
    ("moon_venus", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "venus", "conjunction", "saravali", "2nd_house", "family"],
     "Ch.19 v.5",
     "Moon-Venus conjunction in 2nd house: born into prosperous family, "
     "inherits wealth, earns through luxury goods or entertainment"),
    # House 3
    ("moon_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["moon", "venus", "conjunction", "saravali", "3rd_house"],
     "Ch.19 v.6",
     "Moon-Venus conjunction in 3rd house: artistic talents in communication, "
     "skilled in music and poetry, courageous yet refined disposition"),
    ("moon_venus", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "venus", "conjunction", "saravali", "3rd_house", "sibling"],
     "Ch.19 v.7",
     "Moon-Venus conjunction in 3rd house: gains through siblings, success in "
     "short journeys related to arts or fashion, skilled in persuasion"),
    # House 4
    ("moon_venus", "conjunction_in_house", 4, {},
     "favorable", "strong",
     ["property_vehicles", "mental_health"],
     ["moon", "venus", "conjunction", "saravali", "4th_house"],
     "Ch.19 v.8",
     "Moon-Venus conjunction in 4th house: blessed with beautiful home, luxury "
     "vehicles, domestic happiness, emotionally contented life"),
    ("moon_venus", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["character_temperament", "marriage"],
     ["moon", "venus", "conjunction", "saravali", "4th_house", "mother"],
     "Ch.19 v.9",
     "Moon-Venus conjunction in 4th house: loving relationship with mother, "
     "domestic harmony, aesthetically decorated living spaces"),
    # House 5
    ("moon_venus", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     ["moon", "venus", "conjunction", "saravali", "5th_house"],
     "Ch.19 v.10",
     "Moon-Venus conjunction in 5th house: beautiful and talented children, "
     "creative intelligence, success in performing arts and romance"),
    ("moon_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "5th_house", "creative"],
     "Ch.19 v.11",
     "Moon-Venus conjunction in 5th house: gains through speculation and "
     "entertainment, artistic fame, admired for creative brilliance"),
    ("moon_venus", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "5th_house", "romance"],
     "Ch.19 v.11a",
     "Moon-Venus conjunction in 5th house: deeply romantic disposition, "
     "love affairs lead to marriage, passionate courtship and devotion"),
    # House 6
    ("moon_venus", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     ["moon", "venus", "conjunction", "saravali", "6th_house"],
     "Ch.19 v.12",
     "Moon-Venus conjunction in 6th house: prone to urinary or reproductive "
     "ailments, enmity from women, disputes over luxury or pleasure"),
    ("moon_venus", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["moon", "venus", "conjunction", "saravali", "6th_house", "service"],
     "Ch.19 v.13",
     "Moon-Venus conjunction in 6th house: serves others in aesthetic or "
     "nurturing fields, overcomes rivals through charm rather than force"),
    # House 7
    ("moon_venus", "conjunction_in_house", 7, {},
     "favorable", "strong",
     ["marriage", "physical_appearance"],
     ["moon", "venus", "conjunction", "saravali", "7th_house"],
     "Ch.19 v.14",
     "Moon-Venus conjunction in 7th house: beautiful and loving spouse, "
     "passionate marriage, strong physical attraction in partnerships"),
    ("moon_venus", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "7th_house", "passion"],
     "Ch.19 v.15",
     "Moon-Venus conjunction in 7th house: excessive romantic inclinations, "
     "may have multiple attachments, sensual nature dominates judgment"),
    ("moon_venus", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["wealth", "marriage"],
     ["moon", "venus", "conjunction", "saravali", "7th_house", "trade"],
     "Ch.19 v.15a",
     "Moon-Venus conjunction in 7th house: gains through spouse and "
     "partnerships in luxury trade, business in beauty or fashion"),
    # House 8
    ("moon_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["wealth", "longevity"],
     ["moon", "venus", "conjunction", "saravali", "8th_house"],
     "Ch.19 v.16",
     "Moon-Venus conjunction in 8th house: gains through inheritance or "
     "spouse's wealth, but emotional upheavals in intimate matters"),
    ("moon_venus", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "venus", "conjunction", "saravali", "8th_house", "secret"],
     "Ch.19 v.17",
     "Moon-Venus conjunction in 8th house: secret romantic liaisons, emotional "
     "vulnerability, reproductive health concerns, hidden sorrows"),
    ("moon_venus", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["moon", "venus", "conjunction", "saravali", "8th_house", "occult"],
     "Ch.19 v.17a",
     "Moon-Venus conjunction in 8th house: interest in tantric or occult arts, "
     "transformative emotional experiences, mystical beauty perception"),
    # House 9
    ("moon_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["moon", "venus", "conjunction", "saravali", "9th_house"],
     "Ch.19 v.18",
     "Moon-Venus conjunction in 9th house: devotion to divine feminine, "
     "fortunate in love, gains through religious or artistic patronage"),
    ("moon_venus", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["fame_reputation", "intelligence_education"],
     ["moon", "venus", "conjunction", "saravali", "9th_house", "fortune"],
     "Ch.19 v.19",
     "Moon-Venus conjunction in 9th house: refined philosophical outlook, "
     "artistic appreciation of spiritual traditions, fortunate travels"),
    # House 10
    ("moon_venus", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "10th_house"],
     "Ch.19 v.20",
     "Moon-Venus conjunction in 10th house: fame in artistic or entertainment "
     "fields, career in beauty, fashion, or luxury industries"),
    ("moon_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "venus", "conjunction", "saravali", "10th_house", "public"],
     "Ch.19 v.21",
     "Moon-Venus conjunction in 10th house: public adoration, gains through "
     "dealings with women or aesthetic commerce, respected profession"),
    ("moon_venus", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "10th_house", "charitable"],
     "Ch.19 v.21a",
     "Moon-Venus conjunction in 10th house: charitable and generous in public "
     "life, patronizes arts and culture, admired for refined conduct"),
    # House 11
    ("moon_venus", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "11th_house"],
     "Ch.19 v.22",
     "Moon-Venus conjunction in 11th house: abundant gains through artistic "
     "ventures, wealthy friends, social popularity, fulfilled desires"),
    ("moon_venus", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "11th_house", "network"],
     "Ch.19 v.23",
     "Moon-Venus conjunction in 11th house: benefits from female friends, "
     "romantic fulfillment, gains through elder siblings or social circles"),
    # House 12
    ("moon_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["moon", "venus", "conjunction", "saravali", "12th_house"],
     "Ch.19 v.24",
     "Moon-Venus conjunction in 12th house: expenditure on luxuries and "
     "pleasures, spiritual devotion through art, bed comforts enjoyed"),
    ("moon_venus", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["marriage", "mental_health"],
     ["moon", "venus", "conjunction", "saravali", "12th_house", "loss"],
     "Ch.19 v.25",
     "Moon-Venus conjunction in 12th house: emotional losses in love, "
     "separation from beloved, excessive spending on romantic pursuits"),
    ("moon_venus", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["foreign_travel", "wealth"],
     ["moon", "venus", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.19 v.25a",
     "Moon-Venus conjunction in 12th house: pleasures in foreign lands, "
     "bed comforts and luxury in distant places, gains through exports"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("moon_venus", "conjunction_condition", "own_sign_venus_taurus", {},
     "favorable", "strong",
     ["wealth", "physical_appearance"],
     ["moon", "venus", "conjunction", "saravali", "own_sign", "taurus"],
     "Ch.19 v.26",
     "Moon-Venus conjunction in Taurus (Venus's own sign, Moon exalted): "
     "supreme beauty and luxury, exceptional wealth, aesthetic mastery"),
    ("moon_venus", "conjunction_condition", "own_sign_venus_libra", {},
     "favorable", "strong",
     ["marriage", "fame_reputation"],
     ["moon", "venus", "conjunction", "saravali", "own_sign", "libra"],
     "Ch.19 v.27",
     "Moon-Venus conjunction in Libra (Venus's own sign): harmonious "
     "relationships, artistic fame, balanced and refined personality"),
    ("moon_venus", "conjunction_condition", "exalted_moon_taurus", {},
     "favorable", "strong",
     ["mental_health", "physical_appearance"],
     ["moon", "venus", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.19 v.28",
     "Moon-Venus conjunction in Taurus (Moon exalted): emotional beauty, "
     "nurturing aesthetics, serene mind combined with sensual grace"),
    ("moon_venus", "conjunction_condition", "own_sign_moon_cancer", {},
     "favorable", "strong",
     ["mental_health", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "own_sign", "cancer"],
     "Ch.19 v.29",
     "Moon-Venus conjunction in Cancer (Moon's own sign): deep emotional "
     "sensitivity, nurturing beauty, loving and caring disposition"),
    ("moon_venus", "conjunction_condition", "debilitated_venus_virgo", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "debilitation", "virgo"],
     "Ch.19 v.30",
     "Moon-Venus conjunction in Virgo (Venus debilitated): overly critical "
     "in love, romantic dissatisfaction, beauty marred by perfectionism"),
    ("moon_venus", "conjunction_condition", "debilitated_moon_scorpio", {},
     "unfavorable", "strong",
     ["mental_health", "marriage"],
     ["moon", "venus", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.19 v.31",
     "Moon-Venus conjunction in Scorpio (Moon debilitated): emotional turmoil "
     "in relationships, jealousy and possessiveness, obsessive love"),
    ("moon_venus", "conjunction_condition", "combust_venus", {},
     "unfavorable", "moderate",
     ["marriage", "mental_health"],
     ["moon", "venus", "conjunction", "saravali", "combust", "emotional_dependency"],
     "Ch.19 v.32",
     "Combust Venus with Moon: emotional dependency in relationships, cannot "
     "distinguish love from need, clings to partners excessively"),
    ("moon_venus", "conjunction_condition", "jupiter_aspect_blessing", {},
     "favorable", "strong",
     ["marriage", "spirituality"],
     ["moon", "venus", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.19 v.33",
     "Moon-Venus conjunction aspected by Jupiter: blessed love, devotional "
     "beauty, marriage brings spiritual growth, generous nature"),
    ("moon_venus", "conjunction_condition", "saturn_aspect_restraint", {},
     "unfavorable", "moderate",
     ["marriage", "mental_health"],
     ["moon", "venus", "conjunction", "saravali", "saturn_aspect"],
     "Ch.19 v.34",
     "Moon-Venus conjunction aspected by Saturn: delayed romantic fulfillment, "
     "beauty with melancholy, love restrained by duty or circumstance"),
    ("moon_venus", "conjunction_condition", "mars_aspect_passion", {},
     "mixed", "strong",
     ["marriage", "character_temperament"],
     ["moon", "venus", "conjunction", "saravali", "mars_aspect"],
     "Ch.19 v.35",
     "Moon-Venus conjunction aspected by Mars: intense passion, fiery romance, "
     "quarrels in love but strong physical attraction"),
    ("moon_venus", "conjunction_condition", "kendra_placement", {},
     "favorable", "moderate",
     ["fame_reputation", "marriage"],
     ["moon", "venus", "conjunction", "saravali", "kendra"],
     "Ch.19 v.36",
     "Moon-Venus conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies beauty and charm, public recognition for artistic gifts"),
    ("moon_venus", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["wealth", "spirituality"],
     ["moon", "venus", "conjunction", "saravali", "trikona"],
     "Ch.19 v.37",
     "Moon-Venus conjunction in any trikona (1/5/9): dharmic love, fortune "
     "through artistic merit, creative children, spiritual aesthetics"),
    ("moon_venus", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["moon", "venus", "conjunction", "saravali", "dusthana"],
     "Ch.19 v.38",
     "Moon-Venus conjunction in any dusthana (6/8/12): love brings suffering, "
     "reproductive health issues, expenditure on romantic pursuits"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon-Saturn Conjunction — Ch.19 (SAV434–SAV476)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_SATURN_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("moon_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "strong",
     ["mental_health", "physical_appearance"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "1st_house"],
     "Ch.19 v.39",
     "Moon-Saturn conjunction in 1st house: melancholic disposition, lean and "
     "haggard appearance, emotionally restrained and serious demeanor"),
    ("moon_saturn", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "1st_house", "cold"],
     "Ch.19 v.40",
     "Moon-Saturn conjunction in 1st house: cold and distant personality, "
     "distrusted by others, lacks warmth in social interactions"),
    ("moon_saturn", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "1st_house", "duty"],
     "Ch.19 v.41",
     "Moon-Saturn conjunction in 1st house: strong sense of duty and discipline, "
     "succeeds through persistent effort despite emotional heaviness"),
    # House 2
    ("moon_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "2nd_house"],
     "Ch.19 v.42",
     "Moon-Saturn conjunction in 2nd house: harsh and unpleasant speech, "
     "poverty or delayed wealth accumulation, frugal to the point of misery"),
    ("moon_saturn", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["mental_health", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "2nd_house", "family"],
     "Ch.19 v.43",
     "Moon-Saturn conjunction in 2nd house: unhappy family life, emotional "
     "distance from relatives, financial anxiety dominates thinking"),
    # House 3
    ("moon_saturn", "conjunction_in_house", 3, {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "3rd_house"],
     "Ch.19 v.44",
     "Moon-Saturn conjunction in 3rd house: cautious and calculating mind, "
     "persistence in learning, strained relations with siblings"),
    ("moon_saturn", "conjunction_in_house", 3, {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "3rd_house", "fear"],
     "Ch.19 v.45",
     "Moon-Saturn conjunction in 3rd house: lacks courage, fearful disposition, "
     "hesitant in taking initiative, mental anxiety about trivial matters"),
    # House 4
    ("moon_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "property_vehicles"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "4th_house"],
     "Ch.19 v.46",
     "Moon-Saturn conjunction in 4th house: devoid of domestic happiness, "
     "loss of property, emotionally barren home environment"),
    ("moon_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "4th_house", "mother"],
     "Ch.19 v.47",
     "Moon-Saturn conjunction in 4th house: separation from mother or her "
     "suffering, deep inner sadness, lack of emotional nurturing"),
    ("moon_saturn", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["property_vehicles", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "4th_house", "land"],
     "Ch.19 v.47a",
     "Moon-Saturn conjunction in 4th house: loss of ancestral land through "
     "litigation or neglect, vehicles in disrepair, comfortless dwelling"),
    # House 5
    ("moon_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["progeny", "intelligence_education"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "5th_house"],
     "Ch.19 v.48",
     "Moon-Saturn conjunction in 5th house: delayed children, sorrowful "
     "experiences through progeny, pessimistic intellectual outlook"),
    ("moon_saturn", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["mental_health", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "5th_house", "loss"],
     "Ch.19 v.49",
     "Moon-Saturn conjunction in 5th house: losses in speculation, emotional "
     "inability to enjoy pleasures, dull creative expression"),
    # House 6
    ("moon_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "6th_house"],
     "Ch.19 v.50",
     "Moon-Saturn conjunction in 6th house: overcomes enemies through "
     "persistence, but chronic health issues and digestive complaints"),
    ("moon_saturn", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "6th_house", "disease"],
     "Ch.19 v.51",
     "Moon-Saturn conjunction in 6th house: rheumatic and cold-natured diseases, "
     "depression aggravated by illness, serves others reluctantly"),
    ("moon_saturn", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["career_status", "enemies_litigation"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "6th_house", "labor"],
     "Ch.19 v.51a",
     "Moon-Saturn conjunction in 6th house: success in labor-intensive service, "
     "defeats enemies through sheer endurance, respected in subordinate roles"),
    # House 7
    ("moon_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "7th_house"],
     "Ch.19 v.52",
     "Moon-Saturn conjunction in 7th house: delayed or unhappy marriage, "
     "emotionally cold spouse, loneliness within partnership"),
    ("moon_saturn", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "7th_house", "spouse"],
     "Ch.19 v.53",
     "Moon-Saturn conjunction in 7th house: older or austere spouse, marriage "
     "based on duty rather than love, lack of romantic fulfillment"),
    # House 8
    ("moon_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "8th_house"],
     "Ch.19 v.54",
     "Moon-Saturn conjunction in 8th house: chronic ailments, deep-seated "
     "emotional wounds, fear of death, prolonged suffering in illness"),
    ("moon_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["wealth", "longevity"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "8th_house", "loss"],
     "Ch.19 v.55",
     "Moon-Saturn conjunction in 8th house: loss of inheritance, denied "
     "financial support, poverty through unforeseen calamities"),
    ("moon_saturn", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "8th_house", "chronic"],
     "Ch.19 v.55a",
     "Moon-Saturn conjunction in 8th house: chronic cold-natured diseases, "
     "rheumatism and joint pains, emotional wounds that never fully heal"),
    # House 9
    ("moon_saturn", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["spirituality", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "9th_house"],
     "Ch.19 v.56",
     "Moon-Saturn conjunction in 9th house: lack of religious faith, pessimistic "
     "worldview, difficulties with father or spiritual preceptor"),
    ("moon_saturn", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["career_status", "spirituality"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "9th_house", "ascetic"],
     "Ch.19 v.57",
     "Moon-Saturn conjunction in 9th house: may adopt ascetic lifestyle, "
     "renunciation born from sorrow rather than wisdom, travels far"),
    # House 10
    ("moon_saturn", "conjunction_in_house", 10, {},
     "mixed", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "10th_house"],
     "Ch.19 v.58",
     "Moon-Saturn conjunction in 10th house: career in labor-intensive fields, "
     "rises slowly through persistent effort, lacks joy in work"),
    ("moon_saturn", "conjunction_in_house", 10, {},
     "unfavorable", "moderate",
     ["mental_health", "career_status"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "10th_house", "burden"],
     "Ch.19 v.59",
     "Moon-Saturn conjunction in 10th house: feels burdened by responsibilities, "
     "emotional exhaustion from career demands, joyless authority"),
    ("moon_saturn", "conjunction_in_house", 10, {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "10th_house", "endure"],
     "Ch.19 v.59a",
     "Moon-Saturn conjunction in 10th house: career in mining, agriculture, "
     "or heavy industry, wealth through patient toil and long service"),
    # House 11
    ("moon_saturn", "conjunction_in_house", 11, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "11th_house"],
     "Ch.19 v.60",
     "Moon-Saturn conjunction in 11th house: gains come slowly but steadily, "
     "few but loyal friends, fulfillment of desires after long delay"),
    ("moon_saturn", "conjunction_in_house", 11, {},
     "unfavorable", "weak",
     ["mental_health", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "11th_house", "lonely"],
     "Ch.19 v.61",
     "Moon-Saturn conjunction in 11th house: emotional isolation despite social "
     "network, cannot derive happiness from friendships, melancholic elder years"),
    # House 12
    ("moon_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["mental_health", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "12th_house"],
     "Ch.19 v.62",
     "Moon-Saturn conjunction in 12th house: heavy expenditure, insomnia, "
     "confinement in institutions, deep depression and emotional isolation"),
    ("moon_saturn", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "12th_house", "exile"],
     "Ch.19 v.63",
     "Moon-Saturn conjunction in 12th house: exile from homeland, bedridden "
     "periods, chronic ailments of cold nature, emotional numbness"),
    ("moon_saturn", "conjunction_in_house", 12, {},
     "mixed", "weak",
     ["spirituality", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "12th_house", "detach"],
     "Ch.19 v.63a",
     "Moon-Saturn conjunction in 12th house: enforced detachment leads to "
     "spiritual growth, renunciation through suffering, monastic tendencies"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("moon_saturn", "conjunction_condition", "vish_yoga_formation", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["moon", "saturn", "conjunction", "saravali", "vish_yoga", "poison"],
     "Ch.19 v.64",
     "Vish Yoga (Moon-Saturn conjunction in adverse conditions): poisonous "
     "combination creating chronic melancholy, fear, and physical debility"),
    ("moon_saturn", "conjunction_condition", "own_sign_saturn_capricorn", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "own_sign", "capricorn"],
     "Ch.19 v.65",
     "Moon-Saturn conjunction in Capricorn (Saturn's own sign): structured "
     "emotions channeled into career, disciplined but emotionally austere"),
    ("moon_saturn", "conjunction_condition", "own_sign_saturn_aquarius", {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["moon", "saturn", "conjunction", "saravali", "own_sign", "aquarius"],
     "Ch.19 v.66",
     "Moon-Saturn conjunction in Aquarius (Saturn's own sign): detached "
     "emotional nature, humanitarian outlook, intellectual melancholy"),
    ("moon_saturn", "conjunction_condition", "own_sign_moon_cancer", {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "own_sign", "cancer", "conflict"],
     "Ch.19 v.67",
     "Moon-Saturn conjunction in Cancer (Moon's own sign, Saturn debilitated): "
     "emotional conflict intensified, nurturing nature crushed by restriction"),
    ("moon_saturn", "conjunction_condition", "exalted_moon_taurus", {},
     "mixed", "moderate",
     ["mental_health", "wealth"],
     ["moon", "saturn", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.19 v.68",
     "Moon-Saturn conjunction in Taurus (Moon exalted): emotional strength "
     "partially resists Saturn's melancholy, wealth with emotional cost"),
    ("moon_saturn", "conjunction_condition", "exalted_saturn_libra", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "saturn", "conjunction", "saravali", "exaltation", "libra"],
     "Ch.19 v.69",
     "Moon-Saturn conjunction in Libra (Saturn exalted): disciplined emotions "
     "serve career, balanced but cold disposition, respected authority"),
    ("moon_saturn", "conjunction_condition", "debilitated_moon_scorpio", {},
     "unfavorable", "strong",
     ["mental_health", "longevity"],
     ["moon", "saturn", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.19 v.70",
     "Moon-Saturn conjunction in Scorpio (Moon debilitated): severe emotional "
     "disturbance, morbid thoughts, fear of hidden dangers, chronic ailments"),
    ("moon_saturn", "conjunction_condition", "debilitated_saturn_aries", {},
     "unfavorable", "strong",
     ["mental_health", "career_status"],
     ["moon", "saturn", "conjunction", "saravali", "debilitation", "aries"],
     "Ch.19 v.71",
     "Moon-Saturn conjunction in Aries (Saturn debilitated): impulsive sadness, "
     "undisciplined melancholy, career setbacks from emotional instability"),
    ("moon_saturn", "conjunction_condition", "jupiter_aspect_relief", {},
     "favorable", "moderate",
     ["mental_health", "spirituality"],
     ["moon", "saturn", "conjunction", "saravali", "jupiter_aspect", "relief"],
     "Ch.19 v.72",
     "Moon-Saturn conjunction aspected by Jupiter: relief from melancholy, "
     "wisdom transforms suffering into spiritual growth, protected mind"),
    ("moon_saturn", "conjunction_condition", "venus_aspect_softening", {},
     "mixed", "moderate",
     ["marriage", "mental_health"],
     ["moon", "saturn", "conjunction", "saravali", "venus_aspect"],
     "Ch.19 v.73",
     "Moon-Saturn conjunction aspected by Venus: romantic comfort partially "
     "eases emotional burden, finds solace in beauty and art"),
    ("moon_saturn", "conjunction_condition", "mars_aspect_agitation", {},
     "unfavorable", "strong",
     ["mental_health", "enemies_litigation"],
     ["moon", "saturn", "conjunction", "saravali", "mars_aspect"],
     "Ch.19 v.74",
     "Moon-Saturn conjunction aspected by Mars: emotional agitation intensified, "
     "anger born of frustration, conflicts driven by inner discontent"),
    ("moon_saturn", "conjunction_condition", "kendra_placement", {},
     "unfavorable", "moderate",
     ["mental_health", "career_status"],
     ["moon", "saturn", "conjunction", "saravali", "kendra"],
     "Ch.19 v.75",
     "Moon-Saturn conjunction in any kendra (1/4/7/10): angular strength "
     "makes emotional restriction publicly visible, duty overshadows joy"),
    ("moon_saturn", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["longevity", "mental_health", "physical_health"],
     ["moon", "saturn", "conjunction", "saravali", "dusthana"],
     "Ch.19 v.76",
     "Moon-Saturn conjunction in any dusthana (6/8/12): worst Vish Yoga "
     "effects manifest, chronic disease, deep depression, confinement"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Mars-Mercury Conjunction — Ch.19-20 (SAV477–SAV520)
# ═══════════════════════════════════════════════════════════════════════════════
_MARS_MERCURY_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("mars_mercury", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "1st_house"],
     "Ch.19 v.77",
     "Mars-Mercury conjunction in 1st house: sharp and quick intellect, "
     "argumentative nature, skilled in debate but creates verbal enemies"),
    ("mars_mercury", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "1st_house", "technical"],
     "Ch.19 v.78",
     "Mars-Mercury conjunction in 1st house: technical and mechanical aptitude, "
     "skilled with hands and tools, engineering or surgical ability"),
    ("mars_mercury", "conjunction_in_house", 1, {},
     "unfavorable", "weak",
     ["character_temperament", "enemies_litigation"],
     ["mars", "mercury", "conjunction", "saravali", "1st_house", "quarrel"],
     "Ch.19 v.79",
     "Mars-Mercury conjunction in 1st house: quarrelsome speech, uses intellect "
     "to wound, sharp tongue creates unnecessary conflicts"),
    # House 2
    ("mars_mercury", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["wealth", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "2nd_house"],
     "Ch.19 v.80",
     "Mars-Mercury conjunction in 2nd house: harsh but clever speech, "
     "earns through technical skills, sharp financial acumen"),
    ("mars_mercury", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["mars", "mercury", "conjunction", "saravali", "2nd_house", "speech"],
     "Ch.19 v.81",
     "Mars-Mercury conjunction in 2nd house: cutting and sarcastic speech, "
     "family disputes over money, verbal aggression damages relationships"),
    # House 3
    ("mars_mercury", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["character_temperament", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "3rd_house"],
     "Ch.19 v.82",
     "Mars-Mercury conjunction in 3rd house: courageous and intelligent, "
     "excels in competitive examinations, skilled strategist and writer"),
    ("mars_mercury", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["mars", "mercury", "conjunction", "saravali", "3rd_house", "media"],
     "Ch.19 v.83",
     "Mars-Mercury conjunction in 3rd house: success in media, journalism, "
     "or investigative work, bold communication style gains recognition"),
    ("mars_mercury", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "3rd_house", "sibling"],
     "Ch.19 v.83a",
     "Mars-Mercury conjunction in 3rd house: competitive rapport with siblings, "
     "gains through short travels, boldness in commercial transactions"),
    # House 4
    ("mars_mercury", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "4th_house"],
     "Ch.19 v.84",
     "Mars-Mercury conjunction in 4th house: technical education, interest in "
     "engineering or architecture, domestic arguments over trivial matters"),
    ("mars_mercury", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "4th_house", "restless"],
     "Ch.19 v.85",
     "Mars-Mercury conjunction in 4th house: restless mind, agitated domestic "
     "environment, sharp intellect finds no peace at home"),
    # House 5
    ("mars_mercury", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["intelligence_education", "progeny"],
     ["mars", "mercury", "conjunction", "saravali", "5th_house"],
     "Ch.20 v.1",
     "Mars-Mercury conjunction in 5th house: brilliant but combative intellect, "
     "debates with children, speculative gains through calculated risk"),
    ("mars_mercury", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "5th_house", "strategy"],
     "Ch.20 v.2",
     "Mars-Mercury conjunction in 5th house: strategic thinking, success in "
     "competitive sports or intellectual contests, tactical brilliance"),
    # House 6
    ("mars_mercury", "conjunction_in_house", 6, {},
     "favorable", "strong",
     ["enemies_litigation", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "6th_house"],
     "Ch.20 v.3",
     "Mars-Mercury conjunction in 6th house: destroys enemies through strategic "
     "intelligence, excels in litigation, military planning, or surgery"),
    ("mars_mercury", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["physical_health", "enemies_litigation"],
     ["mars", "mercury", "conjunction", "saravali", "6th_house", "health"],
     "Ch.20 v.4",
     "Mars-Mercury conjunction in 6th house: nervous and inflammatory disorders, "
     "skin eruptions, but overcomes health issues through active effort"),
    ("mars_mercury", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "6th_house", "surgical"],
     "Ch.20 v.4a",
     "Mars-Mercury conjunction in 6th house: aptitude for surgical or forensic "
     "work, excels in military intelligence, skilled in criminal investigation"),
    # House 7
    ("mars_mercury", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "7th_house"],
     "Ch.20 v.5",
     "Mars-Mercury conjunction in 7th house: arguments with spouse, intellectual "
     "domination in partnership, sharp criticism damages marital harmony"),
    ("mars_mercury", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["career_status", "marriage"],
     ["mars", "mercury", "conjunction", "saravali", "7th_house", "business"],
     "Ch.20 v.6",
     "Mars-Mercury conjunction in 7th house: success in business partnerships "
     "through aggressive negotiation, but personal relationships suffer"),
    # House 8
    ("mars_mercury", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     ["mars", "mercury", "conjunction", "saravali", "8th_house"],
     "Ch.20 v.7",
     "Mars-Mercury conjunction in 8th house: danger from sharp instruments, "
     "surgical interventions, legal entanglements, accident-prone nature"),
    ("mars_mercury", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["intelligence_education", "spirituality"],
     ["mars", "mercury", "conjunction", "saravali", "8th_house", "research"],
     "Ch.20 v.8",
     "Mars-Mercury conjunction in 8th house: research into hidden matters, "
     "forensic or investigative skill, intelligence applied to mysteries"),
    ("mars_mercury", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["physical_health", "wealth"],
     ["mars", "mercury", "conjunction", "saravali", "8th_house", "surgery"],
     "Ch.20 v.8a",
     "Mars-Mercury conjunction in 8th house: undergoes surgical procedures, "
     "losses through technical failures, insurance or inheritance disputes"),
    # House 9
    ("mars_mercury", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "9th_house"],
     "Ch.20 v.9",
     "Mars-Mercury conjunction in 9th house: argumentative about religion, "
     "challenges traditional beliefs, sharp philosophical debates"),
    ("mars_mercury", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["character_temperament", "spirituality"],
     ["mars", "mercury", "conjunction", "saravali", "9th_house", "irreligious"],
     "Ch.20 v.10",
     "Mars-Mercury conjunction in 9th house: disrespects preceptors through "
     "intellectual arrogance, conflicts with father over ideological matters"),
    # House 10
    ("mars_mercury", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["mars", "mercury", "conjunction", "saravali", "10th_house"],
     "Ch.20 v.11",
     "Mars-Mercury conjunction in 10th house: successful in technical or "
     "engineering career, military strategist, fame through decisive action"),
    ("mars_mercury", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "10th_house", "command"],
     "Ch.20 v.12",
     "Mars-Mercury conjunction in 10th house: commands through intellect and "
     "force combined, wealth through technical enterprise, respected leader"),
    ("mars_mercury", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["fame_reputation", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "10th_house", "engineer"],
     "Ch.20 v.12a",
     "Mars-Mercury conjunction in 10th house: fame in engineering, technology, "
     "or applied sciences, patents and innovations bring recognition"),
    # House 11
    ("mars_mercury", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "11th_house"],
     "Ch.20 v.13",
     "Mars-Mercury conjunction in 11th house: abundant gains through technical "
     "skill, profits from engineering or trade, influential associates"),
    ("mars_mercury", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "11th_house", "network"],
     "Ch.20 v.14",
     "Mars-Mercury conjunction in 11th house: gains through competitive "
     "networks, respected for sharp intellect, elder siblings prosper"),
    # House 12
    ("mars_mercury", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "enemies_litigation"],
     ["mars", "mercury", "conjunction", "saravali", "12th_house"],
     "Ch.20 v.15",
     "Mars-Mercury conjunction in 12th house: expenditure through litigation, "
     "intelligence wasted on futile arguments, losses through disputes"),
    ("mars_mercury", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["mental_health", "physical_health"],
     ["mars", "mercury", "conjunction", "saravali", "12th_house", "nervous"],
     "Ch.20 v.16",
     "Mars-Mercury conjunction in 12th house: nervous exhaustion, insomnia "
     "from overactive mind, hospitalization from stress-related illness"),
    ("mars_mercury", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["foreign_travel", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "12th_house", "foreign"],
     "Ch.20 v.16a",
     "Mars-Mercury conjunction in 12th house: technical work in foreign lands, "
     "engineering or IT career abroad, expenditure on machinery or tools"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("mars_mercury", "conjunction_condition", "own_sign_mercury_gemini", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.20 v.17",
     "Mars-Mercury conjunction in Gemini (Mercury's own sign): intellectual "
     "aggression channeled into debate, writing, or journalism excellence"),
    ("mars_mercury", "conjunction_condition", "own_sign_mercury_virgo", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.20 v.18",
     "Mars-Mercury conjunction in Virgo (Mercury exalted + own): surgical "
     "precision in analysis, technical mastery, engineering excellence"),
    ("mars_mercury", "conjunction_condition", "own_sign_mars_aries", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.20 v.19",
     "Mars-Mercury conjunction in Aries (Mars's own sign): aggressive intellect, "
     "impulsive decisions, military strategy, engineering aptitude"),
    ("mars_mercury", "conjunction_condition", "own_sign_mars_scorpio", {},
     "mixed", "strong",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.20 v.20",
     "Mars-Mercury conjunction in Scorpio (Mars's own sign): investigative "
     "genius, forensic or detective ability, penetrating analytical mind"),
    ("mars_mercury", "conjunction_condition", "debilitated_mercury_pisces", {},
     "unfavorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["mars", "mercury", "conjunction", "saravali", "debilitation", "pisces"],
     "Ch.20 v.21",
     "Mars-Mercury conjunction in Pisces (Mercury debilitated): confused "
     "aggression, arguments without logical basis, scattered energy"),
    ("mars_mercury", "conjunction_condition", "debilitated_mars_cancer", {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["mars", "mercury", "conjunction", "saravali", "debilitation", "cancer"],
     "Ch.20 v.22",
     "Mars-Mercury conjunction in Cancer (Mars debilitated): emotional arguments, "
     "technical skills undermined by insecurity, domestic verbal fights"),
    ("mars_mercury", "conjunction_condition", "exalted_mercury_virgo", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "exaltation", "virgo"],
     "Ch.20 v.23",
     "Mars-Mercury conjunction in Virgo (Mercury exalted): analytical precision "
     "at its peak, surgical skill, mathematical and scientific genius"),
    ("mars_mercury", "conjunction_condition", "exalted_mars_capricorn", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["mars", "mercury", "conjunction", "saravali", "exaltation", "capricorn"],
     "Ch.20 v.24",
     "Mars-Mercury conjunction in Capricorn (Mars exalted): disciplined "
     "technical mastery, strategic career advancement, engineering wealth"),
    ("mars_mercury", "conjunction_condition", "jupiter_aspect_dharmic", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["mars", "mercury", "conjunction", "saravali", "jupiter_aspect", "dharmic"],
     "Ch.20 v.25",
     "Mars-Mercury conjunction aspected by Jupiter: dharmic debate, sharp "
     "intellect directed toward righteous causes, scholarly argumentation"),
    ("mars_mercury", "conjunction_condition", "saturn_aspect_calculated", {},
     "mixed", "moderate",
     ["career_status", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "saturn_aspect", "strategy"],
     "Ch.20 v.26",
     "Mars-Mercury conjunction aspected by Saturn: calculated strategy, slow "
     "but thorough technical work, persistence in research and engineering"),
    ("mars_mercury", "conjunction_condition", "venus_aspect_refinement", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["mars", "mercury", "conjunction", "saravali", "venus_aspect"],
     "Ch.20 v.27",
     "Mars-Mercury conjunction aspected by Venus: technical skills refined by "
     "aesthetic sense, success in design, architecture, or artistic engineering"),
    ("mars_mercury", "conjunction_condition", "kendra_placement", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["mars", "mercury", "conjunction", "saravali", "kendra"],
     "Ch.20 v.28",
     "Mars-Mercury conjunction in any kendra (1/4/7/10): angular strength "
     "amplifies technical ability, prominent career in engineering or law"),
    ("mars_mercury", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["mars", "mercury", "conjunction", "saravali", "trikona"],
     "Ch.20 v.29",
     "Mars-Mercury conjunction in any trikona (1/5/9): intellectual fire "
     "directed toward dharmic learning, sharp philosophical insight"),
    ("mars_mercury", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "strong",
     ["enemies_litigation", "physical_health"],
     ["mars", "mercury", "conjunction", "saravali", "dusthana"],
     "Ch.20 v.30",
     "Mars-Mercury conjunction in any dusthana (6/8/12): intellect used for "
     "deception, legal troubles, nervous breakdowns, surgical dangers"),
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
    moon_venus = _make_conjunction_rules(
        "moon_venus", ["moon", "venus"], _MOON_VENUS_DATA, 391, "Ch.19",
    )
    moon_saturn = _make_conjunction_rules(
        "moon_saturn", ["moon", "saturn"], _MOON_SATURN_DATA, 434, "Ch.19",
    )
    mars_mercury = _make_conjunction_rules(
        "mars_mercury", ["mars", "mercury"], _MARS_MERCURY_DATA, 477, "Ch.19-20",
    )
    return moon_venus + moon_saturn + mars_mercury


SARAVALI_CONJUNCTIONS_4_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_4_REGISTRY.add(_rule)
