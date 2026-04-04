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
    """Load all rules for a source+chapter from combined corpus.

    V1 rules are soft-classified by category relevance. Rules in non-relevant
    categories are separated as 'excluded' but still tracked and reported.
    Returns (v1_included, v1_excluded, v2).
    """
    from src.corpus.combined_corpus import build_corpus
    corpus = build_corpus()
    relevant_cats = _RELEVANT_V1_CATEGORIES.get(chapter, None)
    v1_included, v1_excluded, v2 = [], [], []
    for r in corpus.all():
        if r.source != source or r.chapter != chapter:
            continue
        if r.last_modified_session >= "S310":
            v2.append(r)
        else:
            if relevant_cats is not None:
                # We have a relevance mapping for this chapter
                if not relevant_cats or r.category not in relevant_cats:
                    # Empty set = no V1 category is relevant; or category doesn't match
                    v1_excluded.append(r)
                else:
                    v1_included.append(r)
            else:
                # No mapping exists — include all V1 rules (unknown chapter)
                v1_included.append(r)
    return v1_included, v1_excluded, v2


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
    """Run migration audit for a single chapter. Returns report dict."""
    v1_rules, v1_excluded, v2_rules = _load_rules(source, chapter)

    # Extract V1 claims (from included rules only)
    v1_claims: list[dict] = []
    for r in v1_rules:
        claims = extract_claims(r.description)
        for c in claims:
            c["v1_rule_id"] = r.rule_id
            v1_claims.append(c)

    # Extract V2 claims
    v2_buckets: list[dict] = []
    for r in v2_rules:
        for pred in r.predictions:
            bucket = extract_v2_bucket(pred)
            bucket["v2_rule_id"] = r.rule_id
            v2_buckets.append(bucket)

    # Match
    results = {"FULL": 0, "PARTIAL": 0, "GAP_CRITICAL": 0, "UNMAPPED": 0}
    gaps: list[dict] = []
    partials: list[dict] = []
    unmapped: list[dict] = []
    low_confidence: list[dict] = []

    for v1c in v1_claims:
        result = match_v1_to_v2(v1c, v2_buckets)
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
            for b in v2_buckets:
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

    # Determine audit status (epistemically honest)
    # UNVERIFIABLE: no V1 baseline to compare against
    # VERIFIED: gaps=0, all partials annotated, confidence>=0.7
    # PARTIAL: some coverage but gaps/unmapped remain
    # INCOMPLETE: significant gaps
    if len(v1_rules) == 0:
        audit_status = "UNVERIFIABLE"
    elif results["GAP_CRITICAL"] == 0 and results["UNMAPPED"] == 0:
        audit_status = "VERIFIED"
    elif results["GAP_CRITICAL"] == 0:
        audit_status = "PARTIAL"
    else:
        audit_status = "INCOMPLETE"

    # Integrity warning: if more rules excluded than included, flag it
    integrity_warning = ""
    if v1_excluded and len(v1_excluded) > len(v1_rules):
        integrity_warning = (
            f"More V1 rules excluded ({len(v1_excluded)}) than included "
            f"({len(v1_rules)}) — chapter integrity risk"
        )

    return {
        "chapter": chapter,
        "source": source,
        "audit_date": str(date.today()),
        "v1_rules": len(v1_rules),
        "v1_excluded": len(v1_excluded),
        "v2_rules": len(v2_rules),
        "v1_claims_extracted": len(v1_claims),
        "v2_claims_extracted": len(v2_buckets),
        "matching": {
            "full": results["FULL"],
            "partial": results["PARTIAL"],
            "gap_critical": results["GAP_CRITICAL"],
            "unmapped": results["UNMAPPED"],
        },
        "confidence": round(avg_confidence, 2),
        "confidence_tier": conf_tier,
        "audit_status": audit_status,
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
        f"V2 rules: {report['v2_rules']} → {report['v2_claims_extracted']} claims extracted",
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
    status = report.get("audit_status", "INCOMPLETE")
    if status == "UNVERIFIABLE":
        lines.append("\nStatus: UNVERIFIABLE (no V1 baseline — V2 encoding cannot be cross-checked)")
    elif status == "VERIFIED":
        lines.append("\nStatus: VERIFIED (all V1 claims matched)")
    elif status == "PARTIAL":
        lines.append(f"\nStatus: PARTIAL (0 gaps, {m['unmapped']} unmapped need review)")
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
