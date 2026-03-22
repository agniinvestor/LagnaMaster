"""tests/test_phase14.py — Phase 14: Maturity Features (S87–90)"""

from __future__ import annotations
import pytest

INDIA = dict(
    year=1947,
    month=8,
    day=15,
    hour=0.0,
    lat=28.6139,
    lon=77.2090,
    tz_offset=5.5,
    ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA)


class TestEducationalLayer:
    def test_explain_factor(self):
        from src.guidance.educational_layer import explain_factor

        e = explain_factor("Jupiter_kendra")
        assert e is not None
        assert "Jupiter" in e.plain_explanation
        assert e.classical_source

    def test_unknown_factor_none(self):
        from src.guidance.educational_layer import explain_factor

        assert explain_factor("nonexistent_factor") is None

    def test_available_topics(self):
        from src.guidance.educational_layer import available_topics

        topics = available_topics()
        assert len(topics) >= 4

    def test_domain_content(self):
        from src.guidance.educational_layer import get_educational_content

        content = get_educational_content("career")
        assert len(content) >= 1
        for c in content:
            assert c.plain_explanation
            assert c.classical_source

    def test_no_raw_scores_in_explanations(self):
        from src.guidance.educational_layer import available_topics, explain_factor

        for t in available_topics():
            e = explain_factor(t)
            if e:
                assert not any(
                    c.isdigit() and c in "-+1234567890"
                    for c in e.plain_explanation
                    if e.plain_explanation.count(c) > 3
                ), f"Topic {t} may contain raw numbers"


class TestReflectionPrompts:
    def test_returns_prompt(self):
        from src.guidance.reflection_prompts import get_reflection_prompt

        p = get_reflection_prompt("career", "Clear passage")
        assert isinstance(p, str) and len(p) > 10
        assert "?" in p  # Socratic — must be a question

    def test_all_domains(self):
        from src.guidance.reflection_prompts import get_reflection_prompt

        for domain in [
            "career",
            "marriage",
            "wealth",
            "mind_psychology",
            "spirituality",
            "default",
        ]:
            p = get_reflection_prompt(domain, "Neutral")
            assert isinstance(p, str) and len(p) > 5

    def test_no_predictions(self):
        from src.guidance.reflection_prompts import get_all_prompts

        for domain in ["career", "marriage"]:
            for p in get_all_prompts(domain):
                assert "will happen" not in p.lower()
                assert "is certain" not in p.lower()


class TestPractitionerHandoff:
    def test_should_recommend(self):
        from src.guidance.practitioner_handoff import should_recommend_practitioner

        assert should_recommend_practitioner(True, 0, 3)
        assert should_recommend_practitioner(False, 1, 0)
        assert should_recommend_practitioner(False, 0, 4)
        assert not should_recommend_practitioner(False, 0, 2)

    def test_build_summary(self, chart):
        from src.guidance.practitioner_handoff import build_chart_summary

        s = build_chart_summary(chart)
        assert s.lagna in [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]
        assert "LagnaMaster" in s.practitioner_note
        assert "supersedes" in s.practitioner_note

    def test_summary_no_raw_scores(self, chart):
        from src.guidance.practitioner_handoff import build_chart_summary

        s = build_chart_summary(chart)
        # Ensure no numeric scores in notable features
        for feat in s.notable_features:
            assert not any(c in feat for c in ["-5.25", "-4.2", "3.0"])


class TestMobileRouter:
    def test_score_to_language_imports(self):
        from src.guidance.score_to_language import score_to_signal

        s = score_to_signal(1.0)
        assert s.bars in range(0, 6)

    def test_disclaimer_for_mobile(self):
        from src.guidance.disclaimer_engine import get_disclaimer

        d = get_disclaimer("career")
        assert len(d) > 20
