"""src/calculations/weight_store.py — Versioned weight store for rule evaluation.

Architecture gap G4 + quality criterion Q6 (three version axes).

The weight store replaces hardcoded ``_WEIGHTS`` dicts with a versioned,
data-driven weight table.  Every output includes three version axes:

  1. **corpus_version** — which rules were used (corpus hash)
  2. **schema_version** — output format version
  3. **weight_version** — which calibration weights were applied

Initial state: base_weight copied from SCHOOL_WEIGHTS (scoring rules) and
confidence values (corpus rules).  empirical_weight = base_weight (no
calibration data yet — that's Phase B / G10).

Public API
----------
  WeightEntry      — one rule's weight data
  WeightStore      — versioned collection of weights
  get_weight_store — singleton accessor (built once, cached)
  VersionInfo      — the three version axes for any output
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G4+Q6", "session": "S328"}

logger = logging.getLogger(__name__)

# Current schema version — bump on breaking changes to EvalResult or WeightEntry
SCHEMA_VERSION = 1

# Current weight version — bump on each calibration run (Phase B)
WEIGHT_VERSION = 1


@dataclass(frozen=True)
class VersionInfo:
    """Three version axes for reproducibility (Q6).

    Any past prediction can be re-derived by specifying these three values.
    """
    corpus_version: str    # hash of corpus state
    schema_version: int    # output format version
    weight_version: int    # calibration generation


@dataclass
class WeightEntry:
    """Weight data for one rule.

    Fields
    ------
    rule_id : str
        The rule this weight applies to.
    base_weight : float
        Original weight from encoding (never changes).
    empirical_weight : float
        Current calibrated weight (starts = base, updated by G10).
    n : int
        Number of observations (0 until Phase B).
    ci_low : float
        Lower bound of 95% confidence interval.
    ci_high : float
        Upper bound of 95% confidence interval.
    contexts : dict
        Context-specific weight overrides (e.g., night_birth, day_birth).
    """
    rule_id: str
    base_weight: float
    empirical_weight: float
    n: int = 0
    ci_low: float = 0.0
    ci_high: float = 0.0
    contexts: dict[str, float] = field(default_factory=dict)


class WeightStore:
    """Versioned collection of rule weights.

    Provides fast lookup by rule_id + school, and carries version info
    for reproducibility.
    """

    def __init__(
        self,
        weights: dict[str, WeightEntry],
        *,
        school_weights: dict[str, dict[str, float]],
        corpus_version: str = "",
        weight_version: int = WEIGHT_VERSION,
    ):
        self._weights = weights
        self._school_weights = school_weights
        self._corpus_version = corpus_version
        self._weight_version = weight_version

    @property
    def version_info(self) -> VersionInfo:
        return VersionInfo(
            corpus_version=self._corpus_version,
            schema_version=SCHEMA_VERSION,
            weight_version=self._weight_version,
        )

    def get(self, rule_id: str, school: str = "parashari") -> float:
        """Get the effective weight for a rule.

        For scoring rules: returns the school-specific weight.
        For corpus rules: returns the empirical_weight (initially = confidence).
        """
        # Scoring rules — school-specific weights
        sw = self._school_weights.get(school, self._school_weights.get("parashari", {}))
        if rule_id in sw:
            return sw[rule_id]

        # Corpus rules — from WeightEntry
        entry = self._weights.get(rule_id)
        if entry is not None:
            return entry.empirical_weight

        return 0.0

    def get_entry(self, rule_id: str) -> Optional[WeightEntry]:
        """Get the full WeightEntry for a rule, or None."""
        return self._weights.get(rule_id)

    def school_weights(self, school: str = "parashari") -> dict[str, float]:
        """Get the full weight dict for a school (scoring rules only)."""
        return self._school_weights.get(school, self._school_weights.get("parashari", {}))

    @property
    def rule_count(self) -> int:
        return len(self._weights)

    @property
    def schools(self) -> list[str]:
        return list(self._school_weights.keys())


# ---------------------------------------------------------------------------
# Builder — constructs the initial weight store from existing data
# ---------------------------------------------------------------------------

def build_weight_store(*, corpus_version: str = "") -> WeightStore:
    """Build the weight store from current scoring rules + corpus rules.

    Scoring rule weights come from SCHOOL_WEIGHTS in scoring_rules.py.
    Corpus rule weights come from each rule's confidence value.
    """
    from src.corpus.scoring_rules import SCHOOL_WEIGHTS

    weights: dict[str, WeightEntry] = {}

    # Seed scoring rule weights from all schools
    all_scoring_ids: set[str] = set()
    for school_weights in SCHOOL_WEIGHTS.values():
        all_scoring_ids.update(school_weights.keys())

    for rule_id in sorted(all_scoring_ids):
        base = SCHOOL_WEIGHTS["parashari"].get(rule_id, 0.0)
        weights[rule_id] = WeightEntry(
            rule_id=rule_id,
            base_weight=base,
            empirical_weight=base,
        )

    # Seed corpus rule weights from confidence
    try:
        from src.corpus.combined_corpus import build_corpus
        corpus = build_corpus()
        for rule in corpus.all():
            if rule.rule_id not in weights:
                weights[rule.rule_id] = WeightEntry(
                    rule_id=rule.rule_id,
                    base_weight=rule.confidence,
                    empirical_weight=rule.confidence,
                )
    except ImportError:
        pass  # corpus module not available
    except Exception:
        logger.warning("Failed to seed weight store from corpus", exc_info=True)

    # Resolve corpus version
    if not corpus_version:
        try:
            from src.corpus.snapshot import corpus_hash
            corpus_version = corpus_hash()
        except ImportError:
            corpus_version = "unknown"
        except Exception:
            logger.warning("Failed to compute corpus hash", exc_info=True)
            corpus_version = "unknown"

    return WeightStore(
        weights=weights,
        school_weights=SCHOOL_WEIGHTS,
        corpus_version=corpus_version,
        weight_version=WEIGHT_VERSION,
    )


# ---------------------------------------------------------------------------
# Singleton accessor
# ---------------------------------------------------------------------------

_CACHED_STORE: Optional[WeightStore] = None


def get_weight_store() -> WeightStore:
    """Get the weight store (built once, cached for the process lifetime)."""
    global _CACHED_STORE
    if _CACHED_STORE is None:
        _CACHED_STORE = build_weight_store()
    return _CACHED_STORE


def reset_weight_store() -> None:
    """Reset the cached store (for testing)."""
    global _CACHED_STORE
    _CACHED_STORE = None


# ---------------------------------------------------------------------------
# D15+D17: JSON serialization / persistence
# ---------------------------------------------------------------------------

_WEIGHTS_DIR = Path("data/weights")


def save_weight_store(store: WeightStore, path: Optional[Path] = None) -> Path:
    """D17: Persist the weight store to JSON.

    Returns the path of the written file.
    """
    import json

    if path is None:
        _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
        path = _WEIGHTS_DIR / f"weights_v{store.version_info.weight_version}.json"

    data = {
        "version_info": {
            "corpus_version": store.version_info.corpus_version,
            "schema_version": store.version_info.schema_version,
            "weight_version": store.version_info.weight_version,
        },
        "school_weights": store._school_weights,
        "weights": {
            rule_id: {
                "base_weight": e.base_weight,
                "empirical_weight": e.empirical_weight,
                "n": e.n,
                "ci_low": e.ci_low,
                "ci_high": e.ci_high,
                "contexts": e.contexts,
            }
            for rule_id, e in store._weights.items()
        },
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True))
    return path


def load_weight_store(path: Path) -> WeightStore:
    """D17: Load a weight store from JSON."""
    import json

    data = json.loads(path.read_text())
    vi = data["version_info"]

    weights = {}
    for rule_id, w in data["weights"].items():
        weights[rule_id] = WeightEntry(
            rule_id=rule_id,
            base_weight=w["base_weight"],
            empirical_weight=w["empirical_weight"],
            n=w.get("n", 0),
            ci_low=w.get("ci_low", 0.0),
            ci_high=w.get("ci_high", 0.0),
            contexts=w.get("contexts", {}),
        )

    return WeightStore(
        weights=weights,
        school_weights=data["school_weights"],
        corpus_version=vi["corpus_version"],
        weight_version=vi["weight_version"],
    )


# ---------------------------------------------------------------------------
# D13: ScoringRule → RuleRecord adapter
# ---------------------------------------------------------------------------

def scoring_rules_as_records() -> list:
    """D13: Adapt ScoringRule objects to RuleRecord-compatible format.

    Returns a list that corpus tools (scorecard, auditor) can inspect
    alongside regular corpus rules.
    """
    from src.corpus.scoring_rules import SCORING_RULES, SCHOOL_WEIGHTS

    records = []
    for sr in SCORING_RULES:
        w_parashari = SCHOOL_WEIGHTS["parashari"].get(sr.weight_key, 0.0)
        records.append({
            "rule_id": f"SCORING_{sr.rule_id}",
            "source": "SCORING",
            "chapter": "house_scoring",
            "school": "parashari",
            "category": "structural_scoring",
            "description": sr.name,
            "confidence": 1.0,
            "verse_ref": sr.verse_ref,
            "condition_type": sr.condition_type,
            "weight_parashari": w_parashari,
            "is_wide_card": sr.is_wide_card,
            "accumulation": sr.accumulation.value,
            "phase": "1B_matrix",
            "system": "natal",
            "entity_target": "native",
            "outcome_direction": "favorable" if w_parashari > 0 else "unfavorable",
        })
    return records
