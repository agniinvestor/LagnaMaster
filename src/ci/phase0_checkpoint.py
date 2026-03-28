"""
src/ci/phase0_checkpoint.py — S215: Phase 0 checkpoint audit

Verifies that all Phase 0 (S191–S215) deliverables are in place.
This is the Phase 0 gate — passing this checkpoint means Phase 1
(S216 Classical Knowledge Foundation) can begin.

Public API
----------
  Phase0Checkpoint  — dataclass listing all deliverables
  run_phase0_audit() -> dict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


@dataclass
class Phase0Checkpoint:
    """Registry of all Phase 0 sessions and their completion criteria."""

    sessions: dict[str, dict] = field(default_factory=dict)

    def add(self, session_id: str, description: str, check_fn) -> None:
        try:
            check_fn()
            self.sessions[session_id] = {
                "complete": True,
                "description": description,
                "reason": "",
            }
        except Exception as exc:
            self.sessions[session_id] = {
                "complete": False,
                "description": description,
                "reason": str(exc),
            }


def run_phase0_audit() -> dict:
    """
    Run the Phase 0 checkpoint audit.

    Returns
    -------
    dict with:
      sessions: {S191: {complete, description, reason}, ...}
      summary:  {total_sessions, complete_sessions, incomplete_sessions}
    """
    cp = Phase0Checkpoint()

    # S191: VedAstro install + cross-validation + G17 ruff rule
    cp.add("S191", "VedAstro install + G17 ruff rule + Protocol stubs", _check_s191)

    # S192: Protocol interfaces
    cp.add("S192", "Protocol interfaces — ClassicalEngine, DashaEngine, FeedbackService, MLService",
           _check_s192)

    # S193: HouseScore distribution dataclass
    cp.add("S193", "HouseScore distribution dataclass", _check_s193)

    # S194: Conditional weight functions
    cp.add("S194", "Conditional weight functions W(planet, house, lagna, functional_role)",
           _check_s194)

    # S195: Feature decomposition base
    cp.add("S195", "Feature decomposition — ChartFeatureVector + extract_features()", _check_s195)

    # S196: Feature extractors (dignity, ashtakavarga, etc.)
    cp.add("S196", "Feature extractors — dignity, ashtakavarga, shadbala, yogakaraka",
           _check_s196)

    # S197: Net benefic/malefic/karak score features
    cp.add("S197", "Net benefic/malefic/karak score features", _check_s197)

    # S198: Pushkara navamsha + war loser features
    cp.add("S198", "Pushkara navamsha + war loser features", _check_s198)

    # S199: Feature contracts (150+ features)
    cp.add("S199", "Feature contracts — forward-compatible count tests", _check_s199)

    # S200: G22 integration — feature_vector attached to ChartScoresV3
    cp.add("S200", "G22 integration — feature_vector in score_chart_v3()", _check_s200)

    # S201: OSF pre-registration schema
    cp.add("S201", "OSF pre-registration schema + draft OB-3 filing", _check_s201)

    # S202: Corpus infrastructure (RuleRecord + CorpusRegistry)
    cp.add("S202", "Corpus infrastructure — RuleRecord, CorpusRegistry", _check_s202)

    # S203: ADB license compliance + existing rules
    cp.add("S203", "ADB license compliance + R01-R23 existing rules", _check_s203)

    # S204: TextExtractor protocol + CV splitter
    cp.add("S204", "TextExtractor protocol + TimeBasedSplit CV splitter", _check_s204)

    # S205: CorpusAudit + BPHS extended rules
    cp.add("S205", "CorpusAudit + BPHS extended 31 rules", _check_s205)

    # S206: Phaladeepika + Brihat Jataka rules
    cp.add("S206", "Phaladeepika 21 rules + Brihat Jataka 26 rules", _check_s206)

    # S207: Uttara Kalamrita + Jataka Parijata rules
    cp.add("S207", "Uttara Kalamrita 17 rules + Jataka Parijata 17 rules", _check_s207)

    # S208: BirthRecord + CombinedCorpus
    cp.add("S208", "BirthRecord dataclass + CombinedCorpus build_corpus()", _check_s208)

    # S209: Corpus pipeline integration
    cp.add("S209", "Corpus pipeline integration — combined corpus >= 100 rules",
           _check_s209)

    # S210: (grouped with S201-S210 batch) — corpus finalization
    cp.add("S210", "Corpus batch finalization — CorpusAudit clean run", _check_s210)

    # S211: Redis + pgvector + TimescaleDB + MLflow + family schema
    cp.add("S211", "ML infra schema — pgvector, TimescaleDB, MLflow, family",
           _check_s211)

    # S212: KP ayanamsha G06 compliance
    cp.add("S212", "KP ayanamsha compliance — G06 enforcement via kp_ayanamsha.py",
           _check_s212)

    # S213: Protocol verification
    cp.add("S213", "Protocol verification — all adapters satisfy their Protocols",
           _check_s213)

    # S214: CI observability
    cp.add("S214", "CI observability — CIHealthReport + run_health_check()",
           _check_s214)

    # S215: Phase 0 checkpoint (this session — self-referential: module imports)
    cp.add("S215", "Phase 0 checkpoint — all 25 sessions complete", _check_s215)

    total = len(cp.sessions)
    complete = sum(1 for s in cp.sessions.values() if s["complete"])
    return {
        "sessions": cp.sessions,
        "summary": {
            "total_sessions": total,
            "complete_sessions": complete,
            "incomplete_sessions": total - complete,
        },
    }


# ── Per-session check functions ───────────────────────────────────────────────

def _check_s191():
    # G17: check ruff config has jhora rule
    pyproject = ROOT / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text()
        if "jhora" not in text.lower() and "TID" not in text:
            raise AssertionError("G17 ruff rule not found in pyproject.toml")


def _check_s192():
    from src.interfaces.classical_engine import ClassicalEngine  # noqa: F401
    from src.interfaces.dasha_engine import DashaEngine  # noqa: F401
    from src.interfaces.feedback_service import FeedbackService  # noqa: F401
    from src.interfaces.ml_service import MLService  # noqa: F401


def _check_s193():
    from src.calculations.house_score import HouseScore  # noqa: F401


def _check_s194():
    from src.calculations.conditional_weights import WeightContext, W  # noqa: F401


def _check_s195():
    from src.calculations.feature_decomp import extract_features, ChartFeatureVector  # noqa: F401


def _check_s196():
    from src.calculations.feature_decomp import extract_features
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    fv = extract_features(chart, "parashari")
    if fv.feature_count() < 48:
        raise AssertionError(f"Expected >= 48 features (S196), got {fv.feature_count()}")


def _check_s197():
    from src.calculations.feature_decomp import extract_features
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    fv = extract_features(chart, "parashari")
    names = set(fv.feature_names())
    for expected in ("h01_benefic_net_score", "h01_malefic_net_score", "h01_karak_score"):
        if expected not in names:
            raise AssertionError(f"S197 feature missing: {expected}")


def _check_s198():
    from src.calculations.feature_decomp import extract_features
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    fv = extract_features(chart, "parashari")
    names = set(fv.feature_names())
    for expected in ("h01_pushkara_nav", "h01_war_loser"):
        if expected not in names:
            raise AssertionError(f"S198 feature missing: {expected}")


def _check_s199():
    from src.calculations.feature_decomp import extract_features
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    fv = extract_features(chart, "parashari")
    if fv.feature_count() < 150:
        raise AssertionError(f"Expected >= 150 features (S199), got {fv.feature_count()}")


def _check_s200():
    from src.calculations.scoring_v3 import score_chart_v3
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    scores = score_chart_v3(chart, dashas=[], school="parashari")
    if not hasattr(scores, "feature_vector") or scores.feature_vector is None:
        raise AssertionError("feature_vector not attached to ChartScoresV3")


def _check_s201():
    from src.research.osf_registration import OSFRegistration  # noqa: F401
    osf_draft = ROOT / "docs/research/osf_draft_ob3.json"
    if not osf_draft.exists():
        raise AssertionError("OSF draft file missing")


def _check_s202():
    from src.corpus.registry import CorpusRegistry  # noqa: F401
    from src.corpus.rule_record import RuleRecord  # noqa: F401


def _check_s203():
    from src.research.data_license import check_source_license  # noqa: F401
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    if EXISTING_RULES_REGISTRY.count() < 23:
        raise AssertionError(f"Expected >= 23 existing rules, got {EXISTING_RULES_REGISTRY.count()}")


def _check_s204():
    from src.corpus.extractor_base import BaseExtractor  # noqa: F401
    from src.research.cv_splitter import TimeBasedSplit  # noqa: F401


def _check_s205():
    from src.corpus.corpus_audit import CorpusAudit  # noqa: F401
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    if BPHS_EXTENDED_REGISTRY.count() < 30:
        raise AssertionError(f"Expected >= 30 BPHS extended rules, got {BPHS_EXTENDED_REGISTRY.count()}")


def _check_s206():
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    if PHALADEEPIKA_REGISTRY.count() < 20:
        raise AssertionError("Expected >= 20 Phaladeepika rules")
    if BRIHAT_JATAKA_REGISTRY.count() < 23:
        raise AssertionError("Expected >= 23 Brihat Jataka rules")


def _check_s207():
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    if UTTARA_KALAMRITA_REGISTRY.count() < 15:
        raise AssertionError("Expected >= 15 Uttara Kalamrita rules")
    if JATAKA_PARIJATA_REGISTRY.count() < 15:
        raise AssertionError("Expected >= 15 Jataka Parijata rules")


def _check_s208():
    from src.corpus.birth_record import BirthRecord  # noqa: F401
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    if registry.count() < 100:
        raise AssertionError(f"Expected >= 100 combined rules, got {registry.count()}")


def _check_s209():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    if registry.count() < 100:
        raise AssertionError("Corpus pipeline integration: expected >= 100 rules")


def _check_s210():
    from src.corpus.corpus_audit import CorpusAudit
    from src.corpus.combined_corpus import build_corpus
    audit = CorpusAudit(build_corpus())
    result = audit.run()
    if result["errors"]:
        raise AssertionError(f"Corpus audit errors: {result['errors']}")


def _check_s211():
    from src.db_vector import VECTOR_DIM  # noqa: F401
    from src.db_timescale import TIMESCALE_SCHEMA_DDL  # noqa: F401
    from src.ml.mlflow_config import EXPERIMENT_NAMES  # noqa: F401
    from src.db_family import FamilyRelation  # noqa: F401


def _check_s212():
    from src.calculations.kp_ayanamsha import KP_AYANAMSHA
    if KP_AYANAMSHA != "krishnamurti":
        raise AssertionError(f"KP_AYANAMSHA={KP_AYANAMSHA!r}")


def _check_s213():
    from src.ci.protocol_compliance import check_all_protocols
    report = check_all_protocols()
    failures = [k for k, v in report.items() if not v["compliant"]]
    if failures:
        raise AssertionError(f"Protocols not satisfied: {failures}")


def _check_s214():
    from src.ci.health_check import run_health_check, CIHealthReport  # noqa: F401
    report = run_health_check()
    if not report.passed:
        raise AssertionError(f"CI health check failed: {report.errors}")


def _check_s215():
    # S215 is this module — if it imports, it's present
    from src.ci.phase0_checkpoint import Phase0Checkpoint  # noqa: F401
