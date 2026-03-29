"""
tests/test_s214_ci_observability.py — S214: CI observability

Tests the CI health check module that provides structured observability
for the pre-push hook and CI pipeline. Verifies corpus counts, protocol
compliance, guardrail status, and module presence.
"""

from __future__ import annotations


# ── Module imports ─────────────────────────────────────────────────────────────

def test_health_check_module_importable():
    from src.ci.health_check import run_health_check  # noqa: F401


def test_health_report_dataclass_importable():
    from src.ci.health_check import CIHealthReport  # noqa: F401


# ── CIHealthReport structure ───────────────────────────────────────────────────

def test_health_report_has_required_fields():
    from src.ci.health_check import CIHealthReport
    import dataclasses
    fields = {f.name for f in dataclasses.fields(CIHealthReport)}
    required = {
        "corpus_rule_count",
        "protocols_compliant",
        "g06_enforced",
        "g17_enforced",
        "phase0_modules_present",
        "errors",
        "passed",
    }
    assert required.issubset(fields), f"Missing fields: {required - fields}"


def test_run_health_check_returns_report():
    from src.ci.health_check import run_health_check, CIHealthReport
    report = run_health_check()
    assert isinstance(report, CIHealthReport)


def test_run_health_check_passed_is_bool():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert isinstance(report.passed, bool)


def test_run_health_check_errors_is_list():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert isinstance(report.errors, list)


def test_run_health_check_corpus_count_positive():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.corpus_rule_count > 0


def test_run_health_check_corpus_count_at_least_100():
    """Combined corpus must have >= 100 rules after Phase 0."""
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.corpus_rule_count >= 100, (
        f"Expected >= 100 rules, got {report.corpus_rule_count}"
    )


def test_run_health_check_protocols_compliant():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.protocols_compliant is True, (
        f"Protocol compliance failed. Errors: {report.errors}"
    )


def test_run_health_check_g06_enforced():
    """G06: KP ayanamsha enforcement must be in place."""
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.g06_enforced is True


def test_run_health_check_g17_enforced():
    """G17: No PyJHora imports in src/ must be enforced."""
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.g17_enforced is True


def test_run_health_check_phase0_modules_present():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.phase0_modules_present is True


def test_run_health_check_overall_passes():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert report.passed is True, (
        f"Health check failed. Errors: {report.errors}"
    )


# ── Text report ────────────────────────────────────────────────────────────────

def test_health_report_to_text_returns_string():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    assert hasattr(report, "to_text")
    text = report.to_text()
    assert isinstance(text, str)
    assert len(text) > 0


def test_health_report_to_text_contains_key_info():
    from src.ci.health_check import run_health_check
    report = run_health_check()
    text = report.to_text()
    assert "corpus" in text.lower() or "rule" in text.lower()
    assert "protocol" in text.lower()


# ── G17 check standalone ───────────────────────────────────────────────────────

def test_check_g17_no_jhora_imports_in_src():
    """G17: src/ must contain no jhora imports."""
    from src.ci.health_check import check_g17_compliance
    result = check_g17_compliance()
    assert result["compliant"] is True, (
        f"G17 violation: jhora import found in {result.get('violations', [])}"
    )


# ── G06 check standalone ───────────────────────────────────────────────────────

def test_check_g06_kp_ayanamsha_module_present():
    """G06: kp_ayanamsha.py must exist and export KP_AYANAMSHA='krishnamurti'."""
    from src.ci.health_check import check_g06_compliance
    result = check_g06_compliance()
    assert result["compliant"] is True, (
        f"G06 check failed: {result.get('error', '')}"
    )
