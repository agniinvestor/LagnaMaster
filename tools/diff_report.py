"""
Aggregate reporting across all cross-validation results.

Outputs: module stability index, ranked disagreements, systematic patterns,
health dashboard metrics.

Usage:
    .venv/bin/python tools/diff_report.py [--json]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS_DIR = ROOT / "tests" / "fixtures" / "verified_360_results"
HISTORY_PATH = ROOT / "tests" / "fixtures" / "verification_history.json"

# Field → module ownership
FIELD_MODULE = defaultdict(lambda: "unknown")
FIELD_MODULE.update({
    "lagna_degree": "positions",
    "lagna_sign": "positions",
})
for _p in ["sun", "moon", "mars", "mercury", "jupiter", "venus",
           "saturn", "rahu", "ketu"]:
    FIELD_MODULE[f"longitude_{_p}"] = "positions"
    FIELD_MODULE[f"sign_{_p}"] = "positions"
    FIELD_MODULE[f"nakshatra_{_p}"] = "nakshatra"


def generate_report(as_json: bool = False) -> dict | None:
    """Generate aggregate cross-validation report."""
    results = []
    for path in sorted(RESULTS_DIR.glob("*.json")):
        results.append(json.loads(path.read_text()))

    if not results:
        print("No results found.")
        return None

    total_charts = len(results)
    total_fields = 0
    total_agreement = 0
    total_systematic = 0
    total_random = 0

    module_total: Counter = Counter()
    module_agreement: Counter = Counter()
    random_list = []

    for r in results:
        s = r.get("summary", {})
        total_fields += s.get("total_fields", 0)
        total_agreement += s.get("agreement", 0)
        total_systematic += s.get("systematic", 0)
        total_random += s.get("random", 0)

        for fname, v in r.get("verdicts", {}).items():
            module = FIELD_MODULE[fname]
            module_total[module] += 1
            if v["status"] == "agreement":
                module_agreement[module] += 1
            elif v["status"] == "random_disagreement":
                random_list.append({
                    "chart_id": r["chart_id"],
                    "field": fname,
                    "lm": v.get("lm"),
                    "pjh": v.get("pjh"),
                    "diff": v.get("diff"),
                })

    stability = {}
    for module in sorted(module_total):
        total = module_total[module]
        agreed = module_agreement[module]
        stability[module] = round(agreed / total, 4) if total > 0 else 0.0

    field_counts = Counter(d["field"] for d in random_list)

    report = {
        "total_charts": total_charts,
        "total_fields": total_fields,
        "agreement_rate": round(total_agreement / total_fields, 4) if total_fields else 0,
        "agreement": total_agreement,
        "systematic": total_systematic,
        "random": total_random,
        "stability_index": stability,
        "random_disagreements_by_field": dict(field_counts.most_common()),
        "random_disagreement_details": random_list[:20],
    }

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("=== Cross-Validation Report ===")
        print(f"Charts: {total_charts}")
        print(f"Fields: {total_fields}")
        print(f"Agreement rate: {report['agreement_rate']:.1%}")
        print(f"  Agreement: {total_agreement}")
        print(f"  Systematic: {total_systematic}")
        print(f"  Random: {total_random}")
        print("\n--- Module Stability Index ---")
        for module, score in sorted(stability.items(), key=lambda x: x[1]):
            bar = "#" * int(score * 20) + "." * (20 - int(score * 20))
            print(f"  {module:<15} {bar} {score:.1%}")
        if field_counts:
            print("\n--- Random Disagreements (by field) ---")
            for field, count in field_counts.most_common(10):
                print(f"  {field}: {count} charts")

    # Append to verification history
    history = []
    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text())
    history.append({
        "date": "2026-04-03",
        "agreement_rate": report["agreement_rate"],
        "random_disagreements": total_random,
        "systematic_patterns": total_systematic,
        "total_charts": total_charts,
    })
    HISTORY_PATH.write_text(json.dumps(history, indent=2))

    return report


def main():
    parser = argparse.ArgumentParser(description="Aggregate diff report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    generate_report(as_json=args.json)


if __name__ == "__main__":
    main()
