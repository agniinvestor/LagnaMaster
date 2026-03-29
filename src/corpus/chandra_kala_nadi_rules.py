"""
src/corpus/chandra_kala_nadi_rules.py — Chandra Kala Nadi Exhaustive (S261)

Exhaustive encoding of Chandra Kala Nadi (also known as Deva Keralam),
a Tamil Nadi text attributed to Sage Chandra Kala. This is one of the
most detailed Nadi texts, providing specific results for Moon in each
nakshatra in each house, planetary combinations, and transit effects.

Key features of CKN:
- Moon-centric analysis (each nakshatra-house combination)
- Detailed dasha-antardasha results
- Transit (Gochara) effects of all planets
- Yoga results specific to nakshatra positions
- Unique "Bhava Parivartan" (house exchange) analysis
- Planet-in-nakshatra specific results (27 nakshatras × 9 planets)

120 rules: CKN001-CKN120.
All: school="nadi", source="ChandraKalaNadi", implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

CHANDRA_KALA_NADI_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Moon in Nakshatras — Houses (CKN001-027) ─────────────────────────────
    RuleRecord(
        rule_id="CKN001",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Ashwini (Ketu-ruled nakshatra): in 1st house → athletic build, "
            "quick mind, healing instincts. Leadership in emergency situations. "
            "CKN unique: Ashwini Moon in 1st gives 'Turaga Lagna' (horse-vehicle destiny)."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Ashwini Chapter",
        tags=["ckn", "moon", "ashwini", "nakshatra", "1st_house", "ketu", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN002",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Bharani (Venus-ruled): in 1st house → sensual, artistic, obstinate. "
            "Connected to Yama (death deity) energy → potential interest in transformation. "
            "CKN: Bharani Moon 1st → involvement with medicine, death/rebirth themes."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Bharani Chapter",
        tags=["ckn", "moon", "bharani", "nakshatra", "1st_house", "venus", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN003",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Krittika (Sun-ruled): in 1st house → sharp, cutting intellect. "
            "Fire energy; excellent for cooking, metallurgy, or surgery. "
            "CKN: Krittika Moon 1st → 'Agni Priya' (fire-beloved) — respected authority."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Krittika Chapter",
        tags=["ckn", "moon", "krittika", "nakshatra", "1st_house", "sun", "fire", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN004",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Rohini (Moon-ruled, own nakshatra): in 1st house → beautiful, "
            "highly creative, sensual, beloved. "
            "CKN: Rohini Moon 1st = 'Chandra Pushti' — Moon's strength fully expressed; "
            "exceptional material prosperity and artistic talent."
        ),
        confidence=0.91,
        verse="Chandra Kala Nadi, Rohini Chapter",
        tags=["ckn", "moon", "rohini", "nakshatra", "1st_house", "beauty", "prosperity", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN005",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Mrigashira (Mars-ruled): in 1st house → restless, searching nature. "
            "Excellent researcher, traveller, curious mind. "
            "CKN: Mrigashira Moon 1st → 'Mriga Lagna' (deer-destiny) — fleet-footed, elusive success."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Mrigashira Chapter",
        tags=["ckn", "moon", "mrigashira", "nakshatra", "1st_house", "mars", "travel", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN006",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Ardra (Rahu-ruled): in 1st house → intense, stormy nature; "
            "genius or destruction. Brilliant but turbulent. "
            "CKN: Ardra Moon 1st → 'Rudra Lagna' — Shiva's energy; great transformation possible."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Ardra Chapter",
        tags=["ckn", "moon", "ardra", "nakshatra", "1st_house", "rahu", "transformation", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN007",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Punarvasu (Jupiter-ruled): in 1st house → philosophical, forgiving, "
            "returns from setbacks repeatedly (Punarvasu = return of light). "
            "CKN: Punarvasu Moon 1st → 'Aditi Putra' (Aditi's son) — protected by divine mother."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Punarvasu Chapter",
        tags=["ckn", "moon", "punarvasu", "nakshatra", "1st_house", "jupiter", "philosophy", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN008",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Pushya (Saturn-ruled): in 1st house → nurturing, disciplined, "
            "motherly, great provider. Pushya is the most auspicious nakshatra. "
            "CKN: Pushya Moon 1st → 'Guru Priya' — blessed by teachers and Jupiter energy."
        ),
        confidence=0.90,
        verse="Chandra Kala Nadi, Pushya Chapter",
        tags=["ckn", "moon", "pushya", "nakshatra", "1st_house", "saturn", "auspicious", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN009",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Ashlesha (Mercury-ruled): in 1st house → sharp, subtle, "
            "serpentine intelligence. Excellent at investigation and healing. "
            "CKN: Ashlesha Moon 1st → 'Sarpa Lagna' — serpent wisdom; kundalini potential."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Ashlesha Chapter",
        tags=["ckn", "moon", "ashlesha", "nakshatra", "1st_house", "mercury", "serpent", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN010",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Magha (Ketu-ruled): in 1st house → royal bearing, ancestral pride, "
            "connected to Pitru (ancestors). Leadership through lineage. "
            "CKN: Magha Moon 1st → 'Raja Simha Lagna' — lion throne, ancestral authority."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Magha Chapter",
        tags=["ckn", "moon", "magha", "nakshatra", "1st_house", "ketu", "ancestors", "royalty", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN011",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Purva Phalguni (Venus-ruled): in 1st house → creative, pleasure-seeking, "
            "artistic, romantic. Career in entertainment or luxury. "
            "CKN: Purva Phalguni Moon 1st → 'Bhaga Lagna' — blessed by prosperity deity."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Purva Phalguni Chapter",
        tags=["ckn", "moon", "purva_phalguni", "nakshatra", "1st_house", "venus", "arts", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN012",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Uttara Phalguni (Sun-ruled): in 1st house → dignified, helpful, "
            "leader in service. Contractual relationships tend to be honoured. "
            "CKN: Uttara Phalguni Moon 1st → 'Aryaman Lagna' — noble friendship and contracts."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Uttara Phalguni Chapter",
        tags=["ckn", "moon", "uttara_phalguni", "nakshatra", "1st_house", "sun", "service", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN013",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Hasta (Moon-ruled): in 1st house → skilled with hands, "
            "dexterous, crafty, and clever. Excellent for crafts, surgery, writing. "
            "CKN: Hasta Moon 1st → 'Savitar Lagna' — Sun's creative hand; manifest destiny."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Hasta Chapter",
        tags=["ckn", "moon", "hasta", "nakshatra", "1st_house", "moon", "crafts", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN014",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Chitra (Mars-ruled): in 1st house → beautiful, architectural, "
            "artistic vision. Excellent designer or artist. "
            "CKN: Chitra Moon 1st → 'Vishwakarma Lagna' — divine architect energy."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Chitra Chapter",
        tags=["ckn", "moon", "chitra", "nakshatra", "1st_house", "mars", "design", "arts", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN015",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Swati (Rahu-ruled): in 1st house → independent, flexible, "
            "diplomatic, business-oriented. Foreign trade. "
            "CKN: Swati Moon 1st → 'Vayu Lagna' — wind-like adaptability, "
            "moves with circumstances."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Swati Chapter",
        tags=["ckn", "moon", "swati", "nakshatra", "1st_house", "rahu", "business", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN016",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Vishakha (Jupiter-ruled): in 1st house → goal-oriented, "
            "ambitious, competitive. Two-natured (this nakshatra spans two signs). "
            "CKN: Vishakha Moon 1st → 'Indra-Agni Lagna' — power and fire combined."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Vishakha Chapter",
        tags=["ckn", "moon", "vishakha", "nakshatra", "1st_house", "jupiter", "ambition", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN017",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Anuradha (Saturn-ruled): in 1st house → devoted, disciplined, "
            "loyal friend. Struggles early but prospers later. "
            "CKN: Anuradha Moon 1st → 'Mitra Lagna' — friendship deity; "
            "success through alliances."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Anuradha Chapter",
        tags=["ckn", "moon", "anuradha", "nakshatra", "1st_house", "saturn", "friendship", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN018",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Jyeshtha (Mercury-ruled): in 1st house → eldest child energy, "
            "responsible, authoritative, protective. "
            "CKN: Jyeshtha Moon 1st → 'Indra Lagna' — king of the gods energy; "
            "natural authority."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Jyeshtha Chapter",
        tags=["ckn", "moon", "jyeshtha", "nakshatra", "1st_house", "mercury", "authority", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN019",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Mula (Ketu-ruled): in 1st house → investigative, goes to root causes. "
            "Destructive and constructive simultaneously. "
            "CKN: Mula Moon 1st → 'Niritti Lagna' — death-and-rebirth energy; "
            "deep transformation capacity."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Mula Chapter",
        tags=["ckn", "moon", "mula", "nakshatra", "1st_house", "ketu", "transformation", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN020",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Purva Ashadha (Venus-ruled): in 1st house → invincible spirit, "
            "never gives up, natural winner. "
            "CKN: Purva Ashadha Moon 1st → 'Apas Lagna' — water deity; "
            "ability to purify and overcome."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Purva Ashadha Chapter",
        tags=["ckn", "moon", "purva_ashadha", "nakshatra", "1st_house", "venus", "victory", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN021",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Uttara Ashadha (Sun-ruled): in 1st house → righteous, "
            "universally victorious, excellent leadership. "
            "CKN: Uttara Ashadha Moon 1st → 'Vishwadeva Lagna' — universal deity energy; "
            "works for collective good."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Uttara Ashadha Chapter",
        tags=["ckn", "moon", "uttara_ashadha", "nakshatra", "1st_house", "sun", "righteousness", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN022",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Shravana (Moon-ruled, own element): in 1st house → excellent listener, "
            "learner, teacher. Connected to Vishnu-Saraswati energy. "
            "CKN: Shravana Moon 1st → 'Vishnu Pada' — Vishnu's footstep; "
            "steady progress and preservation."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Shravana Chapter",
        tags=["ckn", "moon", "shravana", "nakshatra", "1st_house", "moon", "learning", "vishnu", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN023",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Dhanishtha (Mars-ruled): in 1st house → musical talent, wealthy, "
            "gregarious. Houses wealth through effort. "
            "CKN: Dhanishtha Moon 1st → 'Ashta Vasu Lagna' — eight wealth deities; "
            "prosperity through discipline."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Dhanishtha Chapter",
        tags=["ckn", "moon", "dhanishtha", "nakshatra", "1st_house", "mars", "music", "wealth", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN024",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Shatabhisha (Rahu-ruled): in 1st house → scientific mind, "
            "healer of many, secretive. '100 healers' energy. "
            "CKN: Shatabhisha Moon 1st → 'Varuna Lagna' — cosmic law deity; "
            "connection to hidden mysteries."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Shatabhisha Chapter",
        tags=["ckn", "moon", "shatabhisha", "nakshatra", "1st_house", "rahu", "healing", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN025",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Purva Bhadrapada (Jupiter-ruled): in 1st house → intense devotion, "
            "fire-like purification, spiritual warrior. "
            "CKN: Purva Bhadrapada Moon 1st → 'Aja Ekapada Lagna' — one-footed goat deity; "
            "stands firm in spiritual purpose."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Purva Bhadrapada Chapter",
        tags=["ckn", "moon", "purva_bhadrapada", "nakshatra", "1st_house", "jupiter", "spiritual", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN026",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Uttara Bhadrapada (Saturn-ruled): in 1st house → deeply wise, "
            "connected to ocean depths, patient. "
            "CKN: Uttara Bhadrapada Moon 1st → 'Ahir Budhnya Lagna' — serpent of the deep; "
            "wisdom from the unconscious."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Uttara Bhadrapada Chapter",
        tags=["ckn", "moon", "uttara_bhadrapada", "nakshatra", "1st_house", "saturn", "wisdom", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN027",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "Moon in Revati (Mercury-ruled): in 1st house → compassionate, protective "
            "of the weak, watery nature, spiritually inclined. "
            "CKN: Revati Moon 1st → 'Pushan Lagna' — nourisher deity; "
            "guides souls on their journey."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Revati Chapter",
        tags=["ckn", "moon", "revati", "nakshatra", "1st_house", "mercury", "compassion", "nadi"],
        implemented=False,
    ),

    # ── Nadi Specific Planet Combinations (CKN028-060) ───────────────────────
    RuleRecord(
        rule_id="CKN028",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Jupiter-Moon conjunction in any house → 'Gaja Kesari Yoga' (confirmed). "
            "CKN adds: the nakshatra of this conjunction determines the specific career direction. "
            "Jupiter-Moon in Pushya → highest Gaja Kesari: teacher of teachers."
        ),
        confidence=0.90,
        verse="Chandra Kala Nadi, Gaja Kesari",
        tags=["ckn", "jupiter", "moon", "gaja_kesari_yoga", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN029",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Sun-Moon conjunction (Amavasya birth) in any nakshatra → "
            "highly creative but internally conflicted. The nakshatra determines "
            "whether the Sun or Moon energy dominates. Rohini Amavasya → most creative."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Sun-Moon Conjunction",
        tags=["ckn", "sun", "moon", "amavasya", "conjunction", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN030",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Saturn-Moon conjunction → 'Vish Yoga' results amplified by nakshatra. "
            "In Pushya (Saturn's nakshatra) → most intense. "
            "CKN remedy: recite Chandra Stotra at moonrise on Mondays."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Saturn-Moon",
        tags=["ckn", "saturn", "moon", "vish_yoga", "pushya", "depression", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN031",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Mars-Saturn conjunction → fierce determination and potential violence. "
            "In Krittika (fire) → most dangerous; in Pushya → disciplined power. "
            "CKN: this combination in 10th → steel/engineering industry success."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Mars-Saturn",
        tags=["ckn", "mars", "saturn", "conjunction", "industry", "career", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN032",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Venus-Mercury conjunction → exceptional communication about beauty/arts. "
            "In Revati → spiritual art. In Swati → business in aesthetics. "
            "CKN: this combo in 7th → spouse is an artist or in media/communication."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Venus-Mercury",
        tags=["ckn", "venus", "mercury", "conjunction", "arts", "communication", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN033",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Rahu-Jupiter conjunction → 'Guru Chandal Yoga' with nakshatra modification. "
            "In Punarvasu (Jupiter's nakshatra) → Rahu corrupts Jupiter's teachings. "
            "In Ardra (Rahu's nakshatra) → Jupiter struggles but ultimately reforms Rahu's energy."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Rahu-Jupiter",
        tags=["ckn", "rahu", "jupiter", "guru_chandal", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN034",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Ketu-Mercury conjunction → past-life intelligence surfacing. "
            "In Ashlesha → exceptional medical/healing intelligence from past lives. "
            "In Revati → spiritual writing ability. CKN unique interpretation of this combo."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Ketu-Mercury",
        tags=["ckn", "ketu", "mercury", "conjunction", "past_life", "intelligence", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN035",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Sun-Jupiter conjunction → 'Budha-Aditya' variant. "
            "Leadership through wisdom. In Uttara Ashadha → most powerful; "
            "in Krittika → authority figure in spiritual or governmental matters."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Sun-Jupiter",
        tags=["ckn", "sun", "jupiter", "conjunction", "leadership", "wisdom", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN036",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Mars-Venus conjunction → passionate creativity; acting, dance, sports. "
            "In Bharani → extreme passion; in Chitra → great artistic-athletic combination. "
            "Marriage to someone of different cultural background when this is in 7th."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Mars-Venus",
        tags=["ckn", "mars", "venus", "conjunction", "passion", "arts", "sports", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN037",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: all planets in trines (1/5/9) → 'Pushkala Yoga'. "
            "Person is filled with divine grace. "
            "The nakshatra of the Lagna in this case determines which deity's grace is expressed."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Pushkala Yoga",
        tags=["ckn", "pushkala_yoga", "trikona", "divine_grace", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN038",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Moon in 7th from Sun (Poornima/Full Moon birth) → emotionally fulfilled, "
            "excellent relationship with public. "
            "Nakshatra of Moon determines which aspect of public life dominates (e.g., Rohini → food/beauty)."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Full Moon Birth",
        tags=["ckn", "moon", "sun", "poornima", "full_moon", "public", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN039",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: Atmakaraka nakshatra analysis — the soul's deepest wound and gift. "
            "AK in Ardra → soul wound around loss; gift: resilience. "
            "AK in Rohini → soul wound around attachment; gift: creation. "
            "CKN uses this for spiritual counseling."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Atmakaraka Nakshatra",
        tags=["ckn", "atmakaraka", "nakshatra", "soul_wound", "spiritual", "nadi"],
        implemented=False,
    ),

    # ── Transit (Gochara) Rules — CKN Unique (CKN040-060) ────────────────────
    RuleRecord(
        rule_id="CKN040",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN Jupiter transit through the natal Moon nakshatra → 'Guru Transit Yoga'. "
            "Events of Jupiter's karakatva (children, wisdom, marriage, wealth) ripen. "
            "CKN: the specific nakshatra of Moon determines which Jupiter blessing manifests first."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Gochara Chapter",
        tags=["ckn", "transit", "jupiter", "moon", "nakshatra", "gochara", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN041",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN Saturn transit (Sade Sati): the 7.5-year Saturn transit through "
            "Moon's sign and adjacent signs. CKN adds nakshatra-level analysis: "
            "when Saturn transits the exact natal Moon nakshatra → peak karma."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Sade Sati",
        tags=["ckn", "transit", "saturn", "sade_sati", "moon", "karma", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN042",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: when transiting Saturn conjuncts natal Rahu or Ketu → "
            "sudden karmic shifts. If this coincides with natal Moon nakshatra → "
            "major life transformation. CKN calls this 'Karma Kshaya' (karma exhaustion)."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Saturn-Rahu Transit",
        tags=["ckn", "transit", "saturn", "rahu", "ketu", "karma", "transformation", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN043",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: Jupiter transit through the 5th from natal Moon nakshatra group → "
            "marriage and children timing. If natal Jupiter also aspects 7th → "
            "double confirmation of marriage in this transit period."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Jupiter Marriage Transit",
        tags=["ckn", "transit", "jupiter", "marriage", "children", "timing", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN044",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: Mars transit through natal Ascendant nakshatra → health challenges, "
            "accidents, or conflicts. Duration: approximately 7 days in each nakshatra. "
            "CKN specifies avoiding travel or starting ventures during this Mars transit."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Mars Gochara",
        tags=["ckn", "transit", "mars", "lagna", "nakshatra", "health", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN045",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN Ashtama Shani (Saturn 8th from Moon): most difficult of the three "
            "Sade Sati phases. CKN adds: the nakshatra of Moon at birth determines "
            "the specific type of 8th-house challenge (Rohini → financial; Ardra → sudden crisis)."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Ashtama Shani",
        tags=["ckn", "transit", "saturn", "ashtama_shani", "moon", "8th_house", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN046",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: Venus transit through the 7th from natal Moon → romantic opportunities. "
            "Duration: ~23 days per nakshatra. If Venus is the Darakaraka, "
            "this transit activates marriage possibilities."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Venus Gochara",
        tags=["ckn", "transit", "venus", "moon", "7th_house", "marriage", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN047",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN Rahu-Ketu transit through natal Moon nakshatra: 18-month period. "
            "Rahu transiting natal Moon nakshatra → obsessions and confusion intensify. "
            "Ketu transiting natal Moon nakshatra → detachment and spiritual turning point."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Rahu-Ketu Gochara",
        tags=["ckn", "transit", "rahu", "ketu", "moon", "nakshatra", "spiritual", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN048",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN Janma Nakshatra transit rule: any planet transiting the natal Moon nakshatra "
            "activates that planet's full results. "
            "Sun in Janma nakshatra → health/government issues for 1 day. "
            "Mars → energy/accidents for ~7 days."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Janma Nakshatra Transit",
        tags=["ckn", "transit", "janma_nakshatra", "timing", "nadi"],
        implemented=False,
    ),

    # ── Dasha-Antardasha Specific Results (CKN049-075) ───────────────────────
    RuleRecord(
        rule_id="CKN049",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Sun Mahadasha results depend on natal Moon nakshatra. "
            "Sun MD with Moon in Pushya → government honors, father-figure success. "
            "Sun MD with Moon in Ardra → intense career challenges and sudden changes."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Sun Dasha",
        tags=["ckn", "dasha", "sun", "moon", "nakshatra", "career", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN050",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Moon Mahadasha gives results based on Moon's nakshatra. "
            "Moon MD in Rohini → peak emotional fulfillment, prosperity, creativity. "
            "Moon MD in Jyeshtha → authority and protection of others."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Moon Dasha",
        tags=["ckn", "dasha", "moon", "nakshatra", "prosperity", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN051",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Mars Mahadasha results by Moon's nakshatra. "
            "Mars MD with Moon in Ashwini → athletic peak, healing work, entrepreneurship. "
            "Mars MD with Moon in Mrigashira → travel and conquest of new territories."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Mars Dasha",
        tags=["ckn", "dasha", "mars", "moon", "nakshatra", "entrepreneurship", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN052",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Rahu Mahadasha (18 years) with specific nakshatra modifications. "
            "Rahu MD with Moon in Swati → exceptional business and foreign connections. "
            "Rahu MD with Moon in Ardra → brilliant unconventional career, upheavals."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Rahu Dasha",
        tags=["ckn", "dasha", "rahu", "moon", "nakshatra", "business", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN053",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Jupiter Mahadasha (16 years) nakshatra-based results. "
            "Jupiter MD with Moon in Punarvasu → spiritual teacher, prosperity. "
            "Jupiter MD with Moon in Vishakha → goal achievement, recognition."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Jupiter Dasha",
        tags=["ckn", "dasha", "jupiter", "moon", "nakshatra", "spiritual", "prosperity", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN054",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Saturn Mahadasha (19 years) nakshatra-based results. "
            "Saturn MD with Moon in Pushya → peak career achievement through discipline. "
            "Saturn MD with Moon in Anuradha → devoted service and long-term success."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Saturn Dasha",
        tags=["ckn", "dasha", "saturn", "moon", "nakshatra", "career", "service", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN055",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Mercury Mahadasha (17 years) nakshatra modifications. "
            "Mercury MD with Moon in Ashlesha → exceptional business and medical intelligence. "
            "Mercury MD with Moon in Revati → spiritual communication and publishing."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Mercury Dasha",
        tags=["ckn", "dasha", "mercury", "moon", "nakshatra", "business", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN056",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Ketu Mahadasha (7 years) nakshatra modifications. "
            "Ketu MD with Moon in Magha → ancestral wisdom surfaces; royalty karma activates. "
            "Ketu MD with Moon in Mula → deep transformation, kundalini awakening possible."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Ketu Dasha",
        tags=["ckn", "dasha", "ketu", "moon", "nakshatra", "transformation", "spiritual", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN057",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Venus Mahadasha (20 years) nakshatra modifications. "
            "Venus MD with Moon in Bharani → intense creativity, romantic life peaks. "
            "Venus MD with Moon in Purva Phalguni → arts, luxury, entertainment career."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Venus Dasha",
        tags=["ckn", "dasha", "venus", "moon", "nakshatra", "arts", "marriage", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN058",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN antardasha (sub-period) principle: the sub-lord's nakshatra modifies "
            "the main dasha's results. Jupiter main dasha, Saturn sub → structured wisdom; "
            "Jupiter main, Rahu sub → expansion through unconventional means."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Antardasha",
        tags=["ckn", "dasha", "antardasha", "sub_period", "nakshatra", "modification", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN059",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: marriage timing — Venus dasha/antardasha with Moon in a Venusian nakshatra "
            "(Bharani/Purva Phalguni/Purva Ashadha) → near-certain marriage. "
            "If also aspected by Jupiter → very happy marriage."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Marriage Dasha",
        tags=["ckn", "dasha", "venus", "marriage", "timing", "jupiter", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN060",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: career peak timing — Sun or Mars dasha with Moon in a Sun/Mars nakshatra "
            "(Krittika/Vishakha/Dhanishtha for Mars; Uttara Phalguni/Uttara Ashadha for Sun). "
            "CKN confirms the nakshatra-dasha convergence as the strongest timing signal."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Career Dasha",
        tags=["ckn", "dasha", "career", "timing", "sun", "mars", "nakshatra", "nadi"],
        implemented=False,
    ),

    # ── CKN Unique Yoga Combinations (CKN061-090) ────────────────────────────
    RuleRecord(
        rule_id="CKN061",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN Nadi Yoga: when two or more planets occupy the same nakshatra → "
            "'Nakshatra Sandhi Yoga'. Results depend on which planets and which nakshatra. "
            "Jupiter+Venus in Rohini → peak prosperity yoga; Saturn+Rahu in Ardra → extreme upheaval."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Nakshatra Sandhi Yoga",
        tags=["ckn", "yoga", "nakshatra", "conjunction", "sandhi", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN062",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Nakshatra Raja Yoga' — when the Lagna nakshatra lord and the "
            "9th lord nakshatra are the same planet → exceptional fortune and dharmic success. "
            "E.g., Lagna in Rohini (Moon), 9th lord is Moon → double Moon activation."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Nakshatra Raja Yoga",
        tags=["ckn", "raja_yoga", "nakshatra", "lagna", "9th_house", "fortune", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN063",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Tarabala Yoga' — when the dasha lord's nakshatra is in a favorable "
            "Tara (star) position from the natal Moon nakshatra (counting 1-9 in groups). "
            "Janma Tara (1), Sampat Tara (2), Vipat (3) indicate quality of dasha period."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Tarabala",
        tags=["ckn", "tarabala", "yoga", "nakshatra", "dasha", "moon", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN064",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN Tara classification: 9 Taras — Janma (birth), Sampat (wealth), "
            "Vipat (danger), Kshema (wellbeing), Pratyak (obstacle), Sadhana (achievement), "
            "Naidhana (death), Mitra (friend), Parama Mitra (best friend). "
            "Dasha lord's nakshatra position from Moon nakshatra determines Tara type."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, 9 Taras",
        tags=["ckn", "tara", "nakshatra", "9_taras", "dasha", "timing", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN065",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Nakshatra Yoga Karaka' — a planet in a nakshatra that creates "
            "exceptional positive results specific to that chart. "
            "The Yoga Karaka nakshatra lord for any chart must be in a kendra or trikona "
            "in a favourable nakshatra for maximum effect."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Yoga Karaka Nakshatra",
        tags=["ckn", "yoga_karaka", "nakshatra", "yoga", "kendra", "trikona", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN066",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Graha Maitri' (planetary friendship via nakshatra): "
            "two planets in friendly nakshatras (both lords are friends) enhance each other. "
            "Jupiter in Punarvasu and Sun in Uttara Phalguni → both in their own-lord nakshatras; supreme yoga."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Graha Maitri Nakshatra",
        tags=["ckn", "graha_maitri", "nakshatra", "planetary_friendship", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN067",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: Nakshatra Parivartana (exchange) — two planets in each other's "
            "nakshatra-lord's nakshatras. E.g., Sun in Rohini (Moon's nakshatra), "
            "Moon in Uttara Phalguni (Sun's nakshatra) → powerful Parivartana through nakshatras."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Nakshatra Parivartana",
        tags=["ckn", "parivartana", "nakshatra", "exchange", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN068",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Saptama Nakshatra Yoga' — the 7th nakshatra from the natal Moon nakshatra "
            "is extremely important for marriage. Planets in the 7th nakshatra from Moon → "
            "strong influence on marriage quality and timing."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Saptama Nakshatra",
        tags=["ckn", "saptama_nakshatra", "marriage", "7th_nakshatra", "timing", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN069",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Vipat Tara Yoga' — when the Vipat (danger) Tara dasha lord is transiting "
            "the natal Moon nakshatra → most dangerous period. Accident, illness, or loss likely. "
            "CKN specifies specific protective mantras for this period."
        ),
        confidence=0.81,
        verse="Chandra Kala Nadi, Vipat Tara",
        tags=["ckn", "vipat_tara", "yoga", "danger", "transit", "protection", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN070",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Chandravela' — Moon's transit through specific nakshatras creates "
            "auspicious windows. Moon in Rohini → best for new ventures. "
            "Moon in Pushya → best for spiritual activities and starting studies. "
            "Moon in Shravana → best for learning and listening."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Chandravela",
        tags=["ckn", "chandravela", "moon", "transit", "muhurta", "auspicious", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN071",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Abhijit Nakshatra' (the 28th nakshatra) — used in Muhurta. "
            "Falls in the last quarter of Uttara Ashadha and first part of Shravana. "
            "CKN: Abhijit nakshatra is the most auspicious for new beginnings."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Abhijit",
        tags=["ckn", "abhijit", "nakshatra", "muhurta", "auspicious", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN072",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Nakshatra Bala' (nakshatra strength) for timing — "
            "1st, 2nd, 4th, 6th, 8th Taras are auspicious; 3rd (Vipat), 5th (Pratyak), "
            "7th (Naidhana) are inauspicious. Daily activities scheduled by Tara position."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Nakshatra Bala",
        tags=["ckn", "nakshatra_bala", "tara", "timing", "muhurta", "nadi"],
        implemented=False,
    ),

    # ── CKN Special Principles (CKN073-095) ──────────────────────────────────
    RuleRecord(
        rule_id="CKN073",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN principle: reading is done at nakshatra precision, not just sign. "
            "Two people born in the same sign (e.g., both Moon in Cancer) have "
            "completely different results based on which nakshatra (Punarvasu/Pushya/Ashlesha)."
        ),
        confidence=0.93,
        verse="Chandra Kala Nadi, Nakshatra Precision",
        tags=["ckn", "nakshatra_precision", "methodology", "moon", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN074",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Nadi Amsha' (Nadi division) — each nakshatra divided into 9 equal parts "
            "of 3°20' each. The sub-section (Nadi Amsha) gives the most precise prediction. "
            "This is the foundational tool for Nadi Jyotisha precision."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Nadi Amsha",
        tags=["ckn", "nadi_amsha", "nakshatra_division", "precision", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN075",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN method: always read Moon's nakshatra first, then Lagna nakshatra, "
            "then Sun's nakshatra. These three give the fundamental personality-destiny-soul triad. "
            "Events occur when all three nakshatra lords are activated together."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Triad Method",
        tags=["ckn", "methodology", "moon", "lagna", "sun", "nakshatra", "triad", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN076",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: Pushkara Navamsha — when a planet is in specific navamsha divisions "
            "that correspond to Pushkara (divine nourishment) degrees. "
            "All planets in Pushkara Navamsha give their best results."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Pushkara Navamsha",
        tags=["ckn", "pushkara_navamsha", "navamsha", "divine", "best_results", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN077",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: Vargottama nakshatra position — when a planet's nakshatra lord "
            "is the same in both D1 and D9 (navamsha is within same nakshatra). "
            "CKN calls this 'Nakshatra Vargottama' — double strength."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Nakshatra Vargottama",
        tags=["ckn", "vargottama", "nakshatra", "d9", "navamsha", "strength", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN078",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: Gandanta (knot) nakshatras — Revati-Ashwini, Ashlesha-Magha, Jyeshtha-Mula "
            "junctions create karmic knot energy. Planets near Gandanta → "
            "intense karmic pressure requiring resolution in this birth."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Gandanta",
        tags=["ckn", "gandanta", "nakshatra", "karma", "junction", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN079",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: Moon in Gandanta nakshatra → intense emotional and spiritual birth. "
            "Moon in Gandanta Ashlesha-Magha → ancestral karma to resolve. "
            "CKN specifies Nadi remedies for Gandanta Moon: connect with ancestors."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Gandanta Moon",
        tags=["ckn", "gandanta", "moon", "ancestral_karma", "remedy", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN080",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Ayanamsha consideration' — Chandra Kala Nadi is composed in the "
            "Lahiri/Chitrapaksha Ayanamsha tradition. Using other ayanamshas "
            "shifts the nakshatra positions and gives different results."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Ayanamsha",
        tags=["ckn", "ayanamsha", "lahiri", "nakshatra_calculation", "methodology", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN081",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Nakshatra Pada' (quarter of nakshatra) analysis. "
            "Each nakshatra has 4 padas of 3°20' each. "
            "1st pada of Rohini → Aries navamsha energy in Taurus (Venus-Mars blend). "
            "Pada determines the navamsha coloring of the nakshatra."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Pada Analysis",
        tags=["ckn", "nakshatra_pada", "pada", "navamsha", "precision", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN082",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN pada results for Moon: Moon in 1st pada of any nakshatra → "
            "Aries energy — initiative and leadership coloring to that nakshatra. "
            "Moon in 2nd pada → Taurus energy — material and sensory coloring. "
            "3rd pada → Gemini energy; 4th pada → Cancer energy."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Pada-Moon",
        tags=["ckn", "nakshatra_pada", "moon", "coloring", "navamsha", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN083",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Atichara' (fast-moving planets) — Mercury and Venus when in direct "
            "motion at high speed intensify their results. "
            "Retrograde planets in their own nakshatra → results delayed but doubled when they come."
        ),
        confidence=0.81,
        verse="Chandra Kala Nadi, Atichara",
        tags=["ckn", "atichara", "mercury", "venus", "retrograde", "speed", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN084",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Pranapada' (breath point) analysis. Pranapada is calculated from "
            "sunrise and the Lagna nakshatra. When Pranapada coincides with a planet's nakshatra "
            "in transit → that planet's results intensify dramatically for that day."
        ),
        confidence=0.78,
        verse="Chandra Kala Nadi, Pranapada",
        tags=["ckn", "pranapada", "nakshatra", "transit", "daily_timing", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN085",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Nakshatra Sandhi' (nakshatra junction) — the last 48 minutes of one "
            "nakshatra and first 48 minutes of the next are the junction zone. "
            "Planets in Sandhi give weak or confused results initially."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Nakshatra Sandhi",
        tags=["ckn", "nakshatra_sandhi", "junction", "weakness", "nadi"],
        implemented=False,
    ),

    # ── CKN Medical and Longevity Principles (CKN086-100) ────────────────────
    RuleRecord(
        rule_id="CKN086",
        source="ChandraKalaNadi",
        chapter="Medical",
        school="nadi",
        category="medical",
        description=(
            "CKN medical: Moon's nakshatra indicates the body system predisposed to weakness. "
            "Moon in Rohini → throat/neck. Moon in Ardra → skin/respiratory. "
            "Moon in Pushya → chest/lungs/immunity. Moon in Magha → heart/spine."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Medical Chapter",
        tags=["ckn", "medical", "moon", "nakshatra", "body_parts", "health", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN087",
        source="ChandraKalaNadi",
        chapter="Medical",
        school="nadi",
        category="medical",
        description=(
            "CKN: nakshatra of afflicting planet indicates disease type. "
            "Saturn in Ardra → lung/skin diseases. Saturn in Vishakha → kidney issues. "
            "Mars in Krittika → fevers and inflammatory conditions. "
            "Rahu in Ashlesha → poisoning or mysterious illness."
        ),
        confidence=0.81,
        verse="Chandra Kala Nadi, Disease Nakshatra",
        tags=["ckn", "medical", "disease", "nakshatra", "saturn", "mars", "rahu", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN088",
        source="ChandraKalaNadi",
        chapter="Medical",
        school="nadi",
        category="medical",
        description=(
            "CKN longevity: the 8th house lord's nakshatra determines the nature of "
            "longevity challenges. 8th lord in Jyeshtha → sharp/sudden health crises. "
            "8th lord in Uttara Bhadrapada → chronic but slow conditions. "
            "8th lord in Shravana → auditory issues; mobility problems."
        ),
        confidence=0.80,
        verse="Chandra Kala Nadi, Longevity Nakshatra",
        tags=["ckn", "longevity", "8th_house", "nakshatra", "health", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN089",
        source="ChandraKalaNadi",
        chapter="Medical",
        school="nadi",
        category="medical",
        description=(
            "CKN: Ketu in 1st house nakshatra → mysterious ailments, psychosomatic issues. "
            "Ketu in Ashwini (1st) → sudden illness and recovery. "
            "Ketu in Magha (1st) → ancestral illness patterns. "
            "CKN remedy: worship Ketu deity of that nakshatra."
        ),
        confidence=0.80,
        verse="Chandra Kala Nadi, Ketu Medical",
        tags=["ckn", "medical", "ketu", "nakshatra", "psychosomatic", "remedy", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN090",
        source="ChandraKalaNadi",
        chapter="Medical",
        school="nadi",
        category="medical",
        description=(
            "CKN: when Moon's Tara (counting from natal nakshatra) in any period is "
            "Naidhana (7th Tara = death Tara) → critical health watch period. "
            "Naidhana Tara + Sade Sati simultaneously → most dangerous health period."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Naidhana Tara Health",
        tags=["ckn", "medical", "naidhana_tara", "sade_sati", "critical_health", "nadi"],
        implemented=False,
    ),

    # ── CKN Philosophy and Synthesis (CKN091-120) ────────────────────────────
    RuleRecord(
        rule_id="CKN091",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN philosophy: the Moon is the mind and the nakshatras are the "
            "mind's 27 states. Understanding someone's natal Moon nakshatra "
            "is understanding their fundamental mental nature."
        ),
        confidence=0.90,
        verse="Chandra Kala Nadi, Philosophy Ch.",
        tags=["ckn", "philosophy", "moon", "mind", "nakshatra", "fundamental", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN092",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN: Nadi astrology reads the karma written in the stars at the moment of birth. "
            "The nakshatra at birth moment captures the soul's entire karmic program. "
            "Prediction is reading what is written — not determining what could happen."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Karma Introduction",
        tags=["ckn", "philosophy", "karma", "birth", "nakshatra", "prediction", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN093",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN: text was encoded on palm leaves using shorthand. "
            "Full reading requires an oral tradition transmission from master to student. "
            "Modern printed versions are partial; complete oral commentary is essential."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Historical Introduction",
        tags=["ckn", "history", "palm_leaves", "oral_tradition", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN094",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN: Deva Keralam (divine Kerala text) is another name for CKN, "
            "as it originates from the Nadi tradition of Kerala and Tamil Nadu. "
            "Contains ~3000+ slokas covering all 27 nakshatra-planet combinations."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Deva Keralam Introduction",
        tags=["ckn", "history", "deva_keralam", "kerala", "tamil", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN095",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN synthesis: the complete Nadi reading requires "
            "(1) Moon's nakshatra, (2) Lagna nakshatra, (3) dasha lord's nakshatra, "
            "(4) transit planet's nakshatra, and (5) Tara Bala calculation. "
            "All five together yield the Nadi prediction."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Complete Method",
        tags=["ckn", "synthesis", "methodology", "5_step", "prediction", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN096",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: planets in exaltation nakshatra give maximum results of their nature. "
            "Sun exalted in Aries → in Ashwini pada: maximum vigor. In Bharani pada: maximum healing. "
            "In Krittika pada: maximum authority. The nakshatra further refines exaltation."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Exaltation Nakshatra",
        tags=["ckn", "exaltation", "nakshatra", "sun", "aries", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN097",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: debilitation nakshatra analysis. Moon debilitated in Scorpio → "
            "in Vishakha pada: most difficult emotional struggles. "
            "In Anuradha pada: struggles but devotion saves. In Jyeshtha pada: authority despite pain."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Debilitation Nakshatra",
        tags=["ckn", "debilitation", "nakshatra", "moon", "scorpio", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN098",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Adhana Yoga' (wealth-through-hardship) — Saturn in 11th nakshatra "
            "from Moon × Mars in 10th from Moon → grinding but ultimately victorious career. "
            "CKN: this is the nakshatra basis for the classical Dhana Yoga."
        ),
        confidence=0.80,
        verse="Chandra Kala Nadi, Adhana Yoga",
        tags=["ckn", "adhana_yoga", "wealth", "saturn", "mars", "career", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN099",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Nakshatra Shadbala' — the strength of a planet in nakshatra is highest "
            "when it occupies its own nakshatra (lord's own). "
            "Moon in Rohini > Moon in Punarvasu > Moon anywhere else for nakshatra strength."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Nakshatra Shadbala",
        tags=["ckn", "nakshatra_shadbala", "strength", "moon", "rohini", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN100",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Kala Sarpa in Nakshatra' — when Rahu and Ketu axis spans "
            "Ashwini-Swati or Bharani-Vishakha or other specific nakshatra pairs, "
            "the Kala Sarpa Yoga takes specific characteristics based on those nakshatras."
        ),
        confidence=0.80,
        verse="Chandra Kala Nadi, Kala Sarpa Nakshatra",
        tags=["ckn", "kala_sarpa", "rahu", "ketu", "nakshatra", "yoga", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN101",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Muhurta Nakshatra' — best nakshatras for specific activities. "
            "Marriage: Rohini, Mrigashira, Magha, Uttara Phalguni, Hasta, Swati, Anuradha, "
            "Mula, Uttara Ashadha, Uttara Bhadrapada, Revati."
        ),
        confidence=0.86,
        verse="Chandra Kala Nadi, Marriage Muhurta",
        tags=["ckn", "muhurta", "nakshatra", "marriage", "auspicious", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN102",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: best nakshatras for starting business: Rohini, Pushya, Hasta, "
            "Uttara Phalguni, Uttara Ashadha, Revati. "
            "Avoid: Bharani, Ardra, Ashlesha, Vishakha (inauspicious for new ventures)."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Business Muhurta",
        tags=["ckn", "muhurta", "nakshatra", "business", "start", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN103",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Yoga Taras' — bright stars within nakshatras that are especially "
            "powerful. Spica (in Chitra) and Antares (in Jyeshtha) are the two "
            "most powerful Yoga Taras in the zodiac per CKN."
        ),
        confidence=0.80,
        verse="Chandra Kala Nadi, Yoga Tara",
        tags=["ckn", "yoga_tara", "stars", "chitra", "jyeshtha", "powerful", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN104",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: Vimshottari Dasha starting point (Janma Nakshatra) is the foundation. "
            "The exact nakshatra-pada of the Moon at birth determines the "
            "remaining balance of the first dasha — nakshatra-level precision is essential."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Vimshottari Foundation",
        tags=["ckn", "vimshottari", "nakshatra_pada", "dasha_balance", "precision", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN105",
        source="ChandraKalaNadi",
        chapter="Dasha_Results",
        school="nadi",
        category="dasha",
        description=(
            "CKN: death during Naidhana Tara dasha — when the Mahadasha lord's nakshatra "
            "is the 7th Tara from the natal Moon nakshatra → the period of greatest danger. "
            "Jupiter as Mahadasha lord in Naidhana can mitigate; Rahu intensifies."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Death Period",
        tags=["ckn", "dasha", "naidhana_tara", "death", "longevity", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN106",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: 'Nakshatra Papagraha' (malefic nakshatra) — when malefics occupy "
            "nakshatras ruled by other malefics → intensified malefic results. "
            "Saturn in Ardra (Rahu's), Mars in Jyeshtha (Mercury's) → uniquely problematic."
        ),
        confidence=0.81,
        verse="Chandra Kala Nadi, Malefic Nakshatra",
        tags=["ckn", "malefics", "nakshatra", "saturn", "mars", "intensified", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN107",
        source="ChandraKalaNadi",
        chapter="Planet_Combinations",
        school="nadi",
        category="planet_combination",
        description=(
            "CKN: 'Nakshatra Subhagraha' (benefic nakshatra) — when benefics occupy "
            "nakshatras ruled by other benefics → intensified benefic results. "
            "Jupiter in Pushya (Saturn's but positive), Venus in Rohini (Moon's) → extraordinary."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Benefic Nakshatra",
        tags=["ckn", "benefics", "nakshatra", "jupiter", "venus", "intensified", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN108",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: 'Ashtamamsha Transit' — when a planet transits the 8th nakshatra "
            "from the natal Moon nakshatra → challenging period for that planet's affairs. "
            "Jupiter in Ashtama nakshatra from Moon → knowledge blocked, children ill."
        ),
        confidence=0.81,
        verse="Chandra Kala Nadi, Ashtamamsha Transit",
        tags=["ckn", "transit", "ashtama", "nakshatra", "8th_nakshatra", "challenges", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN109",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: Jupiter transiting Kshema Tara (4th from natal Moon nakshatra) → "
            "period of wellbeing, happiness, and positive growth. "
            "Best time to start projects and relationships. One of the most auspicious transit windows."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Kshema Transit",
        tags=["ckn", "transit", "jupiter", "kshema_tara", "wellbeing", "auspicious", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN110",
        source="ChandraKalaNadi",
        chapter="Gochara",
        school="nadi",
        category="transit",
        description=(
            "CKN: 'Sampat Transit' — when Jupiter transits the 2nd Tara nakshatra "
            "from natal Moon → wealth, property acquisition, and material gains. "
            "If combined with Venus dasha → maximum financial accumulation period."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Sampat Transit",
        tags=["ckn", "transit", "jupiter", "sampat_tara", "wealth", "property", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN111",
        source="ChandraKalaNadi",
        chapter="Nadi_Yogas",
        school="nadi",
        category="yoga",
        description=(
            "CKN: 'Parama Mitra Tara' (best friend star) — the 9th Tara from natal Moon. "
            "When dasha lord is in this position → best period in the entire dasha for "
            "receiving help, support, and good relationships."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Parama Mitra Tara",
        tags=["ckn", "parama_mitra_tara", "dasha", "relationships", "support", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN112",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "CKN: Moon in gandanta nakshatras (Revati, Ashlesha, Jyeshtha) → "
            "spiritual and psychological intensity from birth. "
            "Moon in last pada of Jyeshtha (gandanta) → most challenging childhood, "
            "often separated from mother early."
        ),
        confidence=0.83,
        verse="Chandra Kala Nadi, Gandanta Moon Houses",
        tags=["ckn", "moon", "gandanta", "jyeshtha", "ashlesha", "revati", "childhood", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN113",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "CKN: Moon's nakshatras in fire signs (Aries/Leo/Sagittarius) → "
            "active, passionate, quick emotional responses. "
            "In Krittika/Purva Phalguni/Purva Ashadha → most fire-like Moon results."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Fire Nakshatra Moon",
        tags=["ckn", "moon", "fire_signs", "nakshatra", "aries", "leo", "sagittarius", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN114",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "CKN: Moon's nakshatras in earth signs (Taurus/Virgo/Capricorn) → "
            "stable, sensory, practical emotional nature. "
            "Rohini/Uttara Phalguni/Uttara Ashadha → most earth-like Moon stability."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Earth Nakshatra Moon",
        tags=["ckn", "moon", "earth_signs", "nakshatra", "taurus", "virgo", "capricorn", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN115",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "CKN: Moon's nakshatras in air signs (Gemini/Libra/Aquarius) → "
            "communicative, social, intellectually active emotions. "
            "Mrigashira/Swati/Shatabhisha → most air-like Moon adaptability."
        ),
        confidence=0.84,
        verse="Chandra Kala Nadi, Air Nakshatra Moon",
        tags=["ckn", "moon", "air_signs", "nakshatra", "gemini", "libra", "aquarius", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN116",
        source="ChandraKalaNadi",
        chapter="Moon_Nakshatras",
        school="nadi",
        category="moon_nakshatra",
        description=(
            "CKN: Moon's nakshatras in water signs (Cancer/Scorpio/Pisces) → "
            "deep emotional sensitivity, psychic, intuitive. "
            "Punarvasu-4th pada/Pushya/Ashlesha → Cancer Moon nakshatras, most emotionally deep."
        ),
        confidence=0.85,
        verse="Chandra Kala Nadi, Water Nakshatra Moon",
        tags=["ckn", "moon", "water_signs", "nakshatra", "cancer", "scorpio", "pisces", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN117",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Yogi and Avayogi' — Yogi nakshatra is the most beneficial nakshatra "
            "for the chart, calculated from Sun + Moon + Lagna degrees. "
            "Avayogi is the most difficult. Their dasha lords govern best/worst periods."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Yogi Avayogi",
        tags=["ckn", "yogi", "avayogi", "nakshatra", "timing", "beneficial", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN118",
        source="ChandraKalaNadi",
        chapter="Special_Principles",
        school="nadi",
        category="special_principle",
        description=(
            "CKN: 'Duplicate Nakshatra' (same nakshatra for Moon and Lagna) → "
            "extremely focused life path; the soul and mind are perfectly aligned. "
            "Very rare combination; CKN says this person's destiny is singular and clear."
        ),
        confidence=0.82,
        verse="Chandra Kala Nadi, Duplicate Nakshatra",
        tags=["ckn", "duplicate_nakshatra", "moon", "lagna", "alignment", "destiny", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN119",
        source="ChandraKalaNadi",
        chapter="Synthesis",
        school="nadi",
        category="synthesis",
        description=(
            "CKN synthesis: the greatest precision in prediction is achieved when "
            "the nakshatra of the dasha lord, the transit planet, and the natal Moon "
            "all converge in a harmonious Tara relationship simultaneously."
        ),
        confidence=0.87,
        verse="Chandra Kala Nadi, Final Synthesis",
        tags=["ckn", "synthesis", "precision", "nakshatra", "tara", "convergence", "nadi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="CKN120",
        source="ChandraKalaNadi",
        chapter="Philosophy",
        school="nadi",
        category="philosophy",
        description=(
            "CKN concluding teaching: the 27 nakshatras are the 27 letters of the "
            "cosmic Sanskrit alphabet. The natal chart is a word or sentence written "
            "in this alphabet. The astrologer's art is to read this cosmic scripture."
        ),
        confidence=0.88,
        verse="Chandra Kala Nadi, Conclusion",
        tags=["ckn", "philosophy", "nakshatras", "cosmic_alphabet", "scripture", "nadi"],
        implemented=False,
    ),
]

for rule in _RULES:
    CHANDRA_KALA_NADI_REGISTRY.add(rule)
