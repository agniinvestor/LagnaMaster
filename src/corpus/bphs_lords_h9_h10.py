"""
src/corpus/bphs_lords_h9_h10.py — BPHS Lord-in-Houses: H9 + H10 Lords (S220)

Encodes BPHS Ch.32-33: Effects of 9th and 10th house lords placed in each
of the 12 houses.

Sources:
  BPHS Ch.32 — Navamadhipa Phala (9th lord results)
  BPHS Ch.33 — Dashamadhipa Phala (10th lord results)

24 rules total. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H9_H10_REGISTRY = CorpusRegistry()

_RULES = [
    # ── 9th Lord in each house — BPHS Ch.32 ──────────────────────────────────
    RuleRecord(
        rule_id="H9L001",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H1: deeply fortunate, dharmic personality. Father's "
            "blessings manifest in the self. Higher wisdom and philosophy "
            "are personal traits. Remarkable good luck."
        ),
        confidence=0.9,
        verse="Ch.32 v.1-3",
        tags=["9th_lord", "1st_house", "fortune", "dharma", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L002",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H2: wealth through dharma, education, father's "
            "support. Family is cultured and fortunate. Eloquent speech "
            "carries philosophical wisdom."
        ),
        confidence=0.85,
        verse="Ch.32 v.4-5",
        tags=["9th_lord", "2nd_house", "dharmic_wealth", "father"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L003",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H3: dharma expressed through courage and writing. "
            "Siblings support spiritual path. Pilgrimage via short journeys. "
            "Religious publishing or teaching."
        ),
        confidence=0.8,
        verse="Ch.32 v.6-7",
        tags=["9th_lord", "3rd_house", "dharmic_writing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L004",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H4: fortune through domestic happiness. Mother is "
            "dharmic and fortunate. Property acquired through luck. "
            "Education received in ancestral tradition."
        ),
        confidence=0.85,
        verse="Ch.32 v.8-9",
        tags=["9th_lord", "4th_house", "fortunate_home", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L005",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H5 (two trikonas): exceptional dharmic intelligence, "
            "past-life spiritual merit strong. Children inherit religious "
            "traditions. Philosophical creativity."
        ),
        confidence=0.9,
        verse="Ch.32 v.10-11",
        tags=["9th_lord", "5th_house", "double_trikona", "dharma", "intelligence"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L006",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H6 (dusthana): dharma tested through disease or "
            "enmity. Father faces challenges. Long journeys involve hardship. "
            "Karma confronts obstacles before fortune manifests."
        ),
        confidence=0.655,
        verse="Ch.32 v.12-13",
        tags=["9th_lord", "6th_house", "dharma_tested", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L007",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H7: fortunate marriage, dharmic spouse. Long journeys "
            "connected to partnerships. Business at pilgrim centers or "
            "religious institutions."
        ),
        confidence=0.85,
        verse="Ch.32 v.14-15",
        tags=["9th_lord", "7th_house", "fortunate_marriage", "dharmic_spouse"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L008",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H8 (dusthana): father's longevity reduced. Dharma "
            "confronted by hidden obstacles. Long journeys involve danger. "
            "Occult or esoteric philosophical path."
        ),
        confidence=0.65,
        verse="Ch.32 v.16-17",
        tags=["9th_lord", "8th_house", "father_longevity", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L009",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H9 (own house): extremely fortunate, deeply religious, "
            "father's blessing strongest. Higher learning, philosophy, and "
            "dharmic success all maximized."
        ),
        confidence=0.95,
        verse="Ch.32 v.18-19",
        tags=["9th_lord", "9th_house", "fortune", "dharma", "own_house", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L010",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H10 (kendra + trikona lord in kendra): Dharma Karma "
            "Adhipati yoga — professional success and dharmic karma unite. "
            "Career in teaching, law, or religious authority."
        ),
        confidence=0.9,
        verse="Ch.32 v.20-21",
        tags=["9th_lord", "10th_house", "dharma_karma_adhipati", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L011",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H11: gains through dharma, fortune, father. Social "
            "networks include teachers and spiritual authorities. Luck "
            "fulfilled through righteous actions."
        ),
        confidence=0.85,
        verse="Ch.32 v.22-23",
        tags=["9th_lord", "11th_house", "dharmic_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H9L012",
        source="BPHS",
        chapter="Ch.32",
        school="parashari",
        category="bhava_phala",
        description=(
            "9th lord in H12 (dusthana): dharma leads to liberation. Father "
            "takes spiritual renunciation. Long pilgrimages to foreign holy "
            "sites. Moksha becomes the dharmic path."
        ),
        confidence=0.8,
        verse="Ch.32 v.24-25",
        tags=["9th_lord", "12th_house", "liberation", "foreign_pilgrimage"],
        implemented=False,
    ),

    # ── 10th Lord in each house — BPHS Ch.33 ─────────────────────────────────
    RuleRecord(
        rule_id="H10L001",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H1: career-driven personality, actions are visible "
            "to the world. Authority and karma expressed through the self. "
            "Career-defining personality."
        ),
        confidence=0.9,
        verse="Ch.33 v.1-3",
        tags=["10th_lord", "1st_house", "career", "karma", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L002",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H2: professional wealth, career brings family "
            "prosperity. Authority in speech and financial matters. "
            "Career involves banking, finance, or education."
        ),
        confidence=0.85,
        verse="Ch.33 v.4-5",
        tags=["10th_lord", "2nd_house", "career_wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L003",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H3: career through communication, media, or "
            "technology. Siblings support professional goals. Short-distance "
            "commerce as profession."
        ),
        confidence=0.8,
        verse="Ch.33 v.6-7",
        tags=["10th_lord", "3rd_house", "media_career", "communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L004",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H4: career in real estate, domestic goods, "
            "agriculture, or education. Professional base is the home. "
            "Mother's influence on career choice."
        ),
        confidence=0.8,
        verse="Ch.33 v.8-9",
        tags=["10th_lord", "4th_house", "property_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L005",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H5 (kendra lord in trikona): Dharma Karma Adhipati "
            "connection — career enriched by creativity and past merit. "
            "Speculative or creative profession succeeds."
        ),
        confidence=0.85,
        verse="Ch.33 v.10-11",
        tags=["10th_lord", "5th_house", "creative_career", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L006",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H6 (kendra lord in dusthana): career challenged by "
            "enemies or litigation. Service in competitive fields. Authority "
            "in medicine, military, or law."
        ),
        confidence=0.655,
        verse="Ch.33 v.12-13",
        tags=["10th_lord", "6th_house", "service_career", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L007",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H7: career through partnerships, business, or "
            "foreign trade. Professional success through marriage connections. "
            "Spouse assists career."
        ),
        confidence=0.85,
        verse="Ch.33 v.14-15",
        tags=["10th_lord", "7th_house", "business_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L008",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H8 (kendra lord in dusthana): career disruptions, "
            "sudden professional changes. Occult or research-based career. "
            "Authority in matters of legacy or transformation."
        ),
        confidence=0.65,
        verse="Ch.33 v.16-17",
        tags=["10th_lord", "8th_house", "career_disruption", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L009",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H9 (kendra lord in trikona): Dharma Karma Adhipati "
            "yoga — righteous and successful career. Teaching, law, or "
            "religious authority. Father supports career."
        ),
        confidence=0.9,
        verse="Ch.33 v.18-19",
        tags=["10th_lord", "9th_house", "dharma_karma_adhipati", "kendra", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L010",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H10 (own house): exceptional career success, strong "
            "professional authority, public recognition. Karma is clear and "
            "productive. Leadership in chosen field."
        ),
        confidence=0.95,
        verse="Ch.33 v.20-21",
        tags=["10th_lord", "10th_house", "career", "authority", "own_house", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L011",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H11: gains through career, income from professional "
            "networks. Elder siblings assist professional life. Multiple "
            "income streams through career."
        ),
        confidence=0.85,
        verse="Ch.33 v.22-23",
        tags=["10th_lord", "11th_house", "career_gains"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H10L012",
        source="BPHS",
        chapter="Ch.33",
        school="parashari",
        category="bhava_phala",
        description=(
            "10th lord in H12 (kendra lord in dusthana): career in foreign "
            "lands, spiritual institutions, or behind-the-scenes work. "
            "Professional isolation or voluntary withdrawal."
        ),
        confidence=0.655,
        verse="Ch.33 v.24-25",
        tags=["10th_lord", "12th_house", "foreign_career", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H9_H10_REGISTRY.add(_r)
