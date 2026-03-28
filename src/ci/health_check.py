"""
src/ci/health_check.py — S214: CI observability health check

Provides structured observability for the pre-push hook and CI pipeline.
Checks corpus counts, protocol compliance, and critical guardrail status.

Public API
----------
  CIHealthReport   — dataclass with all check results
  run_health_check() -> CIHealthReport
  check_g17_compliance() -> dict
  check_g06_compliance() -> dict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

# Phase 0 required modules: (import_path, symbol) pairs
_PHASE0_MODULES = [
    ("src.interfaces.classical_engine", "ClassicalEngine"),
    ("src.interfaces.dasha_engine", "DashaEngine"),
    ("src.interfaces.feedback_service", "FeedbackService"),
    ("src.interfaces.ml_service", "MLService"),
    ("src.interfaces.adapters.scoring_engine", "ScoringEngineAdapter"),
    ("src.interfaces.adapters.dasha_engine", "VimshottariDasaAdapter"),
    ("src.interfaces.adapters.null_feedback", "NullFeedbackService"),
    ("src.interfaces.adapters.null_ml", "NullMLService"),
    ("src.calculations.conditional_weights", "WeightContext"),
    ("src.calculations.feature_decomp", "extract_features"),
    ("src.calculations.kp_ayanamsha", "KP_AYANAMSHA"),
    ("src.corpus.combined_corpus", "build_corpus"),
    ("src.corpus.corpus_audit", "CorpusAudit"),
    ("src.research.osf_registration", "OSFRegistration"),
    ("src.research.data_license", "check_source_license"),
    ("src.research.cv_splitter", "TimeBasedSplit"),
    ("src.db_vector", "VECTOR_DIM"),
    ("src.db_timescale", "TIMESCALE_SCHEMA_DDL"),
    ("src.ml.mlflow_config", "EXPERIMENT_NAMES"),
    ("src.db_family", "FamilyRelation"),
]


@dataclass
class CIHealthReport:
    """Structured health report for CI pipeline observability."""

    corpus_rule_count: int = 0
    protocols_compliant: bool = False
    g06_enforced: bool = False
    g17_enforced: bool = False
    phase0_modules_present: bool = False
    errors: list[str] = field(default_factory=list)
    passed: bool = False

    def to_text(self) -> str:
        lines = [
            "=== CI Health Report ===",
            f"Corpus rules:          {self.corpus_rule_count}",
            f"Protocols compliant:   {self.protocols_compliant}",
            f"G06 enforced:          {self.g06_enforced}",
            f"G17 enforced:          {self.g17_enforced}",
            f"Phase 0 modules:       {self.phase0_modules_present}",
        ]
        if self.errors:
            lines.append("Errors:")
            for err in self.errors:
                lines.append(f"  - {err}")
        lines.append(f"Overall: {'PASS' if self.passed else 'FAIL'}")
        return "\n".join(lines)


def run_health_check() -> CIHealthReport:
    """Run all CI health checks and return a structured report."""
    report = CIHealthReport()
    errors: list[str] = []

    # 1. Corpus rule count
    try:
        from src.corpus.combined_corpus import build_corpus
        registry = build_corpus()
        report.corpus_rule_count = registry.count()
    except Exception as exc:
        errors.append(f"corpus count failed: {exc}")

    # 2. Protocol compliance
    try:
        from src.ci.protocol_compliance import check_all_protocols
        proto_report = check_all_protocols()
        report.protocols_compliant = all(
            v["compliant"] for v in proto_report.values()
        )
        for name, result in proto_report.items():
            if not result["compliant"]:
                errors.append(f"Protocol {name} not satisfied by {result['adapter']}")
    except Exception as exc:
        errors.append(f"protocol check failed: {exc}")

    # 3. G06 compliance
    g06_result = check_g06_compliance()
    report.g06_enforced = g06_result["compliant"]
    if not g06_result["compliant"]:
        errors.append(f"G06: {g06_result.get('error', 'kp_ayanamsha check failed')}")

    # 4. G17 compliance
    g17_result = check_g17_compliance()
    report.g17_enforced = g17_result["compliant"]
    if not g17_result["compliant"]:
        errors.append(
            f"G17 violation: jhora found in {g17_result.get('violations', [])}"
        )

    # 5. Phase 0 modules present
    module_errors = _check_phase0_modules()
    report.phase0_modules_present = len(module_errors) == 0
    errors.extend(module_errors)

    report.errors = errors
    report.passed = (
        report.corpus_rule_count >= 100
        and report.protocols_compliant
        and report.g06_enforced
        and report.g17_enforced
        and report.phase0_modules_present
        and len(errors) == 0
    )
    return report


def check_g17_compliance() -> dict:
    """
    G17: Verify no PyJHora import statements exist in src/.

    Only flags actual import/from-import lines, not comments or string literals.
    Returns dict with 'compliant' bool and 'violations' list.
    """
    import re
    src_dir = ROOT / "src"
    violations: list[str] = []
    # Match lines like: import jhora, from jhora import ..., import pyJHora
    _import_re = re.compile(
        r"^\s*(?:import|from)\s+[a-zA-Z0-9_.]*[Jj][Hh][Oo][Rr][Aa]",
        re.MULTILINE,
    )
    for py_file in src_dir.rglob("*.py"):
        try:
            text = py_file.read_text(encoding="utf-8")
        except OSError:
            continue
        matches = []
        for i, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            # Skip comment lines
            if stripped.startswith("#"):
                continue
            if _import_re.match(line):
                matches.append(i)
        if matches:
            violations.append(f"{py_file.relative_to(ROOT)}:{matches}")
    return {"compliant": len(violations) == 0, "violations": violations}


def check_g06_compliance() -> dict:
    """
    G06: Verify kp_ayanamsha module exists and KP_AYANAMSHA = 'krishnamurti'.

    Returns dict with 'compliant' bool and 'error' string.
    """
    try:
        from src.calculations.kp_ayanamsha import KP_AYANAMSHA, get_kp_ayanamsha
        if KP_AYANAMSHA != "krishnamurti":
            return {
                "compliant": False,
                "error": f"KP_AYANAMSHA={KP_AYANAMSHA!r}, expected 'krishnamurti'",
            }
        if get_kp_ayanamsha() != "krishnamurti":
            return {"compliant": False, "error": "get_kp_ayanamsha() != 'krishnamurti'"}
        return {"compliant": True, "error": ""}
    except ImportError as exc:
        return {"compliant": False, "error": f"ImportError: {exc}"}


def _check_phase0_modules() -> list[str]:
    """Attempt to import all Phase 0 modules. Return list of errors."""
    import importlib
    errors: list[str] = []
    for module_path, symbol in _PHASE0_MODULES:
        try:
            mod = importlib.import_module(module_path)
            if not hasattr(mod, symbol):
                errors.append(f"{module_path}.{symbol} not found")
        except ImportError as exc:
            errors.append(f"{module_path}: ImportError: {exc}")
    return errors
