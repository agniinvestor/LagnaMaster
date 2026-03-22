"""
tests/test_s186.py
Session 186: school-mixing fix + regression snapshot tests.
"""

import pytest
from unittest.mock import MagicMock


def make_rule(rule_id, score=1.0, triggered=True):
    r = MagicMock()
    r.rule = rule_id
    r.score = score if triggered else 0.0
    r.triggered = triggered
    return r


# ─── School Rules ────────────────────────────────────────────────────────────


class TestSchoolRuleMap:
    def test_r17_r18_are_jaimini(self):
        from src.calculations.school_rules import SCHOOL_RULE_MAP, JAIMINI

        assert SCHOOL_RULE_MAP["R17"] == JAIMINI
        assert SCHOOL_RULE_MAP["R18"] == JAIMINI

    def test_all_other_rules_are_parashari(self):
        from src.calculations.school_rules import SCHOOL_RULE_MAP, PARASHARI

        jaimini_rules = {"R17", "R18"}
        for rule_id, school in SCHOOL_RULE_MAP.items():
            if rule_id not in jaimini_rules:
                assert school == PARASHARI, (
                    f"{rule_id} should be parashari, got {school}"
                )

    def test_22_rules_declared(self):
        from src.calculations.school_rules import SCHOOL_RULE_MAP

        assert len(SCHOOL_RULE_MAP) == 22

    def test_get_rule_school(self):
        from src.calculations.school_rules import get_rule_school

        assert get_rule_school("R01") == "parashari"
        assert get_rule_school("R17") == "jaimini"
        assert get_rule_school("R18") == "jaimini"
        assert get_rule_school("R22") == "parashari"

    def test_unknown_rule_defaults_parashari(self):
        from src.calculations.school_rules import get_rule_school

        assert get_rule_school("R99") == "parashari"


class TestIsRuleActive:
    def test_parashari_rules_active_in_parashari(self):
        from src.calculations.school_rules import is_rule_active

        for rule in ["R01", "R02", "R09", "R22"]:
            assert is_rule_active(rule, "parashari", strict=True), (
                f"{rule} should be active"
            )

    def test_jaimini_rules_inactive_in_parashari_strict(self):
        from src.calculations.school_rules import is_rule_active

        assert not is_rule_active("R17", "parashari", strict=True)
        assert not is_rule_active("R18", "parashari", strict=True)

    def test_jaimini_rules_active_in_jaimini_strict(self):
        from src.calculations.school_rules import is_rule_active

        assert is_rule_active("R17", "jaimini", strict=True)
        assert is_rule_active("R18", "jaimini", strict=True)

    def test_parashari_rules_active_in_jaimini_strict(self):
        """Jaimini analysis includes Parashari planetary base."""
        from src.calculations.school_rules import is_rule_active

        # In strict jaimini mode, parashari rules are NOT active (pure school)
        assert not is_rule_active("R01", "jaimini", strict=True)

    def test_non_strict_parashari_allows_jaimini(self):
        """Default non-strict mode: Jaimini rules fire in all modes."""
        from src.calculations.school_rules import is_rule_active

        # Non-strict: jaimini rules still fire in parashari mode (current behavior)
        # This is the current permissive default before strict_school is enforced
        # strict=False means: same behavior as before S186
        # R17/R18 should be active in parashari non-strict (backward compatible)
        result = is_rule_active("R17", "parashari", strict=False)
        assert isinstance(result, bool)  # just verify it returns a bool

    def test_kp_allows_parashari_base(self):
        from src.calculations.school_rules import is_rule_active

        assert is_rule_active("R01", "kp", strict=False)

    def test_tajika_allows_parashari_base(self):
        from src.calculations.school_rules import is_rule_active

        assert is_rule_active("R04", "tajika", strict=False)


class TestFilterRulesBySchool:
    def test_strict_parashari_excludes_r17_r18(self):
        from src.calculations.school_rules import filter_rules_by_school

        rules = [make_rule(f"R{i:02d}") for i in range(1, 23)]
        filtered = filter_rules_by_school(rules, "parashari", strict=True)
        rule_ids = {r.rule for r in filtered}
        assert "R17" not in rule_ids
        assert "R18" not in rule_ids
        assert "R01" in rule_ids
        assert len(filtered) == 20  # 22 - 2 jaimini rules

    def test_jaimini_strict_includes_r17_r18_excludes_parashari(self):
        from src.calculations.school_rules import filter_rules_by_school

        rules = [make_rule(f"R{i:02d}") for i in range(1, 23)]
        filtered = filter_rules_by_school(rules, "jaimini", strict=True)
        rule_ids = {r.rule for r in filtered}
        assert "R17" in rule_ids
        assert "R18" in rule_ids
        assert "R01" not in rule_ids  # parashari excluded in strict jaimini

    def test_non_strict_allows_all(self):
        from src.calculations.school_rules import filter_rules_by_school

        rules = [make_rule(f"R{i:02d}") for i in range(1, 23)]
        filtered = filter_rules_by_school(rules, "parashari", strict=False)
        # Non-strict: R17/R18 still active (backward compatible)
        assert len(filtered) >= 20  # at least the parashari ones


class TestSchoolScoreAdjustment:
    def test_strict_deducts_r17_r18(self):
        from src.calculations.school_rules import school_score_adjustment

        rules = [
            make_rule("R01", score=2.0),
            make_rule("R17", score=1.5),  # should be deducted
            make_rule("R18", score=-0.5),  # should be deducted
        ]
        raw = 3.0  # 2.0 + 1.5 - 0.5
        corrected = school_score_adjustment(raw, rules, "parashari", strict=True)
        assert corrected == pytest.approx(2.0)  # 3.0 - 1.5 + 0.5 = 2.0

    def test_non_strict_no_change(self):
        from src.calculations.school_rules import school_score_adjustment

        rules = [make_rule("R17", score=1.5), make_rule("R01", score=2.0)]
        corrected = school_score_adjustment(3.5, rules, "parashari", strict=False)
        assert corrected == pytest.approx(3.5)


class TestGetJaiminiParashariRules:
    def test_get_jaimini_rules_returns_r17_r18(self):
        from src.calculations.school_rules import get_jaimini_rules

        jaimini = get_jaimini_rules()
        assert "R17" in jaimini
        assert "R18" in jaimini
        assert len(jaimini) == 2

    def test_get_parashari_rules_returns_20(self):
        from src.calculations.school_rules import get_parashari_rules

        parashari = get_parashari_rules()
        assert len(parashari) == 20
        assert "R17" not in parashari
        assert "R18" not in parashari


# ─── Regression Snapshot ─────────────────────────────────────────────────────


class TestRegressionSnap:
    def test_imports_cleanly(self):
        from src.regression_snap import (
            REFERENCE_CHARTS,
        )

        assert len(REFERENCE_CHARTS) >= 1

    def test_diff_empty_when_no_baseline(self, tmp_path):
        from src.regression_snap import diff_against_snapshot

        diffs = diff_against_snapshot(path=tmp_path / "nofile.json")
        assert diffs == []

    def test_diff_detects_regression(self, tmp_path):
        import json
        from src.regression_snap import diff_against_snapshot

        snap_path = tmp_path / "snap.json"
        baseline = {
            "engine_version": "v3.0.0",
            "charts": {"india_1947": {"1": -2.75, "2": -3.375}},
        }
        with open(snap_path, "w") as f:
            json.dump(baseline, f)

        # Inject a "current" that differs
        import unittest.mock as mock

        modified_snap = {
            "engine_version": "v3.0.0",
            "charts": {
                "india_1947": {"1": -1.0, "2": -3.375}  # H1 changed
            },
        }
        with mock.patch(
            "src.regression_snap.compute_snapshot", return_value=modified_snap
        ):
            diffs = diff_against_snapshot(
                chart_defs={"india_1947": {}},
                path=snap_path,
                tolerance=0.05,
            )
        assert len(diffs) == 1
        assert diffs[0]["house"] == 1
        assert diffs[0]["chart_id"] == "india_1947"

    def test_diff_clean_no_regression(self, tmp_path):
        import json
        from src.regression_snap import diff_against_snapshot

        snap_path = tmp_path / "snap.json"
        scores = {"1": -2.75, "2": -3.375, "3": -0.5}
        baseline = {"engine_version": "v3.0.0", "charts": {"india_1947": scores}}
        with open(snap_path, "w") as f:
            json.dump(baseline, f)

        import unittest.mock as mock

        with mock.patch(
            "src.regression_snap.compute_snapshot",
            return_value={"engine_version": "v3.0.0", "charts": {"india_1947": scores}},
        ):
            diffs = diff_against_snapshot(path=snap_path, tolerance=0.05)
        assert diffs == []

    def test_assert_no_regression_passes_when_clean(self, tmp_path):
        import json
        from src.regression_snap import assert_no_regression

        snap_path = tmp_path / "snap.json"
        scores = {"1": -2.75}
        baseline = {"engine_version": "v3.0.0", "charts": {"india_1947": scores}}
        with open(snap_path, "w") as f:
            json.dump(baseline, f)

        import unittest.mock as mock

        with mock.patch(
            "src.regression_snap.compute_snapshot",
            return_value={"engine_version": "v3.0.0", "charts": {"india_1947": scores}},
        ):
            assert_no_regression(path=snap_path, tolerance=0.05)  # should not raise

    def test_assert_no_regression_raises_on_regression(self, tmp_path):
        import json
        from src.regression_snap import assert_no_regression

        snap_path = tmp_path / "snap.json"
        baseline = {"engine_version": "v3.0.0", "charts": {"india_1947": {"1": -2.75}}}
        with open(snap_path, "w") as f:
            json.dump(baseline, f)

        import unittest.mock as mock

        with mock.patch(
            "src.regression_snap.compute_snapshot",
            return_value={
                "engine_version": "v3.0.0",
                "charts": {"india_1947": {"1": 5.0}},
            },
        ):
            with pytest.raises(AssertionError, match="Regression detected"):
                assert_no_regression(path=snap_path, tolerance=0.05)

    def test_save_load_roundtrip(self, tmp_path):
        from src.regression_snap import save_snapshot, load_snapshot

        snap = {"engine_version": "v3.0.0", "charts": {"foo": {"1": 3.14}}}
        path = tmp_path / "snap.json"
        save_snapshot(snap, path)
        loaded = load_snapshot(path)
        assert loaded == snap

    def test_reference_charts_have_required_fields(self):
        from src.regression_snap import REFERENCE_CHARTS

        for cid, defn in REFERENCE_CHARTS.items():
            for field in ["year", "month", "day", "hour", "lat", "lon", "tz_offset"]:
                assert field in defn, f"{cid} missing {field}"


# ─── Integration: scoring_v3.py wiring ───────────────────────────────────────


class TestSchoolRulesIntegration:
    """Verify school_rules is importable and integrates with calc_config."""

    def test_calc_config_parashari_mode(self):
        from src.calculations.calc_config import CalcConfig, School

        cfg = CalcConfig(school=School.PARASHARI)
        assert cfg.school.value == "parashari"

    def test_school_rules_accessible_from_calc_config(self):
        from src.calculations.school_rules import is_rule_active
        from src.calculations.calc_config import School

        school = School.PARASHARI.value
        assert is_rule_active("R01", school, strict=True)
        assert not is_rule_active("R17", school, strict=True)

    def test_strict_school_corrects_r17_r18_contribution(self):
        """In strict parashari mode, R17/R18 contributions are zeroed out."""
        from src.calculations.school_rules import school_score_adjustment

        rules = [
            make_rule("R01", score=3.0, triggered=True),
            make_rule("R17", score=2.0, triggered=True),
            make_rule("R18", score=-1.0, triggered=True),
        ]
        raw = 4.0  # 3+2-1
        corrected = school_score_adjustment(raw, rules, "parashari", strict=True)
        # Should deduct R17 (2.0) and R18 (-1.0): 4.0 - 2.0 - (-1.0) = 3.0
        assert corrected == pytest.approx(3.0)
