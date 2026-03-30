"""src/corpus/saravali_conjunctions_3.py — S275: Saravali two-planet conjunctions.

SAV261–SAV390 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three conjunction pairs from Saravali Chapters 17-19:
  Moon-Mars    (Ch.17-18) — SAV261–SAV303 (43 rules)
  Moon-Mercury (Ch.18)    — SAV304–SAV346 (43 rules)
  Moon-Jupiter (Ch.18-19) — SAV347–SAV390 (44 rules)

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
# Moon-Mars Conjunction — Ch.17-18 (SAV261–SAV303)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_MARS_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("moon_mars", "conjunction_in_house", 1, {},
     "mixed", "strong",
     ["character_temperament", "physical_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "1st_house"],
     "Ch.17 v.37",
     "Moon-Mars conjunction in 1st house: courageous and bold temperament, "
     "emotional intensity, prone to inflammatory ailments and scars"),
    ("moon_mars", "conjunction_in_house", 1, {},
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "1st_house", "self_effort"],
     "Ch.17 v.38",
     "Moon-Mars conjunction in 1st house: wealth earned through self-effort "
     "and courage, enterprising nature, independent livelihood"),
    # House 2
    ("moon_mars", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["wealth", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "2nd_house"],
     "Ch.17 v.39",
     "Moon-Mars conjunction in 2nd house: harsh speech driven by emotional "
     "impulse, quarrels over finances, family discord"),
    ("moon_mars", "conjunction_in_house", 2, {},
     "unfavorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "2nd_house", "face"],
     "Ch.17 v.40",
     "Moon-Mars conjunction in 2nd house: afflicted face or eyes, "
     "dental problems, blood-related disorders affecting mouth region"),
    # House 3
    ("moon_mars", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["character_temperament", "fame_reputation"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "3rd_house"],
     "Ch.17 v.41",
     "Moon-Mars conjunction in 3rd house: emotionally courageous, bold "
     "among peers, heroic temperament earns public recognition"),
    ("moon_mars", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "3rd_house", "sibling"],
     "Ch.17 v.42",
     "Moon-Mars conjunction in 3rd house: gains through valorous deeds, "
     "beneficial sibling relationships, success in competitive ventures"),
    # House 4
    ("moon_mars", "conjunction_in_house", 4, {},
     "unfavorable", "strong",
     ["mental_health", "property_vehicles"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "4th_house"],
     "Ch.17 v.43",
     "Moon-Mars conjunction in 4th house: emotional turbulence in domestic life, "
     "loss of property through fire or disputes, no peace at home"),
    ("moon_mars", "conjunction_in_house", 4, {},
     "unfavorable", "moderate",
     ["character_temperament", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "4th_house", "mother"],
     "Ch.18 v.1",
     "Moon-Mars conjunction in 4th house: strained relationship with mother, "
     "emotional volatility disrupts domestic happiness"),
    # House 5
    ("moon_mars", "conjunction_in_house", 5, {},
     "unfavorable", "moderate",
     ["progeny", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "5th_house"],
     "Ch.18 v.2",
     "Moon-Mars conjunction in 5th house: emotional conflicts regarding children, "
     "harsh disciplinarian, impulsive decisions in speculative matters"),
    ("moon_mars", "conjunction_in_house", 5, {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "5th_house", "intellect"],
     "Ch.18 v.3",
     "Moon-Mars conjunction in 5th house: sharp but emotionally driven intellect, "
     "creative energy channeled through passionate pursuits"),
    # House 6
    ("moon_mars", "conjunction_in_house", 6, {},
     "favorable", "strong",
     ["enemies_litigation", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "6th_house"],
     "Ch.18 v.4",
     "Moon-Mars conjunction in 6th house: conquers enemies through emotional "
     "determination, success in competitive and combative fields"),
    ("moon_mars", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "6th_house", "health"],
     "Ch.18 v.5",
     "Moon-Mars conjunction in 6th house: blood disorders, fevers, inflammatory "
     "conditions, emotional stress manifesting as physical ailments"),
    # House 7
    ("moon_mars", "conjunction_in_house", 7, {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "7th_house"],
     "Ch.18 v.6",
     "Moon-Mars conjunction in 7th house: Manglik dosha intensified by Moon, "
     "emotional aggression in marriage, frequent domestic quarrels"),
    ("moon_mars", "conjunction_in_house", 7, {},
     "unfavorable", "moderate",
     ["marriage", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "7th_house", "spouse"],
     "Ch.18 v.7",
     "Moon-Mars conjunction in 7th house: spouse suffers emotional distress, "
     "jealousy and possessiveness destabilize partnership"),
    # House 8
    ("moon_mars", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "8th_house"],
     "Ch.18 v.8",
     "Moon-Mars conjunction in 8th house: shortened lifespan, danger from "
     "blood disorders, accidents involving water or fire"),
    ("moon_mars", "conjunction_in_house", 8, {},
     "unfavorable", "strong",
     ["mental_health", "wealth"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "8th_house", "loss"],
     "Ch.18 v.9",
     "Moon-Mars conjunction in 8th house: severe emotional crises, loss of "
     "inheritance, hidden enemies cause financial devastation"),
    # House 9
    ("moon_mars", "conjunction_in_house", 9, {},
     "unfavorable", "moderate",
     ["spirituality", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "9th_house"],
     "Ch.18 v.10",
     "Moon-Mars conjunction in 9th house: emotional conflict with father or "
     "preceptor, impulsive religious views, lacks sustained devotion"),
    ("moon_mars", "conjunction_in_house", 9, {},
     "mixed", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "9th_house", "fortune"],
     "Ch.18 v.11",
     "Moon-Mars conjunction in 9th house: some fortune through courage and "
     "determination, but luck is unstable and dependent on emotional state"),
    # House 10
    ("moon_mars", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "10th_house"],
     "Ch.18 v.12",
     "Moon-Mars conjunction in 10th house: courageous leader, fame through "
     "bold undertakings, successful in military or administrative career"),
    ("moon_mars", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "10th_house", "wealth"],
     "Ch.18 v.13",
     "Moon-Mars conjunction in 10th house: wealth through self-effort and "
     "enterprising ventures, commands authority in profession"),
    # House 11
    ("moon_mars", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "11th_house"],
     "Ch.18 v.14",
     "Moon-Mars conjunction in 11th house: Chandra-Mangal Yoga bears full "
     "fruit, abundant gains through courage and self-effort"),
    ("moon_mars", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "11th_house", "friends"],
     "Ch.18 v.15",
     "Moon-Mars conjunction in 11th house: respected among friends for boldness, "
     "gains through elder siblings, powerful social connections"),
    # House 12
    ("moon_mars", "conjunction_in_house", 12, {},
     "unfavorable", "strong",
     ["wealth", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "12th_house"],
     "Ch.18 v.16",
     "Moon-Mars conjunction in 12th house: heavy expenditure due to emotional "
     "impulsiveness, disturbed sleep, hospitalization from injuries"),
    ("moon_mars", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal", "12th_house", "eye"],
     "Ch.18 v.17",
     "Moon-Mars conjunction in 12th house: eye troubles, blood-related "
     "ailments, hidden enemies cause emotional and financial damage"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("moon_mars", "conjunction_condition", "chandra_mangal_yoga", {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["moon", "mars", "conjunction", "saravali", "chandra_mangal_yoga"],
     "Ch.18 v.18",
     "Chandra-Mangal Yoga (Moon-Mars conjunction in good dignity): wealth "
     "through self-effort, courage in financial matters, enterprising nature"),
    ("moon_mars", "conjunction_condition", "own_sign_mars_aries", {},
     "favorable", "strong",
     ["career_status", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "own_sign", "aries"],
     "Ch.18 v.19",
     "Moon-Mars conjunction in Aries (Mars's own sign): martial courage "
     "amplified, emotionally fearless, bold leadership abilities"),
    ("moon_mars", "conjunction_condition", "own_sign_mars_scorpio", {},
     "mixed", "strong",
     ["career_status", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "own_sign", "scorpio"],
     "Ch.18 v.20",
     "Moon-Mars conjunction in Scorpio (Mars's own sign): emotional intensity "
     "deepened, investigative mind, success in occult or surgical fields"),
    ("moon_mars", "conjunction_condition", "own_sign_moon_cancer", {},
     "mixed", "strong",
     ["mental_health", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "own_sign", "cancer"],
     "Ch.18 v.21",
     "Moon-Mars conjunction in Cancer (Moon's own sign): emotional warfare, "
     "protective aggression, fierce defense of family and home"),
    ("moon_mars", "conjunction_condition", "exalted_moon_taurus", {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.18 v.22",
     "Moon-Mars conjunction in Taurus (Moon exalted): emotional stability "
     "supports courageous action, material gains through determination"),
    ("moon_mars", "conjunction_condition", "exalted_mars_capricorn", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["moon", "mars", "conjunction", "saravali", "exaltation", "capricorn"],
     "Ch.18 v.23",
     "Moon-Mars conjunction in Capricorn (Mars exalted): disciplined courage, "
     "high achievement in structured environments, executive ability"),
    ("moon_mars", "conjunction_condition", "debilitated_moon_scorpio", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["moon", "mars", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.18 v.24",
     "Moon-Mars conjunction in Scorpio (Moon debilitated): severe emotional "
     "disturbance, obsessive tendencies, chronic health issues"),
    ("moon_mars", "conjunction_condition", "debilitated_mars_cancer", {},
     "unfavorable", "strong",
     ["character_temperament", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "debilitation", "cancer"],
     "Ch.18 v.25",
     "Moon-Mars conjunction in Cancer (Mars debilitated): anger without "
     "constructive outlet, emotional volatility, domestic strife"),
    ("moon_mars", "conjunction_condition", "watery_sign_placement", {},
     "unfavorable", "moderate",
     ["mental_health", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "watery_sign"],
     "Ch.18 v.26",
     "Moon-Mars conjunction in watery signs (Cancer/Scorpio/Pisces): emotional "
     "turbulence amplified, mood swings, inner conflict and restlessness"),
    ("moon_mars", "conjunction_condition", "fire_sign_placement", {},
     "favorable", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "fire_sign"],
     "Ch.18 v.27",
     "Moon-Mars conjunction in fire signs (Aries/Leo/Sagittarius): energized "
     "courage, emotional passion channeled into action, dynamic leadership"),
    ("moon_mars", "conjunction_condition", "manglik_dosha_intensified", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "manglik", "emotional_mars"],
     "Ch.18 v.28",
     "Moon-Mars conjunction intensifying Manglik dosha: emotional Mars creates "
     "deeper marital friction, possessiveness and jealousy in relationships"),
    ("moon_mars", "conjunction_condition", "jupiter_aspect_mitigating", {},
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["moon", "mars", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.18 v.29",
     "Moon-Mars conjunction aspected by Jupiter: aggression tempered by wisdom, "
     "emotional courage directed toward dharmic and charitable causes"),
    ("moon_mars", "conjunction_condition", "saturn_aspect_intensifying", {},
     "unfavorable", "strong",
     ["mental_health", "longevity"],
     ["moon", "mars", "conjunction", "saravali", "saturn_aspect"],
     "Ch.18 v.30",
     "Moon-Mars conjunction aspected by Saturn: extreme emotional hardship, "
     "depression combined with suppressed anger, chronic health problems"),
    ("moon_mars", "conjunction_condition", "kendra_strength", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "kendra"],
     "Ch.18 v.31",
     "Moon-Mars conjunction in any kendra (1/4/7/10): angular strength amplifies "
     "both courageous leadership and emotional volatility"),
    ("moon_mars", "conjunction_condition", "trikona_placement", {},
     "mixed", "moderate",
     ["wealth", "spirituality"],
     ["moon", "mars", "conjunction", "saravali", "trikona"],
     "Ch.18 v.32",
     "Moon-Mars conjunction in any trikona (1/5/9): dharmic fire with emotional "
     "underpinning, fortune through courageous initiatives"),
    ("moon_mars", "conjunction_condition", "dusthana_danger", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "mental_health"],
     ["moon", "mars", "conjunction", "saravali", "dusthana"],
     "Ch.18 v.33",
     "Moon-Mars conjunction in any dusthana (6/8/12): severe emotional and "
     "physical affliction, blood disorders, accidents, mental anguish"),
    ("moon_mars", "conjunction_condition", "upachaya_general", {},
     "favorable", "moderate",
     ["career_status", "enemies_litigation"],
     ["moon", "mars", "conjunction", "saravali", "upachaya"],
     "Ch.18 v.34",
     "Moon-Mars conjunction in upachaya houses (3/6/10/11): emotional courage "
     "grows with age, competitive success, progressive career gains"),
    ("moon_mars", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "strong",
     ["mental_health", "enemies_litigation"],
     ["moon", "mars", "conjunction", "saravali", "rahu", "triple"],
     "Ch.18 v.35",
     "Moon-Mars conjunction joined by Rahu: extreme emotional turbulence, "
     "irrational anger, danger from poisoning or treacherous enemies"),
    ("moon_mars", "conjunction_condition", "venus_aspect_softening", {},
     "mixed", "moderate",
     ["marriage", "character_temperament"],
     ["moon", "mars", "conjunction", "saravali", "venus_aspect"],
     "Ch.18 v.36",
     "Moon-Mars conjunction aspected by Venus: emotional aggression softened "
     "in relationships, passionate but more harmonious marital life"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon-Mercury Conjunction — Ch.18 (SAV304–SAV346)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_MERCURY_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("moon_mercury", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "1st_house"],
     "Ch.18 v.35",
     "Moon-Mercury conjunction in 1st house: sharp communicator, eloquent speech, "
     "imaginative mind with practical application"),
    ("moon_mercury", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "1st_house", "skilled"],
     "Ch.18 v.36",
     "Moon-Mercury conjunction in 1st house: skilled in arts and writing, "
     "pleasant personality, earns through intellectual versatility"),
    # House 2
    ("moon_mercury", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "2nd_house"],
     "Ch.18 v.37",
     "Moon-Mercury conjunction in 2nd house: wealth through commercial mind, "
     "persuasive and sweet speech, earns through communication"),
    ("moon_mercury", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "2nd_house", "family"],
     "Ch.18 v.38",
     "Moon-Mercury conjunction in 2nd house: cultured family background, "
     "poetic talent, attractive voice and literary sensibility"),
    # House 3
    ("moon_mercury", "conjunction_in_house", 3, {},
     "favorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "3rd_house"],
     "Ch.18 v.39",
     "Moon-Mercury conjunction in 3rd house: exceptional writing ability, "
     "excels in media and communication, mentally agile"),
    ("moon_mercury", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "3rd_house", "commerce"],
     "Ch.18 v.40",
     "Moon-Mercury conjunction in 3rd house: success in commerce and trade, "
     "benefits from short journeys, profitable sibling relationships"),
    # House 4
    ("moon_mercury", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["property_vehicles", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "4th_house"],
     "Ch.18 v.41",
     "Moon-Mercury conjunction in 4th house: blessed with vehicles and comfort, "
     "learned in traditional arts, good foundational education"),
    ("moon_mercury", "conjunction_in_house", 4, {},
     "mixed", "moderate",
     ["mental_health", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "4th_house", "mind"],
     "Ch.18 v.42",
     "Moon-Mercury conjunction in 4th house: restless and imaginative mind, "
     "emotional thinking patterns, creative but anxious disposition"),
    # House 5
    ("moon_mercury", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "5th_house"],
     "Ch.18 v.43",
     "Moon-Mercury conjunction in 5th house: exceptional creative intelligence, "
     "advisory capability, fame through literary or scholarly work"),
    ("moon_mercury", "conjunction_in_house", 5, {},
     "favorable", "moderate",
     ["progeny", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "5th_house", "progeny"],
     "Ch.18 v.44",
     "Moon-Mercury conjunction in 5th house: intelligent children, success "
     "in creative speculation, inventive and imaginative thinking"),
    # House 6
    ("moon_mercury", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["enemies_litigation", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "6th_house"],
     "Ch.18 v.45",
     "Moon-Mercury conjunction in 6th house: defeats enemies through clever "
     "strategy and emotional intelligence, but prone to anxiety disorders"),
    ("moon_mercury", "conjunction_in_house", 6, {},
     "unfavorable", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "6th_house", "health"],
     "Ch.18 v.46",
     "Moon-Mercury conjunction in 6th house: nervous ailments, digestive "
     "troubles from worry, skin conditions aggravated by emotional stress"),
    # House 7
    ("moon_mercury", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["marriage", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "7th_house"],
     "Ch.18 v.47",
     "Moon-Mercury conjunction in 7th house: intellectually compatible spouse, "
     "communication-based partnership, diplomatic in relationships"),
    ("moon_mercury", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "7th_house", "trade"],
     "Ch.18 v.48",
     "Moon-Mercury conjunction in 7th house: success in trade and commercial "
     "partnerships, earns through public dealings and negotiation"),
    # House 8
    ("moon_mercury", "conjunction_in_house", 8, {},
     "unfavorable", "moderate",
     ["longevity", "mental_health"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "8th_house"],
     "Ch.18 v.49",
     "Moon-Mercury conjunction in 8th house: anxious mind, chronic worry "
     "about hidden matters, health concerns after middle age"),
    ("moon_mercury", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["intelligence_education", "spirituality"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "8th_house", "occult"],
     "Ch.18 v.50",
     "Moon-Mercury conjunction in 8th house: aptitude for occult and mystical "
     "studies, intuitive research ability, but knowledge breeds anxiety"),
    # House 9
    ("moon_mercury", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "9th_house"],
     "Ch.18 v.51",
     "Moon-Mercury conjunction in 9th house: philosophical mind, learned in "
     "scriptures, fame through religious or devotional writing"),
    ("moon_mercury", "conjunction_in_house", 9, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "9th_house", "fortune"],
     "Ch.18 v.52",
     "Moon-Mercury conjunction in 9th house: fortunate in higher education, "
     "gains through teaching, patronage from scholarly institutions"),
    # House 10
    ("moon_mercury", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "10th_house"],
     "Ch.18 v.53",
     "Moon-Mercury conjunction in 10th house: eminent career in writing, "
     "commerce, or public communication, widespread professional fame"),
    ("moon_mercury", "conjunction_in_house", 10, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "10th_house", "commerce"],
     "Ch.18 v.54",
     "Moon-Mercury conjunction in 10th house: wealth through trade, accounting, "
     "or advisory roles, emotionally attuned to public needs"),
    # House 11
    ("moon_mercury", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "11th_house"],
     "Ch.18 v.55",
     "Moon-Mercury conjunction in 11th house: abundant gains through intellect "
     "and emotional intelligence, profitable friendships and networks"),
    ("moon_mercury", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "11th_house", "truth"],
     "Ch.18 v.56",
     "Moon-Mercury conjunction in 11th house: truthful and articulate, "
     "respected for integrity, honored in literary and scholarly circles"),
    # House 12
    ("moon_mercury", "conjunction_in_house", 12, {},
     "unfavorable", "moderate",
     ["wealth", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "12th_house"],
     "Ch.18 v.57",
     "Moon-Mercury conjunction in 12th house: intellect not fully utilized, "
     "excessive mental wandering, expenditure on education or travel"),
    ("moon_mercury", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "foreign_travel"],
     ["moon", "mercury", "conjunction", "saravali", "chandra_budha", "12th_house", "foreign"],
     "Ch.18 v.58",
     "Moon-Mercury conjunction in 12th house: imaginative writing in solitude, "
     "success in foreign lands, poetic or mystical contemplation"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("moon_mercury", "conjunction_condition", "own_sign_mercury_gemini", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["moon", "mercury", "conjunction", "saravali", "own_sign", "gemini"],
     "Ch.18 v.59",
     "Moon-Mercury conjunction in Gemini (Mercury's own sign): scholarly "
     "brilliance, superb communication skills, literary fame"),
    ("moon_mercury", "conjunction_condition", "own_sign_mercury_virgo", {},
     "favorable", "strong",
     ["intelligence_education", "career_status"],
     ["moon", "mercury", "conjunction", "saravali", "own_sign", "virgo"],
     "Ch.18 v.60",
     "Moon-Mercury conjunction in Virgo (Mercury exalted + own): analytical "
     "precision combined with emotional intuition, scholarly excellence"),
    ("moon_mercury", "conjunction_condition", "own_sign_moon_cancer", {},
     "favorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "own_sign", "cancer"],
     "Ch.18 v.61",
     "Moon-Mercury conjunction in Cancer (Moon's own sign): imaginative writing, "
     "poetic mind, emotional depth enriches intellectual expression"),
    ("moon_mercury", "conjunction_condition", "exalted_moon_taurus", {},
     "favorable", "strong",
     ["intelligence_education", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.18 v.62",
     "Moon-Mercury conjunction in Taurus (Moon exalted): stable and creative "
     "mind, artistic sensibility enhances commercial acumen"),
    ("moon_mercury", "conjunction_condition", "debilitated_moon_scorpio", {},
     "unfavorable", "moderate",
     ["mental_health", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.18 v.63",
     "Moon-Mercury conjunction in Scorpio (Moon debilitated): obsessive "
     "thinking, anxious intellect, communication marred by suspicion"),
    ("moon_mercury", "conjunction_condition", "debilitated_mercury_pisces", {},
     "unfavorable", "moderate",
     ["intelligence_education", "career_status"],
     ["moon", "mercury", "conjunction", "saravali", "debilitation", "pisces"],
     "Ch.18 v.64",
     "Moon-Mercury conjunction in Pisces (Mercury debilitated): confused "
     "thinking, dreamy intellect, analytical skills undermined by emotion"),
    ("moon_mercury", "conjunction_condition", "jupiter_aspect_wisdom", {},
     "favorable", "strong",
     ["intelligence_education", "spirituality"],
     ["moon", "mercury", "conjunction", "saravali", "jupiter_aspect"],
     "Ch.18 v.65",
     "Moon-Mercury conjunction aspected by Jupiter: philosophical communication, "
     "profound wisdom, combines emotional and analytical intelligence"),
    ("moon_mercury", "conjunction_condition", "saturn_aspect_melancholy", {},
     "mixed", "moderate",
     ["intelligence_education", "mental_health"],
     ["moon", "mercury", "conjunction", "saravali", "saturn_aspect"],
     "Ch.18 v.66",
     "Moon-Mercury conjunction aspected by Saturn: melancholic but deep thinking, "
     "disciplined intellect, success in research after prolonged effort"),
    ("moon_mercury", "conjunction_condition", "venus_aspect_artistic", {},
     "favorable", "moderate",
     ["intelligence_education", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "venus_aspect"],
     "Ch.18 v.67",
     "Moon-Mercury conjunction aspected by Venus: artistic and musical talent, "
     "beautiful expression, success in creative and aesthetic fields"),
    ("moon_mercury", "conjunction_condition", "mars_aspect_sharpness", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "mars_aspect"],
     "Ch.18 v.68",
     "Moon-Mercury conjunction aspected by Mars: sharp and incisive mind, "
     "argumentative speech, skilled in debate but creates opponents"),
    ("moon_mercury", "conjunction_condition", "kendra_placement", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["moon", "mercury", "conjunction", "saravali", "kendra"],
     "Ch.18 v.69",
     "Moon-Mercury conjunction in any kendra (1/4/7/10): mental agility "
     "gains angular strength, communication abilities widely recognized"),
    ("moon_mercury", "conjunction_condition", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["moon", "mercury", "conjunction", "saravali", "trikona"],
     "Ch.18 v.70",
     "Moon-Mercury conjunction in any trikona (1/5/9): dharmic intellect, "
     "scholarly merit brings fortune, devotional writing ability"),
    ("moon_mercury", "conjunction_condition", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["moon", "mercury", "conjunction", "saravali", "dusthana"],
     "Ch.18 v.71",
     "Moon-Mercury conjunction in any dusthana (6/8/12): intellect burdened "
     "by anxiety, nervous ailments, overthinking and career obstacles"),
    ("moon_mercury", "conjunction_condition", "upachaya_placement", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "upachaya"],
     "Ch.18 v.72",
     "Moon-Mercury conjunction in upachaya houses (3/6/10/11): communication "
     "skills sharpen with age, progressive gains through commerce and writing"),
    ("moon_mercury", "conjunction_condition", "writing_skill", {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["moon", "mercury", "conjunction", "saravali", "writing", "literature"],
     "Ch.18 v.73",
     "Moon-Mercury conjunction well-placed: exceptional writing ability, "
     "imaginative literature, poetic expression brings fame"),
    ("moon_mercury", "conjunction_condition", "commerce_skill", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "mercury", "conjunction", "saravali", "commerce", "trade"],
     "Ch.18 v.74",
     "Moon-Mercury conjunction in good dignity: natural commercial instinct, "
     "emotional intelligence applied to trade and negotiation"),
    ("moon_mercury", "conjunction_condition", "rahu_conjunction_triple", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["moon", "mercury", "conjunction", "saravali", "rahu", "triple"],
     "Ch.18 v.75",
     "Moon-Mercury conjunction joined by Rahu: deceptive communication, "
     "manipulative intellect, nervous disorders and anxiety amplified"),
    ("moon_mercury", "conjunction_condition", "retrograde_mercury", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "conjunction", "saravali", "retrograde"],
     "Ch.18 v.76",
     "Moon-Mercury conjunction with retrograde Mercury: unconventional thinking, "
     "revisits old ideas, delayed but emotionally rich intellectual output"),
    ("moon_mercury", "conjunction_condition", "full_moon_conjunction", {},
     "favorable", "moderate",
     ["intelligence_education", "wealth"],
     ["moon", "mercury", "conjunction", "saravali", "full_moon"],
     "Ch.18 v.77",
     "Moon-Mercury conjunction with full Moon: mental faculties at peak strength, "
     "sharp memory and vivid imagination support commercial success"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Moon-Jupiter Conjunction — Ch.18-19 (SAV347–SAV390)
# ═══════════════════════════════════════════════════════════════════════════════
_MOON_JUPITER_DATA = [
    # ── House placements (12 houses × ~2-3 outcomes) ─────────────────────────
    # House 1
    ("moon_jupiter", "conjunction_in_house", 1, {},
     "favorable", "strong",
     ["character_temperament", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "1st_house"],
     "Ch.18 v.72",
     "Moon-Jupiter conjunction in 1st house: Gajakesari Yoga variant, noble and "
     "wise personality, fame and respect from birth, virtuous character"),
    ("moon_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["physical_health", "physical_appearance"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "1st_house", "body"],
     "Ch.18 v.73",
     "Moon-Jupiter conjunction in 1st house: handsome and well-built body, "
     "radiant complexion, robust health and magnetic personality"),
    ("moon_jupiter", "conjunction_in_house", 1, {},
     "favorable", "moderate",
     ["intelligence_education", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "1st_house", "wisdom"],
     "Ch.18 v.74",
     "Moon-Jupiter conjunction in 1st house: deeply learned and spiritually "
     "inclined, emotional intelligence of the highest order"),
    # House 2
    ("moon_jupiter", "conjunction_in_house", 2, {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "2nd_house"],
     "Ch.18 v.75",
     "Moon-Jupiter conjunction in 2nd house: eloquent and truthful speech, "
     "accumulated wealth, prosperous and generous family life"),
    ("moon_jupiter", "conjunction_in_house", 2, {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "2nd_house", "learning"],
     "Ch.18 v.76",
     "Moon-Jupiter conjunction in 2nd house: learned in scriptures, sweet and "
     "persuasive voice, fame through teaching or scholarly discourse"),
    # House 3
    ("moon_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "3rd_house"],
     "Ch.18 v.77",
     "Moon-Jupiter conjunction in 3rd house: wise and courageous, respected "
     "among peers, successful in communication and advisory roles"),
    ("moon_jupiter", "conjunction_in_house", 3, {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "3rd_house", "sibling"],
     "Ch.18 v.78",
     "Moon-Jupiter conjunction in 3rd house: benefits from siblings, gains "
     "through short journeys, success in publishing and media"),
    # House 4
    ("moon_jupiter", "conjunction_in_house", 4, {},
     "favorable", "strong",
     ["property_vehicles", "mental_health"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "4th_house"],
     "Ch.19 v.1",
     "Moon-Jupiter conjunction in 4th house: blessed with property, vehicles, "
     "and domestic happiness, peaceful and contented mind"),
    ("moon_jupiter", "conjunction_in_house", 4, {},
     "favorable", "moderate",
     ["character_temperament", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "4th_house", "mother"],
     "Ch.19 v.2",
     "Moon-Jupiter conjunction in 4th house: devoted to mother, virtuous "
     "conduct at home, spiritual inclination from early life"),
    # House 5
    ("moon_jupiter", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["progeny", "intelligence_education"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "5th_house"],
     "Ch.19 v.3",
     "Moon-Jupiter conjunction in 5th house: blessed with worthy and intelligent "
     "children, exceptional wisdom, ministerial or advisory success"),
    ("moon_jupiter", "conjunction_in_house", 5, {},
     "favorable", "strong",
     ["fame_reputation", "wealth"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "5th_house", "fortune"],
     "Ch.19 v.4",
     "Moon-Jupiter conjunction in 5th house: fame through creative and "
     "intellectual achievements, fortunate in speculation and investments"),
    # House 6
    ("moon_jupiter", "conjunction_in_house", 6, {},
     "favorable", "moderate",
     ["enemies_litigation", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "6th_house"],
     "Ch.19 v.5",
     "Moon-Jupiter conjunction in 6th house: overcomes enemies through wisdom "
     "and righteous conduct, charitable even toward adversaries"),
    ("moon_jupiter", "conjunction_in_house", 6, {},
     "mixed", "moderate",
     ["physical_health", "mental_health"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "6th_house", "health"],
     "Ch.19 v.6",
     "Moon-Jupiter conjunction in 6th house: generally good health but prone to "
     "liver and digestive ailments, emotional stress from service obligations"),
    # House 7
    ("moon_jupiter", "conjunction_in_house", 7, {},
     "favorable", "strong",
     ["marriage", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "7th_house"],
     "Ch.19 v.7",
     "Moon-Jupiter conjunction in 7th house: virtuous and learned spouse, "
     "harmonious marriage, benefits through partnerships"),
    ("moon_jupiter", "conjunction_in_house", 7, {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "7th_house", "trade"],
     "Ch.19 v.8",
     "Moon-Jupiter conjunction in 7th house: success in business partnerships, "
     "public reputation for fairness and ethical dealing"),
    # House 8
    ("moon_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["longevity", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "8th_house"],
     "Ch.19 v.9",
     "Moon-Jupiter conjunction in 8th house: long life due to Jupiter's "
     "protection, spiritual interest in mysteries, gains through inheritance"),
    ("moon_jupiter", "conjunction_in_house", 8, {},
     "mixed", "moderate",
     ["wealth", "intelligence_education"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "8th_house", "occult"],
     "Ch.19 v.10",
     "Moon-Jupiter conjunction in 8th house: gains through legacy and insurance, "
     "aptitude for occult wisdom, transformation through spiritual study"),
    # House 9
    ("moon_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "9th_house"],
     "Ch.19 v.11",
     "Moon-Jupiter conjunction in 9th house: deeply religious, virtuous, "
     "honored by scholars and priests, pilgrimage and spiritual merit"),
    ("moon_jupiter", "conjunction_in_house", 9, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "9th_house", "fortune"],
     "Ch.19 v.12",
     "Moon-Jupiter conjunction in 9th house: supreme fortune, gains through "
     "father, patronage from religious and educational institutions"),
    # House 10
    ("moon_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "10th_house"],
     "Ch.19 v.13",
     "Moon-Jupiter conjunction in 10th house: eminent career, honored by "
     "rulers, widespread fame through righteous professional conduct"),
    ("moon_jupiter", "conjunction_in_house", 10, {},
     "favorable", "strong",
     ["wealth", "career_status"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "10th_house", "authority"],
     "Ch.19 v.14",
     "Moon-Jupiter conjunction in 10th house: wealth and authority, commands "
     "respect in public sphere, leadership in educational or religious fields"),
    # House 11
    ("moon_jupiter", "conjunction_in_house", 11, {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "11th_house"],
     "Ch.19 v.15",
     "Moon-Jupiter conjunction in 11th house: abundant gains and prosperity, "
     "Gajakesari yoga gives maximum wealth in house of gains"),
    ("moon_jupiter", "conjunction_in_house", 11, {},
     "favorable", "moderate",
     ["character_temperament", "career_status"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "11th_house", "friends"],
     "Ch.19 v.16",
     "Moon-Jupiter conjunction in 11th house: honored among friends, gains "
     "through elder siblings, influential and well-connected socially"),
    # House 12
    ("moon_jupiter", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "12th_house"],
     "Ch.19 v.17",
     "Moon-Jupiter conjunction in 12th house: expenditure on charitable and "
     "spiritual causes, moksha-oriented, success in foreign lands"),
    ("moon_jupiter", "conjunction_in_house", 12, {},
     "mixed", "moderate",
     ["foreign_travel", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari", "12th_house", "foreign"],
     "Ch.19 v.18",
     "Moon-Jupiter conjunction in 12th house: spiritual attainment in solitude, "
     "gains through foreign connections, generous and philanthropic"),

    # ── Conditional / modifier rules ─────────────────────────────────────────
    ("moon_jupiter", "conjunction_condition", "gajakesari_yoga_proper", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "gajakesari_yoga"],
     "Ch.19 v.19",
     "Gajakesari Yoga (Moon-Jupiter conjunction in good dignity): wisdom, "
     "wealth, and fame, native commands respect like an elephant among men"),
    ("moon_jupiter", "conjunction_condition", "own_sign_jupiter_sagittarius", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "own_sign", "sagittarius"],
     "Ch.19 v.20",
     "Moon-Jupiter conjunction in Sagittarius (Jupiter's own sign): maximum "
     "expansion of fortune, deeply spiritual, honored as a teacher"),
    ("moon_jupiter", "conjunction_condition", "own_sign_jupiter_pisces", {},
     "favorable", "strong",
     ["spirituality", "intelligence_education"],
     ["moon", "jupiter", "conjunction", "saravali", "own_sign", "pisces"],
     "Ch.19 v.21",
     "Moon-Jupiter conjunction in Pisces (Jupiter's own sign): mystical wisdom, "
     "compassionate and charitable, success in spiritual and healing fields"),
    ("moon_jupiter", "conjunction_condition", "own_sign_moon_cancer", {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "own_sign", "cancer"],
     "Ch.19 v.22",
     "Moon-Jupiter conjunction in Cancer (Moon exalted + Jupiter exalted): "
     "supreme beneficence, extraordinary wealth, wisdom, and emotional maturity"),
    ("moon_jupiter", "conjunction_condition", "exalted_jupiter_cancer", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "exaltation", "cancer"],
     "Ch.19 v.23",
     "Moon-Jupiter conjunction in Cancer (Jupiter exalted, Moon in own sign): "
     "most auspicious combination, unparalleled prosperity and renown"),
    ("moon_jupiter", "conjunction_condition", "exalted_moon_taurus", {},
     "favorable", "strong",
     ["wealth", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "exaltation", "taurus"],
     "Ch.19 v.24",
     "Moon-Jupiter conjunction in Taurus (Moon exalted): emotional stability "
     "enhances Jupiter's blessings, material and spiritual prosperity"),
    ("moon_jupiter", "conjunction_condition", "debilitated_moon_scorpio", {},
     "unfavorable", "moderate",
     ["mental_health", "wealth"],
     ["moon", "jupiter", "conjunction", "saravali", "debilitation", "scorpio"],
     "Ch.19 v.25",
     "Moon-Jupiter conjunction in Scorpio (Moon debilitated): Jupiter's "
     "blessings diminished, emotional instability undermines prosperity"),
    ("moon_jupiter", "conjunction_condition", "debilitated_jupiter_capricorn", {},
     "unfavorable", "moderate",
     ["wealth", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "debilitation", "capricorn"],
     "Ch.19 v.26",
     "Moon-Jupiter conjunction in Capricorn (Jupiter debilitated): wisdom "
     "constrained, delayed fortune, materialistic rather than spiritual"),
    ("moon_jupiter", "conjunction_condition", "full_moon_conjunction", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "full_moon"],
     "Ch.19 v.27",
     "Moon-Jupiter conjunction with full Moon (Purnima): Gajakesari at maximum "
     "strength, extraordinary fame, wealth, and public influence"),
    ("moon_jupiter", "conjunction_condition", "new_moon_conjunction", {},
     "mixed", "moderate",
     ["wealth", "mental_health"],
     ["moon", "jupiter", "conjunction", "saravali", "new_moon"],
     "Ch.19 v.28",
     "Moon-Jupiter conjunction with new Moon (Amavasya): weakened Gajakesari, "
     "Jupiter's blessings present but emotional strength diminished"),
    ("moon_jupiter", "conjunction_condition", "waxing_moon_strength", {},
     "favorable", "moderate",
     ["wealth", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "waxing_moon"],
     "Ch.19 v.29",
     "Moon-Jupiter conjunction with waxing Moon: progressive increase in "
     "fortune and reputation, emotional confidence supports wisdom"),
    ("moon_jupiter", "conjunction_condition", "waning_moon_weakness", {},
     "mixed", "weak",
     ["wealth", "mental_health"],
     ["moon", "jupiter", "conjunction", "saravali", "waning_moon"],
     "Ch.19 v.30",
     "Moon-Jupiter conjunction with waning Moon: gradual reduction in Moon's "
     "support, Jupiter compensates but emotional vitality is weakened"),
    ("moon_jupiter", "conjunction_condition", "jupiter_aspect_saturn", {},
     "mixed", "moderate",
     ["career_status", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "saturn_aspect"],
     "Ch.19 v.31",
     "Moon-Jupiter conjunction aspected by Saturn: disciplined wisdom, delayed "
     "fortune, spiritual maturity through hardship and perseverance"),
    ("moon_jupiter", "conjunction_condition", "kendra_strength", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "jupiter", "conjunction", "saravali", "kendra"],
     "Ch.19 v.32",
     "Moon-Jupiter conjunction in any kendra (1/4/7/10): Gajakesari yoga at "
     "full angular strength, prominent fame and career success"),
    ("moon_jupiter", "conjunction_condition", "trikona_placement", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["moon", "jupiter", "conjunction", "saravali", "trikona"],
     "Ch.19 v.33",
     "Moon-Jupiter conjunction in any trikona (1/5/9): supreme dharmic blessing, "
     "fortune through wisdom, children, and spiritual merit"),
    ("moon_jupiter", "conjunction_condition", "dusthana_placement", {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["moon", "jupiter", "conjunction", "saravali", "dusthana"],
     "Ch.19 v.34",
     "Moon-Jupiter conjunction in any dusthana (6/8/12): Jupiter's beneficence "
     "mitigates evil houses, spiritual growth through suffering"),
    ("moon_jupiter", "conjunction_condition", "upachaya_general", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "jupiter", "conjunction", "saravali", "upachaya"],
     "Ch.19 v.35",
     "Moon-Jupiter conjunction in upachaya houses (3/6/10/11): progressive "
     "expansion of fortune and wisdom with advancing age"),
    ("moon_jupiter", "conjunction_condition", "mars_aspect_activating", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["moon", "jupiter", "conjunction", "saravali", "mars_aspect"],
     "Ch.19 v.36",
     "Moon-Jupiter conjunction aspected by Mars: wisdom combined with courage, "
     "active philanthropy, but emotional impulsiveness in decisions"),
    ("moon_jupiter", "conjunction_condition", "venus_aspect_luxuries", {},
     "favorable", "moderate",
     ["wealth", "marriage"],
     ["moon", "jupiter", "conjunction", "saravali", "venus_aspect"],
     "Ch.19 v.37",
     "Moon-Jupiter conjunction aspected by Venus: abundant luxuries, beautiful "
     "spouse, artistic sensibility combined with wisdom and generosity"),
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
    moon_mars = _make_conjunction_rules(
        "moon_mars", ["moon", "mars"], _MOON_MARS_DATA, 261, "Ch.17-18",
    )
    moon_mercury = _make_conjunction_rules(
        "moon_mercury", ["moon", "mercury"], _MOON_MERCURY_DATA, 304, "Ch.18",
    )
    moon_jupiter = _make_conjunction_rules(
        "moon_jupiter", ["moon", "jupiter"], _MOON_JUPITER_DATA, 347, "Ch.18-19",
    )
    return moon_mars + moon_mercury + moon_jupiter


SARAVALI_CONJUNCTIONS_3_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_3_REGISTRY.add(_rule)
