"""
src/corpus/rule_record.py — RuleRecord dataclass (S202→S263→S305→S309)

Machine-readable encoding of a classical Jyotish rule.
Each rule maps a classical text citation to a testable, computable predicate.

Three tiers:
  Phase 1A (S216–S262): Representative layer — prose descriptions, topic index.
    Fields: rule_id through engine_ref.
    All Phase 1A rules carry phase="1A_representative" automatically.

  Phase 1B (S263+): Sutra-level layer — structured predictions, ML-ready.
    Additional mandatory fields: primary_condition through system.
    Contract defined in docs/PHASE1B_RULE_CONTRACT.md.
    Outcome taxonomy defined in docs/PHASE1B_OUTCOME_TAXONOMY.md.

  S305 extensions: prediction_type, gender_scope, certainty_level,
    strength_condition, house_system, ayanamsha_sensitive, school_specific,
    remedy, evaluation_method, last_modified_session.

  S309 extensions (Corpus Standard Upgrade):
    predictions          — list of atomic, machine-parseable prediction claims
    entity_target        — WHO the prediction is about (native|father|spouse|...)
    signal_group         — groups rules from the same chart signal
    commentary_context   — translator's notes and practical interpretation
    cross_chapter_refs   — explicit links to other chapters
    timing_window        — structured timing (age, dasha, event)
    functional_modulation — how prediction changes by lagna functional role
    derived_house_chains — bhavat bhavam causal chains (list — a rule can participate in multiple)
    convergence_signals  — independent chart conditions that confirm prediction
    rule_relationship    — alternatives/overrides/additions between rules

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

    S309 extensions (Corpus Standard Upgrade)
    ------------------------------------------
    predictions         Atomic machine-parseable claims. Each dict:
                        {"entity": str, "claim": str, "domain": str,
                         "direction": str, "magnitude": float}
    entity_target       WHO this prediction is about:
                        native|father|mother|spouse|children|siblings|general
    signal_group        Groups rules from same chart observation, e.g. "jupiter_h7_marriage".
                        Engine counts each group once, not each rule independently.
    commentary_context  Translator's notes — practical interpretation not in the verse itself.
                        Santhanam's notes, edge cases, alternative readings.
    cross_chapter_refs  Explicit links to related chapters: ["Ch.44 Maraka", "Ch.83 Curses"]
    timing_window       Structured timing. Dict with:
                        {"type": "age"|"age_range"|"after_event"|"dasha_period"|"unspecified",
                         "value": ..., "precision": "exact"|"approximate"|"unspecified"}
    functional_modulation  How prediction changes by lagna functional role. Dict keyed by
                        functional role: {"yogakaraka": "...", "benefic": "...", "malefic": "..."}
    derived_house_chains   Bhavat bhavam causal chains. List of dicts — a rule can
                        participate in multiple BB chains simultaneously. Each:
                        {"base_house": int, "derivative": str, "effective_house": int,
                         "entity": str, "domain": str}
    convergence_signals    Independent chart conditions that confirm this prediction:
                        ["d9_7th_lord_in_jupiter_sign", "h7_ashtakavarga_above_28"]
    rule_relationship   Alternatives/overrides/additions between rules. Dict:
                        {"type": "alternative"|"addition"|"override"|"contrary_mirror",
                         "related_rules": ["BPHS0803"]}
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

    # ── S309 extensions (Corpus Standard Upgrade) ───────────────────────────
    predictions: list[dict] = field(default_factory=list)
    entity_target: str = "native"
    signal_group: str = ""
    commentary_context: str = ""
    cross_chapter_refs: list[str] = field(default_factory=list)
    timing_window: dict = field(default_factory=dict)
    functional_modulation: dict = field(default_factory=dict)
    derived_house_chains: list[dict] = field(default_factory=list)
    convergence_signals: list[str] = field(default_factory=list)
    rule_relationship: dict = field(default_factory=dict)

    # ── S311 extensions (Governance Framework — Tier 2 Foundations) ──────────
    translator: str = ""                    # Which translator's edition (e.g., "santhanam", "gc_sharma")
    schema_version: int = 2                 # Schema version (1=S202, 2=S309+)
    health_sensitive: bool = False           # G02: longevity/death/disease predictions flagged
    safety_tier: str = "standard"            # standard | restricted | research_only
    falsifiable: bool = True                 # Can a user confirm/deny this prediction?
    requires_entity_consent: bool = False    # G03: needs family member consent before display
    deprecated_reason: str = ""              # Non-empty = rule is deprecated, reason given
    encoding_session_context: str = ""      # Brief note on encoding context (e.g., "batch with Ch.15-19, PDF pp.142-169")

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"RuleRecord {self.rule_id}: confidence={self.confidence} must be [0,1]"
            )

    def to_dict(self) -> dict:
        return asdict(self)
