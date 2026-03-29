"""
src/corpus/bphs_lords_h11_h12.py — BPHS Lord-in-Houses: H11 + H12 Lords (S221)

Encodes BPHS Ch.34-35: Effects of 11th and 12th house lords placed in each
of the 12 houses. Completes the full 12×12 lord-in-house rule set (144 rules).

Sources:
  BPHS Ch.34 — Ekadashadhipa Phala (11th lord results)
  BPHS Ch.35 — Dvadashadhipa Phala (12th lord results)

24 rules total. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H11_H12_REGISTRY = CorpusRegistry()

_RULES = [
    # ── 11th Lord in each house — BPHS Ch.34 ─────────────────────────────────
    RuleRecord(
        rule_id="H11L001",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H1: income and gains define self-image. Elder "
            "siblings' influence strong. Social networks are personally "
            "important. Wealth through own effort."
        ),
        confidence=0.85,
        verse="Ch.34 v.1-3",
        tags=["11th_lord", "1st_house", "income", "gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L002",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H2: steady income supports family wealth. Elder "
            "siblings contribute to family treasury. Financial desires "
            "fulfilled through networking."
        ),
        confidence=0.85,
        verse="Ch.34 v.4-5",
        tags=["11th_lord", "2nd_house", "steady_income", "family"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L003",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H3: gains through communication, siblings, or short "
            "journeys. Social courage. Income from writing, media, or "
            "short-distance commerce."
        ),
        confidence=0.8,
        verse="Ch.34 v.6-7",
        tags=["11th_lord", "3rd_house", "communication_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L004",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H4: gains through property, domestic goods, or "
            "mother. Home is a source of income. Community networks generate "
            "financial gains."
        ),
        confidence=0.8,
        verse="Ch.34 v.8-9",
        tags=["11th_lord", "4th_house", "property_income"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L005",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H5: gains through intelligence, speculation, "
            "children, or creative ventures. Desires fulfilled through "
            "wisdom and merit."
        ),
        confidence=0.85,
        verse="Ch.34 v.10-11",
        tags=["11th_lord", "5th_house", "speculative_gains", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L006",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H6 (dusthana): gains through service, medicine, "
            "or competitive fields. Enemies ultimately defeated. Income "
            "from struggle or litigation."
        ),
        confidence=0.75,
        verse="Ch.34 v.12-13",
        tags=["11th_lord", "6th_house", "service_gains", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L007",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H7: gains through partnerships, marriage, or "
            "foreign business. Spouse contributes to income network. "
            "Business partnerships fulfil financial desires."
        ),
        confidence=0.85,
        verse="Ch.34 v.14-15",
        tags=["11th_lord", "7th_house", "partnership_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L008",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H8 (dusthana): sudden gains through legacy, "
            "occult, or inheritance. Unexpected financial windfalls. "
            "Elder siblings may face challenges."
        ),
        confidence=0.75,
        verse="Ch.34 v.16-17",
        tags=["11th_lord", "8th_house", "sudden_gains", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L009",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H9 (trikona): gains through dharma, fortune, or "
            "father. Religious or academic networks generate income. "
            "Luck and earnings align."
        ),
        confidence=0.85,
        verse="Ch.34 v.18-19",
        tags=["11th_lord", "9th_house", "dharmic_gains", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L010",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H10 (kendra): gains through career and professional "
            "activities. Income grows with authority. Elder siblings assist "
            "career advancement."
        ),
        confidence=0.85,
        verse="Ch.34 v.20-21",
        tags=["11th_lord", "10th_house", "career_gains", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L011",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H11 (own house): exceptional gains, multiple income "
            "sources, fulfilled desires. Elder siblings are highly supportive. "
            "Social circles are expansive and beneficial."
        ),
        confidence=0.9,
        verse="Ch.34 v.22-23",
        tags=["11th_lord", "11th_house", "gains", "income", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H11L012",
        source="BPHS",
        chapter="Ch.34",
        school="parashari",
        category="bhava_phala",
        description=(
            "11th lord in H12 (dusthana): income spent on foreign items, "
            "spiritual pursuits, or charity. Gains through overseas networks. "
            "Elder siblings settle in foreign lands."
        ),
        confidence=0.75,
        verse="Ch.34 v.24-25",
        tags=["11th_lord", "12th_house", "foreign_gains", "expenditure", "dusthana"],
        implemented=False,
    ),

    # ── 12th Lord in each house — BPHS Ch.35 ─────────────────────────────────
    RuleRecord(
        rule_id="H12L001",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H1: personality marked by isolation, loss, or "
            "spiritual tendencies. Foreign residence or withdrawal likely. "
            "Expenses tied to identity and health."
        ),
        confidence=0.75,
        verse="Ch.35 v.1-3",
        tags=["12th_lord", "1st_house", "isolation", "expenses", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L002",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H2: expenditures drain family wealth. Speech "
            "carries hidden costs. Family wealth subject to losses. "
            "Income from secluded or foreign sources."
        ),
        confidence=0.75,
        verse="Ch.35 v.4-5",
        tags=["12th_lord", "2nd_house", "wealth_loss", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L003",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H3: siblings settle in foreign lands or take "
            "spiritual paths. Communication with distant places. Short "
            "journeys end in isolation or foreign experiences."
        ),
        confidence=0.75,
        verse="Ch.35 v.6-7",
        tags=["12th_lord", "3rd_house", "foreign_siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L004",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H4: domestic life disrupted by losses or expenses. "
            "Mother may settle abroad. Property in distant places. "
            "Emotional isolation at home."
        ),
        confidence=0.7,
        verse="Ch.35 v.8-9",
        tags=["12th_lord", "4th_house", "foreign_home", "domestic_loss"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L005",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H5: children may settle abroad or take spiritual "
            "paths. Intelligence turned toward liberation. Speculative "
            "losses; creativity in isolation."
        ),
        confidence=0.7,
        verse="Ch.35 v.10-11",
        tags=["12th_lord", "5th_house", "children_abroad", "spiritual_merit"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L006",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H6 (both dusthana): viparita raja yoga — losses "
            "and obstacles neutralize each other. Hidden recovery from setbacks. "
            "Service in healing or confinement settings."
        ),
        confidence=0.8,
        verse="Ch.35 v.12-13",
        tags=["12th_lord", "6th_house", "viparita_raja_yoga", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L007",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H7: spouse settles abroad or has spiritual inclination. "
            "Losses through partnerships. Bed pleasures and foreign "
            "partnerships are significant."
        ),
        confidence=0.7,
        verse="Ch.35 v.14-15",
        tags=["12th_lord", "7th_house", "foreign_spouse", "partnership_loss"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L008",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H8 (both dusthana): viparita raja yoga — strong "
            "longevity, obstacles destroy themselves. Occult mastery in "
            "isolation. Liberation through deep transformation."
        ),
        confidence=0.8,
        verse="Ch.35 v.16-17",
        tags=["12th_lord", "8th_house", "viparita_raja_yoga", "longevity", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L009",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H9: dharma leads to liberation. Father may take "
            "spiritual renunciation. Long pilgrimages to foreign holy sites. "
            "Moksha path through dharmic loss."
        ),
        confidence=0.75,
        verse="Ch.35 v.18-19",
        tags=["12th_lord", "9th_house", "liberation", "pilgrimage", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L010",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H10 (dusthana lord in kendra): career in foreign "
            "lands, spiritual institutions, or behind-the-scenes. "
            "Professional isolation or voluntary withdrawal."
        ),
        confidence=0.7,
        verse="Ch.35 v.20-21",
        tags=["12th_lord", "10th_house", "foreign_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L011",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H11: gains through foreign sources, spiritual "
            "networks, or charitable activities. Expenses through elder "
            "siblings. Income from secluded or foreign places."
        ),
        confidence=0.75,
        verse="Ch.35 v.22-23",
        tags=["12th_lord", "11th_house", "foreign_gains", "expenditure"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H12L012",
        source="BPHS",
        chapter="Ch.35",
        school="parashari",
        category="bhava_phala",
        description=(
            "12th lord in H12 (own house): spiritual orientation, tendency "
            "toward liberation. Foreign residence and solitude preferred. "
            "Expenses manageable; spiritual practices fulfilling."
        ),
        confidence=0.8,
        verse="Ch.35 v.24-25",
        tags=["12th_lord", "12th_house", "liberation", "foreign", "own_house", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H11_H12_REGISTRY.add(_r)
