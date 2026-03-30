"""src/corpus/saravali_signs_7.py — S287: Saravali Saturn in 12 Signs (Ch.31).

Phase: 1B_matrix | Source: Saravali | School: parashari
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


_SATURN_ARIES_DATA = [
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.1", "Saturn debilitated in Aries: restless and frustrated nature, anger without discipline, impatient with authority"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.2", "Saturn debilitated in Aries: career setbacks, conflicts with employers, delayed professional recognition"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.3", "Saturn debilitated in Aries: financial instability, impulsive spending, difficulty accumulating savings"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.4", "Saturn debilitated in Aries: headaches, dental problems, bone injuries, accidents from rashness"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.5", "Saturn debilitated in Aries: strained relationships, cold partner, delayed or troubled marriage"),
    ("saturn", "sign_placement", "aries", {}, "mixed", "moderate", ['enemies_litigation'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.6", "Saturn debilitated in Aries: legal troubles, disputes with authority, conflicts poorly managed"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.7", "Saturn debilitated in Aries: reputation suffers from impulsive actions, lack of discipline noticed by others"),
    ("saturn", "sign_placement", "aries", {}, "unfavorable", "moderate", ['longevity'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.8", "Saturn debilitated in Aries: health risks from accidents, need for discipline in physical activities"),
    ("saturn", "sign_placement", "aries", {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'aries'], "Ch.31 v.9", "Saturn debilitated in Aries: learning through hardship, practical but scattered education"),
    ("saturn", "sign_condition", "aries_saturn_debilitated", {}, "unfavorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'aries', 'condition'], "Ch.31 v.10", "Saturn debilitated in Aries: severe restriction on progress, must work extremely hard for minimal gains"),
    ("saturn", "sign_condition", "aries_saturn_neecha_bhanga", {}, "favorable", "moderate", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'aries', 'condition'], "Ch.31 v.11", "Saturn debilitated with cancellation in Aries: late rise through struggle, earns respect through perseverance"),
    ("saturn", "sign_condition", "aries_saturn_navamsa", {}, "mixed", "moderate", ['career_status', 'longevity'], ['saturn', 'saravali', 'sign_placement', 'aries', 'condition'], "Ch.31 v.12", "Saturn debilitated in Aries strong navamsa: partial mitigation, structured effort eventually pays off"),
]

_SATURN_TAURUS_DATA = [
    ("saturn", "sign_placement", "taurus", {}, "favorable", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.13", "Saturn in Taurus: slow but steady wealth accumulation, expertise in agriculture, mining, or construction"),
    ("saturn", "sign_placement", "taurus", {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.14", "Saturn in Taurus: patient and enduring nature, practical approach to life, stubborn but reliable"),
    ("saturn", "sign_placement", "taurus", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.15", "Saturn in Taurus: delayed marriage, older or mature spouse, loyal but unromantic partnership"),
    ("saturn", "sign_placement", "taurus", {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.16", "Saturn in Taurus: success in agriculture, real estate, mining, construction, or traditional industries"),
    ("saturn", "sign_placement", "taurus", {}, "mixed", "moderate", ['physical_appearance'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.17", "Saturn in Taurus: sturdy and solid build, aged appearance, strong bones, plain features"),
    ("saturn", "sign_placement", "taurus", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.18", "Saturn in Taurus: throat and neck problems, dental issues, skin dryness, chronic ailments"),
    ("saturn", "sign_placement", "taurus", {}, "favorable", "moderate", ['property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.19", "Saturn in Taurus: acquires land and property through patience, traditional home, lasting assets"),
    ("saturn", "sign_placement", "taurus", {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.20", "Saturn in Taurus: practical knowledge, traditional learning, expertise through long apprenticeship"),
    ("saturn", "sign_placement", "taurus", {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'sign_placement', 'taurus'], "Ch.31 v.21", "Saturn in Taurus: steady constitution, endurance despite ailments, long life through discipline"),
    ("saturn", "sign_condition", "taurus_saturn_venus_sign", {}, "favorable", "moderate", ['wealth', 'property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'taurus', 'condition'], "Ch.31 v.22", "Saturn in Taurus (Venus sign): disciplined luxury, patient accumulation of beautiful assets"),
    ("saturn", "sign_condition", "taurus_saturn_benefic", {}, "favorable", "moderate", ['wealth', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'taurus', 'condition'], "Ch.31 v.23", "Saturn in Taurus aspected by benefics: steady prosperity, recognized for reliability"),
    ("saturn", "sign_condition", "taurus_saturn_navamsa", {}, "favorable", "moderate", ['wealth', 'longevity'], ['saturn', 'saravali', 'sign_placement', 'taurus', 'condition'], "Ch.31 v.24", "Saturn in Taurus strong navamsa: enduring prosperity, solid health, lasting legacy"),
]

_SATURN_GEMINI_DATA = [
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.25", "Saturn in Gemini: slow but thorough learner, methodical thinking, expertise in technical writing or research"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.26", "Saturn in Gemini: serious communicator, dry wit, analytical mind, pessimistic outlook possible"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.27", "Saturn in Gemini: success in research, technical writing, accounting, data analysis, or structured communication"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.28", "Saturn in Gemini: moderate income through intellectual work, careful financial planning"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.29", "Saturn in Gemini: intellectual but emotionally distant partner, communication barriers in marriage"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.30", "Saturn in Gemini: respiratory issues, nervous disorders, shoulder and arm problems"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['physical_appearance'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.31", "Saturn in Gemini: thin build, serious expression, looks older than age, restless eyes"),
    ("saturn", "sign_placement", "gemini", {}, "mixed", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'gemini'], "Ch.31 v.32", "Saturn in Gemini: respected for analytical depth, known for serious scholarship, methodical reputation"),
    ("saturn", "sign_condition", "gemini_saturn_mercury_sign", {}, "mixed", "moderate", ['intelligence_education', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'gemini', 'condition'], "Ch.31 v.33", "Saturn in Gemini (Mercury sign): structured intellect, disciplined communication, technical expertise"),
    ("saturn", "sign_condition", "gemini_saturn_benefic", {}, "favorable", "moderate", ['intelligence_education', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'gemini', 'condition'], "Ch.31 v.34", "Saturn in Gemini aspected by benefics: scholarly recognition, structured knowledge gains social respect"),
]

_SATURN_CANCER_DATA = [
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['mental_health'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.35", "Saturn in Cancer: emotional restriction, depression tendency, difficulty expressing feelings"),
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.36", "Saturn in Cancer: cold domestic atmosphere, emotional distance from spouse, unhappy home life"),
    ("saturn", "sign_placement", "cancer", {}, "mixed", "moderate", ['property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.37", "Saturn in Cancer: property through struggle, old or neglected home, repairs constantly needed"),
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.38", "Saturn in Cancer: emotionally guarded, suspicious nature, fear of abandonment, melancholic disposition"),
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.39", "Saturn in Cancer: stomach and digestive disorders, chest complaints, chronic gastric issues"),
    ("saturn", "sign_placement", "cancer", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.40", "Saturn in Cancer: financial anxiety despite moderate income, hoarding tendency, fear of poverty"),
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['progeny'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.41", "Saturn in Cancer: delayed or difficult childbirth, emotional distance from children, few offspring"),
    ("saturn", "sign_placement", "cancer", {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.42", "Saturn in Cancer: success in real estate, elderly care, traditional foods, or water-related industries"),
    ("saturn", "sign_placement", "cancer", {}, "unfavorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'cancer'], "Ch.31 v.43", "Saturn in Cancer: public image suffers from emotional coldness, perceived as uncaring"),
    ("saturn", "sign_condition", "cancer_saturn_moon_sign", {}, "unfavorable", "moderate", ['mental_health', 'marriage'], ['saturn', 'saravali', 'sign_placement', 'cancer', 'condition'], "Ch.31 v.44", "Saturn in Cancer (Moon sign, enemy): emotional suppression, Vish Yoga tendencies, domestic unhappiness"),
    ("saturn", "sign_condition", "cancer_saturn_benefic", {}, "mixed", "moderate", ['mental_health', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'cancer', 'condition'], "Ch.31 v.45", "Saturn in Cancer aspected by benefics: emotional discipline channels into caregiving career"),
    ("saturn", "sign_condition", "cancer_saturn_navamsa", {}, "mixed", "moderate", ['marriage', 'property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'cancer', 'condition'], "Ch.31 v.46", "Saturn in Cancer strong navamsa: eventually stabilizes home life, acquires property through patience"),
]

_SATURN_LEO_DATA = [
    ("saturn", "sign_placement", "leo", {}, "unfavorable", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.47", "Saturn in Leo: conflicts with authority, ego vs discipline, power struggles with superiors"),
    ("saturn", "sign_placement", "leo", {}, "unfavorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.48", "Saturn in Leo: frustrated ambition, dignity without recognition, proud but denied status"),
    ("saturn", "sign_placement", "leo", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.49", "Saturn in Leo: income through government or authority channels, slow career advancement"),
    ("saturn", "sign_placement", "leo", {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.50", "Saturn in Leo: heart problems, back pain, spine issues, chronic fatigue"),
    ("saturn", "sign_placement", "leo", {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.51", "Saturn in Leo: domineering partner or self, power struggles in marriage, ego clashes"),
    ("saturn", "sign_placement", "leo", {}, "mixed", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.52", "Saturn in Leo: reputation for severity, feared more than loved, respect through intimidation"),
    ("saturn", "sign_placement", "leo", {}, "mixed", "moderate", ['progeny'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.53", "Saturn in Leo: delayed children, strict parenting style, children face obstacles"),
    ("saturn", "sign_placement", "leo", {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'leo'], "Ch.31 v.54", "Saturn in Leo: disciplined but rigid thinking, authority in traditional knowledge"),
    ("saturn", "sign_condition", "leo_saturn_sun_sign", {}, "unfavorable", "moderate", ['career_status', 'character_temperament'], ['saturn', 'saravali', 'sign_placement', 'leo', 'condition'], "Ch.31 v.55", "Saturn in Leo (Sun sign, enemy): authority constantly challenged, ego-discipline conflict"),
    ("saturn", "sign_condition", "leo_saturn_benefic", {}, "mixed", "moderate", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'leo', 'condition'], "Ch.31 v.56", "Saturn in Leo aspected by benefics: eventually earns respect through sustained effort"),
]

_SATURN_VIRGO_DATA = [
    ("saturn", "sign_placement", "virgo", {}, "favorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.57", "Saturn in Virgo: meticulous and analytical, expertise in research, science, or technical fields"),
    ("saturn", "sign_placement", "virgo", {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.58", "Saturn in Virgo: success in medicine, accounting, quality control, service industries, or research"),
    ("saturn", "sign_placement", "virgo", {}, "mixed", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.59", "Saturn in Virgo: perfectionist and critical, worrying nature, helpful but demanding"),
    ("saturn", "sign_placement", "virgo", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.60", "Saturn in Virgo: steady income through service, careful financial management, modest but secure"),
    ("saturn", "sign_placement", "virgo", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.61", "Saturn in Virgo: intestinal disorders, nervous complaints, skin problems, chronic minor ailments"),
    ("saturn", "sign_placement", "virgo", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.62", "Saturn in Virgo: critical of partner, analytical approach to love, practical but unromantic marriage"),
    ("saturn", "sign_placement", "virgo", {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.63", "Saturn in Virgo: respected for expertise and precision, known for thorough work"),
    ("saturn", "sign_placement", "virgo", {}, "mixed", "moderate", ['physical_appearance'], ['saturn', 'saravali', 'sign_placement', 'virgo'], "Ch.31 v.64", "Saturn in Virgo: thin and wiry build, serious expression, neat appearance, looks older"),
    ("saturn", "sign_condition", "virgo_saturn_mercury_sign", {}, "favorable", "moderate", ['intelligence_education', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'virgo', 'condition'], "Ch.31 v.65", "Saturn in Virgo (Mercury sign, friend): analytical discipline, systematic research, technical mastery"),
    ("saturn", "sign_condition", "virgo_saturn_benefic", {}, "favorable", "moderate", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'virgo', 'condition'], "Ch.31 v.66", "Saturn in Virgo aspected by benefics: professional recognition, steady advancement"),
]

_SATURN_LIBRA_DATA = [
    ("saturn", "sign_placement", "libra", {}, "favorable", "strong", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.67", "Saturn exalted in Libra: attains high positions through justice and discipline, administrative excellence"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "strong", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.68", "Saturn exalted in Libra: renowned for fairness and integrity, public respect, lasting reputation"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "strong", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.69", "Saturn exalted in Libra: great wealth through law, justice, trade, or diplomatic service"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.70", "Saturn exalted in Libra: balanced discipline, fair-minded authority, just and impartial nature"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.71", "Saturn exalted in Libra: stable and mature marriage, partner respects authority, lasting partnership"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.72", "Saturn exalted in Libra: knowledge of law, political science, economics, systematic philosophy"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['physical_appearance'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.73", "Saturn exalted in Libra: dignified bearing, tall and lean, authoritative presence"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.74", "Saturn exalted in Libra: strong constitution despite lean build, long and productive life"),
    ("saturn", "sign_placement", "libra", {}, "favorable", "moderate", ['property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'libra'], "Ch.31 v.75", "Saturn exalted in Libra: acquires significant property, institutional buildings, lasting assets"),
    ("saturn", "sign_condition", "libra_saturn_exalted", {}, "favorable", "strong", ['career_status', 'fame_reputation', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'libra', 'condition'], "Ch.31 v.76", "Saturn exalted in Libra: pinnacle of Saturnian strength, supreme discipline, lasting authority"),
    ("saturn", "sign_condition", "libra_saturn_benefic", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'libra', 'condition'], "Ch.31 v.77", "Saturn exalted in Libra aspected by benefics: supreme public authority, revered for justice"),
    ("saturn", "sign_condition", "libra_saturn_malefic", {}, "mixed", "moderate", ['enemies_litigation', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'libra', 'condition'], "Ch.31 v.78", "Saturn exalted in Libra aspected by malefics: authority tested, legal challenges but overcomes"),
    ("saturn", "sign_condition", "libra_saturn_navamsa", {}, "favorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'libra', 'condition'], "Ch.31 v.79", "Saturn exalted in Libra vargottama: supreme disciplined authority, enduring legacy"),
]

_SATURN_SCORPIO_DATA = [
    ("saturn", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.80", "Saturn in Scorpio: secretive and suspicious nature, vindictive when wronged, brooding disposition"),
    ("saturn", "sign_placement", "scorpio", {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.81", "Saturn in Scorpio: success in investigation, research, mining, insurance, or occult disciplines"),
    ("saturn", "sign_placement", "scorpio", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.82", "Saturn in Scorpio: gains through hidden means, inheritance, insurance, or underground resources"),
    ("saturn", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.83", "Saturn in Scorpio: reproductive system problems, piles, chronic hidden ailments, slow recovery"),
    ("saturn", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.84", "Saturn in Scorpio: controlling and possessive partner, trust issues, secret relationships"),
    ("saturn", "sign_placement", "scorpio", {}, "mixed", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.85", "Saturn in Scorpio: deep research ability, occult knowledge, forensic expertise"),
    ("saturn", "sign_placement", "scorpio", {}, "unfavorable", "moderate", ['mental_health'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.86", "Saturn in Scorpio: obsessive tendencies, paranoia, difficulty letting go, psychological burden"),
    ("saturn", "sign_placement", "scorpio", {}, "mixed", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'scorpio'], "Ch.31 v.87", "Saturn in Scorpio: feared and respected, reputation for depth and intensity, secretive public image"),
    ("saturn", "sign_condition", "scorpio_saturn_mars_sign", {}, "unfavorable", "moderate", ['character_temperament', 'physical_health'], ['saturn', 'saravali', 'sign_placement', 'scorpio', 'condition'], "Ch.31 v.88", "Saturn in Scorpio (Mars sign): intense frustration, suppressed aggression, chronic health from stress"),
    ("saturn", "sign_condition", "scorpio_saturn_benefic", {}, "mixed", "moderate", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'scorpio', 'condition'], "Ch.31 v.89", "Saturn in Scorpio aspected by benefics: channeled intensity, success through deep investigation"),
]

_SATURN_SAGITTARIUS_DATA = [
    ("saturn", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['spirituality'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.90", "Saturn in Sagittarius: disciplined spiritual practice, structured religious study, philosophical depth"),
    ("saturn", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.91", "Saturn in Sagittarius: success in law, education, publishing, religious institutions, or governance"),
    ("saturn", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.92", "Saturn in Sagittarius: righteous discipline, follows rules strictly, traditional values upheld"),
    ("saturn", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.93", "Saturn in Sagittarius: wealth through institutional work, education, or religious service, moderate income"),
    ("saturn", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.94", "Saturn in Sagittarius: spouse from different background, marriage based on shared ideals, mature partnership"),
    ("saturn", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.95", "Saturn in Sagittarius: systematic philosophical study, traditional education, expertise in law or theology"),
    ("saturn", "sign_placement", "sagittarius", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.96", "Saturn in Sagittarius: hip and thigh problems, liver sluggishness, sciatic pain"),
    ("saturn", "sign_placement", "sagittarius", {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'sagittarius'], "Ch.31 v.97", "Saturn in Sagittarius: respected for principled living, known for discipline and traditional values"),
    ("saturn", "sign_condition", "sagittarius_saturn_jupiter_sign", {}, "favorable", "moderate", ['spirituality', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'sagittarius', 'condition'], "Ch.31 v.98", "Saturn in Sagittarius (Jupiter sign): disciplined dharma, structured spiritual authority, institutional success"),
    ("saturn", "sign_condition", "sagittarius_saturn_benefic", {}, "favorable", "moderate", ['fame_reputation', 'spirituality'], ['saturn', 'saravali', 'sign_placement', 'sagittarius', 'condition'], "Ch.31 v.99", "Saturn in Sagittarius aspected by benefics: venerated for discipline, spiritual elder status"),
]

_SATURN_CAPRICORN_DATA = [
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "strong", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.100", "Saturn in Capricorn (own sign): natural authority, rise to top positions through discipline and persistence"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "strong", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.101", "Saturn in Capricorn: great wealth through sustained effort, business acumen, corporate leadership"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.102", "Saturn in Capricorn: ambitious and disciplined, pragmatic approach, commands respect through competence"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.103", "Saturn in Capricorn: lasting reputation for reliability and competence, institutional leadership"),
    ("saturn", "sign_placement", "capricorn", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.104", "Saturn in Capricorn: practical marriage, older or mature spouse, duty-based relationship"),
    ("saturn", "sign_placement", "capricorn", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.105", "Saturn in Capricorn: knee problems, joint stiffness, dental issues, but strong overall constitution"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.106", "Saturn in Capricorn: practical knowledge, management expertise, traditional engineering or architecture"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "moderate", ['property_vehicles'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.107", "Saturn in Capricorn: significant property holdings, institutional buildings, lasting infrastructure"),
    ("saturn", "sign_placement", "capricorn", {}, "favorable", "moderate", ['longevity'], ['saturn', 'saravali', 'sign_placement', 'capricorn'], "Ch.31 v.108", "Saturn in Capricorn: strong constitution, endurance, long and productive working life"),
    ("saturn", "sign_condition", "capricorn_saturn_own", {}, "favorable", "strong", ['career_status', 'wealth', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'capricorn', 'condition'], "Ch.31 v.109", "Saturn in own sign Capricorn: full strength, maximum discipline, lasting authority and wealth"),
    ("saturn", "sign_condition", "capricorn_saturn_benefic", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'capricorn', 'condition'], "Ch.31 v.110", "Saturn in Capricorn aspected by benefics: supreme institutional leadership, honored for service"),
    ("saturn", "sign_condition", "capricorn_saturn_navamsa", {}, "favorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'capricorn', 'condition'], "Ch.31 v.111", "Saturn in Capricorn vargottama: unshakeable authority, enduring legacy, disciplined empire"),
]

_SATURN_AQUARIUS_DATA = [
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "strong", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.112", "Saturn in Aquarius (own sign): success through innovation, social reform, technology, or humanitarian work"),
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.113", "Saturn in Aquarius: detached discipline, humanitarian outlook, progressive but structured thinking"),
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.114", "Saturn in Aquarius: income through organizations, technology, social enterprises, or innovation"),
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "moderate", ['intelligence_education'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.115", "Saturn in Aquarius: scientific thinking, technological expertise, innovative research methods"),
    ("saturn", "sign_placement", "aquarius", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.116", "Saturn in Aquarius: unconventional partnership, freedom within commitment, friendship-based marriage"),
    ("saturn", "sign_placement", "aquarius", {}, "mixed", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.117", "Saturn in Aquarius: circulation problems, ankle issues, nervous system sensitivity"),
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.118", "Saturn in Aquarius: known for progressive reform, respected in social organizations, humanitarian reputation"),
    ("saturn", "sign_placement", "aquarius", {}, "favorable", "moderate", ['foreign_travel'], ['saturn', 'saravali', 'sign_placement', 'aquarius'], "Ch.31 v.119", "Saturn in Aquarius: connections with international organizations, systematic foreign engagement"),
    ("saturn", "sign_condition", "aquarius_saturn_own", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'aquarius', 'condition'], "Ch.31 v.120", "Saturn in own sign Aquarius: full strength, innovative authority, lasting social impact"),
    ("saturn", "sign_condition", "aquarius_saturn_benefic", {}, "favorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'aquarius', 'condition'], "Ch.31 v.121", "Saturn in Aquarius aspected by benefics: successful reform, organizational leadership, progressive wealth"),
]

_SATURN_PISCES_DATA = [
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['character_temperament'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.122", "Saturn in Pisces: structured spirituality, disciplined devotion, melancholic but philosophical temperament"),
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['career_status'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.123", "Saturn in Pisces: success in charitable organizations, hospitals, monasteries, or spiritual institutions"),
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['wealth'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.124", "Saturn in Pisces: modest income, money through service or charity, expenses on spiritual causes"),
    ("saturn", "sign_placement", "pisces", {}, "favorable", "moderate", ['spirituality'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.125", "Saturn in Pisces: disciplined spiritual practice, renunciation tendencies, systematic meditation"),
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['marriage'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.126", "Saturn in Pisces: partner with spiritual inclination, compassionate but emotionally restricted marriage"),
    ("saturn", "sign_placement", "pisces", {}, "unfavorable", "moderate", ['physical_health'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.127", "Saturn in Pisces: feet problems, lymphatic issues, chronic fatigue, sensitivity to cold and damp"),
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['mental_health'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.128", "Saturn in Pisces: tendency to depression, melancholic spiritual longing, isolation preferences"),
    ("saturn", "sign_placement", "pisces", {}, "mixed", "moderate", ['fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'pisces'], "Ch.31 v.129", "Saturn in Pisces: quiet reputation, known for service and sacrifice, respected but not celebrated"),
    ("saturn", "sign_condition", "pisces_saturn_jupiter_sign", {}, "mixed", "moderate", ['spirituality', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'pisces', 'condition'], "Ch.31 v.130", "Saturn in Pisces (Jupiter sign): structured devotion, institutional spiritual work, monastic discipline"),
    ("saturn", "sign_condition", "pisces_saturn_benefic", {}, "favorable", "moderate", ['spirituality', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'pisces', 'condition'], "Ch.31 v.131", "Saturn in Pisces aspected by benefics: revered for spiritual discipline, recognized service"),
]

_SATURN_GENERAL_DATA = [
    ("saturn", "sign_condition", "saturn_own_sign", {}, "favorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.132", "Saturn in own sign (Capricorn/Aquarius): full Saturnian strength, disciplined authority, lasting institutions"),
    ("saturn", "sign_condition", "saturn_exalted", {}, "favorable", "strong", ['career_status', 'fame_reputation'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.133", "Saturn exalted in Libra: supreme discipline, just authority, lasting fame through fairness"),
    ("saturn", "sign_condition", "saturn_debilitated", {}, "unfavorable", "strong", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.134", "Saturn debilitated in Aries: severely hampered discipline, frustrated ambition, struggles without structure"),
    ("saturn", "sign_condition", "saturn_friend_sign", {}, "favorable", "moderate", ['career_status', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.135", "Saturn in friendly sign (Mercury/Venus): supported discipline, aesthetic or intellectual structure"),
    ("saturn", "sign_condition", "saturn_enemy_sign", {}, "unfavorable", "moderate", ['career_status', 'mental_health'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.136", "Saturn in enemy sign (Sun/Moon/Mars): conflicted discipline, authority challenged, emotional restriction"),
    ("saturn", "sign_condition", "saturn_retrograde", {}, "mixed", "moderate", ['career_status', 'longevity'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.137", "Saturn retrograde in any sign: karmic review, delayed but thorough rewards, past-life debts"),
    ("saturn", "sign_condition", "saturn_vargottama", {}, "favorable", "strong", ['career_status', 'longevity'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.138", "Saturn vargottama: amplified discipline and endurance, lasting authority across all domains"),
    ("saturn", "sign_condition", "saturn_aspected_jupiter", {}, "favorable", "moderate", ['spirituality', 'career_status'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.139", "Saturn aspected by Jupiter: dharmic discipline, blessed hardship, righteous authority"),
    ("saturn", "sign_condition", "saturn_aspected_mars", {}, "unfavorable", "moderate", ['physical_health', 'enemies_litigation'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.140", "Saturn aspected by Mars: accidents, surgical interventions, conflicts with authority"),
    ("saturn", "sign_condition", "saturn_aspected_venus", {}, "mixed", "moderate", ['marriage', 'wealth'], ['saturn', 'saravali', 'sign_placement', 'general', 'condition'], "Ch.31 v.141", "Saturn aspected by Venus: delayed luxury, patient beauty, artistic discipline eventually rewarded"),
]


def _make_sign_rules(data: list, start_id: int) -> list[RuleRecord]:
    rules: list[RuleRecord] = []
    for i, t in enumerate(data):
        planet, ptype, pval, extra, direction, intensity, domains, tags, vref, desc = t
        pc = {"planet": planet, "placement_type": ptype, "placement_value": [pval] if ptype == "sign_placement" else [], **extra}
        if ptype == "sign_condition":
            pc["yoga_label"] = pval
        rid = f"SAV{start_id + i}"
        rules.append(RuleRecord(
            rule_id=rid, source="Saravali", chapter="Ch.31", school="parashari",
            category="sign_predictions", description=desc, confidence=0.65,
            verse="Saravali " + vref, tags=tags, implemented=False, engine_ref="",
            primary_condition=pc, modifiers=[], exceptions=[],
            outcome_domains=domains, outcome_direction=direction,
            outcome_intensity=intensity, outcome_timing="dasha_dependent",
            lagna_scope=[], dasha_scope=[], verse_ref=vref,
            concordance_texts=[], divergence_notes="",
            phase="1B_matrix", system="natal",
        ))
    return rules


def _build_all_rules() -> list[RuleRecord]:
    all_sign_data = [
        (_SATURN_ARIES_DATA, 1862),
        (_SATURN_TAURUS_DATA, 1874),
        (_SATURN_GEMINI_DATA, 1886),
        (_SATURN_CANCER_DATA, 1896),
        (_SATURN_LEO_DATA, 1908),
        (_SATURN_VIRGO_DATA, 1918),
        (_SATURN_LIBRA_DATA, 1928),
        (_SATURN_SCORPIO_DATA, 1941),
        (_SATURN_SAGITTARIUS_DATA, 1951),
        (_SATURN_CAPRICORN_DATA, 1961),
        (_SATURN_AQUARIUS_DATA, 1973),
        (_SATURN_PISCES_DATA, 1983),
        (_SATURN_GENERAL_DATA, 1993),
    ]
    result: list[RuleRecord] = []
    for data, s in all_sign_data:
        result.extend(_make_sign_rules(data, s))
    return result


SARAVALI_SIGNS_7_REGISTRY = CorpusRegistry()
for _rule in _build_all_rules():
    SARAVALI_SIGNS_7_REGISTRY.add(_rule)
