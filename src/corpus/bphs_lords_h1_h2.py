"""
src/corpus/bphs_lords_h1_h2.py — BPHS Lord-in-Houses: H1 + H2 Lords (S216)

Encodes BPHS Ch.24-25: Effects of lagna lord and 2nd lord placed in each
of the 12 houses. These are classical house-lord position rules forming
the backbone of Parashari house analysis.

Sources:
  BPHS Ch.24 — Lagnadhi-pa Phala (Lagna lord results)
  BPHS Ch.25 — Dvitiyadhipa Phala (2nd lord results)
  PVRNR commentary edition

24 rules total (12 per lord). All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H1_H2_REGISTRY = CorpusRegistry()

_RULES = [
    # ── Lagna Lord (H1 Lord) in each house — BPHS Ch.24 ─────────────────────
    RuleRecord(
        rule_id="H1L001",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H1: native has strong constitution, healthy body, "
            "confident disposition, self-reliant nature. Physical appearance is "
            "notable. General auspiciousness for the self and body."
        ),
        confidence=0.9,
        verse="Ch.24 v.1-3",
        tags=["lagna_lord", "1st_house", "health", "body"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L002",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H2: wealthy family background, good speech, financial "
            "support from family. Early accumulation of wealth. Eloquence and "
            "learning are favored."
        ),
        confidence=0.85,
        verse="Ch.24 v.4-5",
        tags=["lagna_lord", "2nd_house", "wealth", "speech"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L003",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H3: courageous and bold, strong siblings, valor in "
            "undertakings. Talent in writing, communication, or performing arts. "
            "Short journeys are beneficial."
        ),
        confidence=0.85,
        verse="Ch.24 v.6-7",
        tags=["lagna_lord", "3rd_house", "siblings", "courage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L004",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H4: domestic happiness, comfort of home and vehicles, "
            "good relation with mother, land and property acquisition. Native "
            "gains happiness from ancestral wealth."
        ),
        confidence=0.9,
        verse="Ch.24 v.8-9",
        tags=["lagna_lord", "4th_house", "home", "mother", "property"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L005",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H5: intelligent and learned, good memory, fortunate "
            "children. Past-life merit actively supports current life. Creative "
            "and speculative ventures succeed."
        ),
        confidence=0.9,
        verse="Ch.24 v.10-11",
        tags=["lagna_lord", "5th_house", "children", "intelligence", "purva_punya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L006",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H6 (dusthana): enemies trouble the native, prone to "
            "disease and debt. Health issues related to digestive or inflammatory "
            "conditions. Competitions and litigation prevalent."
        ),
        confidence=0.85,
        verse="Ch.24 v.12-13",
        tags=["lagna_lord", "6th_house", "enemies", "disease", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L007",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H7: strong partnership and marriage focus. Life "
            "satisfaction comes through relationships. Tendency to travel abroad "
            "or settle in foreign lands. Business acumen."
        ),
        confidence=0.9,
        verse="Ch.24 v.14-15",
        tags=["lagna_lord", "7th_house", "spouse", "partnership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L008",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H8 (dusthana): longevity concerns, chronic ailments, "
            "hidden troubles. Interest in occult, mysticism, or research. "
            "Transformation through suffering; legacy through crisis."
        ),
        confidence=0.85,
        verse="Ch.24 v.16-17",
        tags=["lagna_lord", "8th_house", "longevity", "occult", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L009",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H9 (trikona): fortunate, religious and dharmic nature, "
            "father's support and welfare. Higher learning, philosophy, and "
            "foreign pilgrimages. Exceptional good luck."
        ),
        confidence=0.9,
        verse="Ch.24 v.18-19",
        tags=["lagna_lord", "9th_house", "fortune", "dharma", "father", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L010",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H10 (kendra): career success and authority. Public "
            "prominence, status, and recognition. Strong professional drive. "
            "Actions in the world are effective and recognized."
        ),
        confidence=0.9,
        verse="Ch.24 v.20-21",
        tags=["lagna_lord", "10th_house", "career", "status", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L011",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H11: social gains, strong income, elder sibling "
            "support. Achievements through networks. Income from multiple "
            "sources. Desires are fulfilled over time."
        ),
        confidence=0.85,
        verse="Ch.24 v.22-23",
        tags=["lagna_lord", "11th_house", "gains", "income", "elder_sibling"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H1L012",
        source="BPHS",
        chapter="Ch.24",
        school="parashari",
        category="bhava_phala",
        description=(
            "Lagna lord in H12 (dusthana): tendency toward foreign residence or "
            "voluntary retreat. Spiritual liberation as life theme. Excessive "
            "expenditure; sleep and solitude favored."
        ),
        confidence=0.85,
        verse="Ch.24 v.24-25",
        tags=["lagna_lord", "12th_house", "foreign", "liberation", "dusthana"],
        implemented=False,
    ),

    # ── 2nd Lord (H2 Lord) in each house — BPHS Ch.25 ────────────────────────
    RuleRecord(
        rule_id="H2L001",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H1: self-earned wealth, financial identity tied to "
            "personal effort. Eloquence and speaking ability generate income. "
            "Face and features are attractive."
        ),
        confidence=0.85,
        verse="Ch.25 v.1-3",
        tags=["2nd_lord", "1st_house", "self_earned", "speech"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L002",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H2 (own house): strong treasury, accumulated wealth "
            "stays in family. Financial stability and preservation. Family "
            "relationships support wealth building."
        ),
        confidence=0.9,
        verse="Ch.25 v.4-5",
        tags=["2nd_lord", "2nd_house", "wealth", "family_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L003",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H3: wealth through siblings, communication, writing, "
            "or media. Income from short-distance trades or commerce. "
            "Financial courage and self-initiative."
        ),
        confidence=0.8,
        verse="Ch.25 v.6-7",
        tags=["2nd_lord", "3rd_house", "siblings_wealth", "commerce"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L004",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H4: property wealth, ancestral inheritance. Wealth "
            "through real estate, agriculture, or mother's line. Comfort and "
            "security from land and domestic investments."
        ),
        confidence=0.85,
        verse="Ch.25 v.8-9",
        tags=["2nd_lord", "4th_house", "property", "inheritance", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L005",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H5: wealth from creativity, children, speculation, and "
            "investments. Financial intelligence and mantra-based success. "
            "Treasury grows through wisdom and merit."
        ),
        confidence=0.85,
        verse="Ch.25 v.10-11",
        tags=["2nd_lord", "5th_house", "speculation", "creativity", "purva_punya"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L006",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H6 (dusthana): wealth through service, competitive "
            "professions, or medicine. Enemies and debts drain financial reserves. "
            "Inconsistent income; wealth after struggle."
        ),
        confidence=0.8,
        verse="Ch.25 v.12-13",
        tags=["2nd_lord", "6th_house", "service_income", "debt", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L007",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H7: wealth through marriage, business partnerships, or "
            "trade. Spouse contributes materially. Joint ventures and foreign "
            "commerce are financial sources."
        ),
        confidence=0.85,
        verse="Ch.25 v.14-15",
        tags=["2nd_lord", "7th_house", "marriage_wealth", "partnership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L008",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H8 (dusthana): inherited wealth, legacies, insurance, "
            "occult business. Sudden gains and losses. Family wealth subject to "
            "disruption; longevity of wealth is uncertain."
        ),
        confidence=0.8,
        verse="Ch.25 v.16-17",
        tags=["2nd_lord", "8th_house", "legacy", "inheritance", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L009",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H9 (trikona): wealth through dharma, luck, long travels, "
            "and father's support. Religious institutions or higher learning "
            "bring financial opportunities."
        ),
        confidence=0.85,
        verse="Ch.25 v.18-19",
        tags=["2nd_lord", "9th_house", "dharmic_wealth", "father", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L010",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H10 (kendra): professional income and career-based "
            "wealth. Authority positions generate financial security. Government "
            "or corporate career is the primary wealth source."
        ),
        confidence=0.9,
        verse="Ch.25 v.20-21",
        tags=["2nd_lord", "10th_house", "career_wealth", "professional", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L011",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H11: steady income from networks, organizations, elder "
            "siblings. Multiple income streams. Financial desires are fulfilled "
            "gradually through social connections."
        ),
        confidence=0.85,
        verse="Ch.25 v.22-23",
        tags=["2nd_lord", "11th_house", "steady_income", "gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H2L012",
        source="BPHS",
        chapter="Ch.25",
        school="parashari",
        category="bhava_phala",
        description=(
            "2nd lord in H12 (dusthana): expenditure exceeds income, wealth "
            "spent on foreign goods or spiritual pursuits. Family wealth "
            "gradually dispersed; charitable spending."
        ),
        confidence=0.8,
        verse="Ch.25 v.24-25",
        tags=["2nd_lord", "12th_house", "expenditure", "losses", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H1_H2_REGISTRY.add(_r)
