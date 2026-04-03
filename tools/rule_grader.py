"""tools/rule_grader.py — Corpus maturity scorecard across the full 25,000 rule estate.

6-level maturity model covering every rule from unmapped to empirically validated:

  L0 UNMAPPED   — Text exists but slokas not yet counted or rule not written
  L1 PROSE      — Rule exists with description + tags only (Phase 1A legacy)
  L2 STRUCTURED — V2 fields present but has quality gaps (missing modifiers, etc.)
  L3 COMPLETE   — V2 perfect — zero quality gaps, canonical signal_group
  L4 COMPARED   — Concordance/divergence recorded with 2+ texts (structured taxonomy)
  L5 VALIDATED  — Empirical data confirms/contradicts (Phase 6+)

Usage:
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --chapter Ch.24
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --level 2
    PYTHONPATH=. .venv/bin/python tools/rule_grader.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# Target from ROADMAP — total rules at completion of Phase 1B
ROADMAP_TARGET = 25000

# Structured divergence type prefixes (from CROSS_TEXT_GOVERNANCE.md)
DIVERGENCE_PREFIXES = ("DIR:", "INT:", "SCO:", "CON:", "EXC:", "ENT:", "DOM:", "TIM:", "SIL:")


@dataclass
class RuleAssessment:
    rule_id: str
    chapter: str
    source: str
    verse_ref: str
    signal_group: str
    level: int = 0
    level_label: str = ""
    gaps: list[str] = field(default_factory=list)


def assess_rule(rule) -> RuleAssessment:
    """Assess a single rule's maturity level (L1-L5). L0 is for unmapped rules (not in corpus)."""
    ra = RuleAssessment(
        rule_id=rule.rule_id,
        chapter=getattr(rule, "chapter", ""),
        source=getattr(rule, "source", ""),
        verse_ref=getattr(rule, "verse_ref", "") or "",
        signal_group=getattr(rule, "signal_group", "") or "",
    )

    # ── Check for L1 PROSE (legacy) ─────────────────────────────────────
    has_conditions = bool(
        getattr(rule, "primary_condition", None)
        and rule.primary_condition.get("conditions")
    )
    has_predictions = bool(getattr(rule, "predictions", None) and rule.predictions)
    has_commentary = bool(
        getattr(rule, "commentary_context", "")
        and len(rule.commentary_context) > 10
    )
    if not has_predictions and not has_conditions and not has_commentary:
        ra.level = 1
        ra.level_label = "L1 PROSE"
        # Note what partial data exists
        if getattr(rule, "verse_ref", "") and "v." in str(rule.verse_ref):
            pass  # has verse ref — useful for re-encoding
        else:
            ra.gaps.append("no_verse_ref")
        if not getattr(rule, "concordance_texts", None):
            ra.gaps.append("no_concordance")
        return ra

    # ── From here, rule has SOME structured fields → assess V2 quality ──

    # Verse audit file exists?
    ch_match = re.search(r"Ch\.(\d+)", ra.chapter)
    has_audit_file = False
    if ch_match:
        audit_path = Path(f"data/verse_audits/ch{ch_match.group(1)}_audit.json")
        has_audit_file = audit_path.exists()

    # Verse-level reference?
    has_verse_num = bool(ra.verse_ref and "v." in ra.verse_ref)

    # Taxonomy compliance?
    from src.corpus.taxonomy import (
        VALID_OUTCOME_DOMAINS, VALID_OUTCOME_DIRECTIONS,
        VALID_OUTCOME_INTENSITIES,
    )
    taxonomy_ok = (
        getattr(rule, "outcome_direction", "") in VALID_OUTCOME_DIRECTIONS
        and getattr(rule, "outcome_intensity", "") in VALID_OUTCOME_INTENSITIES
        and all(d in VALID_OUTCOME_DOMAINS for d in (getattr(rule, "outcome_domains", None) or []))
    )

    # Modifiers captured where commentary suggests them?
    comm = getattr(rule, "commentary_context", "") or ""
    comm_lower = comm.lower()
    has_conditional_lang = any(kw in comm_lower for kw in
        ["if ", "unless", "except", "however", "but if", "provided", "only when"])
    has_modifiers = bool(getattr(rule, "modifiers", None)) or bool(getattr(rule, "exceptions", None))
    # Conditional language is also handled by sibling exception rules or lagna_scope
    has_linked_handling = bool(getattr(rule, "rule_relationship", None)) or bool(getattr(rule, "lagna_scope", None))
    modifiers_complete = has_modifiers or has_linked_handling or not has_conditional_lang

    # Signal_group canonical format?
    sg = ra.signal_group
    canonical_sg = bool(sg and "_" in sg and len(sg.split("_")) >= 3)

    # Conditions present (or legitimately empty for upagrahas/principles)?
    is_general = getattr(rule, "category", "") in ("upagraha_effects",) or not has_conditions
    conditions_ok = has_conditions or is_general

    # Maker-checker review status
    review_status = getattr(rule, "review_status", "unreviewed") or "unreviewed"
    has_review = review_status == "reviewed"

    # ── Collect gaps ────────────────────────────────────────────────────
    gaps = []
    if not taxonomy_ok:
        gaps.append("taxonomy_violation")
    if not has_verse_num:
        gaps.append("no_verse_number")
    if not has_commentary:
        gaps.append("no_commentary")
    if not has_audit_file:
        gaps.append("no_verse_audit_file")
    if not modifiers_complete:
        gaps.append("conditional_language_no_modifier")
    if not canonical_sg:
        gaps.append("signal_group_not_canonical")
    if not conditions_ok:
        gaps.append("no_structured_conditions")
    if not has_review:
        gaps.append("maker_checker_not_reviewed")

    ra.gaps = gaps

    # ── L2 vs L3: any gaps? ────────────────────────────────────────────
    if gaps:
        ra.level = 2
        ra.level_label = "L2 STRUCTURED"
        return ra

    # Zero gaps → L3 COMPLETE
    ra.level = 3
    ra.level_label = "L3 COMPLETE"

    # ── L4 check: structured concordance/divergence with 2+ texts ──────
    conc = getattr(rule, "concordance_texts", None) or []
    div = getattr(rule, "divergence_notes", "") or ""
    has_structured_div = any(div.startswith(p) or f" | {p}" in div for p in DIVERGENCE_PREFIXES)
    multi_text = len(conc) >= 2

    if multi_text or (len(conc) >= 1 and has_structured_div):
        ra.level = 4
        ra.level_label = "L4 COMPARED"

    # L5 requires empirical data — no check possible yet
    return ra


def load_all_rules():
    """Load entire corpus (V2 + legacy)."""
    from src.corpus.combined_corpus import build_corpus
    return build_corpus().all()


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
    parser = argparse.ArgumentParser(description="Corpus Maturity Scorecard")
    parser.add_argument("--chapter", help="Filter by chapter (e.g. Ch.24)")
    parser.add_argument("--level", type=int, help="Show only rules at this level (0-5)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--gaps", action="store_true", help="Show only rules with gaps")
    parser.add_argument("--source", help="Filter by source text (e.g. BPHS, Saravali)")
    args = parser.parse_args()

    # Load and assess all rules
    all_rules = load_all_rules()
    assessments = [assess_rule(r) for r in all_rules]

    # Apply filters
    if args.chapter:
        assessments = [a for a in assessments if a.chapter == args.chapter]
    if args.level is not None:
        assessments = [a for a in assessments if a.level == args.level]
    if args.gaps:
        assessments = [a for a in assessments if a.gaps]
    if args.source:
        assessments = [a for a in assessments if a.source == args.source]

    if args.json:
        out = [{"rule_id": a.rule_id, "chapter": a.chapter, "source": a.source,
                "level": a.level, "level_label": a.level_label, "gaps": a.gaps}
               for a in assessments]
        print(json.dumps(out, indent=2))
        return

    # ── Compute estate totals ───────────────────────────────────────────
    total_in_corpus = len(assessments)
    l0_count = max(0, ROADMAP_TARGET - total_in_corpus)
    level_counts = {0: l0_count, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for a in assessments:
        level_counts[a.level] += 1

    # Source breakdown
    source_levels: dict[str, dict[int, int]] = {}
    for a in assessments:
        src = a.source or "unknown"
        if src not in source_levels:
            source_levels[src] = {i: 0 for i in range(6)}
            source_levels[src]["total"] = 0
        source_levels[src][a.level] += 1
        source_levels[src]["total"] += 1

    # Gap analysis
    all_gaps: dict[str, int] = {}
    for a in assessments:
        for g in a.gaps:
            all_gaps[g] = all_gaps.get(g, 0) + 1

    # ══════════════════════════════════════════════════════════════════════
    # RENDER SCORECARD
    # ══════════════════════════════════════════════════════════════════════

    estate_total = ROADMAP_TARGET
    print()
    print("=" * 76)
    print(f"  CORPUS MATURITY SCORECARD — {estate_total:,} rule estate")
    print("=" * 76)
    print()

    # ── Level distribution ──────────────────────────────────────────────
    print("  MATURITY DISTRIBUTION")
    print("  ─────────────────────")
    level_meta = {
        0: ("L0 UNMAPPED  ", "Not yet encoded                    ", "░"),
        1: ("L1 PROSE     ", "Description only (Phase 1A legacy) ", "▒"),
        2: ("L2 STRUCTURED", "V2 fields present, has quality gaps", "▓"),
        3: ("L3 COMPLETE  ", "V2 perfect, zero gaps, linkable    ", "█"),
        4: ("L4 COMPARED  ", "Cross-text concordance recorded    ", "█"),
        5: ("L5 VALIDATED ", "Empirical data confirms/contradicts", "█"),
    }
    bar_w = 30
    for lvl in range(6):
        count = level_counts[lvl]
        pct = 100 * count / estate_total if estate_total else 0
        label, desc, ch = level_meta[lvl]
        bar = ch * max(1, int(pct / 100 * bar_w)) if count > 0 else ""
        print(f"  {label}  {count:>6,} ({pct:5.1f}%)  {bar}")
        if lvl == 0:
            print(f"  {'':14}  {desc}")
    print()

    # ── Pipeline view ───────────────────────────────────────────────────
    print("  PIPELINE (what needs to move where)")
    print("  ────────────────────────────────────")
    transitions = [
        (0, 1, "L0 → L1", "Encode from source text (ROADMAP sessions)", level_counts[0]),
        (1, 3, "L1 → L3", "Re-encode at V2 (replace prose with structured)", level_counts[1]),
        (2, 3, "L2 → L3", "Fix quality gaps (modifiers, exceptions, conditions)", level_counts[2]),
        (3, 4, "L3 → L4", "Encode partner text + cross-text comparison", level_counts[3]),
        (4, 5, "L4 → L5", "Collect empirical data from chart evaluations", level_counts[4]),
    ]
    for _, _, label, action, count in transitions:
        if count > 0:
            print(f"  {label}  {count:>6,} rules  {action}")
    print()

    # ── Roadmap connection ──────────────────────────────────────────────
    print("  ROADMAP CONNECTION")
    print("  ──────────────────")
    print("  Phase 1B encoding sessions (S313+):  L0 → L3  (new BPHS chapters)")
    print("  Phase 1B re-encode sessions:         L1 → L3  (Saravali, Phaladeepika etc.)")
    print(f"  Quality remediation:                 L2 → L3  ({level_counts[2]} rules with gaps)")
    print("  Cross-text sessions:                 L3 → L4  (after partner text V2-encoded)")
    print("  Phase 6 empirical (S701+):           L4 → L5  (chart evaluation + outcomes)")
    print()

    # ── Source text breakdown ───────────────────────────────────────────
    if not args.chapter and not args.source:
        print("  BY SOURCE TEXT")
        print("  ──────────────")
        print(f"  {'Source':<25} {'Total':>6}  {'L1':>6} {'L2':>6} {'L3':>6} {'L4':>6}")
        print(f"  {'─'*25} {'─'*6}  {'─'*6} {'─'*6} {'─'*6} {'─'*6}")
        for src in sorted(source_levels.keys()):
            sl = source_levels[src]
            print(f"  {src:<25} {sl['total']:>6}  {sl[1]:>6} {sl[2]:>6} {sl[3]:>6} {sl[4]:>6}")
        print()

    # ── Gap analysis (L2 rules only — actionable) ──────────────────────
    l2_gaps: dict[str, int] = {}
    for a in assessments:
        if a.level == 2:
            for g in a.gaps:
                l2_gaps[g] = l2_gaps.get(g, 0) + 1
    if l2_gaps and not args.level:
        print(f"  QUALITY GAPS — L2 → L3 remediation ({level_counts[2]} rules)")
        print("  ───────────────────────────────────────────────────")
        for gap, count in sorted(l2_gaps.items(), key=lambda x: -x[1]):
            print(f"  {count:>5}x  {gap}")
        print()

    # ── Summary bar ─────────────────────────────────────────────────────
    encoded = level_counts[1] + level_counts[2] + level_counts[3] + level_counts[4] + level_counts[5]
    v2_ready = level_counts[3] + level_counts[4] + level_counts[5]
    compared = level_counts[4] + level_counts[5]

    print("  SUMMARY")
    print("  ───────")
    print(f"  Encoded (L1+):     {encoded:>6,} / {estate_total:>6,}  ({100*encoded/estate_total:.1f}%)")
    print(f"  V2 complete (L3+): {v2_ready:>6,} / {estate_total:>6,}  ({100*v2_ready/estate_total:.1f}%)")
    print(f"  Compared (L4+):    {compared:>6,} / {estate_total:>6,}  ({100*compared/estate_total:.1f}%)")
    print(f"  Validated (L5):    {level_counts[5]:>6,} / {estate_total:>6,}  ({100*level_counts[5]/estate_total:.1f}%)")
    print()
    print("=" * 76)


if __name__ == "__main__":
    main()
