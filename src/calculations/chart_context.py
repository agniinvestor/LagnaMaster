"""
src/calculations/chart_context.py
==================================
ChartContext — compute all derived facts ONCE, share with ALL downstream.

Architecture gap G1 + quality criterion Q1 (5-tier ordering).

Tier 1: Positions + Conventions (from BirthChart)
Tier 2: Lordships, House classification (from Tier 1)
Tier 3: Aspects, Conjunction, Combustion, Friendship (from Tiers 1-2)
Tier 4: Dignity, Avasthas (from Tiers 1-3)
Tier 5: Shadbala, Functional roles, Bhava Bala (from Tiers 1-4)

Every downstream module accepts optional ``ctx=`` parameter.
If provided, uses pre-computed values.  If not, computes locally (zero breaking changes).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from src.ephemeris import BirthChart
from src.calculations.house_lord import HouseMap, compute_house_map
from src.calculations.dignity import DignityResult, compute_all_dignities
from src.calculations.functional_roles import FunctionalRoles, compute_functional_roles
from src.calculations.functional_dignity import (
    FunctionalClassification,
    compute_functional_classifications,
)
from src.calculations.ashtakavarga import AshtakavargaChart, compute_ashtakavarga
from src.calculations.avastha_v2 import AvasthaReportV2, compute_avasthas_v2
from src.calculations.shadbala import ShadbalResult, compute_all_shadbala
from src.calculations.varga import VargaChart, compute_varga
from src.calculations.panchadha_maitri import PanchadhaMatrix, compute_panchadha_matrix
from src.calculations.vimshottari_dasa import MahaDasha, compute_vimshottari_dasa

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G1+Q1", "session": "S328"}


# ---------------------------------------------------------------------------
# Tier result containers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Tier1Positions:
    """Raw positional data extracted from BirthChart for convenience."""

    lagna_sign_index: int
    planet_longitudes: dict[str, float]
    planet_sign_indices: dict[str, int]
    planet_retrograde: dict[str, bool]
    planet_speeds: dict[str, float]


@dataclass(frozen=True)
class Tier2Lordships:
    """House-sign-lord mapping (whole-sign)."""

    house_map: HouseMap


@dataclass(frozen=True)
class Tier3Relations:
    """Aspects, combustion (embedded in dignity), and friendship."""

    panchadha_matrix: PanchadhaMatrix


@dataclass(frozen=True)
class Tier4Dignity:
    """Dignity and avasthas for all planets."""

    dignities: dict[str, DignityResult]
    avasthas: AvasthaReportV2


@dataclass(frozen=True)
class Tier5Strengths:
    """Shadbala, functional roles, ashtakavarga."""

    shadbala: dict[str, ShadbalResult]
    functional_roles: FunctionalRoles
    functional_classifications: dict[str, FunctionalClassification]
    ashtakavarga: AshtakavargaChart
    vargas: VargaChart


# ---------------------------------------------------------------------------
# ChartContext — the single derived-facts object
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChartContext:
    """All derived facts for a chart, computed once, shared by all downstream.

    Fields are organised by tier.  Each tier depends only on lower tiers.
    Access via ``ctx.house_map``, ``ctx.dignities``, etc. for convenience.
    """

    # The source chart (Tier 0)
    chart: BirthChart

    # Tier 1
    tier1: Tier1Positions

    # Tier 2
    tier2: Tier2Lordships

    # Tier 3
    tier3: Tier3Relations

    # Tier 4
    tier4: Tier4Dignity

    # Tier 5
    tier5: Tier5Strengths

    # Optional temporal data (requires birth_date)
    dashas: Optional[list[MahaDasha]] = field(default=None)

    # ---- Convenience accessors (flat access, no tier prefix needed) ----

    @property
    def house_map(self) -> HouseMap:
        return self.tier2.house_map

    @property
    def dignities(self) -> dict[str, DignityResult]:
        return self.tier4.dignities

    @property
    def avasthas(self) -> AvasthaReportV2:
        return self.tier4.avasthas

    @property
    def functional_roles(self) -> FunctionalRoles:
        return self.tier5.functional_roles

    @property
    def functional_classifications(self) -> dict[str, FunctionalClassification]:
        return self.tier5.functional_classifications

    @property
    def ashtakavarga(self) -> AshtakavargaChart:
        return self.tier5.ashtakavarga

    @property
    def shadbala(self) -> dict[str, ShadbalResult]:
        return self.tier5.shadbala

    @property
    def vargas(self) -> VargaChart:
        return self.tier5.vargas

    @property
    def panchadha_matrix(self) -> PanchadhaMatrix:
        return self.tier3.panchadha_matrix


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_chart_context(
    chart: BirthChart,
    *,
    birth_date: Optional[date] = None,
) -> ChartContext:
    """Build a ChartContext in strict tier order.

    Parameters
    ----------
    chart : BirthChart
        The computed birth chart from the ephemeris layer.
    birth_date : date, optional
        Calendar birth date.  Required for dasha computation.

    Returns
    -------
    ChartContext with all derived facts pre-computed.
    """
    # ── Tier 1: positions (extract from BirthChart) ─────────────────────
    tier1 = Tier1Positions(
        lagna_sign_index=chart.lagna_sign_index,
        planet_longitudes={n: p.longitude for n, p in chart.planets.items()},
        planet_sign_indices={n: p.sign_index for n, p in chart.planets.items()},
        planet_retrograde={n: p.is_retrograde for n, p in chart.planets.items()},
        planet_speeds={n: p.speed for n, p in chart.planets.items()},
    )

    # ── Tier 2: lordships / house map ───────────────────────────────────
    house_map = compute_house_map(chart)
    tier2 = Tier2Lordships(house_map=house_map)

    # ── Tier 3: relations (friendship — combustion is part of dignity) ──
    panchadha = compute_panchadha_matrix(chart)
    tier3 = Tier3Relations(panchadha_matrix=panchadha)

    # ── Tier 4: dignity + avasthas ──────────────────────────────────────
    dignities = compute_all_dignities(chart)
    avasthas = compute_avasthas_v2(chart)
    tier4 = Tier4Dignity(dignities=dignities, avasthas=avasthas)

    # ── Tier 5: shadbala, functional roles, AV, vargas ──────────────────
    shadbala = compute_all_shadbala(chart)
    func_roles = compute_functional_roles(chart)
    func_cls = compute_functional_classifications(chart.lagna_sign_index)
    av = compute_ashtakavarga(chart)
    vargas = compute_varga(chart)
    tier5 = Tier5Strengths(
        shadbala=shadbala,
        functional_roles=func_roles,
        functional_classifications=func_cls,
        ashtakavarga=av,
        vargas=vargas,
    )

    # ── Optional: dashas ────────────────────────────────────────────────
    dashas = None
    if birth_date is not None:
        dashas = compute_vimshottari_dasa(chart, birth_date)

    return ChartContext(
        chart=chart,
        tier1=tier1,
        tier2=tier2,
        tier3=tier3,
        tier4=tier4,
        tier5=tier5,
        dashas=dashas,
    )
