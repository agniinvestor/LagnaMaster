"""
src/corpus/bphs_graha_bhava_complete.py — BPHS Graha-in-Bhava Complete (S251)

Exhaustive encoding of every planet-in-house combination from BPHS Ch.23–32.
One rule per planet per house = 9 planets × 12 houses = 108 rules.
Each rule captures the primary BPHS effects for that exact combination.

Source: BPHS Ch.23 (Sun), Ch.24 (Moon), Ch.25 (Mars), Ch.26 (Mercury),
        Ch.27 (Jupiter), Ch.28 (Venus), Ch.29 (Saturn),
        Ch.30 (Rahu), Ch.31 (Ketu)

108 rules total: GBC001–GBC108.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY = CorpusRegistry()

_RULES = [
    # ── SUN in Houses 1–12 (GBC001–012) ─────────────────────────────────────
    RuleRecord(
        rule_id="GBC001", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 1st house: Bold, commanding personality, strong constitution, "
            "reddish or dark complexion, self-reliant, leadership qualities. "
            "Tendency toward eye ailments and pitta disorders. Father prominent or authoritative. "
            "Native rises through personal initiative.",
        confidence=0.90, verse="BPHS Ch.23 v.1-4",
        tags=["graha_bhava", "sun_1st", "bold", "leadership", "eye_pitta"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC002", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 2nd house: Harsh or authoritative speech; dental and eye issues. "
            "Family relations strained by ego conflicts. Fluctuating wealth — gains from "
            "government or authority but also expenditure. Father may be source of family "
            "tension. Maraka significance (2nd house Maraka).",
        confidence=0.88, verse="BPHS Ch.23 v.5-8",
        tags=["graha_bhava", "sun_2nd", "harsh_speech", "family_tension", "maraka", "dental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC003", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 3rd house: Courageous, strong-willed, gains through self-effort "
            "and communication. Younger siblings may be few or subordinate to native. "
            "Short journeys, writing and media activities benefit. Ears and shoulders "
            "may be prone to issues. Leadership in early career.",
        confidence=0.88, verse="BPHS Ch.23 v.9-12",
        tags=["graha_bhava", "sun_3rd", "courageous", "self_effort", "siblings", "media"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC004", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 4th house: Domestic unhappiness; mother's health may suffer or "
            "relationship with mother is strained. Real estate dealings are problematic. "
            "Heart and chest issues possible. Native finds it hard to settle; "
            "frequent changes of residence. Property matters involve conflict.",
        confidence=0.87, verse="BPHS Ch.23 v.13-16",
        tags=["graha_bhava", "sun_4th", "domestic_unhappiness", "mother_health", "property_conflict"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC005", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 5th house: Intelligent, philosophical bent, interest in government "
            "or politics. Children may be few or delayed; some texts indicate son after "
            "difficulty. Stomach and digestive ailments. Speculation losses possible. "
            "Authority through intellectual merit.",
        confidence=0.87, verse="BPHS Ch.23 v.17-20",
        tags=["graha_bhava", "sun_5th", "intelligence", "few_children", "stomach", "speculation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC006", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 6th house: Defeats enemies effectively; competitive in disputes. "
            "Maternal uncle may be distant or adversarial. Bilious constitution, "
            "tendency toward inflammation and fevers. Good for government service, "
            "military, law enforcement. Upachaya placement — improves over time.",
        confidence=0.88, verse="BPHS Ch.23 v.21-24",
        tags=["graha_bhava", "sun_6th", "defeats_enemies", "bilious", "government_service", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC007", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 7th house: Spouse may be sickly, egoistic, or challenging to "
            "live with. Delays or difficulties in marriage. Partnership conflicts due to "
            "ego assertion. Native may spend time abroad. Maraka for 7th lord significations. "
            "Strong business acumen in foreign markets.",
        confidence=0.87, verse="BPHS Ch.23 v.25-28",
        tags=["graha_bhava", "sun_7th", "spouse_sickly", "marriage_delays", "foreign", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC008", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 8th house: Short life tendency or chronic ailments; eye weakness "
            "prominent. Father's longevity affected. Obstacles and hidden enemies. "
            "Interest in occult and research. Government-related obstacles. "
            "Can indicate inheritance issues or father's property disputes.",
        confidence=0.86, verse="BPHS Ch.23 v.29-32",
        tags=["graha_bhava", "sun_8th", "short_life", "eye_weakness", "father_longevity", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC009", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 9th house: Highly dharmic, religious, and righteous. Father is "
            "respected, authoritative, or government-connected. Good luck in legal matters "
            "and higher education. Pilgrimage and long journeys. Fortune improves with age. "
            "Favored by authority figures and rulers.",
        confidence=0.90, verse="BPHS Ch.23 v.33-36",
        tags=["graha_bhava", "sun_9th", "dharmic", "father_respected", "luck", "pilgrimage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC010", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 10th house: Digbala (full directional strength). Career excellence, "
            "government authority, fame. Father is prominent or in public life. "
            "Success in administration, politics, medicine, law. One of the most powerful "
            "placements for career. Recognition from rulers.",
        confidence=0.93, verse="BPHS Ch.23 v.37-40",
        tags=["graha_bhava", "sun_10th", "digbala", "career_excellence", "government", "fame"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC011", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 11th house: Good income from government or authority-related work. "
            "Wishes fulfilled, especially career ambitions. Elder siblings may be few but "
            "influential. Gains through father's connections. Good for social status and "
            "leadership of groups.",
        confidence=0.88, verse="BPHS Ch.23 v.41-44",
        tags=["graha_bhava", "sun_11th", "income", "fulfilled_wishes", "elder_siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC012", source="BPHS", chapter="Ch.23", school="parashari",
        category="graha_bhava",
        description="Sun in 12th house: Expenditure and losses; eye weakness especially left eye. "
            "Father absent, distant, or early death of father. Isolation or foreign sojourn. "
            "Government-related expenses. Spiritual inclination grows in later life. "
            "Secret enemies from authority.",
        confidence=0.87, verse="BPHS Ch.23 v.45-48",
        tags=["graha_bhava", "sun_12th", "expenditure", "eye_weakness", "father_absent", "foreign"],
        implemented=False,
    ),
    # ── MOON in Houses 1–12 (GBC013–024) ────────────────────────────────────
    RuleRecord(
        rule_id="GBC013", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 1st house: Emotionally expressive, beautiful appearance, "
            "attractive eyes, popular especially with women. Mother prominent. "
            "Changeable moods and temperament. Psychic sensitivity. "
            "Waxing Moon here = very auspicious; waning Moon = more emotional turbulence.",
        confidence=0.90, verse="BPHS Ch.24 v.1-4",
        tags=["graha_bhava", "moon_1st", "beautiful", "emotional", "popular", "psychic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC014", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 2nd house: Sweet, persuasive speech; wealth comes and goes "
            "with emotional tides. Family emotionally close. Good food and hospitality. "
            "Income from nurturing professions, women, or public sector. "
            "Beautiful face. Maraka significance for longevity.",
        confidence=0.88, verse="BPHS Ch.24 v.5-8",
        tags=["graha_bhava", "moon_2nd", "sweet_speech", "fluctuating_wealth", "family_close", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC015", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 3rd house: Restless, fond of short journeys and travel. "
            "Emotional communication style; writing influenced by feelings. "
            "Siblings (especially sisters) emotionally close. Inconsistent courage — "
            "brave when emotionally motivated. Left ear sensitive.",
        confidence=0.87, verse="BPHS Ch.24 v.9-12",
        tags=["graha_bhava", "moon_3rd", "restless", "short_journeys", "emotional_communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC016", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 4th house: Digbala — exceptional domestic happiness, beautiful "
            "home, loving mother. Property and vehicles acquired. Emotionally secure. "
            "Close bond with mother throughout life. Best placement for Moon. "
            "Full Moon in 4th = outstanding fortune in domestic matters.",
        confidence=0.93, verse="BPHS Ch.24 v.13-16",
        tags=["graha_bhava", "moon_4th", "digbala", "domestic_happiness", "mother_excellent", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC017", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 5th house: Emotionally creative, intuitive intellect, "
            "good memory. Children are emotionally connected to native. "
            "Romance and emotional investment in creative projects. "
            "Speculative tendencies driven by emotion. Good for education and arts.",
        confidence=0.88, verse="BPHS Ch.24 v.17-20",
        tags=["graha_bhava", "moon_5th", "intuitive", "good_memory", "children_bond", "creative"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC018", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 6th house: Digestive and stomach ailments; emotional eating. "
            "Mother's health may suffer. Enemies through emotional manipulation. "
            "Waning Moon here especially difficult. Service-oriented emotional nature. "
            "Maternal relatives may cause emotional trouble.",
        confidence=0.86, verse="BPHS Ch.24 v.21-24",
        tags=["graha_bhava", "moon_6th", "digestive_issues", "mother_health", "emotional_enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC019", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 7th house: Attractive, charming spouse; public-oriented marriage. "
            "Emotional investment in partnerships. Business with women or public. "
            "Multiple emotional connections possible. Marriage partner is nurturing. "
            "Public life strong; success in dealing with masses.",
        confidence=0.88, verse="BPHS Ch.24 v.25-28",
        tags=["graha_bhava", "moon_7th", "attractive_spouse", "public_life", "emotional_partnership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC020", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 8th house: Emotional turbulence; chronic ailments especially "
            "digestive or lymphatic. Mother's longevity affected. Interest in occult "
            "and mysteries. Inheritance through mother or maternal line. "
            "Waning Moon in 8th = particularly challenging for health.",
        confidence=0.85, verse="BPHS Ch.24 v.29-32",
        tags=["graha_bhava", "moon_8th", "emotional_turbulence", "chronic_ailments", "occult", "inheritance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC021", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 9th house: Fortune through mother, women, or public. "
            "Emotional approach to dharma and philosophy. Pilgrimage and foreign "
            "journeys emotionally motivated. Mother is spiritual or religious. "
            "Good luck comes through emotional generosity and intuitive decisions.",
        confidence=0.88, verse="BPHS Ch.24 v.33-36",
        tags=["graha_bhava", "moon_9th", "fortune_mother", "spiritual_mother", "pilgrimage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC022", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 10th house: Public career; fame through nurturing, "
            "emotional connection with masses. Mother involved in or influences career. "
            "Professions involving public, women, food, travel, or healing. "
            "Career fluctuates with lunar phases. Political and public success.",
        confidence=0.88, verse="BPHS Ch.24 v.37-40",
        tags=["graha_bhava", "moon_10th", "public_career", "fame", "mother_career", "masses"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC023", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 11th house: Gains from women, public sector, or emotional "
            "networks. Fulfilled emotional aspirations. Elder siblings emotionally supportive. "
            "Social popularity brings income. Left-ear related gains. "
            "Full Moon in 11th = excellent for manifesting desires.",
        confidence=0.88, verse="BPHS Ch.24 v.41-44",
        tags=["graha_bhava", "moon_11th", "gains_women", "aspirations_fulfilled", "social_income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC024", source="BPHS", chapter="Ch.24", school="parashari",
        category="graha_bhava",
        description="Moon in 12th house: Emotional losses; tendency to isolate. "
            "Spiritual depth and meditation. Sleep disturbances. Foreign connections "
            "through mother or women. Expenditure on nurturing others. "
            "Good for ashram or institutional life. Waning Moon here = difficult.",
        confidence=0.86, verse="BPHS Ch.24 v.45-48",
        tags=["graha_bhava", "moon_12th", "emotional_losses", "spiritual", "foreign", "sleep"],
        implemented=False,
    ),
    # ── MARS in Houses 1–12 (GBC025–036) ─────────────────────────────────────
    RuleRecord(
        rule_id="GBC025", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 1st house: Aggressive, athletic, impulsive, quick-tempered. "
            "Reddish complexion, muscular build, mechanical or surgical aptitude. "
            "Accident-prone (head injuries). Strong vitality but prone to fevers "
            "and inflammatory conditions. Courageous and pioneering.",
        confidence=0.90, verse="BPHS Ch.25 v.1-4",
        tags=["graha_bhava", "mars_1st", "aggressive", "athletic", "accident_prone", "vitality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC026", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 2nd house: Harsh, cutting speech; family conflicts and disputes. "
            "Dental injuries or facial scars. Fluctuating finances with aggressive "
            "earning style. Harsh towards family. Food-related injuries possible. "
            "Maraka significance — 2nd house Mars is a maraka significator.",
        confidence=0.87, verse="BPHS Ch.25 v.5-8",
        tags=["graha_bhava", "mars_2nd", "harsh_speech", "family_conflicts", "dental", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC027", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 3rd house: One of Mars' best placements. Exceptional courage, "
            "athletic ability, strong younger siblings. Victories in competitions, "
            "sports, debate. Short journeys for adventure. Writing on action, "
            "military, or technical topics. Gains through self-effort.",
        confidence=0.92, verse="BPHS Ch.25 v.9-12",
        tags=["graha_bhava", "mars_3rd", "exceptional_courage", "athletic", "competitive_wins", "best_placement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC028", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 4th house: Mangal Dosha — domestic conflicts, property disputes, "
            "accidents in home. Mother's health affected. Vehicles involved in accidents. "
            "Real estate gains through conflict or demolition/construction. "
            "Emotional anger in domestic settings. Agricultural or land work.",
        confidence=0.88, verse="BPHS Ch.25 v.13-16",
        tags=["graha_bhava", "mars_4th", "mangal_dosha", "domestic_conflicts", "mother_health", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC029", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 5th house: Few or delayed children; possible miscarriages "
            "or surgical interventions for progeny. Passionate but rash intellect. "
            "Speculative losses through aggression. Stomach issues. "
            "Strong competitive intelligence; good for sports or martial arts.",
        confidence=0.86, verse="BPHS Ch.25 v.17-20",
        tags=["graha_bhava", "mars_5th", "few_children", "rash_intellect", "speculative_loss"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC030", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 6th house: Excellent placement — destroys enemies, wins all "
            "competitions, overcomes disease through physical strength. Victory in "
            "litigation and disputes. Military, police, or surgical career thrives. "
            "Upachaya placement — aggression becomes productive force.",
        confidence=0.92, verse="BPHS Ch.25 v.21-24",
        tags=["graha_bhava", "mars_6th", "destroys_enemies", "competitive_wins", "military", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC031", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 7th house: Mangal Dosha — marital conflicts, domineering or "
            "aggressive spouse, possible separation. Spouse may be athletic or military. "
            "Partnerships energetic but contentious. Foreign business ventures. "
            "Maraka significance for 7th house. Early marriage can create conflicts.",
        confidence=0.88, verse="BPHS Ch.25 v.25-28",
        tags=["graha_bhava", "mars_7th", "mangal_dosha", "marital_conflicts", "domineering_spouse", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC032", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 8th house: Accident proneness, surgical interventions, short-life "
            "tendency if afflicted. Blood disorders, injuries. Hidden aggression. "
            "Can give occult power and transformation through crisis. "
            "Ancestral property disputes. Inheritance through conflict.",
        confidence=0.86, verse="BPHS Ch.25 v.29-32",
        tags=["graha_bhava", "mars_8th", "accidents", "surgery", "blood_disorders", "occult_power"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC033", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 9th house: Argumentative about religion and dharma; conflicts "
            "with father or guru. Pilgrimage through adventurous journeys. "
            "Legal battles related to dharma or property. Some texts indicate "
            "gains from father's property after conflict.",
        confidence=0.85, verse="BPHS Ch.25 v.33-36",
        tags=["graha_bhava", "mars_9th", "religious_arguments", "father_conflicts", "legal_dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC034", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 10th house: Excellent career through action, engineering, "
            "military, surgery, sports, law enforcement. Digbala in traditional sense "
            "for action. Fast career advancement through boldness. "
            "Father may be in a powerful action-oriented role. Fame through courage.",
        confidence=0.90, verse="BPHS Ch.25 v.37-40",
        tags=["graha_bhava", "mars_10th", "career_action", "military_engineering", "fame_courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC035", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 11th house: Persistent financial gains; competitive income. "
            "Elder siblings may be few but strong. Social leadership through courage. "
            "Income from engineering, military, sports, or competitive fields. "
            "Upachaya — aggression produces long-term gains.",
        confidence=0.88, verse="BPHS Ch.25 v.41-44",
        tags=["graha_bhava", "mars_11th", "financial_gains", "competitive_income", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC036", source="BPHS", chapter="Ch.25", school="parashari",
        category="graha_bhava",
        description="Mars in 12th house: Expenditure through accidents, surgery, or violence. "
            "Foreign conflicts or enemies. Losses through aggression. "
            "Possible imprisonment or military service abroad. "
            "Occult power through martial arts or fire rituals. Sleep disturbed.",
        confidence=0.85, verse="BPHS Ch.25 v.45-48",
        tags=["graha_bhava", "mars_12th", "expenditure_surgery", "foreign_conflict", "imprisonment"],
        implemented=False,
    ),
    # ── MERCURY in Houses 1–12 (GBC037–048) ──────────────────────────────────
    RuleRecord(
        rule_id="GBC037", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 1st house: Intelligent, youthful appearance lasting into "
            "old age, eloquent, communicative, dual-natured. Quick thinking, versatile "
            "interests. Skilled in multiple fields simultaneously. "
            "Nervous system sensitive. Excellent for writing, teaching, trading.",
        confidence=0.90, verse="BPHS Ch.26 v.1-4",
        tags=["graha_bhava", "mercury_1st", "intelligent", "youthful", "eloquent", "versatile"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC038", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 2nd house: Eloquent, persuasive speech; wealth through "
            "writing, trading, or communication. Family values education. "
            "Good with numbers and accounts. Witty and humorous in speech. "
            "Income from intellectual work, commerce, or journalism.",
        confidence=0.88, verse="BPHS Ch.26 v.5-8",
        tags=["graha_bhava", "mercury_2nd", "eloquent_speech", "wealth_communication", "accounts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC039", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 3rd house: Excellent communicator, writer, journalist. "
            "Intellectually clever siblings. Short journeys for learning and business. "
            "Skilled in languages. Technical writing, media, or publishing. "
            "Curious and information-hungry in all communications.",
        confidence=0.88, verse="BPHS Ch.26 v.9-12",
        tags=["graha_bhava", "mercury_3rd", "writer_journalist", "languages", "publishing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC040", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 4th house: Well-educated, intelligent mother. Good real "
            "estate negotiations. Home filled with books and learning. "
            "Comfortable domestic life through intellectual means. "
            "Multiple vehicles or property dealings through negotiations.",
        confidence=0.87, verse="BPHS Ch.26 v.13-16",
        tags=["graha_bhava", "mercury_4th", "educated_mother", "real_estate", "learning_home"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC041", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 5th house: Brilliant scholar, writer, intellectual. "
            "Children are intelligent and academically gifted. Speculative gains "
            "through analysis. Skill in multiple creative-intellectual fields. "
            "Excellent for teachers, analysts, authors.",
        confidence=0.90, verse="BPHS Ch.26 v.17-20",
        tags=["graha_bhava", "mercury_5th", "scholar", "intelligent_children", "analytical"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC042", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 6th house: Defeats enemies through wit and strategy. "
            "Skilled debater in legal matters. Skin disorders and nervous system "
            "ailments. Maternal aunt/uncle may be intellectually prominent. "
            "Service in communications, accounting, or analysis.",
        confidence=0.86, verse="BPHS Ch.26 v.21-24",
        tags=["graha_bhava", "mercury_6th", "defeats_through_wit", "legal_skill", "skin_nervous"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC043", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 7th house: Intelligent, communicative spouse. "
            "Partnerships thrive through negotiation and communication. "
            "Business with trading, communications, or intellectual work. "
            "Spouse may be younger or youthful in appearance. Maraka significance.",
        confidence=0.87, verse="BPHS Ch.26 v.25-28",
        tags=["graha_bhava", "mercury_7th", "intelligent_spouse", "communication_partnership", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC044", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 8th house: Research aptitude, occult intellect, mastery "
            "of secret knowledge. Inheritance through written documents. "
            "Skin disorders, nervous system issues. Long life if unafflicted. "
            "Skill in analysis of hidden matters, investigation.",
        confidence=0.85, verse="BPHS Ch.26 v.29-32",
        tags=["graha_bhava", "mercury_8th", "research_occult", "inheritance_documents", "nervous_system"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC045", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 9th house: Philosophical, scholarly, skilled in law "
            "and foreign languages. Religious intellectual. Father may be in "
            "intellectual or teaching profession. Good fortune through education "
            "and communication. Pilgrimage with learning purpose.",
        confidence=0.87, verse="BPHS Ch.26 v.33-36",
        tags=["graha_bhava", "mercury_9th", "philosophical", "law_languages", "father_teacher"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC046", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 10th house: Career through communication, business, "
            "writing, media, analytics, accounting, or technology. "
            "Excellent in trade and commerce. Multiple career activities simultaneously. "
            "Reputation built through intellectual achievements.",
        confidence=0.88, verse="BPHS Ch.26 v.37-40",
        tags=["graha_bhava", "mercury_10th", "career_communication", "business_media", "multi_career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC047", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 11th house: Multiple income streams through intellect "
            "and communication. Elder siblings intellectually supportive. "
            "Gains from writing, trading, and technology. Social network of "
            "intelligent friends. Wishes fulfilled through clever strategies.",
        confidence=0.87, verse="BPHS Ch.26 v.41-44",
        tags=["graha_bhava", "mercury_11th", "multiple_income", "intelligent_network", "gains_intellect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC048", source="BPHS", chapter="Ch.26", school="parashari",
        category="graha_bhava",
        description="Mercury in 12th house: Foreign language expertise, secretive communication. "
            "Spiritual intellect; interest in meditation and inner knowledge. "
            "Losses through miscommunication or contracts. Hidden intellectual "
            "abilities. Research into spiritual or esoteric subjects.",
        confidence=0.85, verse="BPHS Ch.26 v.45-48",
        tags=["graha_bhava", "mercury_12th", "foreign_language", "secretive", "spiritual_intellect"],
        implemented=False,
    ),
    # ── JUPITER in Houses 1–12 (GBC049–060) ──────────────────────────────────
    RuleRecord(
        rule_id="GBC049", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 1st house: Wise, generous, religious, long-lived. "
            "Large or well-proportioned body. Respected in community. "
            "Strong dharmic sense. Wealth through wisdom. Good health overall. "
            "Natural teacher or guide. Blessings from gurus.",
        confidence=0.92, verse="BPHS Ch.27 v.1-4",
        tags=["graha_bhava", "jupiter_1st", "wise_generous", "religious", "long_lived", "respected"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC050", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 2nd house: Eloquent, learned speech; family values wisdom "
            "and education. Good food and generous hospitality. Wealth accumulates. "
            "Multiple family members scholarly or spiritual. Face is attractive. "
            "Income from teaching, consulting, or religious work.",
        confidence=0.90, verse="BPHS Ch.27 v.5-8",
        tags=["graha_bhava", "jupiter_2nd", "eloquent_speech", "wealth_accumulation", "family_wisdom"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC051", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 3rd house: Preaches wisdom; writes on dharma or philosophy. "
            "Religious siblings. Short journeys for learning and pilgrimage. "
            "Courage expressed through wisdom rather than force. "
            "Ear for higher knowledge. Some texts note reduced bravery.",
        confidence=0.86, verse="BPHS Ch.27 v.9-12",
        tags=["graha_bhava", "jupiter_3rd", "dharmic_writing", "religious_siblings", "wisdom_courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC052", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 4th house: Domestic wisdom and happiness; beautiful, "
            "well-maintained home filled with books and spiritual items. "
            "Mother is spiritual or learned. Property gains. Comfortable vehicles. "
            "Higher education supported by family.",
        confidence=0.90, verse="BPHS Ch.27 v.13-16",
        tags=["graha_bhava", "jupiter_4th", "domestic_wisdom", "spiritual_home", "mother_learned"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC053", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 5th house: Excellent — brilliant children, intelligent "
            "progeny who become scholars or leaders. Creative intelligence and wisdom. "
            "Strong Purva Punya (past-life merit). Spiritual practices are fruitful. "
            "Excellent for teachers, scholars, and creative intellectuals.",
        confidence=0.93, verse="BPHS Ch.27 v.17-20",
        tags=["graha_bhava", "jupiter_5th", "excellent", "brilliant_children", "purva_punya", "wisdom"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC054", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 6th house: Legal challenges and disputes with religious/educational "
            "institutions. Weight and liver issues. Over-generous to enemies. "
            "Enemies may be scholars or from respectable backgrounds. "
            "Service in education or healthcare. Some gains after initial obstacles.",
        confidence=0.84, verse="BPHS Ch.27 v.21-24",
        tags=["graha_bhava", "jupiter_6th", "legal_challenges", "weight_liver", "over_generous"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC055", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 7th house: Wise, noble, and respectable spouse. "
            "Dharmic marriage and partnerships. Spouse brings wisdom and fortune. "
            "Business partnerships with ethical, educated persons. "
            "Maraka significance but Jupiter mitigates its own Maraka effects here.",
        confidence=0.90, verse="BPHS Ch.27 v.25-28",
        tags=["graha_bhava", "jupiter_7th", "wise_spouse", "dharmic_marriage", "ethical_partnerships"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC056", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 8th house: Wisdom about death, occult, and mysteries. "
            "Long life (Jupiter protects 8th house longevity). Inheritance of knowledge "
            "and property. Interest in Jyotish, tantra, and esoteric sciences. "
            "Hidden wealth. Transformation through philosophical understanding.",
        confidence=0.87, verse="BPHS Ch.27 v.29-32",
        tags=["graha_bhava", "jupiter_8th", "occult_wisdom", "long_life", "inheritance", "tantra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC057", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 9th house: Exceptionally religious, philosophical, fortunate. "
            "Father is a scholar, religious leader, or very respected person. "
            "Guru blessings throughout life. Long-distance pilgrimage. "
            "One of the best placements — Jupiter in its own natural house from 5th.",
        confidence=0.93, verse="BPHS Ch.27 v.33-36",
        tags=["graha_bhava", "jupiter_9th", "very_religious", "father_scholar", "guru_blessings", "fortunate"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC058", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 10th house: Prestigious, respected career. Profession "
            "connected to teaching, law, religion, or public service. "
            "Fame through wisdom and ethical conduct. Authority figures respect native. "
            "Excellent for judges, professors, physicians, religious leaders.",
        confidence=0.92, verse="BPHS Ch.27 v.37-40",
        tags=["graha_bhava", "jupiter_10th", "prestigious_career", "respected", "law_religion", "fame"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC059", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 11th house: Abundant gains; many and influential friends. "
            "Elder siblings are learned or helpful. Multiple income streams, especially "
            "from intellectual or spiritual work. Aspirations easily fulfilled. "
            "Gains increase with age. One of Jupiter's strongest income houses.",
        confidence=0.92, verse="BPHS Ch.27 v.41-44",
        tags=["graha_bhava", "jupiter_11th", "abundant_gains", "influential_friends", "aspirations_fulfilled"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC060", source="BPHS", chapter="Ch.27", school="parashari",
        category="graha_bhava",
        description="Jupiter in 12th house: Spiritual liberation aspirations; ashram or "
            "monastery life possible. Generosity leads to expenses. Foreign dharmic "
            "journeys. Bed pleasures are refined. Good for moksha path. "
            "Losses are philosophical — native does not grieve material losses.",
        confidence=0.86, verse="BPHS Ch.27 v.45-48",
        tags=["graha_bhava", "jupiter_12th", "spiritual_liberation", "ashram", "moksha", "generous_losses"],
        implemented=False,
    ),
    # ── VENUS in Houses 1–12 (GBC061–072) ────────────────────────────────────
    RuleRecord(
        rule_id="GBC061", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 1st house: Physically attractive, charming, artistic, "
            "luxury-loving. Popular with opposite sex. Sweet nature, pleasant voice. "
            "Tendency toward sensual pleasures. Good health and longevity. "
            "Success through charisma and aesthetic sensibility.",
        confidence=0.90, verse="BPHS Ch.28 v.1-4",
        tags=["graha_bhava", "venus_1st", "attractive", "charming", "artistic", "luxury"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC062", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 2nd house: Melodious, sweet speech; wealth through arts, "
            "beauty, or women. Beautiful eyes and face. Family values aesthetics. "
            "Income from entertainment, cosmetics, jewellery, or luxury goods. "
            "Good food and material comforts.",
        confidence=0.88, verse="BPHS Ch.28 v.5-8",
        tags=["graha_bhava", "venus_2nd", "sweet_speech", "wealth_arts", "beautiful_face"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC063", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 3rd house: Artistic communication, charming and diplomatic "
            "in interactions. Siblings may be artistically inclined. Short journeys "
            "for pleasure or arts. Writing on beauty, love, or luxury. "
            "Musical or artistic skills in communication.",
        confidence=0.86, verse="BPHS Ch.28 v.9-12",
        tags=["graha_bhava", "venus_3rd", "artistic_communication", "charming", "artistic_siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC064", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 4th house: Beautiful, comfortable home; excellent domestic "
            "happiness. Luxury vehicles. Beautiful, artistic mother. "
            "Property in beautiful locations. Happy family life. "
            "Arts and music in the home. Aesthetic sensibility in domestic environment.",
        confidence=0.90, verse="BPHS Ch.28 v.13-16",
        tags=["graha_bhava", "venus_4th", "beautiful_home", "domestic_happiness", "luxury_vehicle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC065", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 5th house: Creative, romantic, artistically gifted. "
            "Beautiful children; daughters especially blessed. Romantic love affairs. "
            "Speculative gains through creative or entertainment ventures. "
            "Artistic intelligence and aesthetic sensibility.",
        confidence=0.88, verse="BPHS Ch.28 v.17-20",
        tags=["graha_bhava", "venus_5th", "creative_romantic", "beautiful_children", "artistic_intelligence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC066", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 6th house: Enemies may be women or beauty-related. "
            "Health through reproductive system; urinary or reproductive issues possible. "
            "Service in beauty, arts, or healthcare. Wins enemies through charm. "
            "Some relationship issues due to Venus in an inauspicious house.",
        confidence=0.84, verse="BPHS Ch.28 v.21-24",
        tags=["graha_bhava", "venus_6th", "enemies_women", "reproductive_health", "service_arts"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC067", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 7th house: Beautiful, artistic, sensually attractive spouse. "
            "Happy and pleasurable marriage. Partnerships in arts or luxury goods. "
            "Multiple attractions possible. Maraka significance but pleasurable. "
            "Marriage brings beauty and comfort into life.",
        confidence=0.90, verse="BPHS Ch.28 v.25-28",
        tags=["graha_bhava", "venus_7th", "beautiful_spouse", "happy_marriage", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC068", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 8th house: Inheritance from spouse or women. Sensual occult "
            "interests; Tantra, Kundalini practices. Longevity through pleasure. "
            "Hidden beauty or secret romantic life. Transformation through relationships. "
            "Bed pleasures strong throughout life.",
        confidence=0.85, verse="BPHS Ch.28 v.29-32",
        tags=["graha_bhava", "venus_8th", "inheritance_spouse", "tantra", "secret_romantic", "longevity_pleasure"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC069", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 9th house: Fortune through arts, beauty, or women. "
            "Spiritual aesthetics; beautiful temples or places of worship in life. "
            "Father may be artistic or luxury-loving. Dharma expressed through beauty. "
            "Luck in creative and aesthetic fields.",
        confidence=0.87, verse="BPHS Ch.28 v.33-36",
        tags=["graha_bhava", "venus_9th", "fortune_arts", "spiritual_aesthetics", "father_artistic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC070", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 10th house: Career in arts, entertainment, beauty, luxury, "
            "fashion, hospitality, or diplomacy. Famous through aesthetic work. "
            "Attractive workplace and colleagues. Career brings pleasures. "
            "Respected for artistic or diplomatic achievements.",
        confidence=0.88, verse="BPHS Ch.28 v.37-40",
        tags=["graha_bhava", "venus_10th", "career_arts", "entertainment", "famous_aesthetic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC071", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 11th house: Gains from arts, women, luxury goods, "
            "beauty industry. Beautiful social circle; artistic friends. "
            "Elder siblings may be artistic or beautiful. Wishes for pleasure fulfilled. "
            "Multiple and pleasurable income streams.",
        confidence=0.88, verse="BPHS Ch.28 v.41-44",
        tags=["graha_bhava", "venus_11th", "gains_arts", "beautiful_social_circle", "wishes_pleasure"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC072", source="BPHS", chapter="Ch.28", school="parashari",
        category="graha_bhava",
        description="Venus in 12th house: Bed pleasures and sensual enjoyment strong; "
            "focus on private romantic life. Expenditure on luxury and pleasure. "
            "Foreign connections through arts or romance. Spiritual beauty practices. "
            "Eye beauty; comfortable end of life.",
        confidence=0.85, verse="BPHS Ch.28 v.45-48",
        tags=["graha_bhava", "venus_12th", "bed_pleasures", "luxury_expenditure", "foreign_romance"],
        implemented=False,
    ),
    # ── SATURN in Houses 1–12 (GBC073–084) ───────────────────────────────────
    RuleRecord(
        rule_id="GBC073", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 1st house: Thin, dark or sallow complexion; slow to start "
            "but long-lived. Disciplined, hardworking, patient. Detached from body. "
            "Health challenges early in life; improves with age. Serious demeanor. "
            "Longevity excellent if not afflicted. Karmic weight felt in personality.",
        confidence=0.88, verse="BPHS Ch.29 v.1-4",
        tags=["graha_bhava", "saturn_1st", "thin_dark", "disciplined", "longevity", "karmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC074", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 2nd house: Harsh, serious, or minimal speech. Family "
            "hardship especially in childhood. Delayed wealth accumulation through "
            "persistent effort. Dental issues, dark complexion on face. "
            "Maraka significance — Saturn in 2nd is a powerful Maraka.",
        confidence=0.87, verse="BPHS Ch.29 v.5-8",
        tags=["graha_bhava", "saturn_2nd", "harsh_speech", "family_hardship", "delayed_wealth", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC075", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 3rd house: Persistent, systematic courage. Gains through "
            "long-term effort in communications and siblings. Younger siblings may be "
            "few or face hardship. Writing on serious, technical, or historical topics. "
            "Upachaya — Saturn's delays transform into steady gains.",
        confidence=0.88, verse="BPHS Ch.29 v.9-12",
        tags=["graha_bhava", "saturn_3rd", "persistent_courage", "systematic", "upachaya", "technical_writing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC076", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 4th house: Domestic distance and coldness; mother's health "
            "affected or early separation from mother. Property through hard work but "
            "disputes possible. Vehicles acquired late. Agricultural or real estate "
            "work through persistent effort. Emotional detachment at home.",
        confidence=0.86, verse="BPHS Ch.29 v.13-16",
        tags=["graha_bhava", "saturn_4th", "domestic_distance", "mother_separation", "property_delays"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC077", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 5th house: Children delayed or limited; few progeny. "
            "Serious, disciplined intellect. Speculative activities bring losses. "
            "Past-life karmic restrictions on creative expression. "
            "Children if born are serious, studious, or face early hardship.",
        confidence=0.85, verse="BPHS Ch.29 v.17-20",
        tags=["graha_bhava", "saturn_5th", "few_children", "serious_intellect", "speculative_loss", "karmic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC078", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 6th house: Excellent — destroys enemies through persistent "
            "effort. Victory in long-drawn legal disputes. Service sector success; "
            "management of large organizations, labor, or agriculture. "
            "Best placement for Saturn in Upachaya. Health improves over time.",
        confidence=0.92, verse="BPHS Ch.29 v.21-24",
        tags=["graha_bhava", "saturn_6th", "destroys_enemies", "legal_victory", "service_management", "best_upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC079", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 7th house: Late marriage; spouse is older, serious, or from "
            "a different background. Detachment in romantic relationships. "
            "Long-lasting but emotionally distant partnerships. Business partnerships "
            "require patience. Maraka significance.",
        confidence=0.86, verse="BPHS Ch.29 v.25-28",
        tags=["graha_bhava", "saturn_7th", "late_marriage", "older_spouse", "detachment", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC080", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 8th house: Longevity — Saturn in 8th gives long life. "
            "Chronic ailments requiring persistent management. Occult mastery through "
            "discipline. Ancestral property with complications. Shasha Yoga possible. "
            "Transformation through disciplined acceptance of suffering.",
        confidence=0.88, verse="BPHS Ch.29 v.29-32",
        tags=["graha_bhava", "saturn_8th", "longevity", "chronic_ailments", "occult_mastery", "shasha_yoga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC081", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 9th house: Conservative, austere approach to dharma. "
            "Father may be austere, disciplined, or distant. Pilgrimage through hardship. "
            "Fortune comes late but persistently. Challenges to orthodox religion lead "
            "to deeper personal dharmic understanding.",
        confidence=0.85, verse="BPHS Ch.29 v.33-36",
        tags=["graha_bhava", "saturn_9th", "austere_dharma", "father_austere", "late_fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC082", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 10th house: Persistent career; delayed but lasting success. "
            "Authority through long service and discipline. Career in government, "
            "administration, agriculture, law, construction, or labor management. "
            "Upachaya — career builds steadily over decades. Fame in old age.",
        confidence=0.88, verse="BPHS Ch.29 v.37-40",
        tags=["graha_bhava", "saturn_10th", "persistent_career", "delayed_success", "upachaya", "government"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC083", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 11th house: Slow but steadily accumulating income. "
            "Elder siblings face hardship or are few. Social circle of serious, "
            "older persons. Long-term financial goals achieved through discipline. "
            "Upachaya — best placement for slow but permanent wealth accumulation.",
        confidence=0.88, verse="BPHS Ch.29 v.41-44",
        tags=["graha_bhava", "saturn_11th", "slow_accumulation", "elder_siblings", "long_term_gains", "upachaya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC084", source="BPHS", chapter="Ch.29", school="parashari",
        category="graha_bhava",
        description="Saturn in 12th house: Spiritual isolation and disciplined austerity. "
            "Tendency toward hospitals, prisons, or ashrams. Expenditure through "
            "persistent losses but spiritual longevity. Good for moksha through "
            "disciplined renunciation. Feet and left eye issues.",
        confidence=0.85, verse="BPHS Ch.29 v.45-48",
        tags=["graha_bhava", "saturn_12th", "spiritual_isolation", "austerity", "moksha", "hospital"],
        implemented=False,
    ),
    # ── RAHU in Houses 1–12 (GBC085–096) ─────────────────────────────────────
    RuleRecord(
        rule_id="GBC085", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 1st house: Unconventional, unusual appearance, restless, "
            "ambitious beyond normal bounds. Foreign influence on personality. "
            "Illusion of self; confusion about identity. Health issues tied to past-life "
            "karma. Strong worldly desires. Magnetic but unpredictable personality.",
        confidence=0.86, verse="BPHS Ch.30 v.1-4",
        tags=["graha_bhava", "rahu_1st", "unconventional", "foreign_influence", "identity_confusion", "ambitious"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC086", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 2nd house: Unusual speech patterns; may speak foreign languages "
            "or in unconventional ways. Wealth from foreign or unusual sources. "
            "Family background may be mixed or unconventional. Materialistic. "
            "Food habits unusual or exotic.",
        confidence=0.84, verse="BPHS Ch.30 v.5-8",
        tags=["graha_bhava", "rahu_2nd", "unusual_speech", "foreign_wealth", "unconventional_family"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC087", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 3rd house: Extraordinary courage through unconventional means. "
            "Technology, media, and communication skills exceptional. Siblings may be "
            "unconventional or foreign-connected. Short journeys to unusual places. "
            "Innovative writing and bold expression.",
        confidence=0.85, verse="BPHS Ch.30 v.9-12",
        tags=["graha_bhava", "rahu_3rd", "extraordinary_courage", "technology", "innovative_media"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC088", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 4th house: Domestic instability; frequent moves or unusual home. "
            "Mother's health or foreign background. Property dealings with foreigners "
            "or in foreign lands. Vehicles of unusual type. "
            "Emotional restlessness; difficulty settling.",
        confidence=0.83, verse="BPHS Ch.30 v.13-16",
        tags=["graha_bhava", "rahu_4th", "domestic_instability", "foreign_property", "emotional_restlessness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC089", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 5th house: Unconventional intellect; interest in technology, "
            "occult, or foreign subjects. Speculative gains through unconventional means. "
            "Children may be adopted, foreign-born, or unconventional. "
            "Past-life karmic connections with unusual creative expression.",
        confidence=0.83, verse="BPHS Ch.30 v.17-20",
        tags=["graha_bhava", "rahu_5th", "unconventional_intellect", "speculative", "adopted_children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC090", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 6th house: Victory over enemies through cunning and strategy. "
            "Foreign healthcare connections. Unusual diseases requiring unconventional "
            "treatment. Wins litigation through unexpected means. "
            "Success in foreign competition or against foreign adversaries.",
        confidence=0.85, verse="BPHS Ch.30 v.21-24",
        tags=["graha_bhava", "rahu_6th", "cunning_victory", "foreign_healthcare", "unusual_disease"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC091", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 7th house: Unusual or foreign marriage partner. Relationship "
            "complexity and possible deception in partnerships. Maraka significance "
            "with obsessive quality. Business partnerships in foreign markets. "
            "Attraction to the unconventional and exotic.",
        confidence=0.83, verse="BPHS Ch.30 v.25-28",
        tags=["graha_bhava", "rahu_7th", "foreign_spouse", "partnership_complexity", "maraka"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC092", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 8th house: Occult mastery, hidden resources, secret foreign "
            "connections. Transformation through crisis involving foreigners or "
            "unconventional circumstances. Unexpected inheritances. "
            "Longevity with hidden karmic burden. Research into taboo subjects.",
        confidence=0.83, verse="BPHS Ch.30 v.29-32",
        tags=["graha_bhava", "rahu_8th", "occult_mastery", "hidden_resources", "unexpected_inheritance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC093", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 9th house: Unconventional dharma; exotic or foreign philosophical "
            "systems attract. Guru from foreign culture. Father may be unconventional "
            "or have foreign connections. Long journeys to exotic places. "
            "Fortune through unusual or foreign means.",
        confidence=0.82, verse="BPHS Ch.30 v.33-36",
        tags=["graha_bhava", "rahu_9th", "unconventional_dharma", "foreign_guru", "exotic_philosophy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC094", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 10th house: Fame through unconventional career; success in "
            "foreign lands or through technology, media, or mass communication. "
            "Public prominence through unusual or groundbreaking work. "
            "Career involves foreign elements or global scale activities.",
        confidence=0.85, verse="BPHS Ch.30 v.37-40",
        tags=["graha_bhava", "rahu_10th", "fame_unconventional", "foreign_career", "technology_media"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC095", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 11th house: Material gains through foreign, technology, or "
            "unconventional channels. Elder siblings with unusual lives. "
            "Social network diverse and international. Aspirations are worldly "
            "and material. Long-term gains through unconventional networks.",
        confidence=0.84, verse="BPHS Ch.30 v.41-44",
        tags=["graha_bhava", "rahu_11th", "foreign_gains", "technology_income", "international_network"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC096", source="BPHS", chapter="Ch.30", school="parashari",
        category="graha_bhava",
        description="Rahu in 12th house: Foreign residence; past-life karmic debt "
            "manifests as spiritual confusion or material loss. Expenditure through "
            "unconventional or foreign sources. Hidden foreign connections. "
            "Some interest in foreign spiritual systems.",
        confidence=0.82, verse="BPHS Ch.30 v.45-48",
        tags=["graha_bhava", "rahu_12th", "foreign_residence", "past_life_debt", "spiritual_confusion"],
        implemented=False,
    ),
    # ── KETU in Houses 1–12 (GBC097–108) ─────────────────────────────────────
    RuleRecord(
        rule_id="GBC097", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 1st house: Spiritual, mystical, sharp intuition and psychic "
            "sensitivity. Detached from body; mysterious aura. Medical issues related "
            "to past-life karma. Tendency toward spiritual practices. "
            "Personality is enigmatic, hard to categorize.",
        confidence=0.85, verse="BPHS Ch.31 v.1-4",
        tags=["graha_bhava", "ketu_1st", "spiritual", "mystical", "psychic", "past_life_karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC098", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 2nd house: Detachment from family wealth; frugal or minimal "
            "speech. Ancestral spiritual knowledge. Family traditions are spiritual "
            "or austere. Past-life karmic connection to family wealth patterns. "
            "Speech is direct, cutting, or spiritually pointed.",
        confidence=0.83, verse="BPHS Ch.31 v.5-8",
        tags=["graha_bhava", "ketu_2nd", "detachment_wealth", "frugal_speech", "ancestral_spiritual"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC099", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 3rd house: Mystical courage; detachment from siblings or "
            "spiritual relationship with them. Writing on spiritual, mystical, or "
            "esoteric topics. Short journeys to spiritual places. "
            "Communication has a spiritual or cutting precision.",
        confidence=0.83, verse="BPHS Ch.31 v.9-12",
        tags=["graha_bhava", "ketu_3rd", "mystical_courage", "spiritual_writing", "esoteric"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC100", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 4th house: Detachment from home and mother; ancestral karmic "
            "burden in domestic life. Property through spiritual or inherited means. "
            "Difficulty settling in one place. Mother may be spiritually inclined "
            "or have past-life karmic significance.",
        confidence=0.82, verse="BPHS Ch.31 v.13-16",
        tags=["graha_bhava", "ketu_4th", "detachment_home", "ancestral_karma", "no_settlement"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC101", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 5th house: Spiritual intelligence, past-life wisdom accessible. "
            "Children may be few, spiritually inclined, or from past-life connections. "
            "Speculative activities bring detachment. Meditation and mantra siddhis. "
            "Creative intelligence rooted in past-life skills.",
        confidence=0.83, verse="BPHS Ch.31 v.17-20",
        tags=["graha_bhava", "ketu_5th", "spiritual_intelligence", "past_life_wisdom", "mantra_siddhis"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC102", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 6th house: Mysterious ailments with karmic roots; diseases "
            "from past lives. Spiritual enemies or psychic attacks. Victory over enemies "
            "through spiritual means. Service in healing or spiritual practices. "
            "Detachment from competitive struggles.",
        confidence=0.82, verse="BPHS Ch.31 v.21-24",
        tags=["graha_bhava", "ketu_6th", "karmic_diseases", "spiritual_enemies", "healing_service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC103", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 7th house: Unusual or spiritualized partnerships; possible "
            "renunciation of conventional marriage. Spouse may be spiritual, foreign, "
            "or from a past-life connection. Detachment from partnerships over time. "
            "Karmic marriage obligations from past lives.",
        confidence=0.82, verse="BPHS Ch.31 v.25-28",
        tags=["graha_bhava", "ketu_7th", "spiritual_partnership", "past_life_spouse", "detachment_marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC104", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 8th house: Past-life occult mastery activated. Mystical "
            "longevity through detachment. Ancestral spiritual inheritance. "
            "Transformation through surrender. Karmic debt in this life related "
            "to occult misuse in past life. Deep spiritual insight.",
        confidence=0.83, verse="BPHS Ch.31 v.29-32",
        tags=["graha_bhava", "ketu_8th", "occult_mastery", "mystical_longevity", "ancestral_inheritance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC105", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 9th house: Strong moksha inclination; spiritual philosophy "
            "rooted in past-life wisdom. Guru may be from a mystical or non-mainstream "
            "lineage. Father connected to liberation path. Detachment from conventional "
            "religious forms while deeply spiritual within.",
        confidence=0.84, verse="BPHS Ch.31 v.33-36",
        tags=["graha_bhava", "ketu_9th", "moksha_inclination", "mystical_guru", "father_liberation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC106", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 10th house: Unusual career with karmic overtones; work in "
            "spiritual, healing, or research fields. Detachment from career ambitions "
            "over time. Public role feels like a karmic obligation. "
            "Success in careers involving mysticism, medicine, or liberation.",
        confidence=0.82, verse="BPHS Ch.31 v.37-40",
        tags=["graha_bhava", "ketu_10th", "unusual_career", "karmic_obligation", "spiritual_career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC107", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 11th house: Detachment from gains and desires. Gains come "
            "through spiritual networks or unexpectedly. Elder siblings with spiritual "
            "or unusual lives. Aspirations shift toward liberation over time. "
            "Material gains followed by detachment from them.",
        confidence=0.82, verse="BPHS Ch.31 v.41-44",
        tags=["graha_bhava", "ketu_11th", "detachment_gains", "spiritual_network", "liberation_aspiration"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="GBC108", source="BPHS", chapter="Ch.31", school="parashari",
        category="graha_bhava",
        description="Ketu in 12th house: Most powerful for moksha — liberation from the "
            "cycle of rebirth indicated. Spiritual practices bear fruit in isolation. "
            "Ashram or monastery life suits. Past-life merit enables liberation in this life. "
            "Expenditure is for spiritual purposes. Best Ketu placement for moksha.",
        confidence=0.87, verse="BPHS Ch.31 v.45-48",
        tags=["graha_bhava", "ketu_12th", "moksha_powerful", "liberation", "ashram", "spiritual_merit"],
        implemented=False,
    ),
]

for rule in _RULES:
    BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.add(rule)
