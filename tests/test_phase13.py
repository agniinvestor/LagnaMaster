"""tests/test_phase13.py — Phase 13: Feedback Governance (S84–86)"""
from __future__ import annotations
import pytest

@pytest.fixture
def tmp_db(tmp_path):
    return str(tmp_path / "test.db")

class TestFeedbackLoop:
    def test_record_helpful(self, tmp_db):
        from src.feedback.feedback_loop import record_feedback
        r = record_feedback("u1","chart1","career","helpful","2026-03-20",db_path=tmp_db)
        assert r.rating == "helpful"
        assert not r.queued_for_review

    def test_record_concerning_queued(self, tmp_db):
        from src.feedback.feedback_loop import record_feedback
        r = record_feedback("u1","chart1","health","concerning","2026-03-20",db_path=tmp_db)
        assert r.queued_for_review

    def test_invalid_rating(self, tmp_db):
        from src.feedback.feedback_loop import record_feedback
        with pytest.raises(ValueError):
            record_feedback("u1","chart1","career","bad_rating","2026-03-20",db_path=tmp_db)

    def test_quality_metrics(self, tmp_db):
        from src.feedback.feedback_loop import record_feedback, get_quality_metrics
        record_feedback("u1","c1","career","helpful","2026-03-20",db_path=tmp_db)
        m = get_quality_metrics(db_path=tmp_db)
        assert "by_domain" in m
        assert "no automated" in m["note"].lower()

    def test_reproducibility_key(self, tmp_db):
        from src.feedback.feedback_loop import record_feedback
        r = record_feedback("u1","chart1","career","helpful","2026-03-20",
                            engine_version="3.0.0",db_path=tmp_db)
        assert "chart1" in r.reproducibility_key
        assert "3.0.0" in r.reproducibility_key

class TestHarmEscalation:
    def test_no_trigger_normal_usage(self):
        from src.feedback.harm_escalation import check_usage_pattern
        s = check_usage_pattern({"career":1}, 1, 5, ["helpful"])
        assert not s.triggered

    def test_trigger_repeated_neg_domain(self):
        from src.feedback.harm_escalation import check_usage_pattern
        s = check_usage_pattern({"health_longevity":3}, 3, 8, [])
        assert s.triggered
        assert "trusted" in s.prompt.lower()

    def test_trigger_concerning_ratings(self):
        from src.feedback.harm_escalation import check_usage_pattern
        s = check_usage_pattern({}, 2, 8, ["concerning","concerning"])
        assert s.triggered

    def test_prompt_no_crisis_resources(self):
        from src.feedback.harm_escalation import check_usage_pattern
        s = check_usage_pattern({"mind_psychology":4}, 5, 12, [])
        if s.triggered:
            assert "hotline" not in s.prompt.lower()
            assert "crisis line" not in s.prompt.lower()

class TestDependencyPrevention:
    def test_log_session(self, tmp_db):
        from src.feedback.dependency_prevention import log_session, check_dependency_status
        log_session("u1", "career", db_path=tmp_db)
        status = check_dependency_status("u1", db_path=tmp_db)
        assert status.sessions_today >= 1

    def test_nudge_after_3_sessions(self, tmp_db):
        from src.feedback.dependency_prevention import log_session, check_dependency_status
        for _ in range(3):
            log_session("u2", "career", db_path=tmp_db)
        status = check_dependency_status("u2", db_path=tmp_db)
        assert status.show_nudge
        assert not status.is_overuse

    def test_overuse_after_many(self, tmp_db):
        from src.feedback.dependency_prevention import log_session, check_dependency_status
        for _ in range(8):
            log_session("u3", "career", db_path=tmp_db)
        status = check_dependency_status("u3", db_path=tmp_db)
        assert status.is_overuse
