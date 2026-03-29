"""
src/interfaces/adapters/dasha_engine.py — S192

VimshottariDasaAdapter wraps vimshottari_dasa to implement the DashaEngine Protocol.

Layer II (Structural Convergence — Capacity gate) concrete adapter.
Phase 1 will extend this to support Ashtottari, Yogini, Kalachakra (S361+).
"""

from __future__ import annotations

from datetime import date
from typing import Any


def _birth_date_from_chart(chart: Any) -> date:
    """
    Derive a calendar date from BirthChart.jd_ut (Julian Day, UT).

    BirthChart does not store birth_date directly; it stores jd_ut.
    We reverse the Julian Day back to Gregorian calendar via swisseph.
    """
    import swisseph as swe

    # swe.revjul returns (year, month, day_float, hour_float)
    year, month, day_f, _ = swe.revjul(chart.jd_ut)
    return date(int(year), int(month), int(day_f))


class VimshottariDasaAdapter:
    """
    Concrete implementation of the DashaEngine Protocol.

    Wraps:
      compute_vimshottari_dasa()  — full 120-year MD sequence
      current_dasha()             — MD/AD active on a date
      compute_pratyantar_dasha()  — PD (3rd level) within active AD

    For system='narayana', delegates to narayana_dasa module.
    Other systems (Ashtottari, Yogini, Kalachakra) raise NotImplementedError
    until Phase 1 S361.
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
        chart : BirthChart — must have .jd_ut (Julian Day) and Moon longitude
        system : "vimshottari" | "narayana"

        Returns list[MahaDasha] for vimshottari, list[NarayanaPeriod] for narayana.
        """
        birth_date = _birth_date_from_chart(chart)

        if system == "vimshottari":
            from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

            return compute_vimshottari_dasa(
                chart=chart,
                birth_date=birth_date,
            )
        elif system == "narayana":
            from src.calculations.narayana_dasa import compute_narayana_dasha

            return compute_narayana_dasha(
                lagna_sign_idx=chart.lagna_sign_index,
                birth_date=birth_date,
            )
        else:
            raise NotImplementedError(
                f"Dasha system '{system}' not yet implemented. "
                "Ashtottari, Yogini, Kalachakra planned for Phase 1 S361."
            )

    def active_dasha(
        self,
        chart: Any,
        on_date: Any,
        system: str = "vimshottari",
    ) -> tuple[str, str, str]:
        """
        Return the active (MD lord, AD lord, PD lord) triplet on on_date.

        For narayana, returns (period_sign, "", "") — no AD/PD in narayana.
        """
        if on_date is None:
            on_date = date.today()

        if system == "narayana":
            return self._active_narayana(chart, on_date)

        dashas = self.compute_dashas(chart, system=system)  # type: ignore[arg-type]

        from src.calculations.vimshottari_dasa import current_dasha

        md, ad = current_dasha(dashas, on_date=on_date)

        # Compute PD lord within the active AD
        pd_lord = self._active_pd_lord(md, ad, on_date)

        return (md.lord, ad.lord, pd_lord)

    # ── private helpers ───────────────────────────────────────────────────────

    def _active_pd_lord(self, md: Any, ad: Any, on_date: date) -> str:
        """Return the active Pratyantar Dasha lord within (md, ad) on on_date."""
        try:
            from src.calculations.pratyantar_dasha import compute_pratyantar_dasha

            pds = compute_pratyantar_dasha(md, ad)
            for pd in pds:
                if pd.start <= on_date < pd.end:
                    return pd.lord
            # Fallback: last PD
            if pds:
                return pds[-1].lord
        except Exception:
            pass
        # Graceful fallback if PD computation fails
        return ad.lord

    def _active_narayana(self, chart: Any, on_date: date) -> tuple[str, str, str]:
        from src.calculations.narayana_dasa import active_narayana_period

        period = active_narayana_period(
            lagna_sign_idx=chart.lagna_sign_index,
            birth_date=_birth_date_from_chart(chart),
            query_date=on_date,
        )
        if period is None:
            return ("", "", "")
        return (period.sign, "", "")
