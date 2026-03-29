"""
src/corpus/bphs_lords_h3_h4.py — BPHS Lord-in-Houses: H3 + H4 Lords (S217)

Encodes BPHS Ch.26-27: Effects of 3rd and 4th house lords placed in each
of the 12 houses.

Sources:
  BPHS Ch.26 — Tritiyadhipa Phala (3rd lord results)
  BPHS Ch.27 — Chaturthadhipa Phala (4th lord results)

24 rules total. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H3_H4_REGISTRY = CorpusRegistry()

_RULES = [
    # ── 3rd Lord in each house — BPHS Ch.26 ──────────────────────────────────
    RuleRecord(
        rule_id="H3L001",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H1: courageous, bold, valor in self-expression. "
            "Good communication skills; writing or media talent. Siblings "
            "benefit the native's personality and goals."
        ),
        confidence=0.85,
        verse="Ch.26 v.1-3",
        tags=["3rd_lord", "1st_house", "courage", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L002",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H2: income through communication, siblings, or writing. "
            "Speech is a wealth-generating tool. Family wealth supported by "
            "short-distance commerce."
        ),
        confidence=0.8,
        verse="Ch.26 v.4-5",
        tags=["3rd_lord", "2nd_house", "communication_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L003",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H3 (own house): strong siblings, courage, and valor. "
            "Writing, arts, or performing talent is marked. Short travels are "
            "frequent and beneficial."
        ),
        confidence=0.9,
        verse="Ch.26 v.6-7",
        tags=["3rd_lord", "3rd_house", "siblings", "courage", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L004",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H4: domestic courage, real estate transactions, "
            "siblings support domestic life. Vehicles gained through "
            "effort. Mother and siblings have positive connection."
        ),
        confidence=0.8,
        verse="Ch.26 v.8-9",
        tags=["3rd_lord", "4th_house", "home", "siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L005",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H5: courage in creative ventures, children are bold and "
            "communicative. Speculation or short-term trading succeeds. "
            "Intelligence expressed through communication."
        ),
        confidence=0.8,
        verse="Ch.26 v.10-11",
        tags=["3rd_lord", "5th_house", "creativity", "children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L006",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H6 (dusthana): siblings cause enmity or difficulties. "
            "Courage is tested through disease or litigation. Short journeys "
            "bring complications."
        ),
        confidence=0.8,
        verse="Ch.26 v.12-13",
        tags=["3rd_lord", "6th_house", "siblings_enmity", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L007",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H7: courage expressed through partnerships. Siblings "
            "connected to spouse's life. Communication skills benefit "
            "marriage and business."
        ),
        confidence=0.8,
        verse="Ch.26 v.14-15",
        tags=["3rd_lord", "7th_house", "partnership", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L008",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H8 (dusthana): siblings face health challenges or "
            "short life. Courage faces hidden obstacles. Occult writing "
            "or research is possible."
        ),
        confidence=0.75,
        verse="Ch.26 v.16-17",
        tags=["3rd_lord", "8th_house", "siblings_health", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L009",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H9 (trikona): dharmic courage, religious writings or "
            "pilgrimages. Long-distance travel for philosophical pursuits. "
            "Siblings support dharmic life."
        ),
        confidence=0.85,
        verse="Ch.26 v.18-19",
        tags=["3rd_lord", "9th_house", "dharma", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L010",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H10 (kendra): career through communication, media, or "
            "technology. Bold professional ambition. Siblings assist career "
            "advancement."
        ),
        confidence=0.85,
        verse="Ch.26 v.20-21",
        tags=["3rd_lord", "10th_house", "media_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L011",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H11: gains through communication networks, siblings, "
            "or short-term commerce. Fulfillment of desires through courage "
            "and initiative."
        ),
        confidence=0.85,
        verse="Ch.26 v.22-23",
        tags=["3rd_lord", "11th_house", "gains", "siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H3L012",
        source="BPHS",
        chapter="Ch.26",
        school="parashari",
        category="bhava_phala",
        description=(
            "3rd lord in H12 (dusthana): siblings settle in foreign lands or "
            "face isolation. Short travels end in distant or spiritual places. "
            "Courage used for liberation."
        ),
        confidence=0.75,
        verse="Ch.26 v.24-25",
        tags=["3rd_lord", "12th_house", "foreign", "dusthana"],
        implemented=False,
    ),

    # ── 4th Lord in each house — BPHS Ch.27 ──────────────────────────────────
    RuleRecord(
        rule_id="H4L001",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H1: domestic comfort apparent in personality, "
            "motherly or nurturing nature. Real estate interests from youth. "
            "Emotional happiness tied to self-image."
        ),
        confidence=0.85,
        verse="Ch.27 v.1-3",
        tags=["4th_lord", "1st_house", "home", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L002",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H2: wealth through property, ancestral estate, or "
            "mother. Family treasury includes real estate assets. Domestic "
            "comforts generate financial security."
        ),
        confidence=0.85,
        verse="Ch.27 v.4-5",
        tags=["4th_lord", "2nd_house", "property_wealth", "family"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L003",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H3: comfort obtained through effort and courage. "
            "Siblings assist domestic life. Short journeys relate to real "
            "estate or family business."
        ),
        confidence=0.8,
        verse="Ch.27 v.6-7",
        tags=["4th_lord", "3rd_house", "effort", "siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L004",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H4 (own house): exceptional domestic happiness, "
            "comfortable home, strong mother-relationship. Vehicles and "
            "property naturally accumulate."
        ),
        confidence=0.9,
        verse="Ch.27 v.8-9",
        tags=["4th_lord", "4th_house", "home", "mother", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L005",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H5: comfort through children and creative activities. "
            "Mother's merit supports the native. Emotional happiness linked "
            "to intelligence and speculation."
        ),
        confidence=0.85,
        verse="Ch.27 v.10-11",
        tags=["4th_lord", "5th_house", "children", "creativity", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L006",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H6 (dusthana): domestic unhappiness, tension with "
            "mother, property disputes. Vehicles prone to damage. Emotional "
            "comfort disrupted by disease or enemies."
        ),
        confidence=0.8,
        verse="Ch.27 v.12-13",
        tags=["4th_lord", "6th_house", "domestic_issues", "mother", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L007",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H7: domestic happiness through marriage. Spouse "
            "contributes to home comfort. Real estate acquired in partnerships "
            "or through spouse's wealth."
        ),
        confidence=0.85,
        verse="Ch.27 v.14-15",
        tags=["4th_lord", "7th_house", "spouse", "home"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L008",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H8 (dusthana): mother's health suffers, domestic "
            "instability, property subject to loss or hidden encumbrances. "
            "Emotional transformation through crisis."
        ),
        confidence=0.75,
        verse="Ch.27 v.16-17",
        tags=["4th_lord", "8th_house", "mother_health", "property_loss", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L009",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H9 (trikona): domestic happiness through dharma and "
            "fortune. Mother is religious and beneficial. Long journeys for "
            "pilgrimage or education blessed."
        ),
        confidence=0.85,
        verse="Ch.27 v.18-19",
        tags=["4th_lord", "9th_house", "fortune", "mother", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L010",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H10 (kendra): career in real estate, domestic goods, "
            "agriculture, or hospitality. Mother's influence on career. "
            "Authority gained through nurturing qualities."
        ),
        confidence=0.85,
        verse="Ch.27 v.20-21",
        tags=["4th_lord", "10th_house", "career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L011",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H11: gains through property, domestic goods, or mother. "
            "Social network includes domestic or agrarian connections. "
            "Comfort desires are fulfilled."
        ),
        confidence=0.85,
        verse="Ch.27 v.22-23",
        tags=["4th_lord", "11th_house", "property_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H4L012",
        source="BPHS",
        chapter="Ch.27",
        school="parashari",
        category="bhava_phala",
        description=(
            "4th lord in H12 (dusthana): domestic life connected to foreign "
            "residence. Mother settles abroad or in ashram. Property in "
            "distant places; comfort through solitude."
        ),
        confidence=0.75,
        verse="Ch.27 v.24-25",
        tags=["4th_lord", "12th_house", "foreign_home", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H3_H4_REGISTRY.add(_r)
