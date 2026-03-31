"""src/corpus/feature_freeze.py — Feature definition freezing (Tier 3, Item 6).

Extracts all unique prediction claims as the feature vocabulary and provides
freeze/check mechanisms for OSF pre-registration compliance (G22).

Once frozen, any new claim not in the frozen set is flagged as "exploratory" —
it cannot be used in pre-registered SHAP analysis.

Usage:
    from src.corpus.feature_freeze import extract_claims, freeze_claims, check_claim

    # Extract current vocabulary
    claims = extract_claims()  # set of all unique claim strings

    # Freeze for a study
    freeze_claims("study_001")  # saves to data/feature_freezes/study_001.json

    # Check a new claim
    is_registered = check_claim("wealthy_through_career", "study_001")
"""
from __future__ import annotations

import json
from pathlib import Path

FREEZE_DIR = Path("data/feature_freezes")


def extract_claims() -> set[str]:
    """Extract all unique prediction claim strings from the current corpus."""
    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    claims: set[str] = set()
    for r in corpus.all():
        for pred in r.predictions:
            if isinstance(pred, dict) and "claim" in pred:
                claims.add(pred["claim"])
    return claims


def freeze_claims(study_id: str) -> Path:
    """Freeze the current claim vocabulary for a research study.

    Returns the path to the freeze file.
    """
    from src.corpus.snapshot import corpus_hash
    import datetime

    claims = sorted(extract_claims())
    h = corpus_hash()
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")

    FREEZE_DIR.mkdir(parents=True, exist_ok=True)
    path = FREEZE_DIR / f"freeze_{study_id}_{timestamp}.json"

    freeze_data = {
        "study_id": study_id,
        "timestamp": timestamp,
        "corpus_hash": h,
        "claim_count": len(claims),
        "claims": claims,
    }
    path.write_text(json.dumps(freeze_data, indent=2))
    return path


def check_claim(claim: str, study_id: str) -> bool:
    """Check if a claim is in a frozen vocabulary.

    Returns True if registered (can be used in pre-registered analysis).
    Returns False if exploratory (cannot be used).
    """
    # Find the most recent freeze for this study
    if not FREEZE_DIR.exists():
        return False

    freezes = sorted(FREEZE_DIR.glob(f"freeze_{study_id}_*.json"), reverse=True)
    if not freezes:
        return False

    data = json.loads(freezes[0].read_text())
    return claim in data["claims"]


def list_freezes() -> list[dict]:
    """List all frozen vocabularies."""
    if not FREEZE_DIR.exists():
        return []

    result = []
    for f in sorted(FREEZE_DIR.glob("freeze_*.json")):
        data = json.loads(f.read_text())
        result.append({
            "study_id": data["study_id"],
            "timestamp": data["timestamp"],
            "corpus_hash": data["corpus_hash"],
            "claim_count": data["claim_count"],
            "path": str(f),
        })
    return result
