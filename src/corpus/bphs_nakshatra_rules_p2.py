"""
src/corpus/bphs_nakshatra_rules_p2.py — BPHS Nakshatra Rules Part 2 (S235)

Encodes classical nakshatra characteristics and significations for nakshatras
15-27 (Swati through Revati).

Sources:
  BPHS Ch.4-5 — Nakshatra characteristics (second half)
  Brihat Samhita / Phala Deepika / Taittiriya Brahmana

26 rules total: NAK029-NAK054.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_NAKSHATRA_RULES_P2_REGISTRY = CorpusRegistry()

_NAKSHATRA_RULES_P2 = [
    # --- Nakshatra Characteristics 15-27 (NAK029-041) ---
    RuleRecord(
        rule_id="NAK029",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Swati (15): Rahu-ruled, 6°40'-20° Libra. "
            "Nature: Deva, Vata. Symbol: young plant sprout/coral bead. "
            "Deity: Vayu (wind god). "
            "Keywords: independence, flexibility, self-movement, trade, business acumen."
        ),
        confidence=0.89,
        verse="Ch.5 v.1-4",
        tags=["nakshatra", "swati", "rahu", "libra", "independence", "trade", "flexible"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK030",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Vishakha (16): Jupiter-ruled, 20° Libra-3°20' Scorpio. "
            "Nature: Rakshasa, Pitta/Kapha. Symbol: triumphal arch/potter's wheel. "
            "Deity: Indra+Agni. "
            "Keywords: goal-oriented, ambitious, harvest after patience, power through perseverance."
        ),
        confidence=0.89,
        verse="Ch.5 v.5-8",
        tags=["nakshatra", "vishakha", "jupiter", "libra_scorpio", "ambition", "perseverance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK031",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Anuradha (17): Saturn-ruled, 3°20'-16°40' Scorpio. "
            "Nature: Deva, Pitta/Kapha. Symbol: lotus/staff. "
            "Deity: Mitra (god of friendship/contracts). "
            "Keywords: devotion, friendship, secret societies, organizational skill, loyalty."
        ),
        confidence=0.89,
        verse="Ch.5 v.9-12",
        tags=["nakshatra", "anuradha", "saturn", "scorpio", "devotion", "friendship", "loyalty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK032",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Jyeshtha (18): Mercury-ruled, 16°40'-30° Scorpio. "
            "Nature: Rakshasa, Vata/Kapha. Symbol: umbrella/talisman/earring. "
            "Deity: Indra (king of gods). "
            "Keywords: eldest/chief, authority, protective power, magical protection."
        ),
        confidence=0.89,
        verse="Ch.5 v.13-16",
        tags=["nakshatra", "jyeshtha", "mercury", "scorpio", "authority", "chief", "protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK033",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Mula (19): Ketu-ruled, 0°-13°20' Sagittarius. "
            "Nature: Rakshasa, Vata. Symbol: bunch of roots/tail of lion. "
            "Deity: Nirriti (goddess of dissolution/calamity). "
            "Keywords: deep investigation, going to roots, destruction of illusion, liberation."
        ),
        confidence=0.88,
        verse="Ch.5 v.17-20",
        tags=["nakshatra", "mula", "ketu", "sagittarius", "roots", "liberation", "dissolution"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK034",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Purva Ashadha (20): Venus-ruled, 13°20'-26°40' Sagittarius. "
            "Nature: Manushya, Pitta/Vata. Symbol: elephant tusk/fan/winnowing basket. "
            "Deity: Apas (water goddess). "
            "Keywords: invincible victory, purification through water, determination."
        ),
        confidence=0.88,
        verse="Ch.5 v.21-24",
        tags=["nakshatra", "purva_ashadha", "venus", "sagittarius", "victory", "determination"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK035",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Uttara Ashadha (21): Sun-ruled, 26°40' Sagittarius-10° Capricorn. "
            "Nature: Manushya, Pitta. Symbol: elephant tusk/small bed. "
            "Deity: Vishwadevas (universal gods). "
            "Keywords: universal victory, unchallengeable honor, lasting achievement."
        ),
        confidence=0.89,
        verse="Ch.5 v.25-28",
        tags=["nakshatra", "uttara_ashadha", "sun", "sagittarius_capricorn", "victory", "honor"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK036",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Shravana (22): Moon-ruled, 10°-23°20' Capricorn. "
            "Nature: Deva, Kapha/Vata. Symbol: three footprints/ear. "
            "Deity: Vishnu (preserver). "
            "Keywords: listening, learning, connecting, pilgrimage, Vishnu's preservation."
        ),
        confidence=0.91,
        verse="Ch.5 v.29-32",
        tags=["nakshatra", "shravana", "moon", "capricorn", "listening", "learning", "vishnu"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK037",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Dhanishtha (23): Mars-ruled, 23°20' Capricorn-6°40' Aquarius. "
            "Nature: Rakshasa, Pitta/Vata. Symbol: drum/flute. "
            "Deity: Eight Vasus (elemental beings). "
            "Keywords: wealth, music, rhythm, ambition, charitable nature, opulence."
        ),
        confidence=0.89,
        verse="Ch.5 v.33-36",
        tags=["nakshatra", "dhanishtha", "mars", "capricorn_aquarius", "wealth", "music", "rhythm"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK038",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Shatabhisha (24): Rahu-ruled, 6°40'-20° Aquarius. "
            "Nature: Rakshasa, Vata. Symbol: empty circle/100 healers. "
            "Deity: Varuna (god of cosmic law/water). "
            "Keywords: healing, mysticism, secret knowledge, scientific research, isolation."
        ),
        confidence=0.88,
        verse="Ch.5 v.37-40",
        tags=["nakshatra", "shatabhisha", "rahu", "aquarius", "healing", "mysticism", "research"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK039",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Purva Bhadrapada (25): Jupiter-ruled, 20° Aquarius-3°20' Pisces. "
            "Nature: Manushya, Vata/Pitta. Symbol: sword/two front legs of funeral cot. "
            "Deity: Aja Ekapad (one-footed goat/fire dragon). "
            "Keywords: burning intensity, purification, eccentricity, spiritual fire."
        ),
        confidence=0.87,
        verse="Ch.5 v.41-44",
        tags=["nakshatra", "purva_bhadrapada", "jupiter", "aquarius_pisces", "intensity", "purification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK040",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Uttara Bhadrapada (26): Saturn-ruled, 3°20'-16°40' Pisces. "
            "Nature: Manushya, Kapha/Pitta. Symbol: back legs of funeral cot/twins. "
            "Deity: Ahir Budhnya (serpent of the deep/Shiva's serpent). "
            "Keywords: wisdom from depth, compassion, patience, depth of feeling, cosmic truth."
        ),
        confidence=0.88,
        verse="Ch.5 v.45-48",
        tags=["nakshatra", "uttara_bhadrapada", "saturn", "pisces", "wisdom", "compassion", "depth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK041",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Revati (27): Mercury-ruled, 16°40'-30° Pisces. Last nakshatra. "
            "Nature: Deva, Kapha. Symbol: fish/drum. "
            "Deity: Pushan (nourisher, guardian of travelers). "
            "Keywords: completion, nourishment, cosmic journey's end, transition, compassion."
        ),
        confidence=0.90,
        verse="Ch.5 v.49-52",
        tags=["nakshatra", "revati", "mercury", "pisces", "completion", "nourishment", "last_nakshatra"],
        implemented=False,
    ),
    # --- Moon in nakshatras 15-27 (NAK042-054) ---
    RuleRecord(
        rule_id="NAK042",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Swati: independent, flexible, business-minded. "
            "Rahu-Moon: unconventional emotional expression, adaptability, "
            "trading instinct. May be emotionally scattered; thrives in freedom."
        ),
        confidence=0.85,
        verse="Ch.5 v.53-55",
        tags=["nakshatra_moon", "swati", "rahu", "independent", "flexible", "business"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK043",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Vishakha: determined, ambitious, goal-oriented. "
            "Jupiter-Moon: patient pursuit of harvest. Strong religious or "
            "ideological commitment; may be fanatical about beliefs."
        ),
        confidence=0.85,
        verse="Ch.5 v.56-58",
        tags=["nakshatra_moon", "vishakha", "jupiter", "determined", "ambitious", "goal_oriented"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK044",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Anuradha: devoted, loyal, secretive. Saturn-Moon: "
            "disciplined emotions, strong friendships, spiritual devotion. "
            "Organizational talent; protective of loved ones."
        ),
        confidence=0.86,
        verse="Ch.5 v.59-61",
        tags=["nakshatra_moon", "anuradha", "saturn", "devoted", "loyal", "disciplined"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK045",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Jyeshtha: authoritative, protective, eldest energy. "
            "Mercury-Moon: sharp perceptive mind, leadership capacity. "
            "Protective of family; can be controlling or arrogant."
        ),
        confidence=0.84,
        verse="Ch.5 v.62-64",
        tags=["nakshatra_moon", "jyeshtha", "mercury", "authoritative", "protective"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK046",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Mula: investigative, root-seeking, transformative. "
            "Ketu-Moon: past-life awareness, deep emotional release. "
            "May uproot established patterns to find truth. Liberation-oriented."
        ),
        confidence=0.84,
        verse="Ch.5 v.65-67",
        tags=["nakshatra_moon", "mula", "ketu", "investigative", "transformative", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK047",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Purva Ashadha: victorious, purifying emotional nature. "
            "Venus-Moon: aesthetically refined, determined, water connection. "
            "Strong will and enthusiasm; unafraid of challenges."
        ),
        confidence=0.85,
        verse="Ch.5 v.68-70",
        tags=["nakshatra_moon", "purva_ashadha", "venus", "victorious", "purifying"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK048",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Uttara Ashadha: honorable, lasting achievements, universal "
            "recognition. Sun-Moon: dignified, responsible, morally upright. "
            "Victorious through perseverance and ethical conduct."
        ),
        confidence=0.86,
        verse="Ch.5 v.71-73",
        tags=["nakshatra_moon", "uttara_ashadha", "sun", "honorable", "victorious", "ethical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK049",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Shravana: excellent listener, learner, connected to Vishnu. "
            "Moon-Moon: deeply empathic, sensitive, learning-oriented. "
            "Pilgrimage and travel for spiritual growth. Musical ability."
        ),
        confidence=0.87,
        verse="Ch.5 v.74-76",
        tags=["nakshatra_moon", "shravana", "moon", "listening", "learning", "music", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK050",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Dhanishtha: musically talented, wealthy aspirations, rhythmic. "
            "Mars-Moon: dynamic emotions, charitable, ambitious for material success. "
            "Skilled in music, rhythm, and achieving material goals."
        ),
        confidence=0.85,
        verse="Ch.5 v.77-79",
        tags=["nakshatra_moon", "dhanishtha", "mars", "musical", "wealthy", "rhythmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK051",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Shatabhisha: healing-oriented, mystical, secretive. "
            "Rahu-Moon: unconventional wisdom, scientific mind, isolation tendency. "
            "Natural healer; research into hidden or alternative knowledge."
        ),
        confidence=0.84,
        verse="Ch.5 v.80-82",
        tags=["nakshatra_moon", "shatabhisha", "rahu", "healing", "mystical", "scientific"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK052",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Purva Bhadrapada: intensely spiritual, eccentrically wise. "
            "Jupiter-Moon: burning idealism, purification through fire of truth. "
            "Powerful transformation; unconventional spiritual path."
        ),
        confidence=0.84,
        verse="Ch.5 v.83-85",
        tags=["nakshatra_moon", "purva_bhadrapada", "jupiter", "spiritual", "intense", "eccentric"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK053",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Uttara Bhadrapada: deeply compassionate, patient, cosmic wisdom. "
            "Saturn-Moon: emotional depth, connection to cosmic truth. "
            "Service to the suffering; wise elder energy."
        ),
        confidence=0.86,
        verse="Ch.5 v.86-88",
        tags=["nakshatra_moon", "uttara_bhadrapada", "saturn", "compassionate", "cosmic_wisdom"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="NAK054",
        source="BPHS",
        chapter="Ch.5",
        school="parashari",
        category="nakshatra",
        description=(
            "Moon in Revati: nurturing, gentle, completion-oriented. "
            "Mercury-Moon: compassionate intelligence, traveler's wisdom. "
            "Last nakshatra — karmic completion; deeply empathic nature."
        ),
        confidence=0.86,
        verse="Ch.5 v.89-91",
        tags=["nakshatra_moon", "revati", "mercury", "nurturing", "completion", "compassionate"],
        implemented=False,
    ),
]

for _r in _NAKSHATRA_RULES_P2:
    BPHS_NAKSHATRA_RULES_P2_REGISTRY.add(_r)
