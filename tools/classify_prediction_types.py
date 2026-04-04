#!/usr/bin/env python3
"""tools/classify_prediction_types.py — Assign prediction_type to rules missing it."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus.combined_corpus import build_corpus

_HEALTH_KEYWORDS = {"disease", "sickly", "health", "illness", "pain", "wound", "fever", "death",
                     "stomach", "digestion", "inflammation"}
_EVENT_KEYWORDS = {"marriage", "birth", "travel", "accident", "gain", "loss", "age",
                    "marry", "born", "journey"}
_TRAIT_KEYWORDS = {"virtuous", "intelligent", "brave", "lazy", "learned", "handsome", "beautiful",
                    "righteous", "generous", "cruel", "noble"}


def classify(claim: str) -> str:
    """Classify a prediction claim into type category."""
    words = set(claim.lower().split())
    if words & _HEALTH_KEYWORDS:
        return "health"
    if words & _EVENT_KEYWORDS:
        return "event"
    if words & _TRAIT_KEYWORDS:
        return "trait"
    return "status"


def main():
    corpus = build_corpus()
    rules = [r for r in corpus.all() if r.phase.startswith("1B")]
    missing = [r for r in rules if not getattr(r, "prediction_type", "")]
    print(f"Rules without prediction_type: {len(missing)}/{len(rules)}")
    counts = {"trait": 0, "event": 0, "status": 0, "health": 0}
    for r in missing:
        claims = " ".join(p.get("claim", "") for p in (r.predictions or []))
        pt = classify(claims)
        counts[pt] += 1
    print(f"Classification: {counts}")
    print("NOTE: This is a dry-run report. Actual assignment requires modifying chapter files.")


if __name__ == "__main__":
    main()
