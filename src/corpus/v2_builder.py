"""src/corpus/v2_builder.py — Shared V2 rule builder for all chapter files.

Extracts the common builder logic so chapter files contain ONLY data.

Usage:
    from src.corpus.v2_builder import V2ChapterBuilder

    b = V2ChapterBuilder(
        chapter="Ch.14", category="3rd_house_effects",
        id_start=1400, session="S311",
        chapter_tags=["3rd_house", "sahaj_bhava"],
        # Chapter-level defaults (overridable per rule):
        entity_target="siblings",
        prediction_type="event",
    )

    b.add(
        conditions=[{"type": "planet_in_house", "planet": "Sun", "house": 3}],
        signal_group="sun_h3_elder_loss",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[{"entity": "siblings", "claim": "elder_destroyed", ...}],
        verse_ref="Ch.14 v.14",
        description="Sun in 3rd destroys the preborn...",
    )

    REGISTRY = b.build()
"""
from __future__ import annotations

from src.corpus.registry import CorpusRegistry
from src.corpus.rule_record import RuleRecord


class V2ChapterBuilder:
    """Builds V2-compliant RuleRecord objects for a single BPHS chapter."""

    def __init__(
        self,
        *,
        chapter: str,
        category: str,
        id_start: int,
        session: str,
        source: str = "BPHS",
        school: str = "parashari",
        system: str = "natal",
        chapter_tags: list[str] | None = None,
        # Chapter-level defaults (overridable per rule)
        entity_target: str = "native",
        prediction_type: str = "event",
        timing_window: dict | None = None,
    ):
        self.chapter = chapter
        self.category = category
        self.source = source
        self.school = school
        self.system = system
        self.session = session
        self.chapter_tags = chapter_tags or []
        self._default_entity = entity_target
        self._default_pred_type = prediction_type
        self._default_timing = timing_window or {"type": "unspecified"}
        self._num = id_start
        self._rules: list[RuleRecord] = []

    def add(
        self,
        *,
        conditions: list[dict],
        signal_group: str,
        direction: str,
        intensity: str,
        domains: list[str],
        predictions: list[dict],
        verse_ref: str,
        description: str,
        # Optional overrides
        entity_target: str | None = None,
        timing_window: dict | None = None,
        prediction_type: str | None = None,
        commentary_context: str = "",
        concordance_texts: list[str] | None = None,
        divergence_notes: str = "",
        cross_chapter_refs: list[str] | None = None,
        rule_relationship: dict | None = None,
        derived_house_chain: dict | None = None,
        convergence_signals: list[str] | None = None,
        tags: list[str] | None = None,
        modifiers: list[dict] | None = None,
        exceptions: list[str] | None = None,
        lagna_scope: list[str] | None = None,
    ) -> str:
        """Add a rule. Returns the generated rule_id."""
        rid = f"BPHS{self._num:04d}"
        self._num += 1

        conc = concordance_texts or []
        div_count = len([x for x in divergence_notes.split(",") if x.strip()]) if divergence_notes else 0
        confidence = min(1.0, 0.60 + 0.05 + (0.08 * len(conc)) - (0.05 * div_count))

        has_lagna = bool(lagna_scope)
        has_conj = any(c.get("type", "").startswith("planets_conjunct") for c in conditions)
        phase = "1B_conditional" if has_lagna else ("1B_compound" if has_conj else "1B_matrix")

        pc = self._build_primary_condition(conditions)
        all_tags = list(dict.fromkeys(
            ["bphs", "parashari"] + self.chapter_tags + (tags or [])
        ))

        ent = entity_target if entity_target is not None else self._default_entity
        tw = timing_window if timing_window is not None else self._default_timing
        pt = prediction_type if prediction_type is not None else self._default_pred_type

        self._rules.append(RuleRecord(
            rule_id=rid, source=self.source, chapter=self.chapter,
            school=self.school, category=self.category,
            description=f"[BPHS — {self.category}] {description}",
            confidence=confidence, tags=all_tags, implemented=False,
            primary_condition=pc, modifiers=modifiers or [],
            exceptions=exceptions or [], outcome_domains=domains,
            outcome_direction=direction, outcome_intensity=intensity,
            outcome_timing="unspecified", lagna_scope=lagna_scope or [],
            dasha_scope=[], verse_ref=verse_ref,
            concordance_texts=conc, divergence_notes=divergence_notes,
            phase=phase, system=self.system, prediction_type=pt,
            gender_scope="universal", certainty_level="definite",
            strength_condition="any", house_system="sign_based",
            ayanamsha_sensitive=False, evaluation_method="lordship_check",
            last_modified_session=self.session,
            predictions=predictions, entity_target=ent,
            signal_group=signal_group, commentary_context=commentary_context,
            cross_chapter_refs=cross_chapter_refs or [],
            timing_window=tw, functional_modulation={},
            derived_house_chain=derived_house_chain or {},
            convergence_signals=convergence_signals or [],
            rule_relationship=rule_relationship or {},
        ))
        return rid

    def build(self) -> CorpusRegistry:
        """Build and return a CorpusRegistry with all added rules."""
        reg = CorpusRegistry()
        for rule in self._rules:
            reg.add(rule)
        return reg

    def rules(self) -> list[RuleRecord]:
        """Return the raw list of rules."""
        return list(self._rules)

    @staticmethod
    def _build_primary_condition(conditions: list[dict]) -> dict:
        """Build primary_condition with V2 conditions + legacy backward compat."""
        pc: dict = {"conditions": conditions}
        if not conditions:
            pc["planet"] = "general"
            pc["placement_type"] = "general_condition"
            return pc

        c0 = conditions[0]
        ct = c0.get("type", "")
        if ct == "planet_in_house":
            pc["planet"] = c0.get("planet", "")
            pc["placement_type"] = "house"
            pc["placement_value"] = c0.get("house", 0)
        elif ct == "lord_in_house":
            pc["planet"] = f"h{c0.get('lord_of', 0)}_lord"
            pc["placement_type"] = "lordship_placement"
            pc["placement_value"] = c0.get("house", 0)
        elif ct == "planet_in_sign":
            pc["planet"] = c0.get("planet", "")
            pc["placement_type"] = "sign_placement"
            pc["placement_value"] = c0.get("sign", "")
        elif ct == "planet_dignity":
            pc["planet"] = c0.get("planet", "")
            pc["placement_type"] = "lordship_dignity_condition"
        elif ct == "planets_conjunct":
            pc["planet"] = "_".join(c0.get("planets", []))
            pc["placement_type"] = "conjunction_condition"
        elif ct == "planets_conjunct_in_house":
            pc["planet"] = "_".join(c0.get("planets", []))
            pc["placement_type"] = "conjunction_in_house"
            pc["placement_value"] = c0.get("house", 0)
        elif ct == "planet_aspecting":
            pc["planet"] = c0.get("planet", "")
            pc["placement_type"] = "aspect_condition"
        else:
            pc["planet"] = c0.get("planet", "general")
            pc["placement_type"] = ct
        return pc
