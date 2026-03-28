"""
src/corpus/bphs_lords_h7_h8.py — BPHS Lord-in-Houses: H7 + H8 Lords (S219)

Encodes BPHS Ch.30-31: Effects of 7th and 8th house lords placed in each
of the 12 houses.

Sources:
  BPHS Ch.30 — Saptamadhipa Phala (7th lord results)
  BPHS Ch.31 — Ashtamadhipa Phala (8th lord results)

24 rules total. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_LORDS_H7_H8_REGISTRY = CorpusRegistry()

_RULES = [
    # ── 7th Lord in each house — BPHS Ch.30 ──────────────────────────────────
    RuleRecord(
        rule_id="H7L001",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H1: spouse's nature strongly impacts the native. "
            "Partnerships define self-image. Attractive or relationship-focused "
            "personality. Foreign connections through marriage."
        ),
        confidence=0.85,
        verse="Ch.30 v.1-3",
        tags=["7th_lord", "1st_house", "spouse", "partnership"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L002",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H2: wealth through marriage or business partnerships. "
            "Spouse contributes to family treasury. Eloquence used in "
            "negotiation and trade."
        ),
        confidence=0.85,
        verse="Ch.30 v.4-5",
        tags=["7th_lord", "2nd_house", "spouse_wealth", "business"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L003",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H3: partner met through short journeys, communication, "
            "or siblings' connections. Partnership involves media or commerce. "
            "Marriage after much effort and negotiation."
        ),
        confidence=0.8,
        verse="Ch.30 v.6-7",
        tags=["7th_lord", "3rd_house", "partner_through_travel"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L004",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H4: spouse adds domestic comfort, home-oriented "
            "partnership. Marriage brings real estate or vehicle acquisition. "
            "Mother approves of spouse."
        ),
        confidence=0.85,
        verse="Ch.30 v.8-9",
        tags=["7th_lord", "4th_house", "domestic_marriage", "comfort"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L005",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H5: romantic partnership, spouse is intelligent and "
            "creative. Marriage blessed with children. Speculative or artistic "
            "joint ventures succeed."
        ),
        confidence=0.85,
        verse="Ch.30 v.10-11",
        tags=["7th_lord", "5th_house", "romance", "children", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L006",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H6 (dusthana): marital discord, legal disputes in "
            "partnerships. Spouse may face health challenges. Business "
            "partnerships involve conflicts."
        ),
        confidence=0.75,
        verse="Ch.30 v.12-13",
        tags=["7th_lord", "6th_house", "marital_discord", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L007",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H7 (own house): strong marriage, devoted spouse, "
            "successful business partnerships. Native's identity centered "
            "on relationships. High social attractiveness."
        ),
        confidence=0.9,
        verse="Ch.30 v.14-15",
        tags=["7th_lord", "7th_house", "strong_marriage", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L008",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H8 (dusthana): spouse's longevity may be affected, "
            "hidden challenges in partnerships. Sudden changes in marriage. "
            "Occult or transformative relationship."
        ),
        confidence=0.75,
        verse="Ch.30 v.16-17",
        tags=["7th_lord", "8th_house", "spouse_longevity", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L009",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H9 (trikona): fortunate marriage, spouse is dharmic "
            "and cultured. Long journeys associated with marriage. Spiritual "
            "partnerships or guru-disciple dynamics."
        ),
        confidence=0.85,
        verse="Ch.30 v.18-19",
        tags=["7th_lord", "9th_house", "dharmic_marriage", "trikona"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L010",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H10 (kendra): career success through partnerships "
            "or marriage. Spouse assists professional ambitions. Joint ventures "
            "achieve public recognition."
        ),
        confidence=0.85,
        verse="Ch.30 v.20-21",
        tags=["7th_lord", "10th_house", "career_through_partnership", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L011",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H11: gains through partnerships and marriage. Spouse "
            "contributes to income. Network of business partnerships fulfills "
            "financial desires."
        ),
        confidence=0.85,
        verse="Ch.30 v.22-23",
        tags=["7th_lord", "11th_house", "gains_through_marriage"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H7L012",
        source="BPHS",
        chapter="Ch.30",
        school="parashari",
        category="bhava_phala",
        description=(
            "7th lord in H12 (dusthana): spouse settles abroad or in spiritual "
            "institutions. Foreign partnerships. Bed pleasures, liberation "
            "themes in marriage."
        ),
        confidence=0.75,
        verse="Ch.30 v.24-25",
        tags=["7th_lord", "12th_house", "foreign_spouse", "dusthana"],
        implemented=False,
    ),

    # ── 8th Lord in each house — BPHS Ch.31 ──────────────────────────────────
    RuleRecord(
        rule_id="H8L001",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H1 (dusthana lord in ascendant): health challenges, "
            "chronic ailments, interest in occult. Transformative experiences "
            "define personality. Longevity ambiguous."
        ),
        confidence=0.75,
        verse="Ch.31 v.1-3",
        tags=["8th_lord", "1st_house", "health", "occult", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L002",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H2: family wealth subject to sudden disruption, "
            "inheritance disputes. Speech affected by hidden tensions. "
            "Wealth through legacy, occult, or taboo trades."
        ),
        confidence=0.75,
        verse="Ch.31 v.4-5",
        tags=["8th_lord", "2nd_house", "legacy_wealth", "family_disruption"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L003",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H3: siblings face longevity or health challenges. "
            "Courage tested through hidden dangers. Writing about occult or "
            "research subjects."
        ),
        confidence=0.7,
        verse="Ch.31 v.6-7",
        tags=["8th_lord", "3rd_house", "siblings_longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L004",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H4: domestic disruption, mother's longevity challenged, "
            "property subject to hidden encumbrances. Sudden changes in home. "
            "Emotional transformation through family crises."
        ),
        confidence=0.7,
        verse="Ch.31 v.8-9",
        tags=["8th_lord", "4th_house", "mother_longevity", "property_issues"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L005",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H5: children face health challenges or longevity "
            "concerns. Intelligence drawn to taboo or hidden subjects. "
            "Speculation involves high risk."
        ),
        confidence=0.7,
        verse="Ch.31 v.10-11",
        tags=["8th_lord", "5th_house", "children_longevity", "occult"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L006",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H6 (both dusthana): viparita raja yoga — obstacles "
            "neutralize each other. Service in dangerous or healing fields. "
            "Disease patterns complex but manageable."
        ),
        confidence=0.8,
        verse="Ch.31 v.12-13",
        tags=["8th_lord", "6th_house", "viparita_raja_yoga", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L007",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H7: spouse's longevity may be challenged. Sudden "
            "changes in marriage. Occult or hidden aspects to partnerships. "
            "Transformative marital experiences."
        ),
        confidence=0.7,
        verse="Ch.31 v.14-15",
        tags=["8th_lord", "7th_house", "spouse_longevity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L008",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H8 (own house): strong longevity, occult mastery, "
            "interest in research and transformation. Inherits through multiple "
            "sources. Mystical orientation."
        ),
        confidence=0.85,
        verse="Ch.31 v.16-17",
        tags=["8th_lord", "8th_house", "longevity", "occult", "own_house"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L009",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H9 (dusthana lord in trikona): father's longevity "
            "challenged. Dharma confronts hidden obstacles. Long journeys "
            "involve dangers. Research into dharmic or occult subjects."
        ),
        confidence=0.7,
        verse="Ch.31 v.18-19",
        tags=["8th_lord", "9th_house", "father_longevity", "dusthana"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L010",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H10: career in research, medicine, occult, or "
            "hidden services. Professional transformation through crises. "
            "Authority in matters of death, inheritance, or legacy."
        ),
        confidence=0.75,
        verse="Ch.31 v.20-21",
        tags=["8th_lord", "10th_house", "research_career", "kendra"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L011",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H11: sudden gains through legacy, insurance, or "
            "occult practice. Elder siblings may face challenges. Unexpected "
            "financial windfalls and losses alternate."
        ),
        confidence=0.75,
        verse="Ch.31 v.22-23",
        tags=["8th_lord", "11th_house", "sudden_gains", "legacy"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="H8L012",
        source="BPHS",
        chapter="Ch.31",
        school="parashari",
        category="bhava_phala",
        description=(
            "8th lord in H12 (both dusthana): viparita raja yoga potential. "
            "Challenges dissolve through isolation or foreign residence. "
            "Liberation through confronting hidden fears."
        ),
        confidence=0.8,
        verse="Ch.31 v.24-25",
        tags=["8th_lord", "12th_house", "viparita_raja_yoga", "liberation", "dusthana"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_LORDS_H7_H8_REGISTRY.add(_r)
