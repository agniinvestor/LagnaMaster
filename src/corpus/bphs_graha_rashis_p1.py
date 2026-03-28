"""
src/corpus/bphs_graha_rashis_p1.py — BPHS Graha in Rashis Part 1: Sun + Moon (S229)

Encodes BPHS chapters on graha phala (planetary results) based on rashi
placement. Sun and Moon through all 12 signs.

Sources:
  BPHS Ch.3 — Graha Gunadi Adhyaya (planetary qualities per rashi)
  BPHS Ch.17-18 — Graha in rashi phala
  Traditional commentary (PVRNR edition)

24 rules total: SUR001-SUR012 (Sun in rashis), MOR001-MOR012 (Moon in rashis).
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_RASHIS_P1_REGISTRY = CorpusRegistry()

_RASHIS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

_SUN_IN_RASHIS = [
    RuleRecord(
        rule_id="SUR001",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Aries (own-rashi ally, exaltation in same sign region): "
            "strong vitality, leadership, courageous temperament. Pioneer nature. "
            "Good for career in government or authority roles. Sun is exalted at "
            "10° Aries — peak strength here."
        ),
        confidence=0.92,
        verse="Ch.17 v.1-3",
        tags=["sun_in_rashi", "aries", "exaltation_zone", "leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR002",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Taurus: moderate vitality, fondness for comfort and luxury. "
            "Practical, persistent nature. Financial concerns may dominate. "
            "Sun loses some directness in Venus-ruled sign; diplomacy required."
        ),
        confidence=0.85,
        verse="Ch.17 v.4-5",
        tags=["sun_in_rashi", "taurus", "venus_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR003",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Gemini: intellectual vitality, communicative, versatile "
            "disposition. Good for writing, teaching, trade. Mercury-ruled sign "
            "gives Sun a more analytical and adaptable quality."
        ),
        confidence=0.85,
        verse="Ch.17 v.6-7",
        tags=["sun_in_rashi", "gemini", "mercury_sign", "intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR004",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Cancer: emotional sensitivity despite solar strength. "
            "Strong mother-connection, nurturing leadership. Moon-ruled sign "
            "softens the Sun's directness; mood fluctuations possible."
        ),
        confidence=0.85,
        verse="Ch.17 v.8-9",
        tags=["sun_in_rashi", "cancer", "moon_sign", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR005",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Leo (own sign / sva-rashi): maximum solar dignity in Leo. "
            "Commanding presence, natural authority, pride, generosity. "
            "Government service, politics, leadership roles strongly favored. "
            "Moolatrikona: 1°-20° Leo."
        ),
        confidence=0.95,
        verse="Ch.17 v.10-12",
        tags=["sun_in_rashi", "leo", "own_sign", "moolatrikona", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR006",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Virgo: detail-oriented leadership, service-minded nature. "
            "Health consciousness, analytical thinking. Mercury-ruled sign gives "
            "a methodical quality to solar expression. Good for medicine, analysis."
        ),
        confidence=0.83,
        verse="Ch.17 v.13-14",
        tags=["sun_in_rashi", "virgo", "mercury_sign", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR007",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Libra (debilitation rashi, neecha at 10° Libra): diminished "
            "solar vitality, compromise and partnership over self-assertion. "
            "Authority challenged; may work under others. Neecha bhanga can "
            "mitigate if Venus is strong."
        ),
        confidence=0.90,
        verse="Ch.17 v.15-17",
        tags=["sun_in_rashi", "libra", "debilitation", "neecha", "venus_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR008",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Scorpio: intense, investigative leadership. Mars-ruled sign "
            "combines with Sun for fierce determination. Interest in occult, "
            "research, hidden matters. Transformative life events."
        ),
        confidence=0.84,
        verse="Ch.17 v.18-19",
        tags=["sun_in_rashi", "scorpio", "mars_sign", "occult", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR009",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Sagittarius: philosophical, ethical, optimistic leadership. "
            "Jupiter-ruled sign elevates Sun toward dharma and higher knowledge. "
            "Good for law, teaching, religion, higher education."
        ),
        confidence=0.87,
        verse="Ch.17 v.20-21",
        tags=["sun_in_rashi", "sagittarius", "jupiter_sign", "dharma", "philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR010",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Capricorn: disciplined, career-oriented, ambitious nature. "
            "Saturn-ruled sign creates tension between solar ego and saturnine "
            "restraint. Authority earned through hard work, not birth. "
            "Father relationship may be distant or demanding."
        ),
        confidence=0.84,
        verse="Ch.17 v.22-23",
        tags=["sun_in_rashi", "capricorn", "saturn_sign", "ambition", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR011",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Aquarius: humanitarian ideals, group leadership, social "
            "consciousness. Saturn-ruled sign gives Sun a more detached, "
            "universal quality. Politics, social reform, scientific pursuits."
        ),
        confidence=0.83,
        verse="Ch.17 v.24-25",
        tags=["sun_in_rashi", "aquarius", "saturn_sign", "humanitarian"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SUR012",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Sun in Pisces: spiritual, compassionate, creative leadership. "
            "Jupiter-ruled sign gives Sun a mystical, introspective quality. "
            "Good for spiritual pursuits, arts, healing. May lack assertiveness."
        ),
        confidence=0.83,
        verse="Ch.17 v.26-27",
        tags=["sun_in_rashi", "pisces", "jupiter_sign", "spiritual", "compassion"],
        implemented=False,
    ),
]

_MOON_IN_RASHIS = [
    RuleRecord(
        rule_id="MOR001",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Aries: emotionally impulsive, energetic, pioneering feelings. "
            "Quick emotional reactions, leadership instinct. Physical activity "
            "channels emotional energy. Independent emotional nature."
        ),
        confidence=0.87,
        verse="Ch.18 v.1-3",
        tags=["moon_in_rashi", "aries", "mars_sign", "impulsive", "energy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR002",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Taurus (exaltation rashi, peak at 3° Taurus): most stable "
            "emotional expression. Sensual, comfort-seeking, aesthetically "
            "inclined. Strong attachment to family and possessions. "
            "Good for wealth accumulation through steady effort."
        ),
        confidence=0.93,
        verse="Ch.18 v.4-6",
        tags=["moon_in_rashi", "taurus", "exaltation", "venus_sign", "stability", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR003",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Gemini: intellectually curious emotional nature, versatile "
            "feelings, need for mental stimulation. Good communicator, adaptable. "
            "Multiple interests; may scatter emotional energy."
        ),
        confidence=0.85,
        verse="Ch.18 v.7-8",
        tags=["moon_in_rashi", "gemini", "mercury_sign", "intellect", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR004",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Cancer (own sign / sva-rashi): strongest lunar dignity. "
            "Deep emotional sensitivity, nurturing, strong mother bond. "
            "Psychic ability, strong intuition, protective instincts. "
            "Home and family are paramount concerns."
        ),
        confidence=0.95,
        verse="Ch.18 v.9-11",
        tags=["moon_in_rashi", "cancer", "own_sign", "mother", "intuition", "nurturing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR005",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Leo: emotionally dramatic, proud, generous feelings. "
            "Need for recognition and appreciation. Leadership through emotional "
            "expression. Strong ego involvement in feelings."
        ),
        confidence=0.85,
        verse="Ch.18 v.12-13",
        tags=["moon_in_rashi", "leo", "sun_sign", "drama", "pride", "generosity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR006",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Virgo: emotionally analytical, service-oriented feelings. "
            "Worry-prone, perfectionist tendencies. Health consciousness, "
            "detail-oriented emotional processing. Good for healing arts."
        ),
        confidence=0.84,
        verse="Ch.18 v.14-15",
        tags=["moon_in_rashi", "virgo", "mercury_sign", "analytical", "service", "health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR007",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Libra: emotionally balanced, harmonious, partnership-oriented. "
            "Need for fairness and social connection. Artistic sensibility. "
            "Indecisive at times; strong need for relationship harmony."
        ),
        confidence=0.85,
        verse="Ch.18 v.16-17",
        tags=["moon_in_rashi", "libra", "venus_sign", "harmony", "partnership", "art"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR008",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Scorpio (debilitation rashi, neecha at 3° Scorpio): intense, "
            "deep, potentially turbulent emotional life. Passionate, secretive, "
            "transformative. Strong psychic sensitivity but prone to emotional "
            "extremes. Neecha bhanga by Mars strength mitigates."
        ),
        confidence=0.90,
        verse="Ch.18 v.18-20",
        tags=["moon_in_rashi", "scorpio", "debilitation", "neecha", "mars_sign", "intensity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR009",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Sagittarius: emotionally optimistic, philosophical, "
            "freedom-loving. Enthusiasm and expansiveness in feeling. "
            "Love of travel, teaching, higher ideals. Spiritual emotion."
        ),
        confidence=0.85,
        verse="Ch.18 v.21-22",
        tags=["moon_in_rashi", "sagittarius", "jupiter_sign", "optimism", "philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR010",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Capricorn: emotionally reserved, disciplined, practical. "
            "Delayed emotional expression, ambition in feelings. Saturn-ruled "
            "sign gives structure to emotions. Career-oriented emotional security."
        ),
        confidence=0.84,
        verse="Ch.18 v.23-24",
        tags=["moon_in_rashi", "capricorn", "saturn_sign", "reserved", "ambition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR011",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Aquarius: emotionally detached, humanitarian, group-oriented. "
            "Unconventional emotional expression, independent streak. Friends and "
            "social causes matter more than personal attachments."
        ),
        confidence=0.83,
        verse="Ch.18 v.25-26",
        tags=["moon_in_rashi", "aquarius", "saturn_sign", "detachment", "humanitarian"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MOR012",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Moon in Pisces: emotionally receptive, empathic, spiritual. "
            "Strong imagination and intuition. Boundaries between self and others "
            "may blur. Artistic and mystical tendencies. "
            "Strong connection to collective unconscious."
        ),
        confidence=0.85,
        verse="Ch.18 v.27-28",
        tags=["moon_in_rashi", "pisces", "jupiter_sign", "empathy", "spiritual", "intuition"],
        implemented=False,
    ),
]

for _r in _SUN_IN_RASHIS + _MOON_IN_RASHIS:
    BPHS_GRAHA_RASHIS_P1_REGISTRY.add(_r)
