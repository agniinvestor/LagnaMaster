"""
src/corpus/bphs_graha_characteristics.py — BPHS Graha Characteristics (S254)

Exhaustive encoding of all planet (graha) natures, attributes, and karakatva
from BPHS Ch.3-10. Covers: nature/temperament, elements, doshas, body parts,
colors, castes, genders, directions, deities, friendship tables, aspect rules,
combustion degrees, exaltation/debilitation, own signs, karaka roles,
war between planets (Graha Yuddha), planetary periods (dasha years),
rising types (Sheershodaya/Prishtodaya/Ubhayodaya).

Total: ~100 rules (GCH001–GCH100)
All: implemented=False
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_CHARACTERISTICS_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # SUN (SURYA) — BPHS Ch.3
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH001", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun (Surya) — Nature: Sattvik (pure/spiritual). Element: Fire (Agni). "
            "Dosha: Pitta (heat/bile). Body: bones, heart, eyes (right eye for male, left for female). "
            "Color: deep red/copper. Caste: Kshatriya (warrior). Gender: Male. "
            "Direction: East. Deity: Shiva/Agni. Season: Grishma (summer, June-July).",
        confidence=0.95, verse="BPHS Ch.3 v.1-6",
        tags=["graha_nature", "sun", "sattvik", "fire", "pitta", "bones", "kshatriya", "east"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH002", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun — Karakatva (significator roles): Soul (Atmakaraka), father, authority, "
            "government, royalty, physician/Vaidya, forests, temples, east direction. "
            "Indicates: dignity, pride, ambition, fame, willpower, leadership, political power.",
        confidence=0.95, verse="BPHS Ch.3 v.7-12",
        tags=["graha_nature", "sun", "karaka", "father", "authority", "government", "soul", "royalty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH003", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun — Astronomical: Exaltation at 10° Aries; Debilitation at 10° Libra. "
            "Own sign: Leo. Mooltrikona: 0-20° Leo. "
            "Combustion limit: planets within 6° (Moon 12°, Mars 17°, Mercury 14°, Jupiter 11°, "
            "Venus 10°, Saturn 15°) of Sun are combust (asta).",
        confidence=0.95, verse="BPHS Ch.3 v.13-18",
        tags=["graha_nature", "sun", "exaltation_aries", "debilitation_libra", "leo", "combustion"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH004", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun — Friendships: Natural friends: Moon, Mars, Jupiter. "
            "Natural enemies: Venus, Saturn. Neutral: Mercury. "
            "Temporal friendship adds to natural for combined result. "
            "Planet in own/friend sign = good results; enemy sign = difficult.",
        confidence=0.95, verse="BPHS Ch.3 v.19-24",
        tags=["graha_nature", "sun", "friends_moon_mars_jupiter", "enemies_venus_saturn", "neutral_mercury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH005", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun — Aspect: Sun casts full aspect (100%) on 7th house from its position. "
            "No special aspects (unlike Mars/Jupiter/Saturn). "
            "Sun's aspect signifies illumination, authority, and government influence "
            "on aspected house/planet.",
        confidence=0.93, verse="BPHS Ch.3 v.25-28",
        tags=["graha_nature", "sun", "7th_aspect", "full_aspect", "illumination"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MOON (CHANDRA) — BPHS Ch.4
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH006", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon (Chandra) — Nature: Sattvik. Element: Water (Jal). Dosha: Vata/Kapha. "
            "Body: blood, mind, fluids, left eye (male), breasts, stomach. "
            "Color: white/cream. Caste: Vaishya (merchant). Gender: Female. "
            "Direction: Northwest. Deity: Varuna/Uma. Season: Varsha (monsoon).",
        confidence=0.95, verse="BPHS Ch.4 v.1-6",
        tags=["graha_nature", "moon", "sattvik", "water", "vata_kapha", "blood", "mind", "white", "female"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH007", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon — Karakatva: Mind (Manokaraka), mother, public, emotions, "
            "liquids/water, agriculture, silver, pearls, night, travel by water. "
            "Fluctuation, adaptability, nurturing, memory, imagination.",
        confidence=0.95, verse="BPHS Ch.4 v.7-12",
        tags=["graha_nature", "moon", "karaka", "mother", "mind", "public", "water", "silver", "night"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH008", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon — Astronomical: Exaltation at 3° Taurus; Debilitation at 3° Scorpio. "
            "Own sign: Cancer. Mooltrikona: 3-30° Taurus. "
            "Waxing Moon (Shukla Paksha, 8th tithi onward) = benefic/strong. "
            "Waning Moon (Krishna Paksha) = malefic/weak. New Moon most malefic.",
        confidence=0.95, verse="BPHS Ch.4 v.13-18",
        tags=["graha_nature", "moon", "exaltation_taurus", "debilitation_scorpio", "cancer", "waxing_strong"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH009", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon — Friendships: Natural friends: Sun, Mercury. "
            "Natural enemies: none (BPHS: Moon has no enemies). Neutral: Mars, Jupiter, Venus, Saturn. "
            "Moon receives others' enmity but projects none — symbolizes the receptive mind.",
        confidence=0.93, verse="BPHS Ch.4 v.19-24",
        tags=["graha_nature", "moon", "friends_sun_mercury", "no_enemies", "receptive"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MARS (MANGAL/KUJA) — BPHS Ch.5
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH010", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars (Mangal/Kuja) — Nature: Tamasik (inertia/activity). Element: Fire (Agni). "
            "Dosha: Pitta (high). Body: blood, bone marrow, muscles, south direction. "
            "Color: blood red. Caste: Kshatriya. Gender: Male. "
            "Direction: South. Deity: Skanda (Kartikeya). Season: Grishma/Sharad.",
        confidence=0.95, verse="BPHS Ch.5 v.1-6",
        tags=["graha_nature", "mars", "tamasik", "fire", "pitta_high", "blood", "kshatriya", "south"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH011", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars — Karakatva: Younger siblings (Bhratrukaraka), courage, energy, "
            "real estate/land, weapons, surgery, engineering, military, police, fire, "
            "accidents, disputes, passion, aggression, physical strength.",
        confidence=0.95, verse="BPHS Ch.5 v.7-12",
        tags=["graha_nature", "mars", "karaka", "younger_siblings", "courage", "land", "military", "surgery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH012", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars — Astronomical: Exaltation at 28° Capricorn; Debilitation at 28° Cancer. "
            "Own signs: Aries, Scorpio. Mooltrikona: 0-12° Aries. "
            "Special aspects: Mars aspects 4th, 7th, and 8th from its position (full strength). "
            "Retrograde Mars: increased intensity in matters signified.",
        confidence=0.95, verse="BPHS Ch.5 v.13-18",
        tags=["graha_nature", "mars", "exaltation_capricorn", "debilitation_cancer", "aries_scorpio",
              "4th_7th_8th_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH013", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars — Friendships: Natural friends: Sun, Moon, Jupiter. "
            "Natural enemies: Mercury. Neutral: Venus, Saturn. "
            "Mars-Mercury enmity: logic (Mercury) conflicts with impulsive action (Mars). "
            "Mars-Venus neutral: passion and beauty coexist.",
        confidence=0.93, verse="BPHS Ch.5 v.19-24",
        tags=["graha_nature", "mars", "friends_sun_moon_jupiter", "enemy_mercury", "neutral_venus_saturn"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # MERCURY (BUDHA) — BPHS Ch.6
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH014", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury (Budha) — Nature: Rajasik (activity/passion). Element: Earth (Prithvi). "
            "Dosha: Tridosha (all three — adapts to planets joined). "
            "Body: skin, nervous system, tongue, speech organs, lungs. "
            "Color: green. Caste: Shudra/Vaishya. Gender: Neuter/Hermaphrodite. "
            "Direction: North. Deity: Vishnu. Season: Sharad (autumn).",
        confidence=0.95, verse="BPHS Ch.6 v.1-6",
        tags=["graha_nature", "mercury", "rajasik", "earth", "tridosha", "nervous_system", "green", "north"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH015", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury — Karakatva: Intelligence (Buddhikaraka), speech, communication, "
            "trade/commerce, writing, mathematics, education, astrology, younger siblings (secondary), "
            "skin, adaptability, wit, analysis.",
        confidence=0.95, verse="BPHS Ch.6 v.7-12",
        tags=["graha_nature", "mercury", "karaka", "intelligence", "speech", "trade", "writing", "mathematics"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH016", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury — Astronomical: Exaltation at 15° Virgo; Debilitation at 15° Pisces. "
            "Own signs: Gemini, Virgo. Mooltrikona: 15-20° Virgo. "
            "Mercury combust within 14° of Sun loses all strength. "
            "Mercury retrograde: inner thought processes intensified; communication errors.",
        confidence=0.95, verse="BPHS Ch.6 v.13-18",
        tags=["graha_nature", "mercury", "exaltation_virgo", "debilitation_pisces", "gemini_virgo", "combust_14"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH017", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury — Friendships: Natural friends: Sun, Venus. "
            "Natural enemies: Moon. Neutral: Mars, Jupiter, Saturn. "
            "Mercury-Moon tension: rational mind vs. emotional mind conflict. "
            "Mercury inherits nature of planets it conjoins.",
        confidence=0.93, verse="BPHS Ch.6 v.19-24",
        tags=["graha_nature", "mercury", "friends_sun_venus", "enemy_moon", "adapts_conjunctions"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # JUPITER (GURU/BRIHASPATI) — BPHS Ch.7
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH018", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter (Guru/Brihaspati) — Nature: Sattvik. Element: Ether/Space (Akasha). "
            "Dosha: Kapha (phlegm/expansion). Body: liver, fat tissue, hips, thighs. "
            "Color: yellow/gold. Caste: Brahmin (priest/teacher). Gender: Male. "
            "Direction: Northeast. Deity: Indra/Brahma. Season: Hemanta (winter).",
        confidence=0.95, verse="BPHS Ch.7 v.1-6",
        tags=["graha_nature", "jupiter", "sattvik", "ether", "kapha", "liver", "brahmin", "northeast", "yellow"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH019", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter — Karakatva: Children (Putrakaraka), wealth (Dhanakaraka), "
            "guru/teacher, wisdom, religion, law, husband (in female chart), "
            "gold, abundance, long journeys, higher education, philosophy, scripture.",
        confidence=0.95, verse="BPHS Ch.7 v.7-12",
        tags=["graha_nature", "jupiter", "karaka", "children", "wealth", "guru", "wisdom", "religion", "law"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH020", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter — Astronomical: Exaltation at 5° Cancer; Debilitation at 5° Capricorn. "
            "Own signs: Sagittarius, Pisces. Mooltrikona: 0-10° Sagittarius. "
            "Special aspects: Jupiter aspects 5th, 7th, and 9th from its position. "
            "Greatest benefic — pure aspect purifies afflicted houses.",
        confidence=0.95, verse="BPHS Ch.7 v.13-18",
        tags=["graha_nature", "jupiter", "exaltation_cancer", "debilitation_capricorn",
              "sagittarius_pisces", "5th_7th_9th_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH021", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter — Friendships: Natural friends: Sun, Moon, Mars. "
            "Natural enemies: Mercury, Venus. Neutral: Saturn. "
            "Jupiter-Mercury tension: wisdom vs. analytical cleverness. "
            "Jupiter-Venus tension: dharma (Jupiter) vs. kama/desire (Venus).",
        confidence=0.93, verse="BPHS Ch.7 v.19-24",
        tags=["graha_nature", "jupiter", "friends_sun_moon_mars", "enemies_mercury_venus", "neutral_saturn"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # VENUS (SHUKRA) — BPHS Ch.8
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH022", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus (Shukra) — Nature: Rajasik. Element: Water (Jal). "
            "Dosha: Kapha/Vata. Body: reproductive organs, kidneys, face/beauty, semen/ovum. "
            "Color: white/multi-colored. Caste: Brahmin. Gender: Female. "
            "Direction: Southeast. Deity: Lakshmi/Indra. Season: Vasanta (spring).",
        confidence=0.95, verse="BPHS Ch.8 v.1-6",
        tags=["graha_nature", "venus", "rajasik", "water", "kapha", "beauty", "brahmin", "southeast", "white"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH023", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus — Karakatva: Wife/spouse (Kalatrakaraka), vehicles (Vahanakaraka), "
            "luxury, art, music, dance, beauty, sexual pleasure, comforts, "
            "diamonds, jewelry, fine food, theatre, entertainment.",
        confidence=0.95, verse="BPHS Ch.8 v.7-12",
        tags=["graha_nature", "venus", "karaka", "spouse", "vehicles", "luxury", "art", "music", "beauty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH024", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus — Astronomical: Exaltation at 27° Pisces; Debilitation at 27° Virgo. "
            "Own signs: Taurus, Libra. Mooltrikona: 0-15° Libra. "
            "Special aspects: Venus aspects 7th from its position (full). "
            "Venus retrograde: intensified desires, re-evaluation of relationships.",
        confidence=0.95, verse="BPHS Ch.8 v.13-18",
        tags=["graha_nature", "venus", "exaltation_pisces", "debilitation_virgo", "taurus_libra", "7th_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH025", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus — Friendships: Natural friends: Mercury, Saturn. "
            "Natural enemies: Sun, Moon. Neutral: Mars, Jupiter. "
            "Venus-Sun enmity: beauty (Venus) conflicts with authority (Sun). "
            "Venus-Saturn friendship: pleasure principle aligned with karma.",
        confidence=0.93, verse="BPHS Ch.8 v.19-24",
        tags=["graha_nature", "venus", "friends_mercury_saturn", "enemies_sun_moon", "neutral_mars_jupiter"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SATURN (SHANI) — BPHS Ch.9
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH026", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn (Shani) — Nature: Tamasik. Element: Air (Vayu). "
            "Dosha: Vata (air/dryness). Body: teeth, hair, nails, nerves, spleen, bones (long). "
            "Color: black/dark blue. Caste: Shudra (laborer). Gender: Neuter/Male. "
            "Direction: West. Deity: Yama/Brahma (as time). Season: Shishira (late winter).",
        confidence=0.95, verse="BPHS Ch.9 v.1-6",
        tags=["graha_nature", "saturn", "tamasik", "air", "vata", "bones_nerves", "shudra", "west", "black"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH027", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn — Karakatva: Longevity (Ayukaraka), karma, service, discipline, "
            "elderly people, servants/workers, iron, coal, oil, agriculture (labor aspect), "
            "chronic disease, delays, restrictions, wisdom through suffering.",
        confidence=0.95, verse="BPHS Ch.9 v.7-12",
        tags=["graha_nature", "saturn", "karaka", "longevity", "karma", "service", "elderly", "iron", "discipline"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH028", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn — Astronomical: Exaltation at 20° Libra; Debilitation at 20° Aries. "
            "Own signs: Capricorn, Aquarius. Mooltrikona: 0-20° Aquarius. "
            "Special aspects: Saturn aspects 3rd, 7th, and 10th from its position. "
            "Saturn retrograde: karmic delays intensified; inner discipline emphasized.",
        confidence=0.95, verse="BPHS Ch.9 v.13-18",
        tags=["graha_nature", "saturn", "exaltation_libra", "debilitation_aries",
              "capricorn_aquarius", "3rd_7th_10th_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH029", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn — Friendships: Natural friends: Mercury, Venus. "
            "Natural enemies: Sun, Moon, Mars. Neutral: Jupiter. "
            "Saturn-Sun: discipline vs. authority. Saturn-Mars: slowness vs. speed. "
            "Saturn-Mercury-Venus alliance: practical, commercial, analytical cluster.",
        confidence=0.93, verse="BPHS Ch.9 v.19-24",
        tags=["graha_nature", "saturn", "friends_mercury_venus", "enemies_sun_moon_mars", "neutral_jupiter"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # RAHU & KETU — BPHS Ch.10
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH030", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Rahu — Nature: Tamasik. Element: Air/Ether (mixed). "
            "Body: the head (severed from Svarbhanu). Color: smoky/dark. "
            "Caste: outcaste/Chandala. Gender: Neuter. "
            "Direction: Southwest. Deity: Durga/Sarpa (serpent). "
            "Rahu amplifies and distorts the qualities of the house/sign it occupies.",
        confidence=0.93, verse="BPHS Ch.10 v.1-6",
        tags=["graha_nature", "rahu", "tamasik", "shadow_planet", "amplifier", "southwest", "smoky"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH031", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Rahu — Karakatva: Foreign/unusual things, outcaste people, paternal grandfather, "
            "poisons, epidemics, sudden events, ambition, worldly desires, "
            "electronics/technology, foreign lands, unconventional paths.",
        confidence=0.90, verse="BPHS Ch.10 v.7-12",
        tags=["graha_nature", "rahu", "karaka", "foreign", "paternal_grandfather", "sudden", "technology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH032", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Rahu — Astronomical: Rahu has no own sign, exaltation, or debilitation in BPHS. "
            "Behaves like Saturn in most contexts; some authorities give Rahu exaltation in Taurus/Gemini. "
            "Always retrograde; moves backward through zodiac ~18 months per sign. "
            "Rahu in 6th/10th/11th = excellent (Upachaya) for material gains.",
        confidence=0.88, verse="BPHS Ch.10 v.13-18",
        tags=["graha_nature", "rahu", "always_retrograde", "behaves_saturn", "upachaya_6_10_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH033", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Ketu — Nature: Tamasik/Sattvik (spiritual in higher expression). "
            "Body: the tail (Svarbhanu's body). Color: piebald/multicolor. "
            "Direction: Southeast. Deity: Ganesha/Chitragupta. "
            "Ketu detaches from house significations — gives liberation or loss depending on context.",
        confidence=0.93, verse="BPHS Ch.10 v.19-24",
        tags=["graha_nature", "ketu", "tamasik_sattvik", "shadow_planet", "detachment", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH034", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Ketu — Karakatva: Maternal grandfather, moksha/liberation, psychic abilities, "
            "past-life accumulated karma, occult, spirituality, isolation, surgeries, "
            "mystical experiences, Vedic knowledge, sudden losses.",
        confidence=0.90, verse="BPHS Ch.10 v.25-30",
        tags=["graha_nature", "ketu", "karaka", "maternal_grandfather", "moksha", "psychic", "past_life"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PLANETARY ASPECTS (DRISHTI) — BPHS Ch.26
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH035", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_nature",
        description="Planetary Aspects (Graha Drishti): All planets aspect 7th house from position (full/100%). "
            "Special aspects: Saturn aspects 3rd and 10th (75% strength). "
            "Jupiter aspects 5th and 9th (100% strength). "
            "Mars aspects 4th and 8th (100% strength). "
            "Aspect strength: 25%/50%/75%/100% depending on house distance.",
        confidence=0.95, verse="BPHS Ch.26 v.1-8",
        tags=["aspects", "graha_drishti", "special_aspects", "saturn_3_10", "jupiter_5_9", "mars_4_8"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH036", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_nature",
        description="Aspect Strength Gradation: "
            "3rd and 10th from planet: 25% (weak) aspect. "
            "5th and 9th from planet: 50% (medium) aspect. "
            "4th and 8th from planet: 75% (3/4) aspect. "
            "7th from planet: 100% (full) aspect. "
            "Special planet aspects override these for their designated houses.",
        confidence=0.95, verse="BPHS Ch.26 v.9-14",
        tags=["aspects", "aspect_strength", "grading", "25_50_75_100", "full_aspect_7th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH037", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_nature",
        description="Benefic vs Malefic Aspect: Jupiter's aspect purifies any house — "
            "benefic aspect enhances positive significations. "
            "Saturn's aspect on a house causes delays and obstacles. "
            "Mars's aspect creates energy/conflict in aspected house. "
            "Aspect of own lord strengthens a house's results.",
        confidence=0.92, verse="BPHS Ch.26 v.15-20",
        tags=["aspects", "benefic_aspect_jupiter", "malefic_aspect_saturn_mars", "own_lord_aspect"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PLANETARY COMBUSTION (ASTA) — BPHS Ch.27
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH038", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_nature",
        description="Combustion (Asta) Degrees — Planet within these degrees of Sun loses strength: "
            "Moon: 12° (ordinary), 8° (deep); Mars: 17°; Mercury: 14° (direct), 12° (retrograde); "
            "Jupiter: 11°; Venus: 10° (direct), 8° (retrograde); Saturn: 15°. "
            "Combust planet loses 100% natural significations in that area.",
        confidence=0.95, verse="BPHS Ch.27 v.1-8",
        tags=["combustion", "asta", "degrees", "moon_12", "mars_17", "mercury_14", "saturn_15"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH039", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_nature",
        description="Effect of Combustion: Combust planet behaves as if in debilitation — "
            "its natural significations are suppressed. "
            "Combust planet cannot give full dasha results independently. "
            "Exception: planet in own sign when combust retains 25-50% strength.",
        confidence=0.92, verse="BPHS Ch.27 v.9-14",
        tags=["combustion", "effect_asta", "suppressed_signification", "dasha_weakness"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PLANETARY WAR (GRAHA YUDDHA) — BPHS Ch.28
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH040", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_nature",
        description="Graha Yuddha (Planetary War): When two planets (except Sun/Moon/Rahu/Ketu) "
            "are within 1° of each other, they are at war. "
            "The planet with higher celestial latitude wins the war. "
            "The losing planet loses its strength and gives inauspicious results.",
        confidence=0.90, verse="BPHS Ch.28 v.1-6",
        tags=["graha_yuddha", "planetary_war", "1_degree", "latitude_winner", "loser_weakened"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH041", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_nature",
        description="Graha Yuddha — Winner Determination: "
            "Planet with greater northern latitude wins. "
            "When latitudes equal, brighter planet wins. "
            "Winner gains the house/sign advantages; loser loses. "
            "Mars wins over Mercury (usually); Jupiter often wins due to size.",
        confidence=0.88, verse="BPHS Ch.28 v.7-12",
        tags=["graha_yuddha", "winner_north_latitude", "brightness", "loser_loses_signification"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # RISING TYPES (UDAYA LAGNA CLASSIFICATION) — BPHS Ch.25
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH042", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_nature",
        description="Sheershodaya Signs (Rise head-first): Gemini, Leo, Virgo, Libra, Scorpio, Aquarius. "
            "Planets in these signs or lagna being these signs = results manifest early in dasha/period. "
            "Effects are direct, clear, and front-loaded.",
        confidence=0.90, verse="BPHS Ch.25 v.1-6",
        tags=["rising_type", "sheershodaya", "early_results", "gemini_leo_virgo_libra_scorpio_aquarius"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH043", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_nature",
        description="Prishtodaya Signs (Rise tail-first): Aries, Taurus, Cancer, Sagittarius, Capricorn. "
            "Planets here give results late in dasha. Effects are back-loaded and delayed. "
            "Slow start but potential for late-life results.",
        confidence=0.90, verse="BPHS Ch.25 v.7-12",
        tags=["rising_type", "prishtodaya", "late_results", "aries_taurus_cancer_sagittarius_capricorn"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH044", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_nature",
        description="Ubhayodaya Sign (Rise both ways): Pisces rises both ways. "
            "Results manifest both early and late in dasha/period. "
            "Dual-timing effects; some immediate, some delayed. "
            "Most complex timing of all rising types.",
        confidence=0.88, verse="BPHS Ch.25 v.13-16",
        tags=["rising_type", "ubhayodaya", "dual_timing", "pisces", "early_and_late"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # VIMSHOTTARI DASHA PERIODS — BPHS Ch.46
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH045", source="BPHS", chapter="Ch.46", school="parashari",
        category="graha_nature",
        description="Vimshottari Dasha Period Allocation (120-year total): "
            "Sun=6yrs, Moon=10yrs, Mars=7yrs, Rahu=18yrs, Jupiter=16yrs, "
            "Saturn=19yrs, Mercury=17yrs, Ketu=7yrs, Venus=20yrs. "
            "Sequence: Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury→Ketu→Venus→Sun (repeats).",
        confidence=0.98, verse="BPHS Ch.46 v.1-6",
        tags=["dasha", "vimshottari", "period_allocation", "sun_6", "moon_10", "venus_20", "saturn_19"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH046", source="BPHS", chapter="Ch.46", school="parashari",
        category="graha_nature",
        description="Vimshottari Nakshatra Sequence: Each nakshatra's lord determines birth dasha. "
            "Sequence from Ashwini: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury (repeats). "
            "Birth balance = (remaining degrees in birth nakshatra / total nakshatra span) × planet years.",
        confidence=0.98, verse="BPHS Ch.46 v.7-12",
        tags=["dasha", "vimshottari", "nakshatra_sequence", "birth_balance", "ashwini_ketu"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SIGN (RASHI) NATURES — BPHS Ch.4 (signs overview)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH047", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Rashi Modality: Movable (Chara) signs: Aries, Cancer, Libra, Capricorn — "
            "initiative, change, travel, beginnings. "
            "Fixed (Sthira) signs: Taurus, Leo, Scorpio, Aquarius — "
            "stability, endurance, accumulation. "
            "Dual (Dwiswabhava/Ubhaya) signs: Gemini, Virgo, Sagittarius, Pisces — "
            "versatility, transitions, both qualities.",
        confidence=0.95, verse="BPHS Ch.4 v.25-30",
        tags=["rashi", "modality", "chara_movable", "sthira_fixed", "dwiswabhava_dual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH048", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Rashi Elements: Fire (Agni) signs: Aries, Leo, Sagittarius — "
            "energy, ambition, enthusiasm, leadership. "
            "Earth (Prithvi) signs: Taurus, Virgo, Capricorn — "
            "practicality, materialism, endurance. "
            "Air (Vayu) signs: Gemini, Libra, Aquarius — "
            "communication, intelligence, social. "
            "Water (Jal) signs: Cancer, Scorpio, Pisces — "
            "emotion, intuition, sensitivity.",
        confidence=0.95, verse="BPHS Ch.4 v.31-36",
        tags=["rashi", "elements", "fire_aries_leo_sagittarius", "earth", "air", "water"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH049", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Rashi Gender: Male (odd) signs: Aries, Gemini, Leo, Libra, Sagittarius, Aquarius. "
            "Female (even) signs: Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces. "
            "Male lagna = Mahabhagya for male native born in day. "
            "Female lagna = Mahabhagya for female native born at night.",
        confidence=0.93, verse="BPHS Ch.4 v.37-40",
        tags=["rashi", "gender", "male_odd_signs", "female_even_signs", "mahabhagya_condition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH050", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Rashi Directions and Body Parts: Aries=head/east, Taurus=face/south, "
            "Gemini=arms/west, Cancer=chest/north, Leo=stomach/east, Virgo=intestines/south, "
            "Libra=hips/west, Scorpio=genitals/north, Sagittarius=thighs/east, "
            "Capricorn=knees/south, Aquarius=calves/west, Pisces=feet/north.",
        confidence=0.90, verse="BPHS Ch.4 v.41-46",
        tags=["rashi", "directions", "body_parts", "aries_head_east", "pisces_feet"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # NAKSHATRA (LUNAR MANSIONS) BASIC — BPHS Ch.5 (supplementary)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH051", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Nakshatra Trikonas (9-9-9 groups): "
            "Dharma group (Ketu-series): Ashwini, Magha, Moola — spiritual impulse, beginnings. "
            "Artha group (Venus-series): Bharani, Purva Phalguni, Purva Ashadha — wealth, sensuality. "
            "Kama group (Sun-series): Krittika, Uttara Phalguni, Uttara Ashadha — desire, ambition. "
            "Moksha group (Moon-series): Rohini, Hasta, Shravana — liberation, service.",
        confidence=0.88, verse="BPHS Ch.5 v.25-32",
        tags=["nakshatra", "trikonas", "dharma_artha_kama_moksha", "ashwini_magha_moola"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH052", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Nakshatra Ganas (Nature groups): "
            "Deva (divine/benefic): Ashwini, Mrigashira, Punarvasu, Pushya, Hasta, Swati, "
            "Anuradha, Shravana, Revati. "
            "Manushya (human/mixed): Bharani, Rohini, Ardra, Purva Phalguni, Uttara Phalguni, "
            "Purva Ashadha, Uttara Ashadha, Purva Bhadra, Uttara Bhadra. "
            "Rakshasa (demonic/malefic): Krittika, Ashlesha, Magha, Chitra, Vishakha, "
            "Jyeshtha, Moola, Dhanishtha, Shatabhisha.",
        confidence=0.88, verse="BPHS Ch.5 v.33-40",
        tags=["nakshatra", "gana", "deva_divine", "manushya_human", "rakshasa_malefic"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # TEMPORAL FRIENDSHIPS (TATKALIKA MAITRI) — BPHS Ch.3 supplement
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH053", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Tatkalika Maitri (Temporal Friendship): A planet becomes temporary friend "
            "of all planets in houses 2/3/4/10/11/12 from it in the chart. "
            "Temporary enemy: planets in remaining houses (1/5/6/7/8/9). "
            "Combined friendship = Natural + Temporal: "
            "Friend+Friend=Best Friend; Friend+Enemy=Neutral; "
            "Neutral+Friend=Friend; Enemy+Enemy=Bitter Enemy.",
        confidence=0.93, verse="BPHS Ch.3 v.30-38",
        tags=["friendship", "tatkalika_maitri", "temporal_friend_2_3_4_10_11_12", "combined_friendship"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH054", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Planet in Friend/Enemy Sign Effect: "
            "Own sign: 100% strength (Swakshetra). "
            "Best friend sign: 75% strength. "
            "Friend sign: 50% strength. "
            "Neutral sign: 25% strength. "
            "Enemy sign: 12.5% (half strength, unfavorable). "
            "Bitter enemy sign: minimal/negative results.",
        confidence=0.90, verse="BPHS Ch.3 v.39-44",
        tags=["friendship", "sign_strength", "swakshetra_100", "friend_50", "enemy_weak"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SAPTAVARGA AND SIGN STRENGTHS — BPHS Ch.6 (extended)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH055", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Saptavarga Strength (7-divisional composite): "
            "Planet's strength from Rashi (D1), Hora (D2), Drekkana (D3), Saptamsha (D7), "
            "Navamsha (D9), Dwadamsha (D12), Trimshamsha (D30) combined. "
            "Parijatamsha: 1 varga dignity = weak. Uttamamsha: 5 dignities = very strong. "
            "Gopuramsha: 2 dignities. Simhasanamsha: 3. Paravatamsha: 4. Devalokamsha: 6. "
            "Brahmalokamsha: 7 dignities = maximum strength.",
        confidence=0.90, verse="BPHS Ch.6 v.25-34",
        tags=["varga_strength", "saptavarga", "parijatamsha", "gopuramsha", "brahmalokamsha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH056", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Vargottama (Same sign in Rashi and Navamsha): Planet in same sign in D1 and D9 "
            "gains extra strength equivalent to being in own sign. "
            "Vargottama lagna: native has exceptional constitution and luck. "
            "Vargottama Moon: stable, fortunate mind. "
            "Vargottama benefic: maximum benefic results in that house.",
        confidence=0.93, verse="BPHS Ch.6 v.35-40",
        tags=["varga_strength", "vargottama", "d1_d9_same", "extra_strength", "lagna_vargottama"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SPECIAL PLANETARY STATES — BPHS Ch.27-29
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH057", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_nature",
        description="Retrograde (Vakra) Planet: A retrograde planet gains extra strength (1.5× normal). "
            "Retrograde planet in debilitation = debilitation cancelled (acts as if exalted). "
            "Retrograde planet in exaltation = some loss of exaltation strength. "
            "Retrograde planet's dasha gives complex results — first half difficult, second half better.",
        confidence=0.90, verse="BPHS Ch.27 v.15-22",
        tags=["retrograde", "vakra", "extra_strength", "debilitation_cancelled", "complex_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH058", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_nature",
        description="Stationary (Sthambhita) Planet: Planet moving very slowly (just before/after retrograde station). "
            "Extremely powerful — all significations intensely focused. "
            "Stationary malefic: intense affliction. Stationary benefic: intense grace. "
            "Station period lasts 2-7 days.",
        confidence=0.87, verse="BPHS Ch.28 v.13-18",
        tags=["stationary", "sthambhita", "intense_focused", "station_powerful"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH059", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_nature",
        description="Exaltation vs Debilitation Gradation: "
            "Deep exaltation degree = maximum strength (100%). "
            "Moving away from exaltation degree toward debilitation: linearly decreasing strength. "
            "Deep debilitation degree = minimum/negative strength. "
            "Strength is maximum at exact exaltation degree.",
        confidence=0.90, verse="BPHS Ch.29 v.1-8",
        tags=["dignity", "exaltation_gradation", "debilitation_gradation", "degree_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH060", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_nature",
        description="Mooltrikona vs Own Sign: Mooltrikona gives slightly more strength than other own sign. "
            "Sun: Leo 0-20° mooltrikona (strongest), 20-30° just own. "
            "Moon: Taurus 3-30° mooltrikona, Cancer own. "
            "Planet in mooltrikona acts as if in 'highest own expression' in that sector of degrees.",
        confidence=0.90, verse="BPHS Ch.29 v.9-16",
        tags=["dignity", "mooltrikona", "own_sign", "degree_sector", "highest_expression"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # PLANET-SIGN BODY PART MEDICAL ASTROLOGY — BPHS Ch.30
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH061", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Sun Medical Rulership: Head, heart, eyes (right), spine, bones, vitality. "
            "Sun afflicted = fever, heart disease, eye disease, loss of vitality, alopecia. "
            "Sun in 6th/8th/12th with malefic = chronic ailments in Sun's body areas.",
        confidence=0.88, verse="BPHS Ch.30 v.1-6",
        tags=["medical_astrology", "sun_body", "heart", "eyes_right", "spine", "fever"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH062", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Moon Medical Rulership: Blood, bodily fluids, mind, breasts, lungs, left eye. "
            "Moon afflicted = mental disorders, anemia, blood impurities, lung issues, "
            "emotional instability, women's health issues.",
        confidence=0.88, verse="BPHS Ch.30 v.7-12",
        tags=["medical_astrology", "moon_body", "blood", "mind", "lungs", "left_eye", "mental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH063", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Mars Medical Rulership: Blood (circulation), bone marrow, muscles, bile (pitta). "
            "Mars afflicted = injuries, accidents, inflammation, hemorrhage, fever, "
            "accidents with sharp objects, bile disorders.",
        confidence=0.88, verse="BPHS Ch.30 v.13-18",
        tags=["medical_astrology", "mars_body", "bone_marrow", "muscles", "inflammation", "accidents"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH064", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Mercury Medical Rulership: Nervous system, skin, tongue, speech, lungs (secondary). "
            "Mercury afflicted = nervous disorders, skin diseases, speech problems, "
            "anxiety from mental overactivity.",
        confidence=0.88, verse="BPHS Ch.30 v.19-24",
        tags=["medical_astrology", "mercury_body", "nervous_system", "skin", "speech", "anxiety"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH065", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Jupiter Medical Rulership: Liver, fat tissue, hips, thighs, arteries. "
            "Jupiter afflicted = liver disorders, obesity, over-expansion issues, "
            "diabetes (sugar excess), jaundice.",
        confidence=0.88, verse="BPHS Ch.30 v.25-30",
        tags=["medical_astrology", "jupiter_body", "liver", "fat", "hips", "diabetes", "obesity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH066", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Venus Medical Rulership: Reproductive organs, kidneys, semen/ovum, face/skin glow. "
            "Venus afflicted = sexual disorders, kidney disease, venereal disease, "
            "diabetes (kapha type), skin dullness.",
        confidence=0.88, verse="BPHS Ch.30 v.31-36",
        tags=["medical_astrology", "venus_body", "reproductive", "kidneys", "sexual_disorders"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH067", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Saturn Medical Rulership: Bones (long), teeth, nails, hair, spleen, nerves, "
            "joints (chronic), vata disorders. "
            "Saturn afflicted = arthritis, paralysis, chronic illness, hair loss, "
            "dental problems, nerve pain.",
        confidence=0.88, verse="BPHS Ch.30 v.37-42",
        tags=["medical_astrology", "saturn_body", "bones", "joints", "arthritis", "paralysis", "vata"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH068", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_nature",
        description="Rahu/Ketu Medical Rulership: "
            "Rahu = poisoning, unusual diseases, skin diseases, undiagnosed conditions, "
            "epidemics, phobias. "
            "Ketu = mysterious ailments, surgical complications, sudden illness, "
            "moksha-related renunciation of health.",
        confidence=0.85, verse="BPHS Ch.30 v.43-48",
        tags=["medical_astrology", "rahu_ketu_body", "poisoning", "undiagnosed", "mysterious_illness"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # NATURAL KARAKATVA COMPLETE TABLE — BPHS Ch.32
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH069", source="BPHS", chapter="Ch.32", school="parashari",
        category="graha_nature",
        description="Naisargika Karaka (Natural Significators) — Complete House Mapping: "
            "1st: Sun (soul/body). 2nd: Jupiter (wealth), Mercury (speech). "
            "3rd: Mars (siblings/courage). 4th: Moon (mother/happiness), Mercury (education), "
            "Mars (property), Venus (vehicles). 5th: Jupiter (children/wisdom). "
            "6th: Mars (enemies), Saturn (service).",
        confidence=0.95, verse="BPHS Ch.32 v.1-8",
        tags=["karaka", "naisargika", "natural_significator", "house_karaka_1_6"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH070", source="BPHS", chapter="Ch.32", school="parashari",
        category="graha_nature",
        description="Naisargika Karaka — Houses 7-12: "
            "7th: Venus (wife/desire), Jupiter (husband). 8th: Saturn (longevity), Mars (surgery). "
            "9th: Jupiter (dharma/fortune), Sun (father). 10th: Sun (authority), Saturn (karma), "
            "Jupiter (management), Mercury (trade). 11th: Jupiter (gains). 12th: Saturn (loss), "
            "Venus (bed/pleasure), Ketu (moksha).",
        confidence=0.95, verse="BPHS Ch.32 v.9-16",
        tags=["karaka", "naisargika", "natural_significator", "house_karaka_7_12"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # GRAHA STRENGTHS SUMMARY — BPHS Ch.33-34
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH071", source="BPHS", chapter="Ch.33", school="parashari",
        category="graha_nature",
        description="Natural Strength Order (Naisargika Bala): "
            "Sun (60) > Moon (51.43) > Venus (45) > Jupiter (34.29) > "
            "Mercury (25.71) > Mars (17.14) > Saturn (8.57). "
            "This is the inherent brightness/power order. "
            "Used in Shadbala calculations as one of the six strength components.",
        confidence=0.95, verse="BPHS Ch.33 v.1-6",
        tags=["strength", "naisargika_bala", "sun_60", "saturn_8.57", "natural_strength_order"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH072", source="BPHS", chapter="Ch.33", school="parashari",
        category="graha_nature",
        description="Planetary Day Rulership: "
            "Sunday=Sun, Monday=Moon, Tuesday=Mars, Wednesday=Mercury, "
            "Thursday=Jupiter, Friday=Venus, Saturday=Saturn. "
            "A planet is stronger on its own day (Vara Bala in Shadbala = 45 shashtiamshas). "
            "Chart born on planet's day = that planet is temporally strengthened.",
        confidence=0.95, verse="BPHS Ch.33 v.7-12",
        tags=["strength", "vara_bala", "day_ruler", "sunday_sun", "saturday_saturn", "shadbala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH073", source="BPHS", chapter="Ch.33", school="parashari",
        category="graha_nature",
        description="Day/Night Strength (Kala Bala): "
            "Sun, Jupiter, Venus stronger during day. "
            "Moon, Mars, Saturn stronger at night. "
            "Mercury strong both day and night. "
            "Chart born during day = Sun/Jupiter/Venus temporally boosted. "
            "Night birth = Moon/Mars/Saturn boosted.",
        confidence=0.93, verse="BPHS Ch.33 v.13-18",
        tags=["strength", "kala_bala", "day_strong_sun_jupiter_venus", "night_strong_moon_mars_saturn"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH074", source="BPHS", chapter="Ch.33", school="parashari",
        category="graha_nature",
        description="Paksha Bala (Lunar Phase Strength): "
            "Waxing Moon (Shukla Paksha): benefics gain strength day by day from new to full moon. "
            "Waning Moon (Krishna Paksha): malefics gain strength. "
            "Full Moon = maximum Moon strength. New Moon = minimum Moon, maximum malefic.",
        confidence=0.93, verse="BPHS Ch.33 v.19-24",
        tags=["strength", "paksha_bala", "waxing_benefics", "waning_malefics", "full_moon_strong"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH075", source="BPHS", chapter="Ch.34", school="parashari",
        category="graha_nature",
        description="Hora Bala (Hourly Strength): Each planetary hour (Hora) is ruled by a planet. "
            "Sequence from sunrise on each day of week follows planetary day-lord sequence. "
            "Planet ruling the birth hora gains 60 Hora Bala (full strength in Kala Bala). "
            "This is one component of Kala Bala within Shadbala.",
        confidence=0.90, verse="BPHS Ch.34 v.1-6",
        tags=["strength", "hora_bala", "planetary_hour", "birth_hora", "kala_bala_component"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL PLANET CHARACTERISTICS (GCH076–100) ─────────────────────────
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="GCH076", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun — Physical Description of Native: Person with strong Sun has: "
            "honey-colored or reddish eyes, spare body, bilious temperament, "
            "dignified bearing, fine tawny hair, tendency to be proud. "
            "Magnetic personality; tends to command attention.",
        confidence=0.85, verse="BPHS Ch.3 v.29-34",
        tags=["graha_nature", "sun", "physical_description", "reddish_eyes", "dignified", "proud"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH077", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon — Physical Description: Round body, very white, gentle, charming eyes, "
            "phlegmatic and windy constitution, curly hair, fond of water. "
            "Emotional sensitivity visible in face; receptive expression.",
        confidence=0.85, verse="BPHS Ch.4 v.43-48",
        tags=["graha_nature", "moon", "physical_description", "round_body", "white", "charming_eyes"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH078", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars — Physical Description: Blood-red eyes, fickle mind, young appearance, "
            "liberal, bilious, strong and cruel. Sharp, angular features; "
            "athletic build; commanding presence.",
        confidence=0.85, verse="BPHS Ch.5 v.27-32",
        tags=["graha_nature", "mars", "physical_description", "blood_red_eyes", "athletic", "strong"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH079", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury — Physical Description: Greenish-tinged complexion, sharp intellect, "
            "fond of humor, tridoshic constitution, agile build. "
            "Expressive hands and eyes; witty manner.",
        confidence=0.85, verse="BPHS Ch.6 v.27-32",
        tags=["graha_nature", "mercury", "physical_description", "green_complexion", "agile", "witty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH080", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter — Physical Description: Large body, yellowish tinge, phlegmatic, "
            "intelligent, broad chest, scholar. Commanding yet gentle presence; "
            "tendency toward weight gain in later life.",
        confidence=0.85, verse="BPHS Ch.7 v.27-32",
        tags=["graha_nature", "jupiter", "physical_description", "large_body", "yellow", "scholar"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH081", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus — Physical Description: Beautiful form, charming eyes, curly hair, "
            "charming personality, poet/artist sensibility, kapha constitution. "
            "Attractive face; magnetic to opposite sex.",
        confidence=0.85, verse="BPHS Ch.8 v.27-32",
        tags=["graha_nature", "venus", "physical_description", "beautiful", "charming_eyes", "curly_hair"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH082", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn — Physical Description: Emaciated body, coarse hair, lazy, limbs out of proportion, "
            "tawny/dark eyes, vata constitution. "
            "Often appears older than actual age; serious demeanor.",
        confidence=0.85, verse="BPHS Ch.9 v.27-32",
        tags=["graha_nature", "saturn", "physical_description", "emaciated", "dark_eyes", "serious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH083", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Sun Gems and Metals: Gem: Ruby (Manikya). Metal: Copper/Gold. "
            "Mantra: Aditya Hridayam, Gayatri. Day: Sunday. "
            "Recommended in Sun's dasha or to strengthen weak/afflicted Sun.",
        confidence=0.87, verse="BPHS Ch.3 v.35-38",
        tags=["graha_nature", "sun", "gem_ruby", "metal_copper", "mantra", "sunday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH084", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Moon Gems and Metals: Gem: Pearl (Moti). Metal: Silver. "
            "Mantra: Chandra Kavacham, Om Chandraya Namah. Day: Monday. "
            "Pearl recommended in Moon's dasha or for emotional/mental stability.",
        confidence=0.87, verse="BPHS Ch.4 v.49-52",
        tags=["graha_nature", "moon", "gem_pearl", "metal_silver", "mantra", "monday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH085", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Mars Gems and Metals: Gem: Red Coral (Moonga). Metal: Copper/Iron. "
            "Mantra: Mangala Kavacham. Day: Tuesday. "
            "Red coral in Mars dasha or for strengthening courage/physical energy.",
        confidence=0.87, verse="BPHS Ch.5 v.33-36",
        tags=["graha_nature", "mars", "gem_red_coral", "metal_copper_iron", "tuesday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH086", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Mercury Gems and Metals: Gem: Emerald (Panna). Metal: Mixed metals/Bronze. "
            "Mantra: Budha Stotram. Day: Wednesday. "
            "Emerald strengthens communication, intelligence, and business.",
        confidence=0.87, verse="BPHS Ch.6 v.33-36",
        tags=["graha_nature", "mercury", "gem_emerald", "metal_mixed", "wednesday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH087", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Jupiter Gems and Metals: Gem: Yellow Sapphire (Pukhraj). Metal: Gold. "
            "Mantra: Guru Stotram, Brihaspati Kavacham. Day: Thursday. "
            "Yellow sapphire enhances wisdom, fortune, and dharmic merit.",
        confidence=0.87, verse="BPHS Ch.7 v.33-36",
        tags=["graha_nature", "jupiter", "gem_yellow_sapphire", "metal_gold", "thursday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH088", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Venus Gems and Metals: Gem: Diamond (Heera) or White Sapphire. Metal: Silver/Platinum. "
            "Mantra: Shukra Kavacham. Day: Friday. "
            "Diamond enhances beauty, marriage, and creative arts.",
        confidence=0.87, verse="BPHS Ch.8 v.33-36",
        tags=["graha_nature", "venus", "gem_diamond", "metal_silver", "friday"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH089", source="BPHS", chapter="Ch.9", school="parashari",
        category="graha_nature",
        description="Saturn Gems and Metals: Gem: Blue Sapphire (Neelam). Metal: Iron/Lead. "
            "Mantra: Shani Kavacham, Shani Stotra. Day: Saturday. "
            "Blue sapphire only if Saturn is a yoga-karaka; otherwise very risky.",
        confidence=0.87, verse="BPHS Ch.9 v.33-36",
        tags=["graha_nature", "saturn", "gem_blue_sapphire", "metal_iron", "saturday", "risky_gem"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH090", source="BPHS", chapter="Ch.10", school="parashari",
        category="graha_nature",
        description="Rahu/Ketu Gems: Rahu: Hessonite (Gomed). Ketu: Cat's Eye (Lehsunia). "
            "Both extremely sensitive — only worn when planet is well-placed and a benefic for the lagna. "
            "Can cause sudden reversals if inappropriately worn.",
        confidence=0.85, verse="BPHS Ch.10 v.31-36",
        tags=["graha_nature", "rahu_ketu", "gem_hessonite_catseye", "sensitive_gems", "caution"],
        implemented=False,
    ),

    # ── PLANET COLOR, TASTE, DEITY COMPLETE TABLE (GCH091–095) ──────────────
    RuleRecord(
        rule_id="GCH091", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Planetary Tastes (Rasa): Sun=pungent/spicy, Moon=saline, Mars=bitter, "
            "Mercury=mixed, Jupiter=sweet, Venus=sour, Saturn=astringent. "
            "Planet's rasa indicates dietary connection and metabolic influence. "
            "Imbalanced planet = craving for its rasa.",
        confidence=0.85, verse="BPHS Ch.3 v.39-44",
        tags=["graha_nature", "tastes_rasa", "sun_pungent", "jupiter_sweet", "saturn_astringent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH092", source="BPHS", chapter="Ch.3", school="parashari",
        category="graha_nature",
        description="Planetary Deities (Devata) complete: Sun=Shiva/Agni, Moon=Varuna/Uma, "
            "Mars=Skanda/Murugan, Mercury=Vishnu, Jupiter=Indra/Brahma, "
            "Venus=Lakshmi/Indra, Saturn=Yama/Brahma. "
            "Propitiating the deity of an afflicted planet is the primary remedy.",
        confidence=0.87, verse="BPHS Ch.3 v.45-52",
        tags=["graha_nature", "deity", "sun_shiva", "moon_varuna", "saturn_yama", "propitiation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH093", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Planetary Abodes (Sthana): Sun=temples/forests, Moon=water bodies/fluid places, "
            "Mars=fire/kitchen/weapons, Mercury=parks/schools, Jupiter=treasuries/courts, "
            "Venus=bedrooms/pleasures, Saturn=cremation/garbage/dark places. "
            "Planet in relevant house = native frequents that type of location.",
        confidence=0.83, verse="BPHS Ch.4 v.53-58",
        tags=["graha_nature", "abode", "sun_temples", "saturn_cremation", "jupiter_treasury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH094", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Planetary Grains and Trees: Sun=wheat/bael, Moon=rice/jasmine, Mars=red lentils/khadira, "
            "Mercury=green mung/durva grass, Jupiter=chickpeas/peepal tree, "
            "Venus=sugar/white flowers, Saturn=black sesame/ashoka. "
            "Relevant in rituals and upayas (remedies).",
        confidence=0.82, verse="BPHS Ch.4 v.59-64",
        tags=["graha_nature", "grains_trees", "sun_wheat", "jupiter_peepal", "saturn_sesame"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH095", source="BPHS", chapter="Ch.4", school="parashari",
        category="graha_nature",
        description="Planetary Clothes and Colors for Propitiating: "
            "Sun=red cloth, Moon=white cloth, Mars=blood red, Mercury=green, "
            "Jupiter=yellow, Venus=variegated/multi-color, Saturn=black/blue. "
            "Wearing recommended colors on planetary days strengthens planet's benefic influence.",
        confidence=0.82, verse="BPHS Ch.4 v.65-70",
        tags=["graha_nature", "colors", "propitiating", "sun_red", "jupiter_yellow", "saturn_black"],
        implemented=False,
    ),

    # ── FINAL GRAHA CHARACTERISTIC RULES (GCH096–100) ───────────────────────
    RuleRecord(
        rule_id="GCH096", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Planetary Periods of Activity During Day: "
            "Sun strong during noon, Mars midmorning, Jupiter late morning. "
            "Moon strong during evening/night, Venus at dawn/dusk. "
            "Saturn strongest at night (midnight). Mercury strongest during morning hours.",
        confidence=0.82, verse="BPHS Ch.5 v.37-42",
        tags=["graha_nature", "time_of_strength", "sun_noon", "saturn_night", "venus_dawn"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH097", source="BPHS", chapter="Ch.5", school="parashari",
        category="graha_nature",
        description="Planetary Seasons of Strength (Ritu Bala): "
            "Sun strong in summer (Grishma), Moon in monsoon (Varsha), Mars in Grishma/Sharad, "
            "Mercury in autumn (Sharad), Jupiter in winter (Hemanta), Venus in spring (Vasanta), "
            "Saturn in late winter (Shishira).",
        confidence=0.82, verse="BPHS Ch.5 v.43-48",
        tags=["graha_nature", "ritu_bala", "seasonal_strength", "sun_summer", "venus_spring"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH098", source="BPHS", chapter="Ch.6", school="parashari",
        category="graha_nature",
        description="Planetary Age of Influence (Maturation): "
            "Sun matures at age 22, Moon at 24, Mars at 28, Mercury at 32, "
            "Jupiter at 16, Venus at 25, Saturn at 36, Rahu at 42, Ketu at 48. "
            "Before maturation age, planet gives mixed or incomplete results even in good dasha.",
        confidence=0.87, verse="BPHS Ch.6 v.37-42",
        tags=["graha_nature", "maturation_age", "sun_22", "saturn_36", "rahu_42", "jupiter_16"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH099", source="BPHS", chapter="Ch.7", school="parashari",
        category="graha_nature",
        description="Planetary Cabinet Hierarchy: Sun=King, Moon=Queen, Mars=Commander, "
            "Mercury=Prince/Messenger, Jupiter=Minister, Venus=Minister, Saturn=Servant. "
            "Chart analysis: whose 'court' is it? Strongest planet = dominant force in life. "
            "Lagna lord's relationship to these determines native's role in society.",
        confidence=0.87, verse="BPHS Ch.7 v.37-42",
        tags=["graha_nature", "cabinet", "sun_king", "moon_queen", "jupiter_minister", "saturn_servant"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GCH100", source="BPHS", chapter="Ch.8", school="parashari",
        category="graha_nature",
        description="Planetary Objects in Life: "
            "Sun=authority/government/power, Moon=liquids/public/women, Mars=weapons/land/fire, "
            "Mercury=accounts/trade/documents, Jupiter=gold/children/wisdom, "
            "Venus=gems/vehicles/romance, Saturn=iron/oil/workers. "
            "Affliction to planet = trouble with its objects; strength = success with its objects.",
        confidence=0.87, verse="BPHS Ch.8 v.37-42",
        tags=["graha_nature", "objects", "sun_authority", "moon_liquids", "saturn_iron", "objects_signification"],
        implemented=False,
    ),
]

for rule in _RULES:
    BPHS_GRAHA_CHARACTERISTICS_REGISTRY.add(rule)
