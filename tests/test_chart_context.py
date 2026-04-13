"""Tests for ChartContext (G1+Q1) — 5-tier derived facts computation."""

from __future__ import annotations

import time
from datetime import date

import pytest

from src.ephemeris import compute_chart, BirthChart
from src.calculations.chart_context import (
    ChartContext,
    Tier1Positions,
    Tier2Lordships,
    Tier3Relations,
    Tier4Dignity,
    Tier5Strengths,
    build_chart_context,
)
from src.calculations.house_lord import compute_house_map
from src.calculations.dignity import compute_all_dignities
from src.calculations.functional_roles import compute_functional_roles
from src.calculations.ashtakavarga import compute_ashtakavarga
from src.calculations.avastha_v2 import compute_avasthas_v2
from src.calculations.shadbala import compute_all_shadbala
from src.calculations.varga import compute_varga
from src.calculations.panchadha_maitri import compute_panchadha_matrix
from src.calculations.vimshottari_dasa import compute_vimshottari_dasa


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def india_1947_chart() -> BirthChart:
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


@pytest.fixture
def india_1947_ctx(india_1947_chart: BirthChart) -> ChartContext:
    return build_chart_context(india_1947_chart, birth_date=date(1947, 8, 15))


# ---------------------------------------------------------------------------
# Structural tests
# ---------------------------------------------------------------------------

class TestChartContextStructure:
    """Verify ChartContext has correct structure and tier types."""

    def test_returns_chart_context(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx, ChartContext)

    def test_tier1_is_positions(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx.tier1, Tier1Positions)

    def test_tier2_is_lordships(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx.tier2, Tier2Lordships)

    def test_tier3_is_relations(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx.tier3, Tier3Relations)

    def test_tier4_is_dignity(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx.tier4, Tier4Dignity)

    def test_tier5_is_strengths(self, india_1947_ctx: ChartContext):
        assert isinstance(india_1947_ctx.tier5, Tier5Strengths)

    def test_frozen_dataclass(self, india_1947_ctx: ChartContext):
        with pytest.raises(AttributeError):
            india_1947_ctx.tier1 = None  # type: ignore[misc]

    def test_chart_reference_preserved(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        assert india_1947_ctx.chart is india_1947_chart


# ---------------------------------------------------------------------------
# Tier 1: Positions
# ---------------------------------------------------------------------------

class TestTier1Positions:
    def test_lagna_sign_index(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        assert india_1947_ctx.tier1.lagna_sign_index == india_1947_chart.lagna_sign_index

    def test_all_planets_have_longitude(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        for name, pos in india_1947_chart.planets.items():
            assert india_1947_ctx.tier1.planet_longitudes[name] == pos.longitude

    def test_all_planets_have_sign_index(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        for name, pos in india_1947_chart.planets.items():
            assert india_1947_ctx.tier1.planet_sign_indices[name] == pos.sign_index

    def test_all_planets_have_retrograde(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        for name, pos in india_1947_chart.planets.items():
            assert india_1947_ctx.tier1.planet_retrograde[name] == pos.is_retrograde


# ---------------------------------------------------------------------------
# Tier 2: Lordships / House Map
# ---------------------------------------------------------------------------

class TestTier2Lordships:
    def test_house_map_matches_direct_computation(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_house_map(india_1947_chart)
        ctx_hm = india_1947_ctx.house_map
        assert ctx_hm.lagna_sign_idx == direct.lagna_sign_idx
        assert ctx_hm.house_sign == direct.house_sign
        assert ctx_hm.house_lord == direct.house_lord
        assert ctx_hm.planet_house == direct.planet_house

    def test_convenience_accessor(self, india_1947_ctx: ChartContext):
        assert india_1947_ctx.house_map is india_1947_ctx.tier2.house_map


# ---------------------------------------------------------------------------
# Tier 3: Relations
# ---------------------------------------------------------------------------

class TestTier3Relations:
    def test_panchadha_matrix_matches(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_panchadha_matrix(india_1947_chart)
        ctx_pm = india_1947_ctx.panchadha_matrix
        assert ctx_pm.planets == direct.planets
        assert ctx_pm.relations == direct.relations

    def test_convenience_accessor(self, india_1947_ctx: ChartContext):
        assert india_1947_ctx.panchadha_matrix is india_1947_ctx.tier3.panchadha_matrix


# ---------------------------------------------------------------------------
# Tier 4: Dignity + Avasthas
# ---------------------------------------------------------------------------

class TestTier4Dignity:
    def test_dignities_match_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_all_dignities(india_1947_chart)
        for planet, dig in direct.items():
            ctx_dig = india_1947_ctx.dignities[planet]
            assert ctx_dig.dignity == dig.dignity
            assert ctx_dig.combust == dig.combust
            assert ctx_dig.uchcha_bala == pytest.approx(dig.uchcha_bala, abs=1e-6)

    def test_avasthas_match_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_avasthas_v2(india_1947_chart)
        for planet, av in direct.planets.items():
            ctx_av = india_1947_ctx.avasthas.planets[planet]
            assert ctx_av.baaladi_state == av.baaladi_state
            assert ctx_av.combined_modifier == pytest.approx(av.combined_modifier, abs=1e-6)

    def test_convenience_accessors(self, india_1947_ctx: ChartContext):
        assert india_1947_ctx.dignities is india_1947_ctx.tier4.dignities
        assert india_1947_ctx.avasthas is india_1947_ctx.tier4.avasthas


# ---------------------------------------------------------------------------
# Tier 5: Shadbala, Func Roles, AV, Vargas
# ---------------------------------------------------------------------------

class TestTier5Strengths:
    def test_shadbala_matches_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_all_shadbala(india_1947_chart)
        for planet, sb in direct.items():
            ctx_sb = india_1947_ctx.shadbala[planet]
            assert ctx_sb.total == pytest.approx(sb.total, abs=1e-4)

    def test_functional_roles_match_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_functional_roles(india_1947_chart)
        ctx_fr = india_1947_ctx.functional_roles
        assert ctx_fr.functional_benefics == direct.functional_benefics
        assert ctx_fr.functional_malefics == direct.functional_malefics
        assert ctx_fr.yogakaraka == direct.yogakaraka

    def test_ashtakavarga_matches_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_ashtakavarga(india_1947_chart)
        assert india_1947_ctx.ashtakavarga.sarva.total == direct.sarva.total

    def test_vargas_matches_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_varga(india_1947_chart)
        for key in direct.tables:
            ctx_table = india_1947_ctx.vargas.tables[key]
            direct_table = direct.tables[key]
            assert ctx_table.lagna_sign_index == direct_table.lagna_sign_index

    def test_convenience_accessors(self, india_1947_ctx: ChartContext):
        assert india_1947_ctx.shadbala is india_1947_ctx.tier5.shadbala
        assert india_1947_ctx.functional_roles is india_1947_ctx.tier5.functional_roles
        assert india_1947_ctx.ashtakavarga is india_1947_ctx.tier5.ashtakavarga
        assert india_1947_ctx.vargas is india_1947_ctx.tier5.vargas


# ---------------------------------------------------------------------------
# Dashas (optional temporal)
# ---------------------------------------------------------------------------

class TestDashas:
    def test_dashas_computed_with_birth_date(self, india_1947_ctx: ChartContext):
        assert india_1947_ctx.dashas is not None
        assert len(india_1947_ctx.dashas) == 9

    def test_dashas_none_without_birth_date(self, india_1947_chart: BirthChart):
        ctx = build_chart_context(india_1947_chart)
        assert ctx.dashas is None

    def test_dashas_match_direct(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        direct = compute_vimshottari_dasa(india_1947_chart, date(1947, 8, 15))
        for i, md in enumerate(direct):
            assert india_1947_ctx.dashas[i].lord == md.lord


# ---------------------------------------------------------------------------
# Performance (Q9 partial)
# ---------------------------------------------------------------------------

class TestPerformance:
    def test_build_under_200ms(self, india_1947_chart: BirthChart):
        """Q9: Single chart computation < 200ms."""
        # Warm up
        build_chart_context(india_1947_chart, birth_date=date(1947, 8, 15))

        times = []
        for _ in range(5):
            start = time.perf_counter()
            build_chart_context(india_1947_chart, birth_date=date(1947, 8, 15))
            times.append((time.perf_counter() - start) * 1000)

        median = sorted(times)[2]
        assert median < 200.0, f"Median build time {median:.1f}ms exceeds 200ms target"


# ---------------------------------------------------------------------------
# Invariant checks (Q7 partial)
# ---------------------------------------------------------------------------

class TestInvariants:
    def test_every_planet_in_one_sign(self, india_1947_ctx: ChartContext):
        """INV-1: Every planet sign_index in [0, 11]."""
        for planet, si in india_1947_ctx.tier1.planet_sign_indices.items():
            assert 0 <= si <= 11, f"{planet} sign_index={si}"

    def test_every_planet_in_one_house(self, india_1947_ctx: ChartContext):
        """INV: Every planet has house in [1, 12]."""
        for planet, house in india_1947_ctx.house_map.planet_house.items():
            assert 1 <= house <= 12, f"{planet} house={house}"

    def test_every_house_has_one_lord(self, india_1947_ctx: ChartContext):
        """INV-2: Each house has exactly one lord."""
        assert len(india_1947_ctx.house_map.house_lord) == 12
        for i, lord in enumerate(india_1947_ctx.house_map.house_lord):
            assert lord in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"), \
                f"House {i+1} lord={lord}"

    def test_dignity_levels_valid(self, india_1947_ctx: ChartContext):
        """INV-3: Dignity levels are valid DignityLevel enum members."""
        from src.calculations.dignity import DignityLevel

        valid_members = set(DignityLevel)
        for planet, dig in india_1947_ctx.dignities.items():
            assert dig.dignity in valid_members, f"{planet} dignity={dig.dignity}"

    def test_shadbala_non_negative(self, india_1947_ctx: ChartContext):
        """Shadbala total should be non-negative."""
        for planet, sb in india_1947_ctx.shadbala.items():
            assert sb.total >= 0, f"{planet} shadbala total={sb.total}"

    def test_lagna_sign_consistent(self, india_1947_ctx: ChartContext):
        """Lagna sign index from Tier 1 matches house map."""
        assert india_1947_ctx.tier1.lagna_sign_index == india_1947_ctx.house_map.lagna_sign_idx


# ---------------------------------------------------------------------------
# Determinism (Q10 partial)
# ---------------------------------------------------------------------------

class TestDeterminism:
    def test_two_builds_identical(self, india_1947_chart: BirthChart):
        """Q10: Same chart → same context."""
        bd = date(1947, 8, 15)
        ctx1 = build_chart_context(india_1947_chart, birth_date=bd)
        ctx2 = build_chart_context(india_1947_chart, birth_date=bd)

        # Tier 1
        assert ctx1.tier1.planet_longitudes == ctx2.tier1.planet_longitudes
        # Tier 2
        assert ctx1.house_map.house_sign == ctx2.house_map.house_sign
        assert ctx1.house_map.planet_house == ctx2.house_map.planet_house
        # Tier 4
        for p in ctx1.dignities:
            assert ctx1.dignities[p].dignity == ctx2.dignities[p].dignity
            assert ctx1.dignities[p].uchcha_bala == ctx2.dignities[p].uchcha_bala
        # Tier 5
        for p in ctx1.shadbala:
            assert ctx1.shadbala[p].total == ctx2.shadbala[p].total


# ---------------------------------------------------------------------------
# ctx= pass-through: scoring and rule_firing produce same results
# ---------------------------------------------------------------------------

class TestCtxPassthrough:
    """Verify that ctx= produces identical results to computing without ctx."""

    def test_score_chart_with_ctx(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        from src.scoring import score_chart

        without_ctx = score_chart(india_1947_chart)
        with_ctx = score_chart(india_1947_chart, ctx=india_1947_ctx)

        for h in range(1, 13):
            assert with_ctx.houses[h].final_score == pytest.approx(
                without_ctx.houses[h].final_score, abs=1e-6,
            ), f"House {h} score mismatch with ctx="

    def test_score_axis_with_ctx(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        from src.calculations.multi_axis_scoring import score_axis

        without_ctx = score_axis(india_1947_chart, india_1947_chart.lagna_sign_index, "D1")
        with_ctx = score_axis(india_1947_chart, india_1947_chart.lagna_sign_index, "D1", ctx=india_1947_ctx)

        for h in range(1, 13):
            assert with_ctx.scores[h] == pytest.approx(
                without_ctx.scores[h], abs=1e-6,
            ), f"House {h} axis score mismatch with ctx="

    def test_evaluate_chart_with_ctx(self, india_1947_chart: BirthChart, india_1947_ctx: ChartContext):
        from src.calculations.rule_firing import evaluate_chart

        without_ctx = evaluate_chart(india_1947_chart)
        with_ctx = evaluate_chart(india_1947_chart, ctx=india_1947_ctx)

        assert with_ctx.total_fired == without_ctx.total_fired
        without_ids = {r.rule_id for r in without_ctx.fired_rules}
        with_ids = {r.rule_id for r in with_ctx.fired_rules}
        assert with_ids == without_ids
