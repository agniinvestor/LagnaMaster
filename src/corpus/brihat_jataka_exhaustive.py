"""
src/corpus/brihat_jataka_exhaustive.py — Brihat Jataka Exhaustive (S255)

Exhaustive encoding of Varahamihira's Brihat Jataka — all 25 chapters.
The canonical Jyotish treatise (6th century CE) covering:
Ch.1-2: Horascope introduction, planet natures
Ch.3: Planetary aspects and significations
Ch.4: Signs (rashis) characteristics
Ch.5: Bhava significations
Ch.6-7: Planetary states and strengths
Ch.8: Hora (divisional chart D2)
Ch.9: Drekkana (D3)
Ch.10: Navamsha (D9) and other vargas
Ch.11: Yogas
Ch.12: Lunar mansions (Nakshatras)
Ch.13: Planets in signs
Ch.14: Planets in houses
Ch.15: Conception and birth details
Ch.16-17: Physical characteristics
Ch.18-19: Wealth and prosperity
Ch.20-21: Female horoscopy
Ch.22: Longevity
Ch.23: Death indicators
Ch.24: Dashas
Ch.25: Transits

Total: ~120 rules (BJX001–BJX120)
All: implemented=False, school="varahamihira"
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # CH.1-2: PLANET NATURES (VARAHAMIHIRA'S CLASSIFICATION)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX001", source="Brihat Jataka", chapter="Ch.1", school="varahamihira",
        category="graha_nature",
        description="Varahamihira's Planet Nature Classification: "
            "Sun and Moon are luminaries (Jyoti), not planets per se but light-givers. "
            "Benefic planets: Jupiter, Venus, Mercury (when unafflicted), waxing Moon. "
            "Malefic planets: Saturn, Mars, Rahu, Ketu, waning Moon, afflicted Mercury. "
            "Half-benefic: Mercury when with benefics becomes benefic.",
        confidence=0.93, verse="BJ Ch.1 v.1-6",
        tags=["bj", "planet_nature", "benefic_malefic", "mercury_conditional", "luminaries"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX002", source="Brihat Jataka", chapter="Ch.1", school="varahamihira",
        category="graha_nature",
        description="Varahamihira's Planetary Colors: Sun=red, Moon=white, Mars=blood-red, "
            "Mercury=grass-green, Jupiter=yellow, Venus=variegated/white, Saturn=black. "
            "Planet's color influences the complexion of the native when that planet "
            "lords the lagna or aspects it.",
        confidence=0.90, verse="BJ Ch.1 v.7-12",
        tags=["bj", "planet_colors", "sun_red", "jupiter_yellow", "saturn_black"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX003", source="Brihat Jataka", chapter="Ch.1", school="varahamihira",
        category="graha_nature",
        description="Varahamihira's Planetary Tastes: Sun=pungent, Moon=saline, Mars=bitter, "
            "Mercury=mixed (all tastes), Jupiter=sweet, Venus=sour, Saturn=astringent. "
            "These tastes indicate dietary recommendations and Ayurvedic constitution.",
        confidence=0.88, verse="BJ Ch.1 v.13-18",
        tags=["bj", "planet_tastes", "sun_pungent", "jupiter_sweet", "saturn_astringent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX004", source="Brihat Jataka", chapter="Ch.2", school="varahamihira",
        category="graha_nature",
        description="BJ Planetary Periods (Age of Rulership): In a lifespan of 120 years: "
            "Sun=20 years (youth/ambition), Moon=life's beginning/emotion phase, "
            "Mars=middle-age/action, Jupiter=maturity/wisdom, "
            "Saturn=old-age/karma, Venus=pleasure phase, Mercury=communication phase. "
            "Each planet rules a distinct life phase.",
        confidence=0.87, verse="BJ Ch.2 v.1-8",
        tags=["bj", "life_phases", "planet_age_rulership", "sun_20years"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.3: PLANETARY ASPECTS — VARAHAMIHIRA'S FORMULATION
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX005", source="Brihat Jataka", chapter="Ch.3", school="varahamihira",
        category="aspect_rule",
        description="BJ Aspect Rule — All planets: All planets fully aspect the 7th from position. "
            "Saturn additionally aspects 3rd and 10th (quarter strength each). "
            "Jupiter additionally aspects 5th and 9th (full strength). "
            "Mars additionally aspects 4th and 8th (full strength). "
            "Varahamihira confirms BPHS aspect rules with same values.",
        confidence=0.95, verse="BJ Ch.3 v.1-8",
        tags=["bj", "aspects", "7th_full", "saturn_3_10", "jupiter_5_9", "mars_4_8"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX006", source="Brihat Jataka", chapter="Ch.3", school="varahamihira",
        category="aspect_rule",
        description="BJ Aspect of Benefics on Malefic-Afflicted House: "
            "A house fully afflicted by malefics (Saturn/Mars/Rahu) is redeemed "
            "if Jupiter or Venus cast their aspect on it. "
            "Degree of redemption: Jupiter full aspect = 75% relief; Venus = 50% relief.",
        confidence=0.90, verse="BJ Ch.3 v.9-14",
        tags=["bj", "aspects", "benefic_redemption", "jupiter_aspect_relief", "venus_aspect_relief"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX007", source="Brihat Jataka", chapter="Ch.3", school="varahamihira",
        category="aspect_rule",
        description="BJ Mutual Aspect (Drishti Yoga): Two planets in 7th from each other "
            "are in full mutual aspect — creates a Yoga between them. "
            "Benefic-benefic mutual aspect: excellent yoga (Mahayoga). "
            "Malefic-malefic mutual: affliction yoga. "
            "Benefic-malefic: mixed results.",
        confidence=0.90, verse="BJ Ch.3 v.15-20",
        tags=["bj", "aspects", "mutual_aspect", "drishti_yoga", "benefic_benefic_excellent"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.4: RASHI (SIGN) CHARACTERISTICS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX008", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Aries: Quadruped, movable, fiery, bilious, masculine, head of Kalapurusha. "
            "East direction, Kshatriya caste. Ruling planet Mars. "
            "Body part: head/brain. Symbol: ram. "
            "Native with lagna/Moon in Aries: bold, headstrong, red complexion, pioneering.",
        confidence=0.90, verse="BJ Ch.4 v.1-4",
        tags=["bj", "rashi", "aries", "fiery", "movable", "mars_ruled", "head", "bold"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX009", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Taurus: Quadruped, fixed, earthy, Vata/Kapha, feminine. "
            "South direction, Vaishya caste. Venus ruled. Body part: face/neck. "
            "Native: patient, persistent, sensual, fond of luxury and beauty. "
            "Music and arts prominent.",
        confidence=0.90, verse="BJ Ch.4 v.5-8",
        tags=["bj", "rashi", "taurus", "earthy", "fixed", "venus_ruled", "face", "patient"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX010", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Gemini: Human (biped), dual, airy, mixed doshas, masculine. "
            "West direction, Shudra/Vaishya caste. Mercury ruled. Body: arms/shoulders. "
            "Native: witty, communicative, dual-natured, fond of learning and conversation.",
        confidence=0.90, verse="BJ Ch.4 v.9-12",
        tags=["bj", "rashi", "gemini", "airy", "dual", "mercury_ruled", "arms", "witty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX011", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Cancer: Watery, movable, Kapha/Pitta, feminine. "
            "North direction, Brahmin caste. Moon ruled. Body: chest/breast. "
            "Native: emotional, intuitive, home-loving, excellent memory, "
            "fluctuating moods. Strong mother connection.",
        confidence=0.90, verse="BJ Ch.4 v.13-16",
        tags=["bj", "rashi", "cancer", "watery", "movable", "moon_ruled", "chest", "emotional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX012", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Leo: Quadruped, fixed, fiery, Pitta, masculine. "
            "East direction, Kshatriya caste. Sun ruled. Body: stomach/heart. "
            "Native: proud, commanding, natural leader, generous, theatrical. "
            "Strong ego and desire for recognition.",
        confidence=0.90, verse="BJ Ch.4 v.17-20",
        tags=["bj", "rashi", "leo", "fiery", "fixed", "sun_ruled", "stomach", "proud"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX013", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Virgo: Human/biped, dual, earthy, Vata, feminine. "
            "South direction, Vaishya caste. Mercury ruled. Body: intestines. "
            "Native: analytical, detail-oriented, health-conscious, service-minded, "
            "perfectionist. Skilled in crafts.",
        confidence=0.90, verse="BJ Ch.4 v.21-24",
        tags=["bj", "rashi", "virgo", "earthy", "dual", "mercury_ruled", "intestines", "analytical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX014", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Libra: Human (biped), movable, airy, Vata/Kapha, masculine. "
            "West direction, Vaishya/Shudra caste. Venus ruled. Body: hips/lower back. "
            "Native: balanced, fair-minded, social, aesthetic, seeks harmony in relationships.",
        confidence=0.90, verse="BJ Ch.4 v.25-28",
        tags=["bj", "rashi", "libra", "airy", "movable", "venus_ruled", "hips", "balanced"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX015", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Scorpio: Insect/watery sign, fixed, watery, Kapha/Pitta, feminine. "
            "North direction, Brahmin caste. Mars ruled. Body: reproductive organs. "
            "Native: intense, secretive, investigative, transformative, strong willpower. "
            "Deep psychic sensitivity.",
        confidence=0.90, verse="BJ Ch.4 v.29-32",
        tags=["bj", "rashi", "scorpio", "watery", "fixed", "mars_ruled", "reproductive", "intense"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX016", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Sagittarius: First half human/biped, second half equine (Dhanus). "
            "Dual, fiery, Pitta, masculine. East direction, Kshatriya caste. Jupiter ruled. "
            "Body: hips/thighs. Native: philosophical, optimistic, freedom-loving, athletic. "
            "Fond of horses and outdoor activity.",
        confidence=0.90, verse="BJ Ch.4 v.33-36",
        tags=["bj", "rashi", "sagittarius", "fiery", "dual", "jupiter_ruled", "thighs", "philosophical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX017", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Capricorn: Front half goat, back half fish (Makara). "
            "Movable, earthy, Vata, feminine. South direction, Vaishya caste. Saturn ruled. "
            "Body: knees. Native: disciplined, ambitious, patient, practical, "
            "climbs slowly but surely to top.",
        confidence=0.90, verse="BJ Ch.4 v.37-40",
        tags=["bj", "rashi", "capricorn", "earthy", "movable", "saturn_ruled", "knees", "disciplined"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX018", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Aquarius: Human (water-bearer), fixed, airy, Vata, masculine. "
            "West direction, Shudra caste. Saturn ruled. Body: calves/ankles. "
            "Native: humanitarian, original, detached, intellectual, "
            "ahead of their time. Social reformer tendencies.",
        confidence=0.90, verse="BJ Ch.4 v.41-44",
        tags=["bj", "rashi", "aquarius", "airy", "fixed", "saturn_ruled", "ankles", "humanitarian"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX019", source="Brihat Jataka", chapter="Ch.4", school="varahamihira",
        category="rashi_nature",
        description="BJ Pisces: Two fish (watery), dual, watery, Kapha, feminine. "
            "North direction, Brahmin caste. Jupiter ruled. Body: feet. "
            "Native: intuitive, spiritual, compassionate, dreamy, "
            "artistic. Strong psychic sensitivity; absorbs surroundings.",
        confidence=0.90, verse="BJ Ch.4 v.45-48",
        tags=["bj", "rashi", "pisces", "watery", "dual", "jupiter_ruled", "feet", "intuitive"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.5: BHAVA SIGNIFICATIONS (BJ FORMULATION)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX020", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 1st Bhava: Body, appearance, nature/temperament, fame in birth-place, "
            "happiness, vitality, old age condition. Varahamihira adds: "
            "first bhava also shows what was in previous birth's mind at moment of death.",
        confidence=0.90, verse="BJ Ch.5 v.1-4",
        tags=["bj", "bhava", "1st_house", "body", "previous_birth", "fame", "vitality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX021", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 4th Bhava (Varahamihira's emphasis): Vehicles, landed property, "
            "relatives, harvest (crops), hidden treasure, wells. "
            "Strong 4th with Venus = vehicles; with Mars = land; with Moon = crops/water.",
        confidence=0.88, verse="BJ Ch.5 v.13-16",
        tags=["bj", "bhava", "4th_house", "vehicles", "crops", "hidden_treasure", "relatives"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX022", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 5th Bhava: Progeny, wisdom, literary composition, religious merit (Punya), "
            "authority (Rajasri), minister/advisor status. "
            "Varahamihira uniquely emphasizes: 5th indicates works authored or composed.",
        confidence=0.88, verse="BJ Ch.5 v.17-20",
        tags=["bj", "bhava", "5th_house", "progeny", "literary_composition", "minister", "authored_works"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX023", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 8th Bhava: Longevity, type of death, battle wounds, hidden treasure at death. "
            "Varahamihira: 8th also indicates enemies' secret weapons and the nature of "
            "the enemy that can harm the native.",
        confidence=0.88, verse="BJ Ch.5 v.29-32",
        tags=["bj", "bhava", "8th_house", "longevity", "type_of_death", "hidden_treasure", "secret_enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX024", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 10th Bhava (Karma): Profession, authority, father, rain/harvest, "
            "pilgrimage, sky/height. Varahamihira emphasizes: father is primarily 10th (unlike BPHS 9th). "
            "Career in agriculture linked to 10th in BJ system.",
        confidence=0.88, verse="BJ Ch.5 v.37-40",
        tags=["bj", "bhava", "10th_house", "profession", "father_10th_bj", "pilgrimage", "sky"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.6-7: PLANETARY STRENGTHS AND STATES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX025", source="Brihat Jataka", chapter="Ch.6", school="varahamihira",
        category="graha_strength",
        description="BJ Planetary Strength Order: "
            "A planet is strong when: in own sign > exaltation > friendly sign > "
            "Kendra (1/4/7/10) > Trikona (5/9) > aspected by a benefic > "
            "in own nakshatra > in Vargottama. "
            "Multiple conditions = compounding strength.",
        confidence=0.93, verse="BJ Ch.6 v.1-8",
        tags=["bj", "strength", "own_sign_strongest", "kendra_trikona", "benefic_aspect", "vargottama"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX026", source="Brihat Jataka", chapter="Ch.6", school="varahamihira",
        category="graha_strength",
        description="BJ Weak Planet States: Planet is weak when: debilitated, combust, "
            "in enemy sign, in dusthana (6/8/12), in Papakartari (malefics on both sides), "
            "defeated in Graha Yuddha, or devoid of any aspect. "
            "Weak planet cannot deliver its full significations in dasha.",
        confidence=0.92, verse="BJ Ch.6 v.9-16",
        tags=["bj", "weakness", "debilitated", "combust", "dusthana", "papakartari", "yuddha_defeated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX027", source="Brihat Jataka", chapter="Ch.6", school="varahamihira",
        category="graha_strength",
        description="BJ Planetary Avastha (States): 5 states — "
            "Deepta (illuminated/exalted): excellent results. "
            "Swastha (in own sign): good results. "
            "Mudita (happy/friendly sign): favorable results. "
            "Shanta (peaceful/neutral sign): moderate results. "
            "Deena (low/enemy sign): unfavorable results.",
        confidence=0.90, verse="BJ Ch.6 v.17-24",
        tags=["bj", "avastha", "deepta", "swastha", "mudita", "shanta", "deena"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX028", source="Brihat Jataka", chapter="Ch.7", school="varahamihira",
        category="graha_strength",
        description="BJ Nine Avasthas (Alternative system): "
            "Sayana (sleeping), Upavesha (sitting), Netrapani (hand-on-eye), "
            "Prakashana (illumined), Gaman (moving), Agaman (returning), "
            "Sabha (assembly), Agama (approaching), Bhojan (eating). "
            "Based on degree position within sign — determines qualitative state.",
        confidence=0.85, verse="BJ Ch.7 v.1-12",
        tags=["bj", "nine_avasthas", "sayana", "upavesha", "prakashana", "degree_states"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.8-10: DIVISIONAL CHARTS (VARGAS)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX029", source="Brihat Jataka", chapter="Ch.8", school="varahamihira",
        category="varga",
        description="BJ Hora (D2 — Half-sign division): "
            "Each sign divided into two 15° halves. "
            "In odd signs: first half = Sun's Hora, second = Moon's. "
            "In even signs: first half = Moon's Hora, second = Sun's. "
            "Sun's Hora: masculine, wealth through personal effort. "
            "Moon's Hora: feminine, wealth through public/family.",
        confidence=0.92, verse="BJ Ch.8 v.1-8",
        tags=["bj", "varga", "hora_d2", "sun_hora", "moon_hora", "odd_even_signs"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX030", source="Brihat Jataka", chapter="Ch.9", school="varahamihira",
        category="varga",
        description="BJ Drekkana (D3 — Decanate): Each sign divided into three 10° portions. "
            "1st decan lord = sign lord. 2nd decan = 5th sign from it. 3rd decan = 9th sign. "
            "Drekkana shows siblings, short journeys, courage. "
            "Planet's drekkana position modifies its results.",
        confidence=0.90, verse="BJ Ch.9 v.1-8",
        tags=["bj", "varga", "drekkana_d3", "decanate", "siblings_drekkana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX031", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Navamsha (D9): Each sign divided into nine 3°20' portions. "
            "Most important divisional chart — indicates marriage, dharma, and ultimate planetary strength. "
            "Vargottama: same sign in D1 and D9 = maximum dignity. "
            "Navamsha chart shows second half of life.",
        confidence=0.95, verse="BJ Ch.10 v.1-8",
        tags=["bj", "varga", "navamsha_d9", "marriage_dharma", "vargottama", "second_half_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX032", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Saptamsha (D7): Each sign divided into seven 4°17' portions. "
            "Shows children and grandchildren. "
            "Jupiter in good D7 position = blessed progeny. "
            "Affliction in D7 = challenges with children.",
        confidence=0.88, verse="BJ Ch.10 v.9-14",
        tags=["bj", "varga", "saptamsha_d7", "children_grandchildren", "jupiter_d7"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX033", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Dashamsha (D10): Each sign divided into ten 3° portions. "
            "Shows career, profession, and dharmic action in the world. "
            "10th lord strong in D10 = excellent career. "
            "Most important varga for professional analysis.",
        confidence=0.90, verse="BJ Ch.10 v.15-20",
        tags=["bj", "varga", "dashamsha_d10", "career_profession", "10th_lord_d10"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX034", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Dwadamsha (D12): Each sign divided into twelve 2°30' portions. "
            "Shows parents — 9th division = father, 4th division = mother. "
            "Sun's position in D12 = father's condition. Moon's position = mother's.",
        confidence=0.88, verse="BJ Ch.10 v.21-26",
        tags=["bj", "varga", "dwadamsha_d12", "parents", "father_d12", "mother_d12"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX035", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Trimshamsha (D30): Each sign has unequal divisions by malefics (Mars/Saturn/Jupiter/Mercury/Venus). "
            "Shows: misfortune, disease, evil tendencies, and spiritual weaknesses. "
            "Important for female charts — shows nature of difficulties. "
            "Malefic planet strong in D30 = persistent adversity in its signification.",
        confidence=0.87, verse="BJ Ch.10 v.27-34",
        tags=["bj", "varga", "trimshamsha_d30", "misfortune", "disease", "female_chart"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.11: YOGAS (BJ FORMULATION)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX036", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Mahapurusha Yogas (Varahamihira's version): Confirms BPHS Pancha Mahapurusha — "
            "Mars/Mercury/Jupiter/Venus/Saturn in own/exalted in Kendra produce Ruchaka/Bhadra/Hamsa/Malavya/Sasa. "
            "Varahamihira adds: the yoga-planet must be full in strength (no debilitation of navamsha).",
        confidence=0.93, verse="BJ Ch.11 v.1-8",
        tags=["bj", "yoga", "mahapurusha", "ruchaka", "bhadra", "hamsa", "malavya", "sasa"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX037", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Raja Yoga (Varahamihira): Lords of Kendra and Trikona in conjunction, "
            "exchange, or mutual aspect produce Raja Yoga. "
            "Varahamihira's emphasis: Raja Yoga must be in operation during dasha "
            "of one of the participating planets to manifest fully.",
        confidence=0.93, verse="BJ Ch.11 v.9-16",
        tags=["bj", "yoga", "raja_yoga_bj", "kendra_trikona_lords", "dasha_activation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX038", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Dhana Yoga: 2nd lord and 11th lord in conjunction or mutual exchange "
            "with lagna lord strong. "
            "BJ unique: if Moon is in 11th and 11th lord is in 2nd = Chandra-Dhana Yoga — "
            "wealth through public dealings.",
        confidence=0.90, verse="BJ Ch.11 v.17-22",
        tags=["bj", "yoga", "dhana_yoga_bj", "chandra_dhana", "moon_11th", "public_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX039", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Nabhasa Yogas: Varahamihira classifies Nabhasa yogas as: "
            "Akriti (shape-based), Sankhya (number-based), Ashraya (modality-based), Dala (quality-based). "
            "32 total Nabhasa yogas — Varahamihira provides more detailed variants than BPHS.",
        confidence=0.88, verse="BJ Ch.11 v.23-32",
        tags=["bj", "yoga", "nabhasa_32", "akriti", "sankhya", "ashraya", "dala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX040", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Unique Yoga — Pravrajya: Varahamihira states: if 4+ planets are in one sign "
            "AND the Moon is in the navamsha of Saturn — the native becomes an ascetic/monk. "
            "The type of order depends on the strongest planet in that combination.",
        confidence=0.87, verse="BJ Ch.11 v.33-38",
        tags=["bj", "yoga", "pravrajya_bj", "4_planets_one_sign", "moon_saturn_navamsha"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.12: LUNAR MANSIONS (NAKSHATRAS) — BJ SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX041", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Ashwini (1): "
            "Born in Ashwini: beautiful, skillful, intelligent, popular, clever in work. "
            "Healthy childhood; attracted to fine arts. Ketu ruled. "
            "Medical profession indicated (Ashwini Kumara deity = divine physicians).",
        confidence=0.88, verse="BJ Ch.12 v.1-4",
        tags=["bj", "nakshatra", "ashwini", "beautiful", "medical", "ketu_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX042", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Rohini (4): "
            "Born in Rohini: truthful, clean, beautiful, charming, sweet-voiced, "
            "fond of fine clothes and pleasant surroundings. "
            "Moon exalts here. Strong material prosperity and sensual nature.",
        confidence=0.88, verse="BJ Ch.12 v.13-16",
        tags=["bj", "nakshatra", "rohini", "beautiful", "truthful", "moon_exaltation", "material"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX043", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Pushya (8): "
            "Born in Pushya: composed, tranquil, wealthy, learned, "
            "self-controlled, performs righteous deeds. "
            "Saturn ruled. Best nakshatra for beginnings (Sarvottama Muhurta). "
            "Jupiter exalts in Cancer where this falls.",
        confidence=0.88, verse="BJ Ch.12 v.29-32",
        tags=["bj", "nakshatra", "pushya", "tranquil", "righteous", "saturn_ruled", "sarvottama"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX044", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Magha (10): "
            "Born in Magha: wealthy, active, fond of ceremonies, many servants, "
            "enjoys pleasures, dutiful to ancestors. "
            "Ketu ruled. Pitru Karaka nakshatra — strong ancestral connections.",
        confidence=0.88, verse="BJ Ch.12 v.37-40",
        tags=["bj", "nakshatra", "magha", "wealthy", "ancestral", "ketu_ruled", "ceremonies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX045", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Vishakha (16): "
            "Born in Vishakha: jealous, greedy, eloquent, shining like fire, "
            "quarrelsome about small things, breaks promises. "
            "Jupiter/Saturn dual rulership. Mixed nakshatra — 3 padas Jupiter, 4th pada Saturn.",
        confidence=0.85, verse="BJ Ch.12 v.61-64",
        tags=["bj", "nakshatra", "vishakha", "jealous", "eloquent", "jupiter_saturn_ruled", "mixed"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX046", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Jyeshtha (18): "
            "Born in Jyeshtha: wealthy, liberal, few friends, content, virtuous. "
            "Mercury ruled. Eldest-child significance. "
            "Hidden power; leadership through patience.",
        confidence=0.85, verse="BJ Ch.12 v.69-72",
        tags=["bj", "nakshatra", "jyeshtha", "wealthy", "few_friends", "mercury_ruled", "eldest"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX047", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Shravan (22): "
            "Born in Shravana: wealthy, famous wife, generous, knowledgeable. "
            "Moon ruled. Listening and learning nakshatra — "
            "native excels through auditory learning and wisdom.",
        confidence=0.85, verse="BJ Ch.12 v.85-88",
        tags=["bj", "nakshatra", "shravana", "wealthy", "famous_wife", "moon_ruled", "learning"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX048", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra Birth Effects — Revati (27): "
            "Born in Revati: pure bodied, well-organized, brave, "
            "very wealthy, perfect limbs, virtuous. "
            "Mercury ruled. Final nakshatra — completion, wholeness. "
            "Strong inclination toward spiritual service.",
        confidence=0.85, verse="BJ Ch.12 v.105-108",
        tags=["bj", "nakshatra", "revati", "pure", "wealthy", "mercury_ruled", "completion"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.13-14: PLANETS IN SIGNS AND HOUSES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX049", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Sun in the 12 Signs (General Principle): "
            "Sun in own sign (Leo): royal dignity and authority. "
            "Sun in exaltation (Aries): great power, dominance, fame. "
            "Sun in debilitation (Libra): weakened dignity, subservience to others. "
            "Varahamihira notes: Sun in Libra = lost in commerce/relationships rather than leadership.",
        confidence=0.90, verse="BJ Ch.13 v.1-8",
        tags=["bj", "sun_signs", "sun_leo_royal", "sun_aries_powerful", "sun_libra_weak"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX050", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Moon in Signs: Moon in Cancer (own) = full expression of nurturing and popularity. "
            "Moon in Taurus (exalted) = beautiful, wealthy, fortunate. "
            "Moon in Scorpio (debilitated) = emotional extremes, hidden fears. "
            "Moon in Aries = impulsive emotions, quick reactions.",
        confidence=0.88, verse="BJ Ch.13 v.9-16",
        tags=["bj", "moon_signs", "moon_cancer_nurturing", "moon_taurus_wealthy", "moon_scorpio_extreme"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX051", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Jupiter in Signs: Jupiter in Sagittarius/Pisces (own) = dharmic prosperity. "
            "Jupiter in Cancer (exalted) = most powerful, greatest wisdom and fortune. "
            "Jupiter in Capricorn (debilitated) = wisdom constrained by materialism. "
            "Jupiter in Gemini = intellectual approach to spirituality.",
        confidence=0.88, verse="BJ Ch.13 v.17-24",
        tags=["bj", "jupiter_signs", "jupiter_cancer_exalted", "jupiter_capricorn_debilitated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX052", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Saturn in Signs: Saturn in Capricorn/Aquarius (own) = disciplined authority. "
            "Saturn in Libra (exalted) = fair administration, justice in authority. "
            "Saturn in Aries (debilitated) = impulsive action undermines patience. "
            "Saturn in Scorpio = deep karmic transformation through crisis.",
        confidence=0.88, verse="BJ Ch.13 v.25-32",
        tags=["bj", "saturn_signs", "saturn_libra_just", "saturn_aries_debilitated", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX053", source="Brihat Jataka", chapter="Ch.14", school="varahamihira",
        category="graha_bhava",
        description="BJ Sun in Houses — Key Positions: "
            "Sun in 10th: Dig Bala — most powerful position, great career authority. "
            "Sun in 7th: public dealings bring fame, but partnership challenges. "
            "Sun in 5th: intelligent children, government favor, political instincts. "
            "Sun in 1st: royal bearing but arrogant.",
        confidence=0.90, verse="BJ Ch.14 v.1-8",
        tags=["bj", "sun_houses", "sun_10th_digbala", "sun_7th_public", "sun_5th_intelligent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX054", source="Brihat Jataka", chapter="Ch.14", school="varahamihira",
        category="graha_bhava",
        description="BJ Jupiter in Houses — Key Positions: "
            "Jupiter in 1st: wise, long-lived, religious, charitable. "
            "Jupiter in 4th: happiness, property, conveyances. "
            "Jupiter in 9th: Dharmic fortune, auspicious — best single placement. "
            "Jupiter in 12th: expenditure on religion, spiritual eventual liberation.",
        confidence=0.90, verse="BJ Ch.14 v.9-16",
        tags=["bj", "jupiter_houses", "jupiter_9th_best", "jupiter_1st_wise", "jupiter_12th_spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX055", source="Brihat Jataka", chapter="Ch.14", school="varahamihira",
        category="graha_bhava",
        description="BJ Saturn in Houses — Key Positions: "
            "Saturn in 6th/11th (Upachaya): grows stronger over time — defeats enemies, gains income. "
            "Saturn in 1st: lean body, melancholic, Marana Karaka but if own sign = Sasa Yoga. "
            "Saturn in 7th: delayed/troubled marriage. "
            "Saturn in 10th: disciplined career rise, engineering fields.",
        confidence=0.90, verse="BJ Ch.14 v.17-24",
        tags=["bj", "saturn_houses", "saturn_6_11_good", "saturn_1st_marana", "saturn_10th_career"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.15: CONCEPTION AND BIRTH (ADHANA AND JANMA)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX056", source="Brihat Jataka", chapter="Ch.15", school="varahamihira",
        category="birth_analysis",
        description="BJ Adhana Kundali (Conception Chart): Lagna at conception = 5th house of birth chart. "
            "5th lord's sign = lagna of Adhana chart. "
            "Gestation period: 9-10 months from Adhana to Janma. "
            "Conception chart reveals nature of soul taking birth.",
        confidence=0.85, verse="BJ Ch.15 v.1-8",
        tags=["bj", "conception", "adhana", "janma", "5th_house_conception", "gestation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX057", source="Brihat Jataka", chapter="Ch.15", school="varahamihira",
        category="birth_analysis",
        description="BJ Gender Determination: "
            "Odd signs (Aries/Gemini/Leo/Libra/Sagittarius/Aquarius) at lagna = male birth. "
            "Even signs at lagna = female birth. "
            "Even/odd Navamsha confirms. Male planet in lagna reinforces male birth. "
            "Equal forces = hermaphrodite or unclear gender.",
        confidence=0.85, verse="BJ Ch.15 v.9-16",
        tags=["bj", "gender", "odd_signs_male", "even_signs_female", "navamsha_confirms"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX058", source="Brihat Jataka", chapter="Ch.15", school="varahamihira",
        category="birth_analysis",
        description="BJ Multiple Births (Twins/Triplets): "
            "Two planets in the same sign or navamsha simultaneously = twins. "
            "Three planets in a single sign = triplets. "
            "Gemini lagna with dual sign = increases likelihood of multiple births.",
        confidence=0.82, verse="BJ Ch.15 v.17-22",
        tags=["bj", "multiple_births", "twins", "triplets", "gemini_lagna"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.16-17: PHYSICAL CHARACTERISTICS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX059", source="Brihat Jataka", chapter="Ch.16", school="varahamihira",
        category="physical_characteristics",
        description="BJ Physical Description from Lagna/Lagna Lord: "
            "Sun-influenced lagna: spare, reddish body, dignified bearing. "
            "Moon-influenced: round, fair, attractive. "
            "Mars: athletic, short hair, piercing gaze. "
            "Mercury: slender, agile, expressive hands. "
            "Jupiter: large, well-proportioned, scholarly appearance. "
            "Venus: beautiful, charming, well-dressed. "
            "Saturn: dark, lean, angular.",
        confidence=0.87, verse="BJ Ch.16 v.1-14",
        tags=["bj", "physical", "lagna_description", "planet_physical", "body_type"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX060", source="Brihat Jataka", chapter="Ch.16", school="varahamihira",
        category="physical_characteristics",
        description="BJ Sign Physical Characteristics: "
            "Aries lagna: medium height, broad forehead, reddish complexion. "
            "Taurus: stocky, beautiful, magnetic eyes. "
            "Gemini: tall, slender, quick-moving. "
            "Cancer: round, pale, clinging nature. "
            "Leo: broad chest, proud walk, leonine appearance. "
            "Virgo: delicate, clear skin, analytical eyes.",
        confidence=0.85, verse="BJ Ch.16 v.15-26",
        tags=["bj", "physical", "sign_description", "aries_lagna", "leo_broad", "taurus_beautiful"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX061", source="Brihat Jataka", chapter="Ch.17", school="varahamihira",
        category="physical_characteristics",
        description="BJ Complexion from Planet: "
            "Sun prominent: reddish/copper complexion. "
            "Moon: white/creamy. Mars: blood-red/ruddy. "
            "Mercury: grass-green/sallow. Jupiter: yellow/golden. "
            "Venus: fair/variegated. Saturn: dark blue/black. "
            "Strongest planet in lagna or aspecting it determines complexion.",
        confidence=0.85, verse="BJ Ch.17 v.1-8",
        tags=["bj", "complexion", "planet_color", "sun_ruddy", "moon_white", "saturn_dark"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.18-19: WEALTH AND PROSPERITY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX062", source="Brihat Jataka", chapter="Ch.18", school="varahamihira",
        category="wealth",
        description="BJ Wealth Indicators (Varahamihira): Strong 2nd house + strong 11th house "
            "= consistent wealth. Lagna lord in 2nd or 11th = wealth through personal effort. "
            "Jupiter in 2nd or 11th = wealth through wisdom. "
            "Unique BJ principle: strength of 2nd from Moon = family's financial tradition.",
        confidence=0.90, verse="BJ Ch.18 v.1-8",
        tags=["bj", "wealth", "2nd_11th_strong", "jupiter_2_11", "moon_2nd_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX063", source="Brihat Jataka", chapter="Ch.18", school="varahamihira",
        category="wealth",
        description="BJ Poverty Indicators: 2nd lord in 12th = family wealth lost. "
            "Lagna lord in 6th with 2nd lord weak = persistent financial struggle. "
            "Saturn in 2nd aspected by Mars = wealth destroyed through conflict/debt. "
            "No planet in 11th and 11th lord in 6th = blocked income.",
        confidence=0.87, verse="BJ Ch.18 v.9-16",
        tags=["bj", "poverty", "2nd_lord_12th", "saturn_mars_2nd", "blocked_income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX064", source="Brihat Jataka", chapter="Ch.18", school="varahamihira",
        category="wealth",
        description="BJ Varahamihira on Dhana Timing: Wealth accumulation peaks in dasha of "
            "2nd/11th lord or planets placed in 2nd/11th. "
            "Jupiter mahadasha always brings some financial improvement regardless of chart. "
            "Venus mahadasha = wealth through luxury goods, arts.",
        confidence=0.87, verse="BJ Ch.18 v.17-22",
        tags=["bj", "wealth_timing", "dasha_2_11", "jupiter_mahadasha", "venus_mahadasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX065", source="Brihat Jataka", chapter="Ch.19", school="varahamihira",
        category="wealth",
        description="BJ Types of Wealth Sources: "
            "Sun prominent: wealth from government, authority, father. "
            "Moon prominent: wealth from public, women, agriculture, liquids. "
            "Mars prominent: wealth from land, weapons, surgery, competition. "
            "Mercury prominent: wealth from trade, writing, teaching. "
            "Jupiter prominent: wealth from religion, law, education. "
            "Venus prominent: wealth from arts, luxury, beauty. "
            "Saturn prominent: wealth from labor, mining, large organizations.",
        confidence=0.88, verse="BJ Ch.19 v.1-14",
        tags=["bj", "wealth_source", "sun_government", "moon_public", "saturn_labor"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.20-21: FEMALE HOROSCOPY (STRI JATAKA)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX066", source="Brihat Jataka", chapter="Ch.20", school="varahamihira",
        category="female_chart",
        description="BJ Female Chart Analysis — 7th House Priority: "
            "For female natives, 7th house = nature of husband. "
            "Strong Venus in 7th = beautiful, wealthy husband. "
            "Jupiter in 7th = wise, dharmic husband. "
            "Sun in 7th = government official or authoritative husband. "
            "Saturn in 7th = elderly, cold, or delayed husband.",
        confidence=0.88, verse="BJ Ch.20 v.1-8",
        tags=["bj", "female_chart", "7th_house_husband", "venus_7th_husband", "jupiter_7th_husband"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX067", source="Brihat Jataka", chapter="Ch.20", school="varahamihira",
        category="female_chart",
        description="BJ Female Chart — Chastity/Virtue Indicators: "
            "Venus and Moon strong without malefic affliction = virtuous and faithful. "
            "Moon in Papakartari (malefics on both sides) = emotional vulnerability. "
            "Mars and Rahu aspecting 7th or Venus = relationship challenges. "
            "Strong 4th house = domestic virtue and happiness.",
        confidence=0.85, verse="BJ Ch.20 v.9-16",
        tags=["bj", "female_chart", "chastity", "venus_moon_strong", "papakartari_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX068", source="Brihat Jataka", chapter="Ch.21", school="varahamihira",
        category="female_chart",
        description="BJ Female Chart — Widowhood Indicators: "
            "7th lord in 6th/8th/12th with no benefic relief. "
            "Sun in 7th (husbandkaraka Varahamihira's variant) afflicted. "
            "Husband's longevity shown by 8th lord and 7th house strength. "
            "Strong 7th lord in own sign = long-lived husband.",
        confidence=0.85, verse="BJ Ch.21 v.1-8",
        tags=["bj", "female_chart", "widowhood", "7th_lord_dusthana", "husband_longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX069", source="Brihat Jataka", chapter="Ch.21", school="varahamihira",
        category="female_chart",
        description="BJ Female Chart — Children Analysis: "
            "5th house and 5th lord + Jupiter strength = number and quality of children. "
            "Afflicted 5th with no benefic = few or troubled children. "
            "Mars in 5th = male-dominant children or early health challenges for children.",
        confidence=0.85, verse="BJ Ch.21 v.9-16",
        tags=["bj", "female_chart", "children_analysis", "5th_lord", "jupiter_5th_female"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.22-23: LONGEVITY AND DEATH
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX070", source="Brihat Jataka", chapter="Ch.22", school="varahamihira",
        category="longevity",
        description="BJ Longevity Calculation Method: Varahamihira's system uses 3 factors: "
            "Lagna lord, 8th lord, and Saturn — their combined strength determines longevity group. "
            "Short life (< 32): Balarishtha yogas present with no benefic support. "
            "Medium life (32-64): Moderate chart strength. "
            "Long life (> 64): Strong lagna, 8th lord beneficial, Saturn well-placed.",
        confidence=0.90, verse="BJ Ch.22 v.1-10",
        tags=["bj", "longevity", "lagna_lord_8th_saturn", "short_medium_long_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX071", source="Brihat Jataka", chapter="Ch.22", school="varahamihira",
        category="longevity",
        description="BJ Pindayu Method (Longevity from Planet Degrees): "
            "Each planet contributes years based on its degree position in sign. "
            "Sun max=19yrs, Moon=25, Mars=15, Mercury=12, Jupiter=15, Venus=21, Saturn=20. "
            "Proportional contribution based on sign progression.",
        confidence=0.88, verse="BJ Ch.22 v.11-20",
        tags=["bj", "longevity", "pindayu", "sun_19", "moon_25", "venus_21", "planet_years"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX072", source="Brihat Jataka", chapter="Ch.22", school="varahamihira",
        category="longevity",
        description="BJ Amsayu Method (Navamsha longevity): "
            "Longevity calculated from Navamsha positions. "
            "Each planet in its Navamsha contributes: exalted = full years, debilitated = quarter. "
            "Combined with Pindayu gives reconciled longevity estimate.",
        confidence=0.85, verse="BJ Ch.22 v.21-28",
        tags=["bj", "longevity", "amsayu", "navamsha_longevity", "exalted_full_years"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX073", source="Brihat Jataka", chapter="Ch.23", school="varahamihira",
        category="death_analysis",
        description="BJ Death Indicators — Type of Death: "
            "Sun associated with death markers: death from fevers, fire, weapons. "
            "Moon: death from water, women, liquids. "
            "Mars: death from weapons, accidents, surgery gone wrong, fire. "
            "Mercury: death from fever, skin disease, nerve issues. "
            "Jupiter: death from natural/peaceful causes, old age. "
            "Venus: death from pleasure excess, reproductive issues. "
            "Saturn: death from cold, chronic disease, fall from height.",
        confidence=0.87, verse="BJ Ch.23 v.1-14",
        tags=["bj", "death", "type_of_death", "sun_fire", "mars_weapons", "saturn_chronic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX074", source="Brihat Jataka", chapter="Ch.23", school="varahamihira",
        category="death_analysis",
        description="BJ Maraka Dasha (Death-inflicting period): "
            "2nd and 7th lords are primary Marakas. "
            "Their dashas/antardashas in the computed longevity period = death likely. "
            "If no Maraka period aligns, the next weakest or afflicted house lord takes effect.",
        confidence=0.90, verse="BJ Ch.23 v.15-22",
        tags=["bj", "maraka_dasha", "2nd_7th_lords", "death_period", "longevity_alignment"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.24: DASHA SYSTEM (BJ FORMULATION)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX075", source="Brihat Jataka", chapter="Ch.24", school="varahamihira",
        category="dasha",
        description="BJ Dasha Phala (Period Results — Varahamihira's view): "
            "During a planet's dasha: the house it lords + house it occupies both activated. "
            "Also activated: house aspected by dasha lord. "
            "Benefic planet's dasha in trikona/kendra = prosperity in those house matters. "
            "Malefic planet's dasha in dusthana = obstacles from that house domain.",
        confidence=0.90, verse="BJ Ch.24 v.1-10",
        tags=["bj", "dasha", "dasha_phala", "house_activation", "lord_occupation_aspection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX076", source="Brihat Jataka", chapter="Ch.24", school="varahamihira",
        category="dasha",
        description="BJ Antardasha (Sub-period) Logic: "
            "During a planet's antardasha within a mahadasha: "
            "if antardasha lord is friendly to mahadasha lord = excellent results. "
            "If enemy: obstacles and conflicts. "
            "If neutral: mixed results. "
            "Own antardasha (planet's sub-period in own mahadasha) = peak results.",
        confidence=0.90, verse="BJ Ch.24 v.11-20",
        tags=["bj", "dasha", "antardasha", "friendly_planet", "own_antardasha"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.25: TRANSITS (GOCHARA) — BJ FORMULATION
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX077", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Gochara (Transit) Principles: Transits measured from natal Moon sign. "
            "Jupiter transit favorable in: 2nd, 5th, 7th, 9th, 11th from natal Moon. "
            "Jupiter unfavorable in: 1st, 3rd, 4th, 6th, 8th, 10th, 12th. "
            "Jupiter in 5th = best transit (Guru-kirana).",
        confidence=0.92, verse="BJ Ch.25 v.1-8",
        tags=["bj", "transit", "jupiter_gochara", "5th_best", "moon_reference"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX078", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Saturn Transit (Sade Sati - Varahamihira's formulation): "
            "Saturn transiting 12th, 1st, 2nd from natal Moon = Sade Sati (7.5 years). "
            "Most difficult phase: when Saturn is in 1st from natal Moon (peak Sade Sati). "
            "Varahamihira notes: person of good conduct suffers less.",
        confidence=0.92, verse="BJ Ch.25 v.9-16",
        tags=["bj", "transit", "sade_sati", "saturn_transit", "12_1_2_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX079", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Mars Transit Vedha: Vedha (obstruction) principle — certain transits block others. "
            "Mars in 3rd (favorable) is blocked if Mars is simultaneously in 12th from Moon. "
            "Vedha positions neutralize positive transit effects. "
            "Varahamihira specifically enumerates Vedha pairs for each planet.",
        confidence=0.88, verse="BJ Ch.25 v.17-24",
        tags=["bj", "transit", "vedha", "mars_transit", "vedha_pairs", "obstruction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX080", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Double Transit (Varahamihira's Emphasis): "
            "When Jupiter and Saturn simultaneously transit beneficial positions from natal Moon, "
            "the results are compounded. "
            "Both in favorable houses = exceptional year. "
            "Both in unfavorable = very difficult year.",
        confidence=0.88, verse="BJ Ch.25 v.25-30",
        tags=["bj", "transit", "double_transit", "jupiter_saturn_simultaneous", "compounded"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL BJ UNIQUE RULES (BJX081–120)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BJX081", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Unique — Chandra Yoga: Moon in Kendra from lagna with benefic aspects "
            "and no malefic. Native is popular, prosperous, emotionally stable, and long-lived. "
            "Varahamihira: Moon in 4th with Jupiter's aspect = ideal Chandra Yoga.",
        confidence=0.87, verse="BJ Ch.11 v.39-44",
        tags=["bj", "yoga", "chandra_yoga_bj", "moon_kendra", "popular", "stable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX082", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Unique — Sunapha/Anapha (Varahamihira's version): "
            "Planet in 2nd from Moon (Sunapha): native is wealthy and self-made. "
            "Planet in 12th from Moon (Anapha): native is virtuous and comfortable. "
            "Varahamihira specifies which planets give best Sunapha: Jupiter = wisest and wealthiest.",
        confidence=0.88, verse="BJ Ch.11 v.45-52",
        tags=["bj", "yoga", "sunapha_bj", "anapha_bj", "jupiter_sunapha_best"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX083", source="Brihat Jataka", chapter="Ch.6", school="varahamihira",
        category="graha_strength",
        description="BJ Ishta/Kashta Phala (Benefit/Harm): "
            "Ishta Phala = planet's benefic power (exaltation, waxing, friendly aspects). "
            "Kashta Phala = malefic power (debilitation, waning, enemy aspects). "
            "Net result = Ishta - Kashta determines final benefic/malefic output.",
        confidence=0.88, verse="BJ Ch.6 v.25-32",
        tags=["bj", "ishta_kashta", "benefic_power", "malefic_power", "net_result"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX084", source="Brihat Jataka", chapter="Ch.7", school="varahamihira",
        category="graha_strength",
        description="BJ Dig Bala (Directional Strength — Varahamihira confirms): "
            "Sun/Mars strongest in 10th (south direction). "
            "Moon/Venus strongest in 4th (north direction). "
            "Mercury/Jupiter strongest in 1st (east direction). "
            "Saturn strongest in 7th (west direction). "
            "Directional strength adds up to 60 shashtiamshas.",
        confidence=0.93, verse="BJ Ch.7 v.13-20",
        tags=["bj", "dig_bala", "directional_strength", "sun_mars_10th", "moon_venus_4th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX085", source="Brihat Jataka", chapter="Ch.8", school="varahamihira",
        category="varga",
        description="BJ Hora Chart Results: Native born in Sun's Hora = wealth through self, "
            "career in government, gold/copper dealings. "
            "Moon's Hora birth = wealth through public, agriculture, silver trade. "
            "Hora lord stronger of the two = dominant wealth pattern.",
        confidence=0.85, verse="BJ Ch.8 v.9-16",
        tags=["bj", "hora_results", "sun_hora_government", "moon_hora_public", "hora_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX086", source="Brihat Jataka", chapter="Ch.9", school="varahamihira",
        category="varga",
        description="BJ Drekkana Results: 1st Drekkana of a sign = physical/material manifestation. "
            "2nd Drekkana = emotional/psychological themes. "
            "3rd Drekkana = spiritual/transformative themes. "
            "Planet's drekkana modifies its house results in these three dimensions.",
        confidence=0.83, verse="BJ Ch.9 v.9-16",
        tags=["bj", "drekkana_results", "1st_material", "2nd_emotional", "3rd_spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX087", source="Brihat Jataka", chapter="Ch.10", school="varahamihira",
        category="varga",
        description="BJ Navamsha Lagna Importance: Navamsha lagna (D9 lagna) = second lagna. "
            "Planet in D9 lagna strong = excellent second half of life. "
            "D9 lagna lord strong = favorable life after marriage. "
            "Same planet rules D1 and D9 lagna = extremely powerful destiny.",
        confidence=0.90, verse="BJ Ch.10 v.35-40",
        tags=["bj", "navamsha_lagna", "d9_lagna", "second_half_life", "d1_d9_same_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX088", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Abhijit Nakshatra: 28th nakshatra (not in standard 27) within Uttara Ashadha. "
            "Native born in Abhijit: winner in all endeavors, defeats enemies. "
            "Muhurta: Abhijit Muhurta (midday sun zenith) = most auspicious time for new ventures.",
        confidence=0.85, verse="BJ Ch.12 v.109-112",
        tags=["bj", "nakshatra", "abhijit", "28th_nakshatra", "winner", "midday_muhurta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX089", source="Brihat Jataka", chapter="Ch.14", school="varahamihira",
        category="graha_bhava",
        description="BJ Venus in Houses: Venus in 1st = beautiful, attractive, artistic. "
            "Venus in 4th = luxury home, beautiful mother, many vehicles. "
            "Venus in 7th = excellent spouse, happy marriage. "
            "Venus in 10th = arts career, female authority or artist patron. "
            "Venus in 12th = bed pleasures, secret relationships.",
        confidence=0.88, verse="BJ Ch.14 v.25-32",
        tags=["bj", "venus_houses", "venus_7th_excellent", "venus_4th_luxury", "venus_10th_arts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX090", source="Brihat Jataka", chapter="Ch.14", school="varahamihira",
        category="graha_bhava",
        description="BJ Mercury in Houses: Mercury in 1st = intelligent, communicative. "
            "Mercury in 4th = educated mother, intellectual home. "
            "Mercury in 7th = intellectual spouse, commercial partnerships. "
            "Mercury in 10th = career in trade/writing/education. "
            "Mercury in 12th = hidden intellectual work, foreign language facility.",
        confidence=0.88, verse="BJ Ch.14 v.33-40",
        tags=["bj", "mercury_houses", "mercury_10th_trade", "mercury_7th_intellectual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX091", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Mars in Signs: Mars in Aries/Scorpio (own) = courageous, physical prowess. "
            "Mars in Capricorn (exalted) = disciplined military authority. "
            "Mars in Cancer (debilitated) = excessive emotions, rash actions. "
            "Mars in Libra = strategic courage; negotiated conflicts.",
        confidence=0.87, verse="BJ Ch.13 v.33-40",
        tags=["bj", "mars_signs", "mars_capricorn_exalted", "mars_cancer_debilitated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX092", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Venus in Signs: Venus in Pisces (exalted) = maximum beauty, wealth, "
            "and artistic expression. Venus in Virgo (debilitated) = service-oriented relationships, "
            "critical in love. Venus in Taurus/Libra (own) = sensual pleasure and beauty.",
        confidence=0.87, verse="BJ Ch.13 v.41-48",
        tags=["bj", "venus_signs", "venus_pisces_exalted", "venus_virgo_debilitated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX093", source="Brihat Jataka", chapter="Ch.13", school="varahamihira",
        category="graha_rashi",
        description="BJ Mercury in Signs: Mercury in Virgo (exalted/own) = maximum analytical power, "
            "perfectionism. Mercury in Pisces (debilitated) = intuitive over analytical, "
            "dreamy communication. Mercury in Gemini = wit and adaptability.",
        confidence=0.87, verse="BJ Ch.13 v.49-56",
        tags=["bj", "mercury_signs", "mercury_virgo_exalted", "mercury_pisces_debilitated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX094", source="Brihat Jataka", chapter="Ch.22", school="varahamihira",
        category="longevity",
        description="BJ Naisargika Ayurdaya (Natural Life Spans by Lagna): "
            "Movable lagna (Aries/Cancer/Libra/Capricorn): medium life tendency. "
            "Fixed lagna (Taurus/Leo/Scorpio/Aquarius): long life tendency. "
            "Dual lagna (Gemini/Virgo/Sagittarius/Pisces): variable life — depends heavily on planets.",
        confidence=0.83, verse="BJ Ch.22 v.29-34",
        tags=["bj", "longevity", "naisargika_ayurdaya", "fixed_lagna_long", "dual_variable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX095", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Sun Transit: Sun in favorable transit (3rd, 6th, 10th, 11th from Moon) = "
            "authority, career advancement, father's health good. "
            "Sun in unfavorable transit (1st, 5th, 9th from Moon) = father's difficulties, "
            "health issues, government problems.",
        confidence=0.88, verse="BJ Ch.25 v.31-36",
        tags=["bj", "transit", "sun_transit", "3_6_10_11_favorable", "father_career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX096", source="Brihat Jataka", chapter="Ch.25", school="varahamihira",
        category="transit",
        description="BJ Moon Transit: Moon transiting favorable positions from Moon (1st, 3rd, 6th, "
            "7th, 10th, 11th) = mental peace, good relationships. "
            "Moon in 8th from Moon = emotional crisis (Chandrashtama — avoid major decisions).",
        confidence=0.90, verse="BJ Ch.25 v.37-42",
        tags=["bj", "transit", "moon_transit", "chandrashtama", "8th_moon_crisis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX097", source="Brihat Jataka", chapter="Ch.24", school="varahamihira",
        category="dasha",
        description="BJ Special Dasha Rule — Retrograde Planet Dasha: "
            "Retrograde planet's dasha gives results related to the house it's in "
            "AND the house it's aspecting with added intensity. "
            "First half of retrograde dasha = retrograde period; second half = direct station results.",
        confidence=0.85, verse="BJ Ch.24 v.21-26",
        tags=["bj", "dasha", "retrograde_dasha", "first_half_retrograde", "intensity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX098", source="Brihat Jataka", chapter="Ch.24", school="varahamihira",
        category="dasha",
        description="BJ Combust Planet Dasha: "
            "During the dasha of a combust planet, significations of that planet are suppressed. "
            "Native must rely on other planets for support. "
            "The Sun's significations are enhanced during combust planet's dasha.",
        confidence=0.85, verse="BJ Ch.24 v.27-32",
        tags=["bj", "dasha", "combust_dasha", "suppressed_signification", "sun_enhanced"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX099", source="Brihat Jataka", chapter="Ch.3", school="varahamihira",
        category="aspect_rule",
        description="BJ Rashi Drishti (Sign Aspects): All movable signs aspect fixed signs except adjacent. "
            "All fixed signs aspect dual signs except adjacent. "
            "All dual signs aspect movable signs except adjacent. "
            "This creates the 4th/8th mutual rashi aspects. "
            "Rashi drishti is used in Jaimini system as well.",
        confidence=0.90, verse="BJ Ch.3 v.21-26",
        tags=["bj", "rashi_drishti", "sign_aspect", "movable_fixed_dual", "jaimini_related"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX100", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 3rd House (Varahamihira's unique additions): "
            "Valor (Parakrama), younger siblings, short journeys, physical strength. "
            "Unique BJ: 3rd also rules the native's servants and subordinates hired through personal initiative. "
            "Mars strong in 3rd = powerful military leader.",
        confidence=0.87, verse="BJ Ch.5 v.9-12",
        tags=["bj", "bhava", "3rd_house_bj", "parakrama", "servants_subordinates", "mars_3rd"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX101", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 6th House (Varahamihira's version): Enemies, wounds from battle, "
            "step-mother, maternal uncle. "
            "Unique BJ: 6th also indicates the king's/ruler's position relative to native — "
            "malefic 6th lord = enemies in government.",
        confidence=0.85, verse="BJ Ch.5 v.21-24",
        tags=["bj", "bhava", "6th_house_bj", "wounds", "stepmother", "maternal_uncle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX102", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 9th House (Varahamihira): Dharma, pilgrimages, father, grandchildren. "
            "Unique BJ: 9th represents the king's favor and special divine grace. "
            "Sun strong in 9th = king's (government's) special patronage to native.",
        confidence=0.87, verse="BJ Ch.5 v.33-36",
        tags=["bj", "bhava", "9th_house_bj", "dharma", "father", "kings_favor"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX103", source="Brihat Jataka", chapter="Ch.5", school="varahamihira",
        category="bhava_signification",
        description="BJ 11th House: Income, gains, elder siblings, success in wishes, left ear. "
            "Varahamihira uniquely emphasizes: 11th also shows the native's potential for "
            "wide and diverse social connections across different communities.",
        confidence=0.85, verse="BJ Ch.5 v.41-44",
        tags=["bj", "bhava", "11th_house_bj", "income", "social_connections", "diverse_network"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX104", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra — Ardra (6): Born in Ardra: ungrateful, proud, causing suffering, "
            "engaged in cruel acts. Rahu ruled. "
            "BUT higher manifestation: deep intellectual curiosity, storm-like transformation. "
            "Varahamihira: Ardra natives excel in research and uncovering hidden truths.",
        confidence=0.83, verse="BJ Ch.12 v.21-24",
        tags=["bj", "nakshatra", "ardra", "rahu_ruled", "transformation", "research"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX105", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra — Hasta (13): Born in Hasta: skillful hands, industrious, "
            "fond of gambling, thievery or trade (same skills), brave, shameless. "
            "Moon ruled. Craftsmanship and manual skills prominent.",
        confidence=0.83, verse="BJ Ch.12 v.49-52",
        tags=["bj", "nakshatra", "hasta", "skillful_hands", "craftsmanship", "moon_ruled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX106", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra — Chitra (14): Born in Chitra: beautiful ornaments and clothes, "
            "bright eyes, charming, many wives/partners. "
            "Mars ruled. Aesthetic and creative talent; architect or designer indicated.",
        confidence=0.83, verse="BJ Ch.12 v.53-56",
        tags=["bj", "nakshatra", "chitra", "beautiful", "aesthetic", "mars_ruled", "designer"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX107", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra — Moola (19): Born in Moola: wealthy, happy, virtuous, "
            "but causes trouble to parents (especially father). "
            "Ketu ruled. Deep spiritual/occult tendencies; root-level transformation.",
        confidence=0.83, verse="BJ Ch.12 v.73-76",
        tags=["bj", "nakshatra", "moola", "wealthy", "parent_trouble", "ketu_ruled", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX108", source="Brihat Jataka", chapter="Ch.12", school="varahamihira",
        category="nakshatra",
        description="BJ Nakshatra — Shatabhisha (24): Born in Shatabhisha: truthful, controlled, "
            "sorrowful, thoughtful, fond of solitude. "
            "Rahu ruled. Medical/healing abilities; thousand stars = thousand healing herbs. "
            "Tendency toward isolation and self-sufficiency.",
        confidence=0.83, verse="BJ Ch.12 v.93-96",
        tags=["bj", "nakshatra", "shatabhisha", "truthful", "healer", "rahu_ruled", "solitude"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX109", source="Brihat Jataka", chapter="Ch.6", school="varahamihira",
        category="graha_strength",
        description="BJ Planet in Own Nakshatra: A planet transiting or placed in its own nakshatra "
            "(the nakshatra it rules in the Vimshottari sequence) gains extra power. "
            "Called 'Nakshatra Swami Bala' — adds to natural and positional strength.",
        confidence=0.85, verse="BJ Ch.6 v.33-38",
        tags=["bj", "strength", "nakshatra_swami_bala", "own_nakshatra", "extra_power"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX110", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Budha Yoga (not Budhaditya): Mercury in Kendra with Jupiter — "
            "native is a great intellectual, advisor to rulers, mathematician. "
            "Varahamihira: Mercury-Jupiter conjunction/aspect in Kendra = counselor yoga.",
        confidence=0.85, verse="BJ Ch.11 v.53-58",
        tags=["bj", "yoga", "budha_yoga_bj", "mercury_jupiter_kendra", "counselor_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX111", source="Brihat Jataka", chapter="Ch.11", school="varahamihira",
        category="yoga",
        description="BJ Shukra-Kuja Yoga: Venus and Mars conjunct or in mutual aspect. "
            "Native is passionate, romantic, loves fine arts and sports simultaneously. "
            "Strong sexual energy; possibly multiple romantic relationships.",
        confidence=0.83, verse="BJ Ch.11 v.59-64",
        tags=["bj", "yoga", "shukra_kuja", "venus_mars", "passionate", "romantic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX112", source="Brihat Jataka", chapter="Ch.16", school="varahamihira",
        category="physical_characteristics",
        description="BJ Sign-Based Physical Characteristics (continued): "
            "Libra lagna: medium height, graceful, artistic features. "
            "Scorpio: penetrating eyes, secretive expression. "
            "Sagittarius: athletic, energetic, horse-like features (BJ: front half). "
            "Capricorn: sturdy lower body, serious expression. "
            "Aquarius: intellectual forehead, distant gaze. "
            "Pisces: soft, watery eyes, dreamy expression.",
        confidence=0.83, verse="BJ Ch.16 v.27-40",
        tags=["bj", "physical", "libra_graceful", "scorpio_penetrating", "pisces_dreamy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX113", source="Brihat Jataka", chapter="Ch.17", school="varahamihira",
        category="physical_characteristics",
        description="BJ Height and Build: Movable sign lagna = medium height, proportionate build. "
            "Fixed sign lagna = stocky, sturdy build. "
            "Dual sign lagna = tall, slender build. "
            "Strong Saturn in lagna or aspecting = thin, angular. "
            "Strong Jupiter = expansive, large.",
        confidence=0.83, verse="BJ Ch.17 v.9-16",
        tags=["bj", "physical", "height_build", "movable_medium", "fixed_stocky", "dual_tall"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX114", source="Brihat Jataka", chapter="Ch.18", school="varahamihira",
        category="wealth",
        description="BJ Varahamihira on Inheritance: 8th house and its lord show inheritance potential. "
            "Strong 8th lord in 2nd = substantial inheritance. "
            "8th lord in 12th = inheritance wasted or goes abroad. "
            "Jupiter aspecting 8th = inheritance through dharmic/legal means.",
        confidence=0.87, verse="BJ Ch.18 v.23-28",
        tags=["bj", "inheritance", "8th_lord_2nd", "jupiter_8th", "dharmic_inheritance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX115", source="Brihat Jataka", chapter="Ch.19", school="varahamihira",
        category="wealth",
        description="BJ Varahamihira on Land and Real Estate: "
            "Mars and 4th house show land/property. "
            "Mars strong in 4th or 10th = gains from real estate. "
            "Saturn in 4th delays but eventually provides property. "
            "Rahu in 4th = unusual property or foreign real estate.",
        confidence=0.85, verse="BJ Ch.19 v.15-20",
        tags=["bj", "real_estate", "mars_4th", "saturn_4th_delayed", "rahu_4th_foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX116", source="Brihat Jataka", chapter="Ch.20", school="varahamihira",
        category="female_chart",
        description="BJ Female Chart — Marriage Timing: "
            "7th lord's position from Venus determines age of marriage. "
            "Strong Venus in early degrees of its sign = early marriage. "
            "Venus in late degrees or debilitated = late marriage. "
            "Saturn aspect on Venus/7th = significant delay.",
        confidence=0.83, verse="BJ Ch.20 v.17-22",
        tags=["bj", "female_chart", "marriage_timing", "venus_degrees", "saturn_delay"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX117", source="Brihat Jataka", chapter="Ch.22", school="varahamihira",
        category="longevity",
        description="BJ Longevity Reduction Factors: Each of these reduces computed longevity: "
            "Waning Moon = 25% reduction. Combust planets = 10% per planet. "
            "Retrograde malefic in lagna = 15% reduction. "
            "These apply cumulatively to the base longevity calculation.",
        confidence=0.83, verse="BJ Ch.22 v.35-40",
        tags=["bj", "longevity", "reduction_factors", "waning_moon", "combust_reduction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX118", source="Brihat Jataka", chapter="Ch.23", school="varahamihira",
        category="death_analysis",
        description="BJ Death Place: "
            "Sun = death in government buildings, open places. "
            "Moon = death near water, at home. "
            "Mars = death in battle, on road, violent place. "
            "Mercury = near schools, communication centers. "
            "Jupiter = in religious places. "
            "Venus = bedroom, place of pleasure. "
            "Saturn = dark/isolated places, in old buildings.",
        confidence=0.83, verse="BJ Ch.23 v.23-30",
        tags=["bj", "death_place", "sun_government", "mars_battle", "saturn_dark"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX119", source="Brihat Jataka", chapter="Ch.24", school="varahamihira",
        category="dasha",
        description="BJ Dasha of Exalted Planet: Exalted planet's dasha = maximum benefic results "
            "in that planet's natural significations. "
            "Exalted planet in dusthana still gives good results during its dasha — "
            "the exaltation strength overcomes the house weakness.",
        confidence=0.88, verse="BJ Ch.24 v.33-38",
        tags=["bj", "dasha", "exalted_dasha", "maximum_benefic", "dusthana_exalted"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BJX120", source="Brihat Jataka", chapter="Ch.1", school="varahamihira",
        category="graha_nature",
        description="Varahamihira's Introduction to Jyotisha: "
            "Horoscopy (Jataka) is the branch of Jyotisha dealing with individual birth charts. "
            "An accurate birth time is essential — even a moment's error changes the chart. "
            "Varahamihira: 'As the unborn child develops in the womb, the planetary configurations "
            "at birth determine the nature of that soul's worldly manifestation.'",
        confidence=0.90, verse="BJ Ch.1 v.19-26",
        tags=["bj", "introduction", "jataka", "birth_time_accuracy", "planetary_influence"],
        implemented=False,
    ),
]

for rule in _RULES:
    BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.add(rule)
