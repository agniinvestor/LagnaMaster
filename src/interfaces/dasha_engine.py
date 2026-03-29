"""
src/interfaces/dasha_engine.py — S191 Protocol stub

DashaEngine defines the boundary between the timing/dasha layer
and consumers (API, promise_engine, future temporal microservice).

Layer II (Structural Convergence — Capacity gate) interface.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DashaEngine(Protocol):
    """
    Computes Vimshottari and other dasha periods for a birth chart.

    Implementations: vimshottari_dasa, narayana_dasa wrappers.
    Phase 1 will add Ashtottari, Yogini, Kalachakra (S361+).
    """

    def compute_dashas(
        self,
        chart: Any,
        system: str = "vimshottari",
    ) -> list[Any]:
        """
        Compute the full dasha sequence for a chart.

        Parameters
        ----------
        chart : BirthChart
            Birth chart with Moon longitude for nakshatra-based systems.
        system : str
            Dasha system — "vimshottari" (default) | "narayana" | future systems.

        Returns
        -------
        list[MahaDasha]
            Ordered list of mahadashas with antardasha sub-periods.
        """
        ...

    def active_dasha(
        self,
        chart: Any,
        on_date: Any,
        system: str = "vimshottari",
    ) -> Any:
        """
        Return the active MD/AD/PD triplet on a given date.

        Returns
        -------
        tuple[str, str, str]
            (mahadasha_lord, antardasha_lord, pratyantar_lord)
        """
        ...
