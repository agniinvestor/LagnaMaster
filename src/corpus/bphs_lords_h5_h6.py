"""
src/corpus/bphs_lords_h5_h6.py — BPHS Lord-in-Houses: H5 + H6 Lords (S218)

Encodes BPHS Ch.28-29: Effects of 5th and 6th house lords placed in each
of the 12 houses.

Sources:
  BPHS Ch.28 — Panchamadhipa Phala (5th lord results)
  BPHS Ch.29 — Shashthadhipa Phala (6th lord results)

24 rules total. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H5_H6_REGISTRY = CorpusRegistry()

_RULES = [
    # ── 5th Lord in each house — BPHS Ch.28 ──────────────────────────────────
    RuleRecord(
        rule_id="H5L001",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H1: intelligent, creative self-expression prominent. "
            "Past-life merit actively manifests. Speculative or artistic "
            "abilities define the native."
        ),
        confidence=0.9,
        verse="Ch.28 v.1-3",
        tags=["5th_lord", "1st_house", "intelligence", "purva_punya", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L002",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H2: wealth through intelligence, speculation, education. "
            "Children contribute to family treasury. Knowledge brings financial "
            "prosperity."
        ),
        confidence=0.85,
        verse="Ch.28 v.4-5",
        tags=["5th_lord", "2nd_house", "intelligence_wealth", "children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L003",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H3: creative courage, children are bold. Artistic "
            "or intellectual communication. Short writings, poetry, or "
            "storytelling talent."
        ),
        confidence=0.8,
        verse="Ch.28 v.6-7",
        tags=["5th_lord", "3rd_house", "creative_communication"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L004",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H4: domestic happiness through children. Intelligence "
            "rooted in home environment. Education received at home or in "
            "ancestral tradition. Mother is cultured."
        ),
        confidence=0.85,
        verse="Ch.28 v.8-9",
        tags=["5th_lord", "4th_house", "children", "education", "home"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L005",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H5 (own house): exceptional intelligence, multiple "
            "children, strong purva-punya. Creative and speculative success. "
            "Mantra and spiritual practices effective."
        ),
        confidence=0.95,
        verse="Ch.28 v.10-11",
        tags=["5th_lord", "5th_house", "intelligence", "children", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L006",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H6 (dusthana): children face health or enemy-related "
            "troubles. Intelligence tested through competition. Speculative "
            "ventures suffer setbacks."
        ),
        confidence=0.655,
        verse="Ch.28 v.12-13",
        tags=["5th_lord", "6th_house", "children_trouble", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L007",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H7: intelligence in partnerships. Children connected "
            "to spouse's life. Marital harmony through shared intellectual "
            "or creative interests."
        ),
        confidence=0.8,
        verse="Ch.28 v.14-15",
        tags=["5th_lord", "7th_house", "partnership", "children"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L008",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H8 (dusthana): occult intelligence, research into "
            "hidden knowledge. Children fewer or facing difficulties. "
            "Speculative risks lead to sudden transformations."
        ),
        confidence=0.655,
        verse="Ch.28 v.16-17",
        tags=["5th_lord", "8th_house", "occult_intelligence", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L009",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H9: profound intelligence and wisdom, dharmic merit "
            "highly activated. Father is philosophical. Children inherit "
            "spiritual or academic tradition."
        ),
        confidence=0.9,
        verse="Ch.28 v.18-19",
        tags=["5th_lord", "9th_house", "wisdom", "dharma", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L010",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H10 (kendra): career in education, arts, speculation, "
            "or children's fields. Creative intelligence drives professional "
            "success. Mantra and advice-giving as profession."
        ),
        confidence=0.85,
        verse="Ch.28 v.20-21",
        tags=["5th_lord", "10th_house", "creative_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L011",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H11: gains through intelligence, children, or "
            "speculative investments. Creative networks fulfill desires. "
            "Elder siblings support intellectual pursuits."
        ),
        confidence=0.85,
        verse="Ch.28 v.22-23",
        tags=["5th_lord", "11th_house", "gains", "creativity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H5L012",
        source="BPHS",
        chapter="Ch.28",
        school="parashari",
        category="bhava_phala",
        description=(
            "5th lord in H12 (dusthana): children settle abroad or take "
            "spiritual path. Intelligence turned toward liberation. "
            "Past-merit expressed through renunciation."
        ),
        confidence=0.655,
        verse="Ch.28 v.24-25",
        tags=["5th_lord", "12th_house", "liberation", "children_abroad", "dusthana"],
        implemented=False,
    ),

    # ── 6th Lord in each house — BPHS Ch.29 ──────────────────────────────────
    RuleRecord(
        rule_id="H6L001",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H1 (dusthana lord in ascendant): health challenges, "
            "enemies or obstacles mark the personality. Competitive nature. "
            "Service orientation; military or medical inclination."
        ),
        confidence=0.8,
        verse="Ch.29 v.1-3",
        tags=["6th_lord", "1st_house", "health_challenge", "enemies"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L002",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H2: wealth from service, medicine, or military. "
            "Debt or litigation affects family finances. Enemies attempt to "
            "disrupt speech or income."
        ),
        confidence=0.655,
        verse="Ch.29 v.4-5",
        tags=["6th_lord", "2nd_house", "service_wealth", "debt"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L003",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H3: siblings face litigation or health challenges. "
            "Communication used in competitive contexts. Short journeys "
            "involve dispute or difficulty."
        ),
        confidence=0.655,
        verse="Ch.29 v.6-7",
        tags=["6th_lord", "3rd_house", "siblings_dispute"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L004",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H4: domestic tensions, disputes over property, "
            "mother's health affected. Vehicles prone to accidents or damage. "
            "Home may become a source of stress."
        ),
        confidence=0.655,
        verse="Ch.29 v.8-9",
        tags=["6th_lord", "4th_house", "property_dispute", "mother_health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L005",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H5: children face health challenges or enmity. "
            "Intelligence applied to competitive pursuits. Speculative "
            "ventures involve high risk."
        ),
        confidence=0.655,
        verse="Ch.29 v.10-11",
        tags=["6th_lord", "5th_house", "children_health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L006",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H6 (own house): enemies destroy each other (viparita "
            "influence). Litigation and disease exist but native overcomes them. "
            "Service sector success despite obstacles."
        ),
        confidence=0.8,
        verse="Ch.29 v.12-13",
        tags=["6th_lord", "6th_house", "viparita_raja_yoga", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L007",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H7: spouse faces health issues or enmity from "
            "partnerships. Litigation in business. Marriage may involve "
            "legal complications."
        ),
        confidence=0.655,
        verse="Ch.29 v.14-15",
        tags=["6th_lord", "7th_house", "spouse_health", "partnership_dispute"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L008",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H8: enemies defeat each other; viparita raja yoga "
            "potential. Disease and longevity concerns, but hidden strength. "
            "Occult healing or research."
        ),
        confidence=0.8,
        verse="Ch.29 v.16-17",
        tags=["6th_lord", "8th_house", "viparita_raja_yoga", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L009",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H9: dharma tested through disease or litigation. "
            "Father faces health challenges. Long journeys involve hardship. "
            "Service performed as religious duty."
        ),
        confidence=0.655,
        verse="Ch.29 v.18-19",
        tags=["6th_lord", "9th_house", "dharma_challenge", "father_health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L010",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H10: career in medicine, law, military, or competitive "
            "fields. Professional challenges through litigation. Authority "
            "in service-oriented sectors."
        ),
        confidence=0.8,
        verse="Ch.29 v.20-21",
        tags=["6th_lord", "10th_house", "service_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L011",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H11: gains through service, litigation, or medicine. "
            "Enemies ultimately defeated. Elder siblings may cause tension "
            "before reconciliation."
        ),
        confidence=0.8,
        verse="Ch.29 v.22-23",
        tags=["6th_lord", "11th_house", "gains_from_service"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H6L012",
        source="BPHS",
        chapter="Ch.29",
        school="parashari",
        category="bhava_phala",
        description=(
            "6th lord in H12 (both dusthana): viparita raja yoga — enemies "
            "and disease destroy themselves. Hidden strength, eventual triumph. "
            "Foreign residence involves medical or service work."
        ),
        confidence=0.85,
        verse="Ch.29 v.24-25",
        tags=["6th_lord", "12th_house", "viparita_raja_yoga", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H5_H6_REGISTRY.add(_r)
