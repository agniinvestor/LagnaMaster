"""tests/test_phase10.py — Phase 10: Language & Safety Layer (S71–75)"""

from __future__ import annotations


class TestScoreToLanguage:
    def test_five_bars_high_score(self):
        from src.guidance.score_to_language import score_to_signal

        s = score_to_signal(3.5)
        assert s.bars == 5
        assert s.timing_label == "Clear passage"

    def test_zero_bars_low_score(self):
        from src.guidance.score_to_language import score_to_signal

        s = score_to_signal(-2.0)
        assert s.bars == 0
        assert s.timing_label == "Significant resistance"

    def test_all_tiers_covered(self):
        from src.guidance.score_to_language import score_to_signal

        scores = [4.0, 2.0, 1.0, 0.0, -1.0, -2.0]
        bars = [score_to_signal(s).bars for s in scores]
        assert bars == [5, 4, 3, 2, 1, 0]

    def test_signal_display(self):
        from src.guidance.score_to_language import signal_bars_display

        assert signal_bars_display(3) == "●●●○○"
        assert signal_bars_display(0) == "○○○○○"
        assert signal_bars_display(5) == "●●●●●"

    def test_no_raw_score_in_template(self):
        from src.guidance.score_to_language import score_to_signal

        for score in [-3.0, -1.0, 0.0, 1.0, 3.0]:
            s = score_to_signal(score)
            assert str(score) not in s.l1_template

    def test_domain_l1_sentence(self):
        from src.guidance.score_to_language import domain_l1_sentence

        s = domain_l1_sentence(2.0, "career", "Strong", "Now")
        assert isinstance(s, str) and len(s) > 10


class TestFatalismFilter:
    def test_rewrites_financial_ruin(self):
        from src.guidance.fatalism_filter import filter_output

        r = filter_output("financial ruin is possible")
        assert "financial ruin" not in r.lower()

    def test_rewrites_health_crisis(self):
        from src.guidance.fatalism_filter import filter_output

        r = filter_output("Health crisis indicated by 8th house")
        assert "health crisis" not in r.lower()

    def test_preserves_signal_direction(self):
        from src.guidance.fatalism_filter import filter_output

        r = filter_output("career will fail due to afflictions")
        assert "will fail" not in r
        # Signal preserved — some challenge language remains
        assert len(r) > 10

    def test_is_safe_clean_text(self):
        from src.guidance.fatalism_filter import is_safe

        assert is_safe("Conditions are supportive for career decisions.")

    def test_is_safe_flags_bad_text(self):
        from src.guidance.fatalism_filter import is_safe

        assert not is_safe("This period is doomed to failure.")

    def test_flag_patterns(self):
        from src.guidance.fatalism_filter import flag_patterns

        p = flag_patterns("career will be destroyed and financial ruin follows")
        assert len(p) >= 2


class TestExplainabilityTiers:
    def test_l1_no_scores(self):
        from src.guidance.explainability_tiers import explain

        c = explain("career", -1.5, "L1")
        assert c.l2 is None
        assert c.l3 is None
        assert c.l1.signal_bars in range(0, 6)

    def test_l2_has_factors(self):
        from src.guidance.explainability_tiers import explain

        c = explain(
            "career",
            2.0,
            "L2",
            promise_strength="Strong",
            timing="Now",
            active_dasha="Jupiter",
            dasha_activated=True,
        )
        assert c.l2 is not None
        assert len(c.l2.factors) >= 1

    def test_l3_has_technical(self):
        from src.guidance.explainability_tiers import explain

        c = explain(
            "career",
            2.0,
            "L3",
            lpi_data={"D1": 2.0},
            rules_fired=["R04", "R02"],
            confidence_data={"va": 0.8},
        )
        assert c.l3 is not None
        assert c.l3.raw_d1_score == 2.0

    def test_heading_no_raw_score(self):
        from src.guidance.explainability_tiers import explain

        c = explain("wealth", -2.5, "L1")
        assert "-2.5" not in c.l1.heading
        assert "2.5" not in c.l1.heading


class TestDisclaimerEngine:
    def test_career_disclaimer(self):
        from src.guidance.disclaimer_engine import get_disclaimer

        d = get_disclaimer("career")
        assert "not financial" in d.lower() or "not career advice" in d.lower()

    def test_health_disclaimer(self):
        from src.guidance.disclaimer_engine import get_disclaimer

        d = get_disclaimer("health_longevity")
        assert "medical" in d.lower()

    def test_default_disclaimer(self):
        from src.guidance.disclaimer_engine import get_disclaimer

        d = get_disclaimer("unknown_domain")
        assert "professional advice" in d.lower() or "not professional" in d.lower()

    def test_dependency_nudge_trigger(self):
        from src.guidance.disclaimer_engine import should_show_dependency_nudge

        assert should_show_dependency_nudge(3, 5)
        assert should_show_dependency_nudge(1, 15)
        assert not should_show_dependency_nudge(1, 5)
