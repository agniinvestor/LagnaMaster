"""
src/corpus/bphs_special_lagnas.py — BPHS Special Lagnas (S228)

Encodes rules for special ascending references beyond the main lagna:
Chandra Lagna (Moon as ascendant), Surya Lagna (Sun as ascendant),
Bhava Lagna, Hora Lagna, and Ghati Lagna.

Sources:
  BPHS Ch.57-60 — Special Lagna rules and analysis

20 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_SPECIAL_LAGNAS_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord(
        rule_id="SL001",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Chandra Lagna (Moon sign as ascendant): the Moon sign is used "
            "as an alternative reference point. House placements from Moon "
            "reveal emotional and material themes."
        ),
        confidence=0.9,
        verse="Ch.57 v.1-3",
        tags=["special_lagna", "moon", "chandra_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL002",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Triple confirmation: a life event is strongly predicted when "
            "the theme is indicated from lagna, Chandra Lagna, and Surya "
            "Lagna (Sun as ascendant). Triple confirmation = near-certainty."
        ),
        confidence=0.9,
        verse="Ch.57 v.4-7",
        tags=["special_lagna", "triple_confirmation", "chandra_lagna", "surya_lagna"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL003",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Arudha Lagna (AL): the house as far from lagna as lagna lord "
            "is from lagna. Arudha represents the 'image' or 'maya' of the "
            "native — how they are perceived by the world."
        ),
        confidence=0.85,
        verse="Ch.57 v.8-11",
        tags=["special_lagna", "arudha_lagna", "image", "perception"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL004",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Bhava Lagna: lagna that rises at birth based on number of hours "
            "since sunrise. Indicates the native's material prosperity and "
            "fortune from a temporal perspective."
        ),
        confidence=0.655,
        verse="Ch.57 v.12-14",
        tags=["special_lagna", "bhava_lagna", "temporal", "prosperity"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL005",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Hora Lagna: rises every 2.5 hours; based on Sun/Moon hora. "
            "Used for wealth analysis; benefics in kendra from Hora Lagna "
            "indicate strong financial outcomes."
        ),
        confidence=0.655,
        verse="Ch.57 v.15-17",
        tags=["special_lagna", "hora_lagna", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL006",
        source="BPHS",
        chapter="Ch.57",
        school="parashari",
        category="special_lagna",
        description=(
            "Ghati Lagna: rises every 6 minutes; used for power and authority. "
            "Planets in kendra from Ghati Lagna give political power, "
            "administrative authority, and dominance."
        ),
        confidence=0.655,
        verse="Ch.57 v.18-20",
        tags=["special_lagna", "ghati_lagna", "power", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL007",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="special_lagna",
        description=(
            "Upapada Lagna (UL): arudha of H12 lord. Reveals the nature "
            "of marriage partner, relationship quality, and marital karma. "
            "Key reference for marriage analysis."
        ),
        confidence=0.85,
        verse="Ch.58 v.1-4",
        tags=["special_lagna", "upapada", "marriage", "spouse"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL008",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="special_lagna",
        description=(
            "Benefic in Upapada Lagna: benefics (Jupiter, Venus, Mercury) "
            "in UL or aspecting UL give a cultured, beautiful, or fortunate "
            "spouse. Marriage is generally happy."
        ),
        confidence=0.8,
        verse="Ch.58 v.5-8",
        tags=["special_lagna", "upapada", "benefic", "spouse_quality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL009",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="special_lagna",
        description=(
            "Malefic in Upapada Lagna: malefics (Saturn, Mars, Rahu/Ketu) "
            "in UL or aspecting UL can indicate difficulties in marriage, "
            "harsh or challenging spouse, or separation."
        ),
        confidence=0.8,
        verse="Ch.58 v.9-12",
        tags=["special_lagna", "upapada", "malefic", "marriage_challenges"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL010",
        source="BPHS",
        chapter="Ch.58",
        school="parashari",
        category="special_lagna",
        description=(
            "Darapada (A7) analysis: Darapada (arudha of H7) shows the "
            "public image of the spouse and how partnerships appear to others. "
            "A7 with benefics = popular, well-regarded partner."
        ),
        confidence=0.655,
        verse="Ch.58 v.13-15",
        tags=["special_lagna", "darapada", "a7", "partner_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL011",
        source="BPHS",
        chapter="Ch.59",
        school="parashari",
        category="special_lagna",
        description=(
            "Matru Pada (A4): arudha of H4, showing how the native's home "
            "and mother are perceived publicly. Strong A4 = visible domestic "
            "happiness and social comfort."
        ),
        confidence=0.655,
        verse="Ch.59 v.1-3",
        tags=["special_lagna", "matru_pada", "a4", "home_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL012",
        source="BPHS",
        chapter="Ch.59",
        school="parashari",
        category="special_lagna",
        description=(
            "Putrapada (A5): arudha of H5, showing public perception of "
            "children and creative works. Strong A5 = well-known children "
            "or famous creative output."
        ),
        confidence=0.655,
        verse="Ch.59 v.4-6",
        tags=["special_lagna", "putrapada", "a5", "children_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL013",
        source="BPHS",
        chapter="Ch.59",
        school="parashari",
        category="special_lagna",
        description=(
            "Rajyapada (A10): arudha of H10, showing public perception of "
            "career and status. Strong A10 with malefics = feared authority; "
            "with benefics = respected leadership."
        ),
        confidence=0.8,
        verse="Ch.59 v.7-9",
        tags=["special_lagna", "rajyapada", "a10", "career_image"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL014",
        source="BPHS",
        chapter="Ch.59",
        school="parashari",
        category="special_lagna",
        description=(
            "Shree Lagna (SL): special lagna for wealth based on Moon's "
            "longitude in the day/night chart. Benefics in kendra from "
            "Shree Lagna give exceptional material prosperity."
        ),
        confidence=0.655,
        verse="Ch.59 v.10-12",
        tags=["special_lagna", "shree_lagna", "wealth"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL015",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Prana Lagna: vitality lagna rising every 2 hours. Critical for "
            "health analysis; afflictions to Prana Lagna correlate with "
            "specific health vulnerabilities."
        ),
        confidence=0.65,
        verse="Ch.60 v.1-3",
        tags=["special_lagna", "prana_lagna", "health", "vitality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL016",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Deha Lagna: body lagna for physical constitution analysis. "
            "Connects to birth lagna for double confirmation of physical "
            "health themes."
        ),
        confidence=0.65,
        verse="Ch.60 v.4-6",
        tags=["special_lagna", "deha_lagna", "body", "health"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL017",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Surya Lagna (Sun as ascendant): counting houses from Sun's "
            "position gives the Surya Lagna chart. Used for career, "
            "government, and father themes."
        ),
        confidence=0.8,
        verse="Ch.60 v.7-9",
        tags=["special_lagna", "surya_lagna", "sun", "career"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL018",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Concordance across lagna systems: when lagna, Chandra Lagna, "
            "and Surya Lagna all show the same theme, the prediction is "
            "highly reliable. Contradictions indicate uncertainty."
        ),
        confidence=0.85,
        verse="Ch.60 v.10-12",
        tags=["special_lagna", "concordance", "triple_confirmation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL019",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Navamsha Lagna (D9): the Navamsha ascendant is a secondary "
            "chart reference. Strong D9 lagna = fortune in second half of "
            "life; weak D9 lagna = struggles despite good D1."
        ),
        confidence=0.85,
        verse="Ch.60 v.13-15",
        tags=["special_lagna", "navamsha_lagna", "d9", "fortune"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="SL020",
        source="BPHS",
        chapter="Ch.60",
        school="parashari",
        category="special_lagna",
        description=(
            "Varnada Lagna: special lagna for social status and profession. "
            "Planets in kendra from Varnada give social recognition and "
            "professional position matching birth background."
        ),
        confidence=0.65,
        verse="Ch.60 v.16-18",
        tags=["special_lagna", "varnada_lagna", "social_status"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_SPECIAL_LAGNAS_REGISTRY.add(_r)
