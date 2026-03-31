"""tools/verse_audit.py — Verse-by-verse granularity audit tool.

Goes back to SOURCE — for each sloka, lists what's encoded vs what the
granularity definition says SHOULD be encoded. This catches omission
errors that keyword checks on encoded data cannot find.

The auditor reads the PDF, fills in the audit template for each verse,
and the tool compares against the encoded rules.

Usage:
    PYTHONPATH=. .venv/bin/python tools/verse_audit.py --chapter 12

Output: A checklist showing each verse, its claims, and whether each
claim has a corresponding rule.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AUDIT_DIR = Path("data/verse_audits")


def create_audit_template(chapter: int) -> dict:
    """Create an empty audit template for a chapter.

    The auditor fills this in by reading the PDF.
    Each verse gets a list of claims identified from the text.
    """
    template = {
        "chapter": chapter,
        "source": "BPHS",
        "translator": "santhanam",
        "auditor": "",
        "audit_date": "",
        "status": "template",
        "verses": {},
    }
    return template


def load_audit(chapter: int) -> dict | None:
    """Load a completed audit for a chapter."""
    path = AUDIT_DIR / f"ch{chapter}_audit.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


def save_audit(chapter: int, audit: dict) -> Path:
    """Save an audit file."""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    path = AUDIT_DIR / f"ch{chapter}_audit.json"
    path.write_text(json.dumps(audit, indent=2))
    return path


def compare_audit_to_rules(chapter: int) -> dict:
    """Compare a verse audit against encoded rules.

    Returns a report of matches, missing rules, and extra rules.
    """
    audit = load_audit(chapter)
    if not audit:
        return {"error": f"No audit file for Ch.{chapter}. Run --create first."}

    # Load encoded rules
    try:
        mod = __import__(f"src.corpus.bphs_v2_ch{chapter}", fromlist=["x"])
        reg = getattr(mod, f"BPHS_V2_CH{chapter}_REGISTRY")
        rules = reg.all()
    except Exception as e:
        return {"error": f"Cannot load Ch.{chapter} rules: {e}"}

    # Build verse→rules map
    rules_by_verse: dict[str, list] = {}
    for r in rules:
        # Extract verse numbers
        for m in re.findall(r"v\.(\d+)", r.verse_ref):
            v = int(m)
            rules_by_verse.setdefault(v, []).append(r.rule_id)

    report = {
        "chapter": chapter,
        "total_audit_claims": 0,
        "total_encoded_rules": len(rules),
        "matched": [],
        "missing": [],
        "extra_rules": [],
    }

    for verse_str, verse_data in audit.get("verses", {}).items():
        verse_num = int(verse_str)
        claims = verse_data.get("claims", [])
        report["total_audit_claims"] += len(claims)

        encoded = rules_by_verse.get(verse_num, [])

        for claim in claims:
            claim_text = claim.get("claim", "")
            matched = False
            for rid in encoded:
                rule = next((r for r in rules if r.rule_id == rid), None)
                if rule and claim_text.lower() in rule.description.lower():
                    matched = True
                    report["matched"].append({
                        "verse": verse_num,
                        "claim": claim_text,
                        "rule_id": rid,
                    })
                    break
            if not matched:
                report["missing"].append({
                    "verse": verse_num,
                    "claim": claim_text,
                    "type": claim.get("type", "unknown"),
                })

    return report


def main():
    parser = argparse.ArgumentParser(description="Verse-by-verse granularity audit")
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--create", action="store_true",
                       help="Create empty audit template")
    parser.add_argument("--compare", action="store_true",
                       help="Compare audit against encoded rules")
    args = parser.parse_args()

    if args.create:
        template = create_audit_template(args.chapter)
        path = save_audit(args.chapter, template)
        print(f"Template created at {path}")
        print("Fill in verses by reading the PDF, then run --compare")
    elif args.compare:
        report = compare_audit_to_rules(args.chapter)
        if "error" in report:
            print(report["error"])
            sys.exit(1)
        print(f"Ch.{args.chapter} Granularity Audit")
        print(f"  Audit claims: {report['total_audit_claims']}")
        print(f"  Encoded rules: {report['total_encoded_rules']}")
        print(f"  Matched: {len(report['matched'])}")
        print(f"  Missing: {len(report['missing'])}")
        if report["missing"]:
            print("\nMISSING RULES:")
            for m in report["missing"]:
                print(f"  v.{m['verse']}: [{m['type']}] {m['claim']}")
    else:
        print("Specify --create or --compare")


if __name__ == "__main__":
    main()
