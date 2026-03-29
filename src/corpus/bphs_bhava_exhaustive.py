"""
src/corpus/bphs_bhava_exhaustive.py — BPHS Bhava Exhaustive Encoding (S253)

Exhaustive encoding of all 12 bhava (house) significations from BPHS Ch.11-22.
Each house chapter covers: natural karakas, house significations, effects of
all 9 planets in that house, strength/weakness indicators, specific results.

Total: ~120 rules (BVX001–BVX120)
All: implemented=False
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_BHAVA_EXHAUSTIVE_REGISTRY = CorpusRegistry()

_RULES = [
    # ══════════════════════════════════════════════════════════════════════════
    # 1ST HOUSE (LAGNA / TANU BHAVA) — BPHS Ch.11
    # Karakas: Sun (body/soul), Lagna lord
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX001", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="1st House (Tanu Bhava) — primary significations: Physical body, constitution, "
            "complexion, personality, disposition, fame, strength, childhood, lifespan, "
            "self-identity, head/brain. Karaka: Sun (soul/vitality). "
            "Strong lagna = healthy body, magnetic personality, self-confidence.",
        confidence=0.95, verse="BPHS Ch.11 v.1-6",
        tags=["bhava", "1st_house", "tanu_bhava", "body", "personality", "sun_karaka", "lifespan"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX002", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="1st House — Sun in Lagna: Bold, commanding, leadership qualities, pitta constitution. "
            "Tendency toward eye ailments, fevers. Father influential. "
            "Strong vitality but ego-driven decisions. Best for Aries/Leo/Sagittarius lagnas.",
        confidence=0.90, verse="BPHS Ch.11 v.7-10",
        tags=["bhava", "1st_house", "sun_in_lagna", "bold", "leadership", "pitta", "eye_ailment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX003", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="1st House — Moon in Lagna: Attractive, emotional, sensitive, fluctuating health. "
            "Strong mother connection. Good for public life, popularity. "
            "Mind and body highly responsive to environment. Waxing Moon = strength.",
        confidence=0.90, verse="BPHS Ch.11 v.11-14",
        tags=["bhava", "1st_house", "moon_in_lagna", "attractive", "emotional", "public_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX004", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="1st House — Jupiter in Lagna: Wise, dignified, spiritually oriented, robust body. "
            "Long life, learned, respected. Best Hamsa Yoga position. "
            "Generous, fair-minded, favored by authorities.",
        confidence=0.92, verse="BPHS Ch.11 v.15-18",
        tags=["bhava", "1st_house", "jupiter_in_lagna", "wise", "dignified", "longevity", "respected"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX005", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="1st House — Saturn in Lagna: Marana Karaka Sthana for Saturn — worst placement. "
            "Lean body, dark complexion, slow and melancholic. Delays in all matters, "
            "early life hardships. BUT in Capricorn/Aquarius/Libra: Sasa Yoga — authority through discipline.",
        confidence=0.88, verse="BPHS Ch.11 v.19-22",
        tags=["bhava", "1st_house", "saturn_in_lagna", "marana_karaka", "hardship", "sasa_yoga_exception"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 2ND HOUSE (DHANA BHAVA) — BPHS Ch.12
    # Karakas: Jupiter (wealth), Mercury (speech)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX006", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House (Dhana Bhava) — primary significations: Accumulated wealth, speech, "
            "family, right eye, food, face, tongue, teeth, early education, savings, "
            "movable property. Karakas: Jupiter (wealth), Mercury (speech). "
            "Maraka house — affliction here threatens longevity.",
        confidence=0.95, verse="BPHS Ch.12 v.1-6",
        tags=["bhava", "2nd_house", "dhana_bhava", "wealth", "speech", "family", "maraka", "jupiter_karaka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX007", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Jupiter in 2nd: Excellent wealth accumulation, eloquent speech, "
            "large family, good eyesight, sweet voice. Natural dignity here. "
            "Financial prosperity through wisdom and legitimate means.",
        confidence=0.92, verse="BPHS Ch.12 v.7-10",
        tags=["bhava", "2nd_house", "jupiter_2nd", "wealth_excellent", "eloquent", "family_good"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX008", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Mercury in 2nd: Highly articulate, skilled in trading and writing. "
            "Multiple income streams. Good at mathematics, accounting. "
            "Sharp and witty communication. Financial gains through intellectual work.",
        confidence=0.90, verse="BPHS Ch.12 v.11-14",
        tags=["bhava", "2nd_house", "mercury_2nd", "articulate", "trade", "mathematics", "multiple_income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX009", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Mars in 2nd: Harsh speech, family conflicts, dental issues, "
            "eye problems (right). Quick financial gains and losses. "
            "Aggressive in money matters. Family relations strained by impulsiveness.",
        confidence=0.88, verse="BPHS Ch.12 v.15-18",
        tags=["bhava", "2nd_house", "mars_2nd", "harsh_speech", "family_conflict", "dental", "volatile_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX010", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Rahu in 2nd: Unusual speech patterns, foreign language facility, "
            "non-traditional wealth sources, unorthodox family. "
            "Tendency toward falsehood in speech; gains from foreign or unusual sources.",
        confidence=0.85, verse="BPHS Ch.12 v.19-22",
        tags=["bhava", "2nd_house", "rahu_2nd", "foreign_language", "unusual_wealth", "falsehood_speech"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 3RD HOUSE (SAHAJA BHAVA) — BPHS Ch.13
    # Karakas: Mars (courage/siblings), Mercury (communication)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX011", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House (Sahaja Bhava) — primary significations: Younger siblings, courage, "
            "short journeys, communication, writing, arms/shoulders/ears, neighbors, "
            "servants, mental inclinations, business initiatives. "
            "Karakas: Mars (valor/siblings), Mercury (communication). Upachaya — improves over time.",
        confidence=0.95, verse="BPHS Ch.13 v.1-6",
        tags=["bhava", "3rd_house", "sahaja_bhava", "siblings", "courage", "communication", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX012", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Mars in 3rd: Very courageous, overcomes all obstacles, "
            "younger siblings may be powerful or conflicted. Strong arms. "
            "Excellent for self-effort and initiative. "
            "Upachaya placement of natural karaka = strong results over time.",
        confidence=0.90, verse="BPHS Ch.13 v.7-10",
        tags=["bhava", "3rd_house", "mars_3rd", "courageous", "self_effort", "upachaya_natural"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX013", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Mercury in 3rd: Exceptional communicator, writer, journalist. "
            "Multiple siblings; good relations with neighbors. "
            "Skilled in short trips and quick transactions. "
            "Witty, adaptable, curious.",
        confidence=0.90, verse="BPHS Ch.13 v.11-14",
        tags=["bhava", "3rd_house", "mercury_3rd", "communicator", "writer", "witty"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX014", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Saturn in 3rd: Fewer or troubled younger siblings, methodical courage, "
            "persistence over quick action. Gains through sustained effort in 3rd house matters. "
            "Upachaya placement — Saturn here improves significantly with time.",
        confidence=0.87, verse="BPHS Ch.13 v.15-18",
        tags=["bhava", "3rd_house", "saturn_3rd", "persistence", "upachaya_good", "sibling_troubles"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 4TH HOUSE (SUKHA BHAVA) — BPHS Ch.14
    # Karakas: Moon (mother/happiness), Mercury (education), Mars (property), Venus (vehicles)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX015", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House (Sukha Bhava) — primary significations: Mother, domestic happiness, "
            "real estate/land, vehicles, education (foundational), chest/heart/lungs, "
            "inner peace, patrimony, wells/water bodies on land. "
            "Karakas: Moon (mother), Mercury (education), Mars (land), Venus (vehicles). "
            "Affliction here disturbs home life and relationship with mother.",
        confidence=0.95, verse="BPHS Ch.14 v.1-6",
        tags=["bhava", "4th_house", "sukha_bhava", "mother", "property", "happiness", "education_base"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX016", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Moon in 4th: Excellent placement for Moon — own natural Kendra. "
            "Deep mother connection, domestic happiness, popular, emotional stability. "
            "Good real estate luck. Native flourishes in home environment.",
        confidence=0.92, verse="BPHS Ch.14 v.7-10",
        tags=["bhava", "4th_house", "moon_4th", "excellent_placement", "domestic_happiness", "mother_excellent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX017", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Venus in 4th: Luxury home, beautiful vehicles, comfortable life. "
            "Good relationship with mother. Fond of domestic pleasures. "
            "Often own multiple properties. Best combination for real estate.",
        confidence=0.90, verse="BPHS Ch.14 v.11-14",
        tags=["bhava", "4th_house", "venus_4th", "luxury_home", "vehicles_excellent", "real_estate_good"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX018", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Sun in 4th: Domestic unhappiness, strained mother relationship, "
            "heart/chest issues. Frequent relocation. Government or authority matters affect home. "
            "Sun in Kendra is generally good for overall chart but 4th position challenges domesticity.",
        confidence=0.87, verse="BPHS Ch.14 v.15-18",
        tags=["bhava", "4th_house", "sun_4th", "domestic_trouble", "mother_strained", "relocation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX019", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Saturn in 4th: Persistent domestic challenges, delayed property acquisition. "
            "Mother may face health issues or be absent. "
            "BUT native eventually acquires substantial property through patience. "
            "Late-life domestic stability.",
        confidence=0.87, verse="BPHS Ch.14 v.19-22",
        tags=["bhava", "4th_house", "saturn_4th", "delayed_property", "mother_health", "late_stability"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 5TH HOUSE (PUTRA BHAVA) — BPHS Ch.15
    # Karakas: Jupiter (children/wisdom), Sun (intelligence)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX020", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House (Putra Bhava) — primary significations: Children (first-born focus), "
            "intelligence, creativity, speculation, past-life merits (Purva Punya), "
            "mantras/sacred chants, stomach/upper abdomen, romantic love affairs, "
            "government ministry. Karakas: Jupiter (progeny/wisdom), Sun (intelligence). "
            "Trikona — auspicious, carries dharmic merit.",
        confidence=0.95, verse="BPHS Ch.15 v.1-6",
        tags=["bhava", "5th_house", "putra_bhava", "children", "intelligence", "trikona", "purva_punya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX021", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Jupiter in 5th: Excellent — children are blessed and prosperous. "
            "Great intelligence, devotion to dharma, skilled in sacred texts. "
            "Natural karaka in own trikona — maximum wisdom expression.",
        confidence=0.93, verse="BPHS Ch.15 v.7-10",
        tags=["bhava", "5th_house", "jupiter_5th", "blessed_children", "excellent_intelligence", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX022", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Mercury in 5th: Highly analytical mind, good in mathematics and logic. "
            "Children are intelligent. Good at speculation through calculation. "
            "Writing, literary talent. Curious and quick-learning.",
        confidence=0.90, verse="BPHS Ch.15 v.11-14",
        tags=["bhava", "5th_house", "mercury_5th", "analytical", "mathematics", "literary", "curious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX023", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Sun in 5th: Intelligent, philosophical, government interest. "
            "Children may be few or arrive after difficulty. "
            "Stomach ailments. Authority through intellect. Father's influence on education.",
        confidence=0.88, verse="BPHS Ch.15 v.15-18",
        tags=["bhava", "5th_house", "sun_5th", "philosophical", "few_children", "stomach", "government"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX024", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Mars in 5th: Strong will, speculative tendency, impulsive investments. "
            "Children may be male-dominated or face health challenges. "
            "Short temper in romantic relationships. Stomach and abdominal issues.",
        confidence=0.87, verse="BPHS Ch.15 v.19-22",
        tags=["bhava", "5th_house", "mars_5th", "speculative", "impulsive", "children_health", "temper"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 6TH HOUSE (SHATRU BHAVA) — BPHS Ch.16
    # Karakas: Mars (enemies/service), Saturn (servants/disease)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX025", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House (Shatru Bhava) — primary significations: Enemies, disease, debts, "
            "service/employees, maternal uncle/aunt, routine work, digestive system/bowels, "
            "mental anxiety, obstacles, competition. Karakas: Mars (enemies/valor), Saturn (service/disease). "
            "Upachaya — natural malefics here grow stronger over time.",
        confidence=0.95, verse="BPHS Ch.16 v.1-6",
        tags=["bhava", "6th_house", "shatru_bhava", "enemies", "disease", "service", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX026", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Mars in 6th: Defeats all enemies; warrior energy in competition. "
            "Wins legal disputes, excels in military/police/surgery. "
            "Upachaya placement of natural karaka — very powerful for overcoming enemies.",
        confidence=0.92, verse="BPHS Ch.16 v.7-10",
        tags=["bhava", "6th_house", "mars_6th", "defeats_enemies", "military", "surgery", "legal_wins"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX027", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Saturn in 6th: Excellent for overcoming enemies and disease through "
            "persistence. Gains from service; good for managing large workforces. "
            "Delayed but complete victory over adversaries.",
        confidence=0.90, verse="BPHS Ch.16 v.11-14",
        tags=["bhava", "6th_house", "saturn_6th", "persistent_victory", "workforce", "service_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX028", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Jupiter in 6th: Mixed — Jupiter loses strength here (dusthana). "
            "Some protection from disease, but enemies may be influential. "
            "Gains from service but expenditure on litigation. "
            "6th lord Shakata Yoga activation when Jupiter in 6th from Moon.",
        confidence=0.85, verse="BPHS Ch.16 v.15-18",
        tags=["bhava", "6th_house", "jupiter_6th", "mixed_results", "disease_protected", "litigation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX029", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Moon in 6th: Emotional anxiety, digestive troubles, stomach issues. "
            "Fluctuating health. Maternal relatives may be adversarial. "
            "Native may be prone to worry and mental instability. "
            "Waxing Moon mitigates; waning Moon exacerbates.",
        confidence=0.87, verse="BPHS Ch.16 v.19-22",
        tags=["bhava", "6th_house", "moon_6th", "anxiety", "digestive", "mother_adversarial", "worry"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 7TH HOUSE (KALATRA BHAVA) — BPHS Ch.17
    # Karakas: Venus (marriage/desire), Jupiter (husband for female chart)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX030", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House (Kalatra Bhava) — primary significations: Spouse, marriage, "
            "business partnerships, foreign travel, lower abdomen/pelvis/kidneys, "
            "sexual relations, public dealings, contracts, open enemies. "
            "Karakas: Venus (desire/marriage), Jupiter (husband in female chart). "
            "Maraka house — 2nd strongest Maraka after 2nd.",
        confidence=0.95, verse="BPHS Ch.17 v.1-6",
        tags=["bhava", "7th_house", "kalatra_bhava", "spouse", "marriage", "maraka", "partnerships"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX031", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Venus in 7th: Excellent placement — beautiful, charming spouse. "
            "Happy marriage, sensual pleasures, good social reputation. "
            "Multiple relationships possible if afflicted. "
            "Natural karaka in own Kendra — maximum expression of Venus.",
        confidence=0.92, verse="BPHS Ch.17 v.7-10",
        tags=["bhava", "7th_house", "venus_7th", "beautiful_spouse", "happy_marriage", "excellent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX032", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Jupiter in 7th (Male chart): Spouse is wise, educated, well-to-do. "
            "Marriage is a source of dharmic growth. "
            "Partnership in business also blessed. Good for male charts.",
        confidence=0.90, verse="BPHS Ch.17 v.11-14",
        tags=["bhava", "7th_house", "jupiter_7th", "wise_spouse", "dharmic_marriage", "male_chart"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX033", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Mars in 7th (Mangal Dosha): Spouse's health at risk or "
            "marital discord through aggression. Possible separation or loss of partner. "
            "Cancellation if Mars is in Aries/Scorpio/Capricorn or aspected by Jupiter.",
        confidence=0.88, verse="BPHS Ch.17 v.15-18",
        tags=["bhava", "7th_house", "mars_7th", "mangal_dosha", "spouse_health", "marital_discord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX034", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Saturn in 7th: Delayed marriage, aged or serious spouse. "
            "Cold or difficult married life. Spouse may have health issues. "
            "BUT if in own sign (Capricorn/Aquarius/Libra exaltation): powerful and disciplined partnership.",
        confidence=0.87, verse="BPHS Ch.17 v.19-22",
        tags=["bhava", "7th_house", "saturn_7th", "delayed_marriage", "cold_married_life", "aged_spouse"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 8TH HOUSE (AYUR BHAVA) — BPHS Ch.18
    # Karakas: Saturn (longevity), Mars (sudden events)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX035", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House (Ayur Bhava) — primary significations: Longevity, death, chronic disease, "
            "legacy/inheritance, occult knowledge, sudden events, unearned wealth, "
            "sexual organs/reproductive system, transformation, deep psychological matters. "
            "Karakas: Saturn (longevity/death), Mars (sudden events/surgery). "
            "Most difficult dusthana — natural malefics here can paradoxically strengthen longevity.",
        confidence=0.95, verse="BPHS Ch.18 v.1-6",
        tags=["bhava", "8th_house", "ayur_bhava", "longevity", "death", "occult", "inheritance", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX036", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Saturn in 8th: Long life (natural karaka in longevity house). "
            "But chronic illness, slow health deterioration. "
            "Gains from inheritance and legacy. "
            "Deep occult wisdom developed over time.",
        confidence=0.88, verse="BPHS Ch.18 v.7-10",
        tags=["bhava", "8th_house", "saturn_8th", "long_life", "chronic_illness", "inheritance", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX037", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Mars in 8th: Accident-prone, surgical interventions, violent incidents. "
            "Inheritance through conflict. Short temper leads to injuries. "
            "BUT if in Aries/Scorpio/Capricorn: extraordinary physical recovery and survival.",
        confidence=0.87, verse="BPHS Ch.18 v.11-14",
        tags=["bhava", "8th_house", "mars_8th", "accident_prone", "surgery", "inheritance_conflict"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX038", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Jupiter in 8th: Reduced but not eliminated effect — Jupiter loses strength. "
            "Some protection through wisdom. Interest in philosophy of death and liberation. "
            "Inheritance through legal/scholarly channels. Long life despite complications.",
        confidence=0.85, verse="BPHS Ch.18 v.15-18",
        tags=["bhava", "8th_house", "jupiter_8th", "philosophy_death", "spiritual_inheritance", "protected"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX039", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Moon in 8th: Marana Karaka Sthana for Moon — weakened. "
            "Mental disturbances, anxiety, fear of death. Mother's health may be compromised. "
            "Possible sudden emotional crises. Psychic sensitivity as compensating gift.",
        confidence=0.87, verse="BPHS Ch.18 v.19-22",
        tags=["bhava", "8th_house", "moon_8th", "marana_karaka", "anxiety", "psychic", "mother_health"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 9TH HOUSE (DHARMA BHAVA) — BPHS Ch.19
    # Karakas: Jupiter (dharma/fortune), Sun (father)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX040", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House (Dharma Bhava) — primary significations: Father, fortune, dharma, "
            "higher education, long journeys, philosophy, religion, law, guru/teacher, "
            "hips and thighs. Karakas: Jupiter (fortune/dharma), Sun (father). "
            "Best Trikona — highest auspiciousness. Strength here protects entire chart.",
        confidence=0.95, verse="BPHS Ch.19 v.1-6",
        tags=["bhava", "9th_house", "dharma_bhava", "father", "fortune", "trikona", "philosophy", "guru"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX041", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Jupiter in 9th: Exceptional fortune and dharmic merit. "
            "Father is wise and influential. "
            "Native attains high spiritual and educational standing. "
            "Most auspicious placement for overall life prosperity.",
        confidence=0.95, verse="BPHS Ch.19 v.7-10",
        tags=["bhava", "9th_house", "jupiter_9th", "exceptional_fortune", "spiritual", "most_auspicious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX042", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Sun in 9th: Strong father, government favor, powerful karma. "
            "Dharmic leadership; native becomes authority in philosophical/legal matters. "
            "Father's influence shapes destiny. Strong 9th Sun = Pitru Yoga positive.",
        confidence=0.92, verse="BPHS Ch.19 v.11-14",
        tags=["bhava", "9th_house", "sun_9th", "strong_father", "government", "dharmic_leader"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX043", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Mars in 9th: Active dharmic pursuits; father may be military or aggressive. "
            "Legal victories; energetic in religious pursuits. "
            "Can indicate conflict with father or over inheritance.",
        confidence=0.87, verse="BPHS Ch.19 v.15-18",
        tags=["bhava", "9th_house", "mars_9th", "father_military", "legal_victory", "dharma_active"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX044", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Saturn in 9th: Father may be strict, cold, or absent. "
            "Delays in fortune but eventual acquisition of great wisdom. "
            "Philosophical depth through suffering. "
            "Dharmic duty fulfilled through discipline rather than grace.",
        confidence=0.87, verse="BPHS Ch.19 v.19-22",
        tags=["bhava", "9th_house", "saturn_9th", "cold_father", "delayed_fortune", "wisdom_through_discipline"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 10TH HOUSE (KARMA BHAVA) — BPHS Ch.20
    # Karakas: Sun (authority), Saturn (karma/work), Jupiter (career wisdom), Mercury (business)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX045", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House (Karma Bhava) — primary significations: Career, profession, "
            "public status, authority, government, knees and joints. "
            "Father (secondary after 9th). Actions in the world. "
            "Karakas: Sun (authority), Saturn (consistent work), Jupiter (wisdom/management), Mercury (trade). "
            "Most powerful Kendra — the house of dharmic action.",
        confidence=0.95, verse="BPHS Ch.20 v.1-6",
        tags=["bhava", "10th_house", "karma_bhava", "career", "authority", "kendra", "public_status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX046", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Jupiter in 10th: Excellent — wise and ethical career. "
            "High managerial or judicial position. "
            "Respected for professional integrity. "
            "Gains through religion, law, or education.",
        confidence=0.93, verse="BPHS Ch.20 v.7-10",
        tags=["bhava", "10th_house", "jupiter_10th", "wise_career", "judicial", "respected", "ethical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX047", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Sun in 10th: Most powerful Kendra placement for Sun (Dig Bala). "
            "Government authority, leadership, fame through career. "
            "Father is prominent. Medical/administrative/executive success.",
        confidence=0.93, verse="BPHS Ch.20 v.11-14",
        tags=["bhava", "10th_house", "sun_10th", "dig_bala", "government", "fame", "executive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX048", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Saturn in 10th: Methodical career rise; discipline and persistence. "
            "Engineering, mining, construction, administration of large systems. "
            "Late but substantial career achievement. "
            "Sasa Yoga when Saturn in Capricorn/Aquarius/Libra in 10th.",
        confidence=0.90, verse="BPHS Ch.20 v.15-18",
        tags=["bhava", "10th_house", "saturn_10th", "methodical_career", "engineering", "late_achievement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX049", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Mars in 10th: Military, police, surgical career. "
            "Aggressive rise; competitive in profession. "
            "Can achieve high command positions. "
            "Some impulsiveness affects professional reputation.",
        confidence=0.88, verse="BPHS Ch.20 v.19-22",
        tags=["bhava", "10th_house", "mars_10th", "military", "aggressive_career", "command"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 11TH HOUSE (LABHA BHAVA) — BPHS Ch.21
    # Karakas: Jupiter (gains/elder siblings), Saturn (income/persistent gains)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX050", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House (Labha Bhava) — primary significations: Income, gains, elder siblings, "
            "friends, social networks, hopes and desires, left ear, ankles. "
            "Karakas: Jupiter (gains), Saturn (consistent income). "
            "Upachaya — strongest growth house. All planets except Ketu do well here.",
        confidence=0.95, verse="BPHS Ch.21 v.1-6",
        tags=["bhava", "11th_house", "labha_bhava", "income", "gains", "elder_siblings", "upachaya", "desires"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX051", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Jupiter in 11th: Excellent gains from multiple sources. "
            "Elder siblings are prosperous. Wide social network. "
            "Desires fulfilled; financial growth through wisdom and connections.",
        confidence=0.92, verse="BPHS Ch.21 v.7-10",
        tags=["bhava", "11th_house", "jupiter_11th", "excellent_gains", "prosperous_siblings", "desires_fulfilled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX052", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Saturn in 11th: Best Upachaya placement for Saturn — "
            "slow but massive income growth. Elder siblings face delays but eventually succeed. "
            "Gains from large organizations, government contracts, disciplined investment.",
        confidence=0.92, verse="BPHS Ch.21 v.11-14",
        tags=["bhava", "11th_house", "saturn_11th", "best_upachaya", "massive_income", "disciplined_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX053", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Mars in 11th: Strong competitive income, gains through "
            "initiative and enterprise. Elder siblings powerful. "
            "Financial gains through technical fields, real estate, or sports.",
        confidence=0.90, verse="BPHS Ch.21 v.15-18",
        tags=["bhava", "11th_house", "mars_11th", "competitive_income", "enterprise", "technical_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX054", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Moon in 11th: Gains through public, women, hospitality, or real estate. "
            "Fluctuating income tied to emotional cycles. "
            "Waxing Moon = excellent financial growth; waning = reduced.",
        confidence=0.88, verse="BPHS Ch.21 v.19-22",
        tags=["bhava", "11th_house", "moon_11th", "public_gains", "fluctuating_income", "real_estate"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # 12TH HOUSE (VYAYA BHAVA) — BPHS Ch.22
    # Karakas: Saturn (loss/liberation), Venus (bed pleasures), Ketu (moksha)
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX055", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House (Vyaya Bhava) — primary significations: Losses, expenditure, "
            "foreign residence, isolation, spiritual liberation, sleep and bed pleasures, "
            "feet, left eye, confinement/hospitals/ashrams. "
            "Karakas: Saturn (losses/karma), Venus (pleasures/liberation), Ketu (moksha). "
            "Dusthana — but spiritually the most significant house for liberation.",
        confidence=0.95, verse="BPHS Ch.22 v.1-6",
        tags=["bhava", "12th_house", "vyaya_bhava", "losses", "liberation", "foreign", "isolation", "moksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX056", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Ketu in 12th: Moksha placement — spiritual liberation highest priority. "
            "Native seeks isolation and spiritual retreat. "
            "Psychic gifts; connection to past-life memories. "
            "Losses transform into spiritual gains.",
        confidence=0.90, verse="BPHS Ch.22 v.7-10",
        tags=["bhava", "12th_house", "ketu_12th", "moksha_highest", "spiritual_retreat", "psychic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX057", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Venus in 12th: Bed pleasures, sensual expenditure. "
            "Losses through women or luxury. "
            "Foreign residence may involve pleasure-oriented lifestyle. "
            "Spiritual devotion through beauty and art.",
        confidence=0.87, verse="BPHS Ch.22 v.11-14",
        tags=["bhava", "12th_house", "venus_12th", "bed_pleasures", "sensual_expenditure", "foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX058", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Saturn in 12th: Expenditure on Saturnine matters (chronic illness care, "
            "debt service, institutional stay). BUT karmic debts eventually cleared. "
            "Long periods of isolation may precede spiritual liberation.",
        confidence=0.87, verse="BPHS Ch.22 v.15-18",
        tags=["bhava", "12th_house", "saturn_12th", "karmic_debt", "isolation", "debt_clearance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX059", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Jupiter in 12th: Spiritual wisdom in solitude; interest in moksha. "
            "Losses through generosity, religious donation. "
            "Eventually settles near spiritual center. "
            "Vimala Viparita Raja Yoga when 12th lord is Jupiter.",
        confidence=0.87, verse="BPHS Ch.22 v.19-22",
        tags=["bhava", "12th_house", "jupiter_12th", "spiritual_solitude", "religious_donation", "vimala"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX060", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Mars in 12th (Mangal Dosha variant): Expenditure through conflict, "
            "medical expenses, accidents abroad. Marital tension (Mangal Dosha). "
            "BUT in Scorpio: deep occult strength and hidden recovery power.",
        confidence=0.85, verse="BPHS Ch.22 v.23-26",
        tags=["bhava", "12th_house", "mars_12th", "mangal_dosha", "medical_expenses", "occult_strength"],
        implemented=False,
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # CROSS-HOUSE SIGNIFICATION RULES (BVX061–100)
    # Bhavat Bhavam, house strength, specific multi-house interactions
    # ══════════════════════════════════════════════════════════════════════════
    RuleRecord(
        rule_id="BVX061", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Bhavat Bhavam Rule: Each house's secondary house is counted the same distance "
            "from itself as it is from lagna. 4th from 4th = 7th (partner/property of mother). "
            "5th from 5th = 9th (grandchildren, fortune of children). "
            "This principle extends significations to second-order relationships.",
        confidence=0.90, verse="BPHS Ch.11 v.23-26",
        tags=["bhava", "bhavat_bhavam", "secondary_signification", "house_extension"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX062", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Vacant House Rule: A house with no planet is judged by its lord's sign, house, "
            "and aspects. A strong lord in good position = house significations thrive even without occupant. "
            "A weak lord in dusthana = house significations suffer.",
        confidence=0.90, verse="BPHS Ch.11 v.27-30",
        tags=["bhava", "vacant_house", "lord_position", "house_judgment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX063", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="House Strength Hierarchy: Kendra (1/4/7/10) > Trikona (5/9) > Upachaya (3/6/10/11) "
            "> Dusthana (6/8/12) > Maraka (2/7). Planets in Kendra gain angular strength. "
            "Same planet in trikona has trine strength. Dusthana weakens benefics, strengthens malefics.",
        confidence=0.93, verse="BPHS Ch.11 v.31-34",
        tags=["bhava", "house_strength", "kendra_trikona_hierarchy", "angular_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX064", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House as Maraka: Lord of 2nd and any planet in 2nd act as Maraka agents "
            "during their dasha/antardasha when natal longevity period nears completion. "
            "Maraka effect triggered by Maraka lord dasha + Maraka planet's transit on 8th lord.",
        confidence=0.90, verse="BPHS Ch.12 v.23-26",
        tags=["bhava", "2nd_maraka", "maraka_dasha", "longevity_timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX065", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House as Second Maraka: Lord of 7th is the second most powerful Maraka. "
            "Combined Maraka analysis: 2nd lord + 7th lord dashas sequentially = maximum Maraka period. "
            "Benefics in 2nd/7th delay death; malefics accelerate.",
        confidence=0.90, verse="BPHS Ch.17 v.23-26",
        tags=["bhava", "7th_maraka", "combined_maraka", "death_timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX066", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House Longevity Analysis: Three longevity categories from BPHS: "
            "Alpayu (short life < 32 yrs), Madhyayu (medium 32-64 yrs), Purnayu (long > 64 yrs). "
            "Determined by: lagna lord, 8th lord, and Saturn positions — strongest wins. "
            "Balarishtha yoga can shorten; benefic Yoga can extend.",
        confidence=0.90, verse="BPHS Ch.18 v.23-26",
        tags=["bhava", "8th_longevity", "alpayu", "madhyayu", "purnayu", "longevity_classification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX067", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House Purva Punya (Past Merit): Strong 5th house and lord with benefic aspect "
            "= exceptional merit from past births. Native receives unearned fortune, "
            "grace from gurus, and natural intelligence. "
            "Weak 5th = karmic obstacles in intellectual and creative domains.",
        confidence=0.90, verse="BPHS Ch.15 v.23-26",
        tags=["bhava", "5th_purva_punya", "past_merit", "karmic_grace", "intelligence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX068", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House Dig Bala: Planets gain directional strength in specific houses: "
            "Sun/Mars in 10th, Moon/Venus in 4th, Mercury/Jupiter in 1st, Saturn in 7th. "
            "Dig Bala adds up to 60 Shashtiamsas to planet's Shadbala. "
            "Opposite house = 0 Dig Bala (complete directional weakness).",
        confidence=0.92, verse="BPHS Ch.20 v.23-26",
        tags=["bhava", "dig_bala", "directional_strength", "sun_mars_10th", "moon_venus_4th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX069", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House Father Karakatva: Detailed BPHS analysis — 9th house represents father, "
            "9th lord's strength shows father's longevity and fortune. "
            "Sun afflicted in 9th = father ill or adversarial. "
            "Sun exalted in 9th = father very powerful and supportive.",
        confidence=0.90, verse="BPHS Ch.19 v.23-26",
        tags=["bhava", "9th_father", "sun_9th_father", "father_longevity", "father_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX070", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House Mother Karakatva: Moon's position relative to 4th house shows mother's condition. "
            "Moon afflicted in 4th = mother's health compromised. "
            "Moon exalted/own in 4th = devoted, healthy, long-lived mother. "
            "4th lord in 12th = mother may live abroad or in isolation.",
        confidence=0.90, verse="BPHS Ch.14 v.23-26",
        tags=["bhava", "4th_mother", "moon_4th_mother", "mother_longevity", "4th_lord_12th"],
        implemented=False,
    ),

    # ── SPECIFIC HOUSE-PLANET INTERACTIONS (BVX071–100) ─────────────────────
    RuleRecord(
        rule_id="BVX071", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Jupiter in 3rd: Marana Karaka Sthana for Jupiter. "
            "Jupiter weakened here — courage may override wisdom. "
            "Younger siblings may be influential. "
            "Writing/communication gifts despite Jupiter's weakness.",
        confidence=0.85, verse="BPHS Ch.13 v.19-22",
        tags=["bhava", "3rd_house", "jupiter_3rd", "marana_karaka_jupiter", "writing", "siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX072", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Venus in 6th: Marana Karaka Sthana for Venus. "
            "Relationship difficulties, health through sensual excess. "
            "BUT gains from service sector, medical, or fashion. "
            "Enemies may be female or connected to arts.",
        confidence=0.85, verse="BPHS Ch.16 v.23-26",
        tags=["bhava", "6th_house", "venus_6th", "marana_karaka_venus", "relationship_difficulty", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX073", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Mars in 7th Marana Karaka analysis: Mars in 7th is Mars's Marana Karaka. "
            "Spouse's vitality compromised; aggressive partnerships. "
            "Medical intervention in marriage. Separation or violence in extreme cases.",
        confidence=0.87, verse="BPHS Ch.17 v.27-30",
        tags=["bhava", "7th_house", "mars_7th_marana", "spouse_health", "separation_risk"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX074", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Saturn in 2nd: Delayed wealth, speech may be slow or serious. "
            "Frugal with money, builds wealth through discipline. "
            "Teeth and eye (right) issues. Family relations may be cold but stable.",
        confidence=0.87, verse="BPHS Ch.12 v.27-30",
        tags=["bhava", "2nd_house", "saturn_2nd", "delayed_wealth", "frugal", "dental_issues"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX075", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Mars in 4th (Mangal Dosha variant): Domestic conflicts, property disputes. "
            "Frequent relocation. Mother's health may suffer. "
            "BUT good for owning land and real estate eventually through assertive action.",
        confidence=0.87, verse="BPHS Ch.14 v.27-30",
        tags=["bhava", "4th_house", "mars_4th", "domestic_conflict", "mangal_dosha", "property_dispute"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX076", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Rahu in 6th: Excellent for overcoming enemies by unusual means. "
            "Competitive advantage in foreign contexts. "
            "Chronic or unusual diseases may arise. "
            "Service in foreign country or unusual profession.",
        confidence=0.85, verse="BPHS Ch.16 v.27-30",
        tags=["bhava", "6th_house", "rahu_6th", "overcomes_enemies_unusual", "foreign_service", "unusual_disease"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX077", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Rahu in 8th: Deep interest in occult, taboo, death mysteries. "
            "Sudden unexpected events — crisis and transformation. "
            "May inherit through unusual circumstances. "
            "Possible psychic experiences and paranormal encounters.",
        confidence=0.85, verse="BPHS Ch.18 v.27-30",
        tags=["bhava", "8th_house", "rahu_8th", "occult_deep", "sudden_crisis", "paranormal"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX078", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Ketu in 11th: Reduced fulfillment of material desires despite gains. "
            "Gains may come and go quickly. "
            "Elder siblings may be spiritual or detached. "
            "Best for spiritual fulfillment through social causes.",
        confidence=0.83, verse="BPHS Ch.21 v.23-26",
        tags=["bhava", "11th_house", "ketu_11th", "spiritual_gains", "material_unfulfillment", "quick_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX079", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Rahu in 12th: Foreign residence, unusual or clandestine expenses. "
            "Interest in foreign cultures and secret activities. "
            "Karmic debt from unusual sources. "
            "Possible psychic dreams and astral experiences.",
        confidence=0.83, verse="BPHS Ch.22 v.27-30",
        tags=["bhava", "12th_house", "rahu_12th", "foreign_unusual", "clandestine", "astral"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX080", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Moon in 10th: Excellent Dig Bala placement for Moon. "
            "Career in public service, hospitality, or nurturing professions. "
            "Popular figure; emotionally in tune with public sentiment. "
            "Career fluctuates with Moon cycles.",
        confidence=0.90, verse="BPHS Ch.20 v.27-30",
        tags=["bhava", "10th_house", "moon_10th", "dig_bala_moon", "public_career", "popular"],
        implemented=False,
    ),

    # ── HOUSE SIGNIFICATORS AND HEALTH MAPPING (BVX081–100) ─────────────────
    RuleRecord(
        rule_id="BVX081", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Body Parts — House Anatomy Mapping: 1st=head/brain, 2nd=face/teeth/right eye, "
            "3rd=neck/arms/shoulders, 4th=chest/heart/lungs, 5th=stomach/digestive, "
            "6th=intestines/lower abdomen, 7th=pelvis/kidneys/bladder, 8th=sexual organs, "
            "9th=hips/thighs, 10th=knees/joints, 11th=calves/ankles/left ear, 12th=feet/left eye.",
        confidence=0.92, verse="BPHS Ch.11 v.35-38",
        tags=["bhava", "body_anatomy", "house_body_mapping", "health_signification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX082", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="House Affliction and Disease: Malefic in a house + weak lord of that house "
            "= disease in corresponding body part. "
            "Multiple malefics aspecting = chronic or serious condition. "
            "Benefic in same house or benefic aspect on lord = protection from disease.",
        confidence=0.90, verse="BPHS Ch.11 v.39-42",
        tags=["bhava", "house_affliction", "disease_prediction", "malefic_in_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX083", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Ketu in 5th: Past-life spiritual knowledge manifest as intuition. "
            "Children may be spiritually gifted or fewer. "
            "Creative expression through mystical or unconventional channels. "
            "Detachment from speculation.",
        confidence=0.83, verse="BPHS Ch.15 v.27-30",
        tags=["bhava", "5th_house", "ketu_5th", "spiritual_intelligence", "fewer_children", "mystical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX084", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Rahu in 3rd: Extraordinary courage through unconventional means. "
            "Younger siblings may be foreign or unusual. "
            "Communication in foreign languages. "
            "Media, internet, or technology-based courage.",
        confidence=0.83, verse="BPHS Ch.13 v.23-26",
        tags=["bhava", "3rd_house", "rahu_3rd", "unconventional_courage", "foreign_communication", "technology"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX085", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Ketu in 3rd: Courage through spiritual detachment; unconcerned with danger. "
            "Fewer or detached siblings. "
            "Communication may be intuitive rather than analytical. "
            "Past-life warrior energy.",
        confidence=0.83, verse="BPHS Ch.13 v.27-30",
        tags=["bhava", "3rd_house", "ketu_3rd", "spiritual_courage", "detached_siblings", "intuitive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX086", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th House — Venus in 5th: Romantic creativity; artistic intelligence. "
            "Beautiful or talented children. "
            "Speculation through beauty industry, arts, or entertainment. "
            "Love affairs prominent; romantic charisma.",
        confidence=0.87, verse="BPHS Ch.15 v.31-34",
        tags=["bhava", "5th_house", "venus_5th", "romantic_creativity", "artistic", "beautiful_children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX087", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Moon in 7th: Emotionally sensitive spouse; variable in relationships. "
            "Popular in public dealings. "
            "Marriage may be to someone younger or more nurturing. "
            "Business success through public appeal.",
        confidence=0.87, verse="BPHS Ch.17 v.31-34",
        tags=["bhava", "7th_house", "moon_7th", "emotional_spouse", "public_dealings", "nurturing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX088", source="BPHS", chapter="Ch.17", school="parashari",
        category="bhava_signification",
        description="7th House — Mercury in 7th: Intellectual spouse; marriage based on communication. "
            "Business partnerships through writing, trade. "
            "Multiple partnerships or dual relationships possible. "
            "Bhadra Yoga variant if Mercury in own sign.",
        confidence=0.87, verse="BPHS Ch.17 v.35-38",
        tags=["bhava", "7th_house", "mercury_7th", "intellectual_spouse", "dual_partnerships", "trade"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX089", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Venus in 9th: Guru is artistic or gracious. "
            "Foreign pilgrimages; beautiful places of worship. "
            "Fortune through beauty industry, fashion, or entertainment. "
            "Dharma practiced with aesthetic devotion.",
        confidence=0.85, verse="BPHS Ch.19 v.27-30",
        tags=["bhava", "9th_house", "venus_9th", "artistic_guru", "fortune_beauty", "dharma_aesthetic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX090", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Moon in 9th: Fortune connected to women, public, and emotional intelligence. "
            "Mother may be spiritually influential. "
            "Pilgrimage near water bodies. "
            "Luck fluctuates with lunar cycles.",
        confidence=0.85, verse="BPHS Ch.19 v.31-34",
        tags=["bhava", "9th_house", "moon_9th", "fortune_women", "spiritual_mother", "pilgrimage"],
        implemented=False,
    ),

    # ── HOUSE LORD IN HOUSES SUMMARY RULES (BVX091–110) ─────────────────────
    RuleRecord(
        rule_id="BVX091", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Lagna Lord in 1st: Strong self-identity; native is healthy and self-reliant. "
            "Career and life direction determined by own initiative. "
            "Body is vehicle for dharma.",
        confidence=0.90, verse="BPHS Ch.11 v.43-46",
        tags=["bhava", "lagna_lord_1st", "self_identity", "healthy", "self_reliant"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX092", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Lagna Lord in 6th: Health challenges; life oriented around service or competition. "
            "Enemies may be prominent. "
            "Career in health, service, or legal fields. "
            "Harsha Viparita potential if 6th lord also in 6/8/12.",
        confidence=0.87, verse="BPHS Ch.11 v.47-50",
        tags=["bhava", "lagna_lord_6th", "health_challenges", "service_career", "viparita_potential"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX093", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Lagna Lord in 8th: Difficult life; interest in occult, research. "
            "Chronic health issues possible. "
            "BUT if strong (own/exalted): long life, gain through legacy. "
            "Transformation is a central life theme.",
        confidence=0.87, verse="BPHS Ch.11 v.51-54",
        tags=["bhava", "lagna_lord_8th", "difficult_life", "occult", "transformation", "longevity_complex"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX094", source="BPHS", chapter="Ch.11", school="parashari",
        category="bhava_signification",
        description="Lagna Lord in 12th: Losses; possible foreign residence or spiritual life. "
            "Physical dissipation; identity loss in foreign lands. "
            "Vimala potential; strong spiritual orientation compensates for material loss.",
        confidence=0.87, verse="BPHS Ch.11 v.55-58",
        tags=["bhava", "lagna_lord_12th", "foreign_life", "spiritual", "material_loss"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX095", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th Lord in 10th: Excellent career — lord in own house. "
            "Great professional achievement, public recognition, leadership position. "
            "Karma and dharma aligned perfectly in professional domain.",
        confidence=0.92, verse="BPHS Ch.20 v.31-34",
        tags=["bhava", "10th_lord_10th", "excellent_career", "own_house", "leadership", "recognition"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX096", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th Lord in 6th/8th/12th: Career challenges, obstacles, hidden work. "
            "Possible break in career or service in difficult environments. "
            "Viparita potential if these lords exchange or conjoin.",
        confidence=0.85, verse="BPHS Ch.20 v.35-38",
        tags=["bhava", "10th_lord_dusthana", "career_obstacles", "hidden_work", "viparita_potential"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX097", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd Lord in 11th: Wealth flows from savings to income; excellent financial combination. "
            "Family (2nd) supports network (11th). "
            "Native earns through family connections.",
        confidence=0.90, verse="BPHS Ch.12 v.31-34",
        tags=["bhava", "2nd_lord_11th", "wealth_income", "family_network", "financial_excellent"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX098", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th Lord in 2nd: Income supports family wealth; elder siblings help family. "
            "Dhana Parivartana when 2nd-11th exchange — persistent prosperity.",
        confidence=0.88, verse="BPHS Ch.21 v.27-30",
        tags=["bhava", "11th_lord_2nd", "income_supports_wealth", "family_gains", "dhana_combination"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX099", source="BPHS", chapter="Ch.15", school="parashari",
        category="bhava_signification",
        description="5th Lord in 9th: Trikona exchange potential; fortune through children or creativity. "
            "Native's intelligence (5th) and dharma (9th) aligned. "
            "Excellent for higher education and philosophical writing.",
        confidence=0.90, verse="BPHS Ch.15 v.35-38",
        tags=["bhava", "5th_lord_9th", "trikona_link", "fortune_creativity", "higher_education"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX100", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th Lord in 5th: Dharma lord in intelligence house — auspicious. "
            "Past-life merit (5th) amplified by dharmic fortune (9th). "
            "Children become gurus or spiritual authorities. "
            "Native has exceptional philosophical intelligence.",
        confidence=0.90, verse="BPHS Ch.19 v.35-38",
        tags=["bhava", "9th_lord_5th", "dharma_intelligence", "spiritual_children", "philosophical"],
        implemented=False,
    ),

    # ── ADDITIONAL BHAVA RULES (BVX101–120) ──────────────────────────────────
    RuleRecord(
        rule_id="BVX101", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Mercury in 4th: Educated mother; learned domestic environment. "
            "Multiple properties or moves driven by education. "
            "Native is well-read and home-based intellectual.",
        confidence=0.85, verse="BPHS Ch.14 v.31-34",
        tags=["bhava", "4th_house", "mercury_4th", "educated_mother", "intellectual_home", "multiple_property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX102", source="BPHS", chapter="Ch.14", school="parashari",
        category="bhava_signification",
        description="4th House — Jupiter in 4th: Excellent happiness; wise mother, strong education. "
            "Abundant comforts and property. Large home and vehicles. "
            "Spiritual household; philosophical family.",
        confidence=0.90, verse="BPHS Ch.14 v.35-38",
        tags=["bhava", "4th_house", "jupiter_4th", "happiness_excellent", "wise_mother", "abundance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX103", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Mercury in 6th: Excellent analytical ability for solving problems. "
            "Gains from service sector, health administration, or legal writing. "
            "Sharp in debate and argumentation.",
        confidence=0.85, verse="BPHS Ch.16 v.31-34",
        tags=["bhava", "6th_house", "mercury_6th", "problem_solving", "legal_writing", "debate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX104", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Venus in 8th: Sensual pleasures may be hidden or secretive. "
            "Gains from partner's resources. "
            "Transformation through relationships; may inherit through marriage. "
            "Hidden beauty and charm.",
        confidence=0.83, verse="BPHS Ch.18 v.31-34",
        tags=["bhava", "8th_house", "venus_8th", "hidden_pleasures", "partner_resources", "secretive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX105", source="BPHS", chapter="Ch.18", school="parashari",
        category="bhava_signification",
        description="8th House — Mercury in 8th: Research ability, occult writing, analytical approach "
            "to death/transformation themes. Career in research, investigation, statistics. "
            "Hidden knowledge sought.",
        confidence=0.83, verse="BPHS Ch.18 v.35-38",
        tags=["bhava", "8th_house", "mercury_8th", "research", "occult_writing", "investigation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX106", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Venus in 11th: Gains through art, beauty, entertainment. "
            "Elder sisters may be prosperous. "
            "Social network includes creative, artistic, or affluent people. "
            "Income through luxury goods.",
        confidence=0.87, verse="BPHS Ch.21 v.31-34",
        tags=["bhava", "11th_house", "venus_11th", "gains_arts", "luxury_income", "creative_network"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX107", source="BPHS", chapter="Ch.21", school="parashari",
        category="bhava_signification",
        description="11th House — Mercury in 11th: Gains through trade, communication, and networking. "
            "Multiple income streams from diverse sources. "
            "Clever financial management.",
        confidence=0.87, verse="BPHS Ch.21 v.35-38",
        tags=["bhava", "11th_house", "mercury_11th", "trade_gains", "multiple_income", "financial_clever"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX108", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Moon in 12th: Emotional expenditure; restless sleep. "
            "Psychic dreams and subconscious activity. "
            "Mother may be in foreign land. "
            "Spiritual sensitivity through emotional introspection.",
        confidence=0.85, verse="BPHS Ch.22 v.31-34",
        tags=["bhava", "12th_house", "moon_12th", "psychic_dreams", "emotional_expenditure", "mother_foreign"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX109", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Mercury in 12th: Expenditure through communication, writing for others. "
            "Hidden intellectual work; research in isolated settings. "
            "Foreign language studies. "
            "Losses from signed documents or contracts.",
        confidence=0.83, verse="BPHS Ch.22 v.35-38",
        tags=["bhava", "12th_house", "mercury_12th", "hidden_intellect", "foreign_language", "document_losses"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX110", source="BPHS", chapter="Ch.20", school="parashari",
        category="bhava_signification",
        description="10th House — Venus in 10th: Career in arts, beauty, entertainment, fashion. "
            "Malavya Yoga if in Taurus/Libra/Pisces in 10th. "
            "Charming professional persona; liked by colleagues.",
        confidence=0.88, verse="BPHS Ch.20 v.39-42",
        tags=["bhava", "10th_house", "venus_10th", "arts_career", "entertainment", "malavya_10th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX111", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Moon in 3rd: Emotional connection to siblings; nurturing toward neighbors. "
            "Short journeys driven by emotional needs. "
            "Writing with emotional depth. "
            "Fluctuating courage tied to emotional state.",
        confidence=0.85, verse="BPHS Ch.13 v.31-34",
        tags=["bhava", "3rd_house", "moon_3rd", "emotional_siblings", "emotional_writing", "fluctuating_courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX112", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Venus in 3rd: Artistic communication; music and performance. "
            "Siblings may be artistic. "
            "Short travels for pleasure. "
            "Charming and persuasive communication style.",
        confidence=0.85, verse="BPHS Ch.13 v.35-38",
        tags=["bhava", "3rd_house", "venus_3rd", "artistic_communication", "music", "charming"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX113", source="BPHS", chapter="Ch.13", school="parashari",
        category="bhava_signification",
        description="3rd House — Sun in 3rd: Bold communication; leadership in siblings group. "
            "Writing about authority subjects. "
            "Journeys on government work. "
            "Upachaya placement — grows in confidence over time.",
        confidence=0.85, verse="BPHS Ch.13 v.39-42",
        tags=["bhava", "3rd_house", "sun_3rd", "bold_communication", "government_journey", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX114", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Venus in 2nd: Beautiful face, sweet voice, sensual pleasures from food. "
            "Wealth through art, entertainment, or beauty industry. "
            "Family environment is aesthetically pleasing.",
        confidence=0.88, verse="BPHS Ch.12 v.35-38",
        tags=["bhava", "2nd_house", "venus_2nd", "beautiful_face", "sweet_voice", "wealth_arts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX115", source="BPHS", chapter="Ch.12", school="parashari",
        category="bhava_signification",
        description="2nd House — Moon in 2nd: Fluctuating family wealth; emotional attachment to money. "
            "Sweet speech and gentle voice. "
            "Family members are nurturing. "
            "Wealth through food, real estate, public dealings.",
        confidence=0.87, verse="BPHS Ch.12 v.39-42",
        tags=["bhava", "2nd_house", "moon_2nd", "fluctuating_wealth", "sweet_speech", "nurturing_family"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX116", source="BPHS", chapter="Ch.16", school="parashari",
        category="bhava_signification",
        description="6th House — Ketu in 6th: Excellent for defeating hidden enemies. "
            "Past-life service karma resolved. "
            "Unusual diseases may be diagnosed late but resolved spiritually. "
            "Natural healer in mystical/spiritual medicine.",
        confidence=0.83, verse="BPHS Ch.16 v.35-38",
        tags=["bhava", "6th_house", "ketu_6th", "defeats_hidden_enemies", "spiritual_healer", "karma_service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX117", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Mercury in 9th: Philosophical writing; multiple gurus or texts. "
            "Foreign languages for dharmic study. "
            "Higher education in multiple fields. "
            "Dharma through intellectual discourse.",
        confidence=0.87, verse="BPHS Ch.19 v.39-42",
        tags=["bhava", "9th_house", "mercury_9th", "philosophical_writing", "multiple_gurus", "dharma_intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX118", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Rahu in 9th: Unconventional dharma; foreign guru or philosophy. "
            "Fortune through foreign or unusual means. "
            "Ancestral/father's lineage may be non-traditional. "
            "Strong but unconventional spiritual path.",
        confidence=0.83, verse="BPHS Ch.19 v.43-46",
        tags=["bhava", "9th_house", "rahu_9th", "foreign_guru", "unconventional_dharma", "non_traditional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX119", source="BPHS", chapter="Ch.19", school="parashari",
        category="bhava_signification",
        description="9th House — Ketu in 9th: Spiritual liberation as dharmic goal; detached from fortune. "
            "Past-life dharmic authority — native is naturally wise. "
            "Material fortune may be secondary to spiritual pursuit.",
        confidence=0.83, verse="BPHS Ch.19 v.47-50",
        tags=["bhava", "9th_house", "ketu_9th", "spiritual_liberation", "past_life_wisdom", "detached_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BVX120", source="BPHS", chapter="Ch.22", school="parashari",
        category="bhava_signification",
        description="12th House — Sun in 12th: Marana Karaka Sthana for Sun — father may be "
            "absent or in foreign land. Expenditure through authority/ego. "
            "Low vitality; eye (left) issues. "
            "BUT foreign travel on government business is indicated.",
        confidence=0.85, verse="BPHS Ch.22 v.39-42",
        tags=["bhava", "12th_house", "sun_12th", "marana_karaka_sun", "father_foreign", "eye_left", "low_vitality"],
        implemented=False,
    ),
]

for rule in _RULES:
    BPHS_BHAVA_EXHAUSTIVE_REGISTRY.add(rule)
