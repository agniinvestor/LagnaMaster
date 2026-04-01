"""
src/corpus/lagna_extended_rules.py — Lagna (Ascendant) Extended Rules (S248)

Encodes detailed rules for all 12 Lagnas (Ascendants) — the physical body,
personality, and life-path characteristics associated with each rising sign.
Also covers Chandra Lagna (Moon sign) and Surya Lagna (Sun sign) interpretations.

Sources:
  BPHS Ch.7-18 — Lagna Adhyaya (Parashara)
  Phala Deepika Ch.1 — Lagna characteristics
  Brihat Jataka Ch.1 — Rashi Nature and Lagna effects

30 rules total: LGE001-LGE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

LAGNA_EXTENDED_RULES_REGISTRY = CorpusRegistry()

_LAGNA_RULES = [
    # --- Aries Lagna (LGE001) ---
    RuleRecord(
        rule_id="LGE001",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Aries Lagna (Mesha): Mars-ruled. Personality: bold, impulsive, pioneering, "
            "quick to anger and quick to forgive, natural leader, athletic. "
            "Body: head, face; prone to head injuries, fevers, blood issues. "
            "Best houses: 1st, 9th, 10th. Yogakaraka: Saturn (owns 10th+11th). "
            "Favorable periods: Mars, Sun dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.7 v.1-12",
        tags=["lagna", "aries_lagna", "mesha", "mars_ruled", "bold_impulsive"],
        implemented=False,
    ),
    # --- Taurus Lagna (LGE002) ---
    RuleRecord(
        rule_id="LGE002",
        source="BPHS",
        chapter="Ch.8",
        school="parashari",
        category="lagna",
        description=(
            "Taurus Lagna (Vrishabha): Venus-ruled. Personality: patient, stubborn, "
            "sensual, art-loving, practical, financially oriented, slow but steady. "
            "Body: neck, throat; prone to throat issues, thyroid. "
            "Best houses: 1st, 5th, 9th. Yogakaraka: Saturn (owns 9th+10th). "
            "Favorable periods: Venus, Mercury, Saturn dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.8 v.1-12",
        tags=["lagna", "taurus_lagna", "vrishabha", "venus_ruled", "patient_sensual"],
        implemented=False,
    ),
    # --- Gemini Lagna (LGE003) ---
    RuleRecord(
        rule_id="LGE003",
        source="BPHS",
        chapter="Ch.9",
        school="parashari",
        category="lagna",
        description=(
            "Gemini Lagna (Mithuna): Mercury-ruled. Personality: intellectual, versatile, "
            "communicative, witty, dual-natured, restless, skilled in multiple fields. "
            "Body: shoulders, arms, lungs; prone to respiratory issues, nervous system. "
            "Best houses: 1st, 4th, 9th. Most difficult: Saturn (owns 8th+9th). "
            "Favorable periods: Mercury, Venus dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.9 v.1-12",
        tags=["lagna", "gemini_lagna", "mithuna", "mercury_ruled", "intellectual_versatile"],
        implemented=False,
    ),
    # --- Cancer Lagna (LGE004) ---
    RuleRecord(
        rule_id="LGE004",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="lagna",
        description=(
            "Cancer Lagna (Karka): Moon-ruled. Personality: nurturing, intuitive, emotional, "
            "home-loving, psychic, protective, memory-oriented, changeable moods. "
            "Body: chest, breasts, stomach; prone to digestive issues, emotional eating. "
            "Best houses: 1st, 5th, 9th, 11th. Yogakaraka: Mars (owns 5th+10th). "
            "Favorable periods: Moon, Mars, Jupiter dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.10 v.1-12",
        tags=["lagna", "cancer_lagna", "karka", "moon_ruled", "nurturing_intuitive"],
        implemented=False,
    ),
    # --- Leo Lagna (LGE005) ---
    RuleRecord(
        rule_id="LGE005",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="lagna",
        description=(
            "Leo Lagna (Simha): Sun-ruled. Personality: regal, proud, generous, dramatic, "
            "authoritative, loyal, loves recognition and leadership. "
            "Body: heart, spine, back; prone to heart issues, ego-related ailments. "
            "Best houses: 1st, 5th, 9th. Difficult: Saturn (8th+7th lord). "
            "Favorable periods: Sun, Mars, Jupiter dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.11 v.1-12",
        tags=["lagna", "leo_lagna", "simha", "sun_ruled", "regal_proud"],
        implemented=False,
    ),
    # --- Virgo Lagna (LGE006) ---
    RuleRecord(
        rule_id="LGE006",
        source="BPHS",
        chapter="Ch.12",
        school="parashari",
        category="lagna",
        description=(
            "Virgo Lagna (Kanya): Mercury-ruled. Personality: analytical, detail-oriented, "
            "health-conscious, perfectionist, service-minded, practical, critical. "
            "Body: intestines, digestive system; prone to digestive disorders, anxiety. "
            "Best houses: 1st, 5th, 9th. Most challenging: Mars (3rd+8th lord). "
            "Favorable periods: Mercury, Venus dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.12 v.1-12",
        tags=["lagna", "virgo_lagna", "kanya", "mercury_ruled", "analytical_perfectionist"],
        implemented=False,
    ),
    # --- Libra Lagna (LGE007) ---
    RuleRecord(
        rule_id="LGE007",
        source="BPHS",
        chapter="Ch.13",
        school="parashari",
        category="lagna",
        description=(
            "Libra Lagna (Tula): Venus-ruled. Personality: diplomatic, balanced, "
            "relationship-oriented, artistic, indecisive, charming, justice-seeking. "
            "Body: kidneys, lower back; prone to kidney issues, lower back pain. "
            "Best houses: 1st, 5th, 9th. Yogakaraka: Saturn (owns 4th+5th). "
            "Favorable periods: Venus, Saturn, Mercury dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.13 v.1-12",
        tags=["lagna", "libra_lagna", "tula", "venus_ruled", "diplomatic_balanced"],
        implemented=False,
    ),
    # --- Scorpio Lagna (LGE008) ---
    RuleRecord(
        rule_id="LGE008",
        source="BPHS",
        chapter="Ch.14",
        school="parashari",
        category="lagna",
        description=(
            "Scorpio Lagna (Vrischika): Mars-ruled (Ketu co-ruler). "
            "Personality: intense, secretive, transformative, investigative, "
            "psychic, vindictive, deeply passionate, resilient. "
            "Body: reproductive system, bladder; prone to STDs, urinary issues. "
            "Best houses: 1st, 5th, 9th. Yogakaraka: Moon (owns 9th). "
            "Favorable periods: Moon, Sun, Jupiter dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.14 v.1-12",
        tags=["lagna", "scorpio_lagna", "vrischika", "mars_ruled", "intense_secretive"],
        implemented=False,
    ),
    # --- Sagittarius Lagna (LGE009) ---
    RuleRecord(
        rule_id="LGE009",
        source="BPHS",
        chapter="Ch.15",
        school="parashari",
        category="lagna",
        description=(
            "Sagittarius Lagna (Dhanu): Jupiter-ruled. Personality: philosophical, "
            "adventurous, optimistic, teacher/preacher, freedom-loving, generous. "
            "Body: hips, thighs, liver; prone to hip problems, liver issues, excess. "
            "Best houses: 1st, 5th, 9th. Most difficult: Mercury (7th+10th = Kendra adhipati). "
            "Favorable periods: Jupiter, Sun, Mars dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.15 v.1-12",
        tags=["lagna", "sagittarius_lagna", "dhanu", "jupiter_ruled", "philosophical"],
        implemented=False,
    ),
    # --- Capricorn Lagna (LGE010) ---
    RuleRecord(
        rule_id="LGE010",
        source="BPHS",
        chapter="Ch.16",
        school="parashari",
        category="lagna",
        description=(
            "Capricorn Lagna (Makara): Saturn-ruled. Personality: disciplined, ambitious, "
            "practical, persistent, career-focused, responsible, late bloomer. "
            "Body: knees, bones, skin; prone to joint problems, skin conditions, depression. "
            "Best houses: 1st, 5th, 9th. Yogakaraka: Venus (owns 5th+10th). "
            "Favorable periods: Saturn, Mercury, Venus dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.16 v.1-12",
        tags=["lagna", "capricorn_lagna", "makara", "saturn_ruled", "disciplined_ambitious"],
        implemented=False,
    ),
    # --- Aquarius Lagna (LGE011) ---
    RuleRecord(
        rule_id="LGE011",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="lagna",
        description=(
            "Aquarius Lagna (Kumbha): Saturn-ruled (Rahu co-ruler). "
            "Personality: humanitarian, unconventional, intellectual, independent, "
            "idealistic, scientific, detached. "
            "Body: ankles, calves, circulatory system; prone to varicose veins, ankle injuries. "
            "Best houses: 1st, 5th, 9th. Yogakaraka: Venus (owns 4th+9th). "
            "Favorable periods: Saturn, Venus, Mercury dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.17 v.1-12",
        tags=["lagna", "aquarius_lagna", "kumbha", "saturn_ruled", "humanitarian"],
        implemented=False,
    ),
    # --- Pisces Lagna (LGE012) ---
    RuleRecord(
        rule_id="LGE012",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="lagna",
        description=(
            "Pisces Lagna (Meena): Jupiter-ruled (Ketu co-ruler). "
            "Personality: compassionate, spiritual, imaginative, artistic, "
            "intuitive, dreamy, self-sacrificing, psychic. "
            "Body: feet, lymphatic system; prone to foot problems, addiction. "
            "Best houses: 1st, 5th, 9th. Most difficult: Mercury (4th+7th lords). "
            "Favorable periods: Jupiter, Moon, Mars dashas."
        ),
        confidence=0.90,
        verse="BPHS Ch.18 v.1-12",
        tags=["lagna", "pisces_lagna", "meena", "jupiter_ruled", "compassionate_spiritual"],
        implemented=False,
    ),
    # --- Yogakaraka Principles by Lagna (LGE013-016) ---
    RuleRecord(
        rule_id="LGE013",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Yogakaraka by Lagna — Fire Lagnas: "
            "Aries: Saturn (owns 10th+11th) = career gains yogakaraka. "
            "Leo: Mars (owns 4th+9th) = fortune+home yogakaraka. "
            "Sagittarius: None universally agreed; Sun (9th lord) is very favorable. "
            "For fire lagnas, Saturn's role varies significantly."
        ),
        confidence=0.88,
        verse="BPHS Ch.7 v.13-20",
        tags=["lagna", "yogakaraka", "fire_lagna", "aries_leo_sagittarius"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE014",
        source="BPHS",
        chapter="Ch.8",
        school="parashari",
        category="lagna",
        description=(
            "Yogakaraka by Lagna — Earth Lagnas: "
            "Taurus: Saturn (owns 9th+10th) = strongest yogakaraka for earth lagnas. "
            "Virgo: Venus (owns 2nd+9th) = wealth + fortune yogakaraka. "
            "Capricorn: Venus (owns 5th+10th) = best yogakaraka for Capricorn. "
            "Earth lagnas strongly benefit from Venus and Saturn periods."
        ),
        confidence=0.88,
        verse="BPHS Ch.8 v.13-20",
        tags=["lagna", "yogakaraka", "earth_lagna", "taurus_virgo_capricorn", "venus_saturn"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE015",
        source="BPHS",
        chapter="Ch.9",
        school="parashari",
        category="lagna",
        description=(
            "Yogakaraka by Lagna — Air Lagnas: "
            "Gemini: Venus (owns 5th+12th) — some consider favorable for Gemini. "
            "Libra: Saturn (owns 4th+5th) = excellent yogakaraka for Libra. "
            "Aquarius: Venus (owns 4th+9th) = fortune+home yogakaraka. "
            "Air lagnas greatly benefit from Venus periods (exception: Gemini)."
        ),
        confidence=0.87,
        verse="BPHS Ch.9 v.13-20",
        tags=["lagna", "yogakaraka", "air_lagna", "gemini_libra_aquarius", "venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE016",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="lagna",
        description=(
            "Yogakaraka by Lagna — Water Lagnas: "
            "Cancer: Mars (owns 5th+10th) = unique yogakaraka for Cancer lagna. "
            "Scorpio: Jupiter (owns 2nd+5th) = wealth+progeny yogakaraka. "
            "Pisces: Mars (owns 2nd+9th) = wealth+fortune yogakaraka. "
            "Water lagnas benefit from Mars and Jupiter; avoid Mercury."
        ),
        confidence=0.87,
        verse="BPHS Ch.10 v.13-20",
        tags=["lagna", "yogakaraka", "water_lagna", "cancer_scorpio_pisces", "mars_jupiter"],
        implemented=False,
    ),
    # --- Kendra Adhipati Dosha (LGE017-018) ---
    RuleRecord(
        rule_id="LGE017",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Kendra Adhipati Dosha (quadrant lord affliction): Natural benefics "
            "(Jupiter, Venus, Mercury) become malefic when they own Kendra houses. "
            "Jupiter owning 1st/4th/7th/10th from lagna = reduced beneficence. "
            "This applies most strongly for Sagittarius (Jupiter owns 1st+4th) and "
            "Pisces (Jupiter owns 1st+10th) lagnas."
        ),
        confidence=0.88,
        verse="BPHS Ch.7 v.21-28",
        tags=["lagna", "kendra_adhipati_dosha", "benefic_kendra_lord", "jupiter_venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE018",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Trikona Adhipati Shubha (trine lord beneficence): Natural malefics "
            "(Saturn, Mars) become benefic when they own Trikona houses (5th, 9th). "
            "Saturn owning 5th (for Virgo lagna) or 9th (for Taurus/Gemini) = auspicious. "
            "Mars owning 5th (for Cancer) or 9th (for Scorpio/Pisces) = fortunate."
        ),
        confidence=0.87,
        verse="BPHS Ch.7 v.29-36",
        tags=["lagna", "trikona_adhipati", "malefic_trikona_lord", "saturn_mars_benefic"],
        implemented=False,
    ),
    # --- Chandra and Surya Lagna (LGE019-022) ---
    RuleRecord(
        rule_id="LGE019",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Chandra Lagna (Moon sign as Ascendant): Houses counted from Moon sign. "
            "Chandra Lagna predictions reveal emotional and mental tendencies. "
            "For Rashi/Moon sign based predictions, treat Moon sign as Lagna "
            "and apply all lagna-based analysis from Moon's position."
        ),
        confidence=0.88,
        verse="BPHS Ch.7 v.37-42",
        tags=["lagna", "chandra_lagna", "moon_sign", "emotional_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE020",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Surya Lagna (Sun sign as Ascendant): Houses counted from Sun sign. "
            "Surya Lagna reveals soul-level inclinations and dharmic path. "
            "In some traditions, Solar arc calculations use Surya Lagna as reference. "
            "Three-lagna system (Lagna + Chandra + Surya) gives complete picture."
        ),
        confidence=0.86,
        verse="BPHS Ch.7 v.43-48",
        tags=["lagna", "surya_lagna", "sun_sign", "soul_lagna", "three_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE021",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Lagna strength indicators: A strong Lagna requires: "
            "(1) Lagna lord in Kendra/Trikona; (2) Benefics in Lagna; "
            "(3) No malefics in Lagna (esp. 8th lord); (4) Lagna lord unafflicted. "
            "Strong Lagna = strong constitution, good health, ability to overcome adversity."
        ),
        confidence=0.90,
        verse="BPHS Ch.7 v.49-56",
        tags=["lagna", "lagna_strength", "kendra_trikona_lord", "no_malefics", "health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE022",
        source="Phaladeepika",
        chapter="Ch.1",
        school="mantreswara",
        category="lagna",
        description=(
            "Lagna lord in each house — general effects: "
            "Lagna lord in 1st = self-made; 2nd = family wealth; 3rd = siblings/travel; "
            "4th = happiness/home; 5th = children/education; 6th = health challenges; "
            "7th = spouse influence; 8th = longevity/transformation; 9th = fortune; "
            "10th = career; 11th = gains; 12th = spirituality/losses."
        ),
        confidence=0.88,
        verse="PD Ch.1 v.1-12",
        tags=["lagna", "lagna_lord_house", "12_house_results", "general_effects"],
        implemented=False,
    ),
    # --- Special Ascendant Effects (LGE023-027) ---
    RuleRecord(
        rule_id="LGE023",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Planet in Lagna effects: "
            "Sun in Lagna = authority, strong will, prominent father, eye issues. "
            "Moon in Lagna = emotional, public life, beautiful, mother-connection. "
            "Mars in Lagna = aggressive, mechanical skill, accidents risk. "
            "Mercury in Lagna = intelligent, communicative, youthful appearance."
        ),
        confidence=0.88,
        verse="BPHS Ch.7 v.57-70",
        tags=["lagna", "planet_in_lagna", "sun_moon_mars_mercury", "first_house_effects"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE024",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Planet in Lagna (benefics): "
            "Jupiter in Lagna = wisdom, spiritual authority, wealth, righteous, long-lived. "
            "Venus in Lagna = beauty, artistry, sensual pleasures, marital happiness. "
            "Saturn in Lagna = hardworking, slow start, longevity, detachment. "
            "Rahu in Lagna = unconventional, foreign influence, ambitious."
        ),
        confidence=0.87,
        verse="BPHS Ch.7 v.71-82",
        tags=["lagna", "planet_in_lagna", "jupiter_venus_saturn_rahu", "first_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE025",
        source="Brihat Jataka",
        chapter="Ch.1",
        school="varahamihira",
        category="lagna",
        description=(
            "Rising sign physical characteristics (Varahamihira): "
            "Aries: medium stature, long neck, ambitious. Taurus: stocky, dark hair, musical. "
            "Gemini: tall, straight, quick mind. Cancer: broad, round face, shy. "
            "Leo: broad shoulders, bold walk. Virgo: graceful, scholarly appearance."
        ),
        confidence=0.82,
        verse="BJ Ch.1 v.1-6",
        tags=["lagna", "physical_characteristics", "varahamihira", "aries_to_virgo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE026",
        source="Brihat Jataka",
        chapter="Ch.1",
        school="varahamihira",
        category="lagna",
        description=(
            "Rising sign physical characteristics continued: "
            "Libra: graceful, balanced features, charming. Scorpio: intense gaze, strong build. "
            "Sagittarius: athletic, large forehead. Capricorn: thin, bony, prominent nose. "
            "Aquarius: strong calves, humanitarian expression. Pisces: large eyes, dreamy look."
        ),
        confidence=0.82,
        verse="BJ Ch.1 v.7-12",
        tags=["lagna", "physical_characteristics", "varahamihira", "libra_to_pisces"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE027",
        source="Phaladeepika",
        chapter="Ch.1",
        school="mantreswara",
        category="lagna",
        description=(
            "Lagna as karmic lens: The lagna is the 'door' through which the soul "
            "enters physical life. The karaka of the lagna (the planet that rules it) "
            "sets the fundamental life theme. "
            "Lagna degree within the sign matters: early degrees = struggles first, "
            "later success; late degrees = comfort early, challenges later."
        ),
        confidence=0.85,
        verse="PD Ch.1 v.13-20",
        tags=["lagna", "karmic_lens", "soul_entry", "degree_position", "life_theme"],
        implemented=False,
    ),
    # --- Lagna Special Combinations (LGE028-030) ---
    RuleRecord(
        rule_id="LGE028",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "Lagna Vargottama: Lagna degree is in the same sign in both D1 (Rashi) "
            "and D9 (Navamsha). Vargottama Lagna = exceptional chart strength; "
            "person has strong, clear life purpose and identity. "
            "Physical constitution excellent; personality very consistent and authentic."
        ),
        confidence=0.88,
        verse="BPHS Ch.7 v.83-88",
        tags=["lagna", "vargottama_lagna", "d1_d9_same_sign", "exceptional_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE029",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="lagna",
        description=(
            "8th lord in Lagna (Sarpa Yoga variant): 8th lord in Lagna = "
            "health concerns, tendency toward crises, interest in occult/mysteries. "
            "Also creates transformation theme in the personality. "
            "If 8th lord is also a maraka lord = significant health vulnerability. "
            "Benefic influence on lagna can mitigate this."
        ),
        confidence=0.86,
        verse="BPHS Ch.7 v.89-94",
        tags=["lagna", "8th_lord_lagna", "health_concerns", "occult", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="LGE030",
        source="Phaladeepika",
        chapter="Ch.1",
        school="mantreswara",
        category="lagna",
        description=(
            "Multiple planets in Lagna: 3+ planets in Lagna = complex personality "
            "with multiple competing drives. The planet with highest degree dominates. "
            "All benefics in Lagna = highly auspicious, beautiful, talented. "
            "All malefics in Lagna = challenging life but powerful, enduring character."
        ),
        confidence=0.85,
        verse="PD Ch.1 v.21-28",
        tags=["lagna", "multiple_planets_lagna", "3_plus_planets", "complex_personality"],
        implemented=False,
    ),
]

for rule in _LAGNA_RULES:
    LAGNA_EXTENDED_RULES_REGISTRY.add(rule)
