"""
src/corpus/yoga_extended_rules.py — Extended Yoga Rules (S247)

Encodes classical yoga (planetary combination) rules beyond the basic
BPHS yogas covered in S222-S224. Covers Pancha Mahapurusha Yoga,
expanded Dhana Yogas, advanced Raja Yogas, Nabhasa Yogas, and
special combination patterns from multiple classical sources.

Sources:
  BPHS Ch.35-45 — Yoga Adhyaya (Parashara)
  Phala Deepika Ch.6 — Maha Purusha Yogas
  Brihat Jataka Ch.12 — Akriti (figure) Yogas / Nabhasa Yogas

30 rules total: YGE001-YGE030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

YOGA_EXTENDED_RULES_REGISTRY = CorpusRegistry()

_YOGA_EXTENDED_RULES = [
    # --- Pancha Mahapurusha Yogas (YGE001-005) ---
    RuleRecord(
        rule_id="YGE001",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="yoga",
        description=(
            "Ruchaka Yoga (Pancha Mahapurusha): Mars in own sign (Aries/Scorpio) or "
            "exaltation (Capricorn) AND in Kendra (1st/4th/7th/10th). "
            "Result: commander-like personality, military/police/athletic success, "
            "red complexion, strong physique, cruel enemies vanquished. "
            "Person will be famous for courage and physical achievements."
        ),
        confidence=0.93,
        verse="BPHS Ch.35 v.1-5",
        tags=["yoga", "pancha_mahapurusha", "ruchaka_yoga", "mars_kendra", "courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE002",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="yoga",
        description=(
            "Bhadra Yoga (Pancha Mahapurusha): Mercury in own sign (Gemini/Virgo) or "
            "exaltation (Virgo) AND in Kendra. "
            "Result: eloquent speaker, skilled in trade/commerce, sharp intellect, "
            "expertise in multiple subjects, green complexion, lion-like walk. "
            "Person succeeds through intellect, communication, and business acumen."
        ),
        confidence=0.93,
        verse="BPHS Ch.35 v.6-10",
        tags=["yoga", "pancha_mahapurusha", "bhadra_yoga", "mercury_kendra", "intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE003",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="yoga",
        description=(
            "Hamsa Yoga (Pancha Mahapurusha): Jupiter in own sign (Sagittarius/Pisces) or "
            "exaltation (Cancer) AND in Kendra. "
            "Result: knowledge of scriptures, righteous, beautiful proportioned body, "
            "fair complexion, delightful voice, helpful nature, spiritual authority. "
            "Person becomes a renowned teacher, judge, or spiritual leader."
        ),
        confidence=0.93,
        verse="BPHS Ch.35 v.11-15",
        tags=["yoga", "pancha_mahapurusha", "hamsa_yoga", "jupiter_kendra", "spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE004",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="yoga",
        description=(
            "Malavya Yoga (Pancha Mahapurusha): Venus in own sign (Taurus/Libra) or "
            "exaltation (Pisces) AND in Kendra. "
            "Result: beautiful physical appearance, artistic talents, luxury, wealth, "
            "happy domestic life, attractive to opposite sex, sweet voice. "
            "Person enjoys pleasures, arts, fame, and material comforts throughout life."
        ),
        confidence=0.93,
        verse="BPHS Ch.35 v.16-20",
        tags=["yoga", "pancha_mahapurusha", "malavya_yoga", "venus_kendra", "beauty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE005",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="yoga",
        description=(
            "Shasha Yoga (Pancha Mahapurusha): Saturn in own sign (Capricorn/Aquarius) or "
            "exaltation (Libra) AND in Kendra. "
            "Result: authority over forests/mines/real estate, knowledge of metals, "
            "service to masses, strong discipline, longevity, dark complexion. "
            "Person leads through persistence; often reaches position of great authority late in life."
        ),
        confidence=0.93,
        verse="BPHS Ch.35 v.21-25",
        tags=["yoga", "pancha_mahapurusha", "shasha_yoga", "saturn_kendra", "discipline"],
        implemented=False,
    ),
    # --- Nabhasa Yogas (YGE006-012) ---
    RuleRecord(
        rule_id="YGE006",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Nabhasa Yogas overview: Varahamihira's figure-based yogas depending on "
            "distribution of planets across houses. 32 main Nabhasa yogas in 4 groups: "
            "Akriti (figure), Sankhya (number), Ashraya (support), Dala (petal/lotus). "
            "These are chart-shape yogas revealing overall life destiny pattern."
        ),
        confidence=0.88,
        verse="BJ Ch.12 v.1-5",
        tags=["yoga", "nabhasa", "akriti", "sankhya", "figure_yoga", "varahamihira"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE007",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Rajju Yoga (Nabhasa): All planets in movable signs only (Aries, Cancer, Libra, Cap). "
            "Result: person loves travel, cannot stay settled, adventurous, loves freedom, "
            "often in transport/travel-related professions. Life has many relocations."
        ),
        confidence=0.85,
        verse="BJ Ch.12 v.6-9",
        tags=["yoga", "nabhasa", "rajju_yoga", "movable_signs", "travel", "wandering"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE008",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Musala Yoga (Nabhasa): All planets in fixed signs only (Taurus, Leo, Scorpio, Aquarius). "
            "Result: resolute, determined, inflexible, stubborn, persistent, wealthy, "
            "honored, known for their name and reputation surviving after death."
        ),
        confidence=0.85,
        verse="BJ Ch.12 v.10-13",
        tags=["yoga", "nabhasa", "musala_yoga", "fixed_signs", "resolute", "reputation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE009",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Nala Yoga (Nabhasa): All planets in dual/mutable signs only "
            "(Gemini, Virgo, Sagittarius, Pisces). "
            "Result: skilled in multiple trades/arts, versatile, communicative, "
            "indecisive, intellectual, restless mind, changes profession often."
        ),
        confidence=0.85,
        verse="BJ Ch.12 v.14-17",
        tags=["yoga", "nabhasa", "nala_yoga", "dual_signs", "versatile", "multiple_skills"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE010",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Mala Yoga / Sarpa Yoga (Nabhasa Sankhya yogas): "
            "Mala: All 7 planets in 7 consecutive houses = garland; very auspicious, "
            "famous, wealthy, honorable. "
            "Sarpa: All 7 planets in 3 consecutive houses = serpent; "
            "sinful nature, cruel, poor, dependent. These are extreme life patterns."
        ),
        confidence=0.83,
        verse="BJ Ch.12 v.18-25",
        tags=["yoga", "nabhasa", "mala_yoga", "sarpa_yoga", "7_consecutive", "extreme"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE011",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Shula Yoga (Nabhasa): Planets in 3 houses forming a trident/triangle shape. "
            "Result: combative nature, argumentative, skilled in debate, "
            "may suffer from weapons/surgery, becomes wealthy through perseverance. "
            "Shula (trident) = fighting spirit + eventual victory."
        ),
        confidence=0.82,
        verse="BJ Ch.12 v.26-30",
        tags=["yoga", "nabhasa", "shula_yoga", "3_houses", "combative", "trident"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE012",
        source="Brihat_Jataka",
        chapter="Ch.12",
        school="varahamihira",
        category="yoga",
        description=(
            "Yava / Kamala Yogas (Nabhasa): "
            "Yava (barley grain): planets in Kendras and Konas = balanced power; "
            "auspicious life with both material and spiritual success. "
            "Kamala (lotus): all planets in Kendras = highly prestigious, "
            "achiever of great fame, long-lasting legacy."
        ),
        confidence=0.83,
        verse="BJ Ch.12 v.31-38",
        tags=["yoga", "nabhasa", "yava_yoga", "kamala_yoga", "kendra_planets", "prestigious"],
        implemented=False,
    ),
    # --- Advanced Raja Yogas (YGE013-017) ---
    RuleRecord(
        rule_id="YGE013",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Viparita Raja Yoga: Lords of 6th, 8th, or 12th houses mutually exchanging "
            "or one in another's house (dushtana lords in dusthanas). "
            "Result: person rises after great hardships; enemies and obstacles destroy "
            "each other; unexpected elevation through crises and reversals. "
            "Particularly powerful when all 3 dusthana lords are involved."
        ),
        confidence=0.90,
        verse="BPHS Ch.36 v.1-8",
        tags=["yoga", "viparita_raja_yoga", "6_8_12_lords", "rise_through_hardship"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE014",
        source="BPHS",
        chapter="Ch.36",
        school="parashari",
        category="yoga",
        description=(
            "Mahabhagya Yoga: For males — born during daytime, Sun and Moon in odd signs, "
            "Lagna in odd sign. For females — born during night, Sun/Moon in even signs, "
            "Lagna in even sign. Result: great fortune, auspicious life, long-lived "
            "and wealthy, respected by king/authority. Very rare and powerful yoga."
        ),
        confidence=0.88,
        verse="BPHS Ch.36 v.9-16",
        tags=["yoga", "mahabhagya_yoga", "gender_specific", "day_night", "odd_even_sign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE015",
        source="BPHS",
        chapter="Ch.37",
        school="parashari",
        category="yoga",
        description=(
            "Parijata Yoga: Lagna lord or the dispositor of the lagna lord is in own sign, "
            "exaltation, or Moolatrikona — AND is aspected by the 9th lord or another strong "
            "benefic. Result: person rises to prominence in middle age, "
            "is famous, revered by kings, enjoys all worldly comforts."
        ),
        confidence=0.87,
        verse="BPHS Ch.37 v.1-8",
        tags=["yoga", "parijata_yoga", "lagna_lord_strong", "9th_lord_aspect", "prominence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE016",
        source="BPHS",
        chapter="Ch.38",
        school="parashari",
        category="yoga",
        description=(
            "Kesari Yoga: Moon in Kendra from Jupiter (or Jupiter in Kendra from Moon). "
            "Result: eloquent, courageous, destroys enemies, achieves fame, "
            "respected by kings, long-lived. Moon-Jupiter connection in angles = "
            "one of the most common yet genuinely auspicious yogas."
        ),
        confidence=0.90,
        verse="BPHS Ch.38 v.1-5",
        tags=["yoga", "kesari_yoga", "moon_jupiter_kendra", "fame", "eloquent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE017",
        source="BPHS",
        chapter="Ch.39",
        school="parashari",
        category="yoga",
        description=(
            "Amala Yoga: A natural benefic (Jupiter, Venus, or unafflicted Mercury) "
            "in the 10th from Lagna or 10th from Moon (without malefic influence). "
            "Result: spotless reputation, charitable, long-lived, respected by "
            "all communities, enduring fame. 'Amala' = spotless/pure."
        ),
        confidence=0.88,
        verse="BPHS Ch.39 v.1-5",
        tags=["yoga", "amala_yoga", "benefic_10th", "spotless_reputation", "charitable"],
        implemented=False,
    ),
    # --- Dhana Yoga Extended (YGE018-022) ---
    RuleRecord(
        rule_id="YGE018",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Lakshmi Yoga: Lagna lord is strong AND Venus is in own sign or exaltation "
            "in a Kendra or Trikona. "
            "Result: great wealth, beautiful spouse, many pleasures, fame, "
            "long-lived, blessed by Goddess Lakshmi, generous benefactor."
        ),
        confidence=0.88,
        verse="BPHS Ch.40 v.1-6",
        tags=["yoga", "lakshmi_yoga", "venus_strong", "lagna_lord_strong", "wealth_beauty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE019",
        source="BPHS",
        chapter="Ch.40",
        school="parashari",
        category="yoga",
        description=(
            "Saraswati Yoga: Jupiter, Venus, and Mercury are all in Kendra, Trikona, "
            "or 2nd house (strong positions). "
            "Result: highly intelligent, scholarly, expert in arts/sciences, "
            "eloquent poet/writer, respected for learning, fame through knowledge."
        ),
        confidence=0.88,
        verse="BPHS Ch.40 v.7-12",
        tags=["yoga", "saraswati_yoga", "jupiter_venus_mercury", "scholar", "artistic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE020",
        source="BPHS",
        chapter="Ch.41",
        school="parashari",
        category="yoga",
        description=(
            "Kahala Yoga: Lords of 4th and 9th are mutually in Kendra, OR 4th lord and "
            "lagna lord in mutual Kendra, both strong. "
            "Result: bold, stubborn, commands armies, rules over land/territory, "
            "amasses wealth through determination and bravery."
        ),
        confidence=0.85,
        verse="BPHS Ch.41 v.1-6",
        tags=["yoga", "kahala_yoga", "4th_9th_lord", "bold", "territory"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE021",
        source="Phala_Deepika",
        chapter="Ch.6",
        school="mantreswara",
        category="yoga",
        description=(
            "Phala Deepika Dhana Yogas: 2nd/11th lords mutually aspecting = consistent income. "
            "Jupiter in 2nd and 5th lord strong = inherited wealth + progeny wealth. "
            "Venus in 11th with 11th lord strong = gains through entertainment/arts. "
            "Mercury in 2nd or 11th strong = trading profits, writing income."
        ),
        confidence=0.86,
        verse="PD Ch.6 v.1-12",
        tags=["yoga", "dhana_yoga", "2nd_11th_lord", "jupiter_mercury_venus", "income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE022",
        source="BPHS",
        chapter="Ch.42",
        school="parashari",
        category="yoga",
        description=(
            "Chandra-Mangala Yoga: Moon and Mars conjunction or mutual aspect. "
            "Result: wealth through mother, bold financial decisions, "
            "skill in banking/finance, willingness to take risks for gain. "
            "If afflicted: rash decisions, conflict between emotions and actions."
        ),
        confidence=0.85,
        verse="BPHS Ch.42 v.1-5",
        tags=["yoga", "chandra_mangala_yoga", "moon_mars", "wealth", "financial_boldness"],
        implemented=False,
    ),
    # --- Spiritual and Renunciation Yogas (YGE023-026) ---
    RuleRecord(
        rule_id="YGE023",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Pravrajya Yoga (renunciation): 4 or more planets in one house, "
            "especially with Saturn as one of them. "
            "OR Moon+Saturn in mutual aspect with no benefics. "
            "Result: person renounces worldly life and takes to spiritual path/monkhood. "
            "Ketu conjunct Moon+Saturn intensifies this yoga."
        ),
        confidence=0.86,
        verse="BPHS Ch.43 v.1-8",
        tags=["yoga", "pravrajya_yoga", "renunciation", "4_planets_one_house", "monkhood"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE024",
        source="BPHS",
        chapter="Ch.43",
        school="parashari",
        category="yoga",
        description=(
            "Moksha Yoga: Lagna lord, 8th lord, and 12th lord all strong AND "
            "Ketu in Kendra or Trikona, aspected by Jupiter. "
            "Result: person has strong spiritual inclination and eventual liberation. "
            "Jupiter in 12th = moksha by grace and knowledge (Jnana Moksha)."
        ),
        confidence=0.84,
        verse="BPHS Ch.43 v.9-16",
        tags=["yoga", "moksha_yoga", "ketu_kendra", "jupiter_12th", "liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE025",
        source="Phala_Deepika",
        chapter="Ch.6",
        school="mantreswara",
        category="yoga",
        description=(
            "Sanyasa Yogas (renunciation): Moon in Navamsha of Saturn aspected by Saturn, "
            "OR Sun+Saturn in 10th. "
            "5+ planets in one sign (not counting Rahu/Ketu) = saint/hermit. "
            "Phala Deepika gives 21 types of Sanyasa yoga — signifying various paths of renunciation."
        ),
        confidence=0.83,
        verse="PD Ch.6 v.13-24",
        tags=["yoga", "sanyasa_yoga", "moon_saturn", "5_planets_one_sign", "renunciation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE026",
        source="BPHS",
        chapter="Ch.44",
        school="parashari",
        category="yoga",
        description=(
            "Bandhana Yoga (imprisonment/confinement): Saturn+Rahu in 12th or 6th, "
            "OR 12th lord and 6th lord together afflicting lagna lord. "
            "Result: legal troubles, confinement, hospital stays, or forced seclusion. "
            "Malefic Dasha + Bandhana yoga = risk of imprisonment/confinement."
        ),
        confidence=0.83,
        verse="BPHS Ch.44 v.1-8",
        tags=["yoga", "bandhana_yoga", "saturn_rahu_12th", "imprisonment", "confinement"],
        implemented=False,
    ),
    # --- Special and Rare Yogas (YGE027-030) ---
    RuleRecord(
        rule_id="YGE027",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="yoga",
        description=(
            "Anapha Yoga: A planet (other than Sun) in 12th from Moon. "
            "Result: good reputation, physical strength, healthy lifestyle, "
            "independent nature, avoids unnecessary dependencies. "
            "Quality depends on the aspecting planet — Jupiter = wisdom; Venus = pleasure."
        ),
        confidence=0.85,
        verse="BPHS Ch.45 v.1-5",
        tags=["yoga", "anapha_yoga", "planet_12th_moon", "reputation", "independence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE028",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="yoga",
        description=(
            "Sunapha Yoga: A planet (other than Sun) in 2nd from Moon. "
            "Result: self-made person, earns through personal effort, "
            "intelligent, wealthy, similar to a king in status. "
            "Quality depends on planet — Jupiter = wisdom-wealth; Mars = effort-wealth."
        ),
        confidence=0.85,
        verse="BPHS Ch.45 v.6-10",
        tags=["yoga", "sunapha_yoga", "planet_2nd_moon", "self_made", "effort_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE029",
        source="BPHS",
        chapter="Ch.45",
        school="parashari",
        category="yoga",
        description=(
            "Durudhara Yoga: Planets on both sides of Moon (2nd AND 12th from Moon). "
            "Result: enjoys vehicles, assistants, and luxuries; charitable; "
            "moderate wealth throughout life; protected on all sides. "
            "Stronger planets = stronger results; benefics = happy life."
        ),
        confidence=0.85,
        verse="BPHS Ch.45 v.11-15",
        tags=["yoga", "durudhara_yoga", "both_sides_moon", "vehicles", "moderate_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="YGE030",
        source="Phala_Deepika",
        chapter="Ch.6",
        school="mantreswara",
        category="yoga",
        description=(
            "Kartari Yoga (scissors/shear): Malefics in 2nd and 12th from any planet "
            "= Paapa Kartari (malefic scissors) — that planet's significations are cut off. "
            "Benefics in 2nd and 12th = Shubha Kartari (benefic scissors) — "
            "that planet's significations are enhanced and protected from all sides."
        ),
        confidence=0.87,
        verse="PD Ch.6 v.25-32",
        tags=["yoga", "kartari_yoga", "paapa_kartari", "shubha_kartari", "scissors_2nd_12th"],
        implemented=False,
    ),
]

for rule in _YOGA_EXTENDED_RULES:
    YOGA_EXTENDED_RULES_REGISTRY.add(rule)
