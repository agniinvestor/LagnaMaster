"""
src/corpus/rule_record.py — RuleRecord dataclass (S202, extended S263, extended S305)

Machine-readable encoding of a classical Jyotish rule.
Each rule maps a classical text citation to a testable, computable predicate.

Two tiers:
  Phase 1A (S216–S262): Representative layer — prose descriptions, topic index.
    Fields: rule_id through engine_ref.
    All Phase 1A rules carry phase="1A_representative" automatically.

  Phase 1B (S263+): Sutra-level layer — structured predictions, ML-ready.
    Additional mandatory fields: primary_condition through system.
    Contract defined in docs/PHASE1B_RULE_CONTRACT.md.
    Outcome taxonomy defined in docs/PHASE1B_OUTCOME_TAXONOMY.md.

S305 extensions:
  prediction_type    — event|trait|capacity (drives temporal activation logic)
  gender_scope       — universal|male|female (classical texts often assume male)
  certainty_level    — definite|probable|possible (verse assertiveness)
  strength_condition — any|strong|weak|exalted|debilitated|own_sign|combust
  house_system       — sign_based|bhava_chalita|kp (which house system rule assumes)
  ayanamsha_sensitive — True for sign-placement rules (affected by ayanamsha choice)
  school_specific    — dict for non-Parashari fields (Jaimini/KP/Lal Kitab/Nadi/Muhurtha)
  remedy             — remedial measures mentioned in verse
  evaluation_method  — how the scoring engine should evaluate this rule
  last_modified_session — session number when rule was last created or changed

Public API
----------
  RuleRecord    — one classical rule with metadata and confidence score

Confidence (Phase 1B — mechanical formula)
-------------------------------------------
  base = 0.6
  + 0.08 × len(concordance_texts)   [+0.08 per corroborating text]
  + 0.05 if verse_ref               [verse-level citation bonus]
  − 0.05 × count(divergence sources) [penalty per diverging source text]
  capped at [0.10, 1.0]
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class RuleRecord:
    """
    One classical rule in machine-readable form.

    Phase 1A fields (S202)
    ----------------------
    rule_id      Short identifier, e.g. "R01" or "LPF001"
    source       Classical text, e.g. "BPHS", "LaghuParashari"
    chapter      Chapter/section reference, e.g. "Ch.3"
    school       Jyotish school: parashari|kp|jaimini|nadi|lal_kitab|tajika|all
    category     Rule category string
    description  Plain-language statement of the rule
    confidence   0.0–1.0 (see module docstring)
    verse        Optional Sanskrit verse or key phrase
    tags         Free-form tags for search
    implemented  Whether this rule is currently computed by the engine
    engine_ref   Module and function that implements this rule, if any

    Phase 1B structured fields (S263)
    ----------------------------------
    primary_condition   Structured trigger: {planet, placement_type, placement_value}
    modifiers           List of {condition, effect, strength} — what amplifies/negates
    exceptions          Conditions that fully cancel this rule
    outcome_domains     From 15-domain taxonomy in PHASE1B_OUTCOME_TAXONOMY.md
    outcome_direction   favorable|unfavorable|neutral|mixed
    outcome_intensity   strong|moderate|weak|conditional
    outcome_timing      natal_permanent|early_life|middle_life|late_life|dasha_dependent|unspecified
    lagna_scope         Empty = universal; list of lagnas if lagna-conditional
    dasha_scope         Empty = universal; list of dasha lords if dasha-conditional
    verse_ref           "Ch.N v.M" — chapter + specific verse (Phase 1B mandatory)
    concordance_texts   Other texts stating same prediction (populated at encode time)
    divergence_notes    What other texts say differently about same primary_condition
    phase               1A_representative|1A_deprecated|1B_matrix|1B_conditional|1B_compound
    system              natal|horary|varshaphala|muhurtha|transit

    S305 extensions
    ----------------
    prediction_type     event (marriage/death/promotion) | trait (personality/appearance) | capacity (potential)
    gender_scope        universal | male | female
    certainty_level     definite (will/gives) | probable (likely/tends) | possible (may/might)
    strength_condition  any | strong | weak | exalted | debilitated | own_sign | combust | moolatrikona
    house_system        sign_based | bhava_chalita | kp
    ayanamsha_sensitive True if sign-placement type (affected by ayanamsha choice)
    school_specific     Dict for non-Parashari fields: chara_karaka, sublord, remedy, nadi_seq, etc.
    remedy              Remedial measures mentioned in verse
    evaluation_method   How to evaluate: placement_check|yoga_detection|lordship_check|dasha_activation|transit_check
    last_modified_session  Session number when rule was last created or changed
    """
    # ── Phase 1A fields ───────────────────────────────────────────────────────
    rule_id: str
    source: str
    chapter: str
    school: str
    category: str
    description: str
    confidence: float
    verse: str = ""
    tags: list[str] = field(default_factory=list)
    implemented: bool = False
    engine_ref: str = ""

    # ── Phase 1B structured fields (S263) ────────────────────────────────────
    primary_condition: dict = field(default_factory=dict)
    modifiers: list[dict] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    outcome_domains: list[str] = field(default_factory=list)
    outcome_direction: str = ""
    outcome_intensity: str = ""
    outcome_timing: str = "unspecified"
    lagna_scope: list[str] = field(default_factory=list)
    dasha_scope: list[str] = field(default_factory=list)
    verse_ref: str = ""
    concordance_texts: list[str] = field(default_factory=list)
    divergence_notes: str = ""
    phase: str = "1A_representative"
    system: str = "natal"

    # ── S305 extensions ─────────────────────────────────────────────────────
    prediction_type: str = "event"
    gender_scope: str = "universal"
    certainty_level: str = "definite"
    strength_condition: str = "any"
    house_system: str = "sign_based"
    ayanamsha_sensitive: bool = False
    school_specific: dict = field(default_factory=dict)
    remedy: list[str] = field(default_factory=list)
    evaluation_method: str = "placement_check"
    last_modified_session: str = ""

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"RuleRecord {self.rule_id}: confidence={self.confidence} must be [0,1]"
            )

    def to_dict(self) -> dict:
        return asdict(self)
