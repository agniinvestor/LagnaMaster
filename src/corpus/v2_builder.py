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
        derived_house_chains: list[dict] | None = None,
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
            derived_house_chains=derived_house_chains if derived_house_chains is not None else self._auto_bb_chains(conditions),
            convergence_signals=convergence_signals or [],
            rule_relationship=rule_relationship or {},
        ))
        return rid

    def mirror(self, source_rid: str, *,
               direction: str | None = None,
               predictions: list[dict] | None = None,
               description: str | None = None,
               signal_group: str | None = None) -> str:
        """Generate a contrary mirror rule from an existing rule.

        Inverts direction and prediction directions. Links both rules
        via rule_relationship. Returns the new mirror's rule_id.

        Args:
            source_rid: rule_id of the source rule to mirror
            direction: override direction (default: auto-invert)
            predictions: override predictions (default: auto-invert)
            description: override description (default: prefix with 'Contrary:')
            signal_group: override signal_group (default: source + '_mirror')
        """
        # Find source rule
        source = None
        for r in self._rules:
            if r.rule_id == source_rid:
                source = r
                break
        if source is None:
            raise ValueError(f"mirror(): source rule {source_rid} not found")

        # Invert direction
        _DIR_INVERT = {
            "favorable": "unfavorable",
            "unfavorable": "favorable",
            "mixed": "mixed",
            "neutral": "neutral",
        }
        new_dir = direction or _DIR_INVERT.get(source.outcome_direction, "mixed")

        # Invert predictions
        if predictions is not None:
            new_preds = predictions
        else:
            new_preds = []
            for p in source.predictions:
                inv_p = dict(p)
                inv_p["direction"] = _DIR_INVERT.get(p.get("direction", ""), "mixed")
                inv_p["claim"] = "contrary_" + inv_p.get("claim", "")
                new_preds.append(inv_p)

        # Generate new description
        new_desc = description or f"Contrary: {source.description.replace('[BPHS — ' + self.category + '] ', '')}"

        # Generate new signal group
        new_sg = signal_group or source.signal_group + "_mirror"

        rid = f"BPHS{self._num:04d}"
        self._num += 1

        # Link both rules
        mirror_rel = {"type": "contrary_mirror", "related_rules": [source_rid]}

        # Update source rule's relationship too
        if not source.rule_relationship:
            source.rule_relationship = {"type": "alternative", "related_rules": [rid]}
        else:
            existing = source.rule_relationship.get("related_rules", [])
            if rid not in existing:
                existing.append(rid)
                source.rule_relationship["related_rules"] = existing

        self._rules.append(RuleRecord(
            rule_id=rid, source=source.source, chapter=source.chapter,
            school=source.school, category=source.category,
            description=f"[BPHS — {self.category}] {new_desc}",
            confidence=source.confidence, tags=source.tags, implemented=False,
            primary_condition=source.primary_condition,
            modifiers=source.modifiers, exceptions=source.exceptions,
            outcome_domains=source.outcome_domains,
            outcome_direction=new_dir, outcome_intensity=source.outcome_intensity,
            outcome_timing=source.outcome_timing,
            lagna_scope=source.lagna_scope, dasha_scope=source.dasha_scope,
            verse_ref=source.verse_ref,
            concordance_texts=source.concordance_texts,
            divergence_notes=source.divergence_notes,
            phase=source.phase, system=source.system,
            prediction_type=source.prediction_type,
            gender_scope=source.gender_scope,
            certainty_level=source.certainty_level,
            strength_condition=source.strength_condition,
            house_system=source.house_system,
            ayanamsha_sensitive=source.ayanamsha_sensitive,
            evaluation_method=source.evaluation_method,
            last_modified_session=self.session,
            predictions=new_preds, entity_target=source.entity_target,
            signal_group=new_sg,
            commentary_context=source.commentary_context,
            cross_chapter_refs=source.cross_chapter_refs,
            timing_window=source.timing_window,
            functional_modulation=source.functional_modulation,
            derived_house_chains=source.derived_house_chains,
            convergence_signals=source.convergence_signals,
            rule_relationship=mirror_rel,
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
    def _auto_bb_chains(conditions: list[dict]) -> list[dict]:
        """Auto-compute BB chains from conditions using bb_reference.

        This is DETERMINISTIC — BB chains are a function of the house number,
        not the source text. The encoder can override by passing explicit
        derived_house_chains=[...] to add().
        """
        try:
            from src.corpus.bb_reference import get_primary_bb_chains
        except ImportError:
            return []

        for cond in conditions:
            ct = cond.get("type", "")
            if ct in ("planet_in_house", "lord_in_house"):
                hv = cond.get("house", None)
                if isinstance(hv, int) and 1 <= hv <= 12:
                    return get_primary_bb_chains(hv, max_chains=3)
        return []

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
