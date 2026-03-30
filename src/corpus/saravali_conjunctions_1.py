"""src/corpus/saravali_conjunctions_1.py — S273: Saravali two-planet conjunctions.

SAV001–SAV130 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 15-17:
  Sun-Moon   (Ch.15) — SAV001–SAV043 (43 rules)
  Sun-Mars   (Ch.16) — SAV044–SAV086 (43 rules)
  Sun-Mercury (Ch.16-17) — SAV087–SAV130 (44 rules)

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
# Sun-Moon Conjunction — Ch.15 (SAV001–SAV043)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_MOON_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_moon", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["career_status", "physical_appearance"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "1st_house"],
     "Ch.15 v.1",
     "Sun-Moon conjunction in 1st house: native has mechanical or artisan skills, "
     "engaged in servile work, lacks independence in profession"),
    ("sun_moon", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "1st_house", "vision"],
     "Ch.15 v.2",
     "Sun-Moon conjunction in 1st house: defective vision or eye troubles, "
     "thin or lean body, subject to bodily complaints"),
    ("sun_moon", "conjunction_in_house", 1, {},
     "unfavorable", "weak",
     ["character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "1st_house", "temperament"],
     "Ch.15 v.3",
     "Sun-Moon conjunction in 1st house: servile nature, lacks self-assertion, "
     "tends to be dominated by others"),
    # House 2
    ("sun_moon", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "2nd_house"],
     "Ch.15 v.4",
     "Sun-Moon conjunction in 2nd house: employed by others, wealth earned through "
     "service rather than independent enterprise"),
    ("sun_moon", "conjunction_in_house", 2, {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "2nd_house", "speech"],
     "Ch.15 v.5",
     "Sun-Moon conjunction in 2nd house: cunning speech, skilled in persuasion, "
     "intelligent but uses cleverness for personal gain"),
    # House 3
    ("sun_moon", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "3rd_house"],
     "Ch.15 v.6",
     "Sun-Moon conjunction in 3rd house: clever and wise, skilled in scriptural "
     "knowledge, valorous among peers"),
    ("sun_moon", "conjunction_in_house", 3, {},
     "unfavorable", "weak",
     ["wealth", "enemies_litigation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "3rd_house", "miserly"],
     "Ch.15 v.7",
     "Sun-Moon conjunction in 3rd house: miserly disposition, accumulates "
     "but does not enjoy wealth, suspicious of others"),
    # House 4
    ("sun_moon", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "4th_house"],
     "Ch.15 v.8",
     "Sun-Moon conjunction in 4th house: quarrelsome temperament, picks fights "
     "over trivial matters, troubled domestic life"),
    ("sun_moon", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["property_vehicles", "wealth"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "4th_house", "fortune"],
     "Ch.15 v.9",
     "Sun-Moon conjunction in 4th house: generally unfortunate in matters of "
     "landed property, loss of ancestral assets"),
    ("sun_moon", "conjunction_in_house", 4, {},
     "unfavorable", "weak",
     ["mental_health", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "4th_house", "unhappy"],
     "Ch.15 v.10",
     "Sun-Moon conjunction in 4th house: devoid of happiness from mother "
     "and domestic comforts, mental restlessness"),
    # House 5
    ("sun_moon", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["progeny", "intelligence_education"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "5th_house"],
     "Ch.15 v.11",
     "Sun-Moon conjunction in 5th house: obstacles to progeny, delayed children, "
     "difficulty in creative self-expression"),
    ("sun_moon", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "5th_house", "status"],
     "Ch.15 v.12",
     "Sun-Moon conjunction in 5th house: may attain position of authority "
     "but faces envy and obstacles from subordinates"),
    # House 6
    ("sun_moon", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["enemies_litigation", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "6th_house"],
     "Ch.15 v.13",
     "Sun-Moon conjunction in 6th house: conquers enemies, successful in "
     "competitive endeavors, gains through service"),
    ("sun_moon", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "6th_house", "health"],
     "Ch.15 v.14",
     "Sun-Moon conjunction in 6th house: prone to fevers and bilious disorders, "
     "weak constitution requiring careful health management"),
    # House 7
    ("sun_moon", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "7th_house"],
     "Ch.15 v.15",
     "Sun-Moon conjunction in 7th house: shameless conduct, lacks propriety "
     "in social dealings, disregards conventions"),
    ("sun_moon", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "wealth"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "7th_house", "spouse"],
     "Ch.15 v.16",
     "Sun-Moon conjunction in 7th house: humiliated through spouse or partner, "
     "spouse may be sickly or cause loss of status"),
    ("sun_moon", "conjunction_in_house", 7, {},
     "unfavorable", "weak",
     ["physical_health", "physical_appearance"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "7th_house", "body"],
     "Ch.15 v.17",
     "Sun-Moon conjunction in 7th house: afflicted by sexual ailments, "
     "physical debility related to reproductive system"),
    # House 8
    ("sun_moon", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "8th_house"],
     "Ch.15 v.18",
     "Sun-Moon conjunction in 8th house: shortened longevity, chronic ailments, "
     "danger from fevers and inflammatory conditions"),
    ("sun_moon", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["wealth", "property_vehicles"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "8th_house", "loss"],
     "Ch.15 v.19",
     "Sun-Moon conjunction in 8th house: loss of paternal property, denied "
     "inheritance, financial setbacks through unexpected events"),
    # House 9
    ("sun_moon", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["spirituality", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "9th_house"],
     "Ch.15 v.20",
     "Sun-Moon conjunction in 9th house: receives favor from rulers or "
     "government, some religious inclination but lacks deep faith"),
    ("sun_moon", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["spirituality", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "9th_house", "father"],
     "Ch.15 v.21",
     "Sun-Moon conjunction in 9th house: difficulties with father, separation "
     "from preceptor, struggles with traditional religious observance"),
    # House 10
    ("sun_moon", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "10th_house"],
     "Ch.15 v.22",
     "Sun-Moon conjunction in 10th house: successful in undertakings, rises to "
     "prominence through personal effort, good professional reputation"),
    ("sun_moon", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "10th_house", "wealth"],
     "Ch.15 v.23",
     "Sun-Moon conjunction in 10th house: possesses conveyances, attendants, "
     "and material comforts through career achievements"),
    ("sun_moon", "conjunction_in_house", 10, {},
     "favorable", "weak",
     ["character_temperament", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "10th_house", "character"],
     "Ch.15 v.24",
     "Sun-Moon conjunction in 10th house: charitable and virtuous disposition, "
     "engages in meritorious deeds and public service"),
    # House 11
    ("sun_moon", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "11th_house"],
     "Ch.15 v.25",
     "Sun-Moon conjunction in 11th house: accumulates wealth, enjoys gains "
     "from multiple sources, large social network"),
    ("sun_moon", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "11th_house", "status"],
     "Ch.15 v.26",
     "Sun-Moon conjunction in 11th house: truthful and respected in society, "
     "honored by superiors and gains through elder siblings"),
    # House 12
    ("sun_moon", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "physical_health"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "12th_house"],
     "Ch.15 v.27",
     "Sun-Moon conjunction in 12th house: expenditure exceeds income, "
     "weak eyesight, financial losses through hidden enemies"),
    ("sun_moon", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["character_temperament", "marriage"],
     ["sun", "moon", "conjunction", "saravali", "amavasya", "12th_house", "sinful"],
     "Ch.15 v.28",
     "Sun-Moon conjunction in 12th house: sinful inclinations, incurs enmity "
     "of spouse, separated from family or homeland"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_moon", "conjunction_condition", "waxing_moon_conjunction", {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "waxing_moon"],
     "Ch.15 v.29",
     "Sun-Moon conjunction with waxing Moon (Shukla Amavasya): mitigates malefic "
     "results, native gains wealth and reputation despite new moon birth"),
    ("sun_moon", "conjunction_condition", "waning_moon_conjunction", {},
     "unfavorable", "moderate",
     ["mental_health", "physical_health"],
     ["sun", "moon", "conjunction", "saravali", "waning_moon"],
     "Ch.15 v.30",
     "Sun-Moon conjunction with waning Moon (Krishna Amavasya): intensified "
     "malefic results, weak constitution, mental disturbance"),
    ("sun_moon", "conjunction_condition", "benefic_aspect_conjunction", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "moon", "conjunction", "saravali", "benefic_aspect"],
     "Ch.15 v.31",
     "Sun-Moon conjunction aspected by benefics (Jupiter/Venus): malefic "
     "effects greatly reduced, native rises to comfortable position"),
    ("sun_moon", "conjunction_condition", "malefic_aspect_conjunction", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["sun", "moon", "conjunction", "saravali", "malefic_aspect"],
     "Ch.15 v.32",
     "Sun-Moon conjunction aspected by malefics (Saturn/Mars): intensifies "
     "health problems, shortened life, poverty and suffering"),
    ("sun_moon", "conjunction_condition", "own_sign_sun", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.15 v.33",
     "Sun-Moon conjunction in Leo (Sun's own sign): Sun's dignity elevates "
     "results, leadership qualities manifest, government favor"),
    ("sun_moon", "conjunction_condition", "own_sign_moon", {},
     "favorable", "moderate",
     ["mental_health", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "own_sign", "cancer"],
     "Ch.15 v.34",
     "Sun-Moon conjunction in Cancer (Moon's own sign): emotional stability "
     "despite combustion, nurturing nature, maternal blessings"),
    ("sun_moon", "conjunction_condition", "exalted_sun", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "moon", "conjunction", "saravali", "exaltation", "aries"],
     "Ch.15 v.35",
     "Sun-Moon conjunction in Aries (Sun exalted): powerful personality, "
     "great authority, rises to commanding position despite new moon"),
    ("sun_moon", "conjunction_condition", "exalted_moon", {},
     "favorable", "moderate",
     ["wealth", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.15 v.36",
     "Sun-Moon conjunction in Taurus (Moon exalted): strong mind despite "
     "combustion, material prosperity, artistic sensibility"),
    ("sun_moon", "conjunction_condition", "debilitated_sun", {},
     "unfavorable", "strong",
     ["career_status", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "debilitation", "libra"],
     "Ch.15 v.37",
     "Sun-Moon conjunction in Libra (Sun debilitated): weak authority, "
     "servile nature intensified, dominated by spouse or partners"),
    ("sun_moon", "conjunction_condition", "debilitated_moon", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["sun", "moon", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.15 v.38",
     "Sun-Moon conjunction in Scorpio (Moon debilitated): severe mental "
     "affliction, chronic health issues, emotional instability"),
    ("sun_moon", "conjunction_condition", "jupiter_aspect_mitigating", {},
     "favorable", "moderate",
     ["spirituality", "intelligence_education"],
     ["sun", "moon", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.15 v.39",
     "Sun-Moon conjunction with Jupiter's aspect: spiritual wisdom despite "
     "new moon birth, protected from worst effects, learned nature"),
    ("sun_moon", "conjunction_condition", "saturn_aspect_intensifying", {},
     "unfavorable", "strong",
     ["longevity", "career_status"],
     ["sun", "moon", "conjunction", "saravali", "saturn_aspect"],
     "Ch.15 v.40",
     "Sun-Moon conjunction with Saturn's aspect: hardship and toil, delayed "
     "success, chronic ailments, longevity concerns intensified"),
    ("sun_moon", "conjunction_condition", "kendra_placement_general", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "moon", "conjunction", "saravali", "kendra"],
     "Ch.15 v.41",
     "Sun-Moon conjunction in any kendra (1/4/7/10): general principle — "
     "angular strength partially compensates combustion of Moon"),
    ("sun_moon", "conjunction_condition", "trikona_placement_general", {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["sun", "moon", "conjunction", "saravali", "trikona"],
     "Ch.15 v.42",
     "Sun-Moon conjunction in any trikona (1/5/9): trinal placement gives "
     "dharmic protection, some spiritual merit despite affliction"),
    ("sun_moon", "conjunction_condition", "dusthana_placement_general", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "mental_health"],
     ["sun", "moon", "conjunction", "saravali", "dusthana"],
     "Ch.15 v.43",
     "Sun-Moon conjunction in any dusthana (6/8/12): worst effects manifest, "
     "health and longevity severely compromised, poverty likely"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun-Mars Conjunction — Ch.16 (SAV044–SAV086)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_MARS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_mars", "conjunction_in_house", 1, {},
     "mixed", "strong",
     ["physical_health", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "1st_house"],
     "Ch.16 v.1",
     "Sun-Mars conjunction in 1st house: valorous and bold, fiery temperament, "
     "prone to wounds, scars, or burns on the body"),
    ("sun_mars", "conjunction_in_house", 1, {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "1st_house", "cruel"],
     "Ch.16 v.2",
     "Sun-Mars conjunction in 1st house: cruel disposition, engages in violent "
     "acts, creates enemies through aggressive behavior"),
    # House 2
    ("sun_mars", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "2nd_house"],
     "Ch.16 v.3",
     "Sun-Mars conjunction in 2nd house: harsh and unpleasant speech, "
     "quarrels over money, family discord over finances"),
    ("sun_mars", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["sun", "mars", "conjunction", "saravali", "2nd_house", "face"],
     "Ch.16 v.4",
     "Sun-Mars conjunction in 2nd house: diseases of the face or mouth, "
     "dental problems, scarred or marked facial features"),
    # House 3
    ("sun_mars", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["character_temperament", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "3rd_house"],
     "Ch.16 v.5",
     "Sun-Mars conjunction in 3rd house: extremely courageous, respected "
     "for bravery, heroic deeds bring fame and recognition"),
    ("sun_mars", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "mars", "conjunction", "saravali", "3rd_house", "wealth"],
     "Ch.16 v.6",
     "Sun-Mars conjunction in 3rd house: wealthy through own efforts, "
     "successful in competitive ventures, good rapport with siblings"),
    # House 4
    ("sun_mars", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "property_vehicles"],
     ["sun", "mars", "conjunction", "saravali", "4th_house"],
     "Ch.16 v.7",
     "Sun-Mars conjunction in 4th house: devoid of happiness, domestic strife, "
     "loss of property through fire or litigation"),
    ("sun_mars", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "4th_house", "heart"],
     "Ch.16 v.8",
     "Sun-Mars conjunction in 4th house: troubled heart, no peace of mind, "
     "constant conflict with family members and neighbors"),
    # House 5
    ("sun_mars", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["progeny", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "5th_house"],
     "Ch.16 v.9",
     "Sun-Mars conjunction in 5th house: enmity with own children, difficulty "
     "in progeny matters, harsh disciplinarian as parent"),
    ("sun_mars", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["wealth", "mental_health"],
     ["sun", "mars", "conjunction", "saravali", "5th_house", "unstable"],
     "Ch.16 v.10",
     "Sun-Mars conjunction in 5th house: unstable finances, speculative losses, "
     "anger clouds intellectual judgment"),
    # House 6
    ("sun_mars", "conjunction_in_house", 6, {},
     "favorable", "strong",
     ["enemies_litigation", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "6th_house"],
     "Ch.16 v.11",
     "Sun-Mars conjunction in 6th house: destroys all enemies, excels in "
     "competitive fields, fame through combative or surgical skill"),
    ("sun_mars", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "mars", "conjunction", "saravali", "6th_house", "king"],
     "Ch.16 v.12",
     "Sun-Mars conjunction in 6th house: attains a splendid position, "
     "may serve in military or enforcement, earns royal favor"),
    # House 7
    ("sun_mars", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "7th_house"],
     "Ch.16 v.13",
     "Sun-Mars conjunction in 7th house: quarrels with spouse, domineering "
     "in partnerships, marriage marked by conflict and separation"),
    ("sun_mars", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "physical_health"],
     ["sun", "mars", "conjunction", "saravali", "7th_house", "spouse_health"],
     "Ch.16 v.14",
     "Sun-Mars conjunction in 7th house: spouse suffers from fevers or "
     "inflammatory conditions, relationship brings physical stress"),
    # House 8
    ("sun_mars", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["sun", "mars", "conjunction", "saravali", "8th_house"],
     "Ch.16 v.15",
     "Sun-Mars conjunction in 8th house: shortened lifespan, danger from "
     "fire, weapons, or surgical operations, accident-prone"),
    ("sun_mars", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["wealth", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "8th_house", "theft"],
     "Ch.16 v.16",
     "Sun-Mars conjunction in 8th house: loss through theft or treachery, "
     "punished by authorities, legal troubles from violent incidents"),
    # House 9
    ("sun_mars", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["spirituality", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "9th_house"],
     "Ch.16 v.17",
     "Sun-Mars conjunction in 9th house: irreligious conduct, disrespects "
     "elders and preceptors, lacks devotion to tradition"),
    ("sun_mars", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "9th_house", "authority"],
     "Ch.16 v.18",
     "Sun-Mars conjunction in 9th house: may gain authority through "
     "forceful means, success in military or administrative career"),
    # House 10
    ("sun_mars", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "10th_house"],
     "Ch.16 v.19",
     "Sun-Mars conjunction in 10th house: renowned for brave deeds, attains "
     "high position, successful military or executive career"),
    ("sun_mars", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "mars", "conjunction", "saravali", "10th_house", "royal"],
     "Ch.16 v.20",
     "Sun-Mars conjunction in 10th house: earns wealth through royal or "
     "government patronage, commands respect in professional sphere"),
    # House 11
    ("sun_mars", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["sun", "mars", "conjunction", "saravali", "11th_house"],
     "Ch.16 v.21",
     "Sun-Mars conjunction in 11th house: abundant gains, wealthy, "
     "successful in competitive ventures, powerful social network"),
    ("sun_mars", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "11th_house", "leader"],
     "Ch.16 v.22",
     "Sun-Mars conjunction in 11th house: commands respect among friends "
     "and associates, natural leader in group settings"),
    # House 12
    ("sun_mars", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["wealth", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "12th_house"],
     "Ch.16 v.23",
     "Sun-Mars conjunction in 12th house: heavy expenditure, loss through "
     "enemies, punishment from authorities, financial ruin"),
    ("sun_mars", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["sun", "mars", "conjunction", "saravali", "12th_house", "eye"],
     "Ch.16 v.24",
     "Sun-Mars conjunction in 12th house: eye diseases, disturbed sleep, "
     "fevers and inflammatory disorders, hospitalization likely"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_mars", "conjunction_condition", "own_sign_sun_leo", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.16 v.25",
     "Sun-Mars conjunction in Leo (Sun's own sign): commanding authority, "
     "military leadership, administrative prowess amplified"),
    ("sun_mars", "conjunction_condition", "own_sign_mars_aries", {},
     "favorable", "strong",
     ["career_status", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.16 v.26",
     "Sun-Mars conjunction in Aries (Mars's own sign, Sun exalted): supreme "
     "courage, martial excellence, very powerful combination"),
    ("sun_mars", "conjunction_condition", "own_sign_mars_scorpio", {},
     "mixed", "strong",
     ["career_status", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.16 v.27",
     "Sun-Mars conjunction in Scorpio (Mars's own sign): investigative and "
     "secretive nature, success in occult or surgical fields"),
    ("sun_mars", "conjunction_condition", "exalted_mars_capricorn", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["sun", "mars", "conjunction", "saravali", "exaltation", "capricorn"],
     "Ch.16 v.28",
     "Sun-Mars conjunction in Capricorn (Mars exalted): disciplined warrior, "
     "high achievement in structured environments, wealth through effort"),
    ("sun_mars", "conjunction_condition", "debilitated_mars_cancer", {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "debilitation", "cancer"],
     "Ch.16 v.29",
     "Sun-Mars conjunction in Cancer (Mars debilitated): anger without courage, "
     "domestic violence tendencies, emotional instability"),
    ("sun_mars", "conjunction_condition", "debilitated_sun_libra", {},
     "unfavorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "debilitation", "libra"],
     "Ch.16 v.30",
     "Sun-Mars conjunction in Libra (Sun debilitated): aggression without "
     "authority, conflicts in partnerships, weakened leadership"),
    ("sun_mars", "conjunction_condition", "jupiter_aspect_mitigating", {},
     "favorable", "moderate",
     ["spirituality", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.16 v.31",
     "Sun-Mars conjunction aspected by Jupiter: cruelty tempered by wisdom, "
     "courage directed toward righteous causes, dharmic warrior"),
    ("sun_mars", "conjunction_condition", "saturn_aspect_intensifying", {},
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "saturn_aspect"],
     "Ch.16 v.32",
     "Sun-Mars conjunction aspected by Saturn: extreme malefic combination, "
     "danger from authorities, imprisonment, accidents intensified"),
    ("sun_mars", "conjunction_condition", "venus_aspect_softening", {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "venus_aspect"],
     "Ch.16 v.33",
     "Sun-Mars conjunction aspected by Venus: aggression softened in relationships, "
     "passionate but less destructive in marital matters"),
    ("sun_mars", "conjunction_condition", "kendra_strength", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "kendra"],
     "Ch.16 v.34",
     "Sun-Mars conjunction in any kendra (1/4/7/10): angular strength gives "
     "prominent results, both positive courage and negative aggression amplified"),
    ("sun_mars", "conjunction_condition", "trikona_placement", {},
     "mixed", "moderate",
     ["career_status", "spirituality"],
     ["sun", "mars", "conjunction", "saravali", "trikona"],
     "Ch.16 v.35",
     "Sun-Mars conjunction in any trikona (1/5/9): dharmic fire, courage "
     "directed toward righteous action, but impulsive spirituality"),
    ("sun_mars", "conjunction_condition", "dusthana_danger", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "dusthana"],
     "Ch.16 v.36",
     "Sun-Mars conjunction in any dusthana (6/8/12): double malefic in evil "
     "houses creates severe danger — accidents, surgeries, legal troubles"),
    ("sun_mars", "conjunction_condition", "mutual_friend_sign", {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "mars", "conjunction", "saravali", "friend_sign"],
     "Ch.16 v.37",
     "Sun-Mars conjunction in friendly sign (Sagittarius/Jupiter): fiery "
     "energy channeled constructively, leadership with moral compass"),
    ("sun_mars", "conjunction_condition", "enemy_sign_placement", {},
     "unfavorable", "strong",
     ["character_temperament", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "enemy_sign"],
     "Ch.16 v.38",
     "Sun-Mars conjunction in enemy sign: aggression misdirected, creates "
     "powerful enemies, legal battles, defeat in confrontations"),
    ("sun_mars", "conjunction_condition", "surgical_skill", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "mars", "conjunction", "saravali", "surgery", "skill"],
     "Ch.16 v.39",
     "Sun-Mars conjunction in good dignity: aptitude for surgery, metallurgy, "
     "or engineering — skilled with fire, metals, and sharp instruments"),
    ("sun_mars", "conjunction_condition", "military_career", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "conjunction", "saravali", "military", "career"],
     "Ch.16 v.40",
     "Sun-Mars conjunction well-placed: natural aptitude for military, police, "
     "or paramilitary service, commands respect through physical courage"),
    ("sun_mars", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "strong",
     ["longevity", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "rahu", "triple"],
     "Ch.16 v.41",
     "Sun-Mars conjunction joined by Rahu: extreme danger from fire, poison, "
     "or serpents, legal entanglements with severe consequences"),
    ("sun_mars", "conjunction_condition", "ketu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["spirituality", "mental_health"],
     ["sun", "mars", "conjunction", "saravali", "ketu", "triple"],
     "Ch.16 v.42",
     "Sun-Mars conjunction joined by Ketu: sudden events, spiritual crisis, "
     "wounds from mysterious causes, psychic disturbances"),
    ("sun_mars", "conjunction_condition", "upachaya_general", {},
     "favorable", "moderate",
     ["career_status", "enemies_litigation"],
     ["sun", "mars", "conjunction", "saravali", "upachaya"],
     "Ch.16 v.43",
     "Sun-Mars conjunction in upachaya houses (3/6/10/11): malefics thrive "
     "in growth houses — courage, competitive success, career gains"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Sun-Mercury Conjunction — Ch.16-17 (SAV087–SAV130)
# ═══════════════════════════════════════════════════════════════════════════════
_SUN_MERCURY_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("sun_mercury", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "1st_house"],
     "Ch.16 v.44",
     "Sun-Mercury conjunction in 1st house: learned and intelligent, sweet "
     "speech, good reputation for scholarly abilities"),
    ("sun_mercury", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "1st_house", "skilled"],
     "Ch.16 v.45",
     "Sun-Mercury conjunction in 1st house: skilled in arts and sciences, "
     "earns through intellectual work, respected for versatility"),
    # House 2
    ("sun_mercury", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "2nd_house"],
     "Ch.16 v.46",
     "Sun-Mercury conjunction in 2nd house: wealth through learned pursuits, "
     "eloquent and persuasive speech, earns through communication"),
    ("sun_mercury", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "2nd_house", "family"],
     "Ch.16 v.47",
     "Sun-Mercury conjunction in 2nd house: good family background, "
     "attractive appearance, poetic or literary talent"),
    # House 3
    ("sun_mercury", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["character_temperament", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "3rd_house"],
     "Ch.16 v.48",
     "Sun-Mercury conjunction in 3rd house: courageous and intelligent, "
     "excels in communication, successful in writing and media"),
    ("sun_mercury", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "3rd_house", "sibling"],
     "Ch.16 v.49",
     "Sun-Mercury conjunction in 3rd house: benefits from siblings, skilled "
     "in commerce, success through short journeys and trade"),
    # House 4
    ("sun_mercury", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "4th_house"],
     "Ch.16 v.50",
     "Sun-Mercury conjunction in 4th house: blessed with vehicles and "
     "property, learned in traditional sciences, good education"),
    ("sun_mercury", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["mental_health", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "4th_house", "mind"],
     "Ch.16 v.51",
     "Sun-Mercury conjunction in 4th house: restless mind, constantly "
     "planning, may lack domestic peace despite material comforts"),
    # House 5
    ("sun_mercury", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "5th_house"],
     "Ch.17 v.1",
     "Sun-Mercury conjunction in 5th house: exceptional intelligence, "
     "ministerial or advisory position, fame through scholarship"),
    ("sun_mercury", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "5th_house", "progeny"],
     "Ch.17 v.2",
     "Sun-Mercury conjunction in 5th house: intelligent children, success "
     "in speculation with calculated risks, creative brilliance"),
    # House 6
    ("sun_mercury", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "6th_house"],
     "Ch.17 v.3",
     "Sun-Mercury conjunction in 6th house: defeats enemies through "
     "intellectual strategy, but prone to nervous disorders"),
    ("sun_mercury", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "6th_house", "health"],
     "Ch.17 v.4",
     "Sun-Mercury conjunction in 6th house: skin diseases, digestive "
     "troubles, quarrelsome with maternal relatives"),
    # House 7
    ("sun_mercury", "conjunction_in_house", 7, {},
     "mixed", "moderate",
     ["marriage", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "7th_house"],
     "Ch.17 v.5",
     "Sun-Mercury conjunction in 7th house: learned spouse, intellectual "
     "partnership, but ego clashes in marriage"),
    ("sun_mercury", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "7th_house", "trade"],
     "Ch.17 v.6",
     "Sun-Mercury conjunction in 7th house: success in trade and business "
     "partnerships, commercial acumen, diplomatic skill"),
    # House 8
    ("sun_mercury", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["longevity", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "8th_house"],
     "Ch.17 v.7",
     "Sun-Mercury conjunction in 8th house: notoriety rather than fame, "
     "inheritance disputes, health concerns after middle age"),
    ("sun_mercury", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["intelligence_education", "spirituality"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "8th_house", "occult"],
     "Ch.17 v.8",
     "Sun-Mercury conjunction in 8th house: aptitude for occult sciences, "
     "research ability, but knowledge brings anxiety rather than peace"),
    # House 9
    ("sun_mercury", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "9th_house"],
     "Ch.17 v.9",
     "Sun-Mercury conjunction in 9th house: deeply learned in scriptures, "
     "virtuous conduct, fame through religious or philosophical writing"),
    ("sun_mercury", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "9th_house", "fortune"],
     "Ch.17 v.10",
     "Sun-Mercury conjunction in 9th house: fortunate in higher education, "
     "gains through father, patronage from learned institutions"),
    # House 10
    ("sun_mercury", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "10th_house"],
     "Ch.17 v.11",
     "Sun-Mercury conjunction in 10th house: eminent career in administration, "
     "commerce, or intellectual profession, widespread fame"),
    ("sun_mercury", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "10th_house", "commerce"],
     "Ch.17 v.12",
     "Sun-Mercury conjunction in 10th house: wealth through trade, accounting, "
     "or advisory roles, respected in professional community"),
    # House 11
    ("sun_mercury", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "11th_house"],
     "Ch.17 v.13",
     "Sun-Mercury conjunction in 11th house: abundant gains through intellect, "
     "profitable friendships, income from writing or teaching"),
    ("sun_mercury", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "11th_house", "truth"],
     "Ch.17 v.14",
     "Sun-Mercury conjunction in 11th house: truthful and principled, "
     "respected for integrity, honored by scholarly communities"),
    # House 12
    ("sun_mercury", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "12th_house"],
     "Ch.17 v.15",
     "Sun-Mercury conjunction in 12th house: intelligence not fully utilized, "
     "expenditure on education, may settle in foreign lands"),
    ("sun_mercury", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "foreign_travel"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya", "12th_house", "foreign"],
     "Ch.17 v.16",
     "Sun-Mercury conjunction in 12th house: spiritual learning in isolation, "
     "success in foreign lands, earnings spent on charitable causes"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("sun_mercury", "conjunction_condition", "budhaditya_yoga_proper", {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "budhaditya_yoga"],
     "Ch.17 v.17",
     "Budhaditya Yoga (Sun-Mercury conjunction in good dignity): exceptional "
     "intellect, fame through learning, advisory or ministerial position"),
    ("sun_mercury", "conjunction_condition", "mercury_combust", {},
     "unfavorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "combust"],
     "Ch.17 v.18",
     "Mercury combust by Sun (within 14 degrees): intellectual abilities "
     "suppressed, nervous disposition, speech defects or stammering"),
    ("sun_mercury", "conjunction_condition", "mercury_cazimi", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "cazimi"],
     "Ch.17 v.19",
     "Mercury cazimi (within 1 degree of Sun): extraordinarily empowered "
     "intellect, direct communication with authority, brilliant mind"),
    ("sun_mercury", "conjunction_condition", "own_sign_mercury_gemini", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.17 v.20",
     "Sun-Mercury conjunction in Gemini (Mercury's own sign): superb "
     "communication skills, success in commerce, literary fame"),
    ("sun_mercury", "conjunction_condition", "own_sign_mercury_virgo", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.17 v.21",
     "Sun-Mercury conjunction in Virgo (Mercury exalted + own): analytical "
     "genius, precision in work, excellence in mathematics or science"),
    ("sun_mercury", "conjunction_condition", "own_sign_sun_leo", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "own_sign", "leo"],
     "Ch.17 v.22",
     "Sun-Mercury conjunction in Leo (Sun's own sign): authoritative "
     "intellect, leadership through knowledge, government scholarship"),
    ("sun_mercury", "conjunction_condition", "debilitated_mercury_pisces", {},
     "unfavorable", "moderate",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "debilitation", "pisces"],
     "Ch.17 v.23",
     "Sun-Mercury conjunction in Pisces (Mercury debilitated): confused "
     "thinking, poor analytical skills, intellectual potential unrealized"),
    ("sun_mercury", "conjunction_condition", "debilitated_sun_libra", {},
     "mixed", "moderate",
     ["career_status", "marriage"],
     ["sun", "mercury", "conjunction", "saravali", "debilitation", "libra"],
     "Ch.17 v.24",
     "Sun-Mercury conjunction in Libra (Sun debilitated): diplomatic "
     "intelligence but weak authority, success through partnerships"),
    ("sun_mercury", "conjunction_condition", "jupiter_aspect_wisdom", {},
     "favorable", "strong",
     ["intelligence_education", "spirituality"],
     ["sun", "mercury", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.17 v.25",
     "Sun-Mercury conjunction aspected by Jupiter: profound wisdom, "
     "scholarly eminence, combines analytical and intuitive intelligence"),
    ("sun_mercury", "conjunction_condition", "saturn_aspect_discipline", {},
     "mixed", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "saturn_aspect"],
     "Ch.17 v.26",
     "Sun-Mercury conjunction aspected by Saturn: disciplined but slow "
     "intellect, success in technical or research fields after delay"),
    ("sun_mercury", "conjunction_condition", "mars_aspect_sharpness", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "mars_aspect"],
     "Ch.17 v.27",
     "Sun-Mercury conjunction aspected by Mars: sharp and incisive mind, "
     "argumentative, skilled in debate but creates intellectual enemies"),
    ("sun_mercury", "conjunction_condition", "venus_conjunction_triple", {},
     "favorable", "moderate",
     ["wealth", "physical_appearance"],
     ["sun", "mercury", "conjunction", "saravali", "venus", "triple"],
     "Ch.17 v.28",
     "Sun-Mercury conjunction joined by Venus: artistic intelligence, "
     "beautiful speech, success in arts, entertainment, or design"),
    ("sun_mercury", "conjunction_condition", "kendra_placement", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["sun", "mercury", "conjunction", "saravali", "kendra"],
     "Ch.17 v.29",
     "Sun-Mercury conjunction in any kendra (1/4/7/10): Budhaditya yoga "
     "gains angular strength, intellectual abilities widely recognized"),
    ("sun_mercury", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["sun", "mercury", "conjunction", "saravali", "trikona"],
     "Ch.17 v.30",
     "Sun-Mercury conjunction in any trikona (1/5/9): dharmic intellect, "
     "scholarly merit brings fortune, scriptural knowledge"),
    ("sun_mercury", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "dusthana"],
     "Ch.17 v.31",
     "Sun-Mercury conjunction in any dusthana (6/8/12): intellect wasted "
     "on trivial matters, nervous ailments, career disappointments"),
    ("sun_mercury", "conjunction_condition", "commerce_skill", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["sun", "mercury", "conjunction", "saravali", "commerce", "trade"],
     "Ch.17 v.32",
     "Sun-Mercury conjunction in good dignity: natural aptitude for commerce, "
     "accounting, trade, and financial management"),
    ("sun_mercury", "conjunction_condition", "writing_skill", {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["sun", "mercury", "conjunction", "saravali", "writing", "literature"],
     "Ch.17 v.33",
     "Sun-Mercury conjunction well-placed: skilled writer, author, or orator, "
     "fame through literary or journalistic work"),
    ("sun_mercury", "conjunction_condition", "retrograde_mercury", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "mercury", "conjunction", "saravali", "retrograde"],
     "Ch.17 v.34",
     "Sun-Mercury conjunction with retrograde Mercury: unconventional thinking, "
     "revisits old ideas, delayed but original intellectual contributions"),
    ("sun_mercury", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "mercury", "conjunction", "saravali", "upachaya"],
     "Ch.17 v.35",
     "Sun-Mercury conjunction in upachaya houses (3/6/10/11): intellectual "
     "abilities grow with age, progressive gains through communication skills"),
    ("sun_mercury", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["sun", "mercury", "conjunction", "saravali", "rahu", "triple"],
     "Ch.17 v.36",
     "Sun-Mercury conjunction joined by Rahu: deceptive intellect, cunning "
     "speech used for manipulation, nervous disorders, fraudulent tendencies"),
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
    sun_moon = _make_conjunction_rules(
        "sun_moon", ["sun", "moon"], _SUN_MOON_DATA, 1, "Ch.15",
    )
    sun_mars = _make_conjunction_rules(
        "sun_mars", ["sun", "mars"], _SUN_MARS_DATA, 44, "Ch.16",
    )
    sun_mercury = _make_conjunction_rules(
        "sun_mercury", ["sun", "mercury"], _SUN_MERCURY_DATA, 87, "Ch.16-17",
    )
    return sun_moon + sun_mars + sun_mercury


SARAVALI_CONJUNCTIONS_1_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_1_REGISTRY.add(_rule)
