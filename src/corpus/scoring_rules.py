"""src/corpus/scoring_rules.py — The 26 house-scoring rules as DATA.

Architecture gap G2: migrate R01-R24 + D6 + WL from Python if/else chains
to structured rule records.  Each rule specifies WHAT to check (condition_type
+ parameters), not HOW — the evaluator in scoring_rule_eval.py handles HOW.

These rules are house-relative: they apply once per house, with the house
number as context.  Unlike corpus rules (verse-specific predictions), these
are structural scoring rules that evaluate house quality.

Weight tables are also stored here (G4 weight store reads from these at build time).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Accumulation(Enum):
    """How multiple matching planets affect the score."""
    BINARY = "binary"          # fire once (0 or weight)
    PER_PLANET = "per_planet"  # weight × count
    CUSTOM = "custom"          # rule-specific logic


@dataclass(frozen=True)
class ScoringRule:
    """One house-scoring rule as data.

    Fields
    ------
    rule_id : str
        Stable identifier (R01-R24, D6, WL).
    name : str
        Human-readable description.
    condition_type : str
        Dispatch key for the evaluator.
    params : dict
        Condition-specific parameters.
    verse_ref : str
        BPHS/source citation.
    accumulation : Accumulation
        How to aggregate when multiple planets match.
    is_wide_card : bool
        If True, aggregation applies 0.5× multiplier to this rule's score.
    weight_key : str
        Key into the weight table (usually same as rule_id).
    """
    rule_id: str
    name: str
    condition_type: str
    params: dict = field(default_factory=dict)
    verse_ref: str = ""
    accumulation: Accumulation = Accumulation.BINARY
    is_wide_card: bool = False
    weight_key: str = ""

    def __post_init__(self):
        if not self.weight_key:
            object.__setattr__(self, "weight_key", self.rule_id)


# ---------------------------------------------------------------------------
# The 26 rules as data
# ---------------------------------------------------------------------------

SCORING_RULES: list[ScoringRule] = [
    # ── Favorable structural ──────────────────────────────────────────────
    ScoringRule(
        rule_id="R01",
        name="Gentle sign in house",
        condition_type="sign_in_set",
        params={"sign_set": {3, 1, 6, 11, 8}},  # Cancer, Taurus, Libra, Pisces, Sagittarius
        verse_ref="BPHS Ch.3 v.11",
    ),
    ScoringRule(
        rule_id="R02",
        name="Functional benefic in house",
        condition_type="func_benefic_in_house",
        params={"yogakaraka_bonus": True},
        verse_ref="BPHS Ch.34",
        accumulation=Accumulation.PER_PLANET,
    ),
    ScoringRule(
        rule_id="R03",
        name="Benefic aspects house",
        condition_type="func_benefic_aspects_house",
        verse_ref="BPHS Ch.26 v.5",
        is_wide_card=True,
    ),
    ScoringRule(
        rule_id="R04",
        name="Bhavesh in Kendra or Trikona",
        condition_type="bhavesh_in_house_set",
        params={"house_set": "kendra_trikona", "exclude": "dusthana"},
        verse_ref="BPHS Ch.11 v.1-3",
    ),
    ScoringRule(
        rule_id="R05",
        name="Bhavesh with Kendra/Trikona lord",
        condition_type="bhavesh_conjunct_lord_type",
        params={"lord_set": "kendra_trikona"},
        verse_ref="BPHS Ch.11 v.4",
        is_wide_card=True,
    ),
    ScoringRule(
        rule_id="R06",
        name="Bhavesh with functional benefic",
        condition_type="bhavesh_conjunct_func_benefic",
        params={"yogakaraka_bonus": True},
        verse_ref="BPHS Ch.34",
        accumulation=Accumulation.PER_PLANET,
    ),
    ScoringRule(
        rule_id="R07",
        name="Benefic aspects Bhavesh sign",
        condition_type="func_benefic_aspects_bhavesh",
        verse_ref="BPHS Ch.26 v.5",
        is_wide_card=True,
    ),
    ScoringRule(
        rule_id="R08",
        name="House in Shubh Kartari",
        condition_type="shubh_kartari",
        verse_ref="BPHS Ch.11 v.8",
    ),

    # ── Unfavorable structural ────────────────────────────────────────────
    ScoringRule(
        rule_id="R09",
        name="Functional malefic in house",
        condition_type="func_malefic_in_house",
        verse_ref="BPHS Ch.34",
        accumulation=Accumulation.PER_PLANET,
    ),
    ScoringRule(
        rule_id="R10",
        name="Malefic aspects house",
        condition_type="func_malefic_aspects_house",
        verse_ref="BPHS Ch.26 v.5",
    ),
    ScoringRule(
        rule_id="R11",
        name="Dusthana lord in house",
        condition_type="dusthana_lord_in_house",
        verse_ref="BPHS Ch.11 v.9",
    ),
    ScoringRule(
        rule_id="R12",
        name="House in Paap Kartari",
        condition_type="paap_kartari",
        verse_ref="BPHS Ch.11 v.8",
    ),
    ScoringRule(
        rule_id="R13",
        name="Bhavesh with functional malefic",
        condition_type="bhavesh_conjunct_func_malefic",
        params={
            "mitigation_check": True,
            "mitigation_factor": 0.5,   # D5: score multiplier when mitigated
        },
        verse_ref="BPHS Ch.11 note (b), p.125",
        accumulation=Accumulation.CUSTOM,
    ),
    ScoringRule(
        rule_id="R14",
        name="Malefic aspects Bhavesh",
        condition_type="func_malefic_aspects_bhavesh",
        verse_ref="BPHS Ch.26 v.5",
        is_wide_card=True,
    ),
    ScoringRule(
        rule_id="R15",
        name="Bhavesh in Dusthana",
        condition_type="bhavesh_in_house_set",
        params={"house_set": "dusthana"},
        verse_ref="BPHS Ch.11 v.6",
    ),
    ScoringRule(
        rule_id="R16",
        name="Bhavesh with Dusthana lord",
        condition_type="bhavesh_conjunct_dusthana_lord",
        params={"self_exemption": True},
        verse_ref="BPHS Ch.11 note (c), p.125",
        accumulation=Accumulation.CUSTOM,
    ),

    # ── Sthir Karak ───────────────────────────────────────────────────────
    ScoringRule(
        rule_id="R17",
        name="Sthir Karak in or aspecting signified house",
        condition_type="sthira_karaka_support",
        verse_ref="BPHS Ch.32",
        accumulation=Accumulation.PER_PLANET,
    ),
    ScoringRule(
        rule_id="R18",
        name="Sthir Karak in Dusthana from signified house",
        condition_type="sthira_karaka_dusthana",
        verse_ref="BPHS Ch.32",
        accumulation=Accumulation.PER_PLANET,
    ),

    # ── Bhavesh quality ───────────────────────────────────────────────────
    ScoringRule(
        rule_id="R19",
        name="Bhavesh combust",
        condition_type="bhavesh_combust",
        params={
            "cazimi_score": +0.5,       # D5: cazimi overrides to positive
            "asta_vakri_score": -0.5,    # D5: combust + retrograde (reduced)
        },
        verse_ref="BPHS Ch.3 v.42-45",
        accumulation=Accumulation.CUSTOM,
    ),
    ScoringRule(
        rule_id="R20",
        name="Bhavesh in Dig Bala house",
        condition_type="bhavesh_dig_bala",
        verse_ref="BPHS Ch.27 v.36",
    ),
    ScoringRule(
        rule_id="R21",
        name="Bhavesh in Pushkara Navamsha",
        condition_type="bhavesh_pushkara",
        verse_ref="BPHS Ch.4 v.4",
    ),
    ScoringRule(
        rule_id="R22",
        name="Bhavesh retrograde",
        condition_type="bhavesh_retrograde",
        verse_ref="Phaladeepika Ch.2 v.9",
    ),
    ScoringRule(
        rule_id="R23",
        name="Ashtakavarga SAV >= 5",
        condition_type="ashtakavarga_threshold",
        params={"threshold": 5},
        verse_ref="BPHS Ch.66-71",
    ),
    ScoringRule(
        rule_id="R24",
        name="Bhavesh dignity modifier",
        condition_type="bhavesh_dignity_score",
        verse_ref="BPHS Ch.3 v.47-51",
        accumulation=Accumulation.CUSTOM,
    ),

    # ── Special modifiers ─────────────────────────────────────────────────
    ScoringRule(
        rule_id="D6",
        name="Bhavesh avastha modifier",
        condition_type="bhavesh_avastha",
        params={
            "mrita_score": -1.5,     # D5: "bhava will be destroyed" (Ch.11 p.126)
            "vriddha_score": -0.75,  # D5: "ineffective from view point of good results"
            "baala_score": -0.25,    # D5: 1/4 effect — reduced but not destroyed
        },
        verse_ref="BPHS Ch.11 v.14-16",
        accumulation=Accumulation.CUSTOM,
    ),
    ScoringRule(
        rule_id="WL",
        name="Bhavesh war loser penalty",
        condition_type="bhavesh_war_loser",
        params={
            "penalty": -1.5,         # D5: war loser penalty score
        },
        verse_ref="Saravali Ch.4 v.18-22",
        accumulation=Accumulation.CUSTOM,
    ),
]

# Lookup by rule_id for fast access
SCORING_RULES_BY_ID: dict[str, ScoringRule] = {r.rule_id: r for r in SCORING_RULES}

# ---------------------------------------------------------------------------
# Weight tables — per-school rule weights (G4 will move these to weight_store)
# ---------------------------------------------------------------------------

SCHOOL_WEIGHTS: dict[str, dict[str, float]] = {
    "parashari": {
        "R01": 0.5, "R02": 1.0, "R03": 0.75, "R04": 2.0,
        "R05": 0.5, "R06": 1.0, "R07": 0.5, "R08": 0.75,
        "R09": -1.0, "R10": -1.0, "R11": -1.25, "R12": -0.75,
        "R13": -1.0, "R14": -0.5, "R15": -2.0, "R16": -0.75,
        "R17": 0.5, "R18": -0.5, "R19": -1.0, "R20": 0.5,
        "R21": 0.5, "R22": 0.25, "R23": 0.5, "R24": 1.0,
    },
    "kp": {
        "R01": 0.5, "R02": 1.0, "R03": 0.5, "R04": 1.5,
        "R05": 0.5, "R06": 1.0, "R07": 0.5, "R08": 0.75,
        "R09": -1.0, "R10": -1.0, "R11": -1.25, "R12": -0.75,
        "R13": -1.0, "R14": -0.5, "R15": -1.75, "R16": -0.75,
        "R17": 0.5, "R18": -0.5, "R19": -1.0, "R20": 0.5,
        "R21": 0.5, "R22": 0.25, "R23": 0.25, "R24": 1.0,
    },
    "jaimini": {
        "R01": 0.5, "R02": 1.0, "R03": 0.75, "R04": 1.5,
        "R05": 0.5, "R06": 1.0, "R07": 0.5, "R08": 0.5,
        "R09": -1.0, "R10": -1.0, "R11": -1.0, "R12": -0.5,
        "R13": -1.0, "R14": -0.5, "R15": -2.0, "R16": -0.75,
        "R17": 0.75, "R18": -0.75, "R19": -1.0, "R20": 0.25,
        "R21": 0.25, "R22": 0.25, "R23": 0.5, "R24": 1.0,
    },
}

YOGAKARAKA_MULTIPLIER: dict[str, float] = {
    "parashari": 1.5,
    "kp": 1.5,
    "jaimini": 1.25,
}
