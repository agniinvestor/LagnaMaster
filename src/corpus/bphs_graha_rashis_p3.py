"""
src/corpus/bphs_graha_rashis_p3.py — BPHS Graha in Rashis Part 3: Jupiter + Venus (S231)

Encodes BPHS chapters on graha phala (planetary results) based on rashi
placement. Jupiter and Venus through all 12 signs.

Sources:
  BPHS Ch.21-22 — Guru (Jupiter) and Shukra (Venus) in rashi phala
  Traditional commentary (PVRNR edition)

24 rules total: JUR001-JUR012 (Jupiter in rashis), VER001-VER012 (Venus in rashis).
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_RASHIS_P3_REGISTRY = CorpusRegistry()

_JUPITER_IN_RASHIS = [
    RuleRecord(
        rule_id="JUR001",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Aries: enthusiastic expansion, bold idealism, "
            "pioneering philosophy. Mars-ruled sign gives Jupiter directness "
            "in teaching and guidance. Leadership in education or religion."
        ),
        confidence=0.85,
        verse="Ch.21 v.1-2",
        tags=["jupiter_in_rashi", "aries", "mars_sign", "leadership", "philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR002",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Taurus: material abundance, generous nature, love of "
            "comfort and beauty. Venus-ruled sign blends Jupiter's expansion "
            "with Venusian pleasure. Wealth through arts or education."
        ),
        confidence=0.85,
        verse="Ch.21 v.3-4",
        tags=["jupiter_in_rashi", "taurus", "venus_sign", "abundance", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR003",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Gemini: intellectual expansion, versatile wisdom, "
            "love of learning and communication. Mercury-ruled sign gives "
            "Jupiter a rational, analytical quality. Teaching and writing."
        ),
        confidence=0.84,
        verse="Ch.21 v.5-6",
        tags=["jupiter_in_rashi", "gemini", "mercury_sign", "intellect", "teaching"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR004",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Cancer (exaltation rashi, peak at 5° Cancer): "
            "maximum benefic expression — nurturing wisdom, deep compassion, "
            "spiritual devotion, domestic abundance. Strongest placement for "
            "Jupiter; excellent for family, spirituality, and wealth."
        ),
        confidence=0.95,
        verse="Ch.21 v.7-9",
        tags=["jupiter_in_rashi", "cancer", "exaltation", "moon_sign", "compassion", "spiritual", "abundance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR005",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Leo: magnanimous, royal wisdom, generous leadership. "
            "Sun-ruled sign amplifies Jupiter for public recognition, authority "
            "in education or religion. Prideful but broadly benevolent."
        ),
        confidence=0.86,
        verse="Ch.21 v.10-11",
        tags=["jupiter_in_rashi", "leo", "sun_sign", "generosity", "authority", "recognition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR006",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Virgo: analytical wisdom, practical knowledge, "
            "service-oriented teaching. Mercury-ruled sign channels Jupiter "
            "into detail and craft. Good for medicine, editing, technical "
            "education. May over-analyze or be pedantic."
        ),
        confidence=0.83,
        verse="Ch.21 v.12-13",
        tags=["jupiter_in_rashi", "virgo", "mercury_sign", "analytical", "service", "medicine"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR007",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Libra: balanced philosophy, justice, diplomatic wisdom. "
            "Venus-ruled sign gives Jupiter social grace and fairness. "
            "Good for law, counseling, partnerships. Religious harmony."
        ),
        confidence=0.84,
        verse="Ch.21 v.14-15",
        tags=["jupiter_in_rashi", "libra", "venus_sign", "justice", "law", "diplomacy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR008",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Scorpio: deep spiritual wisdom, occult knowledge, "
            "transformative teaching. Mars-ruled sign gives Jupiter depth "
            "and intensity. Research into hidden or esoteric matters. "
            "Profound but secretive guidance."
        ),
        confidence=0.84,
        verse="Ch.21 v.16-17",
        tags=["jupiter_in_rashi", "scorpio", "mars_sign", "spiritual", "occult", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR009",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Sagittarius (own sign / sva-rashi, moolatrikona 0°-10°): "
            "peak Jupiterian expression — philosophical mastery, ethical "
            "teaching, dharmic leadership, higher education, law. "
            "Excellent for guru role, teaching, publishing."
        ),
        confidence=0.95,
        verse="Ch.21 v.18-20",
        tags=["jupiter_in_rashi", "sagittarius", "own_sign", "moolatrikona", "dharma", "philosophy", "teaching"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR010",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Capricorn (debilitation rashi, neecha at 5° Capricorn): "
            "expansion restricted by Saturn's structure. Wisdom becomes "
            "pragmatic but loses idealism. Material focus over spiritual. "
            "Neecha bhanga by Saturn strength or exchange helps."
        ),
        confidence=0.90,
        verse="Ch.21 v.21-23",
        tags=["jupiter_in_rashi", "capricorn", "debilitation", "neecha", "saturn_sign", "material"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR011",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Aquarius: universal wisdom, humanitarian ideals, "
            "social philosophy. Saturn-ruled sign gives Jupiter group "
            "consciousness and reform orientation. Teaching to the masses, "
            "social justice, scientific philosophy."
        ),
        confidence=0.83,
        verse="Ch.21 v.24-25",
        tags=["jupiter_in_rashi", "aquarius", "saturn_sign", "humanitarian", "reform", "universal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JUR012",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Jupiter in Pisces (own sign / sva-rashi): spiritual wisdom, "
            "compassionate grace, mystical insight. Pisces gives Jupiter "
            "its most transcendent expression. Excellent for spiritual "
            "teaching, healing, meditation, moksha path."
        ),
        confidence=0.93,
        verse="Ch.21 v.26-27",
        tags=["jupiter_in_rashi", "pisces", "own_sign", "spiritual", "moksha", "compassion"],
        implemented=False,
    ),
]

_VENUS_IN_RASHIS = [
    RuleRecord(
        rule_id="VER001",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Aries: passionate, impulsive love, bold aesthetic. "
            "Mars-ruled sign gives Venus directness in relationships. "
            "Quick attractions, loves adventure and novelty. "
            "Financial gains through bold action."
        ),
        confidence=0.83,
        verse="Ch.22 v.1-2",
        tags=["venus_in_rashi", "aries", "mars_sign", "passion", "impulsive_love"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER002",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Taurus (own sign / sva-rashi, moolatrikona 0°-15°): "
            "sensual pleasure, luxury, artistic mastery, financial acumen. "
            "Stable relationships, love of beauty and comfort. "
            "Best placement for wealth through arts or trade."
        ),
        confidence=0.95,
        verse="Ch.22 v.3-5",
        tags=["venus_in_rashi", "taurus", "own_sign", "moolatrikona", "luxury", "wealth", "art"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER003",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Gemini: charming communicator, intellectually attractive, "
            "versatile in relationships. Mercury-ruled sign gives Venus wit "
            "and adaptability. Writing about love, communication in arts."
        ),
        confidence=0.84,
        verse="Ch.22 v.6-7",
        tags=["venus_in_rashi", "gemini", "mercury_sign", "charm", "communication", "versatile"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER004",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Cancer: nurturing love, domestic beauty, emotional "
            "attachment in relationships. Moon-ruled sign makes Venus "
            "deeply sentimental. Family-centered; home as a place of beauty."
        ),
        confidence=0.84,
        verse="Ch.22 v.8-9",
        tags=["venus_in_rashi", "cancer", "moon_sign", "nurturing", "home", "sentimental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER005",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Leo: dramatic, generous, proud in love. Sun-ruled "
            "sign amplifies Venus for theatrical romance, artistic "
            "performance, luxury display. Lavish affection; seeks admiration."
        ),
        confidence=0.85,
        verse="Ch.22 v.10-11",
        tags=["venus_in_rashi", "leo", "sun_sign", "drama", "performance", "generosity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER006",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Virgo (debilitation rashi, neecha at 27° Virgo): "
            "critical in love, perfectionist tendencies undermine romance. "
            "Mercury-ruled sign makes Venus over-analytical about relationships. "
            "Neecha bhanga by Mercury strength helps."
        ),
        confidence=0.90,
        verse="Ch.22 v.12-14",
        tags=["venus_in_rashi", "virgo", "debilitation", "neecha", "mercury_sign", "critical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER007",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Libra (own sign / sva-rashi): harmonious relationships, "
            "refined aesthetics, social grace. Balanced love and fairness "
            "in partnerships. Excellent for marriage, arts, diplomacy, luxury trade."
        ),
        confidence=0.94,
        verse="Ch.22 v.15-17",
        tags=["venus_in_rashi", "libra", "own_sign", "harmony", "partnership", "art", "diplomacy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER008",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Scorpio: intense, passionate, transformative love. "
            "Mars-ruled sign gives Venus depth and obsessive quality. "
            "Strong sexuality, hidden relationships possible. "
            "Wealth through joint resources or inheritance."
        ),
        confidence=0.84,
        verse="Ch.22 v.18-19",
        tags=["venus_in_rashi", "scorpio", "mars_sign", "passion", "intensity", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER009",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Sagittarius: philosophical love, adventurous romance, "
            "love of foreign cultures. Jupiter-ruled sign gives Venus "
            "idealism and expansiveness. Relationships with teachers or "
            "across cultural/religious boundaries."
        ),
        confidence=0.83,
        verse="Ch.22 v.20-21",
        tags=["venus_in_rashi", "sagittarius", "jupiter_sign", "adventure", "foreign", "idealism"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER010",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Capricorn: disciplined, practical, status-conscious "
            "in love and money. Saturn-ruled sign gives Venus ambition "
            "in relationships — prefers established, successful partners. "
            "Wealth through sustained effort; delayed but lasting pleasures."
        ),
        confidence=0.83,
        verse="Ch.22 v.22-23",
        tags=["venus_in_rashi", "capricorn", "saturn_sign", "practical", "status", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER011",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Aquarius: unconventional love, humanitarian aesthetics, "
            "progressive relationships. Saturn-ruled sign makes Venus "
            "emotionally detached but socially conscious. Artistic innovation, "
            "open relationship structures possible."
        ),
        confidence=0.82,
        verse="Ch.22 v.24-25",
        tags=["venus_in_rashi", "aquarius", "saturn_sign", "unconventional", "social", "innovation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VER012",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Venus in Pisces (exaltation rashi, peak at 27° Pisces): "
            "most spiritually refined Venus — selfless love, transcendent beauty, "
            "mystical arts. Jupiter-ruled sign elevates Venus for spiritual "
            "devotion through beauty. Excellent for healing arts, music, dance."
        ),
        confidence=0.95,
        verse="Ch.22 v.26-28",
        tags=["venus_in_rashi", "pisces", "exaltation", "jupiter_sign", "spiritual", "selfless_love", "art"],
        implemented=False,
    ),
]

for _r in _JUPITER_IN_RASHIS + _VENUS_IN_RASHIS:
    BPHS_GRAHA_RASHIS_P3_REGISTRY.add(_r)
