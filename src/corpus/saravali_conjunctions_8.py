"""src/corpus/saravali_conjunctions_8.py — S280: Saravali three+ planet conjunctions.

SAV911–SAV1040 (130 rules).
Phase: 1B_compound | Source: Saravali | School: parashari

Three sections from Saravali Chapters 23-24:
  Three-planet conjunctions    (Ch.23) — SAV911–SAV990  (80 rules)
  Four+ planet conjunctions    (Ch.24) — SAV991–SAV1020 (30 rules)
  Special conjunction conditions (Ch.24) — SAV1021–SAV1040 (20 rules)

Saravali (by Kalyana Varma, ~800 CE) gives detailed results for multi-planet
conjunctions (three or more planets in the same sign), including stellium
effects, planetary war, combustion in groups, and nodal axis interactions.

Confidence formula (single-text, Phase 1B):
  base = 0.60 + 0.05 (verse_ref) = 0.65
  No concordance adjustment for this first encoding.
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord

# ═══════════════════════════════════════════════════════════════════════════════
# Three-Planet Conjunctions — Ch.23 (SAV911–SAV990)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sun-Moon-Mars ───────────────────────────────────────────────────────────
_SUN_MOON_MARS_DATA = [
    ("sun_moon_mars", "multi_conjunction", "kendra_placement", {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "moon", "mars", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.1",
     "Sun-Moon-Mars conjunction in a kendra: warrior-like personality, "
     "rises to commanding position but faces constant enemies and rivalry"),
    ("sun_moon_mars", "multi_conjunction", "trikona_placement", {},
     "mixed", "moderate",
     ["spirituality", "character_temperament"],
     ["sun", "moon", "mars", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.2",
     "Sun-Moon-Mars conjunction in a trikona: fiery temperament channeled "
     "toward righteous causes, courage in defense of dharma"),
    ("sun_moon_mars", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["sun", "moon", "mars", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.3",
     "Sun-Moon-Mars conjunction in a dusthana: severe health afflictions, "
     "danger from fire and weapons, accident-prone with shortened longevity"),
    ("sun_moon_mars", "multi_conjunction", "general_character", {},
     "unfavorable", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "moon", "mars", "conjunction", "saravali", "three_planet", "aggressive"],
     "Ch.23 v.4",
     "Sun-Moon-Mars conjunction overall: hot-tempered, aggressive disposition, "
     "creates enmity through impulsive actions, blood-related disorders"),
    ("sun_moon_mars", "multi_conjunction", "benefic_sign", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["sun", "moon", "mars", "conjunction", "saravali", "three_planet", "benefic_sign"],
     "Ch.23 v.5",
     "Sun-Moon-Mars conjunction in a benefic sign: military or administrative "
     "success, earns through courage, leadership in competitive fields"),
]

# ── Sun-Moon-Mercury ────────────────────────────────────────────────────────
_SUN_MOON_MERCURY_DATA = [
    ("sun_moon_mercury", "multi_conjunction", "kendra_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "career_status"],
     ["sun", "moon", "mercury", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.6",
     "Sun-Moon-Mercury conjunction in a kendra: sharp intellect with "
     "administrative ability, skilled communicator in authoritative roles"),
    ("sun_moon_mercury", "multi_conjunction", "trikona_placement", {},
     "favorable", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["sun", "moon", "mercury", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.7",
     "Sun-Moon-Mercury conjunction in a trikona: scholarly mind, fame through "
     "writing or oratory, blessed with scriptural knowledge"),
    ("sun_moon_mercury", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["intelligence_education", "mental_health"],
     ["sun", "moon", "mercury", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.8",
     "Sun-Moon-Mercury conjunction in a dusthana: nervous disorders, intellect "
     "wasted on trivial pursuits, anxiety and communication difficulties"),
    ("sun_moon_mercury", "multi_conjunction", "general_character", {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "moon", "mercury", "conjunction", "saravali", "three_planet", "clever"],
     "Ch.23 v.9",
     "Sun-Moon-Mercury conjunction overall: clever but restless mind, skilled "
     "in arts and commerce, prone to mental fatigue from overthinking"),
    ("sun_moon_mercury", "multi_conjunction", "combustion_effect", {},
     "unfavorable", "moderate",
     ["intelligence_education", "character_temperament"],
     ["sun", "moon", "mercury", "conjunction", "saravali", "three_planet", "combustion"],
     "Ch.23 v.10",
     "Sun-Moon-Mercury conjunction with Mercury combust: speech defects or "
     "communication difficulties, intellectual promise unrealized"),
]

# ── Sun-Moon-Jupiter ────────────────────────────────────────────────────────
_SUN_MOON_JUPITER_DATA = [
    ("sun_moon_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["sun", "moon", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.11",
     "Sun-Moon-Jupiter conjunction in a kendra: highly respected, religious "
     "leader or advisor, gains through wisdom and righteous conduct"),
    ("sun_moon_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["sun", "moon", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.12",
     "Sun-Moon-Jupiter conjunction in a trikona: blessed with fortune and "
     "divine grace, prosperous life guided by dharmic principles"),
    ("sun_moon_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["spirituality", "wealth"],
     ["sun", "moon", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.13",
     "Sun-Moon-Jupiter conjunction in a dusthana: Jupiter's beneficence "
     "mitigates harm but native faces spiritual trials and financial setbacks"),
    ("sun_moon_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "moderate",
     ["character_temperament", "fame_reputation"],
     ["sun", "moon", "jupiter", "conjunction", "saravali", "three_planet", "virtuous"],
     "Ch.23 v.14",
     "Sun-Moon-Jupiter conjunction overall: virtuous, charitable, learned "
     "in scriptures, commands respect from community and authorities"),
    ("sun_moon_jupiter", "multi_conjunction", "own_exaltation", {},
     "favorable", "strong",
     ["career_status", "wealth"],
     ["sun", "moon", "jupiter", "conjunction", "saravali", "three_planet", "exaltation"],
     "Ch.23 v.15",
     "Sun-Moon-Jupiter conjunction with Jupiter in own/exaltation: attains "
     "high office, counselor to rulers, abundant wealth and honor"),
]

# ── Sun-Mars-Mercury ────────────────────────────────────────────────────────
_SUN_MARS_MERCURY_DATA = [
    ("sun_mars_mercury", "multi_conjunction", "kendra_placement", {},
     "mixed", "strong",
     ["career_status", "intelligence_education"],
     ["sun", "mars", "mercury", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.16",
     "Sun-Mars-Mercury conjunction in a kendra: sharp strategic mind, excels "
     "in military planning, engineering, or technical administration"),
    ("sun_mars_mercury", "multi_conjunction", "general_character", {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["sun", "mars", "mercury", "conjunction", "saravali", "three_planet", "strategic"],
     "Ch.23 v.17",
     "Sun-Mars-Mercury conjunction overall: argumentative intellect, skilled "
     "debater, sharp tongue that creates enemies through harsh speech"),
    ("sun_mars_mercury", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "strong",
     ["enemies_litigation", "mental_health"],
     ["sun", "mars", "mercury", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.18",
     "Sun-Mars-Mercury conjunction in a dusthana: litigation troubles, "
     "nervous aggression, intellect channeled toward destructive ends"),
    ("sun_mars_mercury", "multi_conjunction", "benefic_sign", {},
     "favorable", "moderate",
     ["career_status", "wealth"],
     ["sun", "mars", "mercury", "conjunction", "saravali", "three_planet", "benefic_sign"],
     "Ch.23 v.19",
     "Sun-Mars-Mercury conjunction in a benefic sign: success in technical "
     "or surgical fields, earns through precision and analytical skill"),
    ("sun_mars_mercury", "multi_conjunction", "combustion_effect", {},
     "unfavorable", "moderate",
     ["intelligence_education", "physical_health"],
     ["sun", "mars", "mercury", "conjunction", "saravali", "three_planet", "combustion"],
     "Ch.23 v.20",
     "Sun-Mars-Mercury conjunction with Mercury combust: rash decisions, "
     "poor judgment in conflicts, injuries from impulsive actions"),
]

# ── Sun-Mars-Jupiter ────────────────────────────────────────────────────────
_SUN_MARS_JUPITER_DATA = [
    ("sun_mars_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["sun", "mars", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.21",
     "Sun-Mars-Jupiter conjunction in a kendra: powerful commander or leader, "
     "righteous warrior, gains authority through courageous and just actions"),
    ("sun_mars_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "moderate",
     ["character_temperament", "career_status"],
     ["sun", "mars", "jupiter", "conjunction", "saravali", "three_planet", "noble_warrior"],
     "Ch.23 v.22",
     "Sun-Mars-Jupiter conjunction overall: noble and courageous, defender of "
     "tradition, respected for bravery and moral convictions"),
    ("sun_mars_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["enemies_litigation", "spirituality"],
     ["sun", "mars", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.23",
     "Sun-Mars-Jupiter conjunction in a dusthana: fights for righteous causes "
     "but faces legal battles, Jupiter mitigates Mars's destructive tendencies"),
    ("sun_mars_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["fame_reputation", "spirituality"],
     ["sun", "mars", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.24",
     "Sun-Mars-Jupiter conjunction in a trikona: fame through heroic or "
     "religious service, patron of temples, charitable warrior-king"),
    ("sun_mars_jupiter", "multi_conjunction", "malefic_sign", {},
     "mixed", "moderate",
     ["character_temperament", "enemies_litigation"],
     ["sun", "mars", "jupiter", "conjunction", "saravali", "three_planet", "malefic_sign"],
     "Ch.23 v.25",
     "Sun-Mars-Jupiter conjunction in a malefic sign: aggressive righteousness, "
     "tendency to impose beliefs on others, conflict with authority"),
]

# ── Sun-Mercury-Jupiter ─────────────────────────────────────────────────────
_SUN_MERCURY_JUPITER_DATA = [
    ("sun_mercury_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["sun", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.26",
     "Sun-Mercury-Jupiter conjunction in a kendra: brilliant scholar, "
     "advisor to rulers, fame through wisdom and eloquent discourse"),
    ("sun_mercury_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["sun", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "learned"],
     "Ch.23 v.27",
     "Sun-Mercury-Jupiter conjunction overall: deeply learned, skilled in "
     "multiple sciences, virtuous character with sharp intellect"),
    ("sun_mercury_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["wealth", "intelligence_education"],
     ["sun", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.28",
     "Sun-Mercury-Jupiter conjunction in a trikona: fortune through knowledge, "
     "successful in teaching, publishing, or advisory roles"),
    ("sun_mercury_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["sun", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.29",
     "Sun-Mercury-Jupiter conjunction in a dusthana: knowledge not properly "
     "utilized, intellectual frustration, obstacles in academic career"),
    ("sun_mercury_jupiter", "multi_conjunction", "combustion_effect", {},
     "mixed", "moderate",
     ["intelligence_education", "fame_reputation"],
     ["sun", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "combustion"],
     "Ch.23 v.30",
     "Sun-Mercury-Jupiter conjunction with Mercury combust: delayed recognition "
     "of talents, Jupiter sustains wisdom despite Sun's overpowering influence"),
]

# ── Moon-Mars-Mercury ───────────────────────────────────────────────────────
_MOON_MARS_MERCURY_DATA = [
    ("moon_mars_mercury", "multi_conjunction", "kendra_placement", {},
     "mixed", "moderate",
     ["intelligence_education", "character_temperament"],
     ["moon", "mars", "mercury", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.31",
     "Moon-Mars-Mercury conjunction in a kendra: quick-witted and assertive, "
     "skilled in mechanical arts, emotionally volatile intellect"),
    ("moon_mars_mercury", "multi_conjunction", "general_character", {},
     "mixed", "moderate",
     ["character_temperament", "mental_health"],
     ["moon", "mars", "mercury", "conjunction", "saravali", "three_planet", "restless"],
     "Ch.23 v.32",
     "Moon-Mars-Mercury conjunction overall: restless mind, quick to anger "
     "and quick to forgive, skilled in crafts but lacks sustained focus"),
    ("moon_mars_mercury", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["mental_health", "enemies_litigation"],
     ["moon", "mars", "mercury", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.33",
     "Moon-Mars-Mercury conjunction in a dusthana: mental agitation, quarrels "
     "with relatives, nervous disorders from emotional stress"),
    ("moon_mars_mercury", "multi_conjunction", "benefic_sign", {},
     "favorable", "moderate",
     ["career_status", "intelligence_education"],
     ["moon", "mars", "mercury", "conjunction", "saravali", "three_planet", "benefic_sign"],
     "Ch.23 v.34",
     "Moon-Mars-Mercury conjunction in a benefic sign: success in trade, "
     "manufacturing, or technical fields requiring mental agility"),
    ("moon_mars_mercury", "multi_conjunction", "upachaya_placement", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["moon", "mars", "mercury", "conjunction", "saravali", "three_planet", "upachaya"],
     "Ch.23 v.35",
     "Moon-Mars-Mercury conjunction in upachaya houses: progressive improvement "
     "in career and finances, competitive skills sharpen with age"),
]

# ── Moon-Mars-Jupiter ───────────────────────────────────────────────────────
_MOON_MARS_JUPITER_DATA = [
    ("moon_mars_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["moon", "mars", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.36",
     "Moon-Mars-Jupiter conjunction in a kendra: popular leader, commands "
     "both emotional loyalty and martial respect, prosperous career"),
    ("moon_mars_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "moderate",
     ["character_temperament", "wealth"],
     ["moon", "mars", "jupiter", "conjunction", "saravali", "three_planet", "generous"],
     "Ch.23 v.37",
     "Moon-Mars-Jupiter conjunction overall: generous and brave, protects the "
     "weak, earns through righteous enterprise, respected in community"),
    ("moon_mars_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["spirituality", "fame_reputation"],
     ["moon", "mars", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.38",
     "Moon-Mars-Jupiter conjunction in a trikona: religious warrior, defends "
     "dharmic institutions, fame through courageous spiritual service"),
    ("moon_mars_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["enemies_litigation", "physical_health"],
     ["moon", "mars", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.39",
     "Moon-Mars-Jupiter conjunction in a dusthana: legal battles for righteous "
     "causes, health issues from overexertion, Jupiter limits worst outcomes"),
    ("moon_mars_jupiter", "multi_conjunction", "malefic_sign", {},
     "mixed", "moderate",
     ["character_temperament", "career_status"],
     ["moon", "mars", "jupiter", "conjunction", "saravali", "three_planet", "malefic_sign"],
     "Ch.23 v.40",
     "Moon-Mars-Jupiter conjunction in a malefic sign: passionate convictions "
     "create conflict, forceful personality with moral justification"),
]

# ── Moon-Mercury-Jupiter ────────────────────────────────────────────────────
_MOON_MERCURY_JUPITER_DATA = [
    ("moon_mercury_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["intelligence_education", "fame_reputation"],
     ["moon", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.41",
     "Moon-Mercury-Jupiter conjunction in a kendra: Saraswati yoga-like effect, "
     "brilliant scholar, fame through learning and eloquent expression"),
    ("moon_mercury_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "strong",
     ["intelligence_education", "character_temperament"],
     ["moon", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "scholarly"],
     "Ch.23 v.42",
     "Moon-Mercury-Jupiter conjunction overall: refined intellect, poetic "
     "sensibility, learned in sacred and secular sciences, virtuous nature"),
    ("moon_mercury_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["moon", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.43",
     "Moon-Mercury-Jupiter conjunction in a trikona: great fortune through "
     "intellectual pursuits, renowned teacher or author, divine blessings"),
    ("moon_mercury_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["intelligence_education", "mental_health"],
     ["moon", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.44",
     "Moon-Mercury-Jupiter conjunction in a dusthana: knowledge brings anxiety, "
     "overthinking leads to emotional disturbance, academic setbacks"),
    ("moon_mercury_jupiter", "multi_conjunction", "own_exaltation", {},
     "favorable", "strong",
     ["intelligence_education", "wealth"],
     ["moon", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "exaltation"],
     "Ch.23 v.45",
     "Moon-Mercury-Jupiter conjunction with planets in dignity: extraordinary "
     "intellect and wisdom, wealth through scholarship, honored by kings"),
]

# ── Mars-Mercury-Jupiter ────────────────────────────────────────────────────
_MARS_MERCURY_JUPITER_DATA = [
    ("mars_mercury_jupiter", "multi_conjunction", "kendra_placement", {},
     "favorable", "strong",
     ["career_status", "intelligence_education"],
     ["mars", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.46",
     "Mars-Mercury-Jupiter conjunction in a kendra: exceptional strategist, "
     "excels in law, engineering, or military command, logical and decisive"),
    ("mars_mercury_jupiter", "multi_conjunction", "general_character", {},
     "favorable", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mars", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "analytical"],
     "Ch.23 v.47",
     "Mars-Mercury-Jupiter conjunction overall: analytical mind with courage "
     "to act, skilled in debate and litigation, principled fighter"),
    ("mars_mercury_jupiter", "multi_conjunction", "trikona_placement", {},
     "favorable", "strong",
     ["fame_reputation", "career_status"],
     ["mars", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.48",
     "Mars-Mercury-Jupiter conjunction in a trikona: fame through legal or "
     "scholarly excellence, defends truth with sharp intellect and courage"),
    ("mars_mercury_jupiter", "multi_conjunction", "dusthana_placement", {},
     "mixed", "moderate",
     ["enemies_litigation", "intelligence_education"],
     ["mars", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.49",
     "Mars-Mercury-Jupiter conjunction in a dusthana: involved in prolonged "
     "litigation, intellectual combativeness creates professional obstacles"),
    ("mars_mercury_jupiter", "multi_conjunction", "benefic_sign", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mars", "mercury", "jupiter", "conjunction", "saravali", "three_planet", "benefic_sign"],
     "Ch.23 v.50",
     "Mars-Mercury-Jupiter conjunction in a benefic sign: success in technical "
     "or legal professions, earns through precision and ethical practice"),
]

# ── Sun-Venus-Saturn ────────────────────────────────────────────────────────
_SUN_VENUS_SATURN_DATA = [
    ("sun_venus_saturn", "multi_conjunction", "kendra_placement", {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["sun", "venus", "saturn", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.51",
     "Sun-Venus-Saturn conjunction in a kendra: delayed marriage, artistic "
     "discipline, career in entertainment or governance with obstacles"),
    ("sun_venus_saturn", "multi_conjunction", "general_character", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["sun", "venus", "saturn", "conjunction", "saravali", "three_planet", "austere"],
     "Ch.23 v.52",
     "Sun-Venus-Saturn conjunction overall: austere in pleasures, difficulty "
     "in romantic relationships, Venus weakened between two malefics"),
    ("sun_venus_saturn", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "strong",
     ["marriage", "wealth"],
     ["sun", "venus", "saturn", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.53",
     "Sun-Venus-Saturn conjunction in a dusthana: severe marital difficulties, "
     "financial losses through partnerships, denied comforts and luxuries"),
    ("sun_venus_saturn", "multi_conjunction", "trikona_placement", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["sun", "venus", "saturn", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.54",
     "Sun-Venus-Saturn conjunction in a trikona: disciplined creative pursuit, "
     "success through persistent artistic effort, late-blooming recognition"),
    ("sun_venus_saturn", "multi_conjunction", "benefic_aspect", {},
     "mixed", "moderate",
     ["marriage", "wealth"],
     ["sun", "venus", "saturn", "conjunction", "saravali", "three_planet", "benefic_aspect"],
     "Ch.23 v.55",
     "Sun-Venus-Saturn conjunction aspected by benefics: Jupiter's aspect "
     "mitigates marital difficulties, stabilizes finances after middle age"),
]

# ── Moon-Venus-Saturn ───────────────────────────────────────────────────────
_MOON_VENUS_SATURN_DATA = [
    ("moon_venus_saturn", "multi_conjunction", "kendra_placement", {},
     "mixed", "moderate",
     ["marriage", "mental_health"],
     ["moon", "venus", "saturn", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.56",
     "Moon-Venus-Saturn conjunction in a kendra: emotional coldness in "
     "relationships, artistic melancholy, beauty tinged with sorrow"),
    ("moon_venus_saturn", "multi_conjunction", "general_character", {},
     "unfavorable", "moderate",
     ["mental_health", "marriage"],
     ["moon", "venus", "saturn", "conjunction", "saravali", "three_planet", "melancholic"],
     "Ch.23 v.57",
     "Moon-Venus-Saturn conjunction overall: melancholic temperament, "
     "emotional suffering in love, attachment to sorrowful experiences"),
    ("moon_venus_saturn", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "strong",
     ["mental_health", "marriage"],
     ["moon", "venus", "saturn", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.58",
     "Moon-Venus-Saturn conjunction in a dusthana: chronic depression, "
     "troubled marriage, emotional isolation, denied domestic happiness"),
    ("moon_venus_saturn", "multi_conjunction", "trikona_placement", {},
     "mixed", "moderate",
     ["character_temperament", "spirituality"],
     ["moon", "venus", "saturn", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.59",
     "Moon-Venus-Saturn conjunction in a trikona: renunciation tendency, "
     "detachment from worldly pleasures leads to spiritual growth"),
    ("moon_venus_saturn", "multi_conjunction", "upachaya_placement", {},
     "mixed", "moderate",
     ["wealth", "career_status"],
     ["moon", "venus", "saturn", "conjunction", "saravali", "three_planet", "upachaya"],
     "Ch.23 v.60",
     "Moon-Venus-Saturn conjunction in upachaya houses: gradual improvement "
     "in material conditions, emotional stability develops with maturity"),
]

# ── Mars-Venus-Saturn ───────────────────────────────────────────────────────
_MARS_VENUS_SATURN_DATA = [
    ("mars_venus_saturn", "multi_conjunction", "kendra_placement", {},
     "unfavorable", "strong",
     ["marriage", "character_temperament"],
     ["mars", "venus", "saturn", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.61",
     "Mars-Venus-Saturn conjunction in a kendra: intense passions followed "
     "by severe frustration, volatile relationships, domestic violence risk"),
    ("mars_venus_saturn", "multi_conjunction", "general_character", {},
     "unfavorable", "moderate",
     ["marriage", "character_temperament"],
     ["mars", "venus", "saturn", "conjunction", "saravali", "three_planet", "passionate"],
     "Ch.23 v.62",
     "Mars-Venus-Saturn conjunction overall: conflicted desires, Venus "
     "crushed between two malefics, struggles with sensual impulses"),
    ("mars_venus_saturn", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "strong",
     ["marriage", "physical_health"],
     ["mars", "venus", "saturn", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.63",
     "Mars-Venus-Saturn conjunction in a dusthana: reproductive disorders, "
     "marital breakdown, losses through illicit relationships"),
    ("mars_venus_saturn", "multi_conjunction", "trikona_placement", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["mars", "venus", "saturn", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.64",
     "Mars-Venus-Saturn conjunction in a trikona: disciplined approach to "
     "ambition, success in manufacturing or construction industries"),
    ("mars_venus_saturn", "multi_conjunction", "benefic_aspect", {},
     "mixed", "moderate",
     ["marriage", "career_status"],
     ["mars", "venus", "saturn", "conjunction", "saravali", "three_planet", "benefic_aspect"],
     "Ch.23 v.65",
     "Mars-Venus-Saturn conjunction aspected by Jupiter: marital difficulties "
     "reduced, professional success through disciplined effort"),
]

# ── Mercury-Venus-Saturn ────────────────────────────────────────────────────
_MERCURY_VENUS_SATURN_DATA = [
    ("mercury_venus_saturn", "multi_conjunction", "kendra_placement", {},
     "mixed", "moderate",
     ["intelligence_education", "career_status"],
     ["mercury", "venus", "saturn", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.66",
     "Mercury-Venus-Saturn conjunction in a kendra: skilled artisan or "
     "craftsperson, disciplined creative intellect, slow but thorough worker"),
    ("mercury_venus_saturn", "multi_conjunction", "general_character", {},
     "mixed", "moderate",
     ["character_temperament", "intelligence_education"],
     ["mercury", "venus", "saturn", "conjunction", "saravali", "three_planet", "meticulous"],
     "Ch.23 v.67",
     "Mercury-Venus-Saturn conjunction overall: meticulous and detail-oriented, "
     "skilled in fine arts or accounting, reserved social demeanor"),
    ("mercury_venus_saturn", "multi_conjunction", "trikona_placement", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "venus", "saturn", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.68",
     "Mercury-Venus-Saturn conjunction in a trikona: success in commerce, "
     "steady accumulation of wealth through disciplined business acumen"),
    ("mercury_venus_saturn", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["intelligence_education", "wealth"],
     ["mercury", "venus", "saturn", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.69",
     "Mercury-Venus-Saturn conjunction in a dusthana: commercial losses, "
     "artistic talents go unrecognized, financial anxiety and debt"),
    ("mercury_venus_saturn", "multi_conjunction", "upachaya_placement", {},
     "favorable", "moderate",
     ["wealth", "career_status"],
     ["mercury", "venus", "saturn", "conjunction", "saravali", "three_planet", "upachaya"],
     "Ch.23 v.70",
     "Mercury-Venus-Saturn conjunction in upachaya houses: business acumen "
     "improves steadily, late success in commerce or creative industries"),
]

# ── Jupiter-Venus-Saturn ────────────────────────────────────────────────────
_JUPITER_VENUS_SATURN_DATA = [
    ("jupiter_venus_saturn", "multi_conjunction", "kendra_placement", {},
     "mixed", "moderate",
     ["spirituality", "marriage"],
     ["jupiter", "venus", "saturn", "conjunction", "saravali", "three_planet", "kendra"],
     "Ch.23 v.71",
     "Jupiter-Venus-Saturn conjunction in a kendra: tension between spiritual "
     "aspiration and worldly pleasure, disciplined but conflicted values"),
    ("jupiter_venus_saturn", "multi_conjunction", "general_character", {},
     "mixed", "moderate",
     ["character_temperament", "spirituality"],
     ["jupiter", "venus", "saturn", "conjunction", "saravali", "three_planet", "philosophical"],
     "Ch.23 v.72",
     "Jupiter-Venus-Saturn conjunction overall: philosophical and reflective, "
     "oscillates between indulgence and austerity, seeks balanced wisdom"),
    ("jupiter_venus_saturn", "multi_conjunction", "trikona_placement", {},
     "favorable", "moderate",
     ["spirituality", "wealth"],
     ["jupiter", "venus", "saturn", "conjunction", "saravali", "three_planet", "trikona"],
     "Ch.23 v.73",
     "Jupiter-Venus-Saturn conjunction in a trikona: spiritual maturity "
     "through life experience, charitable works, patronage of arts"),
    ("jupiter_venus_saturn", "multi_conjunction", "dusthana_placement", {},
     "unfavorable", "moderate",
     ["wealth", "spirituality"],
     ["jupiter", "venus", "saturn", "conjunction", "saravali", "three_planet", "dusthana"],
     "Ch.23 v.74",
     "Jupiter-Venus-Saturn conjunction in a dusthana: spiritual crisis, "
     "financial losses through misplaced generosity, faith tested"),
    ("jupiter_venus_saturn", "multi_conjunction", "own_exaltation", {},
     "favorable", "strong",
     ["fame_reputation", "spirituality"],
     ["jupiter", "venus", "saturn", "conjunction", "saravali", "three_planet", "exaltation"],
     "Ch.23 v.75",
     "Jupiter-Venus-Saturn conjunction with Jupiter in dignity: honored sage, "
     "respected for wisdom, wealth through ethical enterprise and teaching"),
]

# ── General Three-Planet Rules ──────────────────────────────────────────────
_THREE_PLANET_GENERAL_DATA = [
    ("three_planet_general", "multi_conjunction", "three_benefics", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["three_planet", "conjunction", "saravali", "benefic", "triple_conjunction"],
     "Ch.23 v.76",
     "Three benefics (Jupiter, Venus, Mercury) conjoined: exceptional fortune, "
     "fame through learning, abundant wealth, respected in all circles"),
    ("three_planet_general", "multi_conjunction", "three_malefics", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["three_planet", "conjunction", "saravali", "malefic", "triple_conjunction"],
     "Ch.23 v.77",
     "Three malefics (Sun, Mars, Saturn) conjoined: severe affliction, chronic "
     "health problems, accidents, litigation, and life-threatening dangers"),
    ("three_planet_general", "multi_conjunction", "two_benefic_one_malefic", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["three_planet", "conjunction", "saravali", "mixed", "triple_conjunction"],
     "Ch.23 v.78",
     "Two benefics with one malefic conjoined: malefic's negative influence "
     "substantially mitigated, benefics channel malefic energy productively"),
    ("three_planet_general", "multi_conjunction", "two_malefic_one_benefic", {},
     "unfavorable", "moderate",
     ["career_status", "physical_health"],
     ["three_planet", "conjunction", "saravali", "mixed", "triple_conjunction", "malefic_dominant"],
     "Ch.23 v.79",
     "Two malefics with one benefic conjoined: benefic planet overwhelmed, "
     "its significations suffer, overall negative results with minor relief"),
    ("three_planet_general", "multi_conjunction", "luminaries_with_benefic", {},
     "favorable", "moderate",
     ["fame_reputation", "character_temperament"],
     ["three_planet", "conjunction", "saravali", "luminaries", "triple_conjunction"],
     "Ch.23 v.80",
     "Both luminaries (Sun, Moon) with a benefic: enhanced public standing, "
     "strong personality with emotional intelligence, popular leader"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Four+ Planet Conjunctions — Ch.24 (SAV991–SAV1020)
# ═══════════════════════════════════════════════════════════════════════════════
_FOUR_PLUS_PLANET_DATA = [
    # ── Four-planet combinations ────────────────────────────────────────────
    ("four_planet_conjunction", "multi_conjunction", "four_with_jupiter", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["four_planet", "conjunction", "saravali", "stellium", "jupiter"],
     "Ch.24 v.1",
     "Four planets conjoined including Jupiter: Jupiter's beneficence protects "
     "the stellium, native attains wealth and recognition in chosen field"),
    ("four_planet_conjunction", "multi_conjunction", "four_with_saturn", {},
     "unfavorable", "strong",
     ["career_status", "physical_health"],
     ["four_planet", "conjunction", "saravali", "stellium", "saturn"],
     "Ch.24 v.2",
     "Four planets conjoined including Saturn: heavy karmic load, delayed "
     "success, chronic health issues, life of struggle and perseverance"),
    ("four_planet_conjunction", "multi_conjunction", "four_all_benefics", {},
     "favorable", "strong",
     ["wealth", "fame_reputation", "intelligence_education"],
     ["four_planet", "conjunction", "saravali", "stellium", "all_benefics"],
     "Ch.24 v.3",
     "Four predominantly benefic planets conjoined: extraordinary fortune, "
     "fame and wealth, born into or achieves positions of great privilege"),
    ("four_planet_conjunction", "multi_conjunction", "four_all_malefics", {},
     "unfavorable", "strong",
     ["longevity", "physical_health", "mental_health"],
     ["four_planet", "conjunction", "saravali", "stellium", "all_malefics"],
     "Ch.24 v.4",
     "Four predominantly malefic planets conjoined: severe life afflictions, "
     "poverty, illness, and danger, extremely challenging incarnation"),
    ("four_planet_conjunction", "multi_conjunction", "four_in_kendra", {},
     "favorable", "strong",
     ["career_status", "fame_reputation"],
     ["four_planet", "conjunction", "saravali", "stellium", "kendra"],
     "Ch.24 v.5",
     "Four planets conjoined in a kendra: concentration of power, native "
     "becomes highly influential in their sphere, strong personality"),
    ("four_planet_conjunction", "multi_conjunction", "four_in_dusthana", {},
     "unfavorable", "strong",
     ["longevity", "wealth"],
     ["four_planet", "conjunction", "saravali", "stellium", "dusthana"],
     "Ch.24 v.6",
     "Four planets conjoined in a dusthana: multiple life areas severely "
     "afflicted, health crises, financial ruin, enemies overwhelm"),
    ("four_planet_conjunction", "multi_conjunction", "four_in_trikona", {},
     "favorable", "strong",
     ["wealth", "spirituality"],
     ["four_planet", "conjunction", "saravali", "stellium", "trikona"],
     "Ch.24 v.7",
     "Four planets conjoined in a trikona: tremendous dharmic merit, "
     "fortune and spiritual growth, blessed life with divine protection"),
    ("four_planet_conjunction", "multi_conjunction", "four_luminaries_benefics", {},
     "favorable", "strong",
     ["fame_reputation", "wealth"],
     ["four_planet", "conjunction", "saravali", "stellium", "luminaries", "benefics"],
     "Ch.24 v.8",
     "Sun-Moon-Jupiter-Venus conjoined: extraordinary charisma, leadership "
     "combined with wisdom and grace, prosperous and celebrated life"),
    ("four_planet_conjunction", "multi_conjunction", "four_luminaries_malefics", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["four_planet", "conjunction", "saravali", "stellium", "luminaries", "malefics"],
     "Ch.24 v.9",
     "Sun-Moon-Mars-Saturn conjoined: extreme emotional and physical stress, "
     "turbulent life marked by constant struggle and transformation"),
    ("four_planet_conjunction", "multi_conjunction", "four_mixed_kendra", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["four_planet", "conjunction", "saravali", "stellium", "mixed", "kendra"],
     "Ch.24 v.10",
     "Four mixed planets in a kendra: powerful but contradictory personality, "
     "intense career focus with complex internal conflicts"),

    # ── Five-planet combinations ────────────────────────────────────────────
    ("five_planet_conjunction", "multi_conjunction", "five_general", {},
     "mixed", "strong",
     ["career_status", "fame_reputation", "longevity"],
     ["five_planet", "conjunction", "saravali", "stellium", "rare"],
     "Ch.24 v.11",
     "Five planets conjoined: rare and powerful stellium, life dominated by "
     "the sign of conjunction, extreme concentration of karmic energy"),
    ("five_planet_conjunction", "multi_conjunction", "five_benefic_dominant", {},
     "favorable", "strong",
     ["wealth", "fame_reputation"],
     ["five_planet", "conjunction", "saravali", "stellium", "benefic_dominant"],
     "Ch.24 v.12",
     "Five planets conjoined with benefic dominance: person of exceptional "
     "talent and fortune, rises to great heights, legendary achievements"),
    ("five_planet_conjunction", "multi_conjunction", "five_malefic_dominant", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["five_planet", "conjunction", "saravali", "stellium", "malefic_dominant"],
     "Ch.24 v.13",
     "Five planets conjoined with malefic dominance: severely afflicted life, "
     "extreme hardship, danger of premature death, poverty and suffering"),
    ("five_planet_conjunction", "multi_conjunction", "five_in_kendra", {},
     "mixed", "strong",
     ["career_status", "fame_reputation"],
     ["five_planet", "conjunction", "saravali", "stellium", "kendra"],
     "Ch.24 v.14",
     "Five planets conjoined in a kendra: extraordinary worldly impact, "
     "native's actions have far-reaching consequences, public figure"),
    ("five_planet_conjunction", "multi_conjunction", "five_in_dusthana", {},
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     ["five_planet", "conjunction", "saravali", "stellium", "dusthana"],
     "Ch.24 v.15",
     "Five planets conjoined in a dusthana: overwhelming affliction, "
     "extremely challenging life with multiple crises and transformations"),
    ("five_planet_conjunction", "multi_conjunction", "five_with_nodes", {},
     "unfavorable", "strong",
     ["mental_health", "spirituality"],
     ["five_planet", "conjunction", "saravali", "stellium", "rahu_ketu"],
     "Ch.24 v.16",
     "Five planets conjoined near Rahu or Ketu: eclipsed stellium, karmic "
     "intensity magnified, life of unusual events and spiritual crisis"),

    # ── Six-planet combinations ─────────────────────────────────────────────
    ("six_planet_conjunction", "multi_conjunction", "six_general", {},
     "mixed", "strong",
     ["career_status", "longevity", "fame_reputation"],
     ["six_planet", "conjunction", "saravali", "stellium", "extremely_rare"],
     "Ch.24 v.17",
     "Six planets conjoined: extremely rare, total life transformation, "
     "native's destiny shaped entirely by the conjoined sign and house"),
    ("six_planet_conjunction", "multi_conjunction", "six_benefic_lord", {},
     "mixed", "strong",
     ["fame_reputation", "spirituality"],
     ["six_planet", "conjunction", "saravali", "stellium", "benefic_lord"],
     "Ch.24 v.18",
     "Six planets conjoined in a sign ruled by a benefic: despite intensity, "
     "some protection from worst effects, potential for remarkable achievement"),
    ("six_planet_conjunction", "multi_conjunction", "six_malefic_lord", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["six_planet", "conjunction", "saravali", "stellium", "malefic_lord"],
     "Ch.24 v.19",
     "Six planets conjoined in a sign ruled by a malefic: catastrophic "
     "potential, life-threatening events, radical transformation of destiny"),
    ("six_planet_conjunction", "multi_conjunction", "six_with_lagna_lord", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["six_planet", "conjunction", "saravali", "stellium", "lagna_lord"],
     "Ch.24 v.20",
     "Six planets conjoined including lagna lord: native's identity completely "
     "merged with the stellium, overwhelming personality and destiny"),

    # ── Seven-planet conjunction ────────────────────────────────────────────
    ("seven_planet_conjunction", "multi_conjunction", "seven_theoretical", {},
     "mixed", "strong",
     ["longevity", "career_status", "spirituality"],
     ["seven_planet", "conjunction", "saravali", "stellium", "theoretical", "cosmic"],
     "Ch.24 v.21",
     "All seven planets conjoined: theoretical possibility of cosmic significance, "
     "if ever born, native experiences the totality of planetary karma in one life"),
    ("seven_planet_conjunction", "multi_conjunction", "seven_in_benefic_sign", {},
     "mixed", "strong",
     ["fame_reputation", "spirituality"],
     ["seven_planet", "conjunction", "saravali", "stellium", "theoretical", "benefic_sign"],
     "Ch.24 v.22",
     "All seven planets in a benefic sign: theoretical — if born, may be an "
     "extraordinary soul, saint, or world-altering personality"),
    ("seven_planet_conjunction", "multi_conjunction", "seven_in_malefic_sign", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["seven_planet", "conjunction", "saravali", "stellium", "theoretical", "malefic_sign"],
     "Ch.24 v.23",
     "All seven planets in a malefic sign: theoretical — if born, extreme "
     "suffering and shortest possible lifespan, total karmic convergence"),

    # ── General stellium rules ──────────────────────────────────────────────
    ("stellium_general", "multi_conjunction", "stellium_sign_strength", {},
     "mixed", "strong",
     ["career_status", "character_temperament"],
     ["stellium", "conjunction", "saravali", "sign_strength"],
     "Ch.24 v.24",
     "Any stellium (4+ planets): the sign's natural quality (cardinal/fixed/mutable) "
     "dominates the native's character and determines the mode of life expression"),
    ("stellium_general", "multi_conjunction", "stellium_house_lord", {},
     "mixed", "strong",
     ["career_status", "wealth"],
     ["stellium", "conjunction", "saravali", "house_lord"],
     "Ch.24 v.25",
     "Any stellium: the dispositor (lord of the sign) becomes the most important "
     "planet in the chart, its placement determines stellium outcomes"),
    ("stellium_general", "multi_conjunction", "stellium_strongest_planet", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["stellium", "conjunction", "saravali", "strongest_planet"],
     "Ch.24 v.26",
     "Any stellium: the planet with highest shadbala in the group dominates "
     "results, other planets become subordinate to its significations"),
    ("stellium_general", "multi_conjunction", "stellium_dasha_activation", {},
     "mixed", "strong",
     ["career_status", "wealth"],
     ["stellium", "conjunction", "saravali", "dasha_activation"],
     "Ch.24 v.27",
     "Any stellium: results manifest most powerfully during dasha-bhukti "
     "periods of planets within the stellium, cascading activation pattern"),
    ("stellium_general", "multi_conjunction", "stellium_transit_trigger", {},
     "mixed", "strong",
     ["career_status", "longevity"],
     ["stellium", "conjunction", "saravali", "transit_trigger"],
     "Ch.24 v.28",
     "Any stellium: transits of slow planets (Saturn, Jupiter, Rahu) over "
     "the stellium sign trigger major life events involving all conjoined planets"),
    ("stellium_general", "multi_conjunction", "stellium_eclipse_sensitivity", {},
     "unfavorable", "strong",
     ["mental_health", "physical_health"],
     ["stellium", "conjunction", "saravali", "eclipse"],
     "Ch.24 v.29",
     "Any stellium: solar or lunar eclipse in the stellium sign causes "
     "dramatic upheaval in the native's life, affecting all conjoined significations"),
    ("stellium_general", "multi_conjunction", "stellium_dignity_composite", {},
     "mixed", "moderate",
     ["career_status", "wealth"],
     ["stellium", "conjunction", "saravali", "composite_dignity"],
     "Ch.24 v.30",
     "Any stellium: the overall dignity of the group determines net results; "
     "more planets in own/exaltation signs produce favorable stellium outcomes"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# Special Conjunction Conditions — Ch.24 (SAV1021–SAV1040)
# ═══════════════════════════════════════════════════════════════════════════════
_SPECIAL_CONDITIONS_DATA = [
    # ── Graha Yuddha (Planetary War) ────────────────────────────────────────
    ("graha_yuddha", "conjunction_condition", "planetary_war_general", {},
     "unfavorable", "strong",
     ["career_status", "enemies_litigation"],
     ["graha_yuddha", "planetary_war", "conjunction", "saravali", "special_condition"],
     "Ch.24 v.31",
     "Graha Yuddha (planetary war) in conjunction: when two planets are within "
     "1 degree, the defeated planet's significations suffer severely"),
    ("graha_yuddha", "conjunction_condition", "war_winner_strengthened", {},
     "favorable", "moderate",
     ["career_status", "fame_reputation"],
     ["graha_yuddha", "planetary_war", "conjunction", "saravali", "winner"],
     "Ch.24 v.32",
     "Planetary war winner in conjunction: the victorious planet (brighter/more "
     "northern) gains extra strength, its significations prosper unusually"),
    ("graha_yuddha", "conjunction_condition", "war_loser_weakened", {},
     "unfavorable", "strong",
     ["career_status", "physical_health"],
     ["graha_yuddha", "planetary_war", "conjunction", "saravali", "loser"],
     "Ch.24 v.33",
     "Planetary war loser in conjunction: the defeated planet acts as severely "
     "debilitated, its house lordships and karakatvas are deeply compromised"),
    ("graha_yuddha", "conjunction_condition", "war_in_stellium", {},
     "unfavorable", "strong",
     ["career_status", "enemies_litigation"],
     ["graha_yuddha", "planetary_war", "conjunction", "saravali", "stellium"],
     "Ch.24 v.34",
     "Planetary war within a stellium: intensifies conflict in the native's life, "
     "internal contradictions and external battles, divided loyalties"),

    # ── Combustion in Multi-Planet Conjunctions ─────────────────────────────
    ("combustion_conjunction", "conjunction_condition", "multiple_combust", {},
     "unfavorable", "strong",
     ["career_status", "intelligence_education"],
     ["combustion", "conjunction", "saravali", "special_condition", "multiple"],
     "Ch.24 v.35",
     "Multiple planets combust in conjunction: Sun overpowers several planets, "
     "their significations become dormant, native lacks agency in those areas"),
    ("combustion_conjunction", "conjunction_condition", "combust_benefic", {},
     "unfavorable", "strong",
     ["wealth", "intelligence_education"],
     ["combustion", "conjunction", "saravali", "special_condition", "benefic"],
     "Ch.24 v.36",
     "Benefic planet combust in multi-conjunction: loss of the benefic's "
     "protective influence, wisdom or wealth denied despite other strengths"),
    ("combustion_conjunction", "conjunction_condition", "combust_malefic", {},
     "mixed", "moderate",
     ["enemies_litigation", "career_status"],
     ["combustion", "conjunction", "saravali", "special_condition", "malefic"],
     "Ch.24 v.37",
     "Malefic planet combust in multi-conjunction: malefic's destructive power "
     "reduced by Sun, mixed results as both harm and protection diminish"),

    # ── Retrograde Planets in Conjunction ───────────────────────────────────
    ("retrograde_conjunction", "conjunction_condition", "retrograde_in_group", {},
     "mixed", "moderate",
     ["career_status", "character_temperament"],
     ["retrograde", "conjunction", "saravali", "special_condition", "vakri"],
     "Ch.24 v.38",
     "Retrograde planet in multi-conjunction: revisits and reworks the themes "
     "of conjunction, delayed but intensified results, unconventional expression"),
    ("retrograde_conjunction", "conjunction_condition", "retrograde_benefic_conj", {},
     "favorable", "moderate",
     ["wealth", "intelligence_education"],
     ["retrograde", "conjunction", "saravali", "special_condition", "benefic", "vakri"],
     "Ch.24 v.39",
     "Retrograde benefic in conjunction: enhanced benefic results through "
     "re-examination, delayed blessings arrive in unusual or unexpected forms"),
    ("retrograde_conjunction", "conjunction_condition", "retrograde_malefic_conj", {},
     "unfavorable", "moderate",
     ["physical_health", "enemies_litigation"],
     ["retrograde", "conjunction", "saravali", "special_condition", "malefic", "vakri"],
     "Ch.24 v.40",
     "Retrograde malefic in conjunction: intensified malefic effect, revisits "
     "old karmic debts, chronic or recurring problems in the affected areas"),

    # ── Conjunction at Sign Boundaries (Sandhi) ─────────────────────────────
    ("sandhi_conjunction", "conjunction_condition", "rashi_sandhi", {},
     "unfavorable", "moderate",
     ["career_status", "character_temperament"],
     ["sandhi", "conjunction", "saravali", "special_condition", "rashi_boundary"],
     "Ch.24 v.41",
     "Conjunction at rashi sandhi (sign boundary): planets lose directional "
     "strength, confused significations, native lacks clear identity or purpose"),
    ("sandhi_conjunction", "conjunction_condition", "sandhi_luminaries", {},
     "unfavorable", "strong",
     ["physical_health", "mental_health"],
     ["sandhi", "conjunction", "saravali", "special_condition", "luminaries"],
     "Ch.24 v.42",
     "Luminaries at rashi sandhi in conjunction: weakened vitality and mind, "
     "health issues at transitions, identity crisis during major life changes"),
    ("sandhi_conjunction", "conjunction_condition", "sandhi_stellium", {},
     "unfavorable", "strong",
     ["career_status", "longevity"],
     ["sandhi", "conjunction", "saravali", "special_condition", "stellium"],
     "Ch.24 v.43",
     "Stellium at rashi sandhi: entire group of planets weakened, life direction "
     "unclear, major decisions plagued by uncertainty and reversal"),

    # ── Conjunction at Gandanta Points ──────────────────────────────────────
    ("gandanta_conjunction", "conjunction_condition", "gandanta_general", {},
     "unfavorable", "strong",
     ["longevity", "mental_health"],
     ["gandanta", "conjunction", "saravali", "special_condition", "water_fire"],
     "Ch.24 v.44",
     "Conjunction at gandanta (water-fire sign junction): extreme karmic knot, "
     "life-threatening events at birth or major transitions, spiritual crisis"),
    ("gandanta_conjunction", "conjunction_condition", "gandanta_moon", {},
     "unfavorable", "strong",
     ["mental_health", "longevity"],
     ["gandanta", "conjunction", "saravali", "special_condition", "moon"],
     "Ch.24 v.45",
     "Moon in gandanta within a conjunction: severe emotional distress, "
     "mother's health at risk, mind trapped between material and spiritual"),
    ("gandanta_conjunction", "conjunction_condition", "gandanta_stellium", {},
     "unfavorable", "strong",
     ["longevity", "physical_health"],
     ["gandanta", "conjunction", "saravali", "special_condition", "stellium"],
     "Ch.24 v.46",
     "Stellium at gandanta point: multiple planets at the karmic knot, "
     "extremely intense life experiences, potential for extraordinary transformation"),

    # ── Nodal Axis with Conjunction Groups ──────────────────────────────────
    ("nodal_conjunction", "conjunction_condition", "rahu_with_group", {},
     "unfavorable", "strong",
     ["mental_health", "character_temperament"],
     ["rahu", "conjunction", "saravali", "special_condition", "nodal_axis"],
     "Ch.24 v.47",
     "Rahu conjoined with a planetary group: amplifies desires and obsessions "
     "related to the conjoined planets, unconventional or taboo expressions"),
    ("nodal_conjunction", "conjunction_condition", "ketu_with_group", {},
     "mixed", "strong",
     ["spirituality", "career_status"],
     ["ketu", "conjunction", "saravali", "special_condition", "nodal_axis"],
     "Ch.24 v.48",
     "Ketu conjoined with a planetary group: detachment from significations of "
     "conjoined planets, spiritual insight but worldly losses in those areas"),
    ("nodal_conjunction", "conjunction_condition", "rahu_ketu_axis_stellium", {},
     "unfavorable", "strong",
     ["mental_health", "longevity"],
     ["rahu", "ketu", "conjunction", "saravali", "special_condition", "axis_stellium"],
     "Ch.24 v.49",
     "Stellium along Rahu-Ketu axis: eclipse-like effect on entire group, "
     "karmic intensity at maximum, life of extreme events and transformations"),
    ("nodal_conjunction", "conjunction_condition", "nodes_eclipse_conjunction", {},
     "unfavorable", "strong",
     ["physical_health", "mental_health"],
     ["rahu", "ketu", "conjunction", "saravali", "special_condition", "eclipse"],
     "Ch.24 v.50",
     "Nodal conjunction during eclipse in natal chart: most severe form of "
     "conjunction affliction, life-altering events, requires strong remedial measures"),
]


# ── Builder ──────────────────────────────────────────────────────────────────

def _make_multi_conjunction_rules(
    group_label: str,
    planets: list[str],
    data: list,
    start_num: int,
    chapter: str,
) -> list[RuleRecord]:
    """Build RuleRecord objects for a multi-planet conjunction group."""
    rules: list[RuleRecord] = []
    num = start_num
    for entry in data:
        (planet_group, ptype, label, _conditions,
         odir, oint, odoms, extra_tags, vref, desc) = entry

        rid = f"SAV{num:03d}"

        if ptype == "multi_conjunction":
            primary = {
                "planet": planet_group,
                "placement_type": "multi_conjunction",
                "yoga_label": label,
                "planets": list(planets),
            }
        else:
            primary = {
                "planet": planet_group,
                "placement_type": "conjunction_condition",
                "yoga_label": label,
                "planets": list(planets),
            }

        # Character/personality rules are unspecified; others dasha-dependent
        if any(d in odoms for d in ("character_temperament", "physical_appearance")):
            timing = "unspecified"
        else:
            timing = "dasha_dependent"

        tags = list(dict.fromkeys(
            ["saravali", "parashari", "conjunction", group_label] + extra_tags
        ))

        rules.append(RuleRecord(
            rule_id=rid,
            source="Saravali",
            chapter=chapter,
            school="parashari",
            category="conjunction_predictions",
            description=f"[Saravali — {group_label}] {desc}",
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
    # ── Three-planet conjunctions (SAV911–SAV990) ───────────────────────────
    sun_moon_mars = _make_multi_conjunction_rules(
        "sun_moon_mars", ["sun", "moon", "mars"],
        _SUN_MOON_MARS_DATA, 911, "Ch.23",
    )
    sun_moon_mercury = _make_multi_conjunction_rules(
        "sun_moon_mercury", ["sun", "moon", "mercury"],
        _SUN_MOON_MERCURY_DATA, 916, "Ch.23",
    )
    sun_moon_jupiter = _make_multi_conjunction_rules(
        "sun_moon_jupiter", ["sun", "moon", "jupiter"],
        _SUN_MOON_JUPITER_DATA, 921, "Ch.23",
    )
    sun_mars_mercury = _make_multi_conjunction_rules(
        "sun_mars_mercury", ["sun", "mars", "mercury"],
        _SUN_MARS_MERCURY_DATA, 926, "Ch.23",
    )
    sun_mars_jupiter = _make_multi_conjunction_rules(
        "sun_mars_jupiter", ["sun", "mars", "jupiter"],
        _SUN_MARS_JUPITER_DATA, 931, "Ch.23",
    )
    sun_mercury_jupiter = _make_multi_conjunction_rules(
        "sun_mercury_jupiter", ["sun", "mercury", "jupiter"],
        _SUN_MERCURY_JUPITER_DATA, 936, "Ch.23",
    )
    moon_mars_mercury = _make_multi_conjunction_rules(
        "moon_mars_mercury", ["moon", "mars", "mercury"],
        _MOON_MARS_MERCURY_DATA, 941, "Ch.23",
    )
    moon_mars_jupiter = _make_multi_conjunction_rules(
        "moon_mars_jupiter", ["moon", "mars", "jupiter"],
        _MOON_MARS_JUPITER_DATA, 946, "Ch.23",
    )
    moon_mercury_jupiter = _make_multi_conjunction_rules(
        "moon_mercury_jupiter", ["moon", "mercury", "jupiter"],
        _MOON_MERCURY_JUPITER_DATA, 951, "Ch.23",
    )
    mars_mercury_jupiter = _make_multi_conjunction_rules(
        "mars_mercury_jupiter", ["mars", "mercury", "jupiter"],
        _MARS_MERCURY_JUPITER_DATA, 956, "Ch.23",
    )
    sun_venus_saturn = _make_multi_conjunction_rules(
        "sun_venus_saturn", ["sun", "venus", "saturn"],
        _SUN_VENUS_SATURN_DATA, 961, "Ch.23",
    )
    moon_venus_saturn = _make_multi_conjunction_rules(
        "moon_venus_saturn", ["moon", "venus", "saturn"],
        _MOON_VENUS_SATURN_DATA, 966, "Ch.23",
    )
    mars_venus_saturn = _make_multi_conjunction_rules(
        "mars_venus_saturn", ["mars", "venus", "saturn"],
        _MARS_VENUS_SATURN_DATA, 971, "Ch.23",
    )
    mercury_venus_saturn = _make_multi_conjunction_rules(
        "mercury_venus_saturn", ["mercury", "venus", "saturn"],
        _MERCURY_VENUS_SATURN_DATA, 976, "Ch.23",
    )
    jupiter_venus_saturn = _make_multi_conjunction_rules(
        "jupiter_venus_saturn", ["jupiter", "venus", "saturn"],
        _JUPITER_VENUS_SATURN_DATA, 981, "Ch.23",
    )
    three_planet_general = _make_multi_conjunction_rules(
        "three_planet_general", ["three_planet_group"],
        _THREE_PLANET_GENERAL_DATA, 986, "Ch.23",
    )

    # ── Four+ planet conjunctions (SAV991–SAV1020) ──────────────────────────
    four_plus = _make_multi_conjunction_rules(
        "four_plus_planet", ["four_plus_planet_group"],
        _FOUR_PLUS_PLANET_DATA, 991, "Ch.24",
    )

    # ── Special conjunction conditions (SAV1021–SAV1040) ────────────────────
    special = _make_multi_conjunction_rules(
        "special_conjunction_condition", ["conjunction_group"],
        _SPECIAL_CONDITIONS_DATA, 1021, "Ch.24",
    )

    return (
        sun_moon_mars + sun_moon_mercury + sun_moon_jupiter
        + sun_mars_mercury + sun_mars_jupiter + sun_mercury_jupiter
        + moon_mars_mercury + moon_mars_jupiter + moon_mercury_jupiter
        + mars_mercury_jupiter
        + sun_venus_saturn + moon_venus_saturn + mars_venus_saturn
        + mercury_venus_saturn + jupiter_venus_saturn
        + three_planet_general
        + four_plus + special
    )


SARAVALI_CONJUNCTIONS_8_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_CONJUNCTIONS_8_REGISTRY.add(_rule)
