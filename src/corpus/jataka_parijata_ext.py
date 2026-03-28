"""
src/corpus/jataka_parijata_ext.py — Jataka Parijata Extended Rules (S241)

Encodes Vaidyanatha Dikshita's Jataka Parijata (14th century CE) unique
rules and interpretations not covered in BPHS.

Sources:
  Jataka Parijata (Vaidyanatha Dikshita) — Chapters 2, 4, 7, 11, 12
  P.S. Sastri translation

30 rules total: JPE001-JPE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

JATAKA_PARIJATA_EXT_REGISTRY = CorpusRegistry()

_JATAKA_PARIJATA_EXT = [
    # --- JP Unique Lagna-Based Rules (JPE001-010) ---
    RuleRecord(
        rule_id="JPE001",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Aries Lagna: Mars as lagna lord, energetic leader, impulsive, "
            "short-tempered but forgiving, red/copper complexion, "
            "active life, prone to head injuries. Saturn in lagna = delayed success."
        ),
        confidence=0.86,
        verse="JP Ch.2 v.1-5",
        tags=["aries_lagna", "mars_lagna_lord", "impulsive", "head_injuries", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE002",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Taurus Lagna: Venus as lagna lord, beautiful appearance, "
            "fond of luxury and sensual pleasures, steady temperament, "
            "financial acumen, bull-like persistence, throat/neck vulnerability."
        ),
        confidence=0.86,
        verse="JP Ch.2 v.6-10",
        tags=["taurus_lagna", "venus_lagna_lord", "luxury", "persistence", "throat", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE003",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Gemini Lagna: Mercury as lagna lord, witty, dual nature, "
            "skilled in multiple arts, youthful appearance throughout life, "
            "active hands/arms, versatile communication ability."
        ),
        confidence=0.86,
        verse="JP Ch.2 v.11-15",
        tags=["gemini_lagna", "mercury_lagna_lord", "dual_nature", "witty", "versatile", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE004",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Cancer Lagna: Moon as lagna lord, sensitive, nurturing, "
            "domestic focus, round face, pale complexion, strong emotional memory, "
            "attached to homeland and mother, fluctuating fortunes."
        ),
        confidence=0.86,
        verse="JP Ch.2 v.16-20",
        tags=["cancer_lagna", "moon_lagna_lord", "sensitive", "domestic", "fluctuating", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE005",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Leo Lagna: Sun as lagna lord, commanding presence, generous, "
            "proud, broad shoulders, leadership quality, government service potential, "
            "susceptibility to back problems and heart issues."
        ),
        confidence=0.86,
        verse="JP Ch.2 v.21-25",
        tags=["leo_lagna", "sun_lagna_lord", "commanding", "generous", "leadership", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE006",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Virgo Lagna: Mercury as lagna lord, analytical, health-conscious, "
            "service-oriented, discriminating intellect, moderate build, "
            "skill in arts and crafts, potential digestive issues."
        ),
        confidence=0.85,
        verse="JP Ch.2 v.26-30",
        tags=["virgo_lagna", "mercury_lagna_lord", "analytical", "service", "digestive", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE007",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Libra Lagna: Venus as lagna lord, balanced, diplomatic, "
            "beautiful appearance, skilled in arts, fond of partnerships, "
            "prone to kidney/lower back issues. Justice-oriented."
        ),
        confidence=0.85,
        verse="JP Ch.2 v.31-35",
        tags=["libra_lagna", "venus_lagna_lord", "diplomatic", "partnerships", "kidney", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE008",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Scorpio Lagna: Mars as lagna lord, intense, secretive, "
            "penetrating insight, fearless, prone to conflicts, "
            "reproductive health focus, transformative life experiences."
        ),
        confidence=0.85,
        verse="JP Ch.2 v.36-40",
        tags=["scorpio_lagna", "mars_lagna_lord", "intense", "secretive", "transformative", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE009",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Sagittarius Lagna: Jupiter as lagna lord, philosophical, ethical, "
            "tall/athletic build, jovial nature, love of horses and outdoor activities, "
            "success in law/religion/education, hip area vulnerability."
        ),
        confidence=0.85,
        verse="JP Ch.2 v.41-45",
        tags=["sagittarius_lagna", "jupiter_lagna_lord", "philosophical", "athletic", "hips", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE010",
        source="Jataka_Parijata",
        chapter="Ch.2",
        school="vaidyanatha",
        category="lagna_analysis",
        description=(
            "JP Capricorn+Aquarius+Pisces Lagnas: "
            "Capricorn (Saturn): ambitious, karmic discipline, slow rise. "
            "Aquarius (Saturn): humanitarian, unconventional, networker. "
            "Pisces (Jupiter): spiritual, artistic, boundary-dissolving."
        ),
        confidence=0.84,
        verse="JP Ch.2 v.46-55",
        tags=["capricorn_lagna", "aquarius_lagna", "pisces_lagna", "saturn_jupiter", "vaidyanatha"],
        implemented=False,
    ),
    # --- JP Special Yogas (JPE011-020) ---
    RuleRecord(
        rule_id="JPE011",
        source="Jataka_Parijata",
        chapter="Ch.4",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Parivartana Yoga classifications: "
            "1) Maha Parivartana (exchange between kendra/trikona lords) = very powerful. "
            "2) Dainya Parivartana (exchange involving 6/8/12 lord) = harmful to good houses. "
            "3) Kahala Parivartana (exchange not involving above) = moderate."
        ),
        confidence=0.90,
        verse="JP Ch.4 v.1-6",
        tags=["yoga", "parivartana", "maha_parivartana", "dainya_parivartana", "kahala", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE012",
        source="Jataka_Parijata",
        chapter="Ch.4",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Neecha Bhanga Raja Yoga (NBRY): Neecha (debilitated) planet's yoga "
            "is cancelled when: (1) exaltation lord is in kendra from lagna or Moon, "
            "OR (2) planet that becomes exalted in that sign is in kendra from Moon."
        ),
        confidence=0.92,
        verse="JP Ch.4 v.7-10",
        tags=["yoga", "neecha_bhanga", "nbry", "debilitation_cancelled", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE013",
        source="Jataka_Parijata",
        chapter="Ch.4",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Vesi Yoga: Planets other than Moon in 2nd from Sun → Vesi Yoga. "
            "Benefits from this: lucky, wealthy, lazy-but-successful, broad-minded. "
            "Benefics in 2nd from Sun = Shubha Vesi; malefics = Paapa Vesi."
        ),
        confidence=0.86,
        verse="JP Ch.4 v.11-14",
        tags=["yoga", "vesi_yoga", "sun_2nd", "vasi_yoga", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE014",
        source="Jataka_Parijata",
        chapter="Ch.4",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Vasi Yoga: Planets in 12th from Sun (other than Moon). "
            "Vasi = placed behind Sun. "
            "Benefic Vasi = charitable, respected; Malefic Vasi = cruel nature."
        ),
        confidence=0.85,
        verse="JP Ch.4 v.15-17",
        tags=["yoga", "vasi_yoga", "sun_12th", "vesi_vasi", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE015",
        source="Jataka_Parijata",
        chapter="Ch.4",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Obhayachari Yoga: Planets in both 2nd and 12th from Sun "
            "(excluding Moon). Gives exceptional personality, "
            "royal qualities, self-sufficiency, and widespread fame."
        ),
        confidence=0.85,
        verse="JP Ch.4 v.18-20",
        tags=["yoga", "obhayachari_yoga", "sun_2nd_12th", "fame", "royal", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE016",
        source="Jataka_Parijata",
        chapter="Ch.7",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Chandra Mangala Yoga: Moon and Mars in conjunction or mutual aspect. "
            "Native accumulates wealth through business, especially trade. "
            "May have emotional intensity; bold financial decisions."
        ),
        confidence=0.85,
        verse="JP Ch.7 v.1-3",
        tags=["yoga", "chandra_mangala", "moon_mars", "wealth_through_trade", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE017",
        source="Jataka_Parijata",
        chapter="Ch.7",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Guru-Chandala Yoga: Jupiter conjunct Rahu or Ketu. "
            "Wisdom is tainted or unconventional. Native may challenge "
            "established religious/philosophical norms. Can indicate a reformer."
        ),
        confidence=0.84,
        verse="JP Ch.7 v.4-6",
        tags=["yoga", "guru_chandala", "jupiter_rahu", "unconventional_wisdom", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE018",
        source="Jataka_Parijata",
        chapter="Ch.7",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Shakata Yoga: Moon in 6th, 8th, or 12th from Jupiter. "
            "Life goes up and down like a wheel (shakata = cart wheel). "
            "Success followed by setbacks in recurring cycles."
        ),
        confidence=0.85,
        verse="JP Ch.7 v.7-9",
        tags=["yoga", "shakata_yoga", "moon_6_8_12_jupiter", "cyclical_fortune", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE019",
        source="Jataka_Parijata",
        chapter="Ch.7",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Kemadruma Yoga (Moon alone): Moon with no planets in 2nd or 12th "
            "from it AND no planet in kendra from Moon. "
            "Native faces poverty, hardships, wandering, lack of support."
        ),
        confidence=0.86,
        verse="JP Ch.7 v.10-12",
        tags=["yoga", "kemadruma", "moon_alone", "poverty", "hardship", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE020",
        source="Jataka_Parijata",
        chapter="Ch.7",
        school="vaidyanatha",
        category="yoga",
        description=(
            "JP Kemadruma cancellation: Kemadruma is cancelled if any planet "
            "is in kendra from Moon OR if Moon is in kendra from lagna OR "
            "if Moon is full (Purnima) or near full. Cancellation restores good fortune."
        ),
        confidence=0.86,
        verse="JP Ch.7 v.13-15",
        tags=["yoga", "kemadruma_bhanga", "moon_kendra", "cancellation", "vaidyanatha"],
        implemented=False,
    ),
    # --- JP Timing and Dasha Rules (JPE021-030) ---
    RuleRecord(
        rule_id="JPE021",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Vimshottari Dasha start: Dasha balance at birth is calculated "
            "from Moon's position within its nakshatra. "
            "The remaining portion of the nakshatra = proportion of first dasha remaining."
        ),
        confidence=0.90,
        verse="JP Ch.11 v.1-4",
        tags=["dasha", "vimshottari", "dasha_balance", "birth_calculation", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE022",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Sun Mahadasha (6 years): Government, authority, father themes dominant. "
            "Health of father, career advancement, religious activities. "
            "Difficult if Sun is weak or aspected by malefics in natal chart."
        ),
        confidence=0.86,
        verse="JP Ch.11 v.5-8",
        tags=["dasha", "sun_dasha", "6_years", "government", "father_health", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE023",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Moon Mahadasha (10 years): Emotional fulfillment, mother, domestic happiness. "
            "Travel, public dealings, fluctuating fortunes. "
            "Strong Moon = wealth and comfort; weak Moon = mental disturbances."
        ),
        confidence=0.86,
        verse="JP Ch.11 v.9-12",
        tags=["dasha", "moon_dasha", "10_years", "mother", "emotional", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE024",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Mars Mahadasha (7 years): Courage, siblings, property, accidents. "
            "Land acquisition, conflicts, physical activities. "
            "Strong Mars = success in ventures; weak = accidents and disputes."
        ),
        confidence=0.85,
        verse="JP Ch.11 v.13-16",
        tags=["dasha", "mars_dasha", "7_years", "siblings", "property", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE025",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Rahu Mahadasha (18 years): Foreign connections, unusual experiences. "
            "Rahu amplifies the house it sits in and acts like its dispositor. "
            "Can bring sudden rise or fall; materialistic focus."
        ),
        confidence=0.84,
        verse="JP Ch.11 v.17-20",
        tags=["dasha", "rahu_dasha", "18_years", "foreign", "sudden_change", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE026",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Jupiter Mahadasha (16 years): Expansion, wisdom, children, spirituality. "
            "Best period for education, marriage, and wealth accumulation. "
            "Strong Jupiter = major blessings; afflicted = over-expansion."
        ),
        confidence=0.87,
        verse="JP Ch.11 v.21-24",
        tags=["dasha", "jupiter_dasha", "16_years", "children", "wisdom", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE027",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Saturn Mahadasha (19 years): Discipline, karmic reckoning, hard work. "
            "Longest dasha — service, responsibility, obstacles, and ultimate reward. "
            "Strong Saturn = career pinnacle; weak = illness and delay."
        ),
        confidence=0.87,
        verse="JP Ch.11 v.25-28",
        tags=["dasha", "saturn_dasha", "19_years", "discipline", "karma", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE028",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Mercury Mahadasha (17 years): Communication, trade, intelligence. "
            "Good for education, writing, business, technical professions. "
            "Strong Mercury = multiple successful ventures; afflicted = confusion."
        ),
        confidence=0.85,
        verse="JP Ch.11 v.29-32",
        tags=["dasha", "mercury_dasha", "17_years", "trade", "intelligence", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE029",
        source="Jataka_Parijata",
        chapter="Ch.11",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Ketu Mahadasha (7 years): Spiritual focus, detachment, past-life karma. "
            "May bring losses that lead to liberation. Good for spiritual practice. "
            "Results depend on house Ketu occupies and its dispositor's strength."
        ),
        confidence=0.84,
        verse="JP Ch.11 v.33-36",
        tags=["dasha", "ketu_dasha", "7_years", "spiritual", "detachment", "vaidyanatha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="JPE030",
        source="Jataka_Parijata",
        chapter="Ch.12",
        school="vaidyanatha",
        category="dasha",
        description=(
            "JP Venus Mahadasha (20 years): Longest among benefic dashas. "
            "Pleasure, luxury, marriage, arts, and financial prosperity. "
            "Peak domestic/romantic life. Strong Venus = supreme enjoyment; "
            "afflicted = over-indulgence and health problems."
        ),
        confidence=0.87,
        verse="JP Ch.12 v.1-4",
        tags=["dasha", "venus_dasha", "20_years", "pleasure", "luxury", "marriage", "vaidyanatha"],
        implemented=False,
    ),
]

for _r in _JATAKA_PARIJATA_EXT:
    JATAKA_PARIJATA_EXT_REGISTRY.add(_r)
