"""
src/corpus/kp_sublord_rules.py — KP Sublord System Rules (S233)

Encodes Krishnamurti Paddhati (KP) sublord rules governing planetary
significations, house cusps, and event timing.

Sources:
  KP Astrology: K.S. Krishnamurti's "Stellar Astrological Reader" Vol.1-6
  KP Nakshatra Sublord theory (Nadi-based refinement of Vimshottari)

30 rules total: KPS001-KPS030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

KP_SUBLORD_RULES_REGISTRY = CorpusRegistry()

_KP_SUBLORD_RULES = [
    # --- Nakshatra Lord Structure (KPS001-006) ---
    RuleRecord(
        rule_id="KPS001",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "Each zodiac sign (30°) is divided into 9 sub-divisions per nakshatra "
            "portion. Each nakshatra (13°20') is divided into 9 sub-lords in "
            "proportion to Vimshottari dasha years: Ketu 7, Venus 20, Sun 6, "
            "Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17 years."
        ),
        confidence=0.95,
        verse="Reader_Vol1 p.45",
        tags=["kp_nakshatra", "sublord_structure", "vimshottari_proportion", "fundamental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS002",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Signification hierarchy: Star Lord > Sub Lord > Planet itself. "
            "The sub lord is the decisive factor for event manifestation. "
            "If sub lord is a significator of the event house, event occurs "
            "in that sub lord's period."
        ),
        confidence=0.95,
        verse="Reader_Vol1 p.52",
        tags=["kp_signification", "sublord_decisive", "hierarchy", "fundamental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS003",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "KP House Cusp Sub Lord: The sub lord of a house cusp determines "
            "whether matters of that house will fructify. If cusp sub lord "
            "is significator of that house or favorable houses, results manifest. "
            "If in inimical houses, results are denied."
        ),
        confidence=0.93,
        verse="Reader_Vol1 p.67",
        tags=["kp_cusp", "sublord_cusp", "house_fructification", "fundamental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS004",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Stellar Significators: A planet signifies houses it occupies "
            "(strongest), houses its nakshatra lord occupies/owns (strong), "
            "and houses it owns itself (basic). Occupation > Nakshatra > Ownership."
        ),
        confidence=0.95,
        verse="Reader_Vol1 p.78",
        tags=["kp_significator", "occupation", "nakshatra_lord", "ownership", "hierarchy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS005",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Event Timing Principle: An event occurs when: (1) Dasha lord, "
            "(2) Bhukti lord, and (3) Antara lord are all significators of "
            "the relevant event houses AND transit supports. All three must "
            "align simultaneously."
        ),
        confidence=0.93,
        verse="Reader_Vol1 p.95",
        tags=["kp_timing", "dasha_bhukti_antara", "triple_significator", "fundamental"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS006",
        source="KP",
        chapter="Reader_Vol1",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Ruling Planets (RP) at any moment: Moon's sign lord, Moon's "
            "nakshatra lord, Moon's sublord, Ascendant sign lord, Ascendant "
            "nakshatra lord, Ascendant sublord. These 6 planets govern the "
            "moment and are used for horary and transit analysis."
        ),
        confidence=0.90,
        verse="Reader_Vol1 p.112",
        tags=["kp_ruling_planets", "horary", "transit", "moment_rulers"],
        implemented=False,
    ),
    # --- Marriage / Relationship Houses (KPS007-010) ---
    RuleRecord(
        rule_id="KPS007",
        source="KP",
        chapter="Reader_Vol2",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Marriage: 7th cusp sub lord must be significator of houses "
            "2, 7, or 11 for marriage to occur. If 7th cusp sublord is "
            "connected only to 1, 6, or 10 without 2/7/11, marriage is delayed "
            "or denied in that period."
        ),
        confidence=0.92,
        verse="Reader_Vol2 p.34",
        tags=["kp_marriage", "7th_house", "sublord_2_7_11", "event_denial"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS008",
        source="KP",
        chapter="Reader_Vol2",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Divorce/Separation: 7th cusp sublord connected to houses 6, "
            "10, or 12 (without 2, 7, 11) indicates separation or non-fructification "
            "of marriage. House 12 indicates loss of spouse or distant spouse."
        ),
        confidence=0.88,
        verse="Reader_Vol2 p.41",
        tags=["kp_divorce", "separation", "7th_house", "6_10_12_connection"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS009",
        source="KP",
        chapter="Reader_Vol2",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Second Marriage: 11th cusp sublord and 9th cusp sublord both "
            "being significators of 7th house, combined with 7th cusp sublord "
            "linked to 9th or 11th, indicates potential for second union."
        ),
        confidence=0.84,
        verse="Reader_Vol2 p.52",
        tags=["kp_second_marriage", "11th_cusp", "9th_cusp", "7th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS010",
        source="KP",
        chapter="Reader_Vol2",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Partnership / Business: 7th cusp sublord connected to 7th "
            "and 10th (but not 2nd or 11th) favors business partnership over "
            "marriage. Both houses must be checked with their cusp sublords."
        ),
        confidence=0.84,
        verse="Reader_Vol2 p.63",
        tags=["kp_partnership", "business", "7th_10th", "sublord"],
        implemented=False,
    ),
    # --- Finance / Wealth Houses (KPS011-014) ---
    RuleRecord(
        rule_id="KPS011",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Financial Gain: 2nd cusp sublord must signify houses 2, 6, "
            "10, or 11 for consistent wealth accumulation. House 11 is "
            "most important for income gains. 6 = service income, "
            "10 = career income."
        ),
        confidence=0.90,
        verse="Reader_Vol3 p.28",
        tags=["kp_finance", "2nd_cusp", "wealth", "2_6_10_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS012",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Poverty / Financial Loss: 2nd cusp sublord connected to "
            "houses 8 or 12 without 2, 6, 10, 11 indicates financial loss "
            "or spending exceeds income. 12th indicates expenses and losses."
        ),
        confidence=0.87,
        verse="Reader_Vol3 p.35",
        tags=["kp_poverty", "financial_loss", "8th_12th", "2nd_cusp"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS013",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Inheritance / Sudden Wealth: 8th cusp sublord connected to "
            "2nd and 11th favors sudden gains, inheritance, lottery. "
            "The 8th house in KP = unearned wealth (distinct from Parashari "
            "interpretation of 8th as obstacles)."
        ),
        confidence=0.86,
        verse="Reader_Vol3 p.47",
        tags=["kp_inheritance", "sudden_wealth", "8th_cusp", "2nd_11th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS014",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Loan / Debt: 6th cusp sublord connected to 6th and 8th "
            "without 2nd or 11th indicates borrowing. 6th = taking loans; "
            "12th of 7th (6th) = creditors. Debt cycle shown by 6-8-12 connection."
        ),
        confidence=0.85,
        verse="Reader_Vol3 p.58",
        tags=["kp_debt", "6th_cusp", "loan", "6_8_12"],
        implemented=False,
    ),
    # --- Career / Profession (KPS015-018) ---
    RuleRecord(
        rule_id="KPS015",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Career Success: 10th cusp sublord must be significator of "
            "6, 10, or 11 for career establishment. 6 = service, 10 = authority, "
            "11 = fulfillment of career ambitions. Multiple connections "
            "to these houses indicate professional success."
        ),
        confidence=0.90,
        verse="Reader_Vol3 p.78",
        tags=["kp_career", "10th_cusp", "6_10_11", "profession"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS016",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Government Service: 10th cusp sublord connected to Sun's "
            "significator houses AND 6th house indicates government employment. "
            "Sun = government; 6 = service/employment relationship."
        ),
        confidence=0.85,
        verse="Reader_Vol3 p.89",
        tags=["kp_government_service", "10th_cusp", "sun_significator", "6th_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS017",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Self-Employment / Business: 10th cusp sublord connected to "
            "7th and 10th (without strong 6th) favors independent business. "
            "Mars influence on 10th = technical business; Venus = artistic; "
            "Mercury = trade/communication."
        ),
        confidence=0.84,
        verse="Reader_Vol3 p.97",
        tags=["kp_self_employment", "business", "10th_7th", "planet_nature"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS018",
        source="KP",
        chapter="Reader_Vol3",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Job Change / Promotion: A new job or promotion occurs when "
            "transiting Dasha-Bhukti lords are significators of both 10th "
            "(new role) and 11th (gains/desires fulfilled). "
            "Moon's transit over these periods is the trigger."
        ),
        confidence=0.86,
        verse="Reader_Vol3 p.108",
        tags=["kp_job_change", "promotion", "10th_11th", "moon_transit"],
        implemented=False,
    ),
    # --- Health / Medical (KPS019-022) ---
    RuleRecord(
        rule_id="KPS019",
        source="KP",
        chapter="Reader_Vol4",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Disease / Illness Onset: 6th cusp sublord connected to 6th, "
            "8th, or 12th (affliction triangle) and unconnected to 1st "
            "indicates illness. 8th = chronic/serious, 12th = hospitalization, "
            "6 = acute disease."
        ),
        confidence=0.88,
        verse="Reader_Vol4 p.15",
        tags=["kp_disease", "6th_cusp", "illness", "6_8_12_triangle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS020",
        source="KP",
        chapter="Reader_Vol4",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Recovery from Illness: 1st cusp sublord connected to 1st "
            "and 11th (recovery, gains) supports healing. 5th house also "
            "= relief from disease (12th from 6th). Dasha of 1/5/11 lords "
            "aids recovery."
        ),
        confidence=0.85,
        verse="Reader_Vol4 p.28",
        tags=["kp_recovery", "1st_cusp", "1st_11th_5th", "healing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS021",
        source="KP",
        chapter="Reader_Vol4",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Surgery: 8th cusp sublord connected to 8th and 12th with "
            "Mars or Saturn as significators indicates surgical intervention. "
            "Mars = cutting/operation; 12th = hospitalization/separation."
        ),
        confidence=0.84,
        verse="Reader_Vol4 p.39",
        tags=["kp_surgery", "8th_cusp", "mars", "hospitalization", "12th"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS022",
        source="KP",
        chapter="Reader_Vol4",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Longevity: 1st cusp sublord must be connected to 1st, 5th, "
            "or 11th (life-sustaining houses) for long life. Connection "
            "exclusively to 8th or 12th without 1/5/11 indicates short life "
            "or early health crisis."
        ),
        confidence=0.86,
        verse="Reader_Vol4 p.52",
        tags=["kp_longevity", "1st_cusp", "1_5_11", "life_sustaining"],
        implemented=False,
    ),
    # --- Education / Children / Spirituality (KPS023-026) ---
    RuleRecord(
        rule_id="KPS023",
        source="KP",
        chapter="Reader_Vol5",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Higher Education: 9th cusp sublord connected to 4, 9, and 11 "
            "indicates successful completion of higher studies. 4 = formal "
            "education foundation, 9 = higher/overseas education, 11 = achievement."
        ),
        confidence=0.87,
        verse="Reader_Vol5 p.22",
        tags=["kp_education", "9th_cusp", "4_9_11", "higher_studies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS024",
        source="KP",
        chapter="Reader_Vol5",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Children: 5th cusp sublord connected to 2, 5, or 11 indicates "
            "childbirth is promised. If sublord is connected to 1, 4 (fruitful "
            "signs) and not blocked by Saturn/12th, children are likely."
        ),
        confidence=0.87,
        verse="Reader_Vol5 p.38",
        tags=["kp_children", "5th_cusp", "2_5_11", "childbirth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS025",
        source="KP",
        chapter="Reader_Vol5",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Foreign Travel / Abroad: 3rd cusp sublord connected to 3, "
            "9, and 12 indicates short or long travel. 12th = foreign lands; "
            "9th = long journeys; 3rd = short travel and movement."
        ),
        confidence=0.86,
        verse="Reader_Vol5 p.57",
        tags=["kp_travel", "3rd_cusp", "foreign", "3_9_12", "immigration"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS026",
        source="KP",
        chapter="Reader_Vol5",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Spirituality / Moksha: 12th cusp sublord connected to 4, 8, "
            "and 12 (moksha trikona) with Jupiter as significator indicates "
            "deep spiritual inclination or renunciation. 4 = inner peace, "
            "8 = transformation, 12 = liberation."
        ),
        confidence=0.84,
        verse="Reader_Vol5 p.78",
        tags=["kp_spirituality", "12th_cusp", "moksha_trikona", "4_8_12", "jupiter"],
        implemented=False,
    ),
    # --- Horary / Prashna (KPS027-030) ---
    RuleRecord(
        rule_id="KPS027",
        source="KP",
        chapter="Reader_Vol6",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Horary: In KP horary, the querent selects a number (1-249) "
            "corresponding to a specific degree/sublord position. The sublord "
            "of that number becomes the significator for the query. "
            "This sublord system is unique to KP."
        ),
        confidence=0.90,
        verse="Reader_Vol6 p.10",
        tags=["kp_horary", "prashna", "1_249_number", "sublord_query"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS028",
        source="KP",
        chapter="Reader_Vol6",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Prashna Answer: If the sublord of the querent's chosen number "
            "is a significator of the house relevant to the question, the "
            "answer is YES. If the sublord is in 6, 8, 12 relative to that "
            "house, the answer is NO or delayed."
        ),
        confidence=0.88,
        verse="Reader_Vol6 p.22",
        tags=["kp_prashna", "yes_no", "sublord_significator", "horary_answer"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS029",
        source="KP",
        chapter="Reader_Vol6",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Lost Article / Missing Person: 2nd cusp sublord connected "
            "to 2nd and 11th indicates the missing article/person will be "
            "found. Connection to 8th or 12th alone indicates permanent loss. "
            "Moon's position and sublord provide directional clues."
        ),
        confidence=0.84,
        verse="Reader_Vol6 p.67",
        tags=["kp_lost_article", "horary", "2nd_11th", "recovery"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="KPS030",
        source="KP",
        chapter="Reader_Vol6",
        school="kp",
        category="kp_sublord",
        description=(
            "KP Election (Muhurta): For auspicious timing, ensure the moment's "
            "Ascendant sublord and Moon's sublord are both significators of "
            "houses 1, 2, 6, 10, or 11 (positive houses for the intended activity). "
            "Avoid sublords connected to 8 or 12."
        ),
        confidence=0.85,
        verse="Reader_Vol6 p.89",
        tags=["kp_muhurta", "election", "auspicious_timing", "ascendant_sublord"],
        implemented=False,
    ),
]

for _r in _KP_SUBLORD_RULES:
    KP_SUBLORD_RULES_REGISTRY.add(_r)
