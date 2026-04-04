#!/usr/bin/env python3
"""tools/migration_audit.py — Legacy V1→V2 migration audit tool.

Compares V1 legacy rules against V2 structured rules for a given chapter.
Extracts claims from both using two-tier bucketing (domain+direction +
mechanism tags), then matches to find FULL/PARTIAL/GAP/UNMAPPED.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --chapter 29 --json
    PYTHONPATH=. .venv/bin/python tools/migration_audit.py --all
"""
from __future__ import annotations

import argparse
import json
from datetime import date

from src.corpus.migration_tags import extract_claims, extract_v2_bucket

# ── V1 Category Relevance Filter ─────────────────────────────────────────
# Only these V1 categories are semantically relevant to each V2 chapter.
# V1 rules in other categories (bhava_signification, graha_in_rashi,
# graha_bhava, graha_phala, lagna, etc.) are cross-chapter noise that
# was incorrectly tagged with the chapter number during legacy encoding.
_RELEVANT_V1_CATEGORIES: dict[str, set[str]] = {
    "Ch.12": {"1st_house_effects"},
    "Ch.13": {"2nd_house_effects"},
    "Ch.14": {"3rd_house_effects"},
    "Ch.15": {"4th_house_effects"},
    "Ch.16": {"5th_house_effects"},
    "Ch.17": {"6th_house_effects"},
    "Ch.18": {"7th_house_effects"},
    "Ch.19": {"8th_house_effects"},
    "Ch.20": {"9th_house_effects"},
    "Ch.21": {"10th_house_effects"},
    "Ch.22": {"11th_house_effects"},
    "Ch.23": {"12th_house_effects"},
    "Ch.24": {"bhava_phala"},
    "Ch.25": set(),  # No V1 category matches upagraha effects
    "Ch.29": set(),  # No V1 category matches pada effects
}


def _load_rules(source: str, chapter: str):
    """Load rules for migration audit.

    V1 rules: loaded from the specified chapter, soft-classified by category
    relevance. Non-relevant categories separated as 'excluded'.

    V2 rules: loaded from the ENTIRE V2 corpus (all chapters). This is critical
    because V2 coverage of a concept can span multiple chapters. E.g., "lagna
    lord in 6th" may be in Ch.12 V2 (1st house effects) AND Ch.24 V2 (lords
    in houses). Matching against only same-chapter V2 creates false gaps.

    Returns (v1_included, v1_excluded, v2_same_chapter, v2_all).

    Two V2 pools are returned:
    - v2_same_chapter: V2 rules from the same chapter (for precision matching)
    - v2_all: ALL V2 rules from same source (for gap detection)
    Precision uses same-chapter; gap detection uses full corpus.
    """
    from src.corpus.combined_corpus import build_corpus
    corpus = build_corpus()
    relevant_cats = _RELEVANT_V1_CATEGORIES.get(chapter, None)
    v1_included, v1_excluded = [], []
    v2_same_chapter = []
    v2_all = []
    for r in corpus.all():
        if r.source != source:
            continue
        if r.last_modified_session >= "S310":
            v2_all.append(r)
            if r.chapter == chapter:
                v2_same_chapter.append(r)
        elif r.chapter == chapter:
            if relevant_cats is not None:
                if not relevant_cats or r.category not in relevant_cats:
                    v1_excluded.append(r)
                else:
                    v1_included.append(r)
            else:
                v1_included.append(r)
    return v1_included, v1_excluded, v2_same_chapter, v2_all


def match_v1_to_v2(v1_bucket: dict, v2_buckets: list[dict]) -> str:
    """Match a single V1 claim bucket against all V2 claim buckets.

    Uses subset matching: V1 mechanisms must be a subset of V2 mechanisms
    for a FULL match.

    Returns: "FULL", "PARTIAL", "GAP_CRITICAL", or "UNMAPPED"
    """
    v1_domain_dir = v1_bucket.get("domain_direction", "")
    v1_mechs = set(v1_bucket.get("mechanisms", []))
    confidence = v1_bucket.get("confidence", 1.0)

    # Step 0: Unmapped check
    if confidence < 0.3 and not v1_domain_dir:
        return "UNMAPPED"

    # Step 1: Domain+Direction match
    if not v1_domain_dir:
        return "UNMAPPED"

    domain_matches = [b for b in v2_buckets if b["domain_direction"] == v1_domain_dir]
    if not domain_matches:
        return "GAP_CRITICAL"

    # Step 2: Mechanism match (subset-based)
    if not v1_mechs:
        return "FULL"

    v2_mechs_union: set[str] = set()
    for b in domain_matches:
        v2_mechs_union.update(b.get("mechanisms", []))

    if v1_mechs <= v2_mechs_union:
        return "FULL"
    elif v1_mechs & v2_mechs_union:
        return "PARTIAL"
    else:
        return "PARTIAL"


def audit_chapter(source: str, chapter: str) -> dict:
    """Run migration audit for a single chapter. Returns report dict.

    Uses dual-pool matching:
    - Same-chapter V2: for FULL/PARTIAL precision (strict)
    - All-chapter V2: for gap detection only (prevents false GAP_CRITICAL)

    A claim is GAP_CRITICAL only if NO V2 rule anywhere covers its domain.
    But FULL requires a same-chapter V2 match (prevents overmatching).
    """
    v1_rules, v1_excluded, v2_same, v2_all = _load_rules(source, chapter)

    # Extract V1 claims (from included rules only)
    v1_claims: list[dict] = []
    for r in v1_rules:
        claims = extract_claims(r.description)
        for c in claims:
            c["v1_rule_id"] = r.rule_id
            v1_claims.append(c)

    # Extract V2 claims — both pools
    v2_same_buckets: list[dict] = []
    for r in v2_same:
        for pred in r.predictions:
            bucket = extract_v2_bucket(pred)
            bucket["v2_rule_id"] = r.rule_id
            v2_same_buckets.append(bucket)

    v2_all_buckets: list[dict] = []
    for r in v2_all:
        for pred in r.predictions:
            bucket = extract_v2_bucket(pred)
            bucket["v2_rule_id"] = r.rule_id
            v2_all_buckets.append(bucket)

    # Match
    results = {"FULL": 0, "PARTIAL": 0, "GAP_CRITICAL": 0, "UNMAPPED": 0}
    gaps: list[dict] = []
    partials: list[dict] = []
    unmapped: list[dict] = []
    low_confidence: list[dict] = []

    for v1c in v1_claims:
        # Dual-pool matching:
        # 1. Try same-chapter V2 first (precision)
        # 2. If GAP_CRITICAL in same-chapter, check full corpus (recall)
        # This prevents false gaps while maintaining match precision
        result = match_v1_to_v2(v1c, v2_same_buckets)
        if result == "GAP_CRITICAL":
            # Check if ANY V2 rule covers this domain (cross-chapter)
            cross_result = match_v1_to_v2(v1c, v2_all_buckets)
            if cross_result != "GAP_CRITICAL":
                # Domain exists elsewhere — downgrade to PARTIAL
                # (covered somewhere in V2, but not in same chapter)
                result = "PARTIAL"
        results[result] = results.get(result, 0) + 1

        if result == "GAP_CRITICAL":
            gaps.append({
                "type": "GAP_CRITICAL",
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_claim": v1c["domain_direction"],
                "v1_mechanisms": v1c.get("mechanisms", []),
                "v1_text": v1c.get("source_text", "")[:200],
            })
        elif result == "PARTIAL":
            v1_mechs = set(v1c.get("mechanisms", []))
            v2_mechs_union: set[str] = set()
            for b in v2_same_buckets:
                if b["domain_direction"] == v1c["domain_direction"]:
                    v2_mechs_union.update(b.get("mechanisms", []))
            missing = v1_mechs - v2_mechs_union
            partials.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_bucket": v1c["domain_direction"],
                "v1_mechanisms": list(v1_mechs),
                "v2_mechanisms": list(v2_mechs_union),
                "missing_mechanisms": list(missing),
                "annotation": None,
            })
        elif result == "UNMAPPED":
            unmapped.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_text": v1c.get("source_text", "")[:200],
                "confidence": v1c.get("confidence", 0),
            })

        if v1c.get("confidence", 1.0) < 0.5 and result != "UNMAPPED":
            low_confidence.append({
                "v1_rule_id": v1c.get("v1_rule_id", ""),
                "v1_text": v1c.get("source_text", "")[:200],
                "extracted_bucket": v1c["domain_direction"],
                "confidence": v1c.get("confidence", 0),
            })

    avg_confidence = (
        sum(c.get("confidence", 0) for c in v1_claims) / len(v1_claims)
        if v1_claims else 0.0
    )

    # Confidence tier
    if avg_confidence >= 0.8:
        conf_tier = "HIGH"
    elif avg_confidence >= 0.5:
        conf_tier = "MEDIUM"
    else:
        conf_tier = "LOW"

    # Determine audit status (epistemically honest, two axes)
    # Axis 1: V1 cross-validation status
    # Axis 2: verse audit coverage (from scorecard)
    if len(v1_rules) == 0 and len(v1_excluded) > 0:
        # V1 rules exist but all excluded as out-of-scope
        audit_status = "VERSE_ONLY"  # verified by verse audit, no V1 cross-check possible
    elif len(v1_rules) == 0 and len(v1_excluded) == 0:
        audit_status = "VERSE_ONLY"  # no V1 at all
    elif results["GAP_CRITICAL"] == 0 and results["UNMAPPED"] == 0:
        audit_status = "CROSS_VALIDATED"
    elif results["GAP_CRITICAL"] == 0:
        audit_status = "PARTIAL"
    else:
        audit_status = "INCOMPLETE"

    # Audit confidence tier based on excluded percentage
    total_v1 = len(v1_rules) + len(v1_excluded)
    if total_v1 == 0:
        audit_confidence_tier = "N/A"
    elif len(v1_excluded) / total_v1 < 0.2:
        audit_confidence_tier = "HIGH"
    elif len(v1_excluded) / total_v1 < 0.5:
        audit_confidence_tier = "MEDIUM"
    else:
        audit_confidence_tier = "LOW"

    # Integrity warning
    integrity_warning = ""
    if v1_excluded and len(v1_excluded) > len(v1_rules):
        integrity_warning = (
            f"More V1 rules excluded ({len(v1_excluded)}) than included "
            f"({len(v1_rules)}) — auditing on minority data"
        )

    return {
        "chapter": chapter,
        "source": source,
        "audit_date": str(date.today()),
        "v1_rules": len(v1_rules),
        "v1_excluded": len(v1_excluded),
        "v2_rules_same_chapter": len(v2_same),
        "v2_rules_total": len(v2_all),
        "v1_claims_extracted": len(v1_claims),
        "v2_claims_extracted": len(v2_same_buckets),
        "matching": {
            "full": results["FULL"],
            "partial": results["PARTIAL"],
            "gap_critical": results["GAP_CRITICAL"],
            "unmapped": results["UNMAPPED"],
        },
        "confidence": round(avg_confidence, 2),
        "confidence_tier": conf_tier,
        "audit_status": audit_status,
        "audit_confidence_tier": audit_confidence_tier,
        "integrity_warning": integrity_warning,
        "excluded_categories": sorted({r.category for r in v1_excluded}) if v1_excluded else [],
        "gaps": gaps,
        "partials": partials,
        "unmapped": unmapped,
        "low_confidence": low_confidence,
    }


def format_report(report: dict) -> str:
    """Format audit report as CLI text."""
    ch = report["chapter"]
    excluded = report.get("v1_excluded", 0)
    lines = [
        f"Migration Audit — BPHS {ch}",
        "=" * 40,
        f"V1 rules: {report['v1_rules']} included, {excluded} excluded (out-of-scope)",
        f"  -> {report['v1_claims_extracted']} claims extracted",
        f"V2 rules: {report['v2_rules_same_chapter']} same-chapter, {report['v2_rules_total']} total → {report['v2_claims_extracted']} claims matched against",
        f"Confidence: {report['confidence']:.0%} ({report['confidence_tier']})",
    ]
    if report.get("excluded_categories"):
        lines.append(f"  Excluded categories: {', '.join(report['excluded_categories'])}")
    if report.get("integrity_warning"):
        lines.append(f"  WARNING: {report['integrity_warning']}")
    lines.append("")

    m = report["matching"]
    total = sum(m.values())
    for key in ("full", "partial", "gap_critical", "unmapped"):
        count = m[key]
        pct = f"{count / total * 100:.0f}%" if total > 0 else "0%"
        label = key.upper().replace("_", " ")
        marker = ""
        if key == "gap_critical" and count > 0:
            marker = "  ← domain missing"
        elif key == "partial" and count > 0:
            marker = "  ← mechanism loss"
        elif key == "unmapped" and count > 0:
            marker = "  ← manual review"
        lines.append(f"  {label:20s}: {count:4d} ({pct:>4s}){marker}")

    # Status (epistemically honest)
    act = report.get("audit_confidence_tier", "N/A")
    status = report.get("audit_status", "INCOMPLETE")
    if status == "VERSE_ONLY":
        lines.append("\nStatus: VERSE_ONLY (V2 verified by verse audit, no V1 cross-check available)")
    elif status == "CROSS_VALIDATED":
        lines.append(f"\nStatus: CROSS_VALIDATED (all V1 claims matched) [audit confidence: {act}]")
    elif status == "PARTIAL":
        lines.append(f"\nStatus: PARTIAL (0 gaps, {m['unmapped']} unmapped need review) [audit confidence: {act}]")
    else:
        reasons = []
        if m["gap_critical"] > 0:
            reasons.append(f"{m['gap_critical']} gaps")
        unannotated = sum(1 for p in report["partials"] if not p.get("annotation"))
        if unannotated:
            reasons.append(f"{unannotated} unannotated partials")
        if m["unmapped"] > 0:
            reasons.append(f"{m['unmapped']} unmapped")
        lines.append(f"\nStatus: INCOMPLETE ({', '.join(reasons)})")

    if report["gaps"]:
        lines.append("\nGAPS (must fix):")
        for g in report["gaps"]:
            lines.append(f"  {g['v1_rule_id']}: {g['v1_claim']} → no V2 match")
            if g.get("v1_text"):
                lines.append(f"    text: {g['v1_text'][:100]}")

    if report["partials"]:
        lines.append("\nPARTIALS (must annotate):")
        for p in report["partials"]:
            missing = ", ".join(p.get("missing_mechanisms", []))
            lines.append(
                f"  {p['v1_rule_id']}: {p['v1_bucket']} missing [{missing}]"
            )

    if report["unmapped"]:
        lines.append("\nUNMAPPED (manual review):")
        for u in report["unmapped"]:
            lines.append(
                f"  {u['v1_rule_id']}: \"{u['v1_text'][:80]}\" "
                f"(conf={u['confidence']:.2f})"
            )

    if report["low_confidence"]:
        lines.append("\nLOW CONFIDENCE (review):")
        for lc in report["low_confidence"]:
            lines.append(
                f"  {lc['v1_rule_id']}: \"{lc['v1_text'][:80]}\" "
                f"→ {lc['extracted_bucket']} (conf={lc['confidence']:.2f})"
            )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Legacy V1→V2 Migration Audit"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chapter", help="Chapter number (e.g., 29)")
    group.add_argument(
        "--all", action="store_true", help="Audit all V2-upgraded chapters"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--source", default="BPHS", help="Source text (default: BPHS)"
    )

    args = parser.parse_args()

    if args.chapter:
        chapters = [f"Ch.{args.chapter}"]
    else:
        # All V2-upgraded chapters
        chapters = [
            f"Ch.{n}"
            for n in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29]
        ]

    for ch in chapters:
        report = audit_chapter(args.source, ch)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_report(report))
            print()


if __name__ == "__main__":
    main()
