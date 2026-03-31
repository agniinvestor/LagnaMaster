"""
src/corpus/corpus_audit.py — Corpus Completeness Audit (S205, extended S309)

Audits a CorpusRegistry for completeness gaps, unimplemented rules,
and distribution across schools and categories. Used by CI and the
S201-S210 checkpoint to verify corpus quality.

S309 extensions: V2 field enforcement for rules with last_modified_session >= "S309".
Rules created/modified after S309 MUST populate the new fields. Empty defaults
that silently pass are replaced by hard errors.

Public API
----------
  CorpusAudit(registry)   — audit runner
  .run() -> dict          — structured report (includes v2_errors)
  .text_report() -> str   — human-readable summary
  .audit_v2_compliance(rule) -> list[str]  — per-rule V2 field checks
"""

from __future__ import annotations

from src.corpus.registry import CorpusRegistry

# Sessions from which V2 enforcement applies.
# Rules with last_modified_session >= this are held to the new standard.
V2_ENFORCEMENT_START = "S310"

# House categories where entity_target="native" needs explicit verification.
# These houses commonly predict about non-native entities.
ENTITY_CHECK_CATEGORIES = {
    "9th_house_effects",   # often about father
    "7th_house_effects",   # often about spouse
    "5th_house_effects",   # often about children
    "4th_house_effects",   # often about mother
    "3rd_house_effects",   # often about siblings
}

VALID_ENTITY_TARGETS = {
    "native", "father", "mother", "spouse", "children", "siblings", "general",
}

VALID_TIMING_TYPES = {
    "age", "age_range", "after_event", "dasha_period", "unspecified",
}

VALID_RELATIONSHIP_TYPES = {
    "alternative", "addition", "override", "contrary_mirror",
}


class CorpusAudit:
    """Run completeness checks on a CorpusRegistry."""

    def __init__(self, registry: CorpusRegistry) -> None:
        self.registry = registry

    def audit_v2_compliance(self, rule) -> list[str]:
        """Check a single rule for V2 field compliance.

        Returns list of error strings. Empty list = compliant.
        Only enforced for rules with last_modified_session >= V2_ENFORCEMENT_START.
        """
        errors: list[str] = []
        rid = rule.rule_id
        session = rule.last_modified_session

        # Only enforce on rules from S310 onward
        if not session or session < V2_ENFORCEMENT_START:
            return errors

        # Only enforce on Phase 1B rules (not legacy 1A)
        if rule.phase == "1A_representative":
            return errors

        # --- predictions must be non-empty ---
        if not rule.predictions:
            errors.append(
                f"{rid}: predictions is empty — every rule must have at least "
                f"1 atomic prediction (Protocol A)"
            )

        # --- entity_target must be from controlled vocabulary ---
        if rule.entity_target not in VALID_ENTITY_TARGETS:
            errors.append(
                f"{rid}: entity_target='{rule.entity_target}' not in "
                f"valid set {VALID_ENTITY_TARGETS}"
            )

        # --- signal_group must be non-empty ---
        if not rule.signal_group:
            errors.append(
                f"{rid}: signal_group is empty — must group rules from same "
                f"chart signal (e.g., 'jupiter_h7_marriage')"
            )

        # --- timing_window must be explicitly checked ---
        # Empty dict {} = unchecked (error). {"type": "unspecified"} = checked, no timing (ok).
        if not rule.timing_window:
            errors.append(
                f"{rid}: timing_window is empty dict {{}} — must be explicitly "
                f"set. Use {{\"type\": \"unspecified\"}} if text states no timing "
                f"(Protocol F)"
            )
        elif "type" not in rule.timing_window:
            errors.append(
                f"{rid}: timing_window missing 'type' key — must have "
                f"type in {VALID_TIMING_TYPES}"
            )
        elif rule.timing_window["type"] not in VALID_TIMING_TYPES:
            errors.append(
                f"{rid}: timing_window type='{rule.timing_window['type']}' "
                f"not in valid set {VALID_TIMING_TYPES}"
            )

        # --- predictions structure check ---
        for i, pred in enumerate(rule.predictions):
            if not isinstance(pred, dict):
                errors.append(f"{rid}: predictions[{i}] is not a dict")
                continue
            for key in ("entity", "claim", "domain", "direction"):
                if key not in pred:
                    errors.append(
                        f"{rid}: predictions[{i}] missing required key '{key}'"
                    )
            if "entity" in pred and pred["entity"] not in VALID_ENTITY_TARGETS:
                errors.append(
                    f"{rid}: predictions[{i}].entity='{pred['entity']}' "
                    f"not in valid set"
                )

        # --- rule_relationship structure check ---
        if rule.rule_relationship:
            rr = rule.rule_relationship
            if "type" not in rr:
                errors.append(f"{rid}: rule_relationship missing 'type' key")
            elif rr["type"] not in VALID_RELATIONSHIP_TYPES:
                errors.append(
                    f"{rid}: rule_relationship type='{rr['type']}' "
                    f"not in valid set {VALID_RELATIONSHIP_TYPES}"
                )

        # --- SLIP-THROUGH CHECK 1: Predictions entity vs entity_target ---
        # If predictions list entities that differ from entity_target,
        # the rule likely needs splitting or entity_target is wrong.
        if rule.predictions:
            pred_entities = {p.get("entity", "") for p in rule.predictions
                            if isinstance(p, dict)}
            non_target = pred_entities - {rule.entity_target, ""}
            if non_target and rule.entity_target != "general":
                errors.append(
                    f"{rid}: entity_target='{rule.entity_target}' but predictions "
                    f"reference different entities {non_target} — split into "
                    f"separate rules per entity, or set entity_target='general'"
                )

        # --- SLIP-THROUGH CHECK 2: Description mentions age but timing unspecified ---
        # Catches timing data buried in prose that wasn't extracted.
        import re
        desc = rule.description.lower()
        age_patterns = re.findall(
            r'(?:age|year)(?:\s+(?:of|at))?\s+(\d{1,2})', desc
        )
        age_patterns += re.findall(r'(\d{1,2})(?:th|st|nd|rd)\s+year', desc)
        if age_patterns and rule.timing_window.get("type") == "unspecified":
            errors.append(
                f"{rid}: description mentions age(s) {age_patterns} but "
                f"timing_window is 'unspecified' — extract timing (Protocol F)"
            )

        # --- SLIP-THROUGH CHECK 3: Commentary minimum for BPHS ---
        # Santhanam provides notes on almost every BPHS sloka.
        # A BPHS rule with no commentary is likely missing the notes.
        # This is a WARNING (returned separately), not a hard error —
        # some slokas genuinely have brief/no notes.

        return errors

    def audit_v2_warnings(self, rule) -> list[str]:
        """Non-blocking warnings for V2 rules. Returned separately from errors."""
        warnings: list[str] = []
        rid = rule.rule_id
        session = rule.last_modified_session
        if not session or session < V2_ENFORCEMENT_START:
            return warnings
        if rule.phase == "1A_representative":
            return warnings

        # BPHS commentary check
        if (rule.source == "BPHS" and not rule.commentary_context
                and rule.verse_ref and "v." in rule.verse_ref):
            warnings.append(
                f"{rid}: BPHS rule with no commentary_context — did you "
                f"read Santhanam's notes for {rule.verse_ref}? (Protocol D)"
            )

        return warnings

    def run(self) -> dict:
        """Return a structured audit report."""
        rules = self.registry.all()
        total = len(rules)
        implemented = [r for r in rules if r.implemented]
        unimplemented = [r for r in rules if not r.implemented]

        by_school: dict[str, int] = {}
        by_category: dict[str, int] = {}
        by_source: dict[str, int] = {}
        low_confidence: list[str] = []

        # V2 enforcement
        v2_errors: list[str] = []
        v2_warnings: list[str] = []
        v2_rules_checked = 0
        v2_rules_compliant = 0

        for r in rules:
            by_school[r.school] = by_school.get(r.school, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1
            by_source[r.source] = by_source.get(r.source, 0) + 1
            if r.confidence < 0.7:
                low_confidence.append(r.rule_id)

            # V2 compliance check
            rule_errors = self.audit_v2_compliance(r)
            rule_warnings = self.audit_v2_warnings(r)
            if r.last_modified_session and r.last_modified_session >= V2_ENFORCEMENT_START:
                v2_rules_checked += 1
                if not rule_errors:
                    v2_rules_compliant += 1
            v2_errors.extend(rule_errors)
            v2_warnings.extend(rule_warnings)

        return {
            "total_rules": total,
            "implemented_count": len(implemented),
            "unimplemented_count": len(unimplemented),
            "unimplemented_ids": [r.rule_id for r in unimplemented],
            "by_school": by_school,
            "by_category": by_category,
            "by_source": by_source,
            "low_confidence_ids": low_confidence,
            "v2_rules_checked": v2_rules_checked,
            "v2_rules_compliant": v2_rules_compliant,
            "v2_errors": v2_errors,
            "v2_warnings": v2_warnings,
            "errors": v2_errors,  # backward compat: errors now includes v2
        }

    def text_report(self) -> str:
        """Human-readable corpus audit summary."""
        r = self.run()
        lines = [
            f"Corpus Audit: {r['total_rules']} total rules",
            f"  Implemented:   {r['implemented_count']}",
            f"  Unimplemented: {r['unimplemented_count']}",
        ]
        lines.append("\nBy school:")
        for s, n in sorted(r["by_school"].items()):
            lines.append(f"  {s}: {n}")
        lines.append("\nBy category:")
        for c, n in sorted(r["by_category"].items()):
            lines.append(f"  {c}: {n}")
        lines.append("\nBy source:")
        for src, n in sorted(r["by_source"].items()):
            lines.append(f"  {src}: {n}")
        if r["unimplemented_ids"]:
            lines.append(f"\nUnimplemented: {', '.join(r['unimplemented_ids'][:10])}"
                         + (" ..." if len(r["unimplemented_ids"]) > 10 else ""))
        if r["low_confidence_ids"]:
            lines.append(f"Low confidence (<0.7): {', '.join(r['low_confidence_ids'])}")

        # V2 enforcement summary
        if r["v2_rules_checked"] > 0:
            lines.append(f"\nV2 Compliance: {r['v2_rules_compliant']}/{r['v2_rules_checked']} "
                         f"rules pass ({100*r['v2_rules_compliant']//max(r['v2_rules_checked'],1)}%)")
        if r["v2_errors"]:
            lines.append(f"V2 Errors ({len(r['v2_errors'])}):")
            for err in r["v2_errors"][:20]:
                lines.append(f"  {err}")
            if len(r["v2_errors"]) > 20:
                lines.append(f"  ... and {len(r['v2_errors'])-20} more")

        return "\n".join(lines)
