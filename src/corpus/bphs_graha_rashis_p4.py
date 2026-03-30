"""
src/corpus/bphs_graha_rashis_p4.py — BPHS Graha in Rashis Part 4: Saturn+Rahu+Ketu (S232)

Encodes BPHS chapters on graha phala (planetary results) based on rashi
placement. Saturn, Rahu, and Ketu through all 12 signs.

Sources:
  BPHS Ch.23 — Shani (Saturn) in rashi phala
  BPHS Ch.45-46 — Rahu and Ketu in rashi phala
  Traditional commentary (PVRNR edition)

36 rules total: SAR001-SAR012 (Saturn), RHR001-RHR012 (Rahu), KTR001-KTR012 (Ketu).
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_RASHIS_P4_REGISTRY = CorpusRegistry()

_SATURN_IN_RASHIS = [
    RuleRecord(
        rule_id="SAR001",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Aries (debilitation rashi, neecha at 20° Aries): "
            "Saturn's restriction clashes with Aries impulsiveness. Delays in "
            "initiatives, frustration with limitations. Hard work eventually pays. "
            "Neecha bhanga by Mars strength or exaltation mitigates."
        ),
        confidence=0.90,
        verse="Ch.23 v.1-3",
        tags=["saturn_in_rashi", "aries", "debilitation", "neecha", "mars_sign", "delay"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR002",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Taurus: persistent, methodical accumulation of wealth. "
            "Venus-ruled sign combines with Saturn for durable financial gains. "
            "Earthy, sensual yet disciplined. Slow but steady material progress."
        ),
        confidence=0.84,
        verse="Ch.23 v.4-5",
        tags=["saturn_in_rashi", "taurus", "venus_sign", "wealth", "persistence", "material"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR003",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Gemini: structured thinking, systematic communication, "
            "serious intellectual pursuits. Mercury-ruled sign gives Saturn "
            "analytical depth. Good for research, administration, law."
        ),
        confidence=0.83,
        verse="Ch.23 v.6-7",
        tags=["saturn_in_rashi", "gemini", "mercury_sign", "systematic", "research", "law"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR004",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Cancer: emotional austerity, family responsibilities, "
            "difficult early home life possible. Moon-ruled sign creates "
            "tension between Saturn's detachment and Cancer's need for nurturing. "
            "Discipline in domestic matters."
        ),
        confidence=0.84,
        verse="Ch.23 v.8-9",
        tags=["saturn_in_rashi", "cancer", "moon_sign", "austerity", "family", "emotional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR005",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Leo: authority earned through discipline, not birth. "
            "Sun-ruled sign creates ego-Saturn tension. Leadership through "
            "hard work and perseverance. Father relationship may be restrictive."
        ),
        confidence=0.83,
        verse="Ch.23 v.10-11",
        tags=["saturn_in_rashi", "leo", "sun_sign", "earned_authority", "discipline"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR006",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Virgo: meticulous, perfectionist discipline, health-conscious. "
            "Mercury-ruled sign harmonizes with Saturn for precise analysis. "
            "Excellent for medicine, engineering, craftsmanship, administration."
        ),
        confidence=0.85,
        verse="Ch.23 v.12-13",
        tags=["saturn_in_rashi", "virgo", "mercury_sign", "meticulous", "health", "engineering"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR007",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Libra (exaltation rashi, peak at 20° Libra): "
            "just, fair, socially conscious. Venus-ruled sign harmonizes "
            "with Saturn for excellent judicial, legal, diplomatic ability. "
            "Discipline in relationships; impartial leadership."
        ),
        confidence=0.93,
        verse="Ch.23 v.14-16",
        tags=["saturn_in_rashi", "libra", "exaltation", "venus_sign", "justice", "law", "diplomacy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR008",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Scorpio: intense discipline, profound transformative work. "
            "Mars-ruled sign creates powerful but difficult placement. "
            "Research, occult mastery, endurance through extreme challenges. "
            "Hidden enemies; sustained effort in darkness."
        ),
        confidence=0.84,
        verse="Ch.23 v.17-18",
        tags=["saturn_in_rashi", "scorpio", "mars_sign", "transformation", "endurance", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR009",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Sagittarius: disciplined philosophy, structured religion, "
            "systematic higher knowledge. Jupiter-ruled sign gives Saturn "
            "dharmic focus. Traditional religious practice, law, "
            "formal higher education."
        ),
        confidence=0.83,
        verse="Ch.23 v.19-20",
        tags=["saturn_in_rashi", "sagittarius", "jupiter_sign", "dharma", "structured_philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR010",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Capricorn (own sign / sva-rashi, moolatrikona 0°-20°): "
            "peak Saturnine expression — disciplined ambition, executive "
            "ability, long-term planning, karmic accountability. "
            "Career success through sustained hard work."
        ),
        confidence=0.95,
        verse="Ch.23 v.21-23",
        tags=["saturn_in_rashi", "capricorn", "own_sign", "moolatrikona", "ambition", "career", "discipline"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR011",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Aquarius (own sign / sva-rashi): humanitarian discipline, "
            "social reform, systematic group work. Saturn fully at home in "
            "Aquarius — collective responsibility, technology, social justice "
            "through structured effort."
        ),
        confidence=0.93,
        verse="Ch.23 v.24-26",
        tags=["saturn_in_rashi", "aquarius", "own_sign", "humanitarian", "reform", "technology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SAR012",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Saturn in Pisces: spiritual discipline, structured mysticism, "
            "karma through isolation or service. Jupiter-ruled sign gives "
            "Saturn compassionate wisdom. Monasteries, ashrams, hospitals — "
            "service in hidden or confined settings."
        ),
        confidence=0.83,
        verse="Ch.23 v.27-28",
        tags=["saturn_in_rashi", "pisces", "jupiter_sign", "spiritual", "isolation", "service"],
        implemented=False,
    ),
]

_RAHU_IN_RASHIS = [
    RuleRecord(
        rule_id="RHR001",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Aries: intense ambition, unconventional courage, desire "
            "for pioneer status. Foreign or unusual expression of Aries energy. "
            "Rahu amplifies Mars themes — explosive initiative, risk-taking."
        ),
        confidence=0.80,
        verse="Ch.45 v.1-2",
        tags=["rahu_in_rashi", "aries", "ambition", "unconventional", "foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR002",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Taurus (considered exaltation by some traditions): "
            "intense desire for material comfort and sensual pleasure. "
            "Strong accumulation drive; possible obsessive relationship "
            "with wealth and beauty."
        ),
        confidence=0.658,
        verse="Ch.45 v.3-4",
        tags=["rahu_in_rashi", "taurus", "exaltation_debated", "material", "wealth", "desire"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR003",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Gemini: obsessive learning, compulsive communication, "
            "extraordinary intellectual curiosity. Foreign languages, technology, "
            "multiple careers. Deceptive communication possible."
        ),
        confidence=0.80,
        verse="Ch.45 v.5-6",
        tags=["rahu_in_rashi", "gemini", "intellect", "communication", "foreign_language"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR004",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Cancer: intense emotional needs, unusual family background, "
            "obsessive nurturing or abandonment themes. Mother relationship "
            "complex or foreign. Deep psychological transformation through family."
        ),
        confidence=0.659,
        verse="Ch.45 v.7-8",
        tags=["rahu_in_rashi", "cancer", "emotional", "family", "mother", "psychology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR005",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Leo: intense desire for recognition, unconventional authority. "
            "Foreign or non-traditional leadership. Fame through unusual means. "
            "Can generate magnetic charisma or arrogant self-promotion."
        ),
        confidence=0.659,
        verse="Ch.45 v.9-10",
        tags=["rahu_in_rashi", "leo", "fame", "authority", "charisma", "unconventional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR006",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Virgo: obsessive precision, unusual healing methods, "
            "compulsive analysis. Foreign medicine or unusual service. "
            "Technology and data analysis. Perfectionist anxiety."
        ),
        confidence=0.659,
        verse="Ch.45 v.11-12",
        tags=["rahu_in_rashi", "virgo", "analysis", "healing", "technology", "obsessive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR007",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Libra (considered exaltation by some traditions): "
            "intense desire for partnerships, unusual relationships. "
            "Foreign spouse or business partners. Social manipulation possible; "
            "also diplomatic innovation."
        ),
        confidence=0.658,
        verse="Ch.45 v.13-14",
        tags=["rahu_in_rashi", "libra", "exaltation_debated", "partnership", "foreign", "social"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR008",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Scorpio: deep occult obsessions, transformative intensity, "
            "research into hidden realms. Powerful but dangerous energy. "
            "Interest in psychology, death, secret societies. Extreme transformation."
        ),
        confidence=0.80,
        verse="Ch.45 v.15-16",
        tags=["rahu_in_rashi", "scorpio", "occult", "transformation", "research", "hidden"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR009",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Sagittarius: obsessive philosophical seeking, unorthodox "
            "religion, foreign teachers. Intense pursuit of higher knowledge. "
            "Pseudo-guru tendencies possible; also genuine spiritual quest."
        ),
        confidence=0.659,
        verse="Ch.45 v.17-18",
        tags=["rahu_in_rashi", "sagittarius", "philosophy", "foreign_teacher", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR010",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Capricorn: intense ambition for career status, unusual "
            "professional path. Foreign corporations or government. "
            "Obsessive work ethic; unconventional rise to authority."
        ),
        confidence=0.659,
        verse="Ch.45 v.19-20",
        tags=["rahu_in_rashi", "capricorn", "career", "ambition", "foreign", "government"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR011",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Aquarius (considered own/strong sign by some traditions): "
            "innovative, technological, unconventional group leadership. "
            "Social media, mass movements, science. Humanitarian goals "
            "pursued through unusual means."
        ),
        confidence=0.658,
        verse="Ch.45 v.21-22",
        tags=["rahu_in_rashi", "aquarius", "technology", "innovation", "social_movement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="RHR012",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Rahu in Pisces: spiritual obsession, foreign spiritual paths, "
            "dissolution of identity boundaries. Intense mysticism, psychic "
            "sensitivity. Possible deception in spiritual matters or "
            "extraordinary spiritual attainment."
        ),
        confidence=0.658,
        verse="Ch.45 v.23-24",
        tags=["rahu_in_rashi", "pisces", "spiritual", "mysticism", "dissolution"],
        implemented=False,
    ),
]

_KETU_IN_RASHIS = [
    RuleRecord(
        rule_id="KTR001",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Aries: past-life warrior energy; detachment from ego and "
            "personal initiatives in this life. Spiritual courage; may lack "
            "self-assertion. Moksha through selfless action."
        ),
        confidence=0.658,
        verse="Ch.46 v.1-2",
        tags=["ketu_in_rashi", "aries", "past_life", "detachment", "moksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR002",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Taurus (considered debilitation by some traditions): "
            "detachment from material comfort and sensory pleasure. "
            "Past life wealth now surrendered. Spiritual value over material value."
        ),
        confidence=0.656,
        verse="Ch.46 v.3-4",
        tags=["ketu_in_rashi", "taurus", "detachment", "material_renunciation", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR003",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Gemini: detachment from intellectual cleverness; past "
            "lifetime of communication mastery. Deeper silence over words. "
            "Spiritual insight through transcending mental chatter."
        ),
        confidence=0.657,
        verse="Ch.46 v.5-6",
        tags=["ketu_in_rashi", "gemini", "detachment", "silence", "past_life_intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR004",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Cancer: detachment from emotional security and mother bond. "
            "Past-life nurturing now renounced. Spiritual home-seeking. "
            "May feel emotionally homeless; transcendence through compassion."
        ),
        confidence=0.657,
        verse="Ch.46 v.7-8",
        tags=["ketu_in_rashi", "cancer", "detachment", "mother", "emotional_release"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR005",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Leo: detachment from ego and authority; past-life royal "
            "or leadership mastery now surrendered. Spiritual humility. "
            "Fame may come unexpectedly but is not sought."
        ),
        confidence=0.657,
        verse="Ch.46 v.9-10",
        tags=["ketu_in_rashi", "leo", "ego_detachment", "humility", "past_life_authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR006",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Virgo (considered exaltation by some traditions): "
            "transcendent precision; past-life mastery of analysis and service. "
            "Spiritual discrimination; selfless healing or craft. "
            "Detachment from perfectionism enables deeper wisdom."
        ),
        confidence=0.657,
        verse="Ch.46 v.11-12",
        tags=["ketu_in_rashi", "virgo", "exaltation_debated", "healing", "discrimination", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR007",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Libra (considered debilitation by some traditions): "
            "detachment from relationships and social harmony. Past-life "
            "partnership mastery; solitary path in this life. "
            "Spiritual through aloneness."
        ),
        confidence=0.656,
        verse="Ch.46 v.13-14",
        tags=["ketu_in_rashi", "libra", "debilitation_debated", "detachment", "solitary"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR008",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Scorpio: deep occult insights, liberation through "
            "transformation. Past-life mastery of hidden knowledge. "
            "Natural psychic ability; detachment from death-fear. "
            "Powerful moksha indicator."
        ),
        confidence=0.659,
        verse="Ch.46 v.15-16",
        tags=["ketu_in_rashi", "scorpio", "moksha", "occult", "psychic", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR009",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Sagittarius: detachment from formal religion and dogma; "
            "inner spiritual quest over external rituals. Past-life philosophical "
            "mastery. Direct experience of truth over textbook knowledge."
        ),
        confidence=0.658,
        verse="Ch.46 v.17-18",
        tags=["ketu_in_rashi", "sagittarius", "spiritual_quest", "anti_dogma", "past_life_philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR010",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Capricorn: detachment from career ambition and worldly "
            "status. Past-life professional mastery; this life points toward "
            "spiritual work. Service without recognition."
        ),
        confidence=0.657,
        verse="Ch.46 v.19-20",
        tags=["ketu_in_rashi", "capricorn", "career_detachment", "spiritual_service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR011",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Aquarius: detachment from group identity and social causes. "
            "Past-life humanitarian mastery. Individual spiritual path over "
            "collective movements. Inner freedom over social belonging."
        ),
        confidence=0.656,
        verse="Ch.46 v.21-22",
        tags=["ketu_in_rashi", "aquarius", "group_detachment", "individual_path", "inner_freedom"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KTR012",
        source="BPHS",
        chapter="Ch.46",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Ketu in Pisces (considered own/strong sign by some traditions): "
            "ultimate moksha position — total dissolution, spiritual liberation, "
            "merging with the infinite. Past-life mysticism transcended. "
            "Strongest Ketu for spiritual enlightenment."
        ),
        confidence=0.80,
        verse="Ch.46 v.23-24",
        tags=["ketu_in_rashi", "pisces", "moksha", "liberation", "dissolution", "enlightenment"],
        implemented=False,
    ),
]

for _r in _SATURN_IN_RASHIS + _RAHU_IN_RASHIS + _KETU_IN_RASHIS:
    BPHS_GRAHA_RASHIS_P4_REGISTRY.add(_r)
