"""
src/corpus/bphs_nakshatra_rules_p1.py — BPHS Nakshatra Rules Part 1 (S234)

Encodes classical nakshatra (lunar mansion) characteristics and significations
for nakshatras 1-14 (first half: Ashwini through Chitra).

Sources:
  BPHS Ch.3-4 — Nakshatra characteristics
  Brihat Samhita (Varahamihira) — Nakshatra natures
  Taittiriya Brahmana / Vedic nakshatra descriptions
  Phala Deepika — Nakshatra phala

28 rules total: NAK001-NAK028.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_NAKSHATRA_RULES_P1_REGISTRY = CorpusRegistry()

_NAKSHATRA_RULES = [
    RuleRecord(
        rule_id="NAK001",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Ashwini (1): Ketu-ruled, first nakshatra 0°-13°20' Aries. "
            "Nature: Deva, Vata, Kshatriya. Symbol: horse's head. "
            "Deity: Ashwini Kumaras (divine physicians). "
            "Keywords: swift healing, beginnings, travel, medicine, vitality."
        ),
        confidence=0.92,
        verse="Ch.3 v.1-5",
        tags=["nakshatra", "ashwini", "ketu", "aries", "healing", "swift_action"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK002",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Bharani (2): Venus-ruled, 13°20'-26°40' Aries. "
            "Nature: Manushya, Pitta, Mleccha. Symbol: yoni/womb. "
            "Deity: Yama (god of death/dharma). "
            "Keywords: transformation, death/rebirth, restraint, creativity, sex, discipline."
        ),
        confidence=0.90,
        verse="Ch.3 v.6-10",
        tags=["nakshatra", "bharani", "venus", "aries", "transformation", "death_rebirth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK003",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Krittika (3): Sun-ruled, 26°40' Aries-10° Taurus. Spans both signs. "
            "Nature: Rakshasa, Pitta. Symbol: razor/flame. "
            "Deity: Agni (fire god). "
            "Keywords: sharp intellect, purification, cutting, fame, nurturing by fire."
        ),
        confidence=0.91,
        verse="Ch.3 v.11-15",
        tags=["nakshatra", "krittika", "sun", "aries_taurus", "purification", "fire", "sharp"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK004",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Rohini (4): Moon-ruled (Moon's favorite nakshatra), 10°-23°20' Taurus. "
            "Moon is exalted here. Nature: Manushya, Kapha. Symbol: cart/chariot. "
            "Deity: Brahma (creator). "
            "Keywords: fertility, beauty, abundance, creativity, material prosperity, attraction."
        ),
        confidence=0.94,
        verse="Ch.3 v.16-20",
        tags=["nakshatra", "rohini", "moon", "taurus", "fertility", "abundance", "moon_favorite"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK005",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Mrigashira (5): Mars-ruled, 23°20' Taurus-6°40' Gemini. "
            "Nature: Deva, Vata/Pitta. Symbol: deer's head. "
            "Deity: Soma (Moon/nectar). "
            "Keywords: seeking, gentle, curious mind, wandering, searching for bliss."
        ),
        confidence=0.89,
        verse="Ch.3 v.21-25",
        tags=["nakshatra", "mrigashira", "mars", "taurus_gemini", "seeking", "gentle", "curious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK006",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Ardra (6): Rahu-ruled, 6°40'-20° Gemini. "
            "Nature: Manushya, Vata. Symbol: teardrop/diamond. "
            "Deity: Rudra (storm god). "
            "Keywords: intense transformation through destruction, grief then renewal, storms."
        ),
        confidence=0.89,
        verse="Ch.3 v.26-30",
        tags=["nakshatra", "ardra", "rahu", "gemini", "transformation", "storm", "grief"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK007",
        source="BPHS",
        chapter="Ch.3",
        school="parashari",
        category="nakshatra",
        description=(
            "Punarvasu (7): Jupiter-ruled, 20° Gemini-3°20' Cancer. "
            "Nature: Deva, Vata/Kapha. Symbol: bow and quiver. "
            "Deity: Aditi (mother of gods, infinity). "
            "Keywords: renewal, return, good fortune, philosophical, home-loving, benefic."
        ),
        confidence=0.91,
        verse="Ch.3 v.31-35",
        tags=["nakshatra", "punarvasu", "jupiter", "gemini_cancer", "renewal", "good_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK008",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Pushya (8): Saturn-ruled (most auspicious nakshatra), 3°20'-16°40' Cancer. "
            "Nature: Deva, Kapha. Symbol: flower/udder/circle. "
            "Deity: Brihaspati (Jupiter/guru). "
            "Keywords: nourishment, prosperity, spiritual wisdom, most benefic nakshatra."
        ),
        confidence=0.94,
        verse="Ch.4 v.1-5",
        tags=["nakshatra", "pushya", "saturn", "cancer", "nourishment", "most_auspicious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK009",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Ashlesha (9): Mercury-ruled, 16°40'-30° Cancer. "
            "Nature: Rakshasa, Kapha/Vata. Symbol: serpent coil. "
            "Deity: Nagas (serpent deities). "
            "Keywords: kundalini, hypnotic power, poison/healing, clinging, mystical wisdom."
        ),
        confidence=0.89,
        verse="Ch.4 v.6-10",
        tags=["nakshatra", "ashlesha", "mercury", "cancer", "serpent", "kundalini", "hypnotic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK010",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Magha (10): Ketu-ruled, 0°-13°20' Leo. Begins Leo. "
            "Nature: Rakshasa, Pitta. Symbol: throne/palanquin. "
            "Deity: Pitrs (ancestors). "
            "Keywords: ancestral connection, royal authority, pride, legacy, karma."
        ),
        confidence=0.91,
        verse="Ch.4 v.11-15",
        tags=["nakshatra", "magha", "ketu", "leo", "ancestors", "royal", "legacy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK011",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Purva Phalguni (11): Venus-ruled, 13°20'-26°40' Leo. "
            "Nature: Manushya, Pitta. Symbol: swinging hammock/fig tree. "
            "Deity: Bhaga (god of delight/inheritance). "
            "Keywords: pleasure, creativity, romance, luxury, rest, relaxation, arts."
        ),
        confidence=0.89,
        verse="Ch.4 v.16-20",
        tags=["nakshatra", "purva_phalguni", "venus", "leo", "pleasure", "romance", "arts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK012",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Uttara Phalguni (12): Sun-ruled, 26°40' Leo-10° Virgo. "
            "Nature: Manushya, Vata/Pitta. Symbol: bed/two front legs of cot. "
            "Deity: Aryaman (contracts, patronage). "
            "Keywords: contracts, service, patronage, social responsibility, stability."
        ),
        confidence=0.89,
        verse="Ch.4 v.21-25",
        tags=["nakshatra", "uttara_phalguni", "sun", "leo_virgo", "contracts", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK013",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Hasta (13): Moon-ruled, 10°-23°20' Virgo. "
            "Nature: Deva, Vata/Pitta. Symbol: hand/fist. "
            "Deity: Savitar (creative power of Sun). "
            "Keywords: skill with hands, craftsmanship, healing touch, cleverness, industry."
        ),
        confidence=0.90,
        verse="Ch.4 v.26-30",
        tags=["nakshatra", "hasta", "moon", "virgo", "craftsmanship", "healing_touch", "skill"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK014",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Chitra (14): Mars-ruled, 23°20' Virgo-6°40' Libra. "
            "Nature: Rakshasa, Pitta. Symbol: bright jewel/shining lamp. "
            "Deity: Vishwakarma (divine architect). "
            "Keywords: beauty, artistry, architecture, design, charisma, crafted perfection."
        ),
        confidence=0.91,
        verse="Ch.4 v.31-35",
        tags=["nakshatra", "chitra", "mars", "virgo_libra", "beauty", "art", "architecture"],
        implemented=False,
    ),
    # Nakshatra Moon sign interpretations (NAK015-028)
    RuleRecord(
        rule_id="NAK015",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Ashwini Nakshatra: energetic, impulsive, adventurous personality. "
            "Quick healing ability. Fond of travel and novelty. Independent spirit. "
            "Ketu-influenced Moon gives spiritual restlessness and psychic sensitivity."
        ),
        confidence=0.88,
        verse="Ch.4 v.36-38",
        tags=["nakshatra_moon", "ashwini", "ketu", "energetic", "impulsive", "healing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK016",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Bharani Nakshatra: strong creative force, intense desires. "
            "Disciplined when committed. Works well under authority of Yama "
            "(discipline/dharma). Venus-Moon gives aesthetic and sensual nature."
        ),
        confidence=0.86,
        verse="Ch.4 v.39-41",
        tags=["nakshatra_moon", "bharani", "venus", "creative_intensity", "discipline"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK017",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Krittika Nakshatra: sharp intellect, critical nature, "
            "leadership ability. Agni (fire) purifies emotional nature. "
            "Sun-Moon combination produces authoritative, dignified personality."
        ),
        confidence=0.87,
        verse="Ch.4 v.42-44",
        tags=["nakshatra_moon", "krittika", "sun", "sharp_intellect", "critical", "leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK018",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Rohini Nakshatra: most favored lunar placement by BPHS. "
            "Beautiful, magnetic, creative, artistic, materially blessed. "
            "Moon in its favorite nakshatra: stable emotions, popular, sensual joy."
        ),
        confidence=0.93,
        verse="Ch.4 v.45-47",
        tags=["nakshatra_moon", "rohini", "moon_favorite", "beautiful", "magnetic", "blessed"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK019",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Mrigashira Nakshatra: gentle, curious, seeking nature. "
            "Spiritual seeker, fond of literature and arts. "
            "Mars-Moon: active emotional life; may wander in search of fulfillment."
        ),
        confidence=0.86,
        verse="Ch.4 v.48-50",
        tags=["nakshatra_moon", "mrigashira", "mars", "gentle_seeker", "arts", "wandering"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK020",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Ardra Nakshatra: intense, transformative emotional life. "
            "Storms of grief that lead to renewal. Rahu-Moon: unusual experiences, "
            "foreign influences, powerful storms of transformation."
        ),
        confidence=0.85,
        verse="Ch.4 v.51-53",
        tags=["nakshatra_moon", "ardra", "rahu", "intense", "transformation", "storm"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK021",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Punarvasu Nakshatra: optimistic, philosophical, returning "
            "good fortune. Jupiter-Moon: benevolent, giving, spiritually inclined. "
            "Good communication skills; home-loving but adaptable."
        ),
        confidence=0.88,
        verse="Ch.4 v.54-56",
        tags=["nakshatra_moon", "punarvasu", "jupiter", "optimistic", "philosophical", "benevolent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK022",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Pushya Nakshatra (most auspicious Moon placement per BPHS): "
            "deeply nurturing, prosperous, spiritually wise. Saturn-Moon: "
            "disciplined emotions, responsible caretaking, excellent for teaching."
        ),
        confidence=0.93,
        verse="Ch.4 v.57-59",
        tags=["nakshatra_moon", "pushya", "saturn", "most_auspicious_moon", "nurturing", "prosperous"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK023",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Ashlesha Nakshatra: psychic, sensitive, potentially manipulative. "
            "Mercury-Moon: sharp perceptive intellect. Serpent energy — kundalini, "
            "healing, or venom. Deep attachment patterns; healing through awareness."
        ),
        confidence=0.85,
        verse="Ch.4 v.60-62",
        tags=["nakshatra_moon", "ashlesha", "mercury", "psychic", "serpent_energy", "perceptive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK024",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Magha Nakshatra: proud, ancestrally connected, commanding. "
            "Ketu-Moon: past-life memories strong; ancestral gifts and burdens. "
            "Natural aristocratic bearing; interest in heritage and tradition."
        ),
        confidence=0.87,
        verse="Ch.4 v.63-65",
        tags=["nakshatra_moon", "magha", "ketu", "proud", "ancestors", "tradition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK025",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Purva Phalguni Nakshatra: pleasure-loving, creative, romantic. "
            "Venus-Moon: artistic nature, love of luxury and beauty. "
            "Charismatic and sensually expressive; enjoyment of life's pleasures."
        ),
        confidence=0.87,
        verse="Ch.4 v.66-68",
        tags=["nakshatra_moon", "purva_phalguni", "venus", "pleasure_loving", "creative", "romantic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK026",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Uttara Phalguni Nakshatra: responsible, service-oriented, "
            "reliable. Sun-Moon: noble character; natural advisor and patron. "
            "Strong sense of duty; successful through consistent effort."
        ),
        confidence=0.87,
        verse="Ch.4 v.69-71",
        tags=["nakshatra_moon", "uttara_phalguni", "sun", "responsible", "service", "reliable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK027",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Hasta Nakshatra: skilled, industrious, healing hands. "
            "Moon in own nakshatra ruler's sign (Virgo/Moon-ruled Hasta): "
            "excellent memory, craftsmanship, practical wisdom, service."
        ),
        confidence=0.88,
        verse="Ch.4 v.72-74",
        tags=["nakshatra_moon", "hasta", "moon", "skilled", "healing_hands", "practical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK028",
        source="BPHS",
        chapter="Ch.4",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Chitra Nakshatra: beautiful, artistic, design-oriented. "
            "Mars-Moon: dynamic creative energy; attraction to beautiful objects. "
            "Charismatic; drawn to architecture, jewelry, fashion design."
        ),
        confidence=0.87,
        verse="Ch.4 v.75-77",
        tags=["nakshatra_moon", "chitra", "mars", "artistic", "design", "charismatic"],
        implemented=False,
    ),
]

for _r in _NAKSHATRA_RULES:
    BPHS_NAKSHATRA_RULES_P1_REGISTRY.add(_r)
