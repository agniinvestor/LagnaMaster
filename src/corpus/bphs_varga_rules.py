"""
src/corpus/bphs_varga_rules.py — BPHS Varga (Divisional Chart) Rules (S237)

Encodes rules for interpreting divisional charts: D9 Navamsha (marriage/dharma),
D10 Dashamsha (career), D4 Chaturthamsha (property), D7 Saptamsha (children),
D12 Dwadashamsha (parents), and Shodashamsha principles.

Sources:
  BPHS Ch.6 — Shodashavargas (16 divisional charts)
  BPHS Ch.7 — Varga phala (divisional chart results)
  Traditional commentary

30 rules total: VAR001-VAR030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_VARGA_RULES_REGISTRY = CorpusRegistry()

_VARGA_RULES = [
    # --- Navamsha (D9) Rules (VAR001-010) ---
    RuleRecord(
        rule_id="VAR001",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Navamsha (D9): 9th harmonic of the zodiac. Each sign divided into "
            "9 parts of 3°20' each. D9 is the most important varga — "
            "considered the 'fruit' of the natal chart. "
            "Planet's D9 position modifies its D1 results."
        ),
        confidence=0.95,
        verse="Ch.6 v.1-4",
        tags=["navamsha", "d9", "most_important_varga", "dharma", "marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR002",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Vargottama: A planet in the same sign in D1 and D9. "
            "Vargottama planets gain strength equivalent to exaltation. "
            "Interpreted as a planet at its peak natural expression. "
            "Strongly benefic if already benefic; strongly malefic if malefic."
        ),
        confidence=0.95,
        verse="Ch.6 v.5-8",
        tags=["navamsha", "vargottama", "d9_same_d1", "peak_strength"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR003",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D9 Lagna Lord strength: The D9 lagna lord's position in D9 "
            "determines the quality of marriage and dharmic fulfillment. "
            "D9 lagna lord in kendra = strong marital happiness. "
            "D9 lagna lord in 6/8/12 = marriage obstacles."
        ),
        confidence=0.89,
        verse="Ch.7 v.1-4",
        tags=["navamsha", "d9_lagna", "marriage_quality", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR004",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D9 7th house: Shows the intrinsic nature of the spouse. "
            "The sign on D9 7th cusp describes spouse's appearance and nature. "
            "Planets in D9 7th indicate spouse's character. "
            "D9 7th lord's placement = partner's life circumstances."
        ),
        confidence=0.90,
        verse="Ch.7 v.5-8",
        tags=["navamsha", "d9_7th", "spouse_nature", "marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR005",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Navamsha Pushkara: Certain navamsha positions (3° Aries, 23° Taurus, etc.) "
            "are pushkara (nourishing). A planet in pushkara navamsha gives "
            "particularly benefic results even if it is a malefic planet."
        ),
        confidence=0.86,
        verse="Ch.7 v.9-11",
        tags=["navamsha", "pushkara_navamsha", "benefic_position"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR006",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D9 exaltation/debilitation modifier: If a planet is exalted in D1 "
            "but debilitated in D9, its strength is reduced by half. "
            "If debilitated in D1 but exalted in D9, neecha bhanga is confirmed "
            "and results improve significantly."
        ),
        confidence=0.90,
        verse="Ch.7 v.12-15",
        tags=["navamsha", "d9_exaltation", "d9_debilitation", "strength_modifier"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR007",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Navamsha Lagna (Navamsha Ascendant): The rising sign in D9 "
            "indicates the soul's dharmic path. AK (Atmakaraka) in D9 lagna "
            "or trikona is a powerful moksha indicator (Karakamsha lagna)."
        ),
        confidence=0.87,
        verse="Ch.7 v.16-18",
        tags=["navamsha", "d9_lagna", "dharma_path", "karakamsha", "moksha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR008",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D9 and Timing: Major life changes in marriage/spirituality occur "
            "when dasha lord is transiting over its D9 sign or when the D9 "
            "lagna sign's lord's dasha is running. D9 activates in the second half of life."
        ),
        confidence=0.83,
        verse="Ch.7 v.19-21",
        tags=["navamsha", "d9_timing", "dasha", "second_half_of_life"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR009",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Karakamsha Lagna (Atmakaraka's Navamsha sign projected to D1): "
            "The sign where AK is placed in D9 becomes the Karakamsha lagna. "
            "Planets from Karakamsha lagna determine spiritual inclinations and "
            "highest life purpose."
        ),
        confidence=0.87,
        verse="Ch.7 v.22-25",
        tags=["navamsha", "karakamsha", "atmakaraka", "spiritual_purpose"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR010",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Swamsha: When the Atmakaraka (AK) is in its own sign in D9, "
            "it creates Swamsha — powerful soul placement. Indicates a person "
            "with strong spiritual mission and self-determination."
        ),
        confidence=0.85,
        verse="Ch.7 v.26-28",
        tags=["navamsha", "swamsha", "atmakaraka_own_sign", "spiritual_mission"],
        implemented=False,
    ),
    # --- Dashamsha (D10) Rules (VAR011-018) ---
    RuleRecord(
        rule_id="VAR011",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Dashamsha (D10): 10th harmonic. Each sign divided into 10 parts of 3° each. "
            "Primary varga for career, public achievement, and social status. "
            "D10 is the definitive chart for professional analysis."
        ),
        confidence=0.93,
        verse="Ch.6 v.15-18",
        tags=["dashamsha", "d10", "career", "profession", "social_status"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR012",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 Lagna Lord: The D10 lagna lord's position and strength "
            "determine career success. D10 lagna lord in kendra or trikona "
            "of D10 = professional success. In 8th or 12th = career obstacles."
        ),
        confidence=0.90,
        verse="Ch.7 v.29-32",
        tags=["dashamsha", "d10_lagna", "career_success", "lagna_lord"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR013",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 Sun position: Sun in D10 kendra or trikona gives government service, "
            "authority roles, or public recognition. Sun in D10 1st = "
            "leader in field; Sun in D10 10th = peak career authority."
        ),
        confidence=0.87,
        verse="Ch.7 v.33-35",
        tags=["dashamsha", "d10_sun", "government", "authority", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR014",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 Saturn: Saturn in D10 kendra indicates disciplined, long-term career "
            "achievement. Saturn in D10 10th (its strongest position) = "
            "successful career through hard work, especially after age 36."
        ),
        confidence=0.86,
        verse="Ch.7 v.36-38",
        tags=["dashamsha", "d10_saturn", "career_discipline", "long_term"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR015",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 10th House: The D10 10th lord and planets in D10 10th house "
            "describe the nature of the career. Mercury there = communication/trade; "
            "Mars = technical/military; Jupiter = teaching/advisory."
        ),
        confidence=0.87,
        verse="Ch.7 v.39-41",
        tags=["dashamsha", "d10_10th_house", "career_nature", "planet_career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR016",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 Timing: Career peaks occur when the D10 lagna lord or D10 "
            "10th lord's dasha is running AND they transit their D10 sign. "
            "Mid-career shifts happen at Saturn's D10 house transits."
        ),
        confidence=0.83,
        verse="Ch.7 v.42-44",
        tags=["dashamsha", "d10_timing", "career_peak", "dasha"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR017",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "D10 Panchamsha (5th from D10 lagna): In Dashamsha, the 5th house "
            "shows the authority/recognition one receives. Planets in D10 5th "
            "or its lord's strength determines prestige in the field."
        ),
        confidence=0.82,
        verse="Ch.7 v.45-46",
        tags=["dashamsha", "d10_5th", "recognition", "prestige"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR018",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Vargottama in D10: A planet vargottama in D10 (same sign in D1 and D10) "
            "indicates a natural affinity for career matters related to that planet. "
            "Strong career placement confirmed when D1 and D10 agree on a planet's strength."
        ),
        confidence=0.86,
        verse="Ch.7 v.47-48",
        tags=["dashamsha", "vargottama_d10", "career_affinity", "d1_d10_agreement"],
        implemented=False,
    ),
    # --- Other Key Vargas (VAR019-030) ---
    RuleRecord(
        rule_id="VAR019",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Saptamsha (D7): 7th harmonic for children and creative output. "
            "D7 5th house and its lord indicate the number and nature of children. "
            "Benefics in D7 5th = healthy children; malefics = fewer or health issues."
        ),
        confidence=0.88,
        verse="Ch.6 v.19-22",
        tags=["saptamsha", "d7", "children", "creative_output"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR020",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Dwadashamsha (D12): 12th harmonic for parents. "
            "D12 lagna = overall parental circumstances. "
            "D12 9th = father's wellbeing; D12 4th = mother's wellbeing. "
            "Malefics in D12 lagna indicate early parental separation or illness."
        ),
        confidence=0.86,
        verse="Ch.6 v.23-26",
        tags=["dwadashamsha", "d12", "parents", "father", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR021",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Chaturthamsha (D4): 4th harmonic for property and fixed assets. "
            "D4 4th house and its lord indicate property ownership. "
            "Strong D4 = real estate; benefics in D4 kendra = multiple properties."
        ),
        confidence=0.85,
        verse="Ch.6 v.27-30",
        tags=["chaturthamsha", "d4", "property", "real_estate", "fixed_assets"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR022",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Trimshamsha (D30): 30th harmonic for misfortunes and evil. "
            "Planets in D30 indicate areas of difficulty, vice, and disease. "
            "D30 is specifically read for female charts to assess marital harmony and health."
        ),
        confidence=0.84,
        verse="Ch.6 v.31-34",
        tags=["trimshamsha", "d30", "misfortune", "disease", "female_chart"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR023",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Shodashamsha (D16): 16th harmonic for vehicles, comforts, and conveyances. "
            "D16 4th house rules vehicles. Strong Venus and Moon in D16 "
            "indicate luxury conveyances and material comforts."
        ),
        confidence=0.83,
        verse="Ch.6 v.35-37",
        tags=["shodashamsha", "d16", "vehicles", "comforts", "conveyance"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR024",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Vimshamsha (D20): 20th harmonic for spiritual practices and worship. "
            "D20 12th house shows spiritual liberation path. "
            "Strong Jupiter and Ketu in D20 indicate spiritual attainment."
        ),
        confidence=0.83,
        verse="Ch.6 v.38-40",
        tags=["vimshamsha", "d20", "spiritual", "worship", "liberation_path"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR025",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Chaturvimshamsha (D24): 24th harmonic for higher education and learning. "
            "D24 4th and 5th houses govern academic success. "
            "Strong Mercury and Jupiter in D24 = academic excellence."
        ),
        confidence=0.82,
        verse="Ch.6 v.41-43",
        tags=["chaturvimshamsha", "d24", "higher_education", "learning", "academic"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR026",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Shastiamsha (D60): 60th harmonic — most granular varga. "
            "Each D60 position has specific name (Ghora, Rakshasa, Deva, etc.) "
            "indicating the fundamental karmic quality of the planet's energy."
        ),
        confidence=0.82,
        verse="Ch.6 v.44-47",
        tags=["shastiamsha", "d60", "karmic_quality", "granular_varga"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR027",
        source="BPHS",
        chapter="Ch.6",
        school="parashari",
        category="varga",
        description=(
            "Panchamsha (D5): 5th harmonic for power, spiritual merit, and fame. "
            "D5 1st house shows the person's fame potential. "
            "Strong Sun in D5 kendra = public recognition; Jupiter = spiritual fame."
        ),
        confidence=0.81,
        verse="Ch.6 v.48-50",
        tags=["panchamsha", "d5", "power", "fame", "spiritual_merit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR028",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Bhava Arudha in vargas: The Arudha (pada) principle applies to "
            "divisional charts. In D10, the D10 Arudha Lagna shows how the "
            "person's career is perceived by the world vs. actual career reality."
        ),
        confidence=0.80,
        verse="Ch.7 v.49-51",
        tags=["varga", "arudha_in_varga", "d10_arudha", "perception_vs_reality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR029",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Panchavargas Strength (Pancha Vargeeya Bala): Aggregate of D1, D2, D9, "
            "D3, D12 strengths. A planet strong in all 5 vargas is maximally powerful. "
            "4/5 strong = good; 3/5 = moderate; 2/5 = weak."
        ),
        confidence=0.85,
        verse="Ch.7 v.52-55",
        tags=["varga", "panchamsha_bala", "aggregate_strength", "five_vargas"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="VAR030",
        source="BPHS",
        chapter="Ch.7",
        school="parashari",
        category="varga",
        description=(
            "Saptavargaja Bala (7-varga strength): D1+D2+D3+D7+D9+D12+D30. "
            "Used in classical Shadbala calculations. A planet in its own "
            "or exaltation sign in most vargas has high saptavargaja bala."
        ),
        confidence=0.85,
        verse="Ch.7 v.56-58",
        tags=["varga", "saptavargaja_bala", "7_varga_strength", "shadbala"],
        implemented=False,
    ),
]

for _r in _VARGA_RULES:
    BPHS_VARGA_RULES_REGISTRY.add(_r)
