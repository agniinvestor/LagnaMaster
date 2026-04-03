"""tools/v2_scorecard.py — Exhaustive V2 encoding quality scorecard.

Scores any set of rules against ALL V2 dimensions. Produces a structured
report with metrics, red flags, and suggested fixes.

Usage:
  # Score a specific session's rules:
  .venv/bin/python tools/v2_scorecard.py --session S311

  # Score a specific corpus file:
  .venv/bin/python tools/v2_scorecard.py --file src/corpus/bphs_1b_houses_1.py

  # Score all V2 rules (last_modified_session >= S310):
  .venv/bin/python tools/v2_scorecard.py --v2-only

  # Score entire corpus:
  .venv/bin/python tools/v2_scorecard.py --all

  # Output as JSON (for CI integration):
  .venv/bin/python tools/v2_scorecard.py --session S311 --json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict

# Entity keywords for red-flag detection (keyword → likely entity)
_ENTITY_KEYWORDS = {
    "father": "father",
    "father's": "father",
    "paternal": "father",
    "patrimony": "father",
    "mother": "mother",
    "maternal": "mother",
    "mother's": "mother",
    "spouse": "spouse",
    "wife": "spouse",
    "husband": "spouse",
    "marriage": "spouse",
    "marital": "spouse",
    "conjugal": "spouse",
    "children": "children",
    "sons": "children",
    "daughters": "children",
    "progeny": "children",
    "child": "children",
    "offspring": "children",
    "brother": "siblings",
    "sister": "siblings",
    "co-born": "siblings",
    "siblings": "siblings",
}

# Houses that commonly predict about non-native entities
_HOUSE_ENTITY_MAP = {
    "3rd_house_effects": "siblings",
    "4th_house_effects": "mother",
    "5th_house_effects": "children",
    "7th_house_effects": "spouse",
    "9th_house_effects": "father",
}

# Bhavat bhavam: derivative houses and their expected entity/domain
_BHAVAT_BHAVAM = {
    # (house, category) → expected derived_house_chains fields
    (10, "9th_house_effects"): {"base_house": 9, "derivative": "2nd_from", "entity": "father", "domain": "wealth"},
    (12, "9th_house_effects"): {"base_house": 9, "derivative": "4th_from", "entity": "father", "domain": "property_vehicles"},
    (3, "9th_house_effects"): {"base_house": 9, "derivative": "7th_from", "entity": "father", "domain": "marriage"},
    (5, "9th_house_effects"): {"base_house": 9, "derivative": "9th_from", "entity": "father", "domain": "fortune"},
    (4, "7th_house_effects"): {"base_house": 7, "derivative": "10th_from", "entity": "spouse", "domain": "career_status"},
    (8, "7th_house_effects"): {"base_house": 7, "derivative": "2nd_from", "entity": "spouse", "domain": "wealth"},
    (9, "5th_house_effects"): {"base_house": 5, "derivative": "5th_from", "entity": "children", "domain": "progeny"},
    (6, "4th_house_effects"): {"base_house": 4, "derivative": "3rd_from", "entity": "mother", "domain": "siblings"},
}

VALID_TIMING_TYPES = {"age", "age_range", "after_event", "dasha_period", "unspecified"}
VALID_ENTITY_TARGETS = {"native", "father", "mother", "spouse", "children", "siblings", "general"}
VALID_RELATIONSHIP_TYPES = {"alternative", "addition", "override", "contrary_mirror"}

# Expected predictive verse counts per BPHS chapter (from coverage map).
# Source: actual reading of Santhanam translation, excluding definitional/intro slokas.
# This drives the verse coverage dimension — any chapter where
# rules_encoded < predictive_verses is flagged as incomplete.
_BPHS_PREDICTIVE_VERSES: dict[str, int] = {
    "12": 16, "13": 12, "14": 20, "15": 28, "16": 26, "17": 14,
    "18": 18, "19": 19, "20": 22, "21": 20, "22": 12, "23": 14,
    "24a": 80, "24b": 75, "24c": 80, "25": 90,
}

# Chapter → V2 corpus module name mapping
_BPHS_CHAPTER_MODULES: dict[str, str] = {
    ch: f"src.corpus.bphs_v2_ch{ch}" for ch in _BPHS_PREDICTIVE_VERSES
}


@dataclass
class RedFlag:
    """A quality issue with a suggested fix."""
    rule_id: str
    severity: str  # "error" | "warning" | "info"
    category: str
    message: str
    fix: str


@dataclass
class V2Scorecard:
    """Complete V2 quality scorecard for a set of rules."""
    # ── Identification ────────────────────────────────────────────────────
    label: str = ""
    total_rules: int = 0

    # ── A. Predictions (Gap 1) ────────────────────────────────────────────
    predictions_populated: int = 0
    predictions_empty: int = 0
    predictions_per_rule_mean: float = 0.0
    predictions_per_rule_min: int = 0
    predictions_per_rule_max: int = 0
    rules_with_many_predictions: int = 0  # >3 = potential summarization

    # ── B. Entity Target (Gap 2) ──────────────────────────────────────────
    entity_distribution: dict = field(default_factory=dict)
    entity_mismatch_count: int = 0  # description mentions X but entity says Y

    # ── C. Computable Conditions (Gap 3) ──────────────────────────────────
    has_v2_conditions: int = 0
    missing_v2_conditions: int = 0
    condition_types_used: dict = field(default_factory=dict)

    # ── D. Signal Groups (Gap 4) ──────────────────────────────────────────
    signal_groups_populated: int = 0
    signal_groups_empty: int = 0
    unique_signal_groups: int = 0
    signal_group_conflicts: int = 0  # same group, conflicting directions

    # ── E. One-Claim-One-Rule (Gap 5) ─────────────────────────────────────
    # (covered by predictions_per_rule_max and rules_with_many_predictions)

    # ── F. Commentary (Gap 6) ─────────────────────────────────────────────
    commentary_populated: int = 0
    commentary_empty: int = 0
    cross_chapter_refs_populated: int = 0
    total_cross_refs: int = 0

    # ── G. Timing (Gap 7) ─────────────────────────────────────────────────
    timing_populated: int = 0
    timing_unchecked: int = 0  # bare {} = didn't check
    timing_unspecified: int = 0  # {"type": "unspecified"} = checked, none found
    timing_type_distribution: dict = field(default_factory=dict)

    # ── H. Functional Modulation (Gap 8) ──────────────────────────────────
    functional_modulation_populated: int = 0
    functional_modulation_empty: int = 0

    # ── I. Bhavat Bhavam / Derived House Chain (Gap 9) ────────────────────
    derived_house_chains_populated: int = 0
    derived_house_chains_empty: int = 0
    bhavat_bhavam_expected: int = 0  # rules WHERE a chain is expected
    bhavat_bhavam_missing: int = 0   # expected but not populated

    # ── J. Convergence Signals (Gap 10) ───────────────────────────────────
    convergence_signals_populated: int = 0
    convergence_signals_empty: int = 0
    convergence_signals_per_rule_mean: float = 0.0

    # ── K. Contrary Mirrors (Gap 11) ──────────────────────────────────────
    contrary_mirrors_count: int = 0
    rules_with_relationships: int = 0
    relationship_types: dict = field(default_factory=dict)

    # ── L. Legacy Metrics ─────────────────────────────────────────────────
    modifiers_populated: int = 0
    exceptions_populated: int = 0
    concordance_populated: int = 0
    concordance_mean: float = 0.0
    verse_ref_populated: int = 0
    description_mean_length: float = 0.0

    # ── M. Verse Coverage (breadth) ─────────────────────────────────────
    verse_coverage_chapters: dict = field(default_factory=dict)
    # {ch: {"predictive_verses": N, "rules_encoded": M, "ratio": M/N}}
    verse_coverage_total_predictive: int = 0
    verse_coverage_total_encoded: int = 0
    verse_coverage_ratio: float = 0.0
    verse_coverage_gaps: list = field(default_factory=list)
    # chapters where ratio < 1.0

    # ── N. Chapter Readiness Gate ───────────────────────────────────────
    chapter_readiness: dict = field(default_factory=dict)
    # {ch: {"verse_coverage": ratio, "l3_plus_ratio": ratio, "review_ratio": ratio, "ready": bool}}

    # ── O. Overall ────────────────────────────────────────────────────────
    v2_completeness_score: float = 0.0  # 0-100%
    red_flags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["red_flags"] = [asdict(f) if hasattr(f, "__dataclass_fields__") else f for f in self.red_flags]
        return d


def _detect_entity_in_description(description: str) -> set[str]:
    """Scan description for entity keywords that indicate the OTHER entity
    is the SUBJECT of a prediction (not just mentioned as a possession).

    'wife will not live long' → spouse IS the subject → flag
    'native will have many wives' → native is subject, wives are possessions → no flag
    'maternal happiness' → native's happiness, mother is context → no flag
    """
    desc_lower = description.lower()
    entities = set()

    # Patterns where OTHER entity is the SUBJECT of a prediction verb
    subject_patterns = {
        "spouse": ["wife will", "wife not", "wife incur", "wife diseased",
                   "wife destroyed", "wife predecease", "spouse will",
                   "wife sickly", "wife spendthrift", "wife subdued"],
        "father": ["father will", "father pass", "father lost",
                   "father destroyed", "father die"],
        "mother": ["mother will", "mother lost", "mother die",
                   "mother destroyed", "lose mother"],
        "children": ["sons inimical", "sons hostile", "sons will",
                     "children will", "lose children", "loss of children",
                     "child will"],
        "siblings": ["co-born destroyed", "co-born will", "siblings will",
                     "brothers will"],
    }

    for entity, patterns in subject_patterns.items():
        for pattern in patterns:
            if pattern in desc_lower:
                entities.add(entity)
                break  # one match per entity is enough

    return entities


def _extract_house_from_rule(rule) -> int:
    """Try to extract the primary house number from a rule's condition or category."""
    pc = rule.primary_condition
    if not pc:
        return 0
    pval = pc.get("placement_value", pc.get("house", 0))
    if isinstance(pval, int) and 1 <= pval <= 12:
        return pval
    if isinstance(pval, list) and len(pval) == 1 and isinstance(pval[0], int):
        return pval[0]
    return 0


def score_rules(rules: list, label: str = "") -> V2Scorecard:
    """Score a list of RuleRecord objects against all V2 dimensions."""
    sc = V2Scorecard(label=label, total_rules=len(rules))
    if not rules:
        return sc

    flags: list[RedFlag] = []
    prediction_counts = []
    convergence_counts = []
    desc_lengths = []
    concordance_counts = []
    signal_group_directions: dict[str, list[str]] = {}

    for r in rules:
        rid = r.rule_id
        desc_lengths.append(len(r.description))

        # ── A. Predictions ────────────────────────────────────────────────
        preds = r.predictions
        if preds:
            sc.predictions_populated += 1
            prediction_counts.append(len(preds))
            if len(preds) > 3:
                sc.rules_with_many_predictions += 1
                flags.append(RedFlag(
                    rid, "warning", "one_claim_one_rule",
                    f"{len(preds)} predictions in one rule — potential summarization",
                    f"Split into {len(preds)} separate rules, each with 1 primary prediction",
                ))
            # Check prediction structure
            for i, pred in enumerate(preds):
                if not isinstance(pred, dict):
                    continue
                for key in ("entity", "claim", "domain", "direction"):
                    if key not in pred:
                        flags.append(RedFlag(
                            rid, "error", "prediction_structure",
                            f"predictions[{i}] missing required key '{key}'",
                            f"Add '{key}' to predictions[{i}]",
                        ))
        else:
            sc.predictions_empty += 1
            flags.append(RedFlag(
                rid, "error", "predictions",
                "predictions is empty — no machine-parseable claims",
                "Read the verse + commentary and extract at least 1 atomic prediction "
                "with entity, claim, domain, direction",
            ))

        # ── B. Entity Target ──────────────────────────────────────────────
        entity = r.entity_target
        sc.entity_distribution[entity] = sc.entity_distribution.get(entity, 0) + 1

        # Check for entity mismatch — whose fate is being predicted?
        # Detection looks for patterns where another entity is the SUBJECT
        # of a prediction verb (e.g., "wife will die", "sons will be hostile").
        # "Native will have many sons" is NOT a mismatch — native is the subject.
        desc_entities = _detect_entity_in_description(r.description)
        if desc_entities and entity == "native":
            non_native = desc_entities - {"native"}
            if non_native:
                sc.entity_mismatch_count += 1
                likely = sorted(non_native)[0]
                flags.append(RedFlag(
                    rid, "warning", "entity_mismatch",
                    f"entity_target='native' but description mentions "
                    f"{', '.join(sorted(non_native))}",
                    f"Verify entity_target — likely should be '{likely}' or split "
                    f"into separate rules per entity",
                ))
        # Also flag 'general' misuse — general is for structural principles only,
        # not for predictions that mention multiple entities
        if entity == "general" and desc_entities:
            specific = desc_entities - {"native"}
            if specific:
                sc.entity_mismatch_count += 1
                likely = sorted(specific)[0]
                flags.append(RedFlag(
                    rid, "warning", "entity_general_misuse",
                    f"entity_target='general' but prediction is about "
                    f"{', '.join(sorted(specific))} — 'general' is for "
                    f"structural principles only",
                    f"Set entity_target='{likely}' or split into per-entity rules",
                ))

        # Also check house-category mismatch
        cat = r.category
        if cat in _HOUSE_ENTITY_MAP and entity == "native":
            expected = _HOUSE_ENTITY_MAP[cat]
            # Don't flag if description genuinely is about native
            if expected in desc_entities:
                flags.append(RedFlag(
                    rid, "info", "entity_house_hint",
                    f"Category '{cat}' often predicts about '{expected}', "
                    f"but entity_target='native'",
                    f"Double-check: is this about the native or about {expected}?",
                ))

        # ── C. Computable Conditions ──────────────────────────────────────
        pc = r.primary_condition
        conditions = pc.get("conditions", []) if pc else []
        if isinstance(conditions, list) and conditions and isinstance(conditions[0], dict) and "type" in conditions[0]:
            sc.has_v2_conditions += 1
            for cond in conditions:
                ctype = cond.get("type", "unknown")
                sc.condition_types_used[ctype] = sc.condition_types_used.get(ctype, 0) + 1
        else:
            sc.missing_v2_conditions += 1

        # ── D. Signal Groups ──────────────────────────────────────────────
        if r.signal_group:
            sc.signal_groups_populated += 1
            sg = r.signal_group
            if sg not in signal_group_directions:
                signal_group_directions[sg] = []
            signal_group_directions[sg].append(r.outcome_direction)
        else:
            sc.signal_groups_empty += 1

        # ── F. Commentary ─────────────────────────────────────────────────
        if r.commentary_context:
            sc.commentary_populated += 1
        else:
            sc.commentary_empty += 1
        if r.cross_chapter_refs:
            sc.cross_chapter_refs_populated += 1
            sc.total_cross_refs += len(r.cross_chapter_refs)

        # ── G. Timing ─────────────────────────────────────────────────────
        tw = r.timing_window
        if not tw:
            sc.timing_unchecked += 1
            flags.append(RedFlag(
                rid, "error", "timing_unchecked",
                "timing_window is {} (unchecked)",
                "Read the verse — does it mention an age, dasha, or life event? "
                "If yes, populate timing_window. If no, set {\"type\": \"unspecified\"}",
            ))
        elif tw.get("type") == "unspecified":
            sc.timing_unspecified += 1
        else:
            sc.timing_populated += 1
            ttype = tw.get("type", "unknown")
            sc.timing_type_distribution[ttype] = sc.timing_type_distribution.get(ttype, 0) + 1

        # ── H. Functional Modulation ──────────────────────────────────────
        if r.functional_modulation:
            sc.functional_modulation_populated += 1
        else:
            sc.functional_modulation_empty += 1

        # ── I. Bhavat Bhavam ──────────────────────────────────────────────
        if r.derived_house_chains:
            sc.derived_house_chains_populated += 1
        else:
            sc.derived_house_chains_empty += 1

        # Check if bhavat bhavam is expected
        house_num = _extract_house_from_rule(r)
        if (house_num, cat) in _BHAVAT_BHAVAM:
            sc.bhavat_bhavam_expected += 1
            if not r.derived_house_chains:
                sc.bhavat_bhavam_missing += 1
                expected_chain = _BHAVAT_BHAVAM[(house_num, cat)]
                flags.append(RedFlag(
                    rid, "warning", "bhavat_bhavam_missing",
                    f"House {house_num} in '{cat}' — bhavat bhavam chain expected "
                    f"(this is {expected_chain['derivative']} of H{expected_chain['base_house']}, "
                    f"about {expected_chain['entity']}'s {expected_chain['domain']})",
                    f"Add derived_house_chains: {json.dumps(expected_chain)}",
                ))

        # ── J. Convergence Signals ────────────────────────────────────────
        if r.convergence_signals:
            sc.convergence_signals_populated += 1
            convergence_counts.append(len(r.convergence_signals))
        else:
            sc.convergence_signals_empty += 1

        # ── K. Contrary Mirrors / Relationships ───────────────────────────
        rr = r.rule_relationship
        if rr:
            sc.rules_with_relationships += 1
            rtype = rr.get("type", "unknown")
            sc.relationship_types[rtype] = sc.relationship_types.get(rtype, 0) + 1
            if rtype == "contrary_mirror":
                sc.contrary_mirrors_count += 1

        # ── L. Legacy Metrics ─────────────────────────────────────────────
        if r.modifiers:
            sc.modifiers_populated += 1
        if r.exceptions:
            sc.exceptions_populated += 1
        conc = len(r.concordance_texts) if r.concordance_texts else 0
        concordance_counts.append(conc)
        if conc > 0:
            sc.concordance_populated += 1
        if r.verse_ref:
            sc.verse_ref_populated += 1

    # ── Aggregates ────────────────────────────────────────────────────────
    if prediction_counts:
        sc.predictions_per_rule_mean = sum(prediction_counts) / len(prediction_counts)
        sc.predictions_per_rule_min = min(prediction_counts)
        sc.predictions_per_rule_max = max(prediction_counts)
    if convergence_counts:
        sc.convergence_signals_per_rule_mean = sum(convergence_counts) / len(convergence_counts)
    if concordance_counts:
        sc.concordance_mean = sum(concordance_counts) / len(concordance_counts)
    if desc_lengths:
        sc.description_mean_length = sum(desc_lengths) / len(desc_lengths)

    sc.unique_signal_groups = len(signal_group_directions)

    # Signal group conflict detection
    for sg, directions in signal_group_directions.items():
        unique_dirs = set(directions)
        if "favorable" in unique_dirs and "unfavorable" in unique_dirs:
            # This MIGHT be intentional (alternatives) — flag as info
            sc.signal_group_conflicts += 1
            rule_ids_in_group = [
                r.rule_id for r in rules
                if r.signal_group == sg
            ]
            flags.append(RedFlag(
                rule_ids_in_group[0], "info", "signal_group_conflict",
                f"Signal group '{sg}' has both favorable and unfavorable rules: "
                f"{', '.join(rule_ids_in_group)}",
                "Verify these are linked as alternatives via rule_relationship, "
                "not independent signals",
            ))

    # ── V2 Completeness Score ─────────────────────────────────────────────
    # Weighted score across all dimensions (0-100%)
    n = sc.total_rules
    if n > 0:
        weights = {
            "predictions":      (sc.predictions_populated / n) * 20,   # 20%
            "entity_correct":   ((n - sc.entity_mismatch_count) / n) * 10,  # 10%
            "conditions":       (sc.has_v2_conditions / n) * 15,       # 15%
            "signal_group":     (sc.signal_groups_populated / n) * 10, # 10%
            "timing":           ((sc.timing_populated + sc.timing_unspecified) / n) * 15,  # 15%
            "commentary":       (sc.commentary_populated / n) * 5,     # 5%
            "concordance":      (sc.concordance_populated / n) * 10,   # 10%
            "bhavat_bhavam":    (1 - (sc.bhavat_bhavam_missing / max(sc.bhavat_bhavam_expected, 1))) * 5 if sc.bhavat_bhavam_expected > 0 else 5,  # 5%
            "convergence":      (sc.convergence_signals_populated / n) * 5,  # 5%
            "func_modulation":  (sc.functional_modulation_populated / n) * 5,  # 5%
        }
        sc.v2_completeness_score = sum(weights.values())

    # ── M. Verse Coverage (breadth) ──────────────────────────────────────
    # Count rules per BPHS chapter and compare against expected verses
    import importlib
    total_predictive = 0
    total_encoded = 0
    for ch, expected_verses in _BPHS_PREDICTIVE_VERSES.items():
        module_name = _BPHS_CHAPTER_MODULES[ch]
        try:
            mod = importlib.import_module(module_name)
            reg = None
            for attr in dir(mod):
                if "REGISTRY" in attr:
                    reg = getattr(mod, attr)
                    break
            encoded = reg.count() if reg and hasattr(reg, "count") else 0
        except (ImportError, AttributeError):
            encoded = 0

        ratio = encoded / expected_verses if expected_verses > 0 else 0.0
        sc.verse_coverage_chapters[ch] = {
            "predictive_verses": expected_verses,
            "rules_encoded": encoded,
            "ratio": round(ratio, 2),
        }
        total_predictive += expected_verses
        total_encoded += encoded

        if ratio < 1.0:
            sc.verse_coverage_gaps.append(ch)
            flags.append(RedFlag(
                f"Ch.{ch}", "error" if ratio < 0.5 else "warning",
                "verse_coverage_gap",
                f"Ch.{ch}: {encoded}/{expected_verses} verses encoded ({ratio:.0%})",
                f"Re-read Ch.{ch} source text and encode the "
                f"{expected_verses - encoded} missing predictive verses",
            ))

    sc.verse_coverage_total_predictive = total_predictive
    sc.verse_coverage_total_encoded = total_encoded
    sc.verse_coverage_ratio = (
        round(total_encoded / total_predictive, 3)
        if total_predictive > 0 else 0.0
    )

    # ── N. Chapter Readiness Gate ────────────────────────────────────────
    # Combine verse coverage + maturity level to determine chapter readiness
    from tools.rule_grader import assess_rule as _assess_rule

    # Group rules by chapter
    chapter_rules: dict[str, list] = {}
    for r in rules:
        rid = r.rule_id
        if not rid.startswith("BPHS"):
            continue
        # Map BPHS rule IDs to chapter modules
        for ch in _BPHS_PREDICTIVE_VERSES:
            mod_name = _BPHS_CHAPTER_MODULES[ch]
            try:
                mod = importlib.import_module(mod_name)
                reg = None
                for attr in dir(mod):
                    if "REGISTRY" in attr:
                        reg = getattr(mod, attr)
                        break
                if reg and hasattr(reg, "all"):
                    ch_rule_ids = {cr.rule_id for cr in reg.all()}
                    if rid in ch_rule_ids:
                        chapter_rules.setdefault(ch, []).append(r)
                        break
            except (ImportError, AttributeError):
                continue

    for ch, ch_data in sc.verse_coverage_chapters.items():
        ch_rules_list = chapter_rules.get(ch, [])
        total_ch = len(ch_rules_list)
        l3_plus = 0
        reviewed = 0
        maturity_dist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for r in ch_rules_list:
            a = _assess_rule(r)
            maturity_dist[a.level] += 1
            if a.level >= 3:
                l3_plus += 1
            if getattr(r, "review_status", "unreviewed") == "reviewed":
                reviewed += 1

        l3_ratio = l3_plus / total_ch if total_ch > 0 else 0.0
        review_ratio = reviewed / total_ch if total_ch > 0 else 0.0
        verse_ratio = ch_data["ratio"]
        ready = verse_ratio >= 1.0 and l3_ratio >= 0.9 and review_ratio >= 1.0

        sc.chapter_readiness[ch] = {
            "verse_coverage": verse_ratio,
            "l3_plus_ratio": round(l3_ratio, 2),
            "l3_plus": l3_plus,
            "review_ratio": round(review_ratio, 2),
            "reviewed": reviewed,
            "total_rules": total_ch,
            "maturity": maturity_dist,
            "ready": ready,
        }

        if not ready and total_ch > 0:
            reasons = []
            if verse_ratio < 1.0:
                reasons.append(f"verse coverage {verse_ratio:.0%}")
            if l3_ratio < 0.9:
                reasons.append(f"L3+ ratio {l3_ratio:.0%}")
            if review_ratio < 1.0:
                reasons.append(f"maker-checker {review_ratio:.0%}")
            flags.append(RedFlag(
                f"Ch.{ch}", "warning",
                "chapter_not_ready",
                f"Ch.{ch} not ship-ready: {', '.join(reasons)}",
                f"Encode missing verses, resolve L2 gaps, and complete maker-checker review",
            ))

    sc.red_flags = flags
    return sc


def format_scorecard(sc: V2Scorecard) -> str:
    """Format scorecard as human-readable text."""
    n = sc.total_rules
    if n == 0:
        return f"V2 Scorecard ({sc.label}): No rules to score."

    lines = []
    lines.append(f"V2 Scorecard ({sc.label})")
    lines.append("═" * 70)
    lines.append(f"Total rules:              {n}")
    lines.append(f"V2 Completeness:          {sc.v2_completeness_score:.1f}%")
    lines.append("")

    # A. Predictions
    lines.append("A. PREDICTIONS (one-claim-one-rule)")
    lines.append(f"  Populated:              {sc.predictions_populated}/{n} ({100*sc.predictions_populated//n}%)")
    if sc.predictions_populated > 0:
        lines.append(f"  Per rule:               {sc.predictions_per_rule_mean:.1f} avg, "
                     f"{sc.predictions_per_rule_min} min, {sc.predictions_per_rule_max} max")
    if sc.rules_with_many_predictions > 0:
        lines.append(f"  ⚠ Over-stuffed (>3):   {sc.rules_with_many_predictions}")
    lines.append("")

    # B. Entity Target
    lines.append("B. ENTITY TARGET (who is the prediction about)")
    for entity, count in sorted(sc.entity_distribution.items(), key=lambda x: -x[1]):
        lines.append(f"  {entity:20s} {count:4d} ({100*count//n}%)")
    if sc.entity_mismatch_count > 0:
        lines.append(f"  ⚠ Mismatches:          {sc.entity_mismatch_count}")
    lines.append("")

    # C. Computable Conditions
    lines.append("C. COMPUTABLE CONDITIONS (can the engine fire this rule?)")
    lines.append(f"  V2 conditions:          {sc.has_v2_conditions}/{n} ({100*sc.has_v2_conditions//n}%)")
    lines.append(f"  Legacy (non-computable): {sc.missing_v2_conditions}/{n}")
    if sc.condition_types_used:
        lines.append("  Primitives used:")
        for ctype, count in sorted(sc.condition_types_used.items(), key=lambda x: -x[1]):
            lines.append(f"    {ctype:30s} {count}")
    lines.append("")

    # D. Signal Groups
    lines.append("D. SIGNAL GROUPS (prevents overcounting)")
    lines.append(f"  Populated:              {sc.signal_groups_populated}/{n} ({100*sc.signal_groups_populated//n}%)")
    lines.append(f"  Unique groups:          {sc.unique_signal_groups}")
    if sc.signal_group_conflicts > 0:
        lines.append(f"  ⚠ Direction conflicts: {sc.signal_group_conflicts}")
    lines.append("")

    # G. Timing
    lines.append("G. TIMING (falsifiability)")
    lines.append(f"  Specific timing:        {sc.timing_populated}/{n} ({100*sc.timing_populated//n}%)")
    lines.append(f"  Checked, none found:    {sc.timing_unspecified}")
    lines.append(f"  Unchecked (bare {{}}):    {sc.timing_unchecked}")
    if sc.timing_type_distribution:
        lines.append("  Timing types:")
        for ttype, count in sorted(sc.timing_type_distribution.items(), key=lambda x: -x[1]):
            lines.append(f"    {ttype:20s} {count}")
    lines.append("")

    # I. Bhavat Bhavam
    lines.append("I. BHAVAT BHAVAM (derived house chains)")
    lines.append(f"  Populated:              {sc.derived_house_chains_populated}/{n}")
    if sc.bhavat_bhavam_expected > 0:
        lines.append(f"  Expected (by house):    {sc.bhavat_bhavam_expected}")
        lines.append(f"  Missing:                {sc.bhavat_bhavam_missing}")
    lines.append("")

    # F. Commentary
    lines.append("F. COMMENTARY & CROSS-REFERENCES")
    lines.append(f"  Commentary populated:   {sc.commentary_populated}/{n} ({100*sc.commentary_populated//n}%)")
    lines.append(f"  Rules with cross-refs:  {sc.cross_chapter_refs_populated}")
    lines.append(f"  Total cross-ref links:  {sc.total_cross_refs}")
    lines.append("")

    # H + J + K
    lines.append("H/J/K. ADVANCED FIELDS")
    lines.append(f"  Functional modulation:  {sc.functional_modulation_populated}/{n} ({100*sc.functional_modulation_populated//n}%)")
    lines.append(f"  Convergence signals:    {sc.convergence_signals_populated}/{n} ({100*sc.convergence_signals_populated//n}%)")
    if sc.convergence_signals_populated > 0:
        lines.append(f"    Per rule avg:         {sc.convergence_signals_per_rule_mean:.1f}")
    lines.append(f"  Rule relationships:     {sc.rules_with_relationships}")
    if sc.relationship_types:
        for rtype, count in sorted(sc.relationship_types.items()):
            lines.append(f"    {rtype:20s} {count}")
    lines.append(f"  Contrary mirrors:       {sc.contrary_mirrors_count}")
    lines.append("")

    # L. Legacy
    lines.append("L. LEGACY METRICS")
    lines.append(f"  Modifiers populated:    {sc.modifiers_populated}/{n} ({100*sc.modifiers_populated//n}%)")
    lines.append(f"  Exceptions populated:   {sc.exceptions_populated}/{n}")
    lines.append(f"  Concordance populated:  {sc.concordance_populated}/{n} ({100*sc.concordance_populated//n}%)")
    lines.append(f"  Concordance mean:       {sc.concordance_mean:.2f} texts/rule")
    lines.append(f"  Verse ref populated:    {sc.verse_ref_populated}/{n}")
    lines.append(f"  Description avg length: {sc.description_mean_length:.0f} chars")
    lines.append("")

    # M. Verse Coverage
    lines.append("M. VERSE COVERAGE (breadth — are all source verses encoded?)")
    lines.append(f"  Total predictive verses: {sc.verse_coverage_total_predictive}")
    lines.append(f"  Total rules encoded:     {sc.verse_coverage_total_encoded}")
    lines.append(f"  Coverage ratio:          {sc.verse_coverage_ratio:.0%}")
    if sc.verse_coverage_chapters:
        lines.append("  Per chapter:")
        for ch, info in sorted(sc.verse_coverage_chapters.items(),
                               key=lambda x: x[1]["ratio"]):
            ratio = info["ratio"]
            encoded = info["rules_encoded"]
            expected = info["predictive_verses"]
            status = "✅" if ratio >= 1.0 else "⚠️" if ratio >= 0.5 else "❌"
            lines.append(
                f"    Ch.{ch:4s}: {encoded:3d}/{expected:3d} ({ratio:5.0%}) {status}"
            )
    if sc.verse_coverage_gaps:
        lines.append(f"  ⚠ Chapters with gaps: {', '.join(f'Ch.{c}' for c in sc.verse_coverage_gaps)}")
    lines.append("")

    # N. Chapter Readiness Gate
    lines.append("N. CHAPTER READINESS GATE (verses ≥100% + L3+ ≥90% + reviewed 100% = SHIP)")
    if sc.chapter_readiness:
        for ch in sorted(sc.chapter_readiness.keys()):
            cr = sc.chapter_readiness[ch]
            vc = cr["verse_coverage"]
            l3r = cr["l3_plus_ratio"]
            rr = cr["review_ratio"]
            ready = "SHIP ✅" if cr["ready"] else "BLOCKED ❌"
            mat = cr["maturity"]
            mat_str = f"L1={mat[1]} L2={mat[2]} L3={mat[3]} L4={mat[4]}"
            lines.append(
                f"    Ch.{ch:4s}: verses={vc:5.0%} L3+={l3r:5.0%} "
                f"reviewed={rr:5.0%} [{mat_str}] → {ready}"
            )
        ship_count = sum(1 for cr in sc.chapter_readiness.values() if cr["ready"])
        total_ch = len(sc.chapter_readiness)
        lines.append(f"  Ship-ready: {ship_count}/{total_ch} chapters")
    lines.append("")

    # Red flags
    errors = [f for f in sc.red_flags if f.severity == "error"]
    warnings = [f for f in sc.red_flags if f.severity == "warning"]
    infos = [f for f in sc.red_flags if f.severity == "info"]

    lines.append(f"RED FLAGS: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
    lines.append("─" * 70)

    if errors:
        lines.append(f"\n🔴 ERRORS ({len(errors)}):")
        for f in errors[:15]:
            lines.append(f"  {f.rule_id}: [{f.category}] {f.message}")
            lines.append(f"    → FIX: {f.fix}")
        if len(errors) > 15:
            lines.append(f"  ... and {len(errors) - 15} more errors")

    if warnings:
        lines.append(f"\n🟡 WARNINGS ({len(warnings)}):")
        for f in warnings[:15]:
            lines.append(f"  {f.rule_id}: [{f.category}] {f.message}")
            lines.append(f"    → FIX: {f.fix}")
        if len(warnings) > 15:
            lines.append(f"  ... and {len(warnings) - 15} more warnings")

    if infos:
        lines.append(f"\n🔵 INFO ({len(infos)}):")
        for f in infos[:10]:
            lines.append(f"  {f.rule_id}: [{f.category}] {f.message}")
            lines.append(f"    → FIX: {f.fix}")
        if len(infos) > 10:
            lines.append(f"  ... and {len(infos) - 10} more")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="V2 Encoding Quality Scorecard")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--session", help="Score rules from a specific session (e.g., S311)")
    group.add_argument("--file", help="Score rules from a specific corpus file")
    group.add_argument("--v2-only", action="store_true", help="Score all V2 rules (S310+)")
    group.add_argument("--all", action="store_true", help="Score entire corpus")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    from src.corpus.combined_corpus import build_corpus
    corpus = build_corpus()
    all_rules = corpus.all()

    if args.session:
        rules = [r for r in all_rules if r.last_modified_session == args.session]
        label = f"Session {args.session}"
    elif args.file:
        # Import the specific file's registry
        import importlib
        mod_path = args.file.replace("/", ".").replace(".py", "")
        mod = importlib.import_module(mod_path)
        # Find the registry
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if hasattr(attr, "all") and callable(attr.all):
                rules = attr.all()
                break
        else:
            print(f"No registry found in {args.file}", file=sys.stderr)
            sys.exit(1)
        label = args.file.split("/")[-1].replace(".py", "")
    elif args.v2_only:
        rules = [r for r in all_rules if r.last_modified_session >= "S310"]
        label = "V2 rules (S310+)"
    else:
        rules = all_rules
        label = f"Full corpus ({len(all_rules)} rules)"

    if not rules:
        print(f"No rules found for {label}")
        sys.exit(0)

    sc = score_rules(rules, label)

    if args.json:
        print(json.dumps(sc.to_dict(), indent=2, default=str))
    else:
        print(format_scorecard(sc))


if __name__ == "__main__":
    main()
