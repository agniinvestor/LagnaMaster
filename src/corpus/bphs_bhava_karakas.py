"""
src/corpus/bphs_bhava_karakas.py — BPHS Bhava Karakas and House Significations (S236)

Encodes Chara Karakas (Jaimini), Sthira Karakas (fixed house significators),
and Naisargika Karakas (natural significators of each house).

Sources:
  BPHS Ch.32 — Karaka Adhyaya (planetary karakas)
  BPHS Ch.10-11 — House significations (bhava karakas)
  Jaimini Sutras — Chara Karaka system

30 rules total: BHK001-BHK030.
All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_BHAVA_KARAKAS_REGISTRY = CorpusRegistry()

_BHAVA_KARAKA_RULES = [
    # --- Naisargika (Natural) Karakas for 12 Houses (BHK001-012) ---
    RuleRecord(
        rule_id="BHK001",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "1st House Naisargika Karaka: Sun (self, vitality, soul, father). "
            "Sun signifies the atma (soul), physical constitution, and life force. "
            "Lagna and Sun together describe the native's fundamental character."
        ),
        confidence=0.95,
        verse="Ch.10 v.1-3",
        tags=["bhava_karaka", "1st_house", "sun", "atma", "vitality", "self"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK002",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "2nd House Naisargika Karaka: Jupiter (wealth, family, speech). "
            "Jupiter significates accumulated wealth, family traditions, "
            "and eloquent speech. Venus also co-significates 2nd house wealth."
        ),
        confidence=0.93,
        verse="Ch.10 v.4-6",
        tags=["bhava_karaka", "2nd_house", "jupiter", "wealth", "family", "speech"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK003",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "3rd House Naisargika Karaka: Mars (courage, siblings, communication). "
            "Mars significates younger siblings, courage, effort, short journeys. "
            "Mercury co-significates communication and skill aspects of 3rd house."
        ),
        confidence=0.92,
        verse="Ch.10 v.7-9",
        tags=["bhava_karaka", "3rd_house", "mars", "courage", "siblings", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK004",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "4th House Naisargika Karaka: Moon (mother, home, happiness). "
            "Moon significates mother, homeland, mental peace, vehicles. "
            "Mercury also contributes to education themes of 4th house."
        ),
        confidence=0.94,
        verse="Ch.10 v.10-12",
        tags=["bhava_karaka", "4th_house", "moon", "mother", "home", "happiness"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK005",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "5th House Naisargika Karaka: Jupiter (children, intellect, past merit). "
            "Jupiter is strongest significator for children, intelligence, "
            "mantra siddhi, and purva punya (past life merit)."
        ),
        confidence=0.94,
        verse="Ch.10 v.13-15",
        tags=["bhava_karaka", "5th_house", "jupiter", "children", "intellect", "purva_punya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK006",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "6th House Naisargika Karaka: Mars/Saturn (enemies, disease, service). "
            "Mars rules enemies and conflict; Saturn rules chronic disease and "
            "subordinate workers. Rahu also co-significates the 6th house."
        ),
        confidence=0.90,
        verse="Ch.10 v.16-18",
        tags=["bhava_karaka", "6th_house", "mars", "saturn", "enemies", "disease", "service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK007",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "7th House Naisargika Karaka: Venus (spouse, partnerships, desires). "
            "Venus is the primary karaka for marriage and business partnerships. "
            "Jupiter also co-significates marriage (for female charts)."
        ),
        confidence=0.95,
        verse="Ch.10 v.19-21",
        tags=["bhava_karaka", "7th_house", "venus", "spouse", "partnership", "desire"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK008",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "8th House Naisargika Karaka: Saturn (longevity, transformation, hidden). "
            "Saturn rules the length of life, chronic matters, and what is hidden. "
            "Rahu co-significates sudden events and obstacles of the 8th house."
        ),
        confidence=0.91,
        verse="Ch.10 v.22-24",
        tags=["bhava_karaka", "8th_house", "saturn", "longevity", "transformation", "hidden"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK009",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "9th House Naisargika Karaka: Jupiter/Sun (dharma, father, fortune). "
            "Jupiter rules dharma, guru, higher wisdom. Sun rules father and "
            "divine grace. Both together govern 9th house significations."
        ),
        confidence=0.94,
        verse="Ch.10 v.25-27",
        tags=["bhava_karaka", "9th_house", "jupiter", "sun", "dharma", "father", "fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK010",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "10th House Naisargika Karaka: Sun/Mercury/Jupiter/Saturn (career). "
            "Sun = authority; Mercury = trade/business; Jupiter = consulting/teaching; "
            "Saturn = labor/service. Multiple karakas for diverse 10th house matters."
        ),
        confidence=0.93,
        verse="Ch.10 v.28-30",
        tags=["bhava_karaka", "10th_house", "sun", "mercury", "jupiter", "saturn", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK011",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "11th House Naisargika Karaka: Jupiter (gains, elder siblings, desires). "
            "Jupiter significates elder siblings, profits, fulfillment of desires, "
            "and social circles. Rahu also co-significates 11th house gains."
        ),
        confidence=0.91,
        verse="Ch.10 v.31-33",
        tags=["bhava_karaka", "11th_house", "jupiter", "gains", "elder_siblings", "desires"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK012",
        source="BPHS",
        chapter="Ch.10",
        school="parashari",
        category="bhava_karaka",
        description=(
            "12th House Naisargika Karaka: Saturn/Ketu (loss, liberation, foreign). "
            "Saturn rules expenses, loss, and confinement. Ketu rules moksha "
            "and spiritual liberation. Both govern 12th house matters."
        ),
        confidence=0.91,
        verse="Ch.10 v.34-36",
        tags=["bhava_karaka", "12th_house", "saturn", "ketu", "loss", "liberation", "foreign"],
        implemented=False,
    ),
    # --- Jaimini Chara Karakas (BHK013-020) ---
    RuleRecord(
        rule_id="BHK013",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Jaimini Chara Karaka System: 7 or 8 planets assigned karaka roles "
            "based on degree advancement in their sign. Highest degree = "
            "Atmakaraka (soul significator). System changes each chart."
        ),
        confidence=0.90,
        verse="Ch.32 v.1-4",
        tags=["jaimini", "chara_karaka", "atmakaraka", "soul", "degree_based"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK014",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Atmakaraka (AK): Planet with highest degree in its sign (0-30°). "
            "Represents the soul's primary lesson and desire. "
            "AK in navamsha (D9) shows the innermost nature and spiritual path."
        ),
        confidence=0.92,
        verse="Ch.32 v.5-8",
        tags=["jaimini", "atmakaraka", "soul_lesson", "navamsha", "highest_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK015",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Amatyakaraka (AmK): Planet with 2nd highest degree. "
            "Represents career, profession, and counsel. "
            "The AmK nakshatra lord and sign indicate the primary vocation."
        ),
        confidence=0.88,
        verse="Ch.32 v.9-11",
        tags=["jaimini", "amatyakaraka", "career", "profession", "2nd_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK016",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Bhatrikaraka (BK): Planet with 3rd highest degree. "
            "Represents siblings, courage, and co-workers. "
            "BK indicates the brother/sister dynamic and Martian themes."
        ),
        confidence=0.85,
        verse="Ch.32 v.12-13",
        tags=["jaimini", "bhatrikaraka", "siblings", "3rd_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK017",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Matrikaraka (MK): Planet with 4th highest degree. "
            "Represents mother, home, and emotional security. "
            "MK and 4th house together describe mother and homeland."
        ),
        confidence=0.85,
        verse="Ch.32 v.14-15",
        tags=["jaimini", "matrikaraka", "mother", "home", "4th_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK018",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Putrakaraka (PK): Planet with 5th highest degree. "
            "Represents children, intelligence, and creativity. "
            "PK and 5th house together indicate childbirth prospects."
        ),
        confidence=0.85,
        verse="Ch.32 v.16-17",
        tags=["jaimini", "putrakaraka", "children", "creativity", "5th_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK019",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Gnatikaraka (GK): Planet with 6th highest degree. "
            "Represents enemies, obstacles, disease, and competition. "
            "GK period (dasha) often brings conflict and challenges."
        ),
        confidence=0.84,
        verse="Ch.32 v.18-19",
        tags=["jaimini", "gnatikaraka", "enemies", "obstacles", "6th_degree"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK020",
        source="BPHS",
        chapter="Ch.32",
        school="jaimini",
        category="bhava_karaka",
        description=(
            "Darakaraka (DK): Planet with lowest degree (7th highest in 7-karaka system). "
            "Represents spouse and intimate partnerships. "
            "DK navamsha sign indicates the nature of the spouse."
        ),
        confidence=0.88,
        verse="Ch.32 v.20-22",
        tags=["jaimini", "darakaraka", "spouse", "partnership", "lowest_degree"],
        implemented=False,
    ),
    # --- Sthira Karakas and Special Karaka Rules (BHK021-030) ---
    RuleRecord(
        rule_id="BHK021",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Karaka-Bhava Nashta (karaka destroying its own house): "
            "When the natural significator of a house is placed in that same house, "
            "it tends to harm or complicate that house's results. "
            "E.g., Jupiter in 5th may cause fewer children; Venus in 7th can harm marriage."
        ),
        confidence=0.87,
        verse="Ch.11 v.1-5",
        tags=["bhava_karaka", "karaka_bhava_nashta", "karaka_same_house", "important_principle"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK022",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Father Karaka: Sun is naisargika karaka for father; "
            "in Jaimini, the 9th lord and 9th house are also used. "
            "Affliction to both Sun and 9th house simultaneously indicates "
            "father's difficulties or early separation."
        ),
        confidence=0.88,
        verse="Ch.11 v.6-8",
        tags=["bhava_karaka", "father", "sun", "9th_house", "dual_significator"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK023",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Mother Karaka: Moon is naisargika karaka for mother; "
            "4th lord and 4th house also govern mother. "
            "Both Moon and 4th house must be afflicted for serious mother-related difficulties."
        ),
        confidence=0.88,
        verse="Ch.11 v.9-11",
        tags=["bhava_karaka", "mother", "moon", "4th_house", "dual_significator"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK024",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Spouse Karaka by Gender: For male charts, Venus is primary spouse karaka; "
            "Jupiter is secondary. For female charts, Jupiter is primary; "
            "Mars is secondary spouse karaka. Both must be examined."
        ),
        confidence=0.90,
        verse="Ch.11 v.12-14",
        tags=["bhava_karaka", "spouse", "venus", "jupiter", "mars", "gender_specific"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK025",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Putrakarak (Children) dual assessment: Jupiter as naisargika karaka "
            "AND 5th house lord together determine childbirth. If both are strong, "
            "children are indicated. If both afflicted, childlessness or fewer children."
        ),
        confidence=0.88,
        verse="Ch.11 v.15-17",
        tags=["bhava_karaka", "children", "jupiter", "5th_lord", "dual_assessment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK026",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Sarvatobhadra Chakra — strong Karakas: When a natural house karaka "
            "is placed in a kendra (1,4,7,10) or trikona (1,5,9) from its "
            "own bhava, it strengthens that house's results significantly."
        ),
        confidence=0.84,
        verse="Ch.11 v.18-20",
        tags=["bhava_karaka", "karaka_kendra", "karaka_trikona", "strengthening"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK027",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Lagna Lord as Karaka override: The lagna lord's strength can override "
            "a weak karaka. If lagna lord is in kendra or trikona and the "
            "relevant bhava lord is also strong, the karaka's weakness is mitigated."
        ),
        confidence=0.83,
        verse="Ch.11 v.21-23",
        tags=["bhava_karaka", "lagna_lord", "karaka_override", "mitigation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK028",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Karaka Dasha Activation: The natural significator's dasha period "
            "activates all houses it karakas. Sun dasha activates 1st, 9th; "
            "Venus dasha activates 7th, 2nd; Jupiter dasha activates 2nd, 5th, 9th, 11th."
        ),
        confidence=0.86,
        verse="Ch.11 v.24-26",
        tags=["bhava_karaka", "dasha_activation", "karaka_dasha", "timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK029",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Upachaya houses (3, 6, 10, 11) benefit from malefic planets and "
            "their karakas. Mars in 3rd (its karaka house) becomes beneficial. "
            "Saturn in 10th (career karaka) produces strong career results despite malefic nature."
        ),
        confidence=0.86,
        verse="Ch.11 v.27-29",
        tags=["bhava_karaka", "upachaya", "malefic_benefit", "3_6_10_11"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="BHK030",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="bhava_karaka",
        description=(
            "Shadvargas Karaka Strength: A karaka is most powerful when it is "
            "vargottama (same sign in D1 and D9), exalted in navamsha, or "
            "occupies its own sign in Drekkana (D3). Karaka dignity in divisional "
            "charts confirms its bhava results."
        ),
        confidence=0.84,
        verse="Ch.11 v.30-32",
        tags=["bhava_karaka", "vargottama", "navamsha_dignity", "divisional_strength"],
        implemented=False,
    ),
]

for _r in _BHAVA_KARAKA_RULES:
    BPHS_BHAVA_KARAKAS_REGISTRY.add(_r)
