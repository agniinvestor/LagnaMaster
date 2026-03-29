"""
src/corpus/bphs_graha_rashis_p2.py — BPHS Graha in Rashis Part 2: Mars + Mercury (S230)

Encodes BPHS chapters on graha phala (planetary results) based on rashi
placement. Mars and Mercury through all 12 signs.

Sources:
  BPHS Ch.19-20 — Kuja (Mars) and Budha (Mercury) in rashi phala
  Traditional commentary (PVRNR edition)

24 rules total: MAR001-MAR012 (Mars in rashis), BUR001-BUR012 (Mercury in rashis).
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_RASHIS_P2_REGISTRY = CorpusRegistry()

_MARS_IN_RASHIS = [
    RuleRecord(
        rule_id="MAR001",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Aries (own sign / sva-rashi, moolatrikona 0°-12°): "
            "maximum Martian energy — courageous, athletic, pioneering, "
            "competitive. Strong physical constitution. Leadership in action. "
            "Impulsive decisions; aggression if uncontrolled."
        ),
        confidence=0.93,
        verse="Ch.19 v.1-3",
        tags=["mars_in_rashi", "aries", "own_sign", "moolatrikona", "courage", "action"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR002",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Taurus: willful, stubborn persistence. Sensual desires "
            "can become possessive. Financial conflicts possible. Venus-ruled "
            "sign tempers Mars with aesthetic sensibility but may create "
            "over-indulgence in pleasures."
        ),
        confidence=0.84,
        verse="Ch.19 v.4-5",
        tags=["mars_in_rashi", "taurus", "venus_sign", "persistence", "possessive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR003",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Gemini: mentally combative, argumentative, quick-witted "
            "aggression. Debates and intellectual competition favored. "
            "Mercury-ruled sign channels Mars energy into words and ideas. "
            "Good for law, debate, writing."
        ),
        confidence=0.83,
        verse="Ch.19 v.6-7",
        tags=["mars_in_rashi", "gemini", "mercury_sign", "debate", "intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR004",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Cancer (debilitation rashi, neecha at 28° Cancer): "
            "Martian directness hampered by emotional reactivity. Defensive "
            "aggression, family conflicts. Moon-ruled sign makes Mars moody "
            "and indirect. Neecha bhanga by Moon strength helps."
        ),
        confidence=0.90,
        verse="Ch.19 v.8-10",
        tags=["mars_in_rashi", "cancer", "debilitation", "neecha", "moon_sign", "emotional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR005",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Leo: bold, dramatic, proud warrior energy. Sun-ruled "
            "sign amplifies Mars for authority and command. Natural military "
            "or political leader. Ego involvement in conflicts."
        ),
        confidence=0.86,
        verse="Ch.19 v.11-12",
        tags=["mars_in_rashi", "leo", "sun_sign", "authority", "leadership", "pride"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR006",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Virgo: precise, methodical, service-oriented energy. "
            "Mercury-ruled sign gives Mars analytical focus. Good for "
            "medicine, engineering, craftsmanship. Can be overly critical."
        ),
        confidence=0.83,
        verse="Ch.19 v.13-14",
        tags=["mars_in_rashi", "virgo", "mercury_sign", "precision", "service", "engineering"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR007",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Libra: conflict in partnerships, assertiveness in "
            "relationships. Venus-ruled sign creates tension between "
            "individual will and cooperation. Legal disputes possible. "
            "Balance between competition and harmony needed."
        ),
        confidence=0.84,
        verse="Ch.19 v.15-16",
        tags=["mars_in_rashi", "libra", "venus_sign", "partnership_conflict", "legal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR008",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Scorpio (own sign / sva-rashi): intense, penetrating, "
            "transformative energy. Investigation, occult, surgery, research. "
            "Powerful sexuality. Ability to confront death and darkness. "
            "Fixed water sign gives Mars depth and regenerative power."
        ),
        confidence=0.92,
        verse="Ch.19 v.17-19",
        tags=["mars_in_rashi", "scorpio", "own_sign", "intensity", "occult", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR009",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Sagittarius: righteous warrior, philosophical action. "
            "Jupiter-ruled sign elevates Mars toward dharma and higher causes. "
            "Good for law, military with ethics, sports, adventure."
        ),
        confidence=0.85,
        verse="Ch.19 v.20-21",
        tags=["mars_in_rashi", "sagittarius", "jupiter_sign", "dharma", "adventure"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR010",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Capricorn (exaltation rashi, peak at 28° Capricorn): "
            "disciplined, goal-oriented, powerful executive energy. "
            "Saturn-ruled sign gives Mars structured ambition. "
            "Best placement for career achievement and sustained effort."
        ),
        confidence=0.93,
        verse="Ch.19 v.22-24",
        tags=["mars_in_rashi", "capricorn", "exaltation", "saturn_sign", "ambition", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR011",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Aquarius: social justice warrior, group activism, "
            "unconventional assertiveness. Saturn-ruled sign gives Mars "
            "a detached, ideological quality. Reform movements, technology, "
            "humanitarian causes channeled through Martian drive."
        ),
        confidence=0.82,
        verse="Ch.19 v.25-26",
        tags=["mars_in_rashi", "aquarius", "saturn_sign", "reform", "social_justice"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="MAR012",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mars in Pisces: spiritual warrior, compassionate action, "
            "hidden aggression. Jupiter-ruled sign softens Mars into "
            "service and sacrifice. Healing professions, hidden conflicts, "
            "spiritual disciplines requiring effort."
        ),
        confidence=0.82,
        verse="Ch.19 v.27-28",
        tags=["mars_in_rashi", "pisces", "jupiter_sign", "spiritual", "service", "healing"],
        implemented=False,
    ),
]

_MERCURY_IN_RASHIS = [
    RuleRecord(
        rule_id="BUR001",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Aries: quick, impulsive thinking, decisive communication. "
            "Mars-ruled sign gives Mercury speed but reduces patience for detail. "
            "Good for sales, debate, starting ideas. May speak before thinking."
        ),
        confidence=0.83,
        verse="Ch.20 v.1-2",
        tags=["mercury_in_rashi", "aries", "mars_sign", "quick_mind", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR002",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Taurus: practical, methodical thinking, financial acumen. "
            "Venus-ruled sign gives Mercury an eye for beauty and value. "
            "Good for accounting, arts management, trade in luxury goods."
        ),
        confidence=0.84,
        verse="Ch.20 v.3-4",
        tags=["mercury_in_rashi", "taurus", "venus_sign", "practical", "finance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR003",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Gemini (own sign / sva-rashi, moolatrikona 0°-15°): "
            "peak intellectual agility, versatile communication, curiosity. "
            "Writing, languages, journalism, trade all strongly favored. "
            "Quick wit, multiple interests, social intelligence."
        ),
        confidence=0.94,
        verse="Ch.20 v.5-7",
        tags=["mercury_in_rashi", "gemini", "own_sign", "moolatrikona", "intellect", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR004",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Cancer: emotionally colored thinking, intuitive "
            "communication, good memory for personal experiences. Moon-ruled "
            "sign gives Mercury empathy but may cloud objectivity. "
            "Good for counseling, writing about personal/family matters."
        ),
        confidence=0.83,
        verse="Ch.20 v.8-9",
        tags=["mercury_in_rashi", "cancer", "moon_sign", "intuitive", "memory", "empathy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR005",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Leo: authoritative communication, dramatic expression, "
            "confident intellect. Sun-ruled sign amplifies Mercury for "
            "public speaking, teaching, performance. Ego in communication."
        ),
        confidence=0.84,
        verse="Ch.20 v.10-11",
        tags=["mercury_in_rashi", "leo", "sun_sign", "public_speaking", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR006",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Virgo (own sign and exaltation rashi, peak at 15° Virgo): "
            "maximum analytical precision, discernment, craft. Best placement "
            "for Mercury — meticulous thinking, editing, analysis, medicine, "
            "mathematics, accounting. Critical faculties at peak."
        ),
        confidence=0.96,
        verse="Ch.20 v.12-14",
        tags=["mercury_in_rashi", "virgo", "own_sign", "exaltation", "analysis", "precision", "medicine"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR007",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Libra: diplomatic, balanced thinking, talent for "
            "negotiation and law. Venus-ruled sign gives Mercury aesthetic "
            "judgment and social intelligence. Excellent for partnerships, "
            "contracts, mediation."
        ),
        confidence=0.85,
        verse="Ch.20 v.15-16",
        tags=["mercury_in_rashi", "libra", "venus_sign", "diplomacy", "law", "negotiation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR008",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Scorpio: investigative, secretive, penetrating intellect. "
            "Research, psychology, occult knowledge. Mars-ruled sign gives "
            "Mercury intensity and depth. May be sharp-tongued or sarcastic."
        ),
        confidence=0.84,
        verse="Ch.20 v.17-18",
        tags=["mercury_in_rashi", "scorpio", "mars_sign", "research", "psychology", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR009",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Sagittarius (debilitation rashi, neecha at 15° Sagittarius): "
            "big-picture thinking over detail, philosophical but imprecise. "
            "Jupiter-ruled sign pulls Mercury toward wisdom over analysis. "
            "Good for teaching philosophy; poor for accounting or fine detail."
        ),
        confidence=0.89,
        verse="Ch.20 v.19-21",
        tags=["mercury_in_rashi", "sagittarius", "debilitation", "neecha", "jupiter_sign", "philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR010",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Capricorn: structured, practical, business-oriented "
            "thinking. Saturn-ruled sign gives Mercury discipline and long-term "
            "planning ability. Good for business strategy, administration, "
            "engineering management."
        ),
        confidence=0.84,
        verse="Ch.20 v.22-23",
        tags=["mercury_in_rashi", "capricorn", "saturn_sign", "business", "strategy", "practical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR011",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Aquarius: innovative, humanitarian thinking, "
            "interest in science and technology. Saturn-ruled sign gives "
            "Mercury social awareness and originality. Good for research, "
            "invention, social reform communication."
        ),
        confidence=0.83,
        verse="Ch.20 v.24-25",
        tags=["mercury_in_rashi", "aquarius", "saturn_sign", "innovation", "science", "technology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BUR012",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="graha_in_rashi",
        description=(
            "Mercury in Pisces: intuitive, imaginative thinking, poetic "
            "communication. Jupiter-ruled sign gives Mercury mystical and "
            "creative qualities. Good for arts, spirituality, healing. "
            "May struggle with concrete analysis or boundaries."
        ),
        confidence=0.83,
        verse="Ch.20 v.26-27",
        tags=["mercury_in_rashi", "pisces", "jupiter_sign", "intuition", "poetry", "spiritual"],
        implemented=False,
    ),
]

for _r in _MARS_IN_RASHIS + _MERCURY_IN_RASHIS:
    BPHS_GRAHA_RASHIS_P2_REGISTRY.add(_r)
