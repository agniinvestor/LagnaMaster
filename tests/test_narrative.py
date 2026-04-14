"""Tests for narrative synthesis layer (G7)."""

from __future__ import annotations


import pytest

from src.calculations.narrative import (
    NarrativeReport,
    LifePhase,
    AbsenceEntry,
    DomainNarrative,
)
from src.pipeline import run_pipeline, PipelineResult


@pytest.fixture
def pipeline_1985() -> PipelineResult:
    return run_pipeline(
        year=1985, month=3, day=15, hour=10.5,
        lat=28.61, lon=77.21, tz_offset=5.5,
    )


@pytest.fixture
def pipeline_1770() -> PipelineResult:
    """Beethoven — different lagna, era, latitude."""
    return run_pipeline(
        year=1770, month=12, day=17, hour=1.0,
        lat=50.73, lon=7.1, tz_offset=1.0,
    )


class TestNarrativeReportStructure:
    def test_returns_narrative_report(self, pipeline_1985):
        assert isinstance(pipeline_1985.narrative, NarrativeReport)

    def test_has_life_phases(self, pipeline_1985):
        assert len(pipeline_1985.narrative.life_phases) == 9  # 9 mahadashas

    def test_life_phases_are_typed(self, pipeline_1985):
        for phase in pipeline_1985.narrative.life_phases:
            assert isinstance(phase, LifePhase)
            assert phase.lord
            assert phase.label
            assert phase.start_year > 0
            assert phase.end_year >= phase.start_year
            assert phase.dominant_direction in ("favorable", "unfavorable", "mixed")

    def test_has_overall_arc(self, pipeline_1985):
        assert pipeline_1985.narrative.overall_arc
        assert isinstance(pipeline_1985.narrative.overall_arc, str)

    def test_has_domain_narratives(self, pipeline_1985):
        dn = pipeline_1985.narrative.per_domain_narratives
        assert "career" in dn
        assert "family" in dn
        assert "health" in dn
        assert "spiritual" in dn
        for name, narrative in dn.items():
            assert isinstance(narrative, DomainNarrative)
            assert narrative.overall_direction in ("favorable", "unfavorable", "mixed")

    def test_absence_analysis(self, pipeline_1985):
        for ab in pipeline_1985.narrative.absence_analysis:
            assert isinstance(ab, AbsenceEntry)
            assert 1 <= ab.house <= 12
            assert ab.domain
            assert ab.meaning

    def test_lagna_sign_populated(self, pipeline_1985):
        assert pipeline_1985.narrative.lagna_sign == "Taurus"


class TestLifePhaseContent:
    def test_phases_cover_dasha_sequence(self, pipeline_1985):
        lords = [p.lord for p in pipeline_1985.narrative.life_phases]
        # Should match the dasha sequence from the chart
        assert len(lords) == 9

    def test_phases_have_domain_summaries(self, pipeline_1985):
        active_phases = [p for p in pipeline_1985.narrative.life_phases if p.activated_houses]
        assert len(active_phases) > 0
        for phase in active_phases:
            assert len(phase.domain_summaries) > 0

    def test_domain_summaries_have_houses(self, pipeline_1985):
        for phase in pipeline_1985.narrative.life_phases:
            for ds in phase.domain_summaries:
                assert all(1 <= h <= 12 for h in ds.houses)


class TestDifferentCharts:
    def test_different_lagna_produces_report(self, pipeline_1770):
        assert pipeline_1770.narrative.lagna_sign == "Virgo"
        assert len(pipeline_1770.narrative.life_phases) == 9

    def test_arcs_can_differ(self, pipeline_1985, pipeline_1770):
        # Different charts should produce reports (may or may not have same arc)
        assert isinstance(pipeline_1985.narrative.overall_arc, str)
        assert isinstance(pipeline_1770.narrative.overall_arc, str)


class TestDeterminism:
    def test_two_runs_identical(self, pipeline_1985):
        r2 = run_pipeline(year=1985, month=3, day=15, hour=10.5,
                          lat=28.61, lon=77.21, tz_offset=5.5)
        n1 = pipeline_1985.narrative
        n2 = r2.narrative
        assert n1.overall_arc == n2.overall_arc
        assert len(n1.life_phases) == len(n2.life_phases)
        for a, b in zip(n1.life_phases, n2.life_phases):
            assert a.lord == b.lord
            assert a.dominant_direction == b.dominant_direction
            assert a.activated_houses == b.activated_houses
