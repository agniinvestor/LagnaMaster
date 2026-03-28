"""
tests/test_s203_adb_license.py — S203: ADB license compliance + R01-R23 corpus encoding

Validates data source license tracking and that all 23 existing engine rules
are encoded as RuleRecords in the corpus.
"""

from __future__ import annotations


# ── DataSourceLicense ─────────────────────────────────────────────────────────

def test_data_source_license_import():
    from src.research.data_license import DataSourceLicense
    assert DataSourceLicense is not None


def test_data_source_license_fields():
    import dataclasses
    from src.research.data_license import DataSourceLicense
    field_names = {f.name for f in dataclasses.fields(DataSourceLicense)}
    required = {"source_id", "name", "license_type", "commercial_use_allowed",
                "attribution_required", "url"}
    assert required.issubset(field_names), f"Missing: {required - field_names}"


def test_data_source_license_adb():
    from src.research.data_license import KNOWN_SOURCES
    adb = KNOWN_SOURCES.get("ADB")
    assert adb is not None, "ADB must be in KNOWN_SOURCES"
    assert not adb.commercial_use_allowed, "ADB is non-commercial research license"
    assert adb.attribution_required


def test_data_source_license_public_domain():
    from src.research.data_license import KNOWN_SOURCES
    pd = KNOWN_SOURCES.get("PUBLIC_DOMAIN")
    assert pd is not None
    assert pd.commercial_use_allowed


def test_check_source_raises_for_unknown():
    from src.research.data_license import check_source_license
    try:
        check_source_license("UNKNOWN_DB", commercial=True)
        assert False, "Should raise"
    except (ValueError, KeyError):
        pass


def test_check_source_raises_commercial_for_adb():
    from src.research.data_license import check_source_license
    try:
        check_source_license("ADB", commercial=True)
        assert False, "Should raise — ADB is non-commercial"
    except PermissionError:
        pass


def test_check_source_ok_for_adb_research():
    from src.research.data_license import check_source_license
    # Should not raise for non-commercial research use
    check_source_license("ADB", commercial=False)


# ── R01-R23 corpus encoding ───────────────────────────────────────────────────

def test_existing_rules_corpus_import():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    assert EXISTING_RULES_REGISTRY is not None


def test_existing_rules_all_r01_to_r23_present():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    for i in range(1, 24):
        rule_id = f"R{i:02d}"
        r = EXISTING_RULES_REGISTRY.get(rule_id)
        assert r is not None, f"{rule_id} not found in EXISTING_RULES_REGISTRY"


def test_existing_rules_count():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    assert EXISTING_RULES_REGISTRY.count() >= 23, (
        f"Expected ≥23 rules, got {EXISTING_RULES_REGISTRY.count()}"
    )


def test_existing_rules_are_implemented():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    for r in EXISTING_RULES_REGISTRY.all():
        assert r.implemented, f"{r.rule_id} should be marked implemented=True"


def test_existing_rules_confidence_reasonable():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    for r in EXISTING_RULES_REGISTRY.all():
        assert r.confidence >= 0.7, (
            f"{r.rule_id} confidence={r.confidence} too low for implemented rules"
        )
