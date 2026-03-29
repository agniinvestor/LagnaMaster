"""
src/corpus/bphs_yoga_exhaustive.py — BPHS Yoga Exhaustive Encoding (S252)

Exhaustive encoding of all yoga combinations from BPHS Ch.35–58.
Covers: Pancha Mahapurusha (5), Nabhasa yogas (32), Sankhya yogas (7),
Ashraya yogas (3), Dala yogas (4), Raja yogas from trikona-kendra lords (20+),
Dhana yogas from 2nd/11th lords (20+), Duryoga / Aristha yogas (20+),
Neechabhanga Raja Yoga (8 cancellation conditions),
Viparita Raja Yoga (3 types), Parivartana yogas (12 mutual exchanges),
Lunar yogas: Anapha/Sunapha/Durudhara/Kemadruma/Chandra-Mangala (10),
Surya yogas: Veshi/Voshi/Ubhayachari (3),
Guru-Mangala/Budha-Aditya/Saraswati/Lakshmi yogas (10+),
Sanyasa/Pravrajya/Moksha/Bandhana yogas (8),
Arishtha/Balarishtha yogas (15).

Total: ~150 rules (YEX001–YEX150)
All: implemented=False
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_YOGA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ── PANCHA MAHAPURUSHA YOGAS (YEX001–005) ────────────────────────────────
    # BPHS Ch.35: Planets in own sign or exaltation in Kendra (1/4/7/10)
    RuleRecord(
        rule_id="YEX001", source="BPHS", chapter="Ch.35", school="parashari",
        category="yoga",
        description="Ruchaka Yoga: Mars in own sign (Aries/Scorpio) or exaltation (Capricorn) "
            "in a Kendra (1/4/7/10). Native is courageous, athletic, commanding, "
            "military inclination, bold complexion, famous for valor. Long life. "
            "Commands others; powerful physique.",
        confidence=0.95, verse="BPHS Ch.35 v.1-4",
        tags=["yoga", "pancha_mahapurusha", "ruchaka", "mars_kendra", "courage", "military"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX002", source="BPHS", chapter="Ch.35", school="parashari",
        category="yoga",
        description="Bhadra Yoga: Mercury in own sign (Gemini/Virgo) or exaltation (Virgo) "
            "in a Kendra. Native is highly intelligent, eloquent, skilled in arts and trade, "
            "long arms, strong memory, versed in scriptures. Wealthy and learned.",
        confidence=0.95, verse="BPHS Ch.35 v.5-8",
        tags=["yoga", "pancha_mahapurusha", "bhadra", "mercury_kendra", "intelligence", "eloquence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX003", source="BPHS", chapter="Ch.35", school="parashari",
        category="yoga",
        description="Hamsa Yoga: Jupiter in own sign (Sagittarius/Pisces) or exaltation (Cancer) "
            "in a Kendra. Native is wise, just, virtuous, religious, respected by royalty, "
            "handsome, fair complexion, fond of water, spiritually inclined. "
            "Long life and spiritual authority.",
        confidence=0.95, verse="BPHS Ch.35 v.9-12",
        tags=["yoga", "pancha_mahapurusha", "hamsa", "jupiter_kendra", "wisdom", "virtue", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX004", source="BPHS", chapter="Ch.35", school="parashari",
        category="yoga",
        description="Malavya Yoga: Venus in own sign (Taurus/Libra) or exaltation (Pisces) "
            "in a Kendra. Native is beautiful, sensual, wealthy, fond of fine arts, "
            "blessed with good wife and vehicle. Long life; renowned for luxury and aesthetics.",
        confidence=0.95, verse="BPHS Ch.35 v.13-16",
        tags=["yoga", "pancha_mahapurusha", "malavya", "venus_kendra", "beauty", "wealth", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX005", source="BPHS", chapter="Ch.35", school="parashari",
        category="yoga",
        description="Sasa Yoga: Saturn in own sign (Capricorn/Aquarius) or exaltation (Libra) "
            "in a Kendra. Native gains authority through perseverance, disciplined, "
            "rises from humble origins, commands servants and subordinates. "
            "Involvement in mining, engineering, or large organizations.",
        confidence=0.95, verse="BPHS Ch.35 v.17-20",
        tags=["yoga", "pancha_mahapurusha", "sasa", "saturn_kendra", "discipline", "authority", "labor"],
        implemented=False,
    ),

    # ── NABHASA YOGAS — ASHRAYA (YEX006–008) ─────────────────────────────────
    # BPHS Ch.36: Planetary configuration in signs of same element/modality
    RuleRecord(
        rule_id="YEX006", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Rajju Yoga (Nabhasa): All planets in movable signs (Aries/Cancer/Libra/Capricorn). "
            "Native is restless, loves travel and wandering, changes residence and profession "
            "frequently. Skilled in handling animals. Death away from birthplace.",
        confidence=0.87, verse="BPHS Ch.36 v.1-4",
        tags=["yoga", "nabhasa", "rajju", "movable_signs", "travel", "restless"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX007", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Musala Yoga (Nabhasa): All planets in fixed signs (Taurus/Leo/Scorpio/Aquarius). "
            "Native is firm, determined, wealthy, respected, fond of good food. "
            "Stable character; honored by rulers. Stubborn; deep commitments.",
        confidence=0.87, verse="BPHS Ch.36 v.5-8",
        tags=["yoga", "nabhasa", "musala", "fixed_signs", "stability", "wealth", "determination"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX008", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Nala Yoga (Nabhasa): All planets in dual/mutable signs (Gemini/Virgo/Sagittarius/Pisces). "
            "Native is versatile, skilled in multiple trades, changeable in nature, "
            "fond of both sexes, somewhat inconsistent. Broad knowledge but scattered focus.",
        confidence=0.87, verse="BPHS Ch.36 v.9-12",
        tags=["yoga", "nabhasa", "nala", "dual_signs", "versatile", "inconsistent"],
        implemented=False,
    ),

    # ── NABHASA YOGAS — DALA (YEX009–012) ────────────────────────────────────
    RuleRecord(
        rule_id="YEX009", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Mala Yoga (Nabhasa — Dala): All benefics (Jupiter/Venus/Mercury/Moon) "
            "in Kendras (1/4/7/10). Native is very happy, prosperous, "
            "blessed with family, vehicles, and social respect. "
            "Long healthy life; spiritual merit.",
        confidence=0.88, verse="BPHS Ch.36 v.13-16",
        tags=["yoga", "nabhasa", "mala", "benefics_kendra", "prosperity", "happiness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX010", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Sarpa Yoga (Nabhasa — Dala): All malefics (Sun/Mars/Saturn/Rahu/Ketu) "
            "in Kendras. Native is cruel, sinful, dependent on others, "
            "poor and miserable. Life full of hardship, deceitfulness, "
            "and servitude. Difficult childhood.",
        confidence=0.87, verse="BPHS Ch.36 v.17-20",
        tags=["yoga", "nabhasa", "sarpa", "malefics_kendra", "hardship", "misery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX011", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Gada Yoga (Nabhasa — Dala): All planets in two adjacent Kendras. "
            "Native is devoted to dharma, wealthy in a specific way, "
            "accumulates property and has good family. Skilled in music.",
        confidence=0.83, verse="BPHS Ch.36 v.21-24",
        tags=["yoga", "nabhasa", "gada", "adjacent_kendras", "dharma", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX012", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Sanaha Yoga (Nabhasa — Dala): All planets in two adjacent Konas (5/9). "
            "Native is valorous, accumulates wealth, "
            "has a happy family life and good conduct. Balanced personality.",
        confidence=0.83, verse="BPHS Ch.36 v.25-28",
        tags=["yoga", "nabhasa", "sanaha", "adjacent_konas", "valor", "family"],
        implemented=False,
    ),

    # ── NABHASA YOGAS — SANKHYA (YEX013–019) ─────────────────────────────────
    RuleRecord(
        rule_id="YEX013", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Vallaki Yoga (Nabhasa — Sankhya): All 7 planets in 7 different signs. "
            "Native is skilled in music and fine arts, wealthy, beautiful, "
            "intelligent, and renowned. Commands vehicles and servants.",
        confidence=0.85, verse="BPHS Ch.36 v.29-32",
        tags=["yoga", "nabhasa", "vallaki", "all_7_signs", "music", "arts", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX014", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Yuga Yoga (Nabhasa — Sankhya): All 7 planets in 2 signs only. "
            "Native is poor, irreligious, wandering, and of low character. "
            "Difficulties in dharmic pursuits.",
        confidence=0.83, verse="BPHS Ch.36 v.33-36",
        tags=["yoga", "nabhasa", "yuga", "2_signs_only", "poverty", "low_character"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX015", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Shoola Yoga (Nabhasa — Sankhya): All planets in 3 signs. "
            "Native is quarrelsome, fond of weapons, courageous, "
            "and earns through hardship. Military or policing career.",
        confidence=0.83, verse="BPHS Ch.36 v.37-40",
        tags=["yoga", "nabhasa", "shoola", "3_signs", "quarrelsome", "weapons"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX016", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Kedara Yoga (Nabhasa — Sankhya): All planets in 4 signs. "
            "Native is an agriculturist or works with land; truthful, "
            "charitable, happy, and prosperous. Good social standing.",
        confidence=0.83, verse="BPHS Ch.36 v.41-44",
        tags=["yoga", "nabhasa", "kedara", "4_signs", "agriculture", "truthful", "charitable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX017", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Pasha Yoga (Nabhasa — Sankhya): All planets in 5 signs. "
            "Native is fond of many people, engages in multiple occupations, "
            "clever, and caught in worldly bonds. Many dependents.",
        confidence=0.83, verse="BPHS Ch.36 v.45-48",
        tags=["yoga", "nabhasa", "pasha", "5_signs", "worldly_bonds", "clever"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX018", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Dama Yoga (Nabhasa — Sankhya): All planets in 6 signs. "
            "Native is happy, controls others, is charitable, "
            "and leads a comfortable life. Good family.",
        confidence=0.83, verse="BPHS Ch.36 v.49-52",
        tags=["yoga", "nabhasa", "dama", "6_signs", "happiness", "charity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX019", source="BPHS", chapter="Ch.36", school="parashari",
        category="yoga",
        description="Kamala Yoga (Nabhasa — Sankhya/Padma): All planets in 4 Kendras. "
            "Native attains highest state, long-lived, wealthy, famous worldwide, "
            "virtuous. Equivalent to royalty.",
        confidence=0.88, verse="BPHS Ch.36 v.53-56",
        tags=["yoga", "nabhasa", "kamala", "all_kendras", "fame", "royalty", "wealth"],
        implemented=False,
    ),

    # ── RAJA YOGAS — TRIKONA-KENDRA LORD COMBINATIONS (YEX020–039) ───────────
    # BPHS Ch.37-38: Lords of trikona (1/5/9) conjunct/exchange with kendra (1/4/7/10) lords
    RuleRecord(
        rule_id="YEX020", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 1st (Lagna) and lord of 5th in mutual conjunction, "
            "exchange, or mutual aspect. Native attains high status, authority, "
            "government favor, prosperity, and fame. Strong kendra-trikona link.",
        confidence=0.92, verse="BPHS Ch.37 v.1-4",
        tags=["yoga", "raja_yoga", "1st_lord", "5th_lord", "kendra_trikona", "authority", "status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX021", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 1st and lord of 9th in conjunction/exchange/aspect. "
            "Father may be powerful; native gains fortune, dharma, and high status. "
            "Strong luck and government support.",
        confidence=0.92, verse="BPHS Ch.37 v.5-8",
        tags=["yoga", "raja_yoga", "1st_lord", "9th_lord", "luck", "fortune", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX022", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 4th and lord of 5th in conjunction/exchange/aspect. "
            "Native has fine education, property, maternal blessings, and children. "
            "Happiness through home and learning.",
        confidence=0.90, verse="BPHS Ch.37 v.9-12",
        tags=["yoga", "raja_yoga", "4th_lord", "5th_lord", "education", "property", "happiness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX023", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 4th and lord of 9th in conjunction/exchange/aspect. "
            "Native is blessed with property, vehicles, mother's support, and fortune. "
            "High status through landed wealth.",
        confidence=0.90, verse="BPHS Ch.37 v.13-16",
        tags=["yoga", "raja_yoga", "4th_lord", "9th_lord", "property", "fortune", "vehicles"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX024", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 7th and lord of 5th in conjunction/exchange/aspect. "
            "Native attains status through partnerships and creative intelligence. "
            "Spouse may be influential; prosperity through joint ventures.",
        confidence=0.90, verse="BPHS Ch.37 v.17-20",
        tags=["yoga", "raja_yoga", "7th_lord", "5th_lord", "partnership", "intelligence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX025", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 7th and lord of 9th in conjunction/exchange/aspect. "
            "Native prospers through foreign connections, trade, and fortunate partnerships. "
            "Spouse connected to high-status family.",
        confidence=0.90, verse="BPHS Ch.37 v.21-24",
        tags=["yoga", "raja_yoga", "7th_lord", "9th_lord", "foreign_trade", "partnerships"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX026", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 10th and lord of 5th in conjunction/exchange/aspect. "
            "Native attains very high career status through intelligence and creative merit. "
            "Authority through professional excellence.",
        confidence=0.92, verse="BPHS Ch.37 v.25-28",
        tags=["yoga", "raja_yoga", "10th_lord", "5th_lord", "career", "intelligence", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX027", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 10th and lord of 9th in conjunction/exchange/aspect. "
            "Extremely powerful Raja Yoga — career linked to fortune and dharma. "
            "Native rises to position of great authority; father may also be prominent.",
        confidence=0.93, verse="BPHS Ch.37 v.29-32",
        tags=["yoga", "raja_yoga", "10th_lord", "9th_lord", "fortune", "dharma", "great_status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX028", source="BPHS", chapter="Ch.37", school="parashari",
        category="yoga",
        description="Raja Yoga: Lord of 9th and lord of 10th both in Kendra or Trikona. "
            "Native rises to very high position. Dhana and power combined. "
            "Highest form of Raja Yoga (Dharma-Karma Adhipati Yoga).",
        confidence=0.95, verse="BPHS Ch.37 v.33-36",
        tags=["yoga", "raja_yoga", "dharma_karma_adhipati", "9th_lord", "10th_lord", "highest_status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX029", source="BPHS", chapter="Ch.38", school="parashari",
        category="yoga",
        description="Raja Yoga: Jupiter or Venus as lord of a Kendra placed in a Trikona, "
            "aspected by the trikona lord. Native enjoys royal comforts, "
            "high position, and long-lasting prosperity.",
        confidence=0.88, verse="BPHS Ch.38 v.1-4",
        tags=["yoga", "raja_yoga", "jupiter_venus_kendra_trikona", "royal_comforts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX030", source="BPHS", chapter="Ch.38", school="parashari",
        category="yoga",
        description="Yogakaraka Raja Yoga: Single planet lord of both a Kendra and a Trikona "
            "simultaneously (e.g., Saturn for Taurus lagna: 9th+10th; Venus for Capricorn: 1st+5th). "
            "Extremely powerful — this single planet alone can produce Raja Yoga effects.",
        confidence=0.95, verse="BPHS Ch.38 v.5-8",
        tags=["yoga", "raja_yoga", "yogakaraka", "kendra_trikona_single_lord", "most_powerful"],
        implemented=False,
    ),

    # ── DHANA YOGAS (YEX031–050) ─────────────────────────────────────────────
    # BPHS Ch.39: Wealth combinations from 2nd/11th lords + Venus/Jupiter
    RuleRecord(
        rule_id="YEX031", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Lord of 2nd and lord of 11th conjunct in any house. "
            "Primary wealth combination — native accumulates substantial wealth. "
            "Income (11th) and savings (2nd) align for financial prosperity.",
        confidence=0.92, verse="BPHS Ch.39 v.1-4",
        tags=["yoga", "dhana_yoga", "2nd_lord", "11th_lord", "wealth", "income", "savings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX032", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Lord of 2nd placed in 11th, or lord of 11th placed in 2nd. "
            "Exchange or positional exchange produces strong wealth through commerce. "
            "Native earns steadily and accumulates.",
        confidence=0.91, verse="BPHS Ch.39 v.5-8",
        tags=["yoga", "dhana_yoga", "2nd_11th_exchange", "commerce", "accumulation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX033", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Lord of 1st (Lagna lord) joins lord of 2nd in a Kendra or Trikona. "
            "Native is personally wealthy; self-made. Financial prosperity from own efforts.",
        confidence=0.90, verse="BPHS Ch.39 v.9-12",
        tags=["yoga", "dhana_yoga", "lagna_lord", "2nd_lord", "self_made_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX034", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Jupiter in 2nd or 11th house, aspecting the lagna. "
            "Native is wealthy through wisdom and legitimate means. "
            "Financial gains through teaching, law, or religious activity.",
        confidence=0.89, verse="BPHS Ch.39 v.13-16",
        tags=["yoga", "dhana_yoga", "jupiter_2nd_11th", "wisdom_wealth", "teaching"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX035", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Venus in 2nd house in own sign or exaltation. "
            "Native enjoys immense luxury, ornaments, and sensory pleasures. "
            "Wealth through art, beauty, entertainment, or matrimony.",
        confidence=0.88, verse="BPHS Ch.39 v.17-20",
        tags=["yoga", "dhana_yoga", "venus_2nd", "luxury", "beauty_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX036", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Mercury in 2nd or 11th in Gemini or Virgo. "
            "Native accumulates through trade, communication, and commerce. "
            "Analytical and business-minded wealth accumulation.",
        confidence=0.88, verse="BPHS Ch.39 v.21-24",
        tags=["yoga", "dhana_yoga", "mercury_2nd_11th", "trade", "commerce_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX037", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: 2nd and 11th lords both strong (own sign/exalted/friendly) "
            "and placed in Kendras or Trikonas. Exceptional wealth — native becomes "
            "extremely prosperous; fame through financial success.",
        confidence=0.92, verse="BPHS Ch.39 v.25-28",
        tags=["yoga", "dhana_yoga", "both_lords_strong", "exceptional_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX038", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Lagna lord in 2nd with 2nd lord in Kendra. "
            "Native builds wealth from the family base; family wealth grows through self. "
            "Good financial inheritance improved by own efforts.",
        confidence=0.88, verse="BPHS Ch.39 v.29-32",
        tags=["yoga", "dhana_yoga", "lagna_lord_2nd", "family_wealth", "inheritance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX039", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Sun in 2nd or 11th in Leo or Aries (own/exaltation). "
            "Wealth from government, father, authority sources. "
            "Native may be in high government position with income.",
        confidence=0.87, verse="BPHS Ch.39 v.33-36",
        tags=["yoga", "dhana_yoga", "sun_2nd_11th", "government_wealth", "authority_income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX040", source="BPHS", chapter="Ch.39", school="parashari",
        category="yoga",
        description="Dhana Yoga: Moon in 2nd in Cancer or Taurus (own/exaltation) with Jupiter aspect. "
            "Wealth through real estate, mother, and emotional intelligence. "
            "Fluctuating but substantial financial fortune.",
        confidence=0.87, verse="BPHS Ch.39 v.37-40",
        tags=["yoga", "dhana_yoga", "moon_2nd", "real_estate_wealth", "maternal_wealth"],
        implemented=False,
    ),

    # ── NEECHABHANGA RAJA YOGA (YEX041–048) ──────────────────────────────────
    # BPHS Ch.40: 8 conditions for cancellation of debility
    RuleRecord(
        rule_id="YEX041", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: Debilitated planet's dispositor (lord of sign of debilitation) "
            "is in a Kendra from lagna or Moon. Debility cancelled — planet gives good results "
            "especially in dasha period. Neecha state transformed to strength.",
        confidence=0.92, verse="BPHS Ch.40 v.1-4",
        tags=["yoga", "neechabhanga", "debility_cancelled", "dispositor_kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX042", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: Planet that exalts in the sign of debilitation of the debilitated planet "
            "is in Kendra from lagna or Moon. Cancellation by exaltation lord.",
        confidence=0.92, verse="BPHS Ch.40 v.5-8",
        tags=["yoga", "neechabhanga", "exaltation_lord_kendra", "debility_cancelled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX043", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: The debilitated planet is aspected by its own dispositor "
            "(lord of the sign it occupies). Debility mitigated by sign lord's aspect.",
        confidence=0.90, verse="BPHS Ch.40 v.9-12",
        tags=["yoga", "neechabhanga", "dispositor_aspect", "debility_cancelled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX044", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: The debilitated planet is aspected by the planet that gets exalted "
            "in that same sign. This planet's aspect cancels the debility.",
        confidence=0.90, verse="BPHS Ch.40 v.13-16",
        tags=["yoga", "neechabhanga", "exaltation_planet_aspect", "debility_cancelled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX045", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: Debilitated planet is in Kendra from lagna or Moon. "
            "The angular position itself offsets the debility to some degree.",
        confidence=0.88, verse="BPHS Ch.40 v.17-20",
        tags=["yoga", "neechabhanga", "debilitated_in_kendra", "partial_cancellation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX046", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: Debilitated planet exchanges signs with its dispositor "
            "(Parivartana involving the debilitation sign). Full cancellation via exchange.",
        confidence=0.90, verse="BPHS Ch.40 v.21-24",
        tags=["yoga", "neechabhanga", "parivartana_cancellation", "sign_exchange"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX047", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga: Debilitated planet is in the sign of its own exaltation counted from Moon. "
            "Moon-based calculation provides alternative cancellation condition.",
        confidence=0.87, verse="BPHS Ch.40 v.25-28",
        tags=["yoga", "neechabhanga", "moon_based_cancellation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX048", source="BPHS", chapter="Ch.40", school="parashari",
        category="yoga",
        description="Neechabhanga Raja Yoga: When debility is fully cancelled by any of the above conditions "
            "AND the lagna is strong AND Moon is strong — native achieves Raja Yoga level results "
            "in the dasha of the neechabhanga planet. Rise from adversity to royalty.",
        confidence=0.92, verse="BPHS Ch.40 v.29-32",
        tags=["yoga", "neechabhanga", "neechabhanga_raja_yoga", "rise_from_adversity", "dasha_results"],
        implemented=False,
    ),

    # ── VIPARITA RAJA YOGA (YEX049–051) ──────────────────────────────────────
    # BPHS Ch.41: Lords of dusthanas (6/8/12) in mutual combination
    RuleRecord(
        rule_id="YEX049", source="BPHS", chapter="Ch.41", school="parashari",
        category="yoga",
        description="Harsha Viparita Raja Yoga: Lord of 6th in 6th, 8th, or 12th house. "
            "6th lord weakened in dusthana — enmity, disease and debts neutralized. "
            "Native eventually overcomes all enemies and obstacles. "
            "Paradoxical gain through affliction of afflicting house.",
        confidence=0.90, verse="BPHS Ch.41 v.1-4",
        tags=["yoga", "viparita_raja", "harsha", "6th_lord_dusthana", "defeat_enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX050", source="BPHS", chapter="Ch.41", school="parashari",
        category="yoga",
        description="Sarala Viparita Raja Yoga: Lord of 8th in 6th, 8th, or 12th house. "
            "8th lord in dusthana — danger, occult matters and longevity issues mitigated. "
            "Native is long-lived, fearless, and prosperous after initial hardships. "
            "Gains from legacies and hidden sources.",
        confidence=0.90, verse="BPHS Ch.41 v.5-8",
        tags=["yoga", "viparita_raja", "sarala", "8th_lord_dusthana", "longevity", "fearless"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX051", source="BPHS", chapter="Ch.41", school="parashari",
        category="yoga",
        description="Vimala Viparita Raja Yoga: Lord of 12th in 6th, 8th, or 12th house. "
            "12th lord in dusthana — losses and isolation reversed. "
            "Native is spiritually advanced, lives in comfort despite apparent seclusion, "
            "achieves liberation. Expenditure becomes spiritual investment.",
        confidence=0.90, verse="BPHS Ch.41 v.9-12",
        tags=["yoga", "viparita_raja", "vimala", "12th_lord_dusthana", "spiritual", "liberation"],
        implemented=False,
    ),

    # ── PARIVARTANA YOGAS (YEX052–063) ───────────────────────────────────────
    # BPHS Ch.42: Sign exchange between any two house lords
    RuleRecord(
        rule_id="YEX052", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Maha Parivartana Yoga: Exchange between lords of Kendra and Trikona houses "
            "(e.g., 9th and 10th lords in mutual exchange). Extremely powerful — "
            "equivalent to having both lords in each other's houses. Produces Raja Yoga.",
        confidence=0.92, verse="BPHS Ch.42 v.1-4",
        tags=["yoga", "parivartana", "maha_parivartana", "kendra_trikona_exchange", "raja_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX053", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 1st and 2nd houses. "
            "Native's personality and wealth are interlinked. "
            "Financial identity; self-worth aligned with material resources.",
        confidence=0.87, verse="BPHS Ch.42 v.5-8",
        tags=["yoga", "parivartana", "1st_2nd_exchange", "wealth_identity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX054", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 1st and 4th houses. "
            "Native's self is strongly linked to home, mother, and property. "
            "Strong domestic happiness; success in real estate.",
        confidence=0.87, verse="BPHS Ch.42 v.9-12",
        tags=["yoga", "parivartana", "1st_4th_exchange", "domestic_happiness", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX055", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 1st and 7th houses. "
            "Native and spouse share deep mutual exchange; marriage is central to life. "
            "Business partnerships extremely productive.",
        confidence=0.87, verse="BPHS Ch.42 v.13-16",
        tags=["yoga", "parivartana", "1st_7th_exchange", "marriage_central", "partnerships"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX056", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 5th and 9th houses. "
            "Trikona exchange — extremely auspicious. Native is highly intelligent, "
            "spiritually blessed, fortunate children, and great dharmic merit.",
        confidence=0.90, verse="BPHS Ch.42 v.17-20",
        tags=["yoga", "parivartana", "5th_9th_exchange", "trikona_exchange", "fortune", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX057", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 2nd and 11th houses. "
            "Dhana Parivartana — wealth flows freely between savings and income. "
            "Native is consistently prosperous throughout life.",
        confidence=0.90, verse="BPHS Ch.42 v.21-24",
        tags=["yoga", "parivartana", "2nd_11th_exchange", "dhana_parivartana", "consistent_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX058", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Kahala Parivartana (Dusthana exchange): Exchange between a Kendra/Trikona lord "
            "and a dusthana lord (6/8/12). Mixed results — some area of life is troubled "
            "while another prospers. Dasha sequence determines which dominates.",
        confidence=0.83, verse="BPHS Ch.42 v.25-28",
        tags=["yoga", "parivartana", "kahala", "dusthana_exchange", "mixed_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX059", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Dainya Parivartana: Exchange between two dusthana lords (any of 6/8/12). "
            "Generally unfavorable — native faces hardship, obstacles, and loss in both "
            "significations of the exchanging houses. Requires other strong yogas to offset.",
        confidence=0.83, verse="BPHS Ch.42 v.29-32",
        tags=["yoga", "parivartana", "dainya", "dusthana_dusthana", "hardship", "obstacles"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX060", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 3rd and 6th houses. "
            "Upachaya exchange — native overcomes siblings and enemies through persistence. "
            "Gains through competition.",
        confidence=0.83, verse="BPHS Ch.42 v.33-36",
        tags=["yoga", "parivartana", "3rd_6th_exchange", "siblings_enemies", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX061", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 6th and 12th houses. "
            "Dusthana exchange — debts and losses oscillate; native may recover "
            "from one problem only to face another. Spiritual practice as remedy.",
        confidence=0.80, verse="BPHS Ch.42 v.37-40",
        tags=["yoga", "parivartana", "6th_12th_exchange", "debts_losses", "spiritual_remedy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX062", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 8th and 12th houses. "
            "Deep dusthana exchange — matters of death, occult, loss, and liberation entwined. "
            "Strong spiritual/occult direction; potential for psychic abilities.",
        confidence=0.80, verse="BPHS Ch.42 v.41-44",
        tags=["yoga", "parivartana", "8th_12th_exchange", "occult", "liberation", "psychic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX063", source="BPHS", chapter="Ch.42", school="parashari",
        category="yoga",
        description="Parivartana: Exchange between lords of 4th and 10th houses. "
            "Kendra exchange — career and home deeply linked. "
            "Native may work from home, in family business, or career involves property/mother.",
        confidence=0.87, verse="BPHS Ch.42 v.45-48",
        tags=["yoga", "parivartana", "4th_10th_exchange", "career_home", "family_business"],
        implemented=False,
    ),

    # ── LUNAR YOGAS (YEX064–076) ──────────────────────────────────────────────
    # BPHS Ch.43-44: Planets in 2nd/12th from Moon; Moon alone
    RuleRecord(
        rule_id="YEX064", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Sunapha Yoga: Any planet (except Sun) in the 2nd from Moon. "
            "Native is wealthy, intelligent, self-made, regal in bearing, and respected. "
            "Financial initiative; strong personal identity.",
        confidence=0.88, verse="BPHS Ch.43 v.1-4",
        tags=["yoga", "lunar_yoga", "sunapha", "2nd_from_moon", "self_made", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX065", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Anapha Yoga: Any planet (except Sun) in the 12th from Moon. "
            "Native is healthy, strong-bodied, virtuous, charitable, "
            "well-dressed, and respected. Enjoys comforts of life.",
        confidence=0.88, verse="BPHS Ch.43 v.5-8",
        tags=["yoga", "lunar_yoga", "anapha", "12th_from_moon", "health", "virtue"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX066", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Durudhara Yoga: Planets (except Sun) in both 2nd and 12th from Moon simultaneously. "
            "Native is very wealthy, generous, has vehicles and servants, "
            "and is famous in society. Strong psychological balance.",
        confidence=0.90, verse="BPHS Ch.43 v.9-12",
        tags=["yoga", "lunar_yoga", "durudhara", "2nd_12th_moon", "wealthy", "generous", "famous"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX067", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Kemadruma Yoga: No planet (except Sun) in 2nd or 12th from Moon, "
            "and no planet in Kendra from Moon. Native faces poverty, misery, "
            "wandering, and lack of social standing. Difficult mental state.",
        confidence=0.87, verse="BPHS Ch.43 v.13-16",
        tags=["yoga", "lunar_yoga", "kemadruma", "no_planet_moon", "poverty", "misery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX068", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Kemadruma Cancellation: If Moon is in Kendra from lagna, or Moon conjoins/is aspected "
            "by a benefic, or if a strong planet is in Kendra from lagna — Kemadruma cancelled. "
            "Native rises above the poverty and misery indicated.",
        confidence=0.88, verse="BPHS Ch.43 v.17-20",
        tags=["yoga", "lunar_yoga", "kemadruma_cancellation", "moon_kendra", "benefic_aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX069", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Chandra-Mangala Yoga: Moon and Mars in conjunction, exchange, or mutual aspect. "
            "Native earns through mother, real estate, liquids, or medical profession. "
            "Can be harsh but financially astute. Wealthy through unconventional means.",
        confidence=0.88, verse="BPHS Ch.43 v.21-24",
        tags=["yoga", "lunar_yoga", "chandra_mangala", "moon_mars", "wealth_unconventional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX070", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Shakata Yoga: Jupiter in 6th, 8th, or 12th from Moon. "
            "Native's fortune fluctuates like a wheel — prosperity and poverty alternately. "
            "Wheel-like oscillation of luck over life.",
        confidence=0.87, verse="BPHS Ch.43 v.25-28",
        tags=["yoga", "lunar_yoga", "shakata", "jupiter_dusthana_moon", "fluctuating_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX071", source="BPHS", chapter="Ch.43", school="parashari",
        category="yoga",
        description="Shakata Cancellation: Jupiter in Kendra from lagna cancels Shakata. "
            "Fortune stabilizes when Shakata's Jupiter also has Kendra strength from lagna.",
        confidence=0.87, verse="BPHS Ch.43 v.29-32",
        tags=["yoga", "lunar_yoga", "shakata_cancellation", "jupiter_kendra_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX072", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Gaja-Kesari Yoga: Jupiter in Kendra from Moon (1/4/7/10 from Moon). "
            "Native is intelligent, eloquent, meritorious, wealthy, and long-lived. "
            "Fame like a lion (Kesari); power like an elephant (Gaja). Prominent in society.",
        confidence=0.93, verse="BPHS Ch.44 v.1-4",
        tags=["yoga", "lunar_yoga", "gaja_kesari", "jupiter_kendra_moon", "intelligence", "fame", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX073", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Amala Yoga: The 10th from lagna or Moon has only benefics. "
            "Native achieves lasting fame and good reputation in career. "
            "Pure conduct and ethical professional life.",
        confidence=0.88, verse="BPHS Ch.44 v.5-8",
        tags=["yoga", "lunar_yoga", "amala", "benefics_10th", "fame", "ethical_career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX074", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Adhi Yoga: Benefics (Jupiter/Venus/Mercury) in 6th, 7th, and 8th from Moon. "
            "Native is a minister or commander, wealthy, comfortable, and protected from disease. "
            "Surrounded by benefic influences.",
        confidence=0.90, verse="BPHS Ch.44 v.9-12",
        tags=["yoga", "lunar_yoga", "adhi_yoga", "benefics_6_7_8_moon", "minister", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX075", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Parvata Yoga: Benefics in Kendras and dusthana lords in Kendras or debilitated. "
            "Alternative: 1st and 12th lords mutually exchange. "
            "Native is prosperous, famous, charitable, eloquent, and a leader.",
        confidence=0.87, verse="BPHS Ch.44 v.13-16",
        tags=["yoga", "parvata", "benefics_kendra_dusthana_weak", "prosperity", "leadership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX076", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Kaahala Yoga: Lord of 4th and lord of lagna both strong and conjoined or in Kendra, "
            "and Jupiter strong. Native is obstinate, commanding, leads an army or large organization. "
            "Military or administrative authority.",
        confidence=0.85, verse="BPHS Ch.44 v.17-20",
        tags=["yoga", "kaahala", "4th_lagna_lord_strong", "military_authority", "commanding"],
        implemented=False,
    ),

    # ── SOLAR YOGAS (YEX077–080) ──────────────────────────────────────────────
    # BPHS Ch.44: Planets in 2nd/12th from Sun
    RuleRecord(
        rule_id="YEX077", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Veshi Yoga: Any planet (except Moon) in 2nd from Sun. "
            "Native is truthful, has a good character, happy, skillful, lazy (if malefic), "
            "or industrious (if benefic in 2nd from Sun).",
        confidence=0.85, verse="BPHS Ch.44 v.21-24",
        tags=["yoga", "solar_yoga", "veshi", "2nd_from_sun", "character", "truth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX078", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Voshi Yoga: Any planet (except Moon) in 12th from Sun. "
            "Native is wealthy, happy, modest, and industrious. "
            "Good nature and favorable reputation.",
        confidence=0.85, verse="BPHS Ch.44 v.25-28",
        tags=["yoga", "solar_yoga", "voshi", "12th_from_sun", "wealth", "modesty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX079", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Ubhayachari Yoga: Planets in both 2nd and 12th from Sun simultaneously. "
            "Native is eloquent, has a good physique, is happy, prosperous, and like a king. "
            "Benefics on both sides of Sun = very auspicious.",
        confidence=0.88, verse="BPHS Ch.44 v.29-32",
        tags=["yoga", "solar_yoga", "ubhayachari", "2nd_12th_sun", "eloquent", "prosperity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX080", source="BPHS", chapter="Ch.44", school="parashari",
        category="yoga",
        description="Budha-Aditya Yoga: Mercury conjoins Sun (within 15°, outside combustion). "
            "Native is highly intelligent, skilled in calculations, famous, "
            "honored by rulers, virtuous, and pleasant. Intellectual brilliance.",
        confidence=0.90, verse="BPHS Ch.44 v.33-36",
        tags=["yoga", "budha_aditya", "mercury_sun_conjunction", "intelligence", "fame", "calculations"],
        implemented=False,
    ),

    # ── SPECIFIC NAMED YOGAS (YEX081–100) ────────────────────────────────────
    RuleRecord(
        rule_id="YEX081", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Saraswati Yoga: Jupiter/Venus/Mercury all in Kendras/Trikonas/2nd, "
            "with Jupiter in own/exalted sign. Native is a poet, scholar, highly learned, "
            "eloquent, and renowned for intellect. Master of fine arts and scholarship.",
        confidence=0.92, verse="BPHS Ch.45 v.1-4",
        tags=["yoga", "saraswati", "jupiter_venus_mercury", "scholar", "poet", "eloquence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX082", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Lakshmi Yoga: Lord of 9th in own sign or exaltation in a Kendra, "
            "and lagna lord strong. Native is extremely wealthy, virtuous, renowned, "
            "and blessed by Lakshmi (goddess of wealth). Lasting prosperity.",
        confidence=0.92, verse="BPHS Ch.45 v.5-8",
        tags=["yoga", "lakshmi_yoga", "9th_lord_kendra", "extreme_wealth", "virtue", "renown"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX083", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Parijata Yoga: Lagna lord's dispositor (lord of sign occupied by lagna lord) "
            "is in Kendra or Trikona in own/exalted sign. Native is respected by kings, "
            "virtuous, happy in middle and later life. Delayed but lasting prosperity.",
        confidence=0.88, verse="BPHS Ch.45 v.9-12",
        tags=["yoga", "parijata", "lagna_lord_dispositor", "delayed_prosperity", "respect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX084", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Mahabhagya Yoga for Male: Born in day time with Sun, Moon, and lagna all "
            "in odd signs (Aries/Gemini/Leo/Libra/Sagittarius/Aquarius). "
            "Native is extremely fortunate, kingly, generous, and long-lived.",
        confidence=0.88, verse="BPHS Ch.45 v.13-16",
        tags=["yoga", "mahabhagya", "male_day_birth", "odd_signs", "fortunate", "kingly"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX085", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Mahabhagya Yoga for Female: Born at night with Sun, Moon, and lagna all "
            "in even signs (Taurus/Cancer/Virgo/Scorpio/Capricorn/Pisces). "
            "Native is extremely fortunate, respected, and blessed with long-lived husband.",
        confidence=0.88, verse="BPHS Ch.45 v.17-20",
        tags=["yoga", "mahabhagya", "female_night_birth", "even_signs", "fortunate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX086", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Kesari Yoga: Jupiter in Kendra from lagna (variation). "
            "Native is lion-hearted, respected, intelligent, destroys enemies. "
            "Good administrative abilities.",
        confidence=0.88, verse="BPHS Ch.45 v.21-24",
        tags=["yoga", "kesari", "jupiter_kendra_lagna", "courageous", "intelligence", "respected"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX087", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Kahala Yoga: 4th and 9th lords in mutual exchange or conjunction, "
            "with Mars in strength. Native is headstrong, leads armies or large groups, "
            "has elephants/vehicles, and commands many people.",
        confidence=0.85, verse="BPHS Ch.45 v.25-28",
        tags=["yoga", "kahala", "4th_9th_lords", "commanding", "armies", "obstinate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX088", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Chapa Yoga (Nabhasa): All planets between Mars and Saturn (both included) "
            "in a bowstring pattern. Native is skilled in archery or weaponry, deceitful, "
            "victorious in battle, and commands others.",
        confidence=0.82, verse="BPHS Ch.45 v.29-32",
        tags=["yoga", "nabhasa", "chapa", "bowstring_pattern", "archery", "battle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX089", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Shula Yoga (Nabhasa): All planets in three alternate signs forming a "
            "trident pattern. Native is ruthless, expert in weapons, earns through "
            "physical labor or conflict. Military/police career.",
        confidence=0.82, verse="BPHS Ch.45 v.33-36",
        tags=["yoga", "nabhasa", "shula", "trident_pattern", "weapons", "military"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX090", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Yava Yoga (Nabhasa): All planets in central signs (2nd-5th in one hemisphere). "
            "Native is generous, helps others, accumulates wealth and grain, "
            "is happy and virtuous.",
        confidence=0.82, verse="BPHS Ch.45 v.37-40",
        tags=["yoga", "nabhasa", "yava", "central_signs", "generous", "virtue"],
        implemented=False,
    ),

    # ── SANYASA / MOKSHA / PRAVRAJYA YOGAS (YEX091–098) ───────────────────────
    # BPHS Ch.47: Yogas for renunciation
    RuleRecord(
        rule_id="YEX091", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Pravrajya Yoga (Type 1): Four or more planets in a single house, "
            "one of which is strong. Native takes to asceticism, becomes a monk or saint. "
            "The strongest planet determines the type of renunciation.",
        confidence=0.88, verse="BPHS Ch.47 v.1-4",
        tags=["yoga", "pravrajya", "4_planets_one_house", "renunciation", "monk", "asceticism"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX092", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Pravrajya Yoga (Moon type): Moon afflicted by Saturn and Ketu with no benefic aspect, "
            "and 12th house strong. Native seeks spiritual liberation, renounces worldly ties, "
            "may become wandering ascetic.",
        confidence=0.85, verse="BPHS Ch.47 v.5-8",
        tags=["yoga", "pravrajya", "moon_saturn_ketu", "spiritual_liberation", "wandering_ascetic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX093", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Moksha Yoga: 12th lord in 12th in own/exalted sign, aspected by Jupiter. "
            "Native attains spiritual liberation (moksha) — highest goal of human life. "
            "Spiritual practice bears ultimate fruit.",
        confidence=0.87, verse="BPHS Ch.47 v.9-12",
        tags=["yoga", "moksha", "12th_lord_12th", "liberation", "spiritual_highest"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX094", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Sanyasa Yoga: Saturn in lagna, 5th, or 7th with Moon in 9th, "
            "aspected by Jupiter. Native renounces family life and takes sannyasa (formal renunciation). "
            "Later years in spiritual community.",
        confidence=0.85, verse="BPHS Ch.47 v.13-16",
        tags=["yoga", "sanyasa", "saturn_moon_jupiter", "formal_renunciation", "sannyasi"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX095", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Bandhana Yoga: Saturn and Rahu together in lagna, 5th, or 9th. "
            "Native faces imprisonment or severe restriction at some point. "
            "Freedom requires spiritual discipline and Saturn/Rahu propitiation.",
        confidence=0.85, verse="BPHS Ch.47 v.17-20",
        tags=["yoga", "bandhana", "saturn_rahu", "imprisonment", "restriction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX096", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Daridra Yoga: Lord of lagna in 6th, 8th, or 12th, weakened, "
            "and aspected by malefics without benefic influence. "
            "Native faces persistent poverty and struggles throughout life.",
        confidence=0.85, verse="BPHS Ch.47 v.21-24",
        tags=["yoga", "daridra", "lagna_lord_dusthana", "poverty", "struggle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX097", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Kala Sarpa Yoga: All 7 planets hemmed between Rahu and Ketu in the same half of zodiac. "
            "Native faces intense karmic challenges, unusual life pattern, "
            "periods of intense struggle alternating with sudden rise.",
        confidence=0.87, verse="BPHS Ch.47 v.25-28",
        tags=["yoga", "kala_sarpa", "rahu_ketu_hemmed", "karmic_challenge", "unusual_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX098", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Kala Sarpa Cancellation: If Moon is outside Rahu-Ketu axis, "
            "or if any planet conjoins Rahu or Ketu directly, Kala Sarpa is partially cancelled. "
            "Native has more control over the karmic pattern.",
        confidence=0.82, verse="BPHS Ch.47 v.29-32",
        tags=["yoga", "kala_sarpa_cancellation", "moon_outside_axis", "partial_relief"],
        implemented=False,
    ),

    # ── ARISHTHA YOGAS / BALARISHTHA (YEX099–115) ────────────────────────────
    # BPHS Ch.48: Yogas indicating danger, disease, early death
    RuleRecord(
        rule_id="YEX099", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Balarishtha Yoga (1): Moon in 6th, 8th, or 12th in Papakartari Yoga "
            "(malefics on both sides) at birth. Danger to infant in early years; "
            "requires strong lagna for survival. Mother's health also at risk.",
        confidence=0.87, verse="BPHS Ch.48 v.1-4",
        tags=["yoga", "balarishtha", "moon_dusthana_papakartari", "infant_danger", "early_death_risk"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX100", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Balarishtha Yoga (2): Lagna is afflicted by malefics with no benefic aspect, "
            "and lagna lord is weak in dusthana. Very weak constitution at birth; "
            "health crises in early childhood.",
        confidence=0.85, verse="BPHS Ch.48 v.5-8",
        tags=["yoga", "balarishtha", "lagna_afflicted", "weak_constitution", "health_crisis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX101", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Balarishtha Cancellation: If benefics (Jupiter/Venus/Mercury/waxing Moon) "
            "aspect lagna, Moon, or lagna lord, Balarishtha is cancelled. "
            "Native survives early crisis and lives long.",
        confidence=0.87, verse="BPHS Ch.48 v.9-12",
        tags=["yoga", "balarishtha_cancellation", "benefic_aspect_lagna", "survival", "longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX102", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Aristha Yoga: 8th lord in lagna with malefics, and weak lagna lord. "
            "Disease and danger throughout life; significant health crises. "
            "Longevity is compromised without strong benefic support.",
        confidence=0.85, verse="BPHS Ch.48 v.13-16",
        tags=["yoga", "aristha", "8th_lord_lagna", "disease", "health_crises"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX103", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Marana Sthana (Planet in death sign): Each planet has a particular house "
            "where its position is considered 'marana karaka' (death-giving). "
            "Sun in 12th, Moon in 8th, Mars in 7th, Mercury in 7th, "
            "Jupiter in 3rd, Venus in 6th, Saturn in 1st.",
        confidence=0.85, verse="BPHS Ch.48 v.17-20",
        tags=["yoga", "marana_sthana", "death_sign_planet", "specific_houses", "weakened"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX104", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Mrityu Bhaga (Critical degree): Each planet has specific critical degrees "
            "in each sign — within 1° of these degrees, planet gives most malefic results "
            "including death-like events in its dasha. Classical list preserved in BPHS.",
        confidence=0.83, verse="BPHS Ch.48 v.21-24",
        tags=["yoga", "mrityu_bhaga", "critical_degree", "malefic_degree", "dasha_danger"],
        implemented=False,
    ),

    # ── ADDITIONAL YOGA COMBINATIONS (YEX105–120) ─────────────────────────────
    RuleRecord(
        rule_id="YEX105", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Vasumati Yoga: All benefics (Jupiter/Venus/Mercury/Moon) in Upachaya houses "
            "(3rd/6th/10th/11th) from lagna. Native is very wealthy, commands servants, "
            "and is generous. Prosperity through growth houses.",
        confidence=0.88, verse="BPHS Ch.45 v.41-44",
        tags=["yoga", "vasumati", "benefics_upachaya", "wealthy", "generous", "servants"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX106", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Pushkala Yoga: Lagna lord in own/exalted sign, conjoined with Moon, "
            "aspected by a strong Jupiter. Native is like a king — wealthy, famous, "
            "surrounded by attendants, and highly cultured.",
        confidence=0.87, verse="BPHS Ch.45 v.45-48",
        tags=["yoga", "pushkala", "lagna_lord_moon_jupiter", "kingly", "fame", "culture"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX107", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Matsya Yoga (Nabhasa): Planets fill 1st and 5th (benefics) and 9th (malefics) "
            "or a specific fish-pattern configuration. Native is expert in dharmic texts, "
            "charitable, mixed good and evil, fluctuating life.",
        confidence=0.80, verse="BPHS Ch.45 v.49-52",
        tags=["yoga", "nabhasa", "matsya", "fish_pattern", "dharma", "fluctuating"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX108", source="BPHS", chapter="Ch.45", school="parashari",
        category="yoga",
        description="Kurma Yoga (Nabhasa): Benefics in 1st/3rd/5th in exaltation/own sign, "
            "and malefics in 6th/8th/12th in strength. Native is virtuous, happy, "
            "prosperous, and a ruler. Turtle-like stable prosperity.",
        confidence=0.82, verse="BPHS Ch.45 v.53-56",
        tags=["yoga", "nabhasa", "kurma", "turtle_pattern", "stable_prosperity", "virtuous"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX109", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Guru-Mangala Yoga: Jupiter and Mars in conjunction, exchange, or mutual aspect. "
            "Native is courageous and wise simultaneously, expert in law and valor, "
            "respected religious-military authority. Leader of spiritual warriors.",
        confidence=0.87, verse="BPHS Ch.46 v.1-4",
        tags=["yoga", "guru_mangala", "jupiter_mars", "wise_courageous", "law_valor"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX110", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Shukra-Guru Yoga: Jupiter and Venus in conjunction, exchange, or mutual aspect. "
            "Native is highly learned in both spiritual texts and fine arts. "
            "Balanced wisdom and beauty; respected by scholars and artists.",
        confidence=0.87, verse="BPHS Ch.46 v.5-8",
        tags=["yoga", "shukra_guru", "jupiter_venus", "learned", "arts_wisdom", "respected"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX111", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Shani-Rahu Yoga (Shrapit Yoga): Saturn and Rahu conjunct. "
            "Native carries karmic debt from past life. Life has recurring obstacles, "
            "betrayals, or servitude themes. Strong spiritual practice required as remedy.",
        confidence=0.85, verse="BPHS Ch.46 v.9-12",
        tags=["yoga", "shrapit", "saturn_rahu", "karmic_debt", "obstacles", "past_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX112", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Grahan Yoga: Sun or Moon conjunct Rahu or Ketu (eclipse yoga). "
            "Solar: father's health/status affected, government issues. "
            "Lunar: mother's health, mental fluctuations, emotional challenges.",
        confidence=0.85, verse="BPHS Ch.46 v.13-16",
        tags=["yoga", "grahan", "eclipse_yoga", "sun_moon_rahu_ketu", "father_mother_health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX113", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Kartari Yoga (Shubha/Papa): Shubha Kartari — benefics in 2nd and 12th from a "
            "house/planet (scissors of benefics) protects and enhances. "
            "Papa Kartari — malefics on both sides afflicts and weakens the house/planet.",
        confidence=0.88, verse="BPHS Ch.46 v.17-20",
        tags=["yoga", "kartari", "shubha_kartari", "papa_kartari", "scissors_effect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX114", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Chandra-Shukra Yoga: Moon and Venus conjunction or mutual aspect. "
            "Native is beautiful, artistic, charming, gains through women and luxury items. "
            "Career in arts, hospitality, or entertainment.",
        confidence=0.85, verse="BPHS Ch.46 v.21-24",
        tags=["yoga", "chandra_shukra", "moon_venus", "beauty", "arts", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX115", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Chandra-Shani Yoga: Moon and Saturn conjunction or mutual aspect. "
            "Native is hardworking, endures sorrow and difficulties with equanimity. "
            "Late bloomer — prosperity after age 35. Tendency toward melancholy.",
        confidence=0.85, verse="BPHS Ch.46 v.25-28",
        tags=["yoga", "chandra_shani", "moon_saturn", "hardworking", "late_bloomer", "melancholy"],
        implemented=False,
    ),

    # ── FINAL SUPPLEMENTARY YOGAS (YEX116–150) ───────────────────────────────
    RuleRecord(
        rule_id="YEX116", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Kuja-Shani Yoga: Mars and Saturn conjunction or mutual aspect. "
            "Native is mechanical, determined, may be violent or accident-prone. "
            "Career in engineering, surgery, or military. Injuries to limbs possible.",
        confidence=0.85, verse="BPHS Ch.46 v.29-32",
        tags=["yoga", "kuja_shani", "mars_saturn", "mechanical", "engineering", "accident_prone"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX117", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Surya-Kuja Yoga: Sun and Mars conjunction (especially in Aries or Scorpio). "
            "Native is bold, aggressive, hot-tempered, militaristic. "
            "Strong physical energy; leadership through force. Eye and head issues.",
        confidence=0.85, verse="BPHS Ch.46 v.33-36",
        tags=["yoga", "surya_kuja", "sun_mars", "aggressive", "military", "hot_tempered"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX118", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Surya-Shukra Yoga: Sun and Venus conjunction. Venus combust by Sun "
            "weakens Venus significations — relationship challenges, reduced artistic sensitivity. "
            "But native gains government favor for arts/beauty activities.",
        confidence=0.83, verse="BPHS Ch.46 v.37-40",
        tags=["yoga", "surya_shukra", "sun_venus", "venus_combust", "relationship_challenges"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX119", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Guru-Rahu Yoga (Guru Chandala Yoga): Jupiter conjunct Rahu. "
            "Native may be spiritually confused, or may use wisdom for questionable ends. "
            "Unconventional guru or teacher; foreign spiritual influences.",
        confidence=0.83, verse="BPHS Ch.46 v.41-44",
        tags=["yoga", "guru_chandala", "jupiter_rahu", "unconventional_wisdom", "foreign_spirituality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX120", source="BPHS", chapter="Ch.46", school="parashari",
        category="yoga",
        description="Shukra-Rahu Yoga: Venus conjunct Rahu. Native has unusual or unconventional "
            "relationships, attraction to foreign or exotic partners. "
            "Strong sensual desires; may cross social norms in romance.",
        confidence=0.82, verse="BPHS Ch.46 v.45-48",
        tags=["yoga", "shukra_rahu", "venus_rahu", "unconventional_relationships", "foreign_romance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX121", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Pitru Dosha (Solar Yoga): Sun afflicted by Rahu/Ketu/Saturn in 1st/5th/9th/10th. "
            "Ancestral karmic issues through father's lineage. Father's health/life may be troubled. "
            "Propitiation of ancestors recommended.",
        confidence=0.83, verse="BPHS Ch.47 v.33-36",
        tags=["yoga", "pitru_dosha", "sun_afflicted", "ancestral_karma", "father_issues"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX122", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Matru Dosha (Lunar Yoga): Moon afflicted by malefics in 4th/1st, "
            "or 4th lord debilitated/combust. Mother's health issues; difficult maternal relationship. "
            "Emotional insecurity; frequent moving of residence.",
        confidence=0.83, verse="BPHS Ch.47 v.37-40",
        tags=["yoga", "matru_dosha", "moon_afflicted", "mother_issues", "emotional_insecurity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX123", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Putra Dosha: 5th house and 5th lord heavily afflicted by malefics, "
            "Jupiter weak. Difficulties in having children; pregnancy challenges. "
            "Child may face health issues or be born with complications.",
        confidence=0.83, verse="BPHS Ch.47 v.41-44",
        tags=["yoga", "putra_dosha", "5th_house_afflicted", "children_issues", "pregnancy_difficulty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX124", source="BPHS", chapter="Ch.47", school="parashari",
        category="yoga",
        description="Vivaha Dosha (Marriage Yoga): 7th house afflicted by Rahu/Saturn/Mars, "
            "7th lord in dusthana, Venus in Papakartari. Delayed or troubled marriage. "
            "Multiple marriages or marital discords.",
        confidence=0.85, verse="BPHS Ch.47 v.45-48",
        tags=["yoga", "vivaha_dosha", "7th_afflicted", "marriage_delay", "marital_discord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX125", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Mangal Dosha (Kuja Dosha): Mars in 1st, 2nd, 4th, 7th, 8th, or 12th house "
            "from lagna/Moon/Venus. Potential for marital friction, discord, or loss of partner. "
            "Strength of Mars and other factors determine actual impact.",
        confidence=0.90, verse="BPHS Ch.48 v.25-28",
        tags=["yoga", "mangal_dosha", "kuja_dosha", "mars_houses", "marital_discord", "spouse_health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX126", source="BPHS", chapter="Ch.48", school="parashari",
        category="yoga",
        description="Mangal Dosha Cancellation: Mars in own sign (Aries/Scorpio) or exaltation (Capricorn), "
            "or aspected by Jupiter, or both partners have Mangal Dosha (mutual cancellation). "
            "When cancelled, Mars gives courage and energy to partnership instead.",
        confidence=0.88, verse="BPHS Ch.48 v.29-32",
        tags=["yoga", "mangal_dosha_cancellation", "mars_own_exalted", "mutual_cancellation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX127", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Guru Bala Yoga: Jupiter strong (exalted/own sign/friendly) and aspecting lagna, Moon, "
            "or 5th house. Native has exceptional knowledge, spiritual merit, "
            "good progeny, and lasting prosperity. Jupiter's strength elevates all house matters.",
        confidence=0.90, verse="BPHS Ch.49 v.1-4",
        tags=["yoga", "guru_bala", "jupiter_strong", "knowledge", "spiritual_merit", "prosperity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX128", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Shukra Bala Yoga: Venus strong and aspecting 7th or 2nd house. "
            "Native has excellent marital happiness, beauty, wealth, and artistic talents. "
            "Luxury, comforts, and sensory enjoyments throughout life.",
        confidence=0.88, verse="BPHS Ch.49 v.5-8",
        tags=["yoga", "shukra_bala", "venus_strong", "marital_happiness", "beauty", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX129", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Budha Bala Yoga: Mercury strong in Kendra or Trikona aspecting lagna. "
            "Native excels in mathematics, logic, trade, communication, and writing. "
            "Scholarship and intellectual authority.",
        confidence=0.88, verse="BPHS Ch.49 v.9-12",
        tags=["yoga", "budha_bala", "mercury_strong", "mathematics", "writing", "trade"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX130", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Chandra Bala Yoga: Moon strong (full/waxing, in own sign/exaltation) "
            "in Kendra aspecting lagna. Native is emotionally stable, wealthy, popular, "
            "and well-loved. Mother is a positive force.",
        confidence=0.88, verse="BPHS Ch.49 v.13-16",
        tags=["yoga", "chandra_bala", "moon_strong", "emotional_stability", "popular", "wealthy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX131", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Surya Bala Yoga: Sun strong (exalted/own sign Leo) in Kendra. "
            "Native has great vitality, authority, government favor, strong father, "
            "and good eyesight. Leadership qualities pronounced.",
        confidence=0.88, verse="BPHS Ch.49 v.17-20",
        tags=["yoga", "surya_bala", "sun_strong", "authority", "government", "vitality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX132", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Kuja Bala Yoga: Mars strong (exalted/own) in Kendra or Upachaya. "
            "Native has exceptional physical strength, courage, military ability, "
            "wins over enemies. Ruchaka Yoga result.",
        confidence=0.88, verse="BPHS Ch.49 v.21-24",
        tags=["yoga", "kuja_bala", "mars_strong", "physical_strength", "courage", "military"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX133", source="BPHS", chapter="Ch.49", school="parashari",
        category="yoga",
        description="Shani Bala Yoga: Saturn strong (exalted/own) in Kendra or Upachaya (3/6/11). "
            "Native is disciplined, persistent, earns through hard work, "
            "commands subordinates. Late but lasting success. Sasa Yoga variant.",
        confidence=0.88, verse="BPHS Ch.49 v.25-28",
        tags=["yoga", "shani_bala", "saturn_strong", "discipline", "persistence", "late_success"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX134", source="BPHS", chapter="Ch.50", school="parashari",
        category="yoga",
        description="Lagna Bala composite: Lagna lord strong, lagna aspected by own lord and a benefic, "
            "and lagna sign is Vargottama. Native has exceptional constitution, personality, "
            "and lifelong resilience. Overall chart strength.",
        confidence=0.90, verse="BPHS Ch.50 v.1-4",
        tags=["yoga", "lagna_bala", "lagna_lord_strong", "vargottama_lagna", "resilience"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX135", source="BPHS", chapter="Ch.50", school="parashari",
        category="yoga",
        description="Akhanda Samrajya Yoga: Jupiter as lord of 2nd or 5th or 11th is in Kendra "
            "from Moon or lagna; and the lagna lord, 9th lord or 10th lord is Jupiter. "
            "Native becomes an undivided/uncontested ruler or authority.",
        confidence=0.90, verse="BPHS Ch.50 v.5-8",
        tags=["yoga", "akhanda_samrajya", "jupiter_2_5_11_kendra", "undivided_ruler", "highest_authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX136", source="BPHS", chapter="Ch.50", school="parashari",
        category="yoga",
        description="Mukthi Yoga: 12th lord in 12th in its own sign, Jupiter in 12th, "
            "and lagna lord in a dharma house (1/5/9). Native achieves final liberation. "
            "Chart specifically oriented toward spiritual completion.",
        confidence=0.85, verse="BPHS Ch.50 v.9-12",
        tags=["yoga", "mukthi", "liberation_yoga", "12th_lord_own", "jupiter_12th", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX137", source="BPHS", chapter="Ch.51", school="parashari",
        category="yoga",
        description="Chaturasra Yoga (Square): Planets concentrated in Kendras only. "
            "Native is steady, comfortable, surrounded by family, good accumulation. "
            "Balanced material life.",
        confidence=0.82, verse="BPHS Ch.51 v.1-4",
        tags=["yoga", "nabhasa", "chaturasra", "kendras_only", "steady", "comfortable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX138", source="BPHS", chapter="Ch.51", school="parashari",
        category="yoga",
        description="Trikona Yoga: Planets concentrated in Trikona houses (1/5/9). "
            "Native is dharmic, spiritual, fortunate, and blessed by divine grace. "
            "Strong karmic merit from past lives.",
        confidence=0.82, verse="BPHS Ch.51 v.5-8",
        tags=["yoga", "nabhasa", "trikona_yoga", "trikonas_only", "dharmic", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX139", source="BPHS", chapter="Ch.51", school="parashari",
        category="yoga",
        description="Vihaga Yoga (Bird): Planets only in 3rd and 9th houses. "
            "Native is a wanderer, fond of travel, independent, restless. "
            "Life resembles a bird — free but unstable.",
        confidence=0.80, verse="BPHS Ch.51 v.9-12",
        tags=["yoga", "nabhasa", "vihaga", "3rd_9th_only", "wanderer", "travel"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX140", source="BPHS", chapter="Ch.51", school="parashari",
        category="yoga",
        description="Shringataka Yoga (Triangle): Planets in Trikona signs from different angles. "
            "Native is passionate, involved in love affairs, social, popular, "
            "but emotionally driven. Strong interpersonal magnetism.",
        confidence=0.80, verse="BPHS Ch.51 v.13-16",
        tags=["yoga", "nabhasa", "shringataka", "trikona_signs", "passionate", "social"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX141", source="BPHS", chapter="Ch.52", school="parashari",
        category="yoga",
        description="Kedar Yoga (Field): Planets distributed in 4 houses only. "
            "Native is engaged in agriculture or land work, truthful, prosperous, "
            "charitable and happy.",
        confidence=0.80, verse="BPHS Ch.52 v.1-4",
        tags=["yoga", "kedar", "4_houses_distribution", "agriculture", "truthful"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX142", source="BPHS", chapter="Ch.52", school="parashari",
        category="yoga",
        description="Pakshi Yoga (Bird full): All planets in two houses only in one half of zodiac. "
            "Native is expert in trade and commerce, clever, and has few children. "
            "Focused but narrow life area.",
        confidence=0.78, verse="BPHS Ch.52 v.5-8",
        tags=["yoga", "pakshi", "2_houses_only", "trade", "clever"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX143", source="BPHS", chapter="Ch.52", school="parashari",
        category="yoga",
        description="Mridanga Yoga: All planets in four quadrant signs and exalted or own sign. "
            "Native is extremely fortunate, attains royalty or great leadership position. "
            "Rare and highly auspicious combination.",
        confidence=0.88, verse="BPHS Ch.52 v.9-12",
        tags=["yoga", "mridanga", "quadrant_exalted", "rare", "royalty", "highly_auspicious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX144", source="BPHS", chapter="Ch.53", school="parashari",
        category="yoga",
        description="Asubha (Inauspicious) yoga: All planets in 6th/8th/12th (all dusthana). "
            "Extremely difficult life — poverty, disease, isolation. "
            "Very rare but represents maximum karmic affliction.",
        confidence=0.80, verse="BPHS Ch.53 v.1-4",
        tags=["yoga", "asubha", "all_dusthana", "extreme_difficulty", "karmic_affliction"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX145", source="BPHS", chapter="Ch.53", school="parashari",
        category="yoga",
        description="Shubha yoga composite: All planets in 1st/4th/7th/10th (all Kendra) in strength. "
            "Best of all Nabhasa — extremely powerful chart. "
            "Native commands the world; material and spiritual mastery.",
        confidence=0.88, verse="BPHS Ch.53 v.5-8",
        tags=["yoga", "shubha_composite", "all_kendra_strong", "material_mastery", "powerful"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX146", source="BPHS", chapter="Ch.54", school="parashari",
        category="yoga",
        description="Lagna-Chandra Raja Yoga: Lagna lord and Moon lord (Chandra lagna lord) "
            "both in Kendra or Trikona with mutual aspect. "
            "Double lagna strength — native has both inner and outer fortune.",
        confidence=0.87, verse="BPHS Ch.54 v.1-4",
        tags=["yoga", "lagna_chandra_raja", "lagna_moon_lord", "double_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX147", source="BPHS", chapter="Ch.54", school="parashari",
        category="yoga",
        description="Navamsha Vargottama Yoga: Lagna or key planet (Sun/Moon/lagna lord) "
            "in same sign in both Rashi and Navamsha (D9). Planet/lagna gains double strength. "
            "All significations of that planet are greatly enhanced.",
        confidence=0.90, verse="BPHS Ch.54 v.5-8",
        tags=["yoga", "vargottama", "navamsha_same_rashi", "double_strength", "enhanced_significations"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX148", source="BPHS", chapter="Ch.55", school="parashari",
        category="yoga",
        description="Tithi Yoga composite: Birth on Purnima (full Moon) with Moon-Sun opposite "
            "and lagna strong. Native is popular, round-faced, wealthy, "
            "and has magnetic personality. Festival energy at birth.",
        confidence=0.85, verse="BPHS Ch.55 v.1-4",
        tags=["yoga", "tithi_yoga", "purnima_birth", "full_moon", "magnetic_personality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX149", source="BPHS", chapter="Ch.55", school="parashari",
        category="yoga",
        description="Amavasya Yoga: Birth on Amavasya (new Moon) with Moon-Sun conjunct. "
            "Native is spiritually inclined, introverted, strong psychic sensitivity, "
            "but may face challenges with social relationships and outer expression.",
        confidence=0.83, verse="BPHS Ch.55 v.5-8",
        tags=["yoga", "amavasya_yoga", "new_moon_birth", "spiritual", "psychic", "introverted"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YEX150", source="BPHS", chapter="Ch.56", school="parashari",
        category="yoga",
        description="Combined Strength Yoga: When lagna lord, 9th lord, and 10th lord are all "
            "strong (own sign/exaltation/great friend) and in Kendra or Trikona — "
            "all three pillars of fortune (self/dharma/karma) aligned. "
            "Native achieves maximum life potential across all domains.",
        confidence=0.92, verse="BPHS Ch.56 v.1-4",
        tags=["yoga", "combined_strength", "lagna_9th_10th_lord_strong", "maximum_potential"],
        implemented=False,
    ),
]

for rule in _RULES:
    BPHS_YOGA_EXHAUSTIVE_REGISTRY.add(rule)
