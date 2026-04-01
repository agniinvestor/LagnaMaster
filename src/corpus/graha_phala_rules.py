"""
src/corpus/graha_phala_rules.py — Graha Phala (Planets in Houses) Rules (S250)

Encodes classical results of planets in all 12 houses — each planet's
effects when placed in specific houses from the Lagna. Covers all 7
visible planets (Sun through Saturn) with key house placements.

Sources:
  BPHS Ch.23-32 — Graha Phala Adhyaya
  Phala Deepika Ch.3 — Planets in Houses
  Brihat Jataka Ch.2 — Planet in House effects

30 rules total: GPH001-GPH030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

GRAHA_PHALA_RULES_REGISTRY = CorpusRegistry()

_GRAHA_PHALA_RULES = [
    # --- Sun in Houses (GPH001-004) ---
    RuleRecord(
        rule_id="GPH001",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_phala",
        description=(
            "Sun in Kendra houses (1st/4th/7th/10th): "
            "1st: bold, healthy, eye problems, father prominent. "
            "4th: domestic discord, real estate issues, mother suffers. "
            "7th: weak spouse, possible health issues for partner, foreign travel. "
            "10th: Digbala — career excellence, government authority, father influential. "
            "Sun in Kendra = powerful but can create ego challenges."
        ),
        confidence=0.88,
        verse="BPHS Ch.23 v.1-12",
        tags=["graha_phala", "sun_house", "kendra_1_4_7_10", "digbala_10th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH002",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_phala",
        description=(
            "Sun in Trikona and special houses: "
            "5th: government service, children challenges, intelligent. "
            "9th: father excellent, dharmic, lucky, possible father absence. "
            "11th: gains, fulfillment of wishes, authority over groups. "
            "Sun in Trikona (1/5/9) = overall auspicious results for career and dharma."
        ),
        confidence=0.87,
        verse="BPHS Ch.23 v.13-22",
        tags=["graha_phala", "sun_house", "trikona_5_9_11", "career_dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH003",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_phala",
        description=(
            "Sun in difficult houses: "
            "6th: defeats enemies, health challenges (pitta), maternal uncle issues. "
            "8th: short life tendency, eye problems, quarrels, hidden ailments. "
            "12th: expenses, eye weakness, separation from father, possible foreign stay. "
            "Sun in dusthana = challenges to vitality and authority."
        ),
        confidence=0.86,
        verse="BPHS Ch.23 v.23-32",
        tags=["graha_phala", "sun_house", "dusthana_6_8_12", "health_eye_problems"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH004",
        source="Phaladeepika",
        chapter="Ch.3",
        school="mantreswara",
        category="graha_phala",
        description=(
            "Sun in 2nd and 3rd houses: "
            "2nd: harsh speech, family discord, financial fluctuations, eye issues. "
            "3rd: courageous, strong younger siblings, short journeys, early fame. "
            "Sun in 2nd = Maraka influence affects speech/wealth. "
            "Sun in 3rd = vitality for effort and communication."
        ),
        confidence=0.86,
        verse="PD Ch.3 v.1-8",
        tags=["graha_phala", "sun_house", "2nd_3rd", "maraka_2nd", "courage_3rd"],
        implemented=False,
    ),
    # --- Moon in Houses (GPH005-008) ---
    RuleRecord(
        rule_id="GPH005",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="graha_phala",
        description=(
            "Moon in Kendra houses: "
            "1st: beautiful, popular, emotional, mother-loving. "
            "4th: Digbala — excellent for domestic happiness, property, mother. "
            "7th: attractive spouse, public life, emotional partnerships. "
            "10th: public career, fame, emotional approach to work. "
            "Full Moon in Kendra = most auspicious placement."
        ),
        confidence=0.88,
        verse="BPHS Ch.24 v.1-12",
        tags=["graha_phala", "moon_house", "kendra", "digbala_4th", "full_moon"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH006",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="graha_phala",
        description=(
            "Moon in Trikona: "
            "1st (also Kendra): self-confidence, emotional intelligence. "
            "5th: children, creative intelligence, emotional depth. "
            "9th: dharmic, fortune through mother or women. "
            "Moon in Trikona = strong emotional intelligence and motherly qualities. "
            "Waxing Moon in Trikona = especially beneficial for wealth and happiness."
        ),
        confidence=0.87,
        verse="BPHS Ch.24 v.13-20",
        tags=["graha_phala", "moon_house", "trikona", "waxing_moon", "emotional"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH007",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="graha_phala",
        description=(
            "Moon in difficult houses: "
            "6th: health challenges, digestive issues, maternal difficulties. "
            "8th: emotional turbulence, chronic ailments, interest in occult. "
            "12th: emotional losses, isolation, spiritual depth, foreign connections. "
            "Waning Moon in dusthana = more severe challenges. "
            "Benefic aspect on Moon in dusthana = mitigation."
        ),
        confidence=0.86,
        verse="BPHS Ch.24 v.21-30",
        tags=["graha_phala", "moon_house", "dusthana", "waning_moon", "emotional_challenges"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH008",
        source="Phaladeepika",
        chapter="Ch.3",
        school="mantreswara",
        category="graha_phala",
        description=(
            "Moon in 2nd, 3rd, 11th: "
            "2nd: good speech, wealth from mother/women, emotional about money. "
            "3rd: short journeys, emotional communication, inconsistent courage. "
            "11th: gains from women/public, fulfillment of emotional wishes, social network. "
            "Moon in Upachaya = emotional themes improve with age."
        ),
        confidence=0.85,
        verse="PD Ch.3 v.9-16",
        tags=["graha_phala", "moon_house", "2nd_3rd_11th", "upachaya_moon"],
        implemented=False,
    ),
    # --- Mars in Houses (GPH009-011) ---
    RuleRecord(
        rule_id="GPH009",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="graha_phala",
        description=(
            "Mars in houses — key placements: "
            "1st: aggressive, athletic, accident-prone, strong vitality. "
            "4th: Mangal Dosha for marriage, domestic conflicts, real estate disputes. "
            "7th: Mangal Dosha — marital conflicts, energetic but domineering spouse. "
            "10th: excellent for military/police/engineering; career through action. "
            "Mars in 1st/4th/7th = classical Mangal Dosha."
        ),
        confidence=0.88,
        verse="BPHS Ch.25 v.1-14",
        tags=["graha_phala", "mars_house", "mangal_dosha", "1_4_7", "aggressive"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH010",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="graha_phala",
        description=(
            "Mars in favorable houses: "
            "3rd: excellent courage, athletic, strong siblings. "
            "6th: defeats enemies, wins litigation, strong health resistance. "
            "11th: financial gains, persistent effort, social leadership. "
            "Mars in Upachaya (3/6/10/11) = its aggression becomes productive. "
            "Especially 3rd and 6th = most beneficial for Mars placement."
        ),
        confidence=0.88,
        verse="BPHS Ch.25 v.15-24",
        tags=["graha_phala", "mars_house", "3_6_11", "upachaya_mars", "courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH011",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="graha_phala",
        description=(
            "Mars in difficult houses: "
            "2nd: harsh speech, family conflicts, cuts/injuries near face. "
            "8th: accidents, surgeries, short life tendency if afflicted. "
            "12th: expenditure on surgery, foreign hospitals, violent losses. "
            "Mars in 2nd/8th/12th = significator of physical danger. "
            "Strong Mars aspects can mitigate these effects."
        ),
        confidence=0.86,
        verse="BPHS Ch.25 v.25-34",
        tags=["graha_phala", "mars_house", "2_8_12", "accidents_surgery", "danger"],
        implemented=False,
    ),
    # --- Mercury in Houses (GPH012-013) ---
    RuleRecord(
        rule_id="GPH012",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="graha_phala",
        description=(
            "Mercury in houses — favorable: "
            "1st: intelligent, youthful, communicative, dual nature. "
            "4th: educated, good real estate deals, intelligent mother. "
            "5th: brilliant intellect, writer, multiple talents. "
            "10th: business success, writing/media career, skilled communication. "
            "Mercury in Kendra/Trikona = intellectual excellence."
        ),
        confidence=0.87,
        verse="BPHS Ch.26 v.1-14",
        tags=["graha_phala", "mercury_house", "kendra_trikona", "intellect", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH013",
        source="Phaladeepika",
        chapter="Ch.3",
        school="mantreswara",
        category="graha_phala",
        description=(
            "Mercury in challenging houses: "
            "6th: health through nerves/skin, debates enemies. "
            "8th: research, occult interest, inheritance through documents. "
            "12th: secretive, foreign language expertise, loss through communication. "
            "Mercury in dusthana = intellectual energies turned inward or toward research."
        ),
        confidence=0.84,
        verse="PD Ch.3 v.17-24",
        tags=["graha_phala", "mercury_house", "dusthana", "research_occult", "secretive"],
        implemented=False,
    ),
    # --- Jupiter in Houses (GPH014-016) ---
    RuleRecord(
        rule_id="GPH014",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="graha_phala",
        description=(
            "Jupiter in houses — excellent placements: "
            "1st: wise, religious, generous, long-lived, respected. "
            "5th: brilliant children, creativity, spiritual intelligence. "
            "9th: deeply religious/philosophical, fortunate father, guru blessings. "
            "11th: abundant income, many helpful friends, fulfilled aspirations. "
            "Jupiter in Trikona = overall excellent for wisdom, prosperity, and dharma."
        ),
        confidence=0.90,
        verse="BPHS Ch.27 v.1-14",
        tags=["graha_phala", "jupiter_house", "trikona_excellent", "wisdom_prosperity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH015",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="graha_phala",
        description=(
            "Jupiter in Kendra houses: "
            "4th: happy home, excellent mother, property, vehicles. "
            "7th: wise and noble spouse, successful partnerships. "
            "10th: prestigious career, respected profession, fame. "
            "Jupiter in Kendra = Hamsa Yoga condition; amplifies Kendra themes positively."
        ),
        confidence=0.88,
        verse="BPHS Ch.27 v.15-22",
        tags=["graha_phala", "jupiter_house", "kendra", "hamsa_yoga", "noble"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH016",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="graha_phala",
        description=(
            "Jupiter in difficult houses: "
            "6th: legal challenges, weight issues, enemies through religion/philosophy. "
            "8th: occult wisdom, inheritance, interest in death/transformation. "
            "12th: spiritually inclined, ashram life, loss through generosity. "
            "Jupiter in dusthana still gives wisdom and faith; results just delayed/internalized."
        ),
        confidence=0.85,
        verse="BPHS Ch.27 v.23-32",
        tags=["graha_phala", "jupiter_house", "dusthana", "spiritual_inclined"],
        implemented=False,
    ),
    # --- Venus in Houses (GPH017-019) ---
    RuleRecord(
        rule_id="GPH017",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="graha_phala",
        description=(
            "Venus in houses — favorable: "
            "1st: beautiful, charming, artistic, luxury-loving, popular with opposite sex. "
            "4th: happy home, vehicles, property, beautiful mother. "
            "5th: creative, romantic, artistic children. "
            "7th: beautiful spouse, happy marriage, artistic partnership. "
            "Venus in Kendra/Trikona = Malavya Yoga possibility, excellent happiness."
        ),
        confidence=0.88,
        verse="BPHS Ch.28 v.1-14",
        tags=["graha_phala", "venus_house", "kendra_trikona", "beauty_happiness", "malavya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH018",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="graha_phala",
        description=(
            "Venus in challenging houses: "
            "6th: health through reproductive system; wins over enemies through charm. "
            "8th: inheritance from spouse, sensual occult, interest in Tantra. "
            "12th: bedroom pleasures, spiritual arts, foreign luxury experiences. "
            "Venus in dusthana = pleasures intensified but come with costs."
        ),
        confidence=0.84,
        verse="BPHS Ch.28 v.15-24",
        tags=["graha_phala", "venus_house", "dusthana", "pleasures_costs", "tantra_12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH019",
        source="Phaladeepika",
        chapter="Ch.3",
        school="mantreswara",
        category="graha_phala",
        description=(
            "Venus in 2nd, 3rd, 9th, 10th, 11th: "
            "2nd: eloquent, attractive voice, wealth through arts/women. "
            "3rd: artistic communication, charming siblings. "
            "9th: fortune through arts, spiritual aesthetics, attractive guru. "
            "10th: arts/entertainment career, attractive workplace. "
            "11th: gains from arts/women, beautiful social connections."
        ),
        confidence=0.85,
        verse="PD Ch.3 v.25-36",
        tags=["graha_phala", "venus_house", "2_3_9_10_11", "arts_wealth"],
        implemented=False,
    ),
    # --- Saturn in Houses (GPH020-022) ---
    RuleRecord(
        rule_id="GPH020",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="graha_phala",
        description=(
            "Saturn in houses — challenging but necessary: "
            "1st: thin/dark, disciplined, slow-starter, longevity. "
            "4th: mother suffers, property challenges, domestic distance. "
            "7th: late marriage, older/serious spouse, detachment in relationships. "
            "10th: persistent career, delayed success, authority through long effort. "
            "Saturn in Kendra = life built on hard work and persistence."
        ),
        confidence=0.87,
        verse="BPHS Ch.29 v.1-14",
        tags=["graha_phala", "saturn_house", "kendra", "discipline_delay", "longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH021",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="graha_phala",
        description=(
            "Saturn in favorable houses (Upachaya): "
            "3rd: persistent effort and courage; gains through systematic work. "
            "6th: excellent for defeating enemies; service sector success. "
            "11th: slow but steady income accumulation; long-term financial gains. "
            "Saturn in Upachaya = the best placements; delays are followed by lasting gains."
        ),
        confidence=0.88,
        verse="BPHS Ch.29 v.15-22",
        tags=["graha_phala", "saturn_house", "upachaya_3_6_11", "steady_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH022",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="graha_phala",
        description=(
            "Saturn in difficult houses: "
            "2nd: harsh speech, family hardship, delayed wealth accumulation. "
            "5th: children delayed or limited; intellect serious and disciplined. "
            "8th: Shasha Yoga possible, longevity, chronic illness, occult knowledge. "
            "12th: spiritual isolation, hospital/prison themes, good for liberation. "
            "Saturn in 5th and 8th = most karmic placements."
        ),
        confidence=0.86,
        verse="BPHS Ch.29 v.23-34",
        tags=["graha_phala", "saturn_house", "difficult_2_5_8_12", "karmic", "longevity"],
        implemented=False,
    ),
    # --- Rahu and Ketu in Houses (GPH023-026) ---
    RuleRecord(
        rule_id="GPH023",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="graha_phala",
        description=(
            "Rahu in houses — key effects: "
            "1st: unconventional, foreign influence, ambitious, health issues. "
            "4th: domestic instability, unusual home, possible foreign residence. "
            "7th: unusual marriage, foreign spouse possible, relationship complexity. "
            "10th: fame through unconventional career, public prominence, foreign recognition. "
            "Rahu in Kendra = worldly ambition amplified."
        ),
        confidence=0.85,
        verse="BPHS Ch.30 v.1-14",
        tags=["graha_phala", "rahu_house", "kendra", "foreign_unconventional", "ambitious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH024",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="graha_phala",
        description=(
            "Rahu in Trikona and Upachaya: "
            "5th: unconventional intellect, step-children, speculative gains. "
            "9th: unconventional dharma, foreign gurus, exotic philosophy. "
            "3rd: extraordinary courage, media connections, technology. "
            "6th: victory over enemies through cunning, foreign health care. "
            "11th: material gains through foreign/technology channels."
        ),
        confidence=0.83,
        verse="BPHS Ch.30 v.15-26",
        tags=["graha_phala", "rahu_house", "trikona_upachaya", "unconventional_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH025",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="graha_phala",
        description=(
            "Ketu in houses — key effects: "
            "1st: spiritual, mystical, sharp intuition, medical issues. "
            "4th: detachment from home, mother challenges, ancestral karma. "
            "7th: unusual marriage or renunciation of marriage, spiritualized partnerships. "
            "10th: unusual career, spiritual leadership possible, career detachment. "
            "Ketu in Kendra = past-life karma playing out in this area."
        ),
        confidence=0.83,
        verse="BPHS Ch.31 v.1-14",
        tags=["graha_phala", "ketu_house", "kendra", "spiritual_past_karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH026",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="graha_phala",
        description=(
            "Ketu in favorable positions: "
            "3rd: courage, mystical writing, spiritual siblings. "
            "5th: spiritual intelligence, meditation, past-life wisdom. "
            "9th: strong moksha inclination, spiritual philosophy, liberation-seeking guru. "
            "12th: moksha (liberation), ashram life, spiritual practices bring results. "
            "Ketu in 12th = most powerful for moksha."
        ),
        confidence=0.83,
        verse="BPHS Ch.31 v.15-26",
        tags=["graha_phala", "ketu_house", "spiritual_favorable", "moksha_12th"],
        implemented=False,
    ),
    # --- Combined House Effects (GPH027-030) ---
    RuleRecord(
        rule_id="GPH027",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="graha_phala",
        description=(
            "Combust planets in houses: A planet within 8° of Sun is combust (Asta). "
            "Combust planet loses significations of its house. "
            "Combust Venus = marriage challenges. Combust Mercury = intellectual loss. "
            "Exception: Moon cannot be combust in the traditional sense. "
            "Strength restores when planet emerges from combustion."
        ),
        confidence=0.86,
        verse="BJ Ch.2 v.1-8",
        tags=["graha_phala", "combust", "asta", "planet_sun_8_degrees", "signification_loss"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH028",
        source="BPHS",
        chapter="Ch.23",
        school="parashari",
        category="graha_phala",
        description=(
            "Exalted planet in dusthana: An exalted planet in 6th/8th/12th creates "
            "Viparita-like effects — the planet's strength actually mitigates the dusthana. "
            "Exalted Jupiter in 6th = powerful defeat of enemies despite initial challenges. "
            "Exalted Saturn in 8th = extraordinary longevity and occult mastery. "
            "The house is activated but the planet's strength protects its own significations."
        ),
        confidence=0.84,
        verse="BPHS Ch.23 v.33-40",
        tags=["graha_phala", "exalted_dusthana", "viparita_effect", "strength_mitigates"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH029",
        source="Phaladeepika",
        chapter="Ch.3",
        school="mantreswara",
        category="graha_phala",
        description=(
            "Debilitated planet in Kendra: A debilitated planet in Kendra = "
            "weakness in that house's themes despite the powerful house position. "
            "Debilitated Moon in 4th = emotional insecurity, difficult mother relationship. "
            "Debilitated Venus in 7th = dissatisfaction in marriage. "
            "Neecha Bhanga (debilitation cancellation) restores some strength."
        ),
        confidence=0.84,
        verse="PD Ch.3 v.37-44",
        tags=["graha_phala", "debilitated_kendra", "weakness_kendra", "neecha_bhanga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GPH030",
        source="Brihat Jataka",
        chapter="Ch.2",
        school="varahamihira",
        category="graha_phala",
        description=(
            "Planet in own sign in any house (Swakshetra): A planet in its own sign "
            "in any house = maximum expression of that house's themes. "
            "Mars in Aries in 1st = maximum courage and vitality. "
            "Jupiter in Sagittarius in 5th = extraordinary wisdom and progeny. "
            "Venus in Libra in 7th = ideal marriage. Saturn in Capricorn in 10th = peak career."
        ),
        confidence=0.88,
        verse="BJ Ch.2 v.9-16",
        tags=["graha_phala", "swakshetra", "own_sign_house", "maximum_expression"],
        implemented=False,
    ),
]

for rule in _GRAHA_PHALA_RULES:
    GRAHA_PHALA_RULES_REGISTRY.add(rule)
