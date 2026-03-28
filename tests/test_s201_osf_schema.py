"""
tests/test_s201_osf_schema.py — S201: OSF pre-registration schema

Validates the OSFRegistration dataclass and JSON serialization used to
generate machine-readable pre-registration filings (G22 compliance).
"""

from __future__ import annotations


# ── Schema structure ──────────────────────────────────────────────────────────

def test_osf_registration_import():
    from src.research.osf_registration import OSFRegistration
    assert OSFRegistration is not None


def test_osf_registration_required_fields():
    from src.research.osf_registration import OSFRegistration
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(OSFRegistration)}
    required = {
        "study_id", "title", "hypotheses", "cv_strategy",
        "significance_threshold", "correction_method", "minimum_sample",
    }
    assert required.issubset(field_names), f"Missing fields: {required - field_names}"


def test_hypothesis_spec_fields():
    from src.research.osf_registration import HypothesisSpec
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(HypothesisSpec)}
    assert {"hypothesis_id", "description", "type", "feature_set"}.issubset(field_names)


def test_cv_strategy_fields():
    from src.research.osf_registration import CVStrategy
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(CVStrategy)}
    assert {"train_cutoff_year", "test_from_year", "description"}.issubset(field_names)


def test_osf_registration_to_dict():
    from src.research.osf_registration import OSFRegistration, HypothesisSpec, CVStrategy
    reg = OSFRegistration(
        study_id="OB-3",
        title="Multi-factor classical convergence as a predictive signal",
        hypotheses=[HypothesisSpec(
            hypothesis_id="H1",
            description="Cross-school concordance predicts above single-school baseline",
            type="primary",
            feature_set=["convergence_score"],
        )],
        cv_strategy=CVStrategy(
            train_cutoff_year=2009,
            test_from_year=2010,
            description="Pre-2010 train, 2010+ test — no look-ahead leakage",
        ),
        significance_threshold=0.05,
        correction_method="BH-FDR",
        minimum_sample=1000,
    )
    d = reg.to_dict()
    assert d["study_id"] == "OB-3"
    assert d["correction_method"] == "BH-FDR"
    assert len(d["hypotheses"]) == 1


def test_osf_registration_to_json_roundtrip():
    import json
    from src.research.osf_registration import OSFRegistration, HypothesisSpec, CVStrategy
    reg = OSFRegistration(
        study_id="OB-3-TEST",
        title="Test",
        hypotheses=[HypothesisSpec("H1", "test", "primary", [])],
        cv_strategy=CVStrategy(2009, 2010, "time-split"),
        significance_threshold=0.05,
        correction_method="BH-FDR",
        minimum_sample=500,
    )
    json_str = reg.to_json()
    parsed = json.loads(json_str)
    assert parsed["study_id"] == "OB-3-TEST"


def test_g22_stopping_rule_field():
    """G22 requires a stopping rule — minimum sample before any analysis."""
    from src.research.osf_registration import OSFRegistration
    import dataclasses
    fields = {f.name for f in dataclasses.fields(OSFRegistration)}
    assert "minimum_sample" in fields, "OSFRegistration must have minimum_sample (G22 stopping rule)"


def test_draft_ob3_filing_exists_and_valid():
    """docs/research/osf_draft_ob3.json must exist and be valid JSON."""
    import json
    from pathlib import Path
    path = Path("docs/research/osf_draft_ob3.json")
    assert path.exists(), f"Draft filing not found: {path}"
    data = json.loads(path.read_text())
    assert data.get("study_id") == "OB-3"
    assert data.get("minimum_sample", 0) >= 1000
