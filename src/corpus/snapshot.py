"""src/corpus/snapshot.py — Corpus snapshot API for versioning and reproducibility.

Creates immutable snapshots of the corpus for:
  - Phase 6: Model-corpus version pinning
  - Phase 10: OSF pre-registration feature freezing
  - Operational: Error forensics (which corpus version was active when?)

Usage:
    from src.corpus.snapshot import create_snapshot, load_snapshot, corpus_hash

    # Get deterministic hash of current corpus state
    h = corpus_hash()

    # Save snapshot
    path = create_snapshot(label="pre_phase6_training")

    # Load snapshot
    rules = load_snapshot(path)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SNAPSHOT_DIR = Path("data/corpus_snapshots")


def corpus_hash() -> str:
    """Compute a deterministic hash of the current corpus state.

    The hash is based on rule_id + confidence + primary_condition for each rule,
    sorted by rule_id. This means any change to rules, conditions, or confidence
    changes the hash — triggering model retraining.
    """
    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    rules = sorted(corpus.all(), key=lambda r: r.rule_id)

    hasher = hashlib.sha256()
    for r in rules:
        # Hash the identity-defining fields
        identity = f"{r.rule_id}|{r.confidence:.4f}|{json.dumps(r.primary_condition, sort_keys=True)}|{r.outcome_direction}|{','.join(r.outcome_domains)}"
        hasher.update(identity.encode("utf-8"))

    return hasher.hexdigest()[:16]


def create_snapshot(label: str = "") -> Path:
    """Create an immutable JSON snapshot of the current corpus.

    Returns the path to the snapshot file.
    """
    from src.corpus.combined_corpus import build_corpus
    import datetime

    corpus = build_corpus()
    rules = sorted(corpus.all(), key=lambda r: r.rule_id)
    h = corpus_hash()

    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"corpus_{timestamp}_{h}.json"
    if label:
        filename = f"corpus_{label}_{timestamp}_{h}.json"

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / filename

    snapshot_data = {
        "hash": h,
        "timestamp": timestamp,
        "label": label,
        "rule_count": len(rules),
        "rules": [r.to_dict() for r in rules],
    }

    path.write_text(json.dumps(snapshot_data, indent=2, default=str))
    return path


def load_snapshot(path: Path | str) -> list[dict]:
    """Load rules from a snapshot file. Returns list of rule dicts."""
    path = Path(path)
    data = json.loads(path.read_text())
    return data["rules"]


def get_snapshot_info(path: Path | str) -> dict:
    """Get metadata from a snapshot without loading all rules."""
    path = Path(path)
    data = json.loads(path.read_text())
    return {
        "hash": data["hash"],
        "timestamp": data["timestamp"],
        "label": data.get("label", ""),
        "rule_count": data["rule_count"],
    }
