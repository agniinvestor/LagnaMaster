"""
src/corpus/bhava_phala_rules.py — Bhava Phala (House Results) Extended Rules (S249)

Encodes detailed significations and results for all 12 houses (Bhavas),
going beyond the basic house meanings to include: special house effects,
house lord placements, planetary occupation effects, and classical
house-related principles from BPHS and other texts.

Sources:
  BPHS Ch.11-22 — Bhava Phala Adhyaya
  Uttara Kalamrita Ch.4 — House Significations
  Phala Deepika Ch.7 — Bhava results

30 rules total: BPH001-BPH030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BHAVA_PHALA_RULES_REGISTRY = CorpusRegistry()

_BHAVA_PHALA_RULES = [
    # --- 1st House Extended (BPH001) ---
    RuleRecord(
        rule_id="BPH001",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "1st Bhava (Lagna) extended significations: Self, body, personality, "
            "birth circumstances, general health, vitality, physical appearance, "
            "fame, longevity (alongside 8th), early childhood, social status. "
            "Planets here color entire personality. "
            "Strong Lagna = strong chart. Weak Lagna = life challenges throughout."
        ),
        confidence=0.93,
        verse="BPHS Ch.11 v.1-12",
        tags=["bhava", "1st_house", "lagna", "self_body_health", "personality"],
        implemented=False,
    ),
    # --- 2nd House Extended (BPH002) ---
    RuleRecord(
        rule_id="BPH002",
        source="BPHS",
        chapter="Ch.12",
        school="parashari",
        category="bhava",
        description=(
            "2nd Bhava extended: Wealth accumulation, family, speech, food habits, "
            "eyes (right), face, early education, values, accumulated assets, "
            "Maraka (death-inflicting) effects, oral health. "
            "2nd lord strong in Kendra/Trikona = wealth and eloquent speech. "
            "Malefic in 2nd without benefic = harsh speech, financial ups and downs."
        ),
        confidence=0.90,
        verse="BPHS Ch.12 v.1-12",
        tags=["bhava", "2nd_house", "wealth_family_speech", "maraka", "eyes"],
        implemented=False,
    ),
    # --- 3rd House Extended (BPH003) ---
    RuleRecord(
        rule_id="BPH003",
        source="BPHS",
        chapter="Ch.13",
        school="parashari",
        category="bhava",
        description=(
            "3rd Bhava extended: Siblings (especially younger), courage, short journeys, "
            "communication skills, writing/media, right ear, shoulders, arms, "
            "self-effort, skill development, boldness. "
            "3rd house malefics = courage (harsha yoga). "
            "Benefics in 3rd = gentle, artistic, timid siblings."
        ),
        confidence=0.90,
        verse="BPHS Ch.13 v.1-12",
        tags=["bhava", "3rd_house", "siblings_courage_communication", "short_journeys"],
        implemented=False,
    ),
    # --- 4th House Extended (BPH004) ---
    RuleRecord(
        rule_id="BPH004",
        source="BPHS",
        chapter="Ch.14",
        school="parashari",
        category="bhava",
        description=(
            "4th Bhava extended: Mother, home/land/property, vehicles, education, "
            "emotional happiness, chest/lungs, ancestral property, fixed assets. "
            "4th lord in own sign/exaltation = happy domestic life, property. "
            "Malefics in 4th without benefic aspect = mother's health issues, domestic discord."
        ),
        confidence=0.90,
        verse="BPHS Ch.14 v.1-12",
        tags=["bhava", "4th_house", "mother_home_property", "vehicles_happiness"],
        implemented=False,
    ),
    # --- 5th House Extended (BPH005) ---
    RuleRecord(
        rule_id="BPH005",
        source="BPHS",
        chapter="Ch.15",
        school="parashari",
        category="bhava",
        description=(
            "5th Bhava extended: Children, intellect, creativity, romance, speculation, "
            "past-life merit (Purva Punya), spiritual practices, higher education, "
            "liver/stomach, disciples. "
            "5th lord with Jupiter = many children, intellectual success. "
            "Malefics in 5th = progeny challenges, digestive issues."
        ),
        confidence=0.90,
        verse="BPHS Ch.15 v.1-12",
        tags=["bhava", "5th_house", "children_intellect_creativity", "purva_punya"],
        implemented=False,
    ),
    # --- 6th House Extended (BPH006) ---
    RuleRecord(
        rule_id="BPH006",
        source="BPHS",
        chapter="Ch.16",
        school="parashari",
        category="bhava",
        description=(
            "6th Bhava extended: Diseases, enemies, debts, service/employment, "
            "litigation, maternal uncle, small animals, intestines, digestive tract. "
            "Strong 6th house = ability to overcome enemies and disease. "
            "Malefics in 6th = good (destroys enemies and disease). "
            "Benefics in 6th = gentle but may struggle with adversaries."
        ),
        confidence=0.90,
        verse="BPHS Ch.16 v.1-12",
        tags=["bhava", "6th_house", "disease_enemies_debt", "service", "dusthana"],
        implemented=False,
    ),
    # --- 7th House Extended (BPH007) ---
    RuleRecord(
        rule_id="BPH007",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="bhava",
        description=(
            "7th Bhava extended: Marriage partner, business partnerships, open enemies, "
            "foreign journeys, lower abdomen/kidneys, Maraka (death-inflicting). "
            "7th lord in Kendra/Trikona = fortunate marriage. "
            "Venus + 7th lord strong = beautiful, supportive spouse. "
            "Multiple planets in 7th (especially malefics) = relationship complications."
        ),
        confidence=0.90,
        verse="BPHS Ch.17 v.1-12",
        tags=["bhava", "7th_house", "marriage_partnerships", "maraka", "open_enemies"],
        implemented=False,
    ),
    # --- 8th House Extended (BPH008) ---
    RuleRecord(
        rule_id="BPH008",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="bhava",
        description=(
            "8th Bhava extended: Longevity, chronic illness, sudden events, legacies/inheritances, "
            "occult/research, transformation, reproductive organs, obstacles. "
            "8th lord in 8th = long life (Sarala Yoga). "
            "Benefic in 8th = inheritance, occult powers, transformation through knowledge. "
            "Malefic in 8th = accidents, surgery, hidden enemies."
        ),
        confidence=0.90,
        verse="BPHS Ch.18 v.1-12",
        tags=["bhava", "8th_house", "longevity_transformation_occult", "inheritance", "dusthana"],
        implemented=False,
    ),
    # --- 9th House Extended (BPH009) ---
    RuleRecord(
        rule_id="BPH009",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="bhava",
        description=(
            "9th Bhava extended: Dharma, fortune, father, guru, higher philosophy, "
            "long-distance travel, pilgrimage, hips/thighs, past-life virtues. "
            "9th lord strong = fortunate life, wise father, good luck. "
            "Jupiter in 9th = religious, teacher, blessed. "
            "Malefic in 9th = difficult father relationship, dharma challenges."
        ),
        confidence=0.90,
        verse="BPHS Ch.19 v.1-12",
        tags=["bhava", "9th_house", "dharma_fortune_father", "guru", "pilgrimage"],
        implemented=False,
    ),
    # --- 10th House Extended (BPH010) ---
    RuleRecord(
        rule_id="BPH010",
        source="BPHS",
        chapter="Ch.20",
        school="parashari",
        category="bhava",
        description=(
            "10th Bhava extended: Career/profession, authority, fame, government, "
            "knees/joints, dharmic action (Karma), reputation, public life. "
            "10th lord in 1st/5th/9th = excellent career. "
            "Multiple benefics in 10th = prestigious profession. "
            "Sun in 10th = Digbala (directional strength), government or authority role."
        ),
        confidence=0.90,
        verse="BPHS Ch.20 v.1-12",
        tags=["bhava", "10th_house", "career_authority_fame", "profession", "karma"],
        implemented=False,
    ),
    # --- 11th House Extended (BPH011) ---
    RuleRecord(
        rule_id="BPH011",
        source="BPHS",
        chapter="Ch.21",
        school="parashari",
        category="bhava",
        description=(
            "11th Bhava extended: Gains, income, elder siblings, friends, aspirations, "
            "left ear, social networks, fulfillment of desires. "
            "11th lord strong = consistent income, wish fulfillment. "
            "Malefics in 11th are favorable (Upachaya house — they improve over time). "
            "Jupiter in 11th = multiple income sources, generous friends."
        ),
        confidence=0.90,
        verse="BPHS Ch.21 v.1-12",
        tags=["bhava", "11th_house", "gains_income_friends", "aspirations", "upachaya"],
        implemented=False,
    ),
    # --- 12th House Extended (BPH012) ---
    RuleRecord(
        rule_id="BPH012",
        source="BPHS",
        chapter="Ch.22",
        school="parashari",
        category="bhava",
        description=(
            "12th Bhava extended: Losses/expenditure, foreign residence, spirituality/moksha, "
            "hospitalization/confinement, sleep quality, left eye, feet. "
            "12th lord in 12th = spiritual liberation (Vimala Yoga). "
            "Benefics in 12th = spiritual inclination, comfortable bed pleasures, foreign gains. "
            "Malefics in 12th = wasteful expenditure, forced isolation."
        ),
        confidence=0.90,
        verse="BPHS Ch.22 v.1-12",
        tags=["bhava", "12th_house", "losses_spirituality_foreign", "moksha", "dusthana"],
        implemented=False,
    ),
    # --- Bhava Phal Extended Principles (BPH013-018) ---
    RuleRecord(
        rule_id="BPH013",
        source="Uttara_Kalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="bhava",
        description=(
            "Bhavat Bhavam principle: Each house represents the same house counted from itself. "
            "5th from 5th = 9th (grandchildren, spiritual fortune). "
            "7th from 7th = 1st (the native's own nature in marriage). "
            "9th from 9th = 5th (disciples, intellectual fortune). "
            "This creates recursive layering in house interpretation."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.1-8",
        tags=["bhava", "bhavat_bhavam", "recursive_house", "5th_from_5th", "principle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH014",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Upachaya houses (growing houses): 3rd, 6th, 10th, 11th are Upachaya sthanas. "
            "Malefic planets in these houses improve over time — they energize these themes. "
            "Mars in 3rd = courage grows; Saturn in 6th = overcomes enemies; "
            "Sun in 10th = authority grows; Mars in 11th = persistent gains. "
            "Benefics here give good results but may be gentler."
        ),
        confidence=0.90,
        verse="BPHS Ch.11 v.13-20",
        tags=["bhava", "upachaya", "3_6_10_11", "malefic_favorable", "grows_over_time"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH015",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Dusthana houses (difficult houses): 6th, 8th, 12th are Dusthanas. "
            "Planets here face challenges in their significations. "
            "Natural malefics here may do less damage; natural benefics here may be weakened. "
            "Lords of Dusthanas becoming yogakarakas via Trikona ownership is an exception "
            "(they can give positive results despite Dusthana ownership)."
        ),
        confidence=0.90,
        verse="BPHS Ch.11 v.21-28",
        tags=["bhava", "dusthana", "6_8_12", "difficult_houses", "benefic_weakened"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH016",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Trikona houses (fortune triangles): 1st, 5th, 9th. The most auspicious houses. "
            "Lords of Trikona = Trikona adhipatis = inherently beneficial. "
            "Benefics in Trikona = excellent results for those house themes. "
            "Trikona lord + Kendra lord combination = Raja Yoga. "
            "Planet in own Trikona = maximum comfort in that area of life."
        ),
        confidence=0.92,
        verse="BPHS Ch.11 v.29-36",
        tags=["bhava", "trikona", "1_5_9", "fortune_houses", "adhipati"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH017",
        source="Phala_Deepika",
        chapter="Ch.7",
        school="mantreswara",
        category="bhava",
        description=(
            "House occupation effects — general principle: "
            "The significations of a house prosper when its lord is strong, "
            "unafflicted, and in a good house. "
            "The significations suffer when the lord is in 6/8/12, debilitated, "
            "combusted, or heavily aspected by malefics. "
            "Vacant houses take their results from the lord's placement."
        ),
        confidence=0.88,
        verse="PD Ch.7 v.1-8",
        tags=["bhava", "house_occupation", "lord_strength", "6_8_12_lord", "general_principle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH018",
        source="Phala_Deepika",
        chapter="Ch.7",
        school="mantreswara",
        category="bhava",
        description=(
            "Mutual exchange (Parivartana) between house lords: "
            "Mutual exchange between Kendra lords = power to deliver status and authority. "
            "Exchange between Trikona lords = great fortune and dharmic merit. "
            "Exchange between Kendra and Trikona = strong Raja Yoga type result. "
            "Exchange involving Dusthana lords with good lords = mixed, complex results."
        ),
        confidence=0.88,
        verse="PD Ch.7 v.9-18",
        tags=["bhava", "parivartana", "mutual_exchange", "kendra_trikona", "lord_exchange"],
        implemented=False,
    ),
    # --- Specific House Combinations (BPH019-025) ---
    RuleRecord(
        rule_id="BPH019",
        source="BPHS",
        chapter="Ch.12",
        school="parashari",
        category="bhava",
        description=(
            "2nd and 7th house Maraka principle: Lords of 2nd and 7th are Maraka (killer) lords. "
            "During their Dasha/Antardasha near longevity threshold, health crises occur. "
            "2nd lord + 7th lord in conjunction = double Maraka = high-risk period. "
            "Saturn additionally acts as Maraka when associated with these lords."
        ),
        confidence=0.88,
        verse="BPHS Ch.12 v.13-20",
        tags=["bhava", "maraka", "2nd_7th_lord", "longevity_threshold", "health_crisis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH020",
        source="BPHS",
        chapter="Ch.15",
        school="parashari",
        category="bhava",
        description=(
            "5th lord for progeny: 5th lord in Kendra/Trikona = children thrive. "
            "5th lord in 5th = strong children, multiple progeny. "
            "5th lord in 6/8/12 = difficulties with children. "
            "Jupiter + 5th lord in good aspect = son (in traditional texts). "
            "Venus + 5th lord prominent = daughter(s)."
        ),
        confidence=0.85,
        verse="BPHS Ch.15 v.13-20",
        tags=["bhava", "5th_house", "progeny", "5th_lord_kendra", "jupiter_venus"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH021",
        source="BPHS",
        chapter="Ch.19",
        school="parashari",
        category="bhava",
        description=(
            "9th house and fortune: 9th lord in Lagna = extremely fortunate, luck always present. "
            "9th lord in 5th = fortune through children and intellect. "
            "9th lord in 11th = gains from fortune; good income. "
            "9th lord in own sign or exaltation in Kendra = Dhana Yoga + Raja Yoga combined."
        ),
        confidence=0.87,
        verse="BPHS Ch.19 v.13-20",
        tags=["bhava", "9th_house", "fortune", "9th_lord_placement", "lucky"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH022",
        source="BPHS",
        chapter="Ch.18",
        school="parashari",
        category="bhava",
        description=(
            "8th house longevity assessment: 8th lord in 8th = long life (Sarala Yoga). "
            "8th lord in Lagna (strong) = intense longevity and occult powers. "
            "Saturn in 8th = longevity, chronic delays. "
            "Malefics in 8th without benefic aspect = sudden crises. "
            "Benefic in 8th = grace through transformation."
        ),
        confidence=0.86,
        verse="BPHS Ch.18 v.13-22",
        tags=["bhava", "8th_house", "longevity", "sarala_yoga", "saturn_8th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH023",
        source="Uttara_Kalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="bhava",
        description=(
            "11th house gains: 11th lord in 1st = self-generated income, entrepreneurial gains. "
            "11th lord in 2nd = wealth from family business. "
            "11th lord in 11th = consistent income stream. "
            "Multiple planets in 11th = multiple income sources. "
            "Jupiter in 11th = income through wisdom/teaching; Venus = arts."
        ),
        confidence=0.86,
        verse="UK Ch.4 v.9-16",
        tags=["bhava", "11th_house", "gains_income", "multiple_sources", "11th_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH024",
        source="Phala_Deepika",
        chapter="Ch.7",
        school="mantreswara",
        category="bhava",
        description=(
            "4th house property and happiness: 4th lord in Kendra = property, vehicles. "
            "Saturn in 4th = hardship to mother, ancestral property challenges. "
            "Mars in 4th = property gains through effort but home disputes. "
            "Moon in 4th (Digbala) = good for mother, domestic happiness. "
            "Jupiter in 4th = wisdom at home, spiritual atmosphere."
        ),
        confidence=0.86,
        verse="PD Ch.7 v.19-28",
        tags=["bhava", "4th_house", "property_happiness_mother", "digbala_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH025",
        source="BPHS",
        chapter="Ch.17",
        school="parashari",
        category="bhava",
        description=(
            "7th house marriage timing: Jupiter transiting 7th from natal Moon + "
            "7th lord Dasha = marriage timing indicator. "
            "Venus strong in chart + 7th lord in Kendra/Trikona = early marriage. "
            "7th lord in 6/8/12 = delayed or difficult marriage. "
            "Saturn in 7th = late marriage or marriage to older/serious partner."
        ),
        confidence=0.87,
        verse="BPHS Ch.17 v.13-22",
        tags=["bhava", "7th_house", "marriage_timing", "jupiter_transit", "saturn_7th"],
        implemented=False,
    ),
    # --- Special Bhava Effects (BPH026-030) ---
    RuleRecord(
        rule_id="BPH026",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Empty houses (no planets): Vacant houses take their results from "
            "the sign lord's placement and condition. "
            "A vacant house with strong lord in Kendra/Trikona = house theme thrives. "
            "Vacant house with afflicted lord = house themes suffer. "
            "Aspects to a vacant house also modify results."
        ),
        confidence=0.88,
        verse="BPHS Ch.11 v.37-44",
        tags=["bhava", "vacant_house", "empty_house", "lord_placement", "aspect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH027",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Occupied vs. vacant house: The more planets in a house, the more active "
            "that house is in the native's life — but activity does not always mean success. "
            "Multiple malefics in a house = constant challenges in that area. "
            "Multiple benefics in a house = area of exceptional blessings. "
            "Single strong planet in house = focused, clear results for that house."
        ),
        confidence=0.86,
        verse="BPHS Ch.11 v.45-52",
        tags=["bhava", "occupied_house", "planet_count", "malefic_benefic_occupation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH028",
        source="Phala_Deepika",
        chapter="Ch.7",
        school="mantreswara",
        category="bhava",
        description=(
            "Bhava Chalita vs. Rashi chart: Bhava Chalita (house chart) uses equal "
            "house division from lagna degree; planets may fall in different houses "
            "than in Rashi chart. For precise house results, use Bhava chart. "
            "A planet in Rashi house X but Bhava house Y gives results of house Y."
        ),
        confidence=0.82,
        verse="PD Ch.7 v.29-36",
        tags=["bhava", "bhava_chalita", "equal_house", "rashi_vs_bhava", "house_division"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH029",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava",
        description=(
            "Lord of house in enemy's sign: When a house lord is in an enemy's sign, "
            "the significations of that house face obstacles and conflicts. "
            "House lord in great enemy's sign = severe challenges for that house's themes. "
            "Remedied by a benefic aspect on the house lord or benefic in the house itself."
        ),
        confidence=0.85,
        verse="BPHS Ch.11 v.53-60",
        tags=["bhava", "lord_enemy_sign", "house_obstruction", "benefic_remedy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BPH030",
        source="Uttara_Kalamrita",
        chapter="Ch.4",
        school="kalidasa",
        category="bhava",
        description=(
            "All 12 houses and their health correlations: "
            "1st=head; 2nd=face/neck; 3rd=chest/arms; 4th=heart; 5th=stomach; "
            "6th=intestines/waist; 7th=lower abdomen; 8th=genitals/anus; "
            "9th=hips/thighs; 10th=knees; 11th=calves/ankles; 12th=feet/left eye. "
            "Afflicted house/lord = health issues in corresponding body part."
        ),
        confidence=0.88,
        verse="UK Ch.4 v.17-28",
        tags=["bhava", "health_body_parts", "12_houses_anatomy", "afflicted_house_health"],
        implemented=False,
    ),
]

for rule in _BHAVA_PHALA_RULES:
    BHAVA_PHALA_RULES_REGISTRY.add(rule)
