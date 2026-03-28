"""
tests/test_s215_phase0_checkpoint.py — S215: Phase 0 checkpoint

Comprehensive audit verifying all Phase 0 (S191–S215) deliverables are
in place. This test suite is the Phase 0 gate — if it passes, Phase 1
(S216 Classical Knowledge Foundation) can begin.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent.parent


# ── Module presence: S191 (VedAstro + G17) ────────────────────────────────────

def test_s191_ruff_g17_config_present():
    """G17: ruff must have noqa-jhora rule configured."""
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        # check ruff.toml or setup.cfg
        assert (ROOT / "ruff.toml").exists() or (ROOT / ".ruff.toml").exists(), \
            "No ruff config found"
    else:
        text = pyproject.read_text()
        # G17 rule must be enforced — presence of jhora pattern or TID rule
        assert "jhora" in text.lower() or "TID" in text, \
            "G17 jhora rule not found in pyproject.toml ruff config"


# ── Module presence: S192 (Protocol interfaces) ───────────────────────────────

def test_s192_all_protocol_modules_exist():
    protocols = [
        "src/interfaces/classical_engine.py",
        "src/interfaces/dasha_engine.py",
        "src/interfaces/feedback_service.py",
        "src/interfaces/ml_service.py",
        "src/interfaces/adapters/scoring_engine.py",
        "src/interfaces/adapters/dasha_engine.py",
        "src/interfaces/adapters/null_feedback.py",
        "src/interfaces/adapters/null_ml.py",
    ]
    for path in protocols:
        assert (ROOT / path).exists(), f"Missing Protocol module: {path}"


# ── Module presence: S193 (HouseScore distribution) ──────────────────────────

def test_s193_housescore_distribution_importable():
    from src.calculations.house_score import HouseScore  # noqa: F401


# ── Module presence: S194 (Conditional weights) ───────────────────────────────

def test_s194_conditional_weights_importable():
    from src.calculations.conditional_weights import WeightContext, W  # noqa: F401


# ── Module presence: S195-S200 (Feature decomposition) ───────────────────────

def test_s195_feature_decomp_importable():
    from src.calculations.feature_decomp import extract_features, ChartFeatureVector  # noqa: F401


def test_s195_feature_count_at_least_150():
    """Phase 0 target: 150+ continuous features (13 extractors × 12 houses)."""
    from src.calculations.feature_decomp import extract_features
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    fv = extract_features(chart, school="parashari")
    count = fv.feature_count()
    assert count >= 150, (
        f"Expected >= 150 features, got {count}"
    )


def test_s200_score_chart_v3_attaches_feature_vector():
    from src.calculations.scoring_v3 import score_chart_v3
    from src.ephemeris import compute_chart
    chart = compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    scores = score_chart_v3(chart, dashas=[], school="parashari")
    assert hasattr(scores, "feature_vector")
    assert scores.feature_vector is not None


# ── Module presence: S201-S210 (Corpus infrastructure) ───────────────────────

def test_s201_osf_registration_importable():
    from src.research.osf_registration import OSFRegistration, HypothesisSpec, CVStrategy  # noqa: F401


def test_s201_osf_draft_exists():
    assert (ROOT / "docs/research/osf_draft_ob3.json").exists(), \
        "OSF draft pre-registration file missing"


def test_s202_corpus_infrastructure_importable():
    from src.corpus.registry import CorpusRegistry  # noqa: F401
    from src.corpus.rule_record import RuleRecord  # noqa: F401


def test_s203_data_license_importable():
    from src.research.data_license import check_source_license, KNOWN_SOURCES  # noqa: F401


def test_s204_extractor_cv_importable():
    from src.corpus.extractor_base import BaseExtractor  # noqa: F401
    from src.research.cv_splitter import TimeBasedSplit  # noqa: F401


def test_s205_corpus_audit_importable():
    from src.corpus.corpus_audit import CorpusAudit  # noqa: F401


def test_s205_corpus_audit_runs_clean():
    from src.corpus.corpus_audit import CorpusAudit
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    audit = CorpusAudit(registry)
    result = audit.run()
    assert result["errors"] == [], f"Corpus audit errors: {result['errors']}"


def test_s208_combined_corpus_has_rules():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 100, \
        f"Expected >= 100 rules in combined corpus, got {registry.count()}"


# ── Module presence: S211 (ML infra + family schema) ─────────────────────────

def test_s211_db_vector_importable():
    from src.db_vector import VECTOR_DIM, VECTOR_SCHEMA_DDL  # noqa: F401
    assert VECTOR_DIM == 156


def test_s211_db_timescale_importable():
    from src.db_timescale import TIMESCALE_SCHEMA_DDL  # noqa: F401


def test_s211_mlflow_config_importable():
    from src.ml.mlflow_config import EXPERIMENT_NAMES, get_experiment_config  # noqa: F401


def test_s211_db_family_importable():
    from src.db_family import FamilyRelation, FAMILY_SCHEMA_DDL  # noqa: F401


# ── Module presence: S212 (KP ayanamsha G06) ─────────────────────────────────

def test_s212_kp_ayanamsha_importable():
    from src.calculations.kp_ayanamsha import (
        KP_AYANAMSHA, get_kp_ayanamsha, validate_kp_chart, compute_kp_chart,  # noqa: F401
    )
    assert KP_AYANAMSHA == "krishnamurti"


# ── Module presence: S213 (Protocol compliance) ───────────────────────────────

def test_s213_protocol_compliance_importable():
    from src.ci.protocol_compliance import check_all_protocols  # noqa: F401


# ── Module presence: S214 (CI observability) ──────────────────────────────────

def test_s214_health_check_importable():
    from src.ci.health_check import run_health_check, CIHealthReport  # noqa: F401


# ── GUARDRAILS.md completeness ────────────────────────────────────────────────

def test_guardrails_md_exists_and_has_all_ids():
    text = (ROOT / "docs/GUARDRAILS.md").read_text()
    for i in range(1, 26):
        assert f"G{i:02d}" in text or f"G{i}" in text, \
            f"G{i:02d} missing from GUARDRAILS.md"


def test_guardrails_g06_marked_partial():
    text = (ROOT / "docs/GUARDRAILS.md").read_text()
    # G06 must show 🟡 (partial fix) not 🔴 CURRENTLY VIOLATING
    assert "CURRENTLY VIOLATING" not in text, \
        "G06 still shows CURRENTLY VIOLATING — S212 fix not reflected"


def test_guardrails_g17_annotated():
    text = (ROOT / "docs/GUARDRAILS.md").read_text()
    assert "G17" in text


# ── Phase 0 gate: overall ─────────────────────────────────────────────────────

def test_phase0_checkpoint_module_importable():
    from src.ci.phase0_checkpoint import Phase0Checkpoint, run_phase0_audit  # noqa: F401


def test_phase0_audit_returns_dict():
    from src.ci.phase0_checkpoint import run_phase0_audit
    result = run_phase0_audit()
    assert isinstance(result, dict)


def test_phase0_audit_all_sessions_present():
    from src.ci.phase0_checkpoint import run_phase0_audit
    result = run_phase0_audit()
    assert "sessions" in result
    for session in range(191, 216):
        sid = f"S{session}"
        assert sid in result["sessions"], f"{sid} missing from Phase 0 audit"


def test_phase0_all_sessions_complete():
    from src.ci.phase0_checkpoint import run_phase0_audit
    result = run_phase0_audit()
    for sid, status in result["sessions"].items():
        assert status["complete"] is True, \
            f"{sid} not marked complete: {status.get('reason', '')}"


def test_phase0_audit_summary_present():
    from src.ci.phase0_checkpoint import run_phase0_audit
    result = run_phase0_audit()
    assert "summary" in result
    assert result["summary"]["total_sessions"] == 25  # S191-S215
    assert result["summary"]["complete_sessions"] == 25
