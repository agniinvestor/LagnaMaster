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
    """Builds V2-compliant RuleRecord objects for a single BPHS chapter.

    Enforces depth at build time — PRINCIPLE-BASED, not threshold-based:
      - sloka_count is REQUIRED — declares how many predictive slokas the chapter has
      - build() REFUSES if rules/slokas ratio is catastrophically low (< 0.3)
        This catches summarization (6 rules from 22 slokas) but doesn't anchor to a target.
      - build() checks that EVERY rule has commentary_context populated
        (even "No Santhanam note for this sloka" counts — it proves the note was checked)
      - Concordance is NOT threshold-gated — the encoder checks honestly, some rules
        genuinely have no parallel in other texts

    The standard is the 10 principles, not these numbers.
    """

    # Safety net — catches catastrophic failure only, NOT the standard to work toward
    MIN_RATIO = 0.3         # only catches extreme summarization (L001, L003)

    def __init__(
        self,
        *,
        chapter: str,
        category: str,
        id_start: int,
        session: str,
        sloka_count: int,          # REQUIRED — number of predictive slokas
        source: str = "BPHS",
        school: str = "parashari",
        system: str = "natal",
        chapter_tags: list[str] | None = None,
        # Safety net override (only for genuinely sparse texts)
        min_ratio: float | None = None,
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
        self.sloka_count = sloka_count

        # T1-8: Source text canonicalization
        from src.corpus.source_texts import VALID_SOURCE_NAMES, get_source_info
        if source not in VALID_SOURCE_NAMES:
            raise ValueError(f"T1-8: source='{source}' not in canonical registry. "
                           f"Valid: {sorted(VALID_SOURCE_NAMES)}")
        source_info = get_source_info(source)
        self._translator = source_info.get("translator", "") if source_info else ""
        self._min_ratio = min_ratio if min_ratio is not None else self.MIN_RATIO
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
        # ── Tier 1 validation (build-time) ──────────────────────────────
        ent = entity_target if entity_target is not None else self._default_entity
        self._validate_add(conditions, direction, intensity, domains, predictions,
                           description=description, entity_target=ent,
                           commentary_context=commentary_context,
                           modifiers=modifiers or [])

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
            # Governance Tier 2 auto-derived fields
            translator=getattr(self, '_translator', ''),
            schema_version=2,
            health_sensitive=self._derive_health_sensitive(domains, direction),
            safety_tier="restricted" if self._derive_health_sensitive(domains, direction) else "standard",
            falsifiable=True,
            requires_entity_consent=self._derive_requires_consent(ent),
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
        """Build and return a CorpusRegistry with all added rules.

        REFUSES to build if depth thresholds are not met:
          - rules/slokas ratio >= MIN_RATIO
          - commentary coverage >= MIN_COMMENTARY
          - concordance coverage >= MIN_CONCORDANCE

        Raises ValueError with specific failures if thresholds not met.
        """
        n = len(self._rules)
        failures: list[str] = []

        # Verse audit file check — chapter cannot ship without audit
        # Enforced from S313 onward. Existing chapters grandfathered until
        # their verse audits are created.
        import re as _re
        ch_num_match = _re.search(r'Ch\.(\d+)', self.chapter)
        if ch_num_match and self.session >= "S313":
            from pathlib import Path
            ch_num = ch_num_match.group(1)
            audit_path = Path(f"data/verse_audits/ch{ch_num}_audit.json")
            if not audit_path.exists():
                failures.append(
                    f"AUDIT FAIL: No verse audit file at {audit_path}. "
                    f"Read the PDF, create the audit file listing every claim "
                    f"per verse, THEN encode. See CLAUDE.md Encoding Protocol."
                )

        # Ratio check
        if self.sloka_count > 0:
            ratio = n / self.sloka_count
            if ratio < self._min_ratio:
                failures.append(
                    f"DEPTH FAIL: {n} rules from {self.sloka_count} slokas "
                    f"(ratio {ratio:.2f} < {self._min_ratio}). "
                    f"Re-read the source text — you are summarizing."
                )

        # Commentary check — PRINCIPLE-BASED: every rule must have commentary
        # Even "No Santhanam note for this sloka" counts — it proves the note was checked.
        # Empty string means the encoder didn't check. That's the failure.
        if n > 0:
            missing_commentary = [
                r for r in self._rules if not r.commentary_context
            ]
            if missing_commentary:
                missing_ids = [r.rule_id for r in missing_commentary[:5]]
                failures.append(
                    f"PRINCIPLE FAIL: {len(missing_commentary)} rules have empty "
                    f"commentary_context ({', '.join(missing_ids)}{'...' if len(missing_commentary) > 5 else ''}). "
                    f"Every rule must have commentary — even 'No Santhanam note "
                    f"for this sloka' proves the note was checked. Empty means "
                    f"you didn't check."
                )

        # Concordance — NO threshold. The encoder checks honestly.
        # Some rules genuinely have no parallel. That's fine.
        # But we log the coverage for the scorecard.

        # Sloka coverage verification — verse_refs should span the declared range
        if n > 0 and self.sloka_count > 0:
            import re
            verse_nums: set[int] = set()
            for r in self._rules:
                # Extract verse numbers from "Ch.N v.M" or "Ch.N v.M-P"
                matches = re.findall(r'v\.(\d+)', r.verse_ref)
                for m in matches:
                    verse_nums.add(int(m))
            if verse_nums:
                max_verse = max(verse_nums)
                if max_verse < self.sloka_count * 0.5:
                    failures.append(
                        f"SLOKA COVERAGE FAIL: declared {self.sloka_count} slokas "
                        f"but verse_refs only reach v.{max_verse}. "
                        f"You are skipping the second half of the chapter."
                    )

        # Commentary uniqueness — no copy-paste
        if n > 2:
            commentaries = [r.commentary_context for r in self._rules
                           if r.commentary_context]
            if commentaries:
                from collections import Counter
                dupes = Counter(commentaries)
                repeated = [(c[:50], count) for c, count in dupes.items() if count > 2]
                if repeated:
                    failures.append(
                        f"COMMENTARY FAIL: copy-pasted commentary detected — "
                        f"'{repeated[0][0]}...' appears {repeated[0][1]} times. "
                        f"Each sloka has different notes."
                    )

        if failures:
            raise ValueError(
                f"\n{self.chapter} ({self.category}) CANNOT SHIP:\n"
                + "\n".join(f"  ✗ {f}" for f in failures)
                + f"\n\nThis chapter has {self.sloka_count} predictive slokas. "
                f"You produced {n} rules. Fix the depth before calling build()."
            )

        reg = CorpusRegistry()
        for rule in self._rules:
            reg.add(rule)
        return reg

    def rules(self) -> list[RuleRecord]:
        """Return the raw list of rules."""
        return list(self._rules)

    @staticmethod
    def _validate_add(conditions, direction, intensity, domains, predictions,
                      *, description="", entity_target="native",
                      commentary_context="", modifiers=None):
        """Tier 1 build-time validation — encoding quality gates enforced here."""
        from src.corpus.taxonomy import (
            VALID_OUTCOME_DOMAINS, VALID_OUTCOME_DIRECTIONS,
            VALID_OUTCOME_INTENSITIES, VALID_CONDITION_PRIMITIVES,
            VALID_ENTITY_TARGETS,
        )
        errors = []

        # T1-1: Condition primitive whitelist
        for i, cond in enumerate(conditions):
            ctype = cond.get("type", "")
            if ctype and ctype not in VALID_CONDITION_PRIMITIVES:
                errors.append(
                    f"T1-1: conditions[{i}].type='{ctype}' not a valid primitive — "
                    f"use: {sorted(VALID_CONDITION_PRIMITIVES)}"
                )

        # T1-1 extended: validate new condition primitives' sub-fields
        for i, cond in enumerate(conditions):
            ctype = cond.get("type", "")

            if ctype == "planet_in_sign_type":
                from src.corpus.taxonomy import VALID_SIGN_TYPES
                st = cond.get("sign_type", "")
                if not st or st not in VALID_SIGN_TYPES:
                    errors.append(
                        f"T1-1: conditions[{i}].sign_type='{st}' not valid — "
                        f"use: {sorted(VALID_SIGN_TYPES)}"
                    )
                if not cond.get("planet"):
                    errors.append(f"T1-1: conditions[{i}] planet_in_sign_type missing 'planet'")

            elif ctype == "planet_in_derived_house":
                from src.corpus.taxonomy import VALID_DERIVATIONS, VALID_CONDITION_MODES
                deriv = cond.get("derivation", "")
                if not deriv or deriv not in VALID_DERIVATIONS:
                    errors.append(
                        f"T1-1: conditions[{i}].derivation='{deriv}' not valid — "
                        f"use: {sorted(VALID_DERIVATIONS)}"
                    )
                offset = cond.get("offset")
                if not isinstance(offset, int) or not (1 <= offset <= 12):
                    errors.append(
                        f"T1-1: conditions[{i}].offset={offset} must be int 1-12"
                    )
                if not cond.get("planet"):
                    errors.append(f"T1-1: conditions[{i}] planet_in_derived_house missing 'planet'")
                mode = cond.get("mode", "occupies")
                if mode not in VALID_CONDITION_MODES:
                    errors.append(
                        f"T1-1: conditions[{i}].mode='{mode}' not valid — "
                        f"use: {sorted(VALID_CONDITION_MODES)}"
                    )
                # base_house required for house-based derivations
                _HOUSE_BASED = {"arudha_pada", "upa_pada"}
                if deriv in _HOUSE_BASED and not isinstance(cond.get("base_house"), int):
                    errors.append(
                        f"T1-1: conditions[{i}] derivation='{deriv}' requires base_house (int 1-12)"
                    )

            elif ctype == "upagraha_in_house":
                from src.corpus.taxonomy import VALID_UPAGRAHAS, VALID_CONDITION_MODES
                upa = cond.get("upagraha", "")
                if not upa or upa not in VALID_UPAGRAHAS:
                    errors.append(
                        f"T1-1: conditions[{i}].upagraha='{upa}' not valid — "
                        f"use: {sorted(VALID_UPAGRAHAS)}"
                    )
                house = cond.get("house")
                if not isinstance(house, int) or not (1 <= house <= 12):
                    errors.append(
                        f"T1-1: conditions[{i}].house={house} must be int 1-12"
                    )
                mode = cond.get("mode", "occupies")
                if mode not in VALID_CONDITION_MODES:
                    errors.append(
                        f"T1-1: conditions[{i}].mode='{mode}' not valid — "
                        f"use: {sorted(VALID_CONDITION_MODES)}"
                    )

        # T1-2: Controlled vocabulary — domains, direction, intensity
        for d in domains:
            if d not in VALID_OUTCOME_DOMAINS:
                errors.append(f"T1-2: outcome_domain '{d}' not in taxonomy")
        if direction not in VALID_OUTCOME_DIRECTIONS:
            errors.append(f"T1-2: direction '{direction}' not valid")
        if intensity not in VALID_OUTCOME_INTENSITIES:
            errors.append(f"T1-2: intensity '{intensity}' not valid")

        # T1-3: Planet name normalization — canonical forms
        _CANONICAL_PLANETS = {
            "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn",
            "rahu", "ketu", "any_benefic", "any_malefic", "any_planet",
            "general", "lord_of_1", "lord_of_2", "lord_of_3", "lord_of_4",
            "lord_of_5", "lord_of_6", "lord_of_7", "lord_of_8", "lord_of_9",
            "lord_of_10", "lord_of_11", "lord_of_12",
        }
        for i, cond in enumerate(conditions):
            planet = cond.get("planet", "")
            if planet and planet.lower() not in _CANONICAL_PLANETS:
                # Allow h{N}_lord format and multi-planet conjunctions
                if not (planet.startswith("h") and "_lord" in planet):
                    if "_" not in planet:  # not a conjunction pair
                        errors.append(
                            f"T1-3: conditions[{i}].planet='{planet}' not canonical"
                        )

        # T1-13: Claim minimum length and specificity
        _GENERIC_CLAIMS = {
            "good", "bad", "favorable", "unfavorable", "wealthy", "poor",
            "happy", "unhappy", "positive", "negative", "beneficial",
            "malefic", "benefic", "test", "general",
        }
        for i, pred in enumerate(predictions):
            if not isinstance(pred, dict):
                continue
            claim = pred.get("claim", "")
            if len(claim) < 10:
                errors.append(f"T1-13: predictions[{i}].claim='{claim}' too short ({len(claim)} < 10)")
            if claim.lower().strip("_") in _GENERIC_CLAIMS:
                errors.append(f"T1-13: predictions[{i}].claim='{claim}' is generic")
            # Validate prediction entity
            ent = pred.get("entity", "")
            if ent and ent not in VALID_ENTITY_TARGETS:
                errors.append(f"T1-2: predictions[{i}].entity='{ent}' not valid")

        # T1-14: Entity_target vs description — Q6 from encoding checklist
        # If description says "wife will X" or "sons inimical", entity_target
        # must match the entity whose fate is being predicted.
        # Exclusions: patterns that LOOK like other-entity subjects but aren't
        _POSSESSION_CONTEXT = ["wife will give birth", "wife will bear"]
        _SUBJECT_PATTERNS = {
            "spouse": ["wife will", "wife not ", "wife incur", "wife diseased",
                       "wife destroyed", "wife predecease", "spouse will",
                       "wife sickly", "wife spendthrift", "wife subdued",
                       "wife disobedient", "wife wicked"],
            "father": ["father will", "father pass", "father lost",
                       "father die", "father destroyed"],
            "mother": ["mother will", "mother lost", "mother die",
                       "mother destroyed", "lose mother"],
            "children": ["sons inimical", "sons hostile", "sons will",
                         "children will", "lose children", "loss of children",
                         "child will", "eldest child will"],
            "siblings": ["co-born destroyed", "co-born will"],
        }
        desc_lower = description.lower()
        # Skip if a possession-context pattern matches (e.g., "wife will give birth" is about progeny, not spouse)
        is_possession = any(pc in desc_lower for pc in _POSSESSION_CONTEXT)
        if not is_possession:
            for target_entity, patterns in _SUBJECT_PATTERNS.items():
                for p in patterns:
                    if p in desc_lower:
                        if entity_target not in (target_entity, "general"):
                            errors.append(
                                f"T1-14: description says '{p}' but entity_target='{entity_target}' — "
                                f"should be '{target_entity}' (Q6: whose fate is predicted?)"
                            )
                        break

        # T1-15: Mixed-entity split — Q7 from encoding checklist
        # If description has subject-verb patterns for TWO different entities,
        # the rule should be split (granularity principle #2).
        detected_subjects = set()
        for target_entity, patterns in _SUBJECT_PATTERNS.items():
            for p in patterns:
                if p in desc_lower:
                    detected_subjects.add(target_entity)
                    break
        if len(detected_subjects) > 1:
            errors.append(
                f"T1-15: description mentions {detected_subjects} as prediction subjects — "
                f"split into separate rules per entity (granularity principle #2)"
            )

        # T1-16: Atomic prediction claims — Q8 from encoding checklist
        for i, pred in enumerate(predictions):
            if not isinstance(pred, dict):
                continue
            claim = pred.get("claim", "")
            # Bundled claims with _and_ joining different outcomes
            if "_and_" in claim and len(claim) > 60:
                errors.append(
                    f"T1-16: predictions[{i}].claim is bundled (contains '_and_', "
                    f"len={len(claim)}) — split into atomic claims"
                )

        # T1-17: Prediction entity must match entity_target — Q8 consistency
        for i, pred in enumerate(predictions):
            if not isinstance(pred, dict):
                continue
            pred_ent = pred.get("entity", "")
            if pred_ent and entity_target != "general" and pred_ent != entity_target:
                errors.append(
                    f"T1-17: predictions[{i}].entity='{pred_ent}' does not match "
                    f"entity_target='{entity_target}' — fix entity or set target='general'"
                )

        # T1-18: Modifier quality — effect vocabulary and condition specificity
        _VALID_EFFECTS = {"amplifies", "negates", "conditionalizes"}
        if modifiers is None:
            modifiers = []
        for i, mod in enumerate(modifiers):
            if not isinstance(mod, dict):
                continue
            effect = mod.get("effect", "")
            if effect and effect not in _VALID_EFFECTS:
                errors.append(
                    f"T1-18: modifiers[{i}].effect='{effect}' not valid — "
                    f"use: {sorted(_VALID_EFFECTS)}"
                )
            cond = mod.get("condition", "")
            if cond and len(cond) < 15:
                errors.append(
                    f"T1-18: modifiers[{i}].condition='{cond}' too short "
                    f"({len(cond)} < 15) — describe what the text actually states"
                )

        # T1-19: Conditional language in commentary without modifiers — Q9
        if commentary_context and not modifiers:
            comm_lower = commentary_context.lower()
            _CONDITIONAL_KW = ["if ", "unless ", "except ", "however,", "but if ",
                               "provided ", "only when "]
            has_conditional = any(kw in comm_lower for kw in _CONDITIONAL_KW)
            if has_conditional:
                # Check if exceptions or rule_relationship handle it
                # (can't check here — those aren't passed to _validate_add)
                # So this is advisory, not blocking
                pass  # Handled by scorecard and maturity grader, not builder

        if errors:
            raise ValueError(
                "V2 BUILD VALIDATION FAILED:\n" +
                "\n".join(f"  ✗ {e}" for e in errors)
            )

    @staticmethod
    def _derive_health_sensitive(domains, direction):
        """Derive health_sensitive flag from domains and direction (G02)."""
        health_domains = {"longevity", "physical_health", "mental_health"}
        has_health = bool(set(domains) & health_domains)
        is_negative = direction in ("unfavorable", "mixed")
        return has_health and is_negative

    @staticmethod
    def _derive_requires_consent(entity_target):
        """Derive requires_entity_consent from entity_target (G03)."""
        return entity_target in ("father", "mother", "spouse", "children", "siblings")

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
        elif ct in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
            pc["planet"] = c0.get("planet", c0.get("upagraha", "general"))
            pc["placement_type"] = ct
        else:
            pc["planet"] = c0.get("planet", "general")
            pc["placement_type"] = ct
        return pc
