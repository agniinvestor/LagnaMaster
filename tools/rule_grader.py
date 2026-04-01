"""tools/rule_grader.py — Maturity model for V2-compliant rules.

Measures each rule against a 5-level maturity progression:

  L1 ENCODED   — Rule exists with valid taxonomy fields
  L2 AUDITED   — Verse audit exists, commentary present, structured conditions
  L3 LINKABLE  — Canonical signal_group, ready for cross-text matching
  L4 CONCORDED — Compared against 2+ texts, agreements/divergences recorded
  L5 VALIDATED — Empirical data supporting/contradicting (Phase 6+)

Concordance (L4) is NOT scored until partner texts are V2-encoded.
That dimension is tracked as "pending" rather than penalized.

Usage:
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --chapter Ch.24
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --level 2  # show L2 rules
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL SIGNAL_GROUP CONVENTION
# ═══════════════════════════════════════════════════════════════════════════════
#
# Signal groups are the JOIN KEY for cross-text matching. When Saravali says
# "Jupiter in 7th = wealthy wife" and BPHS says "5th lord in 7th = honourable",
# they must share a signal_group namespace so the concordance engine can detect
# the overlap.
#
# CONVENTION (enforced from S313+):
#   {entity}_{placement_type}_{placement_value}_{outcome_theme}
#
# Examples:
#   h5_lord_in_h7_honourable_progenic       — 5th lord in 7th house
#   jupiter_in_h7_wealthy_wife              — Jupiter in 7th house
#   h1_lord_in_h6_devoid_physical_happiness — 1st lord in 6th house
#   gulika_h5_not_praiseworthy              — Gulika in 5th house
#
# The first 3 segments ({entity}_{placement_type}_{placement_value}) form
# the CANONICAL PREFIX. Two rules from different texts with the same canonical
# prefix are ABOUT THE SAME CONFIGURATION and should be compared.
#
# The final segment ({outcome_theme}) captures WHAT THE TEXT CLAIMS about it.
# Concordance = same prefix + same outcome direction.
# Divergence  = same prefix + different outcome direction or intensity.
#
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# DIVERGENCE TAXONOMY (structured, not free-form)
# ═══════════════════════════════════════════════════════════════════════════════
#
# When two texts disagree, the disagreement has a TYPE:
#
#   DIRECTION_CONFLICT    — Text A says favorable, Text B says unfavorable
#   INTENSITY_DIFFERENCE  — Both say favorable, but one says strong, other weak
#   SCOPE_DIFFERENCE      — Same prediction, different lagna/dasha scope
#   CONDITION_ADDITION    — Text B adds a condition not in Text A
#   EXCEPTION_ADDITION    — Text B notes an exception Text A doesn't mention
#   ENTITY_DIFFERENCE     — Text A about native, Text B about father
#   SILENT                — Text B simply doesn't mention what Text A claims
#
# These types go in divergence_notes as structured prefix:
#   "DIRECTION_CONFLICT: Saravali says unfavorable for wealth"
#   "CONDITION_ADDITION: Phaladeepika adds 'only if aspected by benefic'"
#
# This makes divergences machine-queryable, not just human-readable.
#
# ═══════════════════════════════════════════════════════════════════════════════

DIVERGENCE_TYPES = frozenset({
    "DIRECTION_CONFLICT",
    "INTENSITY_DIFFERENCE",
    "SCOPE_DIFFERENCE",
    "CONDITION_ADDITION",
    "EXCEPTION_ADDITION",
    "ENTITY_DIFFERENCE",
    "SILENT",
})


@dataclass
class RuleMaturity:
    rule_id: str
    chapter: str
    verse_ref: str
    signal_group: str
    level: int = 0          # 1-5
    level_label: str = ""
    checks: dict[str, bool] = field(default_factory=dict)
    gaps: list[str] = field(default_factory=list)
    l4_status: str = "pending"  # "pending" | "concorded" | "diverged" | "unique"


def assess_rule(rule) -> RuleMaturity:
    """Assess a single rule's maturity level."""
    rm = RuleMaturity(
        rule_id=rule.rule_id,
        chapter=rule.chapter,
        verse_ref=rule.verse_ref,
        signal_group=rule.signal_group,
    )

    # ── L1: ENCODED ─────────────────────────────────────────────────────
    # Rule exists with valid taxonomy fields
    from src.corpus.taxonomy import (
        VALID_OUTCOME_DOMAINS, VALID_OUTCOME_DIRECTIONS,
        VALID_OUTCOME_INTENSITIES,
    )
    l1_taxonomy = (
        rule.outcome_direction in VALID_OUTCOME_DIRECTIONS
        and rule.outcome_intensity in VALID_OUTCOME_INTENSITIES
        and all(d in VALID_OUTCOME_DOMAINS for d in (rule.outcome_domains or []))
    )
    l1_predictions = bool(rule.predictions)
    l1_description = bool(rule.description and len(rule.description) > 20)

    rm.checks["L1_taxonomy"] = l1_taxonomy
    rm.checks["L1_predictions"] = l1_predictions
    rm.checks["L1_description"] = l1_description

    if not (l1_taxonomy and l1_predictions and l1_description):
        rm.level = 0
        rm.level_label = "INCOMPLETE"
        if not l1_taxonomy:
            rm.gaps.append("taxonomy_violation")
        if not l1_predictions:
            rm.gaps.append("no_predictions")
        if not l1_description:
            rm.gaps.append("no_description")
        return rm
    rm.level = 1

    # ── L2: AUDITED ─────────────────────────────────────────────────────
    # Verse audit exists, commentary present, structured conditions
    l2_verse_ref = bool(rule.verse_ref and "v." in rule.verse_ref)
    l2_commentary = bool(rule.commentary_context and len(rule.commentary_context) >= 30)

    # Check if verse audit file exists for this chapter
    ch_match = re.search(r'Ch\.(\d+)', rule.chapter)
    l2_audit_file = False
    if ch_match:
        audit_path = Path(f"data/verse_audits/ch{ch_match.group(1)}_audit.json")
        l2_audit_file = audit_path.exists()

    # Modifiers captured where commentary suggests them
    comm_lower = (rule.commentary_context or "").lower()
    has_conditional_lang = any(kw in comm_lower for kw in
        ["if ", "unless", "except", "however", "but if", "provided", "only when"])
    has_modifiers = bool(rule.modifiers) or bool(rule.exceptions)
    l2_modifiers_complete = has_modifiers or not has_conditional_lang

    rm.checks["L2_verse_ref"] = l2_verse_ref
    rm.checks["L2_commentary"] = l2_commentary
    rm.checks["L2_audit_file"] = l2_audit_file
    rm.checks["L2_modifiers"] = l2_modifiers_complete

    if l2_verse_ref and l2_commentary and l2_audit_file:
        rm.level = 2
    else:
        if not l2_verse_ref:
            rm.gaps.append("missing_verse_number")
        if not l2_commentary:
            rm.gaps.append("thin_or_missing_commentary")
        if not l2_audit_file:
            rm.gaps.append("no_verse_audit_file")
        rm.level_label = "L1 ENCODED"
        return rm

    if not l2_modifiers_complete:
        rm.gaps.append("conditional_language_no_modifier")

    # ── L3: LINKABLE ────────────────────────────────────────────────────
    # Canonical signal_group, parseable for cross-text matching
    l3_signal_group = bool(rule.signal_group and len(rule.signal_group) > 5)

    # Check signal_group follows the canonical convention:
    # {entity}_{placement}_{value}_{theme}
    # At minimum, should have entity + some descriptor
    sg = rule.signal_group or ""
    l3_canonical_format = bool(
        sg
        and "_" in sg
        and not sg.startswith("test")
        and len(sg.split("_")) >= 3
    )

    # Structured conditions present (for computable rules)
    pc = rule.primary_condition or {}
    conditions = pc.get("conditions", [])
    l3_conditions = bool(conditions and any(c.get("type") for c in conditions))
    # Upagrahas legitimately have no conditions — don't penalize
    is_upagraha = rule.category == "upagraha_effects"
    l3_conditions_ok = l3_conditions or is_upagraha

    rm.checks["L3_signal_group"] = l3_signal_group
    rm.checks["L3_canonical_format"] = l3_canonical_format
    rm.checks["L3_conditions"] = l3_conditions_ok

    if l3_signal_group and l3_canonical_format and l3_conditions_ok:
        rm.level = 3
    else:
        if not l3_signal_group:
            rm.gaps.append("empty_signal_group")
        if not l3_canonical_format:
            rm.gaps.append("signal_group_not_canonical")
        if not l3_conditions_ok:
            rm.gaps.append("no_structured_conditions")
        rm.level_label = "L2 AUDITED"
        return rm

    # ── L4: CONCORDED (tracked, not scored) ─────────────────────────────
    # This level requires partner texts to be V2-encoded.
    # We track readiness but don't penalize.
    conc = rule.concordance_texts or []
    div = rule.divergence_notes or ""

    if len(conc) >= 2 or (len(conc) >= 1 and div):
        rm.l4_status = "concorded" if not div else "diverged"
        rm.level = 4
    elif len(conc) == 1:
        rm.l4_status = "partial"
    else:
        rm.l4_status = "pending"
    # Don't set gaps for L4 — it's not achievable yet

    # ── L5: VALIDATED (future) ──────────────────────────────────────────
    # Requires empirical data. Always "pending" for now.

    # Set label
    labels = {0: "INCOMPLETE", 1: "L1 ENCODED", 2: "L2 AUDITED",
              3: "L3 LINKABLE", 4: "L4 CONCORDED", 5: "L5 VALIDATED"}
    rm.level_label = labels.get(rm.level, "UNKNOWN")
    return rm


def load_v2_rules():
    """Load only V2-compliant rules (from bphs_v2_ch* files)."""
    rules = []
    from src.corpus.bphs_v2_ch12 import BPHS_V2_CH12_REGISTRY
    from src.corpus.bphs_v2_ch13 import BPHS_V2_CH13_REGISTRY
    from src.corpus.bphs_v2_ch14 import BPHS_V2_CH14_REGISTRY
    from src.corpus.bphs_v2_ch15 import BPHS_V2_CH15_REGISTRY
    from src.corpus.bphs_v2_ch16 import BPHS_V2_CH16_REGISTRY
    from src.corpus.bphs_v2_ch17 import BPHS_V2_CH17_REGISTRY
    from src.corpus.bphs_v2_ch18 import BPHS_V2_CH18_REGISTRY
    from src.corpus.bphs_v2_ch19 import BPHS_V2_CH19_REGISTRY
    from src.corpus.bphs_v2_ch20 import BPHS_V2_CH20_REGISTRY
    from src.corpus.bphs_v2_ch21 import BPHS_V2_CH21_REGISTRY
    from src.corpus.bphs_v2_ch22 import BPHS_V2_CH22_REGISTRY
    from src.corpus.bphs_v2_ch23 import BPHS_V2_CH23_REGISTRY
    from src.corpus.bphs_v2_ch24a import BPHS_V2_CH24A_REGISTRY
    from src.corpus.bphs_v2_ch24b import BPHS_V2_CH24B_REGISTRY
    from src.corpus.bphs_v2_ch24c import BPHS_V2_CH24C_REGISTRY
    from src.corpus.bphs_v2_ch25 import BPHS_V2_CH25_REGISTRY

    for reg in [
        BPHS_V2_CH12_REGISTRY, BPHS_V2_CH13_REGISTRY, BPHS_V2_CH14_REGISTRY,
        BPHS_V2_CH15_REGISTRY, BPHS_V2_CH16_REGISTRY, BPHS_V2_CH17_REGISTRY,
        BPHS_V2_CH18_REGISTRY, BPHS_V2_CH19_REGISTRY, BPHS_V2_CH20_REGISTRY,
        BPHS_V2_CH21_REGISTRY, BPHS_V2_CH22_REGISTRY, BPHS_V2_CH23_REGISTRY,
        BPHS_V2_CH24A_REGISTRY, BPHS_V2_CH24B_REGISTRY, BPHS_V2_CH24C_REGISTRY,
        BPHS_V2_CH25_REGISTRY,
    ]:
        rules.extend(reg.all())
    return rules


def main():
    parser = argparse.ArgumentParser(description="V2 Corpus Maturity Model")
    parser.add_argument("--chapter", help="Filter by chapter (e.g. Ch.24)")
    parser.add_argument("--level", type=int, help="Show only rules at this level")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--gaps", action="store_true", help="Show only rules with gaps")
    args = parser.parse_args()

    rules = load_v2_rules()
    assessments = [assess_rule(r) for r in rules]

    if args.chapter:
        assessments = [a for a in assessments if a.chapter == args.chapter]
    if args.level is not None:
        assessments = [a for a in assessments if a.level == args.level]
    if args.gaps:
        assessments = [a for a in assessments if a.gaps]

    if args.json:
        out = [{"rule_id": a.rule_id, "chapter": a.chapter, "level": a.level,
                "level_label": a.level_label, "l4_status": a.l4_status,
                "checks": a.checks, "gaps": a.gaps} for a in assessments]
        print(json.dumps(out, indent=2))
        return

    total = len(assessments)
    if total == 0:
        print("No rules found matching filters.")
        return

    # ── Count by level ──────────────────────────────────────────────────
    level_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    l4_counts = {"pending": 0, "partial": 0, "concorded": 0, "diverged": 0, "unique": 0}
    chapter_levels: dict[str, dict[int, int]] = {}
    all_gaps: dict[str, int] = {}

    for a in assessments:
        level_counts[a.level] += 1
        l4_counts[a.l4_status] += 1
        ch = a.chapter
        if ch not in chapter_levels:
            chapter_levels[ch] = {i: 0 for i in range(6)}
            chapter_levels[ch]["total"] = 0
        chapter_levels[ch][a.level] += 1
        chapter_levels[ch]["total"] += 1
        for g in a.gaps:
            all_gaps[g] = all_gaps.get(g, 0) + 1

    print()
    print("═" * 72)
    print(f"  V2 CORPUS MATURITY MODEL — {total} rules")
    print("═" * 72)
    print()

    # Maturity distribution
    print("  MATURITY LEVELS")
    print("  ───────────────")
    bar_w = 40
    labels = {
        0: ("INCOMPLETE ", "⬛"),
        1: ("L1 ENCODED ", "🟥"),
        2: ("L2 AUDITED ", "🟧"),
        3: ("L3 LINKABLE", "🟩"),
        4: ("L4 CONCORDD", "🟦"),
        5: ("L5 VALIDATE", "⬜"),
    }
    for lvl in range(6):
        count = level_counts[lvl]
        pct = 100 * count / total if total else 0
        bar = labels[lvl][1] * int(pct / 100 * bar_w)
        print(f"  {labels[lvl][0]}  {count:>4} ({pct:5.1f}%)  {bar}")
    print()

    # L4 concordance readiness (separate tracker — not a quality penalty)
    print("  L4 CONCORDANCE READINESS (not scored — partner texts not V2 yet)")
    print("  ─────────────────────────────────────────────────────────────────")
    for status, emoji in [("concorded", "🟢"), ("diverged", "🟡"),
                          ("partial", "🔵"), ("pending", "⚪")]:
        count = l4_counts[status]
        pct = 100 * count / total if total else 0
        print(f"  {emoji} {status:<12} {count:>4} ({pct:5.1f}%)")
    print("  Note: 'pending' means the rule CANNOT be concorded yet (no partner text).")
    print("  This is expected and will resolve as other texts are V2-encoded.")
    print()

    # Per-chapter breakdown
    print("  PER-CHAPTER MATURITY")
    print("  ────────────────────")
    print(f"  {'Chapter':<10} {'Total':>5}  {'L0':>4} {'L1':>4} {'L2':>4} {'L3':>4} {'L4':>4}  {'Median'}")
    print(f"  {'─'*10} {'─'*5}  {'─'*4} {'─'*4} {'─'*4} {'─'*4} {'─'*4}  {'─'*8}")
    for ch in sorted(chapter_levels.keys()):
        cl = chapter_levels[ch]
        # Find median level
        running = 0
        median = 0
        for lvl in range(6):
            running += cl.get(lvl, 0)
            if running >= cl["total"] / 2:
                median = lvl
                break
        print(f"  {ch:<10} {cl['total']:>5}  {cl[0]:>4} {cl[1]:>4} {cl[2]:>4} {cl[3]:>4} {cl[4]:>4}  L{median}")
    print()

    # Gap analysis
    if all_gaps:
        print("  GAPS (improvement opportunities for current level)")
        print("  ──────────────────────────────────────────────────")
        for gap, count in sorted(all_gaps.items(), key=lambda x: -x[1]):
            print(f"  {count:>4}x  {gap}")
        print()

    # Signal_group coverage for cross-text readiness
    unique_prefixes = set()
    for a in assessments:
        sg = a.signal_group or ""
        parts = sg.split("_")
        if len(parts) >= 3:
            # Extract canonical prefix (entity + placement + value)
            unique_prefixes.add("_".join(parts[:3]))

    print("  CROSS-TEXT LINKING READINESS")
    print("  ────────────────────────────")
    print(f"  Unique signal_group prefixes: {len(unique_prefixes)}")
    print(f"  Rules at L3+ (linkable):      {level_counts[3] + level_counts[4] + level_counts[5]}/{total}")
    print(f"  Rules with conditions:         {sum(1 for a in assessments if a.checks.get('L3_conditions', False))}/{total}")
    print()

    # Summary
    l3_plus = level_counts[3] + level_counts[4] + level_counts[5]
    print("  SUMMARY")
    print("  ───────")
    print(f"  {l3_plus}/{total} rules ({100*l3_plus/total:.0f}%) are L3 LINKABLE — ready for cross-text matching")
    print(f"  {level_counts[0]}/{total} rules need remediation (INCOMPLETE)")
    print("  Divergence taxonomy: defined but not yet enforced (7 types)")
    print("  Next milestone: encode partner text at V2 to enable L4 concordance")
    print()
    print("═" * 72)


if __name__ == "__main__":
    main()
