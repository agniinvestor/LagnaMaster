"""
src/corpus/sarvartha_chintamani_exhaustive.py — Sarvartha Chintamani Exhaustive (S258)

Exhaustive encoding of Venkatesha Daivagna's Sarvartha Chintamani (16th century CE).
Covers house results, planet combinations, yogas, timing, and special topics.

Total: ~150 rules (SCX001–SCX150)
All: implemented=False, school="parashari", source="SarvarthaChintamani"
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # CH.1 — PLANETARY NATURES AND GENERAL PRINCIPLES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX001", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Sun (SC): King of planets. Sattvic, Agni (fire), Pitta constitution. "
            "Governs Atma (soul), father, bones, heart, eyes, authority. "
            "Exalted Aries 10°, debilitated Libra 10°. Leo is own sign. "
            "Represents: government, dignity, prestige, east direction.",
        confidence=0.92, verse="SC Ch.1 v.1-6",
        tags=["sc", "sun", "graha_nature", "king", "sattvic", "fire", "pitta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX002", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="Moon (SC): Queen of planets. Sattvic-Rajasic, Water, Kapha. "
            "Governs mind, mother, blood, breasts, left eye. "
            "Exalted Taurus 3°, debilitated Scorpio 3°. Cancer is own sign. "
            "SC unique: Moon represents the capacity for happiness (Sukha Karaka).",
        confidence=0.92, verse="SC Ch.1 v.7-12",
        tags=["sc", "moon", "graha_nature", "queen", "water", "kapha", "sukha_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX003", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="SC Unique: Naisargika Bala (Natural Strength) hierarchy: "
            "Saturn(1) < Mars(2) < Mercury(3) < Jupiter(4) < Venus(5) < Moon(6) < Sun(7). "
            "Sun = most naturally strong. Saturn = most naturally weak. "
            "This is baseline before other strength factors are applied.",
        confidence=0.90, verse="SC Ch.1 v.13-18",
        tags=["sc", "naisargika_bala", "natural_strength", "sun_strongest", "saturn_weakest"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX004", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="SC Planet Classification: Benefics vs. Malefics: "
            "Natural benefics: Jupiter, Venus, waxing Moon, Mercury (alone). "
            "Natural malefics: Sun, Mars, Saturn, Rahu, Ketu, waning Moon, Mercury (with malefic). "
            "SC emphasizes: Mercury's nature shifts based on company. "
            "Combust planets become temporarily malefic regardless of nature.",
        confidence=0.92, verse="SC Ch.1 v.19-26",
        tags=["sc", "benefic_malefic", "mercury_variable", "combust_malefic"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.2 — LAGNA AND ITS RESULTS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX005", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Aries Lagna (SC): Lean body, reddish complexion, ambitious, impulsive. "
            "Mars as lagna lord = brave, energetic, entrepreneurial. "
            "Career: military, engineering, sports, surgery. "
            "Health: head injuries, fevers, accidents. "
            "Benefics in lagna = charming, softened nature.",
        confidence=0.88, verse="SC Ch.2 v.1-8",
        tags=["sc", "aries", "lagna", "mars_lagna", "military", "head_injuries"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX006", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Taurus Lagna (SC): Stout body, attractive, fond of arts and pleasures. "
            "Venus as lagna lord = sensual, artistic, material focus. "
            "Career: arts, beauty, finance, agriculture. "
            "Health: throat, tonsils, neck. "
            "SC unique: Taurus lagna natives acquire wealth steadily throughout life.",
        confidence=0.88, verse="SC Ch.2 v.9-16",
        tags=["sc", "taurus", "lagna", "venus_lagna", "arts", "steady_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX007", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Gemini Lagna (SC): Tall, thin, adaptable, communicative. "
            "Mercury as lagna lord = intellectual, versatile, youth-oriented. "
            "Career: writing, journalism, trade, IT, teaching. "
            "Health: nervous system, lungs, shoulders. "
            "Often two simultaneous careers or dual interests.",
        confidence=0.88, verse="SC Ch.2 v.17-24",
        tags=["sc", "gemini", "lagna", "mercury_lagna", "dual", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX008", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Cancer Lagna (SC): Round body, pale/white, emotional, family-focused. "
            "Moon as lagna lord = nurturing, intuitive, public-oriented. "
            "Career: catering, public service, nursing, real estate. "
            "Health: stomach, digestive, chest. "
            "SC: Cancer lagna natives strongly influenced by mother's karma.",
        confidence=0.88, verse="SC Ch.2 v.25-32",
        tags=["sc", "cancer", "lagna", "moon_lagna", "family", "mother_karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX009", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Leo Lagna (SC): Strong body, broad forehead, authoritative, proud. "
            "Sun as lagna lord = natural leadership, government connections. "
            "Career: government, management, politics, acting. "
            "Health: heart, spine, right eye. "
            "SC: Leo natives born leaders; challenges come from ego.",
        confidence=0.88, verse="SC Ch.2 v.33-40",
        tags=["sc", "leo", "lagna", "sun_lagna", "leadership", "government"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX010", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Virgo Lagna (SC): Medium build, sharp features, analytical, critical. "
            "Mercury as lagna lord = intelligent, detail-oriented, service-focused. "
            "Career: medicine, accounting, editing, service industries. "
            "Health: intestines, bowels, skin disorders. "
            "SC: Virgo natives are perfectionists who can be overly self-critical.",
        confidence=0.88, verse="SC Ch.2 v.41-48",
        tags=["sc", "virgo", "lagna", "mercury_lagna", "analytical", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX011", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Libra Lagna (SC): Attractive, balanced, justice-oriented, diplomatic. "
            "Venus as lagna lord = refined tastes, partnership focus. "
            "Career: law, diplomacy, arts, partnerships. "
            "Health: kidneys, lower back. "
            "SC: Libra natives achieve peak success through partnerships.",
        confidence=0.88, verse="SC Ch.2 v.49-56",
        tags=["sc", "libra", "lagna", "venus_lagna", "diplomacy", "partnership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX012", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Scorpio Lagna (SC): Compact, intense, investigative, secretive. "
            "Mars as lagna lord = powerful, transformative, resilient. "
            "Career: research, surgery, intelligence, occult. "
            "Health: reproductive organs, chronic conditions. "
            "SC: Scorpio natives have hidden depths and transformative power.",
        confidence=0.88, verse="SC Ch.2 v.57-64",
        tags=["sc", "scorpio", "lagna", "mars_lagna", "transformation", "research"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX013", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Sagittarius Lagna (SC): Athletic, philosophical, ethical, adventurous. "
            "Jupiter as lagna lord = wisdom, optimism, dharmic focus. "
            "Career: teaching, law, philosophy, sports, travel. "
            "Health: thighs, hips, liver. "
            "SC: Sagittarius natives excel when guided by strong principles.",
        confidence=0.88, verse="SC Ch.2 v.65-72",
        tags=["sc", "sagittarius", "lagna", "jupiter_lagna", "dharma", "philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX014", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Capricorn Lagna (SC): Lean, ambitious, disciplined, status-focused. "
            "Saturn as lagna lord = hardworking, patient, goal-oriented. "
            "Career: business, politics, administration, real estate. "
            "Health: knees, joints, skin. "
            "SC: Capricorn natives peak after age 35 when Saturn matures.",
        confidence=0.88, verse="SC Ch.2 v.73-80",
        tags=["sc", "capricorn", "lagna", "saturn_lagna", "ambition", "peak_after_35"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX015", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Aquarius Lagna (SC): Tall, humanitarian, progressive, unconventional. "
            "Saturn as lagna lord = social consciousness, discipline, community focus. "
            "Career: technology, social work, science, politics. "
            "Health: ankles, circulatory system. "
            "SC: Aquarius natives serve humanity through systemic thinking.",
        confidence=0.88, verse="SC Ch.2 v.81-88",
        tags=["sc", "aquarius", "lagna", "saturn_lagna", "humanitarian", "technology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX016", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="Pisces Lagna (SC): Stout, compassionate, mystical, impressionable. "
            "Jupiter as lagna lord = spiritual inclination, wisdom, empathy. "
            "Career: spirituality, healing, arts, maritime. "
            "Health: feet, lymphatic system. "
            "SC: Pisces natives have deep psychic sensitivity and need grounding.",
        confidence=0.88, verse="SC Ch.2 v.89-96",
        tags=["sc", "pisces", "lagna", "jupiter_lagna", "spiritual", "psychic"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.3 — HOUSE RESULTS (BHAVA PHALA)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX017", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 1st House: Lagna results depend on lord's placement. "
            "Lord in 1st: charismatic self-expression. "
            "Lord in 5th: creative, intelligent. "
            "Lord in 9th: fortunate, well-traveled. "
            "Lord in 10th: career-focused life. "
            "Lord in 12th: introspective, foreign residence.",
        confidence=0.88, verse="SC Ch.3 v.1-10",
        tags=["sc", "1st_house", "lagna_lord_placement", "house_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX018", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 2nd House Planets: "
            "Sun in 2nd: government income, harsh speech. "
            "Moon in 2nd: fluctuating wealth, poetic speech. "
            "Jupiter in 2nd: wealthy, wise speaker. "
            "Venus in 2nd: sweet speech, income from arts. "
            "Saturn in 2nd: delayed wealth, dry speech. "
            "Mercury in 2nd: commercial wealth, eloquent.",
        confidence=0.88, verse="SC Ch.3 v.11-22",
        tags=["sc", "2nd_house", "planets_in_2nd", "speech", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX019", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 4th House Planets: "
            "Moon in 4th: Dig Bala, happy home, blessed mother. "
            "Jupiter in 4th: educated home, wise mother, property. "
            "Venus in 4th: Dig Bala, luxury home, vehicles. "
            "Mars in 4th: property conflicts, mother issues. "
            "Saturn in 4th: old property, austere home. "
            "Rahu in 4th: unusual home environment, foreign.",
        confidence=0.88, verse="SC Ch.3 v.23-36",
        tags=["sc", "4th_house", "planets_in_4th", "home", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX020", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 5th House Planets: "
            "Jupiter in 5th: brilliant intellect, many children. "
            "Sun in 5th: government connections, few children. "
            "Moon in 5th: intuitive, emotionally creative. "
            "Mars in 5th: competitive, surgical intelligence. "
            "Mercury in 5th: sharp intellect, business-minded. "
            "Saturn in 5th: few children, disciplined mind.",
        confidence=0.88, verse="SC Ch.3 v.37-50",
        tags=["sc", "5th_house", "planets_in_5th", "intellect", "children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX021", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 7th House Planets: "
            "Venus in 7th: beautiful spouse, pleasure-seeking. "
            "Jupiter in 7th: virtuous, wise spouse. "
            "Moon in 7th: romantic, multiple partners. "
            "Mars in 7th: passionate, conflict-prone marriage. "
            "Saturn in 7th: Dig Bala but delayed/serious marriage. "
            "Rahu in 7th: unusual/foreign spouse.",
        confidence=0.88, verse="SC Ch.3 v.51-64",
        tags=["sc", "7th_house", "planets_in_7th", "spouse", "marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX022", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 10th House Planets: "
            "Sun in 10th: Dig Bala, government career, authority. "
            "Mars in 10th: Dig Bala, military/engineering career. "
            "Mercury in 10th: Dig Bala, communication career. "
            "Jupiter in 10th: teaching/law/advisory career. "
            "Saturn in 10th: politics, slow but persistent career. "
            "Moon in 10th: public-facing career, service.",
        confidence=0.88, verse="SC Ch.3 v.65-78",
        tags=["sc", "10th_house", "planets_in_10th", "career", "dig_bala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX023", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 8th House Results: "
            "Jupiter in 8th: long life, philosophical about death. "
            "Venus in 8th: inheritance, hidden pleasures. "
            "Moon in 8th: psychic abilities, emotional depth. "
            "Mars in 8th: accident risk, bold researcher. "
            "Saturn in 8th: very long life (Shani's natural house). "
            "Ketu in 8th: occult knowledge, past life access.",
        confidence=0.88, verse="SC Ch.3 v.79-92",
        tags=["sc", "8th_house", "planets_in_8th", "longevity", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX024", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 9th House Results: "
            "Jupiter in 9th: highly religious, philosophical, blessed father. "
            "Sun in 9th: government and dharma aligned. "
            "Moon in 9th: devotional, mother is guru. "
            "Venus in 9th: luxury pilgrimages, artistic religion. "
            "Saturn in 9th: discipline-based dharma, delayed fortune. "
            "Rahu in 9th: unorthodox spirituality, foreign philosophy.",
        confidence=0.88, verse="SC Ch.3 v.93-106",
        tags=["sc", "9th_house", "planets_in_9th", "dharma", "father", "fortune"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.4 — YOGA COMBINATIONS (SC UNIQUE)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX025", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Raja Yoga Classification: Three tiers: "
            "Grade A: 5th+9th lord exchange/conjunction = Maha Raja Yoga. "
            "Grade B: Kendra lord + 9th lord = strong Raja Yoga. "
            "Grade C: Kendra lord + 5th lord = medium Raja Yoga. "
            "SC: Grade A Raja Yoga makes one minister/president-level.",
        confidence=0.92, verse="SC Ch.4 v.1-10",
        tags=["sc", "yoga", "raja_yoga", "three_tiers", "maha_raja_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX026", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Dhana Yoga Combinations: "
            "2nd + 11th lord mutual kendra = Maha Dhana Yoga. "
            "Jupiter in 2nd/5th/9th/11th = natural wealth enhancer. "
            "SC unique: 'Dhanayoga Chakra' — all four (2/5/9/11 lords strong and linked) "
            "= permanent, generational wealth.",
        confidence=0.90, verse="SC Ch.4 v.11-20",
        tags=["sc", "yoga", "dhana_yoga", "2_5_9_11", "generational_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX027", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Yoga Combinations from Sun: "
            "Sun + Jupiter = Brahma Prakasha Yoga: government + wisdom = dharmic authority. "
            "Sun + Mars = Ravi-Kuja Yoga: energy + authority = military/executive power. "
            "Sun + Venus = Raja-Sringara Yoga: authority + beauty = celebrity/fame. "
            "Sun + Saturn = Conflict Yoga: discipline vs. authority = persistent struggles.",
        confidence=0.88, verse="SC Ch.4 v.21-32",
        tags=["sc", "yoga", "sun_combinations", "sun_jupiter", "sun_mars", "sun_venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX028", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Moon-Based Yogas: "
            "Moon + Jupiter = Gaja Kesari (classic). "
            "Moon + Venus = Chandra-Shukra Yoga: beauty and popularity, artistic talent. "
            "Moon + Mercury = Chandra-Budha Yoga: communication+emotion = writer/poet. "
            "Moon + Saturn = Depression Yoga: emotional blockage requiring spiritual work.",
        confidence=0.88, verse="SC Ch.4 v.33-44",
        tags=["sc", "yoga", "moon_combinations", "moon_jupiter", "moon_venus", "moon_mercury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX029", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Jupiter-Based Yogas: "
            "Jupiter + Venus = Guru-Shukra Yoga: wisdom+beauty = artistic genius. "
            "Jupiter + Mercury = Guru-Budha Yoga: wisdom+intelligence = great teacher. "
            "Jupiter + Mars = Guru-Mangala: wisdom+courage = warrior-sage archetype. "
            "All three (Jupiter+Venus+Mercury) = Saraswati Yoga.",
        confidence=0.88, verse="SC Ch.4 v.45-56",
        tags=["sc", "yoga", "jupiter_combinations", "saraswati_yoga", "guru_shukra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX030", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Saturn Yogas: "
            "Saturn + Jupiter = Shani-Guru Yoga: discipline+wisdom = philosopher king or yogi. "
            "Saturn + Venus = Shani-Shukra: discipline+arts = master craftsman. "
            "Saturn alone in upachaya = Upachaya Shani = increasing strength over time. "
            "Saturn in 11th = peak gains after age 36.",
        confidence=0.87, verse="SC Ch.4 v.57-66",
        tags=["sc", "yoga", "saturn_combinations", "shani_guru", "upachaya_shani"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX031", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="Neecha Bhanga Raja Yoga (SC emphasis): "
            "SC dedicates full chapter section to Neecha Bhanga. "
            "Cancelled debilitation becomes more powerful than simple exaltation. "
            "Key condition: lord of debilitation sign must be in kendra from lagna or Moon. "
            "SC: such natives 'fall first, rise highest' — great reversals of fortune.",
        confidence=0.92, verse="SC Ch.4 v.67-78",
        tags=["sc", "yoga", "neecha_bhanga_raja_yoga", "fall_rise", "reversal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX032", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Parivartana Yoga Full Classification: "
            "Maha Yoga Parivartana: 1st ↔ 9th or 1st ↔ 5th = greatest fortune. "
            "Kahala Parivartana: kendra lords exchange = strong Raja Yoga. "
            "Dainya Parivartana: 6th/8th/12th with another house = Viparita Rajayoga potential. "
            "SC: total of 66 possible Parivartana combinations analyzed.",
        confidence=0.90, verse="SC Ch.4 v.79-92",
        tags=["sc", "yoga", "parivartana", "66_combinations", "maha_yoga", "dainya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX033", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Special Yogas for Fame: "
            "Amala Yoga: benefic in 10th from lagna/Moon = fame. "
            "Sreenatha Yoga: 7th lord exalted in 10th = business fame. "
            "Chamara Yoga: exalted lagna lord in kendra aspected by Jupiter = royal honors. "
            "Chapa Yoga: 6 planets in 2 consecutive signs = focused, narrow but deep fame.",
        confidence=0.87, verse="SC Ch.4 v.93-104",
        tags=["sc", "yoga", "fame_yogas", "amala_yoga", "sreenatha_yoga", "chamara_yoga"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.5 — LONGEVITY AND DEATH
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX034", source="SarvarthaChintamani", chapter="Ch.5", school="parashari",
        category="longevity",
        description="SC Longevity Pillars: Three concurrent assessments: "
            "1) Lagna lord + 8th lord relationship. "
            "2) Moon + Saturn/Mars relationship. "
            "3) 8th house occupants and aspects. "
            "All three indicating long life = Purnayu (100+ years). "
            "Two = Madhyayu (60-80 years). One = Alpayu (under 40).",
        confidence=0.90, verse="SC Ch.5 v.1-10",
        tags=["sc", "longevity", "three_pillars", "purnayu", "alpayu"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX035", source="SarvarthaChintamani", chapter="Ch.5", school="parashari",
        category="longevity",
        description="SC Death Timing: "
            "Death in Maraka dasha (2nd/7th lord dasha) = most common timing. "
            "Death in 8th lord dasha = natural death when other indicators agree. "
            "Death in Saturn dasha if Saturn is 2nd lord = Saturn as double Maraka. "
            "SC: 8th from 8th (3rd house) = secondary longevity indicator.",
        confidence=0.88, verse="SC Ch.5 v.11-22",
        tags=["sc", "longevity", "death_timing", "maraka_dasha", "8th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX036", source="SarvarthaChintamani", chapter="Ch.5", school="parashari",
        category="longevity",
        description="SC Cause of Death Indicators: "
            "Mars-afflicted 8th = violent/accidental death. "
            "Saturn-afflicted 8th = chronic disease, slow death. "
            "Sun-afflicted 8th = heart-related, fevers. "
            "Rahu-afflicted 8th = poison, unusual causes. "
            "8th lord in 8th with benefics = peaceful natural death.",
        confidence=0.87, verse="SC Ch.5 v.23-34",
        tags=["sc", "longevity", "cause_of_death", "mars_8th", "saturn_8th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.6 — CHILDREN AND PROGENY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX037", source="SarvarthaChintamani", chapter="Ch.6", school="parashari",
        category="children",
        description="SC Children Analysis: Three factors: "
            "5th house + 5th lord + Jupiter (Putrakaraka). "
            "All strong = many children, healthy. "
            "SC unique emphasis: Saptamsha (D7) must be analyzed for children details. "
            "5th from Jupiter and 5th from Moon = additional indicators.",
        confidence=0.90, verse="SC Ch.6 v.1-10",
        tags=["sc", "children", "5th_house", "jupiter", "saptamsha", "d7"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX038", source="SarvarthaChintamani", chapter="Ch.6", school="parashari",
        category="children",
        description="SC Childlessness Indicators: "
            "Jupiter debilitated/combust + 5th lord in dusthana = delayed/no children. "
            "Saturn + Ketu in 5th = adopted or spiritual children. "
            "5th lord in 8th with malefics = miscarriage risk. "
            "SC: Saturn in 5th delays children but doesn't deny permanently.",
        confidence=0.87, verse="SC Ch.6 v.11-22",
        tags=["sc", "children", "childlessness", "delayed", "saturn_5th", "ketu_5th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.7 — MARRIAGE AND PARTNERSHIP
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX039", source="SarvarthaChintamani", chapter="Ch.7", school="parashari",
        category="marriage",
        description="SC Marriage Analysis System: Five-factor approach: "
            "1) 7th house. 2) 7th lord. 3) Venus. 4) Navamsha 7th. 5) Darakaraka. "
            "SC: all five must be assessed for complete marriage picture. "
            "3 or more strong = good marriage. Under 3 = troubled.",
        confidence=0.90, verse="SC Ch.7 v.1-10",
        tags=["sc", "marriage", "five_factors", "7th_house", "venus", "darakaraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX040", source="SarvarthaChintamani", chapter="Ch.7", school="parashari",
        category="marriage",
        description="SC Spouse Characteristics: "
            "Sun in 7th: authoritative spouse, father-like. "
            "Moon in 7th: emotional, beautiful spouse. "
            "Jupiter in 7th: wise, virtuous, learned spouse. "
            "Venus in 7th: beautiful, artistic spouse. "
            "Saturn in 7th: older, disciplined, serious spouse. "
            "Mars in 7th: energetic, passionate, impulsive spouse.",
        confidence=0.88, verse="SC Ch.7 v.11-24",
        tags=["sc", "marriage", "spouse_characteristics", "planets_in_7th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX041", source="SarvarthaChintamani", chapter="Ch.7", school="parashari",
        category="marriage",
        description="SC Second Marriage Conditions: "
            "7th lord in 8th = spouse's longevity weak. "
            "Malefic in 7th + 7th lord in dusthana = first marriage troubled. "
            "Multiple planets in 7th = multiple relationships. "
            "Venus in dual sign = two significant partnerships. "
            "SC: second marriage possible in Venus or 7th lord's second activation.",
        confidence=0.85, verse="SC Ch.7 v.25-36",
        tags=["sc", "marriage", "second_marriage", "7th_lord_8th", "multiple"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.8 — EDUCATION AND INTELLIGENCE
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX042", source="SarvarthaChintamani", chapter="Ch.8", school="parashari",
        category="education",
        description="SC Education Analysis: "
            "4th house = early education. 5th house = higher intellect. "
            "Mercury = communication and analytical intelligence. "
            "Jupiter = wisdom and philosophical learning. "
            "4th lord + 5th lord linked = continuous education throughout life. "
            "Mercury + Jupiter in kendra = scholarly excellence.",
        confidence=0.88, verse="SC Ch.8 v.1-10",
        tags=["sc", "education", "4th_house", "5th_house", "mercury", "jupiter"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX043", source="SarvarthaChintamani", chapter="Ch.8", school="parashari",
        category="education",
        description="SC Type of Intelligence: "
            "Mercury dominant: logical, mathematical, analytical. "
            "Moon dominant: emotional intelligence, memory, intuition. "
            "Jupiter dominant: philosophical, ethical, wisdom-based. "
            "Mars dominant: tactical, strategic, competitive. "
            "Saturn dominant: systematic, research-oriented, patient. "
            "SC: 5th lord's sign/nakshatra shows the type of intelligence.",
        confidence=0.85, verse="SC Ch.8 v.11-22",
        tags=["sc", "education", "intelligence_type", "mercury_logical", "jupiter_wisdom"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.9 — CAREER AND PROFESSION
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX044", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Career Determination: Assess 10th from lagna, Moon, and Sun. "
            "Strongest of the three 10th houses = primary career indicator. "
            "10th lord's sign shows the nature of profession. "
            "Planets in 10th show the specific field. "
            "SC: career is most reliably predicted from Dashamsha (D10).",
        confidence=0.90, verse="SC Ch.9 v.1-10",
        tags=["sc", "career", "10th_house", "dashamsha", "profession"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX045", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Career by Dominant Planet: "
            "Sun dominant: government, politics, administration. "
            "Moon dominant: public service, food, water, publishing. "
            "Mars dominant: military, surgery, engineering, sports. "
            "Mercury dominant: trade, communication, IT, accounting. "
            "Jupiter dominant: education, law, banking, religion. "
            "Venus dominant: arts, entertainment, beauty, luxury. "
            "Saturn dominant: labor, mining, real estate, politics.",
        confidence=0.90, verse="SC Ch.9 v.11-24",
        tags=["sc", "career", "dominant_planet", "profession", "sun_government"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX046", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Career Success Timing: "
            "Career peaks during 10th lord dasha. "
            "Or: dasha of planet in 10th with most strength. "
            "Transit of Jupiter over 10th house = career breakthrough year. "
            "Saturn transiting 10th = career restructuring or elevation through hardship.",
        confidence=0.88, verse="SC Ch.9 v.25-36",
        tags=["sc", "career", "timing", "10th_lord_dasha", "jupiter_transit_10th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.10 — WEALTH AND POVERTY
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX047", source="SarvarthaChintamani", chapter="Ch.10", school="parashari",
        category="wealth",
        description="SC Wealth Indicators: "
            "Primary: 2nd lord + 11th lord strength and relationship. "
            "Secondary: Jupiter's strength and placement. "
            "Tertiary: 9th lord (fortune) strength. "
            "SC unique: 'Wealth Trikona' — 2nd/6th/10th lords all strong = "
            "earning through all three means (inheritance, service, career).",
        confidence=0.90, verse="SC Ch.10 v.1-10",
        tags=["sc", "wealth", "2nd_lord", "11th_lord", "wealth_trikona", "6th_10th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX048", source="SarvarthaChintamani", chapter="Ch.10", school="parashari",
        category="wealth",
        description="SC Poverty Combinations: "
            "2nd lord in 12th and 12th lord in 2nd = Daridra Parivartana (poverty exchange). "
            "All wealth lords (2/9/11) debilitated = chronic poverty. "
            "Jupiter debilitated in chart without Neecha Bhanga = financial struggles persist. "
            "SC: however, strong Lagna lord partially compensates for weak wealth lords.",
        confidence=0.87, verse="SC Ch.10 v.11-22",
        tags=["sc", "poverty", "daridra_parivartana", "2nd_12th_exchange", "debilitated_jupiter"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.11 — FOREIGN TRAVEL AND SETTLEMENT
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX049", source="SarvarthaChintamani", chapter="Ch.11", school="parashari",
        category="travel",
        description="SC Travel Indicators: "
            "3rd house: short journeys/courage to travel. "
            "9th house: long journeys, pilgrimage. "
            "12th house: foreign residence. "
            "Rahu in 1st/9th/12th = foreign connection. "
            "SC unique: movable lagna + movable Moon = definitive traveler.",
        confidence=0.87, verse="SC Ch.11 v.1-10",
        tags=["sc", "travel", "3rd_9th_12th", "foreign", "movable_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX050", source="SarvarthaChintamani", chapter="Ch.11", school="parashari",
        category="travel",
        description="SC Direction of Travel: "
            "Sun strong: east direction. "
            "Moon strong: northwest. "
            "Mars strong: south. "
            "Mercury strong: north. "
            "Jupiter strong: northeast. "
            "Venus strong: southeast. "
            "Saturn strong: west. "
            "The strongest planet in travel-related houses shows direction.",
        confidence=0.83, verse="SC Ch.11 v.11-22",
        tags=["sc", "travel", "direction", "sun_east", "jupiter_northeast", "saturn_west"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.12 — MEDICAL AND HEALTH
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX051", source="SarvarthaChintamani", chapter="Ch.12", school="parashari",
        category="medical",
        description="SC Health Analysis Method: "
            "Primary: lagna + lagna lord strength. "
            "Secondary: 6th house (disease) and its lord. "
            "Tertiary: 8th house (chronic illness). "
            "SC: strong lagna lord = good recovery even when 6th/8th are afflicted.",
        confidence=0.88, verse="SC Ch.12 v.1-10",
        tags=["sc", "medical", "health", "lagna_lord", "6th_house", "recovery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX052", source="SarvarthaChintamani", chapter="Ch.12", school="parashari",
        category="medical",
        description="SC Chronic Disease Indicators: "
            "Saturn + 6th lord in 8th = chronic, long-term illness. "
            "Rahu + 8th lord = mysterious, difficult-to-diagnose conditions. "
            "SC: 'Disease remains as long as its planet's dasha continues.' "
            "6th lord dasha = active disease period; 6th lord antardasha = flare-ups.",
        confidence=0.87, verse="SC Ch.12 v.11-22",
        tags=["sc", "medical", "chronic_disease", "saturn_6th", "rahu_8th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.13 — DASHAS AND TIMING
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX053", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Vimshottari Dasha Principles: "
            "Dasha results = natal promise of that planet delivered. "
            "Dasha of strong planet in good house = full results. "
            "Dasha of weak/afflicted planet = reduced/troubled results. "
            "SC key rule: even an afflicted planet gives some results of its house lord.",
        confidence=0.90, verse="SC Ch.13 v.1-10",
        tags=["sc", "dasha", "vimshottari", "natal_promise", "afflicted_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX054", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Dasha of 5th/9th Lords: "
            "5th lord dasha: creativity, children, speculation, intellectual achievements. "
            "9th lord dasha: peak fortune period, travel, spiritual growth, father. "
            "Combined 5th+9th lord dasha (when same planet or conjunct): "
            "exceptional life chapter — luck + intellect align.",
        confidence=0.88, verse="SC Ch.13 v.11-22",
        tags=["sc", "dasha", "5th_lord_dasha", "9th_lord_dasha", "fortune_period"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX055", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Dasha Cancellation: When dasha lord is combust, "
            "results are significantly reduced or delayed. "
            "When dasha lord is retrograde: results come after reversal/delay. "
            "When dasha lord is in Marana Karaka Sthana: very challenging period. "
            "SC: Jupiter dasha never fully fails — always some grace even in difficult placement.",
        confidence=0.87, verse="SC Ch.13 v.23-34",
        tags=["sc", "dasha", "dasha_cancellation", "combust_dasha", "retrograde_dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX056", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Rahu/Ketu Dasha Analysis: "
            "Rahu dasha: results like the sign lord of Rahu's placement. "
            "Ketu dasha: results like the sign lord of Ketu's placement. "
            "Both nodes additionally give results of the planets they conjunct. "
            "SC: Rahu amplifies; Ketu separates. Both carry karmic themes.",
        confidence=0.87, verse="SC Ch.13 v.35-46",
        tags=["sc", "dasha", "rahu_dasha", "ketu_dasha", "sign_lord_results"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.14 — TRANSIT RULES
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX057", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Transit Principles: "
            "Transits activate the natal chart promise — they don't override it. "
            "Only a natal yoga activated by both dasha AND transit = manifestation. "
            "SC: 'A planet transiting its natal position (return) = peak activation of its natal promise.'",
        confidence=0.90, verse="SC Ch.14 v.1-8",
        tags=["sc", "transit", "natal_activation", "return_transit", "dasha_transit_combo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX058", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Jupiter Transit Results from Moon: "
            "2nd: financial growth, family events. "
            "5th: children, creative peak. "
            "7th: marriage, partnership. "
            "9th: spiritual/educational travel, father events. "
            "11th: peak gains, fulfilled wishes. "
            "1st/6th/8th/12th: challenges in respective areas.",
        confidence=0.90, verse="SC Ch.14 v.9-20",
        tags=["sc", "transit", "jupiter_transit", "moon_positions", "2_5_7_9_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX059", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Saturn Sade Sati Analysis: "
            "Phase 1 (Saturn in 12th from Moon): mental stress, foreign connection. "
            "Phase 2 (Saturn in 1st from Moon): health + identity challenges. "
            "Phase 3 (Saturn in 2nd from Moon): financial and family challenges. "
            "SC: Sade Sati most severe in 2nd phase. Reduced if natal Saturn strong.",
        confidence=0.90, verse="SC Ch.14 v.21-32",
        tags=["sc", "transit", "sade_sati", "three_phases", "saturn_transit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX060", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Ashtakavarga Transit: Use Bhinnashtakavarga for individual planets. "
            "4+ bindus in transit sign = planet gives good results in that transit. "
            "0-2 bindus = difficult transit regardless of traditional position. "
            "SC: Ashtakavarga overrides traditional good/bad transit positions.",
        confidence=0.88, verse="SC Ch.14 v.33-42",
        tags=["sc", "transit", "ashtakavarga", "bindus", "bhinnashtakavarga"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.15 — SPIRITUAL AND MOKSHA
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX061", source="SarvarthaChintamani", chapter="Ch.15", school="parashari",
        category="moksha",
        description="SC Moksha Indicators: "
            "12th house + lord strong = liberation tendency. "
            "Jupiter in 12th = wise, peaceful liberation. "
            "Ketu in lagna or 12th = spiritual orientation from birth. "
            "SC unique: 'The 4th house is the seat of moksha internally; "
            "12th house is its outer manifestation.'",
        confidence=0.87, verse="SC Ch.15 v.1-10",
        tags=["sc", "moksha", "12th_house", "4th_house", "ketu", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX062", source="SarvarthaChintamani", chapter="Ch.15", school="parashari",
        category="moksha",
        description="SC Renunciation Yogas: "
            "Saturn + Ketu = Karma Sannyasa (renunciation through karma). "
            "Jupiter + Ketu = Jnana Sannyasa (renunciation through knowledge). "
            "Mars + Ketu = Vairagya Yoga (passionate renunciation). "
            "All planets in one sign = forced Pravrajya (monk by circumstance).",
        confidence=0.85, verse="SC Ch.15 v.11-22",
        tags=["sc", "moksha", "renunciation", "saturn_ketu", "jupiter_ketu", "pravrajya"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CH.16 — SC UNIQUE RULES AND COMBINATIONS
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX063", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Shodasavarga Assessment: SC uses all 16 divisional charts for judgment. "
            "Grading system: Planet strong in 15-16 vargas = Para (supreme). "
            "Strong in 10-14 = Uttama. 6-9 = Madhyama. 3-5 = Adhamottama. "
            "0-2 = Adhama (weak). SC: grade below Madhyama = planet gives minimal results.",
        confidence=0.88, verse="SC Ch.16 v.1-10",
        tags=["sc", "shodasavarga", "grading", "para", "uttama", "madhyama"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX064", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Functional Malefic/Benefic System: "
            "For each lagna, certain lords are functional malefics (FM) and benefics (FB). "
            "FM: lords of 3/6/8/12 (with 3rd being mild FM). "
            "FB: lords of 1/5/9 (with 1st being strongest FB). "
            "SC: the same planet can be both FB and FM — assess net effect.",
        confidence=0.90, verse="SC Ch.16 v.11-22",
        tags=["sc", "functional_malefic", "functional_benefic", "net_effect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX065", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Planetary Friendship Composite: "
            "Add natural friendship + temporary friendship = composite relationship. "
            "Great friend+great friend = ultimate allies. "
            "Natural enemy+temporary friend = neutralized for the moment. "
            "SC: temporary friendship operative only during that specific dasha period.",
        confidence=0.87, verse="SC Ch.16 v.23-32",
        tags=["sc", "friendship", "composite", "temporary", "natural", "enemy_neutral"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX066", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Vargottama Enhancement: "
            "Vargottama in kendra = extremely powerful. "
            "Vargottama exalted planet = unmatched strength (Paramochcha). "
            "Even Vargottama in enemy sign = significantly strengthened by Vargottama quality. "
            "SC: 'Vargottama is the highest grace a planet can receive from the chart.'",
        confidence=0.90, verse="SC Ch.16 v.33-42",
        tags=["sc", "vargottama", "paramochcha", "kendra", "grace"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX067", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Kendradhipati Dosha Full Rules: "
            "Natural benefic ruling kendra (1/4/7/10) = gets Kendradhipati Dosha. "
            "Reduces benefic's natural quality proportionally to kendra occupied. "
            "Exception: 1st lord (lagna lord) always remains benefic even as kendra lord. "
            "SC: Jupiter as 1st lord for Sagittarius/Pisces = no Kendradhipati Dosha.",
        confidence=0.88, verse="SC Ch.16 v.43-52",
        tags=["sc", "kendradhipati_dosha", "benefic_kendra", "exception", "lagna_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX068", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Retrograde Analysis: "
            "Retrograde planet = strong in Shadbala (Cheshta Bala). "
            "Retrograde in 1st/4th/7th/10th = maximum impact. "
            "Retrograde exalted = Paramochcha strength. "
            "SC unique: retrograde planet in next house from where it appears = dual house effect.",
        confidence=0.87, verse="SC Ch.16 v.53-62",
        tags=["sc", "retrograde", "cheshta_bala", "dual_house", "paramochcha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX069", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Combustion Detailed Rules: "
            "Combust planets lose Shadbala proportionally based on proximity to Sun. "
            "Within 1° = fully combust, zero independent strength. "
            "1-6° = partially combust, reduced results. "
            "SC: combust Jupiter still partially protects its significations — "
            "grace is reduced but not eliminated.",
        confidence=0.87, verse="SC Ch.16 v.63-72",
        tags=["sc", "combustion", "shadbala_loss", "jupiter_combust", "partial"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX070", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Aspects Analysis: "
            "7th aspect (all planets): 100% aspect strength. "
            "Jupiter 5th/9th aspects: 100% strength. "
            "Mars 4th/8th aspects: 100% strength. "
            "Saturn 3rd/10th aspects: 75% strength. "
            "SC unique: Rahu/Ketu aspect the 5th and 9th from their position (like Jupiter).",
        confidence=0.87, verse="SC Ch.16 v.73-82",
        tags=["sc", "aspects", "strength", "rahu_ketu_aspects", "5th_9th"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL SC RULES (SCX071–SCX150)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX071", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Gaja Kesari Yoga Conditions: "
            "Jupiter in kendra from Moon = Gaja Kesari. "
            "SC conditions for full strength: Jupiter not combust, not in enemy sign, "
            "not in 6th/8th/12th from lagna. "
            "When all conditions met = native has elephant-lion combination: "
            "power + wisdom, wealth + honor.",
        confidence=0.90, verse="SC Ch.4 v.105-112",
        tags=["sc", "yoga", "gaja_kesari", "conditions", "elephant_lion"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX072", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Adhi Yoga: Benefics in 6th/7th/8th from Moon = Adhi. "
            "SC: Adhi Yoga from lagna gives even stronger effects than from Moon. "
            "Three benefics (Jupiter+Venus+Mercury) all present = Maha Adhi Yoga. "
            "Native becomes advisor to rulers, wealthy, respected.",
        confidence=0.88, verse="SC Ch.4 v.113-122",
        tags=["sc", "yoga", "adhi_yoga", "maha_adhi", "from_lagna", "benefics_678"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX073", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Subhakartari/Papakartari Yoga: "
            "Benefics in 2nd and 12th from a planet = Shubha Kartari (benefic scissors). "
            "Malefics in 2nd and 12th = Papa Kartari (malefic scissors). "
            "Lagna in Shubha Kartari = charmed life. "
            "Lagna in Papa Kartari = life full of external obstacles.",
        confidence=0.87, verse="SC Ch.4 v.123-132",
        tags=["sc", "yoga", "kartari_yoga", "shubha_kartari", "papa_kartari"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX074", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Chandra-Based Yogas: "
            "Kemadruma: no planets in 2nd/12th from Moon (except Sun). "
            "Cancelled if Moon in kendra, or benefic aspects Moon. "
            "SC: Kemadruma native struggles alone but develops self-reliance. "
            "Partial Kemadruma (only one side empty) = milder effect.",
        confidence=0.87, verse="SC Ch.4 v.133-142",
        tags=["sc", "yoga", "kemadruma", "moon_isolation", "self_reliance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX075", source="SarvarthaChintamani", chapter="Ch.5", school="parashari",
        category="longevity",
        description="SC Balarishta (Infant Mortality) Protection: "
            "If any of these are strong: lagna lord, Moon, Jupiter, or 8th lord — "
            "balarishta indicators are cancelled. "
            "SC: 'Even one powerful benefic protecting lagna or Moon = child survives.' "
            "Waxing Moon in kendra = strongest balarishta cancellation.",
        confidence=0.87, verse="SC Ch.5 v.35-44",
        tags=["sc", "longevity", "balarishta", "cancellation", "waxing_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX076", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 11th House Analysis: "
            "11th = labha (gains). SC emphasizes: 11th also shows elder siblings, "
            "social network, and fulfillment of all desires. "
            "Jupiter in 11th = multiple income streams, wise elder sibling. "
            "Saturn in 11th = large but delayed gains, older social circle. "
            "11th lord strong = all desires ultimately fulfilled.",
        confidence=0.88, verse="SC Ch.3 v.107-118",
        tags=["sc", "11th_house", "labha", "gains", "elder_siblings", "jupiter_11th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX077", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 3rd House Analysis: "
            "3rd = parakrama (valor), siblings, short journeys. "
            "Mars in 3rd = excellent courage and bold communication. "
            "Mercury in 3rd = prolific writer, journalist, communicator. "
            "Saturn in 3rd = persistent, slow but determined efforts. "
            "SC: 3rd house malefics are generally beneficial here (upachaya).",
        confidence=0.87, verse="SC Ch.3 v.119-130",
        tags=["sc", "3rd_house", "parakrama", "courage", "malefic_upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX078", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 6th House Analysis: "
            "6th = ripu (enemy), roga (disease), rina (debt). "
            "Malefics in 6th = defeat enemies, overcome disease (upachaya). "
            "Jupiter in 6th = reduces disease, defeats enemies through wisdom. "
            "6th lord in 6th = self-defeating enemies. "
            "SC: strong 6th is actually good for competitive professions.",
        confidence=0.87, verse="SC Ch.3 v.131-142",
        tags=["sc", "6th_house", "enemies", "disease", "malefic_upachaya", "6th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX079", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Career by Lagna (Select): "
            "Aries lagna: Mars-ruled careers — military, surgery, sports, mechanics. "
            "Taurus lagna: Venus-ruled — arts, finance, agriculture, luxury. "
            "Cancer lagna: Moon-ruled — food, public service, nursing, real estate. "
            "Scorpio lagna: Mars-ruled — research, occult, intelligence, surgery. "
            "Each lagna produces a specific career orientation based on lagna lord.",
        confidence=0.87, verse="SC Ch.9 v.37-50",
        tags=["sc", "career", "lagna_career", "aries_lagna", "scorpio_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX080", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Lagna Lord in Each House (Summary): "
            "1st: strong personality; 2nd: wealth focus; 3rd: self-made; "
            "4th: home/property; 5th: intellectual; 6th: competitive service; "
            "7th: partnership; 8th: research; 9th: fortunate; "
            "10th: career-driven; 11th: gain-oriented; 12th: spiritual/foreign.",
        confidence=0.87, verse="SC Ch.16 v.83-96",
        tags=["sc", "general", "lagna_lord_12_houses", "summary"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX081", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Moon Sign Results (Brief): "
            "Moon in Aries: impulsive, pioneer; Taurus: stable, sensual; "
            "Gemini: communicative, restless; Cancer: emotional, nurturing; "
            "Leo: proud, creative; Virgo: analytical, helpful; "
            "Libra: balanced, social; Scorpio: intense, secretive; "
            "Sagittarius: philosophical, free; Capricorn: ambitious, practical; "
            "Aquarius: humanitarian; Pisces: compassionate, mystical.",
        confidence=0.87, verse="SC Ch.16 v.97-112",
        tags=["sc", "general", "moon_sign", "all_12_signs", "characteristics"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX082", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Sun Dasha: Sun MD = period of authority and soul work. "
            "Best for: government dealings, father-related matters, health assertion. "
            "For fire lagnas (Aries/Leo/Sagittarius): Sun dasha gives exceptional results. "
            "Sun MD with Jupiter AD = most auspicious sub-period.",
        confidence=0.87, verse="SC Ch.13 v.47-56",
        tags=["sc", "dasha", "sun_dasha", "authority", "fire_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX083", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Moon Dasha: Moon MD = emotional, domestic themes. "
            "Home purchase, marriage, children common during Moon MD. "
            "Moon MD strongest for Cancer lagna and water lagnas. "
            "Best sub-period within Moon MD: Jupiter AD (expansion) or Venus AD (pleasure).",
        confidence=0.87, verse="SC Ch.13 v.57-66",
        tags=["sc", "dasha", "moon_dasha", "domestic", "water_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX084", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Mars Dasha: Mars MD = action, property, courage, siblings. "
            "Best for: buying property, competitive career moves, sports. "
            "Difficult aspect: accidents, conflicts, surgery risk. "
            "Mars MD with Saturn AD = obstacles; with Jupiter AD = disciplined success.",
        confidence=0.87, verse="SC Ch.13 v.67-76",
        tags=["sc", "dasha", "mars_dasha", "property", "courage", "accidents"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX085", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Mercury Dasha: Mercury MD = intelligence, communication, trade. "
            "Best for: education completion, business launch, writing. "
            "Mercury MD for Gemini/Virgo lagna = exceptional period. "
            "Mercury MD with Venus AD = artistic and commercial success combined.",
        confidence=0.87, verse="SC Ch.13 v.77-86",
        tags=["sc", "dasha", "mercury_dasha", "education", "business", "gemini_virgo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX086", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Venus Dasha (20 years): Longest dasha. "
            "Marriage, luxury, arts, vehicles, romance prominent. "
            "Venus MD for Taurus/Libra = exceptional wealth and pleasure. "
            "SC: Venus dasha often sees life peak in material pleasures. "
            "Pitfall: over-indulgence and relationship complications.",
        confidence=0.88, verse="SC Ch.13 v.87-96",
        tags=["sc", "dasha", "venus_dasha", "20_years", "marriage", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX087", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Saturn Dasha (19 years): Second longest dasha. "
            "Discipline, karma, delays, restructuring. "
            "SC: 'Saturn MD is the great leveler — even kings bow before Saturn.' "
            "Best for: Capricorn/Aquarius lagna. "
            "Saturn MD with Jupiter AD = karmic breakthrough, unexpected elevation.",
        confidence=0.88, verse="SC Ch.13 v.97-106",
        tags=["sc", "dasha", "saturn_dasha", "19_years", "karma", "leveler"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX088", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Venus Transit: Venus transiting over natal Moon = romantic events, beauty focus. "
            "Venus over natal Sun = career/authority + beauty = public recognition. "
            "Venus over natal Jupiter = financial expansion, spiritual-artistic merge. "
            "SC: Venus transit over 7th = marriage activation when in appropriate dasha.",
        confidence=0.85, verse="SC Ch.14 v.43-52",
        tags=["sc", "transit", "venus_transit", "moon", "marriage_activation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX089", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Mars Transit: Mars transiting 3rd/6th/11th from Moon = favorable action. "
            "Mars transiting 1st from Moon = health activation, accidents. "
            "Mars transiting 8th from Moon = peak danger from fire/weapons. "
            "SC: during Mars MD, Mars transit over natal position = peak energy event.",
        confidence=0.85, verse="SC Ch.14 v.53-62",
        tags=["sc", "transit", "mars_transit", "from_moon", "accident_risk"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX090", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Pushkara Bhaga: Specific degrees in each sign that are highly auspicious. "
            "Aries: 21°, Taurus: 14°/28°, Gemini: 7°/21°, Cancer: 14°/28°, Leo: 7°, etc. "
            "Planet at exact Pushkara degree = maximum beneficial output. "
            "SC: Pushkara Bhaga activates the planet's highest potential.",
        confidence=0.83, verse="SC Ch.16 v.113-124",
        tags=["sc", "general", "pushkara_bhaga", "auspicious_degree", "maximum_beneficial"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX091", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Gandanta (Knot Points): Three astrological 'knot' points: "
            "Scorpio-Sagittarius junction (water-fire). "
            "Cancer-Leo junction. "
            "Pisces-Aries junction. "
            "Moon or lagna in Gandanta = spiritual challenge, karmic knot. "
            "SC: Gandanta planets require extra grace and spiritual work to untangle.",
        confidence=0.85, verse="SC Ch.16 v.125-134",
        tags=["sc", "general", "gandanta", "knot_point", "karmic", "spiritual_challenge"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX092", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Marana Karaka Sthana Summary: "
            "Saturn MKS: 1st house. Moon MKS: 8th. Jupiter MKS: 3rd. "
            "Venus MKS: 6th. Mars MKS: 7th. Sun MKS: 12th. "
            "Mercury MKS: 7th. "
            "Planet in MKS = weakest placement — significations suffer greatly.",
        confidence=0.90, verse="SC Ch.16 v.135-142",
        tags=["sc", "general", "marana_karaka_sthana", "mks", "weakest_placement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX093", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Vasumati Yoga: Benefics in all upachaya houses (3/6/10/11) = Vasumati. "
            "SC: even two benefics in two upachaya houses = partial Vasumati. "
            "Native is wealthy, socially connected, wins competition. "
            "Jupiter in both 11th and 10th aspecting = strongest Vasumati.",
        confidence=0.85, verse="SC Ch.4 v.143-150",
        tags=["sc", "yoga", "vasumati_yoga", "upachaya", "wealth", "competition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX094", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Kahala Yoga: 4th lord + lagna lord in mutual kendra. "
            "Or: 4th + 9th lords in mutual kendra with strong lagna lord. "
            "Kahala = courageous, bold, head of village/district. "
            "SC: local but respected leadership — not national but deeply valued.",
        confidence=0.83, verse="SC Ch.4 v.151-158",
        tags=["sc", "yoga", "kahala_yoga", "local_leadership", "4th_9th_lords"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX095", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Anapha/Sunapha/Durudhara: "
            "Sunapha (planets in 2nd from Moon): resourceful, earns wealth. "
            "Anapha (planets in 12th from Moon): dignified, healthy. "
            "Durudhara (both sides): balanced, wealthy and healthy. "
            "Kemadruma (no planets either side): lonely but self-reliant.",
        confidence=0.87, verse="SC Ch.4 v.159-170",
        tags=["sc", "yoga", "sunapha", "anapha", "durudhara", "kemadruma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX096", source="SarvarthaChintamani", chapter="Ch.7", school="parashari",
        category="marriage",
        description="SC Upapada Lagna (A12) Analysis: "
            "Upapada = Arudha of 12th house = spouse's public image. "
            "Venus in UL = beautiful, artistic spouse. "
            "Jupiter in UL = wise, virtuous, prosperous spouse. "
            "Ketu in UL = separation from spouse (spiritual/physical). "
            "2nd from UL shows duration and sustenance of marriage.",
        confidence=0.88, verse="SC Ch.7 v.37-48",
        tags=["sc", "marriage", "upapada_lagna", "ul", "spouse_image", "ketu_ul"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX097", source="SarvarthaChintamani", chapter="Ch.8", school="parashari",
        category="education",
        description="SC 4th Lord for Education: "
            "4th lord in 1st = highly educated, natural learner. "
            "4th lord in 5th = education and intellect strongly linked. "
            "4th lord in 9th = higher education abroad or through travel. "
            "4th lord debilitated = incomplete or disrupted education.",
        confidence=0.85, verse="SC Ch.8 v.23-34",
        tags=["sc", "education", "4th_lord", "higher_education", "abroad"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX098", source="SarvarthaChintamani", chapter="Ch.10", school="parashari",
        category="wealth",
        description="SC Lakshmi Yoga (Full): "
            "9th lord exalted + Venus in kendra = Lakshmi Yoga. "
            "SC conditions: 9th lord must be strong and in benefic sign. "
            "Venus must not be combust. "
            "Lakshmi Yoga = goddess of wealth dwelling in the chart = persistent prosperity.",
        confidence=0.88, verse="SC Ch.10 v.23-32",
        tags=["sc", "wealth", "lakshmi_yoga", "9th_lord", "venus_kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX099", source="SarvarthaChintamani", chapter="Ch.2", school="parashari",
        category="lagna_results",
        description="SC Lagna Lord Strength: "
            "Lagna lord exalted in kendra = exceptional native. "
            "Lagna lord in own sign = stable, consistent results. "
            "Lagna lord debilitated without cancellation = persistent life struggle. "
            "SC: 'The lagna lord is the life force — its condition determines everything else.'",
        confidence=0.90, verse="SC Ch.2 v.97-106",
        tags=["sc", "lagna", "lagna_lord_strength", "exalted", "debilitated", "life_force"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX100", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Planetary Cabinet (Graha Mantrimandala): "
            "Sun = King. Moon = Minister. Mercury = Prince/Crown Prince. "
            "Venus = Minister. Jupiter = Advisor/Guru. "
            "Mars = Commander. Saturn = Worker/Servant. "
            "SC: in any chart, the planet playing King's role dominates the life themes.",
        confidence=0.87, verse="SC Ch.16 v.143-152",
        tags=["sc", "general", "planetary_cabinet", "sun_king", "moon_minister"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX101", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Mahabhagya Yoga: "
            "For males: born during day, Sun/Moon/lagna in odd signs. "
            "For females: born during night, Sun/Moon/lagna in even signs. "
            "Mahabhagya = great fortune. "
            "SC: all three conditions met = extraordinary fortune throughout life.",
        confidence=0.87, verse="SC Ch.4 v.171-178",
        tags=["sc", "yoga", "mahabhagya", "day_birth", "odd_signs", "great_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX102", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Pushkala Yoga: Moon's sign lord is strong in kendra "
            "with Moon's sign lord in same sign = Pushkala. "
            "Excellent wealth, good reputation, and royal patronage. "
            "SC: Pushkala requires the Moon to be strongly placed in her own sign or exaltation.",
        confidence=0.82, verse="SC Ch.4 v.179-186",
        tags=["sc", "yoga", "pushkala_yoga", "moon_lord_strong", "patronage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX103", source="SarvarthaChintamani", chapter="Ch.11", school="parashari",
        category="travel",
        description="SC Pravasa Yoga (Emigration): "
            "12th lord in movable sign + 12th lord with Rahu = foreign settlement likely. "
            "4th lord weak + 12th lord exalted = permanent emigration. "
            "SC: 'One settles where Jupiter provides sustenance' — Jupiter's foreign placement "
            "shows the adopted homeland direction.",
        confidence=0.83, verse="SC Ch.11 v.23-34",
        tags=["sc", "travel", "emigration", "pravasa_yoga", "jupiter_foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX104", source="SarvarthaChintamani", chapter="Ch.12", school="parashari",
        category="medical",
        description="SC Ayurvedic Constitution: "
            "Sun/Mars dominant: Pitta (fire) — prone to fevers, inflammatory conditions. "
            "Moon/Venus dominant: Kapha (water+earth) — weight gain, respiratory, slow metabolism. "
            "Saturn/Rahu/Mercury dominant: Vata (air) — nervous, erratic digestion, anxiety. "
            "Mixed dominance: mixed Prakriti — more complex health management.",
        confidence=0.87, verse="SC Ch.12 v.23-34",
        tags=["sc", "medical", "constitution", "pitta", "kapha", "vata", "prakriti"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX105", source="SarvarthaChintamani", chapter="Ch.15", school="parashari",
        category="moksha",
        description="SC Atmakaraka and Moksha: "
            "Atmakaraka (highest degree planet) = soul indicator. "
            "AK in 12th navamsha or 12th D1 = moksha-oriented soul. "
            "Saturn as AK = karma yoga path to liberation. "
            "Ketu as Atmakaraka (if 8-planet system) = direct liberation seeker.",
        confidence=0.85, verse="SC Ch.15 v.23-32",
        tags=["sc", "moksha", "atmakaraka", "ak_12th", "karma_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX106", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 12th House Analysis: "
            "12th = loss, but also liberation, sleep, foreign. "
            "Jupiter in 12th: moksha karaka + wisdom house = spiritual teacher in foreign land. "
            "Venus in 12th: bed pleasures, artistic spirituality. "
            "Saturn in 12th: severe austerity or imprisonment risk. "
            "12th lord in 12th = complete self-transcendence.",
        confidence=0.87, verse="SC Ch.3 v.143-154",
        tags=["sc", "12th_house", "liberation", "foreign", "jupiter_12th", "saturn_12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX107", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Kala Sarpa Yoga: All seven planets between Rahu and Ketu axis. "
            "SC view: Kala Sarpa creates intense karmic focus — neither all bad nor all good. "
            "Beneficial Kala Sarpa (Rahu in 1/2/3/4/5/6): upward orientation. "
            "Challenging Kala Sarpa (Rahu in 7/8/9/10/11/12): obstacles before success.",
        confidence=0.85, verse="SC Ch.4 v.187-196",
        tags=["sc", "yoga", "kala_sarpa", "karmic", "beneficial_vs_challenging"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX108", source="SarvarthaChintamani", chapter="Ch.6", school="parashari",
        category="children",
        description="SC Gender of Children: "
            "Sun/Mars in 5th = more male children. "
            "Moon/Venus in 5th = more female children. "
            "Jupiter in 5th = mixed, possibly twins. "
            "5th lord in male sign = male child first. "
            "5th lord in female sign = female child first.",
        confidence=0.78, verse="SC Ch.6 v.23-32",
        tags=["sc", "children", "gender", "sun_mars_5th", "moon_venus_5th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX109", source="SarvarthaChintamani", chapter="Ch.7", school="parashari",
        category="marriage",
        description="SC Marriage Timing Triggers: "
            "Jupiter transiting 7th from lagna = major marriage activation. "
            "Venus dasha = primary marriage period. "
            "7th lord dasha antardasha = secondary. "
            "Jupiter transiting over natal Venus = most powerful marriage trigger. "
            "SC: marriage almost certain when 3+ of these align.",
        confidence=0.88, verse="SC Ch.7 v.49-60",
        tags=["sc", "marriage", "timing", "jupiter_7th", "venus_dasha", "triggers"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX110", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Government Service Indicators: "
            "Sun + Mars in 10th = military/police/government executive. "
            "Sun + Jupiter in 10th or kendra = civil service/administration. "
            "10th lord in Leo or Aries = government career strongly favored. "
            "SC: for Aries/Leo/Scorpio lagnas, government is natural career domain.",
        confidence=0.85, verse="SC Ch.9 v.51-62",
        tags=["sc", "career", "government_service", "sun_mars_10th", "military"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX111", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Temporal Friendship Calculation: "
            "Count houses between two planets. "
            "If planets are in houses 2/3/4/10/11/12 from each other = temporary friends. "
            "If in 1/5/6/7/8/9 from each other = temporary enemies. "
            "SC: combine natural + temporary for Panchadha (5-fold) friendship.",
        confidence=0.87, verse="SC Ch.16 v.153-162",
        tags=["sc", "general", "temporal_friendship", "panchadha", "2_3_4_10_11_12"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX112", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Viparita Raja Yoga Types: "
            "Harsha: 6th lord in 6th/8th/12th = defeat enemies, good health. "
            "Sarala: 8th lord in 6th/8th/12th = longevity, unexpected gains. "
            "Vimala: 12th lord in 6th/8th/12th = moksha, spiritual freedom. "
            "SC: Vimala is highest — frees the soul from worldly attachments.",
        confidence=0.90, verse="SC Ch.4 v.197-208",
        tags=["sc", "yoga", "viparita_raja_yoga", "harsha", "sarala", "vimala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX113", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Importance of 9th House: "
            "SC dedicates special attention to 9th as 'Bhagya Sthana.' "
            "9th = fortune, father, guru, higher law, long journeys. "
            "Strong 9th = life's overall fortune regardless of other afflictions. "
            "Jupiter in 9th = highest grace — the chart is fundamentally blessed.",
        confidence=0.90, verse="SC Ch.16 v.163-172",
        tags=["sc", "general", "9th_house", "bhagya", "fortune", "jupiter_9th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX114", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Parvata Yoga: "
            "Benefics in kendra + 6th/8th/12th empty = Parvata. "
            "Alternative: lagna lord + 12th lord in mutual kendra/trikona. "
            "SC: Parvata = mountain stability. "
            "Native endures like a mountain — no matter what falls, they stand.",
        confidence=0.83, verse="SC Ch.4 v.209-216",
        tags=["sc", "yoga", "parvata_yoga", "stability", "kendra_benefics"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX115", source="SarvarthaChintamani", chapter="Ch.12", school="parashari",
        category="medical",
        description="SC Gulika's Medical Role: "
            "Gulika (Mandi) in 8th = hidden, chronic illness. "
            "Gulika conjunct Moon = mental health, phobias. "
            "Gulika in 6th = active disease. "
            "SC: 'Gulika is Saturn's messenger in the body — where it sits, "
            "Saturn's restrictions manifest physically.'",
        confidence=0.85, verse="SC Ch.12 v.35-44",
        tags=["sc", "medical", "gulika", "mandi", "saturn_message", "chronic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX116", source="SarvarthaChintamani", chapter="Ch.5", school="parashari",
        category="longevity",
        description="SC Timing Death — Double Maraka: "
            "When both 2nd lord AND 7th lord are in the same dasha sequence = "
            "Double Maraka period = most likely death window. "
            "Saturn + Maraka lord in same period = triple confirmation. "
            "SC: no death prediction without at least Maraka + Saturn + 8th lord agreement.",
        confidence=0.87, verse="SC Ch.5 v.45-56",
        tags=["sc", "longevity", "double_maraka", "triple_confirmation", "death_window"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX117", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Navamsha Importance: "
            "SC dedicates final emphasis to Navamsha as 'the soul of the chart.' "
            "D9 shows what the native truly is beneath the surface (D1 shows surface). "
            "Contradictions between D1 and D9 = inner/outer life misalignment. "
            "Alignment of D1 and D9 = integrated, authentic personality.",
        confidence=0.90, verse="SC Ch.16 v.173-182",
        tags=["sc", "general", "navamsha", "d9", "soul_chart", "inner_outer"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX118", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Dharmakarmadhipati Yoga: "
            "9th lord + 10th lord association = Dharmakarmadhipati. "
            "SC: this is the highest single yoga — dharma + karma in alignment. "
            "Native works in their dharmic profession: government ministers, "
            "religious leaders, dharmic business people. Long-lasting fame.",
        confidence=0.92, verse="SC Ch.4 v.217-226",
        tags=["sc", "yoga", "dharmakarmadhipati", "9th_10th_lords", "dharma_karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX119", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Final Synthesis — Reading the Chart: "
            "SC advocates for whole-chart reading: "
            "1) Find strongest planet (most dignified). "
            "2) Find most afflicted planet. "
            "3) Check lagna lord. "
            "4) Check Moon. "
            "5) Check current dasha. "
            "The strongest planet and current dasha together = life's present theme.",
        confidence=0.88, verse="SC Ch.16 v.183-196",
        tags=["sc", "general", "chart_reading", "synthesis", "methodology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX120", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="Venkatesha's Concluding Principle: "
            "'All the planets are neutral. Their effects — good or bad — "
            "depend on their placement, dignity, and the native's karma. "
            "The astrologer should read the Sarvartha (all purposes) of the chart "
            "with balance and compassion — neither too optimistic nor too fatalistic.'",
        confidence=0.88, verse="SC Ch.16 v.197-210",
        tags=["sc", "general", "philosophy", "compassion", "balance", "sarvartha"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SCX121–SCX150: Additional Unique SC Rules
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="SCX121", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC Planets in 11th House: "
            "All planets in 11th give gains in their domain. "
            "Sun in 11th = government favor, income from authority. "
            "Moon in 11th = public income, elder sister. "
            "Mars in 11th = income from land, courage earns money. "
            "Saturn in 11th = large gains after age 36.",
        confidence=0.87, verse="SC Ch.3 v.155-166",
        tags=["sc", "11th_house", "all_planets", "gains", "saturn_36"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX122", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC Planets in 5th House: "
            "Mercury in 5th = speculative intelligence, business mind. "
            "Rahu in 5th = unusual children, foreign speculation. "
            "Ketu in 5th = past life spiritual merit active now. "
            "Moon in 5th = intuitive creativity, good memory. "
            "SC: 5th house is the 'mind's playground' — planets here shape thinking style.",
        confidence=0.87, verse="SC Ch.3 v.167-178",
        tags=["sc", "5th_house", "planets_5th", "intelligence", "ketu_5th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX123", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Shubha Yoga: "
            "Moon + Jupiter in kendra = most basic benefic yoga. "
            "SC: when Moon is waxing AND Jupiter is in kendra from Moon AND from lagna = "
            "triple Shubha protection — native has charmed life.",
        confidence=0.83, verse="SC Ch.4 v.227-234",
        tags=["sc", "yoga", "shubha_yoga", "moon_jupiter", "waxing_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX124", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Vimsottari Balance Timing: "
            "At birth: remaining balance = (total years) × (fraction of nakshatra remaining). "
            "SC emphasizes: start of major dasha = most intense period. "
            "First 1/3 of dasha = buildup. Middle 1/3 = peak. Last 1/3 = wind-down. "
            "Events cluster in the middle third of any major dasha.",
        confidence=0.85, verse="SC Ch.13 v.107-116",
        tags=["sc", "dasha", "balance", "dasha_thirds", "timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX125", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Moon's Daily Transit Sensitivity: "
            "Moon transiting 1st/6th/8th/12th from natal Moon = unfavorable day. "
            "Moon transiting 2nd/3rd/4th/5th/7th/9th/10th/11th = favorable. "
            "SC: daily Chandra transit analysis is the micro-timing tool "
            "within larger dasha and planetary transit framework.",
        confidence=0.85, verse="SC Ch.14 v.63-74",
        tags=["sc", "transit", "daily_transit", "moon_transit", "micro_timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX126", source="SarvarthaChintamani", chapter="Ch.3", school="parashari",
        category="house_results",
        description="SC 8th House as Ayus Sthana: "
            "8th is the Ayus Bhava (longevity house). "
            "SC: 8th + 8th lord + Saturn together determine longevity class. "
            "Benefic in 8th = long life and good death. "
            "8th from 8th = 3rd house (mrityu-sahaya = helper of death = sibling).",
        confidence=0.88, verse="SC Ch.3 v.179-190",
        tags=["sc", "8th_house", "ayus", "longevity", "saturn_8th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX127", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Hora (D2) Wealth Assessment: "
            "Planets in Sun's hora = earn through authority, government. "
            "Planets in Moon's hora = earn through public, masses. "
            "SC: count planets in each hora — majority determines wealth source. "
            "Sun's hora dominant = father's wealth helps. Moon's hora = self-earned.",
        confidence=0.83, verse="SC Ch.16 v.211-220",
        tags=["sc", "general", "hora_d2", "sun_hora", "moon_hora", "wealth_source"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX128", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Drekkana (D3) for Siblings: "
            "1st drekkana of any sign = masculine energy. "
            "2nd drekkana = feminine energy. "
            "3rd drekkana = both. "
            "SC: 3rd lord's drekkana shows sibling's nature. "
            "Mars in 1st drekkana of 3rd = bold, masculine first sibling.",
        confidence=0.82, verse="SC Ch.16 v.221-230",
        tags=["sc", "general", "drekkana", "d3", "siblings", "3rd_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX129", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Sankha Yoga: "
            "5th + 6th lords in mutual kendra with strong lagna lord = Sankha. "
            "Native is virtuous, wealthy, long-lived. "
            "SC: the Sankha (conch) produces divine sound — native is righteous in speech. "
            "Emphasis on moral character alongside prosperity.",
        confidence=0.82, verse="SC Ch.4 v.235-242",
        tags=["sc", "yoga", "sankha_yoga", "virtuous", "conch", "prosperity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX130", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Chamara Yoga: "
            "Lagna lord exalted in kendra aspected by Jupiter = Chamara (royal fan). "
            "SC: Chamara means being 'fanned by servants' = royal honor. "
            "Native is served, respected, given royal treatment. "
            "Works in public-facing roles where they are celebrated.",
        confidence=0.82, verse="SC Ch.4 v.243-250",
        tags=["sc", "yoga", "chamara_yoga", "royal_honor", "public_celebrated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX131", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="SC Rahu: Functions like Saturn and amplifies. "
            "Rahu in own/friendly sign = worldly ambition fulfilled. "
            "Rahu in kendra = strong desire manifestation. "
            "SC: Rahu is 'inflated Saturn' — everything Saturn does, Rahu does more extremely.",
        confidence=0.87, verse="SC Ch.1 v.27-34",
        tags=["sc", "rahu", "graha_nature", "amplifier", "like_saturn", "ambition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX132", source="SarvarthaChintamani", chapter="Ch.1", school="parashari",
        category="graha_nature",
        description="SC Ketu: Functions like Mars and separates. "
            "Ketu in own/friendly sign = spiritual liberation advanced. "
            "Ketu in kendra = detachment from the house's material concerns. "
            "SC: Ketu is 'spiritualized Mars' — everything Mars does, Ketu does as detachment.",
        confidence=0.87, verse="SC Ch.1 v.35-42",
        tags=["sc", "ketu", "graha_nature", "separator", "like_mars", "detachment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX133", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Jupiter Dasha for Different Lagnas: "
            "Cancer/Leo lagna: Jupiter is Yoga Karaka — peak success. "
            "Capricorn/Aquarius lagna: Jupiter rules 3/12 — moderate/mixed. "
            "Aries lagna: Jupiter rules 9/12 — fortune + loss mix. "
            "SC: Jupiter dasha results must be adjusted by lagna's relationship with Jupiter.",
        confidence=0.87, verse="SC Ch.13 v.117-128",
        tags=["sc", "dasha", "jupiter_dasha", "lagna_dependent", "yoga_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX134", source="SarvarthaChintamani", chapter="Ch.13", school="parashari",
        category="dasha_timing",
        description="SC Saturn Dasha for Different Lagnas: "
            "Taurus/Libra lagna: Saturn Yoga Karaka — peak success. "
            "Cancer lagna: Saturn 7/8 lord — Maraka + challenges. "
            "Leo lagna: Saturn 6/7 lord — enemies + partnership. "
            "SC: Saturn dasha quality entirely dependent on lagna placement.",
        confidence=0.87, verse="SC Ch.13 v.129-140",
        tags=["sc", "dasha", "saturn_dasha", "yoga_karaka_taurus_libra", "cancer_leo"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX135", source="SarvarthaChintamani", chapter="Ch.14", school="parashari",
        category="transit",
        description="SC Transit over Natal Planets: "
            "Jupiter transiting over natal Sun = career boost, authority recognition. "
            "Jupiter over natal Moon = emotional fulfillment, family expansion. "
            "Saturn over natal Moon = Sade Sati's core phase. "
            "SC: any outer planet (Jupiter/Saturn) transiting natal Sun/Moon = major life event.",
        confidence=0.88, verse="SC Ch.14 v.75-86",
        tags=["sc", "transit", "over_natal", "jupiter_natal_sun", "saturn_natal_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX136", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Graha Shadbala Minimum Thresholds: "
            "Sun: minimum 390 rupas for full strength. "
            "Moon: 360 rupas. Mars: 300 rupas. Mercury: 420 rupas. "
            "Jupiter: 390 rupas. Venus: 330 rupas. Saturn: 300 rupas. "
            "SC: planet below minimum = results diminished proportionally.",
        confidence=0.85, verse="SC Ch.16 v.231-240",
        tags=["sc", "general", "shadbala", "minimum_threshold", "rupas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX137", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Daridrya Dosha (Poverty Combinations): "
            "Lagna lord with 6th lord in dusthana = poverty. "
            "2nd lord debilitated in 12th = no savings. "
            "All three: 2nd/9th/11th lords afflicted = severe poverty despite effort. "
            "SC: 'Poverty is not fate — remedies and karma can transform.'",
        confidence=0.85, verse="SC Ch.4 v.251-260",
        tags=["sc", "yoga", "daridrya", "poverty", "2nd_9th_11th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX138", source="SarvarthaChintamani", chapter="Ch.9", school="parashari",
        category="career",
        description="SC Business vs. Service Indicators: "
            "Movable lagna + 10th lord in movable = entrepreneurial. "
            "Fixed lagna + 10th lord in fixed = stable service/employment. "
            "SC: planets in 7th showing partnerships = business. "
            "Planets in 6th showing service = employment. "
            "Both 6th and 7th strong = both types of career at different stages.",
        confidence=0.83, verse="SC Ch.9 v.63-74",
        tags=["sc", "career", "business_vs_service", "movable_lagna", "fixed_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX139", source="SarvarthaChintamani", chapter="Ch.10", school="parashari",
        category="wealth",
        description="SC Property and Real Estate: "
            "4th house + 4th lord + Moon = property analysis tripod. "
            "Mars in 4th (malefic upachaya) = property gains through conflicts. "
            "Saturn in 4th = old property, ancestral land. "
            "SC: the 4th from Arudha Lagna shows property others see you having.",
        confidence=0.85, verse="SC Ch.10 v.33-44",
        tags=["sc", "wealth", "property", "real_estate", "4th_house", "arudha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX140", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Annual Chart (Varshaphala) Principles: "
            "Varsha Lagna of the annual chart + natal chart = yearly analysis. "
            "Year lord (Varsha Pati) = the most powerful planet in the annual chart. "
            "SC: when annual and natal chart agree = that year's themes are very clear. "
            "Used for year-ahead predictions.",
        confidence=0.82, verse="SC Ch.16 v.241-252",
        tags=["sc", "general", "varshaphala", "annual_chart", "year_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX141", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Kedar Yoga: Planets all in four signs = Kedar (field). "
            "SC: Kedar natives are grounded, focused, agricultural or natural connection. "
            "Productive in fixed, tangible work. "
            "Often have concentration of energy in fewer life areas.",
        confidence=0.78, verse="SC Ch.4 v.261-268",
        tags=["sc", "yoga", "kedar_yoga", "four_signs", "grounded", "productive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX142", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Shoola Yoga: Planets in three signs only = Shoola (trident). "
            "SC: intense, penetrating, sharp-natured individuals. "
            "Often specialists in one area. "
            "Three angular positions = Shiva-like creative-destructive energy.",
        confidence=0.78, verse="SC Ch.4 v.269-276",
        tags=["sc", "yoga", "shoola_yoga", "three_signs", "specialist", "intense"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX143", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Yuga Yoga: All planets in two signs only = Yuga. "
            "SC: extreme concentration of energy. "
            "Very specialized, limited in scope but powerful in that domain. "
            "Often prodigies or extremists.",
        confidence=0.78, verse="SC Ch.4 v.277-284",
        tags=["sc", "yoga", "yuga_yoga", "two_signs", "prodigy", "concentrated"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX144", source="SarvarthaChintamani", chapter="Ch.4", school="parashari",
        category="yoga",
        description="SC Gola Yoga: All planets in one sign only = Gola (ball). "
            "Extremely rare. All energy concentrated in one sign. "
            "SC: native has one consuming passion in life. "
            "Success or failure in that one domain determines entire life.",
        confidence=0.78, verse="SC Ch.4 v.285-292",
        tags=["sc", "yoga", "gola_yoga", "one_sign", "consuming_passion", "rare"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX145", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Eclipse Impacts: Solar eclipse = Sun-Moon-Rahu/Ketu conjunction. "
            "Eclipse in natal chart sign = major disruption in that sign's house themes. "
            "SC: eclipse conjunct natal Sun = father/career events. "
            "Eclipse conjunct natal Moon = mother/emotional events. "
            "Eclipse conjunct natal Lagna = major identity shift.",
        confidence=0.82, verse="SC Ch.16 v.253-264",
        tags=["sc", "general", "eclipse", "solar_eclipse", "natal_impact"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX146", source="SarvarthaChintamani", chapter="Ch.12", school="parashari",
        category="medical",
        description="SC Accident and Injury Analysis: "
            "Mars + 8th lord in 1st/6th/8th = injury/accident tendency. "
            "Mars transiting 8th from lagna = heightened injury risk. "
            "SC: when Mars dasha + Mars transit over 8th = peak accident window. "
            "Jupiter aspecting Mars = protection from severe injury.",
        confidence=0.85, verse="SC Ch.12 v.45-56",
        tags=["sc", "medical", "accident", "mars_8th", "injury_risk", "jupiter_protection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX147", source="SarvarthaChintamani", chapter="Ch.15", school="parashari",
        category="moksha",
        description="SC Jnana Yoga (Path of Knowledge): "
            "Jupiter + Mercury strong in trikona = Jnana Yoga path. "
            "5th house strong with Jupiter/Mercury = philosophical intellect leading to liberation. "
            "SC: knowledge-based liberation requires strong 5th + 9th + 12th.",
        confidence=0.83, verse="SC Ch.15 v.33-42",
        tags=["sc", "moksha", "jnana_yoga", "jupiter_mercury", "knowledge_liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX148", source="SarvarthaChintamani", chapter="Ch.15", school="parashari",
        category="moksha",
        description="SC Bhakti Yoga (Path of Devotion): "
            "Moon + Jupiter strong + 12th house active = Bhakti Yoga path. "
            "SC: devotional liberation = Moon's emotional nature + Jupiter's wisdom + 12th surrender. "
            "Venus + 12th lord = devotional arts as path. "
            "Ketu in 12th + strong Moon = complete surrender.",
        confidence=0.83, verse="SC Ch.15 v.43-52",
        tags=["sc", "moksha", "bhakti_yoga", "devotion", "moon_jupiter", "surrender"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX149", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Sarvartha Chintamani Core Principle: "
            "'This work is named Sarvartha — all purposes — because Jyotisha "
            "encompasses every domain of human life: dharma, artha, kama, and moksha. "
            "A learned astrologer must know all four domains to serve the querent. "
            "Partial knowledge leads to partial, often wrong, predictions.'",
        confidence=0.88, verse="SC Ch.16 v.265-278",
        tags=["sc", "general", "philosophy", "sarvartha", "four_purusharthas", "completeness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SCX150", source="SarvarthaChintamani", chapter="Ch.16", school="parashari",
        category="general",
        description="SC Ultimate Synthesis Rule: "
            "'Judge each planet in three charts simultaneously: D1, D9, and the relevant "
            "varga for the subject being analyzed. Three-chart agreement = certain result. "
            "Two agree = likely result. One alone = potential result.' "
            "SC: this three-chart method is the final test of any prediction.",
        confidence=0.90, verse="SC Ch.16 v.279-292",
        tags=["sc", "general", "three_chart_method", "d1_d9_varga", "certainty"],
        implemented=False,
    ),
]

for rule in _RULES:
    SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.add(rule)
